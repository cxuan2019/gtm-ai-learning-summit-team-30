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
