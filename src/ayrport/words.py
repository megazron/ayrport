"""The Ayrport vocabulary: every airport word and the Python it becomes.

Each word was picked because the airport thing behaves like the code concept:
a counter takes your details and issues something back (a function), every
bag rides the belt once (a for loop), a shuttle keeps going round while it is
needed (a while loop), a gate opens for you and closes behind you (with).
"""

# Plain one-to-one swaps. Each Ayrport word becomes exactly one Python token.
KEYWORDS = {
    # decisions: checks you must pass to go one way or another
    "check": "if",          # check: go this way if it passes
    "alt": "elif",          # alternative check
    "div": "else",          # divert: everyone who passed no check
    # loops
    "belt": "for",          # every bag on the belt passes once
    "shuttle": "while",     # the shuttle keeps looping while needed
    "leave": "break",       # leave the loop now
    "skip": "continue",     # skip to the next one
    "standby": "pass",      # on standby: nothing happens
    # counters (functions)
    "counter": "def",       # a counter takes your details and does a job
    "issue": "return",      # the counter issues something back to you
    "kiosk": "lambda",      # self-service counter: tiny and nameless
    "drop": "yield",        # bag drop: hand one over, come back for the next
    # terminals (classes)
    "terminal": "class",    # a terminal groups its own counters and data
    # security (errors)
    "screen": "try",        # everything inside goes through screening
    "flagged": "except",    # what to do when screening flags a problem
    "customs": "finally",   # everyone passes customs, flagged or not
    "flag": "raise",        # flag a problem for security to handle
    "xray": "assert",       # x-ray check: must be fine or you stop here
    # resources
    "gate": "with",         # a gate opens for you and closes behind you
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
    "checkin": "input",
    "rwy": "range",
    "wait": "time.sleep",
    "go": "True",
    "nogo": "False",
    "nil": "None",
}

# One-line meanings, used by `ayr words` and the VS Code hover cards.
MEANINGS = {
    "check": "if — a check: go this way only if it passes",
    "alt": "elif — alternative check, tried when the ones above failed",
    "div": "else — divert: where everyone goes when no check passed (also the `else` of a one-line choice)",
    "belt": "for — every bag on the belt passes once: `belt bag in bags:`",
    "shuttle": "while — the shuttle keeps looping while the condition holds",
    "leave": "break — leave the loop now",
    "skip": "continue — skip to the next one in the loop",
    "standby": "pass — on standby: an empty block that does nothing",
    "counter": "def — a counter takes your details and does a job: define a function",
    "issue": "return — the counter issues something back to you",
    "kiosk": "lambda — a self-service counter, tiny and nameless: `kiosk x: x * 2`",
    "drop": "yield — bag drop: hand over one value, come back for the next",
    "terminal": "class — a terminal groups its own counters and data: define a class",
    "arrive": "__init__ — runs when a new one arrives: the constructor",
    "screen": "try — screening: run code that might be flagged",
    "flagged": "except — what to do when screening flags a problem: `flagged ValueError as e:`",
    "customs": "finally — everyone passes customs, flagged or not: always runs",
    "flag": "raise — flag a problem for security to handle",
    "xray": "assert — x-ray check: must be fine or you stop here",
    "gate": "with — opens for you and closes behind you: `gate open(f) as g:`",
    "load": "import — load cargo: `load math`, `load sqrt from math`",
    "pa": "print — public announcement: `pa \"Now boarding\"`",
    "checkin": "input — check-in: ask the passenger for a value",
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
    "check", "alt", "div", "belt", "shuttle", "counter", "terminal", "screen",
    "flagged", "customs", "gate",
    "if", "elif", "else", "while", "for", "def", "class", "try", "except",
    "finally", "with", "async",
}
