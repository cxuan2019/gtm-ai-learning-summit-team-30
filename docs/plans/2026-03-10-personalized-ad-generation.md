# Personalized Ad Generation Agent - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `executing-plans` skill to implement this plan task-by-task.

**Goal:** Build an ADK-powered agent with a React frontend that generates personalized, photorealistic lifestyle images by combining customer data, product data, and brand assets using Gemini 3.1 Flash Image.

**Architecture:** A single ADK root agent orchestrates five function tools (collect customer data, collect product data, collect brand assets, generate image prompt, generate lifestyle image). A FastAPI server runs the agent programmatically and exposes REST endpoints for a React frontend. Local JSON files and static image assets serve as the data layer. The agent uses `load_artifacts` from ADK and a custom `generate_lifestyle_image` tool that calls `gemini-3.1-flash-image-preview` with multi-modal inputs (prompt + customer photo + product image + logo).

**Tech Stack:** Python 3.12+, google-adk, google-genai, FastAPI, uvicorn, React (Vite + TypeScript), uv (build system), pytest

---

## Project Structure

```
hack/
├── ad_personalization_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── collect_customer_data.py
│   │   ├── collect_product_data.py
│   │   ├── collect_brand_assets.py
│   │   ├── generate_image_prompt.py
│   │   └── generate_lifestyle_image.py
│   └── data/
│       ├── customers.json
│       ├── products.json
│       ├── brand_assets.json
│       └── assets/
│           ├── customers/
│           │   ├── alex_morgan.png
│           │   └── jordan_patel.png
│           ├── products/
│           │   ├── trail_running_shoe.png
│           │   └── insulated_water_bottle.png
│           └── brand/
│               └── logo.png
├── server/
│   ├── __init__.py
│   └── app.py
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── App.css
│       └── components/
│           └── ImageGenerator.tsx
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_collect_customer_data.py
│   ├── test_collect_product_data.py
│   ├── test_collect_brand_assets.py
│   ├── test_generate_image_prompt.py
│   ├── test_generate_lifestyle_image.py
│   └── test_server.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

### Task 1: Project Scaffolding

**Files:**

- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `ad_personalization_agent/__init__.py`
- Create: `ad_personalization_agent/tools/__init__.py`
- Create: `server/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

**Step 1: Create `pyproject.toml`**

```toml
[project]
name = "ad-personalization-agent"
version = "0.1.0"
description = "Personalized Ad Generation Agent using ADK and Gemini"
requires-python = ">=3.12"
dependencies = [
    "google-adk>=1.18.0",
    "google-genai>=1.49.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.34.0",
    "python-dotenv>=1.1.0",
    "pillow>=11.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.4.0",
    "pytest-asyncio>=0.23.7",
    "httpx>=0.28.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["ad_personalization_agent", "server"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 2: Create `.env.example`**

```bash
# Google Cloud / Vertex AI
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI="1"

# Or use API key directly
# GOOGLE_API_KEY="your-api-key"
```

**Step 3: Create `.gitignore`**

```
__pycache__/
*.pyc
.env
.venv/
dist/
*.egg-info/
node_modules/
frontend/dist/
.pytest_cache/
```

**Step 4: Create `ad_personalization_agent/__init__.py`**

```python
from . import agent
```

**Step 5: Create `ad_personalization_agent/tools/__init__.py`**

```python
from .collect_customer_data import collect_customer_data
from .collect_product_data import collect_product_data
from .collect_brand_assets import collect_brand_assets
from .generate_image_prompt import generate_image_prompt
from .generate_lifestyle_image import generate_lifestyle_image
```

**Step 6: Create `server/__init__.py`**

```python
```

**Step 7: Create `tests/__init__.py`**

```python
```

**Step 8: Create `tests/conftest.py`**

```python
import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data"


@pytest.fixture
def customers():
    with open(DATA_DIR / "customers.json") as f:
        return json.load(f)


@pytest.fixture
def products():
    with open(DATA_DIR / "products.json") as f:
        return json.load(f)


@pytest.fixture
def brand_assets():
    with open(DATA_DIR / "brand_assets.json") as f:
        return json.load(f)
