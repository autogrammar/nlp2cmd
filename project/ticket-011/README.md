# Ticket 011: Repair noVNC desktop application launch sequence

- **ID**: ticket-011
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

The real desktop demo submits Enter before XFCE Application Finder resolves its command. Mousepad never opens and subsequent document/browser input remains in the launcher. Factor the repeated launch sequence, clear stale input and wait for command resolution; retain keyboard interaction through the noVNC page. Use the current date and open the saved report in Firefox so the demonstration does not depend on external website loading.

SESSION_EXECUTION_AUTHORIZATION: user requested continuing, fixing encountered defects, testing and independent merging. Runtime repair ticket-010 provides the disposable full-demo test environment.

## Acceptance criteria

- [x] AC-01: The recorded full scenario calculates 5754, saves the expected document and opens the file manager and Firefox.
- [x] AC-02: Focused tests and governance pass; startup/failure cleanup behavior is preserved.

Dependency handoff: keep source unchanged while ticket-010 completes independent validation and merge. The current full-demo run is read-only verification; resume IN_PROGRESS after observing that merge.

Prerequisite observed: ticket-010 independently merged in PR23 at d6137da7902baed8c7e2c97954913d0389281b74. Resuming implementation and end-to-end verification, including the analogous save-dialog resolution delay.

Validation: 49 focused tests pass. The new opt-in E2E test passes against a freshly built, unmounted disposable desktop: calculator screenshot OCR confirms 5754; the saved document has the expected text/current date; Firefox is foreground and renders that text; ffprobe validates VP8 WebM at 1280x800. The container is removed in finally. Initial whole-page OCR and filename-based Firefox-title assumptions were corrected against observed screenshots/window behavior. The image and source digests, full recording, logs and verification JSON are preserved in receipt:novnc-full-20261023/evidence. Willman action inspection was repeated after refactoring.
