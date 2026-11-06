"""
PPTX Generator Service.
Constructs high-aesthetic, widescreen 16:9 PowerPoint files with:
- Modern container cards and glassmorphism styling
- High-res embedded AI images and visual badges
- Speaker presenter notes embedded on every slide
- Native OpenXML slide transitions (Fade, Push, Wipe, Zoom)
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
from services.visual_service import fetch_ai_image

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

def render_bullet_points(text_frame, bullet_points, theme, font_size=13):
    text_frame.word_wrap = True
    for i, bp in enumerate(bullet_points):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.space_after = Pt(10)
        p.space_before = Pt(4)
        
        # Check if formatted with **Bold Prefix**: Description
        if "**" in bp:
            parts = bp.split("**")
            # Usually parts = ["", "Bold Prefix", ": Description"]
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

        # Standard plain bullet
        p.text = "• " + bp.strip()
        p.font.name = theme["font_body"]
        p.font.size = Pt(font_size)
        p.font.color.rgb = theme["text_primary_rgb"]

def build_presentation_pptx(presentation_data: dict, theme_name: str = "cyber_emerald", include_images: bool = True) -> str:
    """
    Builds the complete PPTX presentation file and returns absolute path.
    """
    theme = get_theme(theme_name)
    prs = Presentation()
    
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    slides_data = presentation_data.get("slides", [])

    for idx, slide_info in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Slide Animated Transition
        apply_slide_transition(slide, theme.get("transition", "fade"))

        # 2. Solid Background Canvas
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = theme["bg_rgb"]
        bg.line.fill.background()

        # 3. Speaker Presenter Notes
        speaker_notes = slide_info.get("speaker_notes", "")
        if speaker_notes:
            notes_slide = slide.notes_slide
            notes_text_frame = notes_slide.notes_text_frame
            notes_text_frame.text = f"[Presenter Script for Student]:\n{speaker_notes}"

        layout_type = slide_info.get("layout_type", "split_image_right")
        tag = slide_info.get("tag", "TOPIC")
        title = slide_info.get("title", "Presentation Slide")
        subtitle = slide_info.get("subtitle", "")
        bullets = slide_info.get("bullet_points", [])
        stat = slide_info.get("stat_or_highlight", "")
        img_prompt = slide_info.get("image_prompt", f"{title} academic infographic")

        # Slide Number Badge (Bottom Right)
        slide_num_box = slide.shapes.add_textbox(Inches(11.8), Inches(6.9), Inches(1.2), Inches(0.4))
        p_num = slide_num_box.text_frame.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{idx + 1} / {len(slides_data)}"
        p_num.font.name = theme["font_body"]
        p_num.font.size = Pt(10)
        p_num.font.color.rgb = theme["text_secondary_rgb"]

        # ==========================================
        # LAYOUT: TITLE / INTRO SLIDE (Slide 1)
        # ==========================================
        if layout_type == "title" or idx == 0:
            # Main Hero Card
            hero = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
            hero.fill.solid()
            hero.fill.fore_color.rgb = theme["card_bg_rgb"]
            hero.line.color.rgb = theme["card_border_rgb"]
            hero.line.width = Pt(1.5)

            # Category Badge
            create_badge(slide, Inches(1.8), Inches(1.5), Inches(1.8), Inches(0.38), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

            # Big Title
            tbox = slide.shapes.add_textbox(Inches(1.8), Inches(2.1), Inches(9.8), Inches(1.6))
            tf = tbox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = theme["font_title"]
            p.font.size = Pt(36)
            p.font.bold = True
            p.font.color.rgb = theme["text_primary_rgb"]

            # Subtitle
            if subtitle:
                p_sub = tf.add_paragraph()
                p_sub.space_before = Pt(8)
                p_sub.text = subtitle
                p_sub.font.name = theme["font_body"]
                p_sub.font.size = Pt(16)
                p_sub.font.color.rgb = theme["text_secondary_rgb"]

            # Intro Highlights / Agenda Card
            agenda_box = slide.shapes.add_textbox(Inches(1.8), Inches(3.9), Inches(9.8), Inches(1.8))
            render_bullet_points(agenda_box.text_frame, bullets, theme, font_size=13)

            # Footer Highlight Tag
            if stat:
                stat_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(5.6), Inches(4.5), Inches(0.55))
                stat_card.fill.solid()
                stat_card.fill.fore_color.rgb = theme["bg_rgb"]
                stat_card.line.color.rgb = theme["accent_rgb"]
                p_stat = stat_card.text_frame.paragraphs[0]
                p_stat.alignment = PP_ALIGN.CENTER
                p_stat.text = f"★ {stat}"
                p_stat.font.name = theme["font_body"]
                p_stat.font.size = Pt(11)
                p_stat.font.bold = True
                p_stat.font.color.rgb = theme["accent_rgb"]
            continue

        # ==========================================
        # STANDARD HEADER FOR CONTENT SLIDES
        # ==========================================
        # Tag Badge
        create_badge(slide, Inches(0.9), Inches(0.55), Inches(2.2), Inches(0.32), tag, theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

        # Main Title & Subtitle Textbox
        header_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.92), Inches(11.5), Inches(1.1))
        htf = header_box.text_frame
        htf.word_wrap = True
        hp = htf.paragraphs[0]
        hp.text = title
        hp.font.name = theme["font_title"]
        hp.font.size = Pt(26)
        hp.font.bold = True
        hp.font.color.rgb = theme["text_primary_rgb"]

        if subtitle:
            hp_sub = htf.add_paragraph()
            hp_sub.space_before = Pt(4)
            hp_sub.text = subtitle
            hp_sub.font.name = theme["font_body"]
            hp_sub.font.size = Pt(13)
            hp_sub.font.color.rgb = theme["text_secondary_rgb"]

        # ==========================================
        # LAYOUT: THREE CARDS
        # ==========================================
        if layout_type == "three_cards":
            card_w = Inches(3.64)
            card_h = Inches(4.5)
            spacing = Inches(0.3)
            start_x = Inches(0.9)
            start_y = Inches(2.15)

            card_icons = ["01", "02", "03"]
            for c_idx, bp in enumerate(bullets[:3]):
                c_x = start_x + (c_idx * (card_w + spacing))
                card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, start_y, card_w, card_h)
                card_shape.fill.solid()
                card_shape.fill.fore_color.rgb = theme["card_bg_rgb"]
                card_shape.line.color.rgb = theme["card_border_rgb"]
                card_shape.line.width = Pt(1.2)

                # Icon number badge inside card
                create_badge(slide, c_x + Inches(0.3), start_y + Inches(0.3), Inches(0.6), Inches(0.35), card_icons[c_idx], theme["accent_rgb"], theme["bg_rgb"], theme["font_body"])

                c_box = slide.shapes.add_textbox(c_x + Inches(0.25), start_y + Inches(0.85), card_w - Inches(0.5), card_h - Inches(1.0))
                render_bullet_points(c_box.text_frame, [bp], theme, font_size=13.5)
            continue

        # ==========================================
        # LAYOUT: SPLIT IMAGE (LEFT OR RIGHT)
        # ==========================================
        is_image_left = (layout_type == "split_image_left")
        
        # Dimensions for split view
        content_w = Inches(6.5)
        content_h = Inches(4.7)
        img_w = Inches(4.7)
        img_h = Inches(4.7)

        if is_image_left:
            img_left = Inches(0.9)
            content_left = Inches(5.9)
        else:
            content_left = Inches(0.9)
            img_left = Inches(7.7)

        card_top = Inches(2.15)

        # Content Card
        c_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, content_left, card_top, content_w, content_h)
        c_card.fill.solid()
        c_card.fill.fore_color.rgb = theme["card_bg_rgb"]
        c_card.line.color.rgb = theme["card_border_rgb"]
        c_card.line.width = Pt(1.2)

        # Content Points Textbox
        tb_bullets = slide.shapes.add_textbox(content_left + Inches(0.35), card_top + Inches(0.3), content_w - Inches(0.7), Inches(3.3))
        render_bullet_points(tb_bullets.text_frame, bullets, theme, font_size=13.5)

        # Highlight Stat Callout at bottom of content card
        if stat:
            st_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, content_left + Inches(0.35), card_top + Inches(3.8), content_w - Inches(0.7), Inches(0.6))
            st_card.fill.solid()
            st_card.fill.fore_color.rgb = theme["bg_rgb"]
            st_card.line.color.rgb = theme["accent_rgb"]
            sp = st_card.text_frame.paragraphs[0]
            sp.alignment = PP_ALIGN.CENTER
            sp.text = f"💡 {stat}"
            sp.font.name = theme["font_body"]
            sp.font.size = Pt(11.5)
            sp.font.bold = True
            sp.font.color.rgb = theme["accent_rgb"]

        # Visual Card (Image / Graphic Frame)
        img_frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_left, card_top, img_w, img_h)
        img_frame.fill.solid()
        img_frame.fill.fore_color.rgb = theme["card_bg_rgb"]
        img_frame.line.color.rgb = theme["card_border_rgb"]
        img_frame.line.width = Pt(1.2)

        if include_images:
            try:
                local_img_path = fetch_ai_image(img_prompt, seed=idx * 17 + 42)
                if local_img_path and os.path.exists(local_img_path):
                    # Add image inside the frame area with small inset padding
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
    print(f"[PPTXGenerator] Generated PPTX saved at: {file_path}")
    return file_id, file_path
