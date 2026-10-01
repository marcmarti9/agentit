---
name: mcp-server-development
description: Designs and implements Model Context Protocol servers and tool surfaces for external APIs/services. Use when creating or substantially changing an MCP server, its tools/resources/prompts, auth boundary, transport, schemas, pagination or error model. Do not use merely to choose, enable or call an existing MCP; use mcp-tooling-fit for that.
---

# MCP Server Development

## Goal

Build an MCP server whose tool surface lets an agent accomplish real tasks safely, predictably and with bounded context.

MCP SDKs and protocol details change. When correctness depends on current protocol/framework behavior, pair with `source-driven-development` and verify the current official MCP and SDK documentation before committing an interface.

## BUILDER

### 1. Start from user workflows

Map the external service into concrete agent jobs before designing tools.

For each important job identify:

- required inputs;
- external API operations;
- output the model actually needs;
- auth/permission boundary;
- pagination or long-running behavior;
- destructive or financially consequential effects.

Prefer a small coherent first surface over implementing every endpoint blindly.

### 2. Choose tool granularity

Expose primitives when agents need flexible composition. Add workflow-level tools only where they remove repeated fragile orchestration.

A tool should have:

- an action-oriented, unambiguous name;
- a precise description of when to use it;
- constrained typed inputs;
- structured output where supported;
- bounded response size;
- actionable errors.

Do not create several tools that differ only cosmetically.

### 3. Protect the context window

Return the minimum information needed for the next decision.

Use:

- server-side filtering;
- pagination/cursors;
- compact structured fields;
- explicit detail levels when the API returns large objects.

Do not dump raw multi-page API payloads into every response.

### 4. Errors are part of the interface

Translate upstream failures into errors that state:

- what failed;
- which input/resource caused it;
- whether retrying can help;
- what the caller can change next.

Do not leak credentials, tokens, sensitive headers or unnecessary upstream internals.

### 5. Auth and side effects

Use least-privilege credentials and keep secrets outside source.

For destructive, external-message, purchase, deployment, permission or other high-impact tools:

- make the effect explicit in the name/description;
- validate identifiers and scope;
- preserve host/user confirmation requirements;
- avoid hidden writes inside read-looking tools.

### 6. Minimal checks while building

During BUILDER, test the tool or flow currently being implemented:

- schema accepts/rejects expected examples;
- one successful call path;
- one representative upstream error;
- pagination/empty result when relevant.

Then continue implementing. Do not rerun the entire MCP evaluation suite after every tool.

## REVIEW

Review the complete server against the actual workflows:

- tool discoverability and naming;
- schema precision and validation;
- structured output compatibility;
- auth and permission boundaries;
- destructive side effects;
- pagination and large responses;
- rate-limit/retry behavior;
- errors and secret redaction;
- timeouts/cancellation where relevant;
- transport/deployment assumptions;
- current protocol/SDK compatibility.

Exercise representative multi-tool workflows, not only isolated happy paths.

Look for redundant tools and opportunities to simplify the interface before adding more abstraction.

## MCP versus Agentit

This skill builds MCP servers.

`mcp-tooling-fit` chooses or configures an existing MCP/tool capability for a task.

Neither one authorizes credentials, installs, network access or external side effects by itself.

## Completion criteria

- priority workflows are possible through clear tools;
- inputs/outputs are typed and bounded;
- errors guide recovery without leaking secrets;
- high-impact effects are explicit and permission-safe;
- current MCP/SDK contracts were verified where material;
- representative workflows pass in REVIEW;
- the interface contains no speculative tools that lack a current use case.
