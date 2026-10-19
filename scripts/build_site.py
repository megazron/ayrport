"""Collect the Ayrport package and examples into site/bundle.json for Ayrport Studio."""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "src"))

from ayrport import __version__  # noqa: E402
from ayrport.words import MEANINGS  # noqa: E402


def main() -> None:
    package = {p.name: p.read_text(encoding="utf-8")
               for p in sorted((ROOT / "src" / "ayrport").glob("*.py"))}
    examples = {}
    for p in sorted((ROOT / "examples").rglob("*.ayr")):
        examples[p.relative_to(ROOT / "examples").as_posix()] = p.read_text(encoding="utf-8")
    bundle = {"version": __version__, "meanings": MEANINGS, "package": package, "examples": examples}
    (SITE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
    shutil.copyfile(ROOT / "vscode-extension" / "images" / "icon.png", SITE / "icon.png")
    lounge = ROOT / "src" / "ayrport" / "lounge.html"
    if lounge.exists():
        shutil.copyfile(lounge, SITE / "lounge.html")
    print(f"site/bundle.json: {len(package)} modules, {len(examples)} examples")


if __name__ == "__main__":
    main()
