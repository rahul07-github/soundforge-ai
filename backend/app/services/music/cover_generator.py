from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import uuid
import random
import textwrap

COVER_DIR = Path("backend/app/storage/generated/covers")
COVER_DIR.mkdir(parents=True, exist_ok=True)


def generate_cover(prompt: str) -> str:
    file_id = str(uuid.uuid4())[:8]
    cover_path = COVER_DIR / f"{file_id}.png"

    width, height = 1024, 1024

    top = (
        random.randint(10, 50),
        random.randint(10, 50),
        random.randint(40, 100)
    )

    bottom = (
        random.randint(80, 180),
        random.randint(10, 80),
        random.randint(100, 220)
    )

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        r = int(top[0] + (bottom[0] - top[0]) * y / height)
        g = int(top[1] + (bottom[1] - top[1]) * y / height)
        b = int(top[2] + (bottom[2] - top[2]) * y / height)
        draw.line((0, y, width, y), fill=(r, g, b))

    for _ in range(350):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        draw.ellipse(
            (x, y, x + size, y + size),
            fill=(brightness, brightness, brightness)
        )

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 72)
        sub_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    title = "SOUNDFORGE AI"
    subtitle = textwrap.fill(prompt[:90], width=28)

    draw.text((120, 180), title, font=title_font, fill=(255, 255, 255))
    draw.multiline_text(
        (120, 420),
        subtitle,
        font=sub_font,
        fill=(230, 230, 230),
        spacing=12
    )

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    img.save(cover_path)

    return str(cover_path)