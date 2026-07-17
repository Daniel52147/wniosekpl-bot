"""Google / Facebook OAuth2 helpers (Authlib + httpx)."""

from __future__ import annotations

import logging
import secrets
from urllib.parse import urlencode

import httpx
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from src.config import (
    APP_SECRET,
    FACEBOOK_APP_ID,
    FACEBOOK_APP_SECRET,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    PUBLIC_BASE_URL,
)

logger = logging.getLogger(__name__)


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(APP_SECRET, salt="wniosekpl-oauth")


def google_configured() -> bool:
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def facebook_configured() -> bool:
    return bool(FACEBOOK_APP_ID and FACEBOOK_APP_SECRET)


def make_state(provider: str, user_id: int | None = None) -> str:
    return _serializer().dumps(
        {"provider": provider, "nonce": secrets.token_hex(8), "uid": user_id}
    )


def parse_state(state: str, max_age: int = 600) -> dict:
    try:
        return _serializer().loads(state, max_age=max_age)
    except SignatureExpired as exc:
        raise ValueError("state_expired") from exc
    except BadSignature as exc:
        raise ValueError("state_invalid") from exc


def google_authorize_url(state: str) -> str:
    qs = urlencode(
        {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": f"{PUBLIC_BASE_URL}/api/auth/google/callback",
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "online",
            "prompt": "select_account",
        }
    )
    return f"https://accounts.google.com/o/oauth2/v2/auth?{qs}"


def facebook_authorize_url(state: str) -> str:
    qs = urlencode(
        {
            "client_id": FACEBOOK_APP_ID,
            "redirect_uri": f"{PUBLIC_BASE_URL}/api/auth/facebook/callback",
            "state": state,
            "scope": "email,public_profile",
        }
    )
    return f"https://www.facebook.com/v19.0/dialog/oauth?{qs}"


async def google_exchange(code: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{PUBLIC_BASE_URL}/api/auth/google/callback",
                "grant_type": "authorization_code",
            },
        )
        token_resp.raise_for_status()
        tokens = token_resp.json()
        user_resp = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        user_resp.raise_for_status()
        profile = user_resp.json()
    return {
        "provider": "google",
        "provider_id": profile["sub"],
        "email": (profile.get("email") or "").lower(),
        "name": profile.get("name") or profile.get("given_name") or "",
        "email_verified": bool(profile.get("email_verified")),
    }


async def facebook_exchange(code: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        token_resp = await client.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "client_id": FACEBOOK_APP_ID,
                "client_secret": FACEBOOK_APP_SECRET,
                "redirect_uri": f"{PUBLIC_BASE_URL}/api/auth/facebook/callback",
                "code": code,
            },
        )
        token_resp.raise_for_status()
        tokens = token_resp.json()
        user_resp = await client.get(
            "https://graph.facebook.com/me",
            params={
                "fields": "id,name,email",
                "access_token": tokens["access_token"],
            },
        )
        user_resp.raise_for_status()
        profile = user_resp.json()
    return {
        "provider": "facebook",
        "provider_id": str(profile["id"]),
        "email": (profile.get("email") or "").lower(),
        "name": profile.get("name") or "",
        "email_verified": bool(profile.get("email")),
    }
