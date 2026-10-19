# The Ayrport language guide

Ayrport is Python in an airport uniform. It has Python's indentation,
expressions, strings, numbers and standard library; what changes are the
words. Every Ayrport word is an airport thing that **behaves like** the code
it stands for, so if you can find your way through an airport, you can read
Ayrport.

Ayrport is a **superset** of Python: plain Python keywords still work, so you
can mix them while learning. The words below are reserved and cannot be used
as variable names.

## Contents

1. [Announcements and check-in](#announcements-and-check-in)
2. [Values](#values)
3. [Checks (decisions)](#checks-decisions)
4. [Belts and shuttles (loops)](#belts-and-shuttles-loops)
5. [Counters (functions)](#counters-functions)
6. [Terminals (classes)](#terminals-classes)
7. [Security (errors)](#security-errors)
8. [Gates (resources)](#gates-resources)
9. [Loading cargo (imports)](#loading-cargo-imports)
10. [How it works](#how-it-works)

## Announcements and check-in

`pa` is the public announcement system: it prints. No brackets needed.

```ayr
pa "Now boarding"
pa "Gate", 12, sep=": "      # Gate: 12
pa                           # empty line
```

`checkin` asks the passenger for their details: it reads a line of input.

```ayr
name = checkin("Name? ")
```

## Values

| Ayrport | Python  |
|---------|---------|
| `go`    | `True`  |
| `nogo`  | `False` |
| `nil`   | `None`  |

`rwy(n)` (a runway of numbers) is `range(n)`; `wait(s)` pauses for `s` seconds.

## Checks (decisions)

An airport is full of checks, and each one sends you a different way.
`check` is `if`: go this way only if the check passes. `alt` is an
alternative check, tried only when the ones above failed (`elif`). `div`
(divert) is where everyone goes when no check passed (`else`).

```ayr
check bags <= 1:
    pa "carry-on only"
alt bags <= 3:
    pa "drop your bags at the counter"
div:
    pa "excess baggage fee"
```

The same words make a one-line choice:

```ayr
msg = "on time" check delay == 0 div "delayed"
```

## Belts and shuttles (loops)

`belt` is `for`: every bag on the baggage belt passes by exactly once.

```ayr
belt bag in ["red", "blue", "green"]:
    pa "collect", bag
```

`shuttle` is `while`: the shuttle keeps looping round for as long as it is
needed.

```ayr
shuttle queue:
    pa "now serving", queue.pop(0)
```

`leave` gets out of the loop now (`break`). `skip` jumps to the next one
(`continue`). `standby` means nothing happens (`pass`), useful for an empty
block.

## Counters (functions)

You hand your details to a `counter`, it does one job, and it `issue`s
something back to you: that is a function (`def`) and its `return`.

```ayr
counter bag_fee(kg, rate=4.5):
    issue kg * rate

fee = bag_fee(23)
```

A `kiosk` is a self-service counter: tiny and nameless (`lambda`).

```ayr
double = kiosk x: x * 2
```

`drop` works like a bag drop: hand over one value, then come back for the
next (`yield`).

```ayr
counter countdown(n):
    shuttle n > 0:
        drop n
        n -= 1
```

## Terminals (classes)

A `terminal` groups its own counters and data (`class`). `arrive` runs when a
new one arrives (`__init__`). By convention the first parameter of every
counter inside a terminal is `me`, the object itself (Python's `self`).

```ayr
terminal Flight:
    counter arrive(me, code):
        me.code = code

    counter hello(me):
        issue f"This is flight {me.code}"

terminal Charter(Flight):
    counter arrive(me, code):
        super().arrive(code)
```

## Security (errors)

Code you are unsure about goes through `screen`ing. If something gets
`flag`ged, the matching `flagged` block deals with it. Whatever happens,
everyone passes through `customs` at the end.

| Ayrport   | Python    | Meaning                                       |
|-----------|-----------|-----------------------------------------------|
| `screen`  | `try`     | everything inside goes through screening      |
| `flagged` | `except`  | what to do when screening flags a problem     |
| `customs` | `finally` | everyone passes customs, flagged or not       |
| `flag`    | `raise`   | flag a problem for security to handle         |
| `xray`    | `assert`  | x-ray check: must be fine or you stop here    |

```ayr
screen:
    flight.board("Ana")
flagged OverbookedError as e:
    pa "flagged:", e
customs:
    pa "boarding closed"

xray len(crew) >= 2, "need two pilots"
```

When a program crashes, the tower reports it with the Ayrport line:

```
MAYDAY MAYDAY MAYDAY - Runway length zero (ZeroDivisionError)
  at crash.ayr, line 2, in f
    issue x / 0
  division by zero
```

## Gates (resources)

A `gate` opens for you and closes behind you (`with`). Use it for files and
anything else that must be closed after use.

```ayr
gate open("manifest.txt") as f:
    pa f.read()
```

## Loading cargo (imports)

`load` puts cargo on board (`import`). To take only some names out of a
module, put `from` at the end:

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
