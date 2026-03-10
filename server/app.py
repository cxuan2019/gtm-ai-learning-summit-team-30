"""FastAPI server bridging React frontend to ADK agent."""

import base64
import json
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from ad_personalization_agent.agent import root_agent

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data"

app = FastAPI(title="Ad Personalization Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
runner = Runner(
    app_name="ad_personalization",
    agent=root_agent,
    session_service=session_service,
    artifact_service=artifact_service,
)


def _load_json(filename: str) -> list | dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


@app.get("/api/customers")
async def list_customers():
    customers = _load_json("customers.json")
    return [{"id": c["id"], "name": c["name"]} for c in customers]


@app.get("/api/products")
async def list_products():
    products = _load_json("products.json")
    return [
        {"id": p["id"], "title": p["title"], "category": p["category"], "price": p["price"]}
        for p in products
    ]


class GenerateRequest(BaseModel):
    customer_id: str
    product_id: str


@app.post("/api/generate")
async def generate_image(req: GenerateRequest):
    try:
        session = await session_service.create_session(
            app_name="ad_personalization",
            user_id="demo_user",
        )

        message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Generate a personalized lifestyle ad image for customer '{req.customer_id}' featuring product '{req.product_id}'."
                )
            ],
        )

        final_text = ""
        image_base64 = None
        mime_type = "image/png"

        async for event in runner.run_async(
            session_id=session.id,
            user_id="demo_user",
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text
            # Check for tool results containing image data
            if event.actions and event.actions.tool_results:
                for tool_result in event.actions.tool_results:
                    for part in tool_result.content.parts:
                        if part.text:
                            try:
                                data = json.loads(part.text)
                                if isinstance(data, dict) and data.get("image_base64"):
                                    image_base64 = data["image_base64"]
                                    mime_type = data.get("mime_type", "image/png")
                            except (json.JSONDecodeError, TypeError):
                                pass

        return {
            "summary": final_text,
            "image_base64": image_base64,
            "mime_type": mime_type,
        }
    except Exception as e:
        logger.exception("Error generating image")
        raise HTTPException(status_code=500, detail=str(e))


# Serve generated images directory
GENERATED_DIR = DATA_DIR / "assets"
app.mount("/assets", StaticFiles(directory=str(GENERATED_DIR)), name="assets")
