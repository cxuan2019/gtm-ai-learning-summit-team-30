"""Tool for crafting a detailed image generation prompt from customer/product/brand data."""


def generate_image_prompt(
    customer_name: str,
    style_affinity: str,
    preferred_environment: str,
    aesthetic: str,
    product_title: str,
    product_description: str,
    brand_name: str,
    brand_slogan: str,
    brand_colors: str,
    brand_tone: str,
) -> dict:
    """Crafts a detailed, on-brand prompt for photorealistic lifestyle image generation.

    Combines customer style preferences, product details, and brand guidelines
    into a single image generation prompt.

    Args:
        customer_name: Name of the target customer.
        style_affinity: Customer's dominant activity or style (e.g., 'trail running').
        preferred_environment: Customer's preferred visual setting (e.g., 'mountain trails').
        aesthetic: Customer's visual aesthetic preference (e.g., 'rugged outdoor').
        product_title: Name of the product to feature.
        product_description: Text description of the product.
        brand_name: Name of the brand.
        brand_slogan: Brand slogan to include in the image.
        brand_colors: Brand color palette as a string.
        brand_tone: Brand voice/tone description.
    """
    prompt = (
        f"Generate a photorealistic lifestyle advertisement image.\n\n"
        f"SCENE: A {aesthetic} scene set in {preferred_environment}. "
        f"The mood is {brand_tone.lower()}.\n\n"
        f"PRODUCT: Prominently feature the '{product_title}' — {product_description}. "
        f"The product should be the focal point, shown in use within the lifestyle scene.\n\n"
        f"PERSON: Include a person who embodies the {style_affinity} lifestyle, "
        f"naturally interacting with the product in the scene.\n\n"
        f"BRANDING: Include the {brand_name} logo in the corner of the image. "
        f"Display the slogan '{brand_slogan}' as elegant text overlay. "
        f"Use the brand color palette ({brand_colors}) for any graphic elements.\n\n"
        f"STYLE: Photorealistic, high-resolution, professional advertising photography. "
        f"Natural lighting, shallow depth of field on the product. "
        f"The image should feel aspirational and authentic to the {style_affinity} community."
    )
    return {"status": "success", "prompt": prompt}
