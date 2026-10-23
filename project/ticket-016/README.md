# Ticket 016: Bind media recording to actual Playwright video output

- **ID**: ticket-016
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-24

SESSION_EXECUTION_AUTHORIZATION: continued autonomous Willman/Subactor refactoring, immediate encountered defect repairs, tests and protected merge. maxActiveMinutes=120.

The executor currently reports recording without a browser, and never saves the actual page video. Bind only a live, video-enabled Playwright page; keep browser lifecycle with its caller. Reject premature stop without blocking or closing that page. Once the page has closed, save its video to the unique requested output and validate nonempty output. Preserve retry after save failure and reset state after terminal completion.

## Acceptance criteria

- [x] AC-01: Missing, unconfigured or closed pages cannot claim recording; a premature stop preserves the recording and never closes shared browser resources.
- [x] AC-02: A finalized page video is saved through its actual handle, nonempty output is verified and retryable save errors retain state; a real WebM is readable by ffprobe.
- [ ] AC-03: Focused checks, managed governance, required CI and independent exact-head publication pass.

## Validation

Five new regressions fail before the patch. Focused media/executor/noVNC tests:67 passed. Real Playwright/Chromium recording and screenshot checks:3 passed; ffprobe validates the executor WebM as1280x720 with positive duration. Managed governance:PASS; diff check:PASS. Willman symbol analysis binds the changed methods and their new save_as call. Required Python3.11/3.12 CI and independent exact-head merge remain pending.
