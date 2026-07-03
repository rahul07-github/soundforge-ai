from PIL import Image, ImageDraw
import os
import uuid

def generate_cover(prompt):

    os.makedirs(
        "backend/app/storage/generated/covers",
        exist_ok=True
    )

    filename = f"{uuid.uuid4().hex[:8]}.png"

    cover_path = f"backend/app/storage/generated/covers/{filename}"

    img = Image.new(
        "RGB",
        (512, 512),
        color=(30, 30, 30)
    )

    draw = ImageDraw.Draw(img)

    draw.text(
        (50, 250),
        prompt,
        fill=(255, 255, 255)
    )

    img.save(cover_path)

    return cover_path