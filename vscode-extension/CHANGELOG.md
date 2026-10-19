# Changelog

## 1.3.0
- Works out of the box: Ayrport is bundled inside the extension, so only Python is needed (no `pip install`, no PATH setup)
- Finds Python automatically (the Python extension's interpreter, then `py`, `python3`, `python`), or set `ayrport.pythonPath`
- Runs programs directly in their own terminal, so `checkin` (input) works
- Red underline on the line with a syntax error when you open or save a file
- ▶ Run in the status bar, the editor title, the right-click menu and the file explorer; F5 or Ctrl+F5

## 1.2.0
- Vocabulary reworked so every word behaves like what it means: `check` (if), `issue` (return),
  `shuttle` (while), `gate` (with), `checkin` (input)

## 1.1.0
- New airport-terminal vocabulary: `counter`/`depart` (def/return), `terminal`/`arrive` (class/__init__),
  `gate`/`alt`/`div` (if/elif/else), `belt`/`hold` (for/while), `leave`/`skip`/`standby`
  (break/continue/pass), `screen`/`flagged`/`customs`/`flag`/`xray` (try/except/finally/raise/assert),
  `lounge` (with), `kiosk` (lambda), `me` (self)

## 1.0.0
- Syntax highlighting for `.ayr` files
- Hover cards explaining every Ayrport word
- Keyword completions and snippets
- **Ayrport: Run File** (F5 or the ▶ button), **Show Compiled Python**, **Open Tower (REPL)**
- Smart indentation after block lines
