# Ticket 008: Refactor noVNC recording lifecycle

- **ID**: ticket-008
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

Use the existing Playwright capture of the real noVNC page as the single demo recording backend, removing duplicate detached FFmpeg and container-wide pkill. Finalize browser resources, videos and logs on success and failure. Repair encountered MediaRecorder lifecycle and screenshot path defects. This worktree depends on the local ownership prerequisite ticket-007 (124f9235220141c1f0932df41d05666bd3e96a5c); publication still requires that prerequisite and independent validation.

SESSION_EXECUTION_AUTHORIZATION: user requested discovery with semcod/search and refactoring with willman, including fixes in encountered dependencies. The bounded scope amendment adds docker/novnc/demos/** after its ownership prerequisite. No changes to unrelated application behavior or live user desktops.

## Acceptance criteria

- [x] AC-01: --record records the supplied noVNC URL through Playwright, with no detached Docker FFmpeg or global kill operation.
- [x] AC-02: Success and startup/navigation/interaction/close failures always close acquired browser resources and finalize the session log; failure is not reported as a successful demo.
- [x] AC-03: MediaRecorder rejects duplicate starts, returns the actual stop result, and creates screenshot parent directories for default and explicit paths.
- [x] AC-04: Focused regression tests, refactoring analysis and managed governance checks pass; runtime limitations are reported accurately.

## Evidence

semcod/search identified both local nlp2cmd copies; GitHub main is f17e8eb2e3caf5b0f7016a4a061367e7563eb312 and matches this primary checkout. Willman action inspected the demo; code2llm static analysis was run before modification. Existing unrelated desktops will not be used for tests.

Validation: 49 focused tests pass; seven of the media regressions fail against the original main and pass after repair. Managed governance: GOV-PASS, zero errors/warnings. A disposable, unmounted noVNC container delivered an Enter key to its guest test application and produced a valid VP8 WebM at 1280×800; ffprobe verified duration and streams. This does not validate the full example sequence of desktop applications. The test container was removed.

Willman action inspection and code2llm static/refactoring analysis were used. The latter excludes module counts under .worktrees even for explicit paths, so final metrics use a byte-identical source snapshot outside that ignored tree: 283 → 256 lines; maximum reported cyclomatic complexity 9 → 7. Advisory output is not execution or publication authority.

Private evidence: receipt:novnc-refactor-20261023/evidence; stored under the primary checkout's ignored .subactor/receipts/novnc-refactor-20261023. This branch and its prerequisite are local; protected review/merge and deployment have not been performed. Output format is now the existing Playwright WebM recording, without a second MP4 recorder.

SESSION_EXECUTION_AUTHORIZATION (2026-10-23 continuation): user requested continuing, testing and merging through the protected independent delivery controller.
