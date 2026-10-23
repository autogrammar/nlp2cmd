"""Regression tests for the media executor's state and output paths."""
from pathlib import Path
from unittest.mock import MagicMock

from nlp2cmd.execution.base import ExecutorContext
from nlp2cmd.execution.media_recorder import MediaRecorder
from nlp2cmd.utils import media_utils


def test_default_screenshot_creates_parent_and_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    page = MagicMock()
    page.screenshot.side_effect = lambda *, path: Path(path).write_bytes(b"png")
    result = MediaRecorder().take_screenshot({}, ExecutorContext(page=page))
    assert result.success, result.error
    assert Path(result.data["screenshot_path"]).is_file()


def test_explicit_screenshot_creates_nested_parent(tmp_path):
    path = tmp_path / "nested" / "capture.png"
    page = MagicMock()
    page.screenshot.side_effect = lambda *, path: Path(path).write_bytes(b"png")
    result = MediaRecorder().take_screenshot({"path": path}, ExecutorContext(page=page))
    assert result.success, result.error
    assert path.is_file()


def test_screenshot_directory_failure_is_result(tmp_path):
    blocked = tmp_path / "file"
    blocked.write_text("not a directory")
    result = MediaRecorder().take_screenshot({"path": blocked / "image.png"}, ExecutorContext(page=MagicMock()))
    assert not result.success
    assert "Screenshot failed" in result.error


def test_second_start_preserves_active_recorder(tmp_path):
    recorder = MediaRecorder()
    ctx = ExecutorContext(video_dir=str(tmp_path))
    assert recorder.start_recording({}, ctx).success
    active = recorder._video_recorder
    assert not recorder.start_recording({}, ctx).success
    assert recorder._video_recorder is active
    assert recorder.is_recording


def test_stop_returns_backend_output_and_clears_state(monkeypatch):
    backend = MagicMock()
    backend.start_recording.return_value = "expected.webm"
    backend.stop_recording.return_value = "actual.webm"
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    ctx = ExecutorContext()
    assert recorder.start_recording({}, ctx).success
    result = recorder.stop_recording({}, ctx)
    assert result.success
    assert result.data["video_path"] == "actual.webm"
    assert not recorder.is_recording
    assert recorder._video_recorder is None
    assert recorder.stop_recording({}, ctx).success
    backend.stop_recording.assert_called_once()


def test_failed_start_can_retry(monkeypatch):
    backend = MagicMock()
    backend.start_recording.side_effect = [None, "capture.webm"]
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    assert not recorder.start_recording({}, ExecutorContext()).success
    assert not recorder.is_recording
    assert recorder._video_recorder is None
    assert recorder.start_recording({}, ExecutorContext()).success


def test_failed_stop_retains_handle_for_retry(monkeypatch):
    backend = MagicMock()
    backend.start_recording.return_value = "capture.webm"
    backend.stop_recording.side_effect = [RuntimeError("busy"), "capture.webm"]
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    recorder.start_recording({}, ExecutorContext())
    assert not recorder.stop_recording({}, ExecutorContext()).success
    assert recorder.is_recording
    assert recorder.stop_recording({}, ExecutorContext()).success


def test_stop_without_path_is_not_success(monkeypatch):
    backend = MagicMock()
    backend.start_recording.return_value = "capture.webm"
    backend.stop_recording.return_value = None
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    recorder.start_recording({}, ExecutorContext())
    assert not recorder.stop_recording({}, ExecutorContext()).success
    assert not recorder.is_recording
