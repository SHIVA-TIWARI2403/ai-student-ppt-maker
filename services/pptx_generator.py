"""
Gamma-Style Bento PPTX Generator for SlideCraft AI.
Constructs modular, ultra-modern presentation decks inspired by Gamma.app:
- Bento Grid card architectures (floating rounded cards with glass borders)
- Slide 1: Formal Concept Definition Bento Box + Visual Spec Card
- Middle Slides: 2-Column Split Bento, 3-Card Column Bento, and Metric Callout Cards
- Final Slide: Dedicated Gamma-Style Closing & Thank You / Q&A Card
- Full-bleed ambient thematic wallpaper with smart contrast dimming
- Native OpenXML slide transitions (Fade, Push, Wipe, Zoom)
- Presenter script embedded in notes for each slide
"""

import os
import uuid
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

from services.themes import get_theme
from services.visual_service import fetch_ai_image, fetch_background_image

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_ppts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def apply_slide_transition(slide, transition_type: str = "fade"):
    """Injects native OpenXML transition elements for animated presentation playback."""
    try:
        if transition_type == "push":
            xml = f'<p:transition {nsdecls("p")} spd="med"><p:push dir="l"/></p:transition>'
        elif transition_type == "wipe":
            xml = f'<p:transition {nsdecls("p")} spd="med"><p:wipe dir="r"/></p:transition>'
        elif transition_type == "zoom":
            xml = f'<p:transition {nsdecls("p")} spd="med"><p:zoom dir="in"/></p:transition>'
        else:
            xml = f'<p:transition {nsdecls("p")} spd="med"><p:fade/></p:transition>'
        
        tr_element = parse_xml(xml)
        slide._element.insert(0, tr_element)
    except Exception as e:
        print(f"[PPTXGenerator] Transition warning: {e}")

def create_gamma_card(slide, left, top, width, height, bg_rgb, border_rgb, border_width_pt=1.2):
    """Creates a sleek rounded Bento card shape with subtle border, identical to Gamma."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_rgb
    shape.line.color.rgb = border_rgb
    shape.line.width = Pt(border_width_pt)
    return shape

def create_badge(slide, left, top, width, height, text, bg_rgb, text_rgb, font_name="Segoe UI"):
    """Creates a Gamma-style pill badge with uppercase tracked text."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_rgb
    shape.line.fill.background()
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = text.upper()
    p.font.name = font_name
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = text_rgb
    return shape

def render_bullet_points(text_frame, bullet_points, theme, font_size=12):
    text_frame.word_wrap = True
    for i, bp in enumerate(bullet_points):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.space_after = Pt(7)
        p.space_before = Pt(3)
        
        if "**" in bp:
            parts = bp.split("**")
            if len(parts) >= 3:
                r1 = p.add_run()
                r1.text = "• " + parts[1].strip() + (" " if parts[2].startswith(":") else ": ")
                r1.font.bold = True
                r1.font.name = theme["font_body"]
                r1.font.size = Pt(font_size)
                r1.font.color.rgb = theme["accent_rgb"]
                
                r2 = p.add_run()
                r2.text = parts[2].lstrip(": ").strip()
                r2.font.bold = False
                r2.font.name = theme["font_body"]
                r2.font.size = Pt(font_size)
                r2.font.color.rgb = theme["text_primary_rgb"]
                continue

        p.text = "• " + bp.strip()
        p.font.name = theme["font_body"]
        p.font.size = Pt(font_size)
        p.font.color.rgb = theme["text_primary_rgb"]

