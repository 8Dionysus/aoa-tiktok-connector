from __future__ import annotations

import json

import aoa_tiktok_connector.client as client_module
from aoa_tiktok_connector.client import TikTokClient
from aoa_tiktok_connector.config import Credentials


class FakeResponse:
    status = 200

    def __init__(self, payload: dict[str, object]) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def read(self, _limit: int) -> bytes:
        return self.body


def credentials() -> Credentials:
    return Credentials(access_token="act." + ("x" * 48), source_path=None)


def test_account_read_uses_bearer_header_not_query(monkeypatch) -> None:
    calls = []

    def fake_urlopen(request, *, timeout):
        calls.append((request, timeout))
        return FakeResponse(
            {
                "data": {"user": {"open_id": "u1", "display_name": "Owner"}},
                "error": {"code": "ok", "message": "", "log_id": "l1"},
            }
        )

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    account = TikTokClient(credentials()).get_account()
    assert account["open_id"] == "u1"
    request, timeout = calls[0]
    assert "access_token" not in request.full_url
    assert request.get_header("Authorization").startswith("Bearer act.")
    assert timeout == 20.0


def test_video_read_is_bounded_and_drops_unknown_fields(monkeypatch) -> None:
    def fake_urlopen(request, *, timeout):
        assert "video/list" in request.full_url
        body = json.loads(request.data.decode("utf-8"))
        assert body == {"max_count": 10}
        return FakeResponse(
            {
                "data": {
                    "videos": [{"id": "v1", "title": "Example", "unexpected": "drop"}],
                    "cursor": 99,
                    "has_more": True,
                },
                "error": {"code": "ok", "message": "", "log_id": "l1"},
            }
        )

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    page = TikTokClient(credentials()).list_videos(max_count=10)
    assert page["cursor"] == 99
    assert page["has_more"] is True
    assert page["videos"][0]["id"] == "v1"
    assert "unexpected" not in page["videos"][0]
