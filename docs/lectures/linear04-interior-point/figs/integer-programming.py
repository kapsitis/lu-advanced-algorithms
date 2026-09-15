from pulp import *

n = 4
weights = [8, 5, 3, 2]
prices = [15, 12, 4, 2]
carry_weight = 10

model = LpProblem(sense=LpMaximize)
variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]
model += lpDot(weights, variables) <= carry_weight
model += lpDot(prices, variables)

status = model.solve(PULP_CBC_CMD(msg=False))
print("price:", model.objective.value())
print("take:", [variables[i].value() for i in range(n)])