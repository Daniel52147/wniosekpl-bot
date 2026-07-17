"""Persist secrets from /setup UI and overlay them onto process env + config."""

from __future__ import annotations

import os
from pathlib import Path

from src.config import ROOT

SECRETS_PATH = Path(os.getenv("RUNTIME_SECRETS_PATH", str(ROOT / "data" / "secrets.env")))

ALLOWED_KEYS = {
    "STRIPE_SECRET_KEY",
    "STRIPE_PUBLISHABLE_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "STRIPE_PRICE_AI_MONTHLY",
    "STRIPE_PRICE_HUMAN_REVIEW",
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
    "FACEBOOK_APP_ID",
    "FACEBOOK_APP_SECRET",
    "APP_SECRET",
    "OPENAI_API_KEY",
    "OMNIROUTE_API_KEY",
    "OMNIROUTE_BASE_URL",
    "SMTP_HOST",
    "SMTP_FROM",
    "PUBLIC_BASE_URL",
    "ADMIN_API_KEY",
}


def load_runtime_secrets() -> dict[str, str]:
    if not SECRETS_PATH.exists():
        return {}
    out: dict[str, str] = {}
    for line in SECRETS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k in ALLOWED_KEYS:
            out[k] = v.strip()
    return out


def apply_runtime_secrets() -> dict[str, str]:
    """Load secrets into os.environ and refresh src.config module attributes."""
    import src.config as config

    secrets = load_runtime_secrets()
    for k, v in secrets.items():
        os.environ[k] = v
        if hasattr(config, k):
            setattr(config, k, v)
    # derived flags
    if "PUBLIC_BASE_URL" in secrets:
        config.PUBLIC_BASE_URL = secrets["PUBLIC_BASE_URL"].rstrip("/")
    return secrets


def save_runtime_secrets(updates: dict[str, str]) -> dict[str, str]:
    current = load_runtime_secrets()
    for k, v in updates.items():
        if k not in ALLOWED_KEYS:
            continue
        val = (v or "").strip()
        if val:
            current[k] = val
        elif k in current and v == "":
            # explicit empty clears
            current.pop(k, None)
    SECRETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{k}={current[k]}" for k in sorted(current)]
    SECRETS_PATH.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return apply_runtime_secrets()


def setup_status() -> dict:
    apply_runtime_secrets()
    import src.config as config
    from src.oauth import facebook_configured, google_configured
    from src.payments import stripe_configured, stripe_webhook_configured

    return {
        "public_base_url": config.PUBLIC_BASE_URL,
        "stripe": stripe_configured(),
        "stripe_webhook": stripe_webhook_configured(),
        "stripe_prices": bool(config.STRIPE_PRICE_AI_MONTHLY and config.STRIPE_PRICE_HUMAN_REVIEW),
        "google": google_configured(),
        "facebook": facebook_configured(),
        "app_secret_set": bool(config.APP_SECRET and "change-me" not in config.APP_SECRET),
        "redirects": {
            "google": f"{config.PUBLIC_BASE_URL}/api/auth/google/callback",
            "facebook": f"{config.PUBLIC_BASE_URL}/api/auth/facebook/callback",
            "stripe_webhook": f"{config.PUBLIC_BASE_URL}/api/billing/webhook",
        },
    }
