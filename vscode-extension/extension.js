// Ayrport for VS Code: run files, view the compiled Python, hover meanings, completions.
const vscode = require("vscode");
const cp = require("child_process");
const path = require("path");
const WORDS = require("./words.json");

function command() {
  return vscode.workspace.getConfiguration("ayrport").get("command", "ayr");
}

function terminal() {
  const existing = vscode.window.terminals.find((t) => t.name === "Ayrport");
  return existing || vscode.window.createTerminal("Ayrport");
}

function quote(p) {
  return /\s/.test(p) ? `"${p}"` : p;
}

async function activeAyrDocument() {
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.languageId !== "ayrport") {
    vscode.window.showWarningMessage("Open an .ayr file first.");
    return null;
  }
  if (editor.document.isDirty) await editor.document.save();
  return editor.document;
}

async function runFile() {
  const doc = await activeAyrDocument();
  if (!doc) return;
  const term = terminal();
  term.show(true);
  term.sendText(`${command()} ${quote(doc.fileName)}`);
}

async function showPython() {
  const doc = await activeAyrDocument();
  if (!doc) return;
  cp.exec(`${command()} build ${quote(doc.fileName)}`,
    { cwd: path.dirname(doc.fileName) },
    async (err, stdout, stderr) => {
      if (err) {
        vscode.window.showErrorMessage(`Ayrport build failed: ${stderr || err.message}`);
        return;
      }
      const py = await vscode.workspace.openTextDocument({ language: "python", content: stdout });
      vscode.window.showTextDocument(py, vscode.ViewColumn.Beside, true);
    });
}

function openTower() {
  const term = terminal();
  term.show();
  term.sendText(command());
}

function activate(context) {
  const selector = { language: "ayrport" };

  const hover = vscode.languages.registerHoverProvider(selector, {
    provideHover(doc, pos) {
      const range = doc.getWordRangeAtPosition(pos, /[A-Za-z_]\w*/);
      if (!range) return;
      const word = doc.getText(range);
      const meaning = WORDS[word];
      if (!meaning) return;
      const md = new vscode.MarkdownString(`**${word}** — ${meaning}`);
      return new vscode.Hover(md, range);
    },
  });

  const completion = vscode.languages.registerCompletionItemProvider(selector, {
    provideCompletionItems() {
      return Object.entries(WORDS).map(([word, meaning]) => {
        const item = new vscode.CompletionItem(word, vscode.CompletionItemKind.Keyword);
        item.detail = meaning;
        return item;
      });
    },
  });

  context.subscriptions.push(
    hover,
    completion,
    vscode.commands.registerCommand("ayrport.run", runFile),
    vscode.commands.registerCommand("ayrport.showPython", showPython),
    vscode.commands.registerCommand("ayrport.tower", openTower),
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
