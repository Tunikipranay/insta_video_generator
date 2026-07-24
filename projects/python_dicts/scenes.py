"""Sample video: Python Dictionaries — house-style Manim scenes."""
from manim import *
from house_style import *
import config


# ----------------------------------------------------------------- S1: HOOK
class S1_Hook(Scene):
    """~8s. List scans slowly; dict snaps instantly."""

    def construct(self):
        apply_theme(self)

        title = Text("lists search.", font_size=40, color=GREY_B).to_edge(UP, buff=0.8)

        # ---- the list: 8 cells, scanned one by one -----------------------
        cells = VGroup(*[
            Square(0.75, stroke_color=GREY_D, stroke_width=2,
                   fill_color="#161b24", fill_opacity=1)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.12).shift(UP * 1.1)
        labels = VGroup(*[
            Text(w, font_size=20, color=GREY_B).move_to(c)
            for w, c in zip(["ana", "raj", "mia", "leo", "zoe", "kai", "eva", "sam"], cells)
        ])
        target_idx = 6
        scanner = glow_dot(cells[0].get_top() + UP * 0.3, color=config.ACCENT_3)

        self.play(FadeIn(title, shift=DOWN * 0.2),
                  LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.06),
                  FadeIn(labels), run_time=1.2)
        self.add(scanner)
        for i in range(target_idx + 1):
            self.play(scanner.animate.move_to(cells[i].get_top() + UP * 0.3),
                      cells[i].animate.set_stroke(config.ACCENT_3, width=3),
                      run_time=0.28, rate_func=rate_functions.ease_in_out_sine)
        found_slow = label_chip("found... eventually", color=config.ACCENT_3)
        found_slow.next_to(cells[target_idx], DOWN, buff=0.45)
        self.play(FadeIn(found_slow, scale=0.8), run_time=0.4)

        # ---- the dict: instant snap --------------------------------------
        title2 = Text("dicts know.", font_size=40, weight=BOLD,
                      color=config.ACCENT).to_edge(UP, buff=0.8)
        pair = kv_box('"eva"', "42").shift(DOWN * 1.6)
        snap = glow_dot(pair[0].get_left() + LEFT * 2.5, color=config.ACCENT_4)

        self.play(FadeIn(pair, shift=UP * 0.2), run_time=0.6)
        self.add(snap)
        self.play(snap.animate.move_to(pair[0].get_left() + LEFT * 0.4),
                  run_time=0.25, rate_func=rate_functions.rush_into)
        found_fast = label_chip("instant", color=config.ACCENT_4)
        found_fast.next_to(pair, RIGHT, buff=0.5)
        self.play(Transform(title, title2),
                  FadeIn(found_fast, scale=1.4),
                  Flash(pair[0].get_left(), color=config.ACCENT_4, flash_radius=0.7),
                  run_time=0.7)
        self.wait(2.5)


