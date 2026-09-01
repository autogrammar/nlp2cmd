"""
Site Explorer - Automatic discovery of forms and pages on websites.

Algorytm eksploracji strony www:
1. Odwiedź stronę główną i zbierz linki z menu/nawigacji
2. Przeszukaj podstrony (max 2-3 poziomy) pod kątem formularzy
3. Zwróć URL strony zawierającej formularz
4. Cache'uj wyniki w site profile
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from typing import Any, Optional
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request

from nlp2cmd.web_schema.site_explorer_page import SiteExplorerPageMixin
from nlp2cmd.web_schema.site_explorer_types import (
    ARTICLE_KEYWORDS,
    BLOCKED_RESOURCE_PATTERNS,
    CONTACT_KEYWORDS,
    DOCS_FRAMEWORKS,
    DOCS_KEYWORDS,
    FORM_FIELD_KEYWORDS,
    PLATFORM_DOCS_URLS,
    PRODUCT_KEYWORDS,
    ExplorationResult,
    PageInfo,
    debug,
)

# Backward-compatible re-exports
__all__ = [
    "SiteExplorer",
    "quick_find_form",
    "quick_find_content",
    "ExplorationResult",
    "PageInfo",
]


class SiteExplorer(SiteExplorerPageMixin):
    """
    Explores website to find forms, contact pages, and other content.

    Usage:
        explorer = SiteExplorer()
        result = explorer.find_form(url="https://example.com", intent="contact")
        if result.success:
            print(f"Found form at: {result.form_url}")
    """

    CONTACT_KEYWORDS = CONTACT_KEYWORDS
    ARTICLE_KEYWORDS = ARTICLE_KEYWORDS
    PRODUCT_KEYWORDS = PRODUCT_KEYWORDS
    DOCS_KEYWORDS = DOCS_KEYWORDS
    FORM_FIELD_KEYWORDS = FORM_FIELD_KEYWORDS
    BLOCKED_RESOURCE_PATTERNS = BLOCKED_RESOURCE_PATTERNS
    PLATFORM_DOCS_URLS = PLATFORM_DOCS_URLS
    DOCS_FRAMEWORKS = DOCS_FRAMEWORKS

    def __init__(
        self,
        max_depth: int = 2,
        max_pages: int = 10,
        headless: bool = True,
        timeout_ms: int = 15000,
        dynamic_wait_ms: int = 500,
        block_resources: bool = True,
        max_retries: int = 3,
    ):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.dynamic_wait_ms = dynamic_wait_ms
        self.block_resources = block_resources
        self.max_retries = max_retries
        self._explored_urls: set[str] = set()
        self._max_sitemap_urls: int = 50
        self._timing_stats: list[dict[str, Any]] = []

    # ── Strategy 2: Resource Blocking ──────────────────────────────────
    @staticmethod
    def _setup_resource_blocking(context: Any) -> None:
        """Block images, fonts, video, CSS to speed up page loads (~70% faster)."""
        def _abort_heavy(route: Any) -> None:
            try:
                route.abort()
            except Exception:
                pass

        for pattern in BLOCKED_RESOURCE_PATTERNS:
            try:
                context.route(pattern, _abort_heavy)
            except Exception:
                pass
        debug("Resource blocking enabled")

    # ── Strategy 3: Smart URL Patterns ─────────────────────────────────
    def _resolve_platform_url(self, url: str, content_type: str) -> Optional[str]:
        """Try to resolve a direct URL for known platforms (GitHub, RTD, PyPI)."""
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()

        for platform, handlers in PLATFORM_DOCS_URLS.items():
            if platform in netloc:
                handler = handlers.get(content_type) or handlers.get("docs")
                if handler:
                    try:
                        resolved = handler(url)
                        if resolved:
                            debug(f"Platform shortcut: {platform} -> {resolved}")
                            return resolved
                    except Exception:
                        pass
        return None

    # ── Strategy 4: EPIPE Retry with Backoff ───────────────────────────
    def _goto_with_retry(self, page: Any, url: str) -> None:
        """Navigate to URL with exponential backoff on EPIPE / timeout errors."""
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                page.wait_for_timeout(self.dynamic_wait_ms)
                return
            except Exception as e:
                last_exc = e
                err_str = str(e).lower()
                is_retriable = any(kw in err_str for kw in [
                    "epipe", "broken pipe", "timeout", "net::err_",
                    "connection reset", "connection refused",
                ])
                if not is_retriable:
                    raise
                wait_ms = min(1000 * (2 ** attempt), 8000)
                debug(f"Retry {attempt + 1}/{self.max_retries} for {url} after {wait_ms}ms: {e}")
                page.wait_for_timeout(wait_ms)
        if last_exc:
            raise last_exc

    # ── Strategy 7: GitHub API Integration ─────────────────────────────
    @staticmethod
    def _try_github_api(url: str) -> Optional[str]:
        """Try to fetch README via GitHub API (no browser needed)."""
        parsed = urlparse(url)
        if "github.com" not in parsed.netloc:
            return None
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        if len(parts) < 2:
            return None
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        try:
            req = Request(api_url, headers={
                "Accept": "application/vnd.github.v3.raw",
                "User-Agent": "nlp2cmd/1.0",
            })
            with urlopen(req, timeout=5) as resp:
                content = resp.read().decode("utf-8", errors="replace")
                if len(content) > 50:
                    debug(f"GitHub API: fetched README ({len(content)} chars) for {owner}/{repo}")
                    return content
        except Exception as e:
            debug(f"GitHub API failed for {owner}/{repo}: {e}")
        return None

    # ── Strategy 8: Documentation Framework Detection ──────────────────
    def _detect_docs_framework(self, url: str, page_html: str = "") -> Optional[str]:
        """Detect documentation framework from URL or page HTML."""
        url_lower = url.lower()
        html_lower = page_html.lower() if page_html else ""
        combined = url_lower + " " + html_lower

        for framework, indicators in DOCS_FRAMEWORKS.items():
            if any(ind in combined for ind in indicators):
                debug(f"Detected docs framework: {framework} at {url}")
                return framework
        return None

    # ── Strategy 9: Timing Metrics ─────────────────────────────────────
    def _record_timing(self, url: str, phase: str, duration_ms: float) -> None:
        """Record timing metric for a phase."""
        entry = {"url": url, "phase": phase, "duration_ms": round(duration_ms, 1)}
        self._timing_stats.append(entry)
        if duration_ms > 5000:
            debug(f"⚠ SLOW {phase}: {url} took {duration_ms:.0f}ms")
        elif _DEBUG:
            debug(f"Timing {phase}: {url} = {duration_ms:.0f}ms")

    def get_timing_stats(self) -> list[dict[str, Any]]:
        """Return collected timing stats."""
        return list(self._timing_stats)
    def find_content(
        self,
        url: str,
        content_type: str = "article",
        search_term: Optional[str] = None,
        page: Optional[Any] = None,
        context: Optional[Any] = None,
        close_browser: bool = True,
    ) -> ExplorationResult:
        """
        Find content on the website (articles, products, docs, etc.).
        
        Args:
            url: Starting URL (homepage)
            content_type: Type of content to find (article, product, docs, etc.)
            search_term: Optional term to search for in content
            page: Optional existing Playwright page
            context: Optional existing Playwright context
            close_browser: Whether to close browser after exploration
        
        Returns:
            ExplorationResult with content URL or error
        """
        from playwright.sync_api import sync_playwright

        t0 = time.perf_counter()

        # Strategy 3: Try platform-specific URL shortcuts first
        platform_url = self._resolve_platform_url(url, content_type)
        if platform_url and platform_url != url:
            url = platform_url

        # Strategy 7: For GitHub docs, try API first (no browser needed)
        if content_type == "docs" and "github.com" in urlparse(url).netloc:
            readme_content = self._try_github_api(url)
            if readme_content:
                info = PageInfo(url=url, title=f"README ({urlparse(url).path})", score=10.0,
                                load_time_ms=(time.perf_counter() - t0) * 1000)
                self._record_timing(url, "github_api", info.load_time_ms)
                return ExplorationResult(
                    success=True, form_url=url, form_page=info, explored_pages=[info],
                )

        should_close_browser = False
        should_close_context = False
        
        try:
            if page is None:
                p = sync_playwright().start()
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                # Strategy 2: Block heavy resources
                if self.block_resources:
                    self._setup_resource_blocking(context)
                page = context.new_page()
                should_close_browser = True
                should_close_context = close_browser
            
            # Reset state
            self._explored_urls = set()
            self._timing_stats = []
            explored_pages: list[PageInfo] = []

            # Fast-path: try common contact URLs first (cheap and often works even
            # when menu extraction fails or homepage blocks link discovery).
            if content_type in ("contact", "form"):
                try:
                    parsed_base = urlparse(url)
                    base = f"{parsed_base.scheme}://{parsed_base.netloc}" if parsed_base.scheme and parsed_base.netloc else url
                    common_paths = [
                        "/kontakt",
                        "/kontakt/",
                        "/contact",
                        "/contact/",
                        "/kontakt-2",
                        "/kontakt-3",
                    ]
                    for pth in common_paths:
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        cand = self._normalize_url(urljoin(base, pth))
                        result = self._explore_recursive(
                            page=page,
                            url=cand,
                            depth=0,
                            intent=content_type,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and result.contact_field_count > 0:
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
                except Exception:
                    pass
            
            # Start exploration - first analyze the main page for links
            main_page_result = self._explore_recursive(
                page=page,
                url=url,
                depth=0,
                intent=content_type,
                explored_pages=explored_pages,
                base_domain=urlparse(url).netloc,
                search_term=search_term,
            )
            
            debug(f"Main page result: {main_page_result is not None}")
            if main_page_result:
                debug(f"Main page URL: {main_page_result.url}")
                debug(f"Main page has form: {main_page_result.has_form}, contact_fields: {main_page_result.contact_field_count}")
                debug(f"Main page links: {len(main_page_result.links)}")
            
            # If main page has the target content AND it's not contact intent, return it
            if main_page_result and self._has_content_type(main_page_result, content_type) and content_type != "contact":
                return ExplorationResult(
                    success=True,
                    form_url=main_page_result.url,  # Reuse field for content URL
                    form_page=main_page_result,
                    explored_pages=explored_pages,
                )
            
            # For contact intent, always explore contact links first even if main page has form
            if main_page_result and main_page_result.links and len(explored_pages) < self.max_pages:
                debug("Exploring links from main page")
                # Sort links by contact relevance
                contact_links = []
                other_links = []
                
                for link in main_page_result.links[:12]:  # Check more links from main page
                    if len(self._explored_urls) >= self.max_pages:
                        break
                    
                    link_lower = link.lower()
                    if self._is_contact_url(link_lower):
                        contact_links.append(link)
                    else:
                        other_links.append(link)
                
                debug(f"Found {len(contact_links)} contact links: {contact_links}")
                
                # Explore contact links first
                for link in contact_links[:5]:  # Check up to 5 contact links
                    if len(self._explored_urls) >= self.max_pages:
                        break
                    debug(f"Exploring contact link: {link}")
                    result = self._explore_recursive(
                        page=page,
                        url=link,
                        depth=1,
                        intent=content_type,
                        explored_pages=explored_pages,
                        base_domain=urlparse(url).netloc,
                        search_term=search_term,
                    )
                    if result and self._has_content_type(result, content_type):
                        debug(f"Found contact form at: {link}")
                        return ExplorationResult(
                            success=True,
                            form_url=result.url,
                            form_page=result,
                            explored_pages=explored_pages,
                        )
                
                # Then explore other links if no contact form found
                for link in other_links[:3]:  # Check up to 3 other links
                    if len(self._explored_urls) >= self.max_pages:
                        break
                    result = self._explore_recursive(
                        page=page,
                        url=link,
                        depth=1,
                        intent=content_type,
                        explored_pages=explored_pages,
                        base_domain=urlparse(url).netloc,
                        search_term=search_term,
                    )
                    if result and self._has_content_type(result, content_type):
                        return ExplorationResult(
                            success=True,
                            form_url=result.url,
                            form_page=result,
                            explored_pages=explored_pages,
                        )
            
            # No content found - return best candidate
            best_page = self._find_best_content_candidate(explored_pages, content_type, search_term)
            if best_page and self._has_content_type(best_page, content_type):
                return ExplorationResult(
                    success=True,
                    form_url=best_page.url,
                    form_page=best_page,
                    explored_pages=explored_pages,
                )
            
            return ExplorationResult(
                success=False,
                explored_pages=explored_pages,
                error=f"No {content_type} found after exploring {len(explored_pages)} pages",
            )
            
        finally:
            if should_close_context and context:
                context.close()
            if should_close_browser and page:
                try:
                    page.context.browser.close()
                except Exception:
                    pass

    def find_form(
        self,
        url: str,
        intent: str = "contact",
        page: Optional[Any] = None,  # Playwright page object
        context: Optional[Any] = None,  # Playwright context
        close_browser: bool = True,
    ) -> ExplorationResult:
        """
        Find a form on the website matching the intent.
        
        Args:
            url: Starting URL (homepage)
            intent: Type of form to find (contact, search, newsletter, etc.)
            page: Optional existing Playwright page (if None, creates new browser)
            context: Optional existing Playwright context
            close_browser: Whether to close browser after exploration
        
        Returns:
            ExplorationResult with form URL or error
        """
        from playwright.sync_api import sync_playwright

        t0 = time.perf_counter()

        should_close_browser = False
        should_close_context = False
        
        try:
            if page is None:
                p = sync_playwright().start()
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                # Strategy 2: Block heavy resources
                if self.block_resources:
                    self._setup_resource_blocking(context)
                page = context.new_page()
                should_close_browser = True
                should_close_context = close_browser
            
            # Reset state
            self._explored_urls = set()
            self._timing_stats = []
            explored_pages: list[PageInfo] = []

            # Fast-path: try common contact URLs first (cheap and often works even
            # when menu extraction fails or homepage blocks link discovery).
            if content_type in ("contact", "form"):
                try:
                    parsed_base = urlparse(url)
                    base = (
                        f"{parsed_base.scheme}://{parsed_base.netloc}"
                        if parsed_base.scheme and parsed_base.netloc
                        else url
                    )
                    common_paths = [
                        "/kontakt",
                        "/kontakt/",
                        "/contact",
                        "/contact/",
                        "/kontakt-2",
                        "/kontakt-3",
                    ]
                    for pth in common_paths:
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        cand = self._normalize_url(urljoin(base, pth))
                        result = self._explore_recursive(
                            page=page,
                            url=cand,
                            depth=0,
                            intent=content_type,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and result.contact_field_count > 0:
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
                except Exception:
                    pass

            try:
                sitemap_urls = self._get_sitemap_urls(url)
            except Exception:
                sitemap_urls = []

            if sitemap_urls:
                if intent == "contact":
                    debug(f"Found {len(sitemap_urls)} sitemap URLs, prioritizing contact links")
                    # For contact intent, prioritize contact URLs from sitemap
                    contact_sitemap_urls = []
                    other_sitemap_urls = []
                    
                    for u in sitemap_urls:
                        u_lower = u.lower()
                        # More strict contact detection - exclude article-like URLs
                        # Look for exact contact-related words, not partial matches
                        is_contact = any(
                            kw in u_lower.split('-') or kw in u_lower.split('/') 
                            for kw in ["kontakt", "contact", "formularz"]
                        )
                        # Only look for standalone "form" word, not part of other words
                        has_form_word = (
                            " form" in u_lower or u_lower.endswith("form") or 
                            u_lower.startswith("form") or " form/" in u_lower
                        ) and not any(word in u_lower for word in ["informacje", "platform", "transform"])
                        
                        is_contact = is_contact or has_form_word
                        is_article = any(kw in u_lower for kw in ["artykul", "article", "informacje", "news", "blog"])
                        
                        if is_contact and not is_article:
                            contact_sitemap_urls.append(u)
                        else:
                            other_sitemap_urls.append(u)
                    
                    debug(f"Contact sitemap URLs: {contact_sitemap_urls[:3]}")
                    
                    # Explore contact URLs first
                    for u in contact_sitemap_urls[:5]:
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        result = self._explore_recursive(
                            page=page,
                            url=u,
                            depth=0,
                            intent=intent,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and ((intent != "contact" and result.has_form) or (intent == "contact" and result.contact_field_count > 0)):
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
                    
                    # Then explore a few other URLs
                    for u in other_sitemap_urls[:3]:
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        result = self._explore_recursive(
                            page=page,
                            url=u,
                            depth=0,
                            intent=intent,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and ((intent != "contact" and result.has_form) or (intent == "contact" and result.contact_field_count > 0)):
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
                else:
                    # Original logic for non-contact intents
                    for u in sitemap_urls:
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        result = self._explore_recursive(
                            page=page,
                            url=u,
                            depth=0,
                            intent=intent,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and result.has_form:
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
            
            # Start exploration - use the same logic as find_content for contact intent
            if intent == "contact":
                debug(f"Using contact-aware exploration for {url}")
                # Use the same logic as find_content for contact
                main_page_result = self._explore_recursive(
                    page=page,
                    url=url,
                    depth=0,
                    intent=intent,
                    explored_pages=explored_pages,
                    base_domain=urlparse(url).netloc,
                )
                
                debug(f"Main page result: {main_page_result is not None}")
                if main_page_result:
                    debug(f"Main page URL: {main_page_result.url}")
                    debug(f"Main page has form: {main_page_result.has_form}, contact_fields: {main_page_result.contact_field_count}")
                    debug(f"Main page links: {len(main_page_result.links)}")
                
                # For contact intent, always explore contact links first even if main page has form
                if main_page_result and main_page_result.links and len(explored_pages) < self.max_pages:
                    debug("Exploring links from main page")
                    # Sort links by contact relevance
                    contact_links = []
                    other_links = []
                    
                    for link in main_page_result.links[:12]:  # Check more links from main page
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        
                        link_lower = link.lower()
                        if self._is_contact_url(link_lower):
                            contact_links.append(link)
                        else:
                            other_links.append(link)
                    
                    debug(f"Found {len(contact_links)} contact links: {contact_links}")
                    
                    # Explore contact links first
                    for link in contact_links[:5]:  # Check up to 5 contact links
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        debug(f"Exploring contact link: {link}")
                        result = self._explore_recursive(
                            page=page,
                            url=link,
                            depth=1,
                            intent=content_type,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and result.contact_field_count > 0:
                            debug(f"Found contact form at: {link}")
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
                    
                    # Then explore other links if no contact form found
                    for link in other_links[:3]:  # Check up to 3 other links
                        if len(self._explored_urls) >= self.max_pages:
                            break
                        result = self._explore_recursive(
                            page=page,
                            url=link,
                            depth=1,
                            intent=content_type,
                            explored_pages=explored_pages,
                            base_domain=urlparse(url).netloc,
                        )
                        if result and result.contact_field_count > 0:
                            return ExplorationResult(
                                success=True,
                                form_url=result.url,
                                form_page=result,
                                explored_pages=explored_pages,
                            )
            else:
                # Original logic for non-contact intents
                result = self._explore_recursive(
                    page=page,
                    url=url,
                    depth=0,
                    intent=intent,
                    explored_pages=explored_pages,
                    base_domain=urlparse(url).netloc,
                )
                
                if result and result.has_form:
                    return ExplorationResult(
                        success=True,
                        form_url=result.url,
                        form_page=result,
                        explored_pages=explored_pages,
                    )
            
            # No form found - return best candidate or failure
            best_page = self._find_best_form_candidate(explored_pages, intent)
            if best_page and ((intent != "contact" and best_page.has_form) or (intent == "contact" and best_page.contact_field_count > 0)):
                return ExplorationResult(
                    success=True,
                    form_url=best_page.url,
                    form_page=best_page,
                    explored_pages=explored_pages,
                )
            
            return ExplorationResult(
                success=False,
                explored_pages=explored_pages,
                error=f"No form found after exploring {len(explored_pages)} pages",
            )
            
        finally:
            if should_close_context and context:
                context.close()
            if should_close_browser and page:
                try:
                    page.context.browser.close()
                except Exception:
                    pass
    
    def _explore_recursive(
        self,
        page: Any,
        url: str,
        depth: int,
        intent: str,
        explored_pages: list[PageInfo],
        base_domain: str,
        search_term: Optional[str] = None,
    ) -> Optional[PageInfo]:
        """Recursively explore pages to find forms or content."""
        
        # Normalize URL
        url = self._normalize_url(url)
        
        # Skip if already explored or max limits reached
        if url in self._explored_urls:
            return None
        if len(self._explored_urls) >= self.max_pages:
            return None
        if depth > self.max_depth:
            return None
        
        # Check domain - stay on same domain
        parsed = urlparse(url)
        if parsed.netloc != base_domain:
            return None
        
        self._explored_urls.add(url)
        
        try:
            t_start = time.perf_counter()

            # Strategy 4: Navigate with EPIPE retry + exponential backoff
            self._goto_with_retry(page, url)
            
            # Try to dismiss popups first
            self._dismiss_popups(page)
            
            page_info = self._analyze_page(page, url)

            # Strategy 9: Record timing
            elapsed_ms = (time.perf_counter() - t_start) * 1000
            page_info.load_time_ms = elapsed_ms
            self._record_timing(url, "explore", elapsed_ms)

            explored_pages.append(page_info)
            
            # If target content found, return immediately (except for contact - we want to check contact links first)
            if self._has_content_type(page_info, intent) and intent != "contact":
                return page_info
            
            # For contact intent, always explore contact links first even if main page has form
            if intent == "contact":
                # Check if this page has contact-related URL - if yes, return it
                if self._is_contact_url(url.lower()) and page_info.contact_field_count > 0:
                    return page_info  # This is likely a contact page
                # Otherwise, continue exploring to find contact page even if current page has form
            elif page_info.has_form:
                return page_info  # For non-contact intents, return immediately
            
            # Otherwise explore linked pages
            if depth < self.max_depth:
                for link in page_info.links[:5]:  # Limit links per page
                    result = self._explore_recursive(
                        page=page,
                        url=link,
                        depth=depth + 1,
                        intent=intent,
                        explored_pages=explored_pages,
                        base_domain=base_domain,
                        search_term=search_term,
                    )
                    if not result:
                        continue

                    if intent == "contact":
                        if result.contact_field_count > 0:
                            return result
                    else:
                        if result.has_form or self._has_content_type(result, intent):
                            return result
            
            return None
            
        except Exception as e:
            debug(f"Playwright failed for {url}: {e}")
            # Strategy 10: Graceful degradation — try static scrape
            fallback = self._fallback_static_scrape(url)
            if fallback:
                explored_pages.append(fallback)
                return fallback
            return None
    def find_content_twophase(
        self,
        url: str,
        content_type: str = "article",
        search_term: Optional[str] = None,
        quick_timeout_ms: int = 5000,
        quick_max_pages: int = 5,
    ) -> ExplorationResult:
        """Phase 1: quick scan with short timeouts. Phase 2: deep dive on best candidates."""
        from playwright.sync_api import sync_playwright

        t0 = time.perf_counter()
        debug(f"Two-phase exploration: phase 1 (quick scan) for {url}")

        # Phase 1: Quick scan — short timeouts, few pages
        quick_explorer = SiteExplorer(
            max_depth=1,
            max_pages=quick_max_pages,
            headless=self.headless,
            timeout_ms=quick_timeout_ms,
            dynamic_wait_ms=200,
            block_resources=True,
            max_retries=1,
        )
        quick_result = quick_explorer.find_content(
            url=url, content_type=content_type, search_term=search_term,
        )

        phase1_ms = (time.perf_counter() - t0) * 1000
        self._record_timing(url, "twophase_quick", phase1_ms)

        if quick_result.success:
            debug(f"Two-phase: found in phase 1 ({phase1_ms:.0f}ms)")
            return quick_result

        # Phase 2: Deep dive on discovered links
        debug(f"Two-phase: phase 2 (deep dive) on {len(quick_result.explored_pages)} candidates")
        candidate_urls = []
        for pg in quick_result.explored_pages:
            candidate_urls.extend(pg.links[:3])

        if not candidate_urls:
            return quick_result

        # Deduplicate
        seen = set()
        unique_candidates = []
        for c in candidate_urls:
            norm = self._normalize_url(c)
            if norm not in seen:
                seen.add(norm)
                unique_candidates.append(norm)

        deep_explorer = SiteExplorer(
            max_depth=self.max_depth,
            max_pages=self.max_pages,
            headless=self.headless,
            timeout_ms=self.timeout_ms,
            dynamic_wait_ms=self.dynamic_wait_ms,
            block_resources=self.block_resources,
            max_retries=self.max_retries,
        )

        for cand_url in unique_candidates[:8]:
            deep_result = deep_explorer.find_content(
                url=cand_url, content_type=content_type, search_term=search_term,
            )
            if deep_result.success:
                total_ms = (time.perf_counter() - t0) * 1000
                self._record_timing(url, "twophase_deep", total_ms)
                debug(f"Two-phase: found in phase 2 ({total_ms:.0f}ms)")
                return deep_result

        total_ms = (time.perf_counter() - t0) * 1000
        self._record_timing(url, "twophase_fail", total_ms)
        return ExplorationResult(
            success=False,
            explored_pages=quick_result.explored_pages,
            error=f"Two-phase: no {content_type} found after {total_ms:.0f}ms",
        )

    # ── Strategy 6: Parallel Link Exploration ──────────────────────────
    def _explore_links_parallel(
        self,
        urls: list[str],
        content_type: str,
        max_workers: int = 3,
    ) -> list[PageInfo]:
        """Explore multiple URLs in parallel using static fallback (no browser)."""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results: list[PageInfo] = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(self._fallback_static_scrape, u): u for u in urls[:max_workers * 3]}
            for future in as_completed(futures, timeout=10):
                try:
                    info = future.result()
                    if info:
                        results.append(info)
                except Exception:
                    pass
        debug(f"Parallel scan: {len(results)}/{len(urls)} pages fetched")
        return results

    def explore(
        self,
        url: str,
        query: str,
        page: Optional[Any] = None,
        context: Optional[Any] = None,
        close_browser: bool = True,
    ) -> ExplorationResult:
        """Universal exploration - auto-detects intent from query."""
        intent = self._detect_intent_from_query(query)
        
        if intent == "contact":
            return self.find_form(url, intent="contact", page=page, context=context, close_browser=close_browser)
        elif intent in ["article", "product", "docs"]:
            return self.find_content(url, content_type=intent, page=page, context=context, close_browser=close_browser)
        else:
            return self._explore_generic(url, intent, query, page, context, close_browser)
    
    def _detect_intent_from_query(self, query: str) -> str:
        """Detect intent type from natural language query."""
        query_lower = query.lower()
        
        intent_keywords = {
            "contact": self.CONTACT_KEYWORDS,
            "article": self.ARTICLE_KEYWORDS,
            "product": self.PRODUCT_KEYWORDS,
            "docs": self.DOCS_KEYWORDS,
        }
        
        scores = {intent: sum(1 for kw in keywords if kw in query_lower) 
                  for intent, keywords in intent_keywords.items()}
        
        if scores:
            best = max(scores, key=scores.get)
            if scores[best] > 0:
                return best
        return "contact"
    
    def _explore_generic(self, url, intent, query, page, context, close_browser):
        """Generic exploration for any intent type."""
        from playwright.sync_api import sync_playwright
        
        should_close = False
        try:
            if page is None:
                p = sync_playwright().start()
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                if self.block_resources:
                    self._setup_resource_blocking(context)
                page = context.new_page()
                should_close = True
            
            self._explored_urls = set()
            explored_pages = []
            
            result = self._explore_recursive(
                page=page, url=url, depth=0, intent=intent,
                explored_pages=explored_pages,
                base_domain=urlparse(url).netloc,
                search_term=query,
            )
            
            intent_keywords = {
                "contact": self.CONTACT_KEYWORDS,
                "article": self.ARTICLE_KEYWORDS,
                "product": self.PRODUCT_KEYWORDS,
                "docs": self.DOCS_KEYWORDS,
            }
            keywords = intent_keywords.get(intent, [])
            
            best_page = max(
                explored_pages,
                key=lambda p: self._score_for_intent(p, intent, keywords, query),
                default=None
            )
            
            if best_page:
                return ExplorationResult(
                    success=True, form_url=best_page.url,
                    form_page=best_page, explored_pages=explored_pages
                )
            return ExplorationResult(
                success=False, explored_pages=explored_pages,
                error=f"No content found for '{intent}'"
            )
        finally:
            if should_close and context:
                context.close()
    
    def _score_for_intent(self, page_info, intent, keywords, query):
        """Score page for intent."""
        score = 0.0
        url_lower = page_info.url.lower()
        title_lower = page_info.title.lower()
        for kw in keywords:
            if kw in url_lower:
                score += 2.0
            if kw in title_lower:
                score += 1.5
        if intent == "contact" and page_info.has_form:
            score += 3.0
        return score


def quick_find_content(
    url: str,
    content_type: str = "article",
    search_term: Optional[str] = None,
    headless: bool = True,
) -> Optional[str]:
    """
    Quick helper to find content URL without managing browser.
    
    Returns:
        URL of page with content, or None if not found
    """
    explorer = SiteExplorer(headless=headless)
    result = explorer.find_content(url=url, content_type=content_type, search_term=search_term)
    return result.form_url if result.success else None


def quick_find_form(
    url: str,
    intent: str = "contact",
    headless: bool = True,
) -> Optional[str]:
    """
    Quick helper to find form URL without managing browser.
    
    Returns:
        URL of page with form, or None if not found
    """
    explorer = SiteExplorer(headless=headless)
    result = explorer.find_form(url=url, intent=intent)
    return result.form_url if result.success else None
