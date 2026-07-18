from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

import json

from fastapi import FastAPI, File, Header, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

from src.accounts import (
    login_or_register_oauth,
    login_with_password,
    public_user,
    register_with_password,
    request_password_reset,
    reset_password,
    verify_email_token,
)
from src.ai_assistant import answer_question_smart
from src.auth import hash_token, issue_session, logout_session, new_token, resolve_session
from src.checklists import checklist
import src.config as config
from src.config import (
    AI_FREE_DAILY_LIMIT,
    BOT_USERNAME,
    DEFAULT_COUNTRY,
    OUTPUT_DIR,
    PLAN_PRICES,
    ROOT,
    SESSION_DAYS,
    UPLOADS_DIR,
    WEB_CORS_ORIGINS,
    database_backend,
)
from src.countries import get_country, list_countries
from src.database import (
    add_calendar_event,
    admin_overview,
    complete_calendar_event,
    consume_magic_link,
    create_magic_link,
    delete_calendar_event,
    delete_user_data,
    export_user_bundle,
    get_karta_progress,
    get_mos_progress,
    get_subscription,
    init_db,
    join_waitlist,
    list_calendar_events,
    list_payments,
    list_uploads,
    recent_ai_questions,
    record_ai_question,
    record_completion,
    record_payment,
    revoke_all_sessions,
    save_lawyer_lead,
    save_upload,
    set_karta_progress,
    set_mos_progress,
    set_referral,
    set_user_email,
    set_user_profile_fields,
    upsert_user,
)
from src.documents import load_all_documents
from src.entitlements import can_ask_ai, user_plan
from src.karta_wizard import default_progress, progress_view
from src.letter_writer import write_official_letter
from src.llm import complete_chat, llm_configured, llm_status, omniroute_reachable
from src.marketplace import get_lawyer, list_lawyers
from src.notifications import email_configured, notify_user
from src.oauth import (
    facebook_authorize_url,
    facebook_configured,
    facebook_exchange,
    google_authorize_url,
    google_configured,
    google_exchange,
    make_state,
    parse_state,
)
from src.ocr import extract_text, ocr_engine_status
from src.payments import (
    apply_successful_purchase,
    billing_status,
    cancel_subscription,
    create_billing_portal,
    create_checkout_session,
    handle_stripe_event,
    list_invoices,
    mock_billing_allowed,
    stripe_configured,
    stripe_webhook_configured,
    verify_stripe_signature,
)
from src.pdf_service import generate_document_pdf
from src.rate_limit import assistant_limiter, billing_limiter, upload_limiter
from src.services_directory import search_services
from src.validators import is_required, validate_field

LANDING_DIR = ROOT / "landing"
PRODUCT_VERSION = "2.2.8"


def telegram_configured() -> bool:
    token = (config.BOT_TOKEN or "").strip()
    return bool(token) and "your_telegram_bot_token" not in token


def require_admin(x_admin_key: str | None) -> None:
    expected = (config.ADMIN_API_KEY or "").strip()
    if not expected:
        return
    if x_admin_key != expected:
        raise HTTPException(status_code=401, detail="admin_unauthorized")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), microphone=(), camera=()",
        )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.runtime_secrets import apply_runtime_secrets

    apply_runtime_secrets()
    await init_db()
    app.state.documents = load_all_documents()
    yield


app = FastAPI(
    title="WniosekPL Platform",
    description="AI assistant platform for foreigners in Poland: web + Telegram + billing.",
    version=PRODUCT_VERSION,
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=WEB_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if LANDING_DIR.exists():
    app.mount("/static", StaticFiles(directory=LANDING_DIR), name="static")


class AssistantRequest(BaseModel):
    user_id: int
    question: str = Field(..., min_length=1, max_length=2000)
    lang: Literal["ru", "en", "ua", "pl"] = "ru"


class LeadRequest(BaseModel):
    user_id: int
    product: Literal[
        "ai_subscription",
        "human_review",
        "karta_pobytu",
        "human_review_paid",
    ]


class GenerateRequest(BaseModel):
    user_id: int
    lang: Literal["ru", "en", "ua", "pl"] = "ru"
    answers: dict[str, str]


class CheckoutRequest(BaseModel):
    user_id: int
    product: Literal["ai_subscription", "human_review"]


class PromoRequest(BaseModel):
    user_id: int | None = None
    code: str = Field(..., min_length=3, max_length=64)


class LetterRequest(BaseModel):
    user_id: int
    lang: Literal["ru", "en", "ua", "pl"] = "ru"
    name: str
    city: str = "Warszawa"
    date: str = ""
    office: str
    case_no: str = "brak"
    topic: str
    content: str


class CalendarCreate(BaseModel):
    user_id: int
    title: str
    due_at: str
    kind: str = "custom"
    notes: str = ""


class KartaUpdate(BaseModel):
    user_id: int
    step_id: str
    done: bool = True


class MosStepUpdate(BaseModel):
    user_id: int | None = None
    step_id: str
    done: bool = True


class MosDeadlineRequest(BaseModel):
    user_id: int | None = None
    due_at: str = Field(..., min_length=8, max_length=32)
    days_before: int = 14


class SessionRequest(BaseModel):
    user_id: int | None = None
    label: str = "web"


class MagicLinkRequest(BaseModel):
    user_id: int
    email: str = Field(..., min_length=3, max_length=200)


class LawyerLeadRequest(BaseModel):
    user_id: int
    lawyer_id: str
    contact: str = ""
    message: str = ""


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=8, max_length=128)
    name: str = ""
    lang: Literal["ru", "en", "ua", "pl"] = "ru"