# -------------------------------------------------------------- S2: CONCEPT
class S2_Concept(ThreeDScene):
    """~26s. 3D hash machine: key -> number -> bucket."""

    def construct(self):
        apply_theme(self)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-55 * DEGREES, zoom=0.85)

        title = Text("how a dict works", font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(title)
        title.set_opacity(0)

        # ---- buckets: a row of slots on the ground -----------------------
        buckets = VGroup(*[
            Prism(dimensions=[1.0, 1.0, 0.25]).set_fill("#161b24", opacity=1)
            .set_stroke(GREY_D, width=1.5)
            for _ in range(7)
        ]).arrange(RIGHT, buff=0.25).shift(DOWN * 2 + IN * 0.5)
        idx_labels = VGroup()
        for i, b in enumerate(buckets):
            lb = Text(str(i), font_size=22, color=GREY_C)
            lb.rotate(90 * DEGREES, axis=RIGHT)
            lb.move_to(b.get_center() + OUT * 0.35)
            idx_labels.add(lb)

        # ---- the hash machine: rotating cube -----------------------------
        machine = Cube(side_length=1.5, fill_opacity=0.12,
                       fill_color=config.ACCENT, stroke_color=config.ACCENT,
                       stroke_width=2).shift(UP * 1.2)
        machine_label = Text("hash()", font_size=30, color=config.ACCENT)
        self.add_fixed_in_frame_mobjects(machine_label)
        machine_label.move_to(RIGHT * 3.4 + UP * 1.9)

        self.play(title.animate.set_opacity(1),
                  LaggedStart(*[FadeIn(b, shift=OUT * 0.3) for b in buckets],
                              lag_ratio=0.08),
                  FadeIn(idx_labels), run_time=2)
        self.play(DrawBorderThenFill(machine), FadeIn(machine_label), run_time=1.5)
        self.wait(1.5)
        self.begin_ambient_camera_rotation(rate=0.05)
        machine_spin = Rotate(machine, angle=TAU, axis=UP + 0.3 * RIGHT,
                              run_time=26, rate_func=linear)
        self.add(machine)

        def feed(key_str, val_str, bucket_i, num_str):
            key = Text(key_str, font_size=30, color=config.ACCENT_2)
            self.add_fixed_in_frame_mobjects(key)
            key.move_to(LEFT * 5.5 + UP * 2.6)
            self.play(FadeIn(key, shift=RIGHT * 0.4), run_time=0.6)
            # fly into the machine (approx center of frame where cube sits)
            self.play(key.animate.move_to(UP * 1.2).scale(0.3).set_opacity(0),
                      Flash(machine.get_center(), color=config.ACCENT,
                            flash_radius=1.2, num_lines=10),
                      run_time=0.9, rate_func=rate_functions.ease_in_out_sine)
            self.remove(key)
            num = Text(num_str, font_size=34, weight=BOLD, color=config.ACCENT_4)
            self.add_fixed_in_frame_mobjects(num)
            num.move_to(UP * 0.2)
            self.play(FadeIn(num, scale=1.6), run_time=0.5)
            # travel to the bucket
            spark = glow_dot(machine.get_center(), color=config.ACCENT_4)
            self.add(spark)
            self.play(spark.animate.move_to(buckets[bucket_i].get_center() + OUT * 0.4),
                      num.animate.set_opacity(0),
                      run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
            self.remove(num)
            pair = kv_box(key_str, val_str, width=2.6).scale(0.7)
            pair.rotate(90 * DEGREES, axis=RIGHT)
            pair.move_to(buckets[bucket_i].get_center() + OUT * 0.55)
            self.play(FadeOut(spark), FadeIn(pair, shift=OUT * 0.2),
                      buckets[bucket_i].animate.set_stroke(config.ACCENT_4, width=3),
                      run_time=0.7)

        feed('"alice"', "97", 2, "hash → 2")
        self.wait(1.5)
        feed('"bob"', "63", 5, "hash → 5")
        self.wait(1.0)

        caption = Text("the key's hash IS the address — no searching",
                       font_size=28, color=GREY_A)
        self.add_fixed_in_frame_mobjects(caption)
        caption.to_edge(DOWN, buff=0.7).set_opacity(0)
        self.play(caption.animate.set_opacity(1), run_time=1)
        self.wait(3)
        same = Text("10 items or 10,000,000 — same speed",
                    font_size=30, weight=BOLD, color=config.ACCENT_2)
        self.add_fixed_in_frame_mobjects(same)
        same.to_edge(DOWN, buff=0.7).set_opacity(0)
        self.play(caption.animate.set_opacity(0), same.animate.set_opacity(1),
                  run_time=1)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()


# ------------------------------------------------------------- S3: USE CASE
class S3_UseCase(Scene):
    """~30s. Counting votes in one pass with dict.get()."""

    def construct(self):
        apply_theme(self)

        chip = label_chip("USE CASE", color=config.ACCENT_2).to_corner(UL, buff=0.45)
        headline = Text("count a million votes in one pass",
                        font_size=34, weight=BOLD).to_edge(UP, buff=0.6)
        headline.shift(RIGHT * 1.1)
        self.play(FadeIn(chip, scale=0.8), Write(headline), run_time=1.5)

        code = code_block(
            'votes = {}\n'
            'for name in ballots:\n'
            '    votes[name] = votes.get(name, 0) + 1\n'
            '\n'
            'winner = max(votes, key=votes.get)',
            font_size=24,
        ).scale(0.95).shift(LEFT * 3.1 + DOWN * 0.4)
        self.play(FadeIn(code, shift=UP * 0.3), run_time=1.2)
        self.wait(3.0)

        # live tally on the right
        names = ["alice", "bob", "carol"]
        counts = {n: 0 for n in names}
        boxes = {}
        tally = VGroup()
        for i, n in enumerate(names):
            b = kv_box(f'"{n}"', "0", width=3.0)
            boxes[n] = b
            tally.add(b)
        tally.arrange(DOWN, buff=0.35).shift(RIGHT * 3.6 + DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in tally],
                              lag_ratio=0.15), run_time=1.2)

        ballots = ["alice", "bob", "alice", "carol", "alice", "bob", "alice"]
        for ballot in ballots:
            counts[ballot] += 1
            tag = Text(f'"{ballot}"', font_size=26, color=config.ACCENT)
            tag.move_to(UP * 2.2 + RIGHT * 0.2)
            new_box = kv_box(f'"{ballot}"', str(counts[ballot]), width=3.0)
            new_box.move_to(boxes[ballot])
            self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.45)
            self.play(tag.animate.move_to(boxes[ballot]).scale(0.4).set_opacity(0),
                      run_time=0.6, rate_func=rate_functions.ease_in_out_sine)
            self.remove(tag)
            old = boxes[ballot]
            boxes[ballot] = new_box
            tally.remove(old); tally.add(new_box)
            self.play(ReplacementTransform(old, new_box),
                      Flash(new_box[0].get_right() + LEFT * 0.5,
                            color=config.ACCENT_2, flash_radius=0.4, num_lines=6),
                      run_time=0.35)

        # winner
        crown = Text("winner", font_size=24, weight=BOLD, color=config.ACCENT_4)
        crown.next_to(boxes["alice"], UP, buff=0.2)
        win_ring = SurroundingRectangle(boxes["alice"], color=config.ACCENT_4,
                                        corner_radius=0.15, buff=0.12)
        self.play(Create(win_ring), FadeIn(crown, shift=DOWN * 0.15), run_time=0.9)
        self.wait(1.5)

        punch = Text("every ballot = one instant lookup",
                     font_size=30, color=config.ACCENT_2)
        punch.to_edge(DOWN, buff=0.6)
        self.play(Write(punch), run_time=1.2)
        self.wait(6.0)


