from sys import stdin

cmds = stdin.read().strip().split('$ ')[1:]

files = dict()
curdirs = [files]


def mkdir(name):
    cur = curdirs[-1]
    if name not in cur:
        cur[name] = dict()


for cmd in cmds:
    # print('|' + cmd + '|')
    if cmd.startswith("cd"):
        arg = cmd.split()[1]
        if arg == '/':
            curdirs = [files]
        elif arg == '..':
            curdirs.pop()
        else:
            mkdir(arg)
            curdirs.append(curdirs[-1][arg])
    else:
        assert cmd.startswith("ls")
        for l in cmd.strip().split('\n')[1:]:
            a, b = l.split()
            if a == "dir":
                mkdir(b)
            else:
                curdirs[-1][b] = int(a)


def pf(d, r=0):
    tab = "   " * r
    for k, v in d.items():
        if isinstance(v, int):
            print(tab, k, v)
        else:
            print(tab, k, ':')
            pf(v, r + 1)


def mksz(d):
    if isinstance(d, int):
        return d
    t = 0
    for subd in d.values():
        t += mksz(subd)
    d['^SZ'] = t
    return t


def accumszs(d, l):
    if isinstance(d, int):
        return
    for subd in d.values():
        accumszs(subd, l)
    l.append(d['^SZ'])


mksz(files)
szs = []
accumszs(files, szs)
# print(sum(sz for sz in szs if sz <= 100000))
szs.sort()
targ = files['^SZ'] - 40000000
for sz in szs:
    if sz >= targ:
        print(sz)
        break