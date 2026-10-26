import pulp

prob = pulp.LpProblem("bitu_sadale", pulp.LpMinimize)
x = pulp.LpVariable.dicts("biti", range(n), lowBound=0, cat="Integer")
prob += pulp.lpSum(d[i] * x[i] for i in range(n))           # mērķa funkcija
prob += pulp.lpSum(x[i] for i in range(n)) <= B, "bitraide"  # nosaukts ierobežojums
prob.solve(pulp.HiGHS(msg=False))
print(pulp.LpStatus[prob.status], pulp.value(prob.objective))