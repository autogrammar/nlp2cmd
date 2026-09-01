"""Mutable runtime state for legacy multi-action browser runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MultiActionState:
    page: Any
    context: Any
    url: str
    schema_loader: Any
    console: Any
    console_wrapper: Any
    confirm: bool
    extracted_data: list[dict[str, str]] = field(default_factory=list)
    detected_form_fields: list[object] | None = None
    filled_any_form_field: bool = False
    saw_fill_form_action: bool = False
