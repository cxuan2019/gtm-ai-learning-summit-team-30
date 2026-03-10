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
