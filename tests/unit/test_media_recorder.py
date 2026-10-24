"""Regression tests for the media executor's state and output paths."""
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from nlp2cmd.execution.base import ExecutorContext
from nlp2cmd.execution.executor_registry import ExecutorRegistry
from nlp2cmd.execution.media_recorder import MediaRecorder
from nlp2cmd.utils import media_utils


@pytest.fixture
def recording_context(tmp_path):
    page = MagicMock()
    page.is_closed.return_value = False
    return ExecutorContext(page=page, video_dir=str(tmp_path))


def _invoke_media(recorder, action, entry, params, ctx):
    if entry == "direct":
        method = recorder.take_screenshot if action == "screenshot" else getattr(recorder, action)
        return method(params, ctx)
    if entry == "execute":
        return recorder.execute({**params, "action": action}, ctx)
    registry = ExecutorRegistry()
    registry.register(recorder)
    return registry.dispatch(action, params, ctx)


@pytest.mark.parametrize("action", ["start_recording", "stop_recording", "screenshot"])
@pytest.mark.parametrize("entry", ["direct", "execute", "registry"])
@pytest.mark.parametrize("page_present", [False, True])
def test_media_dry_run_does_not_touch_browser_or_files(tmp_path, action, entry, page_present):
    page = MagicMock() if page_present else None
    if page is not None:
        page.is_closed.return_value = False
        page.screenshot.side_effect = lambda *, path: Path(path).write_bytes(b"unexpected capture")
    ctx = ExecutorContext(page=page, dry_run=True, video_dir=str(tmp_path / "videos"))
    recorder = MediaRecorder()

    result = _invoke_media(recorder, action, entry, {"path": str(tmp_path / "capture.png")}, ctx)

    assert result.success, result.error
    assert result.data == {"dry_run": True, "action": action}
    assert page is None or page.mock_calls == []
    assert list(tmp_path.iterdir()) == []
    assert not recorder.is_recording
    assert recorder._video_recorder is None


@pytest.mark.parametrize("action", ["start_recording", "stop_recording", "screenshot"])
@pytest.mark.parametrize("entry", ["direct", "execute", "registry"])
def test_media_dry_run_preserves_active_recording(recording_context, tmp_path, action, entry):
    recorder = MediaRecorder()
    assert recorder.start_recording({}, recording_context).success
    handle = recorder._video_recorder
    video = recording_context.page.video
    recording_context.page.is_closed.return_value = True
    recording_context.page.reset_mock()
    recording_context.dry_run = True

    result = _invoke_media(recorder, action, entry, {"path": str(tmp_path / "capture.png")}, recording_context)

    assert result.success, result.error
    assert result.data == {"dry_run": True, "action": action}
    assert recorder.is_recording
    assert recorder._video_recorder is handle
    assert recorder._recorded_video is video
    assert recording_context.page.mock_calls == []
    assert list(tmp_path.iterdir()) == []


def test_unknown_media_action_still_fails_in_dry_run():
    result = MediaRecorder().execute({"action": "unknown"}, ExecutorContext(dry_run=True))
    assert not result.success


@pytest.mark.parametrize("page_state", ["missing", "unconfigured", "closed"])
def test_start_requires_live_video_enabled_page(tmp_path, page_state):
    page = None if page_state == "missing" else MagicMock()
    if page is not None:
        page.is_closed.return_value = page_state == "closed"
        if page_state == "unconfigured":
            page.video = None
    recorder = MediaRecorder()

    result = recorder.start_recording({}, ExecutorContext(page=page, video_dir=str(tmp_path)))

    assert not result.success
    assert not recorder.is_recording
    assert recorder._video_recorder is None
    assert list(tmp_path.iterdir()) == []


