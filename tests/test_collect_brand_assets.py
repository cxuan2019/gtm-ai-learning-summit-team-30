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
