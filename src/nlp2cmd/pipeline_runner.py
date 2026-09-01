from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from nlp2cmd.adapters.base import SafetyPolicy
from nlp2cmd.ir import ActionIR
from nlp2cmd.utils.data_files import find_data_file
from rich.console import Console
from nlp2cmd.utils.yaml_compat import yaml

# Utility functions, classes, and dataclasses extracted to pipeline_runner_utils.py
from nlp2cmd.pipeline_runner_utils import (  # noqa: F401
    _debug,
    _DEBUG,
    _with_epipe_retry,
    _field_attrs,
    _is_junk_field,
    _is_contact_relevant_field,
    _looks_like_comment_form,
    _filter_form_fields,
    _MarkdownConsoleWrapper,
    ShellExecutionPolicy,
    RunnerResult,
    # Screenshot and video utilities
    get_timestamp,
    ensure_dir,
    ask_for_screenshot,
    take_screenshot,
    VideoRecorder,
    ask_for_video_recording,
)


class PipelineRunner:
    def __init__(
        self,
        *,
        shell_policy: Optional[ShellExecutionPolicy] = None,
        safety_policy: Optional[SafetyPolicy] = None,
        headless: bool = True,
        enable_history: bool = True,
        video_fmt: Optional[str] = None,
        video_dir: str = "./recordings",
        intract_gate: Optional[Any] = None,
    ):
        self.shell_policy = shell_policy or ShellExecutionPolicy()
        try:
            self.shell_policy.load_from_data()
        except Exception:
            pass
        self.safety_policy = safety_policy
        self.headless = headless
        # When video recording is requested, force headless=False so there's content to record
        self.video_fmt = video_fmt
        self.video_dir = video_dir
        if video_fmt:
            self.headless = False
        self.enable_history = enable_history
        self._history = None
        self._executor_registry = None
        self._intract_gate = intract_gate
        if self._intract_gate is None and os.getenv("NLP2CMD_INTRACT_GATE", "0").strip().lower() in {
            "1", "true", "yes", "on",
        }:
            try:
                from nlp2cmd.intract.pipeline_gate import PipelineRunnerGate

                self._intract_gate = PipelineRunnerGate()
            except Exception:
                self._intract_gate = None

        # Etap 3: opt-in modular executor dispatch
        if os.getenv("NLP2CMD_USE_EXECUTOR_REGISTRY", "1") == "1":
            try:
                from nlp2cmd.execution.executor_registry import create_default_registry
                self._executor_registry = create_default_registry(
                    shell_policy=self.shell_policy,
                    safety_policy=self.safety_policy,
                )
            except Exception:
                self._executor_registry = None

        if enable_history:
            try:
                from nlp2cmd.web_schema.history import InteractionHistory
                self._history = InteractionHistory()
            except Exception:
                self._history = None

    def run(
        self,
        ir: ActionIR,
        *,
        cwd: Optional[str] = None,
        timeout_s: float = 15.0,
        dry_run: bool = True,
        confirm: bool = False,
        web_url: Optional[str] = None,
        video_fmt: Optional[str] = None,
        video_dir: Optional[str] = None,
    ) -> RunnerResult:
        started = time.time()
        try:
            if self._intract_gate is not None:
                gate_result = self._intract_gate.check(ir)
                if not gate_result.passed:
                    return RunnerResult(
                        success=False,
                        kind=str(ir.dsl_kind),
                        error=self._intract_gate.failure_message(gate_result),
                        data=self._intract_gate.gate_result_metadata(gate_result),
                        duration_ms=(time.time() - started) * 1000.0,
                    )

            if ir.dsl_kind == "shell" and self._executor_registry and "shell" in self._executor_registry:
                from nlp2cmd.execution.base import ExecutorContext
                ctx = ExecutorContext(
                    dry_run=dry_run, confirm=confirm, headless=self.headless,
                    video_fmt=video_fmt or self.video_fmt,
                    video_dir=video_dir or self.video_dir,
                )
                executor_result = self._executor_registry.dispatch(
                    "shell",
                    {"command": ir.dsl, "cwd": cwd, "timeout_s": timeout_s},
                    ctx,
                )
                res = executor_result.to_runner_result()
            elif ir.dsl_kind == "shell":
                res = self._run_shell(ir.dsl, cwd=cwd, timeout_s=timeout_s, dry_run=dry_run, confirm=confirm)
            elif ir.dsl_kind == "dom":
                res = self._run_dom_dql(ir.dsl, dry_run=dry_run, confirm=confirm, web_url=web_url,
                                        video_fmt=video_fmt, video_dir=video_dir)
            else:
                res = RunnerResult(
                    success=False,
                    kind=str(ir.dsl_kind),
                    error=f"Unsupported dsl_kind: {ir.dsl_kind}",
                )

            res.duration_ms = (time.time() - started) * 1000.0
            return res
        except Exception as e:
            return RunnerResult(
                success=False,
                kind=str(ir.dsl_kind),
                error=str(e),
                duration_ms=(time.time() - started) * 1000.0,
            )

    # --- Method bodies are in mixin modules ---
    # See: pipeline_runner_shell.py, pipeline_runner_browser.py,
    #      pipeline_runner_desktop.py, pipeline_runner_plans.py


# Compose PipelineRunner from mixins via class re-definition.
# This preserves backward compatibility: all imports of PipelineRunner still work.
from nlp2cmd.pipeline_runner_shell import ShellExecutionMixin  # noqa: E402
from nlp2cmd.pipeline_runner_browser import BrowserExecutionMixin  # noqa: E402
from nlp2cmd.pipeline_runner_browser_multi import BrowserMultiActionMixin  # noqa: E402
from nlp2cmd.pipeline_runner_browser_dispatch import BrowserDispatchMixin  # noqa: E402
from nlp2cmd.pipeline_runner_desktop import DesktopExecutionMixin  # noqa: E402
from nlp2cmd.pipeline_runner_plans import PlanExecutionMixin  # noqa: E402

_BasePipelineRunner = PipelineRunner


class PipelineRunner(  # type: ignore[no-redef]
    ShellExecutionMixin,
    BrowserExecutionMixin,
    BrowserMultiActionMixin,
    BrowserDispatchMixin,
    DesktopExecutionMixin,
    PlanExecutionMixin,
    _BasePipelineRunner,
):
    """PipelineRunner composed from execution mixins.

    Mixins:
    - ShellExecutionMixin: _run_shell, _parse_shell_command, _check_against_safety_policy
    - BrowserExecutionMixin: _run_dom_dql
    - BrowserMultiActionMixin: _run_dom_multi_action
    - BrowserDispatchMixin: _run_dom_multi_action_dispatch
    - DesktopExecutionMixin: _dismiss_popups, _detect_desktop_backend,
      _execute_desktop_plan_step, _xdotool_keys_to_ydotool, etc.
    - PlanExecutionMixin: execute_action_plan, _execute_plan_step,
      _resolve_plan_variables, _do_verify_env, _llm_suggest_article_selectors
    """
    pass
