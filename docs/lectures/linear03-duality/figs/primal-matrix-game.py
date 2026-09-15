from pulp import *

model = LpProblem(sense=LpMinimize)

x1 = LpVariable(name="x1", lowBound=0)
x2 = LpVariable(name="x2", lowBound=0)
z = LpVariable(name="z")

model += z - 1*x1 - 4*x2 >= 0
model += z - 8*x1 - 2*x2 >= 0
model += x1 + x2 == 1 
model += z  # Mērķa funkcija

status = model.solve(PULP_CBC_CMD(msg=False))
print(f"(x1,x2) = {x1.value(), x2.value()}")
print(f"Value of the game = {model.objective.value()}")
