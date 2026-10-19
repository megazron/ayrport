# Ayrport for VS Code

Language support for [Ayrport](https://github.com/megazron/ayrport), the programming language spoken in airport and flight terms.

## Features

- Syntax highlighting for `.ayr` files
- Hover over any Ayrport word (`counter`, `check`, `flagged`, ...) to see what it means
- Keyword completions and snippets: type `counter`, `check`, `belt`, `shuttle`, `terminal`, `screen`, `gate` and press Tab
- **Run** the current file with **F5**, the ▶ button, **Run Ayrport** in the status bar, or right-click → Run
- Syntax errors get a red underline when you save
- **Ayrport: Show Compiled Python** opens the Python your file compiles to, side by side
- **Ayrport: Open Tower (REPL)** for an interactive prompt
- Auto-indent after block lines (`check x:`, `counter f():`, ...)

## Requirements

Just **Python 3.9+**. Ayrport itself is bundled inside the extension, so there
is nothing else to install. The extension uses the Python you picked in the
Python extension, or `py` / `python3` / `python` from your PATH. To force a
specific one, set **Settings → Ayrport: Python Path**.

```ayr
counter greet(name):
    issue f"Now boarding: {name}"

pa greet("you")
```
