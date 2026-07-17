# OmniRoute → WniosekPL

WniosekPL uses [OmniRoute](https://github.com/diegosouzapw/OmniRoute) as the **AI gateway**:
one OpenAI-compatible endpoint, 200+ providers, free tiers, auto-fallback.

We do **not** vendor the whole OmniRoute monorepo (Next.js / Electron).
We run it as a sidecar and call `POST /v1/chat/completions`.

## Why

| Without OmniRoute | With OmniRoute |
|-------------------|----------------|
| One paid OpenAI key | Free + paid providers, auto-fallback |
| Hard limit / outage = dead AI | Cascade across Groq, OpenRouter free, Gemini, … |
| Manual model picks | `model: auto` smart routing |

## Quick start

```bash
# 1) Start gateway
bash scripts/start_omniroute.sh
# Dashboard: http://127.0.0.1:20128

# 2) In dashboard: Providers → connect a FREE provider (e.g. OpenCode Free / Kiro)
# 3) Endpoints → copy API key into .env:

OMNIROUTE_ENABLED=true
OMNIROUTE_BASE_URL=http://127.0.0.1:20128/v1
OMNIROUTE_API_KEY=your_key_from_dashboard
OMNIROUTE_MODEL=auto

# Optional direct fallbacks (used if OmniRoute is down):
GROQ_API_KEY=
OPENROUTER_API_KEY=
OPENAI_API_KEY=

# 4) Restart WniosekPL API + bot
```

Or everything via Compose:

```bash
docker compose up -d
docker compose --profile bot up -d
```

## How WniosekPL routes LLM calls

Order in `src/llm.py`:

1. **OmniRoute** (`OMNIROUTE_BASE_URL`) — preferred
2. **OpenAI** direct (if `OPENAI_API_KEY` + api.openai.com)
3. **Groq** free/cheap (`GROQ_API_KEY`)
4. **OpenRouter** free pool (`OPENROUTER_API_KEY`, model `openrouter/free`)

If none work → rule-based + knowledge answers (product still works).

## Health

`GET /health` and `GET /api/meta` expose:

- `llm.omniroute_enabled`
- `llm.fallback_chain`
- `llm.gateway`

## License note

OmniRoute is MIT. Keep attribution when redistributing their software/images.
WniosekPL only depends on their HTTP API / Docker image.
