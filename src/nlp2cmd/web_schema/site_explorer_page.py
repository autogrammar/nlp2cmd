"""Page analysis, scoring, and sitemap helpers for SiteExplorer."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Any, Optional
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request

try:
    from nlp2cmd.page_analysis import PageAnalyzer, PageAnalysisResult  # noqa: F401
    PAGE_ANALYSIS_AVAILABLE = True
except ImportError:
    PAGE_ANALYSIS_AVAILABLE = False

from nlp2cmd.web_schema.site_explorer_types import (
    CONTACT_KEYWORDS,
    ARTICLE_KEYWORDS,
    PRODUCT_KEYWORDS,
    DOCS_KEYWORDS,
    FORM_FIELD_KEYWORDS,
    PageInfo,
    debug,
)


class SiteExplorerPageMixin:
    """Page-level analysis helpers mixed into SiteExplorer."""

    @staticmethod
    def _fallback_static_scrape(url: str, timeout: int = 5) -> Optional[PageInfo]:
        """Fallback: fetch page with urllib (no JS) when Playwright fails."""
        try:
            req = Request(url, headers={"User-Agent": "nlp2cmd/1.0 (static fallback)"})
            with urlopen(req, timeout=timeout) as resp:
                html = resp.read().decode("utf-8", errors="replace")

            info = PageInfo(url=url)

            # Extract title
            m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if m:
                info.title = m.group(1).strip()

            # Count form fields
            inputs = len(re.findall(r'<input\b', html, re.IGNORECASE))
            textareas = len(re.findall(r'<textarea\b', html, re.IGNORECASE))
            info.form_count = inputs + textareas
            info.has_form = info.form_count > 0

            # Extract links
            for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
                href = m.group(1)
                if href.startswith(("http://", "https://")):
                    info.links.append(href)
                elif href.startswith("/"):
                    info.links.append(urljoin(url, href))
            info.links = info.links[:20]

            debug(f"Static fallback OK: {url} title='{info.title[:40]}' forms={info.form_count} links={len(info.links)}")
            return info
        except Exception as e:
            debug(f"Static fallback failed for {url}: {e}")
            return None
    def _analyze_page(self, page: Any, url: str, console: Optional[Any] = None) -> PageInfo:
        """Analyze a page for forms, iframes, and links."""
        info = PageInfo(url=url)

        try:
            info.title = page.title() or ""
        except Exception:
            pass

        # Look for forms/fields
        try:
            inputs = page.query_selector_all('input:not([type="hidden"])')
            textareas = page.query_selector_all('textarea')
            selects = page.query_selector_all('select')

            info.form_count = len(inputs) + len(textareas) + len(selects)
            info.has_form = info.form_count > 0
        except Exception:
            inputs = []
            textareas = []
            selects = []
            info.form_count = 0
            info.has_form = False

        # Compute contact-like vs junk fields for contact intent.
        # This helps avoid false positives (search boxes, cookie consent toggles,
        # comment forms, captcha-only pages).
        try:
            field_nodes = []
            try:
                field_nodes.extend(inputs[:30])
            except Exception:
                field_nodes.extend(inputs)
            try:
                field_nodes.extend(textareas[:15])
            except Exception:
                field_nodes.extend(textareas)

            def _is_junk_desc(field_type: str, name: str, fid: str, placeholder: str, aria: str) -> bool:
                ft = (field_type or "").strip().lower()
                n = (name or "").strip().lower()
                i = (fid or "").strip().lower()
                p = (placeholder or "").strip().lower()
                a = (aria or "").strip().lower()
                hay = " ".join([n, i, p, a])

                if ft == "search" or n in {"s", "q", "search", "query"}:
                    return True
                if "search" in hay or "szukaj" in hay or "wyszuki" in hay:
                    return True

                if "cookie" in hay or "consent" in hay:
                    return True
                if i.startswith("cky") or "cky" in hay:
                    return True
                if i.startswith("cmplz") or "cmplz" in hay:
                    return True

                if "captcha" in hay or "recaptcha" in hay or "g-recaptcha" in hay or "hcaptcha" in hay:
                    return True

                if n.startswith("apbct__") or "cleantalk" in hay:
                    return True

                if "comment" in hay or n in {"author", "email", "url"}:
                    return True

                return False

            def _is_contact_desc(field_type: str, name: str, fid: str, placeholder: str, aria: str) -> bool:
                ft = (field_type or "").strip().lower()
                n = (name or "").strip().lower()
                i = (fid or "").strip().lower()
                p = (placeholder or "").strip().lower()
                a = (aria or "").strip().lower()
                hay = " ".join([n, i, p, a])

                if _is_junk_desc(field_type, name, fid, placeholder, aria):
                    return False

                if ft in {"email", "tel"}:
                    return True
                if ft == "textarea":
                    return True

                tokens = [
                    "email",
                    "e-mail",
                    "mail",
                    "telefon",
                    "phone",
                    "wiadomo",
                    "message",
                    "temat",
                    "subject",
                    "imi",
                    "name",
                ]
                return any(t in hay for t in tokens)

            for node in field_nodes:
                try:
                    tag = (node.evaluate('el => el.tagName.toLowerCase()') or "").strip().lower()
                except Exception:
                    tag = ""
                try:
                    ftype = (node.get_attribute('type') or ("textarea" if tag == "textarea" else "text"))
                except Exception:
                    ftype = "text"
                try:
                    name = node.get_attribute('name') or ""
                except Exception:
                    name = ""
                try:
                    fid = node.get_attribute('id') or ""
                except Exception:
                    fid = ""
                try:
                    placeholder = node.get_attribute('placeholder') or ""
                except Exception:
                    placeholder = ""
                try:
                    aria = node.get_attribute('aria-label') or ""
                except Exception:
                    aria = ""

                if _is_junk_desc(str(ftype), name, fid, placeholder, aria):
                    info.junk_field_count += 1
                if _is_contact_desc(str(ftype), name, fid, placeholder, aria):
                    info.contact_field_count += 1
        except Exception:
            pass
        
        # Check for forms inside iframes (common for contact widgets)
        if not info.has_form:
            try:
                iframes = page.query_selector_all('iframe')
                for i, iframe in enumerate(iframes[:3]):  # Check first 3 iframes
                    try:
                        frame = iframe.content_frame()
                        if frame:
                            # Count inputs in iframe
                            iframe_inputs = frame.query_selector_all('input:not([type="hidden"])')
                            iframe_textareas = frame.query_selector_all('textarea')
                            if len(iframe_inputs) > 0 or len(iframe_textareas) > 0:
                                info.has_form = True
                                info.form_count += len(iframe_inputs) + len(iframe_textareas)
                                break
                    except Exception:
                        continue
            except Exception:
                pass
        
        # Score page based on content
        info.score = self._score_page(page, url, info)
        
        # Extract links for further exploration
        try:
            selector_groups = [
                'nav a[href], header a[href], [role="navigation"] a[href]',
                'footer a[href]',
                'a[href]',
            ]
            for sel in selector_groups:
                links = page.query_selector_all(sel)
                for link in links:
                    try:
                        href = link.get_attribute('href')
                        if href:
                            absolute_url = urljoin(url, href)
                            parsed = urlparse(absolute_url)
                            if parsed.netloc == urlparse(url).netloc:
                                if not any(absolute_url.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.mp4']):
                                    info.links.append(absolute_url)
                    except Exception:
                        continue
        except Exception:
            pass
        
        # Remove duplicates but preserve order
        seen = set()
        unique_links = []
        for link in info.links:
            normalized = self._normalize_url(link)
            if normalized not in seen:
                seen.add(normalized)
                unique_links.append(normalized)
        info.links = unique_links[:10]  # Limit links
        
        return info
    
    def _analyze_page_dispatch(self, page: Any, url: str, console: Optional[Any] = None) -> PageInfo:
        """New page analysis using modular PageAnalyzer.
        
        This is the refactored version that uses the page_analysis package.
        Falls back to legacy _analyze_page if modular version unavailable.
        """
        if not PAGE_ANALYSIS_AVAILABLE:
            return self._analyze_page(page, url, console)
        
        try:
            from nlp2cmd.page_analysis import PageAnalyzer
            
            analyzer = PageAnalyzer(max_links=10)
            result = analyzer.analyze(page, url)
            
            # Convert PageAnalysisResult to PageInfo
            info = PageInfo(url=url)
            info.title = result.title
            info.has_form = result.has_form
            info.form_count = result.form_count
            info.links = result.links
            info.score = result.score
            
            # Copy field classification counts
            info.contact_field_count = result.contact_field_count
            info.junk_field_count = result.junk_field_count
            
            return info
            
        except Exception as e:
            debug(f"PageAnalyzer failed: {e}, falling back to legacy")
            return self._analyze_page(page, url, console)
    
    def _dismiss_popups(self, page: Any) -> None:
        """Try to dismiss common popups and cookie consents."""
        dismiss_selectors = [
            'button:has-text("Accept all")',
            'button:has-text("Akceptuj wszystko")',
            'button:has-text("Zaakceptuj")',
            'button:has-text("Accept")',
            'button:has-text("Zgadzam się")',
            'button:has-text("Zgadzam sie")',
            'button:has-text("I agree")',
            'button:has-text("OK")',
            'button[aria-label*="Accept"]',
            'button[aria-label*="Akceptuj"]',
            '[data-testid="cookie-accept"]',
            '.cookie-accept',
            '#onetrust-accept-btn-handler',
        ]
        
        for selector in dismiss_selectors:
            try:
                page.wait_for_selector(selector, state="visible", timeout=1500)
                page.click(selector, timeout=1500)
                page.wait_for_timeout(500)
                break
            except Exception:
                continue
    
    def _score_page(self, page: Any, url: str, info: PageInfo, intent: str = "contact") -> float:
        """Score page relevance for finding content."""
        score = 0.0
        url_lower = url.lower()
        title_lower = info.title.lower()
        
        # Choose keyword set based on intent
        if intent == "contact":
            keywords = CONTACT_KEYWORDS
        elif intent == "article":
            keywords = ARTICLE_KEYWORDS
        elif intent == "product":
            keywords = PRODUCT_KEYWORDS
        elif intent == "docs":
            keywords = DOCS_KEYWORDS
        else:
            keywords = CONTACT_KEYWORDS  # Default
        
        # URL contains intent keywords
        for kw in keywords:
            if kw in url_lower:
                score += 2.0
        
        # Title contains intent keywords
        for kw in keywords:
            if kw in title_lower:
                score += 1.5
        
        # Special scoring for different content types
        if intent == "contact" and info.has_form:
            score += 4.0  # Increased boost for forms
            # Check for email/phone fields (strong indicator of contact form)
            try:
                page_html = page.content().lower()
                indicators = FORM_FIELD_KEYWORDS + ["required", "wyslij", "wyślij", "submit"]
                for kw in indicators:
                    if kw in page_html:
                        score += 0.5
            except Exception:
                pass
        elif intent == "article":
            # Check for article-like content
            try:
                page_html = page.content().lower()
                article_indicators = ["<article", "<h1", "<h2", "blog", "news", "post"]
                for indicator in article_indicators:
                    if indicator in page_html:
                        score += 0.3
            except Exception:
                pass
        elif intent == "product":
            # Check for product indicators
            try:
                page_html = page.content().lower()
                product_indicators = ["price", "cena", "buy", "kup", "cart", "koszyk", "shop"]
                for indicator in product_indicators:
                    if indicator in page_html:
                        score += 0.3
            except Exception:
                pass
        elif intent == "docs":
            # Check for documentation indicators
            try:
                page_html = page.content().lower()
                docs_indicators = ["documentation", "docs", "manual", "guide", "tutorial", "faq"]
                for indicator in docs_indicators:
                    if indicator in page_html:
                        score += 0.3
            except Exception:
                pass
        
        return score
    
    @staticmethod
    def _is_contact_url(url_lower: str) -> bool:
        """Check if a lowered URL looks like a contact/form page.

        Avoids false positives from words like 'informacje', 'platform', 'transform'.
        """
        # Direct keyword hits
        if any(kw in url_lower for kw in ["kontakt", "contact", "formularz"]):
            return True
        # Standalone "form" (not inside other words)
        has_form_word = (
            "/form" in url_lower or url_lower.endswith("/form")
            or "-form" in url_lower or "form-" in url_lower
        ) and not any(w in url_lower for w in ["informacje", "platform", "transform", "perform", "reform"])
        return has_form_word

    def _find_best_form_candidate(
        self,
        pages: list[PageInfo],
        intent: str,
    ) -> Optional[PageInfo]:
        """Find the best page with form based on scores."""
        # Filter pages with forms
        form_pages = [p for p in pages if p.has_form]
        if not form_pages:
            return None
        
        # Prioritize pages with contact-related URLs for contact intent
        if intent == "contact":
            contact_urls = [p for p in form_pages if self._is_contact_url(p.url.lower())]
            if contact_urls:
                form_pages = contact_urls
        
        # Sort by score descending
        form_pages.sort(key=lambda p: p.score, reverse=True)
        return form_pages[0]
    
    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL for comparison."""
        # Remove fragment
        url = url.split('#')[0]
        # Remove trailing slash
        url = url.rstrip('/')
        return url

    def _get_sitemap_urls(self, base_url: str) -> list[str]:
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            return []

        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

        try:
            with urlopen(sitemap_url, timeout=max(1, int(self.timeout_ms / 1000))) as resp:
                raw = resp.read()
        except Exception:
            return []

        try:
            root = ET.fromstring(raw)
        except Exception:
            return []

        ns = ""
        if root.tag.startswith("{") and "}" in root.tag:
            ns = root.tag.split("}", 1)[0] + "}"

        urls: list[str] = []

        if root.tag.endswith("sitemapindex"):
            for sm in root.findall(f"{ns}sitemap"):
                loc = sm.find(f"{ns}loc")
                if loc is None or not (loc.text or "").strip():
                    continue
                sm_url = (loc.text or "").strip()
                try:
                    with urlopen(sm_url, timeout=max(1, int(self.timeout_ms / 1000))) as resp:
                        sm_raw = resp.read()
                    sm_root = ET.fromstring(sm_raw)
                except Exception:
                    continue

                sm_ns = ""
                if sm_root.tag.startswith("{") and "}" in sm_root.tag:
                    sm_ns = sm_root.tag.split("}", 1)[0] + "}"

                for u in sm_root.findall(f"{sm_ns}url"):
                    loc2 = u.find(f"{sm_ns}loc")
                    if loc2 is None:
                        continue
                    txt = (loc2.text or "").strip()
                    if not txt:
                        continue
                    if urlparse(txt).netloc != parsed.netloc:
                        continue
                    urls.append(txt)
                    if len(urls) >= self._max_sitemap_urls:
                        break
                if len(urls) >= self._max_sitemap_urls:
                    break
        else:
            for u in root.findall(f"{ns}url"):
                loc = u.find(f"{ns}loc")
                if loc is None:
                    continue
                txt = (loc.text or "").strip()
                if not txt:
                    continue
                if urlparse(txt).netloc != parsed.netloc:
                    continue
                urls.append(txt)
                if len(urls) >= self._max_sitemap_urls:
                    break

        if not urls:
            return []

        def _score_url(u: str) -> float:
            ul = u.lower()
            s = 0.0
            for kw in CONTACT_KEYWORDS:
                if kw in ul:
                    s += 2.0
            if any(x in ul for x in ["kontakt", "contact", "formularz", "form", "wiadomosc", "wiadomość"]):
                s += 2.0
            if any(x in ul for x in ["tel", "email", "mail"]):
                s += 1.0
            return s

        urls = sorted(urls, key=_score_url, reverse=True)
        return urls[: self._max_sitemap_urls]

    def _has_content_type(self, page_info: PageInfo, content_type: str) -> bool:
        """Check if page has specific content type."""
        if content_type in ["contact", "form"]:
            return page_info.has_form
        
        intent_keywords = {
            "article": ARTICLE_KEYWORDS,
            "product": PRODUCT_KEYWORDS,
            "docs": DOCS_KEYWORDS,
        }
        keywords = intent_keywords.get(content_type, [])
        url_lower = page_info.url.lower()
        title_lower = page_info.title.lower()
        
        for kw in keywords:
            if kw in url_lower or kw in title_lower:
                return True
        return False
    
    def _find_best_content_candidate(
        self,
        pages: list[PageInfo],
        content_type: str,
        search_term: Optional[str] = None,
    ) -> Optional[PageInfo]:
        """Find best page for content type."""
        intent_keywords = {
            "article": ARTICLE_KEYWORDS,
            "product": PRODUCT_KEYWORDS,
            "docs": DOCS_KEYWORDS,
        }
        keywords = intent_keywords.get(content_type, [])
        
        best_page = None
        best_score = -1.0
        
        for p in pages:
            score = 0.0
            url_lower = p.url.lower()
            title_lower = p.title.lower()
            
            for kw in keywords:
                if kw in url_lower:
                    score += 2.0
                if kw in title_lower:
                    score += 1.5
            
            if search_term:
                st_lower = search_term.lower()
                if st_lower in url_lower:
                    score += 3.0
                if st_lower in title_lower:
                    score += 2.0
            
            if score > best_score:
                best_score = score
                best_page = p
        
        return best_page

