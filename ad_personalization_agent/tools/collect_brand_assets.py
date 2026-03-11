"""Tool for collecting brand asset data."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def collect_brand_assets() -> dict:
    """Fetches the brand asset library including logo, colors, slogan, and font guidelines."""
    with open(DATA_DIR / "brand_assets.json") as f:
        brand = json.load(f)

    logo_path = str(DATA_DIR / brand["logo"])
    return {
        "status": "success",
        "brand": {
            "brand_name": brand["brand_name"],
            "description": brand["brand_description"],
            "slogan": brand["brand_slogan"],
            "color": brand["brand_color"],
            "font": brand["brand_font"],
            "logo_path": logo_path,
        },
    }