```

**Step 9: Install dependencies**

Run: `uv sync`
Expected: Dependencies installed successfully

**Step 10: Commit**

```bash
git init
git add pyproject.toml .env.example .gitignore ad_personalization_agent/__init__.py ad_personalization_agent/tools/__init__.py server/__init__.py tests/__init__.py tests/conftest.py
git commit -m "feat: project scaffolding with uv, ADK, FastAPI deps"
```

---

### Task 2: Sample Data Files

**Files:**

- Create: `ad_personalization_agent/data/customers.json`
- Create: `ad_personalization_agent/data/products.json`
- Create: `ad_personalization_agent/data/brand_assets.json`
- Create: `ad_personalization_agent/data/assets/customers/.gitkeep`
- Create: `ad_personalization_agent/data/assets/products/.gitkeep`
- Create: `ad_personalization_agent/data/assets/brand/.gitkeep`

**Step 1: Create `ad_personalization_agent/data/customers.json`**

```json
[
  {
    "id": "cust_001",
    "name": "Alex Morgan",
    "photo": "assets/customers/alex_morgan.png",
    "browsing_history": [
      "trail running shoes",
      "hiking gear",
      "outdoor fitness trackers",
      "camping equipment"
    ],
    "past_purchases": [
      {"product": "Ultralight Hiking Boots", "category": "footwear", "date": "2025-11-15"},
      {"product": "Quick-Dry Trail Shorts", "category": "apparel", "date": "2025-09-22"},
      {"product": "GPS Running Watch", "category": "electronics", "date": "2025-07-10"}
    ],
    "style_preferences": {
      "dominant_activity": "trail running",
      "preferred_environment": "mountain trails",
      "aesthetic": "rugged outdoor"
    }
  },
  {
    "id": "cust_002",
    "name": "Jordan Patel",
    "photo": "assets/customers/jordan_patel.png",
    "browsing_history": [
      "yoga mats",
      "meditation cushions",
      "organic protein powder",
      "studio lighting"
    ],
    "past_purchases": [
      {"product": "Premium Yoga Mat", "category": "fitness", "date": "2025-12-01"},
      {"product": "Bamboo Water Bottle", "category": "accessories", "date": "2025-10-18"},
      {"product": "Organic Cotton Hoodie", "category": "apparel", "date": "2025-08-05"}
    ],
    "style_preferences": {
      "dominant_activity": "yoga and wellness",
      "preferred_environment": "studio and home",
      "aesthetic": "minimalist zen"
    }
  },
  {
    "id": "cust_003",
    "name": "Sam Rivera",
    "photo": "assets/customers/sam_rivera.png",
    "browsing_history": [
      "road cycling jerseys",
      "carbon fiber bikes",
      "cycling computers",
      "energy gels"
    ],
    "past_purchases": [
      {"product": "Aero Cycling Jersey", "category": "apparel", "date": "2025-11-28"},
      {"product": "Clipless Pedals Pro", "category": "equipment", "date": "2025-09-14"},
      {"product": "Insulated Water Bottle", "category": "accessories", "date": "2025-06-30"}
    ],
    "style_preferences": {
      "dominant_activity": "road cycling",
      "preferred_environment": "open roads and countryside",
      "aesthetic": "sleek performance"
    }
  }
]
```

**Step 2: Create `ad_personalization_agent/data/products.json`**

```json
[
  {
    "id": "prod_001",
    "title": "Apex Trail Runner X1",
    "description": "Ultra-lightweight trail running shoe with Vibram outsole, responsive midsole cushioning, and waterproof Gore-Tex upper. Built for rugged mountain terrain with superior grip and ankle support.",
    "category": "footwear",
    "image": "assets/products/trail_running_shoe.png",
    "price": 189.99
  },
  {
    "id": "prod_002",
    "title": "ThermoCore Insulated Bottle",
    "description": "Double-wall vacuum insulated stainless steel water bottle. Keeps drinks cold for 24 hours or hot for 12. Leak-proof sport cap with one-hand operation. 750ml capacity.",
    "category": "accessories",
    "image": "assets/products/insulated_water_bottle.png",
    "price": 44.99
  },
  {
    "id": "prod_003",
    "title": "FlexForm Pro Yoga Mat",
    "description": "Premium 6mm natural rubber yoga mat with alignment markers. Non-slip surface on both sides, antimicrobial coating, and carrying strap included. Eco-friendly and biodegradable.",
    "category": "fitness",
    "image": "assets/products/yoga_mat.png",
    "price": 89.99
  },
  {
    "id": "prod_004",
    "title": "AeroVent Cycling Jersey",
    "description": "Race-fit cycling jersey with 3-pocket rear panel, full-length YKK zipper, and laser-cut ventilation. UPF 50+ sun protection. Italian-made fabric with moisture-wicking technology.",
    "category": "apparel",
    "image": "assets/products/cycling_jersey.png",
    "price": 129.99
  }
]
```

**Step 3: Create `ad_personalization_agent/data/brand_assets.json`**

```json
{
  "brand_name": "Summit Athletics",
  "slogan": "Rise Above. Push Beyond.",
  "description": "Summit Athletics is a premium outdoor and fitness brand that empowers athletes to conquer their limits. We blend cutting-edge performance technology with sustainable materials.",
  "colors": {
    "primary": "#1B4D3E",
    "secondary": "#E8A838",
    "accent": "#F5F5F5"
  },
  "font": "Montserrat Bold",
  "logo": "assets/brand/logo.png",
  "tone": "Confident, aspirational, and grounded in nature. Speaks to athletes who see outdoor fitness as a lifestyle, not just a hobby."
}
```

**Step 4: Create `.gitkeep` files for asset directories**

```bash
mkdir -p ad_personalization_agent/data/assets/customers
mkdir -p ad_personalization_agent/data/assets/products
mkdir -p ad_personalization_agent/data/assets/brand
touch ad_personalization_agent/data/assets/customers/.gitkeep
touch ad_personalization_agent/data/assets/products/.gitkeep
touch ad_personalization_agent/data/assets/brand/.gitkeep
```

**Step 5: Generate placeholder images**

Create a script `scripts/generate_placeholders.py` that uses PIL to generate simple colored placeholder PNGs for each customer, product, and logo so tools can load them during development and testing:

```python
"""Generate placeholder images for development."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data" / "assets"

PLACEHOLDERS = {
    "customers/alex_morgan.png": ("Alex M.", "#4A90D9", (256, 256)),
    "customers/jordan_patel.png": ("Jordan P.", "#7B68EE", (256, 256)),
    "customers/sam_rivera.png": ("Sam R.", "#E07C4F", (256, 256)),
    "products/trail_running_shoe.png": ("Trail Shoe", "#2E8B57", (512, 512)),
    "products/insulated_water_bottle.png": ("Bottle", "#4682B4", (512, 512)),
    "products/yoga_mat.png": ("Yoga Mat", "#9370DB", (512, 512)),
    "products/cycling_jersey.png": ("Jersey", "#DC143C", (512, 512)),
    "brand/logo.png": ("Summit Athletics", "#1B4D3E", (512, 256)),
}


def generate():
    for path, (label, color, size) in PLACEHOLDERS.items():
        img = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(img)
        draw.text((size[0] // 2, size[1] // 2), label, fill="white", anchor="mm")
        out = ASSETS / path
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        print(f"Created {out}")


if __name__ == "__main__":
    generate()
```

Run: `uv run python scripts/generate_placeholders.py`

**Step 6: Commit**

```bash
git add ad_personalization_agent/data/ scripts/generate_placeholders.py
git commit -m "feat: add sample customer, product, and brand data with placeholders"
```

---

### Task 3: Customer Data Collection Tool

**Files:**

- Create: `ad_personalization_agent/tools/collect_customer_data.py`
- Create: `tests/test_collect_customer_data.py`

**Step 1: Write the failing test**

```python
# tests/test_collect_customer_data.py
import pytest
from ad_personalization_agent.tools.collect_customer_data import collect_customer_data


def test_collect_known_customer():
    result = collect_customer_data(customer_id="cust_001")
    assert result["status"] == "success"
    assert result["customer"]["name"] == "Alex Morgan"
    assert "past_purchases" in result["customer"]
    assert "browsing_history" in result["customer"]
    assert "style_preferences" in result["customer"]
    assert "photo_path" in result["customer"]


def test_collect_unknown_customer():
    result = collect_customer_data(customer_id="cust_999")
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()


def test_inferred_style_affinity():
    result = collect_customer_data(customer_id="cust_001")
    assert result["customer"]["style_preferences"]["dominant_activity"] == "trail running"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_collect_customer_data.py -v`
Expected: FAIL with ImportError or ModuleNotFoundError

**Step 3: Write minimal implementation**

```python
# ad_personalization_agent/tools/collect_customer_data.py
"""Tool for collecting and analyzing customer profile data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def collect_customer_data(customer_id: str) -> dict:
    """Collects customer profile data including browsing history and purchase patterns.

    Args:
        customer_id: The unique identifier of the customer (e.g., 'cust_001').
    """
    with open(DATA_DIR / "customers.json") as f:
        customers = json.load(f)

    for customer in customers:
        if customer["id"] == customer_id:
            photo_path = str(DATA_DIR / customer["photo"])
            return {
                "status": "success",
                "customer": {
                    "id": customer["id"],
                    "name": customer["name"],
                    "photo_path": photo_path,
                    "browsing_history": customer["browsing_history"],
                    "past_purchases": customer["past_purchases"],
                    "style_preferences": customer["style_preferences"],
                },
            }

    return {"status": "error", "message": f"Customer '{customer_id}' not found."}
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_collect_customer_data.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add ad_personalization_agent/tools/collect_customer_data.py tests/test_collect_customer_data.py
git commit -m "feat: add collect_customer_data tool with tests"
```

---

### Task 4: Product Data Collection Tool

**Files:**

- Create: `ad_personalization_agent/tools/collect_product_data.py`
- Create: `tests/test_collect_product_data.py`

**Step 1: Write the failing test**

```python
# tests/test_collect_product_data.py
from ad_personalization_agent.tools.collect_product_data import collect_product_data


