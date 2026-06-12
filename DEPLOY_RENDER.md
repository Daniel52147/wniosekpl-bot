# Деплой WniosekPL на Render

Telegram-бот работает через **polling** (`python bot.py`), поэтому на Render нужен **Background Worker**, не Web Service.

## 1. Подготовка репозитория

1. Создайте репозиторий на GitHub (например `wniosekpl`).
2. Залейте папку `urzad-ai` (или весь `Project`, тогда укажите Root Directory ниже).
3. **Никогда не коммитьте** файл `.env` — только `.env.example`.
4. По желанию закоммитьте PDF в `templates/official/` — иначе бот скачает их при старте с gov.pl.

```bash
git init
git add .
git commit -m "WniosekPL bot"
git remote add origin https://github.com/ВАШ_АККАУНТ/wniosekpl.git
git push -u origin main
```

## 2. Создание сервиса на Render

### Вариант A — через Blueprint (проще)

1. [dashboard.render.com](https://dashboard.render.com) → **New** → **Blueprint**.
2. Подключите GitHub-репозиторий.
3. Render подхватит `render.yaml` из корня репозитория.
4. При создании введите секреты:
   - `BOT_TOKEN` — от [@BotFather](https://t.me/BotFather)
   - `BOT_USERNAME` — без `@`, например `wniosekpl_bot`
   - `ADMIN_TELEGRAM_IDS` — ваш ID от [@userinfobot](https://t.me/userinfobot)

### Вариант B — вручную

1. **New** → **Background Worker**.
2. Подключите репозиторий.
3. Настройки:

| Поле | Значение |
|------|----------|
| **Name** | `wniosekpl-bot` |
| **Region** | Frankfurt (ближе к Польше) |
| **Branch** | `main` |
| **Root Directory** | `urzad-ai` *(если репо = весь Project)* |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

4. **Environment Variables** (Environment):

| Key | Value |
|-----|--------|
| `BOT_TOKEN` | токен бота |
| `BOT_USERNAME` | username без @ |
| `ADMIN_TELEGRAM_IDS` | ваш Telegram ID |
| `DATABASE_PATH` | `/data/urzad.db` |

5. **Disk** (важно для базы пользователей):
   - Add disk → Mount path: `/data` → Size: 1 GB  
   Без диска SQLite **сбрасывается** при каждом redeploy.

6. **Create Worker** → дождитесь зелёного статуса **Live**.

## 3. Проверка

1. В логах Render должно быть: `WniosekPL bot started`.
2. В Telegram: `/start` у вашего бота.
3. От вашего аккаунта: `/stats` (если ID в `ADMIN_TELEGRAM_IDS`).

## 4. Обновление бота

Каждый `git push` в `main` → Render пересобирает Worker автоматически (если включён Auto-Deploy).

## 5. Частые проблемы

| Проблема | Решение |
|----------|---------|
| Бот не отвечает | Проверьте `BOT_TOKEN`, логи Worker, статус Live |
| Два инстанса | Остановите `python bot.py` на своём ПК — только один polling |
| База обнулилась | Подключите Persistent Disk на `/data` |
| SSL при скачивании PDF | Бот сам повторяет с fallback; смотрите логи |
| Free tier засыпает | Worker на free **не спит** как Web; polling держит процесс активным |

## 6. Стоимость

- **Free Worker** — ограничения Render (может быть недоступен в некоторых регионах).
- Для продакшена лучше **Starter Worker** (~$7/мес) + диск 1 GB.

## 7. Локально vs Render

- Локально: `.env` с теми же переменными.
- На Render: только Environment Variables в панели, **не** файл `.env`.
