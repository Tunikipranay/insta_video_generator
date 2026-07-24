from manim import *
from house_style import *
import config

class S1_Hook(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title and hook text
        hook_text = Text(
            "Most Python devs write loops like it's 2005.",
            font_size=40,
            color=config.ACCENT
        )
        
        self.play(FadeIn(hook_text, run_time=2))
        self.wait(1)
        
        # Split screen setup
        left_code = code_block(
            """result = []
for x in range(5):
    result.append(x * 2)""",
            font_size=24
        )
        left_code.shift(LEFT * 3.5)
        
        right_code = code_block(
            "[x * 2 for x in range(5)]",
            font_size=28
        )
        right_code.shift(RIGHT * 3.5)
        
        self.play(hook_text.animate.shift(UP * 3.5), run_time=1)
        self.play(
            FadeIn(left_code, run_time=1.5),
            FadeIn(right_code, run_time=1.5)
        )
        self.wait(1)
        
        # Fade left to gray, right glows
        self.play(
            left_code.animate.set_opacity(0.3),
            run_time=1
        )
        
        glow = glow_dot(right_code, radius=0.8, color=config.ACCENT_2)
        self.add(glow)
        self.play(
            glow.animate.scale(1.2),
            run_time=1
        )
        self.wait(1)


class S2_Concept(Scene):
    def construct(self):
        apply_theme(self)
        
        title = Text("List Comprehension Anatomy", font_size=36, color=config.ACCENT)
        self.add(title)
        title.shift(UP * 3.5)
        
        # Build the comprehension piece by piece
        bracket_open = Text("[", font_size=48, color=config.ACCENT_3)
        expression = code_block("x * 2", font_size=32)
        for_text = Text("for", font_size=28, color=config.ACCENT)
        variable = Text("x", font_size=32, color=config.ACCENT_4)
        in_text = Text("in", font_size=28, color=config.ACCENT)
        iterable = code_block("range(5)", font_size=28)
        bracket_close = Text("]", font_size=48, color=config.ACCENT_3)
        
        parts = VGroup(
            bracket_open,
            expression,
            for_text,
            variable,
            in_text,
            iterable,
            bracket_close
        )
        parts.arrange(RIGHT, buff=0.3)
        parts.shift(DOWN * 0.5)
        
        self.play(LaggedStart(
            *[FadeIn(part, run_time=1.5) for part in parts],
            lag_ratio=0.15,
            run_time=6
        ))
        self.wait(1)
        
        # Show input list
        input_list = Text("[0, 1, 2, 3, 4]", font_size=28, color=config.ACCENT_2)
        input_list.shift(DOWN * 2)
        self.play(FadeIn(input_list, run_time=1.5))
        self.wait(0.5)
        
        # Show transformation flow
        arrow1 = Text("→", font_size=36, color=config.ACCENT)
        arrow1.shift(DOWN * 2)
        arrow1.shift(RIGHT * 1.5)
        self.play(FadeIn(arrow1, run_time=1))
        
        # Show output
        output_list = Text("[0, 2, 4, 6, 8]", font_size=28, color=config.ACCENT_3)
        output_list.shift(DOWN * 2)
        output_list.shift(RIGHT * 4)
        self.play(FadeIn(output_list, run_time=1.5))
        self.wait(3)


class S3_UseCase(Scene):
    def construct(self):
        apply_theme(self)
        
        title = Text("Real World: Email Cleaning", font_size=36, color=config.ACCENT)
        title.shift(UP * 3.5)
        self.add(title)
        
        # Show raw email data
        raw_emails = code_block(
            """emails = [
    '  Alice@Gmail.com',
    'bob@YAHOO.com',
    ' CHARLIE@outlook.com'
]""",
            font_size=20
        )
        raw_emails.shift(LEFT * 2 + UP * 1)
        
        self.play(FadeIn(raw_emails, run_time=2))
        self.wait(1)
        
        # Show the comprehension
        comprehension = code_block(
            "[email.strip().lower() for email in emails]",
            font_size=24
        )
        comprehension.shift(DOWN * 0.5)
        
        self.play(FadeIn(comprehension, run_time=1.5))
        self.wait(1)
        
        # Show transformation
        transform_text = Text("Transformation pipeline:", font_size=24, color=config.ACCENT_4)
        transform_text.shift(DOWN * 2)
        self.play(FadeIn(transform_text, run_time=1))
        
        # Show steps
        step1 = Text(".strip() removes spaces", font_size=18, color=config.ACCENT_2)
        step1.shift(DOWN * 2.7)
        step1.shift(LEFT * 1.5)
        
        step2 = Text(".lower() converts case", font_size=18, color=config.ACCENT_2)
        step2.shift(DOWN * 3.2)
        step2.shift(LEFT * 1.5)
        
        self.play(
            FadeIn(step1, run_time=1),
            FadeIn(step2, run_time=1)
        )
        self.wait(1)
        
        # Show result
        result = code_block(
            """[
    'alice@gmail.com',
    'bob@yahoo.com',
    'charlie@outlook.com'
]""",
            font_size=20
        )
        result.shift(RIGHT * 2 + DOWN * 1)
        
        self.play(FadeIn(result, run_time=2))
        self.wait(3)


class S4_Payoff(Scene):
    def construct(self):
        apply_theme(self)
        
        # Create comparison — slow = red, fast = green, boxes sized to text
        def badge(title, sub, color):
            t = Text(title, font_size=30, color=color)
            s = Text(sub, font_size=24, color=GREY_B)
            inner = VGroup(t, s).arrange(DOWN, buff=0.3)
            box = RoundedRectangle(corner_radius=0.18,
                                   width=inner.get_width() + 0.9,
                                   height=inner.get_height() + 0.7,
                                   stroke_color=color, stroke_width=2.5,
                                   fill_color="#161b24", fill_opacity=1)
            inner.move_to(box)
            return VGroup(box, inner)

        left_side = badge("for loop", "slower", config.ACCENT_3).shift(LEFT * 3.4)
        right_side = badge("list comprehension", "faster ✓",
                           config.ACCENT_4).shift(RIGHT * 3.0)

        self.play(
            FadeIn(left_side, run_time=1.5),
            FadeIn(right_side, run_time=1.5)
        )
        self.wait(2)

        # Fade left, crown right
        self.play(left_side.animate.set_opacity(0.25), run_time=1.5)
        self.wait(1)
        win = SurroundingRectangle(right_side, color=config.ACCENT_4,
                                   corner_radius=0.2, buff=0.15)
        takeaway = Text("one line. faster. pythonic.", font_size=34,
                        weight=BOLD, color=config.ACCENT_2)
        takeaway.to_edge(DOWN, buff=0.8)
        self.play(Create(win), Write(takeaway), run_time=1.5)
        self.wait(2)


class S5_CTA(Scene):
    def construct(self):
        apply_theme(self)
        
        card = end_card()
        
        self.play(
            FadeIn(card, run_time=2),
            card.animate.scale(1.05),
            run_time=2
        )
        self.wait(3)