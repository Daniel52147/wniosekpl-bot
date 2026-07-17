from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from src.ai_assistant import answer_question_smart
from src.checklists import checklist
from src.config import ADMIN_IDS, AI_FREE_DAILY_LIMIT, OUTPUT_DIR, PUBLIC_BASE_URL
from src.database import (
    add_calendar_event,
    add_reminder,
    ai_questions_today,
    delete_user_data,
    feedback_count,
    get_karta_progress,
    get_language,
    get_stats,
    join_waitlist,
    list_calendar_events,
    record_ai_question,
    record_completion,
    save_feedback,
    set_karta_progress,
    set_language,
    set_referral,
    upsert_user,
    user_exists,
    waitlist_count,
)
from src.entitlements import can_ask_ai, user_plan
from src.karta_wizard import default_progress, progress_view
from src.field_explainer import explain_field
from src.profile import (
    clear_profile,
    get_last_document,
    load_profile_prefill,
    profile_label,
    save_last_document,
    set_profile_field,
    update_profile,
)
from src.drafts import clear_draft, load_draft, save_draft
from src.labels import doc_description, field_label
from src.tips import tip_after_pdf
from src.form_flow import (
    apply_answer,
    ask_package_field,
    deliver_pdf,
    form_summary,
    generate_one,
    init as init_form_flow,
    package_summary,
    persist_draft,
    send_field_question,
    send_preview,
    start_package,
    start_single_doc,
)
from src.reminders import default_remind_at
from src.documents import DocumentDef, load_all_documents
from src.form_versions import version_line
from src.keyboards import (
    after_pdf_keyboard,
    ai_upgrade_keyboard,
    confirm_keyboard,
    documents_keyboard,
    edit_fields_keyboard,
    field_nav_keyboard,
    language_keyboard,
    main_reply_keyboard,
    meldunek_menu_keyboard,
    package_confirm_keyboard,
    podstawa_prawna_keyboard,
    draft_resume_keyboard,
    profile_keyboard,
    quick_keyboard,
    reminder_keyboard,
    review_keyboard,
)
from src.pdf_preview import add_preview_watermark
from src.packages import (
    PACKAGES,
    PRZEPROWADZKA,
    build_answers_for_doc,
    fields_to_ask,
    package_field_sequence,
)
from src.pdf_service import generate_document_pdf
from src.podstawa_prawna import preset_value
from src.states import FormStates
from src.texts import mode_note, t
from src.validators import is_required

router = Router()
DOCUMENTS = load_all_documents()
init_form_flow(DOCUMENTS)
PKG_TITLES = {
    p.title(lang) for p in PACKAGES.values() for lang in ("ru", "en", "ua", "pl")
}
PROFIL_BTNS = {t("profil_btn", lang) for lang in ("ru", "en", "ua", "pl")}
MENU_BTNS = {t("menu", lang) for lang in ("ru", "en", "ua", "pl")}
ANOTHER_BTNS = {t("another", lang) for lang in ("ru", "en", "ua", "pl")}


async def _register_user(message: Message, lang: str | None = None) -> str:
    user = message.from_user
    assert user
    await upsert_user(user.id, user.username, user.first_name, lang)
    if lang:
        return lang
    return await get_language(user.id)


async def _show_profile(message: Message, lang: str) -> None:
    profile = await load_profile_prefill(message.from_user.id)
    if not profile:
        await message.answer(t("profile_empty", lang))
        return
    lines = [t("profile_title", lang), ""]
    for key, val in profile.items():
        lines.append(f"• <b>{profile_label(key, lang)}</b>: {val}")
    await message.answer("\n".join(lines), reply_markup=profile_keyboard(profile, lang))


