from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Literal, Optional

from rich.console import Console

from nlp2cmd.pipeline_runner_browser_multi_extract import BrowserMultiExtractMixin
from nlp2cmd.pipeline_runner_browser_multi_forms import BrowserMultiFormMixin
from nlp2cmd.pipeline_runner_browser_multi_nav import BrowserMultiNavMixin
from nlp2cmd.pipeline_runner_browser_multi_persist import BrowserMultiPersistMixin
from nlp2cmd.pipeline_runner_browser_multi_state import MultiActionState
from nlp2cmd.pipeline_runner_utils import (
    _debug,
    RunnerResult,
    VideoRecorder,
    ask_for_video_recording,
)

ActionOutcome = RunnerResult | Literal["continue"] | None


class BrowserMultiActionMixin(
    BrowserMultiNavMixin,
    BrowserMultiFormMixin,
    BrowserMultiExtractMixin,
    BrowserMultiPersistMixin,
):
    """Legacy multi-action browser execution for PipelineRunner."""

    def _dispatch_legacy_multi_action(
        self,
        state: MultiActionState,
        action: str | None,
        action_spec: dict[str, Any],
        action_index: int,
    ) -> ActionOutcome:
        if action in {"goto", "navigate"}:
            self._legacy_multi_goto(state, action_spec)
            return None
        if action == "explore_for_content":
            self._legacy_multi_explore_content(state, action_spec)
            return None
        if action == "explore_for_form":
            self._legacy_multi_explore_form(state, action_spec)
            return None
        if action == "fill_form":
            return self._legacy_multi_fill_form(state, action_spec, action_index)
        if action in ("extract_company_websites_deep", "extract_companies"):
            return self._legacy_multi_extract_companies(state, action_spec, action_index)
        if action == "save_to_file":
            return self._legacy_multi_save_to_file(state, action_spec, action_index)
        if action == "save_to_csv":
            return self._legacy_multi_save_to_csv(state, action_spec, action_index)
        return RunnerResult(
            success=False,
            kind="dom",
            error=f"Action {action_index}: Unsupported action: {action}",
        )

    def _run_dom_multi_action(
        self,
        payload: dict[str, Any],
        *,
        dry_run: bool,
        confirm: bool,
        web_url: Optional[str],
        video_fmt: Optional[str] = None,
        video_dir: Optional[str] = None,
    ) -> RunnerResult:
        """Execute multiple browser actions in sequence."""
        actions = payload.get("actions", [])
        url = payload.get("url") or web_url

        if not url:
            return RunnerResult(success=False, kind="dom", error="Missing url for multi-action")

        if not confirm:
            for a in actions:
                if isinstance(a, dict) and str(a.get("action") or "") == "press":
                    if str(a.get("key") or "") in {"Enter", "Return"}:
                        return RunnerResult(
                            success=False,
                            kind="dom",
                            error="Action requires confirmation",
                            data={
                                "requires_confirmation": True,
                                "confirmation_reason": "press_enter",
                                "url": url,
                            },
                        )
                if isinstance(a, dict) and str(a.get("action") or "") == "submit":
                    return RunnerResult(
                        success=False,
                        kind="dom",
                        error="Action requires confirmation",
                        data={
                            "requires_confirmation": True,
                            "confirmation_reason": "submit",
                            "url": url,
                        },
                    )

        if dry_run:
            return RunnerResult(
                success=True,
                kind="dom",
                data={"dry_run": True, "url": url, "actions": actions},
            )

        console = Console()

        try:
            from playwright.sync_api import sync_playwright  # type: ignore
        except Exception as e:
            return RunnerResult(success=False, kind="dom", error=f"Playwright not available: {e}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            from nlp2cmd.web_schema.form_data_loader import FormDataLoader

            schema_loader = FormDataLoader(site=str(url))
            ctx_opts = schema_loader.get_browser_context_options()

            should_record_video = False
            effective_video_dir = video_dir or "./recordings"

            if video_fmt:
                should_record_video = True
                effective_video_dir = video_dir or "./recordings"
                _debug(f"Video recording enabled via --video {video_fmt}")
            else:
                try:
                    is_tty = bool(getattr(sys.stdin, "isatty", lambda: False)())
                except Exception:
                    is_tty = False
                if confirm and is_tty:
                    should_record_video, effective_video_dir = ask_for_video_recording(console)

            video_recorder = None

            if should_record_video:
                video_recorder = VideoRecorder(output_dir=effective_video_dir)
                video_path = video_recorder.start_recording(name_prefix="browser_automation")
                if video_path:
                    console.print(f"[dim]🎥 Nagrywanie wideo: {video_path}[/dim]")
                    ctx_opts["record_video_dir"] = effective_video_dir
                    ctx_opts["record_video_size"] = {"width": 1280, "height": 720}

            context = browser.new_context(**ctx_opts)

            if not should_record_video:
                try:
                    blocked = (
                        "**/*.png", "**/*.jpg", "**/*.jpeg", "**/*.gif", "**/*.svg",
                        "**/*.webp", "**/*.ico", "**/*.bmp", "**/*.tiff",
                        "**/*.woff", "**/*.woff2", "**/*.ttf", "**/*.eot",
                        "**/*.mp4", "**/*.webm", "**/*.ogg", "**/*.mp3",
                    )

                    def _abort_heavy(route):
                        try:
                            route.abort()
                        except Exception:
                            pass

                    for pat in blocked:
                        context.route(pat, _abort_heavy)
                    _debug("Resource blocking enabled in pipeline_runner")
                except Exception:
                    pass

            page = context.new_page()
            from nlp2cmd.pipeline_runner_utils import _MarkdownConsoleWrapper

            console_wrapper = _MarkdownConsoleWrapper(console, enable_markdown=True)
            state = MultiActionState(
                page=page,
                context=context,
                url=str(url),
                schema_loader=schema_loader,
                console=console,
                console_wrapper=console_wrapper,
                confirm=confirm,
            )

            try:
                for i, action_spec in enumerate(actions):
                    action = action_spec.get("action")
                    action_t0 = time.perf_counter()
                    _debug(f"action[{i}]: executing '{action}' spec={action_spec}")

                    outcome = self._dispatch_legacy_multi_action(
                        state,
                        action,
                        action_spec,
                        i,
                    )
                    if outcome == "continue":
                        continue
                    if isinstance(outcome, RunnerResult):
                        return outcome

                    action_elapsed = (time.perf_counter() - action_t0) * 1000
                    _debug(f"action[{i}] '{action}' completed in {action_elapsed:.0f}ms")

                page.wait_for_timeout(2000)

                video_saved_path = None
                if video_recorder and video_recorder.is_recording:
                    try:
                        pw_video = page.video
                        if pw_video:
                            target = video_recorder.video_path or str(
                                Path(effective_video_dir) / "browser_automation.webm"
                            )
                            try:
                                pw_video.save_as(target)
                                video_saved_path = target
                            except Exception:
                                try:
                                    video_saved_path = pw_video.path()
                                except Exception:
                                    video_saved_path = None
                            if video_saved_path:
                                console.print(f"[green]🎥 Video saved: {video_saved_path}[/green]")
                    except Exception as ve:
                        _debug(f"Video save_as failed: {ve}")
                    video_recorder.stop_recording(console, saved_path=video_saved_path)

                browser.close()

                result_data: dict[str, Any] = {
                    "url": state.url,
                    "actions_executed": len(actions),
                    "extracted_count": len(state.extracted_data),
                }
                if video_saved_path:
                    result_data["video"] = video_saved_path
                return RunnerResult(success=True, kind="dom", data=result_data)

            except Exception as e:
                if video_recorder and video_recorder.is_recording:
                    try:
                        pw_video = page.video
                        if pw_video and video_recorder.video_path:
                            pw_video.save_as(video_recorder.video_path)
                            console.print(
                                f"[yellow]🎥 Partial video saved: {video_recorder.video_path}[/yellow]"
                            )
                    except Exception:
                        pass
                    video_recorder.stop_recording(console)

                browser.close()
                return RunnerResult(success=False, kind="dom", error=f"Multi-action execution failed: {e}")
