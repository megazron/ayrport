"""Import hook: lets Python `import` an .ayr file like any other module."""

from __future__ import annotations

import importlib.machinery
import os
import sys

from .runtime import HELPERS
from .transpiler import transpile

SUFFIX = ".ayr"


class AyrLoader(importlib.machinery.SourceFileLoader):
    """Loads `name.ayr` (or `name/__init__.ayr`) as a Python module."""

    def get_code(self, fullname):
        path = self.get_filename(fullname)
        source = self.get_data(path).decode("utf-8")
        return compile(transpile(source), path, "exec", dont_inherit=True)

    def exec_module(self, module):
        for key, value in HELPERS.items():
            module.__dict__.setdefault(key, value)
        super().exec_module(module)


class AyrFinder:
    """Meta path finder that looks for .ayr files along sys.path."""

    def __init__(self):
        self._finders: dict[str, importlib.machinery.FileFinder] = {}

    def find_spec(self, fullname, path=None, target=None):
        for entry in (path if path is not None else sys.path):
            if not isinstance(entry, str):
                continue
            entry = entry or os.getcwd()
            if not os.path.isdir(entry):
                continue
            finder = self._finders.get(entry)
            if finder is None:
                finder = importlib.machinery.FileFinder(entry, (AyrLoader, [SUFFIX]))
                self._finders[entry] = finder
            spec = finder.find_spec(fullname, target)
            if spec is not None and spec.loader is not None:
                return spec
        return None

    def invalidate_caches(self):
        self._finders.clear()


_finder: AyrFinder | None = None


def install() -> None:
    """Teach Python to import .ayr files. Safe to call more than once."""
    global _finder
    if _finder is not None and _finder in sys.meta_path:
        return
    _finder = AyrFinder()
    # sit just before the normal path finder so `pkg/__init__.ayr` wins over
    # Python treating `pkg/` as an empty namespace package
    for i, f in enumerate(sys.meta_path):
        if f is importlib.machinery.PathFinder:
            sys.meta_path.insert(i, _finder)
            break
    else:
        sys.meta_path.append(_finder)


def uninstall() -> None:
    global _finder
    if _finder is not None and _finder in sys.meta_path:
        sys.meta_path.remove(_finder)
    _finder = None
