import math
import matplotlib.pyplot as plt

def draw_line(x1, y1, length, angle_deg):
    angle_rad = math.radians(angle_deg)
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 + length * math.sin(angle_rad)
    plt.plot([x1, x2], [y1, y2], linewidth=2)
    return x2, y2

plt.figure(figsize=(8, 6))
plt.title("Recursive Tree (2D)")
plt.xlim(-150, 150)
plt.ylim(0, 250)
plt.gca().set_aspect("equal")
plt.grid(True, alpha=0.3)

draw_line(0, 20, 100, 90)

plt.show()
