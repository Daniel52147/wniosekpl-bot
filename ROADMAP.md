# WniosekPL — roadmap

## Done (through v2.4.4)

- [x] MOS guide → finale (attachments + Open MOS + 5 portal steps)
- [x] Onboarding (purpose / PESEL / deadline)
- [x] Web PDF drafts + site↔Telegram link (MOS, drafts, calendar, subscription)
- [x] Auth (email/password, OAuth hooks, magic link, RODO export/delete)
- [x] Stripe checkout + webhook verification gate (`whsec` required for live)
- [x] Single-disk deploy (`start_render.sh` / docker compose)
- [x] `/ready` prod checklist + SQLite backups
- [x] Trust / FAQ / gov.pl links
- [x] AI + knowledge; helper PDFs; cabinet Teraz/Dokumenty/Konto
- [x] Now hero: one human next step + % ready (v2.4.3)
- [x] Cabinet polish: RU/UA copy, first-visit declutter, errors/retry, sticky tabs, What’s new (v2.4.4)

## Secondary (keep, don’t expand on main path)

- OCR uploads, lawyer marketplace APIs, multi-city services catalog
- These stay as API/bot extras — not the default cabinet journey

## Next (real prod calm)

- [ ] Stable custom domain (user/ops) + monitoring alerts on `/ready`
- [ ] Wire Postgres (`DATABASE_URL`) for horizontal scale — schema stub exists
- [ ] Deeper account merge (onboarding plan server-side, payment identity remap)
- [ ] Optional multi-country packs after MOS path is rock-solid
