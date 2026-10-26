# Kāpostu-burkānu uzdevuma pieļaujamais apgabals un optimālās peļņas taisne.
# Rezultāts: cabbage-carrots-feasible.png (tajā pašā direktorijā)
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

OUT = Path(__file__).with_suffix(".png")

# Pieļaujamā apgabala virsotnes: x_k <= 3, x_b <= 4, x_k + x_b <= 5, x_k, x_b >= 0
vertices = [(0, 0), (3, 0), (3, 2), (1, 4), (0, 4)]

fig, ax = plt.subplots(figsize=(6.4, 5.6))
ax.add_patch(Polygon(vertices, closed=True, facecolor="#cfe3f7",
                     edgecolor="#1f5fa0", linewidth=2))

# Ierobežojumu taisnes
t = np.linspace(-0.5, 6.5, 2)
ax.axvline(3, color="gray", linestyle=":", linewidth=1)
ax.axhline(4, color="gray", linestyle=":", linewidth=1)
ax.plot(t, 5 - t, color="gray", linestyle=":", linewidth=1)
ax.text(3.05, 5.6, r"$x_k = 3$", color="dimgray")
ax.text(4.9, 4.08, r"$x_b = 4$", color="dimgray")
ax.text(4.25, 0.35, r"$x_k + x_b = 5$", color="dimgray", rotation=-45)

# Peļņas līmeņa līnijas 1200 x_k + 1700 x_b = z
for z in (2000, 4000, 6000):
    ax.plot(t, (z - 1200 * t) / 1700, color="#c0392b", linestyle="--",
            linewidth=0.9, alpha=0.6)
    ax.text(0.03, z / 1700 + 0.05, f"{z}", color="#c0392b", fontsize=8, alpha=0.8)
ax.plot(t, (8000 - 1200 * t) / 1700, color="#c0392b", linewidth=2.2)
ax.text(3.45, 2.52, r"$1200x_k + 1700x_b = 8000$", color="#c0392b", rotation=-35.2,
        rotation_mode="anchor")

# Gradienta virziens c = (1200, 1700), mērogots
ax.annotate("", xy=(1.0 + 0.6, 0.6 + 0.85), xytext=(1.0, 0.6),
            arrowprops=dict(arrowstyle="-|>", color="#c0392b", linewidth=1.5))
ax.text(1.62, 1.45, r"$\mathbf{c}$", color="#c0392b", fontsize=12)

# Virsotnes un optimums
for (x, y) in vertices:
    ax.plot(x, y, "o", color="#1f5fa0", markersize=4)
ax.plot(1, 4, "o", color="#c0392b", markersize=9, zorder=5)
ax.annotate(r"$(1,4)$, peļņa $8000$", xy=(1, 4), xytext=(0.05, 5.3),
            arrowprops=dict(arrowstyle="-", color="black", linewidth=0.8))
ax.text(1.1, 1.9, "pieļaujamais\napgabals", color="#1f5fa0", ha="center")

ax.set_xlim(-0.3, 6.3)
ax.set_ylim(-0.3, 6.0)
ax.set_aspect("equal")
ax.set_xlabel(r"$x_k$ (kāposti, ha)")
ax.set_ylabel(r"$x_b$ (burkāni, ha)")
ax.grid(True, linewidth=0.3)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
