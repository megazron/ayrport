# Ayrport for VS Code

Language support for [Ayrport](https://github.com/megazron/ayrport), the programming language spoken in airport and flight terms.

## Features

- Syntax highlighting for `.ayr` files
- Hover over any Ayrport word (`counter`, `gate`, `flagged`, ...) to see what it means
- Keyword completions and snippets: type `counter`, `gate`, `belt`, `terminal`, `screen`, `lounge` and press Tab
- **Run** the current file with **F5** or the ▶ button in the editor title bar
- **Ayrport: Show Compiled Python** opens the Python your file compiles to, side by side
- **Ayrport: Open Tower (REPL)** for an interactive prompt
- Auto-indent after block lines (`gate x:`, `counter f():`, ...)

## Requirements

Install the language itself:

```bash
pip install git+https://github.com/megazron/ayrport
```

If `ayr` is not on your PATH, set **Settings → Ayrport: Command** to `python -m ayrport`.

```ayr
counter greet(name):
    depart f"Now boarding: {name}"

pa greet("you")
```
