"""Tests for nlp2cmd.execution — Etap 3: modular executors."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from nlp2cmd.execution.base import ExecutorContext, ExecutorResult
from nlp2cmd.execution.executor_registry import (
    ExecutorRegistry,
    create_default_registry,
)
from nlp2cmd.execution.media_recorder import MediaRecorder
from nlp2cmd.execution.shell_executor import ShellExecutor

# ── ExecutorResult ──────────────────────────────────────────────────────

class TestExecutorResult:
    def test_basic(self):
        r = ExecutorResult(success=True, kind="shell", data={"foo": "bar"})
        assert r.success is True
        assert r.kind == "shell"
        assert r.data["foo"] == "bar"
        assert r.error is None

    def test_to_runner_result(self):
        r = ExecutorResult(success=False, kind="shell", error="fail")
        rr = r.to_runner_result()
        assert rr.success is False
        assert rr.kind == "shell"
        assert rr.error == "fail"


# ── ExecutorContext ─────────────────────────────────────────────────────

class TestExecutorContext:
    def test_defaults(self):
        ctx = ExecutorContext()
        assert ctx.dry_run is False
        assert ctx.confirm is False
        assert ctx.headless is True
        assert ctx.variables == {}

    def test_custom(self):
        ctx = ExecutorContext(dry_run=True, confirm=True, headless=False)
        assert ctx.dry_run is True
        assert ctx.confirm is True


# ── ShellExecutor ───────────────────────────────────────────────────────

class TestShellExecutor:
    def test_empty_command(self):
        executor = ShellExecutor()
        ctx = ExecutorContext()
        result = executor.execute({"command": ""}, ctx)
        assert result.success is False
        assert "Empty" in result.error

    def test_dry_run(self):
        executor = ShellExecutor()
        ctx = ExecutorContext(dry_run=True)
        result = executor.execute({"command": "ls -la"}, ctx)
        assert result.success is True
        assert result.data.get("dry_run") is True
        assert result.data.get("argv") == ["ls", "-la"]

    def test_supported_actions(self):
        executor = ShellExecutor()
        assert "shell" in executor.supported_actions
        assert "run_command" in executor.supported_actions

    @patch("nlp2cmd.execution.shell_executor.subprocess.run")
    def test_successful_execution(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="hello\n", stderr=""
        )
        executor = ShellExecutor()
        ctx = ExecutorContext(dry_run=False)
        result = executor.execute({"command": "echo hello"}, ctx)
        assert result.success is True
        assert result.data["stdout"] == "hello\n"
        assert result.data["returncode"] == 0

    @patch("nlp2cmd.execution.shell_executor.subprocess.run")
    def test_failed_execution(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="not found"
        )
        executor = ShellExecutor()
        ctx = ExecutorContext(dry_run=False)
        result = executor.execute({"command": "bad_cmd"}, ctx)
        assert result.success is False
        assert "not found" in result.error

    def test_shell_policy_sudo_blocked(self):
        policy = MagicMock()
        policy.allow_sudo = False
        policy.allow_pipes = True
        policy.blocked_regex = []
        policy.require_confirm_regex = []
        policy.allowlist = None

        executor = ShellExecutor(shell_policy=policy)
        ctx = ExecutorContext()
        result = executor.execute({"command": "sudo rm -rf /"}, ctx)
        assert result.success is False
        assert "sudo" in result.error.lower()

    def test_shell_policy_pipes_blocked(self):
        policy = MagicMock()
        policy.allow_sudo = True
        policy.allow_pipes = False
        policy.blocked_regex = []
        policy.require_confirm_regex = []
        policy.allowlist = None

        executor = ShellExecutor(shell_policy=policy)
        ctx = ExecutorContext()
        result = executor.execute({"command": "ls | grep foo"}, ctx)
        assert result.success is False
        assert "Pipes" in result.error or "pipe" in result.error.lower()

    def test_confirmation_required(self):
        policy = MagicMock()
        policy.allow_sudo = True
        policy.allow_pipes = True
        policy.blocked_regex = []
        policy.require_confirm_regex = [r"rm\s"]
        policy.allowlist = None

        executor = ShellExecutor(shell_policy=policy)
        ctx = ExecutorContext(confirm=False)
        result = executor.execute({"command": "rm file.txt"}, ctx)
        assert result.success is False
        assert "confirmation" in result.error.lower()

    def test_confirmation_granted(self):
        policy = MagicMock()
        policy.allow_sudo = True
        policy.allow_pipes = True
        policy.blocked_regex = []
        policy.require_confirm_regex = [r"rm\s"]
        policy.allowlist = None

        executor = ShellExecutor(shell_policy=policy)
        ctx = ExecutorContext(confirm=True, dry_run=True)
        result = executor.execute({"command": "rm file.txt"}, ctx)
        assert result.success is True
        assert result.data.get("dry_run") is True


# ── MediaRecorder ───────────────────────────────────────────────────────

class TestMediaRecorder:
    def test_supported_actions(self):
        recorder = MediaRecorder()
        assert "screenshot" in recorder.supported_actions
        assert "start_recording" in recorder.supported_actions
        assert "stop_recording" in recorder.supported_actions

    def test_stop_without_recording(self):
        recorder = MediaRecorder()
        ctx = ExecutorContext()
        result = recorder.stop_recording({}, ctx)
        assert result.success is True
        assert result.data.get("recording") is False

    def test_screenshot_no_page(self):
        recorder = MediaRecorder()
        ctx = ExecutorContext(page=None)
        result = recorder.take_screenshot({}, ctx)
        assert result.success is False
        assert "No page" in result.error

    def test_screenshot_with_mock_page(self):
        recorder = MediaRecorder()
        mock_page = MagicMock()
        ctx = ExecutorContext(page=mock_page)
        result = recorder.take_screenshot({"path": "/tmp/test.png"}, ctx)
        assert result.success is True
        mock_page.screenshot.assert_called_once_with(path="/tmp/test.png")

    def test_get_context_options_no_video(self):
        recorder = MediaRecorder()
        assert recorder.get_context_options() == {}

    def test_get_context_options_with_video(self):
        recorder = MediaRecorder(output_dir="/tmp/vids")
        opts = recorder.get_context_options(video_fmt="webm")
        assert opts["record_video_dir"] == "/tmp/vids"
        assert opts["record_video_size"]["width"] == 1280

    def test_is_recording_initially_false(self):
        recorder = MediaRecorder()
        assert recorder.is_recording is False

    def test_execute_dispatch(self):
        recorder = MediaRecorder()
        ctx = ExecutorContext(page=MagicMock())
        result = recorder.execute({"action": "screenshot", "path": "/tmp/x.png"}, ctx)
        assert result.success is True

    def test_execute_unknown_action(self):
        recorder = MediaRecorder()
        ctx = ExecutorContext()
        result = recorder.execute({"action": "fly_to_moon"}, ctx)
        assert result.success is False
        assert "Unknown" in result.error


# ── ExecutorRegistry ────────────────────────────────────────────────────

class TestExecutorRegistry:
    def test_dispatch_media_start_binds_action_without_mutating_params(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        registry = ExecutorRegistry()
        recorder = MediaRecorder()
        registry.register(recorder)
        page = MagicMock()
        page.is_closed.return_value = False
        params = {"name_prefix": "selected"}

        result = registry.dispatch("start_recording", params, ExecutorContext(page=page, video_dir=str(tmp_path)))

        assert result.success, result.error
        assert recorder.is_recording
        assert params == {"name_prefix": "selected"}
        page.screenshot.assert_not_called()

    def test_dispatch_media_stop_finalizes_selected_recording(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        registry = ExecutorRegistry()
        recorder = MediaRecorder()
        registry.register(recorder)
        page = MagicMock()
        page.is_closed.return_value = False
        page.video.save_as.side_effect = lambda path: Path(path).write_bytes(b"recorded video")
        ctx = ExecutorContext(page=page, video_dir=str(tmp_path))
        assert recorder.start_recording({}, ctx).success
        page.is_closed.return_value = True
        params = {}

        result = registry.dispatch("stop_recording", params, ctx)

        assert result.success, result.error
        assert not recorder.is_recording
        assert Path(result.data["video_path"]).read_bytes() == b"recorded video"
        assert params == {}
        page.screenshot.assert_not_called()

    def test_dispatch_rejects_conflicting_payload_before_executor(self):
        registry = ExecutorRegistry()
        executor = MagicMock()
        executor.supported_actions = ["start_recording"]
        executor.execute.return_value = ExecutorResult(success=True, kind="media")
        registry.register(executor)
        params = {"action": "screenshot"}

        result = registry.dispatch("start_recording", params, ExecutorContext(dry_run=True))

        assert not result.success
        assert "action" in result.error.lower()
        assert params == {"action": "screenshot"}
        executor.execute.assert_not_called()

    def test_register_and_dispatch(self):
        registry = ExecutorRegistry()
        executor = ShellExecutor()
        registry.register(executor)

        assert "shell" in registry
        assert "run_command" in registry
        assert registry.get("shell") is executor

    def test_dispatch_unknown(self):
        registry = ExecutorRegistry()
        ctx = ExecutorContext()
        result = registry.dispatch("nonexistent", {}, ctx)
        assert result.success is False
        assert "No executor" in result.error

    def test_dispatch_shell_dry_run(self):
        registry = ExecutorRegistry()
        registry.register(ShellExecutor())
        ctx = ExecutorContext(dry_run=True)
        result = registry.dispatch("shell", {"command": "ls"}, ctx)
        assert result.success is True
        assert result.data.get("dry_run") is True

    def test_registered_actions(self):
        registry = ExecutorRegistry()
        registry.register(ShellExecutor())
        registry.register(MediaRecorder())
        actions = registry.registered_actions
        assert "shell" in actions
        assert "screenshot" in actions
        assert actions == sorted(actions)

    def test_len(self):
        registry = ExecutorRegistry()
        assert len(registry) == 0
        registry.register(ShellExecutor())
        assert len(registry) >= 3  # shell, run_command, execute

    def test_create_default_registry(self):
        registry = create_default_registry()
        assert len(registry) >= 5  # shell + media actions
        assert "shell" in registry
        assert "screenshot" in registry
        assert "start_recording" in registry
