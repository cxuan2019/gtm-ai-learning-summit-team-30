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
