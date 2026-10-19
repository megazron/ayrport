import pytest

from ayrport import transpile


@pytest.mark.parametrize("ayr, py", [
    ("gate x: standby", "if x: pass"),
    ("alt x: standby", "elif x: pass"),
    ("div: standby", "else: pass"),
    ("hold go: leave", "while True: break"),
    ("belt i in rwy(3): skip", "for i in range(3): continue"),
    ("counter f(x): depart x", "def f(x): return x"),
    ("terminal A(B): standby", "class A(B): pass"),
    ("screen: standby", "try: pass"),
    ("flagged ValueError as e: flag", "except ValueError as e: raise"),
    ("customs: standby", "finally: pass"),
    ("xray x, 'no'", "assert x, 'no'"),
    ("lounge open(p) as f: standby", "with open(p) as f: pass"),
    ("f = kiosk x: x", "f = lambda x: x"),
    ("drop 1", "yield 1"),
    ("x = nil", "x = None"),
    ("y = nogo", "y = False"),
    ("a = 1 gate ok div 2", "a = 1 if ok else 2"),
    ("counter arrive(me): standby", "def __init__(me): pass"),
    ("super().arrive()", "super().__init__()"),
])
def test_keywords(ayr, py):
    assert transpile(ayr) == py


@pytest.mark.parametrize("ayr, py", [
    ('pa "hi"', 'print("hi")'),
    ("pa a, b, sep='-'", "print(a, b, sep='-')"),
    ("pa", "print()"),
    ("pa x  # note", "print(x)  # note"),
    ("pa x; pa y", "print(x); print(y)"),
    ("gate x: pa 'yes'", "if x: print('yes')"),
    ("pa(1)", "print((1))"),
    ("pa (1,\n    2)", "print((1,\n    2))"),
    ("f = kiosk x: pa(x)", "f = lambda x: print(x)"),
])
def test_pa(ayr, py):
    assert transpile(ayr) == py


@pytest.mark.parametrize("ayr, py", [
    ("load math", "import math"),
    ("load numpy as np", "import numpy as np"),
    ("load sqrt from math", "from math import sqrt"),
    ("load sqrt, pi from math", "from math import sqrt, pi"),
    ("load path as p from os", "from os import path as p"),
    ("load x from .sibling", "from .sibling import x"),
    ("load (a,\n b) from m", "from m import (a,\n b)"),
    ("from math import tau", "from math import tau"),
])
def test_load(ayr, py):
    assert transpile(ayr) == py


def test_strings_and_comments_untouched():
    src = 'x = "gate counter depart pa"  # belt hold leave\n'
    assert transpile(src) == src


def test_triple_quoted_string_untouched():
    src = 'doc = """counter\ndepart\n"""\n'
    assert transpile(src) == src


def test_fstring_expressions_are_translated():
    assert transpile('s = f"{a gate ok div b} depart"') == 's = f"{a if ok else b} depart"'
    assert transpile("s = f'{{nil}} {nil}'") == "s = f'{{nil}} {None}'"


def test_attribute_names_untouched():
    assert transpile("plane.depart()") == "plane.depart()"
    assert transpile("tower.go = 1") == "tower.go = 1"


def test_line_numbers_preserved():
    src = "load sqrt from math\ncounter f(x):\n    pa x\n    depart x\n"
    assert transpile(src).count("\n") == src.count("\n")


def test_assigning_to_pa_is_not_a_print():
    assert transpile("pa = 3") == "print = 3"  # an alias, not a call


def test_plain_python_still_works():
    src = "def f(x):\n    if x:\n        return [i for i in range(x)]\n"
    assert transpile(src) == src


def test_standalone_header_for_wait():
    assert transpile("wait(1)", standalone=True).startswith("from time import sleep as wait")
    assert not transpile("pa 1", standalone=True).startswith("from")


def test_vscode_words_match_language():
    import json
    from pathlib import Path

    from ayrport import MEANINGS

    words = Path(__file__).resolve().parent.parent / "vscode-extension" / "words.json"
    assert json.loads(words.read_text(encoding="utf-8")) == MEANINGS
