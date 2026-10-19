"""Compile and run Ayrport code, and explain crashes in airport terms."""

from __future__ import annotations

import linecache
import os
import sys
import time
import traceback
from types import CodeType

from .transpiler import transpile

# Names every Ayrport program can use, even inside f-strings and eval().
HELPERS = {
    "pa": print,
    "checkin": input,
    "rwy": range,
    "wait": time.sleep,
    "go": True,
    "nogo": False,
    "nil": None,
}

# What the tower says for common errors.
CALLOUTS = {
    "NameError": "Unknown callsign",
    "SyntaxError": "Flight plan rejected",
    "IndentationError": "Flight plan rejected: bad indentation",
    "TypeError": "Wrong aircraft type",
    "ValueError": "Bad cargo value",
    "ZeroDivisionError": "Runway length zero",
    "IndexError": "No such seat",
    "KeyError": "No such booking",
    "AttributeError": "Aircraft has no such part",
    "ImportError": "Cargo not found",
    "ModuleNotFoundError": "Cargo not found",
    "FileNotFoundError": "Gate not found",
    "AssertionError": "Checklist failed",
    "RecursionError": "Stuck in a holding pattern",
    "KeyboardInterrupt": "Flight cancelled",
}


def compile_ayr(source: str, filename: str = "<ayrport>", mode: str = "exec") -> CodeType:
    """Compile Ayrport source into a Python code object."""
    return compile(transpile(source), filename, mode)


def new_namespace(name: str = "__main__", filename: str | None = None) -> dict:
    ns = {"__name__": name, "__builtins__": __builtins__}
    if filename:
        ns["__file__"] = filename
    ns.update(HELPERS)
    return ns


def run(source: str, namespace: dict | None = None, filename: str = "<ayrport>") -> dict:
    """Run Ayrport source and return the namespace it ran in.

    >>> ns = run("counter double(x):\\n    issue x * 2\\n")
    >>> ns["double"](21)
    42
    """
    if namespace is None:
        namespace = new_namespace("__ayrport__")
    else:
        for key, value in HELPERS.items():
            namespace.setdefault(key, value)
    _remember(filename, source)
    exec(compile_ayr(source, filename), namespace)
    return namespace


def run_file(path: str, name: str = "__main__") -> dict:
    """Run an .ayr file as a script and return its namespace."""
    from .importer import install

    install()
    path = os.path.abspath(path)
    with open(path, encoding="utf-8") as f:
        source = f.read()
    folder = os.path.dirname(path)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    return run(source, new_namespace(name, path), path)


def _remember(filename: str, source: str) -> None:
    """Let tracebacks show Ayrport lines even for code that has no file."""
    if filename.startswith("<"):
        lines = source.splitlines(keepends=True)
        linecache.cache[filename] = (len(source), None, lines, filename)


def explain(exc: BaseException, source_lines: list[str] | None = None) -> str:
    """Format an exception as a MAYDAY report pointing at the Ayrport line."""
    kind = type(exc).__name__
    callout = CALLOUTS.get(kind, "Mayday")
    lines = [f"MAYDAY MAYDAY MAYDAY - {callout} ({kind})"]
    if isinstance(exc, SyntaxError):
        where = f"  at {exc.filename}, line {exc.lineno}"
        lines.append(where)
        text = None
        if source_lines and exc.lineno and 0 < exc.lineno <= len(source_lines):
            text = source_lines[exc.lineno - 1]
        elif exc.filename and exc.lineno:
            text = linecache.getline(exc.filename, exc.lineno)
        if text:
            lines.append("    " + text.strip())
        lines.append(f"  {exc.msg}")
        return "\n".join(lines)
    frames = [f for f in traceback.extract_tb(exc.__traceback__)
              if not f.filename.startswith(os.path.dirname(__file__))]
    for fr in frames:
        lines.append(f"  at {fr.filename}, line {fr.lineno}, in {fr.name}")
        code = linecache.getline(fr.filename, fr.lineno).strip()
        if code:
            lines.append(f"    {code}")
    lines.append(f"  {exc}" if str(exc) else f"  {kind}")
    return "\n".join(lines)