def test_stop_saves_bound_video_only_after_its_page_closes(tmp_path):
    page = MagicMock()
    page.is_closed.return_value = False
    page.video.save_as.side_effect = lambda path: Path(path).write_bytes(b"saved video")
    context = MagicMock()
    ctx = ExecutorContext(page=page, context=context, video_dir=str(tmp_path))
    recorder = MediaRecorder()
    started = recorder.start_recording({}, ctx)
    assert started.success

    premature = recorder.stop_recording({}, ctx)

    assert not premature.success
    assert recorder.is_recording
    page.video.save_as.assert_not_called()
    page.close.assert_not_called()
    context.close.assert_not_called()
    page.is_closed.return_value = True
    other_page = MagicMock()
    stopped = recorder.stop_recording({}, ExecutorContext(page=other_page))
    assert stopped.success, stopped.error
    output = Path(stopped.data["video_path"])
    assert str(output) == started.data["video_path"]
    assert output.read_bytes() == b"saved video"
    page.video.save_as.assert_called_once_with(str(output))
    other_page.video.save_as.assert_not_called()
    assert not recorder.is_recording


def test_video_save_failure_can_retry_without_losing_bound_handle(tmp_path):
    page = MagicMock()
    page.is_closed.return_value = False
    ctx = ExecutorContext(page=page, video_dir=str(tmp_path))
    recorder = MediaRecorder()
    assert recorder.start_recording({}, ctx).success
    page.is_closed.return_value = True
    page.video.save_as.side_effect = OSError("temporary save failure")

    failed = recorder.stop_recording({}, ctx)

    assert not failed.success
    assert recorder.is_recording
    page.video.save_as.side_effect = lambda path: Path(path).write_bytes(b"retried video")
    retried = recorder.stop_recording({}, ctx)
    assert retried.success, retried.error
    assert Path(retried.data["video_path"]).read_bytes() == b"retried video"
    assert not recorder.is_recording


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


@pytest.mark.parametrize("reuse_recorder", [False, True])
def test_rapid_screenshots_preserve_each_capture(monkeypatch, tmp_path, reuse_recorder):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(media_utils, "get_timestamp", lambda: "20261023_120000")
    captures = iter([b"first capture", b"second capture"])
    page = MagicMock()
    page.screenshot.side_effect = lambda *, path: Path(path).write_bytes(next(captures))
    ctx = ExecutorContext(page=page)
    recorder = MediaRecorder()

    first = recorder.take_screenshot({}, ctx)
    second = (recorder if reuse_recorder else MediaRecorder()).take_screenshot({}, ctx)

    assert first.success and second.success
    first_path, second_path = Path(first.data["screenshot_path"]), Path(second.data["screenshot_path"])
    assert first_path != second_path
    assert first_path.read_bytes() == b"first capture"
    assert second_path.read_bytes() == b"second capture"


def test_second_start_preserves_active_recorder(recording_context):
    recorder = MediaRecorder()
    ctx = recording_context
    assert recorder.start_recording({}, ctx).success
    active = recorder._video_recorder
    assert not recorder.start_recording({}, ctx).success
    assert recorder._video_recorder is active
    assert recorder.is_recording


def test_stop_returns_backend_output_and_clears_state(monkeypatch, recording_context):
    backend = MagicMock()
    backend.start_recording.return_value = "expected.webm"
    backend.stop_recording.return_value = "actual.webm"
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    ctx = recording_context
    assert recorder.start_recording({}, ctx).success
    ctx.page.is_closed.return_value = True
    result = recorder.stop_recording({}, ctx)
    assert result.success
    assert result.data["video_path"] == "actual.webm"
    assert not recorder.is_recording
    assert recorder._video_recorder is None
    assert recorder.stop_recording({}, ctx).success
    backend.stop_recording.assert_called_once()


def test_failed_start_can_retry(monkeypatch, recording_context):
    backend = MagicMock()
    backend.start_recording.side_effect = [None, "capture.webm"]
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    assert not recorder.start_recording({}, recording_context).success
    assert not recorder.is_recording
    assert recorder._video_recorder is None
    assert recorder.start_recording({}, recording_context).success


def test_failed_stop_retains_handle_for_retry(monkeypatch, recording_context):
    backend = MagicMock()
    backend.start_recording.return_value = "capture.webm"
    backend.stop_recording.side_effect = [RuntimeError("busy"), "capture.webm"]
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    recorder.start_recording({}, recording_context)
    recording_context.page.is_closed.return_value = True
    assert not recorder.stop_recording({}, recording_context).success
    assert recorder.is_recording
    assert recorder.stop_recording({}, recording_context).success


