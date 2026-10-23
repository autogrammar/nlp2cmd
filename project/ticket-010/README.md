# Ticket 010: Repair and verify noVNC desktop runtime

- **ID**: ticket-010
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

Repair the noVNC Docker runtime after the full-demo build exposed a missing Ubuntu digest and a Firefox package requiring Snap. Verify startup, desktop applications and recorded interactions in a disposable container, preserving existing user sessions. Fix directly observed startup/runtime defects within the three declared infrastructure files.

SESSION_EXECUTION_AUTHORIZATION: user requested continuing, repairing encountered dependencies, testing and merging through independent validation. Ownership prerequisite ticket-009 was independently merged in PR22.

## Acceptance criteria

- [x] AC-01: The pinned runtime image builds and its non-root desktop starts with a working Firefox.
- [x] AC-02: The runtime launches terminal, calculator, editor, file manager and Firefox; noVNC forwards input and produces valid video. End-to-end script timing defects are owned by ticket-011.
- [x] AC-03: Runtime failure is observable, Compose configuration and managed checks pass, and disposable test resources are cleaned up.

Scope reconciliation: real desktop tests exposed independent launcher/save-dialog timing defects in the application demo. Ticket-011 owns that script repair and depends on this runtime. This ticket claims runtime readiness, not a successful unchanged full sequence. The failing and diagnostic recordings are preserved in receipt:novnc-full-20261023/evidence.

Validation: exact final image built successfully. A new unmounted container accepted noVNC keyboard input and launched galculator, Mousepad, Thunar and Firefox; its foreground process is websockify. Its non-root Playwright Chromium launches successfully. VP8 WebM was finalized at 1280x800. Invalid geometry exits with status 1; injected VNC/proxy failures preserve statuses 23/24. Compose publishes only loopback ports. 49 focused tests and managed governance pass. Full presentation automation is still tracked separately in ticket-011.
