"""Behavioral tests for demo resource ownership and real video finalization."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def demo():
    path = Path(__file__).resolve().parents[2] / "docker/novnc/demos/demo_desktop_gui.py"
    spec = importlib.util.spec_from_file_location("novnc_demo", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def session(demo, monkeypatch, tmp_path):
    events = []
    logger = MagicMock()
    logger.end.return_value = tmp_path / "session.md"
    logger.end.side_effect = lambda **kw: events.append("log") or tmp_path / "session.md"
    monkeypatch.setitem(sys.modules, "nlp2cmd.cli.session_logger", SimpleNamespace(SessionLogger=lambda *a, **kw: logger))
    page = MagicMock()
    path = tmp_path / "unique.webm"
    def video_path():
        assert "context" in events
        events.append("video")
        return str(path)
    page.video.path.side_effect = video_path
    context = MagicMock()
    context.new_page.return_value = page
    def close_context():
        events.append("context")
        path.write_bytes(b"recorded frames")
    context.close.side_effect = close_context
    browser = MagicMock()
    browser.new_context.return_value = context
    browser.close.side_effect = lambda: events.append("browser")
    playwright = MagicMock()
    playwright.chromium.launch.return_value = browser
    manager = MagicMock()
    manager.__enter__.return_value = playwright
    monkeypatch.setitem(sys.modules, "playwright", SimpleNamespace())
    monkeypatch.setitem(sys.modules, "playwright.sync_api", SimpleNamespace(sync_playwright=lambda: manager))
    monkeypatch.setattr(demo, "_run_desktop_steps", MagicMock())
    monkeypatch.setattr(demo.time, "sleep", lambda _: None)
    return SimpleNamespace(page=page, context=context, browser=browser, playwright=playwright,
                           events=events, logger=logger, path=path, directory=tmp_path)


def test_record_remote_page_and_finalize_in_order(demo, session):
    path = demo.run_demo(record=True, headless=True, novnc_url="http://remote:6089/", output_dir=session.directory)
    assert path == session.path
    assert session.events == ["context", "video", "browser", "log"]
    session.page.goto.assert_called_once_with("http://remote:6089/vnc.html?autoconnect=true", wait_until="load", timeout=8000)
    options = session.browser.new_context.call_args.kwargs
    assert options["record_video_dir"] == str(session.directory)
    assert options["record_video_size"] == options["viewport"]
    assert session.logger.end.call_args.kwargs["summary"]["Status"] == "completed"


@pytest.mark.parametrize("failure", ["launch", "context", "page", "connect", "ready", "canvas", "steps", "close", "video"])
def test_failures_finalize_only_acquired_resources(demo, session, failure):
    error = RuntimeError("broken " + failure)
    operations = {"launch": session.playwright.chromium.launch,
                  "context": session.browser.new_context, "page": session.context.new_page,
                  "connect": session.page.goto, "ready": session.page.wait_for_function,
                  "canvas": session.page.wait_for_selector,
                  "steps": demo._run_desktop_steps, "close": session.context.close,
                  "video": session.page.video.path}
    operations[failure].side_effect = error
    with pytest.raises(RuntimeError):
        demo.run_demo(record=True, output_dir=session.directory)
    assert session.browser.close.call_count == (0 if failure == "launch" else 1)
    assert session.context.close.call_count == (0 if failure in {"launch", "context"} else 1)
    session.logger.end.assert_called_once()
    assert session.logger.end.call_args.kwargs["summary"]["Status"] == "failed"
    if failure in {"canvas", "steps"}:
        assert session.path.is_file(), "Keep the partial recording on an interaction failure"


def test_missing_video_is_failure(demo, session):
    session.context.close.side_effect = lambda: session.events.append("context")
    with pytest.raises(RuntimeError, match="nonempty"):
        demo.run_demo(record=True, output_dir=session.directory)
    session.browser.close.assert_called_once()
    assert session.logger.end.call_args.kwargs["summary"]["Status"] == "failed"


def test_recording_disabled_does_not_access_video(demo, session):
    assert demo.run_demo(record=False, output_dir=session.directory) is None
    assert "record_video_dir" not in session.browser.new_context.call_args.kwargs
    session.page.video.path.assert_not_called()


def test_cli_failure_returns_nonzero(demo, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["demo_desktop_gui.py", "--record"])
    monkeypatch.setattr(demo, "ensure_playwright", lambda: True)
    monkeypatch.setattr(demo, "run_demo", MagicMock(side_effect=RuntimeError("failed")))
    assert demo.main() == 1



def test_repeated_runs_preserve_session_reports(demo, session, monkeypatch):
    path = Path(__file__).resolve().parents[2] / "src/nlp2cmd/cli/session_logger.py"
    spec = importlib.util.spec_from_file_location("real_session_logger", path)
    logger_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(logger_module)
    monkeypatch.setitem(sys.modules, "nlp2cmd.cli.session_logger", logger_module)
    session.page.screenshot.return_value = None

    demo.run_demo(output_dir=session.directory)
    first_report = next(session.directory.glob("*.md"))
    original = first_report.read_bytes()
    demo.run_demo(output_dir=session.directory)

    assert len(list(session.directory.glob("*.md"))) == 2
    assert first_report.read_bytes() == original
    assert len(list(session.directory.glob("*_screenshots"))) == 2


@pytest.mark.e2e
def test_full_desktop_demo_in_disposable_container(demo, tmp_path):
    """Run with NLP2CMD_NOVNC_TEST_IMAGE=<built image> and pytest -m e2e.

    Creates its own desktop with no host mounts and a dynamically allocated
    loopback port. Requires Docker, Playwright/Chromium, FFmpeg and Tesseract.
    The normal unit/CI suite excludes e2e tests via pytest.ini.
    """
    image = os.environ.get("NLP2CMD_NOVNC_TEST_IMAGE")
    assert image, "Set NLP2CMD_NOVNC_TEST_IMAGE to a built docker/novnc image"
    for binary in ("docker", "ffprobe", "tesseract"):
        assert shutil.which(binary), f"The noVNC e2e test requires {binary}"

    def command(*args):
        return subprocess.run(args, check=True, capture_output=True, text=True,
                              timeout=30).stdout

    container = command(
        "docker", "run", "--pull=never", "-d", "--memory", "2g", "--cpus", "2",
        "--shm-size", "512m", "-p", "127.0.0.1::6080", image,
    ).strip()
    try:
        port = command("docker", "port", container, "6080/tcp").strip().split(":")[-1]
        legacy_path = "/home/nlp2cmd/nlp2cmd_report.txt"
        legacy_document = "Existing presentation: preserve this document."
        subprocess.run(["docker", "exec", "-i", container, "tee", legacy_path],
                       input=legacy_document, text=True, capture_output=True,
                       check=True, timeout=30)
        previous_documents, previous_screenshots, videos = set(), set(), set()
        previous_artifacts, verifications = {}, []
        previous_document_path, previous_document = None, None
        for run in range(2):
            video = demo.run_demo(record=True, headless=True,
                                  novnc_url=f"http://127.0.0.1:{port}", output_dir=tmp_path)
            documents = set(command("docker", "exec", container, "find", "/home/nlp2cmd",
                                    "-maxdepth", "1", "-name", "nlp2cmd_report_*.txt").splitlines())
            new_documents = documents - previous_documents
            assert len(new_documents) == 1, "Each run must save its own desktop document"
            document_path = new_documents.pop()
            document = command("docker", "exec", container, "cat", document_path)
            previous_documents = documents
            assert command("docker", "exec", container, "cat", legacy_path) == legacy_document
            if previous_document_path:
                assert command("docker", "exec", container, "cat", previous_document_path) == previous_document
            previous_document_path, previous_document = document_path, document
            assert "NLP2CMD Desktop Automation Report" in document
            assert "This document was created autonomously by NLP2CMD." in document
            assert f"Date: {demo.date.today().isoformat()}" in document
            processes = command("docker", "exec", container, "ps", "-eo", "comm").lower()
            assert all(name in processes for name in ("galculator", "mousepad", "thunar", "firefox"))

            screenshot_dirs = set(tmp_path.glob("desktop_gui_demo_*_screenshots"))
            new_screenshots = screenshot_dirs - previous_screenshots
            assert len(new_screenshots) == 1
            screenshots = new_screenshots.pop()
            previous_screenshots = screenshot_dirs
            calculator = next(screenshots.glob("*entered_calculation*.png"))
            # Desktop screenshots contain separate text regions, not a document page.
            calculator_text = command("tesseract", str(calculator), "stdout", "--psm", "11")
            assert "5754" in re.sub(r"\s|,", "", calculator_text)
            final = next(screenshots.glob("*final_desktop_state.png"))
            browser_text = command("tesseract", str(final), "stdout", "--psm", "11")
            assert "thisdocumentwascreatedautonomouslyby" in re.sub(r"\W", "", browser_text.lower())
            # Firefox can retain its generic window title for a local text file.
            # Verify it is foreground; OCR above independently verifies the content.
            browser_title = command("docker", "exec", container, "xdotool",
                                    "getactivewindow", "getwindowname")
            assert "Mozilla Firefox" in browser_title

            probe = json.loads(command("ffprobe", "-v", "error", "-show_streams",
                                       "-show_format", "-of", "json", str(video)))
            stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
            assert (stream["width"], stream["height"]) == (1280, 800)
            assert float(probe["format"]["duration"]) > 30
            assert video not in videos
            videos.add(video)
            assert len(list(tmp_path.glob("*.md"))) == run + 1
            for artifact, digest in previous_artifacts.items():
                assert hashlib.sha256(artifact.read_bytes()).hexdigest() == digest
            previous_artifacts = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in tmp_path.rglob("*") if p.is_file()}
            verifications.append({"documentPath": document_path,
                "video": str(video), "document": document, "browserTitle": browser_title,
                "calculatorOCR": calculator_text, "browserOCR": browser_text, "probe": probe,
                "image": command("docker", "inspect", "--format", "{{.Image}}", container).strip(),
            })
        (tmp_path / "verification.json").write_text(json.dumps(verifications, indent=2) + "\n")
    finally:
        try:
            logs = subprocess.run(["docker", "logs", container], capture_output=True,
                                  text=True, timeout=15)
            (tmp_path / "container.log").write_text(logs.stdout + logs.stderr)
        finally:
            command("docker", "rm", "-f", container)