def test_collect_known_product():
    result = collect_product_data(product_id="prod_001")
    assert result["status"] == "success"
    assert result["product"]["title"] == "Apex Trail Runner X1"
    assert "description" in result["product"]
    assert "image_path" in result["product"]


def test_collect_unknown_product():
    result = collect_product_data(product_id="prod_999")
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_collect_product_data.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# ad_personalization_agent/tools/collect_product_data.py
"""Tool for collecting product catalog data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def collect_product_data(product_id: str) -> dict:
    """Fetches product catalog data including name, description, and image path.

    Args:
        product_id: The unique identifier of the product (e.g., 'prod_001').
    """
    with open(DATA_DIR / "products.json") as f:
        products = json.load(f)

    for product in products:
        if product["id"] == product_id:
            image_path = str(DATA_DIR / product["image"])
            return {
                "status": "success",
                "product": {
                    "id": product["id"],
                    "title": product["title"],
                    "description": product["description"],
                    "category": product["category"],
                    "image_path": image_path,
                    "price": product["price"],
                },
            }

    return {"status": "error", "message": f"Product '{product_id}' not found."}
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_collect_product_data.py -v`
Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add ad_personalization_agent/tools/collect_product_data.py tests/test_collect_product_data.py
git commit -m "feat: add collect_product_data tool with tests"
```

---

### Task 5: Brand Assets Collection Tool

**Files:**

- Create: `ad_personalization_agent/tools/collect_brand_assets.py`
- Create: `tests/test_collect_brand_assets.py`

**Step 1: Write the failing test**

```python
# tests/test_collect_brand_assets.py
from ad_personalization_agent.tools.collect_brand_assets import collect_brand_assets


def test_collect_brand_assets():
    result = collect_brand_assets()
    assert result["status"] == "success"
    brand = result["brand"]
    assert brand["brand_name"] == "Summit Athletics"
    assert brand["slogan"] == "Rise Above. Push Beyond."
    assert "logo_path" in brand
    assert "colors" in brand
    assert "font" in brand
    assert "tone" in brand
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_collect_brand_assets.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# ad_personalization_agent/tools/collect_brand_assets.py
"""Tool for collecting brand asset data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def collect_brand_assets() -> dict:
    """Fetches the brand asset library including logo, colors, slogan, and tone guidelines."""
    with open(DATA_DIR / "brand_assets.json") as f:
        brand = json.load(f)

    logo_path = str(DATA_DIR / brand["logo"])
    return {
        "status": "success",
        "brand": {
            "brand_name": brand["brand_name"],
            "slogan": brand["slogan"],
            "description": brand["description"],
            "colors": brand["colors"],
            "font": brand["font"],
            "logo_path": logo_path,
            "tone": brand["tone"],
        },
    }
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_collect_brand_assets.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add ad_personalization_agent/tools/collect_brand_assets.py tests/test_collect_brand_assets.py
git commit -m "feat: add collect_brand_assets tool with tests"
```

---

### Task 6: Image Prompt Generation Tool

**Files:**

- Create: `ad_personalization_agent/tools/generate_image_prompt.py`
- Create: `tests/test_generate_image_prompt.py`

**Step 1: Write the failing test**

```python
# tests/test_generate_image_prompt.py
from ad_personalization_agent.tools.generate_image_prompt import generate_image_prompt


