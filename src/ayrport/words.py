"""The Ayrport vocabulary: every airport word and the Python it lands as."""

# Plain one-to-one swaps. Each Ayrport word becomes exactly one Python token.
KEYWORDS = {
    # decisions
    "gate": "if",           # pass through this gate if ...
    "alt": "elif",          # alternate gate
    "div": "else",          # divert everyone else
    # loops
    "belt": "for",          # every bag on the belt
    "hold": "while",        # wait in the hold room while ...
    "leave": "break",       # leave the queue now
    "skip": "continue",     # skip to the next passenger
    "standby": "pass",      # on standby, do nothing
    # counters (functions) and terminals (classes)
    "counter": "def",       # a counter does one job
    "depart": "return",     # the result departs the counter
    "kiosk": "lambda",      # a tiny self-service counter
    "drop": "yield",        # bag drop: hand one over, keep going
    "terminal": "class",    # a terminal holds counters and gates
    # security
    "screen": "try",        # security screening
    "flagged": "except",    # caught at security
    "customs": "finally",   # everyone goes through customs
    "flag": "raise",        # flag a problem
    "xray": "assert",       # x-ray check: must be true
    # resources
    "lounge": "with",       # enter the lounge, tidy up on the way out
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

# Special method names. `arrive` is the constructor.
DUNDERS = {
    "arrive": "__init__",
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
    "gate": "if — pass through this gate if the condition holds",
    "alt": "elif — alternate gate: try another condition",
    "div": "else — divert: everyone else goes here (also the `else` of a one-line choice)",
    "belt": "for — every bag on the belt: `belt bag in bags:`",
    "hold": "while — wait in the hold room while the condition holds",
    "leave": "break — leave the loop now",
    "skip": "continue — skip to the next pass of the loop",
    "standby": "pass — on standby: an empty block",
    "counter": "def — open a counter: define a function",
    "depart": "return — the result departs the counter",
    "kiosk": "lambda — a tiny self-service counter: `kiosk x: x * 2`",
    "drop": "yield — bag drop: hand one value over and keep going",
    "terminal": "class — a terminal groups counters: define a class",
    "arrive": "__init__ — runs when a new object arrives: the constructor",
    "screen": "try — security screening: run code that might fail",
    "flagged": "except — caught at security: `flagged ValueError as e:`",
    "customs": "finally — everyone goes through customs: always runs",
    "flag": "raise — flag a problem: raise an error",
    "xray": "assert — x-ray check: stop if it is not true",
    "lounge": "with — enter the lounge, tidied up after: `lounge open(f) as g:`",
    "load": "import — load cargo: `load math`, `load sqrt from math`",
    "pa": "print — public announcement: `pa \"Now boarding\"`",
    "chkin": "input — check in a value from the passenger",
    "rwy": "range — a runway of numbers: `rwy(10)`",
    "wait": "time.sleep — wait n seconds",
    "go": "True",
    "nogo": "False",
    "nil": "None",
    "me": "the object itself — conventional name for self",
}

# Every word the transpiler reserves.
RESERVED = set(KEYWORDS) | set(STATEMENTS) | set(DUNDERS)

# Statements that open an indented block (Ayrport and plain Python spellings).
BLOCK_OPENERS = {
    "gate", "alt", "div", "hold", "belt", "counter", "terminal", "screen",
    "flagged", "customs", "lounge",
    "if", "elif", "else", "while", "for", "def", "class", "try", "except",
    "finally", "with", "async",
}
