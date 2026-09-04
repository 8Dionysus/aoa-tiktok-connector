# aoa-tiktok-connector Agent Guide

## Owner

This repository owns the portable TikTok connector source surface.
It is independently publishable and must remain usable without sibling repos.

## Hard boundaries

- Use official, authorized provider APIs. Do not introduce scraping or bypasses by default.
- Keep credentials, tokens, account identifiers, raw exports, and media out of Git.
- Evidence reads and publication effects are separate planes.
- Publication stays disabled until an approval-gated effect owner is explicitly added.
- Runtime MCP/HTTP composition, queues, scheduling, retries, and secret injection belong to abyss-stack.
- Cross-platform campaign logic belongs to a future social orchestrator, not this connector.
- Treat provider policy, scopes, quotas, pricing, and review status as live facts to reverify.

## Provider boundary

Broad research access is eligibility-gated and Direct Post has product-review and utility constraints. Phase 0 therefore targets authorized-display evidence and draft-first preparation; direct publication is not assumed.

## Required checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-tiktok doctor --json
```

Do not claim live capability from these checks alone.
