from pulp import *

model = LpProblem(sense=LpMinimize)
y1 = LpVariable(name="y1", lowBound=0)
y2 = LpVariable(name="y2", lowBound=0)
y3 = LpVariable(name="y3", lowBound=0)

model += y1 + y3 >= 1200
model += y2 + y3 >= 1700
model += 3*y1 + 4*y2 + 5*y3

status = model.solve(PULP_CBC_CMD(msg=False))
print(f'(y1, y2, y3)= ({y1.value()}, {y2.value()}, {y3.value()})')
print(f'Peļņas augšējais novērtējums: {model.objective.value()}')
