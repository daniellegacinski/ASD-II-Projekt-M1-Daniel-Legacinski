import math
import random
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider


class RecursiveTreeApp:
    def __init__(self):
        # Parametry początkowe
        self.branching = 2
        self.depth = 8
        self.randomness = 8.0
        self.length_scale = 0.72
        self.speed = 1
        self.mode = "DFS"
        self.base_length = 120.0
        self.base_angle = 90.0
        self.line_width_base = 3.5

        # Stan animacji
        self.segments = []
        self.current_index = 0
        self.running = False

        # Ustawienie figury
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.08, right=0.95, top=0.93, bottom=0.34)

        self.ax.set_title("Recursive Tree (2D) - BFS / DFS", fontsize=16, pad=12)
        self.ax.set_xlim(-220, 220)
        self.ax.set_ylim(0, 420)
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.25)

        # Tekst informacyjny
        self.info_text = self.ax.text(
            0.02, 0.98, "",
            transform=self.ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        # Widgety
        self._create_widgets()

        # Timer do animacji
        self.timer = self.fig.canvas.new_timer(interval=60)
        self.timer.add_callback(self._animate_step)

        # Pierwsze generowanie
        self.generate_tree()
        self.draw_current()

    def _create_widgets(self):
        # Slidery
        ax_branch = plt.axes([0.12, 0.24, 0.30, 0.03])
        ax_depth = plt.axes([0.12, 0.19, 0.30, 0.03])
        ax_random = plt.axes([0.12, 0.14, 0.30, 0.03])
        ax_scale = plt.axes([0.12, 0.09, 0.30, 0.03])
        ax_speed = plt.axes([0.12, 0.04, 0.30, 0.03])

        self.slider_branch = Slider(ax_branch, "Branching", 2, 5, valinit=self.branching, valstep=1)
        self.slider_depth = Slider(ax_depth, "Depth", 1, 11, valinit=self.depth, valstep=1)
        self.slider_random = Slider(ax_random, "Randomness", 0, 35, valinit=self.randomness, valstep=1)
        self.slider_scale = Slider(ax_scale, "Length scale", 0.55, 0.85, valinit=self.length_scale, valstep=0.01)
        self.slider_speed = Slider(ax_speed, "Speed", 1, 20, valinit=self.speed, valstep=1)

        # Przyciski
        ax_start = plt.axes([0.55, 0.20, 0.14, 0.05])
        ax_reset = plt.axes([0.73, 0.20, 0.14, 0.05])
        ax_generate = plt.axes([0.55, 0.11, 0.14, 0.05])
        ax_mode = plt.axes([0.73, 0.11, 0.14, 0.05])

        self.btn_start = Button(ax_start, "Start / Stop")
        self.btn_reset = Button(ax_reset, "Reset")
        self.btn_generate = Button(ax_generate, "Generate")
        self.btn_mode = Button(ax_mode, f"Mode: {self.mode}")

        # Akcje
        self.btn_start.on_clicked(self.toggle_animation)
        self.btn_reset.on_clicked(self.reset_animation)
        self.btn_generate.on_clicked(self.regenerate_from_ui)
        self.btn_mode.on_clicked(self.toggle_mode)

    def get_depth_color(self, level, max_depth):
        ratio = level / max_depth if max_depth > 0 else 0
        r = 0.35 + 0.20 * ratio
        g = 0.18 + 0.55 * ratio
        b = 0.08 + 0.12 * ratio
        return (r, g, b)

    def node_children_angles(self, parent_angle, branching, spread=60):
        if branching == 1:
            return [parent_angle]

        start = -spread / 2
        step = spread / (branching - 1)
        return [parent_angle + start + i * step for i in range(branching)]

    def create_segment(self, x1, y1, length, angle_deg, level, max_depth):
        angle_rad = math.radians(angle_deg)
        x2 = x1 + length * math.cos(angle_rad)
        y2 = y1 + length * math.sin(angle_rad)

        width = max(0.8, self.line_width_base * (1 - level / (max_depth + 1)))
        color = self.get_depth_color(level, max_depth)

        return {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "level": level,
            "width": width,
            "color": color,
        }

    def generate_tree(self):
        self.branching = int(self.slider_branch.val)
        self.depth = int(self.slider_depth.val)
        self.randomness = float(self.slider_random.val)
        self.length_scale = float(self.slider_scale.val)
        self.speed = int(self.slider_speed.val)

        self.segments = []
        self.current_index = 0

        root_x = 0
        root_y = 20
        trunk_length = self.base_length
        trunk_angle = self.base_angle

        # (x, y, length, angle, level)
        root_state = (root_x, root_y, trunk_length, trunk_angle, 0)

        if self.mode == "DFS":
            structure = [root_state]
            pop_method = structure.pop
            push_method = structure.append
        else:
            structure = deque([root_state])
            pop_method = structure.popleft
            push_method = structure.append

        while structure:
            x, y, length, angle, level = pop_method()

            seg = self.create_segment(x, y, length, angle, level, self.depth)
            self.segments.append(seg)

            if level >= self.depth:
                continue

            child_length = length * self.length_scale
            child_base_angles = self.node_children_angles(angle, self.branching, spread=70)

            children = []
            for child_angle in child_base_angles:
                rand_offset = random.uniform(-self.randomness, self.randomness)
                rand_scale = random.uniform(0.92, 1.08)

                new_angle = child_angle + rand_offset
                new_length = child_length * rand_scale

                child_state = (
                    seg["x2"],
                    seg["y2"],
                    new_length,
                    new_angle,
                    level + 1,
                )
                children.append(child_state)

            if self.mode == "DFS":
                children.reverse()

            for child in children:
                push_method(child)

        self.update_info_text()

    def update_info_text(self):
        self.info_text.set_text(
            f"Mode: {self.mode}\n"
            f"Branching: {self.branching}\n"
            f"Depth: {self.depth}\n"
            f"Randomness: {self.randomness:.0f}°\n"
            f"Length scale: {self.length_scale:.2f}\n"
            f"Speed: {self.speed}\n"
            f"Drawn: {self.current_index}/{len(self.segments)}"
        )

    def draw_current(self):
        self.ax.clear()
        self.ax.set_title("Recursive Tree (2D) - BFS / DFS", fontsize=16, pad=12)
        self.ax.set_xlim(-220, 220)
        self.ax.set_ylim(0, 420)
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.25)

        for i in range(self.current_index):
            seg = self.segments[i]
            self.ax.plot(
                [seg["x1"], seg["x2"]],
                [seg["y1"], seg["y2"]],
                linewidth=seg["width"],
                color=seg["color"],
            )

            if seg["level"] == self.depth:
                self.ax.plot(seg["x2"], seg["y2"], marker="o", markersize=3, color="green")

        self.info_text = self.ax.text(
            0.02, 0.98, "",
            transform=self.ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )
        self.update_info_text()

        self.fig.canvas.draw_idle()

    def _animate_step(self):
        if not self.running:
            return

        # aktualizacja speed na żywo
        self.speed = int(self.slider_speed.val)

        if self.current_index < len(self.segments):
            self.current_index += self.speed
            if self.current_index > len(self.segments):
                self.current_index = len(self.segments)
            self.draw_current()
        else:
            self.running = False
            self.timer.stop()

    def toggle_animation(self, event):
        self.running = not self.running
        if self.running:
            self.timer.start()
        else:
            self.timer.stop()

    def reset_animation(self, event):
        self.running = False
        self.timer.stop()
        self.current_index = 0
        self.draw_current()

    def regenerate_from_ui(self, event):
        self.running = False
        self.timer.stop()
        self.generate_tree()
        self.draw_current()

    def toggle_mode(self, event):
        self.mode = "BFS" if self.mode == "DFS" else "DFS"
        self.btn_mode.label.set_text(f"Mode: {self.mode}")
        self.running = False
        self.timer.stop()
        self.generate_tree()
        self.draw_current()


if __name__ == "__main__":
    app = RecursiveTreeApp()
    plt.show()