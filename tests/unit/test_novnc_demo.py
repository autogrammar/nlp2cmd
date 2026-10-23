"""Behavioral tests for demo resource ownership and real video finalization."""
import importlib.util
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


@pytest.mark.e2e
def test_full_desktop_demo_in_disposable_container(demo, tmp_path):
    """Run with NLP2CMD_NOVNC_TEST_IMAGE=<built image> and pytest -m e2e.

    Creates its own desktop with no host mounts and a dynamically allocated
    loopback port. Requires Docker, Playwright/Chromium, FFmpeg and Tesseract.
    The normal unit/CI suite excludes e2e tests via pytest.ini.
    """
    image = os.environ.get("NLP2CMD_NOVNC_TEST_IMAGE")
    if not image:
        pytest.skip("Set NLP2CMD_NOVNC_TEST_IMAGE to a built docker/novnc image")
    pytest.importorskip("playwright.sync_api")
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
        video = demo.run_demo(record=True, headless=True,
                              novnc_url=f"http://127.0.0.1:{port}", output_dir=tmp_path)
        document = command("docker", "exec", container, "cat",
                           "/home/nlp2cmd/nlp2cmd_report.txt")
        assert "NLP2CMD Desktop Automation Report" in document
        assert "This document was created autonomously by NLP2CMD." in document
        assert f"Date: {demo.date.today().isoformat()}" in document
        processes = command("docker", "exec", container, "ps", "-eo", "comm").lower()
        assert all(name in processes for name in ("galculator", "mousepad", "thunar", "firefox"))

        screenshots = tmp_path / "desktop_gui_demo_screenshots"
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
        (tmp_path / "verification.json").write_text(json.dumps({
            "video": str(video), "document": document, "browserTitle": browser_title,
            "calculatorOCR": calculator_text, "browserOCR": browser_text, "probe": probe,
            "image": command("docker", "inspect", "--format", "{{.Image}}", container).strip(),
        }, indent=2) + "\n")
    finally:
        try:
            logs = subprocess.run(["docker", "logs", container], capture_output=True,
                                  text=True, timeout=15)
            (tmp_path / "container.log").write_text(logs.stdout + logs.stderr)
        finally:
            command("docker", "rm", "-f", container)
