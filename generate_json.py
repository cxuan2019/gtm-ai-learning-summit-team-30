import json
import os

images_dir = "images/"
customer_images = [f for f in os.listdir(images_dir) if f.startswith('customer_') and f.endswith('.png')]
customer_images.sort()

customers_data = [
    {
        'customer_name': 'Chloe Vance',
        'customer_image': os.path.join(images_dir, customer_images[0] if len(customer_images) > 0 else ''),
        'browsing_history': 'Women\'s running shoes, athletic apparel, yoga mats',
        'past_purchase': 'Nike React Infinity Run, sports bra'
    },
    {
        'customer_name': 'David Chen',
        'customer_image': os.path.join(images_dir, customer_images[1] if len(customer_images) > 1 else ''),
        'browsing_history': 'Men\'s basketball shoes, streetwear sneakers, hoodies',
        'past_purchase': 'Air Jordan 1 High, Nike tech fleece'
    },
    {
        'customer_name': 'Jamal Reynolds',
        'customer_image': os.path.join(images_dir, customer_images[2] if len(customer_images) > 2 else ''),
        'browsing_history': 'Skate shoes, vintage sneakers, casual wear',
        'past_purchase': 'Nike SB Dunk Low, vintage Nike windbreaker'
    }
]

products_data = [
    {
        'product_name': 'Nike Air Force 1 \'07',
        'product_description': 'The radiance lives on in the Nike Air Force 1 \'07, the b-ball icon that puts a fresh spin on what you know best: crisp leather, bold colours and the perfect amount of flash to make you shine.',
        'product_image': os.path.join(images_dir, 'product_1.png'),
        'product_style': 'Classic, Streetwear, Everyday'
    },
    {
        'product_name': 'Nike Air Max 90',
        'product_description': 'Lace up and feel the legacy. Produced at the intersection of art, music and culture, this champion running shoe helped define the \'90s.',
        'product_image': os.path.join(images_dir, 'product_2.png'),
        'product_style': 'Retro, Sporty, Bold'
    },
    {
        'product_name': 'Nike Dunk Low Retro',
        'product_description': 'Created for the hardwood but taken to the streets, the \'80s b-ball icon returns with perfectly shined overlays and classic team colours.',
        'product_image': os.path.join(images_dir, 'product_3.png'),
        'product_style': 'Skate, Vintage, Casual'
    }
]

output_data = {
    'customers': customers_data,
    'products': products_data
}

with open('data.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Generated data.json")
