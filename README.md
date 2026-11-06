# 🎓 SlideCraft AI — Autonomous Academic Presentation Engine

> **Autonomous AI Slide Deck Synthesis for Students, Researchers, and Evaluators**  
> Generate exhaustive, high-theory academic presentations up to **25 slides** — complete with **formal concept definitions on Slide 1, deep theoretical mechanics, full-bleed thematic wallpapers, animated OpenXML slide transitions, and a dedicated closing Thank You & Q&A defense slide**. 100% Free & Open Source!

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PowerPoint](https://img.shields.io/badge/Format-Native%20.PPTX-D24726?style=for-the-badge&logo=microsoftpowerpoint)](https://microsoft.com/powerpoint)
[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)
[![Deep Research](https://img.shields.io/badge/Capacity-Up%20to%2025%20Slides-purple?style=for-the-badge)](https://github.com/SHIVA-TIWARI2403/ai-student-ppt-maker)

---

## 🌟 Key Capabilities & Upgrades

* **📖 Formal Concept Definition on Slide 1:** Automatically extracts and structures an exact scientific/engineering definition and primary operational premise on the introductory slide.
* **🙏 Dedicated Closing & Thank You Note on Final Slide:** Includes a formal appreciation note acknowledging faculty mentors, thesis committees, and opening the floor for Q&A discussion.
* **📚 Exhaustive Theoretical Depth (Up to 25 Slides):** Scales from brief 3-slide overviews up to 25-slide deep doctoral dissertations with mathematical formulations, asymptotic complexity, architectural blueprints, and empirical stress tests.
* **🌌 Thematic Full-Bleed Background Imagery:** Automatically synthesizes and dims high-resolution scientific background wallpapers with contrast overlays for maximum readability.
* **✨ Native PowerPoint OpenXML Transitions:** Generates genuine slide transitions (*Fade, Push, Wipe, Zoom*) directly embedded in the `.pptx` XML for dynamic presentation playback.
* **🎙️ Academic Presenter Scripts:** Embedded talking points for every slide (accessible in PowerPoint's Notes pane or via the live browser drawer).
* **🎨 5 Curated Academic Palettes:** Cyber Emerald, Academic Navy, Modern Minimalist, Vibrant Sunset, and Ocean Cyan.
* **💻 Interactive In-Browser Studio:** Real-time 16:9 stage preview, keyboard arrow navigation (`←` / `→`), smooth 25-slide thumbnail track, and fullscreen presentation mode.

---

## 🚀 Quick Start (1-Click Run)

### Windows
Double click `run.bat` or run:
```cmd
git clone https://github.com/SHIVA-TIWARI2403/ai-student-ppt-maker.git
cd ai-student-ppt-maker
run.bat
```

### Linux / macOS
```bash
git clone https://github.com/SHIVA-TIWARI2403/ai-student-ppt-maker.git
cd ai-student-ppt-maker
chmod +x run.sh
./run.sh
```

Navigate to `http://127.0.0.1:8000` in your web browser.

---

## 🏛️ Project Architecture

```
ai-student-ppt-maker/
├── main.py                  # FastAPI server & REST API
├── run.bat                  # 1-click Windows launcher
├── run.sh                   # 1-click Unix launcher
├── requirements.txt         # Core dependencies
├── services/
│   ├── ai_engine.py         # 25-slide academic curriculum & Gemini integration
│   ├── pptx_generator.py    # python-pptx builder with background imagery & transitions
│   ├── visual_service.py    # AI image & dimmed background generation pipeline
│   └── themes.py            # Academic color palettes & typography specifications
├── static/
│   ├── css/style.css        # Glassmorphic dark styling & 16:9 stage CSS
│   └── js/app.js            # Live carousel controller & PPTX exporter
└── templates/
    └── index.html           # Professional academic web studio interface
```

---

## 🔌 API Specification

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the Academic Presentation Studio |
| `POST` | `/api/generate` | Generates deep academic slide deck with definitions, visuals & scripts |
| `POST` | `/api/export-pptx` | Compiles native 16:9 `.pptx` with layouts, cards, wallpapers & transitions |
| `GET` | `/api/download/{id}` | Direct file download of the compiled `.pptx` file |
| `GET` | `/api/themes` | Returns available academic color schemes |

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

Developed with ❤️ by [Shiva Tiwari](https://github.com/SHIVA-TIWARI2403)
