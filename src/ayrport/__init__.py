"""Ayrport — a programming language spoken in airport and flight terms.

Ayrport compiles to Python, so it runs anywhere Python runs and can use any
Python library. Importing this package also teaches Python to import `.ayr`
files directly::

    import ayrport
    import flights          # loads flights.ayr from sys.path

    ayrport.run('pa "Now boarding"')
    print(ayrport.transpile('check go: pa "boarding"'))
"""

from .importer import install, uninstall
from .runtime import HELPERS, compile_ayr, explain, run, run_file
from .transpiler import transpile, translate_expression
from .words import KEYWORDS, MEANINGS

__version__ = "1.3.0"

__all__ = [
    "transpile", "translate_expression", "compile_ayr", "run", "run_file",
    "install", "uninstall", "explain", "KEYWORDS", "MEANINGS", "HELPERS",
    "__version__",
]

install()
