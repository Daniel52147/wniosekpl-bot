# WniosekPL Platform v1.0

AI-помощник для иностранцев в Польше: **web + Telegram + billing + cabinet**.

**Pomocnik, nie urząd** — не юридическая консультация.

## Что умеет v1.0

- AI-чат (rule-based + knowledge base; LLM если есть `OPENAI_API_KEY`)
- Генерация PDF: PESEL, meldunek, umowa, pismo, upoważnienie, oświadczenie, karta prep
- Анализ загруженных PDF/писем
- Генератор официальных писем
- Чеклист karty pobytu
- Календарь сроков
- Каталог urzędów / услуг
- Оплата: Stripe или demo mock-checkout (`19 zł` AI / `29 zł` review)
- Личный кабинет пользователя
- Telegram-бот как канал (`/ask`, `/karta`, `/calendar`, `/premium`)

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# BOT_TOKEN + опционально OPENAI_API_KEY / STRIPE_SECRET_KEY
python -m uvicorn server:app --reload
# отдельно:
python bot.py
```

Сайт: `http://127.0.0.1:8000`

## API

| Endpoint | Описание |
|----------|----------|
| `GET /health` | статус платформы |
| `GET /api/meta` | план, лимиты, флаги LLM/Stripe/Telegram |
| `GET /api/documents` | список документов |
| `GET /api/documents/{id}` | поля + checklist |
| `POST /api/documents/{id}/generate` | PDF |
| `POST /api/assistant/ask` | AI |
| `POST /api/billing/checkout` | Stripe/mock оплата |
| `GET /api/cabinet/{user_id}` | личный кабинет |
| `POST /api/letters/generate` | письмо |
| `POST /api/uploads/analyze` | разбор PDF/фото |
| `GET /api/karta/{user_id}` | checklist karty |
| `GET/POST /api/calendar` | календарь |
| `GET /api/services` | urzędy / услуги |
| `GET /api/admin/overview` | админка |

## Оплата

Без Stripe ключей работает **mock checkout**:
1. `POST /api/billing/checkout`
2. открывается `/api/billing/mock-complete`
3. активируется подписка на 30 дней

С ключами Stripe — создаётся настоящий Checkout Session.

## Telegram

Нужен `BOT_TOKEN` в `.env` и запущенный `python bot.py`.

Команды: `/start` `/ask` `/docs` `/karta` `/calendar` `/premium` `/review`

## Тесты

```bash
python -m pytest tests/ -q
```

## Деплой

См. `DEPLOY_RENDER.md`. Для production задайте:
`PUBLIC_BASE_URL`, `OPENAI_API_KEY`, `STRIPE_*`, `ADMIN_API_KEY`.
