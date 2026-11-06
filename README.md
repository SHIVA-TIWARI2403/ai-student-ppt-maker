# 🎓 SlideGen AI — Free AI Presentation Maker for Students

> **"Bass Idea Do Aur AI Banna Krr Dega PPT!"**  
> Generate high-impact, academic & technical slide decks in seconds — complete with **AI visuals, animated slide transitions, structured bullet points, and student viva presenter notes**. 100% Free & Open Source!

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PowerPoint](https://img.shields.io/badge/Format-Native%20.PPTX-D24726?style=for-the-badge&logo=microsoftpowerpoint)](https://microsoft.com/powerpoint)
[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4?style=for-the-badge&logo=google)](https://aistudio.google.com)

---

## ✨ Why SlideGen AI?

Most AI presentation tools (Gamma, Beautiful.ai) are either heavily paywalled or restrict students after 1 or 2 trial decks. **SlideGen AI** is built specifically for school, college, and university students to generate unlimited, professional `.pptx` presentations completely free!

### 🌟 Key Features

* **⚡ Single-Prompt Generation:** Type any topic (e.g., *"CRISPR Gene Editing"*, *"Quantum Computing Architecture"*, *"Renewable Energy 2026"*) and select your slide count (3 to 15 slides).
* **🎨 100% Native `.pptx` Files:** Genuine PowerPoint format compatible with **Microsoft PowerPoint, Google Slides, Apple Keynote, and LibreOffice**.
* **✨ Animated Slide Transitions:** Automatically embeds native OpenXML transitions (*Fade, Push, Wipe, Zoom*) directly into the presentation for engaging classroom playback.
* **🖼️ Auto Visuals & Diagrams:** Integrated with **Pollinations AI** and **Unsplash** to generate high-resolution illustrations and diagrams relevant to each slide.
* **🎙️ Student Viva / Presenter Notes:** Every slide comes with an embedded presenter script telling you exactly what to say to your teacher/audience.
* **🎭 5 Professional Academic Themes:**
  * **Cyber Emerald:** Dark tech mode for Computer Science, Engineering, and AI.
  * **Academic Navy:** Authoritative deep cobalt for research seminars.
  * **Modern Minimalist:** Editorial clean light aesthetic.
  * **Vibrant Sunset:** Creative gradient vibe for projects and humanities.
  * **Ocean Cyan:** Deep marine blue with neon cyan accents.
* **💻 Interactive In-Browser Studio:** Flip through slides with arrow keys, preview speaker notes, and enter fullscreen presentation mode right in your browser!
* **🛡️ Zero-Key Offline Fallback Mode:** Works out of the box even without entering an API key. Optional custom Gemini 2.0 Flash key support for unlimited dynamic topics.

---

## 🚀 Quick Start (1-Click Run)

### Windows
Double click `run.bat` or run in terminal:
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

The app will start at `http://127.0.0.1:8000`!

---

## 🛠️ Tech Stack & Architecture

```
ai-student-ppt-maker/
├── main.py                  # FastAPI application & API endpoints
├── run.bat                  # 1-click Windows launcher
├── run.sh                   # 1-click Linux/Mac launcher
├── requirements.txt         # Core dependencies
├── services/
│   ├── ai_engine.py         # Gemini 2.0 Flash + Intelligent Offline Generator
│   ├── pptx_generator.py    # python-pptx engine with native XML transitions
│   ├── visual_service.py    # Free AI image & Unsplash fetching pipeline
│   └── themes.py            # Academic & modern aesthetic presets
├── static/
│   ├── css/style.css        # Glassmorphic UI & 16:9 stage styling
│   └── js/app.js            # Live carousel controller & PPTX exporter
└── templates/
    └── index.html           # Student-first web studio interface
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the interactive Student Presentation Studio |
| `POST` | `/api/generate` | Generates structured slide content with visuals & notes |
| `POST` | `/api/export-pptx` | Compiles `.pptx` with layouts, cards, and transitions |
| `GET` | `/api/download/{id}` | Direct file download of the compiled PowerPoint presentation |
| `GET` | `/api/themes` | Lists all active color palettes and font styling |

---

## 🤝 Contributing

Contributions are warmly welcomed!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more details.

Developed with ❤️ by [Shiva Tiwari](https://github.com/SHIVA-TIWARI2403)
