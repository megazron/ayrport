"""The Ayrport vocabulary: every airport word and the Python it lands as."""

# Plain one-to-one swaps. Each Ayrport word becomes exactly one Python token.
KEYWORDS = {
    # flow control
    "clr": "if",          # cleared for ...
    "alt": "elif",        # alternate airport
    "div": "else",        # divert
    "hold": "while",      # holding pattern
    "taxi": "for",        # taxi through every item
    "abort": "break",     # abort the takeoff
    "around": "continue", # go-around, try the next one
    "idle": "pass",       # engines idling, do nothing
    # functions and classes
    "fly": "def",         # file a flight plan
    "land": "return",     # land with a value
    "jet": "lambda",      # small, fast, anonymous
    "drop": "yield",      # drop cargo, keep flying
    "hangar": "class",    # where the aircraft are built
    # errors
    "pre": "try",         # pre-flight
    "mayday": "except",   # catch a distress call
    "post": "finally",    # post-flight, always runs
    "sos": "raise",       # send a distress call
    "chk": "assert",      # checklist item
    # context
    "gate": "with",       # open a gate, close it after
    # values
    "go": "True",
    "nogo": "False",
    "nil": "None",
}

# Words that turn a whole statement around rather than swapping one token.
STATEMENTS = {
    "pa": "print(...)",                     # public announcement
    "load": "import / from ... import",     # load cargo
}

# Special method names. `prep` is the constructor.
DUNDERS = {
    "prep": "__init__",
}

# Helpers available inside every Ayrport program.
BUILTINS = {
    "pa": "print",
    "chkin": "input",
    "rwy": "range",
    "wait": "time.sleep",
    "go": "True",
    "nogo": "False",
    "nil": "None",
}

# One-line meanings, used by `ayr words` and the VS Code hover cards.
MEANINGS = {
    "clr": "if — cleared for: run the block when the condition holds",
    "alt": "elif — alternate airport: try another condition",
    "div": "else — divert: the fallback branch (also the `else` of a ternary)",
    "hold": "while — holding pattern: loop while the condition holds",
    "taxi": "for — taxi through every item: `taxi x in items:`",
    "abort": "break — abort: leave the loop now",
    "around": "continue — go-around: skip to the next loop pass",
    "idle": "pass — engines idling: an empty block",
    "fly": "def — file a flight plan: define a function",
    "land": "return — land: hand a value back to the caller",
    "jet": "lambda — a small anonymous function: `jet x: x * 2`",
    "drop": "yield — drop cargo and keep flying (generators)",
    "hangar": "class — a hangar builds aircraft: define a class",
    "prep": "__init__ — pre-flight prep: the constructor",
    "pre": "try — pre-flight: run code that might fail",
    "mayday": "except — catch a distress call: `mayday ValueError as e:`",
    "post": "finally — post-flight: always runs",
    "sos": "raise — send a distress call: raise an error",
    "chk": "assert — checklist item: stop if it is not true",
    "gate": "with — open a gate and close it after: `gate open(f) as g:`",
    "load": "import — load cargo: `load math`, `load sqrt from math`",
    "pa": "print — public announcement: `pa \"Now boarding\"`",
    "chkin": "input — check in a value from the passenger",
    "rwy": "range — runway of numbers: `rwy(10)`",
    "wait": "time.sleep — wait n seconds",
    "go": "True",
    "nogo": "False",
    "nil": "None",
    "cap": "the captain — conventional name for self",
}

# Every word the transpiler reserves.
RESERVED = set(KEYWORDS) | set(STATEMENTS) | set(DUNDERS)

# Statements that open an indented block (Ayrport and plain Python spellings).
BLOCK_OPENERS = {
    "clr", "alt", "div", "hold", "taxi", "fly", "hangar", "pre", "mayday",
    "post", "gate",
    "if", "elif", "else", "while", "for", "def", "class", "try", "except",
    "finally", "with", "async",
}
