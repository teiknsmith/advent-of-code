from sys import stdin
import heapq as q

tosee = []
g = list(map(list, stdin.read().strip().split('\n')))
n, m = len(g), len(g[0])
d = [[float('inf')] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        if g[i][j] == 'S':
            d[i][j] = 0
            tosee = [(0, i, j)]
            g[i][j] = ord('a')
        elif g[i][j] == 'E':
            g[i][j] = ord('z')
            ti, tj = i, j
        else:
            g[i][j] = ord(g[i][j])
# {*map(print, g)}
# print()
DII = [1, 0, -1, 0, 1]
while tosee:
    _, i, j = q.heappop(tosee)
    for ii in range(4):
        ni = i + DII[ii]
        nj = j + DII[ii + 1]
        if 0 <= ni < n and 0 <= nj < m and d[i][j] + 1 < d[ni][
                nj] and g[i][j] + 1 >= g[ni][nj]:
            d[ni][nj] = d[i][j] + 1
            q.heappush(tosee, (d[ni][nj], ni, nj))
# {*map(print, d)}

print(d[ti][tj])

tosee = [(0, ti, tj)]
d = [[float('inf')] * m for _ in range(n)]
d[ti][tj] = 0
while tosee:
    _, i, j = q.heappop(tosee)
    for ii in range(4):
        ni = i + DII[ii]
        nj = j + DII[ii + 1]
        if 0 <= ni < n and 0 <= nj < m and d[i][j] + 1 < d[ni][
                nj] and g[ni][nj] + 1 >= g[i][j]:
            d[ni][nj] = d[i][j] + 1
            q.heappush(tosee, (d[ni][nj], ni, nj))

ads = [d[i][j] for i in range(n) for j in range(m) if g[i][j] == ord('a')]
print(min(ads))