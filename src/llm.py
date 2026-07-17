"""Optional OpenAI-compatible LLM client with safe local fallback."""

from __future__ import annotations

import logging

import httpx

from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

logger = logging.getLogger(__name__)


def llm_configured() -> bool:
    return bool((OPENAI_API_KEY or "").strip())


async def complete_chat(
    system: str,
    user: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 900,
) -> str | None:
    if not llm_configured():
        return None
    payload = {
        "model": OPENAI_MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        logger.warning("LLM request failed", exc_info=True)
        return None
