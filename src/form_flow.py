"""Form wizard logic (shared by Telegram handlers)."""

from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from src.checklists import checklist
from src.config import OUTPUT_DIR
from src.database import record_completion
from src.drafts import clear_draft, save_draft
from src.documents import DocumentDef
from src.form_versions import version_line
from src.keyboards import (
    after_pdf_keyboard,
    confirm_keyboard,
    field_nav_keyboard,
    package_confirm_keyboard,
    podstawa_prawna_keyboard,
    reminder_keyboard,
)
from src.labels import doc_description, field_label
from src.packages import (
    PRZEPROWADZKA,
    fields_to_ask,
    package_field_sequence,
)
from src.pdf_preview import add_preview_watermark
from src.pdf_service import generate_document_pdf
from src.profile import load_profile_prefill, save_last_document, update_profile
from src.states import FormStates
from src.texts import mode_note, t
from src.tips import tip_after_pdf
from src.validators import is_required, validate_field

DOCUMENTS: dict[str, DocumentDef] = {}


def init(docs: dict[str, DocumentDef]) -> None:
    global DOCUMENTS
    DOCUMENTS = docs


def form_summary(doc: DocumentDef, answers: dict[str, str], lang: str) -> str:
    lines = [t("confirm_intro", lang)]
    for field in doc.fields:
        val = answers.get(field.key, "—")
        lines.append(f"<b>{field_label(field, lang)}</b>: {val}")
    return "\n".join(lines)


def package_summary(answers: dict[str, str], lang: str) -> str:
    from src.profile import profile_label

    lines = [t("confirm_intro", lang)]
    for key in (
        "imie",
        "nazwisko",
        "adres_zamieszkania",
        "podstawa_prawna",
        "wlasciciel_nieruchomosci",
    ):
        if answers.get(key):
            lines.append(f"<b>{profile_label(key, lang)}</b>: {answers[key]}")
    lines.append(f"\n<i>{t('package_summary_note', lang)}</i>")
    return "\n".join(lines)


async def persist_draft(user_id: int, state: FSMContext) -> None:
    current = await state.get_state()
    if not current:
        return
    data = await state.get_data()
    await save_draft(user_id, {"state": current, **data})


async def send_field_question(
    target: Message,
    doc: DocumentDef | None,
    field,
    idx: int,
    total: int,
    lang: str,
    doc_id: str = "",
) -> None:
    header = f"📄 <b>{doc.title(lang)}</b>\n\n" if doc else ""
    ver = version_line(doc.id, lang) if doc else ""
    ver_block = f"{ver}\n\n" if ver else ""
    did = doc_id or (doc.id if doc else "package")
    markup = field_nav_keyboard(
        did,
        field.key,
        lang,
        show_back=idx > 0,
        show_help=bool(field.hint(lang)),
        show_skip=not is_required(field.key),
    )
    progress = t("progress", lang).format(cur=idx + 1, total=total)
    await target.answer(
        f"{header}{ver_block}{progress}\n{field.question(lang)}\n\n"
        f"<i>{t('skip_hint', lang)}</i>",
        reply_markup=markup,
    )


