moves = set()
ms = (3, 4, 6, 8, 10)
for m1 in ms:
  for m2 in ms:
    for m3 in ms:
      moves.add(tuple(sorted((m1, m2, m3))))
for move in list(moves):
  for b in range(1, 8):
    t = list(move)
    for i in range(3):
      if (b//(2**i))%2:
        t[i] *= -1
    b = sorted(i for i in t if i<0)
    if b == sorted(set(b)):
      moves.add(tuple(sorted(t)))
moves = sorted(moves)

n = len(moves)
top = [[0]*n for i in range(n)]
for i in range(n):
  for j in range(n):
    for m in moves[i]:
      if m>0:
        if -m not in moves[j]:
          top[i][j] += m

top = [[top[i][j]-top[j][i] for j in range(n)] for i in range(n)]

best_from_top = []
for i, row in enumerate(top):
    over_0 = [x for x in row if x > 0]
    if len(over_0) > 100:
        best_from_top.append(i)

isPerfect = lambda x: all(any(top[i][j]<0 for j in x) for i in range(170))

a = isPerfect(best_from_top)
print(a)
"""
from itertools import combinations
for moveSet in combinations(range(170), 4):
    if isPerfect(moveSet):
        print(moveSet)
"""