"""Tool for crafting a detailed image generation prompt from customer/product/brand data."""


def generate_image_prompt(
    customer_name: str,
    browsing_history: str,
    past_purchases: str,
    product_title: str,
    product_description: str,
    product_style: str,
    brand_name: str,
    brand_slogan: str,
    brand_color: str,
) -> dict:
    """Crafts a detailed, on-brand prompt for photorealistic lifestyle image generation.

    Combines customer interests, product details, and brand guidelines
    into a single image generation prompt.

    Args:
        customer_name: Name of the target customer.
        browsing_history: Customer's browsing history summary.
        past_purchases: Customer's past purchase summary.
        product_title: Name of the product to feature.
        product_description: Text description of the product.
        product_style: Product style tags (e.g., 'Classic, Streetwear, Everyday').
        brand_name: Name of the brand.
        brand_slogan: Brand slogan to include in the image.
        brand_color: Primary brand color hex code.
    """
    prompt = (
        f"Generate a photorealistic lifestyle advertisement image.\n\n"
        f"CUSTOMER CONTEXT: The target customer is interested in: {browsing_history}. "
        f"They have previously purchased: {past_purchases}. "
        f"Design the scene to appeal to their style and interests.\n\n"
        f"PRODUCT: Prominently feature the '{product_title}' — {product_description}. "
        f"The product style is {product_style}. "
        f"The product should be the focal point, shown in use within the lifestyle scene.\n\n"
        f"PERSON: Include a person who naturally fits the {product_style} aesthetic, "
        f"wearing or interacting with the product in a lifestyle setting.\n\n"
        f"BRANDING: Include the {brand_name} logo in the corner of the image. "
        f"Display the slogan '{brand_slogan}' as elegant text overlay. "
        f"Use the brand color ({brand_color}) for any graphic elements.\n\n"
        f"STYLE: Photorealistic, high-resolution, professional advertising photography. "
        f"Natural lighting, shallow depth of field on the product. "
        f"The image should feel aspirational and authentic."
    )
    return {"status": "success", "prompt": prompt}
