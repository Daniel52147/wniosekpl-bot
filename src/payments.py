"""Full Stripe billing: checkout, portal, invoices, subscriptions, webhooks + mock."""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx

import src.config as config
from src.config import PLAN_PRICES
from src.database import (
    clear_subscription,
    get_subscription,
    get_user_profile,
    list_payments,
    payment_by_external_id,
    record_payment,
    set_stripe_customer_id,
    set_subscription,
    update_subscription_record,
    upsert_user,
)
from src.entitlements import mark_human_review_purchased

logger = logging.getLogger(__name__)


def stripe_configured() -> bool:
    return bool((config.STRIPE_SECRET_KEY or "").strip())


def stripe_webhook_configured() -> bool:
    return bool((config.STRIPE_WEBHOOK_SECRET or "").strip())


def mock_billing_allowed() -> bool:
    """Mock unlock is only for demos without Stripe (or explicit opt-in)."""
    import os

    flag = (os.getenv("ALLOW_MOCK_BILLING") or "").strip().lower()
    if flag in {"1", "true", "yes", "on"}:
        return True
    if flag in {"0", "false", "no", "off"}:
        return False
    return not stripe_configured()


def price_id_for(product: str) -> str:
    if product == "ai_subscription":
        return (config.STRIPE_PRICE_AI_MONTHLY or "").strip()
    if product == "human_review":
        return (config.STRIPE_PRICE_HUMAN_REVIEW or "").strip()
    return ""


def billing_status() -> dict:
    modes = []
    if stripe_configured():
        modes.append("stripe")
    if mock_billing_allowed():
        modes.append("mock")
    return {
        "stripe_configured": stripe_configured(),
        "stripe_webhook_configured": stripe_webhook_configured(),
        "mock_billing_allowed": mock_billing_allowed(),
        "publishable_key": config.STRIPE_PUBLISHABLE_KEY or None,
        "prices": PLAN_PRICES,
        "price_ids": {
            "ai_subscription": bool(config.STRIPE_PRICE_AI_MONTHLY),
            "human_review": bool(config.STRIPE_PRICE_HUMAN_REVIEW),
        },
        "modes": modes or ["unavailable"],
    }


async def _stripe(method: str, path: str, data: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            method,
            f"https://api.stripe.com/v1{path}",
            data=data,
            auth=(config.STRIPE_SECRET_KEY, ""),
        )
        if resp.status_code >= 400:
            logger.warning("Stripe %s %s -> %s %s", method, path, resp.status_code, resp.text[:300])
            resp.raise_for_status()
        return resp.json()


async def ensure_stripe_customer(user_id: int, email: str | None = None) -> str | None:
    if not stripe_configured():
        return None
    profile = await get_user_profile(user_id) or {}
    existing = profile.get("stripe_customer_id")
    if existing:
        return existing
    data = {
        "metadata[user_id]": str(user_id),
    }
    if email or profile.get("email"):
        data["email"] = email or profile.get("email")
    if profile.get("display_name") or profile.get("first_name"):
        data["name"] = profile.get("display_name") or profile.get("first_name")
    customer = await _stripe("POST", "/customers", data)
    await set_stripe_customer_id(user_id, customer["id"])
    return customer["id"]


async def create_checkout_session(user_id: int, product: str) -> dict:
    if product not in PLAN_PRICES:
        raise ValueError("unknown_product")

    if stripe_configured():
        if not price_id_for(product):
            raise ValueError("missing_stripe_price")
        try:
            return await _stripe_checkout(user_id, product)
        except Exception as exc:
            logger.warning("Stripe checkout failed", exc_info=True)
            raise ValueError(f"stripe_checkout_failed:{exc}") from exc

    if not mock_billing_allowed():
        raise ValueError("billing_unavailable")

    qs = urlencode({"user_id": user_id, "product": product})
    return {
        "mode": "mock",
        "checkout_url": f"{config.PUBLIC_BASE_URL}/api/billing/mock-complete?{qs}",
        "product": product,
        "amount_pln": PLAN_PRICES[product]["amount_pln"],
    }


