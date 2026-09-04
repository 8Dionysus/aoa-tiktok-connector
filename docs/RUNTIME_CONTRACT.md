# Runtime Contract

There is no live runtime in Phase 0.

When admitted, abyss-stack owns deployment composition, process supervision, secret
injection, MCP/HTTP exposure, schedules, queues, retries, and runtime health. This
repository supplies an installable package and provider behavior.

A future runtime must preserve:

- evidence reads as read-only operations
- draft and publication-plan creation as no-effect operations
- publication commit as a separately authorized external write
- account allowlists, idempotency keys, and durable receipts
- processing/public-visibility state distinct from submission success
- revocation, retention, deletion, quota, and cost controls

Source validation is not runtime admission, and runtime health is not consumer acceptance.
