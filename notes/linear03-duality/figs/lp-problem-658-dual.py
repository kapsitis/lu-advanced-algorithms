from pulp import *

model = LpProblem(sense=LpMinimize)
y1 = LpVariable(name="y1", lowBound=0)
y2 = LpVariable(name="y2", lowBound=0)

model += 6*y1 + 10*y2 >= 5
model += 5*y1 + 20*y2 >= 7
model += 8*y1 + 10*y2 >= 6
model += 16*y1 + 35*y2

status = model.solve(PULP_CBC_CMD(msg=False))
print(f'(y1, y2)= ({y1.value()}, {y2.value()})')
print(f'Augšējais novērtējums: {model.objective.value()}')
