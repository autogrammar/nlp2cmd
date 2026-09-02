from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

from nlp2cmd.pipeline_runner_browser_multi_state import MultiActionState
from nlp2cmd.pipeline_runner_utils import (
    _debug,
    _filter_form_fields,
    RunnerResult,
    get_timestamp,
    ask_for_screenshot,
    take_screenshot,
)
from nlp2cmd.utils.yaml_compat import yaml

ActionOutcome = RunnerResult | Literal["continue"] | None

class BrowserMultiNavMixin:
    """Navigation and exploration actions for legacy multi-action runs."""

    def _legacy_multi_goto(self, state: MultiActionState, action_spec: dict[str, Any]) -> None:
            action_url = action_spec.get("url", state.url)
            state.page.goto(str(action_url), wait_until="domcontentloaded")
            state.page.wait_for_timeout(500)
            
            # Try to dismiss common popups/cookie consents
            self._dismiss_popups(state.page, state.schema_loader)

    def _legacy_multi_explore_content(
        self, state: MultiActionState, action_spec: dict[str, Any]
    ) -> None:
            # Explore site to find content
            try:
                from nlp2cmd.web_schema.site_explorer import SiteExplorer
                
                content_type = action_spec.get("content_type", "article")
                state.console_wrapper.print(f"🔍 Exploring site for {content_type}...", language="text")
                # Use smaller limits for docs to avoid timeouts
                max_pages = 2 if content_type == "docs" else 8
                max_depth = 1 if content_type == "docs" else 2
                explorer = SiteExplorer(max_depth=max_depth, max_pages=max_pages, headless=self.headless, timeout_ms=5000, dynamic_wait_ms=1000)
                
                # Don't close browser - reuse current state.context
                explore_result = explorer.find_content(
                    url=state.url,
                    content_type=content_type,
                    page=state.page,
                    context=state.context,
                    close_browser=False,
                )
                
                if explore_result.success and explore_result.form_url:
                    content_url = explore_result.form_url
                    state.console_wrapper.print(f"✓ Found {content_type} at: {content_url}", language="text")
                    
                    # Navigate to the discovered content state.page
                    if content_url != state.page.url:
                        state.page.goto(content_url, wait_until="domcontentloaded")
                        state.page.wait_for_timeout(1500)
                    
                    # Update URL for subsequent actions
                    state.url = content_url
                else:
                    state.console_wrapper.print(f"No {content_type} found during exploration", language="text")
            except Exception as e:
                state.console_wrapper.print(f"Content exploration failed: {e}", language="text")

    def _legacy_multi_explore_form(
        self, state: MultiActionState, action_spec: dict[str, Any]
    ) -> None:
            # Explore site to find forms before filling
            try:
                from nlp2cmd.web_schema.site_explorer import SiteExplorer
                
                intent = action_spec.get("intent", "contact")
                state.console_wrapper.print(f"🔍 Exploring site for {intent} form...", language="text")
                explorer = SiteExplorer(max_depth=2, max_pages=8, headless=self.headless)
                
                # Don't close browser - reuse current state.context
                explore_result = explorer.find_form(
                    url=state.url,
                    intent=intent,
                    page=state.page,
                    context=state.context,
                    close_browser=False,
                )
                
                if explore_result.success and explore_result.form_url:
                    form_url = explore_result.form_url
                    state.console_wrapper.print(f"✓ Found form at: {form_url}", language="text")
                    
                    # Navigate to the discovered form state.page
                    if form_url != state.page.url:
                        state.page.goto(form_url, wait_until="domcontentloaded")
                        state.page.wait_for_timeout(1500)
                    
                    # Update URL for subsequent actions
                    state.url = form_url
                else:
                    state.console_wrapper.print("No form found during exploration", language="text")
            except Exception as e:
                state.console_wrapper.print(f"Site exploration failed: {e}", language="text")

