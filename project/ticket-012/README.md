# Ticket 012: Retire broken metadata trigger after verified central synchronization

- **ID**: ticket-012
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

Remove the consumer metadata dispatcher that fails because ORG_SYNC_PAT is absent. The replacement is the existing central coordinator, whose exact allowlist now includes autogrammar/nlp2cmd through independently merged [semcod/.github PR #6](https://github.com/semcod/.github/pull/6). The canonical [operator document](https://github.com/semcod/.github/blob/main/docs/information/org-metadata-sync.md) owns the cross-repository mechanism.

SESSION_EXECUTION_AUTHORIZATION: user requested continuation, repairs, tests and autonomous protected merge using Willman/Subactor. Write scope is the obsolete consumer workflow, its user-facing maintenance pointer in README.md and this allocated ticket.

## Acceptance criteria

- [x] AC-01: Central exact-target dry-run, apply and API readback succeed; homepage, Pages and existing topics are preserved before trigger removal.
- [ ] AC-02: Governance, focused tests and required Python CI pass; independent Validator reviews and merges the exact head.

No credential copying. The central schedule runs every six hours, subject to GitHub queue delays. This change does not provide immediate synchronization after push.

Central validation: [dry-run](https://github.com/semcod/.github/actions/runs/40008628248) and [apply](https://github.com/semcod/.github/actions/runs/40008751286) passed at coordinator head `1bf78ef804bb7da8f4442af0d38789cfca23ac40`. API readback confirmed the autogrammar topic was added and homepage, Pages, description and existing topics preserved. Evidence: receipt:nlp2cmd-metadata-20261023/evidence.

Local validation: 49 focused tests passed. GOV-DELIVERY-001 identified an inconsistent draft classification (XS permits at most 10 minutes, while the estimate including publication preparation was 30). Corrected to S without expanding the one-file scope or budgets.

Governance: passed with zero errors/warnings. Required Python 3.11/3.12 CI and independent publication remain pending at commit creation.

The adopted pre-commit material-delivery check ignores deleted paths and rejected the deletion plus ticket carriers. Added a useful README maintenance pointer documenting the verified central route and six-hour schedule; scope includes that pointer, with two implementation files. Managed hooks remain unchanged.
