"""A small, forgiving lexer for Ayrport source.

Ayrport shares Python's lexical rules (strings, numbers, comments,
indentation), so the lexer only needs to tell code apart from strings and
comments. It never fails: an unterminated string simply runs to the end of the
input, which keeps the REPL happy while a block is still being typed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

NAME, STRING, NUMBER, COMMENT, OP, WS, NL = (
    "NAME", "STRING", "NUMBER", "COMMENT", "OP", "WS", "NL",
)

_NAME_RE = re.compile(r"[^\W\d]\w*")
_NUMBER_RE = re.compile(r"\d[\w.]*|\.\d[\w.]*")
_WS_RE = re.compile(r"[ \t\f]+|\\\r?\n")
_STRING_PREFIXES = {
    "r", "u", "b", "f", "br", "rb", "fr", "rf",
}
_OPEN = "([{"
_CLOSE = ")]}"


@dataclass
class Token:
    kind: str
    text: str
    line: int

    def is_name(self, *words: str) -> bool:
        return self.kind == NAME and (not words or self.text in words)

    def is_op(self, *ops: str) -> bool:
        return self.kind == OP and (not ops or self.text in ops)


def _scan_string(src: str, i: int) -> int:
    """Return the index just past the string literal whose quote is at src[i]."""
    quote = src[i]
    triple = src.startswith(quote * 3, i)
    end_mark = quote * 3 if triple else quote
    j = i + len(end_mark)
    n = len(src)
    while j < n:
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if not triple and c == "\n":
            return j  # unterminated single-line string: stop at the newline
        if src.startswith(end_mark, j):
            return j + len(end_mark)
        j += 1
    return n


def tokenize(src: str) -> list[Token]:
    tokens: list[Token] = []
    i, n, line = 0, len(src), 1
    while i < n:
        c = src[i]
        start = i
        if c == "\n":
            kind, i = NL, i + 1
        elif c == "\r":
            kind = NL
            i += 2 if src.startswith("\r\n", i) else 1
        elif c == "#":
            end = src.find("\n", i)
            kind, i = COMMENT, (n if end == -1 else end)
        elif c in "'\"":
            kind, i = STRING, _scan_string(src, i)
        elif m := _WS_RE.match(src, i):
            kind, i = WS, m.end()
        elif m := _NAME_RE.match(src, i):
            word = m.group()
            if word.lower() in _STRING_PREFIXES and m.end() < n and src[m.end()] in "'\"":
                kind, i = STRING, _scan_string(src, m.end())
            else:
                kind, i = NAME, m.end()
        elif m := _NUMBER_RE.match(src, i):
            kind, i = NUMBER, m.end()
        else:
            kind, i = OP, i + 1
            # keep multi-character operators whole so `==` is never read as `=`
            for op in ("**=", "//=", ">>=", "<<=", "...", "->", ":=", "==", "!=",
                       "<=", ">=", "**", "//", "+=", "-=", "*=", "/=", "%=",
                       "&=", "|=", "^=", "@=", ">>", "<<"):
                if src.startswith(op, start):
                    i = start + len(op)
                    break
        text = src[start:i]
        tokens.append(Token(kind, text, line))
        line += text.count("\n")
    return tokens


def depth_change(tok: Token) -> int:
    if tok.kind == OP:
        if tok.text in _OPEN:
            return 1
        if tok.text in _CLOSE:
            return -1
    return 0
