# ABH Agent Protocol

## Purpose

Agent Protocol is the programmatic interface that lets AI agents read and later write ABH governance state without scraping human-oriented CLI text.

The protocol does not replace the CLI. The CLI remains the execution substrate; Agent Protocol defines the structured contracts that can be exposed through JSON output and MCP tools.

## Current Gap

ABH has a parameterized CLI for plans, verifications, audits, memory, routing, drift, close, and doctor. It now exposes explicit JSON output for core read commands, structured ABH errors, and an MCP stdio server.

Before Stage 2, an agent could run commands but could not reliably parse results, distinguish business blocking from system errors, or discover stable tool schemas. Stage 2 closes that gap by making the CLI and MCP contracts machine-readable while keeping repository files as the source of truth.

## Principles

- Repository files remain the source of truth.
- Human-readable Markdown and natural CLI output remain supported by default.
- Machine-readable output must be explicit, stable, and schema-versioned.
- MCP tools must wrap existing ABH behavior instead of bypassing state, audit, or doctor gates.
- Read capability comes before write capability.
- Write capability must preserve existing plan, verification, audit, close, memory, and drift rules.

## Protocol Layers

### Layer 1: JSON CLI Contract

Core read commands should expose a machine-readable mode such as `--json`.

Minimum read commands:

- `abh plan status`
- `abh plan list`
- `abh audit list`
- `abh memory list`
- `abh memory search`
- `abh route`
- `abh doctor`
- `abh drift analyze`

Each JSON response should include:

- `schema_version`
- `ok`
- `command`
- `data`
- `errors`
- `warnings`

Example shape:

```json
{
  "schema_version": "1",
  "ok": true,
  "command": "plan list",
  "data": {
    "plans": []
  },
  "errors": [],
  "warnings": []
}
```

### Layer 2: Structured Error Contract

Agents need structured errors, not stderr text alone.

Error entries should include:

- `code`
- `message`
- `category`
- `details`

Recommended categories:

- `usage`
- `validation`
- `not_found`
- `business_rule`
- `consistency`
- `system`

Exit codes should remain compatible with the current CLI:

- `0`: success
- `1`: consistency or doctor failure
- `2`: ABH validation or business rule error
- parser usage errors continue to follow argparse behavior

### Layer 3: Agent Tool Schema

Agent-facing tools should be derived from CLI commands and internal models.

Initial tool groups:

- `plans`: list plans, show plan status
- `audits`: list audits
- `memory`: list and search memory
- `route`: recommend reading order for a question
- `drift`: analyze text evidence
- `doctor`: report workspace consistency

Each tool must define:

- input schema
- output schema
- side effects
- required evidence
- failure modes

### Layer 4: Read-only MCP Server

The first MCP Server was delivered as read-only before any write tools were opened.

Allowed tools:

- `abh_plan_list`
- `abh_plan_status`
- `abh_audit_list`
- `abh_memory_list`
- `abh_memory_search`
- `abh_route`
- `abh_doctor`
- `abh_drift_list`

Current entrypoint:

```bash
python3 -m abh.mcp_server
```

The server uses stdio JSON-RPC messages and returns MCP tool results with both text content and `structuredContent`. `abh_drift_list` lists existing drift reports without creating new ones.

### Layer 5: Controlled Write MCP Tools

Write tools were added only after JSON output and read-only MCP were stable.

Allowed controlled write tools:

- `abh_plan_create`
- `abh_plan_transition`
- `abh_verify_record`
- `abh_audit_request`
- `abh_audit_record`
- `abh_close_plan`
- `abh_memory_add`
- `abh_drift_analyze`

Write tools must:

- call the same core functions as the CLI
- preserve state transition rules
- preserve audit-before-close
- preserve doctor and schema expectations
- require explicit `confirm=true`
- return structured verification evidence
- be covered by CLI and MCP contract tests

## Near-term Plans

- `plan-012-agent-protocol-foundation`: completed; defined this protocol baseline and aligned roadmap/task-board.
- `plan-013-json-output-and-errors`: completed; implemented JSON output and structured errors for read commands.
- `plan-014-readonly-mcp-server`: completed; exposes read-only MCP tools over the JSON/internal object contract.
- `plan-015-controlled-mcp-write-tools`: completed; exposes controlled MCP write tools with explicit confirmation and existing ABH gates.

## Milestone Status

Stage 2 / Agent Protocol Foundation is complete as of `plan-015-controlled-mcp-write-tools` closure. ABH has explicit JSON CLI contracts, structured errors, read-only MCP tools, and controlled MCP write tools guarded by explicit confirmation and existing ABH gates.

## Non-goals

- Do not implement MCP before JSON contracts are clear.
- Do not make JSON output the default human CLI output.
- Do not give agents write tools before read tools are stable.
- Do not bypass ABH closure, audit, memory, or doctor gates.