class LoginRequest(BaseModel):
    email: str
    password: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=128)


class BillingUserRequest(BaseModel):
    user_id: int


def _docs() -> dict:
    return getattr(app.state, "documents", None) or load_all_documents()


def _mode_for(doc_id: str) -> str:
    from src.official_forms import has_official_template

    return "official" if has_official_template(doc_id) else "helper"


async def _resolve_user(
    user_id: int | None,
    authorization: str | None = None,
) -> int:
    session_user = await resolve_session(authorization)
    if session_user:
        return session_user
    if user_id is not None:
        return user_id
    raise HTTPException(status_code=401, detail="auth_required")


@app.get("/", include_in_schema=False)
async def landing_page():
    landing = LANDING_DIR / "index.html"
    if landing.exists():
        return FileResponse(landing)
    return {"name": "WniosekPL", "version": PRODUCT_VERSION}


@app.get("/profile", include_in_schema=False)
@app.get("/app", include_in_schema=False)
async def profile_app_page():
    """Logged-in workspace: AI, MOS, documents, billing — separate from marketing landing."""
    page = LANDING_DIR / "app.html"
    if page.exists():
        return FileResponse(page)
    raise HTTPException(status_code=404, detail="profile_ui_missing")


@app.get("/admin", include_in_schema=False)
async def admin_page():
    page = LANDING_DIR / "admin.html"
    if page.exists():
        return FileResponse(page)
    raise HTTPException(status_code=404, detail="admin_ui_missing")


@app.get("/setup", include_in_schema=False)
async def setup_page():
    page = LANDING_DIR / "setup.html"
    if page.exists():
        return FileResponse(page)
    raise HTTPException(status_code=404, detail="setup_ui_missing")


@app.get("/api/setup/status")
async def setup_status_api():
    from src.runtime_secrets import setup_status

    return setup_status()


class SetupConfigure(BaseModel):
    keys: dict[str, str]


@app.post("/api/setup/configure")
async def setup_configure(
    payload: SetupConfigure,
    x_admin_key: str | None = Header(default=None),
):
    require_admin(x_admin_key)
    from src.runtime_secrets import save_runtime_secrets, setup_status

    saved = save_runtime_secrets(payload.keys or {})
    return {
        "ok": True,
        "saved_keys": sorted(saved.keys()),
        "status": setup_status(),
    }


@app.get("/health")
async def health():
    """Cheap liveness probe for deploy platforms."""
    return {
        "status": "ok",
        "version": PRODUCT_VERSION,
        "documents_count": len(_docs()),
    }


@app.get("/ready")
async def ready():
    """Detailed readiness / dependency status."""
    return {
        "status": "ok",
        "version": PRODUCT_VERSION,
        "telegram_configured": telegram_configured(),
        "llm_configured": llm_configured(),
        "llm": llm_status(),
        "omniroute_reachable": await omniroute_reachable(),
        "stripe_configured": stripe_configured(),
        "stripe_webhook_configured": stripe_webhook_configured(),
        "mock_billing_allowed": mock_billing_allowed(),
        "email_configured": email_configured(),
        "database_backend": database_backend(),
        "ocr": ocr_engine_status(),
        "default_country": DEFAULT_COUNTRY,
        "documents_count": len(_docs()),
        "public_base_url": config.PUBLIC_BASE_URL,
    }


