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
    tokens = [t for t in q.replace(",", " ").split() if len(t) > 2]
    scored: list[tuple[int, dict]] = []
    for article in _load_articles():
        tags = " ".join(article.get("tags", [])).casefold()
        title = (article.get("title", {}) or {}).get(lang, "")
        body = (article.get("body", {}) or {}).get(lang, "")
        article_id = (article.get("id") or "").casefold()
        blob = f"{tags} {title} {body}".casefold()
        score = 0
        for token in tokens:
            if token == article_id or token in tags.split():
                score += 5
            elif token in title.casefold():
                score += 3
            elif token in blob:
                score += 1
        for tag in article.get("tags", []):
            if tag.casefold() in q:
                score += 3
        if article_id and article_id in q:
            score += 6
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
