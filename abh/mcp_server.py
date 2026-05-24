from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import Any, TextIO

from .cli import abh_error_payload, make_envelope
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
    load_plan,
    record_audit,
    record_verification,
    request_audit,
    route_question,
    search_memory,
    transition_plan,
)
from .models import DriftReport, SCHEMA_VERSION
from .storage import drift_dir, read_json

PROTOCOL_VERSION = "2025-11-25"

JSONRPC_PARSE_ERROR = -32700
JSONRPC_INVALID_REQUEST = -32600
JSONRPC_METHOD_NOT_FOUND = -32601
JSONRPC_INVALID_PARAMS = -32602
JSONRPC_INTERNAL_ERROR = -32603


def text_property(description: str) -> dict[str, str]:
    return {"type": "string", "description": description}


def bool_property(description: str) -> dict[str, str]:
    return {"type": "boolean", "description": description}


def array_property(description: str) -> dict[str, Any]:
    return {"type": "array", "description": description, "items": {"type": "string"}}


def object_schema(
    properties: dict[str, Any],
    required: list[str] | None = None,
    *,
    read_only: bool,
    description: str,
) -> dict[str, Any]:
    return {
        "description": description,
        "readOnly": read_only,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": list(required or []),
            "additionalProperties": False,
        },
    }


TOOLS: dict[str, dict[str, Any]] = {
    "abh_plan_list": object_schema({}, read_only=True, description="List ABH plans without modifying repository state."),
    "abh_plan_status": object_schema(
        {"plan_id": text_property("Plan id, for example plan-014-readonly-mcp-server.")},
        ["plan_id"],
        read_only=True,
        description="Read one ABH plan by id.",
    ),
    "abh_audit_list": object_schema({}, read_only=True, description="List ABH audit records without modifying repository state."),
    "abh_memory_list": object_schema({}, read_only=True, description="List ABH memory records without modifying repository state."),
    "abh_memory_search": object_schema(
        {
            "type": text_property("Optional memory type."),
            "query": text_property("Optional case-insensitive search text."),
        },
        read_only=True,
        description="Search ABH memory records by optional type and query text.",
    ),
    "abh_route": object_schema(
        {"question": text_property("Question to route through ABH governance context.")},
        ["question"],
        read_only=True,
        description="Recommend ABH reading order for a question.",
    ),
    "abh_doctor": object_schema({}, read_only=True, description="Check ABH workspace consistency without modifying repository state."),
    "abh_drift_list": object_schema({}, read_only=True, description="List existing ABH drift reports without creating new drift reports."),
    "abh_plan_create": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "plan_id": text_property("Plan id to create."),
            "title": text_property("Plan title."),
            "attractor": text_property("Attractor document path."),
            "baseline": text_property("Baseline document path or baseline label."),
            "owner": text_property("Optional owner."),
            "status": text_property("draft or ready."),
            "goals": array_property("Plan goals."),
            "non_goals": array_property("Plan non-goals."),
            "exit_criteria": array_property("Plan exit criteria."),
            "validation_checklist": array_property("Validation checklist."),
            "closure_evidence": array_property("Closure evidence paths."),
        },
        ["confirm", "plan_id", "title", "attractor", "baseline"],
        read_only=False,
        description="Create an ABH plan through existing core rules.",
    ),
    "abh_plan_transition": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "plan_id": text_property("Plan id."),
            "to": text_property("Target status."),
        },
        ["confirm", "plan_id", "to"],
        read_only=False,
        description="Transition an ABH plan through the existing state machine.",
    ),
    "abh_verify_record": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "plan_id": text_property("Plan id."),
            "command": text_property("Verification command."),
            "result": text_property("pass, fail, or partial."),
            "artifacts": array_property("Verification artifact paths."),
            "failed_checks": array_property("Failed checks."),
        },
        ["confirm", "plan_id", "command", "result"],
        read_only=False,
        description="Record verification evidence for a plan.",
    ),
    "abh_audit_request": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "plan_id": text_property("Plan id."),
            "audit_id": text_property("Audit id."),
            "auditor": text_property("Auditor label."),
            "scope": text_property("Audit scope."),
            "evidence": array_property("Evidence items."),
        },
        ["confirm", "plan_id", "audit_id", "auditor", "scope", "evidence"],
        read_only=False,
        description="Request an independent audit.",
    ),
    "abh_audit_record": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "audit_id": text_property("Audit id."),
            "result": text_property("pass, fail, partial, or need_info."),
            "rationale": text_property("Audit rationale."),
            "findings": array_property("Findings in Severity|Finding|Evidence|Recommendation form."),
            "follow_ups": array_property("Follow-up items."),
        },
        ["confirm", "audit_id", "result", "rationale"],
        read_only=False,
        description="Record an audit verdict.",
    ),
    "abh_close_plan": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "plan_id": text_property("Plan id."),
        },
        ["confirm", "plan_id"],
        read_only=False,
        description="Close a plan after a passing audit.",
    ),
    "abh_memory_add": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "memory_id": text_property("Memory id."),
            "type": text_property("Memory type."),
            "summary": text_property("Memory summary."),
            "context": text_property("Memory context."),
            "implication": text_property("Memory implication."),
            "evidence": array_property("Evidence items."),
            "related": array_property("Related records."),
            "deprecation_policy": text_property("Optional deprecation policy."),
        },
        ["confirm", "memory_id", "type", "summary", "context", "implication", "evidence"],
        read_only=False,
        description="Add a memory record.",
    ),
    "abh_drift_analyze": object_schema(
        {
            "confirm": bool_property("Must be true to permit repository writes."),
            "drift_id": text_property("Drift report id."),
            "source": text_property("Text source path to analyze."),
            "evidence": array_property("Evidence items."),
            "memory_id": text_property("Optional memory id to write."),
            "plan_id": text_property("Optional plan id baseline."),
        },
        ["confirm", "drift_id", "source"],
        read_only=False,
        description="Analyze drift and write a drift report.",
    ),
}


