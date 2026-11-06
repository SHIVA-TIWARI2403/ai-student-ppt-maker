"""
High-Impact, Punchy Student AI Engine for SlideCraft AI.
Generates crazy cool, student-friendly presentations up to 25 slides:
- Short, crisp, easy-to-understand plain English (NO heavy essay text!)
- Simple, high-clarity concept definition on Slide 1
- High-impact highlight statistics on every slide
- Crazy cool Thank You & Q&A closing slide
- Conversational presenter scripts for confident student viva/presentations
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an award-winning creative presentation designer known for making complex topics super simple, crazy cool, and easy to present.

CORE DESIGN RULES:
1. SHORT & PUNCHY: Maximum 2 to 3 bullet points per slide. Keep each bullet under 10 to 14 words!
2. EASY PLAIN WORDING: Write in clear, engaging, conversational English. Zero boring academic jargon walls!
3. SLIDE 1 CONCEPT DEFINITION:
   - Provide a clear, simple 1-sentence definition: "What is it in simple words?"
4. FINAL SLIDE:
   - Dedicated "Thank You & Q&A" slide with an energetic closing and invitation for questions.
5. CRAZY STATS & EMOJIS: Use emojis (⚡, 🚀, 🧠, 🛡️, 💡) and punchy highlight stats on every slide.
6. OUTPUT FORMAT: Strictly valid JSON matching the schema.
"""

