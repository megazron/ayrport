"""Runs the copy of Ayrport bundled with the VS Code extension."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ayrport.cli import main  # noqa: E402

sys.exit(main())
