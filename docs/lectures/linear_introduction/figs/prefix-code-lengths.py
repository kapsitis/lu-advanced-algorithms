# Optimālie prefiksu koda garumi kā veselo skaitļu lineāra programma.
# Mainīgais y[i][l] = 1 nozīmē, ka i-tā simbola kodavārda garums ir l.
# Tad gan vidējais garums, gan Krafta nevienādība ir lineāras izteiksmes no y.
import heapq
from math import ceil, log2

from pulp import LpBinary, LpMinimize, LpProblem, LpVariable, PULP_CBC_CMD, lpSum

p = [0.4, 0.3, 0.2, 0.1]
n = len(p)
L = range(1, n)                          # optimālā kodā garums nepārsniedz n - 1

model = LpProblem(sense=LpMinimize)
y = [[LpVariable(name=f"y_{i}_{l}", cat=LpBinary) for l in L] for i in range(n)]
for i in range(n):
    model += lpSum(y[i]) == 1            # katram simbolam tieši viens garums
model += lpSum(y[i][k] * 2 ** -l for i in range(n) for k, l in enumerate(L)) <= 1
model += lpSum(p[i] * l * y[i][k] for i in range(n) for k, l in enumerate(L))

model.solve(PULP_CBC_CMD(msg=False))
ilp_lengths = [sum(l * round(y[i][k].value()) for k, l in enumerate(L)) for i in range(n)]

# Salīdzinājumam: Hafmana algoritms (glabā tikai garumus)
heap = [(pi, [i]) for i, pi in enumerate(p)]
huffman_lengths = [0] * n
heapq.heapify(heap)
while len(heap) > 1:
    p1, s1 = heapq.heappop(heap)
    p2, s2 = heapq.heappop(heap)
    for i in s1 + s2:
        huffman_lengths[i] += 1
    heapq.heappush(heap, (p1 + p2, s1 + s2))

H = -sum(pi * log2(pi) for pi in p)
shannon_lengths = [ceil(-log2(pi)) for pi in p]
avg = lambda lengths: sum(pi * li for pi, li in zip(p, lengths))

print(f"Relaksācija (entropija):  l_i = {[round(-log2(pi), 3) for pi in p]}, H = {H:.4f}")
print(f"Veselo skaitļu LP:        l_i = {ilp_lengths}, vidēji {avg(ilp_lengths):.4f}")
print(f"Hafmana kods:             l_i = {huffman_lengths}, vidēji {avg(huffman_lengths):.4f}")
print(f"Šenona kods ceil(-log p): l_i = {shannon_lengths}, vidēji {avg(shannon_lengths):.4f}")
