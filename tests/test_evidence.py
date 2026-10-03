from __future__ import annotations

from aoa_tiktok_connector.evidence import evidence_page


def test_evidence_page_preserves_provenance() -> None:
    page = evidence_page(
        {"open_id": "u1", "display_name": "Owner"},
        {
            "videos": [{"id": "v1", "share_url": "https://www.tiktok.com/@owner/video/v1"}],
            "cursor": 99,
            "has_more": True,
        },
        observed_at="2026-09-04T12:00:00Z",
    )
    assert page["network_effect"] == "read_only"
    assert page["next_cursor"] == 99
    assert page["has_more"] is True
    packet = page["items"][0]
    assert packet["permission_basis"] == "tiktok_display_api:video.list"
    assert packet["source_url"] == "https://www.tiktok.com/@owner/video/v1"
