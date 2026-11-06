"""
High-Impact, Punchy Student AI Engine for SlideCraft AI.
Features:
- Slide 1: Core Concept Definition & Scope
- Middle Slides: Short, crisp, 2-3 bullet points with emojis (no heavy theory)
- Final Slide: Pure, Minimalist "Thank You!" and Q&A (No keyword lists or takeaways!)
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an award-winning creative presentation designer.

CORE DESIGN RULES:
1. SLIDE 1: Must feature a simple, high-impact CORE CONCEPT definition in plain English.
2. MIDDLE SLIDES: Maximum 2 to 3 short bullets per slide (under 12 words each!). Easy plain wording.
3. FINAL SLIDE: PURE, CLEAN "THANK YOU!" ONLY. Do NOT add any summary keywords, takeaways, or bullet points to the final slide!
4. EMOJIS & STATS: Use modern emojis (⚡, 🚀, 🧠, 🛡️, 💡) and punchy highlight stats.
5. STRICT JSON output matching the requested schema.
"""

def generate_academic_deep_deck(topic: str, slide_count: int, education_level: str = "College") -> dict:
    """
    Punchy student-friendly generator with Core Concept on Slide 1 and pure Thank You on the final slide.
    """
    clean_topic = topic.strip().title()
    count = max(3, min(slide_count, 25))

    master_modules = [
        # Slide 1: Core Concept Definition & Scope
        {
            "layout_type": "title",
            "tag": "CORE CONCEPT",
            "title": f"{clean_topic}",
            "subtitle": "The Complete Student Presentation & Guide",
            "formal_definition": f"In simple words, {clean_topic} is a breakthrough technology that replaces slow traditional systems with super-smart, automated processing to solve complex problems in seconds.",
            "bullet_points": [
                f"🚀 **The Big Idea**: Why {clean_topic} is changing the world right now.",
                "⚡ **Superpowers**: How it computes and automates at lightning speed.",
                "🎯 **Key Roadmap**: Core basics, real-world magic, and future trends."
            ],
            "stat_or_highlight": "🚀 Next-Gen Tech 2026",
            "image_prompt": f"Futuristic glowing conceptual 3d illustration of {clean_topic}, neon cyan and emerald, clean render",
            "speaker_notes": f"Hi everyone! Today we are exploring {clean_topic}. In simple words, it's all about making systems faster, smarter, and scalable."
        },
        # Slide 2: Why It Matters
        {
            "layout_type": "split_image_right",
            "tag": "THE BIG WHY",
            "title": "Why Everyone is Talking About It",
            "subtitle": "The Old Way vs. The Modern Breakthrough",
            "bullet_points": [
                "🐢 **The Old Problem**: Traditional methods were slow, manual, and expensive.",
                "⚡ **The Modern Leap**: Solves in minutes what used to take weeks of effort.",
                "💡 **Massive Impact**: Millions of users and systems benefit every day."
            ],
            "stat_or_highlight": "⚡ 10x Faster Results",
            "image_prompt": f"Comparison visual between old technology and futuristic glowing {clean_topic}, 3d render",
            "speaker_notes": f"Why does this matter? Old approaches were too slow. Modern solutions accelerate everything by 10x."
        },
        # Slide 3: How It Works in 3 Steps
        {
            "layout_type": "three_cards",
            "tag": "HOW IT WORKS",
            "title": "How It Works in 3 Simple Steps",
            "subtitle": "The Secret Engine Behind the Magic",
            "bullet_points": [
                "📥 **Step 1: Smart Ingestion**: Collects messy raw data and cleans it instantly.",
                "🧠 **Step 2: Core Processing**: Runs intelligent algorithms to find optimal answers.",
                "🚀 **Step 3: Instant Delivery**: Serves verified results to users with zero lag."
            ],
            "stat_or_highlight": "⏱️ Sub-second Response",
            "image_prompt": f"Three connected glowing futuristic steps showing workflow of {clean_topic}, 3d isometric",
            "speaker_notes": f"You can understand the inner mechanics in 3 simple steps: Smart input, core processing, and instant delivery."
        },
        # Slide 4: Key Pillars
        {
            "layout_type": "three_cards",
            "tag": "THE SECRET SAUCE",
            "title": "The 3 Key Pillars of Success",
            "subtitle": "What Makes It So Powerful?",
            "bullet_points": [
                "⚡ **Speed**: Computes at mind-blowing rates without overheating.",
                "🛡️ **Reliability**: Self-heals automatically if any component fails.",
                "📈 **Scalability**: Handles 1 user or 100 million users effortlessly."
            ],
            "stat_or_highlight": "🌟 99.9% Uptime",
            "image_prompt": f"Three floating glowing neon crystal pillars representing speed, reliability and scale",
            "speaker_notes": f"These three pillars are the secret sauce: ultra-fast speed, bulletproof reliability, and effortless scale."
        },
        # Slide 5: Real-World Use Cases
        {
            "layout_type": "split_image_left",
            "tag": "REAL WORLD",
            "title": "Real-World Superpowers in Action",
            "subtitle": "Where Is It Being Used Right Now?",
            "bullet_points": [
                "🏥 **Healthcare**: Spotting diseases and discovering new medicines years faster.",
                "🚗 **Smart Mobility**: Powering autonomous vehicles and self-optimizing traffic.",
                "📱 **Everyday Apps**: Running your favorite instant search and recommendation tools."
            ],
            "stat_or_highlight": "🌍 1B+ Daily Users",
            "image_prompt": f"Modern futuristic city and medical lab using {clean_topic} in everyday life, 3d render",
            "speaker_notes": f"This isn't just theory—it's already saving lives in healthcare, running smart cars, and powering everyday apps."
        },
        # Slide 6: Crazy Performance Stats
        {
            "layout_type": "deep_theory",
            "tag": "THE NUMBERS",
            "title": "Insane Benchmark Numbers",
            "subtitle": "The Proof is in the Data",
            "bullet_points": [
                "🚀 **Speed Boost**: Up to 100x faster than traditional baseline methods.",
                "🔋 **Green Computing**: Cuts electrical power draw and carbon emissions by 40%.",
                "🎯 **Precision**: Consistent 99.8% accuracy even during peak traffic spikes."
            ],
            "stat_or_highlight": "🚀 100x Acceleration",
            "image_prompt": f"Glowing 3D neon holographic statistics and data speed bars on dark glass pedestal",
            "speaker_notes": f"Check out these numbers! We are seeing up to 100 times acceleration while saving 40% energy."
        },
        # Slide 7: The Big Challenges
        {
            "layout_type": "split_image_right",
            "tag": "CHALLENGES",
            "title": "The Big Challenges & How We Fix Them",
            "subtitle": "Overcoming Roadblocks Like a Pro",
            "bullet_points": [
                "💰 **Initial Hardware Cost**: Setting up specialized chips requires smart budgeting.",
                "🔒 **Data Security**: Must enforce strict encryption so hackers can't intercept.",
                "🎓 **Skill Gap**: We need more trained students and engineers to build the future."
            ],
            "stat_or_highlight": "🛡️ 100% End-to-End Encrypted",
            "image_prompt": f"Futuristic digital cyber lock and puzzle pieces connecting smoothly, 3d render",
            "speaker_notes": f"Of course, there are challenges like cost and security, but smart engineers are actively solving them."
        },
        # Slide 8: What's Next in 2026+
        {
            "layout_type": "three_cards",
            "tag": "THE FUTURE",
            "title": "What's Coming Next in 2026+",
            "subtitle": "The Next Big Leap Forward",
            "bullet_points": [
                "🤖 **Autonomous AI Agents**: Systems that debug and optimize themselves 24/7.",
                "⚛️ **Quantum Convergence**: Blending quantum chips for exponential computing leaps.",
                "📱 **Pocket-Sized Power**: Running supercomputer models directly on your phone."
            ],
            "stat_or_highlight": "🔮 2026-2030 Horizon",
            "image_prompt": f"Futuristic digital horizon with flying autonomous drones and glowing neural networks, 3d render",
            "speaker_notes": f"Looking ahead to 2026 and beyond, we will see self-healing systems and supercomputers running on our phones."
        },
        # Final Slide: PURE THANK YOU ONLY (Zero keywords, zero takeaways!)
        {
            "layout_type": "thank_you",
            "tag": "THANK YOU",
            "title": "Thank You!",
            "subtitle": "Any Questions? Let's Discuss!",
            "formal_definition": "",
            "bullet_points": [], # Pure Thank You - No keyword pills or takeaways!
            "stat_or_highlight": "💬 Q&A Time",
            "image_prompt": "Celebratory minimal glowing presentation spotlight on dark stage",
            "speaker_notes": "Thank you so much for your time and attention! I'm happy to take any questions now."
        }
    ]

    selected = []
    # Always Slide 1 is Core Concept
    first_slide = dict(master_modules[0])
    first_slide["slide_number"] = 1
    selected.append(first_slide)

    middle_count = count - 2
    if middle_count > 0:
        available_middle = master_modules[1:-1]
        for i in range(middle_count):
            mod_idx = i % len(available_middle)
            slide_copy = dict(available_middle[mod_idx])
            slide_copy["slide_number"] = i + 2
            selected.append(slide_copy)

    # Always Last Slide is PURE THANK YOU
    if count > 1:
        closing_slide = dict(master_modules[-1])
        closing_slide["slide_number"] = count
        selected.append(closing_slide)

    return {
        "presentation_title": clean_topic,
        "presentation_subtitle": "Student Presentation Guide",
        "target_audience": education_level,
        "slides": selected
    }