@app.get("/api/meta")
async def product_meta(
    user_id: int | None = Query(default=None),
    authorization: str | None = Header(default=None),
):
    resolved = user_id
    session_user = await resolve_session(authorization)
    if session_user:
        resolved = session_user
    plan = await user_plan(resolved) if resolved else {
        "plan": "free",
        "unlimited": False,
        "ai_used_today": 0,
        "ai_limit": AI_FREE_DAILY_LIMIT,
        "ai_left": AI_FREE_DAILY_LIMIT,
    }
    return {
        "name": "WniosekPL",
        "version": PRODUCT_VERSION,
        "ai_free_daily_limit": AI_FREE_DAILY_LIMIT,
        "used_today": plan.get("ai_used_today", 0),
        "free_questions_left": plan.get("ai_left"),
        "plan": plan,
        "channels": ["web", "telegram"],
        "telegram_configured": telegram_configured(),
        "telegram_username": BOT_USERNAME,
        "llm_configured": llm_configured(),
        "llm": llm_status(),
        "omniroute_reachable": await omniroute_reachable(),
        "stripe_configured": stripe_configured(),
        "stripe_webhook_configured": stripe_webhook_configured(),
        "email_configured": email_configured(),
        "database_backend": database_backend(),
        "ocr": ocr_engine_status(),
        "default_country": DEFAULT_COUNTRY,
        "countries": list_countries(),
        "documents_count": len(_docs()),
        "prices": PLAN_PRICES,
        "public_base_url": config.PUBLIC_BASE_URL,
        "ai_gateway": "omniroute",
        "auth": {
            "password": True,
            "google": google_configured(),
            "facebook": facebook_configured(),
            "magic_link": True,
        },
        "billing": billing_status(),
    }


