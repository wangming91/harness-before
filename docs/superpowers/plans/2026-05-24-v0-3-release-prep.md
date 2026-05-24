# v0.3 Release Prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare ABH v0.3.0 as a formal release after Stage 3 completion.

**Architecture:** This is a release governance slice, not a feature slice. It updates version metadata, release documentation, roadmap numbering, and ABH records while keeping CLI/MCP behavior and runtime schemas unchanged.

**Tech Stack:** Python packaging metadata, Markdown docs, ABH CLI dogfooding.

---

### Task 1: Version Metadata

**Files:**
- Modify: `pyproject.toml`
- Modify: `abh/__init__.py`

- [ ] **Step 1: Set package version to 0.3.0**

Change `[project].version` in `pyproject.toml` to `0.3.0`.

- [ ] **Step 2: Set runtime version to 0.3.0**

Change `abh.__version__` in `abh/__init__.py` to `0.3.0`.

- [ ] **Step 3: Verify version import**

Run: `python3 -c 'import abh; print(abh.__version__)'`
Expected: `0.3.0`

### Task 2: Release Documentation

**Files:**
- Create: `docs/releases/v0.3.0.md`
- Modify: `README.md`
- Modify: `docs/development-roadmap.md`
- Modify: `docs/task-board.md`
- Modify: `docs/阶段规划.md`

- [ ] **Step 1: Add v0.3.0 release notes**

Create release notes with scope, validation evidence, known limitations, and upgrade notes.

- [ ] **Step 2: Update public docs**

Update README and roadmap to declare v0.3.0 as current, make release-prep the plan-026 slice, and move Stage 4 Attractor Registry to plan-027.

- [ ] **Step 3: Run docs consistency**

Run: `python3 -m abh doctor`
Expected: `doctor: ok`

### Task 3: Verification, Audit, Release Tag

**Files:**
- Modify: `.abh/plans/plan-026-v0-3-release-prep.json`
- Modify: `docs/plans/plan-026-v0-3-release-prep.md`
- Modify: `.abh/audits/audit-026-v0-3-release-prep.json`
- Modify: `docs/audits/audit-026-v0-3-release-prep.md`

- [ ] **Step 1: Run validation checklist**

Run:

```bash
python3 -m unittest tests/test_cli.py -v
python3 -m abh doctor
python3 -m compileall abh tests
git diff --check
python3 -m abh plan status plan-026-v0-3-release-prep --json
```

- [ ] **Step 2: Run release install smoke**

Run editable install in a clean temporary virtual environment and verify `abh --help`, `abh doctor`, and `abh.__version__`.

- [ ] **Step 3: Record audit and close plan**

Record a passing audit, transition the plan to closing, and close it.

- [ ] **Step 4: Commit, tag, and push**

Commit release-prep changes, tag `v0.3.0`, and push branch plus tag.
