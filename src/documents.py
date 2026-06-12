from dataclasses import dataclass
from pathlib import Path

import yaml

from src.config import DOCUMENTS_DIR


@dataclass
class FieldDef:
    key: str
    label_pl: str
    question_ru: str
    question_en: str
    question_ua: str
    hint_ru: str = ""
    hint_en: str = ""
    hint_ua: str = ""
    hint_pl: str = ""

    question_pl: str = ""

    def question(self, lang: str) -> str:
        pl_q = self.question_pl or f"Podaj: {self.label_pl}"
        return {
            "ru": self.question_ru,
            "en": self.question_en,
            "ua": self.question_ua,
            "pl": pl_q,
        }.get(lang, self.question_ru)

    def hint(self, lang: str) -> str:
        return {
            "ru": self.hint_ru,
            "en": self.hint_en,
            "ua": self.hint_ua,
            "pl": self.hint_pl or self.hint_ru,
        }.get(lang, self.hint_ru)


@dataclass
class DocumentDef:
    id: str
    title_pl: str
    title_ru: str
    title_en: str
    title_ua: str
    description_ru: str
    description_en: str
    fields: list[FieldDef]
    description_pl: str = ""
    description_ua: str = ""

    def title(self, lang: str) -> str:
        return {
            "ru": self.title_ru,
            "en": self.title_en,
            "ua": self.title_ua,
            "pl": self.title_pl,
        }.get(lang, self.title_ru)

    def description(self, lang: str) -> str:
        return {
            "ru": self.description_ru,
            "en": self.description_en,
            "ua": self.description_ua or self.description_ru,
            "pl": self.description_pl or self.description_ru,
        }.get(lang, self.description_ru)


def load_all_documents() -> dict[str, DocumentDef]:
    docs: dict[str, DocumentDef] = {}
    for path in sorted(DOCUMENTS_DIR.glob("*.yaml")):
        with path.open(encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        fields = [
            FieldDef(
                key=item["key"],
                label_pl=item["label_pl"],
                question_ru=item["question_ru"],
                question_en=item["question_en"],
                question_ua=item.get("question_ua", item["question_ru"]),
                question_pl=item.get("question_pl", ""),
                hint_ru=item.get("hint_ru", ""),
                hint_en=item.get("hint_en", ""),
                hint_ua=item.get("hint_ua", ""),
                hint_pl=item.get("hint_pl", ""),
            )
            for item in raw["fields"]
        ]
        doc = DocumentDef(
            id=raw["id"],
            title_pl=raw["title_pl"],
            title_ru=raw["title_ru"],
            title_en=raw["title_en"],
            title_ua=raw.get("title_ua", raw["title_ru"]),
            description_ru=raw["description_ru"],
            description_en=raw["description_en"],
            fields=fields,
            description_pl=raw.get("description_pl", ""),
            description_ua=raw.get("description_ua", ""),
        )
        docs[doc.id] = doc
    return docs
