"""Stripe Checkout + mock billing for local/demo mode."""

from __future__ import annotations

import logging
from urllib.parse import urlencode

import httpx

from src.config import (
    PLAN_PRICES,
    PUBLIC_BASE_URL,
    STRIPE_PRICE_AI_MONTHLY,
    STRIPE_PRICE_HUMAN_REVIEW,
    STRIPE_SECRET_KEY,
)

logger = logging.getLogger(__name__)


def stripe_configured() -> bool:
    return bool((STRIPE_SECRET_KEY or "").strip())


def price_id_for(product: str) -> str:
    if product == "ai_subscription":
        return STRIPE_PRICE_AI_MONTHLY
    if product == "human_review":
        return STRIPE_PRICE_HUMAN_REVIEW
    return ""


async def create_checkout_session(user_id: int, product: str) -> dict:
    if product not in PLAN_PRICES:
        raise ValueError("unknown_product")

    if stripe_configured() and price_id_for(product):
        return await _stripe_checkout(user_id, product)

    # Demo/mock checkout that activates entitlement without Stripe keys.
    qs = urlencode({"user_id": user_id, "product": product})
    return {
        "mode": "mock",
        "checkout_url": f"{PUBLIC_BASE_URL}/api/billing/mock-complete?{qs}",
        "product": product,
        "amount_pln": PLAN_PRICES[product]["amount_pln"],
    }


async def _stripe_checkout(user_id: int, product: str) -> dict:
    price = price_id_for(product)
    data = {
        "mode": "subscription" if product == "ai_subscription" else "payment",
        "success_url": f"{PUBLIC_BASE_URL}/?billing=success&product={product}",
        "cancel_url": f"{PUBLIC_BASE_URL}/?billing=cancel",
        "line_items[0][price]": price,
        "line_items[0][quantity]": "1",
        "metadata[user_id]": str(user_id),
        "metadata[product]": product,
        "client_reference_id": str(user_id),
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.stripe.com/v1/checkout/sessions",
                data=data,
                auth=(STRIPE_SECRET_KEY, ""),
            )
            resp.raise_for_status()
            payload = resp.json()
            return {
                "mode": "stripe",
                "checkout_url": payload["url"],
                "session_id": payload["id"],
                "product": product,
                "amount_pln": PLAN_PRICES[product]["amount_pln"],
            }
    except Exception:
        logger.warning("Stripe checkout failed; falling back to mock", exc_info=True)
        qs = urlencode({"user_id": user_id, "product": product})
        return {
            "mode": "mock",
            "checkout_url": f"{PUBLIC_BASE_URL}/api/billing/mock-complete?{qs}",
            "product": product,
            "amount_pln": PLAN_PRICES[product]["amount_pln"],
        }
