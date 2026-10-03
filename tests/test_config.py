from __future__ import annotations

import stat

import pytest

from aoa_tiktok_connector.config import (
    ACCESS_TOKEN_ENV,
    ConfigError,
    initialize_credentials_file,
    load_credentials,
)

TOKEN = "act." + ("x" * 48)


def test_initialize_and_load_credentials(tmp_path) -> None:
    path = tmp_path / "credentials.env"
    created_path, created = initialize_credentials_file(path, environ={})
    assert created is True
    assert created_path == path
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    path.write_text(f"{ACCESS_TOKEN_ENV}={TOKEN}\n", encoding="utf-8")
    path.chmod(0o600)
    credentials = load_credentials(path, environ={})
    assert credentials.access_token == TOKEN
    assert credentials.safe_summary()["access_token_exposed"] is False


def test_rejects_group_readable_credentials(tmp_path) -> None:
    path = tmp_path / "credentials.env"
    path.write_text(f"{ACCESS_TOKEN_ENV}={TOKEN}\n", encoding="utf-8")
    path.chmod(0o640)
    with pytest.raises(ConfigError, match="mode 0600"):
        load_credentials(path, environ={})


def test_environment_credentials_do_not_require_a_file() -> None:
    credentials = load_credentials("/does/not/exist", environ={ACCESS_TOKEN_ENV: TOKEN})
    assert credentials.source_path is None
    assert credentials.safe_summary()["source"] == "environment"