def test_generate_prompt_contains_key_elements():
    result = generate_image_prompt(
        customer_name="Alex Morgan",
        style_affinity="trail running",
        preferred_environment="mountain trails",
        aesthetic="rugged outdoor",
        product_title="Apex Trail Runner X1",
        product_description="Ultra-lightweight trail running shoe with Vibram outsole",
        brand_name="Summit Athletics",
        brand_slogan="Rise Above. Push Beyond.",
        brand_colors="primary: #1B4D3E, secondary: #E8A838",
        brand_tone="Confident, aspirational, and grounded in nature",
    )
    assert result["status"] == "success"
    prompt = result["prompt"]
    # Prompt must reference the product
    assert "Apex Trail Runner X1" in prompt
    # Prompt must reference the environment
    assert "mountain" in prompt.lower() or "trail" in prompt.lower()
    # Prompt must reference brand elements
    assert "Summit Athletics" in prompt
    assert "Rise Above. Push Beyond." in prompt
    # Prompt must request photorealistic style
    assert "photorealistic" in prompt.lower()


def test_generate_prompt_includes_logo_instruction():
    result = generate_image_prompt(
        customer_name="Jordan Patel",
        style_affinity="yoga and wellness",
        preferred_environment="studio and home",
        aesthetic="minimalist zen",
        product_title="FlexForm Pro Yoga Mat",
        product_description="Premium 6mm natural rubber yoga mat",
        brand_name="Summit Athletics",
        brand_slogan="Rise Above. Push Beyond.",
        brand_colors="primary: #1B4D3E, secondary: #E8A838",
        brand_tone="Confident, aspirational",
    )
    prompt = result["prompt"]
    assert "logo" in prompt.lower()
    assert "slogan" in prompt.lower()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_generate_image_prompt.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# ad_personalization_agent/tools/generate_image_prompt.py
