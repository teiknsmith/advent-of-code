import sys
import re
import functools
JMP='jmp'
ACC='acc'
NOP='nop'

lines = sys.stdin.readlines()
def stoc(s):
    c, n = s.split()
    return (c, int(n))
cmds = [stoc(l) for l in lines]
""" part 1
acc = 0
ip = 0
visited = set()
while ip not in visited:
    visited.add(ip)
    jmp = 1
    cmd = cmds[ip]
    if cmd[0] == JMP:
        jmp = cmd[1]
    elif cmd[0] == ACC:
        acc += cmd[1]
    ip += jmp
print(acc)
"""

for i in range(len(cmds)):
    if cmds[i][0] == ACC:
        continue
    acc = 0
    ip = 0
    visited = set()
    success = False
    while True:
        visited.add(ip)
        jmp = 1
        cmd = cmds[ip]
        ex = cmd[0]
        if ip == i:
            if cmd[0] == JMP:
                ex = NOP
            elif cmd[0] == NOP:
                ex = JMP
        if ex == JMP:
            jmp = cmd[1]
        elif ex == ACC:
            acc += cmd[1]
        ip += jmp

        if ip in visited:
            break
        if ip == len(cmds):
            success = True
            break
    if success:
        print(acc)

