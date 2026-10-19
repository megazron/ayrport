# The Ayrport language guide

Ayrport is Python in an airport uniform. It has Python's indentation,
expressions, strings, numbers and standard library; what changes are the
words. Every Ayrport word comes from the airport terminal: counters, gates,
baggage belts, security, customs and lounges.

Ayrport is a **superset** of Python: plain Python keywords still work, so you
can mix them while learning. The words below are reserved and cannot be used
as variable names.

## Contents

1. [Announcements and check-in](#announcements-and-check-in)
2. [Values](#values)
3. [Gates (decisions)](#gates-decisions)
4. [Belts and hold rooms (loops)](#belts-and-hold-rooms-loops)
5. [Counters (functions)](#counters-functions)
6. [Terminals (classes)](#terminals-classes)
7. [Security (errors)](#security-errors)
8. [Lounges (resources)](#lounges-resources)
9. [Loading cargo (imports)](#loading-cargo-imports)
10. [How it works](#how-it-works)

## Announcements and check-in

`pa` (public announcement) prints. No brackets needed.

```ayr
pa "Now boarding"
pa "Gate", 12, sep=": "      # Gate: 12
pa                           # empty line
```

`chkin` (check-in) reads a line from the user.

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

## Gates (decisions)

`gate` is `if`: you pass through the gate when the condition holds. `alt`
(alternate gate) is `elif`, and `div` (divert) is `else`.

```ayr
gate bags <= 1:
    pa "carry-on only"
alt bags <= 3:
    pa "check in at the counter"
div:
    pa "excess baggage fee"
```

The same words make a one-line choice:

```ayr
msg = "on time" gate delay == 0 div "delayed"
```

## Belts and hold rooms (loops)

`belt` is `for`: every bag on the baggage belt goes past once.

```ayr
belt bag in ["red", "blue", "green"]:
    pa "collect", bag
```

`hold` is `while`: wait in the hold room while the condition holds.

```ayr
hold queue:
    pa "now serving", queue.pop(0)
```

`leave` exits the loop (`break`). `skip` jumps to the next pass
(`continue`). `standby` does nothing (`pass`).

## Counters (functions)

A `counter` does one job (`def`). Its result `depart`s (`return`).

```ayr
counter bag_fee(kg, rate=4.5):
    depart kg * rate
```

A `kiosk` is a tiny self-service counter (`lambda`):

```ayr
double = kiosk x: x * 2
```

`drop` hands out values one at a time, like a bag drop (`yield`):

```ayr
counter countdown(n):
    hold n > 0:
        drop n
        n -= 1
```

## Terminals (classes)

A `terminal` groups counters together (`class`). `arrive` runs when a new
object arrives (`__init__`), and by convention the first parameter is `me`
(Python's `self`).

```ayr
terminal Flight:
    counter arrive(me, code):
        me.code = code

    counter hello(me):
        depart f"This is flight {me.code}"

terminal Charter(Flight):
    counter arrive(me, code):
        super().arrive(code)
```

## Security (errors)

| Ayrport   | Python    | Meaning                         |
|-----------|-----------|---------------------------------|
| `screen`  | `try`     | security screening              |
| `flagged` | `except`  | caught at security              |
| `customs` | `finally` | everyone goes through customs   |
| `flag`    | `raise`   | flag a problem                  |
| `xray`    | `assert`  | x-ray check: must be true       |

```ayr
screen:
    flight.board("Ana")
flagged OverbookedError as e:
    pa "flagged:", e
customs:
    pa "boarding closed"
```

When a program crashes, the tower reports it with the Ayrport line:

```
MAYDAY MAYDAY MAYDAY - Runway length zero (ZeroDivisionError)
  at crash.ayr, line 2, in f
    depart x / 0
  division by zero
```

## Lounges (resources)

`lounge` opens something and tidies it up when the block ends (`with`).

```ayr
lounge open("manifest.txt") as f:
    pa f.read()
```

## Loading cargo (imports)

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
