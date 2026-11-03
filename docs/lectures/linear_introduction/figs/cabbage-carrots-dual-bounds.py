# Kāpostu-burkānu uzdevums: duālā uzdevuma pieļaujamie punkti (y1, y2, y3)
# dod augšējos novērtējumus peļņai. Katram y apvienotā nevienādība
#   y1*x_k + y2*x_b + y3*(x_k + x_b) <= 3*y1 + 4*y2 + 5*y3
# ir pusplakne, kas satur visu pieļaujamo apgabalu (x_k, x_b) plaknē.
# Rezultāts: cabbage-carrots-dual-bounds.png (tajā pašā direktorijā)
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

OUT = Path(__file__).with_suffix(".png")

vertices = [(0, 0), (3, 0), (3, 2), (1, 4), (0, 4)]
duals = [
    ((1200, 1700, 0), "#7f8c8d", "--"),
    ((200, 700, 1000), "#e67e22", "-."),
    ((0, 500, 1200), "#c0392b", "-"),
]

fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.add_patch(Polygon(vertices, closed=True, facecolor="#cfe3f7",
                     edgecolor="#1f5fa0", linewidth=2))
for (x, y) in vertices:
    ax.plot(x, y, "o", color="#1f5fa0", markersize=4)

t = np.linspace(-0.5, 7.0, 2)
for (y1, y2, y3), color, style in duals:
    a_k, a_b = y1 + y3, y2 + y3          # apvienotās nevienādības koeficienti
    bound = 3 * y1 + 4 * y2 + 5 * y3     # duālā mērķfunkcija
    ax.plot(t, (bound - a_k * t) / a_b, color=color, linestyle=style, linewidth=2,
            label=rf"$\mathbf{{y}} = ({y1}, {y2}, {y3})$: peļņa $\leq {bound}$")

# Punkts (3,4) izpilda abus sēklu ierobežojumus, bet ne zemes ierobežojumu
ax.plot(3, 4, "s", color="#7f8c8d", markersize=6)
ax.annotate(r"$(3,4)$", xy=(3, 4), xytext=(3.2, 4.35))
ax.plot(1, 4, "o", color="#c0392b", markersize=9, zorder=5)
ax.annotate(r"$(1,4)$", xy=(1, 4), xytext=(0.35, 4.35))
ax.text(1.1, 1.9, "pieļaujamais\napgabals", color="#1f5fa0", ha="center")

ax.set_xlim(-0.3, 7.0)
ax.set_ylim(-0.3, 7.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x_k$ (kāposti, ha)")
ax.set_ylabel(r"$x_b$ (burkāni, ha)")
ax.grid(True, linewidth=0.3)
ax.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
