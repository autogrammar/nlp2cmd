# Ticket 009: Register noVNC runtime infrastructure ownership

- **ID**: ticket-009
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

Assign the existing noVNC Dockerfile, startup script and Compose file to infrastructure. The full-demo build found an unavailable base-image digest, but these runtime files have no workstream owner. Keep demo Python code in application ownership.

SESSION_EXECUTION_AUTHORIZATION: user requested continuing, fixing encountered defects, testing and merging through independent validation.

## Acceptance criteria

- [x] AC-01: The three runtime files belong to infrastructure and demo Python remains application-owned; managed governance passes.
