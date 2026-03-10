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
