import math
import random
import matplotlib.pyplot as plt

BRANCHING = 2
DEPTH = 8
LENGTH_SCALE = 0.72
RANDOMNESS = 8
SPREAD = 60

def depth_color(level, max_depth):
    ratio = level / max_depth if max_depth > 0 else 0
    return (0.35 + 0.20 * ratio, 0.18 + 0.55 * ratio, 0.08 + 0.12 * ratio)

def child_angles(parent_angle, branching, spread):
    if branching == 1:
        return [parent_angle]
    start = -spread / 2
    step = spread / (branching - 1)
    return [parent_angle + start + i * step for i in range(branching)]

def draw_branch(x1, y1, length, angle_deg, level, max_depth):
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    color = depth_color(level, max_depth)
    width = max(0.8, 3.5 * (1 - level / (max_depth + 1)))
    plt.plot([x1, x2], [y1, y2], linewidth=width, color=color)

    if level < max_depth:
        for child_angle in child_angles(angle_deg, BRANCHING, SPREAD):
            offset = random.uniform(-RANDOMNESS, RANDOMNESS)
            scale = random.uniform(0.92, 1.08)
            draw_branch(x2, y2, length * LENGTH_SCALE * scale, child_angle + offset, level + 1, max_depth)

plt.figure(figsize=(10, 7))
plt.title("Recursive Tree (2D)")
plt.xlim(-220, 220)
plt.ylim(0, 400)
plt.gca().set_aspect("equal")
plt.grid(True, alpha=0.25)

draw_branch(0, 20, 120, 90, 0, DEPTH)

plt.show()
