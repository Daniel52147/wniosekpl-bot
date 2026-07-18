# Changelog

## 2.4.2 — 2026-07-18

### New-user UX + official tone
- Official bar (MOS / UdSC / Profil Zaufany / Info) on landing and cabinet
- 3-stage path: Prepare → Review → File in MOS
- First-visit “How to use profile” card; clearer tab hints
- Onboarding and landing copy emphasize filing only on gov.pl

## 2.4.1 — 2026-07-18

### Prod hardening
- Live Stripe checkout blocked without `STRIPE_WEBHOOK_SECRET` (`whsec_…`)
- Single-process deploy: `scripts/start_render.sh` + updated `render.yaml` (API+bot one disk)
- `/ready` prod checklist + shared-DB hint; `POST /api/admin/backup`
- Backup prune (keep 14); deploy docs rewritten

### One product (web ↔ Telegram)
- Link banner on Teraz; landing CTA → `/profile?tab=account&link=1`
- On link: sync MOS progress, PDF drafts, calendar events, active subscription

### Focus
- Removed dead `platform.js` from cabinet main path
- AI odwołanie actions point back to MOS, not lawyer marketplace
- Trust FAQ: sync scope; README aligned to v2.4 main scenario

## 2.4.0 — 2026-07-18

- MOS finale screen (attachments + Open MOS + 5 portal steps)
- Web PDF form drafts (localStorage + API)
- Account link codes / Telegram `/link`
- Trust block + FAQ on landing and Konto

## 2.3.0 — 2026-07-18

- 3-question onboarding → personalized next MOS step
- Cabinet simplified to Teraz / Dokumenty / Konto

## 2.2.0 — 2026-07-17

### Product
- New helper docs: **odwołanie**, **zaświadczenie o zameldowaniu**
- Relocation package ZIP API: `GET/POST /api/packages…`
- Extra knowledge FAQ (kolejka UW, szkoła, bank, PIT)
- Services: Wrocław / Gdańsk / Poznań + PUE ZUS
- Marketplace: Poznań students + Trójmiasto
- AI topics: praca, odwołanie
- OCR ready with Tesseract (pol+eng)

### Auth / privacy
- `POST /api/auth/logout`
- `GET /api/account/export` (RODO)
- `DELETE /api/account`
- Referral attach endpoint

### Platform
- Calendar list/delete APIs
- PWA manifest, robots.txt, sitemap
- README + version alignment to 2.2
- BotFather commands: `/lawyers`, `/countries`

## 2.1.0

- Email/password auth, Google/Facebook OAuth hooks
- Full Stripe billing surface + `/setup` wizard

## 2.0.0

- OmniRoute AI gateway integration
- Platform cabinet / karta / letters / uploads
