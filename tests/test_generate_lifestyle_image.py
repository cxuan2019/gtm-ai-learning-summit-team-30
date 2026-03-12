from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ad_personalization_agent.tools.generate_lifestyle_image import (
    generate_lifestyle_image,
    _load_image_bytes,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data"


def test_load_image_bytes_valid(tmp_path):
    img_file = tmp_path / "test.png"
    img_file.write_bytes(b"\x89PNG fake image data")
    result = _load_image_bytes(str(img_file))
    assert result == b"\x89PNG fake image data"


def test_load_image_bytes_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        _load_image_bytes(str(tmp_path / "nonexistent" / "path.png"))


@pytest.mark.asyncio
async def test_generate_lifestyle_image_saves_to_disk(tmp_path):
    fake_image_bytes = b"\x89PNG generated image"

    mock_response = MagicMock()
    mock_part = MagicMock()
    mock_part.inline_data = MagicMock(data=fake_image_bytes, mime_type="image/png")
    mock_part.text = None
    mock_response.candidates = [MagicMock(content=MagicMock(parts=[mock_part]))]

    mock_client = MagicMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    with (
        patch(
            "ad_personalization_agent.tools.generate_lifestyle_image._get_genai_client",
            return_value=mock_client,
        ),
        patch(
            "ad_personalization_agent.tools.generate_lifestyle_image.OUTPUT_DIR",
            tmp_path,
        ),
    ):
        result = await generate_lifestyle_image(
            prompt="A photorealistic lifestyle image",
            customer_photo_path=str(DATA_DIR / "images" / "customer_1_1773176273591.png"),
            product_image_path=str(DATA_DIR / "images" / "product_1.png"),
            logo_image_path=str(DATA_DIR / "brand_asset" / "logo.png"),
        )

    assert result["status"] == "success"
    assert "image_path" in result
    # Verify the image was saved to disk
    saved_file = Path(result["image_path"])
    assert saved_file.exists()
    assert saved_file.read_bytes() == fake_image_bytes

    # Verify the API was called with the right model
    call_kwargs = mock_client.aio.models.generate_content.call_args
    assert call_kwargs.kwargs["model"] == "gemini-3.1-flash-image-preview"
