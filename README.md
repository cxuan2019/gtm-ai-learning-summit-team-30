# Personalized Ad Generation Agent

ADK-powered agent that generates personalized lifestyle advertisement images
using Gemini 3.1 Flash Image.

## Setup

```bash
# Install Python dependencies
uv sync

# Generate placeholder images for development
uv run python scripts/generate_placeholders.py

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud project or API key

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