"""Tool for crafting a detailed image generation prompt from customer/product/brand data."""


def generate_image_prompt(
    customer_name: str,
    style_affinity: str,
    preferred_environment: str,
    aesthetic: str,
    product_title: str,
    product_description: str,
    brand_name: str,
    brand_slogan: str,
    brand_colors: str,
    brand_tone: str,
) -> dict:
    """Crafts a detailed, on-brand prompt for photorealistic lifestyle image generation.

    Combines customer style preferences, product details, and brand guidelines
    into a single image generation prompt.

    Args:
        customer_name: Name of the target customer.
        style_affinity: Customer's dominant activity or style (e.g., 'trail running').
        preferred_environment: Customer's preferred visual setting (e.g., 'mountain trails').
        aesthetic: Customer's visual aesthetic preference (e.g., 'rugged outdoor').
        product_title: Name of the product to feature.
        product_description: Text description of the product.
        brand_name: Name of the brand.
        brand_slogan: Brand slogan to include in the image.
        brand_colors: Brand color palette as a string.
        brand_tone: Brand voice/tone description.
        brand_font: Brand font name.
    """
    prompt = (
        f"Generate a photorealistic lifestyle advertisement image.\n\n"
        f"SCENE: A {aesthetic} scene set in {preferred_environment}. "
        f"The mood is {brand_tone.lower()}.\n\n"
        f"PRODUCT: Prominently feature the '{product_title}' — {product_description}. "
        f"The product should be the focal point, shown in use within the lifestyle scene.\n\n"
        f"PERSON: Include a person who embodies the {style_affinity} lifestyle, "
        f"naturally interacting with the product in the scene.\n\n"
        f"BRANDING: Include the {brand_name} logo in the corner of the image. "
        f"Display the slogan '{brand_slogan}' as elegant text overlay. "
        f"Use the brand color palette ({brand_colors}) for any graphic elements.\n\n"
        f"STYLE: Photorealistic, high-resolution, professional advertising photography. "
        f"Natural lighting, shallow depth of field on the product. "
        f"The image should feel aspirational and authentic to the {style_affinity} community."
    )
    return {"status": "success", "prompt": prompt}
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_generate_image_prompt.py -v`
Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add ad_personalization_agent/tools/generate_image_prompt.py tests/test_generate_image_prompt.py
git commit -m "feat: add generate_image_prompt tool with tests"
```

---

### Task 7: Lifestyle Image Generation Tool

**Files:**

- Create: `ad_personalization_agent/tools/generate_lifestyle_image.py`
- Create: `tests/test_generate_lifestyle_image.py`

**Step 1: Write the failing test**

This tool calls the Gemini API, so tests mock the API client. The test validates that the tool correctly assembles multi-modal content (prompt + images) and handles the API response.

