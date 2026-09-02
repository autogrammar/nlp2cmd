"""Types, constants, and platform URL helpers for site exploration."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlparse

_DEBUG = os.environ.get("NLP2CMD_DEBUG", "").lower() in ("1", "true", "yes")


def debug(msg: str) -> None:
    """Print debug message to stderr when NLP2CMD_DEBUG=1."""
    if _DEBUG:
        print(f"DEBUG [SiteExplorer] {msg}", file=sys.stderr, flush=True)


def github_readme_url(url: str) -> str:
    """Convert github.com/owner/repo to raw README URL."""
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) >= 2:
        return f"https://github.com/{parts[0]}/{parts[1]}"
    return url


def github_docs_url(url: str) -> str:
    """Try to resolve GitHub repo docs (wiki, /docs, or README)."""
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) >= 2:
        return f"https://github.com/{parts[0]}/{parts[1]}/tree/main/docs"
    return url


def pypi_to_docs_url(url: str) -> Optional[str]:
    """Convert pypi.org/project/X to readthedocs or homepage."""
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) >= 2 and parts[0] == "project":
        pkg = parts[1].lower().replace("-", "").replace("_", "")
        return f"https://{pkg}.readthedocs.io/en/latest/"
    return None


@dataclass
class PageInfo:
    """Information about a discovered page."""
    url: str
    title: str = ""
    links: list[str] = field(default_factory=list)
    has_form: bool = False
    form_count: int = 0
    contact_field_count: int = 0
    junk_field_count: int = 0
    score: float = 0.0
    load_time_ms: float = 0.0


@dataclass
class ExplorationResult:
    """Result of site exploration."""
    success: bool
    form_url: Optional[str] = None
    form_page: Optional[PageInfo] = None
    explored_pages: list[PageInfo] = field(default_factory=list)
    error: Optional[str] = None


CONTACT_KEYWORDS = [
    "kontakt", "contact", "napisz do nas", "write to us",
    "formularz", "form", "wiadomość", "message",
    "pomoc", "help", "support", "serwis",
    "zapytaj", "ask", "biuro", "office", "dane", "info",
    "obsługa", "obsuga", "klienta", "customer",
]

ARTICLE_KEYWORDS = [
    "artykuł", "article", "blog", "news", "wiadomości", "aktualności",
    "publikacja", "publication", "post", "wpis", "treść", "content",
    "poradnik", "guide", "tutorial", "instrukcja", "manual",
]

PRODUCT_KEYWORDS = [
    "produkt", "product", "usługa", "service", "oferta", "offer",
    "sklep", "shop", "store", "cennik", "price", "cena", "buy",
    "katalog", "catalog", "portfolio", "galeria", "gallery",
]

DOCS_KEYWORDS = [
    "dokumentacja", "documentation", "docs", "pomoc", "help",
    "faq", "pytania", "questions", "support", "wsparcie",
    "manual", "instrukcja", "guide", "tutorial", "readme",
    "wiki", "api", "reference", "examples", "przykłady",
    "github", "gitlab", "bitbucket", "repository", "repo",
]

FORM_FIELD_KEYWORDS = [
    "email", "e-mail", "telefon", "phone", "imię", "name",
    "nazwisko", "surname", "wiadomość", "message", "temat", "subject",
]

BLOCKED_RESOURCE_PATTERNS = (
    "**/*.png", "**/*.jpg", "**/*.jpeg", "**/*.gif", "**/*.svg",
    "**/*.webp", "**/*.ico", "**/*.bmp", "**/*.tiff",
    "**/*.woff", "**/*.woff2", "**/*.ttf", "**/*.eot",
    "**/*.mp4", "**/*.webm", "**/*.ogg", "**/*.mp3",
)

PLATFORM_DOCS_URLS: dict[str, Any] = {
    "github.com": {
        "readme": github_readme_url,
        "docs": github_docs_url,
    },
    "readthedocs.io": {
        "docs": lambda url: url if "/en/" in url else url.rstrip("/") + "/en/latest/",
    },
    "docs.python.org": {
        "docs": lambda _url: "https://docs.python.org/3/",
    },
    "pypi.org": {
        "docs": pypi_to_docs_url,
    },
}

DOCS_FRAMEWORKS: dict[str, list[str]] = {
    "readthedocs": ["/en/latest/", "/en/stable/", "readthedocs.io"],
    "mkdocs": ["/mkdocs.yml", "mkdocs-material", "/site/"],
    "gitbook": ["gitbook.io", ".gitbook.io"],
    "sphinx": ["/_static/sphinx", "searchindex.js", "genindex.html"],
    "docusaurus": ["/docs/", "/blog/", "docusaurus"],
}
