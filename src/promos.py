"""Promo codes for free AI months (and similar grants)."""

from __future__ import annotations

from src.database import (
    has_redeemed_promo,
    record_payment,
    record_promo_redemption,
    set_subscription,
    upsert_user,
)

# Built-in codes. Values are intentionally simple for ops.
PROMO_CATALOG: dict[str, dict] = {
    "WAKACJE": {
        "product": "ai_subscription",
        "days": 30,
        "label": "1 miesiąc AI gratis",
        "max_redemptions": None,  # unlimited total
        "once_per_user": True,
    },
}


def normalize_code(code: str) -> str:
    return (code or "").strip().upper().replace(" ", "")


def describe_promo(code: str) -> dict | None:
    key = normalize_code(code)
    meta = PROMO_CATALOG.get(key)
    if not meta:
        return None
    return {"code": key, **meta}


async def redeem_promo(user_id: int, code: str) -> dict:
    meta = describe_promo(code)
    if not meta:
        raise ValueError("invalid_promo")

    await upsert_user(user_id, None, None, None)

    if meta.get("once_per_user") and await has_redeemed_promo(user_id, meta["code"]):
        raise ValueError("promo_already_used")

    days = int(meta["days"])
    product = meta["product"]
    await set_subscription(
        user_id,
        product,
        status="active",
        source=f"promo:{meta['code']}",
        days=days,
    )
    await record_promo_redemption(user_id, meta["code"], product, days)
    await record_payment(
        user_id,
        product,
        0,
        "promo",
        "promo",
        external_id=f"promo-{meta['code']}-{user_id}",
    )
    return {
        "ok": True,
        "code": meta["code"],
        "product": product,
        "days": days,
        "label": meta["label"],
        "message": f"Aktywowano: {meta['label']} ({days} dni).",
    }
