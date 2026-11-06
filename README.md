# 🎓 SlideCraft AI — Autonomous Presentation & PPT Maker for Students

> **Autonomous AI Slide Deck Synthesis with Gamma-Style Bento Cards**  
> Generate punchy, modern slide presentations up to **25 slides** — complete with **Core Concept definition on Slide 1, 2-3 short easy-to-read bullets with emojis, 100% watermark-free HD visuals, native OpenXML PowerPoint slide transitions, and a pure minimalist closing Thank You & Q&A slide**. 100% Free & Open Source!

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PowerPoint](https://img.shields.io/badge/Format-Native%20.PPTX-D24726?style=for-the-badge&logo=microsoftpowerpoint)](https://microsoft.com/powerpoint)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

---

## 🛠️ Tech Stack & Skills

This project leverages modern full-stack, AI, and document generation technologies:

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/PowerPoint_OpenXML-D24726?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white" alt="PowerPoint PPTX" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Pillow-111111?style=for-the-badge&logo=python&logoColor=white" alt="Pillow Image Processing" />
  <img src="https://img.shields.io/badge/Uvicorn-2C3E50?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Uvicorn Server" />
</p>

| Technology | Purpose in Project |
| :--- | :--- |
| **Python 3.10+** | Core application logic, OpenXML manipulation, and presentation building |
| **FastAPI & Uvicorn** | High-performance asynchronous REST API backend serving templates & generation endpoints |
| **python-pptx & OpenXML** | Compiling genuine Microsoft PowerPoint files (.pptx) with custom Bento shapes and transitions |
| **Google Gemini API** | AI-driven content structuring, concise bullet points, and conversational presenter scripts |
| **JavaScript (ES6+)** | Dynamic Gamma-style Bento UI, keyboard navigation (`←`/`→`), dual view mode controller |
| **Tailwind CSS & Outfit** | Glassmorphic dark styling, modern geometric typography, and responsive 16:9 stage layout |
| **Pillow (PIL)** | Image resizing, dimming, aspect ratio handling, and gradient backdrop synthesis |

---

## 🌟 Key Capabilities

* **💡 Core Concept Definition on Slide 1:** Simple, punchy 1-sentence explanation in plain English ("What is it in simple words?").
* **🎉 Pure Minimalist "Thank You!" Final Slide:** Clean closing hero card opening the floor for Q&A without any cluttered keyword lists.
* **⚡ Short, Punchy Wording:** Maximum 2 to 3 short bullets per slide (under 12 words each) with modern emojis (`🚀`, `⚡`, `🧠`, `💡`, `🛡️`).
* **🖼️ 100% Watermark-Free Visuals:** Curated high-resolution Unsplash photos and clean 3D graphics (zero ads, zero watermarks).
* **✨ Native PowerPoint OpenXML Transitions:** Generates genuine slide transitions (*Fade, Push, Wipe, Zoom*) directly embedded in the `.pptx` XML for dynamic presentation playback.
* **🎴 Dual View Modes (Gamma Edition):**
  * **Presentation Deck (16:9):** Presentation stage with arrow key navigation and fullscreen present mode.
  * **Continuous Document:** Scroll smoothly through all cards on a single page, exactly like a shareable Gamma web presentation.
* **🎙️ Student Presenter Scripts:** Embedded talking points for every slide (accessible in PowerPoint's Notes pane or via the live browser drawer).
* **🎨 5 Modern Color Palettes:** Obsidian Emerald, Midnight Cobalt, Stark Minimalist, Onyx Rose, and Deep Marine.

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
│   ├── ai_engine.py         # Punchy student content engine & Gemini integration
│   ├── pptx_generator.py    # Gamma-style Bento PPTX generator with XML transitions
│   ├── visual_service.py    # Clean, watermark-free visual pipeline
│   └── themes.py            # Modern color palettes & typography specifications
├── static/
│   ├── css/style.css        # Outfit & Plus Jakarta typography & Bento CSS
│   └── js/app.js            # Dual view mode controller & PPTX exporter
└── templates/
    └── index.html           # Gamma-style web studio interface
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

Developed with ❤️ by [Shiva Tiwari](https://github.com/SHIVA-TIWARI2403)
