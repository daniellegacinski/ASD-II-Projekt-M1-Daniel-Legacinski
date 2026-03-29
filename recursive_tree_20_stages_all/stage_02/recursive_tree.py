import math
import matplotlib.pyplot as plt

def draw_branch(x1, y1, length, angle_deg, depth):
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    plt.plot([x1, x2], [y1, y2], linewidth=2)

    if depth > 0:
        draw_branch(x2, y2, length * 0.7, angle_deg - 25, depth - 1)
        draw_branch(x2, y2, length * 0.7, angle_deg + 25, depth - 1)

plt.figure(figsize=(8, 6))
plt.title("Recursive Tree (2D)")
plt.xlim(-180, 180)
plt.ylim(0, 300)
plt.gca().set_aspect("equal")
plt.grid(True, alpha=0.3)

draw_branch(0, 20, 100, 90, 6)

plt.show()
