"""
Executor registry — Etap 3 of the NLP refactoring plan.

Maps action names / domain types to executor instances.
The pipeline runner uses this to dispatch to the right executor
instead of embedding all logic in a single God Object method.
"""

from __future__ import annotations

import logging
from typing import Any

from nlp2cmd.execution.base import BaseExecutor, ExecutorContext, ExecutorResult

log = logging.getLogger(__name__)


class ExecutorRegistry:
    """Central registry that maps action names to executor instances.

    Usage::

        registry = ExecutorRegistry()
        registry.register(ShellExecutor())
        registry.register(MediaRecorder())

        result = registry.dispatch("shell", params, ctx)
    """

    def __init__(self) -> None:
        self._executors: dict[str, BaseExecutor] = {}

    def register(self, executor: BaseExecutor) -> None:
        """Register an executor for all its supported actions."""
        for action in executor.supported_actions:
            self._executors[action] = executor
            log.debug("Registered executor %s for action '%s'",
                      type(executor).__name__, action)

    def get(self, action: str) -> BaseExecutor | None:
        """Lookup executor for an action name."""
        return self._executors.get(action)

    def dispatch(
        self,
        action: str,
        params: dict[str, Any],
        ctx: ExecutorContext,
    ) -> ExecutorResult:
        """Dispatch an action to the appropriate executor.

        Returns an error result if no executor is registered for the action.
        """
        executor = self._executors.get(action)
        if executor is None:
            return ExecutorResult(
                success=False,
                kind="unknown",
                error=f"No executor registered for action: {action}",
            )
        if "action" in params and params["action"] != action:
            return ExecutorResult(success=False, kind="unknown",
                                  error="Payload action must match dispatch action")
        return executor.execute({**params, "action": action}, ctx)

    @property
    def registered_actions(self) -> list[str]:
        """Return sorted list of all registered action names."""
        return sorted(self._executors.keys())

    def __contains__(self, action: str) -> bool:
        return action in self._executors

    def __len__(self) -> int:
        return len(self._executors)


def create_default_registry(
    shell_policy: Any = None,
    safety_policy: Any = None,
) -> ExecutorRegistry:
    """Create an ExecutorRegistry pre-loaded with all built-in executors.

    This is the recommended way to get a registry instance.
    """
    registry = ExecutorRegistry()

    try:
        from nlp2cmd.execution.shell_executor import ShellExecutor
        registry.register(ShellExecutor(
            shell_policy=shell_policy,
            safety_policy=safety_policy,
        ))
    except Exception as e:
        log.debug("ShellExecutor not available: %s", e)

    try:
        from nlp2cmd.execution.media_recorder import MediaRecorder
        registry.register(MediaRecorder())
    except Exception as e:
        log.debug("MediaRecorder not available: %s", e)

    return registry
