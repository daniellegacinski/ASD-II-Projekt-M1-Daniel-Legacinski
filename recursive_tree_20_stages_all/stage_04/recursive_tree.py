import math
import random
import matplotlib.pyplot as plt

BRANCHING = 2
DEPTH = 7
LENGTH_SCALE = 0.72
RANDOMNESS = 8
SPREAD = 60

def child_angles(parent_angle, branching, spread):
    if branching == 1:
        return [parent_angle]
    start = -spread / 2
    step = spread / (branching - 1)
    return [parent_angle + start + i * step for i in range(branching)]

def draw_branch(x1, y1, length, angle_deg, depth):
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    plt.plot([x1, x2], [y1, y2], linewidth=2)

    if depth > 0:
        for child_angle in child_angles(angle_deg, BRANCHING, SPREAD):
            offset = random.uniform(-RANDOMNESS, RANDOMNESS)
            scale = random.uniform(0.92, 1.08)
            draw_branch(x2, y2, length * LENGTH_SCALE * scale, child_angle + offset, depth - 1)

plt.figure(figsize=(8, 6))
plt.title("Recursive Tree (2D)")
plt.xlim(-220, 220)
plt.ylim(0, 340)
plt.gca().set_aspect("equal")
plt.grid(True, alpha=0.3)

draw_branch(0, 20, 110, 90, DEPTH)

plt.show()
