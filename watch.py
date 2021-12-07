#!/usr/bin/env python3
import glob
import os
import time
from subprocess import run, PIPE, STDOUT, TimeoutExpired
from utils import show_bits

WIDTH = 30
def solve(test_input, timeout=30):
    """Run sol.py on the input and return the output (or an appropriate message)"""
    try:
        res = run(['python3', 'sol.py'],
                  input=test_input,
                  stdout=PIPE,
                  stderr=STDOUT,
                  universal_newlines=True,
                  timeout=timeout)
    except TimeoutExpired as e:
        return f'TIMED OUT!! SO FAR:\n{e.output}'
    else:
        return res.stdout


def str_all(tests, real):
    """Run sol.py on all inputs and return the results as a str"""
    testsout = []
    for test in tests:
        testsout.append(solve(test))
    realout = solve(real)

    res_lines = []
    for testin, testout in zip(tests, testsout):
        res_lines.append(f'{show_bits(testin)}')
        res_lines.append('-' * WIDTH)
        res_lines.append(f'{show_bits(testout)}')
        res_lines.append('=' * WIDTH)
        res_lines.append('=' * WIDTH)

    res_lines.append('=' * WIDTH)
    res_lines.append(f'THE REAL DEAL:\n{show_bits(real)}')
    res_lines.append('-' * WIDTH)
    res_lines.append(f'{show_bits(realout)}')
    return '\n'.join(res_lines)


tests = []
for filename in glob.glob('*.in'):
    with open(filename, 'r') as fin:
        if filename == 'final.in':
            challenge_input = fin.read()
        else:
            tests.append(fin.read())

og_time = 0
while True:
    mtime = os.path.getmtime('sol.py')
    if mtime > og_time:
        to_print = str_all(tests, challenge_input)
        to_print = f"timestamp: {mtime}\n\n" + to_print
        os.system('clear')
        print(to_print)
        og_time = mtime
    time.sleep(0.2)
