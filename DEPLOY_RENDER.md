# Деплой WniosekPL (прод без костылей)

Цель: **один домен + одна SQLite + webhook Stripe + бот на том же диске**.

## Рекомендуемый путь A — Docker (VPS)

```bash
cp .env.example .env
# PUBLIC_BASE_URL=https://ваш-домен
# STRIPE_* включая STRIPE_WEBHOOK_SECRET=whsec_...
# BOT_TOKEN=...
docker compose --profile bot up -d
```

API и bot монтируют один volume `wniosekpl-data` → общий прогресс и связка сайт↔Telegram работают.

Cron бэкапа (на хосте):

```bash
0 3 * * * cd /opt/wniosekpl && docker compose exec -T api python -c "from scripts.backup_db import backup_database; print(backup_database())"
```

Проверка: `curl https://ваш-домен/ready` → `prod_checklist.stripe_webhook`, `stable_domain`, `db_backups`.

---

## Путь B — Render Blueprint

1. [dashboard.render.com](https://dashboard.render.com) → **New** → **Blueprint** → этот репозиторий.
2. Подхватывается `render.yaml`: **один** web-сервис `wniosekpl`, старт `bash scripts/start_render.sh`.
3. Задайте секреты:
   - `PUBLIC_BASE_URL` = `https://<service>.onrender.com` (потом свой домен)
   - `BOT_TOKEN`, `STRIPE_*`, особенно **`STRIPE_WEBHOOK_SECRET`**
   - `ADMIN_API_KEY`
4. Disk `/data` обязателен.

Скрипт старта:

- поднимает API;
- если есть `BOT_TOKEN` — бота **в том же процессе/диске**;
- делает стартовый backup и фоновый раз в 12ч.

**Не добавляйте** отдельный Background Worker со своим диском — это ломает «один аккаунт».

### Stripe webhook на Render

1. `/setup` → скопируйте URL `…/api/billing/webhook`
2. Stripe Workbench → Webhooks → destination → Reveal `whsec_…`
3. Вставьте в `STRIPE_WEBHOOK_SECRET` и Save
4. Без `whsec` live checkout **заблокирован** (ошибка `stripe_webhook_required`)

### Свой домен

Render → Custom Domain → обновите `PUBLIC_BASE_URL` → перезапуск.  
Cloudflare Tunnel (`*.trycloudflare.com`) годится только для демо: `/ready` пометит `stable_domain: false`.

### Ручной backup

```bash
curl -X POST https://ваш-домен/api/admin/backup -H "X-Admin-Key: $ADMIN_API_KEY"
```

---

## Postgres

`DATABASE_URL` и `scripts/postgres_schema.sql` — заготовка. Рантайм пока всегда SQLite.  
Пока не переедем — держите один файл БД и бэкапы.

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| Разный прогресс сайт/бот | Разные диски / разные `DATABASE_PATH` |
| Checkout 400 `stripe_webhook_required` | Вставьте `whsec_…` в `/setup` |
| База обнулилась | Нет Persistent Disk на `/data` |
| Tunnel URL меняется | Поставьте постоянный домен |
| Free tier спит | Платный инстанс или внешний ping `/health` |
