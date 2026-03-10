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
