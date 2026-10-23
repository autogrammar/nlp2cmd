# Ticket 015: Preserve rapid successive screenshot captures

- **ID**: ticket-015
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

A real-file probe captured two images within the same second: both calls succeeded, returned one identical path, and the second overwrote the first. The automatically generated filename uses only a timestamp with second precision. Give each default screenshot a unique name and retain the current explicit-path contract. Cover repeated captures with a frozen clock and a real Playwright browser.

SESSION_EXECUTION_AUTHORIZATION: user requests continuing autonomously with Willman and Subactor, repairing encountered recording defects, testing and independent protected merging.

Bound: maxActiveMinutes=120; only the media executor and its regression tests.

## Acceptance criteria

- [x] AC-01: Repeated default screenshots within the same second produce different paths and preserve each image; explicit paths and error results remain supported.
- [x] AC-02: A real Playwright test produces distinct PNG screenshots and preserves the first capture after the second.
- [ ] AC-03: Focused tests, governance and required CI pass before independent Validator merge.

Validation: both repeated-capture regressions failed before the fix. After the fix, 62 focused tests and two real Playwright E2E tests pass, including distinct red/blue PNG screenshots with the first preserved. Governance passes without findings. Willman indexed MediaRecorder.take_screenshot through its symbol API; action metadata extraction only supports top-level functions and is not applicable to this class-only module. The bounded Willman queue scan had no runnable tickets. Required CI and independent Validator publication remain pending.
