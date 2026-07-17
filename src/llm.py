"""OpenAI-compatible LLM client with OmniRoute gateway + provider fallbacks.

Primary path: OmniRoute (http://localhost:20128/v1) — free multi-provider router.
Fallback: direct OpenAI / Groq / OpenRouter / custom endpoints from env.
If nothing is configured, callers keep using rule-based answers.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import httpx

from src.config import (
    GROQ_API_KEY,
    LLM_FALLBACK_MODELS,
    OMNIROUTE_API_KEY,
    OMNIROUTE_BASE_URL,
    OMNIROUTE_ENABLED,
    OMNIROUTE_MODEL,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENROUTER_API_KEY,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LlmEndpoint:
    name: str
    base_url: str
    api_key: str
    model: str


def _endpoints() -> list[LlmEndpoint]:
    items: list[LlmEndpoint] = []
    if OMNIROUTE_ENABLED and (OMNIROUTE_API_KEY or OPENAI_API_KEY):
        items.append(
            LlmEndpoint(
                name="omniroute",
                base_url=OMNIROUTE_BASE_URL.rstrip("/"),
                api_key=(OMNIROUTE_API_KEY or OPENAI_API_KEY).strip(),
                model=OMNIROUTE_MODEL or OPENAI_MODEL or "auto",
            )
        )
    if (OPENAI_API_KEY or "").strip() and "api.openai.com" in OPENAI_BASE_URL:
        items.append(
            LlmEndpoint(
                name="openai",
                base_url=OPENAI_BASE_URL.rstrip("/"),
                api_key=OPENAI_API_KEY.strip(),
                model=OPENAI_MODEL,
            )
        )
    elif (OPENAI_API_KEY or "").strip() and not OMNIROUTE_ENABLED:
        # Custom OpenAI-compatible base (already pointed at a gateway).
        items.append(
            LlmEndpoint(
                name="openai_compatible",
                base_url=OPENAI_BASE_URL.rstrip("/"),
                api_key=OPENAI_API_KEY.strip(),
                model=OPENAI_MODEL,
            )
        )
    if (GROQ_API_KEY or "").strip():
        items.append(
            LlmEndpoint(
                name="groq",
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_API_KEY.strip(),
                model=LLM_FALLBACK_MODELS.get("groq", "llama-3.3-70b-versatile"),
            )
        )
    if (OPENROUTER_API_KEY or "").strip():
        items.append(
            LlmEndpoint(
                name="openrouter",
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY.strip(),
                model=LLM_FALLBACK_MODELS.get(
                    "openrouter",
                    "openrouter/free",
                ),
            )
        )
    # Deduplicate by (base_url, model, key)
    seen: set[tuple[str, str, str]] = set()
    unique: list[LlmEndpoint] = []
    for ep in items:
        key = (ep.base_url, ep.model, ep.api_key)
        if key in seen:
            continue
        seen.add(key)
        unique.append(ep)
    return unique


def llm_configured() -> bool:
    return bool(_endpoints())


def llm_status() -> dict:
    endpoints = _endpoints()
    return {
        "configured": bool(endpoints),
        "omniroute_enabled": OMNIROUTE_ENABLED,
        "omniroute_base_url": OMNIROUTE_BASE_URL,
        "gateway": endpoints[0].name if endpoints else None,
        "fallback_chain": [ep.name for ep in endpoints],
        "model_primary": endpoints[0].model if endpoints else None,
    }


async def complete_chat(
    system: str,
    user: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 900,
) -> str | None:
    endpoints = _endpoints()
    if not endpoints:
        return None

    payload_base = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    last_error: Exception | None = None
    async with httpx.AsyncClient(timeout=60.0) as client:
        for ep in endpoints:
            payload = {**payload_base, "model": ep.model}
            headers = {
                "Authorization": f"Bearer {ep.api_key}",
                "Content-Type": "application/json",
            }
            if ep.name == "openrouter":
                headers["HTTP-Referer"] = "https://wniosekpl.local"
                headers["X-Title"] = "WniosekPL"
            try:
                resp = await client.post(
                    f"{ep.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                text = data["choices"][0]["message"]["content"].strip()
                if text:
                    logger.info("LLM ok via %s model=%s", ep.name, ep.model)
                    return text
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "LLM endpoint %s failed; trying next fallback",
                    ep.name,
                    exc_info=True,
                )
                continue
    if last_error:
        logger.warning("All LLM endpoints failed: %s", last_error)
    return None


async def omniroute_reachable() -> bool:
    if not OMNIROUTE_ENABLED:
        return False
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{OMNIROUTE_BASE_URL.rstrip('/')}/models")
            return resp.status_code < 500
    except Exception:
        return False