def jsonrpc_response(request_id: object, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def jsonrpc_error(
    request_id: object,
    code: int,
    message: str,
    *,
    category: str = "system",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
            "data": {
                "category": category,
                "details": details or {},
            },
        },
    }


def tool_definitions() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for name, definition in TOOLS.items():
        read_only = bool(definition["readOnly"])
        tools.append(
            {
                "name": name,
                "title": name.replace("_", " "),
                "description": definition["description"],
                "inputSchema": definition["inputSchema"],
                "annotations": {
                    "readOnlyHint": read_only,
                    "destructiveHint": not read_only,
                    "idempotentHint": read_only,
                    "openWorldHint": False,
                },
            }
        )
    return tools


def require_string(arguments: dict[str, Any], key: str) -> str:
    value = arguments.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AbhError(f"invalid tool argument: {key} is required")
    return value


def optional_string(arguments: dict[str, Any], key: str, default: str | None = None) -> str | None:
    value = arguments.get(key, default)
    if value is None:
        return None
    if not isinstance(value, str):
        raise AbhError(f"invalid tool argument: {key} must be a string")
    return value


def optional_string_list(arguments: dict[str, Any], key: str) -> list[str] | None:
    value = arguments.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise AbhError(f"invalid tool argument: {key} must be a list of strings")
    return list(value)


def require_confirm(arguments: dict[str, Any]) -> None:
    if arguments.get("confirm") is not True:
        raise AbhError("cannot run write tool without confirm=true")


def list_drift_reports() -> list[DriftReport]:
    directory = drift_dir()
    if not directory.exists():
        return []
    reports: list[DriftReport] = []
    for path in sorted(directory.glob("*.json")):
        reports.append(DriftReport.from_dict(read_json(path)))
    return reports


def call_plan_list(arguments: dict[str, Any]) -> dict[str, Any]:
    plans = list_plans()
    return {"plans": [plan.to_dict() for plan in plans], "total": len(plans)}


def call_plan_status(arguments: dict[str, Any]) -> dict[str, Any]:
    plan_id = require_string(arguments, "plan_id")
    return {"plan": load_plan(plan_id).to_dict()}


def call_audit_list(arguments: dict[str, Any]) -> dict[str, Any]:
    audits = list_audits()
    return {"audits": [audit.to_dict() for audit in audits], "total": len(audits)}


def call_memory_list(arguments: dict[str, Any]) -> dict[str, Any]:
    memories = list_memories()
    return {"memories": [memory.to_dict() for memory in memories], "total": len(memories)}


