"""Behavioral tests for demo resource ownership and real video finalization."""
import importlib.util
from pathlib import Path
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
