/**
 * SlideCraft AI - Punchy Student Bento Studio Controller
 * Modern Outfit typography, short easy-to-read bullets, zero clutter, and clean visuals.
 */

let currentPresentation = null;
let currentSlideIndex = 0;
let currentTheme = "cyber_emerald";
let includeBackground = true;
let currentViewMode = "deck";

const THEME_STYLES = {
    cyber_emerald: {
        bg: "#07090E",
        cardBg: "#111622",
        cardBorder: "rgba(255, 255, 255, 0.08)",
        textPrimary: "#F8FAFC",
        textSecondary: "#94A3B8",
        accent: "#10B981"
    },
    academic_navy: {
        bg: "#080E1C",
        cardBg: "#10192D",
        cardBorder: "rgba(255, 255, 255, 0.08)",
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
        bg: "#160C22",
        cardBg: "#221334",
        cardBorder: "rgba(255, 255, 255, 0.08)",
        textPrimary: "#FFFFFF",
        textSecondary: "#D1C4E9",
        accent: "#F43F5E"
    },
    ocean_cyan: {
        bg: "#051720",
        cardBg: "#0B222E",
        cardBorder: "rgba(255, 255, 255, 0.08)",
        textPrimary: "#E0F2FE",
        textSecondary: "#7DD3FC",
        accent: "#06B6D4"
    }
};

document.addEventListener("DOMContentLoaded", () => {
    initThemeSelector();
    initPresetTopics();
    initEventListeners();
    initViewModeSwitch();
});

function initViewModeSwitch() {
    const deckBtn = document.getElementById("viewDeckBtn");
    const docBtn = document.getElementById("viewDocBtn");
    if (!deckBtn || !docBtn) return;

    deckBtn.addEventListener("click", () => {
        currentViewMode = "deck";
        deckBtn.className = "px-3.5 py-1.5 rounded-lg bg-emerald-500 text-white font-bold transition flex items-center gap-1.5 shadow-sm";
        docBtn.className = "px-3.5 py-1.5 rounded-lg text-gray-400 hover:text-white transition flex items-center gap-1.5";
        document.getElementById("stageContainerWrapper").classList.remove("hidden");
        document.getElementById("documentContainerWrapper").classList.add("hidden");
        renderCurrentSlide();
    });

    docBtn.addEventListener("click", () => {
        currentViewMode = "document";
        docBtn.className = "px-3.5 py-1.5 rounded-lg bg-emerald-500 text-white font-bold transition flex items-center gap-1.5 shadow-sm";
        deckBtn.className = "px-3.5 py-1.5 rounded-lg text-gray-400 hover:text-white transition flex items-center gap-1.5";
        document.getElementById("stageContainerWrapper").classList.add("hidden");
        document.getElementById("documentContainerWrapper").classList.remove("hidden");
        renderContinuousDocument();
    });
}

