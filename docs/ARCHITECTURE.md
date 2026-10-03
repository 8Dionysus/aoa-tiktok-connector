# Architecture

## Current source surface

```text
TikTok Display API (OAuth not connected)
             |
      bounded read adapter
             |
 policy gate -> normalized evidence packet
             |
       agent selection/preparation
             |
 publication plan (no external effect)
             |
 approval-gated publisher/runtime (external owner, disabled)
```

The repository owns provider-specific interpretation and portable contracts.
A future social orchestrator may coordinate multiple connectors through those
contracts, but it must not absorb provider credentials or policy decisions.

## Current components

- connector/manifest.json: declared capabilities and effect posture
- connector/schemas/: starter interoperability contracts
- connector/profiles/starter.json: secret-free offline profile
- src/: strict local credentials, bounded profile/video reads, evidence normalization, CLI
- scripts/validate_connector.py: public-safety and identity checks
