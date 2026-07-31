"""Email/password + OAuth account lifecycle."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from src.auth import hash_token, issue_session, new_token
from src.database import (
    create_email_token,
    create_web_user,
    consume_email_token,
    get_user_by_email,
    get_user_by_facebook,
    get_user_by_google,
    get_user_profile,
    link_oauth_identity,
    set_password_hash,
    set_user_profile_fields,
    upsert_user,
)
from src.notifications import notify_user
from src.passwords import hash_password, verify_password
from src.config import PUBLIC_BASE_URL

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> str:
    email = (email or "").strip().lower()
    if not EMAIL_RE.match(email) or len(email) > 200:
        raise ValueError("invalid_email")
    return email


def validate_password(password: str) -> str:
    if len(password or "") < 8:
        raise ValueError("password_too_short")
    if len(password) > 128:
        raise ValueError("password_too_long")
    return password


async def register_with_password(
    email: str,
    password: str,
    *,
    name: str = "",
    lang: str = "ru",
) -> dict:
    email = validate_email(email)
    password = validate_password(password)
    existing = await get_user_by_email(email)
    if existing:
        raise ValueError("email_taken")
    user_id = await create_web_user(
        email=email,
        password_hash=hash_password(password),
        display_name=(name or email.split("@")[0])[:80],
        lang=lang,
        provider="password",
    )
    verify_tok = new_token()
    expires = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    await create_email_token(hash_token(verify_tok), user_id, email, "verify", expires)
    link = f"{PUBLIC_BASE_URL}/api/auth/verify-email?token={verify_tok}"
    await notify_user(
        user_id=user_id,
        email=email,
        subject="WniosekPL — potwierdź email",
        body=f"Confirm your email: {link}",
    )
    session = await issue_session(user_id, label="password")
    return {
        "user": await public_user(user_id),
        "session": session,
        "verify_url": link,
    }


async def login_with_password(email: str, password: str) -> dict:
    email = validate_email(email)
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.get("password_hash")):
        raise ValueError("invalid_credentials")
    session = await issue_session(int(user["telegram_id"]), label="password")
    return {"user": await public_user(int(user["telegram_id"])), "session": session}


async def login_or_register_oauth(profile: dict) -> dict:
    provider = profile["provider"]
    provider_id = profile["provider_id"]
    email = (profile.get("email") or "").lower()
    name = (profile.get("name") or "")[:80]

    user = None
    if provider == "google":
        user = await get_user_by_google(provider_id)
    elif provider == "facebook":
        user = await get_user_by_facebook(provider_id)

    if not user and email:
        user = await get_user_by_email(email)

    if user:
        user_id = int(user["telegram_id"])
        await link_oauth_identity(
            user_id,
            provider=provider,
            provider_id=provider_id,
            email=email or user.get("email"),
            name=name or user.get("display_name") or user.get("first_name"),
            email_verified=bool(profile.get("email_verified")),
        )
    else:
        if not email:
            raise ValueError("oauth_email_required")
        user_id = await create_web_user(
            email=email,
            password_hash=None,
            display_name=name or email.split("@")[0],
            lang="ru",
            provider=provider,
            google_id=provider_id if provider == "google" else None,
            facebook_id=provider_id if provider == "facebook" else None,
            email_verified=bool(profile.get("email_verified")),
        )

    session = await issue_session(user_id, label=provider)
    return {"user": await public_user(user_id), "session": session}


async def verify_email_token(token: str) -> int:
    row = await consume_email_token(hash_token(token), purpose="verify")
    if not row:
        raise ValueError("invalid_or_expired_token")
    user_id = int(row["telegram_id"])
    await set_user_profile_fields(user_id, email_verified=True)
    return user_id


async def request_password_reset(email: str) -> dict:
    email = validate_email(email)
    user = await get_user_by_email(email)
    # Always ok to avoid email enumeration.
    if not user:
        return {"ok": True}
    user_id = int(user["telegram_id"])
    tok = new_token()
    expires = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    await create_email_token(hash_token(tok), user_id, email, "reset", expires)
    link = f"{PUBLIC_BASE_URL}/?reset_token={tok}#account"
    await notify_user(
        user_id=user_id,
        email=email,
        subject="WniosekPL — reset hasła",
        body=f"Reset password: {link}",
    )
    return {"ok": True, "reset_url": link}


async def reset_password(token: str, password: str) -> dict:
    password = validate_password(password)
    row = await consume_email_token(hash_token(token), purpose="reset")
    if not row:
        raise ValueError("invalid_or_expired_token")
    user_id = int(row["telegram_id"])
    await set_password_hash(user_id, hash_password(password))
    session = await issue_session(user_id, label="password_reset")
    return {"user": await public_user(user_id), "session": session}


async def public_user(user_id: int) -> dict:
    await upsert_user(user_id, None, None, None)
    row = await get_user_profile(user_id) or {}
    return {
        "user_id": user_id,
        "email": row.get("email"),
        "name": row.get("display_name") or row.get("first_name") or "",
        "email_verified": bool(row.get("email_verified")),
        "auth_provider": row.get("auth_provider") or "anonymous",
        "has_password": bool(row.get("password_hash")),
        "google_linked": bool(row.get("google_id")),
        "facebook_linked": bool(row.get("facebook_id")),
        "stripe_customer_id": row.get("stripe_customer_id"),
    }
