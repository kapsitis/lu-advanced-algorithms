from scipy.optimize import linprog

# Objective function coefficients
c = [16, 35]

# Inequality constraints matrix (left-hand side)
A = [[-6, -10],  # The signs are inverted due to 'linprog' assumes <= form
     [-5, -20],
     [-8, -10]]

# Inequality constraints vector (right-hand side)
b = [-5, -7, -6]  # The signs are inverted due to the same reason

# Bounds for variables y_1 and y_2, respectively
bounds_y1 = (0, None)  # y_1 >= 0
bounds_y2 = (0, None)  # y_2 >= 0

# Set up and solve the linear program
result = linprog(c, A_ub=A, b_ub=b, bounds=[bounds_y1, bounds_y2], method='highs')

# Check if the optimization was successful
if result.success:
    print("Optimal value:", result.fun)
    print("Optimal values for y1 and y2:", result.x)
else:
    print("Optimization failed:", result.message)