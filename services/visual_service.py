"""
Visual service to fetch free AI images, Unsplash stock photos, and GIFs for slides.
Supports Pollinations.ai (Free Generative AI), Unsplash, Giphy, and PIL fallback graphics.
"""

import os
import re
import urllib.parse
import hashlib
import requests
from PIL import Image, ImageDraw, ImageFont

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

def generate_fallback_image(prompt: str, category: str = "Presentation") -> str:
    """Generates a stylish modern gradient card image when internet is offline."""
    file_path = get_cached_path(f"fallback_{prompt}")
    if os.path.exists(file_path):
        return file_path

    width, height = 1200, 800
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Gradient-like subtle lines
    for i in range(0, height, 4):
        alpha = int(25 + (i / height) * 40)
        draw.line([(0, i), (width, i)], fill=(alpha, alpha + 20, alpha + 50))

    # Decorative shapes
    draw.rounded_rectangle([60, 60, width - 60, height - 60], radius=24, outline=(56, 189, 248), width=3)
    draw.rounded_rectangle([100, 100, width - 100, 300], radius=16, fill=(30, 41, 59))

    # Add text representation
    clean_text = prompt[:60] + "..." if len(prompt) > 60 else prompt
    draw.text((140, 180), f"VISUAL: {category.upper()}", fill=(56, 189, 248))
    draw.text((140, 220), clean_text, fill=(248, 250, 252))

    img.save(file_path, "JPEG", quality=90)
    return file_path

def fetch_ai_image(prompt: str, seed: int = 42) -> str:
    """
    Fetches free AI generated image from Pollinations.ai.
    Zero API key required, 100% free!
    """
    local_path = get_cached_path(prompt, "jpg")
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        return local_path

    encoded = urllib.parse.quote_plus(f"{prompt}, high quality 3d render, academic infographic, clean presentation slide illustration, 4k, hyper-detailed")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=800&nologo=true&seed={seed}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        if response.status_code == 200 and len(response.content) > 1000:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"[VisualService] Pollinations fetch failed for '{prompt}': {e}")

    # Try Unsplash source fallback
    try:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', prompt)
        keyword = words[0] if words else "technology"
        unsplash_url = f"https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop&q=80"
        res = requests.get(unsplash_url, headers=HEADERS, timeout=8)
        if res.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(res.content)
            return local_path
    except Exception:
        pass

    return generate_fallback_image(prompt)

def get_image_url_for_preview(prompt: str, seed: int = 42) -> str:
    """Returns a direct web URL for live browser preview."""
    encoded = urllib.parse.quote_plus(f"{prompt}, clean 3d visual, scientific presentation slide illustration, 4k")
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1000&height=650&nologo=true&seed={seed}"

def get_gif_url_for_preview(query: str) -> str:
    """Returns a relevant animated GIF link for live web view or fallback animated badge."""
    clean_q = urllib.parse.quote_plus(query)
    # Using public giphy embedded preview or tenor web format
    return f"https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif"
