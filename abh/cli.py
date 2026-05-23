from __future__ import annotations

import argparse
import sys

from .core import (
    AbhError,
    add_memory,
    analyze_drift,
    close_plan,
    create_plan,
    doctor,
    list_audits,
    list_memories,
    list_plans,
    plan_status_line,
    record_audit,
    record_verification,
    request_audit,
    route_question,
    search_memory,
    transition_plan,
    validate_identifier,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="abh", description="Attractor Before Harness CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="manage plans")
    plan_sub = plan_parser.add_subparsers(dest="plan_command", required=True)

    create = plan_sub.add_parser("create", help="create a plan")
    create.add_argument("--id", required=True)
    create.add_argument("--title", required=True)
    create.add_argument("--attractor", required=True)
    create.add_argument("--baseline", required=True)
    create.add_argument("--owner", default="platform")
    create.add_argument("--status", choices=["draft", "ready"], default="draft")
    create.add_argument("--goal", action="append", default=[])
    create.add_argument("--non-goal", action="append", default=[])
    create.add_argument("--exit-criterion", action="append", default=[])
    create.add_argument("--validation", action="append", default=[])
    create.add_argument("--closure-evidence", action="append", default=[])
    create.set_defaults(handler=handle_plan_create)

    status = plan_sub.add_parser("status", help="show plan status")
    status.add_argument("plan_id")
    status.set_defaults(handler=handle_plan_status)

    plan_list = plan_sub.add_parser("list", help="list all plans")
    plan_list.set_defaults(handler=handle_plan_list)

    transition = plan_sub.add_parser("transition", help="move plan to another status")
    transition.add_argument("plan_id")
    transition.add_argument("--to", required=True, choices=["draft", "ready", "running", "blocked", "closing", "closed"])
    transition.set_defaults(handler=handle_plan_transition)

    verify_parser = subparsers.add_parser("verify", help="record verification runs")
    verify_sub = verify_parser.add_subparsers(dest="verify_command", required=True)

    record = verify_sub.add_parser("record", help="record a verification run")
    record.add_argument("plan_id")
    record.add_argument("--command", required=True)
    record.add_argument("--result", required=True, choices=["pass", "fail", "partial"])
    record.add_argument("--artifact", action="append", default=[])
    record.add_argument("--failed-check", action="append", default=[])
    record.set_defaults(handler=handle_verify_record)

    audit_parser = subparsers.add_parser("audit", help="manage independent audits")
    audit_sub = audit_parser.add_subparsers(dest="audit_command", required=True)

    audit_request = audit_sub.add_parser("request", help="request an audit")
    audit_request.add_argument("plan_id")
    audit_request.add_argument("--id", required=True)
    audit_request.add_argument("--auditor", required=True)
    audit_request.add_argument("--scope", required=True)
    audit_request.add_argument("--evidence", action="append", default=[])
    audit_request.set_defaults(handler=handle_audit_request)

    audit_record = audit_sub.add_parser("record", help="record an audit verdict")
    audit_record.add_argument("audit_id")
    audit_record.add_argument("--result", required=True, choices=["pass", "fail", "partial", "need_info"])
    audit_record.add_argument("--rationale", required=True)
    audit_record.add_argument("--finding", action="append", default=[])
    audit_record.add_argument("--follow-up", action="append", default=[])
    audit_record.set_defaults(handler=handle_audit_record)

    audit_list = audit_sub.add_parser("list", help="list all audits")
    audit_list.set_defaults(handler=handle_audit_list)

    close = subparsers.add_parser("close", help="close a plan after passing audit")
    close.add_argument("plan_id")
    close.set_defaults(handler=handle_close)

    doctor_parser = subparsers.add_parser("doctor", help="check workspace consistency")
    doctor_parser.set_defaults(handler=handle_doctor)

    memory_parser = subparsers.add_parser("memory", help="manage externalized memory")
    memory_sub = memory_parser.add_subparsers(dest="memory_command", required=True)

    memory_add = memory_sub.add_parser("add", help="add a memory record")
    memory_add.add_argument("--id", required=True)
    memory_add.add_argument("--type", required=True, choices=["false_assumption", "rejected_path", "divergent_pattern", "overturned_completion"])
    memory_add.add_argument("--summary", required=True)
    memory_add.add_argument("--context", required=True)
    memory_add.add_argument("--implication", required=True)
    memory_add.add_argument("--evidence", action="append", default=[])
    memory_add.add_argument("--related", action="append", default=[])
    memory_add.add_argument("--deprecation-policy")
    memory_add.set_defaults(handler=handle_memory_add)

    memory_search = memory_sub.add_parser("search", help="search memory records")
    memory_search.add_argument("--type", choices=["false_assumption", "rejected_path", "divergent_pattern", "overturned_completion"])
    memory_search.add_argument("--query")
    memory_search.set_defaults(handler=handle_memory_search)

    memory_list = memory_sub.add_parser("list", help="list all memory records")
    memory_list.set_defaults(handler=handle_memory_list)

    route = subparsers.add_parser("route", help="recommend reading order for a question")
    route.add_argument("--question", required=True)
    route.set_defaults(handler=handle_route)

    drift_parser = subparsers.add_parser("drift", help="analyze drift")
    drift_sub = drift_parser.add_subparsers(dest="drift_command", required=True)

    drift_analyze = drift_sub.add_parser("analyze", help="analyze drift from a text source")
    drift_analyze.add_argument("--id", required=True)
    drift_analyze.add_argument("--source", required=True)
    drift_analyze.add_argument("--evidence", action="append", default=[])
    drift_analyze.add_argument("--memory-id")
    drift_analyze.add_argument("--plan")
    drift_analyze.set_defaults(handler=handle_drift_analyze)

    return parser


def handle_plan_create(args: argparse.Namespace) -> int:
    create_plan(
        plan_id=args.id,
        title=args.title,
        attractor=args.attractor,
        baseline=args.baseline,
        owner=args.owner,
        status=args.status,
        goals=args.goal,
        non_goals=args.non_goal,
        exit_criteria=args.exit_criterion,
        validation_checklist=args.validation,
        closure_evidence=args.closure_evidence,
    )
    print(f"created plan {args.id}")
    return 0


def handle_plan_status(args: argparse.Namespace) -> int:
    from .core import load_plan

    validate_identifier(args.plan_id, "plan id")
    plan = load_plan(args.plan_id)
    print(plan_status_line(plan))
    return 0


def handle_plan_transition(args: argparse.Namespace) -> int:
    transition_plan(args.plan_id, args.to)
    print(f"transitioned {args.plan_id} -> {args.to}")
    return 0


def handle_plan_list(args: argparse.Namespace) -> int:
    plans = list_plans()
    for plan in plans:
        runs = len(plan.verification_runs)
        audits = len(plan.audit_ids)
        print(f"{plan.id}  [{plan.status}]  {plan.title}  (verifications: {runs}, audits: {audits})")
    print(f"\ntotal: {len(plans)} plan(s)")
    return 0


def handle_verify_record(args: argparse.Namespace) -> int:
    run = record_verification(
        plan_id=args.plan_id,
        command=args.command,
        result=args.result,
        artifacts=args.artifact,
        failed_checks=args.failed_check,
    )
    print(f"recorded verification {run.id} for {args.plan_id}")
    return 0


def handle_audit_request(args: argparse.Namespace) -> int:
    audit = request_audit(
        audit_id=args.id,
        plan_id=args.plan_id,
        auditor=args.auditor,
        scope=args.scope,
        evidence=args.evidence,
    )
    print(f"requested audit {audit.id} for {audit.plan_id}")
    return 0


def handle_audit_record(args: argparse.Namespace) -> int:
    audit = record_audit(
        audit_id=args.audit_id,
        result=args.result,
        rationale=args.rationale,
        findings=args.finding,
        follow_ups=args.follow_up,
    )
    print(f"recorded audit {audit.id}: {audit.result}")
    return 0


def handle_audit_list(args: argparse.Namespace) -> int:
    audits = list_audits()
    for audit in audits:
        status_info = f" [{audit.status}]" if audit.status == "complete" else ""
        result_info = f" result={audit.result}" if audit.status == "complete" else ""
        print(f"{audit.id}  -> {audit.plan_id}{status_info}{result_info}")
    print(f"\ntotal: {len(audits)} audit(s)")
    return 0


def handle_close(args: argparse.Namespace) -> int:
    plan = close_plan(args.plan_id)
    print(f"closed plan {plan.id}")
    return 0


def handle_doctor(args: argparse.Namespace) -> int:
    issues = doctor()
    if not issues:
        print("doctor: ok")
        return 0
    print("doctor: found consistency issues")
    for issue in issues:
        print(f"- {issue}")
    return 1


def handle_memory_add(args: argparse.Namespace) -> int:
    memory = add_memory(
        memory_id=args.id,
        memory_type=args.type,
        summary=args.summary,
        context=args.context,
        implication=args.implication,
        evidence=args.evidence,
        related=args.related,
        deprecation_policy=args.deprecation_policy,
    )
    print(f"recorded memory {memory.id}")
    return 0


def handle_memory_search(args: argparse.Namespace) -> int:
    results = search_memory(memory_type=args.type, query=args.query)
    for memory in results:
        print(f"{memory.id} [{memory.memory_type}] {memory.summary}")
    return 0


def handle_memory_list(args: argparse.Namespace) -> int:
    memories = list_memories()
    for mem in memories:
        evidence_count = len(mem.evidence)
        print(f"{mem.id}  [{mem.memory_type}]  {mem.summary}  (evidence: {evidence_count})")
    print(f"\ntotal: {len(memories)} memory record(s)")
    return 0


def handle_route(args: argparse.Namespace) -> int:
    result = route_question(args.question)
    print(f"Route: {result['route']}")
    print("Reading order:")
    for item in result["reading_order"]:
        print(f"- {item}")
    print(f"Rationale: {result['rationale']}")
    return 0


def handle_drift_analyze(args: argparse.Namespace) -> int:
    report = analyze_drift(
        drift_id=args.id,
        source=args.source,
        evidence=args.evidence,
        memory_id=args.memory_id,
        plan_id=args.plan,
    )
    print(f"drift report {report.id}")
    for finding in report.findings:
        print(f"- {finding.drift_type}: {finding.evidence}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        handler = getattr(args, "handler", None)
        if handler is None:
            parser.print_help()
            return 1
        return handler(args)
    except AbhError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except SystemExit as exc:
        return int(exc.code)
