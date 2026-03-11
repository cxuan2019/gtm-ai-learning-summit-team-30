# Personalized Ad Generation Agent

ADK-powered agent that generates personalized lifestyle advertisement images
for Nike using Gemini 3.1 Flash Image. Combines customer data, product catalog,
and brand assets to create photorealistic, on-brand ad creatives.

## Setup

```bash
# Install Python dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud project

# Install frontend dependencies
cd frontend && npm install && cd ..
```

## Running

Start both backend and frontend:

```bash
# Terminal 1: FastAPI server
uv run uvicorn server.app:app --reload --port 8000

# Terminal 2: React dev server
cd frontend && npm run dev
```

Open http://localhost:5173

## Running via ADK Web UI

```bash
uv run adk web --port 8000
```

## Testing

```bash
uv run pytest -v
```

## Architecture

```
React UI (:5173) → FastAPI (:8000) → ADK Runner → Root Agent (gemini-2.5-flash)
                                                        │
                                         Tools executed in sequence:
                                         1. collect_customer_data
                                         2. collect_product_data
                                         3. collect_brand_assets
                                         4. generate_image_prompt
                                         5. generate_lifestyle_image → Gemini 3.1 Flash Image
```

## Data

- **Customers**: Chloe Vance, David Chen, Jamal Reynolds
- **Products**: Nike Air Force 1 '07, Nike Air Max 90, Nike Dunk Low Retro
- **Brand**: Nike — "Just Do It." slogan, black color scheme, Futura font

Customer photos, product images, and brand logo are sourced from `gtm-ai-learning-summit-team-30/`.
