# Primāli duālā centrālā ceļa metode uzdevumam
#   max(-x1/3 + x2), x1 + x2 <= 4, 2x1 - x2 <= 3, x1, x2 >= 0
# (tas pats piemērs, kas afīnās mērogošanas metodei). Standartformā ar
# papildmainīgajiem x3, x4 tas ir min c^T x, kur Ax = b, x >= 0.
# Programma izdrukā iterāciju tabulu un saglabā primal-dual-path.png
# (centrālais ceļš un iterācijas plaknē (x1, x2)).
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

OUT = Path(__file__).with_suffix(".png")

A = np.array([[1.0, 1.0, 1.0, 0.0],
              [2.0, -1.0, 0.0, 1.0]])
b = np.array([4.0, 3.0])
c = np.array([1 / 3, -1.0, 0.0, 0.0])        # min c^T x  <=>  max(-x1/3 + x2)
n = len(c)


def newton_step(x, y, s, target_mu, eta):
    """Viens Ņūtona solis sistēmai Ax = b, A^T y + s = c, x_j s_j = target_mu."""
    r_p = b - A @ x
    r_d = c - A.T @ y - s
    r_c = target_mu - x * s
    M = A @ np.diag(x / s) @ A.T                # normālvienādojumu matrica A D A^T
    dy = np.linalg.solve(M, r_p - A @ ((r_c - x * r_d) / s))
    ds = r_d - A.T @ dy
    dx = (r_c - x * ds) / s
    # Soļa garums: paliek iekšpusē (x > 0, s > 0), ejot ne vairāk kā eta daļu līdz robežai
    alpha_p = min([1.0] + [eta * -x[j] / dx[j] for j in range(n) if dx[j] < 0])
    alpha_d = min([1.0] + [eta * -s[j] / ds[j] for j in range(n) if ds[j] < 0])
    return x + alpha_p * dx, y + alpha_d * dy, s + alpha_d * ds, alpha_p, alpha_d


# Sākumpunkts: primāli pieļaujams x un duāli pieļaujams (y, s) ar x, s > 0
x0 = np.array([1.0, 1.0, 2.0, 2.0])
y0 = np.array([-2.0, -0.5])
s0 = c - A.T @ y0

# Iterācijas ar sigma = 0.1, eta = 0.9
sigma, eta = 0.1, 0.9
x, y, s = x0, y0, s0
iterates = [x]
print(" k      x1       x2        mu       gap   alpha_P  alpha_D")
print(f" 0 {x[0]:8.5f} {x[1]:8.5f} {x @ s / n:9.5f} {x @ s:9.5f}")
for k in range(1, 7):
    x, y, s, a_p, a_d = newton_step(x, y, s, sigma * (x @ s) / n, eta)
    iterates.append(x)
    print(f"{k:2d} {x[0]:8.5f} {x[1]:8.5f} {x @ s / n:9.5f} {x @ s:9.5f} {a_p:8.4f} {a_d:8.4f}")
print("y =", y, " s =", s)

# Centrālais ceļš: katram mu atrod punktu ar x_j s_j = mu (vairāki Ņūtona soļi)
path = []
x, y, s = x0, y0, s0
for mu in np.geomspace(50, 1e-4, 120):
    for _ in range(30):
        x, y, s, _, _ = newton_step(x, y, s, mu, 0.95)
    path.append(x[:2])
path = np.array(path)

fig, ax = plt.subplots(figsize=(5.0, 5.6))
ax.add_patch(Polygon([(0, 0), (1.5, 0), (7 / 3, 5 / 3), (0, 4)], closed=True,
                     facecolor="#cfe3f7", edgecolor="#1f5fa0", linewidth=2))
ax.plot(path[:, 0], path[:, 1], color="#2e8b57", linewidth=2,
        label=r"centrālais ceļš $x_j s_j = \mu$")
pts = np.array([p[:2] for p in iterates])
ax.plot(pts[:, 0], pts[:, 1], "o--", color="#c0392b", markersize=6, linewidth=1.2,
        label="iterācijas ($\\sigma = 0.1$)")
for k, (px, py) in enumerate(pts[:4]):
    ax.annotate(f"$\\mathbf{{x}}^{{({k})}}$", (px, py), xytext=(8, -4),
                textcoords="offset points", color="#c0392b")
ax.plot(0, 4, "*", color="black", markersize=13, label="optimums $(0, 4)$")
ax.plot(path[0, 0], path[0, 1], "s", color="#2e8b57", markersize=6)
ax.annotate("analītiskais centrs\n($\\mu \\to \\infty$)", path[0], xytext=(1.25, 1.9),
            arrowprops=dict(arrowstyle="-", color="#2e8b57", linewidth=0.8),
            color="#2e8b57", fontsize=9)

ax.set_xlim(-0.3, 2.8)
ax.set_ylim(-0.3, 4.5)
ax.set_aspect("equal")
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.grid(True, linewidth=0.3)
ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
