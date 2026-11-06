/**
 * SlideCraft AI - Presentation Studio Controller
 * Academic presentation generator with 25-slide capacity, formal definition, deep theory, and background overlays.
 */

let currentPresentation = null;
let currentSlideIndex = 0;
let currentTheme = "cyber_emerald";
let includeBackground = true;

const THEME_STYLES = {
    cyber_emerald: {
        bg: "#0D1117",
        cardBg: "#161B22",
        cardBorder: "#30363D",
        textPrimary: "#F0F6FC",
        textSecondary: "#8B949E",
        accent: "#10B981"
    },
    academic_navy: {
        bg: "#0B132B",
        cardBg: "#1C2541",
        cardBorder: "#3A506B",
        textPrimary: "#FFFFFF",
        textSecondary: "#94A3B8",
        accent: "#48CAE4"
    },
    modern_minimalist: {
        bg: "#F8FAFC",
        cardBg: "#FFFFFF",
        cardBorder: "#E2E8F0",
        textPrimary: "#0F172A",
        textSecondary: "#64748B",
        accent: "#6366F1"
    },
    vibrant_sunset: {
        bg: "#1E112A",
        cardBg: "#2D1B3E",
        cardBorder: "#4E2B6B",
        textPrimary: "#FFFFFF",
        textSecondary: "#D1C4E9",
        accent: "#F43F5E"
    },
    ocean_cyan: {
        bg: "#071E26",
        cardBg: "#0D2E3A",
        cardBorder: "#1B4D5F",
        textPrimary: "#E0F2FE",
        textSecondary: "#7DD3FC",
        accent: "#06B6D4"
    }
};

document.addEventListener("DOMContentLoaded", () => {
    initThemeSelector();
    initPresetTopics();
    initEventListeners();
});

function initThemeSelector() {
    const cards = document.querySelectorAll(".theme-card");
    cards.forEach(card => {
        card.addEventListener("click", () => {
            cards.forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            currentTheme = card.dataset.theme;
            if (currentPresentation) {
                renderCurrentSlide();
            }
        });
    });
}

function initPresetTopics() {
    const pills = document.querySelectorAll(".preset-topic-pill");
    const input = document.getElementById("topicInput");
    pills.forEach(pill => {
        pill.addEventListener("click", () => {
            input.value = pill.innerText.replace(/^[^\w\s]+\s*/, '').trim();
            input.focus();
        });
    });
}

function initEventListeners() {
    document.getElementById("generateBtn").addEventListener("click", handleGenerateDeck);
    document.getElementById("prevSlideBtn").addEventListener("click", () => navigateSlide(-1));
    document.getElementById("nextSlideBtn").addEventListener("click", () => navigateSlide(1));
    document.getElementById("fullscreenBtn").addEventListener("click", toggleFullscreen);
    document.getElementById("downloadPptxBtn").addEventListener("click", handleDownloadPptx);

    document.addEventListener("keydown", (e) => {
        if (!currentPresentation) return;
        if (e.key === "ArrowLeft") navigateSlide(-1);
        if (e.key === "ArrowRight") navigateSlide(1);
    });
}

