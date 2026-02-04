from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict

from jose import jwt

from infrastructure.config import settings


def _load_key(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def create_access_token(subject: str, role: str, company_id: str | None) -> str:
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
        "company_id": company_id,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_access_ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, _load_key(settings.jwt_private_key_path), algorithm="RS256")


def create_refresh_token(subject: str, token_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "jti": token_id,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=settings.jwt_refresh_ttl_days)).timestamp()),
    }
    return jwt.encode(payload, _load_key(settings.jwt_private_key_path), algorithm="RS256")


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        _load_key(settings.jwt_public_key_path),
        algorithms=["RS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )
