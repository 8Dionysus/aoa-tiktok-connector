# Architecture

## Current source surface

```text
official provider API (not connected)
             |
      provider adapter (planned)
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

## Phase 0 components

- connector/manifest.json: declared capabilities and effect posture
- connector/schemas/: starter interoperability contracts
- connector/profiles/starter.json: secret-free offline profile
- src/: installable doctor CLI with no network path
- scripts/validate_connector.py: public-safety and identity checks
