w = input()
n = len(w)
for i in range(14, 1 + n):
    if len(set(w[i - 14:i])) == 14:
        print(i)
        break