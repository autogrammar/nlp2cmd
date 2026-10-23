"""
Media recorder — Etap 3 of the NLP refactoring plan.

Handles video recording and screenshot capture for browser automation.
Extracted from ``pipeline_runner._run_dom_multi_action`` video logic.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from nlp2cmd.execution.base import BaseExecutor, ExecutorContext, ExecutorResult

class MediaRecorder(BaseExecutor):
    """Manages video recording and screenshots during browser sessions."""

    def __init__(self, output_dir: str = "./recordings") -> None:
        self._output_dir = output_dir
        self._video_recorder: Any = None
        self._recording = False
        self._recording_page: Any = None
        self._recorded_video: Any = None

    @property
    def supported_actions(self) -> list[str]:
        return ["start_recording", "stop_recording", "screenshot"]

    def execute(
        self,
        params: dict[str, Any],
        ctx: ExecutorContext,
    ) -> ExecutorResult:
        action = params.get("action", "screenshot")
        if action == "start_recording":
            return self.start_recording(params, ctx)
        if action == "stop_recording":
            return self.stop_recording(params, ctx)
        if action == "screenshot":
            return self.take_screenshot(params, ctx)
        return ExecutorResult(
            success=False, kind="media",
            error=f"Unknown media action: {action}",
        )

    def start_recording(
        self,
        params: dict[str, Any],
        ctx: ExecutorContext,
    ) -> ExecutorResult:
        """Start video recording."""
        if self._recording:
            return ExecutorResult(success=False, kind="media", error="Recording already active")
        output_dir = params.get("output_dir", ctx.video_dir or self._output_dir)
        name_prefix = params.get("name_prefix", "browser_automation")

        try:
            page = ctx.page
            if page is None or page.is_closed():
                return ExecutorResult(success=False, kind="media", error="No live page available for recording")
            video = page.video
            if video is None:
                return ExecutorResult(success=False, kind="media",
                                      error="Create the browser context with record_video_dir before recording")
            from nlp2cmd.utils.media_utils import VideoRecorder
            recorder = VideoRecorder(output_dir=output_dir)
            video_path = recorder.start_recording(name_prefix=name_prefix)
            if video_path:
                self._video_recorder = recorder
                self._recording = True
                self._recording_page = page
                self._recorded_video = video
                return ExecutorResult(
                    success=True, kind="media",
                    data={"video_path": str(video_path), "recording": True},
                )
            return ExecutorResult(
                success=False, kind="media",
                error="VideoRecorder.start_recording returned no path",
            )
        except Exception as e:
            return ExecutorResult(
                success=False, kind="media",
                error=f"Failed to start recording: {e}",
            )

    def stop_recording(
        self,
        params: dict[str, Any],
        ctx: ExecutorContext,
    ) -> ExecutorResult:
        """Stop video recording and return output path."""
        if not self._video_recorder or not self._recording:
            return ExecutorResult(
                success=True, kind="media",
                data={"recording": False, "note": "No active recording"},
            )
        try:
            if not self._recording_page.is_closed():
                return ExecutorResult(success=False, kind="media",
                                      error="Close the recorded page or its context before stopping recording")
            # save_as waits for the page to close, so never call it on a live page.
            self._recorded_video.save_as(self._video_recorder.video_path)
            video_path = self._video_recorder.stop_recording()
            self._recording = False
            self._video_recorder = None
            self._recording_page = None
            self._recorded_video = None
            if not video_path:
                return ExecutorResult(success=False, kind="media",
                                      error="VideoRecorder.stop_recording returned no path")
            return ExecutorResult(
                success=True, kind="media",
                data={"recording": False, "stopped": True, "video_path": str(video_path)},
            )
        except Exception as e:
            return ExecutorResult(
                success=False, kind="media",
                error=f"Failed to stop recording: {e}",
            )

    def take_screenshot(
        self,
        params: dict[str, Any],
        ctx: ExecutorContext,
    ) -> ExecutorResult:
        """Take a screenshot of the current page."""
        page = ctx.page
        if page is None:
            return ExecutorResult(
                success=False, kind="media",
                error="No page available for screenshot",
            )

        try:
            from nlp2cmd.utils.media_utils import get_timestamp, ensure_dir
            path = Path(params.get("path") or f"./screenshots/screenshot_{get_timestamp()}_{uuid4().hex}.png")
            ensure_dir(path.parent)
            path = str(path)
            page.screenshot(path=path)
            return ExecutorResult(
                success=True, kind="media",
                data={"screenshot_path": path},
            )
        except Exception as e:
            return ExecutorResult(
                success=False, kind="media",
                error=f"Screenshot failed: {e}",
            )

    @property
    def is_recording(self) -> bool:
        return self._recording

    def get_context_options(self, video_fmt: Optional[str] = None) -> dict[str, Any]:
        """Return Playwright context options for video recording."""
        if not video_fmt:
            return {}
        return {
            "record_video_dir": self._output_dir,
            "record_video_size": {"width": 1280, "height": 720},
        }

    @staticmethod
    def should_record_interactive(console: Any, confirm: bool) -> tuple[bool, str]:
        """Ask user interactively whether to record video (TTY only)."""
        try:
            is_tty = bool(getattr(sys.stdin, "isatty", lambda: False)())
        except Exception:
            is_tty = False

        if confirm and is_tty:
            try:
                from nlp2cmd.utils.media_utils import ask_for_video_recording
                return ask_for_video_recording(console)
            except Exception:
                pass
        return False, "./recordings"
