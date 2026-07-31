# Third-party software

## OmniRoute

- Project: [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute)
- License: MIT
- Role in WniosekPL: optional OpenAI-compatible AI gateway (Docker image / npm package)
- Integration: `src/llm.py`, `docker-compose.yml`, `scripts/start_omniroute.sh`, `docs/OMNIROUTE.md`

WniosekPL does not redistribute OmniRoute source code. Run the official image or `npx omniroute` locally, then point `OMNIROUTE_BASE_URL` at `/v1`.