def build_presentation_pptx(presentation_data: dict, theme_name: str = "cyber_emerald", include_images: bool = True, include_background: bool = True) -> str:
    """
    Builds a Gamma-grade Bento presentation deck up to 25 slides.
    """
    theme = get_theme(theme_name)
    prs = Presentation()
    
    # 16:9 Widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    topic_title = presentation_data.get("presentation_title", "Research Presentation")
    slides_data = presentation_data.get("slides", [])
    total_slides = len(slides_data)

    bg_image_path = None
    if include_background:
        try:
            bg_image_path = fetch_background_image(topic_title, theme_name)
        except Exception as e:
            print(f"[PPTXGenerator] Background fetch warning: {e}")

    for idx, slide_info in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Slide Animated Transition
        apply_slide_transition(slide, theme.get("transition", "fade"))

        # 2. Ambient Background Canvas / Wallpaper
        if bg_image_path and os.path.exists(bg_image_path):
            try:
                slide.shapes.add_picture(bg_image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
            except Exception:
                bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
                bg.fill.solid()
                bg.fill.fore_color.rgb = theme["bg_rgb"]
                bg.line.fill.background()
        else:
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
            bg.fill.solid()
            bg.fill.fore_color.rgb = theme["bg_rgb"]
            bg.line.fill.background()

        # 3. Presenter Speaker Notes
        speaker_notes = slide_info.get("speaker_notes", "")
        if speaker_notes:
            notes_slide = slide.notes_slide
            notes_text_frame = notes_slide.notes_text_frame
            notes_text_frame.text = f"[Gamma Presenter Script]:\n{speaker_notes}"

        layout_type = slide_info.get("layout_type", "split_image_right")
        tag = slide_info.get("tag", "RESEARCH MODULE")
        title = slide_info.get("title", "Presentation Slide")
        subtitle = slide_info.get("subtitle", "")
        bullets = slide_info.get("bullet_points", [])
        stat = slide_info.get("stat_or_highlight", "")
        img_prompt = slide_info.get("image_prompt", f"{title} scientific illustration")
        formal_def = slide_info.get("formal_definition", "")
        closing_msg = slide_info.get("closing_message", "")

        # Slide Number Badge (Bottom Right)
        slide_num_box = slide.shapes.add_textbox(Inches(11.8), Inches(7.0), Inches(1.2), Inches(0.4))
        p_num = slide_num_box.text_frame.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{idx + 1} / {total_slides}"
        p_num.font.name = theme["font_body"]
        p_num.font.size = Pt(9.5)
        p_num.font.color.rgb = theme["text_secondary_rgb"]

        # =========================================================================
        # SLIDE 1: GAMMA HERO BENTO COVER (FORMAL DEFINITION & PREMISE)
        # =========================================================================
        if idx == 0 or layout_type == "title":
            # Top Tag Badge
            create_badge(slide, Inches(0.9), Inches(0.55), Inches(2.6), Inches(0.35), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            # Hero Presentation Title
            tbox = slide.shapes.add_textbox(Inches(0.9), Inches(0.95), Inches(11.5), Inches(1.3))
            tf = tbox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = theme["font_title"]
            p.font.size = Pt(30)
            p.font.bold = True
            p.font.color.rgb = theme["text_primary_rgb"]

            if subtitle:
                p_sub = tf.add_paragraph()
                p_sub.space_before = Pt(3)
                p_sub.text = subtitle
                p_sub.font.name = theme["font_body"]
                p_sub.font.size = Pt(13)
                p_sub.font.color.rgb = theme["text_secondary_rgb"]

            # Bento Left: Formal Definition & Research Scope Card
            bento_left = create_gamma_card(slide, Inches(0.9), Inches(2.2), Inches(6.8), Inches(4.6), theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)
            
            # Definition Pill Header inside Bento Card
            create_badge(slide, Inches(1.2), Inches(2.45), Inches(3.2), Inches(0.32), "📖 FORMAL ACADEMIC DEFINITION", theme["bg_rgb"], theme["accent_rgb"], theme["font_body"])

            def_text_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.85), Inches(6.2), Inches(1.3))
            dtf = def_text_box.text_frame
            dtf.word_wrap = True
            dp = dtf.paragraphs[0]
            dp.text = formal_def or f"Formally defined, {topic_title} is an advanced academic domain governing algorithmic data pipelines, architectural mechanics, and deterministic performance evaluations."
            dp.font.name = theme["font_body"]
            dp.font.size = Pt(11.5)
            dp.font.color.rgb = theme["text_primary_rgb"]

            # Agenda / Scope points inside Bento Left
            scope_box = slide.shapes.add_textbox(Inches(1.2), Inches(4.2), Inches(6.2), Inches(2.4))
            render_bullet_points(scope_box.text_frame, bullets, theme, font_size=11.5)

            # Bento Right: Visual Diagram & Stat Frame
            bento_right = create_gamma_card(slide, Inches(8.0), Inches(2.2), Inches(4.433), Inches(4.6), theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)
            
            if include_images:
                try:
                    local_img = fetch_ai_image(img_prompt, seed=idx * 23 + 101)
                    if local_img and os.path.exists(local_img):
                        slide.shapes.add_picture(local_img, Inches(8.2), Inches(2.4), width=Inches(4.033), height=Inches(3.3))
                except Exception as e:
                    print(f"[PPTXGenerator] Slide 1 visual error: {e}")

            # Highlight Metric inside Bento Right
            if stat:
                st_card = create_gamma_card(slide, Inches(8.2), Inches(5.85), Inches(4.033), Inches(0.7), theme["bg_rgb"], theme["accent_rgb"], 1.2)
                sp = st_card.text_frame.paragraphs[0]
                sp.alignment = PP_ALIGN.CENTER
                sp.text = f"★ {stat}"
                sp.font.name = theme["font_body"]
                sp.font.size = Pt(11.5)
                sp.font.bold = True
                sp.font.color.rgb = theme["accent_rgb"]
            continue

        # =========================================================================
        # FINAL SLIDE: GAMMA THANK YOU & DEFENSE Q&A CLOSING
        # =========================================================================
        if idx == total_slides - 1 or layout_type == "thank_you":
            # Header
            create_badge(slide, Inches(0.9), Inches(0.55), Inches(2.8), Inches(0.35), "DEFENSE CONCLUSION", theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            th_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.95), Inches(11.5), Inches(1.3))
            th_tf = th_box.text_frame
            th_tf.word_wrap = True
            p_th = th_tf.paragraphs[0]
            p_th.text = "Thank You for Your Time & Attention"
            p_th.font.name = theme["font_title"]
            p_th.font.size = Pt(30)
            p_th.font.bold = True
            p_th.font.color.rgb = theme["text_primary_rgb"]

            p_th_sub = th_tf.add_paragraph()
            p_th_sub.space_before = Pt(3)
            p_th_sub.text = subtitle or "Floor is now Open for Questions, Academic Inquiries & Constructive Critiques"
            p_th_sub.font.name = theme["font_body"]
            p_th_sub.font.size = Pt(13)
            p_th_sub.font.color.rgb = theme["accent_rgb"]

            # Bento Left: Key Takeaways Recap Card
            b_left = create_gamma_card(slide, Inches(0.9), Inches(2.2), Inches(6.0), Inches(4.6), theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)
            create_badge(slide, Inches(1.2), Inches(2.45), Inches(2.6), Inches(0.32), "SUMMARY SYNTHESIS", theme["bg_rgb"], theme["accent_rgb"], theme["font_body"])
            
            sum_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.9), Inches(5.4), Inches(3.6))
            render_bullet_points(sum_box.text_frame, bullets, theme, font_size=12)

            # Bento Right: Appreciation & Q&A Forum Card
            b_right = create_gamma_card(slide, Inches(7.2), Inches(2.2), Inches(5.233), Inches(4.6), theme["card_bg_rgb"], theme["accent_rgb"], 1.5)
            create_badge(slide, Inches(7.5), Inches(2.45), Inches(2.8), Inches(0.32), "ACKNOWLEDGMENTS", theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            appr_box = slide.shapes.add_textbox(Inches(7.5), Inches(2.95), Inches(4.6), Inches(1.8))
            ap_tf = appr_box.text_frame
            ap_tf.word_wrap = True
            ap = ap_tf.paragraphs[0]
            ap.text = closing_msg or "We express sincere gratitude to our academic mentors, thesis advisory committee, and peer researchers whose critical insights have enriched this investigation."
            ap.font.name = theme["font_body"]
            ap.font.size = Pt(12)
            ap.font.color.rgb = theme["text_primary_rgb"]

            # Q&A Big Button Callout
            qa_pill = create_gamma_card(slide, Inches(7.5), Inches(5.3), Inches(4.633), Inches(1.1), theme["bg_rgb"], theme["accent_rgb"], 1.2)
            qp = qa_pill.text_frame.paragraphs[0]
            qp.alignment = PP_ALIGN.CENTER
            qp.text = "💬 OPEN FOR QUESTIONS & ANSWERS (Q&A)"
            qp.font.name = theme["font_title"]
            qp.font.size = Pt(12.5)
            qp.font.bold = True
            qp.font.color.rgb = theme["accent_rgb"]
            continue

        # =========================================================================
        # STANDARD HEADER FOR MIDDLE CONTENT SLIDES
        # =========================================================================
        create_badge(slide, Inches(0.9), Inches(0.55), Inches(2.6), Inches(0.32), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

        header_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.92), Inches(11.5), Inches(1.1))
        htf = header_box.text_frame
        htf.word_wrap = True
        hp = htf.paragraphs[0]
        hp.text = title
        hp.font.name = theme["font_title"]
        hp.font.size = Pt(24)
        hp.font.bold = True
        hp.font.color.rgb = theme["text_primary_rgb"]

        if subtitle:
            hp_sub = htf.add_paragraph()
            hp_sub.space_before = Pt(2)
            hp_sub.text = subtitle
            hp_sub.font.name = theme["font_body"]
            hp_sub.font.size = Pt(12.5)
            hp_sub.font.color.rgb = theme["text_secondary_rgb"]

        # =========================================================================
        # MIDDLE LAYOUT: THREE CARDS BENTO
        # =========================================================================
        if layout_type == "three_cards":
            card_w = Inches(3.64)
            card_h = Inches(4.7)
            spacing = Inches(0.3)
            start_x = Inches(0.9)
            start_y = Inches(2.1)

            card_labels = ["01 / AXIOM", "02 / MECHANISM", "03 / DEPLOYMENT"]
            for c_idx, bp in enumerate(bullets[:3]):
                c_x = start_x + (c_idx * (card_w + spacing))
                card_shape = create_gamma_card(slide, c_x, start_y, card_w, card_h, theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)
                create_badge(slide, c_x + Inches(0.3), start_y + Inches(0.3), Inches(1.5), Inches(0.32), card_labels[c_idx], theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

                c_box = slide.shapes.add_textbox(c_x + Inches(0.25), start_y + Inches(0.8), card_w - Inches(0.5), card_h - Inches(1.0))
                render_bullet_points(c_box.text_frame, [bp], theme, font_size=13)
            continue

        # =========================================================================
        # MIDDLE LAYOUT: SPLIT IMAGE BENTO (LEFT OR RIGHT)
        # =========================================================================
        is_image_left = (layout_type == "split_image_left")
        content_w = Inches(6.5)
        content_h = Inches(4.75)
        img_w = Inches(4.7)
        img_h = Inches(4.75)

        if is_image_left:
            img_left = Inches(0.9)
            content_left = Inches(5.9)
        else:
            content_left = Inches(0.9)
            img_left = Inches(7.7)

        card_top = Inches(2.1)

        # Content Bento Card
        c_card = create_gamma_card(slide, content_left, card_top, content_w, content_h, theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)
        tb_bullets = slide.shapes.add_textbox(content_left + Inches(0.35), card_top + Inches(0.3), content_w - Inches(0.7), Inches(3.4))
        render_bullet_points(tb_bullets.text_frame, bullets, theme, font_size=13)

        if stat:
            st_card = create_gamma_card(slide, content_left + Inches(0.35), card_top + Inches(3.85), content_w - Inches(0.7), Inches(0.65), theme["bg_rgb"], theme["accent_rgb"], 1.2)
            sp = st_card.text_frame.paragraphs[0]
            sp.alignment = PP_ALIGN.CENTER
            sp.text = f"💡 Empirical Benchmark: {stat}"
            sp.font.name = theme["font_body"]
            sp.font.size = Pt(11)
            sp.font.bold = True
            sp.font.color.rgb = theme["accent_rgb"]

        # Visual Bento Frame
        img_frame = create_gamma_card(slide, img_left, card_top, img_w, img_h, theme["card_bg_rgb"], theme["card_border_rgb"], 1.2)

        if include_images:
            try:
                local_img_path = fetch_ai_image(img_prompt, seed=idx * 17 + 42)
                if local_img_path and os.path.exists(local_img_path):
                    slide.shapes.add_picture(
                        local_img_path,
                        img_left + Inches(0.15),
                        card_top + Inches(0.15),
                        width=img_w - Inches(0.3),
                        height=img_h - Inches(0.3)
                    )
            except Exception as e:
                print(f"[PPTXGenerator] Image embed error on slide {idx+1}: {e}")

    file_id = f"gamma_deck_{uuid.uuid4().hex[:10]}"
    file_path = os.path.join(OUTPUT_DIR, f"{file_id}.pptx")
    prs.save(file_path)
    print(f"[PPTXGenerator] Generated {len(slides_data)}-slide Gamma Bento PPTX at: {file_path}")
    return file_id, file_path
