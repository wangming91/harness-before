from __future__ import annotations

import io
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import TestCase
import os

from abh.cli import main


class Chdir:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.previous: Path | None = None

    def __enter__(self):
        self.previous = Path.cwd()
        os.chdir(self.path)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.previous is not None:
            os.chdir(self.previous)


class CliTests(TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "architecture" / "attractors").mkdir(parents=True, exist_ok=True)
        (self.root / "docs" / "architecture" / "attractors" / "abh-core-attractor.md").write_text("# Attractor\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with Chdir(self.root), redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_plan_create_status_transition_and_verify(self) -> None:
        code, out, err = self.run_cli(
            "plan",
            "create",
            "--id",
            "plan-100-demo",
            "--title",
            "Demo",
            "--attractor",
            "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline",
            "initial baseline",
            "--status",
            "ready",
            "--goal",
            "ship skeleton",
            "--non-goal",
            "web ui",
            "--exit-criterion",
            "cli commands exist",
            "--validation",
            "unit tests pass",
            "--closure-evidence",
            "docs/plans/plan-100-demo.md",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("created plan plan-100-demo", out)
        self.assertTrue((self.root / ".abh" / "plans" / "plan-100-demo.json").exists())
        self.assertTrue((self.root / "docs" / "plans" / "plan-100-demo.md").exists())

        code, out, err = self.run_cli(
            "plan",
            "status",
            "plan-100-demo",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("plan-100-demo [ready]", out)

        code, out, err = self.run_cli(
            "verify",
            "record",
            "plan-100-demo",
            "--command",
            "python -m pytest",
            "--result",
            "pass",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("recorded verification", out)

        code, out, err = self.run_cli(
            "plan",
            "transition",
            "plan-100-demo",
            "--to",
            "running",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("transitioned plan-100-demo -> running", out)

    def test_failed_verification_blocks_ready_plan(self) -> None:
        code, out, err = self.run_cli(
            "plan",
            "create",
            "--id",
            "plan-102-ready",
            "--title",
            "Ready Plan",
            "--attractor",
            "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline",
            "baseline",
            "--status",
            "ready",
            "--goal",
            "ship loop",
            "--non-goal",
            "audit",
            "--exit-criterion",
            "validation recorded",
            "--validation",
            "unit tests pass",
            "--closure-evidence",
            "docs/plans/plan-102-ready.md",
        )
        self.assertEqual(code, 0, err)

        code, out, err = self.run_cli(
            "verify",
            "record",
            "plan-102-ready",
            "--command",
            "python -m pytest",
            "--result",
            "fail",
            "--failed-check",
            "unit tests",
        )
        self.assertEqual(code, 0, err)

        code, out, err = self.run_cli("plan", "status", "plan-102-ready")
        self.assertEqual(code, 0, err)
        self.assertIn("plan-102-ready [blocked]", out)

    def test_invalid_ready_transition_is_rejected(self) -> None:
        code, out, err = self.run_cli(
            "plan",
            "create",
            "--id",
            "plan-101-draft",
            "--title",
            "Draft",
            "--attractor",
            "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline",
            "baseline",
        )
        self.assertEqual(code, 0, err)
        stderr = io.StringIO()
        stdout = io.StringIO()
        with Chdir(self.root), redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["plan", "transition", "plan-101-draft", "--to", "ready"])
        self.assertNotEqual(code, 0)
        self.assertIn("plan is not ready", stderr.getvalue())

    def create_ready_plan(self, plan_id: str = "plan-200-audit") -> None:
        code, out, err = self.run_cli(
            "plan",
            "create",
            "--id",
            plan_id,
            "--title",
            "Audited Plan",
            "--attractor",
            "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline",
            "baseline",
            "--status",
            "ready",
            "--goal",
            "ship audited close",
            "--non-goal",
            "remote service",
            "--exit-criterion",
            "audit passes",
            "--validation",
            "unit tests pass",
            "--closure-evidence",
            "docs/audits/audit-200-audit.md",
        )
        self.assertEqual(code, 0, err)

    def test_audit_record_allows_close_only_after_pass(self) -> None:
        self.create_ready_plan()
        code, out, err = self.run_cli("close", "plan-200-audit")
        self.assertEqual(code, 2)
        self.assertIn("passing audit", err)

        code, out, err = self.run_cli(
            "audit",
            "request",
            "plan-200-audit",
            "--id",
            "audit-200-audit",
            "--auditor",
            "independent reviewer",
            "--scope",
            "Sprint 3 close gate",
            "--evidence",
            "tests/test_cli.py",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("requested audit audit-200-audit", out)
        self.assertTrue((self.root / ".abh" / "audits" / "audit-200-audit.json").exists())
        self.assertTrue((self.root / "docs" / "audits" / "audit-200-audit.md").exists())

        code, out, err = self.run_cli(
            "audit",
            "record",
            "audit-200-audit",
            "--result",
            "partial",
            "--finding",
            "Medium|Missing evidence|docs/plans/plan-200-audit.md|Add evidence",
            "--rationale",
            "not enough evidence",
        )
        self.assertEqual(code, 0, err)
        code, out, err = self.run_cli("close", "plan-200-audit")
        self.assertEqual(code, 2)
        self.assertIn("passing audit", err)

        code, out, err = self.run_cli(
            "audit",
            "record",
            "audit-200-audit",
            "--result",
            "pass",
            "--rationale",
            "all exit criteria verified",
        )
        self.assertEqual(code, 0, err)

        code, out, err = self.run_cli("close", "plan-200-audit")
        self.assertEqual(code, 0, err)
        self.assertIn("closed plan plan-200-audit", out)

        code, out, err = self.run_cli("plan", "status", "plan-200-audit")
        self.assertEqual(code, 0, err)
        self.assertIn("plan-200-audit [closed]", out)

    def test_memory_add_and_search_by_type_and_keyword(self) -> None:
        code, out, err = self.run_cli(
            "memory",
            "add",
            "--id",
            "mem-001",
            "--type",
            "overturned_completion",
            "--summary",
            "Audit overturned a premature close",
            "--context",
            "Close was attempted without evidence.",
            "--evidence",
            "docs/audits/audit-200-audit.md",
            "--related",
            "plan-200-audit",
            "--implication",
            "Require pass audit before close.",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("recorded memory mem-001", out)
        self.assertTrue((self.root / ".abh" / "memory" / "mem-001.json").exists())
        self.assertTrue((self.root / "docs" / "memory" / "mem-001.md").exists())

        code, out, err = self.run_cli(
            "memory",
            "search",
            "--type",
            "overturned_completion",
            "--query",
            "premature",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("mem-001 [overturned_completion]", out)
        self.assertIn("Audit overturned a premature close", out)

    def test_route_recommends_reading_order_for_close_question(self) -> None:
        code, out, err = self.run_cli(
            "route",
            "--question",
            "Can we close this plan after the implementation claims completion?",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("Route: completion_audit", out)
        self.assertIn("docs/plans/", out)
        self.assertIn("docs/audits/", out)
        self.assertIn("docs/memory/", out)

    def test_drift_analyze_detects_patterns_and_can_write_memory(self) -> None:
        drift_source = self.root / "drift-source.txt"
        drift_source.write_text(
            "\n".join(
                [
                    "Imported a remote database dependency even though the plan said no external database.",
                    "Moved audit logic into the plan manager boundary.",
                    "Skipped tests and renamed ready to prepared in documentation.",
                ]
            ),
            encoding="utf-8",
        )

        code, out, err = self.run_cli(
            "drift",
            "analyze",
            "--id",
            "drift-001",
            "--source",
            str(drift_source),
            "--evidence",
            "drift-source.txt",
            "--memory-id",
            "mem-drift-001",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("drift-001", out)
        self.assertIn("boundary_drift", out)
        self.assertIn("dependency_drift", out)
        self.assertIn("test_drift", out)
        self.assertIn("terminology_drift", out)
        self.assertTrue((self.root / ".abh" / "drift" / "drift-001.json").exists())
        self.assertTrue((self.root / "docs" / "drift" / "drift-001.md").exists())
        self.assertTrue((self.root / ".abh" / "memory" / "mem-drift-001.json").exists())

        code, out, err = self.run_cli(
            "memory",
            "search",
            "--type",
            "divergent_pattern",
            "--query",
            "dependency_drift",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("mem-drift-001 [divergent_pattern]", out)

    def test_plan_list_returns_all_plans(self) -> None:
        self.run_cli(
            "plan", "create",
            "--id", "plan-list-a",
            "--title", "Plan A for list test",
            "--attractor", "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline", "baseline",
        )
        self.run_cli(
            "plan", "create",
            "--id", "plan-list-b",
            "--title", "Plan B for list test",
            "--attractor", "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline", "baseline",
        )
        code, out, err = self.run_cli("plan", "list")
        self.assertEqual(code, 0, err)
        self.assertIn("plan-list-a  [draft]  Plan A for list test", out)
        self.assertIn("plan-list-b  [draft]  Plan B for list test", out)
        self.assertIn("total: 2 plan(s)", out)

    def test_memory_list_returns_all_memories(self) -> None:
        self.run_cli(
            "memory", "add",
            "--id", "mem-list-a",
            "--type", "false_assumption",
            "--summary", "list test assumption",
            "--context", "testing memory list",
            "--implication", "list works",
            "--evidence", "tests/test_cli.py",
        )
        self.run_cli(
            "memory", "add",
            "--id", "mem-list-b",
            "--type", "rejected_path",
            "--summary", "another list test",
            "--context", "testing memory list again",
            "--implication", "list works twice",
            "--evidence", "tests/test_cli.py",
        )
        code, out, err = self.run_cli("memory", "list")
        self.assertEqual(code, 0, err)
        self.assertIn("mem-list-a  [false_assumption]  list test assumption", out)
        self.assertIn("mem-list-b  [rejected_path]  another list test", out)
        self.assertIn("total: 2 memory record(s)", out)

    def test_audit_list_returns_all_audits(self) -> None:
        self.create_ready_plan("plan-audit-list")
        self.run_cli(
            "audit", "request",
            "plan-audit-list",
            "--id", "audit-list-a",
            "--auditor", "reviewer",
            "--scope", "test audit list",
            "--evidence", "tests/test_cli.py",
        )
        self.run_cli(
            "audit", "request",
            "plan-audit-list",
            "--id", "audit-list-b",
            "--auditor", "reviewer",
            "--scope", "test audit list again",
            "--evidence", "tests/test_cli.py",
        )
        code, out, err = self.run_cli("audit", "list")
        self.assertEqual(code, 0, err)
        self.assertIn("audit-list-a  -> plan-audit-list", out)
        self.assertIn("audit-list-b  -> plan-audit-list", out)
        self.assertIn("total: 2 audit(s)", out)

    def test_route_injects_active_plans(self) -> None:
        self.run_cli(
            "plan", "create",
            "--id", "plan-route-active",
            "--title", "Active Plan",
            "--attractor", "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline", "baseline",
            "--status", "ready",
            "--goal", "test route injection",
            "--non-goal", "web ui",
            "--exit-criterion", "route test passes",
            "--validation", "unit tests pass",
            "--closure-evidence", "tests/test_cli.py",
        )
        self.run_cli(
            "verify", "record",
            "plan-route-active",
            "--command", "python -m pytest",
            "--result", "pass",
        )
        self.run_cli(
            "plan", "transition", "plan-route-active", "--to", "running",
        )
        code, out, err = self.run_cli("route", "--question", "Can we close this plan?")
        self.assertEqual(code, 0, err)
        self.assertIn("Route: completion_audit", out)
        self.assertIn("active plans", out.lower())
        self.assertIn("plan-route-active", out)

    def test_drift_with_plan_detects_non_goal_violation(self) -> None:
        drift_source = self.root / "drift-plan.txt"
        drift_source.write_text("重构存储层并引入外部服务\n", encoding="utf-8")
        self.run_cli(
            "plan", "create",
            "--id", "plan-drift-baseline",
            "--title", "Drift Baseline Plan",
            "--attractor", "docs/architecture/attractors/abh-core-attractor.md",
            "--baseline", "baseline",
            "--status", "ready",
            "--goal", "cli commands",
            "--non-goal", "不重构存储层",
            "--exit-criterion", "drift test passes",
            "--validation", "unit tests pass",
            "--closure-evidence", "tests/test_cli.py",
        )
        code, out, err = self.run_cli(
            "drift", "analyze",
            "--id", "drift-plan-001",
            "--source", str(drift_source),
            "--plan", "plan-drift-baseline",
        )
        self.assertEqual(code, 0, err)
        self.assertIn("boundary_drift", out)
        self.assertIn("plan non-goal violation", out)