# Ticket 002: fix password store test isolation with dotenv

- **ID**: ticket-002
- **Owner**: agent:gemini
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-04

## Goal and scope

Ensure `test_password_store.py` scenarios with cleared environment are properly
isolated from host `.env` files via `patch("dotenv.load_dotenv")`.

## Acceptance criteria

- [x] AC-01: `pytest -q tests/unit/test_password_store.py` passes cleanly.
- [x] AC-02: `project/governance-check.sh` passes cleanly.

## Tracking boundary

This directory contains the minimal reviewed intent.
