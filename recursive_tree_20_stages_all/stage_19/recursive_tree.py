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
        self.speed = 2
        self.mode = "DFS"

        self.base_length = 120.0
        self.base_angle = 90.0
        self.line_width_base = 4.2

        # Stan animacji
        self.segments = []
        self.current_index = 0
        self.running = False

        # Kolory
        self.bg_color = "#0f172a"          # granatowe tło
        self.panel_color = "#111827"       # panel
        self.text_color = "#e5e7eb"        # jasny tekst
        self.grid_color = "#334155"        # siatka
        self.leaf_color = "#7dd3fc"        # liście
        self.trunk_dark = "#7c4a2d"        # początek pnia
        self.branch_light = "#d6b48a"      # końcowe gałęzie

        # Figura
        self.fig, self.ax = plt.subplots(figsize=(11, 8))
        self.fig.patch.set_facecolor(self.bg_color)
        plt.subplots_adjust(left=0.07, right=0.96, top=0.92, bottom=0.36)

        self.setup_axes()

        # Tekst informacyjny
        self.info_text = self.ax.text(
            0.02, 0.98, "",
            transform=self.ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color=self.text_color,
            bbox=dict(
                boxstyle="round,pad=0.45",
                facecolor="#111827",
                edgecolor="#475569",
                alpha=0.95
            ),
        )

        # Widgety
        self._create_widgets()

        # Timer
        self.timer = self.fig.canvas.new_timer(interval=60)
        self.timer.add_callback(self._animate_step)

        # Pierwsze generowanie
        self.generate_tree()
        self.draw_current()

    def setup_axes(self):
        self.ax.set_facecolor(self.bg_color)
        self.ax.set_title(
            "Drzewo rekurencyjne (2D) — wizualizacja BFS / DFS",
            fontsize=16,
            color=self.text_color,
            pad=14,
            fontweight="bold",
        )
        self.ax.set_xlim(-240, 240)
        self.ax.set_ylim(0, 430)
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.22, color=self.grid_color, linestyle="--")

        for spine in self.ax.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1.0)

        self.ax.tick_params(colors="#94a3b8", labelsize=9)

    def style_widget_axis(self, axis_obj):
        axis_obj.set_facecolor(self.panel_color)
        for spine in axis_obj.spines.values():
            spine.set_edgecolor("#475569")
            spine.set_linewidth(1.0)

    def _create_widgets(self):
        # Osie sliderów
        ax_branch = plt.axes([0.10, 0.26, 0.32, 0.03])
        ax_depth = plt.axes([0.10, 0.21, 0.32, 0.03])
        ax_random = plt.axes([0.10, 0.16, 0.32, 0.03])
        ax_scale = plt.axes([0.10, 0.11, 0.32, 0.03])
        ax_speed = plt.axes([0.10, 0.06, 0.32, 0.03])

        for ax_ in [ax_branch, ax_depth, ax_random, ax_scale, ax_speed]:
            self.style_widget_axis(ax_)

        self.slider_branch = Slider(ax_branch, "Gałęzie", 2, 5, valinit=self.branching, valstep=1)
        self.slider_depth = Slider(ax_depth, "Głębokość", 1, 11, valinit=self.depth, valstep=1)
        self.slider_random = Slider(ax_random, "Losowość", 0, 35, valinit=self.randomness, valstep=1)
        self.slider_scale = Slider(ax_scale, "Skala długości", 0.55, 0.85, valinit=self.length_scale, valstep=0.01)
        self.slider_speed = Slider(ax_speed, "Prędkość", 1, 20, valinit=self.speed, valstep=1)

        # Polskie kolory napisów sliderów
        for slider in [
            self.slider_branch,
            self.slider_depth,
            self.slider_random,
            self.slider_scale,
            self.slider_speed,
        ]:
            try:
                slider.label.set_color(self.text_color)
                slider.valtext.set_color(self.text_color)
                slider.poly.set_facecolor("#38bdf8")
                slider.track.set_color("#334155")
                if hasattr(slider, "vline"):
                    slider.vline.set_color("#e2e8f0")
            except Exception:
                pass

        # Osie przycisków
        ax_start = plt.axes([0.55, 0.23, 0.15, 0.06])
        ax_reset = plt.axes([0.75, 0.23, 0.15, 0.06])
        ax_generate = plt.axes([0.55, 0.13, 0.15, 0.06])
        ax_mode = plt.axes([0.75, 0.13, 0.15, 0.06])

        for ax_ in [ax_start, ax_reset, ax_generate, ax_mode]:
            self.style_widget_axis(ax_)

        self.btn_start = Button(ax_start, "Start / Stop", color="#1e293b", hovercolor="#334155")
        self.btn_reset = Button(ax_reset, "Reset", color="#1e293b", hovercolor="#334155")
        self.btn_generate = Button(ax_generate, "Generuj", color="#1e293b", hovercolor="#334155")
        self.btn_mode = Button(ax_mode, f"Tryb: {self.mode}", color="#1e293b", hovercolor="#334155")

        for btn in [self.btn_start, self.btn_reset, self.btn_generate, self.btn_mode]:
            btn.label.set_color(self.text_color)
            btn.label.set_fontsize(10)
            btn.label.set_fontweight("bold")

        # Akcje
        self.btn_start.on_clicked(self.toggle_animation)
        self.btn_reset.on_clicked(self.reset_animation)
        self.btn_generate.on_clicked(self.regenerate_from_ui)
        self.btn_mode.on_clicked(self.toggle_mode)

    def blend_hex(self, c1, c2, t):
        c1 = c1.lstrip("#")
        c2 = c2.lstrip("#")
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)

        return (r / 255, g / 255, b / 255)

    def get_depth_color(self, level, max_depth):
        ratio = level / max_depth if max_depth > 0 else 0
        return self.blend_hex(self.trunk_dark, self.branch_light, ratio)

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

        width = max(0.9, self.line_width_base * (1 - level / (max_depth + 1)))
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
            f"Tryb: {self.mode}\n"
            f"Liczba gałęzi: {self.branching}\n"
            f"Głębokość: {self.depth}\n"
            f"Losowość: {self.randomness:.0f}°\n"
            f"Skala długości: {self.length_scale:.2f}\n"
            f"Prędkość: {self.speed}\n"
            f"Narysowano: {self.current_index}/{len(self.segments)}"
        )

    def draw_background_label(self):
        self.ax.text(
            0.99,
            0.02,
            "Projekt: Drzewo Rekurencyjne 2D",
            transform=self.ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=9,
            color="#64748b",
            alpha=0.8,
        )

    def draw_current(self):
        self.ax.clear()
        self.setup_axes()

        for i in range(self.current_index):
            seg = self.segments[i]

            self.ax.plot(
                [seg["x1"], seg["x2"]],
                [seg["y1"], seg["y2"]],
                linewidth=seg["width"],
                color=seg["color"],
                solid_capstyle="round",
            )

            # Liście
            if seg["level"] == self.depth:
                self.ax.scatter(
                    seg["x2"],
                    seg["y2"],
                    s=16,
                    color=self.leaf_color,
                    alpha=0.95,
                    edgecolors="none",
                )

        # Tekst informacyjny po clear()
        self.info_text = self.ax.text(
            0.02,
            0.98,
            "",
            transform=self.ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color=self.text_color,
            bbox=dict(
                boxstyle="round,pad=0.45",
                facecolor="#111827",
                edgecolor="#475569",
                alpha=0.95
            ),
        )

        self.update_info_text()
        self.draw_background_label()
        self.fig.canvas.draw_idle()

    def _animate_step(self):
        if not self.running:
            return

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
        self.btn_mode.label.set_text(f"Tryb: {self.mode}")
        self.running = False
        self.timer.stop()
        self.generate_tree()
        self.draw_current()


if __name__ == "__main__":
    app = RecursiveTreeApp()
    plt.show()