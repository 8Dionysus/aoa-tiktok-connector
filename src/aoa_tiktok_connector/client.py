"""Bounded read-only client for TikTok Display API v2."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from aoa_tiktok_connector import CONNECTOR_ID, __version__
from aoa_tiktok_connector.config import Credentials

API_BASE_URL = "https://open.tiktokapis.com/v2"
ACCOUNT_FIELDS = ("open_id", "union_id", "avatar_url", "display_name")
VIDEO_FIELDS = (
    "id",
    "title",
    "video_description",
    "duration",
    "cover_image_url",
    "embed_link",
    "share_url",
    "create_time",
)


class TikTokError(RuntimeError):
    """Base class for safe connector failures."""


class TikTokTransportError(TikTokError):
    """The API could not be reached or returned malformed transport data."""


@dataclass(frozen=True)
class TikTokAPIError(TikTokError):
    status: int | None
    code: str | None
    safe_message: str
    log_id: str | None

    def __str__(self) -> str:
        parts = [self.safe_message]
        if self.code:
            parts.append(f"code={self.code}")
        if self.status is not None:
            parts.append(f"http={self.status}")
        if self.log_id:
            parts.append(f"log_id={self.log_id}")
        return "; ".join(parts)


class TikTokClient:
    def __init__(
        self,
        credentials: Credentials,
        *,
        timeout_seconds: float = 20.0,
        max_response_bytes: int = 2_000_000,
    ) -> None:
        self.credentials = credentials
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def get_account(self) -> dict[str, Any]:
        fields = ",".join(ACCOUNT_FIELDS)
        payload = self._request("GET", "user/info/", {"fields": fields})
        data = payload.get("data")
        candidate = data.get("user") if isinstance(data, dict) else None
        if not isinstance(candidate, dict) or not candidate.get("open_id"):
            raise TikTokTransportError("TikTok user info response lacked a user")
        return {
            field: candidate[field]
            for field in ACCOUNT_FIELDS
            if field in candidate and candidate[field] is not None
        }

    def list_videos(
        self,
        *,
        max_count: int = 20,
        cursor: int | None = None,
    ) -> dict[str, Any]:
        if not 1 <= max_count <= 20:
            raise ValueError("max count must be between 1 and 20")
        body: dict[str, object] = {"max_count": max_count}
        if cursor is not None:
            body["cursor"] = cursor
        fields = ",".join(VIDEO_FIELDS)
        payload = self._request("POST", "video/list/", {"fields": fields}, body=body)
        data = payload.get("data")
        if not isinstance(data, dict) or not isinstance(data.get("videos"), list):
            raise TikTokTransportError("TikTok video list response lacked videos")
        videos: list[dict[str, Any]] = []
        for candidate in data["videos"]:
            if not isinstance(candidate, dict) or not candidate.get("id"):
                continue
            videos.append(
                {
                    field: candidate[field]
                    for field in VIDEO_FIELDS
                    if field in candidate and candidate[field] is not None
                }
            )
        return {
            "videos": videos,
            "cursor": data.get("cursor"),
            "has_more": bool(data.get("has_more", False)),
        }

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, str],
        *,
        body: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        query = f"?{urlencode(params)}" if params else ""
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = Request(
            f"{API_BASE_URL}/{path}{query}",
            data=data,
            headers={
                "Authorization": f"Bearer {self.credentials.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": f"{CONNECTOR_ID}/{__version__}",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                status = getattr(response, "status", 200)
                raw = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            raw = exc.read(self.max_response_bytes + 1)
            payload = self._decode_json(raw, allow_error=True)
            raise self._api_error(payload, status=exc.code) from None
        except (URLError, TimeoutError, OSError) as exc:
            raise TikTokTransportError(
                f"TikTok API transport failed: {type(exc).__name__}"
            ) from None
        if len(raw) > self.max_response_bytes:
            raise TikTokTransportError("TikTok API response exceeded the size limit")
        payload = self._decode_json(raw)
        error = payload.get("error")
        if isinstance(error, dict) and error.get("code") not in {None, "", "ok"}:
            raise self._api_error(payload, status=status)
        return payload

    def _decode_json(self, raw: bytes, *, allow_error: bool = False) -> dict[str, Any]:
        if len(raw) > self.max_response_bytes:
            raise TikTokTransportError("TikTok API response exceeded the size limit")
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            if allow_error:
                return {}
            raise TikTokTransportError("TikTok API returned invalid JSON") from None
        if not isinstance(payload, dict):
            raise TikTokTransportError("TikTok API returned a non-object JSON response")
        return payload

    def _api_error(self, payload: dict[str, Any], *, status: int | None) -> TikTokAPIError:
        error = payload.get("error")
        if not isinstance(error, dict):
            error = payload
        message = str(error.get("message") or "TikTok API request failed")
        safe_message = message.replace(self.credentials.access_token, "[redacted]")
        return TikTokAPIError(
            status=status,
            code=str(error["code"]) if error.get("code") is not None else None,
            safe_message=safe_message,
            log_id=str(error["log_id"]) if error.get("log_id") else None,
        )