function initThemeSelector() {
    const cards = document.querySelectorAll(".theme-card");
    cards.forEach(card => {
        card.addEventListener("click", () => {
            cards.forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            currentTheme = card.dataset.theme;
            if (currentPresentation) {
                if (currentViewMode === "deck") {
                    renderCurrentSlide();
                } else {
                    renderContinuousDocument();
                }
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
        if (!currentPresentation || currentViewMode !== "deck") return;
        if (e.key === "ArrowLeft") navigateSlide(-1);
        if (e.key === "ArrowRight") navigateSlide(1);
    });
}

async function handleGenerateDeck() {
    const topic = document.getElementById("topicInput").value.trim();
    if (!topic) {
        alert("Please enter a presentation topic.");
        document.getElementById("topicInput").focus();
        return;
    }

    const slideCount = parseInt(document.getElementById("slideCountInput").value) || 8;
    const educationLevel = document.getElementById("eduLevelInput").value;
    const apiKey = document.getElementById("geminiKeyInput").value.trim();
    const includeImages = document.getElementById("toggleImages").checked;
    includeBackground = document.getElementById("toggleBackground").checked;
    const includeAnimations = document.getElementById("toggleAnimations").checked;

    const btn = document.getElementById("generateBtn");
    const originalBtnHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Generating Punchy Cards...`;

    const progressDiv = document.getElementById("progressStatus");
    progressDiv.classList.remove("hidden");
    progressDiv.innerText = `Crafting ${slideCount} punchy, easy-to-read Bento cards...`;

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
        document.getElementById("viewModeContainer").classList.remove("hidden");
        document.getElementById("totalCardsCountBadge").innerText = `${currentPresentation.slides.length} CARDS`;

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

function formatBullets(bullets, theme) {
    return bullets.map(b => {
        if (b.includes("**")) {
            return b.replace(/\*\*(.*?)\*\*/g, `<strong class="font-bold text-white">$1</strong>`);
        }
        return b;
    }).map(b => `<li class="mb-3 flex items-start gap-3 text-sm md:text-base"><span class="text-emerald-400 font-bold mt-0.5">•</span><span>${b}</span></li>`).join("");
}

function renderCurrentSlide() {
    if (!currentPresentation || !currentPresentation.slides) return;
    const slides = currentPresentation.slides;
    const slide = slides[currentSlideIndex];
    const theme = THEME_STYLES[currentTheme] || THEME_STYLES["cyber_emerald"];

    document.getElementById("slideCounter").innerText = `Slide ${currentSlideIndex + 1} of ${slides.length}`;
    document.getElementById("deckMainTitle").innerText = currentPresentation.presentation_title || "Presentation";
    document.getElementById("speakerNotesContent").innerText = slide.speaker_notes || "No presenter script for this slide.";

    const stage = document.getElementById("slideStage");
    stage.style.background = theme.bg;
    stage.style.color = theme.textPrimary;

    const tag = slide.tag || "OVERVIEW";
    const title = slide.title || "";
    const subtitle = slide.subtitle || "";
    const bullets = slide.bullet_points || [];
    const stat = slide.stat_or_highlight || "";
    const imgUrl = slide.preview_image_url || "";
    const formalDef = slide.formal_definition || "";
    const closingMsg = slide.closing_message || "";

    const formattedBullets = formatBullets(bullets, theme);

    let contentHtml = "";

    // =========================================================================
    // SLIDE 1: HERO CONCEPT DEFINITION (EASY PLAIN ENGLISH)
    // =========================================================================
    if (currentSlideIndex === 0 || slide.layout_type === "title") {
        contentHtml = `
            <div class="h-full w-full p-8 md:p-11 flex flex-col justify-between gamma-active-slide">
                <!-- Header -->
                <div>
                    <span class="gamma-pill mb-2">${tag}</span>
                    <h1 class="text-3xl md:text-5xl font-black tracking-tight" style="color:${theme.textPrimary}">${title}</h1>
                    <p class="text-xs md:text-sm mt-1 font-medium" style="color:${theme.textSecondary}">${subtitle}</p>
                </div>

                <!-- Bento Grid -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 my-auto items-stretch">
                    
                    <!-- Left: Simple Concept Box -->
                    <div class="md:col-span-7 p-6 rounded-2xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <div>
                            <!-- Simple Plain English Concept Box -->
                            <div class="p-4 rounded-xl border mb-4" style="background:rgba(16, 185, 129, 0.08); border-color:${theme.accent}">
                                <span class="text-[11px] font-extrabold uppercase tracking-wider block mb-1" style="color:${theme.accent}">
                                    💡 IN SIMPLE WORDS:
                                </span>
                                <p class="text-sm md:text-base font-semibold leading-relaxed" style="color:${theme.textPrimary}">
                                    ${formalDef || "A super-fast, modern breakthrough that replaces slow traditional systems with automated, intelligent computing."}
                                </p>
                            </div>

                            <ul class="space-y-1.5">
                                ${formattedBullets}
                            </ul>
                        </div>
                    </div>

                    <!-- Right: Visual & Highlight Card -->
                    <div class="md:col-span-5 p-5 rounded-2xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <div class="rounded-xl overflow-hidden border border-white/10 h-[200px] relative">
                            <img src="${imgUrl}" alt="${title}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=85'"/>
                        </div>
                        ${stat ? `
                            <div class="mt-3 p-3 rounded-xl text-center font-bold text-sm" style="background:rgba(16, 185, 129, 0.1); border: 1px solid ${theme.accent}; color:${theme.accent}">
                                ${stat}
                            </div>
                        ` : ""}
                    </div>

                </div>

                <!-- Footer -->
                <div class="flex items-center justify-between text-xs pt-1 border-t border-white/5" style="color:${theme.textSecondary}">
                    <span>${currentPresentation.target_audience || "Student Presentation"}</span>
                    <span>1 / ${slides.length}</span>
                </div>
            </div>
        `;
    }
    // =========================================================================
    // FINAL SLIDE: CRAZY COOL THANK YOU & Q&A
    // =========================================================================
    else if (currentSlideIndex === slides.length - 1 || slide.layout_type === "thank_you") {
        contentHtml = `
            <div class="h-full w-full p-8 md:p-11 flex flex-col justify-between gamma-active-slide text-center">
                <div>
                    <span class="gamma-pill mb-2">🎉 THAT'S A WRAP!</span>
                    <h2 class="text-3xl md:text-5xl font-black tracking-tight" style="color:${theme.textPrimary}">
                        Thank You! Time for Q&A!
                    </h2>
                    <p class="text-sm md:text-lg font-semibold mt-1" style="color:${theme.accent}">
                        Any Questions or Thoughts? Let's Discuss!
                    </p>
                </div>

                <!-- Bento Grid -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 my-auto text-left items-stretch">
                    <!-- Left: Top Takeaways -->
                    <div class="md:col-span-6 p-6 rounded-2xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <span class="gamma-pill text-[10px] mb-3 self-start">KEY TAKEAWAYS</span>
                        <ul class="space-y-2 my-auto">
                            ${formattedBullets}
                        </ul>
                    </div>

                    <!-- Right: Q&A Forum -->
                    <div class="md:col-span-6 p-6 rounded-2xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.accent}">
                        <div>
                            <span class="gamma-pill text-[10px] mb-2">CREDITS & THANKS</span>
                            <p class="text-sm leading-relaxed italic mt-2 text-gray-300">
                                "${closingMsg || "Huge thanks to our teachers, mentors, and classmates for listening! Now let's open the floor."}"
                            </p>
                        </div>

                        <div class="mt-4 p-4 rounded-xl text-center font-extrabold text-sm uppercase tracking-wider shadow-lg" style="background:${theme.accent}; color:#07090E">
                            💬 ASK ME ANYTHING (Q&A)
                        </div>
                    </div>
                </div>

                <div class="text-right text-xs" style="color:${theme.textSecondary}">
                    ${currentSlideIndex + 1} / ${slides.length}
                </div>
            </div>
        `;
    }
    // =========================================================================
    // MIDDLE SLIDES: SHORT, PUNCHY BENTO GRIDS
    // =========================================================================
    else {
        contentHtml = `
            <div class="h-full w-full p-7 md:p-9 flex flex-col justify-between gamma-active-slide">
                <!-- Header -->
                <div>
                    <span class="gamma-pill mb-1.5">${tag}</span>
                    <h2 class="text-2xl md:text-4xl font-extrabold tracking-tight" style="color:${theme.textPrimary}">${title}</h2>
                    ${subtitle ? `<p class="text-xs md:text-sm mt-0.5 font-medium" style="color:${theme.textSecondary}">${subtitle}</p>` : ""}
                </div>

                <!-- Bento Grid -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 my-auto items-stretch">
                    
                    <!-- Text Bento -->
                    <div class="md:col-span-7 p-6 rounded-2xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <ul class="space-y-2 my-auto">
                            ${formattedBullets}
                        </ul>
                        ${stat ? `
                            <div class="mt-4 p-3 rounded-xl text-sm font-bold text-center border" style="background:rgba(16, 185, 129, 0.08); border-color:${theme.accent}; color:${theme.accent}">
                                ${stat}
                            </div>
                        ` : ""}
                    </div>

                    <!-- Clean Visual Bento (Zero Watermark) -->
                    <div class="md:col-span-5 rounded-2xl overflow-hidden border border-white/10 relative flex items-center justify-center min-h-[230px]" style="background:${theme.cardBg}">
                        <img src="${imgUrl}" alt="${title}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=85'"/>
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

function renderContinuousDocument() {
    const docWrapper = document.getElementById("documentContainerWrapper");
    if (!docWrapper || !currentPresentation || !currentPresentation.slides) return;
    const theme = THEME_STYLES[currentTheme] || THEME_STYLES["cyber_emerald"];

    docWrapper.innerHTML = "";

    currentPresentation.slides.forEach((slide, idx) => {
        const card = document.createElement("div");
        card.className = "gamma-doc-card";
        card.style.background = theme.cardBg;
        card.style.borderColor = theme.cardBorder;

        const tag = slide.tag || "CARD";
        const title = slide.title || "";
        const subtitle = slide.subtitle || "";
        const bullets = slide.bullet_points || [];
        const stat = slide.stat_or_highlight || "";
        const imgUrl = slide.preview_image_url || "";
        const formalDef = slide.formal_definition || "";

        const formattedBullets = formatBullets(bullets, theme);

        card.innerHTML = `
            <div class="flex items-center justify-between mb-3">
                <span class="gamma-pill text-xs">${tag}</span>
                <span class="text-xs font-mono text-gray-500 font-bold">#${idx + 1}</span>
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold mb-1" style="color:${theme.textPrimary}">${title}</h2>
            ${subtitle ? `<p class="text-sm mb-5 font-medium" style="color:${theme.textSecondary}">${subtitle}</p>` : ""}

            ${formalDef ? `
                <div class="p-4 rounded-xl border mb-5" style="background:rgba(16, 185, 129, 0.08); border-color:${theme.accent}">
                    <span class="text-[11px] font-extrabold uppercase tracking-wider block mb-1" style="color:${theme.accent}">
                        💡 IN SIMPLE WORDS:
                    </span>
                    <p class="text-sm font-semibold" style="color:${theme.textPrimary}">${formalDef}</p>
                </div>
            ` : ""}

            <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
                <div class="md:col-span-7">
                    <ul class="space-y-2">
                        ${formattedBullets}
                    </ul>
                    ${stat ? `
                        <div class="mt-4 p-2.5 rounded-xl text-xs font-bold border" style="background:rgba(16, 185, 129, 0.08); border-color:${theme.accent}; color:${theme.accent}">
                            ${stat}
                        </div>
                    ` : ""}
                </div>
                <div class="md:col-span-5 rounded-2xl overflow-hidden border border-white/10 h-[220px]">
                    <img src="${imgUrl}" alt="${title}" class="w-full h-full object-cover"/>
                </div>
            </div>
        `;
        docWrapper.appendChild(card);
    });
}

function renderThumbnails() {
    const container = document.getElementById("thumbnailStrip");
    container.innerHTML = "";

    if (!currentPresentation || !currentPresentation.slides) return;

    currentPresentation.slides.forEach((slide, idx) => {
        const thumb = document.createElement("div");
        thumb.className = `cursor-pointer rounded-xl p-2.5 border text-left transition-all ${idx === currentSlideIndex ? 'ring-2 ring-emerald-500 border-emerald-500 bg-[#151B28]' : 'border-white/10 bg-[#090B10] opacity-70 hover:opacity-100'}`;
        thumb.style.minWidth = "160px";
        thumb.innerHTML = `
            <div class="text-[10px] font-bold text-emerald-400 font-mono">#${idx + 1} ${slide.tag || "CARD"}</div>
            <div class="text-xs font-bold truncate text-white mt-1">${slide.title || "Untitled"}</div>
        `;
        thumb.addEventListener("click", () => {
            currentSlideIndex = idx;
            if (currentViewMode === "deck") {
                renderCurrentSlide();
            }
        });
        container.appendChild(thumb);
    });
}

function highlightActiveThumbnail() {
    const thumbs = document.querySelectorAll("#thumbnailStrip > div");
    thumbs.forEach((t, i) => {
        if (i === currentSlideIndex) {
            t.className = "cursor-pointer rounded-xl p-2.5 border text-left transition-all ring-2 ring-emerald-500 border-emerald-500 bg-[#151B28]";
            t.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
        } else {
            t.className = "cursor-pointer rounded-xl p-2.5 border text-left transition-all border-white/10 bg-[#090B10] opacity-70 hover:opacity-100";
        }
    });
}

async function handleDownloadPptx() {
    if (!currentPresentation) return;

    const btn = document.getElementById("downloadPptxBtn");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Compiling .PPTX...`;

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
        a.download = `${currentPresentation.presentation_title || 'Presentation'}.pptx`;
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
