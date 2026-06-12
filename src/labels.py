"""Localized field labels for summaries and UI."""

from src.documents import DocumentDef, FieldDef
from src.profile import profile_label


def field_label(field: FieldDef, lang: str) -> str:
    if lang == "pl":
        return field.label_pl
    label = profile_label(field.key, lang)
    if label != field.key:
        return label
    return field.label_pl


def field_question_short(field: FieldDef, lang: str) -> str:
    q = field.question(lang)
    return q if len(q) <= 40 else field_label(field, lang)


def doc_description(doc: DocumentDef, lang: str) -> str:
    return doc.description(lang)
