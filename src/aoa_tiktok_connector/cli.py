"""Fail-closed CLI for the TikTok Phase 1 read plane."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from aoa_tiktok_connector import CONNECTOR_ID, PROVIDER, __version__
from aoa_tiktok_connector.client import TikTokAPIError, TikTokClient, TikTokTransportError
from aoa_tiktok_connector.config import ConfigError, initialize_credentials_file, load_credentials
from aoa_tiktok_connector.evidence import evidence_page


def doctor_packet() -> dict[str, object]:
    """Return source state without touching credentials or the network."""
    return {
        "schema": "aoa_social_connector_doctor_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "version": __version__,
        "phase": "experimental",
        "source_adapter": "implemented_unadmitted",
        "publication_adapter": "not_implemented",
        "network_touched": False,
        "write_effects_enabled": False,
        "runtime_deployed": False,
        "ready": False,
    }


def _credentials_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--credentials-file",
        type=Path,
        help="owner-local credential file; defaults under ~/.config",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")


def _bounded_count(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= 20:
        raise argparse.ArgumentTypeError("max count must be between 1 and 20")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aoa-tiktok")
    subparsers = parser.add_subparsers(dest="command", required=True)
    doctor = subparsers.add_parser("doctor", help="report source state without network")
    doctor.add_argument("--json", action="store_true", help="emit JSON")

    setup = subparsers.add_parser("setup", help="create an empty mode-0600 credential file")
    _credentials_argument(setup)

    config_check = subparsers.add_parser(
        "config-check",
        help="validate credentials locally without an API request",
    )
    _credentials_argument(config_check)

    auth_check = subparsers.add_parser(
        "auth-check",
        help="perform one bounded read of the authorized profile",
    )
    _credentials_argument(auth_check)

    videos_list = subparsers.add_parser(
        "videos-list",
        help="read one bounded page of authorized public videos as evidence packets",
    )
    _credentials_argument(videos_list)
    videos_list.add_argument("--max-count", type=_bounded_count, default=20)
    videos_list.add_argument("--cursor", type=int, help="provider cursor from a previous page")
    return parser


def _emit(payload: dict[str, object], *, json_mode: bool, human: str) -> None:
    if json_mode:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(human)


def _emit_error(args: argparse.Namespace, category: str, message: str) -> int:
    payload = {
        "schema": "aoa_tiktok_error_v1",
        "connector_id": CONNECTOR_ID,
        "category": category,
        "message": message,
        "token_exposed": False,
    }
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)
    else:
        print(f"{CONNECTOR_ID}: {category}: {message}", file=sys.stderr)
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            packet = doctor_packet()
            _emit(
                packet,
                json_mode=args.json,
                human=(
                    f"{CONNECTOR_ID}: Phase 1 source prepared; "
                    "network idle and publication disabled"
                ),
            )
            return 0

        if args.command == "setup":
            path, created = initialize_credentials_file(args.credentials_file)
            packet = {
                "schema": "aoa_tiktok_setup_v1",
                "connector_id": CONNECTOR_ID,
                "credentials_file": str(path),
                "created": created,
                "mode": "0600",
                "contains_secret": False,
            }
            _emit(
                packet,
                json_mode=args.json,
                human=f"credentials template {'created' if created else 'already exists'}: {path}",
            )
            return 0

        credentials = load_credentials(args.credentials_file)
        if args.command == "config-check":
            packet = credentials.safe_summary()
            _emit(packet, json_mode=args.json, human="credentials valid; token not displayed")
            return 0

        client = TikTokClient(credentials)
        account = client.get_account()
        if args.command == "auth-check":
            packet = {
                "schema": "aoa_tiktok_auth_check_v1",
                "connector_id": CONNECTOR_ID,
                "provider": PROVIDER,
                "connected": True,
                "required_scope": "user.info.basic",
                "account": account,
                "network_effect": "read_only",
                "token_exposed": False,
            }
            _emit(
                packet,
                json_mode=args.json,
                human=f"connected: {account.get('display_name', 'unknown')}",
            )
            return 0

        if args.command == "videos-list":
            videos = client.list_videos(max_count=args.max_count, cursor=args.cursor)
            packet = evidence_page(account, videos)
            _emit(
                packet,
                json_mode=args.json,
                human=f"read {len(packet['items'])} authorized public video(s)",
            )
            return 0
    except ConfigError as exc:
        return _emit_error(args, "configuration", str(exc))
    except TikTokAPIError as exc:
        return _emit_error(args, "tiktok_api", str(exc))
    except TikTokTransportError as exc:
        return _emit_error(args, "transport", str(exc))

    return _emit_error(args, "internal", "unsupported command")
