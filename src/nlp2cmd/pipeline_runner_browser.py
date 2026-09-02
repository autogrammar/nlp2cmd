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


class BrowserExecutionMixin:
    """DOM/browser execution methods for PipelineRunner."""

    def _run_dom_dql(
        self,
        dql_json: str,
        *,
        dry_run: bool,
        confirm: bool,
        web_url: Optional[str],
        video_fmt: Optional[str] = None,
        video_dir: Optional[str] = None,
    ) -> RunnerResult:
        try:
            payload = json.loads(dql_json)
        except Exception as e:
            return RunnerResult(success=False, kind="dom", error=f"Invalid dom_dql.v1 JSON: {e}")

        if not isinstance(payload, dict) or payload.get("dsl") != "dom_dql.v1":
            return RunnerResult(success=False, kind="dom", error="Unsupported dom DQL payload")

        # Check if this is a multi-action sequence
        actions = payload.get("actions")
        if actions and isinstance(actions, list):
            return self._run_dom_multi_action(payload, dry_run=dry_run, confirm=confirm, web_url=web_url,
                                               video_fmt=video_fmt, video_dir=video_dir)

        url = payload.get("url") or web_url
        action = str(payload.get("action") or "")
        target = payload.get("target") or {}
        selector = str((target or {}).get("value") or "")

        if not url:
            return RunnerResult(success=False, kind="dom", error="Missing url for dom action")
        if not action:
            return RunnerResult(success=False, kind="dom", error="Missing action")
        if action not in {"goto", "navigate"} and not selector:
            return RunnerResult(success=False, kind="dom", error="Missing target selector")

        params = payload.get("params") or {}
        if dry_run:
            return RunnerResult(
                success=True,
                kind="dom",
                data={"dry_run": True, "url": url, "action": action, "selector": selector, "params": params},
            )

        if action in {"click", "type", "select"} and not confirm:
            pass

        try:
            from playwright.sync_api import sync_playwright  # type: ignore
        except Exception as e:
            return RunnerResult(success=False, kind="dom", error=f"Playwright not available: {e}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            if action in {"goto", "navigate"}:
                page.goto(str(url))
                page.wait_for_timeout(250)
            else:
                page.goto(str(url))
                page.wait_for_timeout(250)

                locator = page.locator(selector).first

                if action == "click":
                    locator.click()
                elif action == "type":
                    value = (params or {}).get("value")
                    if value is None:
                        return RunnerResult(success=False, kind="dom", error="Missing params.value for type")
                    locator.fill(str(value))
                elif action == "select":
                    value = (params or {}).get("value")
                    if value is None:
                        return RunnerResult(success=False, kind="dom", error="Missing params.value for select")
                    locator.select_option(str(value))
                else:
                    return RunnerResult(success=False, kind="dom", error=f"Unsupported dom action: {action}")

            browser.close()

        return RunnerResult(success=True, kind="dom", data={"url": url, "action": action, "selector": selector})
    
