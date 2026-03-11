# Personalized Ad Generation Agent

ADK-powered agent that generates personalized, photorealistic lifestyle advertisement images for Nike by combining customer data, product catalog, and brand assets using Gemini 3.1 Flash Image.

## Key Features

- **AI-Powered Image Generation** — Produces photorealistic lifestyle ads using Gemini 3.1 Flash Image with multimodal inputs (customer photo + product image + brand logo + text prompt)
- **Personalized to Each Customer** — Tailors ad creative based on browsing history, past purchases, and style preferences
- **Agentic Workflow** — Google ADK agent orchestrates a strict 5-step tool-calling sequence, from data collection through image generation
- **Full-Stack Application** — React frontend with Nike branding + FastAPI backend + ADK agent runtime
- **Brand-Consistent Output** — Automatically incorporates brand logo, slogan, colors, and font guidelines into every generated image

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

**Root Agent** (`ad_personalization_agent/agent.py`): A single ADK `Agent` using `gemini-2.5-flash` as the orchestrator. Its system instruction enforces the strict 5-step tool-calling sequence above. Registered tools include 5 custom `FunctionTool`s plus ADK's built-in `load_artifacts`.

**Server** (`server/app.py`): FastAPI backend with four endpoints:
- `GET /api/customers` — list customer profiles for the dropdown
- `GET /api/products` — list products for the dropdown
- `GET /api/brand` — return brand assets (logo URL, slogan, colors)
- `POST /api/generate` — run the agent and return the generated image as base64

**Frontend** (`frontend/`): Vite + React + TypeScript. Fetches brand assets to render Nike-branded UI, provides customer/product dropdowns, and displays the generated lifestyle image.

## Repository Structure

```
.
├── ad_personalization_agent/
│   ├── agent.py                    # Root ADK agent definition
│   ├── tools/
│   │   ├── collect_customer_data.py
│   │   ├── collect_product_data.py
│   │   ├── collect_brand_assets.py
│   │   ├── generate_image_prompt.py
│   │   └── generate_lifestyle_image.py
│   └── data/
│       ├── customers.json          # 3 customer profiles
│       ├── products.json           # 3 Nike products
│       ├── brand_assets.json       # Nike brand config
│       ├── images/                 # Customer photos and product images
│       └── brand_asset/            # Nike brand logo
├── server/
│   └── app.py                      # FastAPI backend
├── frontend/
│   └── src/
│       ├── App.tsx                 # Nike-branded shell
│       └── components/
│           └── ImageGenerator.tsx  # Main UI component
├── tests/                          # pytest test suite
├── pyproject.toml
└── .env.example
```

## Data

All data is local JSON — no database required.

**Customers** — 3 profiles with browsing history, purchase history, and photos:
| ID | Name | Style Signals |
|----|------|---------------|
| cust_001 | Chloe Vance | Running shoes, athletic apparel, yoga |
| cust_002 | David Chen | Basketball shoes, streetwear, hoodies |
| cust_003 | Jamal Reynolds | Skate shoes, vintage sneakers, casual wear |

**Products** — 3 Nike shoes:
| ID | Title | Style |
|----|-------|-------|
| prod_001 | Nike Air Force 1 '07 | Classic, Streetwear, Everyday |
| prod_002 | Nike Air Max 90 | Retro, Sporty, Bold |
| prod_003 | Nike Dunk Low Retro | Skate, Vintage, Casual |

**Brand** — Nike: "Just Do It." slogan, `#000000` color, Futura Condensed Extra Black font.

Customer photos, product images, and brand logo are stored in `ad_personalization_agent/data/`.

## Setup

```bash
# Install Python dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud project ID

# Install frontend dependencies
cd frontend && npm install && cd ..
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | — |
| `GOOGLE_CLOUD_LOCATION` | API region | `global` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Enable Vertex AI | `1` |

## Running

Start both backend and frontend:

```bash
# Terminal 1: FastAPI server
uv run uvicorn server.app:app --reload --port 8000

# Terminal 2: React dev server
cd frontend && npm run dev
```

Open http://localhost:5173

### Running via ADK Web UI

```bash
uv run adk web --port 8000
```

## Testing

```bash
uv run pytest -v
```
