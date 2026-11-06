"""
AI Engine for Student PPT Maker.
Uses Google Gemini 2.0/1.5 Flash for intelligent structured slide generation.
Includes a rich Offline Fallback Engine for instant zero-key student presentations.
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an award-winning academic presentation designer and professor.
Your job is to create visually compelling, highly accurate, and student-ready presentation decks.

Rules for high scoring student presentations:
1. NO generic boring walls of text. Use punchy, high-impact bullet points with bold lead-ins (e.g. "**Concept Name**: Explanation").
2. Include realistic statistics or highlight metrics where applicable.
3. Provide realistic, natural speaker notes for each slide (what the student should actually say during presentation/viva).
4. Provide descriptive visual image prompts (for 3D renders/academic diagrams).
5. Output strictly in JSON format matching the requested schema.
"""

def get_fallback_presentation(topic: str, slide_count: int, education_level: str = "College") -> dict:
    """
    Intelligent zero-key offline generator.
    Guarantees students always get a high-quality presentation instantly.
    """
    clean_topic = topic.strip().title()
    
    # Archetype layout templates
    templates = [
        {
            "layout_type": "title",
            "tag": "OVERVIEW",
            "title": f"{clean_topic}",
            "subtitle": f"A Comprehensive Academic Study & Future Perspectives",
            "bullet_points": [
                f"**Scope & Relevance**: Why {clean_topic} is vital in {education_level} education and modern industry.",
                "**Core Objectives**: Understanding fundamental principles, architectures, and real-world impact.",
                "**Presentation Roadmap**: Foundations, practical case studies, challenges, and future innovations."
            ],
            "stat_or_highlight": "Academic Year 2026",
            "image_prompt": f"Modern futuristic scientific concept representation of {clean_topic}, clean 3d render, glowing aesthetics",
            "gif_query": f"{clean_topic} technology innovation",
            "speaker_notes": f"Welcome everyone. Today, I will be presenting our research and analysis on {clean_topic}, examining its core principles and future relevance."
        },
        {
            "layout_type": "split_image_right",
            "tag": "BACKGROUND & FOUNDATION",
            "title": f"The Evolution & Significance of {clean_topic}",
            "subtitle": "Historical Context & Modern Transformation",
            "bullet_points": [
                "**Historical Roots**: Early paradigms and limitations of legacy approaches.",
                f"**Technological Breakthroughs**: How rapid advancements elevated {clean_topic} to mainstream importance.",
                "**Critical Significance**: Solving bottlenecks in performance, scalability, and efficiency."
            ],
            "stat_or_highlight": "85% Adoption Growth",
            "image_prompt": f"Infographic concept of evolution and milestones in {clean_topic}, crisp digital diagram, 3d render",
            "gif_query": "timeline progress development",
            "speaker_notes": f"To understand where we are today, we must look at how {clean_topic} emerged from initial theoretical models into a practical global solution."
        },
        {
            "layout_type": "three_cards",
            "tag": "CORE ARCHITECTURE",
            "title": f"Key Pillars & Mechanisms",
            "subtitle": "The Foundational Components Driving the System",
            "bullet_points": [
                "**Structural Design**: Modular architecture ensuring reliable execution and fail-safe redundancy.",
                "**Data Flow & Processing**: Low-latency transmission pipelines optimized for high-throughput computing.",
                "**Control Logic**: Algorithmic decision-making governed by strict validation rules."
            ],
            "stat_or_highlight": "3 Core Pillars",
            "image_prompt": f"3D blueprint schematic diagram showing inner mechanics of {clean_topic}, neon cyan and slate blue",
            "gif_query": "technology gears mechanism loop",
            "speaker_notes": f"Here we break down the operational architecture into three indispensable components that allow {clean_topic} to function reliably."
        },
        {
            "layout_type": "split_image_left",
            "tag": "PRACTICAL IMPLEMENTATION",
            "title": f"Real-World Applications & Use Cases",
            "subtitle": "Translating Theory into Tangible Industry Solutions",
            "bullet_points": [
                "**Industry Integration**: Automated workflows saving thousands of engineering hours.",
                "**Data-Driven Outcomes**: Enhancing predictive accuracy and operational decision-making.",
                "**End-User Impact**: Delivering seamless, scalable services across enterprise and community domains."
            ],
            "stat_or_highlight": "10x Efficiency Gain",
            "image_prompt": f"Modern industrial laboratory using {clean_topic} in real life, clean 3d render, isometric perspective",
            "gif_query": "futuristic laboratory scientist working",
            "speaker_notes": f"In this slide, let us explore actual deployment scenarios where {clean_topic} delivers measurable benefits and high return on effort."
        },
        {
            "layout_type": "split_image_right",
            "tag": "CHALLENGES & LIMITATIONS",
            "title": "Critical Challenges & Ethical Considerations",
            "subtitle": "Addressing Constraints and Safety Protocols",
            "bullet_points": [
                "**Resource Overhead**: Balancing high computational costs with energy efficiency.",
                "**Security & Privacy**: Mitigating vulnerabilities and preserving strict compliance standards.",
                "**Algorithmic Transparency**: Ensuring auditable outcomes and minimizing unintended bias."
            ],
            "stat_or_highlight": "Top Priority: Security",
            "image_prompt": f"Digital shield and data protection lock abstract concept for {clean_topic}, 3d render",
            "gif_query": "cyber security digital lock shield",
            "speaker_notes": f"No technology comes without trade-offs. It is essential for researchers to address key bottlenecks such as cost, security, and ethical stewardship."
        },
        {
            "layout_type": "quote_stat",
            "tag": "PERFORMANCE METRICS",
            "title": "Benchmark Results & Empirical Findings",
            "subtitle": "Demonstrating Quantitative Improvements",
            "bullet_points": [
                "**Latency Reduction**: Average response times dropping by more than 60% in controlled stress tests.",
                "**Resource Utilization**: Optimized memory footprints enabling deployment on standard hardware.",
                "**Accuracy & Stability**: Consistent performance exceeding legacy baselines across all test sets."
            ],
            "stat_or_highlight": "99.4% Uptime & Reliability",
            "image_prompt": f"Glowing 3D holographic bar charts and data visualization graphics, futuristic analytics dashboard",
            "gif_query": "analytics chart rising data",
            "speaker_notes": f"Our comparative empirical data confirms that modern implementations deliver superior reliability and throughput under heavy loads."
        },
        {
            "layout_type": "three_cards",
            "tag": "FUTURE HORIZONS",
            "title": f"Next Frontier: The Future of {clean_topic}",
            "subtitle": "Emerging Trends and Next-Generation Innovations",
            "bullet_points": [
                "**Autonomous Systems**: Integration with self-learning neural engines for zero-touch optimization.",
                "**Cross-Disciplinary Synergy**: Merging with quantum computing and IoT edge ecosystems.",
                "**Global Standardization**: Establishing international protocols for interoperability and safety."
            ],
            "stat_or_highlight": "Next 5-Year Horizon",
            "image_prompt": f"Visionary futuristic cityscape with flying autonomous drones and interconnected glowing networks 3d render",
            "gif_query": "futuristic city network connection",
            "speaker_notes": f"Looking ahead, the convergence of {clean_topic} with autonomous architectures will redefine what is possible in the coming decade."
        },
        {
            "layout_type": "summary_quiz",
            "tag": "CONCLUSION & SUMMARY",
            "title": "Summary & Key Takeaways",
            "subtitle": "Final Thoughts and Open Discussion",
            "bullet_points": [
                f"**Paradigm Shift**: {clean_topic} represents a fundamental leap forward in contemporary technology.",
                "**Continuous Learning**: Ongoing research is rapidly eliminating initial constraints and scaling adoption.",
                "**Actionable Next Steps**: Continued development of open-source frameworks and educational curricula."
            ],
            "stat_or_highlight": "Thank You / Q&A",
            "image_prompt": f"Minimalist sleek modern graduation cap and knowledge lightbulb icon glowing on dark slate, 3d render",
            "gif_query": "applause presentation thank you",
            "speaker_notes": f"In conclusion, {clean_topic} provides a transformative foundation for our future. Thank you for your time, and I now welcome any questions."
        }
    ]

    selected_slides = []
    # If student requests fewer or more slides, adapt gracefully
    total_templates = len(templates)
    for i in range(slide_count):
        idx = min(i, total_templates - 1) if i < total_templates - 1 else (total_templates - 1 if i == slide_count - 1 else i % (total_templates - 1))
        slide_copy = dict(templates[idx])
        slide_copy["slide_number"] = i + 1
        selected_slides.append(slide_copy)

    # Ensure last slide is conclusion
    if slide_count > 1 and selected_slides[-1]["tag"] != "CONCLUSION & SUMMARY":
        conclusion = dict(templates[-1])
        conclusion["slide_number"] = slide_count
        selected_slides[-1] = conclusion

    return {
        "presentation_title": clean_topic,
        "presentation_subtitle": f"Academic Research & Analysis — {education_level} Level",
        "target_audience": education_level,
        "slides": selected_slides
    }

