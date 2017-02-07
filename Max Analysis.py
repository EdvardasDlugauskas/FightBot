moves = set()
ms = (3, 4, 6, 8, 10)
for m1 in ms:
    for m2 in ms:
        for m3 in ms:
            moves.add(tuple(sorted((m1, m2, m3))))

s = list(moves)
for move in s:
    for b in range(1, 8):
        t = list(move)
        for i in range(3):
            if (b // (2 ** i)) % 2:
                t[i] *= -1
        b = sorted(i for i in t if i < 0)
        if b == sorted(set(b)):
            moves.add(tuple(sorted(t)))
moves = sorted(moves)
del s

n = len(moves)
dmg = [[0] * n for i in range(n)]
for i in range(n):
    for j in range(n):
        score = 0
        for m in moves[i]:
            if m > 0:
                if -m not in moves[j]:
                    score += m
        dmg[i][j] = score

dif = [[dmg[i][j] - dmg[j][i] for j in range(n)] for i in range(n)]

tot = [sum(t) for t in dif]

top = [sorted((a[i], i) for i in range(len(a))) for a in dif]

moveToIndex = lambda m1, m2, m3: moves.index(tuple(sorted((m1, m2, m3))))

bestMoves = lambda m1, m2, m3: top[moveToIndex(m1, m2, m3)]

for num in (163, 162, 158, 39, 168):
    print(str(num) + ": " + str(moves[num]))