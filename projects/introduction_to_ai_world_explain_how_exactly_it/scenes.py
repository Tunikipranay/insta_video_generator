from manim import *
from house_style import *
import config

class S1_Hook(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("How AI Really Works")
        self.play(FadeIn(title))
        self.wait(1)
        
        # Smartphone mockup
        phone_bg = RoundedRectangle(corner_radius=0.3, width=2.5, height=4.5, stroke_width=2, stroke_color=config.ACCENT)
        phone_screen = RoundedRectangle(corner_radius=0.25, width=2.3, height=4.3, fill_color=config.BG_COLOR, fill_opacity=1, stroke_width=0)
        phone = VGroup(phone_bg, phone_screen).arrange(DOWN)
        
        # Chat bubbles
        user_question = Text("What's a good\nbedtime routine?", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        user_bubble = RoundedRectangle(corner_radius=0.2, width=2, height=0.8, fill_color=config.ACCENT, fill_opacity=0.3, stroke_width=0)
        user_bubble.surround(user_question, stretch=True, dim_to_match=0)
        user_msg = VGroup(user_bubble, user_question)
        user_msg.next_to(phone_screen, RIGHT, buff=-1.9).shift(UP*0.8)
        
        phone_with_chat = VGroup(phone, user_msg)
        phone_with_chat = fit(phone_with_chat, height=4.5)
        
        self.play(FadeIn(phone_with_chat), run_time=1.5)
        self.wait(1.5)
        
        # AI response appears word by word
        response_words = ["Here's", "a", "good", "routine:", "Dim", "lights", "one", "hour", "before", "bed..."]
        ai_response_texts = []
        
        for i, word in enumerate(response_words):
            word_text = Text(word, font_size=24, font=config.FONT_NAME, color=config.ACCENT)
            ai_response_texts.append(word_text)
        
        ai_response_group = VGroup(*ai_response_texts).arrange(RIGHT, buff=0.15)
        ai_bubble = RoundedRectangle(corner_radius=0.2, width=2.2, height=1, fill_color=config.ACCENT_2, fill_opacity=0.2, stroke_width=0)
        ai_bubble.surround(ai_response_group, stretch=True, dim_to_match=0)
        ai_msg = VGroup(ai_bubble, ai_response_group)
        ai_msg.next_to(phone_screen, LEFT, buff=-1.9).shift(DOWN*0.5)
        
        # Animate word by word
        for word_text in ai_response_texts:
            self.play(FadeIn(word_text), run_time=0.3)
        
        phone_with_chat.add(ai_msg)
        self.wait(2)
        
        # Zoom in on response
        self.play(phone_with_chat.animate.scale(1.3), run_time=1.5)
        self.wait(2)
        
        # Fade to black with question mark
        self.play(FadeOut(phone_with_chat), FadeOut(title), run_time=1.5)
        question_mark = Text("?", font_size=100, font=config.FONT_NAME, color=config.ACCENT)
        self.play(FadeIn(question_mark), question_mark.animate.scale(1.5), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(question_mark), run_time=1)
        self.wait(0.5)


class S2_Before(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("The Old Way: Rules")
        self.play(FadeIn(title))
        self.wait(3.7)
        
        cur = None
        
        # Beat 1: Simple if-then rules
        rule1 = Text("IF user types 'hello'", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        rule2 = Text("THEN output 'Hi there!'", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        rule_group = VGroup(rule1, rule2).arrange(DOWN, buff=0.4)
        cur = swap(self, cur, rule_group)
        self.wait(4.7)
        
        # Beat 2: More rules appear
        rules_list = VGroup(
            Text("IF user types 'hello' → THEN say 'Hi'", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("IF user types 'help' → THEN show menu", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("IF user types 'price' → THEN show $99", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("IF user types 'bye' → THEN say 'Goodbye'", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.5)
        cur = swap(self, cur, rules_list)
        self.wait(5.2)
        
        # Beat 3: Rules multiply and tangle
        tangled_rules = VGroup(
            Text("If-Then Rule #1", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("If-Then Rule #2", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("If-Then Rule #3", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("If-Then Rule #4", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("If-Then Rule #5", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("If-Then Rule #6", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("...", font_size=28, font=config.FONT_NAME, color=config.ACCENT),
        ).arrange(DOWN, buff=0.3)
        cur = swap(self, cur, tangled_rules)
        self.wait(5.2)
        
        # Beat 4: Frustrated person with papers
        person_circle = Circle(radius=0.3, fill_color=config.ACCENT_3, fill_opacity=0.6, stroke_width=1, stroke_color=config.ACCENT)
        person_label = Text("Programmer", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        person = VGroup(person_circle, person_label).arrange(DOWN, buff=0.2)
        
        papers = VGroup()
        for i in range(5):
            paper = RoundedRectangle(width=0.6, height=1, corner_radius=0.05, fill_color=config.ACCENT_2, fill_opacity=0.5, stroke_width=1)
            paper.shift(UP * 0.15 * i)
            papers.add(paper)
        
        papers.next_to(person, RIGHT, buff=0.5)
        group = VGroup(person, papers)
        group = fit(group, height=4)
        cur = swap(self, cur, group)
        self.wait(4.7)
        
        # Beat 5: Papers topple
        self.play(papers.animate.shift(RIGHT*0.8 + UP*1.5), run_time=1.5)
        self.wait(4.2)
        
        # Beat 6: Question text
        question_text = Text("What about questions\nwe didn't think of?", font_size=32, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, question_text)
        self.wait(5.7)


class S3_Concept(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("Learning from Examples")
        self.play(FadeIn(title))
        self.wait(3.6)
        
        cur = None
        
        # Beat 1: Mail sorter setup
        sorter_head = Circle(radius=0.25, fill_color=config.ACCENT_3, fill_opacity=0.7, stroke_width=1)
        sorter_body = Rectangle(width=0.4, height=0.6, fill_color=config.ACCENT_3, fill_opacity=0.6, stroke_width=1)
        sorter_body.next_to(sorter_head, DOWN, buff=0.05)
        sorter = VGroup(sorter_head, sorter_body)
        sorter_label = Text("Mail Sorter", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR)
        sorter_label.next_to(sorter, DOWN, buff=0.3)
        sorter_full = VGroup(sorter, sorter_label)
        
        # Bins
        bins = VGroup()
        bin_labels = ["Northeast", "Midwest", "South", "West"]
        for i, label in enumerate(bin_labels):
            bin_rect = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, fill_color=config.ACCENT_2, fill_opacity=0.4, stroke_width=1, stroke_color=config.ACCENT)
            bin_text = Text(label, font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
            bin_text.scale(0.8)
            bin_full = VGroup(bin_rect, bin_text).arrange(DOWN)
            bin_full.shift(RIGHT * (i - 1.5) * 1.2)
            bins.add(bin_full)
        
        sorter_full.shift(UP * 1.5)
        bins.shift(DOWN * 1.5)
        
        scene1 = VGroup(sorter_full, bins)
        scene1 = fit(scene1, height=4.5)
        cur = swap(self, cur, scene1)
        self.wait(4.6)
        
        # Beat 2: First letter with features
        letter1 = Rectangle(width=0.4, height=0.6, fill_color=config.ACCENT, fill_opacity=0.3, stroke_width=1)
        letter1.shift(UP * 0.5 + LEFT * 2.5)
        features1 = VGroup(
            Text("Zip: 02134", font_size=24, font=config.FONT_NAME, color=config.ACCENT_4),
            Text("Size: Small", font_size=24, font=config.FONT_NAME, color=config.ACCENT_4),
        ).arrange(DOWN, buff=0.2)
        features1.next_to(letter1, RIGHT, buff=0.3)
        
        letter_group1 = VGroup(letter1, features1)
        self.play(FadeIn(letter_group1), run_time=1)
        scene1.add(letter_group1)
        self.wait(4.1)
        
        # Beat 3: More letters appear
        letters_and_features = VGroup()
        for i in range(3):
            letter = Rectangle(width=0.35, height=0.55, fill_color=config.ACCENT, fill_opacity=0.3, stroke_width=1)
            letter.shift(LEFT * (2.5 - i * 0.6) + DOWN * (0.2 + i * 0.4))
            letters_and_features.add(letter)
        
        self.play(FadeIn(letters_and_features), run_time=1)
        scene1.add(letters_and_features)
        self.wait(4.6)
        
        # Beat 4: Pattern highlights
        highlight1 = SurroundingRectangle(letter1, buff=0.15, color=config.ACCENT_2, stroke_width=2)
        self.play(FadeIn(highlight1), run_time=1)
        self.wait(4.1)
        self.play(FadeOut(highlight1), run_time=0.8)
        self.wait(3.6)
        
        # Beat 5: Sorter nods (implied by new gesture visual)
        nod_text = Text("Pattern recognized!", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        nod_text.next_to(sorter_full, UP, buff=0.5)
        self.play(FadeIn(nod_text), run_time=1)
        scene1.add(nod_text)
        self.wait(4.6)
        
        # Beat 6: NEW letter arrives
        new_letter = Rectangle(width=0.4, height=0.6, fill_color=config.ACCENT_4, fill_opacity=0.5, stroke_width=2, stroke_color=config.ACCENT_4)
        new_letter.shift(UP * 0.8 + LEFT * 3)
        new_label = Text("NEW!", font_size=24, font=config.FONT_NAME, color=config.ACCENT_4)
        new_label.next_to(new_letter, UP, buff=0.2)
        new_group = VGroup(new_letter, new_label)
        
        cur = swap(self, cur, scene1)
        self.play(FadeIn(new_group), run_time=1)
        scene1.add(new_group)
        self.wait(4.6)
        
        # Beat 7: Sorter sorts it
        arrow = Arrow(new_letter.get_bottom(), bins[0].get_top(), buff=0.2, color=config.ACCENT, stroke_width=2)
        self.play(FadeIn(arrow), run_time=1)
        self.wait(4.6)
        
        # Beat 8: Analogy to AI
        analogy_box = VGroup(
            Text("Learning from examples → Finding patterns → Predicting on new data", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        )
        
        ai_map = VGroup(
            Text("Training data → Model weights → AI response", font_size=26, font=config.FONT_NAME, color=config.ACCENT),
        )
        
        analogy_and_map = VGroup(analogy_box, ai_map).arrange(DOWN, buff=0.6)
        cur = swap(self, cur, analogy_and_map)
        self.wait(6.0)


class S4_Example(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("Training in Code")
        self.play(FadeIn(title))
        self.wait(2.8)
        
        cur = None
        
        # Beat 1: Code step 1 - load data
        code_line1 = code_block("data = load_conversations()", font_size=26)
        step1_label = Text("Step 1: Load data", font_size=24, font=config.FONT_NAME, color=config.ACCENT)
        step1_label.next_to(code_line1, RIGHT, buff=0.5)
        step1_group = VGroup(code_line1, step1_label)
        step1_group = fit(step1_group, height=3)
        cur = swap(self, cur, step1_group)
        self.wait(3.8)
        
        # Beat 2: Code step 2 - create model
        code_line2 = code_block("model = create_model()", font_size=26)
        step2_label = Text("Step 2: Empty model\nwith random weights", font_size=24, font=config.FONT_NAME, color=config.ACCENT)
        step2_label.next_to(code_line2, RIGHT, buff=0.5)
        step2_group = VGroup(code_line2, step2_label)
        step2_group = fit(step2_group, height=3)
        cur = swap(self, cur, step2_group)
        self.wait(3.8)
        
        # Beat 3: Code step 3 - the training loop
        code_line3 = code_block("for sentence in data:\n  prediction = model(sentence[:−1])\n  error = prediction − correct\n  adjust_weights(model, error)", font_size=24)
        step3_label = Text("Step 3: The Magic Loop", font_size=24, font=config.FONT_NAME, color=config.ACCENT)
        step3_label.next_to(code_line3, RIGHT, buff=0.5)
        step3_group = VGroup(code_line3, step3_label)
        step3_group = fit(step3_group, height=3.5)
        cur = swap(self, cur, step3_group)
        self.wait(4.3)
        
        # Beat 4: Example sentence
        example_text = Text("Input: 'The customer reported a problem with'", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, example_text)
        self.wait(3.8)
        
        # Beat 5: Wrong prediction
        wrong_pred = Text("Model predicts: 'cat'", font_size=26, font=config.FONT_NAME, color=config.ACCENT_2)
        cur = swap(self, cur, wrong_pred)
        self.wait(3.3)
        
        # Beat 6: Correct answer
        correct_ans = Text("Correct answer: 'payment'", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        comparison = VGroup(wrong_pred.copy(), correct_ans).arrange(DOWN, buff=0.5)
        cur = swap(self, cur, comparison)
        self.wait(3.8)
        
        # Beat 7: Adjustment arrow
        error_box = Text("Error detected!", font_size=26, font=config.FONT_NAME, color=config.ACCENT_3)
        adjustment = Text("Adjust weights automatically", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        adjust_group = VGroup(error_box, adjustment).arrange(DOWN, buff=0.5)
        cur = swap(self, cur, adjust_group)
        self.wait(3.8)
        
        # Beat 8: Loop repeats
        loop_text = Text("See next sentence...\nAdjust again...\nAnd again...", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, loop_text)
        self.wait(4.8)
        
        # Beat 9: Confidence graph
        conf_label = Text("Model confidence:", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        conf_bar_bg = Rectangle(width=3, height=0.4, fill_color=config.ACCENT_2, fill_opacity=0.2, stroke_width=1, stroke_color=config.ACCENT_2)
        conf_bar = Rectangle(width=0.3, height=0.4, fill_color=config.ACCENT, fill_opacity=0.8, stroke_width=0)
        conf_bar.align_to(conf_bar_bg, LEFT)
        
        conf_group = VGroup(conf_label, conf_bar_bg, conf_bar).arrange(DOWN, buff=0.3)
        cur = swap(self, cur, conf_group)
        
        # Animate bar filling
        self.play(conf_bar.animate.set_width(2.7), run_time=3)
        self.wait(3.3)
        
        # Beat 10: After training - frozen weights
        trained_text = Text("Training complete.\nWeights are now frozen.", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, trained_text)
        self.wait(3.8)
        
        # Beat 11: Using the model
        usage_input = Text("User: 'The customer reported a problem with'", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        usage_output = Text("Model predicts: 'payment' ✓", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        usage_group = VGroup(usage_input, usage_output).arrange(DOWN, buff=0.5)
        cur = swap(self, cur, usage_group)
        self.wait(4.8)
        
        # Beat 12: Word-by-word continuation
        continuation = Text("Word by word, the answer grows.", font_size=26, font=config.FONT_NAME, color=config.ACCENT_2)
        cur = swap(self, cur, continuation)
        self.wait(4.3)


class S5_Recap(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("The Key Insight")
        self.play(FadeIn(title))
        self.wait(1)
        
        cur = None
        
        # Beat 1: Not magic, not a rulebook
        insight1 = Text("AI isn't magic.\nAI doesn't follow a hidden rulebook.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, insight1)
        self.wait(2.5)
        
        # Beat 2: It learns patterns
        insight2 = Text("It learned patterns by looking\nat thousands of examples.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, insight2)
        self.wait(2.5)
        
        # Beat 3: Like the mail sorter
        insight3 = VGroup(
            Text("Just like our mail sorter", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("learned from letters.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.3)
        cur = swap(self, cur, insight3)
        self.wait(2.5)
        
        # Beat 4: It builds answers piece by piece
        insight4 = Text("It builds answers\nby predicting one piece at a time.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, insight4)
        self.wait(2.5)
        
        # Beat 5: The weights are patterns
        insight5 = Text("The weights are the learned patterns.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, insight5)
        self.wait(2)
        
        # Beat 6: Training is just showing examples
        insight6 = Text("Training is just showing examples\nand letting math adjust those patterns.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, insight6)
        self.wait(3)
        
        # Beat 7: Summary journey
        journey = VGroup(
            Text("Data", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("→", font_size=26, font=config.FONT_NAME, color=config.ACCENT),
            Text("Patterns Learned", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("→", font_size=26, font=config.FONT_NAME, color=config.ACCENT),
            Text("Prediction on New Input", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(RIGHT, buff=0.3)
        journey = fit(journey, width=7)
        cur = swap(self, cur, journey)
        self.wait(4)
        
        # Beat 8: That's the whole thing
        final = Text("That's the whole thing.", font_size=32, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, final)
        self.wait(3)


class S6_CTA(Scene):
    def construct(self):
        apply_theme(self)
        
        # Title
        title = scene_title("Go Deeper")
        self.play(FadeIn(title))
        self.wait(1)
        
        cur = None
        
        # Beat 1: Next steps
        cta1 = Text("Build your own model", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, cta1)
        self.wait(2)
        
        # Beat 2: Math
        cta2 = Text("See the math behind the weights", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, cta2)
        self.wait(2)
        
        # Beat 3: Limitations
        cta3 = Text("Understand why AI sometimes gets things wrong", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, cta3)
        self.wait(2.5)
        
        # Beat 4: Call to action
        cta_final = VGroup(
            Text("Full tutorials coming", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("Subscribe so you don't miss them", font_size=28, font=config.FONT_NAME, color=config.ACCENT),
        ).arrange(DOWN, buff=0.5)
        cur = swap(self, cur, cta_final)
        self.wait(3)
        
        # End card
        self.play(FadeOut(cur), FadeOut(title), run_time=1)
        end = end_card()
        self.play(FadeIn(end), end.animate.scale(1.05), run_time=1.5)
        self.wait(3)


class T1_Hook(Scene):
    def construct(self):
        apply_theme(self)
        
        # Smartphone
        phone_bg = RoundedRectangle(corner_radius=0.3, width=2.5, height=4.5, stroke_width=2, stroke_color=config.ACCENT)
        phone_screen = RoundedRectangle(corner_radius=0.25, width=2.3, height=4.3, fill_color=config.BG_COLOR, fill_opacity=1, stroke_width=0)
        phone = VGroup(phone_bg, phone_screen)
        
        # Chat
        user_text = Text("How do chatbots work?", font_size=24, font=config.FONT_NAME, color=config.TEXT_COLOR)
        user_bubble = RoundedRectangle(corner_radius=0.15, width=2, height=0.7, fill_color=config.ACCENT, fill_opacity=0.3, stroke_width=0)
        user_bubble.surround(user_text, stretch=True, dim_to_match=0)
        user_msg = VGroup(user_bubble, user_text)
        user_msg.move_to(phone_screen.get_center()).shift(UP*0.8)
        
        # Response words
        response = "They're not looking things up..."
        resp_text = Text(response, font_size=24, font=config.FONT_NAME, color=config.ACCENT)
        ai_bubble = RoundedRectangle(corner_radius=0.15, width=2.1, height=0.8, fill_color=config.ACCENT_2, fill_opacity=0.2, stroke_width=0)
        ai_bubble.surround(resp_text, stretch=True, dim_to_match=0)
        ai_msg = VGroup(ai_bubble, resp_text)
        ai_msg.move_to(phone_screen.get_center()).shift(DOWN*0.5)
        
        phone_full = VGroup(phone, user_msg, ai_msg)
        phone_full = fit(phone_full, height=4.5)
        
        self.play(FadeIn(phone_full), run_time=1.5)
        self.wait(2)
        
        # Confused face
        confused = Text("❓", font_size=60, font=config.FONT_NAME, color=config.ACCENT)
        confused.next_to(phone_full, RIGHT, buff=0.8)
        
        self.play(FadeIn(confused), run_time=1)
        self.wait(2)
        
        # Fade and question mark
        self.play(FadeOut(phone_full), FadeOut(confused), run_time=1)
        big_q = Text("?", font_size=120, font=config.FONT_NAME, color=config.ACCENT)
        self.play(FadeIn(big_q), run_time=1.5)
        self.wait(2)


class T2_Tease(Scene):
    def construct(self):
        apply_theme(self)
        
        cur = None
        
        # Beat 1: The insight
        insight = Text("It learned by watching thousands of examples.", font_size=28, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, insight)
        self.wait(2.6)
        
        # Beat 2: Not rules
        not_rules = Text("Not by reading rules.", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, not_rules)
        self.wait(2.1)
        
        # Beat 3: Mail sorter analogy
        mail_setup = VGroup(
            Text("Imagine training a mail sorter", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("by showing them letters.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.3)
        cur = swap(self, cur, mail_setup)
        self.wait(3.1)
        
        # Beat 4: Patterns, not rules
        patterns = Text("They notice patterns.\nNever memorize rules.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, patterns)
        self.wait(3.1)
        
        # Beat 5: AI does the same
        ai_same = VGroup(
            Text("That's exactly what AI does.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("It learns patterns from data.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.3)
        cur = swap(self, cur, ai_same)
        self.wait(3.1)
        
        # Beat 6: Word by word
        prediction = Text("Then predicts one piece at a time.", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, prediction)
        self.wait(2.6)
        
        # Beat 7: No magic
        no_magic = VGroup(
            Text("No magic. Just math.", font_size=28, font=config.FONT_NAME, color=config.ACCENT),
            Text("That noticed patterns you didn't write down.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.4)
        cur = swap(self, cur, no_magic)
        self.wait(3.6)
        
        # Beat 8: Code teaser
        code_teaser = Text("In our full video, we walk through actual code.", font_size=26, font=config.FONT_NAME, color=config.ACCENT)
        cur = swap(self, cur, code_teaser)
        self.wait(3.1)
        
        # Beat 9: Show how
        show_how = Text("And show you exactly how that works.", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR)
        cur = swap(self, cur, show_how)
        self.wait(3.6)


class T3_CTA(Scene):
    def construct(self):
        apply_theme(self)
        
        # Call to action text
        cta_text = VGroup(
            Text("The full breakdown is on our YouTube", font_size=28, font=config.FONT_NAME, color=config.TEXT_COLOR),
            Text("Link in the description", font_size=26, font=config.FONT_NAME, color=config.ACCENT),
            Text("Come see inside", font_size=26, font=config.FONT_NAME, color=config.TEXT_COLOR),
        ).arrange(DOWN, buff=0.5)
        
        cta_text = fit(cta_text, height=3)
        self.play(FadeIn(cta_text), run_time=1.5)
        self.wait(2)
        
        # End card
        self.play(FadeOut(cta_text), run_time=1)
        end = end_card(title="Full video on YouTube")
        self.play(FadeIn(end), end.animate.scale(1.05), run_time=1.5)
        self.wait(3)