# Auth + Billing (v2.1)

## Registration

- **Email + password**: `POST /api/auth/register`, `POST /api/auth/login`
- **Google**: set `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET`, redirect URI  
  `{PUBLIC_BASE_URL}/api/auth/google/callback`
- **Facebook**: set `FACEBOOK_APP_ID` + `FACEBOOK_APP_SECRET`, redirect URI  
  `{PUBLIC_BASE_URL}/api/auth/facebook/callback`
- **Magic link / email verify / password reset** — SMTP optional (`SMTP_HOST`/`SMTP_FROM`); without SMTP links are returned in API for demo.

Also set `APP_SECRET` (long random) for OAuth state signing.

## Stripe (full payments)

1. Create Products/Prices in Stripe Dashboard (AI monthly + human review one-time).
2. Env:

```bash
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_AI_MONTHLY=price_...
STRIPE_PRICE_HUMAN_REVIEW=price_...
PUBLIC_BASE_URL=https://your.domain
```

3. Webhook endpoint: `POST {PUBLIC_BASE_URL}/api/billing/webhook`  
   Events: `checkout.session.completed`, `customer.subscription.updated`,  
   `customer.subscription.deleted`, `invoice.paid`

4. APIs:
   - `POST /api/billing/checkout` — Checkout Session (or mock)
   - `POST /api/billing/portal` — Customer Portal
   - `POST /api/billing/cancel` — cancel at period end
   - `GET /api/billing/invoices/{user_id}` — history

Without Stripe keys the app uses **mock checkout** (activates plan immediately for demos).
