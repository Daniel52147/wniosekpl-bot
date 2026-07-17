# WniosekPL Platform v2.2

AI-помощник для иностранцев в Польше: **web + Telegram + auth + Stripe + OmniRoute**.

**Pomocnik, nie urząd** — не юридическая консультация.

## Что умеет v2.2

- Регистрация: email/пароль, Google/Facebook OAuth, magic link, RODO export/delete
- AI-чат: rules + knowledge + OmniRoute/LLM cascade
- PDF: PESEL, meldunek, umowa, pismo, upoważnienie, oświadczenie, odwołanie, zaświadczenie, karta prep
- Пакет «Przeprowadzka» → ZIP из 3 PDF
- OCR PDF/фото (Tesseract), письма, checklist karty, календарь
- Marketplace юристов, каталог urzędów (Warszawa/Kraków/Wrocław/Gdańsk/Poznań)
- Оплата: Stripe checkout/portal/invoices/webhooks или mock
- Setup wizard `/setup` для ключей без правки кода
- Telegram-бот как канал

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# BOT_TOKEN обязателен для бота
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
# отдельно:
python bot.py
# опционально AI gateway:
bash scripts/start_omniroute.sh
```

Сайт: `http://127.0.0.1:8000` · Setup: `/setup` · Admin: `/admin`

## Docker

```bash
docker compose up -d
docker compose --profile bot up -d
```

## Документация

- `docs/AUTH_BILLING.md` — auth + Stripe
- `docs/OMNIROUTE.md` — AI gateway
- `DEPLOY_RENDER.md` — Render Blueprint (`render.yaml`)
- `THIRD_PARTY.md` — OmniRoute attribution

## Тесты

```bash
python -m pytest tests/ -q
```

## Версия

`GET /health` → `"version": "2.2.0"`
