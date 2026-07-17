# WniosekPL

AI-помощник для иностранцев в Польше: web + Telegram.

Спрашиваете на RU/EN/UA/PL — получаете чеклист, объяснение и PDF на польских бланках.

**Pomocnik, nie urząd** — не юридическая консультация.

## Что это

| Канал | Как запускать |
|-------|----------------|
| **Web / API** | `python -m uvicorn server:app --reload` |
| **Telegram** | `python bot.py` |

## Документы

| Документ | ID | Источник |
|----------|-----|----------|
| **PESEL** | `pesel` | gov.pl AcroForm |
| **Meldunek czasowy** | `meldunek` | EL/ZC/1 overlay |
| **Meldunek stały** | `meldunek_staly` | EL/ZPS/1 overlay |
| **Umowa najmu** | `umowa_najmu` | Szablon pomocniczy |
| **Pakiet Przeprowadzka** | package | umowa + meldunek + PESEL |

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# BOT_TOKEN от @BotFather — только если нужен Telegram
python -m uvicorn server:app --reload
```

На Windows при SSL-ошибках: `RELAX_SSL=true` в `.env` (только локально).

Откройте `http://127.0.0.1:8000` — сайт с AI-чатом.

## Web API

| Endpoint | Описание |
|----------|----------|
| `GET /` | Продуктовый web UI |
| `GET /health` | Проверка сервера |
| `GET /api/meta?user_id=` | Версия, лимит AI, остаток вопросов |
| `GET /api/documents?lang=ru` | Список доступных документов |
| `POST /api/assistant/ask` | AI-помощник с лимитом бесплатных вопросов |
| `POST /api/leads` | Заявки на подписку, human review или waitlist |

## Telegram-команды

| Команда | Описание |
|---------|----------|
| `/start` | Главное меню |
| `/ask` | AI-помощник по документам в Польше |
| `/docs` | Выбор документа |
| `/profil` | Сохранённые данные |
| `/ostatni` | Повторить последний PDF |
| `/lang` | Смена языка |
| `/help` | Справка |
| `/review` | Заявка на проверку документов человеком |
| `/cancel` | Отмена + сброс черновика |
| `/usun` | Удалить данные (RODO) |
| `/privacy` | Политика |
| `/stats` | Статистика (admin) |

## Функции

- Web UI с живым AI-чатом
- AI-помощник MVP: 5 бесплатных вопросов в день (PESEL, karta pobytu, ZUS/NFZ, письма)
- Официальные PDF PESEL / Meldunek
- Пакет «Переезд» — 3 документа за один раз
- Профиль и автозаполнение, черновик формы
- Чеклисты, podgląd PDF, напоминания meldunek
- Lead capture: подписка AI 19 zł/мес и human review 29 zł
- Telegram как дополнительный канал

## Тесты

```bash
python -m pytest tests/ -q
```

## Деплой

См. `DEPLOY_RENDER.md`. Основной сервис — Web API; Telegram worker опционален.

## База

SQLite: `data/urzad.db` (или `DATABASE_PATH`)
