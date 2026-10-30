# Sawalni tool-calling agent

Editable source in **[python/src](python/src)** and **[typescript/src](typescript/src)**. Pick either language. No generated bundle is needed.

## Setup

Create an API key at https://api.sawalni.com. Enable the models used below and add credits. Requests consume credits.

```sh
cp .env.example .env
# Edit .env and set SAWALNI_API_KEY.
```

### Python 3.11+

```sh
cd python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
set -a; . ../.env; set +a
python src/main.py What time is it?
```

### TypeScript / Node.js 24+

```sh
cd typescript
npm ci
npm run check
npm start -- What time is it?
```

## Extend it

Edit `src/main` for the entry point and `src/client` for API transport. The key stays in the backend process. Requests have a 120-second timeout. HTTP errors stop the flow. These are local developer starters. Add authentication, rate limits, persistence and deployment settings before exposing a service publicly.

API reference: https://api.sawalni.com/docs

Edit `src/agent` to add tools. The loop preserves tool call IDs, validates the allowlist and arguments, and stops after six model rounds. The example tools return UTC time and roll a six-sided die. It never executes model-generated code.

## Local HTTP backend

Python: `python src/server.py`. TypeScript: `npm run serve`. Both bind to `127.0.0.1:3000`. Keep these local adapters behind authenticated application routes when you deploy.

Send `POST /api/chat` with JSON `{ "text": "What time is it?" }`. The response is JSON `{ "reply": "..." }`.

```sh
curl http://127.0.0.1:3000/api/chat -H 'Content-Type: application/json' -d '{"text":"What time is it?"}'
```

## Tests

Run `python -m unittest discover -s tests` from `python/`. Run `npm test` from `typescript/`. Tests use synthetic model replies and do not spend credits.

Run `python tests/smoke.py` from the repository root with Python dependencies installed and Node.js 24 on PATH. It checks both languages against a local HTTP fixture. It does not call the paid API.
