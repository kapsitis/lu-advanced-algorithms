from pulp import *

# problem formulation; KA002
# Uz galda atrodas pulksteņi ar ciparnīcu; katrs no tiem rāda kaut kādu laiku 
# no 00:00 līdz 11:59. Vienā gājienā atļauts paņemt jebkurus divus no pulksteņiem 
# un pagriezt tos uz priekšu par vienādu skaitu minūšu (šo minūšu skaitu
# sauksim par pagrieziena laiku). Ar šiem gājieniem jāpanāk, lai visi pulksteņi 
# rādītu vienādu laiku. Kāda ir mazākā pagrieziena laiku summa, 
# ar kuru to noteikti var izdarīt.



model = LpProblem(sense=LpMinimize)

# x_12 = LpVariable(name="x12", lowBound=0)
# x_13 = LpVariable(name="x13", lowBound=0)
# x_14 = LpVariable(name="x14", lowBound=0)
# x_15 = LpVariable(name="x15", lowBound=0)
# x_23 = LpVariable(name="x23", lowBound=0)
# x_24 = LpVariable(name="x24", lowBound=0)
# x_25 = LpVariable(name="x25", lowBound=0)
# x_34 = LpVariable(name="x34", lowBound=0)
# x_35 = LpVariable(name="x35", lowBound=0)
# x_45 = LpVariable(name="x45", lowBound=0)

x_12 = LpVariable(name="x12", lowBound=0, cat=LpInteger)
x_13 = LpVariable(name="x13", lowBound=0, cat=LpInteger)
x_14 = LpVariable(name="x14", lowBound=0, cat=LpInteger)
x_15 = LpVariable(name="x15", lowBound=0, cat=LpInteger)
x_23 = LpVariable(name="x23", lowBound=0, cat=LpInteger)
x_24 = LpVariable(name="x24", lowBound=0, cat=LpInteger)
x_25 = LpVariable(name="x25", lowBound=0, cat=LpInteger)
x_34 = LpVariable(name="x34", lowBound=0, cat=LpInteger)
x_35 = LpVariable(name="x35", lowBound=0, cat=LpInteger)
x_45 = LpVariable(name="x45", lowBound=0, cat=LpInteger)


variables = [x_12, x_13, x_14, x_15, x_23, x_24, x_25, x_34, x_35, x_45]
weights = [1]*10



# values = [1, 144, 288, 432, 576]
values = [1,719, 719, 719, 719]
max_value = max(values)

model += x_12 + x_13 + x_14 + x_15 >= (max_value - values[0])
model += x_12 + x_23 + x_24 + x_25 >= (max_value - values[1])
model += x_13 + x_23 + x_34 + x_35 >= (max_value - values[2])
model += x_14 + x_24 + x_34 + x_45 >= (max_value - values[3])
model += x_15 + x_25 + x_35 + x_45 >= (max_value - values[4])


# model += x_12 + x_13 + x_14 + x_15 + x_23 + x_24 + x_25 + x_34 + x_35 + x_45
model += lpDot(weights, variables)

# solve (without being verbose)
status = model.solve(PULP_CBC_CMD(msg=False))

subset_variables = [
    [x_12, x_13, x_14, x_15], 
    [x_12, x_23, x_24, x_25], 
    [x_13, x_23, x_34, x_35], 
    [x_14, x_24, x_34, x_45],
    [x_15, x_25, x_35, x_45]
]

sums = []
for i in range(0,5): 
    total_value = values[i] + sum(var.value() for var in subset_variables[i])
    sums.append(total_value)

print(f'Values: {values}')
print(f'(x12, x13, x14, x15) = ({x_12.value()}, {x_13.value()}, {x_14.value()}, {x_15.value()})')
print(f'     (x23, x24, x25) =       ({x_23.value()}, {x_24.value()}, {x_25.value()})')
print(f'          (x34, x35) =            ({x_34.value()}, {x_35.value()})')
print(f'               (x45) =                 ({x_45.value()})')
print(f"Clocks: {sums}")
print("Turned amount:", model.objective.value())
