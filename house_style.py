"""
House style: reusable cinematic components so every video looks like
one channel. Import this in every scene file.
"""
from manim import *
import config

# Apply global look
Text.set_default(color=config.TEXT_COLOR, font_size=36)


def apply_theme(scene: Scene):
    scene.camera.background_color = config.BG_COLOR


def glow_dot(point=ORIGIN, color=None, radius=0.09):
    """A dot with a soft glow — the signature 3b1b feel."""
    color = color or config.ACCENT
    layers = VGroup()
    for i, (r, op) in enumerate([(radius * 5, 0.08), (radius * 3, 0.15),
                                 (radius * 1.8, 0.3), (radius, 1.0)]):
        layers.add(Dot(point=point, radius=r, color=color,
                       fill_opacity=op, stroke_width=0))
    return layers


def title_card(text, sub=None):
    """Opening title with accent underline."""
    t = Text(text, font_size=56, weight=BOLD)
    underline = Line(LEFT, RIGHT, color=config.ACCENT, stroke_width=6)
    underline.set_width(t.get_width() * 0.6)
    underline.next_to(t, DOWN, buff=0.25)
    g = VGroup(t, underline)
    if sub:
        s = Text(sub, font_size=28, color=GREY_B)
        s.next_to(underline, DOWN, buff=0.35)
        g.add(s)
    return g


def code_block(code_str, language="python", font_size=26):
    """Dark rounded code window with traffic-light dots."""
    code = Code(
        code_string=code_str,
        language=language,
        background="window",
        formatter_style="monokai",
        paragraph_config={"font_size": font_size,
                          "font": config.CODE_FONT},
    )
    return code


def kv_box(key, value, key_color=None, val_color=None, width=3.4):
    """A key → value cell used for dict visualisations."""
    key_color = key_color or config.ACCENT
    val_color = val_color or config.ACCENT_2
    kt = Text(str(key), font_size=28, color=key_color)
    vt = Text(str(value), font_size=28, color=val_color)
    arrow = Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0,
                  color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.35)
    row = VGroup(kt, arrow, vt).arrange(RIGHT, buff=0.3)
    box = RoundedRectangle(corner_radius=0.15, width=width,
                           height=row.get_height() + 0.5,
                           stroke_color=GREY_D, stroke_width=2,
                           fill_color="#161b24", fill_opacity=1)
    row.move_to(box)
    return VGroup(box, row)


def label_chip(text, color=None):
    """Small pill label, e.g. 'O(1)' or 'USE CASE'."""
    color = color or config.ACCENT
    t = Text(text, font_size=24, color=config.BG_COLOR, weight=BOLD)
    pill = RoundedRectangle(corner_radius=0.25, width=t.get_width() + 0.6,
                            height=t.get_height() + 0.35,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    t.move_to(pill)
    return VGroup(pill, t)


def end_card():
    """Standard CTA end card — identical on every video = brand memory."""
    follow = Text("Follow for more", font_size=34, color=GREY_B)
    handle = Text(config.INSTA_HANDLE, font_size=52, weight=BOLD,
                  color=config.ACCENT)
    yt = Text(f"YouTube  {config.YOUTUBE_HANDLE}", font_size=26, color=GREY_B)
    g = VGroup(follow, handle, yt).arrange(DOWN, buff=0.4)
    ring = Circle(radius=0.5, color=config.ACCENT_2, stroke_width=5)
    cam = VGroup(
        RoundedRectangle(corner_radius=0.25, width=1.1, height=1.1,
                         stroke_color=config.ACCENT_2, stroke_width=5),
        Circle(radius=0.28, color=config.ACCENT_2, stroke_width=5),
        Dot(radius=0.05, color=config.ACCENT_2).shift(UP * 0.35 + RIGHT * 0.35),
    )
    cam.next_to(g, UP, buff=0.5)
    return VGroup(cam, g)