@app.post("/api/auth/register")
async def auth_register(payload: RegisterRequest):
    try:
        result = await register_with_password(
            payload.email,
            payload.password,
            name=payload.name,
            lang=payload.lang,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@app.post("/api/auth/login")
async def auth_login(payload: LoginRequest):
    try:
        return await login_with_password(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@app.post("/api/auth/password/forgot")
async def auth_password_forgot(payload: PasswordResetRequest):
    try:
        return await request_password_reset(payload.email)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/auth/password/reset")
async def auth_password_reset(payload: PasswordResetConfirm):
    try:
        return await reset_password(payload.token, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/auth/verify-email")
async def auth_verify_email(token: str):
    try:
        user_id = await verify_email_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    session = await issue_session(user_id, label="email_verified")
    return RedirectResponse(
        f"/profile?auth=verified&user_id={user_id}&token={session['token']}&tab=overview",
        status_code=302,
    )


@app.get("/api/auth/providers")
async def auth_providers():
    return {
        "password": True,
        "google": google_configured(),
        "facebook": facebook_configured(),
        "magic_link": True,
    }


@app.get("/api/auth/google/start")
async def auth_google_start():
    if not google_configured():
        raise HTTPException(status_code=503, detail="google_oauth_not_configured")
    state = make_state("google")
    return RedirectResponse(google_authorize_url(state), status_code=302)


@app.get("/api/auth/google/callback")
async def auth_google_callback(code: str | None = None, state: str | None = None):
    if not code or not state:
        raise HTTPException(status_code=400, detail="oauth_missing_params")
    try:
        parse_state(state)
        profile = await google_exchange(code)
        result = await login_or_register_oauth(profile)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="oauth_failed") from exc
    tok = result["session"]["token"]
    uid = result["user"]["user_id"]
    return RedirectResponse(
        f"/profile?auth=ok&provider=google&user_id={uid}&token={tok}&tab=overview",
        status_code=302,
    )


@app.get("/api/auth/facebook/start")
async def auth_facebook_start():
    if not facebook_configured():
        raise HTTPException(status_code=503, detail="facebook_oauth_not_configured")
    state = make_state("facebook")
    return RedirectResponse(facebook_authorize_url(state), status_code=302)


@app.get("/api/auth/facebook/callback")
async def auth_facebook_callback(code: str | None = None, state: str | None = None):
    if not code or not state:
        raise HTTPException(status_code=400, detail="oauth_missing_params")
    try:
        parse_state(state)
        profile = await facebook_exchange(code)
        result = await login_or_register_oauth(profile)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="oauth_failed") from exc
    tok = result["session"]["token"]
    uid = result["user"]["user_id"]
    return RedirectResponse(
        f"/profile?auth=ok&provider=facebook&user_id={uid}&token={tok}&tab=overview",
        status_code=302,
    )


@app.post("/api/auth/session")
async def auth_session(payload: SessionRequest):
    user_id = payload.user_id or (10_000_000 + int(uuid4().int % 900_000_000))
    await upsert_user(user_id, None, None, None)
    session = await issue_session(user_id, days=SESSION_DAYS, label=payload.label)
    return session


@app.post("/api/auth/magic-link")
async def auth_magic_link(payload: MagicLinkRequest):
    await upsert_user(payload.user_id, None, None, None)
    await set_user_email(payload.user_id, payload.email)
    await set_user_profile_fields(payload.user_id, email=payload.email)
    token = new_token()
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    await create_magic_link(hash_token(token), payload.user_id, payload.email, expires)
    link = f"{config.PUBLIC_BASE_URL}/api/auth/claim?token={token}"
    await notify_user(
        user_id=payload.user_id,
        email=payload.email,
        subject="WniosekPL login link",
        body=f"Open this link to sign in: {link}",
    )
    return {
        "ok": True,
        "email": payload.email,
        "expires_at": expires,
        "claim_url": link if not email_configured() else None,
        "emailed": email_configured(),
    }


@app.get("/api/auth/claim")
async def auth_claim(token: str):
    row = await consume_magic_link(hash_token(token))
    if not row:
        raise HTTPException(status_code=400, detail="invalid_or_expired_link")
    user_id = int(row["telegram_id"])
    await set_user_email(user_id, row.get("email") or "")
    session = await issue_session(user_id, days=SESSION_DAYS, label="magic")
    return RedirectResponse(
        f"/profile?auth=ok&user_id={user_id}&token={session['token']}&tab=overview",
        status_code=302,
    )


@app.get("/api/auth/me")
async def auth_me(authorization: str | None = Header(default=None)):
    user_id = await resolve_session(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid_session")
    return {
        "user": await public_user(user_id),
        "plan": await user_plan(user_id),
        "subscription": await get_subscription(user_id),
        "billing": billing_status(),
    }


@app.get("/api/documents")
async def list_documents(lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    docs = _docs()
    return [
        {
            "id": doc.id,
            "title": doc.title(lang),
            "description": doc.description(lang),
            "fields_count": len(doc.fields),
            "mode": _mode_for(doc.id),
        }
        for doc in docs.values()
    ]


@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: str, lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    doc = _docs().get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document_not_found")
    return {
        "id": doc.id,
        "title": doc.title(lang),
        "description": doc.description(lang),
        "fields_count": len(doc.fields),
        "mode": _mode_for(doc.id),
        "fields": [
            {
                "key": field.key,
                "label": field.label_pl,
                "question": field.question(lang),
                "required": is_required(field.key),
            }
            for field in doc.fields
        ],
        "checklist": checklist(doc_id, lang),
    }


@app.post("/api/documents/{doc_id}/generate")
async def generate_document(doc_id: str, payload: GenerateRequest):
    doc = _docs().get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document_not_found")
    await upsert_user(payload.user_id, None, None, payload.lang)
    errors: dict[str, str] = {}
    answers: dict[str, str] = {}
    for field in doc.fields:
        value = (payload.answers.get(field.key) or "").strip()
        err = validate_field(field.key, value, payload.lang)
        if err:
            errors[field.key] = err
        answers[field.key] = value
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})
    output = OUTPUT_DIR / f"web_{doc_id}_{payload.user_id}_{uuid4().hex[:8]}.pdf"
    path, mode = generate_document_pdf(doc, answers, output)
    await record_completion(payload.user_id, doc_id)
    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"wniosekpl_{doc_id}.pdf",
        headers={"X-WniosekPL-Mode": mode},
    )


@app.post("/api/assistant/ask")
async def ask_assistant(payload: AssistantRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not assistant_limiter.allow(f"{ip}:{payload.user_id}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    await upsert_user(payload.user_id, None, None, payload.lang)
    allowed, plan = await can_ask_ai(payload.user_id)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "daily_limit_reached",
                "limit": AI_FREE_DAILY_LIMIT,
                "upgrade_product": "ai_subscription",
                "plan": plan,
            },
        )
    result = await answer_question_smart(payload.question, payload.lang)
    await record_ai_question(payload.user_id, payload.question, result.topic)
    plan_after = await user_plan(payload.user_id)
    return {
        "topic": result.topic,
        "answer": result.text,
        "actions": list(result.actions),
        "free_questions_left": plan_after.get("ai_left"),
        "limit": plan_after.get("ai_limit") or AI_FREE_DAILY_LIMIT,
        "plan": plan_after,
        "llm_configured": llm_configured(),
    }


@app.post("/api/leads")
async def create_lead(payload: LeadRequest):
    await upsert_user(payload.user_id, None, None, None)
    created = await join_waitlist(payload.user_id, payload.product)
    return {"product": payload.product, "created": created}


@app.get("/api/billing/status")
async def billing_status_api():
    return billing_status()


