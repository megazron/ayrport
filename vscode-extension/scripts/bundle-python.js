// Copies the Ayrport Python package into the extension so it runs without a pip install.
const fs = require("fs");
const path = require("path");

const src = path.join(__dirname, "..", "..", "src", "ayrport");
const dest = path.join(__dirname, "..", "python", "ayrport");

fs.rmSync(dest, { recursive: true, force: true });
fs.mkdirSync(dest, { recursive: true });
for (const name of fs.readdirSync(src)) {
  if (/\.(py|html)$/.test(name)) fs.copyFileSync(path.join(src, name), path.join(dest, name));
}
console.log(`bundled ayrport into ${path.relative(process.cwd(), dest)}`);
