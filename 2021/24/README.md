# AoC 2021/24

Welp. Took more than 24 hours (not straight coding time, I've been spending some time with the fam for the holiday.)

Am I proud of the code here? Some of it, yes. Some of it, not so much.

Some working out I did is recorded [later in this README](#arithmetic-hand-work).

## Some Description of the Process
### Code/Automation
I started with a super naive brute force, just walk backwards from 99999999999999 and run the full instructions on each number until you get a success.

While that was slowly trodding along, I thought about optimizations - first the somewhat obvious ones like pre-computing operations with only constants and reducing identity expressions (e.g. `var1 * 0` → `0`).

Around this phase, I figured it would be easier to debug if I had a graph representation of the expression to be evaluated. So I quickly refreshed my [DOT language](http://graphviz.org/doc/info/lang.html) skills so that I could use [graph-easy](https://github.com/ironcamel/Graph-Easy) to render the graph in the terminal for ease in testing. This wasn't too cumbersome, but it was my first install after recently setting up WSL, so it took a little while longer than it perhaps should have.

The graph form actually helped me see that \[a\] distributive rule~~s~~ would actually be helpful. That started making the reduction logic even more ugly, and I was starting to not like it.

It was at this point that I recognized I already had a pretty decent compiler on hand: `gcc`. At this point, programmatically translating the input to fairly concise C code was relatively easy. So I spun that up, and it was cranking through much faster! This solution would be able to search through the entire space in a mere handful of weeks, and likely get the highest valid model# by morning tomorrow!

But I was unsatisfied with this, knowing that there was a faster solution. Thus began the arithmetic.

### Arithmetic/Hand Work

The variables (vₓ and dₓ) referenced here are as noted in `monad.c` (as produced by `sol.py` for my input), and references to those statements will be labeled as [Cxx] where xx is the line number.

We are looking for constraints on possible bindings for all `d` that result in the monad function returning 0, i.e.
```
 0. 0 = (v₈₂//26)*(1+25v₈₇) + (d₁₃+2)v₈₇      [C18]
```
Additional useful constraints derived from the problem description with minimal workings-out:
```
 1. 1 ≤ dₓ ≤ 9 | 0 ≤ x ≤ 14
 2. vₓ ∈ {0,1} | x ∈ {9,26,40,54,65,76,87}
```
A short proof by contradiction showed that v₈₇ must be 0:
```
 |   3. v₈₇ ≠ 0                          []
 |   4. v₈₇ = 1                          [3, 2]
 |   5. 0 = (v₈₂//26)*(26) + (d₁₃+2)      [0, 4, sub.]
 |   6. v₈₂//26 = (d₁₃+2)/26              [5]
 |   7. 3/26 ≤ v₈₂//26 ≤ 11/26           [6, 1]
 |   8. v₈₂//26 ∉ ℤ                      [7]
 |   9. v₈₂//26 ∈ ℤ                      [// prop.]
10. v₈₇ = 0                          [pbc]
```

And we're off! This is looking good, we have a strong conclusion for one of our unknowns! Unfortunately, the working out is far less clean beyond this first conclusions, and only resulted in possible ranges of values, not specific values, for the unknown variables and digits.

So I started working from the other side `[C4]`, seeing if anything better would come of it. As I was doing this working out, the operations began to feel strangely familiar...this is you would read a number in base 26!

Armed with this realization and a good bit of reasoning power, the lines in the monad function began to make perfect sense! And I could finally thank myself for the work I did earlier with reductions in expressions, as I'm fairly certain that the difficulty in interpretation would have been much higher without the reductions.

Without too much detail into the proofs or what operations are which, the main operations performed in the evaluation are adding a base26 digit to a number, getting the last base26 digit, comparing the difference between two digits to a fixed delta, and conditionally adding a digit based on the truthiness of a previous comparison.

After translating the operations, you can express the intermediate variables relatively easily as base26 numbers and inequality comparisons. Adding digits is sometimes conditional on previous comparisons, these are enclosed in `[]`s:
```
v4 = <d₀+8,d₁+8,d₂+12>

v₉ = inequal?(d₃, d₂+12-8)

v₂₁ = <d₀+8,d₁+8[,d₃+10],d₄+2,d₅+8>

v₂₆ = inequal?(d₆, d₅+8-11)

v₃₅ = <d₀+8,d₁+8[,d₃+10],d₄+2[,d₆+4],d₇+9>

v₄₀ = inequal?(d₈, d₇+9-3)

v₄₉ = <d₀+8,d₁+8[,d₃+10],d₄+2[,d₆+4][,d₈+10],d₉+3>

v₅₄ = inequal?(d₁₀, d₉+3-3)

v₆₀ = <d₀+8,d₁+8[,d₃+10],d₄+2[,d₆+4][,d₈+10][,d₁0+7]>
```

At this point, the expressions for these variables would become even more complicated. However, the last value must be 0, which means v₈₂ must be one (base26) digit, v₇₁ must be two digits, and v₆₀ three. So all the optional digits must be unset, meaning that all the `inequal?` values must be false, and thus we arrive at a list of necessary equalities:
```
d₃ = d₂+4
d₆ = d₅-3
d₈ = d₇+6
d₁₀ = d₉
d₁₁ = d₄+1
d₁₂ = d₁-2
d₁₃ = d₀-8
```
From these equalities, finding the largest number composed of these digits is nearly trivial - for each pair of digits in an equality, set the larger to 9 and the smaller to satisfy the equality. Finding the smallest number is very similar.

## Final Thoughts

As I get to this section, I'm wondering why wrote this the way I did. And how to appropriately end