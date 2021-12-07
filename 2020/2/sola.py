import sys
import re
class Password:
    PATT = re.compile(r"""(\d+)-(\d+) (.): (.*)""")
    
    def __init__(self, line):
        match = Password.PATT.match(line)
        cmin, cmax, self.c, self.pswd = match.groups()
        self.cmin = int(cmin)
        self.cmax = int(cmax)

    def valid(self):
        n = self.pswd.count(self.c)
        return n >= self.cmin and n <= self.cmax
        

l = sys.stdin.read().split('\n')
l = [Password(el) for el in l if el]
f = [el for el in l if el.valid()]
print(len(f))
