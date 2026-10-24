# Ticket 017: Honor media dry-run and bind registry dispatch action

- **ID**: ticket-017
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-24

SESSION_EXECUTION_AUTHORIZATION: continued autonomous Willman/Subactor refactoring, encountered defect repair, tests and protected publication. maxActiveMinutes=120.

Observed on main d6cf5b6: dry-run screenshot creates a file; registry dispatch of start_recording with ordinary params executes screenshot instead. Guard direct and routed media actions before side effects and preserve active recording handles during a preview. Reject a conflicting payload action and copy the selected action into the payload without mutating caller input.

## Acceptance criteria

- [x] AC-01: Direct, execute and registry media dry-runs do not access the browser, create artifacts or change active recording state; results explicitly identify a planned action.
- [x] AC-02: Registry dispatch invokes its selected media action and rejects mismatches before execution without changing caller params.
- [ ] AC-03: Real Playwright checks, focused tests, managed governance, required CI and independent exact-head merge pass.

## Validation

Twenty-one initial regression cases failed on the previous source. Focused media/executor/noVNC qualification:98 passed, including preview without a page and preview during an active recording. Four real Chromium tests passed, including browser/disk preservation and existing WebM recording verification. Ruff on the four owned files, managed governance and diff checks pass. Removed existing local import/annotation lint errors within the same scope. Willman AST symbol analysis is recorded externally. Required Python3.11/3.12 CI and independent exact-head publication remain pending.
