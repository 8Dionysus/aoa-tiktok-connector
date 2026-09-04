# AOA-TIKTOK-D-0001 — Independent TikTok connector owner

- Status: Accepted
- Date: 2026-09-04
- Accepted by: Operator

## Context

AoA needs agents to collect and select social-network evidence and later prepare
publication drafts from governed material. Instagram, X, Pinterest, TikTok, and
YouTube share workflow concepts but differ materially in authorization, data access,
review, quota, cost, media, processing, and publication semantics.

## Decision

Keep TikTok in its own independently publishable repository: aoa-tiktok-connector.
Use a symmetric social-connector contract for evidence, drafts, publication plans,
and receipts. Keep cross-platform orchestration in a future separate owner and keep
effectful publication disabled until an approval-gated runtime is admitted.

## Alternatives considered

- One aoa-social-connector containing every provider.
- Group providers by media shape, such as short video or image networks.
- Independent provider connectors with a shared contract and later orchestrator.

The third alternative is accepted.

## Rationale

Provider policy and capability changes should be reviewable, releasable, and
reversible without coupling unrelated networks. Symmetry belongs in contracts and
validation, while authentication and provider behavior remain owner-local.

## Consequences

- Some scaffolding is intentionally duplicated across connector repositories.
- Shared contract evolution must be coordinated explicitly.
- A platform may advance at a different pace without weakening another provider.
- No connector gains autonomous publication authority from this decision.

## Provider boundary

Broad research access is eligibility-gated and Direct Post has product-review and utility constraints. Phase 0 therefore targets authorized-display evidence and draft-first preparation; direct publication is not assumed.

## Source surfaces

- README.md
- CHARTER.md
- BOUNDARIES.md
- connector/manifest.json
- connector/SOURCE_POLICY.md
- connector/schemas/
- docs/RUNTIME_CONTRACT.md

## Effect authority

None in Phase 0. Publication commit remains disabled and requires a later explicit
operator-approved runtime contract.
