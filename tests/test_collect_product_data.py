from ad_personalization_agent.tools.collect_product_data import collect_product_data


def test_collect_known_product():
    result = collect_product_data(product_id="prod_001")
    assert result["status"] == "success"
    assert result["product"]["title"] == "Nike Air Force 1 '07"
    assert "description" in result["product"]
    assert "image_path" in result["product"]
    assert "style" in result["product"]


def test_collect_unknown_product():
    result = collect_product_data(product_id="prod_999")
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()
