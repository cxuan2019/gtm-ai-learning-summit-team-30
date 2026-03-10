"""Generate placeholder images for development."""
from pathlib import Path
from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "ad_personalization_agent" / "data" / "assets"

PLACEHOLDERS = {
    "customers/alex_morgan.png": ("Alex M.", "#4A90D9", (256, 256)),
    "customers/jordan_patel.png": ("Jordan P.", "#7B68EE", (256, 256)),
    "customers/sam_rivera.png": ("Sam R.", "#E07C4F", (256, 256)),
    "products/trail_running_shoe.png": ("Trail Shoe", "#2E8B57", (512, 512)),
    "products/insulated_water_bottle.png": ("Bottle", "#4682B4", (512, 512)),
    "products/yoga_mat.png": ("Yoga Mat", "#9370DB", (512, 512)),
    "products/cycling_jersey.png": ("Jersey", "#DC143C", (512, 512)),
    "brand/logo.png": ("Summit Athletics", "#1B4D3E", (512, 256)),
}

def generate():
    for path, (label, color, size) in PLACEHOLDERS.items():
        img = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(img)
        draw.text((size[0] // 2, size[1] // 2), label, fill="white", anchor="mm")
        out = ASSETS / path
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        print(f"Created {out}")

if __name__ == "__main__":
    generate()