async def ask_package_field(message: Message, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    seq = data["package_seq"]
    idx = data["package_field_index"]
    answers = data.get("package_answers", {})
    while idx < len(seq) and (answers.get(seq[idx].key) or "").strip():
        idx += 1
    if idx >= len(seq):
        await state.set_state(FormStates.package_confirming)
        await message.answer(
            package_summary(answers, lang),
            reply_markup=package_confirm_keyboard(lang),
        )
        await persist_draft(message.from_user.id, state)
        return

    await state.update_data(package_field_index=idx)
    field = seq[idx]
    total = data.get("remaining_total", len(seq))
    left = len([f for f in seq if not (answers.get(f.key) or "").strip()])
    qnum = total - left + 1
    if field.key == "podstawa_prawna":
        await message.answer(t("podstawa_pick", lang), reply_markup=podstawa_prawna_keyboard(lang))
        return
    await send_field_question(message, None, field, qnum - 1, total, lang, "package")
    await persist_draft(message.from_user.id, state)


async def start_single_doc(
    target: Message,
    state: FSMContext,
    doc_id: str,
    lang: str,
    user_id: int,
    prefill: dict[str, str] | None = None,
    use_profile: bool = True,
) -> None:
    doc = DOCUMENTS[doc_id]
    answers = dict(prefill or {})
    if use_profile:
        profile = await load_profile_prefill(user_id)
        if profile:
            answers = {**profile, **answers}
            await target.answer(t("profile_used", lang))
    desc = doc_description(doc, lang)
    if desc:
        await target.answer(f"ℹ️ {desc}")

    remaining = fields_to_ask(doc, answers)
    ver = version_line(doc_id, lang)
    if ver:
        await target.answer(ver)

    if not remaining:
        await state.set_state(FormStates.confirming)
        await state.update_data(doc_id=doc_id, answers=answers, field_index=len(doc.fields))
        await target.answer(form_summary(doc, answers, lang), reply_markup=confirm_keyboard(lang))
        return

    await state.set_state(FormStates.waiting_answer)
    await state.update_data(
        doc_id=doc_id,
        field_index=doc.fields.index(remaining[0]),
        answers=answers,
        package_mode=False,
        remaining_total=len(remaining),
        question_num=1,
    )
    field = remaining[0]
    if field.key == "podstawa_prawna":
        await target.answer(
            f"📄 <b>{doc.title(lang)}</b>\n\n{t('podstawa_pick', lang)}",
            reply_markup=podstawa_prawna_keyboard(lang),
        )
        return
    await send_field_question(target, doc, field, 0, len(remaining), lang, doc_id)
    await persist_draft(user_id, state)


async def start_package(target: Message, state: FSMContext, lang: str, user_id: int) -> None:
    pkg = PRZEPROWADZKA
    seq = package_field_sequence(DOCUMENTS)
    profile = await load_profile_prefill(user_id)
    answers = profile or {}
    remaining = [f for f in seq if not (answers.get(f.key) or "").strip()]
    start_idx = next(
        (i for i, f in enumerate(seq) if not (answers.get(f.key) or "").strip()),
        len(seq),
    )
    await state.clear()
    await state.set_state(FormStates.package_collecting)
    await state.update_data(
        package_answers=answers,
        package_field_index=start_idx,
        package_seq=seq,
        remaining_total=len(remaining) or len(seq),
    )
    if profile:
        await target.answer(t("profile_used", lang))
    await target.answer(f"<b>{pkg.title(lang)}</b>\n{pkg.intro(lang)}")
    await target.answer(checklist("przeprowadzka", lang))
    await ask_package_field(target, state, lang)


async def generate_one(
    user_id: int, doc_id: str, answers: dict[str, str], lang: str
) -> tuple[Path, str]:
    doc = DOCUMENTS[doc_id]
    path = OUTPUT_DIR / f"{doc_id}_{user_id}_{id(answers)}.pdf"
    try:
        return generate_document_pdf(doc, answers, path)
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc


async def send_preview(
    target: Message, doc_id: str, answers: dict[str, str], user_id: int, lang: str
) -> None:
    doc = DOCUMENTS[doc_id]
    preview_path = OUTPUT_DIR / f"preview_wm_{doc_id}_{user_id}.pdf"
    path, _ = await generate_one(user_id, doc_id, answers, lang)
    add_preview_watermark(path, preview_path)
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
    await target.answer_document(
        FSInputFile(preview_path),
        caption=f"👁 {t('preview_caption', lang)} — {doc.title(lang)}",
    )
    await target.answer(t("preview_sent", lang))


async def apply_answer(
    message: Message, state: FSMContext, key: str, value: str, lang: str
) -> None:
    err = validate_field(key, value, lang)
    if err:
        await message.answer(t("validation_error", lang).format(err=err))
        return

    current = await state.get_state()

    if current == FormStates.package_collecting.state:
        data = await state.get_data()
        answers = data.get("package_answers", {})
        answers[key] = value
        if data.get("editing_from_confirm"):
            await state.set_state(FormStates.package_confirming)
            await state.update_data(package_answers=answers, editing_from_confirm=False)
            await message.answer(
                package_summary(answers, lang),
                reply_markup=package_confirm_keyboard(lang),
            )
            return
        idx = data["package_field_index"] + 1
        await state.update_data(package_answers=answers, package_field_index=idx)
        await ask_package_field(message, state, lang)
        await persist_draft(message.from_user.id, state)
        return

    data = await state.get_data()
    doc_id = data["doc_id"]
    doc = DOCUMENTS[doc_id]
    answers = data.get("answers", {})
    answers[key] = value
    if data.get("editing_from_confirm"):
        await state.set_state(FormStates.confirming)
        await state.update_data(answers=answers, editing_from_confirm=False)
        await message.answer(form_summary(doc, answers, lang), reply_markup=confirm_keyboard(lang))
        await persist_draft(message.from_user.id, state)
        return

    remaining = fields_to_ask(doc, answers)
    if not remaining:
        await state.set_state(FormStates.confirming)
        await state.update_data(answers=answers)
        await message.answer(form_summary(doc, answers, lang), reply_markup=confirm_keyboard(lang))
        await persist_draft(message.from_user.id, state)
        return

    field = remaining[0]
    new_idx = doc.fields.index(field)
    total = data.get("remaining_total", len(remaining))
    qnum = total - len(remaining) + 1
    await state.update_data(answers=answers, field_index=new_idx, question_num=qnum)
    if field.key == "podstawa_prawna":
        await message.answer(t("podstawa_pick", lang), reply_markup=podstawa_prawna_keyboard(lang))
        await persist_draft(message.from_user.id, state)
        return
    await send_field_question(message, doc, field, qnum - 1, total, lang, doc_id)
    await persist_draft(message.from_user.id, state)


async def deliver_pdf(
    callback: CallbackQuery,
    state: FSMContext,
    doc_id: str,
    answers: dict[str, str],
    lang: str,
) -> None:
    doc = DOCUMENTS[doc_id]
    user_id = callback.from_user.id
    await callback.message.answer(t("generating", lang))
    try:
        path, pdf_mode = await generate_one(user_id, doc_id, answers, lang)
    except RuntimeError:
        await callback.message.answer(t("pdf_error", lang))
        await callback.answer()
        return
    await record_completion(user_id, doc_id)
    await update_profile(user_id, answers)
    await save_last_document(user_id, doc_id)
    await state.clear()
    await clear_draft(user_id)

    note = mode_note(pdf_mode, lang)
    await callback.message.answer_document(
        FSInputFile(path),
        caption=f"{doc.title(lang)}\n{note}",
    )
    cl = checklist(doc_id, lang)
    if cl:
        await callback.message.answer(cl)
    tip = tip_after_pdf(doc_id, lang)
    if tip:
        await callback.message.answer(tip)
    if doc_id in ("meldunek", "meldunek_staly"):
        zus_cl = checklist("zus", lang)
        if zus_cl:
            await callback.message.answer(zus_cl)
    await callback.message.answer(t("done", lang), reply_markup=after_pdf_keyboard(lang))
    if doc_id in ("meldunek", "meldunek_staly"):
        await callback.message.answer(
            t("remind_offer", lang),
            reply_markup=reminder_keyboard(lang),
        )
    await callback.answer()
