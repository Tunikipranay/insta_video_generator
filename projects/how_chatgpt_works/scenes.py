"""Episode 1: How ChatGPT Works — series intro, house-style Manim scenes."""
from manim import *
from house_style import *
import config


def token_chip(text, color, font_size=28):
    t = Text(text, font_size=font_size, color=color, font=config.CODE_FONT)
    box = RoundedRectangle(corner_radius=0.12,
                           width=t.get_width() + 0.45,
                           height=t.get_height() + 0.4,
                           stroke_color=color, stroke_width=2,
                           fill_color="#161b24", fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


# ----------------------------------------------------------------- S1: HOOK
class S1_Hook(Scene):
    """~9s. Chat reply appears word by word; freeze on next-word choice."""

    def construct(self):
        apply_theme(self)

        # user bubble
        u_text = Text("explain gravity", font_size=28)
        u_box = RoundedRectangle(corner_radius=0.25,
                                 width=u_text.get_width() + 0.7,
                                 height=u_text.get_height() + 0.55,
                                 fill_color="#1d3a4f", fill_opacity=1,
                                 stroke_color=config.ACCENT, stroke_width=1.5)
        u_text.move_to(u_box)
        user = VGroup(u_box, u_text).move_to(UP * 2.4 + RIGHT * 3.2)

        # ai reply words
        words = VGroup(*[Text(w, font_size=30)
                         for w in ["Gravity", "is", "the", "force", "that",
                                   "pulls"]])
        words.arrange(RIGHT, buff=0.22).move_to(UP * 0.9 + LEFT * 1.2)
        a_box = RoundedRectangle(corner_radius=0.25,
                                 width=words.get_width() + 0.8,
                                 height=words.get_height() + 0.6,
                                 fill_color="#161b24", fill_opacity=1,
                                 stroke_color=GREY_D, stroke_width=1.5)
        a_box.move_to(words)

        self.play(FadeIn(user, shift=LEFT * 0.3), run_time=0.7)
        self.play(FadeIn(a_box), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.12) for w in words],
                              lag_ratio=0.35), run_time=1.8)

        # the freeze: what comes next?
        q = Text("?", font_size=34, weight=BOLD, color=config.ACCENT_2)
        q.next_to(words, RIGHT, buff=0.3)
        self.play(FadeIn(q, scale=1.5), run_time=0.4)

        cands = VGroup(
            label_chip("objects   72%", color=config.ACCENT_4),
            label_chip("you   11%", color=config.ACCENT),
            label_chip("planets   9%", color=config.ACCENT_2),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.8)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cands],
                              lag_ratio=0.2), run_time=1.0)
        ring = SurroundingRectangle(cands[0], color=config.ACCENT_4,
                                    corner_radius=0.25, buff=0.1)
        self.play(Create(ring), run_time=0.5)

        title = Text("it's just predicting the next word",
                     font_size=38, weight=BOLD, color=config.ACCENT)
        title.move_to(DOWN * 2.5)
        self.play(Write(title), run_time=1.3)
        self.wait(2.3)


# --------------------------------------------------------------- S2: TOKENS
class S2_Tokens(Scene):
    """~16s. Sentence -> token chips -> columns of numbers."""

    def construct(self):
        apply_theme(self)

        step = label_chip("STEP 1 · TOKENS", color=config.ACCENT).to_corner(UL, buff=0.45)
        self.play(FadeIn(step, scale=0.85), run_time=0.6)

        sentence = Text('"how does chatgpt work?"', font_size=40)
        sentence.move_to(UP * 1.6)
        self.play(Write(sentence), run_time=1.4)
        self.wait(0.5)

        pieces = ["how", "does", "chat", "gpt", "work", "?"]
        colors = [config.ACCENT, config.ACCENT_2, config.ACCENT_3,
                  config.ACCENT_4, config.ACCENT, config.ACCENT_2]
        chips = VGroup(*[token_chip(p, c) for p, c in zip(pieces, colors)])
        chips.arrange(RIGHT, buff=0.25).move_to(UP * 0.2)
        self.play(ReplacementTransform(sentence, chips),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)

        # highlight the chatgpt split
        split_ring = SurroundingRectangle(VGroup(chips[2], chips[3]),
                                          color=config.ACCENT_3,
                                          corner_radius=0.15, buff=0.12)
        split_cap = Text('"chatgpt"  =  2 tokens', font_size=26,
                         color=config.ACCENT_3)
        split_cap.next_to(split_ring, UP, buff=0.3)
        self.play(Create(split_ring), FadeIn(split_cap, shift=DOWN * 0.15),
                  run_time=0.9)
        self.wait(1.2)
        self.play(FadeOut(split_ring), FadeOut(split_cap), run_time=0.5)

        # numbers pour out of each chip
        cols = VGroup()
        for chip in chips:
            nums = Text("0.12\n-0.98\n0.44\n⋮", font_size=17,
                        color=GREY_B, line_spacing=0.8)
            nums.next_to(chip, DOWN, buff=0.45)
            cols.add(nums)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cols],
                              lag_ratio=0.12), run_time=1.6)

        cap = Text("every token becomes a vector — AI only speaks math",
                   font_size=28, color=config.ACCENT_2)
        cap.to_edge(DOWN, buff=0.7)
        self.play(Write(cap), run_time=1.2)
        self.wait(7.0)