def call_memory_search(arguments: dict[str, Any]) -> dict[str, Any]:
    memory_type = arguments.get("type")
    query = arguments.get("query")
    if memory_type is not None and not isinstance(memory_type, str):
        raise AbhError("invalid tool argument: type must be a string")
    if query is not None and not isinstance(query, str):
        raise AbhError("invalid tool argument: query must be a string")
    memories = search_memory(memory_type=memory_type, query=query)
    return {"memories": [memory.to_dict() for memory in memories], "total": len(memories)}


def call_route(arguments: dict[str, Any]) -> dict[str, Any]:
    question = require_string(arguments, "question")
    return {"route": route_question(question)}


def call_drift_list(arguments: dict[str, Any]) -> dict[str, Any]:
    reports = list_drift_reports()
    return {"drift_reports": [report.to_dict() for report in reports], "total": len(reports)}


def call_plan_create(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    plan = create_plan(
        plan_id=require_string(arguments, "plan_id"),
        title=require_string(arguments, "title"),
        attractor=require_string(arguments, "attractor"),
        baseline=require_string(arguments, "baseline"),
        owner=optional_string(arguments, "owner", "platform") or "platform",
        status=optional_string(arguments, "status", "draft") or "draft",
        goals=optional_string_list(arguments, "goals"),
        non_goals=optional_string_list(arguments, "non_goals"),
        exit_criteria=optional_string_list(arguments, "exit_criteria"),
        validation_checklist=optional_string_list(arguments, "validation_checklist"),
        closure_evidence=optional_string_list(arguments, "closure_evidence"),
    )
    return {"plan": plan.to_dict()}


def call_plan_transition(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    plan = transition_plan(require_string(arguments, "plan_id"), require_string(arguments, "to"))
    return {"plan": plan.to_dict()}


def call_verify_record(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    run = record_verification(
        plan_id=require_string(arguments, "plan_id"),
        command=require_string(arguments, "command"),
        result=require_string(arguments, "result"),
        artifacts=optional_string_list(arguments, "artifacts"),
        failed_checks=optional_string_list(arguments, "failed_checks"),
    )
    return {"verification": run.to_dict()}


def call_audit_request(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    audit = request_audit(
        plan_id=require_string(arguments, "plan_id"),
        audit_id=require_string(arguments, "audit_id"),
        auditor=require_string(arguments, "auditor"),
        scope=require_string(arguments, "scope"),
        evidence=optional_string_list(arguments, "evidence"),
    )
    return {"audit": audit.to_dict()}


def call_audit_record(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    audit = record_audit(
        audit_id=require_string(arguments, "audit_id"),
        result=require_string(arguments, "result"),
        rationale=require_string(arguments, "rationale"),
        findings=optional_string_list(arguments, "findings"),
        follow_ups=optional_string_list(arguments, "follow_ups"),
    )
    return {"audit": audit.to_dict()}


def call_close_plan(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    plan = close_plan(require_string(arguments, "plan_id"))
    return {"plan": plan.to_dict()}


def call_memory_add(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    memory = add_memory(
        memory_id=require_string(arguments, "memory_id"),
        memory_type=require_string(arguments, "type"),
        summary=require_string(arguments, "summary"),
        context=require_string(arguments, "context"),
        implication=require_string(arguments, "implication"),
        evidence=optional_string_list(arguments, "evidence"),
        related=optional_string_list(arguments, "related"),
        deprecation_policy=optional_string(arguments, "deprecation_policy"),
    )
    return {"memory": memory.to_dict()}


def call_drift_analyze(arguments: dict[str, Any]) -> dict[str, Any]:
    require_confirm(arguments)
    report = analyze_drift(
        drift_id=require_string(arguments, "drift_id"),
        source=require_string(arguments, "source"),
        evidence=optional_string_list(arguments, "evidence"),
        memory_id=optional_string(arguments, "memory_id"),
        plan_id=optional_string(arguments, "plan_id"),
    )
    return {"drift_report": report.to_dict()}


TOOL_HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "abh_plan_list": call_plan_list,
    "abh_plan_status": call_plan_status,
    "abh_audit_list": call_audit_list,
    "abh_memory_list": call_memory_list,
    "abh_memory_search": call_memory_search,
    "abh_route": call_route,
    "abh_drift_list": call_drift_list,
    "abh_plan_create": call_plan_create,
    "abh_plan_transition": call_plan_transition,
    "abh_verify_record": call_verify_record,
    "abh_audit_request": call_audit_request,
    "abh_audit_record": call_audit_record,
    "abh_close_plan": call_close_plan,
    "abh_memory_add": call_memory_add,
    "abh_drift_analyze": call_drift_analyze,
}


def tool_result(envelope: dict[str, Any], *, is_error: bool) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(envelope, ensure_ascii=False)}],
        "structuredContent": envelope,
        "isError": is_error,
    }


def handle_initialize(request_id: object, params: object) -> dict[str, Any]:
    protocol_version = PROTOCOL_VERSION
    if isinstance(params, dict) and isinstance(params.get("protocolVersion"), str):
        protocol_version = str(params["protocolVersion"])
    return jsonrpc_response(
        request_id,
        {
            "protocolVersion": protocol_version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "abh", "version": SCHEMA_VERSION},
            "instructions": "ABH MCP exposes read-only governance tools and controlled write tools that require confirm=true.",
        },
    )


def handle_tools_call(request_id: object, params: object) -> dict[str, Any]:
    if not isinstance(params, dict):
        return jsonrpc_error(request_id, JSONRPC_INVALID_PARAMS, "tools/call params must be an object", category="validation")
    name = params.get("name")
    if not isinstance(name, str):
        return jsonrpc_error(request_id, JSONRPC_INVALID_PARAMS, "tools/call requires a string name", category="validation")
    if name not in TOOL_HANDLERS and name != "abh_doctor":
        return jsonrpc_error(request_id, JSONRPC_METHOD_NOT_FOUND, f"Unknown tool: {name}", category="not_found")
    arguments = params.get("arguments", {})
    if not isinstance(arguments, dict):
        return jsonrpc_error(request_id, JSONRPC_INVALID_PARAMS, "tool arguments must be an object", category="validation")
    try:
        if name == "abh_doctor":
            issues = doctor()
            if issues:
                envelope = make_envelope(
                    ok=False,
                    command=name,
                    data={"issues": issues},
                    errors=[
                        {
                            "code": "doctor_issues",
                            "message": "doctor found consistency issues",
                            "category": "consistency",
                            "details": {"issues": issues},
                        }
                    ],
                )
                return jsonrpc_response(request_id, tool_result(envelope, is_error=True))
            envelope = make_envelope(ok=True, command=name, data={"issues": []})
            return jsonrpc_response(request_id, tool_result(envelope, is_error=False))
        data = TOOL_HANDLERS[name](arguments)
        envelope = make_envelope(ok=True, command=name, data=data)
        return jsonrpc_response(request_id, tool_result(envelope, is_error=False))
    except AbhError as exc:
        envelope = make_envelope(ok=False, command=name, errors=[abh_error_payload(exc)])
        return jsonrpc_response(request_id, tool_result(envelope, is_error=True))


def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(message, dict):
        return jsonrpc_error(None, JSONRPC_INVALID_REQUEST, "JSON-RPC message must be an object", category="validation")
    request_id = message.get("id")
    method = message.get("method")
    if not isinstance(method, str):
        return jsonrpc_error(request_id, JSONRPC_INVALID_REQUEST, "JSON-RPC method is required", category="validation")
    if method.startswith("notifications/"):
        return None
    if method == "initialize":
        return handle_initialize(request_id, message.get("params", {}))
    if method == "tools/list":
        return jsonrpc_response(request_id, {"tools": tool_definitions()})
    if method == "tools/call":
        return handle_tools_call(request_id, message.get("params", {}))
    if method == "ping":
        return jsonrpc_response(request_id, {})
    return jsonrpc_error(request_id, JSONRPC_METHOD_NOT_FOUND, f"Unknown method: {method}", category="not_found")


def serve_stdio(input_stream: TextIO | None = None, output_stream: TextIO | None = None) -> int:
    reader = input_stream or sys.stdin
    writer = output_stream or sys.stdout
    for line in reader:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            response = jsonrpc_error(
                None,
                JSONRPC_PARSE_ERROR,
                "Parse error",
                category="validation",
                details={"message": str(exc)},
            )
        else:
            response = handle_message(message)
        if response is not None:
            writer.write(json.dumps(response, ensure_ascii=False) + "\n")
            writer.flush()
    return 0


def main() -> int:
    return serve_stdio()


if __name__ == "__main__":
    raise SystemExit(main())