async def _open_main_menu(
    message: Message,
    state: FSMContext,
    pending_ref: str | None = None,
    pending_action: str | None = None,
) -> None:
    await state.clear()
    if pending_ref:
        await state.update_data(pending_ref=pending_ref)
    if pending_action:
        await state.update_data(pending_action=pending_action)

    user = message.from_user
    assert user

    if not await user_exists(user.id):
        await message.answer(t("choose_lang", "ru"), reply_markup=language_keyboard())
        return

    if pending_ref:
        await set_referral(user.id, pending_ref)

    lang = await _register_user(message)
    await message.answer(t("welcome", lang), reply_markup=main_reply_keyboard(lang))
    if pending_action == "review":
        await message.answer(t("review_offer", lang), reply_markup=review_keyboard(lang))
        return
    if pending_action == "ai":
        await state.set_state(FormStates.waiting_ai_question)
        used = await ai_questions_today(user.id)
        left = max(AI_FREE_DAILY_LIMIT - used, 0)
        await message.answer(
            f"{t('ai_prompt', lang)}\n\n{t('ai_usage_left', lang).format(left=left)}"
        )
        return
    await message.answer(t("choose_doc", lang), reply_markup=quick_keyboard(lang))
    draft = await load_draft(user.id)
    if draft:
        await message.answer(t("draft_offer", lang), reply_markup=draft_resume_keyboard(lang))
    else:
        await message.answer(t("all_docs", lang), reply_markup=documents_keyboard(DOCUMENTS, lang))


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject) -> None:
    pending_ref = None
    pending_action = None
    if command.args and command.args.startswith("ref_"):
        pending_ref = command.args[4:]
    elif command.args == "review":
        pending_action = "review"
    elif command.args == "ai":
        pending_action = "ai"
    await _open_main_menu(message, state, pending_ref, pending_action)


