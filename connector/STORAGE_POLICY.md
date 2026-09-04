# Storage Policy

Repository Git may contain code, schemas, policies, small synthetic fixtures, and
reviewed documentation only.

Operator-local state belongs outside Git. The suggested host-managed root is:

    /srv/abyss-machine/storage/connectors/aoa-tiktok-connector

Portable deployments may override it with AOA_TIKTOK_CONNECTOR_STATE_ROOT.

Never commit tokens, refresh tokens, client secrets, cookies, account identifiers,
raw exports, downloaded media, indexes, publication payloads, or receipts containing
private account data. Runtime retention and deletion policy must be configured before
live admission.
