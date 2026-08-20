<<<<<<< HEAD
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import uuid
import random
import textwrap
=======
from pathlib import Path
import random
import textwrap
import uuid

from PIL import Image, ImageDraw, ImageFilter, ImageFont

>>>>>>> origin

COVER_DIR = Path("backend/app/storage/generated/covers")
COVER_DIR.mkdir(parents=True, exist_ok=True)


<<<<<<< HEAD
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
=======
def load_font(size: int, bold: bool = False):
    font_paths = []

    if bold:
        font_paths = [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
    else:
        font_paths = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
        ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue

    return ImageFont.load_default()


def get_theme(prompt: str):
    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ["sad", "breakup", "lonely", "cry"]):
        return {
            "top": (8, 20, 38),
            "bottom": (38, 62, 94),
            "accent": (120, 170, 255),
            "mood": "sad",
        }

    if any(word in prompt_lower for word in ["romantic", "love", "heart"]):
        return {
            "top": (52, 12, 42),
            "bottom": (150, 45, 100),
            "accent": (255, 170, 210),
            "mood": "romantic",
        }

    if any(word in prompt_lower for word in ["rap", "hip hop", "street"]):
        return {
            "top": (10, 10, 10),
            "bottom": (70, 0, 90),
            "accent": (235, 80, 255),
            "mood": "rap",
        }

    if any(word in prompt_lower for word in ["happy", "party", "dance"]):
        return {
            "top": (255, 100, 40),
            "bottom": (255, 185, 60),
            "accent": (255, 255, 255),
            "mood": "happy",
        }

    if "lofi" in prompt_lower:
        return {
            "top": (25, 20, 48),
            "bottom": (65, 48, 90),
            "accent": (210, 180, 255),
            "mood": "lofi",
        }

    return {
        "top": (20, 24, 40),
        "bottom": (70, 35, 110),
        "accent": (220, 220, 255),
        "mood": "default",
    }


def draw_gradient(image, top_color, bottom_color):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for y in range(height):
        ratio = y / max(height - 1, 1)

        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)

        draw.line((0, y, width, y), fill=(r, g, b))


def add_cinematic_elements(image, theme):
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = image.size
    mood = theme["mood"]

    for _ in range(220):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(1, 3)
        opacity = random.randint(60, 190)

        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=(255, 255, 255, opacity),
        )

    if mood == "sad":
        for _ in range(120):
            x = random.randint(0, width)
            y = random.randint(0, height)
            length = random.randint(12, 35)

            draw.line(
                (x, y, x - 4, y + length),
                fill=(180, 210, 255, random.randint(40, 120)),
                width=1,
            )

        draw.ellipse(
            (730, 120, 920, 310),
            fill=(220, 235, 255, 28),
        )

        draw.rectangle(
            (0, 760, width, height),
            fill=(0, 0, 0, 70),
        )

        draw.ellipse(
            (620, 460, 870, 950),
            fill=(5, 8, 18, 210),
        )

    elif mood == "romantic":
        for _ in range(20):
            x = random.randint(100, width - 100)
            y = random.randint(150, height - 150)
            radius = random.randint(20, 70)

            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(255, 130, 190, random.randint(15, 45)),
            )

    elif mood == "rap":
        for _ in range(12):
            x = random.randint(0, width)
            y = random.randint(0, height)

            draw.line(
                (x, y, x + random.randint(80, 220), y),
                fill=(255, 0, 210, random.randint(35, 85)),
                width=random.randint(2, 6),
            )

    elif mood == "happy":
        for _ in range(35):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(12, 42)

            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(
                    random.randint(180, 255),
                    random.randint(120, 255),
                    random.randint(70, 220),
                    60,
                ),
            )

    elif mood == "lofi":
        draw.rectangle(
            (90, 200, 450, 760),
            fill=(30, 24, 52, 150),
            outline=(220, 190, 255, 90),
            width=4,
        )

        draw.rectangle(
            (580, 240, 920, 700),
            fill=(20, 18, 38, 160),
            outline=(160, 130, 220, 90),
            width=4,
        )


def generate_cover(prompt: str) -> str:
    clean_prompt = (prompt or "Untitled Song").strip()

    file_id = uuid.uuid4().hex[:8]
    cover_path = COVER_DIR / f"{file_id}.png"

    width = 1024
    height = 1024

    theme = get_theme(clean_prompt)

    image = Image.new("RGB", (width, height))
    draw_gradient(image, theme["top"], theme["bottom"])

    image = image.filter(ImageFilter.GaussianBlur(radius=0.4))

    add_cinematic_elements(image, theme)

    draw = ImageDraw.Draw(image, "RGBA")

    draw.rectangle(
        (0, 0, width, 190),
        fill=(0, 0, 0, 85),
    )

    draw.rectangle(
        (0, height - 230, width, height),
        fill=(0, 0, 0, 105),
    )

    brand_font = load_font(72, bold=True)
    title_font = load_font(42, bold=False)
    label_font = load_font(28, bold=True)

    draw.text(
        (70, 65),
        "SOUNDFORGE AI",
        font=brand_font,
        fill=(255, 255, 255, 255),
    )

    wrapped_title = textwrap.fill(clean_prompt[:90], width=26)

    draw.multiline_text(
        (70, height - 190),
        wrapped_title,
        font=title_font,
        fill=(255, 255, 255, 255),
        spacing=12,
    )

    draw.rounded_rectangle(
        (70, height - 65, 295, height - 20),
        radius=10,
        fill=(*theme["accent"], 55),
        outline=(*theme["accent"], 180),
        width=2,
    )

    draw.text(
        (90, height - 57),
        "GENERATED MUSIC",
        font=label_font,
        fill=(255, 255, 255, 255),
    )

    image.save(cover_path, format="PNG")
>>>>>>> origin

    return str(cover_path)