#!/usr/bin/env python3
import os
import shutil
import subprocess

from html.parser import HTMLParser

from utils import show_bits, get_with_cookie

# copy template solution file to local sol.py
shutil.copy("../../template.py", "sol.py")
subprocess.run(['code', '-r', 'sol.py'])


class TestGrabber(HTMLParser):
    """An HTMLParser to pull out text in <pre><code> blocks"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tests = []
        self.inpre = False
        self.intest = False
        self.thistest = ""
        self.alldata = ""
        self.proximity_post_match_word = 0

    def handle_starttag(self, tag, attrs):
        #if tag == 'pre':
        #    self.inpre = True
        #if self.inpre and tag == 'code':
        if tag == 'code':
            self.intest = True

    def handle_data(self, data: str):
        MATCH_WORD = "example"
        i = len(self.alldata) - len(MATCH_WORD)
        self.alldata += data.lower()
        if self.alldata.find(MATCH_WORD, i) > -1:
            self.proximity_post_match_word = 2
        if self.intest:
            self.thistest += data

    def handle_endtag(self, tag):
        if self.intest and tag == 'code':
            self.tests.append((self.proximity_post_match_word, self.thistest))
            if self.proximity_post_match_word > 0:
                self.proximity_post_match_word -= 1
            self.thistest = ""
            self.intest = False
        if tag == 'pre':
            self.inpre = False

    def get_tests(self):
        return [
            t for _, t in sorted(
                grabber.tests, key=lambda t: (t[0], len(t[1])), reverse=True)
        ]


# gather the day info from the working directory
# assumes a folder for each year, and folders for each day in that year
cwd = os.getcwd()
root, day = os.path.split(cwd)
root, year = os.path.split(root)

# get the input for the test
r = get_with_cookie(f"https://adventofcode.com/{year}/day/{day}/input")
challenge_input = r.text

# and write it to the file 'final.in'
with open('final.in', 'w') as inout:
    inout.write(challenge_input)

# get the tests from the readme
r = get_with_cookie(f"https://adventofcode.com/{year}/day/{day}")
grabber = TestGrabber()
grabber.feed(r.text)

# display the final test for easy comparison in the next section
print("the final test input looks kinda like this:")
print(show_bits(challenge_input))

# and write each test into a file 'test0.in', 'test1.in', ...
for i, test in enumerate(grabber.get_tests()):
    CUT_CHARS = 'yuiop[]\\hjkl;\'bnm,./67890-=^&*()_+YUIOP{}|HJKL:"BNM<>?'
    print(show_bits(test))
    print()
    print(
        f"Type any key in '{CUT_CHARS}' to keep this then stop considering tests.\n"
        "Type anything else to include this as a test and keep looking through more.\n"
        "To skip this test but consider others, just press enter.\n"
        "Input: ",
        end='')
    s = input()
    if s:
        with open(f"test{i}.in", 'w') as testout:
            testout.write(test)
        if s[0] in CUT_CHARS:
            break