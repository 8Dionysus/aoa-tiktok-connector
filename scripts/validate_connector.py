#!/usr/bin/env python3
"""Validate the symmetric TikTok connector source surface."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONNECTOR_ID = "aoa-tiktok-connector"
PROVIDER = "tiktok"
REQUIRED = (
    ".env.example",
    ".github/workflows/validate.yml",
    ".gitignore",
    "AGENTS.md",
    "BOUNDARIES.md",
    "CHANGELOG.md",
    "CHARTER.md",
    "LICENSE",
    "PRIVACY.md",
    "README.md",
    "ROADMAP.md",
    "STATUS.md",
    "TERMS.md",
    "assets/app-icon.png",
    "connector/SOURCE_POLICY.md",
    "connector/STORAGE_POLICY.md",
    "connector/fixtures/README.md",
    "connector/manifest.json",
    "connector/profiles/starter.json",
    "connector/schemas/capability_manifest.schema.json",
    "connector/schemas/evidence_packet.schema.json",
    "connector/schemas/publication_plan.schema.json",
    "connector/schemas/publication_receipt.schema.json",
    "docs/ARCHITECTURE.md",
    "docs/RUNTIME_CONTRACT.md",
    "docs/SETUP_TIKTOK.md",
    "docs/decisions/README.md",
    "docs/decisions/AOA-TIKTOK-D-0001-independent-provider-owner.md",
    "evals/README.md",
    "pyproject.toml",
    "stats/README.md",
    "src/aoa_tiktok_connector/__init__.py",
    "src/aoa_tiktok_connector/__main__.py",
    "src/aoa_tiktok_connector/cli.py",
    "src/aoa_tiktok_connector/client.py",
    "src/aoa_tiktok_connector/config.py",
    "src/aoa_tiktok_connector/evidence.py",
    "tests/test_cli.py",
    "tests/test_client.py",
    "tests/test_config.py",
    "tests/test_evidence.py",
)
FORBIDDEN_NAMES = {".env", "client_secret.json", "credentials.json", "token.json"}
FORBIDDEN_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".zip", ".sqlite", ".db"}
IGNORED_PARTS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__"}


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing:{relative}")

    json_paths = sorted((ROOT / "connector").rglob("*.json"))
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid_json:{path.relative_to(ROOT)}:{exc}")

    manifest_path = ROOT / "connector" / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("connector_id") != CONNECTOR_ID:
            errors.append("manifest_connector_id_mismatch")
        if manifest.get("provider") != PROVIDER:
            errors.append("manifest_provider_mismatch")
        commit = manifest.get("planes", {}).get("publication_commit", {})
        if commit.get("status") != "disabled":
            errors.append("publication_commit_must_be_disabled")
        if commit.get("requires_approval") is not True:
            errors.append("publication_commit_must_require_approval")
        policy = manifest.get("policy", {})
        if policy.get("scraping_enabled") is not False:
            errors.append("scraping_must_be_disabled")
        if policy.get("credentials_in_repo") is not False:
            errors.append("credentials_must_be_outside_repo")

    for path in ROOT.rglob('*'):
        if not path.is_file() or IGNORED_PARTS.intersection(path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"forbidden_file:{relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden_artifact:{relative}")
        if path.stat().st_size > 1_000_000:
            errors.append(f"oversized_file:{relative}")
        if path.suffix.lower() in {'.md', '.py', '.toml', '.yml', '.yaml', '.json', '.example'}:
            content = path.read_text(encoding="utf-8", errors="ignore")
            private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
            if private_key_marker in content:
                errors.append(f"private_key_material:{relative}")

    result = {
        "schema": "aoa_social_connector_validation_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "ok": not errors,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
