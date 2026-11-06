"""
SlideCraft AI - Advanced Academic Presentation Engine.
High-theory research presentation generator for university students & researchers.
Features background imagery, formal concept definitions, up to 25 slides, and dedicated thank you notes.
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from services.themes import THEMES, get_theme
from services.ai_engine import generate_presentation_with_gemini
from services.pptx_generator import build_presentation_pptx
from services.visual_service import get_image_url_for_preview, get_background_url_for_preview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
GENERATED_DIR = os.path.join(BASE_DIR, "generated_ppts")

app = FastAPI(
    title="SlideCraft AI",
    description="Autonomous Academic Presentation Engine for Students & Researchers",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class GenerateRequest(BaseModel):
    topic: str
    slide_count: int = 10
    education_level: str = "Master's & Doctoral"
    theme: str = "cyber_emerald"
    include_images: bool = True
    include_background: bool = True
    include_animations: bool = True
    gemini_api_key: Optional[str] = None

class ExportRequest(BaseModel):
    presentation_data: Dict[str, Any]
    theme: str = "cyber_emerald"
    include_images: bool = True
    include_background: bool = True

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SlideCraft AI is starting...</h1>"

@app.get("/api/themes")
async def list_themes():
    return list(THEMES.values())

@app.post("/api/generate")
async def generate_deck(req: GenerateRequest):
    if not req.topic or len(req.topic.strip()) < 2:
        raise HTTPException(status_code=400, detail="Research topic or thesis title is required.")

    # Support up to 25 slides
    count = max(3, min(req.slide_count, 25))
    
    # 1. Generate deep scholarly presentation structure
    data = generate_presentation_with_gemini(
        topic=req.topic,
        slide_count=count,
        education_level=req.education_level,
        api_key=req.gemini_api_key
    )

    # 2. Enrich with visual preview URLs and background wallpaper
    bg_preview = get_background_url_for_preview(req.topic)
    for idx, slide in enumerate(data.get("slides", [])):
        img_prompt = slide.get("image_prompt", f"{req.topic} scientific illustration")
        slide["preview_image_url"] = get_image_url_for_preview(img_prompt, seed=idx * 19 + 7)
        slide["preview_bg_url"] = bg_preview

    return {
        "status": "success",
        "theme": req.theme,
        "include_background": req.include_background,
        "presentation": data
    }

@app.post("/api/export-pptx")
async def export_pptx(req: ExportRequest):
    try:
        file_id, file_path = build_presentation_pptx(
            presentation_data=req.presentation_data,
            theme_name=req.theme,
            include_images=req.include_images,
            include_background=req.include_background
        )
        return {
            "status": "success",
            "file_id": file_id,
            "download_url": f"/api/download/{file_id}"
        }
    except Exception as e:
        print(f"[ExportError] {e}")
        raise HTTPException(status_code=500, detail=f"PPTX build error: {str(e)}")

@app.get("/api/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join(GENERATED_DIR, f"{file_id}.pptx")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Requested presentation not found.")
    
    return FileResponse(
        path=file_path,
        filename=f"{file_id}.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🚀 SlideCraft AI (Academic Defense & Research Edition) is live!")
    print("  👉 Access Web Interface: http://127.0.0.1:8000")
    print("=" * 70 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
