from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from rich.console import Console

from nlp2cmd.pipeline_runner_utils import (
    _debug,
    _filter_form_fields,
    _MarkdownConsoleWrapper,
    RunnerResult,
    get_timestamp,
    ask_for_screenshot,
    take_screenshot,
    VideoRecorder,
    ask_for_video_recording,
)
from nlp2cmd.utils.yaml_compat import yaml
from nlp2cmd.dom_actions import ActionDispatcher


from nlp2cmd.dom_actions import ActionResult

class BrowserDispatchMixin:
    """ActionDispatcher-based multi-action browser execution."""

    def _run_dom_multi_action_dispatch(
        self,
        payload: dict[str, Any],
        *,
        dry_run: bool,
        confirm: bool,
        web_url: Optional[str],
        video_fmt: Optional[str] = None,
        video_dir: Optional[str] = None,
    ) -> RunnerResult:
        """Execute multiple browser actions using the modular ActionDispatcher (v2).
        
        This method uses the ActionDispatcher to route actions to modular handlers.
        Falls back to legacy _run_dom_multi_action if no handler is registered.
        
        Args:
            payload: dom_dql.v1 payload with actions list
            dry_run: If True, don't actually execute
            confirm: If True, require confirmation for sensitive actions
            web_url: Base URL if not in payload
            video_fmt: Video format for recording
            video_dir: Directory for video recordings
            
        Returns:
            RunnerResult with success/failure and extracted data
        """
        actions = payload.get("actions", [])
        url = payload.get("url") or web_url
        
        if not url:
            return RunnerResult(success=False, kind="dom", error="Missing url for multi-action")
        
        if dry_run:
            return RunnerResult(
                success=True,
                kind="dom",
                data={"dry_run": True, "url": url, "actions": actions, "dispatcher": "v2"},
            )
        
        console = Console()
        console_wrapper = _MarkdownConsoleWrapper(console, enable_markdown=True)
        
        try:
            from playwright.sync_api import sync_playwright  # type: ignore
        except Exception as e:
            return RunnerResult(success=False, kind="dom", error=f"Playwright not available: {e}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            from nlp2cmd.web_schema.form_data_loader import FormDataLoader
            
            schema_loader = FormDataLoader(site=str(url))
            ctx_opts = schema_loader.get_browser_context_options()
            
            # Video recording setup (simplified - see _run_dom_multi_action for full impl)
            video_recorder = None
            _effective_video_dir = video_dir or "./recordings"
            
            if video_fmt:
                video_recorder = VideoRecorder(output_dir=_effective_video_dir)
                video_path = video_recorder.start_recording(name_prefix="browser_automation_v2")
                if video_path:
                    console.print(f"[dim]🎥 Recording: {video_path}[/dim]")
                    ctx_opts["record_video_dir"] = _effective_video_dir
                    ctx_opts["record_video_size"] = {"width": 1280, "height": 720}
            
            context = browser.new_context(**ctx_opts)
            page = context.new_page()
            
            # Accumulated data for save actions
            extracted_data: list[dict[str, str]] = []
            
            try:
                for i, action_spec in enumerate(actions):
                    action = action_spec.get("action")
                    _action_t0 = time.perf_counter()
                    _debug(f"action[{i}] (v2): executing '{action}' spec={action_spec}")
                    
                    # Try new dispatcher first, fallback to legacy if no handler
                    if ActionDispatcher.has_handler(action):
                        result = ActionDispatcher.dispatch(
                            action=action,
                            action_spec=action_spec,
                            page=page,
                            context=context,
                            url=url,
                            console=console_wrapper,
                            schema_loader=schema_loader,
                            extracted_data=extracted_data,
                        )
                    else:
                        # No modular handler yet - return error with fallback info
                        result = ActionResult(
                            success=False,
                            error=f"Action '{action}' not yet implemented in v2 dispatcher. Use legacy _run_dom_multi_action.",
                            should_continue=False
                        )
                    
                    _action_elapsed = (time.perf_counter() - _action_t0) * 1000
                    _debug(f"action[{i}] (v2) '{action}' completed in {_action_elapsed:.0f}ms")
                    
                    if not result.success:
                        browser.close()
                        return RunnerResult(
                            success=False,
                            kind="dom",
                            error=result.error,
                            data={"action_index": i, "action": action}
                        )
                    
                    if not result.should_continue:
                        break
                    
                    # Update URL if action returned new URL
                    if result.data and result.data.get("url"):
                        url = result.data["url"]
                
                # Cleanup
                browser.close()
                
                return RunnerResult(
                    success=True,
                    kind="dom",
                    data={
                        "url": url,
                        "actions_executed": len(actions),
                        "extracted_count": len(extracted_data),
                        "extracted_data": extracted_data,
                        "dispatcher": "v2",
                    },
                )
                
            except Exception as e:
                browser.close()
                return RunnerResult(
                    success=False,
                    kind="dom",
                    error=f"Multi-action v2 execution failed: {e}"
                )

