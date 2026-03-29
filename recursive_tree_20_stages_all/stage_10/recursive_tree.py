import math
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

class RecursiveTreeApp:
    def __init__(self):
        self.branching = 2
        self.depth = 8
        self.randomness = 8.0
        self.length_scale = 0.72
        self.base_length = 120.0
        self.base_angle = 90.0

        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(left=0.08, right=0.95, top=0.93, bottom=0.34)

        ax_branch = plt.axes([0.12, 0.24, 0.30, 0.03])
        ax_depth = plt.axes([0.12, 0.19, 0.30, 0.03])

        self.slider_branch = Slider(ax_branch, "Branching", 2, 5, valinit=self.branching, valstep=1)
        self.slider_depth = Slider(ax_depth, "Depth", 1, 11, valinit=self.depth, valstep=1)

        ax_generate = plt.axes([0.55, 0.11, 0.14, 0.05])
        self.btn_generate = Button(ax_generate, "Generate")
        self.btn_generate.on_clicked(self.regenerate)

        self.draw_tree()

    def get_depth_color(self, level, max_depth):
        ratio = level / max_depth if max_depth > 0 else 0
        return (0.35 + 0.20 * ratio, 0.18 + 0.55 * ratio, 0.08 + 0.12 * ratio)

    def child_angles(self, parent_angle, branching, spread=60):
        if branching == 1:
            return [parent_angle]
        start = -spread / 2
        step = spread / (branching - 1)
        return [parent_angle + start + i * step for i in range(branching)]

    def draw_branch(self, x1, y1, length, angle_deg, level, max_depth):
        angle_rad = math.radians(angle_deg)
        x2 = x1 + length * math.cos(angle_rad)
        y2 = y1 + length * math.sin(angle_rad)
        width = max(0.8, 3.5 * (1 - level / (max_depth + 1)))
        color = self.get_depth_color(level, max_depth)
        self.ax.plot([x1, x2], [y1, y2], linewidth=width, color=color)

        if level == max_depth:
            self.ax.plot(x2, y2, marker="o", markersize=3, color="green")

        if level < max_depth:
            for child_angle in self.child_angles(angle_deg, self.branching, spread=70):
                offset = random.uniform(-self.randomness, self.randomness)
                scale = random.uniform(0.92, 1.08)
                self.draw_branch(x2, y2, length * self.length_scale * scale, child_angle + offset, level + 1, max_depth)

    def draw_tree(self):
        self.branching = int(self.slider_branch.val)
        self.depth = int(self.slider_depth.val)
        self.ax.clear()
        self.ax.set_title("Recursive Tree (2D)")
        self.ax.set_xlim(-220, 220)
        self.ax.set_ylim(0, 420)
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.25)
        self.draw_branch(0, 20, self.base_length, self.base_angle, 0, self.depth)
        self.fig.canvas.draw_idle()

    def regenerate(self, event):
        self.draw_tree()

if __name__ == "__main__":
    app = RecursiveTreeApp()
    plt.show()
