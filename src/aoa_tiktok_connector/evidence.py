"""Normalize authorized TikTok videos into AoA evidence packets."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from aoa_tiktok_connector import CONNECTOR_ID, PROVIDER


def evidence_page(
    account: dict[str, Any],
    videos_page: dict[str, Any],
    *,
    observed_at: str | None = None,
) -> dict[str, Any]:
    timestamp = observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    packets: list[dict[str, Any]] = []
    for video in videos_page.get("videos", []):
        if not isinstance(video, dict) or not video.get("id"):
            continue
        source_url = str(
            video.get("share_url") or video.get("embed_link") or "https://www.tiktok.com/"
        )
        packets.append(
            {
                "schema": "aoa_social_evidence_packet_v1",
                "provider": PROVIDER,
                "source_id": str(video["id"]),
                "source_url": source_url,
                "observed_at": timestamp,
                "permission_basis": "tiktok_display_api:video.list",
                "payload": dict(video),
            }
        )
    return {
        "schema": "aoa_social_evidence_page_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "observed_at": timestamp,
        "account": dict(account),
        "items": packets,
        "next_cursor": videos_page.get("cursor"),
        "has_more": bool(videos_page.get("has_more", False)),
        "network_effect": "read_only",
    }
