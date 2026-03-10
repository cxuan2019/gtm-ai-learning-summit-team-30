# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ADK-powered agent that generates personalized, photorealistic lifestyle advertisement images by combining customer data, product data, and brand assets using Gemini 3.1 Flash Image.

## Build & Run Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest -v

# Run a single test
uv run pytest tests/test_collect_customer_data.py::test_collect_known_customer -v

# Start FastAPI backend
uv run uvicorn server.app:app --reload --port 8000

# Start React frontend (separate terminal)
cd frontend && npm run dev

# Run via ADK Web UI instead
uv run adk web --port 8000

# Generate placeholder images
uv run python scripts/generate_placeholders.py

# Build frontend for production
cd frontend && npm run build
```

## Architecture

```
User (React @ :5173) → FastAPI (server/app.py @ :8000) → ADK Runner → Root Agent
                                                                         │
                                                          5 tools executed in sequence:
                                                          1. collect_customer_data
                                                          2. collect_product_data
                                                          3. collect_brand_assets
                                                          4. generate_image_prompt
                                                          5. generate_lifestyle_image
                                                                         │
                                                              Gemini 3.1 Flash Image API
```

**Root Agent** (`ad_personalization_agent/agent.py`): Single ADK `Agent` using `gemini-2.5-flash` as orchestrator. System instruction enforces strict 5-step tool calling sequence. Registered tools: 5 custom `FunctionTool`s + ADK's `load_artifacts`.

**Tools** (`ad_personalization_agent/tools/`): One file per tool. Data tools read from local JSON files in `ad_personalization_agent/data/`. The image generation tool (`generate_lifestyle_image.py`) calls `gemini-3.1-flash-image-preview` with multimodal inputs (customer photo + product image + logo + text prompt) and returns base64-encoded image.

**Server** (`server/app.py`): FastAPI with three endpoints: `GET /api/customers`, `GET /api/products`, `POST /api/generate`. The generate endpoint creates an ADK session, runs the agent via `Runner.run_async()`, extracts image data from tool results, and returns `{summary, image_base64, mime_type}`.

**Frontend** (`frontend/`): Vite + React + TypeScript. `ImageGenerator` component fetches dropdown data from `/api/customers` and `/api/products`, sends `POST /api/generate` with selected IDs, displays the base64 image as a hero shot. Vite proxy forwards `/api` to backend at `:8000`.

## Data Layer

All data is local JSON — no database required:
- `ad_personalization_agent/data/customers.json` — 3 customer profiles with browsing history, purchases, style preferences
- `ad_personalization_agent/data/products.json` — 4 products with descriptions and image paths
- `ad_personalization_agent/data/brand_assets.json` — Summit Athletics brand config (colors, slogan, logo path, tone)
- `ad_personalization_agent/data/assets/` — placeholder PNGs for customers, products, and brand logo

## Key Patterns

- **Tool return format**: All tools return `{"status": "success", ...}` or `{"status": "error", "message": "..."}`.
- **Image paths**: Tools return absolute filesystem paths (resolved from `DATA_DIR`). The image generation tool reads these paths to load image bytes.
- **Gemini client**: `generate_lifestyle_image.py` uses a `_get_genai_client()` factory for testability (mocked in tests).
- **ADK imports**: Using `google-adk>=1.26.0`. Key imports: `from google.adk import Runner`, `from google.adk.agents import Agent`, `from google.adk.sessions import InMemorySessionService`.

## Environment

Requires `.env` file (copy from `.env.example`):
- `GOOGLE_CLOUD_PROJECT` — GCP project ID
- `GOOGLE_CLOUD_LOCATION` — Region (default: us-central1)
- `GOOGLE_GENAI_USE_VERTEXAI` — Set to "1" for Vertex AI