def test_stop_without_path_is_not_success(monkeypatch, recording_context):
    backend = MagicMock()
    backend.start_recording.return_value = "capture.webm"
    backend.stop_recording.return_value = None
    monkeypatch.setattr(media_utils.VideoRecorder, "start_recording", backend.start_recording)
    monkeypatch.setattr(media_utils.VideoRecorder, "stop_recording", backend.stop_recording)
    recorder = MediaRecorder()
    recorder.start_recording({}, recording_context)
    recording_context.page.is_closed.return_value = True
    assert not recorder.stop_recording({}, recording_context).success
    assert not recorder.is_recording


@pytest.mark.parametrize("output_kind", ["missing", "empty", "directory"])
@pytest.mark.parametrize("explicit_path", [False, True])
def test_video_helper_rejects_unsaved_output(tmp_path, output_kind, explicit_path):
    recorder = media_utils.VideoRecorder(output_dir=tmp_path)
    expected = Path(recorder.start_recording())
    output = tmp_path / "actual.webm" if explicit_path else expected
    if output_kind == "empty":
        output.touch()
    elif output_kind == "directory":
        output.mkdir()
    console = MagicMock()

    assert recorder.stop_recording(console, saved_path=str(output) if explicit_path else None) is None
    assert not recorder.is_recording
    assert not any("Nagranie zapisane" in str(call) for call in console.print.call_args_list)


@pytest.mark.parametrize("explicit_path", [False, True])
def test_video_helper_returns_only_existing_nonempty_output(tmp_path, explicit_path):
    recorder = media_utils.VideoRecorder(output_dir=tmp_path)
    expected = Path(recorder.start_recording())
    output = tmp_path / "actual.webm" if explicit_path else expected
    output.write_bytes(b"recorded video frames")
    console = MagicMock()

    assert recorder.stop_recording(console, saved_path=str(output) if explicit_path else None) == str(output)
    assert not recorder.is_recording
    assert any("Nagranie zapisane" in str(call) for call in console.print.call_args_list)


def test_later_session_cannot_reuse_previous_video(monkeypatch, tmp_path):
    monkeypatch.setattr(media_utils, "get_timestamp", lambda: "20261023_120000")
    first = media_utils.VideoRecorder(output_dir=tmp_path)
    first_path = Path(first.start_recording())
    first_path.write_bytes(b"earlier session")
    assert first.stop_recording() == str(first_path)

    second = media_utils.VideoRecorder(output_dir=tmp_path)
    assert second.start_recording() != str(first_path)
    assert second.stop_recording() is None
    assert first_path.read_bytes() == b"earlier session"


def test_real_media_executor_does_not_report_nonexistent_video(recording_context):
    ctx = recording_context
    recorder = MediaRecorder()
    assert recorder.start_recording({}, ctx).success
    ctx.page.is_closed.return_value = True
    result = recorder.stop_recording({}, ctx)
    assert not result.success
    assert "video_path" not in result.data
    assert not recorder.is_recording


@pytest.mark.e2e
def test_media_dry_run_with_real_browser_leaves_page_and_disk_unchanged(tmp_path):
    from playwright.sync_api import sync_playwright

    recorder = MediaRecorder(output_dir=str(tmp_path / "videos"))
    registry = ExecutorRegistry()
    registry.register(recorder)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            page = context.new_page()
            page.set_content("<h1>Preview must preserve this page</h1>")
            ctx = ExecutorContext(page=page, context=context, dry_run=True, video_dir=str(tmp_path / "videos"))
            for action in recorder.supported_actions:
                result = registry.dispatch(action, {"path": str(tmp_path / "capture.png")}, ctx)
                assert result.success, result.error
                assert result.data == {"dry_run": True, "action": action}
            assert not page.is_closed()
            assert page.locator("h1").inner_text() == "Preview must preserve this page"
            assert context.pages == [page]
            assert not recorder.is_recording
            assert list(tmp_path.iterdir()) == []
            context.close()
        finally:
            browser.close()


