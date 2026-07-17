from functools import lru_cache
from pathlib import Path

import yaml

from src.config import KNOWLEDGE_DIR


@lru_cache(maxsize=1)
def _load_articles() -> list[dict]:
    articles: list[dict] = []
    for path in sorted(Path(KNOWLEDGE_DIR).glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
        articles.extend(raw.get("articles", []))
    return articles


def search_knowledge(query: str, lang: str = "ru", limit: int = 3) -> list[dict]:
    q = (query or "").casefold()
    scored: list[tuple[int, dict]] = []
    for article in _load_articles():
        tags = " ".join(article.get("tags", [])).casefold()
        title = (article.get("title", {}) or {}).get(lang, "")
        body = (article.get("body", {}) or {}).get(lang, "")
        blob = f"{tags} {title} {body}".casefold()
        score = sum(1 for token in q.split() if token and token in blob)
        for tag in article.get("tags", []):
            if tag.casefold() in q:
                score += 2
        if score:
            scored.append((score, article))
    scored.sort(key=lambda item: item[0], reverse=True)
    result = []
    for _, article in scored[:limit]:
        result.append(
            {
                "id": article.get("id"),
                "title": (article.get("title", {}) or {}).get(lang, ""),
                "body": (article.get("body", {}) or {}).get(lang, ""),
                "tags": article.get("tags", []),
            }
        )
    return result


def knowledge_context(query: str, lang: str = "ru") -> str:
    hits = search_knowledge(query, lang=lang, limit=3)
    if not hits:
        return ""
    parts = []
    for hit in hits:
        parts.append(f"### {hit['title']}\n{hit['body'].strip()}")
    return "\n\n".join(parts)
