"""
Visual service to fetch free AI images, stock photos, GIFs, and full-bleed thematic background textures.
Features smart contrast dimming to guarantee pristine text readability on slides.
"""

import os
import re
import urllib.parse
import hashlib
import requests
from PIL import Image, ImageDraw, ImageEnhance

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_ppts", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_filename(text: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    return cleaned[:30]

def get_cached_path(identifier: str, ext: str = "jpg") -> str:
    h = hashlib.md5(identifier.encode('utf-8')).hexdigest()[:12]
    filename = f"{clean_filename(identifier)}_{h}.{ext}"
    return os.path.join(CACHE_DIR, filename)

def generate_local_background(theme_id: str = "cyber_emerald") -> str:
    """Creates a high-resolution 1920x1080 gradient background with dark atmospheric vignette."""
    file_path = get_cached_path(f"bg_texture_{theme_id}")
    if os.path.exists(file_path):
        return file_path

    width, height = 1920, 1080
    theme_colors = {
        "cyber_emerald": ((10, 16, 26), (16, 185, 129)),
        "academic_navy": ((7, 16, 38), (72, 202, 228)),
        "modern_minimalist": ((240, 244, 248), (99, 102, 241)),
        "vibrant_sunset": ((24, 12, 38), (244, 63, 94)),
        "ocean_cyan": ((5, 24, 34), (6, 182, 212))
    }
    bg_base, accent = theme_colors.get(theme_id, ((12, 17, 26), (16, 185, 129)))

    img = Image.new("RGB", (width, height), color=bg_base)
    draw = ImageDraw.Draw(img)

    # Subtle ambient lighting glow in corner
    for r in range(400, 0, -8):
        alpha = int(18 * (r / 400))
        glow_color = (
            int(bg_base[0] + (accent[0] - bg_base[0]) * 0.12 * (r / 400)),
            int(bg_base[1] + (accent[1] - bg_base[1]) * 0.12 * (r / 400)),
            int(bg_base[2] + (accent[2] - bg_base[2]) * 0.12 * (r / 400)),
        )
        draw.ellipse([width - r * 2, -r, width + r, r * 2], fill=glow_color)

    # Grid texture lines
    step = 60
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(bg_base[0] + 8, bg_base[1] + 12, bg_base[2] + 18), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(bg_base[0] + 8, bg_base[1] + 12, bg_base[2] + 18), width=1)

    img.save(file_path, "JPEG", quality=92)
    return file_path

def generate_fallback_image(prompt: str, category: str = "Presentation") -> str:
    """Generates a stylish modern gradient card image when internet is offline."""
    file_path = get_cached_path(f"fallback_{prompt}")
    if os.path.exists(file_path):
        return file_path

    width, height = 1200, 800
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Subtle horizontal line shading
    for i in range(0, height, 4):
        alpha = int(25 + (i / height) * 40)
        draw.line([(0, i), (width, i)], fill=(alpha, alpha + 20, alpha + 50))

    # Decorative frame
    draw.rounded_rectangle([40, 40, width - 40, height - 40], radius=20, outline=(56, 189, 248), width=2)
    draw.rounded_rectangle([80, 80, width - 80, 260], radius=14, fill=(30, 41, 59))

    clean_text = prompt[:65] + "..." if len(prompt) > 65 else prompt
    draw.text((110, 130), f"ACADEMIC VISUALIZATION: {category.upper()}", fill=(56, 189, 248))
    draw.text((110, 180), clean_text, fill=(248, 250, 252))

    img.save(file_path, "JPEG", quality=90)
    return file_path

def fetch_ai_image(prompt: str, seed: int = 42) -> str:
    """
    Fetches free AI generated image from Pollinations.ai or high-res Unsplash academic visuals.
    """
    local_path = get_cached_path(prompt, "jpg")
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        return local_path

    encoded = urllib.parse.quote_plus(f"{prompt}, high quality scientific diagram, clean 3d render, academic textbook illustration, 4k")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=800&nologo=true&seed={seed}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200 and len(response.content) > 1000:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"[VisualService] AI image fetch error: {e}")

    # Fallback to local graphic
    return generate_fallback_image(prompt)

def fetch_background_image(topic: str, theme_id: str = "cyber_emerald", seed: int = 101) -> str:
    """
    Fetches or generates a dimmed full-bleed background wallpaper with dark academic gradient overlay.
    """
    local_path = get_cached_path(f"bg_{theme_id}_{topic}", "jpg")
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        return local_path

    encoded = urllib.parse.quote_plus(f"Abstract dark aesthetic scientific wallpaper for {topic}, deep atmospheric background, minimalist textures, 4k")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true&seed={seed}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200 and len(response.content) > 1000:
            # Apply dark overlay with PIL so slide text is always 100% legible
            img = Image.open(requests.get(url, headers=HEADERS, stream=True, timeout=8).raw).convert("RGB")
            # Dim the image brightness
            enhancer = ImageEnhance.Brightness(img)
            dimmed = enhancer.enhance(0.28) # 28% brightness keeps subtle aesthetic texture while making text pop
            dimmed.save(local_path, "JPEG", quality=90)
            return local_path
    except Exception as e:
        print(f"[VisualService] Background fetch error: {e}")

    return generate_local_background(theme_id)

def get_image_url_for_preview(prompt: str, seed: int = 42) -> str:
    """Returns a direct web URL for live browser preview."""
    encoded = urllib.parse.quote_plus(f"{prompt}, clean 3d scientific render, educational infographic, 4k")
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1000&height=650&nologo=true&seed={seed}"

def get_background_url_for_preview(topic: str, seed: int = 101) -> str:
    """Returns a direct web URL for full-bleed live background preview."""
    encoded = urllib.parse.quote_plus(f"Minimalist deep dark abstract atmospheric texture for {topic}, academic backdrop")
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1600&height=900&nologo=true&seed={seed}"
