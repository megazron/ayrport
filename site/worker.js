// Runs Ayrport programs with Python compiled to WebAssembly (Pyodide).
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
importScripts(PYODIDE + "pyodide.js");

let pyodide = null;
let inputCount = 0;

function send(type, data = {}) {
  postMessage({ type, ...data });
}

// Blocks this worker until the page answers (see sw.js).
function askInput(prompt) {
  const id = `${Date.now()}-${inputCount++}`;
  send("input", { id, prompt });
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `__ayr_input__?id=${encodeURIComponent(id)}`, false);
  try {
    xhr.send(null);
  } catch (e) {
    return "";
  }
  return xhr.status === 200 ? xhr.responseText : "";
}

async function boot() {
  pyodide = await loadPyodide({ indexURL: PYODIDE });
  const bundle = await (await fetch("bundle.json", { cache: "no-cache" })).json();
  const fs = pyodide.FS;
  fs.mkdirTree("/home/pyodide/ayrport");
  for (const [name, text] of Object.entries(bundle.package)) {
    fs.writeFile(`/home/pyodide/ayrport/${name}`, text);
  }
  fs.mkdirTree("/home/pyodide/work");
  for (const [name, text] of Object.entries(bundle.examples)) {
    const full = `/home/pyodide/work/${name}`;
    fs.mkdirTree(full.slice(0, full.lastIndexOf("/")));
    fs.writeFile(full, text);
  }
  pyodide.setStdout({ batched: (s) => send("out", { text: s + "\n" }) });
  pyodide.setStderr({ batched: (s) => send("err", { text: s + "\n" }) });
  pyodide.registerJsModule("ayrhost", {
    ask: (prompt) => askInput(prompt),
    lounge: () => send("lounge"),
  });
  pyodide.runPython(`
import builtins, os, sys
sys.path.insert(0, "/home/pyodide")
sys.path.insert(1, "/home/pyodide/work")
os.chdir("/home/pyodide/work")
import ayrhost, ayrport
from ayrport import runtime

def _input(prompt=""):
    sys.stdout.flush()
    return ayrhost.ask(str(prompt))

builtins.input = _input
runtime.HELPERS["checkin"] = _input
`);
  send("ready", { version: bundle.version });
}

const booted = boot().catch((e) => send("fatal", { text: String(e) }));

self.onmessage = async (e) => {
  const msg = e.data;
  if (msg.type !== "run") return;
  await booted;
  if (!pyodide) return;
  pyodide.FS.writeFile("/home/pyodide/work/main.ayr", msg.code);
  pyodide.globals.set("_ayr_src", msg.code);
  const result = pyodide.runPython(`
import sys, linecache, re
from ayrport.runtime import explain, new_namespace, run
linecache.checkcache()
_path = "/home/pyodide/work/main.ayr"
_line = 0
_ok = True
try:
    run(_ayr_src, new_namespace("__main__", _path), _path)
except SystemExit:
    pass
except BaseException as _e:
    _ok = False
    sys.stdout.flush()
    _report = explain(_e, _ayr_src.splitlines())
    print(_report.replace(_path, "your program"), file=sys.stderr)
    _hits = re.findall(r"your program, line (\\d+)", _report.replace(_path, "your program"))
    _line = int(_hits[-1]) if _hits else 0
sys.stdout.flush()
sys.stderr.flush()
(_ok, _line)
`);
  const [ok, line] = result.toJs();
  result.destroy();
  send("done", { ok, line });
};