@app.post("/api/billing/promo")
async def billing_promo(
    payload: PromoRequest,
    authorization: str | None = Header(default=None),
):
    from src.promos import redeem_promo

    user_id = await _resolve_user(payload.user_id, authorization)
    try:
        result = await redeem_promo(user_id, payload.code)
    except ValueError as exc:
        detail = str(exc)
        status = 409 if detail == "promo_already_used" else 400
        raise HTTPException(status_code=status, detail=detail) from exc
    return result


@app.post("/api/billing/checkout")
async def billing_checkout(
    payload: CheckoutRequest,
    request: Request,
    authorization: str | None = Header(default=None),
):
    ip = request.client.host if request.client else "unknown"
    user_id = await _resolve_user(payload.user_id, authorization)
    if not billing_limiter.allow(f"{ip}:{user_id}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    await upsert_user(user_id, None, None, None)
    try:
        session = await create_checkout_session(user_id, payload.product)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await record_payment(
        user_id,
        payload.product,
        PLAN_PRICES[payload.product]["amount_pln"],
        "checkout_created",
        session.get("mode", "mock"),
        session.get("session_id"),
    )
    return session


@app.get("/api/billing/mock-complete")
async def billing_mock_complete(user_id: int, product: str):
    if not mock_billing_allowed():
        raise HTTPException(status_code=403, detail="mock_billing_disabled")
    if product not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="unknown_product")
    await apply_successful_purchase(
        user_id,
        product,
        provider="mock",
        external_id=f"mock-{uuid4().hex[:10]}",
    )
    await notify_user(
        user_id=user_id,
        subject="WniosekPL payment (demo)",
        body=f"Product {product} activated for user {user_id}.",
    )
    return RedirectResponse(f"/profile?billing=success&product={product}&user_id={user_id}&tab=billing")


