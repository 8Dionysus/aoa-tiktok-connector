# Roadmap

## Phase 0 — repository skeleton

- [x] independent owner repository
- [x] shared contract schemas
- [x] provider policy snapshot
- [x] offline doctor, validator, tests, and CI

## Phase 1 — evidence adapter

- [ ] reverify official API, scopes, quotas, terms, and review path
- [ ] add OAuth or app-auth flow using operator-local secret storage
- [ ] implement bounded reads and normalized evidence packets
- [ ] add synthetic fixtures and policy/negative tests

## Phase 2 — preparation

- [ ] validate media and metadata before upload
- [ ] produce deterministic drafts and publication plans
- [ ] add idempotency and dry-run contracts

## Phase 3 — effect admission

- [ ] add explicit operator approval and account allowlists
- [ ] return durable publication receipts and processing state
- [ ] compose in abyss-stack and prove an ordinary consumer path

Cross-platform orchestration remains a separate future owner.

## Evidence and measurement admission

This source package supplies no eval verdicts or live metrics. Test results
remain test evidence, not automatically admitted proof. When these surfaces
become real, evals should cover policy denial, evidence provenance,
normalization, media validation, idempotency, and publication-plan safety.
Runtime measurements must distinguish requests, authorized and denied
reads, cost/quota use, prepared plans, approved submissions, processing
outcomes, publication outcomes, and consumer-observed acceptance. Add
content-bearing owner surfaces when that work is admitted; empty placeholder
districts are not required beforehand.
