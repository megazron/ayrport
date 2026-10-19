// Ayrport for VS Code: run files, check them as you type, view the compiled Python,
// hover meanings and completions. Ships its own copy of Ayrport, so only Python is needed.
const vscode = require("vscode");
const cp = require("child_process");
const path = require("path");
const WORDS = require("./words.json");

let launcher;
let python = null; // { exe } once found
let runTerminal = null;
let diagnostics;

function config() {
  return vscode.workspace.getConfiguration("ayrport");
}

// --- finding Python -------------------------------------------------------

function realExecutable(cmd, args) {
  try {
    const out = cp.execFileSync(
      cmd,
      [...args, "-c", "import sys; print(sys.executable if sys.version_info >= (3, 9) else '')"],
      { timeout: 10000, windowsHide: true, encoding: "utf8" },
    );
    const exe = out.trim();
    return exe || null;
  } catch {
    return null;
  }
}

async function pythonExtensionInterpreter(resource) {
  const ext = vscode.extensions.getExtension("ms-python.python");
  if (!ext) return null;
  try {
    if (!ext.isActive) await ext.activate();
    const env = ext.exports?.environments?.getActiveEnvironmentPath?.(resource);
    return env?.path || null;
  } catch {
    return null;
  }
}

async function findPython(resource) {
  if (python) return python;
  const candidates = [];
  const configured = config().get("pythonPath");
  if (configured) candidates.push([configured, []]);
  const fromExt = await pythonExtensionInterpreter(resource);
  if (fromExt) candidates.push([fromExt, []]);
  if (process.platform === "win32") {
    candidates.push(["py", ["-3"]], ["python", []], ["python3", []]);
  } else {
    candidates.push(["python3", []], ["python", []]);
  }
  for (const [cmd, args] of candidates) {
    const exe = realExecutable(cmd, args);
    if (exe) {
      python = { exe };
      return python;
    }
  }
  const pick = await vscode.window.showErrorMessage(
    "Ayrport needs Python 3.9 or newer, and none was found.",
    "Download Python",
    "Set Python path",
  );
  if (pick === "Download Python") vscode.env.openExternal(vscode.Uri.parse("https://www.python.org/downloads/"));
  if (pick === "Set Python path") vscode.commands.executeCommand("workbench.action.openSettings", "ayrport.pythonPath");
  return null;
}

// --- commands -------------------------------------------------------------

async function targetDocument(uri) {
  let doc;
  if (uri instanceof vscode.Uri) {
    doc = await vscode.workspace.openTextDocument(uri);
  } else {
    doc = vscode.window.activeTextEditor?.document;
  }
  if (!doc || doc.languageId !== "ayrport") {
    vscode.window.showWarningMessage("Open an .ayr file to run it.");
    return null;
  }
  if (doc.isUntitled) {
    const saved = await doc.save();
    if (!saved) return null;
    doc = vscode.window.activeTextEditor?.document || doc;
  } else if (doc.isDirty) {
    await doc.save();
  }
  return doc;
}

function newTerminal(name, args, cwd) {
  return vscode.window.createTerminal({
    name,
    shellPath: python.exe,
    shellArgs: [launcher, ...args],
    cwd,
    env: { PYTHONUTF8: "1", PYTHONIOENCODING: "utf-8" },
    iconPath: new vscode.ThemeIcon("rocket"),
  });
}

async function runFile(uri) {
  const doc = await targetDocument(uri);
  if (!doc || !(await findPython(doc.uri))) return;
  if (runTerminal) runTerminal.dispose();
  runTerminal = newTerminal(`Ayrport: ${path.basename(doc.fileName)}`, [doc.fileName], path.dirname(doc.fileName));
  runTerminal.show();
}

async function openTower() {
  if (!(await findPython())) return;
  const folder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  newTerminal("Ayrport tower", [], folder).show();
}