def generate_presentation_with_gemini(topic: str, slide_count: int, education_level: str = "College", api_key: str = None) -> dict:
    """
    Calls Google Gemini API for custom high-intelligence presentation.
    Falls back safely to the offline engine if API key is invalid or absent.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key or len(key.strip()) < 10:
        print("[AIEngine] No Gemini API key provided. Using Smart Offline Template Engine.")
        return get_fallback_presentation(topic, slide_count, education_level)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key.strip()}"
    
    prompt = f"""
Create a highly professional academic presentation deck for a {education_level} student.
Topic: "{topic}"
Exact Number of Slides: {slide_count}

Output MUST be a single valid JSON object following this EXACT schema:
{{
  "presentation_title": "Short Catchy Main Title",
  "presentation_subtitle": "Descriptive academic subtitle",
  "target_audience": "{education_level}",
  "slides": [
    {{
      "slide_number": 1,
      "layout_type": "title",
      "tag": "ONE WORD BADGE (e.g. OVERVIEW, MECHANISM, APPLICATION, CONCLUSION)",
      "title": "Clear Slide Heading",
      "subtitle": "Short descriptive slide sub-heading",
      "bullet_points": [
        "**Specific Concept**: Concrete explanation with student-friendly depth.",
        "**Key Mechanism**: Clear, non-fluffy bullet point with bold lead-in.",
        "**Critical Insight**: Data-backed or analytical observation."
      ],
      "stat_or_highlight": "Memorable metric or phrase (e.g. '10x Speed', '99.8% Precision', 'Key Takeaway')",
      "image_prompt": "Detailed visual prompt for high quality 3d render/infographic illustration",
      "gif_query": "3-word keyword for finding matching animated GIF",
      "speaker_notes": "2-3 natural sentences guiding the student on what to say to the audience."
    }}
  ]
}}

Requirements:
- Exactly {slide_count} slides in the 'slides' array.
- Slide 1 must be an engaging Title/Introduction slide.
- Slide {slide_count} must be a conclusive Takeaway/Summary slide.
- Middle slides must vary in layout_type: use 'split_image_left', 'split_image_right', 'three_cards', 'quote_stat'.
- Use factual, student-appropriate information for the topic "{topic}".
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4
        }
    }

    try:
        res = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Clean up markdown code fence if present
            cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
            cleaned = re.sub(r'\s*```$', '', cleaned)
            parsed = json.loads(cleaned)
            if "slides" in parsed and len(parsed["slides"]) > 0:
                print(f"[AIEngine] Successfully generated {len(parsed['slides'])} slides via Gemini API!")
                return parsed
        else:
            print(f"[AIEngine] Gemini API Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[AIEngine] Error calling Gemini: {e}")

    # Seamless fallback
    print("[AIEngine] Falling back to offline generator.")
    return get_fallback_presentation(topic, slide_count, education_level)