async def _stripe_checkout(user_id: int, product: str) -> dict:
    price = price_id_for(product)
    customer = await ensure_stripe_customer(user_id)
    data = {
        "mode": "subscription" if product == "ai_subscription" else "payment",
        "success_url": f"{config.PUBLIC_BASE_URL}/?billing=success&product={product}",
        "cancel_url": f"{config.PUBLIC_BASE_URL}/?billing=cancel",
        "line_items[0][price]": price,
        "line_items[0][quantity]": "1",
        "metadata[user_id]": str(user_id),
        "metadata[product]": product,
        "client_reference_id": str(user_id),
        "allow_promotion_codes": "true",
        "billing_address_collection": "auto",
    }
    if customer:
        data["customer"] = customer
        data["customer_update[address]"] = "auto"
    if product == "ai_subscription":
        data["subscription_data[metadata][user_id]"] = str(user_id)
        data["subscription_data[metadata][product]"] = product
    payload = await _stripe("POST", "/checkout/sessions", data)
    return {
        "mode": "stripe",
        "checkout_url": payload["url"],
        "session_id": payload["id"],
        "product": product,
        "amount_pln": PLAN_PRICES[product]["amount_pln"],
        "customer_id": customer,
    }


async def create_billing_portal(user_id: int) -> dict:
    if not stripe_configured():
        return {
            "mode": "mock",
            "portal_url": f"{config.PUBLIC_BASE_URL}/#account",
            "message": "Stripe not configured — use mock cancel/manage on site.",
        }
    customer = await ensure_stripe_customer(user_id)
    if not customer:
        raise ValueError("no_customer")
    payload = await _stripe(
        "POST",
        "/billing_portal/sessions",
        {
            "customer": customer,
            "return_url": f"{config.PUBLIC_BASE_URL}/?billing=portal#account",
        },
    )
    return {"mode": "stripe", "portal_url": payload["url"]}


async def cancel_subscription(user_id: int, *, at_period_end: bool = True) -> dict:
    sub = await get_subscription(user_id)
    if stripe_configured() and sub and sub.get("stripe_subscription_id"):
        sid = sub["stripe_subscription_id"]
        if at_period_end:
            payload = await _stripe(
                "POST",
                f"/subscriptions/{sid}",
                {"cancel_at_period_end": "true"},
            )
        else:
            payload = await _stripe("DELETE", f"/subscriptions/{sid}")
        await update_subscription_record(
            user_id,
            plan=sub.get("plan") or "ai_subscription",
            status=payload.get("status") or "canceled",
            source="stripe",
            expires_at=sub.get("expires_at"),
            stripe_subscription_id=sid,
            cancel_at_period_end=bool(payload.get("cancel_at_period_end")),
        )
        return {"ok": True, "mode": "stripe", "status": payload.get("status")}

    await clear_subscription(user_id)
    return {"ok": True, "mode": "mock", "status": "canceled"}


async def list_invoices(user_id: int) -> list[dict]:
    local = await list_payments(user_id, limit=50)
    items = [
        {
            "id": p.get("external_id") or f"pay_{p['id']}",
            "product": p.get("product"),
            "amount_pln": p.get("amount_pln"),
            "status": p.get("status"),
            "provider": p.get("provider"),
            "created_at": p.get("created_at"),
            "source": "local",
        }
        for p in local
    ]
    if not stripe_configured():
        return items
    profile = await get_user_profile(user_id) or {}
    customer = profile.get("stripe_customer_id")
    if not customer:
        return items
    try:
        payload = await _stripe("GET", f"/invoices?customer={customer}&limit=20")
        for inv in payload.get("data") or []:
            items.append(
                {
                    "id": inv.get("id"),
                    "product": "invoice",
                    "amount_pln": int(round((inv.get("amount_paid") or 0) / 100)),
                    "status": inv.get("status"),
                    "provider": "stripe",
                    "created_at": datetime.fromtimestamp(
                        inv.get("created") or 0, tz=timezone.utc
                    ).isoformat(),
                    "hosted_invoice_url": inv.get("hosted_invoice_url"),
                    "source": "stripe",
                }
            )
    except Exception:
        logger.warning("Failed to list Stripe invoices", exc_info=True)
    return items


