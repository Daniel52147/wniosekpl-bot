from contextlib import asynccontextmanager
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.ai_assistant import answer_question
from src.checklists import checklist
from src.config import (
    AI_FREE_DAILY_LIMIT,
    BOT_TOKEN,
    BOT_USERNAME,
    OUTPUT_DIR,
    ROOT,
    WEB_CORS_ORIGINS,
)
from src.database import (
    ai_questions_today,
    init_db,
    join_waitlist,
    record_ai_question,
    upsert_user,
)
from src.documents import load_all_documents
from src.pdf_service import generate_document_pdf
from src.validators import validate_field

LANDING_DIR = ROOT / "landing"
PRODUCT_VERSION = "0.3.0"


def telegram_configured() -> bool:
    token = (BOT_TOKEN or "").strip()
    return bool(token) and "your_telegram_bot_token" not in token


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.documents = load_all_documents()
    yield


app = FastAPI(
    title="WniosekPL API",
    description="Web API and product surface for the WniosekPL AI assistant.",
    version=PRODUCT_VERSION,
    lifespan=lifespan,
)

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
    user_id: int = Field(..., description="Stable application user id")
    question: str = Field(..., min_length=1, max_length=2000)
    lang: Literal["ru", "en", "ua", "pl"] = "ru"


class AssistantResponse(BaseModel):
    topic: str
    answer: str
    free_questions_left: int
    limit: int


class LeadRequest(BaseModel):
    user_id: int = Field(..., description="Stable application user id")
    product: Literal["ai_subscription", "human_review", "karta_pobytu"]


class LeadResponse(BaseModel):
    product: str
    created: bool


class FieldSummary(BaseModel):
    key: str
    label: str
    question: str
    required: bool


class DocumentSummary(BaseModel):
    id: str
    title: str
    description: str
    fields_count: int
    mode: str


class DocumentDetail(DocumentSummary):
    fields: list[FieldSummary]
    checklist: str


class GenerateRequest(BaseModel):
    user_id: int = Field(..., description="Stable application user id")
    lang: Literal["ru", "en", "ua", "pl"] = "ru"
    answers: dict[str, str]


class MetaResponse(BaseModel):
    name: str
    version: str
    ai_free_daily_limit: int
    used_today: int
    free_questions_left: int
    channels: list[str]
    telegram_configured: bool
    telegram_username: str
    documents_count: int


def _docs() -> dict:
    return getattr(app.state, "documents", None) or load_all_documents()


def _mode_for(doc_id: str) -> str:
    from src.official_forms import has_official_template

    return "official" if has_official_template(doc_id) else "helper"


@app.get("/", include_in_schema=False)
async def landing_page():
    landing = LANDING_DIR / "index.html"
    if landing.exists():
        return FileResponse(landing)
    return {"name": "WniosekPL API", "version": PRODUCT_VERSION}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": PRODUCT_VERSION,
        "telegram_configured": telegram_configured(),
        "documents_count": len(_docs()),
    }


@app.get("/api/meta", response_model=MetaResponse)
async def product_meta(user_id: int | None = Query(default=None)):
    used = await ai_questions_today(user_id) if user_id else 0
    docs = _docs()
    return MetaResponse(
        name="WniosekPL",
        version=PRODUCT_VERSION,
        ai_free_daily_limit=AI_FREE_DAILY_LIMIT,
        used_today=used,
        free_questions_left=max(AI_FREE_DAILY_LIMIT - used, 0),
        channels=["web", "telegram"],
        telegram_configured=telegram_configured(),
        telegram_username=BOT_USERNAME,
        documents_count=len(docs),
    )


@app.get("/api/documents", response_model=list[DocumentSummary])
async def list_documents(lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    docs = _docs()
    return [
        DocumentSummary(
            id=doc.id,
            title=doc.title(lang),
            description=doc.description(lang),
            fields_count=len(doc.fields),
            mode=_mode_for(doc.id),
        )
        for doc in docs.values()
    ]


@app.get("/api/documents/{doc_id}", response_model=DocumentDetail)
async def get_document(doc_id: str, lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    docs = _docs()
    doc = docs.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document_not_found")
    from src.validators import is_required

    return DocumentDetail(
        id=doc.id,
        title=doc.title(lang),
        description=doc.description(lang),
        fields_count=len(doc.fields),
        mode=_mode_for(doc.id),
        fields=[
            FieldSummary(
                key=field.key,
                label=field.label_pl,
                question=field.question(lang),
                required=is_required(field.key),
            )
            for field in doc.fields
        ],
        checklist=checklist(doc_id, lang),
    )


@app.post("/api/documents/{doc_id}/generate")
async def generate_document(doc_id: str, payload: GenerateRequest):
    docs = _docs()
    doc = docs.get(doc_id)
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
    try:
        path, mode = generate_document_pdf(doc, answers, output)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"pdf_failed: {exc}") from exc

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=f"wniosekpl_{doc_id}.pdf",
        headers={"X-WniosekPL-Mode": mode},
    )


@app.get("/api/checklists/{doc_id}")
async def get_checklist(doc_id: str, lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    text = checklist(doc_id, lang)
    if not text:
        raise HTTPException(status_code=404, detail="checklist_not_found")
    return {"id": doc_id, "lang": lang, "text": text}


@app.post("/api/assistant/ask", response_model=AssistantResponse)
async def ask_assistant(payload: AssistantRequest):
    await upsert_user(payload.user_id, None, None, payload.lang)
    used = await ai_questions_today(payload.user_id)
    if used >= AI_FREE_DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "daily_limit_reached",
                "limit": AI_FREE_DAILY_LIMIT,
                "upgrade_product": "ai_subscription",
            },
        )

    result = answer_question(payload.question, payload.lang)
    await record_ai_question(payload.user_id, payload.question, result.topic)
    return AssistantResponse(
        topic=result.topic,
        answer=result.text,
        free_questions_left=max(AI_FREE_DAILY_LIMIT - used - 1, 0),
        limit=AI_FREE_DAILY_LIMIT,
    )


@app.post("/api/leads", response_model=LeadResponse)
async def create_lead(payload: LeadRequest):
    await upsert_user(payload.user_id, None, None, None)
    created = await join_waitlist(payload.user_id, payload.product)
    return LeadResponse(product=payload.product, created=created)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
