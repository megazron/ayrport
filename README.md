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
load sqrt from math

hangar Aircraft:
    fly prep(cap, callsign, seats):
        cap.callsign = callsign
        cap.seats = seats

    fly status(cap, delay):
        clr delay == 0:
            land "ON TIME"
        alt delay < 30:
            land "DELAYED"
        div:
            land "CANCELLED"

plane = Aircraft("AY101", 180)
taxi d in [0, 12, 95]:
    pa plane.callsign, plane.status(d)
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

Every keyword is short and comes from the airport.

| Ayrport  | Python          | Think of it as            |
|----------|-----------------|---------------------------|
| `pa`     | `print(...)`    | public announcement       |
| `chkin`  | `input`         | check in                  |
| `clr`    | `if`            | cleared for               |
| `alt`    | `elif`          | alternate airport         |
| `div`    | `else`          | divert                    |
| `taxi`   | `for`           | taxi through each item    |
| `hold`   | `while`         | holding pattern           |
| `abort`  | `break`         | abort takeoff             |
| `around` | `continue`      | go-around                 |
| `idle`   | `pass`          | engines idling            |
| `fly`    | `def`           | file a flight plan        |
| `land`   | `return`        | land with a value         |
| `jet`    | `lambda`        | small and fast            |
| `drop`   | `yield`         | drop cargo, keep flying   |
| `hangar` | `class`         | where aircraft are built  |
| `prep`   | `__init__`      | pre-flight prep           |
| `cap`    | `self`          | the captain (convention)  |
| `pre`    | `try`           | pre-flight                |
| `mayday` | `except`        | catch a distress call     |
| `post`   | `finally`       | post-flight               |
| `sos`    | `raise`         | send a distress call      |
| `chk`    | `assert`        | checklist item            |
| `gate`   | `with`          | open a gate, close after  |
| `load`   | `import`        | load cargo                |
| `go` / `nogo` / `nil` | `True` / `False` / `None` | |
| `rwy`    | `range`         | a runway of numbers       |
| `wait`   | `time.sleep`    | wait at the gate          |

`load sqrt, pi from math` is `from math import sqrt, pi`.
A one-line choice reads `"on time" clr delay == 0 div "late"`.

Full guide: **[docs/language.md](docs/language.md)**.

## Use Ayrport from Python

Ayrport is also a Python library. Importing it lets Python `import` any `.ayr`
file like a normal module:

```python
import ayrport
import flightdeck                    # loads flightdeck.ayr

print(flightdeck.eta(5600))

ns = ayrport.run('fly hi(x):\n    land f"hi {x}"\n')   # run a snippet
print(ns["hi"]("there"))

print(ayrport.transpile('clr fuel < 10: pa "low fuel"'))
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

**Install:** download `ayrport-1.0.0.vsix` from the
[latest release](https://github.com/megazron/ayrport/releases/latest), then

```bash
code --install-extension ayrport-1.0.0.vsix
```

or in VS Code: *Extensions → ⋯ → Install from VSIX…*

Build it yourself with `cd vscode-extension && npx @vscode/vsce package`.

## Crashes, in airport terms

```
MAYDAY MAYDAY MAYDAY - Runway length zero (ZeroDivisionError)
  at crash.ayr, line 4, in boom
    land 1 / 0
  division by zero
```

Error lines always point at your `.ayr` file: Ayrport keeps line N of your code
as line N of the Python it runs.

## How it works

```
flight.ayr ──► lexer ──► token rewrite ──► Python source ──► CPython
                 │            │
     strings and comments     clr→if, fly→def, pa x→print(x),
     are never touched        load a from m→from m import a
```

- `src/ayrport/words.py`, the whole vocabulary in one table
- `src/ayrport/lexer.py`, splits code from strings and comments
- `src/ayrport/transpiler.py`, the token rewriter
- `src/ayrport/importer.py`, the `.ayr` import hook
- `src/ayrport/cli.py`, the `ayr` command and the tower REPL

## Examples

See [`examples/`](examples): `hello.ayr`, `basics.ayr` (the whole language),
`fleet.ayr` (classes and errors), `files.ayr`, `fizzbuzz.ayr`, and
`embed.py` (Ayrport from Python).

## Develop

```bash
git clone https://github.com/megazron/ayrport && cd ayrport
pip install -e ".[test]"
pytest
```

## License

MIT © Gaus Mohiuddin Sayyad