async function handleGenerateDeck() {
    const topic = document.getElementById("topicInput").value.trim();
    if (!topic) {
        alert("Please specify your presentation or research defense topic.");
        document.getElementById("topicInput").focus();
        return;
    }

    const slideCount = parseInt(document.getElementById("slideCountInput").value) || 10;
    const educationLevel = document.getElementById("eduLevelInput").value;
    const apiKey = document.getElementById("geminiKeyInput").value.trim();
    const includeImages = document.getElementById("toggleImages").checked;
    includeBackground = document.getElementById("toggleBackground").checked;
    const includeAnimations = document.getElementById("toggleAnimations").checked;

    const btn = document.getElementById("generateBtn");
    const originalBtnHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Synthesizing ${slideCount} Academic Slides...`;

    const progressDiv = document.getElementById("progressStatus");
    progressDiv.classList.remove("hidden");
    progressDiv.innerText = `Conducting theoretical literature review and assembling ${slideCount} structured slides...`;

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                topic: topic,
                slide_count: slideCount,
                education_level: educationLevel,
                theme: currentTheme,
                include_images: includeImages,
                include_background: includeBackground,
                include_animations: includeAnimations,
                gemini_api_key: apiKey || null
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Generation failed.");
        }

        const data = await response.json();
        currentPresentation = data.presentation;
        currentSlideIndex = 0;

        document.getElementById("studioPlaceholder").classList.add("hidden");
        document.getElementById("studioDeckSection").classList.remove("hidden");
        
        renderThumbnails();
        renderCurrentSlide();

        document.getElementById("studioDeckSection").scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        alert("Generation Error: " + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnHtml;
        progressDiv.classList.add("hidden");
    }
}

function navigateSlide(direction) {
    if (!currentPresentation || !currentPresentation.slides) return;
    const total = currentPresentation.slides.length;
    currentSlideIndex = Math.max(0, Math.min(currentSlideIndex + direction, total - 1));
    renderCurrentSlide();
}

function renderCurrentSlide() {
    if (!currentPresentation || !currentPresentation.slides) return;
    const slides = currentPresentation.slides;
    const slide = slides[currentSlideIndex];
    const theme = THEME_STYLES[currentTheme] || THEME_STYLES["cyber_emerald"];

    document.getElementById("slideCounter").innerText = `Slide ${currentSlideIndex + 1} of ${slides.length}`;
    document.getElementById("deckMainTitle").innerText = currentPresentation.presentation_title || "Research Presentation";
    document.getElementById("speakerNotesContent").innerText = slide.speaker_notes || "No presenter script for this slide.";

    const stage = document.getElementById("slideStage");
    
    // Background Wallpaper
    const bgUrl = slide.preview_bg_url || "";
    const bgStyle = (includeBackground && bgUrl) 
        ? `background: linear-gradient(rgba(10, 15, 26, 0.88), rgba(10, 15, 26, 0.94)), url('${bgUrl}') center/cover no-repeat;` 
        : `background: ${theme.bg};`;

    stage.setAttribute("style", bgStyle);
    stage.style.color = theme.textPrimary;

    const tag = slide.tag || "RESEARCH MODULE";
    const title = slide.title || "";
    const subtitle = slide.subtitle || "";
    const bullets = slide.bullet_points || [];
    const stat = slide.stat_or_highlight || "";
    const imgUrl = slide.preview_image_url || "";
    const formalDef = slide.formal_definition || "";
    const closingMsg = slide.closing_message || "";

    const formattedBullets = bullets.map(b => {
        if (b.includes("**")) {
            return b.replace(/\*\*(.*?)\*\*/g, `<strong style="color:${theme.accent}">$1</strong>`);
        }
        return b;
    }).map(b => `<li class="mb-2.5 flex items-start gap-2.5 text-xs md:text-sm"><span style="color:${theme.accent}" class="mt-0.5">•</span><span>${b}</span></li>`).join("");

    let contentHtml = "";

    // =========================================================
    // SLIDE 1: FORMAL CONCEPT DEFINITION & RESEARCH SCOPE
    // =========================================================
    if (currentSlideIndex === 0 || slide.layout_type === "title") {
        contentHtml = `
            <div class="h-full w-full p-8 md:p-12 flex flex-col justify-between slide-content-active">
                <div>
                    <span class="inline-block px-3 py-1 rounded text-xs font-bold tracking-wider mb-3 uppercase" style="background:${theme.accent}; color:${theme.bg}">
                        ${tag}
                    </span>
                    <h1 class="text-3xl md:text-4xl font-black tracking-tight" style="color:${theme.textPrimary}">${title}</h1>
                    <p class="text-xs md:text-sm font-medium mt-1" style="color:${theme.textSecondary}">${subtitle}</p>

                    <!-- Formal Academic Definition Box -->
                    <div class="mt-4 p-4 rounded-xl border" style="background:${theme.cardBg}; border-color:${theme.accent}; box-shadow: 0 0 15px rgba(16, 185, 129, 0.15)">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider block mb-1" style="color:${theme.accent}">
                            📖 FORMAL ACADEMIC DEFINITION & PREMISE:
                        </span>
                        <p class="text-xs md:text-sm leading-relaxed" style="color:${theme.textPrimary}">
                            ${formalDef || "Systematic theoretical and engineering framework governing mathematical abstraction, computational pipeline optimization, and deterministic evaluation criteria."}
                        </p>
                    </div>
                </div>

                <!-- Theoretical Agenda Breakdown -->
                <div class="p-4 rounded-xl border mt-3" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                    <ul class="space-y-1">
                        ${formattedBullets}
                    </ul>
                </div>

                <div class="flex items-center justify-between text-xs mt-3 pt-2 border-t border-gray-800" style="color:${theme.textSecondary}">
                    <span>${currentPresentation.target_audience || "Doctoral & Master's Defense"}</span>
                    ${stat ? `<span class="px-3 py-1 rounded-full font-bold" style="border: 1px solid ${theme.accent}; color:${theme.accent}">★ ${stat}</span>` : ""}
                </div>
            </div>
        `;
    }
    // =========================================================
    // FINAL SLIDE: DEDICATED CLOSING & THANK YOU / Q&A
    // =========================================================
    else if (currentSlideIndex === slides.length - 1 || slide.layout_type === "thank_you") {
        contentHtml = `
            <div class="h-full w-full p-8 md:p-12 flex flex-col justify-between slide-content-active text-center" style="background: radial-gradient(circle at center, ${theme.cardBg} 0%, rgba(10, 15, 26, 0.95) 100%);">
                <div>
                    <span class="inline-block px-3 py-1 rounded text-xs font-bold tracking-wider mb-3 uppercase" style="background:${theme.accent}; color:${theme.bg}">
                        DEFENSE CONCLUSION & ACKNOWLEDGMENTS
                    </span>
                    <h2 class="text-3xl md:text-5xl font-black tracking-tight" style="color:${theme.textPrimary}">
                        Thank You for Your Time & Attention
                    </h2>
                    <p class="text-sm md:text-lg font-medium mt-2" style="color:${theme.accent}">
                        Floor is now Open for Questions, Academic Inquiries & Constructive Feedback
                    </p>
                </div>

                <!-- Courteous Closing Note -->
                <div class="max-w-2xl mx-auto p-5 rounded-xl border text-left" style="background:${theme.cardBg}; border-color:${theme.accent}">
                    <p class="text-xs md:text-sm leading-relaxed italic" style="color:${theme.textPrimary}">
                        "${closingMsg || "We express our sincere gratitude to our academic mentors, thesis advisory committee, and fellow researchers whose guidance has made this investigation possible."}"
                    </p>
                </div>

                <!-- Key Takeaways Recap -->
                <div class="max-w-3xl mx-auto text-left p-4 rounded-xl border" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                    <ul class="space-y-1">
                        ${formattedBullets}
                    </ul>
                </div>

                <div class="flex items-center justify-center gap-3">
                    <span class="px-5 py-2 rounded-xl text-xs font-extrabold uppercase tracking-wider" style="background:${theme.accent}; color:${theme.bg}">
                        💬 OPEN FOR QUESTIONS & DISCUSSION (Q&A)
                    </span>
                </div>
            </div>
        `;
    }
    // =========================================================
    // STANDARD / DEEP THEORY CONTENT SLIDES
    // =========================================================
    else {
        contentHtml = `
            <div class="h-full w-full p-6 md:p-8 flex flex-col justify-between slide-content-active">
                <!-- Header -->
                <div>
                    <span class="inline-block px-2.5 py-0.5 rounded text-[11px] font-bold tracking-wider mb-1 uppercase" style="background:${theme.accent}; color:${theme.bg}">
                        ${tag}
                    </span>
                    <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight" style="color:${theme.textPrimary}">${title}</h2>
                    ${subtitle ? `<p class="text-xs mt-1" style="color:${theme.textSecondary}">${subtitle}</p>` : ""}
                </div>

                <!-- Main Content Grid -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto items-stretch">
                    <div class="md:col-span-7 p-5 rounded-xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <ul class="space-y-1.5">
                            ${formattedBullets}
                        </ul>
                        ${stat ? `
                            <div class="mt-3 p-2 rounded-lg text-xs font-bold text-center border" style="background:${theme.bg}; border-color:${theme.accent}; color:${theme.accent}">
                                💡 Empirical Benchmark: ${stat}
                            </div>
                        ` : ""}
                    </div>

                    <div class="md:col-span-5 rounded-xl overflow-hidden border relative flex items-center justify-center min-h-[220px]" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <img src="${imgUrl}" alt="${title}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80'"/>
                    </div>
                </div>

                <div class="text-right text-xs" style="color:${theme.textSecondary}">
                    ${currentSlideIndex + 1} / ${slides.length}
                </div>
            </div>
        `;
    }

    stage.innerHTML = contentHtml;
    highlightActiveThumbnail();
}

function renderThumbnails() {
    const container = document.getElementById("thumbnailStrip");
    container.innerHTML = "";

    if (!currentPresentation || !currentPresentation.slides) return;

    currentPresentation.slides.forEach((slide, idx) => {
        const thumb = document.createElement("div");
        thumb.className = `cursor-pointer rounded-lg p-2 border text-left transition-all ${idx === currentSlideIndex ? 'ring-2 ring-emerald-500 border-emerald-500' : 'border-gray-800 bg-gray-900/70 opacity-70 hover:opacity-100'}`;
        thumb.style.minWidth = "150px";
        thumb.innerHTML = `
            <div class="text-[10px] font-bold text-emerald-400">#${idx + 1} ${slide.tag || "MODULE"}</div>
            <div class="text-xs font-semibold truncate text-white mt-1">${slide.title || "Untitled"}</div>
        `;
        thumb.addEventListener("click", () => {
            currentSlideIndex = idx;
            renderCurrentSlide();
        });
        container.appendChild(thumb);
    });
}

function highlightActiveThumbnail() {
    const thumbs = document.querySelectorAll("#thumbnailStrip > div");
    thumbs.forEach((t, i) => {
        if (i === currentSlideIndex) {
            t.className = "cursor-pointer rounded-lg p-2 border text-left transition-all ring-2 ring-emerald-500 border-emerald-500 bg-gray-800";
            t.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
        } else {
            t.className = "cursor-pointer rounded-lg p-2 border text-left transition-all border-gray-800 bg-gray-900/70 opacity-70 hover:opacity-100";
        }
    });
}

async function handleDownloadPptx() {
    if (!currentPresentation) return;

    const btn = document.getElementById("downloadPptxBtn");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Compiling PPTX Deck...`;

    try {
        const includeImages = document.getElementById("toggleImages").checked;
        const res = await fetch("/api/export-pptx", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                presentation_data: currentPresentation,
                theme: currentTheme,
                include_images: includeImages,
                include_background: includeBackground
            })
        });

        if (!res.ok) {
            throw new Error("Failed to compile PowerPoint file.");
        }

        const data = await res.json();
        const a = document.createElement("a");
        a.href = data.download_url;
        a.download = `${currentPresentation.presentation_title || 'Academic_Presentation'}.pptx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

    } catch (e) {
        alert("Download Error: " + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

function toggleFullscreen() {
    const stage = document.getElementById("slideStage");
    if (!document.fullscreenElement) {
        stage.requestFullscreen().catch(err => {
            alert(`Fullscreen error: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}
