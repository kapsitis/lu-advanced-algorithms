from pulp import *

model = LpProblem(sense=LpMaximize)
x_k = LpVariable(name="kaposti", lowBound=0)
x_b = LpVariable(name="burkani", lowBound=0)

model += x_k <= 3        # kāpostu ierobežojums
model += x_b <= 4        # burkānu ierobežojums
model += x_k + x_b <= 5  # platības ierobežojums (5 ha)
model += 1200 * x_k + 1700 * x_b

status = model.solve(PULP_CBC_CMD(msg=False))
print(f'Kāposti: {x_k.value()}')
print(f'Burkāni: {x_b.value()}')
print(f'Peļņa: {model.objective.value()}')
