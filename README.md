# WniosekPL

Бесплатный Telegram-бот для иностранцев в Польше: отвечаете на вопросы на RU/EN/UA/PL — получаете PDF на польских бланках.

**Pomocnik, nie urząd** — не юридическая консультация.

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
cd urzad-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# BOT_TOKEN от @BotFather
python bot.py
```

На Windows при SSL-ошибках: `RELAX_SSL=true` в `.env` (только локально).

## Команды

| Команда | Описание |
|---------|----------|
| `/start` | Главное меню |
| `/docs` | Выбор документа |
| `/profil` | Сохранённые данные |
| `/ostatni` | Повторить последний PDF |
| `/lang` | Смена языка |
| `/help` | Справка |
| `/cancel` | Отмена + сброс черновика |
| `/usun` | Удалить данные (RODO) |
| `/privacy` | Политика |
| `/stats` | Статистика (admin) |

## Функции

- Официальные PDF PESEL / Meldunek
- Пакет «Переезд» — 3 документа за один раз
- Профиль и автозаполнение, черновик формы
- Валидация полей, исправление одного поля
- Чеклисты (PESEL, meldunek, ZUS, karta pobytu)
- Podgląd PDF, напоминания meldunek, рефералы `?start=ref_xxx`

## Тесты

```bash
python -m pytest tests/ -q
```

## Деплой

См. `DEPLOY_RENDER.md`. Лендинг: `landing/index.html`.

## База

SQLite: `data/urzad.db`
