#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import requests
import time

from pathlib import Path

DATA_DIR = "./data/"


class Leaderboard:
    NO_TIME = '--:--:--'
    SORTBYS = {
        'local': lambda p: (-p['local_score'], p['last_star_ts']),
        'stars': lambda p: (-p['stars'], p['last_star_ts']),
        'dtlocal': lambda p: p['dt_sortkey']
    }

    def __init__(self, year, code, sortby, sortlink):
        self.year = year
        self.code = code
        self.sortname = sortby
        self.sortby = Leaderboard.SORTBYS[sortby]
        self.usehtml = sortlink is not None
        self.sortlink = sortlink

        self.__process()

    def __process(self):
        data = self.__get_json()
        self.players = [p for p in data['members'].values()]

        self.ndays = max(len(p['completion_day_level']) for p in self.players)

        self.minmaxts = {
            d: {s: [float('inf'), 0]
                for s in range(1, 4)}
            for d in range(1, self.ndays + 1)
        }
        for player in self.players:
            player['dt_sortkey'] = [0, 0, player['last_star_ts']]
            for day, stars in player['completion_day_level'].items():
                release_time = datetime.datetime(
                    year=self.year,
                    month=12,
                    day=int(day),
                    hour=5,
                    tzinfo=datetime.timezone.utc).timestamp()
                for k in list(stars.keys()):
                    stars[int(k)] = stars[k]['get_star_ts'] - release_time
                if '2' in stars:
                    stars[3] = stars[2] - stars[1]
                for k in [1, 2, 3]:
                    if k in stars:
                        minmax = self.minmaxts[int(day)][k]
                        minmax[0] = min(minmax[0], stars[k])
                        minmax[1] = max(minmax[1], stars[k])
                        td = datetime.timedelta(seconds=stars[k])
                        m, s = divmod(td.seconds, 60)
                        h, m = divmod(m, 60)
                        h += td.days * 24
                        stars[str(
                            k
                        )] = ">=100hrs" if h >= 100 else f"{h:0>2}:{m:0>2}:{s:0>2}"
                    else:
                        stars[str(k)] = Leaderboard.NO_TIME

        for d in range(1, self.ndays + 1):
            for sub, player in enumerate(
                    sorted(self.players,
                           key=lambda p: p['completion_day_level'].get(
                               str(d), {}).get(3, float('inf')))):
                if (str(d) not in player['completion_day_level']) or (
                        3 not in player['completion_day_level'][str(d)]):
                    break
                player['dt_sortkey'][0] -= len(self.players) - sub
                player['dt_sortkey'][1] -= 1

        self.index_width = len(str(len(self.players)))
        self.score_width = max(len(str(self.__score(p))) for p in self.players)

        self.players.sort(key=self.sortby)

    def __score(self, player):
        return -self.sortby(player)[0]

    def __print_sort_header(self):
        print("Sort by:", end='')
        if self.usehtml:
            for k in Leaderboard.SORTBYS:
                print('  ', end='')
                if k == self.sortname:
                    print("<strong>", end='')
                self.sortlink[1] = k
                url = ''.join(self.sortlink)
                print(f'<a href="{url}">[{k}]</a>', end='')
                if k == self.sortname:
                    print("</strong>", end='')
            print()
        else:
            print(self.sortname)

    def __print_table_headers(self):
        iwidth = self.index_width
        scwidth = self.score_width
        ndays = self.ndays

        print(f"{1:>{iwidth+scwidth+17}}", end='')
        for d in range(2, ndays + 1):
            print(f"{d:>27}", end='')
        print()

        print(' ' * (iwidth + scwidth + 2), end='')
        for _ in range(ndays):
            print(f" {'='*26}", end='')
        print()

        print(' ' * (iwidth + scwidth - 1), end='')
        for _ in range(ndays):
            print(f"       S1       S2       Δt", end='')
        print()

        print(' ' * (iwidth + scwidth + 2), end='')
        for _ in range(ndays):
            print(f" {' '.join(['='*8]*3)}", end='')
        print()

    def __printing_time_field(self, player_starval_map, day, star):
        base_str = player_starval_map[star]
        MIN_OPACITY, MAX_OPACITY = 0.15, 1.0
        mint, maxt = self.minmaxts[day][int(star)]
        NO_TIME_OPACITY = 0.05
        if self.usehtml:
            opacity = NO_TIME_OPACITY
            if int(star) in player_starval_map:
                t = player_starval_map[int(star)]
                opacity = MAX_OPACITY - (MAX_OPACITY - MIN_OPACITY) * (
                    t - mint) / (maxt - mint)
            return f'<span class="time" data-opacity="{opacity}" style="filter: opacity({opacity});">{base_str}</span>'
        else:
            return base_str

    def __print_table(self):
        iwidth = self.index_width
        scwidth = self.score_width
        ndays = self.ndays
        noattempt = {str(i): Leaderboard.NO_TIME for i in range(1, 4)}
        for i, player in enumerate(self.players):
            print(f"{i+1:>{iwidth}}) {self.__score(player):>{scwidth}}",
                  end='')
            for d in range(ndays):
                times = player['completion_day_level'].get(
                    str(d + 1), noattempt)
                for k in "123":
                    print('',
                          self.__printing_time_field(times, d + 1, k),
                          end='')
            print('', player['name'])
            print()

    def print(self):
        self.__print_sort_header()
        self.__print_table_headers()
        self.__print_table()

    def __get_raw_from_source(self):
        url = (f"https://adventofcode.com/{self.year}/"
               f"leaderboard/private/view/{self.code}.json")
        with open(DATA_DIR + 'cookie', 'r') as cookie_in:
            session = cookie_in.read()
        jar = requests.cookies.RequestsCookieJar()
        jar.set('session', session)
        r = requests.get(url, cookies=jar)
        return r.json()

    def __get_json(self):
        cache_path = Path(DATA_DIR + f'.lbcache/{self.year}.{self.code}.json')
        use_cache = (cache_path.exists()
                     and cache_path.stat().st_mtime + 900 > time.time())
        if use_cache:
            with open(cache_path, 'r') as fin:
                return json.load(fin)
        else:
            res = self.__get_raw_from_source()
            with open(cache_path, 'w') as fout:
                json.dump(res, fout)
            return res


