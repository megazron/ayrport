# The Ayrport language guide

Ayrport is Python wearing a pilot's uniform. It has Python's indentation,
expressions, strings, numbers and standard library; what changes are the
words. Every Ayrport word is short and comes from airports and flying.

Ayrport is a **superset** of Python: plain Python keywords still work, so you
can mix them while learning. The words below are reserved and cannot be used
as variable names.

## Contents

1. [Printing and input](#printing-and-input)
2. [Values](#values)
3. [Decisions](#decisions)
4. [Loops](#loops)
5. [Functions](#functions)
6. [Classes](#classes)
7. [Errors](#errors)
8. [Resources](#resources)
9. [Loading code](#loading-code)
10. [How it works](#how-it-works)

## Printing and input

`pa` (public announcement) prints. No brackets needed.

```ayr
pa "Now boarding"
pa "Gate", 12, sep=": "      # Gate: 12
pa                           # empty line
```

`chkin` (check in) reads a line from the user.

```ayr
name = chkin("Name? ")
```

## Values

| Ayrport | Python  |
|---------|---------|
| `go`    | `True`  |
| `nogo`  | `False` |
| `nil`   | `None`  |

`rwy(n)` (runway) is `range(n)`; `wait(s)` pauses for `s` seconds.

## Decisions

`clr` (cleared for) is `if`, `alt` (alternate airport) is `elif`, `div`
(divert) is `else`.

```ayr
clr fuel > 50:
    pa "cleared for takeoff"
alt fuel > 10:
    pa "refuel first"
div:
    pa "grounded"
```

The same words make a one-line choice:

```ayr
msg = "on time" clr delay == 0 div "delayed"
```

## Loops

`taxi` is `for`, `hold` (holding pattern) is `while`.

```ayr
taxi gate in rwy(1, 6):
    pa "gate", gate

hold altitude < 30000:
    altitude += 1000
```

`abort` leaves the loop (`break`). `around` (go-around) skips to the next pass
(`continue`). `idle` does nothing (`pass`).

## Functions

`fly` defines a function, `land` returns a value.

```ayr
fly fuel_needed(km, burn=3.2):
    land km * burn
```

`jet` is a small anonymous function (`lambda`):

```ayr
double = jet x: x * 2
```

`drop` hands out values one at a time (`yield`):

```ayr
fly countdown(n):
    hold n > 0:
        drop n
        n -= 1
```

## Classes

A `hangar` builds aircraft (`class`). The constructor is `prep`, and by
convention the first parameter is `cap`, the captain (Python's `self`).

```ayr
hangar Aircraft:
    fly prep(cap, callsign):
        cap.callsign = callsign

    fly hello(cap):
        land f"This is {cap.callsign}"

hangar Jumbo(Aircraft):
    fly prep(cap, callsign):
        super().prep(callsign)
```

## Errors

| Ayrport  | Python    | Meaning                        |
|----------|-----------|--------------------------------|
| `pre`    | `try`     | pre-flight: code that may fail |
| `mayday` | `except`  | catch a distress call          |
| `post`   | `finally` | post-flight: always runs       |
| `sos`    | `raise`   | send a distress call           |
| `chk`    | `assert`  | checklist item                 |

```ayr
pre:
    plane.board("Ana")
mayday OverbookedError as e:
    pa "MAYDAY:", e
post:
    pa "boarding closed"
```

When a program crashes, the tower reports it with the Ayrport line:

```
MAYDAY MAYDAY MAYDAY - Runway length zero (ZeroDivisionError)
  at crash.ayr, line 2, in f
    land x / 0
  division by zero
```

## Resources

`gate` opens something and closes it when the block ends (`with`).

```ayr
gate open("manifest.txt") as f:
    pa f.read()
```

## Loading code

`load` is `import`. To take names out of a module, put `from` at the end:

```ayr
load math
load numpy as np
load sqrt, pi from math        # from math import sqrt, pi
load x from .sibling           # relative imports work too
```

`load` finds both Python modules and other `.ayr` files.

## How it works

The `ayr` tool translates Ayrport into Python token by token and runs it with
the normal Python interpreter. Words inside strings and comments are never
touched, and line N of your `.ayr` file stays line N of the Python, so error
lines are always right. See the Python for any file with:

```bash
ayr build flight.ayr
```