@router.callback_query(F.data.startswith("lang:"))
async def on_language(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.split(":")[1]
    data = await state.get_data()
    pending_ref = data.get("pending_ref")
    pending_action = data.get("pending_action")
    await state.clear()
    await set_language(callback.from_user.id, lang)
    await upsert_user(
        callback.from_user.id,
        callback.from_user.username,
        callback.from_user.first_name,
        lang,
    )
    if pending_ref:
        await set_referral(callback.from_user.id, pending_ref)
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(t("welcome", lang), reply_markup=main_reply_keyboard(lang))
    if pending_action == "review":
        await callback.message.answer(t("review_offer", lang), reply_markup=review_keyboard(lang))
        await callback.answer()
        return
    if pending_action == "ai":
        await state.set_state(FormStates.waiting_ai_question)
        used = await ai_questions_today(callback.from_user.id)
        left = max(AI_FREE_DAILY_LIMIT - used, 0)
        await callback.message.answer(
            f"{t('ai_prompt', lang)}\n\n{t('ai_usage_left', lang).format(left=left)}"
        )
        await callback.answer()
        return
    await callback.message.answer(t("choose_doc", lang), reply_markup=quick_keyboard(lang))
    await callback.message.answer(t("all_docs", lang), reply_markup=documents_keyboard(DOCUMENTS, lang))
    await callback.answer()


@router.message(Command("lang"))
async def cmd_lang(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(message.from_user.id)
    await message.answer(t("choose_lang", lang), reply_markup=language_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    lang = await _register_user(message)
    await message.answer(t("help", lang))


@router.message(Command("guide"))
async def cmd_guide(message: Message) -> None:
    lang = await _register_user(message)
    await message.answer(t("guide_text", lang))


@router.message(Command("ask"))
@router.message(Command("ai"))
async def cmd_ai_assistant(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(FormStates.waiting_ai_question)
    lang = await _register_user(message)
    used = await ai_questions_today(message.from_user.id)
    left = max(AI_FREE_DAILY_LIMIT - used, 0)
    await message.answer(
        f"{t('ai_prompt', lang)}\n\n{t('ai_usage_left', lang).format(left=left)}"
    )


@router.message(Command("review"))
async def cmd_review(message: Message) -> None:
    lang = await _register_user(message)
    await message.answer(t("review_offer", lang), reply_markup=review_keyboard(lang))


@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext) -> None:
    await state.set_state(FormStates.waiting_feedback)
    lang = await _register_user(message)
    await message.answer(t("feedback_prompt", lang))


@router.message(FormStates.waiting_feedback)
async def on_feedback(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    await save_feedback(message.from_user.id, message.text.strip())
    await state.clear()
    await message.answer(t("feedback_ok", lang))


@router.message(FormStates.waiting_ai_question)
async def on_ai_question(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    allowed, plan = await can_ask_ai(message.from_user.id)
    if not allowed:
        await state.clear()
        await message.answer(t("ai_limit_reached", lang), reply_markup=ai_upgrade_keyboard(lang))
        return

    answer = await answer_question_smart(message.text.strip(), lang)
    await record_ai_question(message.from_user.id, message.text.strip(), answer.topic)
    plan_after = await user_plan(message.from_user.id)
    left = plan_after.get("ai_left")
    left_txt = "∞" if plan_after.get("unlimited") else str(left)
    await message.answer(
        f"{answer.text}\n\n{t('ai_usage_left', lang).format(left=left_txt)}",
        reply_markup=ai_upgrade_keyboard(lang) if (left == 0 and not plan_after.get("unlimited")) else None,
    )
    await state.clear()


@router.message(Command("premium"))
async def cmd_premium(message: Message) -> None:
    lang = await _register_user(message)
    plan = await user_plan(message.from_user.id)
    await message.answer(
        f"Plan: <b>{plan['plan']}</b>\n"
        f"Web checkout: {PUBLIC_BASE_URL}\n"
        f"/review — human check 29 zł\n"
        f"AI unlimited — 19 zł/mies (site checkout)\n"
        f"/lawyers — marketplace\n"
        f"/countries — roadmap krajów",
    )


@router.message(Command("lawyers"))
async def cmd_lawyers(message: Message) -> None:
    await _register_user(message)
    from src.marketplace import list_lawyers

    lines = ["<b>Marketplace prawników</b>", f"Lead online: {PUBLIC_BASE_URL}/#lawyers", ""]
    for item in list_lawyers()[:6]:
        lines.append(
            f"• <b>{item['name']}</b> ({item['city']}) — od {item['price_from_pln']} zł\n"
            f"  {', '.join(item['specialties'])}"
        )
    await message.answer("\n".join(lines))


@router.message(Command("countries"))
async def cmd_countries(message: Message) -> None:
    await _register_user(message)
    from src.countries import list_countries

    lines = ["<b>Kraje WniosekPL</b>"]
    for item in list_countries():
        lines.append(f"• {item['name']} ({item['code']}) — {item['status']}")
    await message.answer("\n".join(lines))


@router.message(Command("karta"))
async def cmd_karta(message: Message) -> None:
    lang = await _register_user(message)
    steps = await get_karta_progress(message.from_user.id)
    if not steps:
        steps = default_progress()
        await set_karta_progress(message.from_user.id, steps)
    lines = ["<b>Karta pobytu checklist</b>"]
    for step in progress_view(steps, lang):
        mark = "✅" if step["done"] else "☐"
        lines.append(f"{mark} {step['title']}")
    cl = checklist("karta_pobytu", lang)
    if cl:
        lines.append("")
        lines.append(cl)
    await message.answer("\n".join(lines))


@router.message(Command("calendar"))
async def cmd_calendar(message: Message) -> None:
    lang = await _register_user(message)
    events = await list_calendar_events(message.from_user.id)
    if not events:
        from datetime import datetime, timedelta, timezone

        due = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()
        await add_calendar_event(
            message.from_user.id,
            "Przygotuj dokumenty do karty pobytu",
            due,
            "karta",
        )
        events = await list_calendar_events(message.from_user.id)
    lines = ["<b>Kalendarz</b>"]
    for ev in events[:15]:
        lines.append(f"• {ev['due_at']}: {ev['title']}")
    await message.answer("\n".join(lines))


@router.message(Command("profil"))
async def cmd_profil(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang = await _register_user(message)
    await _show_profile(message, lang)


@router.message(Command("ostatni"))
async def cmd_ostatni(message: Message, state: FSMContext) -> None:
    lang = await _register_user(message)
    doc_id = await get_last_document(message.from_user.id)
    if not doc_id:
        await message.answer(t("repeat_last_none", lang))
        return
    await state.clear()
    await start_single_doc(message, state, doc_id, lang, message.from_user.id)


@router.message(Command("privacy"))
async def cmd_privacy(message: Message) -> None:
    lang = await _register_user(message)
    await message.answer(t("privacy", lang))


@router.message(Command("usun"))
async def cmd_usun(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(message.from_user.id)
    await delete_user_data(message.from_user.id)
    await message.answer(t("usun_done", lang))


@router.message(Command("docs"))
@router.message(F.text.in_(PKG_TITLES | ANOTHER_BTNS))
async def cmd_docs(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang = await _register_user(message)
    if message.text in PKG_TITLES:
        await start_package(message, state, lang, message.from_user.id)
        return
    await message.answer(t("choose_doc", lang), reply_markup=quick_keyboard(lang))
    await message.answer(t("all_docs", lang), reply_markup=documents_keyboard(DOCUMENTS, lang))


@router.message(F.text.in_(MENU_BTNS))
async def cmd_menu(message: Message, state: FSMContext) -> None:
    await _open_main_menu(message, state)


@router.message(F.text.in_(PROFIL_BTNS))
async def cmd_profil_btn(message: Message, state: FSMContext) -> None:
    await cmd_profil(message, state)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await clear_draft(message.from_user.id)
    lang = await _register_user(message)
    await message.answer(t("cancelled", lang))


@router.callback_query(F.data == "meldunek:menu")
async def meldunek_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(
        t("meldunek_menu", lang),
        reply_markup=meldunek_menu_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "action:repeat_last")
async def action_repeat_last(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    doc_id = await get_last_document(callback.from_user.id)
    if not doc_id:
        await callback.message.answer(t("repeat_last_none", lang))
        await callback.answer()
        return
    await state.clear()
    await start_single_doc(
        callback.message, state, doc_id, lang, callback.from_user.id
    )
    await callback.answer()


@router.callback_query(F.data == "action:docs")
async def action_docs(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("choose_doc", lang), reply_markup=quick_keyboard(lang))
    await callback.message.answer(t("all_docs", lang), reply_markup=documents_keyboard(DOCUMENTS, lang))
    await callback.answer()


@router.callback_query(F.data == "action:menu")
async def action_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("welcome", lang), reply_markup=main_reply_keyboard(lang))
    await callback.message.answer(t("choose_doc", lang), reply_markup=quick_keyboard(lang))
    await callback.message.answer(t("all_docs", lang), reply_markup=documents_keyboard(DOCUMENTS, lang))
    await callback.answer()


@router.callback_query(F.data == "package:przeprowadzka")
async def on_package_start(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    await start_package(callback.message, state, lang, callback.from_user.id)
    await callback.answer()


@router.callback_query(F.data == "action:use_profile")
async def action_use_profile(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    profile = await load_profile_prefill(callback.from_user.id)
    if not profile:
        await callback.message.answer(t("profile_empty", lang))
    else:
        lines = [t("profile_used", lang), ""]
        for k, v in list(profile.items())[:12]:
            lines.append(f"• <b>{profile_label(k, lang)}</b>: {v}")
        await callback.message.answer("\n".join(lines))
    await callback.message.answer(
        t("choose_doc", lang),
        reply_markup=documents_keyboard(DOCUMENTS, lang),
    )
    await callback.answer()


@router.callback_query(F.data == "action:guide")
async def action_guide(callback: CallbackQuery) -> None:
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("guide_text", lang))
    await callback.answer()


@router.callback_query(F.data == "action:ask_ai")
async def action_ask_ai(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(FormStates.waiting_ai_question)
    lang = await get_language(callback.from_user.id)
    used = await ai_questions_today(callback.from_user.id)
    left = max(AI_FREE_DAILY_LIMIT - used, 0)
    await callback.message.answer(
        f"{t('ai_prompt', lang)}\n\n{t('ai_usage_left', lang).format(left=left)}"
    )
    await callback.answer()


@router.callback_query(F.data == "action:review")
async def action_review(callback: CallbackQuery) -> None:
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("review_offer", lang), reply_markup=review_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "action:resume_draft")
async def action_resume_draft(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    draft = await load_draft(callback.from_user.id)
    if not draft:
        await callback.answer()
        return
    st = draft.get("state")
    data = {k: v for k, v in draft.items() if k != "state"}
    if st == FormStates.confirming.state:
        await state.set_state(FormStates.confirming)
        await state.update_data(**data)
        doc = DOCUMENTS[data["doc_id"]]
        await callback.message.answer(
            form_summary(doc, data["answers"], lang),
            reply_markup=confirm_keyboard(lang),
        )
    elif st == FormStates.package_confirming.state:
        await state.set_state(FormStates.package_confirming)
        await state.update_data(**data)
        await callback.message.answer(
            package_summary(data["package_answers"], lang),
            reply_markup=package_confirm_keyboard(lang),
        )
    elif st == FormStates.waiting_answer.state:
        await state.set_state(FormStates.waiting_answer)
        await state.update_data(**data)
        doc = DOCUMENTS[data["doc_id"]]
        field = doc.fields[data["field_index"]]
        qnum = data.get("question_num", 1)
        total = data.get("remaining_total", 1)
        if field.key == "podstawa_prawna":
            await callback.message.answer(
                t("podstawa_pick", lang),
                reply_markup=podstawa_prawna_keyboard(lang),
            )
        else:
            await send_field_question(
                callback.message, doc, field, qnum - 1, total, lang, data["doc_id"]
            )
    elif st == FormStates.package_collecting.state:
        await state.set_state(FormStates.package_collecting)
        await state.update_data(**data)
        await ask_package_field(callback.message, state, lang)
    await callback.answer()


@router.callback_query(F.data == "action:discard_draft")
async def action_discard_draft(callback: CallbackQuery) -> None:
    await clear_draft(callback.from_user.id)
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("cancelled", lang))
    await callback.answer()


@router.callback_query(F.data == "action:zus")
async def action_zus(callback: CallbackQuery) -> None:
    lang = await get_language(callback.from_user.id)
    text = checklist("zus", lang)
    if text:
        await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "karta:checklist")
async def karta_checklist(callback: CallbackQuery) -> None:
    lang = await get_language(callback.from_user.id)
    text = checklist("karta_pobytu", lang)
    if text:
        await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data.startswith("waitlist:"))
async def on_waitlist(callback: CallbackQuery) -> None:
    product = callback.data.split(":")[1]
    lang = await get_language(callback.from_user.id)
    ok = await join_waitlist(callback.from_user.id, product)
    if product == "ai_subscription":
        await callback.message.answer(t("ai_subscription_ok" if ok else "ai_subscription_dup", lang))
        await callback.answer()
        return
    if product == "human_review":
        await callback.message.answer(t("review_waitlist_ok" if ok else "review_waitlist_dup", lang))
        await callback.answer()
        return
    await callback.message.answer(t("waitlist_ok" if ok else "waitlist_dup", lang))
    cl = checklist("karta_pobytu", lang)
    if cl:
        await callback.message.answer(cl)
    await callback.answer()


@router.callback_query(F.data == "profile:clear")
async def profile_clear(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(callback.from_user.id)
    await clear_profile(callback.from_user.id)
    await callback.message.answer(t("profile_cleared", lang))
    await callback.answer()


@router.callback_query(F.data.startswith("profile:edit:"))
async def profile_edit_start(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 2)[2]
    lang = await get_language(callback.from_user.id)
    await state.set_state(FormStates.profile_editing)
    await state.update_data(profile_key=key)
    await callback.message.answer(
        t("profile_edit_prompt", lang).format(label=profile_label(key, lang))
    )
    await callback.answer()


@router.message(FormStates.profile_editing)
async def profile_edit_save(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    data = await state.get_data()
    key = data.get("profile_key", "")
    if key:
        await set_profile_field(message.from_user.id, key, message.text.strip())
    await state.clear()
    await message.answer(t("profile_updated", lang))
    await _show_profile(message, lang)


@router.callback_query(F.data.startswith("remind:"))
async def on_remind(callback: CallbackQuery) -> None:
    lang = await get_language(callback.from_user.id)
    choice = callback.data.split(":")[1]
    if choice != "skip":
        days = int(choice)
        await add_reminder(callback.from_user.id, default_remind_at(days))
        await callback.message.answer(t("remind_set", lang))
    await callback.answer()


@router.callback_query(F.data == "nav:back")
async def on_nav_back(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    current = await state.get_state()

    if current == FormStates.package_collecting.state:
        data = await state.get_data()
        idx = data["package_field_index"]
        if idx <= 0:
            await callback.answer()
            return
        idx -= 1
        seq = data["package_seq"]
        answers = data.get("package_answers", {})
        answers.pop(seq[idx].key, None)
        await state.update_data(package_field_index=idx, package_answers=answers)
        await ask_package_field(callback.message, state, lang)
        await callback.answer()
        return

    if current == FormStates.waiting_answer.state:
        data = await state.get_data()
        doc_id = data["doc_id"]
        doc = DOCUMENTS[doc_id]
        idx = data["field_index"]
        if idx <= 0:
            await callback.answer()
            return
        idx -= 1
        answers = data.get("answers", {})
        answers.pop(doc.fields[idx].key, None)
        await state.update_data(field_index=idx, answers=answers)
        field = doc.fields[idx]
        if field.key == "podstawa_prawna":
            await callback.message.answer(
                t("podstawa_pick", lang),
                reply_markup=podstawa_prawna_keyboard(lang),
            )
        else:
            await send_field_question(
                callback.message, doc, field, idx, len(doc.fields), lang, doc_id
            )
        await callback.answer()


@router.callback_query(F.data == "nav:skip")
async def on_nav_skip(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    current = await state.get_state()

    if current == FormStates.package_collecting.state:
        data = await state.get_data()
        seq = data["package_seq"]
        idx = data["package_field_index"]
        field = seq[idx]
        if is_required(field.key):
            await callback.answer(t("skip_not_allowed", lang), show_alert=True)
            return
        await apply_answer(callback.message, state, field.key, "", lang)
        await callback.answer()
        return

    if current == FormStates.waiting_answer.state:
        data = await state.get_data()
        doc = DOCUMENTS[data["doc_id"]]
        field = doc.fields[data["field_index"]]
        if is_required(field.key):
            await callback.answer(t("skip_not_allowed", lang), show_alert=True)
            return
        await apply_answer(callback.message, state, field.key, "", lang)
        await callback.answer()
        return

    await callback.answer()


@router.callback_query(F.data.startswith("help:"))
async def on_field_help(callback: CallbackQuery) -> None:
    parts = callback.data.split(":", 2)
    doc_id = parts[1]
    field_key = parts[2]
    lang = await get_language(callback.from_user.id)
    hint = ""
    if doc_id == "package":
        for f in package_field_sequence(DOCUMENTS):
            if f.key == field_key:
                hint = f.hint(lang)
                break
    elif doc_id in DOCUMENTS:
        for f in DOCUMENTS[doc_id].fields:
            if f.key == field_key:
                hint = f.hint(lang)
                break
    text = hint or explain_field(field_key, lang) or t("field_help_missing", lang)
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data.startswith("doc:"))
async def on_document(callback: CallbackQuery, state: FSMContext) -> None:
    doc_id = callback.data.split(":")[1]
    if doc_id not in DOCUMENTS:
        await callback.answer("Unknown document", show_alert=True)
        return
    lang = await get_language(callback.from_user.id)
    await state.clear()
    await start_single_doc(
        callback.message, state, doc_id, lang, callback.from_user.id
    )
    await callback.answer()


@router.callback_query(F.data.startswith("podstawa:"))
async def on_podstawa(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    choice = callback.data.split(":")[1]
    current = await state.get_state()

    if choice == "custom":
        await state.set_state(FormStates.waiting_podstawa_custom)
        await callback.message.answer(t("podstawa_custom", lang) + " — wpisz teraz:")
        await callback.answer()
        return

    value = preset_value(choice)
    await apply_answer(callback.message, state, "podstawa_prawna", value, lang)
    await callback.answer()


@router.message(FormStates.waiting_podstawa_custom)
async def on_podstawa_custom(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    await apply_answer(message, state, "podstawa_prawna", message.text.strip(), lang)


@router.message(FormStates.package_collecting)
async def on_package_answer(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    data = await state.get_data()
    seq = data["package_seq"]
    idx = data["package_field_index"]
    field = seq[idx]
    if field.key == "podstawa_prawna":
        await message.answer(t("podstawa_pick", lang), reply_markup=podstawa_prawna_keyboard(lang))
        return
    await apply_answer(message, state, field.key, message.text.strip(), lang)


@router.message(FormStates.waiting_answer)
async def on_answer(message: Message, state: FSMContext) -> None:
    if not message.text:
        return
    lang = await get_language(message.from_user.id)
    data = await state.get_data()
    doc_id = data["doc_id"]
    doc = DOCUMENTS[doc_id]
    field = doc.fields[data["field_index"]]
    if field.key == "podstawa_prawna":
        await message.answer(t("podstawa_pick", lang), reply_markup=podstawa_prawna_keyboard(lang))
        return
    await apply_answer(message, state, field.key, message.text.strip(), lang)


@router.callback_query(FormStates.confirming, F.data == "confirm:edit_menu")
async def confirm_edit_menu(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    data = await state.get_data()
    doc = DOCUMENTS[data["doc_id"]]
    fields = [(f.key, field_label(f, lang)) for f in doc.fields]
    await callback.message.answer(
        t("edit_field_pick", lang),
        reply_markup=edit_fields_keyboard(fields, "confirm:edit", lang),
    )
    await callback.answer()


@router.callback_query(FormStates.confirming, F.data.startswith("confirm:edit:"))
async def confirm_edit_field(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    key = callback.data.split(":", 2)[2]
    data = await state.get_data()

    if key == "back":
        doc = DOCUMENTS[data["doc_id"]]
        await callback.message.answer(
            form_summary(doc, data["answers"], lang),
            reply_markup=confirm_keyboard(lang),
        )
        await callback.answer()
        return

    doc_id = data["doc_id"]
    doc = DOCUMENTS[doc_id]
    idx = next((i for i, f in enumerate(doc.fields) if f.key == key), 0)
    await state.set_state(FormStates.waiting_answer)
    await state.update_data(field_index=idx, editing_from_confirm=True)
    field = doc.fields[idx]
    if field.key == "podstawa_prawna":
        await callback.message.answer(
            t("podstawa_pick", lang),
            reply_markup=podstawa_prawna_keyboard(lang),
        )
    else:
        await send_field_question(
            callback.message, doc, field, idx, len(doc.fields), lang, doc_id
        )
    await callback.answer()


@router.callback_query(FormStates.package_confirming, F.data == "package:edit_menu")
async def package_edit_menu(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    data = await state.get_data()
    seq = data["package_seq"]
    fields = [(f.key, field_label(f, lang)) for f in seq]
    await callback.message.answer(
        t("edit_field_pick", lang),
        reply_markup=edit_fields_keyboard(fields, "package:edit", lang),
    )
    await callback.answer()


@router.callback_query(FormStates.package_confirming, F.data.startswith("package:edit:"))
async def package_edit_field(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    key = callback.data.split(":", 2)[2]
    data = await state.get_data()

    if key == "back":
        await callback.message.answer(
            package_summary(data["package_answers"], lang),
            reply_markup=package_confirm_keyboard(lang),
        )
        await callback.answer()
        return

    seq = data["package_seq"]
    idx = next((i for i, f in enumerate(seq) if f.key == key), 0)
    await state.set_state(FormStates.package_collecting)
    await state.update_data(package_field_index=idx, editing_from_confirm=True)
    field = seq[idx]
    if field.key == "podstawa_prawna":
        await callback.message.answer(
            t("podstawa_pick", lang),
            reply_markup=podstawa_prawna_keyboard(lang),
        )
    else:
        await send_field_question(
            callback.message, None, field, idx, len(seq), lang, "package"
        )
    await callback.answer()


@router.callback_query(FormStates.confirming, F.data == "confirm:checklist")
async def show_checklist(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    data = await state.get_data()
    doc_id = data.get("doc_id", "")
    text = checklist(doc_id, lang)
    if text:
        await callback.message.answer(text)
    await callback.answer()


@router.callback_query(FormStates.package_confirming, F.data == "package:checklist")
async def package_checklist_preview(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(checklist("przeprowadzka", lang))
    for doc_id in PRZEPROWADZKA.doc_order:
        cl = checklist(doc_id, lang)
        if cl:
            await callback.message.answer(cl)
    await callback.answer()


@router.callback_query(FormStates.package_confirming, F.data == "package:cancel")
async def package_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("cancelled", lang))
    await callback.answer()


@router.callback_query(FormStates.confirming, F.data == "confirm:preview")
async def confirm_preview(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    lang = await get_language(callback.from_user.id)
    await callback.message.answer(t("generating", lang))
    try:
        await send_preview(
            callback.message,
            data["doc_id"],
            data["answers"],
            callback.from_user.id,
            lang,
        )
    except RuntimeError:
        await callback.message.answer(t("pdf_error", lang))
    await callback.answer()


@router.callback_query(FormStates.package_confirming, F.data == "package:preview")
async def package_preview(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    shared = data["package_answers"]
    lang = await get_language(callback.from_user.id)
    doc_id = "umowa_najmu"
    answers = build_answers_for_doc(DOCUMENTS[doc_id], shared)
    await callback.message.answer(t("generating", lang))
    try:
        await send_preview(callback.message, doc_id, answers, callback.from_user.id, lang)
        await callback.message.answer(t("package_preview_note", lang))
    except RuntimeError:
        await callback.message.answer(t("pdf_error", lang))
    await callback.answer()


@router.callback_query(FormStates.confirming, F.data == "confirm:no")
async def confirm_no(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    doc_id = data.get("doc_id")
    if doc_id:
        lang = await get_language(callback.from_user.id)
        await start_single_doc(
            callback.message, state, doc_id, lang, callback.from_user.id, use_profile=False
        )
    await callback.answer()


@router.callback_query(FormStates.confirming, F.data == "confirm:yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    doc_id = data["doc_id"]
    answers = data["answers"]
    lang = await get_language(callback.from_user.id)
    await deliver_pdf(callback, state, doc_id, answers, lang)


@router.callback_query(FormStates.package_confirming, F.data == "package:generate")
async def package_generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    shared = data["package_answers"]
    lang = await get_language(callback.from_user.id)
    user_id = callback.from_user.id

    await callback.message.answer(t("generating_package", lang))

    for doc_id in PRZEPROWADZKA.doc_order:
        doc = DOCUMENTS[doc_id]
        answers = build_answers_for_doc(doc, shared)
        try:
            path, mode = await generate_one(user_id, doc_id, answers, lang)
        except RuntimeError:
            await callback.message.answer(t("pdf_error", lang))
            await callback.answer()
            return
        await record_completion(user_id, doc_id)
        note = mode_note(mode, lang)
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

    await update_profile(user_id, shared)
    await save_last_document(user_id, "umowa_najmu")
    await state.clear()
    await clear_draft(user_id)
    await callback.message.answer(
        t("package_done", lang) + "\n\n" + checklist("przeprowadzka", lang),
        reply_markup=after_pdf_keyboard(lang),
    )
    await callback.message.answer(t("remind_offer", lang), reply_markup=reminder_keyboard(lang))
    await callback.answer()


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if ADMIN_IDS and message.from_user.id not in ADMIN_IDS:
        return
    stats = await get_stats()
    fb = await feedback_count()
    lines = [
        f"Users: {stats['users']} (+{stats['users_1d']} / 24h, +{stats['users_7d']} / 7d)",
        f"PDFs: {stats['completions']}",
        f"AI questions: {stats['ai_questions']} (+{stats['ai_questions_7d']} / 7d)",
        f"Feedback: {fb}",
    ]
    for doc_id, count in stats["by_document"]:
        lines.append(f"  - {doc_id}: {count}")
    karta = await waitlist_count("karta_pobytu")
    lines.append(f"Waitlist karta pobytu: {karta}")
    human_review = await waitlist_count("human_review")
    lines.append(f"Paid review leads: {human_review}")
    ai_subscription = await waitlist_count("ai_subscription")
    lines.append(f"AI subscription leads: {ai_subscription}")
    if stats.get("by_referral"):
        lines.append("Referrals:")
        for ref, count in stats["by_referral"]:
            lines.append(f"  - {ref}: {count}")
    await message.answer("\n".join(lines))
