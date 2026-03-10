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
    assert "Apex Trail Runner X1" in prompt
    assert "mountain" in prompt.lower() or "trail" in prompt.lower()
    assert "Summit Athletics" in prompt
    assert "Rise Above. Push Beyond." in prompt
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