function runAyr(args, cwd) {
  return new Promise((resolve) => {
    cp.execFile(python.exe, [launcher, ...args], {
      cwd,
      windowsHide: true,
      env: { ...process.env, PYTHONUTF8: "1", PYTHONIOENCODING: "utf-8" },
    }, (err, stdout, stderr) => resolve({ err, stdout, stderr }));
  });
}

async function showPython(uri) {
  const doc = await targetDocument(uri);
  if (!doc || !(await findPython(doc.uri))) return;
  const { err, stdout, stderr } = await runAyr(["build", doc.fileName], path.dirname(doc.fileName));
  if (err) {
    vscode.window.showErrorMessage(`Ayrport build failed: ${stderr || err.message}`);
    return;
  }
  const py = await vscode.workspace.openTextDocument({ language: "python", content: stdout });
  vscode.window.showTextDocument(py, vscode.ViewColumn.Beside, true);
}

// --- red squiggles for syntax errors ---------------------------------------

async function checkDocument(doc) {
  if (doc.languageId !== "ayrport" || doc.isUntitled || !config().get("checkOnSave", true)) return;
  if (!(await findPython(doc.uri))) return;
  const { err, stderr } = await runAyr(["check", doc.fileName], path.dirname(doc.fileName));
  if (!err) {
    diagnostics.delete(doc.uri);
    return;
  }
  const m = /line (\d+)/.exec(stderr || "");
  const lines = (stderr || "").trim().split(/\r?\n/);
  const message = lines[lines.length - 1].trim() || "Flight plan rejected";
  const line = m ? Math.max(0, Math.min(doc.lineCount - 1, Number(m[1]) - 1)) : 0;
  const range = doc.lineAt(line).range;
  const d = new vscode.Diagnostic(range, `Flight plan rejected: ${message}`, vscode.DiagnosticSeverity.Error);
  d.source = "ayrport";
  diagnostics.set(doc.uri, [d]);
}

// --- activation -------------------------------------------------------------

function activate(context) {
  launcher = context.asAbsolutePath(path.join("python", "ayr_launch.py"));
  diagnostics = vscode.languages.createDiagnosticCollection("ayrport");
  const selector = { language: "ayrport" };

  const status = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  status.text = "$(play) Run Ayrport";
  status.tooltip = "Run this .ayr file (F5)";
  status.command = "ayrport.run";
  const updateStatus = () => {
    const ed = vscode.window.activeTextEditor;
    if (ed && ed.document.languageId === "ayrport") status.show();
    else status.hide();
  };
  updateStatus();

  context.subscriptions.push(
    diagnostics,
    status,
    vscode.window.onDidChangeActiveTextEditor(updateStatus),
    vscode.workspace.onDidSaveTextDocument(checkDocument),
    vscode.workspace.onDidOpenTextDocument(checkDocument),
    vscode.workspace.onDidCloseTextDocument((d) => diagnostics.delete(d.uri)),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("ayrport.pythonPath")) python = null;
    }),
    vscode.window.onDidCloseTerminal((t) => {
      if (t === runTerminal) runTerminal = null;
    }),
    vscode.languages.registerHoverProvider(selector, {
      provideHover(doc, pos) {
        const range = doc.getWordRangeAtPosition(pos, /[A-Za-z_]\w*/);
        if (!range) return;
        const word = doc.getText(range);
        const meaning = WORDS[word];
        if (!meaning) return;
        return new vscode.Hover(new vscode.MarkdownString(`**${word}** — ${meaning}`), range);
      },
    }),
    vscode.languages.registerCompletionItemProvider(selector, {
      provideCompletionItems() {
        return Object.entries(WORDS).map(([word, meaning]) => {
          const item = new vscode.CompletionItem(word, vscode.CompletionItemKind.Keyword);
          item.detail = meaning;
          return item;
        });
      },
    }),
    vscode.commands.registerCommand("ayrport.run", runFile),
    vscode.commands.registerCommand("ayrport.showPython", showPython),
    vscode.commands.registerCommand("ayrport.tower", openTower),
  );

  vscode.workspace.textDocuments.forEach(checkDocument);
}

function deactivate() {}

module.exports = { activate, deactivate };
