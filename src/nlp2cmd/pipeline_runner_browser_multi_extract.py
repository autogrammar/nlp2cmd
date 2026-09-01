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

class BrowserMultiExtractMixin:
    """Company website extraction legacy actions."""

    def _legacy_multi_extract_companies(
        self,
        state: MultiActionState,
        action_spec: dict[str, Any],
        action_index: int,
    ) -> ActionOutcome:
            # Navigate to each company profile and extract their external website
            try:
                _debug("extract_company_websites_deep: starting deep extraction")
                # Oferteo renders results dynamically; wait more robustly than domcontentloaded.
                try:
                    state.page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    state.page.wait_for_load_state("domcontentloaded", timeout=10000)
                state.page.wait_for_timeout(1200)

                # Dismiss popups first
                self._dismiss_popups(state.page, state.schema_loader)

                max_companies = action_spec.get("max_companies", 20)
                companies_data: list[dict[str, str]] = []
                base_url = state.page.url
                attempts: list[dict[str, object]] = []

                try:
                    _start_url = str(state.page.url or "")
                except Exception:
                    _start_url = ""
                try:
                    _start_path = urlparse(_start_url).path
                except Exception:
                    _start_path = ""

                # If we start on Oferteo homepage, we are likely on category tiles, not company listings.
                # Try a best-effort jump to a city listing (this command is specifically for Gdańsk).
                cur = ""
                try:
                    cur = str(state.page.url or "")
                except Exception:
                    cur = ""

                try:
                    cur_path = urlparse(cur).path or ""
                except Exception:
                    cur_path = ""

                _cond = ("oferteo.pl" in cur and cur_path in {"", "/"})
                if _cond:
                    for cand in [
                        "https://www.oferteo.pl/firmy/gdansk",
                        "https://www.oferteo.pl/firmy/gda%C5%84sk",
                        "https://www.oferteo.pl/firmy-gdansk",
                        "https://www.oferteo.pl/firmy-budowlane/gdansk",
                    ]:
                        attempt: dict[str, object] = {"candidate": cand}
                        attempts.append(attempt)
                        try:
                            resp = state.page.goto(cand, wait_until="domcontentloaded", timeout=15000)
                            state.page.wait_for_timeout(900)
                            self._dismiss_popups(state.page, state.schema_loader)

                            try:
                                status = int(resp.status) if resp is not None else None
                            except Exception:
                                status = None

                            try:
                                cur_after = str(state.page.url or "")
                            except Exception:
                                cur_after = ""

                            try:
                                firma_cnt = state.page.evaluate(
                                    r"""() => Array.from(document.querySelectorAll('a[href]'))
          .map(a => (a.getAttribute('href') || '').toLowerCase())
          .filter(h => h.includes('/firma')).length"""
                                )
                            except Exception:
                                firma_cnt = 0

                            try:
                                title = state.page.title() or ""
                            except Exception:
                                title = ""

                            attempt["status"] = status
                            attempt["final_url"] = cur_after
                            attempt["title"] = title
                            attempt["firma_links"] = firma_cnt
                            attempt["error"] = None

                            # accept the first candidate that navigates away from homepage successfully
                            if status is None or (isinstance(status, int) and status < 400):
                                if urlparse(cur_after).path.strip("/") != "":
                                    base_url = state.page.url
                                    break
                        except Exception as e:
                            attempt["error"] = str(e)
                            continue

                try:
                    state.console_wrapper.print(
                        yaml.safe_dump(
                            {
                                "status": "oferteo_nav_attempts",
                                "start_url": _start_url,
                                "start_path": _start_path,
                                "current_url": str(state.page.url or ""),
                                "condition": bool(locals().get("_cond", False)),
                                "attempts": attempts,
                            },
                            sort_keys=False,
                            allow_unicode=True,
                        ).rstrip(),
                        language="yaml",
                    )
                except Exception:
                    pass

                # If we start on the global catalog page, it may not show company profile links directly.
                # Jump to a city listing page to get real company profiles.
                try:
                    cur = str(state.page.url or "")
                    if "oferteo.pl" in cur and "/katalog-firm" in urlparse(cur).path:
                        state.page.goto("https://www.oferteo.pl/firmy/gdansk", wait_until="domcontentloaded", timeout=15000)
                        state.page.wait_for_timeout(1200)
                        self._dismiss_popups(state.page, state.schema_loader)
                        base_url = state.page.url
                except Exception:
                    pass

                # Best-effort: if we still are on the homepage, force the most likely listing URL.
                try:
                    if "oferteo.pl" in str(state.page.url or "") and urlparse(str(state.page.url or "")).path.strip("/") == "":
                        state.page.goto("https://www.oferteo.pl/firmy/gdansk", wait_until="domcontentloaded", timeout=15000)
                        state.page.wait_for_timeout(900)
                        self._dismiss_popups(state.page, state.schema_loader)
                        base_url = state.page.url
                except Exception:
                    pass

                # Wait for dynamically loaded company links to appear.
                # This avoids false negatives when the page is hydrated by JS after initial load.
                try:
                    start_t = time.time()
                    last_seen = 0
                    while (time.time() - start_t) < 15.0:
                        try:
                            cnt = state.page.evaluate(
                                r"""() => Array.from(document.querySelectorAll('a[href]'))
          .map(a => (a.getAttribute('href') || '').toLowerCase())
          .filter(h => h.includes('/firma')).length"""
                            )
                        except Exception:
                            cnt = 0

                        if isinstance(cnt, int) and cnt > 0:
                            _debug(f"extract_company_websites_deep: detected {cnt} '/firma/' links after wait")
                            break

                        # If the count is not growing, try a gentle scroll to trigger lazy loading.
                        if isinstance(cnt, int) and cnt == last_seen:
                            try:
                                state.page.evaluate("() => window.scrollBy(0, Math.max(600, window.innerHeight))")
                            except Exception:
                                pass
                        if isinstance(cnt, int):
                            last_seen = cnt
                        state.page.wait_for_timeout(900)
                except Exception:
                    pass

                # Find company profile links on the catalog state.page
                _debug("extract_company_websites_deep: finding company links")
                company_links: list[dict[str, str]] = []
                try:
                    from state.urllib.parse import urljoin
                except Exception:
                    urljoin = None

                def _collect_company_links() -> list[dict[str, str]]:
                    res = state.page.evaluate(r"""() => {
                        const links = [];
                        const seen = new Set();

                        // Prefer the main listings area if present
                        const roots = document.querySelectorAll('main, [role="main"], .results, .listing, #content, .companies, .firmy');
                        const root = roots.length > 0 ? roots[0] : document.body;

                        const allLinks = Array.from(root.querySelectorAll('a[href]'));
                        for (const el of allLinks) {
                            const href = (el.getAttribute('href') || '').trim();
                            const text = (el.textContent || '').trim().replace(/\s+/g, ' ');
                            if (!href || !text) continue;
                            if (text.length < 2 || text.length > 140) continue;
                            if (/^(#|javascript:|mailto:|tel:)/i.test(href)) continue;

                            const hrefLower = href.toLowerCase();
                            // Exclude categories/listings and noise
                            // Categories sometimes use /firma-... or /firmy-...
                            if (hrefLower.includes('/firma-')) continue;
                            if (hrefLower.includes('/firmy-')) continue;
                            if (hrefLower.includes('/firmy/')) continue;
                            if (hrefLower.includes('/katalog') || hrefLower.includes('/kategorie') || hrefLower.includes('/branze') || hrefLower.includes('/uslugi')) continue;
                            if (hrefLower.includes('facebook.com') || hrefLower.includes('instagram.com') || hrefLower.includes('linkedin.com')) continue;

                            // Company profiles: be flexible across portals
                            const looksLikeCompany = (
                                hrefLower.includes('/firma') ||
                                hrefLower.includes('/company/') ||
                                hrefLower.includes('/wykonawca') ||
                                hrefLower.includes('/profil')
                            );
                            if (!looksLikeCompany) continue;

                            if (seen.has(hrefLower)) continue;
                            seen.add(hrefLower);
                            links.push({name: text, href: href});
                        }

                        return links;
                    }""")
                    return res if isinstance(res, list) else []

                # Try multiple passes with scrolling to load more results
                try:
                    seen_hrefs: set[str] = set()
                    for pass_idx in range(4):
                        batch = _collect_company_links()
                        for item in batch:
                            if not isinstance(item, dict):
                                continue
                            name = str(item.get("name", "")).strip()
                            href = str(item.get("href", "")).strip()
                            if not name or not href:
                                continue

                            # Make URL absolute
                            if not href.startswith("http"):
                                from state.urllib.parse import urljoin
                                href = urljoin(base_url, href)

                            key = href.lower()
                            if key in seen_hrefs:
                                continue
                            seen_hrefs.add(key)
                            company_links.append({"name": name, "href": href})

                        if len(company_links) >= 120:
                            break

                        # Scroll to load more
                        try:
                            state.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                            state.page.wait_for_timeout(900)
                        except Exception:
                            break
                except Exception:
                    pass
                
                _debug(f"extract_company_websites_deep: raw company_links type={type(company_links)}, value={str(company_links)[:200]}")

                if not isinstance(company_links, list) or not company_links:
                    # For Oferteo, generic fallback is too noisy (categories, navigation, etc.).
                    # Fail fast so we don't save incorrect category URLs.
                    if "oferteo.pl" in str(state.page.url or ""):
                        try:
                            cur_url = str(state.page.url or "")
                        except Exception:
                            cur_url = ""
                        try:
                            cur_title = state.page.title() or ""
                        except Exception:
                            cur_title = ""

                        try:
                            sample = state.page.evaluate(
                                r"""() => {
                                    const hrefs = Array.from(document.querySelectorAll('a[href]'))
                                        .map(a => (a.getAttribute('href') || '').trim())
                                        .filter(h => h);
                                    const interesting = hrefs.filter(h => /firma|wykonawca|profil/i.test(h));
                                    const text = (document.body && document.body.innerText) ? document.body.innerText.toLowerCase() : '';
                                    const maybeBot = (text.includes('captcha') || text.includes('cloudflare') || text.includes('robot'));
                                    return {
                                        links_total: hrefs.length,
                                        interesting_sample: interesting.slice(0, 12),
                                        maybe_bot: maybeBot,
                                    };
                                }"""
                            )
                        except Exception:
                            sample = None

                        try:
                            state.console_wrapper.print(
                                yaml.safe_dump(
                                    {
                                        "status": "oferteo_no_profile_links",
                                        "url": cur_url,
                                        "title": cur_title,
                                        "attempts": attempts,
                                        "sample": sample,
                                    },
                                    sort_keys=False,
                                    allow_unicode=True,
                                ).rstrip(),
                                language="yaml",
                            )
                        except Exception:
                            pass

                        state.console_wrapper.print("⚠️  No /firma/ links found on Oferteo listing state.page", language="text")
                        return RunnerResult(
                            success=False,
                            kind="dom",
                            error="No company profile links found on Oferteo",
                            data={"url": cur_url, "title": cur_title, "attempts": attempts, "sample": sample},
                        )

                    _debug("extract_company_websites_deep: no company links found, trying fallback")
                    # Fallback: try to find any links that look like company profiles
                    company_links = state.page.evaluate(r"""() => {
                        const links = [];
                        const seen = new Set();
                        const allLinks = Array.from(document.querySelectorAll('a[href]'));
                        for (const el of allLinks) {
                            const href = el.getAttribute('href') || '';
                            const text = el.textContent.trim();
                            // Look for any non-empty link with reasonable text
                            if (!href || href.startsWith('#') || href.startsWith('javascript:')) continue;
                            if (!text || text.length < 3 || text.length > 80) continue;
                            // Skip common non-company links
                            if (href.includes('facebook') || href.includes('twitter') ||
                                href.includes('linkedin') || href.includes('instagram')) continue;
                            if (seen.has(href)) continue;
                            seen.add(href);
                            links.push({name: text, href: href});
                        }
                        return links.slice(0, 50);
                    }""")
                    _debug(f"extract_company_websites_deep: fallback found {len(company_links) if isinstance(company_links, list) else 0} links")

                if not isinstance(company_links, list) or not company_links:
                    state.console_wrapper.print("⚠️  No company links found on catalog state.page", language="text")
                    return RunnerResult(success=False, kind="dom", error="No company links found")

                _debug(f"extract_company_websites_deep: found {len(company_links)} potential companies")
                state.console_wrapper.print(f"🔍 Found {len(company_links)} company profiles to check", language="text")

                # Process profiles until we gather max_companies real websites
                target_websites = int(max_companies) if isinstance(max_companies, int) else 20
                # Keep this bounded so the whole run can finish under CLI timeouts.
                # We collect rows even when website is empty, so there's no need to scan huge lists.
                max_profiles_to_check = max(10, min(int(target_websites), 25))
                if isinstance(company_links, list):
                    state.console_wrapper.print(f"🔍 Found {len(company_links)} company profiles to check", language="text")

                # Always keep a fast fallback list of profile URLs.
                # Oferteo often doesn't expose external websites publicly; in that case we still want
                # to save >= max_companies profile URLs.
                profile_fallback: list[dict[str, str]] = []
                try:
                    _max_companies_int = int(max_companies)
                except Exception:
                    _max_companies_int = 20
                _max_companies_int = max(1, min(_max_companies_int, 200))

                for company in company_links[:_max_companies_int]:
                    try:
                        name = str(company.get("name", "")).strip()
                        href = str(company.get("href", "")).strip()
                        if not href:
                            continue
                        if not href.startswith("http"):
                            from state.urllib.parse import urljoin
                            href = urljoin(base_url, href)
                        profile_fallback.append({"name": name, "oferteo_url": href, "website": ""})
                    except Exception:
                        continue

                # Visit a small probe set of profiles and try to extract external websites.
                # (If this succeeds, save_to_file will write websites; otherwise it will write profile URLs.)
                target_websites = _max_companies_int
                action_deadline = time.time() + 85.0
                checked = 0
                probe_profiles = min(max_profiles_to_check, _max_companies_int)

                for idx, company in enumerate(company_links[:probe_profiles], 1):
                    try:
                        if time.time() >= action_deadline:
                            _debug("extract_company_websites_deep: time budget exceeded; stopping early")
                            break

                        checked += 1
                        name = str(company.get("name", "")).strip()
                        href = str(company.get("href", "")).strip()
                        if not name or not href:
                            continue

                        # Make URL absolute
                        if not href.startswith("http"):
                            from state.urllib.parse import urljoin
                            href = urljoin(base_url, href)

                        _debug(f"Processing {idx}/{min(len(company_links), max_profiles_to_check)}: {name}")
                        state.console_wrapper.print(f"[{idx}/{min(len(company_links), max_profiles_to_check)}] Checking: {name}", language="text")

                        # Navigate to company profile
                        state.page.goto(href, wait_until="domcontentloaded", timeout=7000)
                        state.page.wait_for_timeout(250)
                        self._dismiss_popups(state.page, state.schema_loader)

                        # Find external website link on the profile state.page
                        external_site = state.page.evaluate(r"""() => {
                            // Look for external website links (not social media)
                            const externalPatterns = [
                                'a[href^="http"]:not([href*="oferteo.pl"]):not([href*="facebook.com"]):not([href*="twitter.com"]):not([href*="instagram.com"]):not([href*="linkedin.com"]):not([href*="youtube.com"])',
                                // Sometimes Oferteo uses redirect links to external sites
                                'a[href*="oferteo.pl"][href*="redirect"]',
                                'a[href*="oferteo.pl"][href*="url="]',
                                '.website a', '.www a', '.company-website a',
                                'a.external-link', 'a[rel="nofollow"]',
                                '[data-website] a', '.biz-website a'
                            ];
                            for (const pattern of externalPatterns) {
                                const links = document.querySelectorAll(pattern);
                                for (const link of links) {
                                    const href = link.getAttribute('href');
                                    if (href && href.startsWith('http') && 
                                        !href.includes('oferteo.pl') &&
                                        !href.includes('facebook.com') &&
                                        !href.includes('google.com')) {
                                        return href;
                                    }

                                    // Allow oferteo redirects (decoded later in Python)
                                    if (href && href.includes('oferteo.pl') && (href.includes('redirect') || href.includes('url='))) {
                                        return href;
                                    }
                                }
                            }
                            // Try to find by text content
                            const allLinks = document.querySelectorAll('a[href^="http"]');
                            for (const link of allLinks) {
                                const href = link.getAttribute('href');
                                const text = link.textContent.toLowerCase();
                                if (href && !href.includes('oferteo.pl') && 
                                    (text.includes('www.') || text.includes('strona') || 
                                     text.includes('website') || text.includes('witryna'))) {
                                    return href;
                                }
                            }

                            // Last resort: find anything that looks like a domain in visible text
                            const bodyText = (document.body && document.body.innerText) ? document.body.innerText : '';
                            const m = bodyText.match(/\b([a-z0-9][a-z0-9\-]{0,62}\.)+[a-z]{2,}\b/i);
                            if (m && m[0]) {
                                return m[0];
                            }
                            return null;
                        }""")

                        # Filter out non-company websites (app stores, social, tracking)
                        if external_site and isinstance(external_site, str):
                            raw_ext = external_site.strip()
                            ext_low = raw_ext.lower()

                            # If it's a bare domain found in text, normalize to https://
                            if ext_low and (not ext_low.startswith("http")) and "." in ext_low and "/" not in ext_low:
                                raw_ext = f"https://{raw_ext}"
                                ext_low = raw_ext.lower()

                            # Decode oferteo redirect links if present
                            try:
                                from state.urllib.parse import parse_qs, unquote, urlparse

                                parsed = urlparse(raw_ext)
                                if "oferteo.pl" in (parsed.netloc or ""):
                                    qs = parse_qs(parsed.query or "")
                                    for key in ("url", "u", "target", "redirect"):
                                        if key in qs and qs[key]:
                                            cand = unquote(str(qs[key][0]))
                                            if cand.startswith("http"):
                                                raw_ext = cand
                                                ext_low = raw_ext.lower()
                                                break
                            except Exception:
                                pass

                            bad_domains = [
                                "apps.apple.com",
                                "play.google.com",
                                "itunes.apple.com",
                                "oferteo.pl",
                                "facebook.com",
                                "instagram.com",
                                "linkedin.com",
                                "twitter.com",
                                "x.com",
                                "youtube.com",
                                "tiktok.com",
                                "goo.gl",
                                "bit.ly",
                            ]
                            if any(b in ext_low for b in bad_domains):
                                external_site = None
                            else:
                                external_site = raw_ext

                        if external_site and isinstance(external_site, str):
                            companies_data.append({
                                "name": name,
                                "oferteo_url": href,
                                "website": external_site
                            })
                            state.console_wrapper.print(f"   ✓ Found website: {external_site}", language="text")
                            _debug(f"Found website for {name}: {external_site}")

                            # Stop early when we have enough real websites
                            real_websites = [c for c in companies_data if c.get("website")]
                            if len(real_websites) >= target_websites:
                                break
                        else:
                            state.console_wrapper.print(f"   ⚠ No external website found", language="text")
                            companies_data.append({
                                "name": name,
                                "oferteo_url": href,
                                "website": ""
                            })

                        # Go back to catalog (lighter than re-loading base_url each time)
                        try:
                            state.page.go_back(wait_until="domcontentloaded", timeout=9000)
                            state.page.wait_for_timeout(200)
                        except Exception:
                            state.page.goto(base_url, wait_until="domcontentloaded", timeout=15000)
                            state.page.wait_for_timeout(300)

                    except Exception as e:
                        _debug(f"Error processing company: {e}")
                        continue

                # If we didn't find any real websites, fall back to the listing profile URLs.
                # This guarantees that downstream save_to_file can write >= max_companies entries.
                try:
                    real_websites_cnt = len([c for c in companies_data if str(c.get("website") or "").strip()])
                except Exception:
                    real_websites_cnt = 0
                if real_websites_cnt == 0 and profile_fallback:
                    companies_data = profile_fallback

                _debug(f"extract_company_websites_deep: extracted {len(companies_data)} companies with websites")

                if not companies_data:
                    state.console_wrapper.print("⚠️  No company website data extracted", language="text")
                    return RunnerResult(success=False, kind="dom", error="No company website data extracted")

                # Store for save_to_csv action
                state.extracted_data.extend(companies_data)

                # Display results
                state.console_wrapper.print(f"\n✅ Extracted {len(companies_data)} companies with websites:", language="text")
                for c in companies_data[:10]:
                    website = c.get("website", "N/A")
                    state.console_wrapper.print(f"  • {c['name']}: {website}", language="text")
                if len(companies_data) > 10:
                    state.console_wrapper.print(f"  ... and {len(companies_data) - 10} more", language="text")

            except Exception as e:
                return RunnerResult(success=False, kind="dom", error=f"Action {action_index}: Deep company extraction failed: {e}")