```python
# tests/test_generate_lifestyle_image.py
import base64
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ad_personalization_agent.tools.generate_lifestyle_image import (
    generate_lifestyle_image,
    _load_image_bytes,
)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data" / "assets"


def test_load_image_bytes_valid(tmp_path):
    img_file = tmp_path / "test.png"
    img_file.write_bytes(b"\x89PNG fake image data")
    result = _load_image_bytes(str(img_file))
    assert result == b"\x89PNG fake image data"


def test_load_image_bytes_missing():
    with pytest.raises(FileNotFoundError):
        _load_image_bytes("/nonexistent/path.png")


@pytest.mark.asyncio
async def test_generate_lifestyle_image_calls_api():
    fake_image_bytes = b"\x89PNG generated image"

    mock_response = MagicMock()
    mock_part = MagicMock()
    mock_part.inline_data = MagicMock(data=fake_image_bytes, mime_type="image/png")
    mock_part.text = None
    mock_response.candidates = [MagicMock(content=MagicMock(parts=[mock_part]))]

    mock_client = MagicMock()
    mock_client.models.generate_content_async = AsyncMock(return_value=mock_response)

    with patch(
        "ad_personalization_agent.tools.generate_lifestyle_image._get_genai_client",
        return_value=mock_client,
    ):
        result = await generate_lifestyle_image(
            prompt="A photorealistic lifestyle image",
            customer_photo_path=str(ASSETS_DIR / "customers" / "alex_morgan.png"),
            product_image_path=str(ASSETS_DIR / "products" / "trail_running_shoe.png"),
            logo_image_path=str(ASSETS_DIR / "brand" / "logo.png"),
        )

    assert result["status"] == "success"
    assert "image_base64" in result
    decoded = base64.b64decode(result["image_base64"])
    assert decoded == fake_image_bytes

    # Verify the API was called with the right model
    call_kwargs = mock_client.models.generate_content_async.call_args
    assert call_kwargs.kwargs["model"] == "gemini-3.1-flash-image-preview"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_generate_lifestyle_image.py -v`
Expected: FAIL with ImportError

**Step 3: Write minimal implementation**

```python
# ad_personalization_agent/tools/generate_lifestyle_image.py
"""Tool for generating photorealistic lifestyle images using Gemini."""

import base64
import logging
from pathlib import Path

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gemini-3.1-flash-image-preview"


def _get_genai_client() -> genai.Client:
    """Returns a configured genai client."""
    return genai.Client()


def _load_image_bytes(image_path: str) -> bytes:
    """Load image bytes from a local file path.

    Args:
        image_path: Absolute path to the image file.
    """
    path = Path(image_path)
    if not path.exists():
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
        response = await client.models.generate_content_async(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
    except Exception as e:
        logger.error("Image generation API call failed: %s", e)
        return {"status": "error", "message": f"API call failed: {e}"}

    # Extract generated image from response
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.inline_data and part.inline_data.data:
                image_b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                return {
                    "status": "success",
                    "image_base64": image_b64,
                    "mime_type": part.inline_data.mime_type or "image/png",
                }

    return {"status": "error", "message": "No image was returned by the model."}
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_generate_lifestyle_image.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add ad_personalization_agent/tools/generate_lifestyle_image.py tests/test_generate_lifestyle_image.py
git commit -m "feat: add generate_lifestyle_image tool with Gemini 3.1 Flash Image"
```

---

### Task 8: ADK Agent Configuration

**Files:**

- Create: `ad_personalization_agent/agent.py`

**Step 1: Write the agent**