async def apply_successful_purchase(
    user_id: int,
    product: str,
    *,
    provider: str,
    external_id: str | None,
    subscription_id: str | None = None,
    days: int = 30,
) -> None:
    await upsert_user(user_id, None, None, None)
    if external_id:
        existing = await payment_by_external_id(external_id)
        if existing and existing.get("status") == "paid":
            return
    await record_payment(
        user_id,
        product,
        PLAN_PRICES[product]["amount_pln"],
        "paid",
        provider,
        external_id,
    )
    if product == "ai_subscription":
        expires = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
        await update_subscription_record(
            user_id,
            plan="ai_subscription",
            status="active",
            source=provider,
            expires_at=expires,
            stripe_subscription_id=subscription_id,
            cancel_at_period_end=False,
        )
        # keep legacy helper in sync
        await set_subscription(user_id, "ai_subscription", source=provider, days=days)
    elif product == "human_review":
        await mark_human_review_purchased(user_id)


def verify_stripe_signature(payload: bytes, sig_header: str | None) -> bool:
    if not stripe_webhook_configured():
        return False
    if not sig_header:
        return False
    parts = {}
    for item in sig_header.split(","):
        if "=" in item:
            k, v = item.split("=", 1)
            parts[k.strip()] = v.strip()
    timestamp = parts.get("t")
    signature = parts.get("v1")
    if not timestamp or not signature:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - ts) > 60 * 5:
        return False
    signed = f"{timestamp}.".encode("utf-8") + payload
    expected = hmac.new(
        config.STRIPE_WEBHOOK_SECRET.encode("utf-8"),
        signed,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def parse_checkout_completed(event: dict) -> dict | None:
    if event.get("type") != "checkout.session.completed":
        return None
    obj = (event.get("data") or {}).get("object") or {}
    meta = obj.get("metadata") or {}
    user_raw = meta.get("user_id") or obj.get("client_reference_id")
    product = meta.get("product")
    if not user_raw or product not in PLAN_PRICES:
        return None
    try:
        user_id = int(user_raw)
    except (TypeError, ValueError):
        return None
    return {
        "user_id": user_id,
        "product": product,
        "session_id": obj.get("id"),
        "subscription_id": obj.get("subscription"),
        "customer_id": obj.get("customer"),
        "payment_status": obj.get("payment_status"),
    }


async def handle_stripe_event(event: dict) -> dict:
    etype = event.get("type")
    obj = (event.get("data") or {}).get("object") or {}

    if etype == "checkout.session.completed":
        parsed = parse_checkout_completed(event)
        if not parsed:
            return {"handled": False}
        payment_status = (parsed.get("payment_status") or "").lower()
        if payment_status not in {"paid", "no_payment_required"}:
            return {
                "handled": False,
                "reason": "payment_not_completed",
                "payment_status": payment_status or None,
            }
        if parsed.get("customer_id"):
            await set_stripe_customer_id(parsed["user_id"], parsed["customer_id"])
        await apply_successful_purchase(
            parsed["user_id"],
            parsed["product"],
            provider="stripe",
            external_id=parsed.get("session_id"),
            subscription_id=parsed.get("subscription_id"),
        )
        return {"handled": True, "user_id": parsed["user_id"], "product": parsed["product"]}

    if etype in {"customer.subscription.updated", "customer.subscription.deleted"}:
        meta = obj.get("metadata") or {}
        user_raw = meta.get("user_id")
        if not user_raw:
            return {"handled": False, "reason": "no_user"}
        user_id = int(user_raw)
        status = obj.get("status") or "canceled"
        period_end = obj.get("current_period_end")
        expires = (
            datetime.fromtimestamp(period_end, tz=timezone.utc).isoformat()
            if period_end
            else None
        )
        if etype == "customer.subscription.deleted" or status in {
            "canceled",
            "unpaid",
            "incomplete_expired",
        }:
            await clear_subscription(user_id)
        else:
            await update_subscription_record(
                user_id,
                plan="ai_subscription",
                status=status,
                source="stripe",
                expires_at=expires,
                stripe_subscription_id=obj.get("id"),
                cancel_at_period_end=bool(obj.get("cancel_at_period_end")),
            )
        return {"handled": True, "user_id": user_id, "status": status}

    if etype == "invoice.paid":
        meta = (obj.get("subscription_details") or {}).get("metadata") or obj.get("metadata") or {}
        user_raw = meta.get("user_id")
        if user_raw:
            await apply_successful_purchase(
                int(user_raw),
                "ai_subscription",
                provider="stripe",
                external_id=obj.get("id"),
                subscription_id=obj.get("subscription"),
            )
            return {"handled": True, "user_id": int(user_raw)}
        return {"handled": False}

    return {"handled": False, "type": etype}
