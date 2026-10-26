# Maksimālā plūsma no S uz T grafā graph-capacities.png kā lineāra programma.
from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD

capacities = {
    ("S", "A"): 11, ("S", "C"): 14,
    ("A", "B"): 15,
    ("C", "A"): 3, ("C", "B"): 3, ("C", "D"): 7,
    ("B", "T"): 12, ("B", "D"): 2,
    ("D", "T"): 15,
}
nodes = {u for edge in capacities for u in edge}

model = LpProblem(sense=LpMaximize)
f = {(u, v): LpVariable(name=f"f_{u}{v}", lowBound=0, upBound=c)   # 0 <= f_uv <= c_uv
     for (u, v), c in capacities.items()}

for v in nodes - {"S", "T"}:                                        # plūsmas saglabāšanās
    model += (sum(f[e] for e in f if e[1] == v)
              == sum(f[e] for e in f if e[0] == v)), f"saglabasanas_{v}"
model += sum(f[e] for e in f if e[0] == "S")                        # izplūde no S

model.solve(PULP_CBC_CMD(msg=False))
for (u, v), var in f.items():
    print(f"f_{u}{v} = {var.value():g}  (ietilpība {capacities[u, v]})")
print(f"Maksimālā plūsma: {model.objective.value():g}")
