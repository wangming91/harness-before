from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import Any, TextIO

from .cli import abh_error_payload, make_envelope
from .core import (
    AbhError,
    doctor,
    list_audits,
    list_memories,
    list_plans,
    load_plan,
    route_question,
    search_memory,
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


TOOLS: dict[str, dict[str, Any]] = {
    "abh_plan_list": {
        "description": "List ABH plans without modifying repository state.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "abh_plan_status": {
        "description": "Read one ABH plan by id.",
        "inputSchema": {
            "type": "object",
            "properties": {"plan_id": text_property("Plan id, for example plan-014-readonly-mcp-server.")},
            "required": ["plan_id"],
            "additionalProperties": False,
        },
    },
    "abh_audit_list": {
        "description": "List ABH audit records without modifying repository state.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "abh_memory_list": {
        "description": "List ABH memory records without modifying repository state.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "abh_memory_search": {
        "description": "Search ABH memory records by optional type and query text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": text_property("Optional memory type."),
                "query": text_property("Optional case-insensitive search text."),
            },
            "additionalProperties": False,
        },
    },
    "abh_route": {
        "description": "Recommend ABH reading order for a question.",
        "inputSchema": {
            "type": "object",
            "properties": {"question": text_property("Question to route through ABH governance context.")},
            "required": ["question"],
            "additionalProperties": False,
        },
    },
    "abh_doctor": {
        "description": "Check ABH workspace consistency without modifying repository state.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "abh_drift_list": {
        "description": "List existing ABH drift reports without creating new drift reports.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
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
        tools.append(
            {
                "name": name,
                "title": name.replace("_", " "),
                "description": definition["description"],
                "inputSchema": definition["inputSchema"],
                "annotations": {
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
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


def call_doctor(arguments: dict[str, Any]) -> dict[str, Any]:
    return {"issues": []}


def call_drift_list(arguments: dict[str, Any]) -> dict[str, Any]:
    reports = list_drift_reports()
    return {"drift_reports": [report.to_dict() for report in reports], "total": len(reports)}


TOOL_HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "abh_plan_list": call_plan_list,
    "abh_plan_status": call_plan_status,
    "abh_audit_list": call_audit_list,
    "abh_memory_list": call_memory_list,
    "abh_memory_search": call_memory_search,
    "abh_route": call_route,
    "abh_doctor": call_doctor,
    "abh_drift_list": call_drift_list,
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
            "instructions": "ABH MCP exposes read-only governance tools. Write operations remain CLI-only.",
        },
    )


def handle_tools_call(request_id: object, params: object) -> dict[str, Any]:
    if not isinstance(params, dict):
        return jsonrpc_error(request_id, JSONRPC_INVALID_PARAMS, "tools/call params must be an object", category="validation")
    name = params.get("name")
    if not isinstance(name, str):
        return jsonrpc_error(request_id, JSONRPC_INVALID_PARAMS, "tools/call requires a string name", category="validation")
    if name not in TOOL_HANDLERS:
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