# -------------------------------------------------------------- S4: PAYOFF
class S4_Payoff(Scene):
    """~11s. O(n) vs O(1) race + takeaway."""

    def construct(self):
        apply_theme(self)

        lane_y = 1.0
        start_x, end_x = -5.2, 5.2
        list_chip = label_chip("list  O(n)", color=config.ACCENT_3)
        dict_chip = label_chip("dict  O(1)", color=config.ACCENT_4)
        list_chip.move_to(LEFT * 5.2 + UP * (lane_y + 0.8))
        dict_chip.move_to(LEFT * 5.2 + DOWN * (2 - lane_y + 0.3) + UP * 0.0)
        dict_chip.move_to([start_x, -1.0 + 0.8, 0])
        list_chip.move_to([start_x, lane_y + 0.8, 0])

        lane1 = Line([start_x, lane_y, 0], [end_x, lane_y, 0],
                     color=GREY_D, stroke_width=2)
        lane2 = Line([start_x, -1.0, 0], [end_x, -1.0, 0],
                     color=GREY_D, stroke_width=2)
        finish = DashedLine([end_x, lane_y + 0.5, 0], [end_x, -1.5, 0],
                            color=GREY_C)
        runner_list = glow_dot([start_x, lane_y, 0], color=config.ACCENT_3)
        runner_dict = glow_dot([start_x, -1.0, 0], color=config.ACCENT_4)

        self.play(FadeIn(lane1), FadeIn(lane2), FadeIn(finish),
                  FadeIn(list_chip, scale=0.8), FadeIn(dict_chip, scale=0.8),
                  run_time=1.0)
        self.add(runner_list, runner_dict)
        self.play(
            runner_dict.animate(run_time=0.35,
                                rate_func=rate_functions.rush_into
                                ).move_to([end_x, -1.0, 0]),
        )
        self.play(Flash([end_x, -1.0, 0], color=config.ACCENT_4,
                        flash_radius=0.6), run_time=0.3)
        self.play(runner_list.animate(run_time=3.2, rate_func=linear
                                      ).move_to([end_x, lane_y, 0]))

        takeaway = VGroup(
            Text("need to look things up?", font_size=34, color=GREY_A),
            Text("reach for a dict.", font_size=46, weight=BOLD,
                 color=config.ACCENT),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 2.9)
        self.play(Write(takeaway[0]), run_time=0.8)
        self.play(FadeIn(takeaway[1], scale=1.15), run_time=0.7)
        self.wait(4.5)


# ----------------------------------------------------------------- S5: CTA
class S5_CTA(Scene):
    """~5s. Standard end card."""

    def construct(self):
        apply_theme(self)
        card = end_card()
        self.play(FadeIn(card, scale=1.08),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.wait(3.5)
