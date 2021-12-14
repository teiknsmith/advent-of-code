# Teikn's Advent of Code

This is a collection of tools and solutions for [Advent of Code](https://adventofcode.com/)

## Solutions

Solutions are organized by year/day in appropriately named folders. The language of the solutions is indicated by the file type - most of these will by Python solutions (`.py`), but occasionally I'll use Haskell (`'hs`), C/C++ (`.c`/`.cpp`), or some other language/system - if it's rather obscure, I'll try to include a readme note (e.g. `2020/21`), although I don't guarantee it (e.g. `2020/4`).

I started doing Advent of Code before I was tracking it with git, and so some of the old solution folders have excess files or template code in the solution -- I'm slowly cleaning these up, but it is a WIP.

## Competitive Tools

I have a slight aversion to using tools other people made. Don't @ me.

### `setup.py`

A scraper that fetches my input for me, and also tries to make it easier to get the test inputs. It's kinda smart at presenting the most likely tests first (thanks [Eric](https://twitter.com/ericwastl) for being somewhat predictable).

Also copies my template to the solution folder and opens the code.

### `watch.py`

A watcher that runs my code whenever the file changes, testing against all files matching `*.in` (created in `setup`). Also provides a way to submit the solutions more easily (clicking into the small submit box on the main site is a struggle sometimes, now I just have to click anywhere in the terminal running `watch`).

### `utils.py`

Just some bits of code used in `setup` and `watch`

### `new`

Probably didn't need this subsection. The file is pretty readable

### `template.py`

Try typing the following quickly and without errors.

```(newi, newj) in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if 0 <= newi < imax and 0 <= newj < jmax```

Now you know why I have this.

## Alternate Leaderboard

One night after finishing the day's problem, I was curious about how quickly I adapted my Part 1 solution to fit Part 2, and how I compared to other people on a personal leaderboard in this metric. I could have manually read the data from the API myself, but I figured I might be curious in the future, so I should automate it. Then I realized that other people on the leaderboard might be curious, so I should publish it. At ~5:30 am the next day, the site was live!

Hence the `web` and `data` folders.

I still haven't set up my personal site (it's on the to-do list, I promise...), so I'm using the hosting of BYU's CS Dept. Also, I haven't done much with front-end work. And as alluded to, this was mostly the work of one ~~night~~ very early morning. Hence, the architecture is not super great. If I have oodles of time and nothing to do, then maybe I'll refactor/rebuild this. But until then, this works well enough.