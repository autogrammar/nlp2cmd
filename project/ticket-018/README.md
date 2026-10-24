# Ticket 018: Verify Firefox report before completing noVNC presentation

- **ID**: ticket-018
- **Owner**: tom
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-24

## Goal and scope

Require observable Firefox navigation and report content before declaring the
noVNC presentation completed. Use the existing noVNC clipboard transport and a
unique document marker, without Docker access or new runtime dependencies.
Bound the readiness wait and preserve the existing failure/video finalization.

## Acceptance criteria

- [x] AC-01: Continuing autonomous repair/test/merge authorization is recorded.
- [x] AC-02: Delayed readiness succeeds; stale reports, missing clipboard feedback
  and browser failures cannot produce a completed presentation.
- [x] AC-03: 74 focused unit tests, all 5 real-browser/noVNC acceptance tests,
  and governance against the accepted base pass. Both consecutive desktop
  presentations verify the current report while preserving earlier artifacts.
- [ ] AC-04: Independent exact-head validation precedes protected merge.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
