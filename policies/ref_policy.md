# Doc-First Policy (Ref MCP)

Before any infra/cloud/auth/SDK/IaC change:
1) Call `ref.search_documentation` with service, SDK/library version, and task.
2) Paste a short bullet summary + official URL.
3) Compare docs against repo config (versions, IaC).
4) If mismatch, STOP and propose a reconciliation plan.
5) Default to `response_format="concise"`; request detailed only when identifiers are required.