# ---------------------------------------------------------- S3: TRANSFORMER
class S3_Transformer(ThreeDScene):
    """~15s. 3D attention web rising through a stack of layers."""

    def construct(self):
        apply_theme(self)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES,
                                    zoom=0.9)

        step = label_chip("STEP 2 · THE TRANSFORMER", color=config.ACCENT_2)
        self.add_fixed_in_frame_mobjects(step)
        step.to_corner(UL, buff=0.45).set_opacity(0)

        # stack of layers along z
        layers = VGroup()
        for i in range(4):
            sq = Square(side_length=4.6)
            sq.set_fill(config.ACCENT, opacity=0.10)
            sq.set_stroke(config.ACCENT, width=1.8, opacity=0.8)
            sq.shift(OUT * (0.9 * i + 0.6))
            layers.add(sq)

        # token dots on the ground
        xs = [-1.8, -0.9, 0.0, 0.9, 1.8]
        dots = VGroup(*[glow_dot([x, 0, -0.4], color=config.ACCENT_2)
                        for x in xs])

        self.play(step.animate.set_opacity(1),
                  LaggedStart(*[FadeIn(sq, shift=OUT * 0.4) for sq in layers],
                              lag_ratio=0.15),
                  run_time=2.0)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.1), run_time=1.0)
        self.begin_ambient_camera_rotation(rate=0.055)

        # attention web: every token connects to every token on layer 1
        lines = VGroup()
        for xa in xs:
            for xb in xs:
                ln = Line([xa, 0, -0.4], [xb, 0, 0.6],
                          stroke_color=config.ACCENT_2, stroke_width=1.6,
                          stroke_opacity=0.45)
                lines.add(ln)
        self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.02),
                  run_time=2.6)

        cap = Text("every token attends to every other token",
                   font_size=28, color=GREY_A)
        self.add_fixed_in_frame_mobjects(cap)
        cap.to_edge(DOWN, buff=0.7).set_opacity(0)
        self.play(cap.animate.set_opacity(1), run_time=0.8)

        # a spark rises through the stack = the signal flowing up
        spark = glow_dot([0, 0, 0.6], color=config.ACCENT_4)
        self.add(spark)
        self.play(spark.animate.move_to([0, 0, 3.6]),
                  run_time=1.8, rate_func=rate_functions.ease_in_out_sine)
        self.play(Flash([0, 0, 3.6], color=config.ACCENT_4, flash_radius=0.8),
                  FadeOut(spark), run_time=0.6)
        self.wait(6.2)
        self.stop_ambient_camera_rotation()