def read_boards_from_config_file():
    boards = []
    with open(DATA_DIR + 'leaderboards', 'r') as fin:
        for l in fin.readlines():
            boards.append(l.strip().split('=', 1))
    return boards


def display_boards(boards):
    for i, (_, name) in enumerate(boards):
        print(f'{i}: {name}')


def get_board_id_from_user(boards):
    display_boards(boards)
    board_idx = -1
    while not (0 <= board_idx < len(boards)):
        try:
            board_idx = int(
                input("Select the index of the leaderboard you want to see: "))
            boards[board_idx]
        except ValueError:
            print("You must enter an int")
        except IndexError:
            print("The index must be in range")
    return boards[board_idx][0]


printerrs = False


def get_args():
    global printerrs
    SORTKEY_FILLER = '~~'
    parser = argparse.ArgumentParser(
        description="generate more detailed advent of code leaderboard")
    parser.add_argument("-y", "--year", help="year of the leaderboard to use")
    parser.add_argument("-c",
                        "--code",
                        help="code of the leaderboard to use"
                        " (found at the end of the url for the leaderboard)")
    parser.add_argument(
        "-s",
        "--sort",
        default='local',
        help="what to sort the players by."
        " `local` and `stars` are the same as on the official site."
        " `dtlocal` is like `local`, but orders the ranking for each daily star only by the delta time"
    )
    parser.add_argument(
        "-w",
        "--web-sortlink-template",
        metavar=f'LI{SORTKEY_FILLER}NK',
        dest='web_sortlink_template',
        help=
        "a template sortlink to provide for the link tags in a sort header. omit for a plain text sort header."
        f" use `{SORTKEY_FILLER}` in the link to show where the sortkey belongs, `e.g. foo.bar/aoc?sortby={SORTKEY_FILLER}&board=12345`."
        f" if you want to use a {SORTKEY_FILLER} in the link otherwise, tough luck for now. if you ping me, maybe I'll do something about it"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help=
        "suppress the suppression of errors (by default, all exceptions are caught and a web-friendly message presented)"
    )
    parser.add_argument(
        "-r",
        "--readme",
        action="store_true",
        help="prior to all other output, spit out the readme (html)")
    args = parser.parse_args()

    if args.debug:
        printerrs = True

    year = args.year
    code = args.code
    sortby = args.sort
    sort_choices = ['local', 'stars', 'dtlocal']
    if sortby not in sort_choices:
        print(f"Invalid sort identifier - must be in {sort_choices}")
        raise Exception("")
    sortlink = args.web_sortlink_template
    if sortlink is not None:
        try:
            l, r = sortlink.split(SORTKEY_FILLER)
            sortlink = [l, '', r]
        except:
            raise
    if year is None:
        year = datetime.datetime.now().year
    try:
        year = int(year)
    except:
        print("Invalid year - must be an int")
        raise
    if code is None:
        board_list = read_boards_from_config_file()
        code = get_board_id_from_user(board_list)
        print()
    try:
        code = int(code)
    except:
        print("Invalid leaderboard id - must be an int")
        raise
    return args.readme, (year, code, sortby, sortlink)


if __name__ == '__main__':
    try:
        readme, args = get_args()
        year, code, _, _ = args
        linkify = lambda text: f'[<a href="https://adventofcode.com/{year}/leaderboard/private/view/{code}">{text}</a>]'
        if readme:
            print("<div id='readme'>")
            print(
                f"this is a different view of an {linkify('Advent of Code leaderboard')}.\n"
                "rather than just displaying stars, the time it took to solve each problem is shown\n"
                "\n"
                "note that in keeping with the rate limit request tied to the endpoint this page scrapes from,\n"
                "this page takes a minimum 15 of minutes between pulling updates from the Advent of Code servers.\n"
                "as such, this page does not update in real time and will not always have the most recent results\n"
                "\n"
                "for each day (up to the most recent any competitor has completed at least one star on), there are three columns:\n"
                "    -S1: the time it took from the release of the puzzle to when the first star was earned\n"
                "    -S1: the time it took from the release of the puzzle to when the second star was earned\n"
                "    -Δt: S2 - S1, or the time it took to finish Part Two after finishing Part One\n"
                "\n"
                "additionally, another sort option is presented.\n"
                f"'local' and 'stars' are the same as on {linkify('the official site')} - click 'Ordering' to see how those are calculated.\n"
                "the new option, 'dtlocal', is calculated much like 'local' with the highest ranking earning N points, etc.\n"
                "however, the initial ranking is done once per day, and is ordered by lowest Δt"
            )
            print("</div>")
        lb = Leaderboard(*args)
        lb.print()
    except:
        if printerrs:
            raise

        RUH_ROH = "somethings not working right now, please ping/dm me to let me know (unless it's your fault -- if so, then fix yourself, child!)."
        RUH_ROH = "I'm woking on this, sorry for the problmes"
        try:
            with open(DATA_DIR + 'knownerrors') as fin:
                errs = fin.read().strip().split('\n')
            if errs and errs[0]:
                print("I am aware of the following issues:")
                for err in errs:
                    print("  -", err)
                print(
                    "If you know that something else is wrong, please let me know."
                )
            else:
                print(RUH_ROH)
        except:
            print(RUH_ROH)
