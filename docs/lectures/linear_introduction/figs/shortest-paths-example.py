# Uzzīmē svērtu grafu īsāko ceļu uzdevumam un saglabā to SVG formātā.
# Grafu (virsotnes ar koordinātēm, šķautnes ar svariem, sākuma un mērķa
# virsotni) nolasa no JSON faila:
#   python shortest-paths-example.py [grafs.json] [rezultats.svg]
# Pēc noklusējuma: shortest-paths-example.json -> shortest-paths-example.svg
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = Path(__file__).parent
graph_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "shortest-paths-example.json"
out_file = Path(sys.argv[2]) if len(sys.argv) > 2 else graph_file.with_suffix(".svg")

graph = json.loads(graph_file.read_text(encoding="utf-8"))
pos = graph["nodes"]
source, target = graph.get("source"), graph.get("target")
R = 16  # virsotnes rādiuss (koordinātu vienībās)

plt.rcParams["svg.fonttype"] = "none"  # SVG failā teksts paliek kā teksts
fig, ax = plt.subplots(figsize=(6, 4.2))

for u, v, w in graph["edges"]:
    (x1, y1), (x2, y2) = pos[u], pos[v]
    if graph.get("directed"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#333333", linewidth=1.2,
                                    shrinkA=R + 1, shrinkB=R + 1))
    else:
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=1.2, zorder=1)
    # Svaru novieto mazliet blakus šķautnes viduspunktam (perpendikulāri tai)
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / length, dx / length
    ax.text((x1 + x2) / 2 + 11 * nx, (y1 + y2) / 2 + 11 * ny, str(w),
            ha="center", va="center", fontsize=12, style="italic")

for name, (x, y) in pos.items():
    face = "#fff8b0" if name == source else "#c9c9f5" if name == target else "white"
    ax.add_patch(Circle((x, y), R, facecolor=face, edgecolor="#333333",
                        linewidth=1.4, zorder=2))
    ax.text(x, y, name, ha="center", va="center", fontsize=14, zorder=3)
if source is not None:
    x, y = pos[source]
    ax.text(x - R - 4, y + R, "0", color="#1f77d0", fontsize=11, ha="right",
            fontweight="bold")

xs = [p[0] for p in pos.values()]
ys = [p[1] for p in pos.values()]
ax.set_xlim(min(xs) - 2 * R, max(xs) + 2 * R)
ax.set_ylim(min(ys) - 2 * R, max(ys) + 2 * R)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(out_file, metadata={"Date": None})
print(f"Saglabāts: {out_file}")
