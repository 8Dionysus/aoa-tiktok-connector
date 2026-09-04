"""Offline CLI surface; it deliberately contains no provider client."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from aoa_tiktok_connector import CONNECTOR_ID, PROVIDER, __version__


def doctor_packet() -> dict[str, object]:
    """Return source-skeleton state without touching network or credentials."""
    return {
        "schema": "aoa_social_connector_doctor_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "version": __version__,
        "phase": "skeleton",
        "source_adapter": "not_implemented",
        "publication_adapter": "not_implemented",
        "network_touched": False,
        "write_effects_enabled": False,
        "runtime_deployed": False,
        "ready": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aoa-tiktok")
    subparsers = parser.add_subparsers(dest="command", required=True)
    doctor = subparsers.add_parser("doctor", help="report offline skeleton state")
    doctor.add_argument("--json", action="store_true", help="emit JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        packet = doctor_packet()
        if args.json:
            print(json.dumps(packet, indent=2, sort_keys=True))
        else:
            print(f"{CONNECTOR_ID}: Phase 0 skeleton; network and writes disabled")
        return 0
    return 2