```python
# ad_personalization_agent/agent.py
"""Personalized Ad Generation Agent using ADK."""

from google.adk.agents import Agent
from google.adk.tools import load_artifacts

from .tools.collect_brand_assets import collect_brand_assets
from .tools.collect_customer_data import collect_customer_data
from .tools.collect_product_data import collect_product_data
from .tools.generate_image_prompt import generate_image_prompt
from .tools.generate_lifestyle_image import generate_lifestyle_image

SYSTEM_INSTRUCTION = """You are a Personalized Ad Generation Assistant for Summit Athletics.

Your job is to generate photorealistic lifestyle advertisement images that are
personalized for a specific customer and product. You must follow these steps
in order:

## Step 1: Collect Customer Data
Use the `collect_customer_data` tool with the provided customer_id.
Analyze their past purchases and browsing history to understand their dominant
style affinity, preferred environment, and aesthetic preferences.

## Step 2: Collect Product Data
Use the `collect_product_data` tool with the provided product_id.
Retrieve the product title, description, category, and image path.

## Step 3: Collect Brand Assets
Use the `collect_brand_assets` tool to fetch the brand logo, slogan, colors,
font, and tone guidelines.

## Step 4: Generate Image Prompt
Use the `generate_image_prompt` tool to craft a detailed, on-brand prompt for
the image generator. Pass in the customer style preferences, product details,
and brand guidelines gathered in the previous steps.

## Step 5: Generate Lifestyle Image
Use the `generate_lifestyle_image` tool with the prompt from Step 4, along
with the customer photo path, product image path, and logo image path.
This will generate a photorealistic lifestyle image using Gemini.

## Important Rules
- Always execute steps 1-5 in order.
- Never skip a step or make assumptions about data — always use the tools.
- If any tool returns an error status, report the error and stop.
- After generating the image, present a summary of what was generated including
  the customer name, product, and a description of the scene.
"""

root_agent = Agent(
    name="ad_personalization_agent",
    model="gemini-2.5-flash",
    description="Generates personalized lifestyle advertisement images by combining customer, product, and brand data.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        collect_customer_data,
        collect_product_data,
        collect_brand_assets,
        generate_image_prompt,
        generate_lifestyle_image,
        load_artifacts,
    ],
)
```

**Step 2: Verify the agent loads via ADK CLI**

Run: `cd /usr/local/google/home/jordantotten/antigravity/hack && uv run adk run ad_personalization_agent --help`
Expected: ADK recognizes the agent (no import errors)

**Step 3: Commit**

```bash
git add ad_personalization_agent/agent.py
git commit -m "feat: configure root ADK agent with 5 tools and system instruction"
```

---

### Task 9: FastAPI Server

**Files:**

- Create: `server/app.py`
- Create: `tests/test_server.py`

**Step 1: Write the failing test**

```python
# tests/test_server.py
import pytest
from httpx import ASGITransport, AsyncClient

from server.app import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_list_customers(client):
    resp = await client.get("/api/customers")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    assert data[0]["id"] == "cust_001"
    assert "name" in data[0]


@pytest.mark.asyncio
async def test_list_products(client):
    resp = await client.get("/api/products")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2
    assert data[0]["id"] == "prod_001"
    assert "title" in data[0]


@pytest.mark.asyncio
async def test_generate_missing_fields(client):
    resp = await client.post("/api/generate", json={})
    assert resp.status_code == 422
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_server.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# server/app.py
"""FastAPI server bridging React frontend to ADK agent."""

import base64
import json
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.adk import Runner
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
runner = Runner(
    app_name="ad_personalization",
    agent=root_agent,
    session_service=session_service,
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


# Serve generated images directory
GENERATED_DIR = DATA_DIR / "assets"
app.mount("/assets", StaticFiles(directory=str(GENERATED_DIR)), name="assets")
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_server.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add server/app.py tests/test_server.py
git commit -m "feat: add FastAPI server with customer/product/generate endpoints"
```

---

### Task 10: React Frontend

**Files:**

- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/App.css`
- Create: `frontend/src/components/ImageGenerator.tsx`

**Step 1: Create `frontend/package.json`**

```json
{
  "name": "ad-personalization-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.4.0",
    "typescript": "^5.7.0",
    "vite": "^6.0.0"
  }
}
```

**Step 2: Create `frontend/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

**Step 3: Create `frontend/vite.config.ts`**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
```

**Step 4: Create `frontend/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Summit Athletics - Ad Personalization</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Step 5: Create `frontend/src/main.tsx`**

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Step 6: Create `frontend/src/App.tsx`**

```tsx
import ImageGenerator from "./components/ImageGenerator";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Summit Athletics</h1>
        <p className="subtitle">Personalized Ad Generation</p>
      </header>
      <main>
        <ImageGenerator />
      </main>
    </div>
  );
}

export default App;
```

**Step 7: Create `frontend/src/App.css`**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  background: #f5f5f5;
  color: #1a1a1a;
}

.app {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}

.app-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #1b4d3e;
  color: white;
  border-radius: 12px;
}

.app-header h1 {
  font-size: 2rem;
}

.subtitle {
  opacity: 0.85;
  margin-top: 0.25rem;
}

.generator-panel {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.control-group {
  flex: 1;
  min-width: 200px;
}

.control-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1b4d3e;
}

.control-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
}

.generate-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
  background: #e8a838;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.generate-btn:hover:not(:disabled) {
  background: #d4952e;
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.result {
  margin-top: 2rem;
  text-align: center;
}

