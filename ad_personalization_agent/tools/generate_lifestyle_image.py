"""Tool for generating photorealistic lifestyle images using Gemini."""

import logging
import uuid
from pathlib import Path

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gemini-3.1-flash-image-preview"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "assets" / "generated"


def _get_genai_client() -> genai.Client:
    """Returns a configured genai client for image generation."""
    return genai.Client(vertexai=True)


def _load_image_bytes(image_path: str) -> bytes:
    """Load image bytes from a local file path.

    Args:
        image_path: Absolute path to the image file.
    """
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")
    return path.read_bytes()


async def generate_lifestyle_image(
    prompt: str,
    customer_photo_path: str,
    product_image_path: str,
    logo_image_path: str,
) -> dict:
    """Generates a photorealistic lifestyle image using Gemini multimodal generation.

    Takes the crafted prompt along with reference images (customer photo,
    product image, brand logo) and generates a new composite lifestyle image.
    Saves the result to disk and returns the file path (not the image data)
    to avoid token overflow in the agent context.

    Args:
        prompt: The detailed image generation prompt.
        customer_photo_path: Path to the customer's photo.
        product_image_path: Path to the product image.
        logo_image_path: Path to the brand logo image.
    """
    try:
        customer_bytes = _load_image_bytes(customer_photo_path)
        product_bytes = _load_image_bytes(product_image_path)
        logo_bytes = _load_image_bytes(logo_image_path)
    except FileNotFoundError as e:
        return {"status": "error", "message": str(e)}

    contents = [
        types.Part.from_bytes(data=customer_bytes, mime_type="image/png"),
        types.Part.from_bytes(data=product_bytes, mime_type="image/png"),
        types.Part.from_bytes(data=logo_bytes, mime_type="image/png"),
        types.Part.from_text(text=prompt),
    ]

    client = _get_genai_client()

    try:
        response = await client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
    except Exception as e:
        logger.error("Image generation API call failed: %s", e)
        return {"status": "error", "message": f"API call failed: {e}"}

    # Extract generated image and save to disk
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.inline_data and part.inline_data.data:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                filename = f"{uuid.uuid4().hex}.png"
                output_path = OUTPUT_DIR / filename
                output_path.write_bytes(part.inline_data.data)
                return {
                    "status": "success",
                    "image_path": str(output_path),
                    "mime_type": part.inline_data.mime_type or "image/png",
                }

    return {"status": "error", "message": "No image was returned by the model."}
