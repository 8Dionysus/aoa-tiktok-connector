# Source Policy

Provider: TikTok

Policy snapshot: 2026-09-04. Reverify all live conditions before adapter work.

## Planned official surfaces

- read: authorized_profile
- read: authorized_public_videos
- publication-plan target: draft_upload
- deferred: direct_post
- deferred: research_api
- deferred: arbitrary_public_search

## Admission rules

- Official provider APIs and authorized accounts only.
- Every observation records source identity, time, URL, and permission basis.
- Account allowlists and topic allowlists are explicit configuration.
- Rate, quota, cost, retention, deletion, and review obligations fail closed.
- HTML scraping, session-cookie automation, CAPTCHA bypass, and stealth collection are out of scope.
- API success does not establish public visibility or consumer acceptance.

## Current provider boundary

Broad research access is eligibility-gated and Direct Post has product-review and utility constraints. Phase 0 therefore targets authorized-display evidence and draft-first preparation; direct publication is not assumed.

Official documentation: https://developers.tiktok.com/