def generate_presentation_with_gemini(topic: str, slide_count: int, education_level: str = "College", api_key: str = None) -> dict:
    """
    Calls Google Gemini for punchy student deck with Core Concept on slide 1 and pure Thank You on final slide.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key or len(key.strip()) < 10:
        print("[AIEngine] Using Clean Student Engine (Core Concept on Slide 1 & Pure Thank You).")
        return generate_academic_deep_deck(topic, slide_count, education_level)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key.strip()}"
    
    prompt = f"""
Create an exciting, clean, student-friendly presentation deck!
Topic: "{topic}"
Slide Count: {slide_count}

MANDATORY RULES:
1. SLIDE 1: Must feature a simple, easy-to-understand CORE CONCEPT definition in 'formal_definition'.
2. MIDDLE SLIDES: Exactly 2 to 3 short bullets (under 12 words each!). Easy plain wording.
3. FINAL SLIDE: PURE 'THANK YOU!' ONLY. Set 'bullet_points' to an empty array []. Do NOT include any summary takeaways, keywords, or bullet points on the final slide!
4. EMOJIS & STATS: Use emojis (⚡, 🚀, 🧠, 🛡️, 💡) and punchy highlight stats.

Output strictly valid JSON:
{{
  "presentation_title": "Catchy Title",
  "presentation_subtitle": "Student Guide",
  "target_audience": "{education_level}",
  "slides": [
    {{
      "slide_number": 1,
      "layout_type": "title",
      "tag": "CORE CONCEPT",
      "title": "Title",
      "subtitle": "Subtitle",
      "formal_definition": "What it is in simple words (1 easy sentence).",
      "bullet_points": ["🚀 **Key Idea**: Short punchy point."],
      "stat_or_highlight": "🚀 10x Faster",
      "image_prompt": "Clean futuristic illustration",
      "speaker_notes": "Simple 2-sentence script."
    }}
  ]
}}
"""

    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT}, {"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}
    }

    try:
        res = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
            cleaned = re.sub(r'\s*```$', '', cleaned)
            parsed = json.loads(cleaned)
            if "slides" in parsed and len(parsed["slides"]) > 0:
                # Ensure last slide has empty bullets
                parsed["slides"][-1]["bullet_points"] = []
                parsed["slides"][-1]["title"] = "Thank You!"
                parsed["slides"][-1]["subtitle"] = "Any Questions? Let's Discuss!"
                return parsed
    except Exception as e:
        print(f"[AIEngine] Gemini note: {e}")

    return generate_academic_deep_deck(topic, slide_count, education_level)
