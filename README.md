# WniosekPL Platform v2.4

AI-помощник для иностранцев в Польше: **гид в MOS 2.0**, не клон urzędu.

**Pomocnik, nie urząd** — не юридическая консультация. Официальный wniosek — только на [mos.cudzoziemcy.gov.pl](https://mos.cudzoziemcy.gov.pl).

## Главный сценарий (то, ради чего продукт)

1. Короткий onboarding (цель / PESEL / срок pobytu)
2. Чеклист готовности → экран «всё готово»
3. Что приложить + **Открыть MOS** + 5 шагов в портале (логин → wniosek → pliki → podpis → UPO)
4. PDF-черновики на сайте (поля сохраняются)
5. Один прогресс: сайт ↔ Telegram (`/profile?tab=account&link=1`)

Всё остальное (OCR, marketplace юристов, OAuth) — вторично и не в главном пути кабинета.

## Каналы

| | |
|--|--|
| Сайт | `/` маркетинг · `/profile` кабинет (Teraz / Dokumenty / Konto) |
| Telegram | `@wniosekpl_bot` — тот же прогресс после связки |
| Setup | `/setup` — Stripe `whsec_…`, OAuth, PUBLIC_BASE_URL |
| Health | `/health` · `/ready` (prod checklist) |

## Быстрый старт (локально)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# BOT_TOKEN — для бота; без Stripe — mock billing
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
# отдельно (та же DATABASE_PATH!):
python bot.py
```

Сайт: `http://127.0.0.1:8000` · Setup: `/setup` · Admin: `/admin`

## Прод без костылей

**Рекомендуется: Docker Compose** — API + bot на одном volume SQLite:

```bash
docker compose --profile bot up -d
```

**Render:** Blueprint `render.yaml` поднимает **один** web-сервис через `scripts/start_render.sh` (API + bot + периодический backup на одном диске).  
Не создавайте отдельный worker со своим диском — получите два разных прогресса.

Обязательно:

1. Постоянный `PUBLIC_BASE_URL` (не `*.trycloudflare.com`)
2. `STRIPE_WEBHOOK_SECRET=whsec_…` в `/setup` — без него live checkout блокируется
3. Persistent disk `/data` + бэкапы (`python -m scripts.backup_db` или `POST /api/admin/backup`)
4. Смотрите `/ready` → `prod_checklist`

Подробнее: [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)

> `DATABASE_URL` / Postgres: схема в `scripts/postgres_schema.sql` — **пока не подключена** к рантайму. Прод сегодня = SQLite + бэкапы на общем диске.

## Стек

- FastAPI + aiogram + SQLite (`aiosqlite`)
- Stripe checkout / portal / webhooks (нужен `whsec`)
- OmniRoute / OpenAI cascade для AI
- Официальные PDF-шаблоны + helper-формы

## Тесты

```bash
python -m pytest tests/ -q
```

## Версия

`PRODUCT_VERSION` в `server.py` → **2.4.1**. См. [CHANGELOG.md](./CHANGELOG.md).
