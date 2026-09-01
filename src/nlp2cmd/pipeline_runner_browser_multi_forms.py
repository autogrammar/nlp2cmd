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

class BrowserMultiFormMixin:
    """Form discovery/fill legacy actions."""

    def _legacy_multi_fill_form(
        self,
        state: MultiActionState,
        action_spec: dict[str, Any],
        action_index: int,
    ) -> ActionOutcome:
            # Automatic form filling from .env and data/*.json
            try:
                from nlp2cmd.web_schema.form_handler import FormHandler
                from nlp2cmd.web_schema.site_explorer import SiteExplorer
                
                form_handler = FormHandler(console=state.console, use_markdown=True)
                data_loader = state.schema_loader

                state.saw_fill_form_action = True
                
                # Wait for page to be fully loaded.
                # Try networkidle first (best for static sites), but fall back
                # to domcontentloaded for sites with persistent network activity
                # (analytics, chat widgets, websockets) that prevent networkidle.
                state.console_wrapper.print("⏳ Waiting for page to load...", language="text")
                try:
                    state.page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    # networkidle timed out — page has persistent connections
                    try:
                        state.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    except Exception:
                        pass  # proceed anyway, DOM is likely ready
                state.page.wait_for_timeout(1500)
                
                # Detect form fields
                state.console_wrapper.print("🔍 Detecting form fields...", language="text")
                fill_target = state.page
                fields = form_handler.detect_form_fields(fill_target)
                state.detected_form_fields = fields

                # If the state.page contains only junk fields (cookie/search/captcha/comments),
                # treat it as no form found and attempt discovery/navigation.
                fields = _filter_form_fields(fields, state.console_wrapper)
                state.detected_form_fields = fields
                
                if not fields:
                    state.console_wrapper.print("No form fields detected on this state.page", language="text")

                    try:
                        state.console_wrapper.print(
                            yaml.safe_dump(
                                {
                                    "status": "form_discovery_started",
                                    "strategy": "site_explorer",
                                    "max_depth": 2,
                                    "max_pages": 8,
                                    "url": state.url,
                                },
                                sort_keys=False,
                                allow_unicode=True,
                            ).rstrip(),
                            language="yaml",
                        )
                    except Exception:
                        pass

                    try:
                        explorer = SiteExplorer(max_depth=2, max_pages=8, headless=self.headless)
                        explore_result = explorer.find_form(
                            url=state.url,
                            intent="contact",
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
                            
                            # Retry form detection
                            state.console_wrapper.print("🔁 Retrying form field detection after exploration...", language="text")
                            fill_target = state.page
                            fields = form_handler.detect_form_fields(fill_target)
                            state.detected_form_fields = fields

                            fields = _filter_form_fields(fields, state.console_wrapper)
                            state.detected_form_fields = fields
                    except Exception as e:
                        state.console_wrapper.print(f"Site exploration failed: {e}", language="text")
                        # Fall through to simpler heuristic

                    # Fallback: simple heuristic - try to navigate to contact state.page
                    if not fields:
                        try:
                            # First try direct contact URLs (many sites hide menu items behind a hamburger).
                            try:
                                from state.urllib.parse import urljoin
                                base = str(state.page.url or state.url)
                            except Exception:
                                base = str(state.url)

                            direct_paths = [
                                "/kontakt",
                                "/kontakt/",
                                "/kontakt.html",
                                "/kontakt.php",
                                "/kontakt-i-dane",
                                "/kontakt-2",
                                "/kontakt-2/",
                                "/contact",
                                "/contact/",
                            ]

                            direct_attempts: list[dict[str, object]] = []
                            for pth in direct_paths:
                                if fields:
                                    break
                                try:
                                    cand_url = urljoin(base, pth)
                                    direct_attempt: dict[str, object] = {"candidate": cand_url}
                                    direct_attempts.append(direct_attempt)
                                    resp = state.page.goto(cand_url, wait_until="domcontentloaded", timeout=12000)
                                    state.page.wait_for_timeout(1200)
                                    self._dismiss_popups(state.page, state.schema_loader)

                                    # Some sites render the contact form only after JS hydration or scroll.
                                    try:
                                        state.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                                    except Exception:
                                        pass
                                    state.page.wait_for_timeout(900)

                                    try:
                                        direct_attempt["forms"] = int(
                                            state.page.evaluate("() => document.querySelectorAll('form').length")
                                        )
                                    except Exception:
                                        direct_attempt["forms"] = None

                                    try:
                                        direct_attempt["status"] = int(resp.status) if resp is not None else None
                                    except Exception:
                                        direct_attempt["status"] = None
                                    try:
                                        direct_attempt["final_url"] = str(state.page.url or "")
                                    except Exception:
                                        direct_attempt["final_url"] = ""
                                    try:
                                        direct_attempt["title"] = state.page.title() or ""
                                    except Exception:
                                        direct_attempt["title"] = ""

                                    fields = form_handler.detect_form_fields(state.page)
                                    state.detected_form_fields = fields
                                    fields = _filter_form_fields(fields, state.console_wrapper)
                                    state.detected_form_fields = fields
                                except Exception:
                                    try:
                                        if direct_attempts:
                                            direct_attempts[-1]["error"] = "goto_failed"
                                    except Exception:
                                        pass
                                    continue

                            try:
                                state.console_wrapper.print(
                                    yaml.safe_dump(
                                        {
                                            "status": "direct_contact_nav_attempts",
                                            "base": base,
                                            "attempts": direct_attempts,
                                        },
                                        sort_keys=False,
                                        allow_unicode=True,
                                    ).rstrip(),
                                    language="yaml",
                                )
                            except Exception:
                                pass

                            if fields:
                                clicked = True
                            else:
                                clicked = False

                            candidates = [
                                'a[href*="kontakt" i]',
                                'a:has-text("Kontakt")',
                                'a:has-text("Kontakt") >> visible=true',
                                'a:has-text("Contact")',
                                'a[href*="contact" i]',
                            ]

                            if not clicked:
                                for sel in candidates:
                                    try:
                                        loc = state.page.locator(sel).first
                                        if loc.count() > 0:
                                            loc.click(timeout=1500)
                                            state.page.wait_for_load_state("domcontentloaded", timeout=8000)
                                            state.page.wait_for_timeout(1200)
                                            clicked = True
                                            break
                                    except Exception:
                                        continue

                            if clicked:
                                state.console_wrapper.print("🔁 Retrying form field detection after navigating...", language="text")
                                fill_target = state.page
                                fields = form_handler.detect_form_fields(fill_target)
                                state.detected_form_fields = fields

                                fields = _filter_form_fields(fields, state.console_wrapper)
                                state.detected_form_fields = fields
                        except Exception:
                            pass

                    # If still no fields, check if there is a contact form inside an iframe.
                    if not fields:
                        try:
                            frames = list(getattr(state.page, "frames", []) or [])
                        except Exception:
                            frames = []

                        frame_attempts: list[dict[str, object]] = []
                        for fr in frames[1:]:
                            try:
                                fr_url = ""
                                try:
                                    fr_url = str(fr.url or "")
                                except Exception:
                                    fr_url = ""

                                frame_attempt: dict[str, object] = {"frame_url": fr_url}
                                frame_attempts.append(frame_attempt)

                                fr_fields = form_handler.detect_form_fields(fr)
                                fr_fields = _filter_form_fields(fr_fields, state.console_wrapper)
                                if fr_fields:
                                    fill_target = fr
                                    fields = fr_fields
                                    frame_attempt["found_fields"] = len(fr_fields)
                                    break
                                frame_attempt["found_fields"] = 0
                            except Exception as e:
                                frame_attempts.append({"error": str(e)})
                                continue

                        try:
                            state.console_wrapper.print(
                                yaml.safe_dump(
                                    {
                                        "status": "iframe_form_scan",
                                        "frames": len(frames),
                                        "attempts": frame_attempts,
                                        "selected": "frame" if fill_target is not state.page else "page",
                                    },
                                    sort_keys=False,
                                    allow_unicode=True,
                                ).rstrip(),
                                language="yaml",
                            )
                        except Exception:
                            pass

                    if not fields:
                        # Graceful fallback: some sites have a "Kontakt" state.page but no contact form
                        # (only a site-wide search form). In that case, extract contact info instead
                        # of failing hard.
                        contact_info: dict[str, object] = {"mailto": [], "tel": [], "emails": [], "phones": []}
                        try:
                            contact_info = state.page.evaluate(r"""() => {
                                const mailto = Array.from(document.querySelectorAll('a[href^="mailto:"]'))
                                    .map(a => (a.getAttribute('href') || '').trim())
                                    .filter(Boolean);
                                const tel = Array.from(document.querySelectorAll('a[href^="tel:"]'))
                                    .map(a => (a.getAttribute('href') || '').trim())
                                    .filter(Boolean);

                                const text = (document.body && (document.body.innerText || document.body.textContent)) ? (document.body.innerText || document.body.textContent) : '';

                                const emails = [];
                                const emailRe = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi;
                                let m;
                                while ((m = emailRe.exec(text)) !== null) {
                                    emails.push(m[0]);
                                    if (emails.length >= 20) break;
                                }

                                const phones = [];
                                const phoneRe = /\b(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}\b/g;
                                let p;
                                while ((p = phoneRe.exec(text)) !== null) {
                                    const cand = (p[0] || '').trim();
                                    if (!cand) continue;
                                    // Keep only plausible lengths
                                    const digits = cand.replace(/\D/g, '');
                                    if (digits.length < 7 || digits.length > 15) continue;
                                    phones.push(cand);
                                    if (phones.length >= 20) break;
                                }

                                const uniq = (arr) => Array.from(new Set(arr));
                                return {
                                    mailto: uniq(mailto),
                                    tel: uniq(tel),
                                    emails: uniq(emails),
                                    phones: uniq(phones),
                                };
                            }""")
                        except Exception:
                            contact_info = {"mailto": [], "tel": [], "emails": [], "phones": []}

                        try:
                            state.console_wrapper.print(
                                yaml.safe_dump(
                                    {
                                        "status": "no_contact_form_fallback_contact_info",
                                        "url": str(state.page.url or state.url),
                                        "contact_info": contact_info,
                                    },
                                    sort_keys=False,
                                    allow_unicode=True,
                                ).rstrip(),
                                language="yaml",
                            )
                        except Exception:
                            pass

                        return RunnerResult(
                            success=True,
                            kind="dom",
                            data={
                                "url": str(state.page.url or state.url),
                                "contact_info": contact_info,
                                "note": "No contact form detected; extracted contact info instead.",
                            },
                        )
                
                # Optional screenshot after form interaction (only if not in auto-confirm mode)
                if not state.confirm:
                    try:
                        default_screenshot_path = f"./screenshots/form_{get_timestamp()}.png"
                        should_screenshot, screenshot_path = ask_for_screenshot(state.console, default_screenshot_path)
                        if should_screenshot:
                            take_screenshot(state.page, screenshot_path, state.console)
                    except Exception:
                        pass  # Screenshot is optional, don't fail if it errors
                    
            except Exception as e:
                state.console_wrapper.print(f"fill_form failed: {e}", language="text")
                return RunnerResult(
                    success=False,
                    kind="dom",
                    error=f"fill_form error: {e}",
                    data={"url": state.url},
                )

