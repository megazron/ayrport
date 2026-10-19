<p align="center">
  <img src="vscode-extension/images/icon.png" width="120" alt="Ayrport logo">
</p>

<h1 align="center">Ayrport</h1>

<p align="center"><b>A programming language spoken in airport and flight terms.</b><br>
Short words, Python power. Runs anywhere Python runs.</p>

<p align="center">
  <a href="https://github.com/megazron/ayrport/actions/workflows/ci.yml"><img src="https://github.com/megazron/ayrport/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

```ayr
terminal Flight:
    counter arrive(me, code, seats):
        me.code = code
        me.seats = seats

    counter status(me, delay):
        gate delay == 0:
            depart "ON TIME"
        alt delay < 30:
            depart "DELAYED"
        div:
            depart "CANCELLED"

flight = Flight("AY101", 180)
belt d in [0, 12, 95]:
    pa flight.code, flight.status(d)
```

```
AY101 ON TIME
AY101 DELAYED
AY101 CANCELLED
```

## Install

```bash
pip install git+https://github.com/megazron/ayrport
```

This gives you the `ayr` command and the `ayrport` Python package.

## Run

```bash
ayr flight.ayr            # run a file
ayr                       # open the tower (interactive prompt)
ayr build flight.ayr      # show the Python it compiles to (-o out.py to save)
ayr check *.ayr           # check files for errors without running them
ayr words                 # list every Ayrport word
```

`python -m ayrport ...` works the same way.

## The words

Every keyword comes from the airport terminal: counters, gates, belts,
security, customs and lounges.

| Ayrport    | Python       | Think of it as                         |
|------------|--------------|----------------------------------------|
| `counter`  | `def`        | a counter does one job                 |
| `depart`   | `return`     | the result departs the counter         |
| `kiosk`    | `lambda`     | a tiny self-service counter            |
| `terminal` | `class`      | a terminal groups counters             |
| `arrive`   | `__init__`   | runs when a new object arrives         |
| `me`       | `self`       | the object itself (convention)         |
| `gate`     | `if`         | pass through this gate if ...          |
| `alt`      | `elif`       | alternate gate                         |
| `div`      | `else`       | divert everyone else                   |
| `belt`     | `for`        | every bag on the baggage belt          |
| `hold`     | `while`      | wait in the hold room while ...        |
| `leave`    | `break`      | leave the loop                         |
| `skip`     | `continue`   | skip to the next one                   |
| `standby`  | `pass`       | on standby, do nothing                 |
| `drop`     | `yield`      | bag drop: hand one over, keep going    |
| `screen`   | `try`        | security screening                     |
| `flagged`  | `except`     | caught at security                     |
| `customs`  | `finally`    | everyone goes through customs          |
| `flag`     | `raise`      | flag a problem                         |
| `xray`     | `assert`     | x-ray check                            |
| `lounge`   | `with`       | enter the lounge, tidied up after      |
| `load`     | `import`     | load cargo                             |
| `pa`       | `print(...)` | public announcement                    |
| `chkin`    | `input`      | check-in                               |
| `rwy`      | `range`      | a runway of numbers                    |
| `wait`     | `time.sleep` | wait at the gate                       |
| `go` / `nogo` / `nil` | `True` / `False` / `None` |              |

`load sqrt, pi from math` is `from math import sqrt, pi`.
A one-line choice reads `"on time" gate delay == 0 div "late"`.

Full guide: **[docs/language.md](docs/language.md)**.

## Use Ayrport from Python

Ayrport is also a Python library. Importing it lets Python `import` any `.ayr`
file like a normal module:

```python
import ayrport
import flightdeck                    # loads flightdeck.ayr

print(flightdeck.eta(5600))

ns = ayrport.run('counter hi(x):\n    depart f"hi {x}"\n')   # run a snippet
print(ns["hi"]("there"))

print(ayrport.transpile('gate fuel < 10: pa "low fuel"'))
# if fuel < 10: print("low fuel")
```

| Function | What it does |
|---|---|
| `ayrport.run(source)` | run Ayrport code, return its variables |
| `ayrport.run_file(path)` | run an `.ayr` file |
| `ayrport.transpile(source)` | Ayrport source → Python source |
| `ayrport.compile_ayr(source)` | Ayrport source → Python code object |
| `ayrport.install()` / `uninstall()` | turn the `.ayr` import hook on/off (on by default) |

And it works the other way too: `load numpy as np` inside Ayrport loads any
Python library.

## VS Code extension

The [`vscode-extension`](vscode-extension) folder holds the Ayrport extension:
syntax highlighting, hover cards that explain every word, completions,
snippets, auto-indent, and a ▶ **Run** button (F5).

**Install:** download `ayrport-1.1.0.vsix` from the
[latest release](https://github.com/megazron/ayrport/releases/latest), then

```bash
code --install-extension ayrport-1.1.0.vsix
```

or in VS Code: *Extensions → ⋯ → Install from VSIX…*

Build it yourself with `cd vscode-extension && npx @vscode/vsce package`.

## Crashes, in airport terms

```
MAYDAY MAYDAY MAYDAY - Runway length zero (ZeroDivisionError)
  at crash.ayr, line 4, in boom
    depart 1 / 0
  division by zero
```

Error lines always point at your `.ayr` file: Ayrport keeps line N of your code
as line N of the Python it runs.

## How it works

```
flight.ayr ──► lexer ──► token rewrite ──► Python source ──► CPython
                 │            │
     strings and comments     gate→if, counter→def, pa x→print(x),
     are never touched        load a from m→from m import a
```

- `src/ayrport/words.py`, the whole vocabulary in one table
- `src/ayrport/lexer.py`, splits code from strings and comments
- `src/ayrport/transpiler.py`, the token rewriter
- `src/ayrport/importer.py`, the `.ayr` import hook
- `src/ayrport/cli.py`, the `ayr` command and the tower REPL

## Examples

See [`examples/`](examples): `hello.ayr`, `basics.ayr` (the whole language),
`fleet.ayr` (terminals and security), `files.ayr`, `fizzbuzz.ayr`, and
`embed.py` (Ayrport from Python).

## Develop

```bash
git clone https://github.com/megazron/ayrport && cd ayrport
pip install -e ".[test]"
pytest
```

## License

MIT © Gaus Mohiuddin Sayyad
