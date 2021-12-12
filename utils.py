import requests
import os
import functools

def show_bits(text,
              max_lines=20,
              tail_lines_needed=4,
              max_chars=100,
              tail_chars_needed=30):
    """"Extract 600 characters from a line good for displaying"""
    lines = text.split('\n')
    if len(lines) > max_lines:
        lines = lines[:max_lines - tail_lines_needed -
                      1] + [" ... "] + lines[-tail_lines_needed:]

    disp_lines = []
    for line in lines:
        if len(line) > max_chars:
            line = line[:max_chars - tail_chars_needed -
                        5] + " ... " + line[-tail_chars_needed:]
        disp_lines.append(line)
    return '\n'.join(disp_lines)

@functools.lru_cache(1)
def get_cookie_jar():
    # grab the session cookie from the stored file
    with open('../../data/cookie', 'r') as cookie_in:
        session = cookie_in.read()
    jar = requests.cookies.RequestsCookieJar()
    jar.set('session', session)
    return jar


def get_with_cookie(url):
    return requests.get(url, cookies=get_cookie_jar())

def yearday():
    """gather the day info from the working directory
    assumes a folder for each year, and folders for each day in that year
    """
    cwd = os.getcwd()
    root, day = os.path.split(cwd)
    root, year = os.path.split(root)
    return year, day
