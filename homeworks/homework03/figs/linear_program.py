from pulp import *

model = LpProblem(sense=LpMaximize)
x_1 = LpVariable(name="x_1", lowBound=0)
x_2 = LpVariable(name="x_2", lowBound=0)
x_3 = LpVariable(name="x_3", lowBound=0)


model += 7*x_1 + 4*x_2 + 5*x_3 <= 25 
model += 5*x_1 + 3*x_2 + 6*x_3 <= 19 
model += 5*x_1 + 3*x_2 + 5*x_3 

status = model.solve(PULP_CBC_CMD(msg=False))
print(f'(x_1, x_2, x_3) = ({x_1.value()}, {x_2.value()}, {x_3.value()})')
print(f'Max = {model.objective.value()}')

