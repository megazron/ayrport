import importlib
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import ayrport

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def test_run_returns_namespace():
    ns = ayrport.run("counter double(x):\n    issue x * 2\nanswer = double(21)\n")
    assert ns["answer"] == 42


def test_helpers_available():
    ns = ayrport.run("r = list(rwy(3))\nflags = [go, nogo, nil]\nhelper = pa\n")
    assert ns["r"] == [0, 1, 2]
    assert ns["flags"] == [True, False, None]
    assert ns["helper"] is print


def test_classes_and_errors():
    ns = ayrport.run(textwrap.dedent("""
        terminal Plane:
            counter arrive(me, seats):
                me.seats = seats
            counter board(me, n):
                check n > me.seats:
                    flag ValueError("full")
                issue n
        p = Plane(2)
        screen:
            p.board(5)
        flagged ValueError as e:
            caught = str(e)
        customs:
            done = go
    """))
    assert ns["caught"] == "full"
    assert ns["done"] is True


def test_import_ayr_module(tmp_path, monkeypatch):
    (tmp_path / "tower_mod.ayr").write_text("counter ping():\n    issue 'pong'\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    mod = importlib.import_module("tower_mod")
    assert mod.ping() == "pong"


def test_import_ayr_package(tmp_path, monkeypatch):
    pkg = tmp_path / "airfield"
    pkg.mkdir()
    (pkg / "__init__.ayr").write_text("NAME = 'airfield'\n")
    (pkg / "radar.ayr").write_text("load NAME from airfield\ncounter scan():\n    issue NAME + ' radar'\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    from airfield import radar
    assert radar.scan() == "airfield radar"


def test_traceback_points_at_ayr_line(tmp_path):
    f = tmp_path / "crash.ayr"
    f.write_text("x = 1\n\ncounter boom():\n    issue 1 / 0\n\nboom()\n")
    with pytest.raises(ZeroDivisionError) as info:
        ayrport.run_file(str(f))
    report = ayrport.explain(info.value)
    assert "Runway length zero" in report
    assert "line 4" in report and "issue 1 / 0" in report


@pytest.mark.parametrize("name", ["basics", "fleet", "files", "fizzbuzz", "flightdeck"])
def test_examples_run(name):
    out = subprocess.run([sys.executable, "-m", "ayrport", str(EXAMPLES / f"{name}.ayr")],
                         capture_output=True, text=True, cwd=EXAMPLES)
    assert out.returncode == 0, out.stderr


def test_embed_example():
    out = subprocess.run([sys.executable, "embed.py"], capture_output=True, text=True, cwd=EXAMPLES)
    assert out.returncode == 0, out.stderr
    assert "AY007" in out.stdout


def test_build_output_runs_as_plain_python(tmp_path):
    py = tmp_path / "out.py"
    subprocess.run([sys.executable, "-m", "ayrport", "build", str(EXAMPLES / "fizzbuzz.ayr"),
                    "-o", str(py)], check=True, capture_output=True)
    out = subprocess.run([sys.executable, "-I", str(py)], capture_output=True, text=True)
    assert out.stdout.splitlines()[14] == "FizzBuzz"


def test_check_command(tmp_path):
    bad = tmp_path / "bad.ayr"
    bad.write_text("check x\n    pa 1\n")
    out = subprocess.run([sys.executable, "-m", "ayrport", "check", str(bad)],
                         capture_output=True, text=True)
    assert out.returncode == 1
    assert "Flight plan rejected" in out.stderr
