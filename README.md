# aoa-tiktok-connector

Policy-gated TikTok evidence and draft-upload connector for AoA.

Phase 0 is an offline, policy-first skeleton. It makes no live API calls,
contains no credentials, and cannot publish content.

## Owned here

- TikTok-specific source policy and capability discovery
- normalized evidence-packet and publication-plan contracts
- provider-specific parsing, preparation, validation, and local decisions
- a fail-closed local CLI and repository validator

## Owned elsewhere

- cross-network campaign orchestration and editorial policy
- live MCP/HTTP composition, scheduling, queues, retries, and secret injection
- final publication authority and operator approval
- heavy captures, media, indexes, and generated corpora

## Current boundary

Broad research access is eligibility-gated and Direct Post has product-review and utility constraints. Phase 0 therefore targets authorized-display evidence and draft-first preparation; direct publication is not assumed.

Official documentation: https://developers.tiktok.com/

API terms, scopes, quotas, review requirements, and pricing can change. Recheck
the official documentation before implementing or admitting a live adapter.

## Bootstrap checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-tiktok doctor --json
```

A green bootstrap proves only the source skeleton. It does not prove API access,
OAuth, deployment, publication, or consumer acceptance.
