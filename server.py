from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.ai_assistant import answer_question
from src.config import AI_FREE_DAILY_LIMIT, ROOT, WEB_CORS_ORIGINS
from src.database import (
    ai_questions_today,
    init_db,
    join_waitlist,
    record_ai_question,
    upsert_user,
)
from src.documents import load_all_documents

LANDING_DIR = ROOT / "landing"
PRODUCT_VERSION = "0.2.0"


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


class DocumentSummary(BaseModel):
    id: str
    title: str
    description: str
    fields_count: int


class MetaResponse(BaseModel):
    name: str
    version: str
    ai_free_daily_limit: int
    used_today: int
    free_questions_left: int
    channels: list[str]


@app.get("/", include_in_schema=False)
async def landing_page():
    landing = LANDING_DIR / "index.html"
    if landing.exists():
        return FileResponse(landing)
    return {"name": "WniosekPL API", "version": PRODUCT_VERSION}


@app.get("/health")
async def health():
    return {"status": "ok", "version": PRODUCT_VERSION}


@app.get("/api/meta", response_model=MetaResponse)
async def product_meta(user_id: int | None = Query(default=None)):
    used = await ai_questions_today(user_id) if user_id else 0
    return MetaResponse(
        name="WniosekPL",
        version=PRODUCT_VERSION,
        ai_free_daily_limit=AI_FREE_DAILY_LIMIT,
        used_today=used,
        free_questions_left=max(AI_FREE_DAILY_LIMIT - used, 0),
        channels=["web", "telegram"],
    )


@app.get("/api/documents", response_model=list[DocumentSummary])
async def list_documents(lang: Literal["ru", "en", "ua", "pl"] = "ru"):
    docs = getattr(app.state, "documents", None) or load_all_documents()
    return [
        DocumentSummary(
            id=doc.id,
            title=doc.title(lang),
            description=doc.description(lang),
            fields_count=len(doc.fields),
        )
        for doc in docs.values()
    ]


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
