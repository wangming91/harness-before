# Roadmap Sync And Doctor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `abh doctor` as a first consistency gate and update project planning docs so Sprint 8 reflects the current product state.

**Architecture:** Keep the first `doctor` small and Git-native: compare `.abh` JSON records with their Markdown documents for plans, audits, memory, and drift reports. Expose the check through `abh.cli` and keep object-specific filesystem rules in `abh.core` to match the existing project style.

**Tech Stack:** Python standard library, `argparse`, `unittest`, repository-local JSON and Markdown files.

---

### Task 1: Add Doctor Behavior

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `abh/core.py`
- Modify: `abh/cli.py`

- [ ] **Step 1: Write failing tests**

Add tests that prove `doctor` passes on synced plan data, reports a missing Markdown document for a JSON record, and reports an orphan Markdown document without a JSON record.

- [ ] **Step 2: Run focused tests and confirm RED**

Run: `python3 -m unittest tests.test_cli.CliTests.test_doctor_passes_when_json_and_docs_are_in_sync tests.test_cli.CliTests.test_doctor_reports_missing_markdown_for_json_record tests.test_cli.CliTests.test_doctor_reports_orphan_markdown_without_json -v`

Expected: tests fail because `doctor` is not implemented.

- [ ] **Step 3: Implement minimal doctor check**

Add a core function that checks `.abh/{plans,audits,memory,drift}/*.json` against `docs/{plans,audits,memory,drift}/*.md`, ignoring `README.md` and `templates/`.

- [ ] **Step 4: Wire CLI command**

Add top-level `abh doctor` command that prints issue lines and returns `0` when healthy, `1` when consistency issues exist.

- [ ] **Step 5: Verify GREEN**

Run the focused doctor tests, then the full CLI suite.

### Task 2: Sync Planning Docs

**Files:**
- Modify: `README.md`
- Modify: `docs/development-roadmap.md`
- Modify: `docs/task-board.md`
- Modify: `docs/plans/README.md`

- [ ] **Step 1: Update docs**

Document Sprint 8, `abh doctor`, and the policy that docs/JSON consistency is a close gate.

- [ ] **Step 2: Verify docs and CLI**

Run: `python3 -m unittest tests/test_cli.py -v`

Run: `python3 -m abh doctor`

Expected: both commands pass.

### Task 3: ABH Closure

**Files:**
- Modify: `.abh/plans/plan-008-roadmap-sync-and-doctor.json`
- Modify: `docs/plans/plan-008-roadmap-sync-and-doctor.md`
- Create: `.abh/verifications/*.json`
- Create: `.abh/audits/audit-008-roadmap-sync-and-doctor.json`
- Create: `docs/audits/audit-008-roadmap-sync-and-doctor.md`

- [ ] **Step 1: Record verification**

Record passing verification for the full test suite and `abh doctor`.

- [ ] **Step 2: Request and record audit**

Create an independent audit record with evidence covering code, tests, and planning docs.

- [ ] **Step 3: Close plan**

Run `abh close plan-008-roadmap-sync-and-doctor` after audit passes.
