from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from src.config import BOT_USERNAME
from src.documents import DocumentDef
from src.packages import PACKAGES
from src.podstawa_prawna import PODSTAWA_PRESETS
from src.texts import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            ],
            [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang:ua")],
            [InlineKeyboardButton(text="🇵🇱 Polski", callback_data="lang:pl")],
        ]
    )


DOC_ORDER = (
    "pesel",
    "meldunek",
    "meldunek_staly",
    "umowa_najmu",
    "pismo_do_urzedu",
    "upowaznienie",
    "oswiadczenie_dochodow",
    "karta_pobytu_przygotowanie",
)


def quick_keyboard(lang: str) -> InlineKeyboardMarkup:
    pkg = PACKAGES["przeprowadzka"]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("ai_ask_btn", lang), callback_data="action:ask_ai")],
            [
                InlineKeyboardButton(text=pkg.title(lang), callback_data="package:przeprowadzka"),
                InlineKeyboardButton(text=t("quick_pesel", lang), callback_data="doc:pesel"),
            ],
            [
                InlineKeyboardButton(text=t("quick_meldunek", lang), callback_data="meldunek:menu"),
                InlineKeyboardButton(text=t("quick_umowa", lang), callback_data="doc:umowa_najmu"),
            ],
            [
                InlineKeyboardButton(text=t("guide_btn", lang), callback_data="action:guide"),
                InlineKeyboardButton(text=t("repeat_last_btn", lang), callback_data="action:repeat_last"),
            ],
            [InlineKeyboardButton(text=t("review_btn", lang), callback_data="action:review")],
        ]
    )


def review_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("review_waitlist_btn", lang), callback_data="waitlist:human_review")],
            [InlineKeyboardButton(text=t("another", lang), callback_data="action:docs")],
        ]
    )


def ai_upgrade_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("ai_subscription_btn", lang), callback_data="waitlist:ai_subscription")],
            [InlineKeyboardButton(text=t("review_btn", lang), callback_data="action:review")],
            [InlineKeyboardButton(text=t("another", lang), callback_data="action:docs")],
        ]
    )


def draft_resume_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("draft_resume_btn", lang), callback_data="action:resume_draft")],
            [InlineKeyboardButton(text=t("draft_discard_btn", lang), callback_data="action:discard_draft")],
        ]
    )


def meldunek_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("meldunek_czasowy_btn", lang), callback_data="doc:meldunek")],
            [InlineKeyboardButton(text=t("meldunek_staly_btn", lang), callback_data="doc:meldunek_staly")],
            [InlineKeyboardButton(text=t("menu", lang), callback_data="action:docs")],
        ]
    )


def documents_keyboard(docs: dict[str, DocumentDef], lang: str) -> InlineKeyboardMarkup:
    pkg = PACKAGES["przeprowadzka"]
    buttons = [
        [InlineKeyboardButton(text=t("ai_ask_btn", lang), callback_data="action:ask_ai")],
        [InlineKeyboardButton(text=pkg.title(lang), callback_data="package:przeprowadzka")],
        [
            InlineKeyboardButton(text="🆔 PESEL", callback_data="doc:pesel"),
            InlineKeyboardButton(text="🏠 Meldunek", callback_data="meldunek:menu"),
        ],
    ]
    for doc_id in DOC_ORDER:
        doc = docs.get(doc_id)
        if not doc or doc_id in ("pesel", "meldunek", "meldunek_staly"):
            continue
        buttons.append(
            [InlineKeyboardButton(text=doc.title(lang), callback_data=f"doc:{doc.id}")]
        )
    buttons.append(
        [
            InlineKeyboardButton(text=t("karta_checklist_btn", lang), callback_data="karta:checklist"),
            InlineKeyboardButton(text=t("karta_waitlist_btn", lang), callback_data="waitlist:karta_pobytu"),
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(text=t("zus_checklist_btn", lang), callback_data="action:zus"),
            InlineKeyboardButton(text=t("guide_btn", lang), callback_data="action:guide"),
        ]
    )
    buttons.append([InlineKeyboardButton(text=t("review_btn", lang), callback_data="action:review")])
    buttons.append(
        [InlineKeyboardButton(text=t("profile_use_btn", lang), callback_data="action:use_profile")]
    )
    buttons.append(
        [InlineKeyboardButton(text=t("repeat_last_btn", lang), callback_data="action:repeat_last")]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def field_nav_keyboard(
    doc_id: str,
    field_key: str,
    lang: str,
    show_back: bool,
    show_help: bool,
    show_skip: bool = False,
) -> InlineKeyboardMarkup | None:
    rows = []
    nav_row = []
    if show_back:
        nav_row.append(InlineKeyboardButton(text=t("back_btn", lang), callback_data="nav:back"))
    if show_skip:
        nav_row.append(InlineKeyboardButton(text=t("skip_btn", lang), callback_data="nav:skip"))
    if nav_row:
        rows.append(nav_row)
    if show_help:
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("field_help_btn", lang),
                    callback_data=f"help:{doc_id}:{field_key}",
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows) if rows else None


