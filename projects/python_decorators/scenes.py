from manim import *
from house_style import *
import config

class S1_Hook(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = title_card("The Copy-Paste Problem")
        self.add(title)
        self.wait(0.5)
        
        # Three function definitions
        func_defs = VGroup()
        
        code1 = code_block("""def greet(name):
    start = time.time()
    print(f"Hello, {name}")
    end = time.time()
    print(f"Took {end-start}s")""", lang="python")
        code1.scale(0.6).to_edge(LEFT).shift(UP*1.5)
        
        code2 = code_block("""def calculate(x, y):
    start = time.time()
    result = x + y
    end = time.time()
    print(f"Took {end-start}s")""", lang="python")
        code2.scale(0.6).next_to(code1, RIGHT, buff=0.3).shift(UP*1.5)
        
        code3 = code_block("""def fetch_data(url):
    start = time.time()
    data = request.get(url)
    end = time.time()
    print(f"Took {end-start}s")""", lang="python")
        code3.scale(0.6).next_to(code1, DOWN, buff=0.5).align_to(code1, LEFT)
        
        func_defs.add(code1, code2, code3)
        
        # Remove title and add code
        self.remove(title)
        self.play(FadeIn(func_defs, rate_func=rate_functions.ease_in_out_sine), run_time=2)
        self.wait(1)
        
        # Highlight repeated code in red
        highlight1 = SurroundingRectangle(code1[0][-8:], color=config.ACCENT, stroke_width=3, buff=0.1)
        highlight2 = SurroundingRectangle(code2[0][-8:], color=config.ACCENT, stroke_width=3, buff=0.1)
        highlight3 = SurroundingRectangle(code3[0][-8:], color=config.ACCENT, stroke_width=3, buff=0.1)
        
        self.play(Create(highlight1), run_time=1)
        self.wait(0.8)
        self.play(Create(highlight2), run_time=1)
        self.wait(0.8)
        self.play(Create(highlight3), run_time=1)
        self.wait(1)
        
        # Text callout
        question = Text("Copy-paste everywhere?", color=config.ACCENT, font_size=36)
        question.to_edge(DOWN)
        self.play(FadeIn(question, shift=UP*0.5), run_time=1)
        self.wait(2)
        
        # hold on the pain point — never end a scene on black
        self.wait(2)

class S2_Before(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = Text("Option 1: Edit the function", color=config.ACCENT, font_size=32)
        title.to_edge(UP)
        self.add(title)
        self.wait(0.3)
        
        # Left side: function with timing mixed in
        left_label = Text("Edit function directly", color=config.ACCENT_2, font_size=24)
        left_label.scale(0.7).to_edge(UP, buff=1.5).to_edge(LEFT, buff=1)
        
        left_code = code_block("""def my_function():
    start = time.time()
    # ... main logic ...
    end = time.time()
    print(f"Time: {end-start}s")""", lang="python")
        left_code.scale(0.55).next_to(left_label, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        
        self.play(FadeIn(left_label), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(left_code), run_time=1.5)
        self.wait(1.5)
        
        # Right side: wrapper every time you call
        right_label = Text("Wrap every call", color=config.ACCENT_2, font_size=24)
        right_label.scale(0.7).to_edge(UP, buff=1.5).to_edge(RIGHT, buff=1)
        
        right_code = code_block("""# Call site 1
start = time.time()
my_function()
end = time.time()
print(f"Time: {end-start}s")

# Call site 2
start = time.time()
my_function()
end = time.time()
print(f"Time: {end-start}s")""", lang="python")
        right_code.scale(0.5).next_to(right_label, DOWN, buff=0.3).to_edge(RIGHT, buff=0.3)
        
        self.play(FadeIn(right_label), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(right_code), run_time=1.5)
        self.wait(1.5)
        
        # Highlight the problem on the right
        problem_box = SurroundingRectangle(right_code, color=config.ACCENT, stroke_width=2.5, buff=0.2)
        self.play(Create(problem_box), run_time=1)
        
        problem_text = Text("Tedious & error-prone", color=config.ACCENT, font_size=20)
        problem_text.next_to(problem_box, DOWN, buff=0.3)
        self.play(FadeIn(problem_text, shift=UP*0.3), run_time=0.8)
        self.wait(2)
        
        # Fade everything
        self.wait(2)

class S3_Concept(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = title_card("Decorators: The Mail Room Metaphor")
        self.add(title)
        self.wait(0.5)
        self.remove(title)
        
        # Mailroom scene
        # Building outline
        building = Rectangle(width=8, height=5, color=config.ACCENT_2, stroke_width=2)
        building.shift(LEFT*2 + DOWN*0.5)
        
        # Window for mail room
        window = Rectangle(width=1.5, height=1.5, color=config.ACCENT, stroke_width=2)
        window.move_to(building.get_corner(UP+RIGHT) + LEFT*1 + DOWN*0.5)
        
        # Mail clerk (simple circle)
        clerk = Circle(radius=0.4, color=config.ACCENT_2, fill_opacity=0.3, stroke_width=2)
        clerk.move_to(window)
        
        # Package (function)
        package = Rectangle(width=1, height=1.2, color=config.ACCENT_3, fill_opacity=0.5, stroke_width=2)
        package_label = Text("your_function()", font_size=16, color=WHITE)
        package_label.scale(0.5).move_to(package)
        package_group = VGroup(package, package_label)
        package_group.move_to(LEFT*4 + UP*1.5)
        
        self.play(FadeIn(building), FadeIn(window), FadeIn(clerk), FadeIn(package_group), run_time=2)
        self.wait(1)
        
        # Animate package moving to clerk
        self.play(package_group.animate.move_to(window), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1)
        
        # Stamps appear (decorator options)
        stamp1 = Text("@timer", font_size=18, color=config.ACCENT).shift(RIGHT*2 + UP*1)
        stamp2 = Text("@log", font_size=18, color=config.ACCENT).shift(RIGHT*2)
        stamp3 = Text("@check_permissions", font_size=18, color=config.ACCENT).shift(RIGHT*2 + DOWN*1)
        stamps = VGroup(stamp1, stamp2, stamp3)
        
        self.play(FadeIn(stamps, lag_ratio=0.3, rate_func=rate_functions.ease_in_out_sine), run_time=1.5)
        self.wait(1.5)
        
        # Wrap the package (add glow and border)
        wrapped_box = Rectangle(width=1.4, height=1.6, color=config.ACCENT_4, stroke_width=2.5)
        wrapped_box.move_to(window)
        wrapped_label = Text("wrapper", font_size=14, color=WHITE)
        wrapped_label.scale(0.5).move_to(window)
        
        self.play(FadeOut(stamps), FadeIn(wrapped_box), FadeIn(wrapped_label), 
                  Uncreate(package), run_time=1.5)
        self.wait(1)
        
        # Package emerges from the other side
        package_out_left = Rectangle(width=1, height=1.2, color=config.ACCENT_3, fill_opacity=0.7, stroke_width=2)
        package_out_label = Text("your_function()", font_size=16, color=WHITE)
        package_out_label.scale(0.5).move_to(package_out_left)
        package_out = VGroup(package_out_left, package_out_label)
        package_out.move_to(window)
        
        glow = Circle(radius=0.9, color=config.ACCENT_4, stroke_width=1.5, stroke_opacity=0.5)
        glow.move_to(window)
        
        self.play(FadeIn(glow), run_time=0.8)
        self.wait(0.5)
        
        # Move wrapped package to the right
        self.play(package_out.animate.shift(RIGHT*3), glow.animate.shift(RIGHT*3), 
                  FadeOut(wrapped_box), FadeOut(wrapped_label), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1)
        
        # Key insight text
        insight = Text("Define wrapping logic once.\nApply to many functions.", 
                      color=config.ACCENT, font_size=24, line_spacing=1.5)
        insight.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(insight, shift=UP*0.5), run_time=1)
        self.wait(2)
        
        # Fade everything
        self.wait(2)

class S4_Example(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = title_card("Real Example: Login Decorator")
        self.add(title)
        self.wait(0.5)
        self.remove(title)
        
        # Decorator definition
        decorator_code = code_block("""def require_login(func):
    def wrapper(*args, **kwargs):
        if not user_logged_in():
            return "Error: Not logged in"
        return func(*args, **kwargs)
    return wrapper""", lang="python")
        decorator_code.scale(0.65).to_edge(LEFT, buff=0.5).shift(UP*1)
        
        self.play(FadeIn(decorator_code), run_time=2)
        self.wait(1.5)
        
        # Endpoint with decorator
        endpoint_code = code_block("""@require_login
def get_user_dashboard():
    return "Your dashboard"
    
@require_login
def update_profile(name, email):
    return "Profile updated"
    
@require_login
def delete_account():
    return "Account deleted\"""", lang="python")
        endpoint_code.scale(0.65).to_edge(RIGHT, buff=0.5).shift(UP*1)
        
        # Highlight the @ symbol
        at_rect = SurroundingRectangle(endpoint_code[0][0:1], color=config.ACCENT, stroke_width=2, buff=0.1)
        
        self.play(FadeIn(endpoint_code), run_time=2)
        self.wait(1)
        self.play(Create(at_rect), run_time=0.8)
        self.wait(1)
        
        # Arrow from @ to decorator
        arrow = Arrow(endpoint_code.get_corner(UP+LEFT), decorator_code.get_corner(DOWN+RIGHT), 
                     color=config.ACCENT_2, stroke_width=2, buff=0.2)
        self.play(Create(arrow), run_time=1)
        self.wait(1.5)
        
        # Show function calls
        call_box_label = Text("Function calls:", font_size=22, color=config.ACCENT)
        call_box_label.to_edge(DOWN, buff=2)
        
        call_code = code_block("""result = get_user_dashboard()
result = update_profile("Alice", "alice@ex.com")
result = delete_account()""", lang="python")
        call_code.scale(0.6).next_to(call_box_label, DOWN, buff=0.3)
        
        self.play(FadeIn(call_box_label), FadeIn(call_code), run_time=1.5)
        self.wait(1)
        
        # Show gates (permission checks) for each call
        gate1 = Rectangle(width=0.5, height=2.5, color=config.ACCENT_4, stroke_width=2, fill_opacity=0.3)
        gate1.next_to(call_code, RIGHT, buff=0.5).shift(UP*0.3)
        gate1_label = Text("✓", font_size=32, color=config.ACCENT_4)
        gate1_label.move_to(gate1)
        gate1_group = VGroup(gate1, gate1_label)
        
        gate2 = Rectangle(width=0.5, height=2.5, color=config.ACCENT_4, stroke_width=2, fill_opacity=0.3)
        gate2.next_to(call_code, RIGHT, buff=0.5).shift(DOWN*0.3)
        gate2_label = Text("✓", font_size=32, color=config.ACCENT_4)
        gate2_label.move_to(gate2)
        gate2_group = VGroup(gate2, gate2_label)
        
        self.play(FadeIn(gate1_group), FadeIn(gate2_group), run_time=1.2)
        self.wait(1.5)
        
        # Show blocked call
        blocked_call = Text("call = blocked_endpoint()", font_size=18, color=config.ACCENT)
        blocked_call.shift(DOWN*2.5 + RIGHT*0.5)
        
        blocked_gate = Rectangle(width=0.5, height=1, color=config.ACCENT, stroke_width=2.5, fill_opacity=0.5)
        blocked_gate.next_to(blocked_call, RIGHT, buff=0.3)
        blocked_label = Text("✗", font_size=28, color=config.ACCENT)
        blocked_label.move_to(blocked_gate)
        blocked_group = VGroup(blocked_gate, blocked_label)
        
        self.play(FadeIn(blocked_call), FadeIn(blocked_group), run_time=1)
        self.wait(1.5)
        
        # Key insight
        insight = Text("One @ symbol. One logic change updates all.", 
                      color=config.ACCENT, font_size=22)
        insight.to_edge(DOWN, buff=0.3)
        
        self.play(FadeOut(VGroup(decorator_code, endpoint_code, at_rect, arrow, 
                                 call_box_label, call_code, gate1_group, gate2_group, 
                                 blocked_call, blocked_group)), 
                 FadeIn(insight), run_time=1.5)
        self.wait(3)

class S5_Recap(Scene):
    def construct(self):
        apply_theme(self)
        
        # Return to mailroom in fast-forward
        # Building
        building = Rectangle(width=7, height=4.5, color=config.ACCENT_2, stroke_width=2)
        building.shift(LEFT*2 + DOWN*0.5)
        
        # Window
        window = Rectangle(width=1.5, height=1.5, color=config.ACCENT, stroke_width=2)
        window.move_to(building.get_corner(UP+RIGHT) + LEFT*1 + DOWN*0.5)
        
        # Clerk
        clerk = Circle(radius=0.4, color=config.ACCENT_2, fill_opacity=0.3, stroke_width=2)
        clerk.move_to(window)
        
        self.play(FadeIn(building), FadeIn(window), FadeIn(clerk), run_time=1)
        self.wait(0.5)
        
        # Three packages arrive in sequence (fast)
        packages = []
        for i in range(3):
            pkg = Rectangle(width=0.8, height=1, color=config.ACCENT_3, fill_opacity=0.5, stroke_width=2)
            pkg.shift(LEFT*5 + UP*(1.5 - i*1.2))
            packages.append(pkg)
        
        # Animate packages through wrapping process quickly
        for pkg in packages:
            self.play(pkg.animate.move_to(window), run_time=0.6, rate_func=rate_functions.ease_in_out_sine)
            # Wrap
            wrapped = Rectangle(width=1.1, height=1.3, color=config.ACCENT_4, stroke_width=2)
            wrapped.move_to(window)
            glow = Circle(radius=0.8, color=config.ACCENT_4, stroke_width=1, stroke_opacity=0.4)
            glow.move_to(window)
            self.play(FadeIn(wrapped), FadeIn(glow), Uncreate(pkg), run_time=0.4)
            # Unwrap and move out
            pkg_out = Rectangle(width=0.8, height=1, color=config.ACCENT_3, fill_opacity=0.7, stroke_width=2)
            pkg_out.move_to(window)
            self.play(FadeOut(wrapped), FadeOut(glow), FadeIn(pkg_out), 
                     pkg_out.animate.shift(RIGHT*3.5), run_time=0.6, rate_func=rate_functions.ease_in_out_sine)
        
        self.wait(1)
        
        # Text overlay
        text_line1 = Text("Define once.", color=config.ACCENT, font_size=28, weight=BOLD)
        text_line2 = Text("Apply many.", color=config.ACCENT_2, font_size=28, weight=BOLD)
        text_line3 = Text("Change anywhere.", color=config.ACCENT_3, font_size=28, weight=BOLD)
        
        text_group = VGroup(text_line1, text_line2, text_line3).arrange(DOWN, buff=0.4)
        text_group.to_edge(RIGHT, buff=1).shift(DOWN*0.5)
        
        self.play(FadeIn(text_group, lag_ratio=0.3, rate_func=rate_functions.ease_in_out_sine), run_time=1.5)
        self.wait(2)
        
        # Function in gift box icon
        gift_box = Rectangle(width=1.2, height=1.2, color=config.ACCENT_4, fill_opacity=0.4, stroke_width=2)
        gift_box.shift(LEFT*3 + DOWN*1.5)
        
        func_text = Text("func()", font_size=20, color=WHITE)
        func_text.move_to(gift_box)
        
        ribbon = Line(gift_box.get_corner(UP+LEFT), gift_box.get_corner(DOWN+RIGHT), 
                     color=config.ACCENT, stroke_width=2.5)
        
        self.play(FadeIn(gift_box), FadeIn(func_text), Create(ribbon), run_time=1.5)
        self.wait(1.5)
        
        self.wait(2)

class S6_CTA(Scene):
    def construct(self):
        apply_theme(self)
        
        card = end_card()
        self.play(FadeIn(card, scale=0.9), run_time=1.5)
        self.wait(3)

class T1_Hook(Scene):
    def construct(self):
        apply_theme(self)
        
        # Three functions with repeated code
        code1 = Text("def greet():\n    start = time.time()\n    print(...)\n    end = time.time()", 
                    font_size=16, font=config.CODE_FONT, color=WHITE).shift(LEFT*2.5 + UP*1)
        code2 = Text("def calculate():\n    start = time.time()\n    result = ...\n    end = time.time()", 
                    font_size=16, font=config.CODE_FONT, color=WHITE).shift(UP*1)
        code3 = Text("def fetch_data():\n    start = time.time()\n    data = ...\n    end = time.time()", 
                    font_size=16, font=config.CODE_FONT, color=WHITE).shift(RIGHT*2.5 + UP*1)
        
        codes = VGroup(code1, code2, code3)
        self.play(FadeIn(codes, rate_func=rate_functions.ease_in_out_sine), run_time=1.5)
        self.wait(0.5)
        
        # Flash the repeated code in red
        for i in range(3):
            self.play(codes.animate.set_color(color_gradient([config.ACCENT, WHITE], 3)), run_time=0.4)
            self.play(codes.animate.set_color(WHITE), run_time=0.4)
        
        self.wait(0.5)
        
        # Question text
        question = Text("Write once. Use everywhere?", color=config.ACCENT, font_size=28)
        question.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(question, shift=UP*0.3), run_time=0.8)
        self.wait(1)
        
        # Gift box wraps around first function
        box = Rectangle(width=2.5, height=2.2, color=config.ACCENT, stroke_width=2.5)
        box.move_to(code1)
        
        self.play(Create(box), run_time=1)
        self.wait(1)
        self.play(box.animate.scale(1.1), run_time=0.6)
        
        self.wait(1.5)

class T2_Tease(Scene):
    def construct(self):
        apply_theme(self)
        
        # Mailroom animation with decorator concept
        building = Rectangle(width=6, height=4, color=config.ACCENT_2, stroke_width=2)
        building.shift(LEFT*2)
        
        window = Rectangle(width=1.2, height=1.2, color=config.ACCENT, stroke_width=2)
        window.move_to(building.get_corner(UP+RIGHT) + LEFT*0.8 + DOWN*0.4)
        
        clerk = Circle(radius=0.3, color=config.ACCENT_2, fill_opacity=0.4, stroke_width=2)
        clerk.move_to(window)
        
        self.play(FadeIn(building), FadeIn(window), FadeIn(clerk), run_time=1.2)
        self.wait(0.5)
        
        # Package arrives
        package = Rectangle(width=0.7, height=0.9, color=config.ACCENT_3, fill_opacity=0.6, stroke_width=2)
        package.shift(LEFT*4 + UP*0.8)
        
        self.play(FadeIn(package), run_time=0.5)
        self.play(package.animate.move_to(window), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)
        
        # Spiral of @ symbols wrapping
        at_symbols = []
        for angle in [0, 60, 120, 180, 240, 300]:
            at_text = Text("@", font_size=24, color=config.ACCENT_4)
            rad = np.radians(angle)
            pos = window.get_center() + np.array([0.6*np.cos(rad), 0.6*np.sin(rad), 0])
            at_text.move_to(pos)
            at_symbols.append(at_text)
        
        self.play(FadeIn(VGroup(*at_symbols), lag_ratio=0.2), Uncreate(package), run_time=1)
        self.wait(0.5)
        
        # Package emerges with glow
        package_out = Rectangle(width=0.7, height=0.9, color=config.ACCENT_3, fill_opacity=0.8, stroke_width=2.5)
        package_out.move_to(window)
        glow = Circle(radius=0.7, color=config.ACCENT_4, stroke_width=2, stroke_opacity=0.6)
        glow.move_to(window)
        
        self.play(FadeIn(glow), FadeOut(VGroup(*at_symbols)), FadeIn(package_out), run_time=0.8)
        self.wait(0.3)
        
        # Move out
        self.play(package_out.animate.shift(RIGHT*3), glow.animate.shift(RIGHT*3), run_time=1, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        
        # Three more packages go through quickly
        for i in range(3):
            pkg_in = Rectangle(width=0.6, height=0.8, color=config.ACCENT_3, fill_opacity=0.5, stroke_width=1.5)
            pkg_in.shift(LEFT*4 + UP*(0.8 - i*0.6))
            pkg_glow = Circle(radius=0.6, color=config.ACCENT_4, stroke_width=1, stroke_opacity=0.5)
            pkg_glow.move_to(window)
            self.play(FadeIn(pkg_in), run_time=0.3)
            self.play(pkg_in.animate.move_to(window), run_time=0.4, rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeIn(pkg_glow), Uncreate(pkg_in), run_time=0.3)
            pkg_out_fast = Rectangle(width=0.6, height=0.8, color=config.ACCENT_3, fill_opacity=0.7, stroke_width=1.5)
            pkg_out_fast.move_to(window)
            self.play(FadeOut(pkg_glow), FadeIn(pkg_out_fast), pkg_out_fast.animate.shift(RIGHT*3), run_time=0.4)
        
        self.wait(0.5)
        
        # Code editor with @decorator
        editor_box = Rectangle(width=4, height=2.5, color=config.ACCENT_2, stroke_width=1.5, fill_opacity=0.1)
        editor_box.shift(RIGHT*2 + DOWN*0.5)
        
        decorator_line = Text("@decorator", font_size=20, color=config.ACCENT, font=config.CODE_FONT)
        decorator_line.move_to(editor_box.get_top() + DOWN*0.4)
        
        func_line = Text("def my_function():", font_size=18, color=WHITE, font=config.CODE_FONT)
        func_line.next_to(decorator_line, DOWN, buff=0.2)
        
        self.play(FadeIn(editor_box), FadeIn(decorator_line), FadeIn(func_line), run_time=1.2)
        self.wait(1.5)
        
        # Narration text callout
        superpowers = Text("Superpowers: timing, logging,\npermissions, and more.", 
                          color=config.ACCENT_2, font_size=18, line_spacing=1.3)
        superpowers.shift(RIGHT*2 + DOWN*2.2)
        self.play(FadeIn(superpowers, shift=UP*0.3), run_time=1)
        self.wait(2)
        
        self.wait(1.5)

class T3_CTA(Scene):
    def construct(self):
        apply_theme(self)
        
        card = end_card(title="Full video on YouTube")
        self.play(FadeIn(card, scale=0.9), run_time=1.5)
        self.wait(3)