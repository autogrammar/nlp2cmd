# Ticket 001: Route nlp2cmd vision through central SubLLM

- **ID**: ticket-001
- **Owner**: unresolved:human
- **Status**: DONE
- **Created**: 2026-09-16

## Goal and scope

Route image inputs through the central `subactor/subllm` vision transport
instead of per-repository provider clients, as part of the fleet-wide SubLLM
vision rollout (sibling of the published imgl integration).

## Acceptance criteria

- [x] AC-01: `OpenRouterClient` submits through the SubLLM transport when
  available.
- [x] AC-02: Hosted Python matrix passes (3.11/3.12).

## Session authorization

Continuation of the 2026-09-16 automation-completion session authorized by
the repository owner.