def reminder_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("remind_25", lang), callback_data="remind:25"),
                InlineKeyboardButton(text=t("remind_90", lang), callback_data="remind:90"),
            ],
            [InlineKeyboardButton(text=t("remind_no", lang), callback_data="remind:skip")],
        ]
    )


def podstawa_prawna_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for key, preset in PODSTAWA_PRESETS.items():
        label = preset.get(f"label_{lang}", preset["label_ru"])
        rows.append(
            [InlineKeyboardButton(text=label, callback_data=f"podstawa:{key}")]
        )
    rows.append(
        [InlineKeyboardButton(text=t("podstawa_custom", lang), callback_data="podstawa:custom")]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def edit_fields_keyboard(
    fields: list[tuple[str, str]],
    prefix: str,
    lang: str,
) -> InlineKeyboardMarkup:
    rows = []
    for key, label in fields:
        short = label[:28] + "…" if len(label) > 28 else label
        rows.append(
            [InlineKeyboardButton(text=f"✏️ {short}", callback_data=f"{prefix}:{key}")]
        )
    rows.append([InlineKeyboardButton(text=t("back_to_confirm", lang), callback_data=f"{prefix}:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def profile_keyboard(data: dict[str, str], lang: str) -> InlineKeyboardMarkup:
    from src.profile import PROFILE_LABELS, profile_label

    rows = []
    for key in PROFILE_LABELS:
        if key in data and data[key]:
            label = profile_label(key, lang)
            rows.append(
                [InlineKeyboardButton(text=f"✏️ {label}", callback_data=f"profile:edit:{key}")]
            )
    rows.append([InlineKeyboardButton(text=t("profile_clear_btn", lang), callback_data="profile:clear")])
    rows.append([InlineKeyboardButton(text=t("menu", lang), callback_data="action:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_keyboard(lang: str, show_checklist: bool = True) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t("confirm_btn_preview", lang), callback_data="confirm:preview")],
        [InlineKeyboardButton(text=t("confirm_btn_ok", lang), callback_data="confirm:yes")],
        [InlineKeyboardButton(text=t("confirm_btn_fix_field", lang), callback_data="confirm:edit_menu")],
        [InlineKeyboardButton(text=t("confirm_btn_edit", lang), callback_data="confirm:no")],
    ]
    if show_checklist:
        rows.insert(
            1,
            [InlineKeyboardButton(text=t("confirm_btn_checklist", lang), callback_data="confirm:checklist")],
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def package_confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("confirm_btn_preview", lang), callback_data="package:preview")],
            [InlineKeyboardButton(text=t("package_generate", lang), callback_data="package:generate")],
            [InlineKeyboardButton(text=t("confirm_btn_checklist", lang), callback_data="package:checklist")],
            [InlineKeyboardButton(text=t("confirm_btn_fix_field", lang), callback_data="package:edit_menu")],
            [InlineKeyboardButton(text=t("confirm_btn_edit", lang), callback_data="package:cancel")],
        ]
    )


def after_pdf_keyboard(lang: str) -> InlineKeyboardMarkup:
    share_url = (
        f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME}"
        f"&text=WniosekPL%20%E2%80%94%20darmowy%20pomocnik%20formularzy%20%F0%9F%87%B5%F0%9F%87%B1"
    )
    rows = [
        [InlineKeyboardButton(text=t("review_btn", lang), callback_data="action:review")],
        [InlineKeyboardButton(text=t("share_btn", lang), url=share_url)],
        [InlineKeyboardButton(text=t("another", lang), callback_data="action:docs")],
        [InlineKeyboardButton(text=t("menu", lang), callback_data="action:menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def main_reply_keyboard(lang: str) -> ReplyKeyboardMarkup:
    pkg = PACKAGES["przeprowadzka"]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=pkg.title(lang))],
            [KeyboardButton(text=t("another", lang)), KeyboardButton(text=t("profil_btn", lang))],
            [KeyboardButton(text=t("menu", lang))],
        ],
        resize_keyboard=True,
    )
