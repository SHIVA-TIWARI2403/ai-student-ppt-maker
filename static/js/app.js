/**
 * AI Student PPT Maker - Frontend Controller
 * Handles generation, slide deck carousel, live theme rendering, and PPTX export.
 */

let currentPresentation = null;
let currentSlideIndex = 0;
let currentTheme = "cyber_emerald";
let availableThemes = {};

// Default theme styling definitions for immediate browser rendering
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
    // Generate Button
    document.getElementById("generateBtn").addEventListener("click", handleGenerateDeck);

    // Slide navigation
    document.getElementById("prevSlideBtn").addEventListener("click", () => navigateSlide(-1));
    document.getElementById("nextSlideBtn").addEventListener("click", () => navigateSlide(1));

    // Fullscreen present mode
    document.getElementById("fullscreenBtn").addEventListener("click", toggleFullscreen);

    // PPTX Download Button
    document.getElementById("downloadPptxBtn").addEventListener("click", handleDownloadPptx);

    // Keyboard navigation
    document.addEventListener("keydown", (e) => {
        if (!currentPresentation) return;
        if (e.key === "ArrowLeft") navigateSlide(-1);
        if (e.key === "ArrowRight") navigateSlide(1);
    });
}

async function handleGenerateDeck() {
    const topic = document.getElementById("topicInput").value.trim();
    if (!topic) {
        alert("Please enter a presentation topic or idea!");
        document.getElementById("topicInput").focus();
        return;
    }

    const slideCount = parseInt(document.getElementById("slideCountInput").value) || 6;
    const educationLevel = document.getElementById("eduLevelInput").value;
    const apiKey = document.getElementById("geminiKeyInput").value.trim();
    const includeImages = document.getElementById("toggleImages").checked;
    const includeGifs = document.getElementById("toggleGifs").checked;
    const includeAnimations = document.getElementById("toggleAnimations").checked;

    // UI Loading state
    const btn = document.getElementById("generateBtn");
    const originalBtnHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Generating Slides with AI...`;

    const progressDiv = document.getElementById("progressStatus");
    progressDiv.classList.remove("hidden");
    progressDiv.innerText = "Analyzing topic & crafting academic structure...";

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
                include_gifs: includeGifs,
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

        // Render live preview
        document.getElementById("studioPlaceholder").classList.add("hidden");
        document.getElementById("studioDeckSection").classList.remove("hidden");
        
        renderThumbnails();
        renderCurrentSlide();

        // Scroll smoothly to presentation studio
        document.getElementById("studioDeckSection").scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        alert("Error generating presentation: " + error.message);
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

    // Update Counter & Title
    document.getElementById("slideCounter").innerText = `Slide ${currentSlideIndex + 1} of ${slides.length}`;
    document.getElementById("deckMainTitle").innerText = currentPresentation.presentation_title || "Presentation";

    // Update Presenter Notes
    document.getElementById("speakerNotesContent").innerText = slide.speaker_notes || "No notes for this slide.";

    const stage = document.getElementById("slideStage");
    stage.style.backgroundColor = theme.bg;
    stage.style.color = theme.textPrimary;

    // Build Slide HTML based on Layout
    const tag = slide.tag || "OVERVIEW";
    const title = slide.title || "";
    const subtitle = slide.subtitle || "";
    const bullets = slide.bullet_points || [];
    const stat = slide.stat_or_highlight || "";
    const imgUrl = slide.preview_image_url || "";

    let contentHtml = "";

    // Bullet points HTML helper
    const formattedBullets = bullets.map(b => {
        if (b.includes("**")) {
            return b.replace(/\*\*(.*?)\*\*/g, `<strong style="color:${theme.accent}">$1</strong>`);
        }
        return b;
    }).map(b => `<li class="mb-3 flex items-start gap-2"><span style="color:${theme.accent}">•</span><span>${b}</span></li>`).join("");

    if (slide.layout_type === "title" || currentSlideIndex === 0) {
        // Hero Title Layout
        contentHtml = `
            <div class="h-full w-full p-8 md:p-12 flex flex-col justify-between slide-content-active" style="background: radial-gradient(circle at 80% 20%, ${theme.cardBg} 0%, ${theme.bg} 100%);">
                <div>
                    <span class="inline-block px-3 py-1 rounded text-xs font-bold tracking-wider mb-4" style="background:${theme.accent}; color:${theme.bg}">
                        ${tag.toUpperCase()}
                    </span>
                    <h1 class="text-3xl md:text-5xl font-black mb-3 tracking-tight" style="color:${theme.textPrimary}">${title}</h1>
                    <p class="text-base md:text-xl font-medium" style="color:${theme.textSecondary}">${subtitle}</p>
                </div>
                
                <div class="p-6 rounded-xl border mt-6" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                    <ul class="text-sm md:text-base space-y-2">
                        ${formattedBullets}
                    </ul>
                </div>

                <div class="flex items-center justify-between text-xs mt-4" style="color:${theme.textSecondary}">
                    <span>${currentPresentation.target_audience || "Academic Presentation"}</span>
                    ${stat ? `<span class="px-3 py-1 rounded-full font-bold" style="background:${theme.bg}; border: 1px solid ${theme.accent}; color:${theme.accent}">★ ${stat}</span>` : ""}
                </div>
            </div>
        `;
    } else {
        // Content Slide with Split Layout
        contentHtml = `
            <div class="h-full w-full p-6 md:p-8 flex flex-col justify-between slide-content-active">
                <!-- Header -->
                <div>
                    <span class="inline-block px-2.5 py-0.5 rounded text-xs font-bold tracking-wider mb-2" style="background:${theme.accent}; color:${theme.bg}">
                        ${tag.toUpperCase()}
                    </span>
                    <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight" style="color:${theme.textPrimary}">${title}</h2>
                    ${subtitle ? `<p class="text-xs md:text-sm mt-1" style="color:${theme.textSecondary}">${subtitle}</p>` : ""}
                </div>

                <!-- Main Grid -->
                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 my-auto items-stretch">
                    <!-- Bullets Column -->
                    <div class="md:col-span-7 p-6 rounded-xl border flex flex-col justify-between" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <ul class="text-sm md:text-base space-y-2">
                            ${formattedBullets}
                        </ul>
                        ${stat ? `
                            <div class="mt-4 p-2.5 rounded-lg text-xs font-bold text-center border" style="background:${theme.bg}; border-color:${theme.accent}; color:${theme.accent}">
                                💡 ${stat}
                            </div>
                        ` : ""}
                    </div>

                    <!-- Visual Column -->
                    <div class="md:col-span-5 rounded-xl overflow-hidden border relative flex items-center justify-center min-h-[220px]" style="background:${theme.cardBg}; border-color:${theme.cardBorder}">
                        <img src="${imgUrl}" alt="${title}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" onerror="this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop&q=80'"/>
                    </div>
                </div>

                <!-- Footer slide number -->
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
        thumb.className = `cursor-pointer rounded-lg p-2 border text-left transition-all ${idx === currentSlideIndex ? 'ring-2 ring-emerald-500 border-emerald-500' : 'border-gray-700 bg-gray-900/60 opacity-70 hover:opacity-100'}`;
        thumb.style.minWidth = "140px";
        thumb.innerHTML = `
            <div class="text-[10px] font-bold text-emerald-400">#${idx + 1} ${slide.tag || "SLIDE"}</div>
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
            t.className = "cursor-pointer rounded-lg p-2 border text-left transition-all border-gray-700 bg-gray-900/60 opacity-70 hover:opacity-100";
        }
    });
}

async function handleDownloadPptx() {
    if (!currentPresentation) return;

    const btn = document.getElementById("downloadPptxBtn");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Building .PPTX...`;

    try {
        const includeImages = document.getElementById("toggleImages").checked;
        const res = await fetch("/api/export-pptx", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                presentation_data: currentPresentation,
                theme: currentTheme,
                include_images: includeImages
            })
        });

        if (!res.ok) {
            throw new Error("Failed to compile PowerPoint file.");
        }

        const data = await res.json();
        // Trigger browser download
        const a = document.createElement("a");
        a.href = data.download_url;
        a.download = `${currentPresentation.presentation_title || 'presentation'}.pptx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

    } catch (e) {
        alert("Error generating PPTX: " + e.message);
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
