# Ticket 014: Reject missing and empty video recording outputs

- **ID**: ticket-014
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

A real MediaRecorder start/stop pair returned success with a path that did not exist. VideoRecorder currently returns its planned filename without checking for a saved file, and timestamp-only naming can reuse a previous session path within one second. Validate nonempty file output and use a unique expected path per session so old recordings cannot turn an unsaved session into success. Keep existing saved_path fallback and caller signatures.

SESSION_EXECUTION_AUTHORIZATION: user requests continuing autonomously with Willman and Subactor, repairing encountered defects, testing and independent protected merging.

Bound: maxActiveMinutes=120, scoped to the helper and its regression tests.

## Acceptance criteria

- [x] AC-01: Missing, empty or directory outputs return no saved video and cannot cause executor success; valid explicit and expected paths continue to work.
- [x] AC-02: Starting another session in the same second cannot reuse an earlier video. A real Playwright recording finalizes successfully through the helper.
- [ ] AC-03: Focused tests, governance and required CI pass before independent Validator merge.

Validation: eight targeted regressions failed before the fix. After the fix, 60 focused tests pass. A real Playwright recording is saved, finalized through VideoRecorder, and verified with ffprobe (640x480 video, positive duration). Governance passes without findings. Willman inspected the helper operation; its bounded project scan has no runnable queued tickets. Existing pipeline callers retain their signatures and explicit saved_path fallback. Required publication tests and independent Validator review remain pending.
