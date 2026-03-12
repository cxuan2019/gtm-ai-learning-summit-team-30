# Session Notes — Personalized Ad Generation Agent

## Current State

**Branch**: `feat/ad-personalization-agent` on `https://github.com/cxuan2019/gtm-ai-learning-summit-team-30.git`

**Status**: Working end-to-end. The app generates personalized Nike lifestyle ad images via an ADK agent pipeline. All 14 tests pass.

### Uncommitted Changes

- `frontend/src/App.css` — logo size increased to 140px with negative margin for better rendering in the header banner
- `frontend/index.html` — title changed from "Summit Athletics" to "Nike"
- `ad_personalization_agent/data/images/` and `brand_asset/` — symlinks replaced with actual file copies
- `README.md` — updated to remove symlink references
- 3 new generated images in `assets/generated/` (untracked, excluded by .gitignore)

These changes need to be committed and pushed.

### PR Status

A PR has **not** been created yet. `gh` CLI is not installed. The PR can be created manually at:
https://github.com/cxuan2019/gtm-ai-learning-summit-team-30/pull/new/feat/ad-personalization-agent

Or by installing `gh` CLI and running `gh pr create`.

## Architecture Overview

```
React UI (:5173) → FastAPI (:8000) → ADK Runner → Root Agent (gemini-2.5-flash)
                                                        │
                                         1. collect_customer_data
                                         2. collect_product_data
                                         3. collect_brand_assets
                                         4. generate_image_prompt
                                         5. generate_lifestyle_image → Gemini 3.1 Flash Image
```

- **Root Agent**: `ad_personalization_agent/agent.py` — single ADK Agent with 5 FunctionTools + `load_artifacts`
- **Server**: `server/app.py` — FastAPI with endpoints: `GET /api/customers`, `GET /api/products`, `GET /api/brand`, `POST /api/generate`
- **Frontend**: `frontend/` — Vite + React + TypeScript, Nike-branded UI

## Key Technical Details

### Environment (.env)

```
GOOGLE_CLOUD_PROJECT="hybrid-vertex"
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI="1"
```

- `GOOGLE_CLOUD_LOCATION` must be `"global"` — `us-central1` causes 404 for `gemini-3.1-flash-image-preview`
- `load_dotenv()` is called at the top of `server/app.py` before any Google imports

### Known Gotchas

1. **Async API**: Use `client.aio.models.generate_content()`, NOT `client.models.generate_content_async()` (the latter doesn't exist in google-genai)
2. **Vertex AI client**: Must use `genai.Client(vertexai=True)` explicitly in `generate_lifestyle_image.py`
3. **Token overflow**: The image generation tool saves images to disk and returns only the file path — never return base64 data in tool responses or it will exceed the 1M token context limit
4. **ADK 1.26 EventActions**: No `tool_results` attribute — extract image data from `event.content.parts[].function_response.response` instead
5. **InMemoryArtifactService**: Required in the Runner because `load_artifacts` tool is registered
6. **Dev dependencies**: `pytest` is in optional `[dev]` extras — install with `uv sync --extra dev`

### Data

All data lives in `ad_personalization_agent/data/`:
- `customers.json` — 3 Nike customers (Chloe Vance, David Chen, Jamal Reynolds)
- `products.json` — 3 Nike shoes (Air Force 1, Air Max 90, Dunk Low Retro)
- `brand_assets.json` — Nike brand config (Just Do It., #000000, Futura font)
- `images/` — customer photos and product images (copied from gtm-ai-learning-summit-team-30)
- `brand_asset/` — Nike logo (copied from gtm-ai-learning-summit-team-30)

### Running Locally

```bash
# Terminal 1
uv run uvicorn server.app:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

Open http://localhost:5173

### Running Tests

```bash
uv sync --extra dev
uv run pytest -v
```

## Possible Next Steps

- Commit and push the remaining uncommitted changes
- Create a PR (install `gh` CLI or use the GitHub web UI)
- Consider removing the `gtm-ai-learning-summit-team-30/` directory since images are now copied into `data/`
- Add more customers or products
- Deploy to Cloud Run or another hosting platform
