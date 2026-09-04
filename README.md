# aoa-tiktok-connector

Policy-gated TikTok evidence and draft-upload connector for AoA.

[Privacy Policy](PRIVACY.md) · [Terms of Service](TERMS.md)

Phase 1 prepares a bounded TikTok Display API read path for an authorized owner
account. It keeps credentials outside Git and cannot publish content.

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

## Connect the owner account

Start in TikTok Developer Portal Sandbox, add Login Kit and Display API, and
request only `user.info.basic` plus `video.list`. See
[`docs/SETUP_TIKTOK.md`](docs/SETUP_TIKTOK.md).

## Bootstrap checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-tiktok doctor --json
```

A green bootstrap proves only the prepared source adapter. It does not prove a
valid OAuth token, deployment, publication, or consumer acceptance.
