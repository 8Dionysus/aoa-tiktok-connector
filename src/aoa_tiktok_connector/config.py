"""Secret-safe local configuration for TikTok APIs."""

from __future__ import annotations

import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

CONNECTOR_ID = "aoa-tiktok-connector"
DEFAULT_CREDENTIALS_PATH = Path.home() / ".config" / CONNECTOR_ID / "credentials.env"
CREDENTIALS_FILE_ENV = "AOA_TIKTOK_CREDENTIALS_FILE"
ACCESS_TOKEN_ENV = "AOA_TIKTOK_ACCESS_TOKEN"

_TEMPLATE = """# Owner-local secret file for aoa-tiktok-connector.
# Keep mode 0600. Never commit or paste the token into chat.
AOA_TIKTOK_ACCESS_TOKEN=
"""


class ConfigError(ValueError):
    """Configuration is missing or violates the connector secret boundary."""


@dataclass(frozen=True)
class Credentials:
    access_token: str
    source_path: Path | None

    def safe_summary(self) -> dict[str, object]:
        return {
            "schema": "aoa_tiktok_credentials_check_v1",
            "credentials_file": str(self.source_path) if self.source_path else None,
            "source": "file" if self.source_path else "environment",
            "access_token_present": True,
            "access_token_exposed": False,
        }


def credentials_path(
    explicit: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    env = os.environ if environ is None else environ
    raw = explicit or env.get(CREDENTIALS_FILE_ENV)
    return Path(raw).expanduser() if raw else DEFAULT_CREDENTIALS_PATH


def initialize_credentials_file(
    explicit: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> tuple[Path, bool]:
    path = credentials_path(explicit, environ)
    if path.exists() or path.is_symlink():
        _validate_secret_file(path)
        return path, False
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(_TEMPLATE)
    os.chmod(path, 0o600)
    return path, True


def load_credentials(
    explicit: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Credentials:
    env = os.environ if environ is None else environ
    env_token = env.get(ACCESS_TOKEN_ENV, "").strip()
    source_path: Path | None = None
    values: dict[str, str] = {}
    if not env_token:
        source_path = credentials_path(explicit, env)
        _validate_secret_file(source_path)
        values = _parse_env_file(source_path)
    token = env_token or values.get(ACCESS_TOKEN_ENV, "").strip()
    if len(token) < 20:
        raise ConfigError(
            f"{ACCESS_TOKEN_ENV} is missing or too short; fill the owner-local credential file"
        )
    return Credentials(access_token=token, source_path=source_path)


def _validate_secret_file(path: Path) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ConfigError(
            f"credentials file is missing: {path}; run 'aoa-tiktok setup'"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ConfigError(f"credentials file must not be a symlink: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ConfigError(f"credentials path must be a regular file: {path}")
    if metadata.st_uid != os.getuid():
        raise ConfigError(f"credentials file must be owned by the current user: {path}")
    if stat.S_IMODE(metadata.st_mode) & 0o077:
        raise ConfigError(f"credentials file must have mode 0600: {path}")


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"invalid credentials line {number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key != ACCESS_TOKEN_ENV:
            raise ConfigError(f"unsupported credentials key on line {number}: {key}")
        if key in values:
            raise ConfigError(f"duplicate credentials key on line {number}: {key}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values