# -------------------------------------------------------------- S4: PREDICT
class S4_Predict(Scene):
    """~17s. Probability ranking, pick, append, repeat — and the catch."""

    def construct(self):
        apply_theme(self)

        step = label_chip("STEP 3 · PREDICT", color=config.ACCENT_4)
        step.to_corner(UL, buff=0.45)
        self.play(FadeIn(step, scale=0.85), run_time=0.5)

        prompt = Text("The capital of France is", font_size=34)
        blank = Text("____", font_size=34, color=config.ACCENT_2)
        line = VGroup(prompt, blank).arrange(RIGHT, buff=0.3).move_to(UP * 2.3)
        self.play(Write(prompt), FadeIn(blank), run_time=1.2)

        # ranked probability bars
        data = [("Paris", 0.92, config.ACCENT_4),
                ("Lyon", 0.03, config.ACCENT),
                ("Rome", 0.02, config.ACCENT_2),
                ("banana", 0.0001, config.ACCENT_3)]
        rows = VGroup()
        for name, p, color in data:
            label = Text(name, font_size=26, font=config.CODE_FONT)
            label.set_width(min(label.get_width(), 1.8))
            bar = Rectangle(width=max(5.5 * p, 0.12), height=0.34,
                            fill_color=color, fill_opacity=0.9, stroke_width=0)
            pct = Text(f"{p:.2%}" if p >= 0.01 else "0.01%",
                       font_size=22, color=GREY_B)
            row = VGroup(label, bar, pct)
            rows.add(row)
        # align: labels right-aligned at fixed x, bars grow rightward
        y = 0.9
        for row in rows:
            label, bar, pct = row
            label.move_to([-3.2, y, 0], aligned_edge=RIGHT)
            bar.move_to([-2.8, y, 0], aligned_edge=LEFT)
            pct.next_to(bar, RIGHT, buff=0.25)
            y -= 0.75
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.4) for r in rows],
                              lag_ratio=0.15), run_time=1.6)
        self.wait(1.2)

        # Paris wins and flies into the blank
        ring = SurroundingRectangle(rows[0], color=config.ACCENT_4,
                                    corner_radius=0.12, buff=0.15)
        self.play(Create(ring), run_time=0.6)
        paris = Text("Paris", font_size=34, weight=BOLD, color=config.ACCENT_4)
        paris.move_to(rows[0][0])
        self.add(paris)
        self.play(paris.animate.move_to(blank.get_center()),
                  blank.animate.set_opacity(0),
                  run_time=0.9, rate_func=rate_functions.ease_in_out_sine)

        # repeat loop
        arrow = CurvedArrow(paris.get_top() + UP * 0.15 + RIGHT * 0.4,
                            prompt.get_corner(UL) + UP * 0.25,
                            angle=TAU / 7, color=config.ACCENT,
                            stroke_width=3, tip_length=0.2)
        rep = Text("repeat", font_size=24, color=config.ACCENT)
        rep.next_to(line, UP, buff=0.55)
        self.play(Create(arrow), FadeIn(rep), run_time=1.0)
        self.wait(1.5)

        catch = VGroup(
            Text("it ranks likely words — it never checks facts",
                 font_size=28, color=config.ACCENT_3),
            Text("that's why it can be confidently wrong",
                 font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        self.play(Write(catch[0]), run_time=1.2)
        self.play(FadeIn(catch[1], shift=UP * 0.15), run_time=0.8)
        self.wait(6.5)


# -------------------------------------------------------------- S5: ROADMAP
class S5_Roadmap(Scene):
    """~13s. What's next in the series."""

    def construct(self):
        apply_theme(self)

        title = Text("coming up in this series", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.7)
        self.play(Write(title), run_time=1.2)

        def card(ep, name, teaser, color):
            chip = label_chip(ep, color=color)
            n = Text(name, font_size=32, weight=BOLD)
            t = Text(teaser, font_size=24, color=GREY_B)
            inner = VGroup(n, t).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.18, width=9.2, height=1.5,
                                   stroke_color=color, stroke_width=2,
                                   fill_color="#161b24", fill_opacity=1)
            chip.move_to(box.get_left() + RIGHT * 1.0)
            inner.move_to(box.get_left() + RIGHT * 2.0, aligned_edge=LEFT)
            return VGroup(box, chip, inner)

        cards = VGroup(
            card("EP 2", "Tokenizers", "why AI can't spell", config.ACCENT),
            card("EP 3", "Embeddings", "how meaning becomes math",
                 config.ACCENT_2),
            card("EP 4", "Attention", "the hundred-billion-dollar idea",
                 config.ACCENT_4),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 1.2) for c in cards],
                              lag_ratio=0.3),
                  run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1.0)
        for c in cards:
            self.play(c[0].animate.set_stroke(width=4), run_time=0.25)
            self.play(c[0].animate.set_stroke(width=2), run_time=0.25)
        self.wait(7.0)


# ------------------------------------------------------------------ S6: CTA
class S6_CTA(Scene):
    """~5s. Standard end card."""

    def construct(self):
        apply_theme(self)
        card = end_card()
        self.play(FadeIn(card, scale=1.08),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.wait(3.5)