@app.post("/api/billing/portal")
async def billing_portal(
    payload: BillingUserRequest,
    authorization: str | None = Header(default=None),
):
    user_id = await _resolve_user(payload.user_id, authorization)
    try:
        return await create_billing_portal(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/billing/cancel")
async def billing_cancel(
    payload: BillingUserRequest,
    authorization: str | None = Header(default=None),
):
    user_id = await _resolve_user(payload.user_id, authorization)
    return await cancel_subscription(user_id, at_period_end=True)


@app.get("/api/billing/invoices/{user_id}")
async def billing_invoices(
    user_id: int,
    authorization: str | None = Header(default=None),
):
    resolved = await _resolve_user(user_id, authorization)
    return {"items": await list_invoices(resolved)}


@app.post("/api/billing/webhook")
async def billing_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
):
    payload = await request.body()
    if stripe_configured():
        if not stripe_webhook_configured() or not verify_stripe_signature(
            payload, stripe_signature
        ):
            raise HTTPException(status_code=400, detail="invalid_signature")
    elif stripe_webhook_configured() and not verify_stripe_signature(
        payload, stripe_signature
    ):
        raise HTTPException(status_code=400, detail="invalid_signature")

    try:
        event = json.loads(payload.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid_json") from exc

    result = await handle_stripe_event(event)
    if result.get("handled") and result.get("user_id"):
        await notify_user(
            user_id=int(result["user_id"]),
            subject="WniosekPL payment update",
            body=f"Billing event: {event.get('type')}",
        )
    return {"received": True, **result}


@app.get("/api/cabinet/{user_id}")
async def cabinet(
    user_id: int,
    authorization: str | None = Header(default=None),
):
    resolved = await _resolve_user(user_id, authorization)
    await upsert_user(resolved, None, None, None)
    plan = await user_plan(resolved)
    return {
        "user_id": resolved,
        "plan": plan,
        "payments": await list_payments(resolved),
        "calendar": await list_calendar_events(resolved),
        "uploads": await list_uploads(resolved),
        "ai_history": await recent_ai_questions(resolved),
        "karta": progress_view(await get_karta_progress(resolved)),
        "mos": await get_mos_progress(resolved),
    }


@app.get("/api/resume")
async def resume_snapshot(
    lang: Literal["ru", "en", "ua", "pl"] = "pl",
    user_id: int | None = Query(default=None),
    authorization: str | None = Header(default=None),
):
    """Compact 'what to finish' snapshot for the chat-side profile rail."""
    from src.mos_guide import guide_payload, next_action

    resolved = None
    mos_done: dict[str, bool] = {}
    calendar: list = []
    karta_left = 0
    plan = {}
    if authorization or user_id is not None:
        try:
            resolved = await _resolve_user(user_id, authorization)
            mos_done = await get_mos_progress(resolved)
            calendar = (await list_calendar_events(resolved))[:3]
            karta_steps = progress_view(await get_karta_progress(resolved), lang)
            karta_left = sum(1 for s in karta_steps if not s.get("done"))
            plan = await user_plan(resolved)
        except Exception:
            resolved = None

    nxt = next_action(mos_done, lang)
    copy = guide_payload(lang, done=mos_done)["copy"]
    session_user = await resolve_session(authorization)
    return {
        "user_id": resolved,
        "plan": plan,
        "mos_next": nxt,
        "mos_label": copy.get("next_title"),
        "calendar": calendar,
        "karta_left": karta_left,
        "logged_in": session_user is not None,
    }


@app.post("/api/calendar")
async def calendar_create(payload: CalendarCreate):
    await upsert_user(payload.user_id, None, None, None)
    event_id = await add_calendar_event(
        payload.user_id,
        payload.title,
        payload.due_at,
        payload.kind,
        payload.notes,
    )
    return {"id": event_id, "ok": True}


@app.post("/api/calendar/{event_id}/done")
async def calendar_done(event_id: int, user_id: int):
    ok = await complete_calendar_event(event_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="event_not_found")
    return {"ok": True}


@app.get("/api/mos/guide")
async def mos_guide_api(
    lang: Literal["ru", "en", "ua", "pl"] = "pl",
    user_id: int | None = Query(default=None),
    authorization: str | None = Header(default=None),
):
    from src.mos_guide import guide_payload

    done: dict[str, bool] = {}
    resolved = None
    if authorization or user_id:
        try:
            resolved = await _resolve_user(user_id, authorization)
            done = await get_mos_progress(resolved)
        except Exception:
            done = {}
    payload = guide_payload(lang, done=done)
    if resolved:
        payload["user_id"] = resolved
        payload["saved_progress"] = done
    return payload


@app.post("/api/mos/step")
async def mos_step_api(
    payload: MosStepUpdate,
    authorization: str | None = Header(default=None),
):
    from src.mos_guide import READY_STEPS, next_action

    user_id = await _resolve_user(payload.user_id, authorization)
    valid = {s["id"] for s in READY_STEPS}
    if payload.step_id not in valid:
        raise HTTPException(status_code=400, detail="unknown_step")
    steps = await get_mos_progress(user_id)
    steps[payload.step_id] = payload.done
    await set_mos_progress(user_id, steps)
    return {"ok": True, "steps": steps, "next_action": next_action(steps, "pl")}


@app.post("/api/mos/deadline")
async def mos_deadline_api(
    payload: MosDeadlineRequest,
    authorization: str | None = Header(default=None),
):
    user_id = await _resolve_user(payload.user_id, authorization)
    await upsert_user(user_id, None, None, None)
    due = payload.due_at.strip()[:32]
    event_id = await add_calendar_event(
        user_id,
        title="Koniec legalnego pobytu — złóż MOS",
        due_at=due,
        kind="mos_deadline",
        notes=f"Przypomnienie: złóż wniosek w MOS przed końcem legalnego pobytu ({due}).",
    )
    # Mark readiness step + add a prep reminder days_before if still in the future.
    steps = await get_mos_progress(user_id)
    steps["legal_stay"] = True
    await set_mos_progress(user_id, steps)
    reminder_id = None
    try:
        from datetime import date as date_cls, timedelta

        end = date_cls.fromisoformat(due[:10])
        remind = end - timedelta(days=max(1, min(payload.days_before, 60)))
        if remind >= date_cls.today():
            reminder_id = await add_calendar_event(
                user_id,
                title="Za 14 dni koniec pobytu — przygotuj MOS",
                due_at=remind.isoformat(),
                kind="mos_reminder",
                notes="Sprawdź checklistę MOS, załączniki i Profil Zaufany.",
            )
    except Exception:
        reminder_id = None
    return {
        "ok": True,
        "event_id": event_id,
        "reminder_id": reminder_id,
        "due_at": due,
        "steps": steps,
    }


@app.get("/api/karta/{user_id}")
async def karta_get(user_id: int, lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    steps = await get_karta_progress(user_id)
    if not steps:
        steps = default_progress()
        await set_karta_progress(user_id, steps)
    return {
        "user_id": user_id,
        "steps": progress_view(steps, lang),
        "checklist": checklist("karta_pobytu", lang),
    }


@app.post("/api/karta/step")
async def karta_step(payload: KartaUpdate):
    steps = await get_karta_progress(payload.user_id) or default_progress()
    if payload.step_id not in default_progress():
        raise HTTPException(status_code=400, detail="unknown_step")
    steps[payload.step_id] = payload.done
    await set_karta_progress(payload.user_id, steps)
    return {"steps": progress_view(steps)}


@app.post("/api/letters/generate")
async def letters_generate(payload: LetterRequest):
    await upsert_user(payload.user_id, None, None, payload.lang)
    data = payload.model_dump()
    if not data.get("date"):
        data["date"] = datetime.now().strftime("%d.%m.%Y")
    result = await write_official_letter(data, payload.lang)
    return result


@app.post("/api/uploads/analyze")
async def uploads_analyze(
    request: Request,
    user_id: int = Query(...),
    lang: Literal["ru", "en", "ua", "pl"] = Query("ru"),
    file: UploadFile = File(...),
):
    ip = request.client.host if request.client else "unknown"
    if not upload_limiter.allow(f"{ip}:{user_id}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    await upsert_user(user_id, None, None, lang)
    plan = await user_plan(user_id)
    suffix = Path(file.filename or "upload.bin").suffix.lower() or ".bin"
    dest = UPLOADS_DIR / f"{user_id}_{uuid4().hex[:10]}{suffix}"
    content = await file.read()
    dest.write_bytes(content)
    text = extract_text(dest)
    system = (
        "Explain this Polish office document in simple language for a foreigner. "
        "Say if it looks like refusal or a request for more documents. "
        "Extract deadlines if present. Not legal advice. Answer in user language."
    )
    user = f"Language: {lang}\nExtracted text:\n{text[:8000] or '[no text extracted]'}"
    explanation = await complete_chat(system, user)
    if not explanation:
        explanation = (
            "Не удалось полностью распознать документ. "
            "Если это PDF с текстом — попробуйте ещё раз. "
            "Если фото — установите Tesseract или опишите ключевые фразы в AI-чате."
            if lang == "ru"
            else "Could not fully parse the document. Install Tesseract for image OCR "
            "or paste key phrases into the AI chat."
        )
        if not plan.get("unlimited"):
            explanation += (
                "\n\nTip: AI subscription unlocks richer document analysis when OPENAI_API_KEY is configured."
            )
    upload_id = await save_upload(
        user_id,
        file.filename or dest.name,
        str(dest),
        text,
        explanation,
    )
    return {
        "id": upload_id,
        "filename": file.filename,
        "extracted_text_preview": text[:1200],
        "explanation": explanation,
        "llm_configured": llm_configured(),
        "ocr": ocr_engine_status(),
    }


@app.get("/api/services")
async def services(
    city: str | None = None,
    category: str | None = None,
    q: str | None = None,
):
    return search_services(city=city, category=category, query=q)


@app.get("/api/lawyers")
async def lawyers(
    city: str | None = None,
    specialty: str | None = None,
    language: str | None = None,
):
    return list_lawyers(city=city, specialty=specialty, language=language)


@app.post("/api/lawyers/leads")
async def lawyers_lead(payload: LawyerLeadRequest):
    if not get_lawyer(payload.lawyer_id):
        raise HTTPException(status_code=404, detail="lawyer_not_found")
    await upsert_user(payload.user_id, None, None, None)
    lead_id = await save_lawyer_lead(
        payload.user_id,
        payload.lawyer_id,
        payload.contact,
        payload.message,
    )
    await notify_user(
        user_id=payload.user_id,
        subject="WniosekPL lawyer lead",
        body=f"Lead #{lead_id} for {payload.lawyer_id}: {payload.message[:200]}",
    )
    return {"id": lead_id, "ok": True}


@app.get("/api/countries")
async def countries(status: str | None = None):
    return {
        "default": DEFAULT_COUNTRY,
        "items": list_countries(status=status),
    }


@app.get("/api/countries/{code}")
async def country_detail(code: str):
    item = get_country(code)
    if not item:
        raise HTTPException(status_code=404, detail="country_not_found")
    return item


@app.get("/api/admin/overview")
async def admin(x_admin_key: str | None = Header(default=None)):
    require_admin(x_admin_key)
    data = await admin_overview()
    data["version"] = PRODUCT_VERSION
    data["database_backend"] = database_backend()
    data["features"] = {
        "llm": llm_configured(),
        "stripe": stripe_configured(),
        "stripe_webhook": stripe_webhook_configured(),
        "email": email_configured(),
        "ocr": ocr_engine_status(),
        "telegram": telegram_configured(),
    }
    return data


@app.get("/api/demo/seed-calendar/{user_id}")
async def seed_calendar(user_id: int):
    """Create sample reminders for demos."""
    await upsert_user(user_id, None, None, None)
    now = datetime.now(timezone.utc)
    samples = [
        ("Sprawdź ubezpieczenie", 7, "insurance"),
        ("Termin karty pobytu — przygotuj dokumenty", 30, "karta"),
        ("Wizyta w urzędzie / kolejka", 0, "urzad"),
    ]
    ids = []
    for title, days, kind in samples:
        due = (now + timedelta(days=days)).date().isoformat()
        ids.append(await add_calendar_event(user_id, title, due, kind))
    return {"created": ids}



@app.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    path = LANDING_DIR / "robots.txt"
    if path.exists():
        return FileResponse(path, media_type="text/plain")
    return RedirectResponse("/")


@app.get("/manifest.webmanifest", include_in_schema=False)
async def web_manifest():
    path = LANDING_DIR / "manifest.webmanifest"
    if path.exists():
        return FileResponse(path, media_type="application/manifest+json")
    raise HTTPException(status_code=404, detail="manifest_missing")


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml():
    path = LANDING_DIR / "sitemap.xml"
    if path.exists():
        return FileResponse(path, media_type="application/xml")
    raise HTTPException(status_code=404, detail="sitemap_missing")


@app.post("/api/auth/logout")
async def auth_logout(authorization: str | None = Header(default=None)):
    ok = await logout_session(authorization)
    return {"ok": ok}


@app.get("/api/account/export")
async def account_export(authorization: str | None = Header(default=None)):
    user_id = await resolve_session(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid_session")
    return await export_user_bundle(user_id)


@app.delete("/api/account")
async def account_delete(authorization: str | None = Header(default=None)):
    user_id = await resolve_session(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid_session")
    await revoke_all_sessions(user_id)
    await delete_user_data(user_id)
    return {"ok": True, "deleted_user_id": user_id}


class ReferralRequest(BaseModel):
    user_id: int
    code: str = Field(..., min_length=2, max_length=64)


@app.post("/api/account/referral")
async def account_referral(
    payload: ReferralRequest,
    authorization: str | None = Header(default=None),
):
    user_id = await _resolve_user(payload.user_id, authorization)
    await set_referral(user_id, payload.code)
    return {"ok": True}


@app.get("/api/calendar/{user_id}")
async def calendar_list(user_id: int, authorization: str | None = Header(default=None)):
    resolved = await _resolve_user(user_id, authorization)
    return {"items": await list_calendar_events(resolved)}


@app.delete("/api/calendar/{event_id}")
async def calendar_delete(event_id: int, user_id: int, authorization: str | None = Header(default=None)):
    resolved = await _resolve_user(user_id, authorization)
    ok = await delete_calendar_event(event_id, resolved)
    if not ok:
        raise HTTPException(status_code=404, detail="event_not_found")
    return {"ok": True}


@app.get("/api/packages")
async def packages_list(lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    from src.packages import PACKAGES

    return [
        {
            "id": pkg.id,
            "title": pkg.title(lang),
            "intro": pkg.intro(lang),
            "documents": pkg.doc_order,
        }
        for pkg in PACKAGES.values()
    ]


class PackageGenerateRequest(BaseModel):
    user_id: int
    lang: Literal["ru", "en", "ua", "pl"] = "ru"
    answers: dict[str, str]


@app.post("/api/packages/{package_id}/generate")
async def packages_generate(package_id: str, payload: PackageGenerateRequest):
    from src.packages import PACKAGES, build_answers_for_doc
    from zipfile import ZipFile
    import io

    pkg = PACKAGES.get(package_id)
    if not pkg:
        raise HTTPException(status_code=404, detail="package_not_found")
    docs = _docs()
    await upsert_user(payload.user_id, None, None, payload.lang)
    buf = io.BytesIO()
    with ZipFile(buf, "w") as zf:
        for doc_id in pkg.doc_order:
            doc = docs.get(doc_id)
            if not doc:
                continue
            answers = build_answers_for_doc(doc, payload.answers)
            errors = {}
            for field in doc.fields:
                value = (answers.get(field.key) or "").strip()
                err = validate_field(field.key, value, payload.lang)
                if err and is_required(field.key):
                    errors[field.key] = err
                answers[field.key] = value
            if errors:
                raise HTTPException(
                    status_code=400,
                    detail={"document_id": doc_id, "errors": errors},
                )
            out = OUTPUT_DIR / f"pkg_{package_id}_{doc_id}_{payload.user_id}_{uuid4().hex[:6]}.pdf"
            path, _mode = generate_document_pdf(doc, answers, out)
            await record_completion(payload.user_id, doc_id)
            zf.write(path, arcname=f"{doc_id}.pdf")
    buf.seek(0)
    from fastapi.responses import StreamingResponse

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="wniosekpl_{package_id}.zip"'},
    )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
