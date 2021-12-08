import requests


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


# grab the session cookie from the stored file
with open('../../data/cookie', 'r') as cookie_in:
    session = cookie_in.read()
jar = requests.cookies.RequestsCookieJar()
jar.set('session', session)


def get_with_cookie(url):
    return requests.get(url, cookies=jar)