.result img {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.summary {
  margin-top: 1rem;
  padding: 1rem;
  background: #f0f7f4;
  border-radius: 8px;
  text-align: left;
  white-space: pre-wrap;
}

.error {
  color: #c0392b;
  margin-top: 1rem;
  padding: 1rem;
  background: #fde8e8;
  border-radius: 8px;
}

.loading {
  margin-top: 2rem;
  text-align: center;
  color: #1b4d3e;
  font-weight: 600;
}
```

**Step 8: Create `frontend/src/components/ImageGenerator.tsx`**

```tsx
import { useEffect, useState } from "react";

interface Customer {
  id: string;
  name: string;
}

interface Product {
  id: string;
  title: string;
  category: string;
  price: number;
}

interface GenerateResult {
  summary: string;
  image_base64: string | null;
  mime_type: string;
}

function ImageGenerator() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [selectedProduct, setSelectedProduct] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/customers")
      .then((r) => r.json())
      .then(setCustomers);
    fetch("/api/products")
      .then((r) => r.json())
      .then(setProducts);
  }, []);

  const handleGenerate = async () => {
    if (!selectedCustomer || !selectedProduct) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const resp = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: selectedCustomer,
          product_id: selectedProduct,
        }),
      });
      if (!resp.ok) throw new Error(`Server error: ${resp.status}`);
      const data: GenerateResult = await resp.json();
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator-panel">
      <div className="controls">
        <div className="control-group">
          <label htmlFor="customer-select">Customer</label>
          <select
            id="customer-select"
            value={selectedCustomer}
            onChange={(e) => setSelectedCustomer(e.target.value)}
          >
            <option value="">Select a customer...</option>
            {customers.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="product-select">Product</label>
          <select
            id="product-select"
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
          >
            <option value="">Select a product...</option>
            {products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title} — ${p.price}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        className="generate-btn"
        onClick={handleGenerate}
        disabled={!selectedCustomer || !selectedProduct || loading}
      >
        {loading ? "Generating..." : "Generate Lifestyle Image"}
      </button>

      {loading && (
        <div className="loading">
          Generating your personalized ad image... This may take a moment.
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          {result.image_base64 && (
            <img
              src={`data:${result.mime_type};base64,${result.image_base64}`}
              alt="Generated lifestyle ad"
            />
          )}
          {result.summary && <div className="summary">{result.summary}</div>}
        </div>
      )}
    </div>
  );
}

export default ImageGenerator;
```

**Step 9: Install frontend dependencies and verify build**

```bash
cd frontend && npm install && npm run build
```

Expected: Build succeeds with no errors

**Step 10: Commit**

```bash
git add frontend/
git commit -m "feat: add React frontend with customer/product dropdowns and image display"
```

---

### Task 11: End-to-End Wiring and Run Script

**Files:**

- Create: `README.md`

**Step 1: Create `README.md`**

```markdown
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
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with setup and run instructions"
```

---

### Task 12: Full Test Suite Verification

**Step 1: Run all tests**

Run: `uv run pytest -v`
Expected: All tests pass

**Step 2: Manual smoke test**

1. Start backend: `uv run uvicorn server.app:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Open http://localhost:5173
4. Select "Alex Morgan" from customer dropdown
5. Select "Apex Trail Runner X1" from product dropdown
6. Click "Generate Lifestyle Image"
7. Verify image appears in the result area

**Step 3: Final commit**

```bash
git add -A
git commit -m "chore: final verification pass"
```

---

## Summary of Tools ↔ Agent Flow

```
User selects customer + product in React UI
         │
         ▼
    POST /api/generate {customer_id, product_id}
         │
         ▼
    FastAPI → Runner.run_async(agent, message)
         │
         ▼
    ┌─────────────────────────────────────────┐
    │         ADK Root Agent                  │
    │  (gemini-2.5-flash orchestrator)        │
    │                                         │
    │  1. collect_customer_data(customer_id)   │
    │  2. collect_product_data(product_id)     │
    │  3. collect_brand_assets()               │
    │  4. generate_image_prompt(...)            │
    │  5. generate_lifestyle_image(            │
    │       prompt, customer_photo,            │
    │       product_image, logo)               │
    │     → calls gemini-3.1-flash-image       │
    └─────────────────────────────────────────┘
         │
         ▼
    Response: {summary, image_base64, mime_type}
         │
         ▼
    React renders hero image + summary
```
