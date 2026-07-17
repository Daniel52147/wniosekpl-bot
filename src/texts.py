BRAND = "WniosekPL"

TEXTS = {
    "welcome": {
        "ru": (
            f"👋 <b>{BRAND}</b> — pomocnik, <b>nie urząd</b>.\n\n"
            "Бесплатно: официальные PDF (PESEL gov.pl, Meldunek EL/ZC/1) "
            "или <b>📦 Пакет «Переезд»</b> — 3 документа за один раз.\n\n"
            "⚠️ Не юридическая консультация. Проверьте dane i podpis właściciela.\n\n"
            "💯 <b>100% бесплатно</b> — без оплаты, без подписки."
        ),
        "en": (
            f"👋 <b>{BRAND}</b> — helper, <b>not a government office</b>.\n\n"
            "Free official PDFs or <b>📦 Relocation package</b> (3 docs at once).\n\n"
            "💯 <b>100% free</b> — no payment, no subscription."
        ),
        "ua": (
            f"👋 <b>{BRAND}</b> — помічник, <b>не urząd</b>.\n\n"
            "Безкоштовно: офіційні PDF (PESEL, Meldunek) або "
            "<b>📦 Пакет «Переїзд»</b> — 3 документи за раз.\n\n"
            "💯 <b>100% безкоштовно</b> — без оплати, без підписки."
        ),
        "pl": (
            f"👋 <b>{BRAND}</b> — pomocnik, <b>nie urząd</b>.\n\n"
            "Bezpłatnie: PESEL, Meldunek, pakiet Przeprowadzka.\n\n"
            "💯 <b>100% za darmo</b> — bez płatności."
        ),
    },
    "all_docs": {
        "ru": "📋 Все документы:",
        "en": "📋 All documents:",
        "ua": "📋 Усі документи:",
        "pl": "📋 Wszystkie formularze:",
    },
    "choose_lang": {
        "ru": "🌐 Выберите язык / Choose language:",
        "en": "🌐 Choose your language:",
        "ua": "🌐 Оберіть мову:",
        "pl": "🌐 Wybierz język:",
    },
    "choose_doc": {
        "ru": "📄 Документ или пакет:",
        "en": "📄 Document or package:",
        "ua": "📄 Документ або пакет:",
        "pl": "📄 Formularz lub pakiet:",
    },
    "ai_ask_btn": {
        "ru": "🤖 Спросить AI-помощника",
        "en": "🤖 Ask AI assistant",
        "ua": "🤖 Запитати AI-помічника",
        "pl": "🤖 Zapytaj asystenta AI",
    },
    "ai_subscription_btn": {
        "ru": "🚀 Хочу безлимит за 19 zł/мес",
        "en": "🚀 I want unlimited for 19 zł/mo",
        "ua": "🚀 Хочу безліміт за 19 zł/міс",
        "pl": "🚀 Chcę bez limitu za 19 zł/mies.",
    },
    "ai_prompt": {
        "ru": (
            "🤖 Напишите вопрос о жизни и документах в Польше.\n\n"
            "Пример: «Я гражданин Украины, работаю официально, хочу карту побыту».\n"
            "Бесплатно: 5 вопросов в день. /cancel — отмена."
        ),
        "en": (
            "🤖 Send a question about life and paperwork in Poland.\n\n"
            "Example: “I am Ukrainian, legally employed, and need a residence card”.\n"
            "Free: 5 questions per day. /cancel to abort."
        ),
        "ua": (
            "🤖 Напишіть питання про життя і документи в Польщі.\n\n"
            "Приклад: «Я громадянин України, працюю офіційно, хочу карту побиту».\n"
            "Безкоштовно: 5 питань на день. /cancel — скасувати."
        ),
        "pl": (
            "🤖 Napisz pytanie o życie i dokumenty w Polsce.\n\n"
            "Przykład: „Jestem z Ukrainy, pracuję legalnie i chcę kartę pobytu”.\n"
            "Za darmo: 5 pytań dziennie. /cancel — anuluj."
        ),
    },
    "ai_usage_left": {
        "ru": "Осталось бесплатных вопросов сегодня: {left}.",
        "en": "Free questions left today: {left}.",
        "ua": "Залишилось безкоштовних питань сьогодні: {left}.",
        "pl": "Darmowe pytania na dziś: {left}.",
    },
    "ai_limit_reached": {
        "ru": (
            "Лимит бесплатных AI-вопросов на сегодня закончился.\n\n"
            "Идея подписки: <b>19 zł/мес</b> — больше вопросов, анализ PDF/фото и генерация писем. "
            "Нажмите кнопку, если хотите такой тариф."
        ),
        "en": (
            "You reached today's free AI question limit.\n\n"
            "Subscription idea: <b>19 zł/mo</b> for more questions, PDF/photo analysis, and letter generation. "
            "Tap if you want this plan."
        ),
        "ua": (
            "Ліміт безкоштовних AI-питань на сьогодні закінчився.\n\n"
            "Ідея підписки: <b>19 zł/міс</b> — більше питань, аналіз PDF/фото і генерація листів."
        ),
        "pl": (
            "Dzisiejszy limit darmowych pytań AI został wykorzystany.\n\n"
            "Pomysł subskrypcji: <b>19 zł/mies.</b> — więcej pytań, analiza PDF/zdjęć i generowanie pism. "
            "Kliknij, jeśli chcesz taki plan."
        ),
    },
    "ai_subscription_ok": {
        "ru": "✅ Интерес к подписке сохранён. Это поможет понять спрос и запустить тариф быстрее.",
        "en": "✅ Subscription interest saved. This helps validate demand and launch the plan faster.",
        "ua": "✅ Інтерес до підписки збережено.",
        "pl": "✅ Zainteresowanie subskrypcją zapisane. To pomoże szybciej uruchomić plan.",
    },
    "ai_subscription_dup": {
        "ru": "Вы уже отметили интерес к подписке.",
        "en": "You already marked interest in the subscription.",
        "ua": "Ви вже відмітили інтерес до підписки.",
        "pl": "Już zaznaczyłeś zainteresowanie subskrypcją.",
    },
    "cancelled": {
        "ru": "Отменено. /start — снова.",
        "en": "Cancelled. /start to restart.",
        "ua": "Скасовано. /start",
        "pl": "Anulowano. /start",
    },
    "confirm_intro": {
        "ru": "Проверьте данные перед PDF:\n\n",
        "en": "Review before PDF:\n\n",
        "ua": "Перевірте дані:\n\n",
        "pl": "Sprawdź dane przed PDF:\n\n",
    },
    "confirm_btn_ok": {
        "ru": "✅ Всё верно — скачать PDF",
        "en": "✅ Download PDF",
        "ua": "✅ Завантажити PDF",
        "pl": "✅ Pobierz PDF",
    },
    "confirm_btn_edit": {
        "ru": "🔄 Заполнить заново",
        "en": "🔄 Fill again from scratch",
        "ua": "🔄 Заповнити заново",
        "pl": "🔄 Wypełnij od nowa",
    },
    "confirm_btn_fix_field": {
        "ru": "✏️ Исправить одно поле",
        "en": "✏️ Fix one field",
        "ua": "✏️ Виправити поле",
        "pl": "✏️ Popraw jedno pole",
    },
    "edit_field_pick": {
        "ru": "Выберите поле для исправления:",
        "en": "Pick a field to fix:",
        "ua": "Оберіть поле для виправлення:",
        "pl": "Wybierz pole do poprawy:",
    },
    "back_to_confirm": {
        "ru": "↩️ К проверке данных",
        "en": "↩️ Back to review",
        "ua": "↩️ До перевірки",
        "pl": "↩️ Wróć do podsumowania",
    },
    "validation_error": {
        "ru": "❌ {err}",
        "en": "❌ {err}",
        "ua": "❌ {err}",
        "pl": "❌ {err}",
    },
    "confirm_btn_checklist": {
        "ru": "📋 Чеклист в urząd",
        "en": "📋 Office checklist",
        "ua": "📋 Чекліст",
        "pl": "📋 Checklista do urzędu",
    },
    "confirm_btn_preview": {
        "ru": "👁 Podgląd PDF (wodny znak)",
        "en": "👁 Preview PDF (watermark)",
        "ua": "👁 Перегляд PDF",
        "pl": "👁 Podgląd PDF (znak wodny)",
    },
    "preview_sent": {
        "ru": "👁 To podgląd — pobierz finalny PDF po przycisku «Скачать».",
        "en": "👁 Preview only — tap Download for the final file.",
        "ua": "👁 Це перегляд.",
        "pl": "👁 To podgląd — finalny PDF po «Pobierz».",
    },
    "preview_caption": {
        "ru": "Podgląd",
        "en": "Preview",
        "ua": "Перегляд",
        "pl": "Podgląd",
    },
    "field_help_btn": {
        "ru": "❓ Co to znaczy?",
        "en": "❓ What does this mean?",
        "ua": "❓ Що це?",
        "pl": "❓ Co to znaczy?",
    },
    "field_help_missing": {
        "ru": "Brak opisu — wpisz dane jak w paszporcie.",
        "en": "No hint — use passport spelling.",
        "ua": "Немає підказки.",
        "pl": "Brak opisu pola.",
    },
    "usun_done": {
        "ru": "🗑 Twoje dane zostały usunięte z bazy WniosekPL.",
        "en": "🗑 Your data was deleted.",
        "ua": "🗑 Дані видалено.",
        "pl": "🗑 Dane usunięte.",
    },
    "generating": {
        "ru": "⏳ Генерирую PDF…",
        "en": "⏳ Generating PDF…",
        "ua": "⏳ Генерую PDF…",
        "pl": "⏳ Generuję PDF…",
    },
    "generating_package": {
        "ru": "⏳ Генерирую 3 PDF (pakiet)…",
        "en": "⏳ Generating 3 PDFs…",
        "ua": "⏳ 3 PDF…",
        "pl": "⏳ Generuję 3 PDF…",
    },
    "done": {
        "ru": "✅ Готово! Распечатайте, подпишите, отнесите в urząd.\n\n💯 Бесплатно — поделитесь ботом с друзьями.",
        "en": "✅ Done! Print, sign, submit.\n\n💯 Free — share the bot with friends.",
        "ua": "✅ Готово! Друкуйте, підпишіть, подайте в urząd.\n\n💯 Безкоштовно — поділіться ботом.",
        "pl": "✅ Gotowe! Drukuj, podpisz, złóż w urzędzie.\n\n💯 Za darmo — poleć znajomym.",
    },
    "package_done": {
        "ru": "✅ Пакет готов — 3 PDF выше. Ниже общий чеклист.",
        "en": "✅ Package ready — 3 PDFs above.",
        "ua": "✅ Пакет готовий — 3 PDF.",
        "pl": "✅ Pakiet gotowy — 3 PDF powyżej.",
    },
    "package_generate": {
        "ru": "✅ Сгенерировать все 3 PDF",
        "en": "✅ Generate all 3 PDFs",
        "ua": "✅ 3 PDF",
        "pl": "✅ Generuj 3 PDF",
    },
    "package_next": {
        "ru": "➡️ Следующий шаг пакета",
        "en": "➡️ Next in package",
        "ua": "➡️ Далі",
        "pl": "➡️ Dalej",
    },
    "podstawa_custom": {
        "ru": "✏️ Своя podstawa (введите текстом)",
        "en": "✏️ Custom legal basis (type)",
        "ua": "✏️ Своя podstawa",
        "pl": "✏️ Inna podstawa (wpisz)",
    },
    "podstawa_pick": {
        "ru": "Выберите podstawę prawną (§7 PESEL) или введите свою:",
        "en": "Pick legal basis (§7 PESEL) or type your own:",
        "ua": "Оберіть podstawę prawną:",
        "pl": "Wybierz podstawę prawną (§7 PESEL):",
    },
    "another": {
        "ru": "📄 Ещё один документ",
        "en": "📄 Another document",
        "ua": "📄 Ще один документ",
        "pl": "📄 Inny formularz",
    },
    "menu": {
        "ru": "🏠 Меню",
        "en": "🏠 Menu",
        "ua": "🏠 Меню",
        "pl": "🏠 Menu",
    },
    "share_btn": {
        "ru": "📤 Поделиться ботом",
        "en": "📤 Share bot",
        "ua": "📤 Поділитися",
        "pl": "📤 Udostępnij bota",
    },
    "privacy": {
        "ru": (
            f"<b>Политика конфиденциальности {BRAND}</b>\n\n"
            "Мы храним: Telegram ID, язык, имя пользователя, данные профиля "
            "(имя, адрес и т.д. для автозаполнения), черновики форм, "
            "статистику сгенерированных PDF и отзывы (/feedback).\n\n"
            "Мы не продаём данные третьим лицам. PDF создаётся на сервере бота "
            "и отправляется вам в Telegram.\n\n"
            "Удалить все данные: /usun (RODO).\n\n"
            f"{BRAND} — pomocnik, nie urząd. Это не юридическая консультация. "
            "Проверьте данные перед подачей в urząd."
        ),
        "en": (
            f"<b>{BRAND} Privacy Policy</b>\n\n"
            "We store: Telegram ID, language, username, profile data "
            "(name, address, etc. for autofill), form drafts, PDF completion "
            "stats, and feedback messages.\n\n"
            "We do not sell your data. PDFs are generated on our server and "
            "sent to you in Telegram.\n\n"
            "Delete all your data: /usun (GDPR/RODO).\n\n"
            f"{BRAND} is a helper — not a government office. "
            "This is not legal advice. Verify all data before submitting."
        ),
        "ua": "Зберігаємо Telegram ID. Видалити: /usun",
        "pl": (
            f"<b>Polityka prywatności {BRAND}</b>\n"
            "Przechowujemy ID Telegram, język, statystyki PDF.\n"
            "Usuń dane: /usun. To pomocnik — nie urząd."
        ),
    },
    "help": {
        "ru": (
            f"<b>{BRAND}</b>\n"
            "/start — меню\n"
            "/ask — AI-помощник по документам\n"
            "/docs — документы\n"
            "/lang — язык\n"
            "/cancel — отмена\n"
            "/usun — удалить данные\n"
            "/privacy — политика\n"
            "/ostatni — повторить последний PDF\n"
            "/profil — ваши сохранённые данные\n"
            "/guide — что мне нужно?\n"
            "/review — проверка человеком за 29 zł\n"
            "/feedback — отзыв или проблема\n\n"
            "📦 Пакет «Переезд» · EL/ZC/1 · EL/ZPS/1"
        ),
        "en": (
            f"<b>{BRAND}</b>\n"
            "/start /ask /docs /lang /cancel /usun /privacy /review\n"
            "📦 Relocation package · EL/ZC/1 · EL/ZPS/1"
        ),
        "ua": f"<b>{BRAND}</b>\n/start /ask /docs /lang /cancel /usun",
        "pl": (
            f"<b>{BRAND}</b>\n"
            "/start — menu\n"
            "/ask — asystent AI od dokumentów\n"
            "/docs — formularze\n"
            "/lang — język\n"
            "/cancel — anuluj\n"
            "/usun — usuń dane (RODO)\n"
            "/privacy — polityka\n"
            "/ostatni — ostatni formularz\n"
            "/profil — zapisane dane\n"
            "/guide — przewodnik\n"
            "/review — sprawdzenie przez człowieka za 29 zł\n"
            "/feedback — opinia\n\n"
            "📦 Pakiet Przeprowadzka · meldunek czasowy/stały · PESEL"
        ),
    },
    "skip_hint": {
        "ru": "Необязательное поле — ⏭ Пропустить. /cancel — отменить",
        "en": "Optional — tap Skip. /cancel to abort",
        "ua": "Необов'язкове — ⏭ Пропустити. /cancel — скасувати",
        "pl": "Pole opcjonalne — ⏭ Pomiń. /cancel — anuluj",
    },
    "skip_btn": {
        "ru": "⏭ Пропустить",
        "en": "⏭ Skip",
        "ua": "⏭ Пропустити",
        "pl": "⏭ Pomiń",
    },
    "skip_not_allowed": {
        "ru": "Это поле обязательное",
        "en": "This field is required",
        "ua": "Це поле обов'язкове",
        "pl": "To pole jest wymagane",
    },
    "back_btn": {
        "ru": "⬅️ Назад",
        "en": "⬅️ Back",
        "ua": "⬅️ Назад",
        "pl": "⬅️ Wstecz",
    },
    "profile_use_btn": {
        "ru": "♻️ Заполнить из сохранённых данных",
        "en": "♻️ Use saved data",
        "ua": "♻️ Збережені дані",
        "pl": "♻️ Użyj zapisanych danych",
    },
    "profile_used": {
        "ru": "♻️ Подставлены сохранённые данные — проверьте и дополните.",
        "en": "♻️ Prefilled from your profile — review and complete.",
        "ua": "♻️ Підставлено збережені дані.",
        "pl": "♻️ Uzupełniono zapisany profil — sprawdź dane.",
    },
    "profile_empty": {
        "ru": "Нет сохранённых данных. Сначала заполните любой документ.",
        "en": "No saved profile yet.",
        "ua": "Немає збережених даних.",
        "pl": "Brak zapisanego profilu.",
    },
    "profile_title": {
        "ru": "👤 <b>Ваш профиль</b> — данные для автозаполнения:",
        "en": "👤 <b>Your profile</b> — autofill data:",
        "ua": "👤 <b>Ваш профіль</b> — дані для автозаповнення:",
        "pl": "👤 <b>Twój profil</b> — dane do autouzupełniania:",
    },
    "profile_edit_prompt": {
        "ru": "Введите новое значение для <b>{label}</b>:\n/cancel — отмена",
        "en": "Enter new value for <b>{label}</b>:\n/cancel to abort",
        "ua": "Введіть нове значення для <b>{label}</b>:",
        "pl": "Wpisz nową wartość dla <b>{label}</b>:",
    },
    "profile_updated": {
        "ru": "✅ Профиль обновлён.",
        "en": "✅ Profile updated.",
        "ua": "✅ Профіль оновлено.",
        "pl": "✅ Profil zaktualizowany.",
    },
    "profile_clear_btn": {
        "ru": "🗑 Очистить профиль",
        "en": "🗑 Clear profile",
        "ua": "🗑 Очистити профіль",
        "pl": "🗑 Wyczyść profil",
    },
    "profile_cleared": {
        "ru": "🗑 Профиль очищен (история PDF сохранена).",
        "en": "🗑 Profile cleared.",
        "ua": "🗑 Профіль очищено.",
        "pl": "🗑 Profil wyczyszczony.",
    },
    "karta_checklist_btn": {
        "ru": "📋 Чеклист",
        "en": "📋 Checklist",
        "ua": "📋 Чекліст",
        "pl": "📋 Checklista",
    },
    "karta_waitlist_btn": {
        "ru": "🛂 Karta pobytu — скоро (записаться)",
        "en": "🛂 Residence card — coming soon",
        "ua": "🛂 Karta pobytu — скоро",
        "pl": "🛂 Karta pobytu — wkrótce (zapisz się)",
    },
    "waitlist_ok": {
        "ru": "✅ Вы в списке ожидания Karta pobytu. Напишем, когда будет готово.",
        "en": "✅ You're on the Karta pobytu waitlist.",
        "ua": "✅ Ви в списку очікування.",
        "pl": "✅ Jesteś na liście oczekujących na Kartę pobytu.",
    },
    "waitlist_dup": {
        "ru": "Вы уже в списке ожидания.",
        "en": "Already on the waitlist.",
        "ua": "Вже в списку.",
        "pl": "Już jesteś na liście.",
    },
    "remind_25": {
        "ru": "🔔 Через 25 дней",
        "en": "🔔 In 25 days",
        "ua": "🔔 Через 25 днів",
        "pl": "🔔 Za 25 dni",
    },
    "remind_90": {
        "ru": "🔔 Через 90 дней",
        "en": "🔔 In 90 days",
        "ua": "🔔 Через 90 днів",
        "pl": "🔔 Za 90 dni",
    },
    "remind_no": {
        "ru": "Не напоминать",
        "en": "No reminder",
        "ua": "Без нагадування",
        "pl": "Bez przypomnienia",
    },
    "remind_set": {
        "ru": "🔔 Напоминание установлено.",
        "en": "🔔 Reminder set.",
        "ua": "🔔 Нагадування встановлено.",
        "pl": "🔔 Przypomnienie ustawione.",
    },
    "remind_offer": {
        "ru": "🔔 Напомнить проверить meldunek / pobyt?",
        "en": "🔔 Set a meldunek reminder?",
        "ua": "🔔 Нагадати про meldunek?",
        "pl": "🔔 Ustawić przypomnienie o meldunku?",
    },
    "repeat_last_btn": {
        "ru": "🔁 Повторить последний документ",
        "en": "🔁 Repeat last document",
        "ua": "🔁 Повторити останній",
        "pl": "🔁 Ostatni formularz",
    },
    "repeat_last_none": {
        "ru": "Пока нет истории. Сначала сгенерируйте любой PDF.",
        "en": "No history yet.",
        "ua": "Ще немає історії.",
        "pl": "Brak historii — wygeneruj pierwszy PDF.",
    },
    "meldunek_menu": {
        "ru": "🏠 <b>Meldunek</b> — выберите тип:",
        "en": "🏠 <b>Meldunek</b> — pick type:",
        "ua": "🏠 <b>Meldunek</b> — оберіть тип:",
        "pl": "🏠 <b>Meldunek</b> — wybierz typ:",
    },
    "meldunek_czasowy_btn": {
        "ru": "⏱ Pobyt czasowy (EL/ZC/1)",
        "en": "⏱ Temporary (EL/ZC/1)",
        "ua": "⏱ Pobyt czasowy",
        "pl": "⏱ Pobyt czasowy (EL/ZC/1)",
    },
    "meldunek_staly_btn": {
        "ru": "📍 Pobyt stały (EL/ZPS/1)",
        "en": "📍 Permanent (EL/ZPS/1)",
        "ua": "📍 Pobyt stały",
        "pl": "📍 Pobyt stały (EL/ZPS/1)",
    },
    "quick_pesel": {
        "ru": "🆔 PESEL",
        "en": "🆔 PESEL",
        "ua": "🆔 PESEL",
        "pl": "🆔 PESEL",
    },
    "quick_meldunek": {
        "ru": "🏠 Meldunek",
        "en": "🏠 Meldunek",
        "ua": "🏠 Meldunek",
        "pl": "🏠 Meldunek",
    },
    "quick_umowa": {
        "ru": "📄 Umowa",
        "en": "📄 Rental",
        "ua": "📄 Umowa",
        "pl": "📄 Umowa",
    },
    "guide_btn": {
        "ru": "❓ Что мне нужно?",
        "en": "❓ What do I need?",
        "ua": "❓ Що мені потрібно?",
        "pl": "❓ Czego potrzebuję?",
    },
    "review_btn": {
        "ru": "🔎 Проверка человеком — 29 zł",
        "en": "🔎 Human review — 29 zł",
        "ua": "🔎 Перевірка людиною — 29 zł",
        "pl": "🔎 Sprawdzenie przez człowieka — 29 zł",
    },
    "review_waitlist_btn": {
        "ru": "✅ Хочу проверку за 29 zł",
        "en": "✅ I want review for 29 zł",
        "ua": "✅ Хочу перевірку за 29 zł",
        "pl": "✅ Chcę sprawdzenie za 29 zł",
    },
    "review_offer": {
        "ru": (
            "<b>Платная проверка документов</b>\n\n"
            "Бот бесплатно генерирует PDF. За <b>29 zł</b> можно запросить "
            "проверку человеком перед подачей: данные, типичные ошибки, "
            "чеклист и что взять в urząd.\n\n"
            "Это не юридическая консультация и не гарантия решения urzędu. "
            "Сейчас собираем первые заявки — нажмите кнопку, если вам это нужно."
        ),
        "en": (
            "<b>Paid document review</b>\n\n"
            "The bot generates PDFs for free. For <b>29 zł</b>, you can request "
            "a human check before submission: data, common mistakes, checklist, "
            "and what to take to the office.\n\n"
            "Not legal advice and not a government decision guarantee. "
            "We are collecting early requests now."
        ),
        "ua": (
            "<b>Платна перевірка документів</b>\n\n"
            "Бот безкоштовно генерує PDF. За <b>29 zł</b> можна замовити "
            "перевірку людиною перед подачею: дані, типові помилки, чекліст.\n\n"
            "Це не юридична консультація. Зараз збираємо перші заявки."
        ),
        "pl": (
            "<b>Płatne sprawdzenie dokumentów</b>\n\n"
            "Bot generuje PDF za darmo. Za <b>29 zł</b> możesz poprosić "
            "o sprawdzenie przez człowieka przed złożeniem: dane, typowe błędy, "
            "checklista i co zabrać do urzędu.\n\n"
            "To nie porada prawna ani gwarancja decyzji urzędu. "
            "Teraz zbieramy pierwsze zgłoszenia."
        ),
    },
    "review_waitlist_ok": {
        "ru": "✅ Заявка сохранена. Админ увидит её в статистике и сможет связаться с вами в Telegram.",
        "en": "✅ Request saved. The admin will see it in stats and can contact you on Telegram.",
        "ua": "✅ Заявку збережено. Адмін побачить її в статистиці.",
        "pl": "✅ Zgłoszenie zapisane. Admin zobaczy je w statystykach i może odezwać się na Telegramie.",
    },
    "review_waitlist_dup": {
        "ru": "Вы уже оставили заявку на проверку.",
        "en": "You already requested a review.",
        "ua": "Ви вже залишили заявку.",
        "pl": "Masz już zgłoszenie na sprawdzenie.",
    },
    "guide_text": {
        "ru": (
            "<b>Короткий гид</b>\n\n"
            "🆕 <b>Только приехали?</b> → 📦 Пакет «Переезд» (umowa + meldunek + PESEL)\n"
            "🏠 <b>Есть квартира?</b> → Meldunek (нужна подпись właściciela)\n"
            "🆔 <b>Нужен PESEL?</b> → после meldunku, с §7 podstawa prawna\n"
            "📄 <b>Аренда?</b> → Umowa najmu (szablon, nie urzędowy)\n"
            "🛂 <b>Karta pobytu?</b> → чеклист в меню, формуляр скоро\n\n"
            "💯 Всё бесплатно. /profil — сохранённые данные."
        ),
        "en": (
            "<b>Quick guide</b>\n\n"
            "🆕 <b>Just arrived?</b> → 📦 Relocation package\n"
            "🏠 <b>Have a flat?</b> → Meldunek (landlord signature required)\n"
            "🆔 <b>Need PESEL?</b> → after meldunek + §7 legal basis\n"
            "📄 <b>Renting?</b> → Rental agreement template\n"
            "🛂 <b>Residence card?</b> → checklist in menu\n\n"
            "💯 All free. /profil — saved data."
        ),
        "ua": (
            "<b>Короткий гід</b>\n\n"
            "🆕 <b>Щойно приїхали?</b> → 📦 Пакет «Переїзд»\n"
            "🏠 <b>Є квартира?</b> → Meldunek (підпис власника)\n"
            "🆔 <b>Потрібен PESEL?</b> → після meldunku + §7\n"
            "🛂 <b>Karta pobytu?</b> → чекліст у меню"
        ),
        "pl": (
            "<b>Krótki przewodnik</b>\n\n"
            "🆕 <b>Świeżo w Polsce?</b> → 📦 Pakiet Przeprowadzka\n"
            "🏠 <b>Masz mieszkanie?</b> → Meldunek (podpis właściciela)\n"
            "🆔 <b>Potrzebujesz PESEL?</b> → po meldunku + §7 podstawa prawna\n"
            "📄 <b>Najem?</b> → Umowa najmu (szablon)\n"
            "🛂 <b>Karta pobytu?</b> → checklista w menu\n\n"
            "💯 Za darmo. /profil — zapisane dane."
        ),
    },
    "draft_offer": {
        "ru": "📝 У вас есть незаконченная форма. Продолжить?",
        "en": "📝 You have an unfinished form. Continue?",
        "ua": "📝 Є незавершена форма. Продовжити?",
        "pl": "📝 Masz niedokończony formularz. Kontynuować?",
    },
    "draft_resume_btn": {
        "ru": "▶️ Продолжить заполнение",
        "en": "▶️ Continue form",
        "ua": "▶️ Продовжити",
        "pl": "▶️ Kontynuuj",
    },
    "draft_discard_btn": {
        "ru": "🗑 Начать заново",
        "en": "🗑 Discard draft",
        "ua": "🗑 Скасувати",
        "pl": "🗑 Odrzuć szkic",
    },
    "profil_btn": {
        "ru": "👤 Профиль",
        "en": "👤 Profile",
        "ua": "👤 Профіль",
        "pl": "👤 Profil",
    },
    "progress": {
        "ru": "Вопрос {cur} из {total}",
        "en": "Question {cur} of {total}",
        "ua": "Питання {cur} з {total}",
        "pl": "Pytanie {cur} z {total}",
    },
    "package_preview_note": {
        "ru": "👁 Podgląd — przykład umowy najmu. Pełny pakiet: 3 PDF po zatwierdzeniu.",
        "en": "👁 Preview — rental sample only. Full package: 3 PDFs after confirm.",
        "ua": "👁 Перегляд — зразок umowy. Повний пакет: 3 PDF.",
        "pl": "👁 Podgląd — przykład umowy. Pełny pakiet: 3 PDF po zatwierdzeniu.",
    },
    "zus_checklist_btn": {
        "ru": "🏥 ZUS",
        "en": "🏥 ZUS",
        "ua": "🏥 ZUS",
        "pl": "🏥 ZUS",
    },
    "feedback_prompt": {
        "ru": "Напишите отзыв или проблему (1 сообщение). /cancel — отмена.",
        "en": "Send feedback or report a problem. /cancel to abort.",
        "ua": "Напишіть відгук або проблему. /cancel — скасувати.",
        "pl": "Napisz opinię lub zgłoś problem. /cancel — anuluj.",
    },
    "feedback_ok": {
        "ru": "✅ Спасибо! Мы учтём ваш отзыв.",
        "en": "✅ Thanks! Feedback received.",
        "ua": "✅ Дякуємо!",
        "pl": "✅ Dziękujemy za opinię!",
    },
    "pdf_error": {
        "ru": "❌ Не удалось создать PDF. Попробуйте /docs или /feedback — опишите проблему.",
        "en": "❌ PDF generation failed. Try /docs again.",
        "ua": "❌ Помилка PDF.",
        "pl": "❌ Nie udało się wygenerować PDF. Spróbuj /docs.",
    },
    "package_summary_note": {
        "ru": "📦 3 PDF: umowa, meldunek, PESEL",
        "en": "📦 3 PDFs: rental, meldunek, PESEL",
        "ua": "📦 3 PDF: umowa, meldunek, PESEL",
        "pl": "📦 3 PDF: umowa, meldunek, PESEL",
    },
}

MODE_NOTES = {
    "official": {
        "ru": "📋 Официальный бланк gov.pl / MSWiA",
        "en": "📋 Official gov.pl / MSWiA form",
        "ua": "📋 Офіційний бланк gov.pl",
        "pl": "📋 Oficjalny formularz rządowy (gov.pl / MSWiA)",
    },
    "helper": {
        "ru": "📄 Шаблон WniosekPL",
        "en": "📄 WniosekPL template",
        "ua": "📄 Szablon WniosekPL",
        "pl": "📄 Pomocnik WniosekPL",
    },
    "helper_fallback": {
        "ru": "📄 Pomocnik — fallback",
        "en": "📄 Helper fallback",
        "ua": "📄 Pomocnik — fallback",
        "pl": "📄 Pomocnik — błąd urzędowego PDF",
    },
}


def t(key: str, lang: str) -> str:
    block = TEXTS.get(key, {})
    return block.get(lang, block.get("ru", key))


def mode_note(mode: str, lang: str) -> str:
    block = MODE_NOTES.get(mode, {})
    return block.get(lang, block.get("pl", ""))