@pytest.mark.e2e
def test_media_executor_saves_real_playwright_video(tmp_path):
    import json
    import subprocess

    from playwright.sync_api import sync_playwright

    recorder = MediaRecorder(output_dir=str(tmp_path / "saved"))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context(**recorder.get_context_options(video_fmt="webm"))
            page = context.new_page()
            ctx = ExecutorContext(page=page, context=context, video_dir=str(tmp_path / "saved"))
            page.set_content("<h1>Real media executor recording</h1>")
            started = recorder.start_recording({}, ctx)
            assert started.success, started.error
            page.wait_for_timeout(500)
            ctx.dry_run = True
            preview = recorder.stop_recording({}, ctx)
            assert preview.data == {"dry_run": True, "action": "stop_recording"}
            assert recorder.is_recording and not page.is_closed()
            ctx.dry_run = False
            premature = recorder.stop_recording({}, ctx)
            assert not premature.success and not page.is_closed()
            page.close()
            stopped = recorder.stop_recording({}, ctx)
            assert stopped.success, stopped.error
            context.close()
        finally:
            browser.close()

    output = Path(stopped.data["video_path"])
    assert str(output) == started.data["video_path"]
    assert output.is_file() and output.stat().st_size > 0
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(output),
    ], text=True, timeout=30))
    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    assert (stream["width"], stream["height"]) == (1280, 720)
    assert float(probe["format"]["duration"]) > 0
    assert not recorder.is_recording
    (tmp_path / "verification.json").write_text(json.dumps(probe, indent=2) + "\n")


@pytest.mark.e2e
def test_video_helper_finalizes_real_playwright_recording(tmp_path):
    """Explicit E2E requires installed Playwright/Chromium and ffprobe."""
    import json
    import shutil
    import subprocess

    from playwright.sync_api import sync_playwright

    assert shutil.which("ffprobe"), "The recording E2E requires ffprobe"
    recorder = media_utils.VideoRecorder(output_dir=tmp_path)
    output = recorder.start_recording()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": 640, "height": 480},
                record_video_dir=str(tmp_path),
                record_video_size={"width": 640, "height": 480},
            )
            page = context.new_page()
            page.set_content("<h1>NLP2CMD recording verification</h1>")
            page.wait_for_timeout(500)
            video = page.video
            assert video is not None
            context.close()
            video.save_as(output)
        finally:
            browser.close()
    assert recorder.stop_recording(saved_path=output) == output
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", output,
    ], text=True, timeout=30))
    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    assert (stream["width"], stream["height"]) == (640, 480)
    assert float(probe["format"]["duration"]) > 0
    (tmp_path / "verification.json").write_text(json.dumps(probe, indent=2) + "\n")


@pytest.mark.e2e
def test_rapid_screenshots_with_real_playwright(monkeypatch, tmp_path):
    """Explicit E2E requires an installed Playwright Chromium browser."""
    import json

    from playwright.sync_api import sync_playwright

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(media_utils, "get_timestamp", lambda: "20261023_120000")
    recorder = MediaRecorder()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 640, "height": 480})
            ctx = ExecutorContext(page=page)
            page.set_content("<body style='background:red'>First capture</body>")
            first = recorder.take_screenshot({}, ctx)
            assert first.success, first.error
            first_path = Path(first.data["screenshot_path"])
            first_bytes = first_path.read_bytes()
            page.set_content("<body style='background:blue'>Second capture</body>")
            second = recorder.take_screenshot({}, ctx)
            assert second.success, second.error
            second_path = Path(second.data["screenshot_path"])
        finally:
            browser.close()

    assert first_path != second_path
    assert first_path.read_bytes() == first_bytes
    assert first_bytes != second_path.read_bytes()
    assert all(p.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") for p in (first_path, second_path))
    (tmp_path / "verification.json").write_text(json.dumps({
        "first": str(first_path), "second": str(second_path), "firstPreserved": True,
    }, indent=2) + "\n")
