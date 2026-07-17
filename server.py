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

from src.ai_assistant import answer_question_smart
from src.auth import hash_token, issue_session, new_token, resolve_session
from src.checklists import checklist
from src.config import (
    ADMIN_API_KEY,
    AI_FREE_DAILY_LIMIT,
    BOT_TOKEN,
    BOT_USERNAME,
    DEFAULT_COUNTRY,
    OUTPUT_DIR,
    PLAN_PRICES,
    PUBLIC_BASE_URL,
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
    get_karta_progress,
    init_db,
    join_waitlist,
    list_calendar_events,
    list_payments,
    list_uploads,
    payment_by_external_id,
    recent_ai_questions,
    record_ai_question,
    record_completion,
    record_payment,
    save_lawyer_lead,
    save_upload,
    set_karta_progress,
    set_subscription,
    set_user_email,
    upsert_user,
)
from src.documents import load_all_documents
from src.entitlements import can_ask_ai, mark_human_review_purchased, user_plan
from src.karta_wizard import default_progress, progress_view
from src.letter_writer import write_official_letter
from src.llm import complete_chat, llm_configured
from src.marketplace import get_lawyer, list_lawyers
from src.notifications import email_configured, notify_user
from src.ocr import extract_text, ocr_engine_status
from src.payments import (
    create_checkout_session,
    parse_checkout_completed,
    stripe_configured,
    stripe_webhook_configured,
    verify_stripe_signature,
)
from src.pdf_service import generate_document_pdf
from src.rate_limit import assistant_limiter, billing_limiter, upload_limiter
from src.services_directory import search_services
from src.validators import is_required, validate_field

LANDING_DIR = ROOT / "landing"
PRODUCT_VERSION = "2.0.0"


def telegram_configured() -> bool:
    token = (BOT_TOKEN or "").strip()
    return bool(token) and "your_telegram_bot_token" not in token


def require_admin(x_admin_key: str | None) -> None:
    if not ADMIN_API_KEY:
        return
    if x_admin_key != ADMIN_API_KEY:
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


@app.get("/admin", include_in_schema=False)
async def admin_page():
    page = LANDING_DIR / "admin.html"
    if page.exists():
        return FileResponse(page)
    raise HTTPException(status_code=404, detail="admin_ui_missing")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": PRODUCT_VERSION,
        "telegram_configured": telegram_configured(),
        "llm_configured": llm_configured(),
        "stripe_configured": stripe_configured(),
        "stripe_webhook_configured": stripe_webhook_configured(),
        "email_configured": email_configured(),
        "database_backend": database_backend(),
        "ocr": ocr_engine_status(),
        "default_country": DEFAULT_COUNTRY,
        "documents_count": len(_docs()),
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
        "stripe_configured": stripe_configured(),
        "stripe_webhook_configured": stripe_webhook_configured(),
        "email_configured": email_configured(),
        "database_backend": database_backend(),
        "ocr": ocr_engine_status(),
        "default_country": DEFAULT_COUNTRY,
        "countries": list_countries(),
        "documents_count": len(_docs()),
        "prices": PLAN_PRICES,
        "public_base_url": PUBLIC_BASE_URL,
    }


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
    token = new_token()
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    await create_magic_link(hash_token(token), payload.user_id, payload.email, expires)
    link = f"{PUBLIC_BASE_URL}/api/auth/claim?token={token}"
    await notify_user(
        user_id=payload.user_id,
        email=payload.email,
        subject="WniosekPL login link",
        body=f"Open this link to sign in: {link}",
    )
    # In demo/dev return the link so the flow is testable without SMTP.
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
        f"/?auth=ok&user_id={user_id}&token={session['token']}",
        status_code=302,
    )


@app.get("/api/auth/me")
async def auth_me(authorization: str | None = Header(default=None)):
    user_id = await resolve_session(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="invalid_session")
    return {"user_id": user_id, "plan": await user_plan(user_id)}


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


@app.post("/api/billing/checkout")
async def billing_checkout(payload: CheckoutRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not billing_limiter.allow(f"{ip}:{payload.user_id}"):
        raise HTTPException(status_code=429, detail="rate_limited")
    await upsert_user(payload.user_id, None, None, None)
    session = await create_checkout_session(payload.user_id, payload.product)
    await record_payment(
        payload.user_id,
        payload.product,
        PLAN_PRICES[payload.product]["amount_pln"],
        "checkout_created",
        session.get("mode", "mock"),
        session.get("session_id"),
    )
    return session


@app.get("/api/billing/mock-complete")
async def billing_mock_complete(user_id: int, product: str):
    if product not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="unknown_product")
    await upsert_user(user_id, None, None, None)
    await record_payment(
        user_id,
        product,
        PLAN_PRICES[product]["amount_pln"],
        "paid",
        "mock",
        f"mock-{uuid4().hex[:10]}",
    )
    if product == "ai_subscription":
        await set_subscription(user_id, "ai_subscription", source="mock", days=30)
    elif product == "human_review":
        await mark_human_review_purchased(user_id)
    await notify_user(
        user_id=user_id,
        subject="WniosekPL payment (demo)",
        body=f"Product {product} activated for user {user_id}.",
    )
    return RedirectResponse(f"/?billing=success&product={product}&user_id={user_id}")


@app.post("/api/billing/webhook")
async def billing_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
):
    payload = await request.body()
    if stripe_webhook_configured():
        if not verify_stripe_signature(payload, stripe_signature):
            raise HTTPException(status_code=400, detail="invalid_signature")

    try:
        event = json.loads(payload.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid_json") from exc

    parsed = parse_checkout_completed(event)
    if not parsed:
        return {"received": True, "handled": False}

    external_id = parsed.get("session_id") or ""
    if external_id:
        existing = await payment_by_external_id(external_id)
        if existing and existing.get("status") == "paid":
            return {"received": True, "handled": True, "duplicate": True}

    user_id = parsed["user_id"]
    product = parsed["product"]
    await upsert_user(user_id, None, None, None)
    await record_payment(
        user_id,
        product,
        PLAN_PRICES[product]["amount_pln"],
        "paid",
        "stripe",
        external_id or None,
    )
    if product == "ai_subscription":
        await set_subscription(user_id, "ai_subscription", source="stripe", days=30)
    elif product == "human_review":
        await mark_human_review_purchased(user_id)
    await notify_user(
        user_id=user_id,
        subject="WniosekPL payment confirmed",
        body=f"Stripe checkout completed for {product}.",
    )
    return {"received": True, "handled": True, "user_id": user_id, "product": product}


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