def generate_academic_deep_deck(topic: str, slide_count: int, education_level: str = "College") -> dict:
    """
    Punchy, student-friendly generator up to 25 slides with easy wording and high visual impact.
    """
    clean_topic = topic.strip().title()
    count = max(3, min(slide_count, 25))

    master_modules = [
        # Slide 1: Concept Definition & Intro
        {
            "layout_type": "title",
            "tag": "CORE CONCEPT",
            "title": f"{clean_topic}",
            "subtitle": "The Ultimate Student Guide: Concepts, Superpowers & Future Impact",
            "formal_definition": f"In simple words, {clean_topic} is a breakthrough technology that replaces slow traditional systems with super-smart, automated processing to solve complex problems in seconds.",
            "bullet_points": [
                f"🚀 **The Big Idea**: Why {clean_topic} is changing the world right now.",
                "⚡ **Superpowers**: How it computes and automates at lightning speed.",
                "🎯 **What We'll Cover**: Key basics, real-world magic, and future trends."
            ],
            "stat_or_highlight": "🚀 Next-Gen Tech 2026",
            "image_prompt": f"Futuristic glowing conceptual 3d illustration of {clean_topic}, neon cyan and emerald, ultra-clean",
            "speaker_notes": f"Hi everyone! Today we are exploring {clean_topic}. In simple words, it's all about making systems faster, smarter, and scalable."
        },
        # Slide 2: Why It Matters
        {
            "layout_type": "split_image_right",
            "tag": "THE BIG WHY",
            "title": f"Why Everyone is Talking About It",
            "subtitle": "The Old Way vs. The New Super-Smart Way",
            "bullet_points": [
                "🐢 **The Old Bottleneck**: Traditional methods were slow, expensive, and broke under pressure.",
                "⚡ **The Modern Breakthrough**: {clean_topic} solves in minutes what used to take weeks.",
                "💡 **Massive Impact**: Millions of users benefit every single day."
            ],
            "stat_or_highlight": "⚡ 10x Faster Results",
            "image_prompt": f"Comparison visual between old technology and futuristic glowing {clean_topic}, clean 3d render",
            "speaker_notes": f"Why does this matter to us? Because old systems were too slow. {clean_topic} changes the game by speeding up everything."
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
                "📈 **Scalability**: Handles 1 user or 100 million users without slowing down."
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
        # Slide 9: Top 3 Takeaways
        {
            "layout_type": "deep_theory",
            "tag": "SUMMARY",
            "title": "Top 3 Things to Remember",
            "subtitle": "The Short Summary for Your Exam & Viva",
            "bullet_points": [
                f"💡 **1. Core Concept**: {clean_topic} replaces slow legacy models with super-fast automation.",
                "⚡ **2. Huge Wins**: Delivers 10x speed, 99.9% reliability, and cuts energy waste.",
                "🚀 **3. The Future**: High student career demand across AI, software, and research."
            ],
            "stat_or_highlight": "🎯 100% Exam Ready",
            "image_prompt": f"Golden shiny glowing lightbulb and graduation star on dark glass pedestal, 3d render",
            "speaker_notes": f"If you remember just three things today: it's fast, it's reliable, and it's where the best future careers are."
        },
        # Slide 10: Final Thank You & Q&A Slide
        {
            "layout_type": "thank_you",
            "tag": "THAT'S A WRAP",
            "title": "Thank You! Time for Q&A!",
            "subtitle": "Questions? Ideas? Let's Discuss!",
            "closing_message": "Huge thanks to our teachers, mentors, and classmates for listening! Now let's open the floor.",
            "bullet_points": [
                f"🎓 **Topic Wrapped**: {clean_topic} — Mastered!",
                "💬 **Open Floor**: Ask me anything about the concepts or implementation.",
                "📂 **Slides & Code**: Ready to download and explore anytime."
            ],
            "stat_or_highlight": "🎉 Ask Me Anything!",
            "image_prompt": f"Celebratory sleek auditorium with glowing spotlight on presentation stage, modern minimalist 3d render",
            "speaker_notes": f"Thank you so much everyone for your time! I'd love to take any questions or thoughts you have right now."
        }
    ]

    # Dynamically scale up to count requested
    selected = []
    # Always Slide 1 is Definition/Intro
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

    # Always Last Slide is Thank You
    if count > 1:
        closing_slide = dict(master_modules[-1])
        closing_slide["slide_number"] = count
        selected.append(closing_slide)

    return {
        "presentation_title": clean_topic,
        "presentation_subtitle": "Student Presentation Guide — Concepts, Superpowers & Real-World Impact",
        "target_audience": education_level,
        "slides": selected
    }

def generate_presentation_with_gemini(topic: str, slide_count: int, education_level: str = "College", api_key: str = None) -> dict:
    """
    Calls Google Gemini for punchy, crazy cool, student-friendly slide generation.
    Falls back to the punchy offline student engine.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key or len(key.strip()) < 10:
        print("[AIEngine] Using Punchy Student Slide Engine (Easy Plain English).")
        return generate_academic_deep_deck(topic, slide_count, education_level)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key.strip()}"
    
    prompt = f"""
Create an exciting, ultra-engaging, student-friendly presentation deck!
Topic: "{topic}"
Slide Count: {slide_count}

CRITICAL RULES:
1. NO HEAVY PARAGRAPHS: Max 2 to 3 short bullet points per slide (under 12 words each!).
2. EASY PLAIN WORDING: Write in clear, modern, punchy English that students can understand and present effortlessly.
3. SLIDE 1 MUST HAVE A SIMPLE CONCEPT DEFINITION:
   - 'formal_definition': "What is it in simple words?" (1 short crystal-clear sentence).
4. LAST SLIDE MUST BE A FUN THANK YOU / Q&A SLIDE:
   - Title: "Thank You! Time for Q&A!"
   - Subtitle: "Any Questions? Fire Away!"
5. EMOJIS & STATS: Use relevant emojis (⚡, 🚀, 🧠, 🛡️, 💡) and crazy cool highlight stats on every slide.

Output strictly valid JSON matching this schema:
{{
  "presentation_title": "Short Catchy Title",
  "presentation_subtitle": "Simple student subtitle",
  "target_audience": "{education_level}",
  "slides": [
    {{
      "slide_number": 1,
      "layout_type": "title",
      "tag": "CORE CONCEPT",
      "title": "Catchy Heading",
      "subtitle": "Short subtitle",
      "formal_definition": "What it is in simple words (1 easy sentence).",
      "bullet_points": [
        "🚀 **Key Idea**: Short punchy point under 12 words.",
        "⚡ **Superpower**: Another short clear point."
      ],
      "stat_or_highlight": "🚀 10x Faster",
      "image_prompt": "Clean futuristic 3d illustration",
      "speaker_notes": "Simple 2-sentence script for what the student should say."
    }}
  ]
}}
"""

    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT}, {"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.4}
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
                print(f"[AIEngine] Generated {len(parsed['slides'])} punchy slides via Gemini!")
                return parsed
    except Exception as e:
        print(f"[AIEngine] Gemini note: {e}")

    return generate_academic_deep_deck(topic, slide_count, education_level)
