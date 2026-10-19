"""Turn Ayrport source into Python source.

The translation is token based, so words inside strings and comments are never
touched, and it is line preserving: line N of the Ayrport file is line N of the
generated Python. That keeps tracebacks pointing at the right Ayrport line.
"""

from __future__ import annotations

import re

from .lexer import COMMENT, NAME, NL, OP, STRING, WS, Token, depth_change, tokenize
from .words import BLOCK_OPENERS, DUNDERS, KEYWORDS

# Helper words that translate straight to a Python builtin.
_BUILTIN_SWAPS = {"pa": "print", "chkin": "input", "rwy": "range"}

_ASSIGN_OPS = {"=", "+=", "-=", "*=", "/=", "//=", "%=", "**=", "@=", "&=",
               "|=", "^=", ">>=", "<<=", ":="}
_NOT_A_STATEMENT = _ASSIGN_OPS | {".", ",", ":", ")", "]", "}"}
_FSTRING_HEAD = re.compile(r"([A-Za-z]*)('''|\"\"\"|'|\")")


def transpile(source: str, standalone: bool = False) -> str:
    """Translate Ayrport source to Python source.

    With ``standalone=True`` a header is added so the output runs with plain
    ``python`` (it costs one line of line-number alignment).
    """
    tokens = [_translate_fstring(t) if t.kind == STRING else t
              for t in tokenize(source)]
    out: list[Token] = []
    for stmt in _statements(tokens):
        out.extend(_rewrite_statement(stmt))
    code = "".join(t.text for t in _swap_names(out))
    if standalone and _uses_name(out, "wait"):
        code = "from time import sleep as wait  # ayrport helper\n" + code
    return code


def _uses_name(tokens: list[Token], word: str) -> bool:
    prev = None
    for t in tokens:
        if t.kind == NAME and t.text == word and not (prev and prev.is_op(".")):
            return True
        if t.kind not in (WS, NL, COMMENT):
            prev = t
    return False


def _sig(tokens: list[Token]) -> list[int]:
    return [i for i, t in enumerate(tokens) if t.kind not in (WS, NL, COMMENT)]


def _statements(tokens: list[Token]):
    """Split the token stream into simple statements.

    A statement ends at a newline outside brackets, at a `;`, or at the colon
    that opens a block (so `gate x: pa x` is two statements).
    """
    stmt: list[Token] = []
    depth = 0
    first: Token | None = None
    for tok in tokens:
        stmt.append(tok)
        depth = max(0, depth + depth_change(tok))
        if first is None and tok.kind not in (WS, NL, COMMENT):
            first = tok
        if depth:
            continue
        ends = (
            tok.kind == NL
            or tok.is_op(";")
            or (tok.is_op(":") and first is not None and first.kind == NAME
                and first.text in BLOCK_OPENERS)
        )
        if ends:
            yield stmt
            stmt, first = [], None
    if stmt:
        yield stmt


def _rewrite_statement(stmt: list[Token]) -> list[Token]:
    sig = _sig(stmt)
    if not sig:
        return stmt
    first = stmt[sig[0]]
    nxt = stmt[sig[1]] if len(sig) > 1 else None
    if first.is_name("pa") and not (nxt and nxt.is_op(*_NOT_A_STATEMENT)):
        return _rewrite_pa(stmt, sig)
    if first.is_name("load") and nxt is not None and not nxt.is_op(*_NOT_A_STATEMENT):
        return _rewrite_load(stmt, sig)
    return stmt


def _body_end(stmt: list[Token], sig: list[int]) -> int:
    """Index of the last meaningful token, ignoring a trailing `;` separator."""
    last = sig[-1]
    if stmt[last].is_op(";") and len(sig) > 1:
        last = sig[-2]
    return last


def _rewrite_pa(stmt: list[Token], sig: list[int]) -> list[Token]:
    """`pa a, b` -> `print(a, b)`"""
    start = sig[0]
    line = stmt[start].line
    if len(sig) == 1 or (len(sig) == 2 and stmt[sig[1]].is_op(";")):
        return stmt[:start] + [Token(OP, "print()", line)] + stmt[start + 1:]
    end = _body_end(stmt, sig)
    middle = stmt[start + 1:end + 1]
    while middle and middle[0].kind == WS:
        middle = middle[1:]
    return (stmt[:start] + [Token(OP, "print(", line)] + middle
            + [Token(OP, ")", stmt[end].line)] + stmt[end + 1:])


def _rewrite_load(stmt: list[Token], sig: list[int]) -> list[Token]:
    """`load m` -> `import m`;  `load a, b from m` -> `from m import a, b`"""
    start = sig[0]
    line = stmt[start].line
    depth = 0
    from_at = None
    for i in range(start + 1, len(stmt)):
        depth += depth_change(stmt[i])
        if depth == 0 and stmt[i].is_name("from"):
            from_at = i
            break
    if from_at is None:
        return stmt[:start] + [Token(NAME, "import", line)] + stmt[start + 1:]
    end = _body_end(stmt, sig)
    what = _strip(stmt[start + 1:from_at])
    module = _strip(stmt[from_at + 1:end + 1])
    return (stmt[:start]
            + [Token(NAME, "from", line), Token(WS, " ", line)] + module
            + [Token(WS, " ", line), Token(NAME, "import", line), Token(WS, " ", line)]
            + what + stmt[end + 1:])


def _strip(tokens: list[Token]) -> list[Token]:
    while tokens and tokens[0].kind == WS:
        tokens = tokens[1:]
    while tokens and tokens[-1].kind == WS:
        tokens = tokens[:-1]
    return tokens


def _swap_names(tokens: list[Token]) -> list[Token]:
    out: list[Token] = []
    prev: Token | None = None
    for tok in tokens:
        if tok.kind == NAME:
            after_dot = prev is not None and prev.is_op(".")
            word = tok.text
            if word in DUNDERS:
                tok = Token(NAME, DUNDERS[word], tok.line)
            elif not after_dot and word in KEYWORDS:
                tok = Token(NAME, KEYWORDS[word], tok.line)
            elif not after_dot and word in _BUILTIN_SWAPS:
                tok = Token(NAME, _BUILTIN_SWAPS[word], tok.line)
        out.append(tok)
        if tok.kind not in (WS, NL, COMMENT):
            prev = tok
    return out


def translate_expression(expr: str) -> str:
    """Translate a single Ayrport expression (no statement rewrites)."""
    tokens = [_translate_fstring(t) if t.kind == STRING else t for t in tokenize(expr)]
    return "".join(t.text for t in _swap_names(tokens))


def _translate_fstring(tok: Token) -> Token:
    """Translate the `{...}` expressions inside an f-string."""
    m = _FSTRING_HEAD.match(tok.text)
    if not m or "f" not in m.group(1).lower():
        return tok
    text = tok.text
    out = []
    i = m.end()
    n = len(text)
    out.append(text[:i])
    while i < n:
        c = text[i]
        if c in "{}" and text.startswith(c * 2, i):
            out.append(c * 2)
            i += 2
        elif c == "{":
            j = _match_brace(text, i)
            out.append("{" + translate_expression(text[i + 1:j]) + "}")
            i = j + 1
        else:
            out.append(c)
            i += 1
    return Token(STRING, "".join(out), tok.line)


def _match_brace(text: str, i: int) -> int:
    depth = 0
    j = i
    n = len(text)
    while j < n:
        c = text[j]
        if c in "'\"":
            k = text.find(c, j + 1)
            j = n - 1 if k == -1 else k
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return n - 1
