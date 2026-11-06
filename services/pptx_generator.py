"""
PPTX Generator Service for SlideCraft AI.
Constructs high-aesthetic, widescreen 16:9 PowerPoint files with:
- Full-bleed thematic background textures with smart contrast overlay
- Slide 1: Prominent Formal Academic Concept Definition Card
- Middle Slides: Deep theoretical frameworks, mathematical models, and architectural cards
- Final Slide: Dedicated Closing & Thank You / Q&A Slide
- Native OpenXML slide transitions (Fade, Push, Wipe, Zoom)
- Embedded presenter notes for every slide
- Supports 3 up to 25 slides seamlessly
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

def create_badge(slide, left, top, width, height, text, bg_rgb, text_rgb, font_name="Segoe UI"):
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
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = text_rgb
    return shape

def render_bullet_points(text_frame, bullet_points, theme, font_size=12):
    text_frame.word_wrap = True
    for i, bp in enumerate(bullet_points):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.space_after = Pt(8)
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
    Builds an academic presentation up to 25 slides with formal definition, deep theory, and thank you note.
    """
    theme = get_theme(theme_name)
    prs = Presentation()
    
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    topic_title = presentation_data.get("presentation_title", "Research Presentation")
    slides_data = presentation_data.get("slides", [])

    # Pre-fetch or generate background texture if requested
    bg_image_path = None
    if include_background:
        try:
            bg_image_path = fetch_background_image(topic_title, theme_name)
        except Exception as e:
            print(f"[PPTXGenerator] Background error: {e}")

    total_slides = len(slides_data)

    for idx, slide_info in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Slide Animated Transition
        apply_slide_transition(slide, theme.get("transition", "fade"))

        # 2. Background Canvas & Wallpaper
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
            notes_text_frame.text = f"[Academic Presenter Script]:\n{speaker_notes}"

        layout_type = slide_info.get("layout_type", "split_image_right")
        tag = slide_info.get("tag", "RESEARCH TOPIC")
        title = slide_info.get("title", "Academic Presentation Slide")
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
        # SLIDE 1: FORMAL CONCEPT DEFINITION & ACADEMIC INTRO
        # =========================================================================
        if idx == 0 or layout_type == "title":
            # Hero Backdrop Card
            hero = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.7), Inches(11.533), Inches(6.1))
            hero.fill.solid()
            hero.fill.fore_color.rgb = theme["card_bg_rgb"]
            hero.line.color.rgb = theme["card_border_rgb"]
            hero.line.width = Pt(1.5)

            # Category Badge
            create_badge(slide, Inches(1.3), Inches(1.0), Inches(2.6), Inches(0.35), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            # Main Presentation Title
            tbox = slide.shapes.add_textbox(Inches(1.3), Inches(1.45), Inches(10.7), Inches(1.3))
            tf = tbox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = theme["font_title"]
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = theme["text_primary_rgb"]

            if subtitle:
                p_sub = tf.add_paragraph()
                p_sub.space_before = Pt(4)
                p_sub.text = subtitle
                p_sub.font.name = theme["font_body"]
                p_sub.font.size = Pt(14)
                p_sub.font.color.rgb = theme["text_secondary_rgb"]

            # Prominent Formal Academic Definition Box
            def_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(2.85), Inches(10.7), Inches(1.3))
            def_box.fill.solid()
            def_box.fill.fore_color.rgb = theme["bg_rgb"]
            def_box.line.color.rgb = theme["accent_rgb"]
            def_box.line.width = Pt(1.5)

            dtf = def_box.text_frame
            dtf.word_wrap = True
            dtf.margin_left = dtf.margin_top = dtf.margin_right = dtf.margin_bottom = Inches(0.12)
            
            p_def_head = dtf.paragraphs[0]
            p_def_head.text = "📖 FORMAL ACADEMIC DEFINITION & CORE PREMISE:"
            p_def_head.font.name = theme["font_title"]
            p_def_head.font.size = Pt(10.5)
            p_def_head.font.bold = True
            p_def_head.font.color.rgb = theme["accent_rgb"]

            p_def_body = dtf.add_paragraph()
            p_def_body.space_before = Pt(3)
            p_def_body.text = formal_def or f"Formally, {topic_title} is characterized as an advanced academic paradigm governing specialized architectures and algorithmic pipelines to achieve deterministic computational performance."
            p_def_body.font.name = theme["font_body"]
            p_def_body.font.size = Pt(11.5)
            p_def_body.font.color.rgb = theme["text_primary_rgb"]

            # Research Scope Bullets
            b_box = slide.shapes.add_textbox(Inches(1.3), Inches(4.3), Inches(10.7), Inches(1.8))
            render_bullet_points(b_box.text_frame, bullets, theme, font_size=12)

            # Footer Highlight Tag
            if stat:
                create_badge(slide, Inches(1.3), Inches(6.15), Inches(3.4), Inches(0.4), f"★ {stat}", theme["bg_rgb"], theme["accent_rgb"], theme["font_body"])
            continue

        # =========================================================================
        # FINAL SLIDE: DEDICATED CLOSING & THANK YOU / Q&A
        # =========================================================================
        if idx == total_slides - 1 or layout_type == "thank_you":
            # Hero Container
            ty_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.8), Inches(10.933), Inches(5.9))
            ty_card.fill.solid()
            ty_card.fill.fore_color.rgb = theme["card_bg_rgb"]
            ty_card.line.color.rgb = theme["accent_rgb"]
            ty_card.line.width = Pt(2.0)

            # Category Badge
            create_badge(slide, Inches(1.8), Inches(1.2), Inches(2.6), Inches(0.35), "DEFENSE CONCLUSION", theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            # Big Thank You Heading
            t_box = slide.shapes.add_textbox(Inches(1.8), Inches(1.7), Inches(9.8), Inches(1.4))
            ttf = t_box.text_frame
            ttf.word_wrap = True
            tp = ttf.paragraphs[0]
            tp.text = "Thank You for Your Time & Attention"
            tp.font.name = theme["font_title"]
            tp.font.size = Pt(34)
            tp.font.bold = True
            tp.font.color.rgb = theme["text_primary_rgb"]

            tp_sub = ttf.add_paragraph()
            tp_sub.space_before = Pt(6)
            tp_sub.text = subtitle or "Floor is now Open for Questions, Academic Inquiries & Constructive Critiques"
            tp_sub.font.name = theme["font_body"]
            tp_sub.font.size = Pt(16)
            tp_sub.font.color.rgb = theme["accent_rgb"]

            # Closing Appreciation Message Box
            msg_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(3.2), Inches(9.8), Inches(1.1))
            msg_box.fill.solid()
            msg_box.fill.fore_color.rgb = theme["bg_rgb"]
            msg_box.line.color.rgb = theme["card_border_rgb"]
            msg_box.line.width = Pt(1.0)
            
            mtf = msg_box.text_frame
            mtf.word_wrap = True
            mtf.margin_left = mtf.margin_top = mtf.margin_right = mtf.margin_bottom = Inches(0.12)
            mp = mtf.paragraphs[0]
            mp.text = closing_msg or "We express our profound gratitude to our academic mentors, thesis advisory committee, and peer researchers whose guidance has made this investigation possible."
            mp.font.name = theme["font_body"]
            mp.font.size = Pt(12)
            mp.font.color.rgb = theme["text_primary_rgb"]

            # Key Summary Takeaways Box
            sum_box = slide.shapes.add_textbox(Inches(1.8), Inches(4.45), Inches(9.8), Inches(1.5))
            render_bullet_points(sum_box.text_frame, bullets, theme, font_size=12)

            # Highlight Forum Tag
            create_badge(slide, Inches(1.8), Inches(5.95), Inches(4.5), Inches(0.45), "💬 OPEN FOR Q&A & DISCUSSION", theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])
            continue

        # =========================================================================
        # STANDARD HEADER FOR MIDDLE CONTENT SLIDES
        # =========================================================================
        create_badge(slide, Inches(0.9), Inches(0.5), Inches(2.6), Inches(0.32), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

        header_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.85), Inches(11.5), Inches(1.1))
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
            hp_sub.space_before = Pt(3)
            hp_sub.text = subtitle
            hp_sub.font.name = theme["font_body"]
            hp_sub.font.size = Pt(13)
            hp_sub.font.color.rgb = theme["text_secondary_rgb"]

        # =========================================================================
        # LAYOUT: DEEP THEORY (WIDE STRUCTURED ACADEMIC CARD)
        # =========================================================================
        if layout_type == "deep_theory":
            theory_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(2.05), Inches(11.533), Inches(4.75))
            theory_card.fill.solid()
            theory_card.fill.fore_color.rgb = theme["card_bg_rgb"]
            theory_card.line.color.rgb = theme["card_border_rgb"]
            theory_card.line.width = Pt(1.2)

            tb_theory = slide.shapes.add_textbox(Inches(1.25), Inches(2.25), Inches(10.8), Inches(3.6))
            render_bullet_points(tb_theory.text_frame, bullets, theme, font_size=13.5)

            if stat:
                st_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.25), Inches(6.05), Inches(5.5), Inches(0.55))
                st_card.fill.solid()
                st_card.fill.fore_color.rgb = theme["bg_rgb"]
                st_card.line.color.rgb = theme["accent_rgb"]
                sp = st_card.text_frame.paragraphs[0]
                sp.alignment = PP_ALIGN.CENTER
                sp.text = f"💡 Empirical Benchmark: {stat}"
                sp.font.name = theme["font_body"]
                sp.font.size = Pt(11)
                sp.font.bold = True
                sp.font.color.rgb = theme["accent_rgb"]
            continue

        # =========================================================================
        # LAYOUT: THREE CARDS (COLUMNS)
        # =========================================================================
        if layout_type == "three_cards":
            card_w = Inches(3.64)
            card_h = Inches(4.7)
            spacing = Inches(0.3)
            start_x = Inches(0.9)
            start_y = Inches(2.05)

            card_labels = ["PILLAR 01", "PILLAR 02", "PILLAR 03"]
            for c_idx, bp in enumerate(bullets[:3]):
                c_x = start_x + (c_idx * (card_w + spacing))
                card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, start_y, card_w, card_h)
                card_shape.fill.solid()
                card_shape.fill.fore_color.rgb = theme["card_bg_rgb"]
                card_shape.line.color.rgb = theme["card_border_rgb"]
                card_shape.line.width = Pt(1.2)

                create_badge(slide, c_x + Inches(0.3), start_y + Inches(0.3), Inches(1.4), Inches(0.32), card_labels[c_idx], theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

                c_box = slide.shapes.add_textbox(c_x + Inches(0.25), start_y + Inches(0.8), card_w - Inches(0.5), card_h - Inches(1.0))
                render_bullet_points(c_box.text_frame, [bp], theme, font_size=13)
            continue

        # =========================================================================
        # LAYOUT: SPLIT IMAGE (LEFT OR RIGHT)
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

        card_top = Inches(2.05)

        c_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, content_left, card_top, content_w, content_h)
        c_card.fill.solid()
        c_card.fill.fore_color.rgb = theme["card_bg_rgb"]
        c_card.line.color.rgb = theme["card_border_rgb"]
        c_card.line.width = Pt(1.2)

        tb_bullets = slide.shapes.add_textbox(content_left + Inches(0.35), card_top + Inches(0.3), content_w - Inches(0.7), Inches(3.4))
        render_bullet_points(tb_bullets.text_frame, bullets, theme, font_size=13)

        if stat:
            st_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, content_left + Inches(0.35), card_top + Inches(3.9), content_w - Inches(0.7), Inches(0.6))
            st_card.fill.solid()
            st_card.fill.fore_color.rgb = theme["bg_rgb"]
            st_card.line.color.rgb = theme["accent_rgb"]
            sp = st_card.text_frame.paragraphs[0]
            sp.alignment = PP_ALIGN.CENTER
            sp.text = f"💡 Empirical Benchmark: {stat}"
            sp.font.name = theme["font_body"]
            sp.font.size = Pt(11)
            sp.font.bold = True
            sp.font.color.rgb = theme["accent_rgb"]

        # Image Frame Card
        img_frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_left, card_top, img_w, img_h)
        img_frame.fill.solid()
        img_frame.fill.fore_color.rgb = theme["card_bg_rgb"]
        img_frame.line.color.rgb = theme["card_border_rgb"]
        img_frame.line.width = Pt(1.2)

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

    file_id = f"student_ppt_{uuid.uuid4().hex[:10]}"
    file_path = os.path.join(OUTPUT_DIR, f"{file_id}.pptx")
    prs.save(file_path)
    print(f"[PPTXGenerator] Generated {len(slides_data)}-slide PPTX at: {file_path}")
    return file_id, file_path
