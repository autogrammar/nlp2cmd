# Ticket 013: Preserve artifacts across repeated noVNC presentations

- **ID**: ticket-013
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-10-23

## Goal and scope

A real disposable desktop containing an earlier nlp2cmd_report.txt reproduced a false success: the old document stayed intact, Mousepad remained in Save As, and Firefox showed the old document. Reports and screenshots also use fixed output names. Give each presentation a shared unique session identifier for its desktop document and local log artifacts; retain unique Playwright video files. Validate two complete runs against one desktop, including preservation of an earlier document and all first-run artifacts.

SESSION_EXECUTION_AUTHORIZATION: the user requested continuing autonomously with Willman and Subactor, repairing encountered defects, testing and protected merging. Publication is authorized through the independent Validator; local tests never grant merge authority.

## Acceptance criteria

- [x] AC-01: Two complete recorded presentations on one desktop create distinct documents with the expected content; an existing document and first-run artifacts remain unchanged.
- [x] AC-02: Focused regressions and governance pass; each full recording contains the calculator result and the newly saved document in Firefox.
- [ ] AC-03: Publish through exact-head independent review and protected merge.

Validation: baseline E2E reproduced false success with a pre-existing document. The new repeated-report unit regression failed before the fix. After the fix, 50 focused tests pass and the two-run desktop E2E passes in 153.17 seconds: two distinct saved documents, two valid recordings, calculator/browser OCR and unchanged prior artifacts. Governance passes with zero findings. Willman action inspection was repeated; its bounded queue scan found no runnable work. Protected publication profile requires Python 3.11 and 3.12 CI checks and independent Validator approval.
