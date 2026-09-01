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

class BrowserMultiPersistMixin:
    """Persist extracted data from legacy multi-action runs."""

    def _legacy_multi_save_to_file(
        self,
        state: MultiActionState,
        action_spec: dict[str, Any],
        action_index: int,
    ) -> ActionOutcome:
            # Save extracted data to a file
            try:
                filename = action_spec.get("filename", "extracted_data.txt")
                file_format = action_spec.get("format", "txt")
                also_copy = bool(action_spec.get("also_copy") or action_spec.get("copy_to_clipboard"))
                also_print = bool(action_spec.get("also_print") or action_spec.get("print_to_terminal"))
                _debug(f"save_to_file: saving {len(state.extracted_data)} items to {filename}")

                if not state.extracted_data:
                    state.console_wrapper.print("⚠️  No data to save (extraction produced no results)", language="text")
                    return "continue"

                filepath = Path(filename)
                seen: set[str] = set()
                lines: list[str] = []

                def _is_bad_website(u: str) -> bool:
                    low = (u or "").strip().lower()
                    if not low:
                        return True
                    if not (low.startswith("http://") or low.startswith("https://")):
                        return True
                    bad = [
                        "oferteo.pl",
                        "apps.apple.com",
                        "play.google.com",
                        "itunes.apple.com",
                        "facebook.com",
                        "instagram.com",
                        "linkedin.com",
                        "twitter.com",
                        "x.com",
                        "youtube.com",
                        "tiktok.com",
                        "business.safety.google",
                        "policies.google.com",
                    ]
                    return any(b in low for b in bad)

                dicts = [it for it in state.extracted_data if isinstance(it, dict)]
                has_website_field = any("website" in it for it in dicts)
                has_real_websites = False
                if has_website_field:
                    for it in dicts:
                        try:
                            w = str(it.get("website") or "").strip()
                        except Exception:
                            w = ""
                        if w and not _is_bad_website(w):
                            has_real_websites = True
                            break

                for item in state.extracted_data:
                    if isinstance(item, dict):
                        candidate = ""
                        if has_website_field:
                            if has_real_websites:
                                # In company-website extraction mode, only write real external websites.
                                if item.get("website"):
                                    candidate = str(item.get("website") or "").strip()
                                else:
                                    candidate = ""
                            else:
                                # Fallback: profiles do not expose external websites. Save profile URLs instead.
                                if item.get("oferteo_url"):
                                    candidate = str(item.get("oferteo_url") or "").strip()
                                elif item.get("url"):
                                    candidate = str(item.get("url") or "").strip()
                                else:
                                    candidate = ""
                        elif item.get("url"):
                            candidate = str(item.get("url") or "").strip()
                        elif item.get("oferteo_url"):
                            candidate = str(item.get("oferteo_url") or "").strip()
                        else:
                            candidate = " ".join(str(v) for v in item.values()).strip()

                        if has_website_field and has_real_websites and _is_bad_website(candidate):
                            continue

                        if not candidate:
                            continue
                        key = candidate.lower()
                        if key in seen:
                            continue
                        seen.add(key)
                        lines.append(candidate)
                    else:
                        candidate = str(item).strip()
                        if not candidate:
                            continue
                        key = candidate.lower()
                        if key in seen:
                            continue
                        seen.add(key)
                        lines.append(candidate)

                filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")

                state.console_wrapper.print(f"💾 Saved {len(lines)} entries to {filepath.resolve()}", language="text")

                if also_print:
                    try:
                        state.console_wrapper.print("\n".join(lines), language="text")
                    except Exception as pe:
                        _debug(f"save_to_file: print failed: {pe}")

                if also_copy:
                    copied = False
                    copy_err = None
                    payload = ("\n".join(lines) + "\n").encode("utf-8")
                    try:
                        # Prefer Wayland
                        p = subprocess.Popen(
                            ["wl-copy"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE,
                        )
                        _, err = p.communicate(payload, timeout=3)
                        copied = p.returncode == 0
                        if not copied:
                            copy_err = (err or b"").decode("utf-8", errors="ignore")
                    except FileNotFoundError:
                        pass
                    except Exception as ce:
                        copy_err = str(ce)

                    if not copied:
                        try:
                            p = subprocess.Popen(
                                ["xclip", "-selection", "clipboard"],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE,
                            )
                            _, err = p.communicate(payload, timeout=3)
                            copied = p.returncode == 0
                            if not copied:
                                copy_err = (err or b"").decode("utf-8", errors="ignore")
                        except FileNotFoundError:
                            pass
                        except Exception as ce:
                            copy_err = str(ce)

                    if not copied:
                        try:
                            p = subprocess.Popen(
                                ["xsel", "--clipboard", "--input"],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE,
                            )
                            _, err = p.communicate(payload, timeout=3)
                            copied = p.returncode == 0
                            if not copied:
                                copy_err = (err or b"").decode("utf-8", errors="ignore")
                        except FileNotFoundError:
                            pass
                        except Exception as ce:
                            copy_err = str(ce)

                    if copied:
                        state.console_wrapper.print(
                            yaml.safe_dump(
                                {
                                    "status": "copied_to_clipboard",
                                    "lines": len(lines),
                                },
                                sort_keys=False,
                                allow_unicode=True,
                            ).rstrip(),
                            language="yaml",
                        )
                    else:
                        state.console_wrapper.print(
                            yaml.safe_dump(
                                {
                                    "status": "clipboard_copy_skipped",
                                    "reason": "no_clipboard_tool",
                                    "error": str(copy_err or ""),
                                },
                                sort_keys=False,
                                allow_unicode=True,
                            ).rstrip(),
                            language="yaml",
                        )

                state.console_wrapper.print(
                    yaml.safe_dump(
                        {
                            "status": "saved_to_file",
                            "filename": str(filepath.resolve()),
                            "entries": len(lines),
                        },
                        sort_keys=False, allow_unicode=True,
                    ).rstrip(),
                    language="yaml",
                )
                _debug(f"save_to_file: wrote {len(lines)} lines to {filepath.resolve()}")

            except Exception as e:
                return RunnerResult(success=False, kind="dom", error=f"Action {action_index}: Save to file failed: {e}")

    def _legacy_multi_save_to_csv(
        self,
        state: MultiActionState,
        action_spec: dict[str, Any],
        action_index: int,
    ) -> ActionOutcome:
            # Save extracted data to a CSV file
            try:
                filename = action_spec.get("filename", "companies.csv")
                _debug(f"save_to_csv: saving {len(state.extracted_data)} items to {filename}")

                if not state.extracted_data:
                    state.console_wrapper.print("⚠️  No data to save (extraction produced no results)", language="text")
                    return "continue"

                import csv
                from io import StringIO

                filepath = Path(filename)

                # Determine fieldnames from first item
                fieldnames = list(state.extracted_data[0].keys()) if state.extracted_data else ["name", "website"]

                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for item in state.extracted_data:
                        writer.writerow(item)

                state.console_wrapper.print(f"💾 Saved {len(state.extracted_data)} entries to CSV: {filepath.resolve()}", language="text")
                state.console_wrapper.print(
                    yaml.safe_dump(
                        {
                            "status": "saved_to_csv",
                            "filename": str(filepath.resolve()),
                            "entries": len(state.extracted_data),
                            "columns": fieldnames,
                        },
                        sort_keys=False, allow_unicode=True,
                    ).rstrip(),
                    language="yaml",
                )
                _debug(f"save_to_csv: wrote {len(state.extracted_data)} rows to {filepath.resolve()}")

            except Exception as e:
                return RunnerResult(success=False, kind="dom", error=f"Action {action_index}: Save to CSV failed: {e}")

