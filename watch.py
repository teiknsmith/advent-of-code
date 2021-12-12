#!/usr/bin/env python3
import glob
import os
import time
from subprocess import run, PIPE, STDOUT, TimeoutExpired
import sys
import threading
from collections import deque
from utils import *

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

WRONG_ANSWER_STR = "That's not the right answer"
def submit_to_server(answer, part):
    year, day = yearday()
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    form =f"level={part}&answer={answer}"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    jar = get_cookie_jar()
    r = requests.post(url, cookies=jar, data=form, headers=headers)
    return WRONG_ANSWER_STR not in r.text

active_part = 1
def submit(answer):
    global active_part
    if submit_to_server(answer, active_part):
        active_part += 1
        return True
    return False

def add_input(myin):
    while True:
        myin.append(sys.stdin.read(1))


altstdin = deque()
input_thread = threading.Thread(target=add_input, args=(altstdin,))
input_thread.daemon = True
input_thread.start()
inputline = []

og_time = 0
while True:
    mtime = os.path.getmtime('sol.py')
    if mtime > og_time:
        to_print = str_all(tests, challenge_input)
        to_print = f"timestamp: {mtime}\n\n" + to_print
        os.system('clear')
        print(to_print)
        og_time = mtime
    if altstdin:
        inputline += list(altstdin)
        altstdin.clear()
        if inputline[-1] == '\n':
            answer = ''.join(inputline)
            inputline.clear()
            if submit(answer):
                if active_part > 2:
                    print("Well done! You solved it!")
                    break
                else:
                    print(f"Success! Now onto part {active_part}")
            else:
                print("Yikes, now we gotta wait. dang it")
    time.sleep(0.2)
