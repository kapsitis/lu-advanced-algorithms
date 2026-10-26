import numpy as np

# Coefficient matrix A
A = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1]
])

# Right-hand side vector b
b = np.array([1, 2, 13])

# Solve the system of equations
solution = np.linalg.solve(A, b)

# Print the solution
print(f"[x1,x2,x3] = ({solution[0]}, {solution[1]}, {solution[2]})")
