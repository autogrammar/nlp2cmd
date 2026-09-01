"""Shared types for nlp2cmd doctor checks."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Status(Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    FIXED = "fixed"


@dataclass
class CheckResult:
    name: str
    status: Status
    message: str
    details: dict = field(default_factory=dict)
    fix_applied: bool = False
    fix_command: Optional[str] = None

