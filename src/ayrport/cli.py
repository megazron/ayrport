"""The `ayr` command.

    ayr flight.ayr            run a file
    ayr build flight.ayr      print the Python it compiles to (-o to save)
    ayr check flight.ayr      check a file without running it
    ayr words                 list every Ayrport word
    ayr                       open the tower (interactive prompt)
"""

from __future__ import annotations

import argparse
import code
import os
import sys

from . import __version__
from .runtime import HELPERS, explain, run_file
from .transpiler import transpile
from .words import MEANINGS

STUDIO_URL = "https://megazron.github.io/ayrport/"

BANNER = (
    f"Ayrport {__version__} tower — Python {sys.version.split()[0]}\n"
    "Type `words()` for the vocabulary, Ctrl-D to close the tower."
)


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def cmd_run(path: str, argv: list[str]) -> int:
    sys.argv = [path] + argv
    try:
        run_file(path)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except BaseException as e:  # report everything, including Ctrl-C
        lines = _read(path).splitlines() if os.path.exists(path) else None
        print(explain(e, lines), file=sys.stderr)
        return 1
    return 0


def cmd_build(path: str, out: str | None) -> int:
    py = transpile(_read(path), standalone=True)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(py)
        print(f"Landed {out}")
    else:
        sys.stdout.write(py)
    return 0


def cmd_check(paths: list[str]) -> int:
    bad = 0
    for path in paths:
        source = _read(path)
        try:
            compile(transpile(source), path, "exec")
            print(f"cleared   {path}")
        except SyntaxError as e:
            bad += 1
            print(explain(e, source.splitlines()), file=sys.stderr)
    return 1 if bad else 0


def words() -> None:
    width = max(map(len, MEANINGS))
    for word, meaning in MEANINGS.items():
        print(f"  {word:<{width}}  {meaning}")


class Tower(code.InteractiveConsole):
    """A REPL that speaks Ayrport."""

    def runsource(self, source, filename="<tower>", symbol="single"):
        return super().runsource(transpile(source), filename, symbol)

    def showsyntaxerror(self, filename=None, **kwargs):
        _, err, _ = sys.exc_info()
        self.write(explain(err) + "\n")

    def showtraceback(self):
        _, err, tb = sys.exc_info()
        err.__traceback__ = tb.tb_next if tb else tb  # drop the console's own frame
        self.write(explain(err) + "\n")


def cmd_repl() -> int:
    from .importer import install

    install()
    ns = {"__name__": "__main__", "words": words}
    ns.update(HELPERS)
    sys.ps1, sys.ps2 = "ayr> ", "...  "
    Tower(ns).interact(banner=BANNER, exitmsg="Tower closed. Safe travels.")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    commands = {"build", "check", "words", "run", "tower", "studio"}
    # `ayr file.ayr args...` is the short form of `ayr run file.ayr args...`
    if argv and argv[0] not in commands and not argv[0].startswith("-"):
        return cmd_run(argv[0], argv[1:])

    p = argparse.ArgumentParser(prog="ayr", description="Ayrport: code in airport terms.")
    p.add_argument("-V", "--version", action="version", version=f"ayrport {__version__}")
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("run", help="run an .ayr file")
    r.add_argument("file")
    r.add_argument("args", nargs=argparse.REMAINDER)
    b = sub.add_parser("build", help="compile an .ayr file to Python")
    b.add_argument("file")
    b.add_argument("-o", "--out", help="write the Python here instead of stdout")
    c = sub.add_parser("check", help="check .ayr files for errors without running them")
    c.add_argument("files", nargs="+")
    sub.add_parser("words", help="list every Ayrport word")
    sub.add_parser("tower", help="interactive prompt (same as plain `ayr`)")
    sub.add_parser("studio", help="open Ayrport Studio in your browser")
    a = p.parse_args(argv)

    if a.cmd == "run":
        return cmd_run(a.file, a.args)
    if a.cmd == "build":
        return cmd_build(a.file, a.out)
    if a.cmd == "check":
        return cmd_check(a.files)
    if a.cmd == "studio":
        import webbrowser
        webbrowser.open(STUDIO_URL)
        print(f"Ayrport Studio: {STUDIO_URL}")
        return 0
    if a.cmd == "words":
        words()
        return 0
    return cmd_repl()


if __name__ == "__main__":
    sys.exit(main())
