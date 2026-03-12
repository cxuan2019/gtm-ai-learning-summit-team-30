from ad_personalization_agent.tools.generate_image_prompt import generate_image_prompt


def test_generate_prompt_contains_key_elements():
    result = generate_image_prompt(
        customer_name="Chloe Vance",
        browsing_history="Women's running shoes, athletic apparel, yoga mats",
        past_purchases="Nike React Infinity Run, sports bra",
        product_title="Nike Air Force 1 '07",
        product_description="The b-ball icon that puts a fresh spin on what you know best",
        product_style="Classic, Streetwear, Everyday",
        brand_name="Nike",
        brand_slogan="Just Do It.",
        brand_color="#000000",
    )
    assert result["status"] == "success"
    prompt = result["prompt"]
    assert "Nike Air Force 1" in prompt
    assert "Nike" in prompt
    assert "Just Do It." in prompt
    assert "photorealistic" in prompt.lower()


def test_generate_prompt_includes_logo_instruction():
    result = generate_image_prompt(
        customer_name="David Chen",
        browsing_history="Men's basketball shoes, streetwear sneakers",
        past_purchases="Air Jordan 1 High, Nike tech fleece",
        product_title="Nike Air Max 90",
        product_description="Champion running shoe that helped define the '90s",
        product_style="Retro, Sporty, Bold",
        brand_name="Nike",
        brand_slogan="Just Do It.",
        brand_color="#000000",
    )
    prompt = result["prompt"]
    assert "logo" in prompt.lower()
    assert "slogan" in prompt.lower()
