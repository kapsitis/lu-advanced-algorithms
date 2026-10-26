# Īsākie ceļi no sākuma virsotnes uz visām virsotnēm kā lineāra programma.
# Grafu nolasa no tā paša JSON faila, ko izmanto shortest-paths-example.py:
#   python shortest-paths-lp.py [grafs.json]
import json
import sys
from pathlib import Path

from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD, lpSum

HERE = Path(__file__).parent
graph_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "shortest-paths-example.json"
graph = json.loads(graph_file.read_text(encoding="utf-8"))
s = graph["source"]

# Neorientētu šķautni aizstāj ar divām pretēji vērstām šķautnēm
arcs = []
for u, v, w in graph["edges"]:
    arcs.append((u, v, w))
    if not graph.get("directed"):
        arcs.append((v, u, w))

model = LpProblem(sense=LpMaximize)
x = {v: LpVariable(name=f"x_{v}") for v in graph["nodes"]}

model += x[s] == 0                       # sākuma virsotnes potenciāls
for u, v, w in arcs:
    model += x[v] - x[u] <= w            # trijstūra nevienādība katrai šķautnei
model += lpSum(x.values())               # maksimizē visu potenciālu summu

model.solve(PULP_CBC_CMD(msg=False))
for v in graph["nodes"]:
    print(f"d({s}, {v}) = {x[v].value():g}")
print(f"Mērķfunkcija: {model.objective.value():g}")

# Īsāko ceļu koks: šķautnes, kurās nevienādība pārvēršas par vienādību
for v in graph["nodes"]:
    if v != s:
        parents = [u for u, w_v, w in arcs
                   if w_v == v and abs(x[v].value() - x[u].value() - w) < 1e-9]
        print(f"{v}: iepriekšējā virsotne {', '.join(parents)}")
