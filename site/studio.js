// Ayrport Studio: editor, runner, examples and Flight School.
"use strict";

const $ = (s) => document.querySelector(s);
const store = {
  get(k, d) { try { const v = localStorage.getItem("ayr." + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("ayr." + k, JSON.stringify(v)); } catch { /* private mode */ } },
};

const DEFAULT_CODE = `# Welcome to Ayrport Studio!  Press ▶ Take off to run this.

pa "Welcome to Ayrport ✈"

counter boarding_call(flight, gate_no):
    issue f"Flight {flight} is now boarding at gate {gate_no}"

belt flight, gate_no in [("AY101", "A3"), ("AY204", "B12")]:
    pa boarding_call(flight, gate_no)
`;

// ---------------------------------------------------------------- words

const WORDS = {
  control: ["check", "alt", "div", "belt", "shuttle", "leave", "skip", "issue", "drop", "screen", "flagged", "customs", "flag",
            "if", "elif", "else", "while", "for", "break", "continue", "return", "yield", "try", "except", "finally", "raise", "in", "and", "or", "not", "is", "as", "from"],
  other: ["gate", "xray", "standby", "load", "with", "assert", "pass", "import", "global", "del"],
  def: ["counter", "terminal", "kiosk", "def", "class", "lambda"],
  consts: ["go", "nogo", "nil", "True", "False", "None"],
  builtins: ["pa", "checkin", "rwy", "wait", "print", "input", "range", "len", "str", "int", "float", "list", "dict", "round", "sorted", "sum", "min", "max", "abs", "enumerate", "zip", "open", "super", "isinstance"],
};
const KIND = {};
for (const w of WORDS.control) KIND[w] = "t-kw";
for (const w of WORDS.other) KIND[w] = "t-kw";
for (const w of WORDS.def) KIND[w] = "t-def";
for (const w of WORDS.consts) KIND[w] = "t-const";
for (const w of WORDS.builtins) KIND[w] = "t-bi";
KIND.me = "t-me"; KIND.self = "t-me"; KIND.arrive = "t-fn";

const SNIPPETS = [
  ["pa", 'pa "Now boarding"'],
  ["checkin", 'name = checkin("Your name? ")'],
  ["check", 'check bags > 2:\n    pa "excess baggage"\ndiv:\n    pa "all good"'],
  ["belt", "belt bag in bags:\n    pa bag"],
  ["rwy", "belt number in rwy(1, 6):\n    pa \"Gate\", number"],
  ["shuttle", "shuttle seconds > 0:\n    pa seconds\n    seconds = seconds - 1"],
  ["counter", "counter greet(name):\n    issue \"Welcome, \" + name"],
  ["issue", "issue result"],
  ["terminal", "terminal Flight:\n    counter arrive(me, code):\n        me.code = code\n\n    counter call(me):\n        issue \"Now boarding \" + me.code"],
  ["screen", "screen:\n    pa 10 / 0\nflagged ZeroDivisionError as e:\n    pa \"flagged:\", e"],
  ["flag", 'flag ValueError("something is wrong")'],
  ["gate", 'gate open("notes.txt", "w") as f:\n    f.write("hello")'],
  ["kiosk", "double = kiosk x: x * 2"],
  ["load", "load random"],
  ["wait", "wait(1)"],
  ["leave", "leave"],
  ["skip", "skip"],
];

// ---------------------------------------------------------------- lessons

const LESSONS = [
  {
    title: "Your first announcement",
    story: "Every airport has a public announcement system. In Ayrport it's called <code>pa</code>. Whatever you put after <code>pa</code> gets announced in the output on the right.",
    mission: "Change the announcement so it says <b>Now boarding</b>, then press ▶ Take off.",
    starter: 'pa "Hello, traveller!"\n',
    hint: "Text goes inside quotes: pa \"Now boarding\"",
    check: (out) => /now boarding/i.test(out),
  },
  {
    title: "Check-in",
    story: "<code>checkin</code> asks the passenger a question and waits for their answer. You can keep the answer in a name, like <code>name</code>, and use it later.",
    mission: "Run the program, type your name in the output box and press Enter. The program should <b>welcome</b> you.",
    starter: 'name = checkin("What is your name? ")\npa "Welcome aboard,", name\n',
    hint: "When the program asks, click the box in the output, type, and press Enter.",
    check: (out, code) => /checkin/.test(code) && /welcome/i.test(out),
  },
  {
    title: "Checks",
    story: "Airports are full of checks that send you one way or another. <code>check</code> means <i>if</i>. <code>alt</code> is another check, tried only if the first one failed. <code>div</code> (divert) is where everyone goes when no check passed.",
    mission: "Change the number of <code>bags</code> so the program announces the <b>excess baggage fee</b>.",
    starter: 'bags = 1\n\ncheck bags <= 1:\n    pa "Carry-on only, enjoy your flight"\nalt bags <= 3:\n    pa "Please drop your bags at the counter"\ndiv:\n    pa "That is an excess baggage fee!"\n',
    hint: "More than 3 bags goes to div. Try bags = 5",
    check: (out) => /excess baggage fee/i.test(out),
  },
  {
    title: "The baggage belt",
    story: "<code>belt</code> repeats something for every item, like bags going past on the baggage belt. <code>rwy(1, 4)</code> is a runway of numbers: 1, 2, 3 (it stops just before 4).",
    mission: "Open <b>gates 1 to 5</b>, so the last line says <b>Gate 5 is open</b>.",
    starter: 'belt number in rwy(1, 4):\n    pa "Gate", number, "is open"\n',
    hint: "rwy stops just before the second number. To reach 5, use rwy(1, 6).",
    check: (out) => /gate 5 is open/i.test(out) && /gate 1 is open/i.test(out) && !/gate 6 is open/i.test(out),
  },
  {
    title: "The shuttle",
    story: "A <code>shuttle</code> keeps looping round while something is true. Here it counts down while <code>seconds</code> is above zero. Careful: if the number never changes, the shuttle never stops (press ■ Stop if that happens).",
    mission: "Count down from <b>10</b>, then announce <b>Liftoff!</b>",
    starter: 'seconds = 3\n\nshuttle seconds > 0:\n    pa seconds\n    seconds = seconds - 1\n\npa "Doors closing"\n',
    hint: "Start with seconds = 10 and change the last line to pa \"Liftoff!\"",
    check: (out) => out.trim().split("\n")[0].trim() === "10" && /liftoff/i.test(out),
  },
  {
    title: "Open a counter",
    story: "A <code>counter</code> does one job: you hand it some details and it <code>issue</code>s something back. Make a counter once, use it as often as you like.",
    mission: "Make a counter <code>bag_fee(kg)</code> that issues <code>(kg - 23) * 12.5</code>, then announce the fee for a <b>30 kg</b> bag.",
    starter: 'counter welcome(name):\n    issue "Welcome aboard, " + name\n\npa welcome("Ana")\n',
    hint: "counter bag_fee(kg):\n    issue (kg - 23) * 12.5\n\npa bag_fee(30)",
    check: (out) => /87\.5/.test(out),
  },
  {
    title: "Passenger lists",
    story: "A list keeps many things in order: <code>[\"Ana\", \"Ben\"]</code>. <code>.append(...)</code> adds one more, <code>len(...)</code> counts them, and <code>belt</code> visits each one.",
    mission: "Add more passengers until the program announces <b>5 passengers on board</b>.",
    starter: 'passengers = ["Ana", "Ben"]\npassengers.append("Cy")\n\npa len(passengers), "passengers on board"\nbelt name in passengers:\n    pa "Welcome,", name\n',
    hint: 'Add two more lines like passengers.append("Your name")',
    check: (out) => /\b5 passengers on board/i.test(out),
  },
  {
    title: "Terminals",
    story: "A <code>terminal</code> groups counters and data together (other languages call this a class). <code>arrive</code> runs whenever a new one is made, and <code>me</code> means \"this one\".",
    mission: "Make a flight <b>AY101</b> to <b>Tokyo</b> and announce its boarding call.",
    starter: 'terminal Flight:\n    counter arrive(me, code, destination):\n        me.code = code\n        me.destination = destination\n\n    counter call(me):\n        issue f"Flight {me.code} to {me.destination} is now boarding"\n\nflight = Flight("AY000", "Nowhere")\npa flight.call()\n',
    hint: 'Change the line to flight = Flight("AY101", "Tokyo")',
    check: (out) => /AY101/.test(out) && /tokyo/i.test(out),
  },
  {
    title: "Security",
    story: "Code that might go wrong goes through <code>screen</code>ing. If a problem is flagged, the <code>flagged</code> block deals with it instead of the program crashing.",
    mission: "Run it once to see the answer get flagged. Then change <code>answer</code> to a number so it <b>passes security</b>.",
    starter: 'answer = "seven"\n\nscreen:\n    bags = int(answer)\n    pa "You have", bags, "bags. Passed security!"\nflagged ValueError:\n    pa "Flagged! That is not a number"\n',
    hint: 'Numbers do not need words: answer = "7"',
    check: (out) => /passed security/i.test(out),
  },
  {
    title: "Captain's exam",
    story: "Time to fly solo. Write your own program — anything you like: a departures board, a quiz, a fee calculator.",
    mission: "Use a <code>counter</code>, a <code>belt</code> and a <code>check</code> in one program that runs without a mayday.",
    starter: "# Your own flight. Use counter, belt and check.\n\n",
    hint: "Peek at the Examples menu for ideas.",
    check: (out, code) => /\bcounter\b/.test(code) && /\bbelt\b/.test(code) && /\bcheck\b/.test(code),
  },
];

// ---------------------------------------------------------------- editor

const ta = $("#code"), hl = $("#hl"), gutter = $("#gutter"), errline = $("#errline");
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const TOKEN = /(#[^\n]*)|((?:\b[rRbBuUfF]{1,2})?(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?))|(\b\d[\d_]*(?:\.\d*)?(?:[eE][+-]?\d+)?\b)|([A-Za-z_]\w*)|([^#'"A-Za-z_\d]+|[\s\S])/g;

function highlight(src) {
  let html = "", prev = "", m;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(src))) {
    const [t, com, str, num, word] = m;
    if (com) html += `<span class="t-com">${esc(t)}</span>`;
    else if (str) html += `<span class="t-str">${esc(t)}</span>`;
    else if (num) html += `<span class="t-num">${t}</span>`;
    else if (word) {
      const cls = (prev === "counter" || prev === "def" || prev === "terminal" || prev === "class") ? "t-fn" : KIND[word];
      html += cls ? `<span class="${cls}">${t}</span>` : t;
      prev = word;
    } else html += esc(t);
  }
  return html;
}

function render() {
  const src = ta.value;
  hl.innerHTML = highlight(src) + "\n ";
  const lines = src.split("\n").length;
  let g = "";
  for (let i = 1; i <= lines; i++) g += i + "\n";
  gutter.textContent = g;
  sync();
}
function sync() {
  hl.parentElement.scrollTop = ta.scrollTop;
  hl.parentElement.scrollLeft = ta.scrollLeft;
  gutter.scrollTop = ta.scrollTop;
  if (!errline.hidden) errline.style.transform = `translateY(${-ta.scrollTop}px)`;
}
function markError(line) {
  if (!line) { errline.hidden = true; return; }
  errline.hidden = false;
  errline.style.top = `${14 + (line - 1) * 22}px`;
  sync();
}
function setCode(src) {
  ta.value = src;
  markError(0);
  render();
  store.set("code", src);
}

function insertAtCursor(text) {
  const start = ta.selectionStart, end = ta.selectionEnd;
  const before = ta.value.slice(0, start);
  const lineStart = before.lastIndexOf("\n") + 1;
  const indent = before.slice(lineStart).match(/^\s*/)[0];
  const atLineStart = before.slice(lineStart).trim() === "";
  let chunk = text.split("\n").map((l, i) => (i ? indent + l : l)).join("\n");
  if (!atLineStart) chunk = "\n" + indent + chunk;
  ta.focus();
  ta.setRangeText(chunk + "\n" + indent, start, end, "end");
  onEdit();
}

function onEdit() {
  markError(0);
  render();
  store.set("code", ta.value);
}

ta.addEventListener("input", onEdit);
ta.addEventListener("scroll", sync);
ta.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); run(); return; }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); save(); return; }
  const start = ta.selectionStart, end = ta.selectionEnd, v = ta.value;
  if (e.key === "Tab") {
    e.preventDefault();
    const ls = v.lastIndexOf("\n", start - 1) + 1;
    if (e.shiftKey) {
      const m = v.slice(ls).match(/^ {1,4}/);
      if (m) { ta.setRangeText("", ls, ls + m[0].length, "preserve"); ta.selectionStart = ta.selectionEnd = Math.max(ls, start - m[0].length); }
    } else if (start !== end && v.slice(start, end).includes("\n")) {
      const block = v.slice(ls, end).replace(/^/gm, "    ");
      ta.setRangeText(block, ls, end, "select");
    } else {
      ta.setRangeText("    ", start, end, "end");
    }
    onEdit();
  } else if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const ls = v.lastIndexOf("\n", start - 1) + 1;
    const line = v.slice(ls, start);
    let indent = line.match(/^\s*/)[0];
    if (/:\s*(#.*)?$/.test(line)) indent += "    ";
    else if (/^\s*(issue|leave|skip|standby|flag|return|break|continue|pass|raise)\b/.test(line)) indent = indent.slice(4);
    ta.setRangeText("\n" + indent, start, end, "end");
    onEdit();
  } else if (e.key === "Backspace" && start === end) {
    const ls = v.lastIndexOf("\n", start - 1) + 1;
    const before = v.slice(ls, start);
    if (before.length && /^ +$/.test(before) && before.length % 4 === 0) {
      e.preventDefault();
      ta.setRangeText("", start - 4, start, "end");
      onEdit();
    }
  }
});

// ---------------------------------------------------------------- console

const out = $("#out");
let outputText = "";
function print(text, cls) {
  const empty = out.querySelector(".empty");
  if (empty) empty.remove();
  const span = document.createElement("span");
  if (cls) span.className = cls;
  span.textContent = text;
  out.appendChild(span);
  if (!cls || cls === "echo") outputText += text;
  out.scrollTop = out.scrollHeight;
}
function clearOutput() {
  out.innerHTML = "";
  outputText = "";
}
$("#clearBtn").onclick = () => { clearOutput(); out.innerHTML = '<div class="empty">Output cleared.</div>'; };

// ---------------------------------------------------------------- status, sound, toast

const statusEl = $("#status");
function status(text, kind = "") {
  statusEl.textContent = text;
  statusEl.className = "status " + kind;
}
let soundOn = store.get("sound", true);
let audio;
function chime(notes = [659.25, 523.25]) {
  if (!soundOn) return;
  try {
    audio = audio || new AudioContext();
    const t0 = audio.currentTime + 0.02;
    notes.forEach((f, i) => {
      const o = audio.createOscillator(), o2 = audio.createOscillator(), g = audio.createGain();
      o.frequency.value = f; o2.frequency.value = f * 2.76; o2.type = "sine";
      const g2 = audio.createGain(); g2.gain.value = 0.15;
      o.connect(g); o2.connect(g2); g2.connect(g); g.connect(audio.destination);
      const t = t0 + i * 0.32;
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(0.18, t + 0.01);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 1.4);
      o.start(t); o2.start(t); o.stop(t + 1.5); o2.stop(t + 1.5);
    });
  } catch { /* no audio */ }
}
function toast(text) {
  const t = $("#toast");
  t.textContent = text;
  t.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.remove("show"), 2600);
}

// ---------------------------------------------------------------- runner

let worker = null, ready = false, running = false, pendingRun = false;
let controlled = Promise.resolve(false);

if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  controlled = navigator.serviceWorker.register("sw.js").then(() => {
    if (navigator.serviceWorker.controller) return true;
    return new Promise((resolve) => {
      navigator.serviceWorker.addEventListener("controllerchange", () => resolve(true), { once: true });
      setTimeout(() => resolve(!!navigator.serviceWorker.controller), 4000);
    });
  }).catch(() => false);
}

function startWorker() {
  ready = false;
  status("Boarding Python…", "busy");
  worker = new Worker("worker.js");
  worker.onmessage = (e) => handle(e.data);
  worker.onerror = (e) => { status("Python failed to load", "bad"); print(`Could not start Python: ${e.message}\n`, "err"); };
}

function handle(msg) {
  switch (msg.type) {
    case "ready":
      ready = true;
      status("Ready for takeoff", "ok");
      if (pendingRun) { pendingRun = false; run(); }
      break;
    case "fatal":
      status("Python failed to load", "bad");
      print("Python could not load. Check your internet connection and reload the page.\n" + msg.text + "\n", "err");
      break;
    case "out": print(msg.text); break;
    case "err": print(msg.text, "err"); break;
    case "input": ask(msg.id, msg.prompt); break;
    case "lounge": openLounge(); break;
    case "done": finish(msg.ok, msg.line); break;
  }
}

function setRunning(on) {
  running = on;
  $("#runBtn").disabled = on;
  $("#stopBtn").disabled = !on;
}

function run() {
  if (running) return;
  if (!ready) { pendingRun = true; status("Boarding Python… your program will run in a moment", "busy"); return; }
  clearOutput();
  markError(0);
  setRunning(true);
  status("In flight…", "busy");
  worker.postMessage({ type: "run", code: ta.value });
}

function finish(ok, line) {
  setRunning(false);
  out.querySelectorAll(".ask").forEach((a) => a.remove());
  if (ok) {
    status("Landed ✓", "ok");
    if (!outputText.trim()) print("(The program ran but announced nothing. Use pa to announce something.)\n", "sys");
    chime([783.99, 659.25]);
  } else {
    status(line ? `Mayday on line ${line}` : "Mayday", "bad");
    markError(line);
  }
  checkLesson();
}

function stop() {
  if (!running) return;
  worker.terminate();
  print("\n■ Flight stopped.\n", "sys");
  setRunning(false);
  startWorker();
}

function ask(id, prompt) {
  status("Waiting for check-in…", "busy");
  const row = document.createElement("div");
  row.className = "ask";
  const label = document.createElement("span");
  label.textContent = prompt;
  const input = document.createElement("input");
  input.placeholder = "type here and press Enter";
  row.append(label, input);
  const empty = out.querySelector(".empty");
  if (empty) empty.remove();
  out.appendChild(row);
  input.focus();
  out.scrollTop = out.scrollHeight;
  input.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    const value = input.value;
    row.remove();
    print(prompt);
    print(value + "\n", "echo");
    status("In flight…", "busy");
    const sw = navigator.serviceWorker && navigator.serviceWorker.controller;
    if (sw) sw.postMessage({ id, value });
  });
  if (!(navigator.serviceWorker && navigator.serviceWorker.controller)) {
    print("Typing answers needs a normal browser window (it is blocked here). Reload the page and try again.\n", "err");
  }
}

$("#runBtn").onclick = run;
$("#stopBtn").onclick = stop;

// ---------------------------------------------------------------- lounge

function openLounge() {
  const box = $("#lounge");
  box.querySelector("iframe").src = "lounge.html";
  box.hidden = false;
}
$("#loungeClose").onclick = () => {
  const box = $("#lounge");
  box.hidden = true;
  box.querySelector("iframe").src = "about:blank";
};

// ---------------------------------------------------------------- files

function save() {
  const first = ta.value.split("\n").find((l) => l.trim().startsWith("#"));
  const name = (store.get("filename", null) || "my_flight.ayr");
  const blob = new Blob([ta.value], { type: "text/plain" });
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: name });
  a.click();
  URL.revokeObjectURL(a.href);
  toast(`Saved ${name}`);
  return first;
}
$("#saveBtn").onclick = save;
$("#openBtn").onclick = () => $("#fileInput").click();
$("#fileInput").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  setCode(await file.text());
  store.set("filename", file.name.endsWith(".ayr") ? file.name : file.name + ".ayr");
  toast(`Opened ${file.name}`);
  e.target.value = "";
};
$("#newBtn").onclick = () => {
  if (ta.value.trim() && !confirm("Start a new program? Your current one will be replaced (Save it first if you want to keep it).")) return;
  setCode('pa "Hello from Ayrport!"\n');
  store.set("filename", "my_flight.ayr");
  clearOutput();
};

function encode(s) { return btoa(String.fromCharCode(...new TextEncoder().encode(s))); }
function decode(s) { return new TextDecoder().decode(Uint8Array.from(atob(s), (c) => c.charCodeAt(0))); }
$("#shareBtn").onclick = async () => {
  const url = `${location.origin}${location.pathname}#code=${encodeURIComponent(encode(ta.value))}`;
  try { await navigator.clipboard.writeText(url); toast("Link copied — anyone who opens it sees your program"); }
  catch { prompt("Copy this link:", url); }
};

// ---------------------------------------------------------------- examples

let bundle = null;
function prettyName(path) {
  return path.replace(/\.ayr$/, "").replace(/[_/]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
async function loadBundle() {
  bundle = await (await fetch("bundle.json", { cache: "no-cache" })).json();
  const sel = $("#examples");
  const order = ["hello", "basics", "departures_board", "check_in_desk", "baggage_claim", "security_line", "boarding_queue", "seat_map", "route_planner", "delay_stats", "airline_fleet", "fleet", "lost_and_found", "files", "fizzbuzz", "countdown_to_takeoff", "use_package"];
  const names = Object.keys(bundle.examples).filter((p) => !p.includes("/") && p !== "flightdeck.ayr");
  names.sort((a, b) => (order.indexOf(a.slice(0, -4)) + 1 || 99) - (order.indexOf(b.slice(0, -4)) + 1 || 99));
  for (const p of names) sel.add(new Option(prettyName(p), p));
  const meanings = bundle.meanings || {};
  const chips = $("#chips");
  for (const [word, text] of SNIPPETS) {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = word;
    b.title = meanings[word] ? `${word} — ${meanings[word].split(" — ").pop()} (click to insert)` : "click to insert";
    b.onclick = () => insertAtCursor(text);
    chips.appendChild(b);
  }
}
$("#examples").onchange = (e) => {
  const p = e.target.value;
  e.target.value = "";
  if (!p || !bundle) return;
  if (ta.value.trim() && ta.value !== DEFAULT_CODE && !confirm("Open this example? It replaces the program you have now.")) return;
  setCode(bundle.examples[p]);
  store.set("filename", p);
  clearOutput();
  print(`Opened example "${prettyName(p)}". Press ▶ Take off to run it.\n`, "sys");
};

// ---------------------------------------------------------------- flight school

let lessonIndex = store.get("lesson", 0);
let done = new Set(store.get("stamps", []));

function renderStamps() {
  const box = $("#stamps");
  box.innerHTML = "";
  LESSONS.forEach((l, i) => {
    const b = document.createElement("button");
    b.className = "stamp" + (done.has(i) ? " done" : "") + (i === lessonIndex ? " here" : "");
    b.textContent = done.has(i) ? "✓" : i + 1;
    b.title = l.title;
    b.onclick = () => showLesson(i, true);
    box.appendChild(b);
  });
}

function showLesson(i, loadStarter) {
  lessonIndex = Math.max(0, Math.min(LESSONS.length - 1, i));
  store.set("lesson", lessonIndex);
  const l = LESSONS[lessonIndex];
  $("#lesson").innerHTML = `
    <div class="kicker">Lesson ${lessonIndex + 1} of ${LESSONS.length}${done.has(lessonIndex) ? " · stamped ✓" : ""}</div>
    <h3>${l.title}</h3>
    <p>${l.story}</p>
    <div class="mission"><b>Mission:</b> ${l.mission}</div>
    <div class="row">
      <button class="btn" id="starterBtn">↺ Reset code</button>
      <button class="btn" id="hintBtn">💡 Hint</button>
    </div>
    <div class="hint" id="hintText" hidden></div>
    <div id="lessonResult"></div>
    <div class="row">
      <button class="btn" id="prevBtn" ${lessonIndex === 0 ? "disabled" : ""}>← Back</button>
      <button class="btn" id="nextBtn" ${lessonIndex === LESSONS.length - 1 ? "disabled" : ""}>Next lesson →</button>
    </div>`;
  $("#starterBtn").onclick = () => { setCode(l.starter); clearOutput(); };
  $("#hintBtn").onclick = () => { const h = $("#hintText"); h.hidden = !h.hidden; h.textContent = l.hint; };
  $("#prevBtn").onclick = () => showLesson(lessonIndex - 1, true);
  $("#nextBtn").onclick = () => showLesson(lessonIndex + 1, true);
  if (loadStarter) { setCode(l.starter); clearOutput(); }
  renderStamps();
}

function checkLesson() {
  if ($("#school").hidden) return;
  const l = LESSONS[lessonIndex];
  const result = $("#lessonResult");
  if (!result) return;
  const failed = statusEl.classList.contains("bad");
  if (!failed && l.check(outputText, ta.value)) {
    const first = !done.has(lessonIndex);
    done.add(lessonIndex);
    store.set("stamps", [...done]);
    result.innerHTML = `<div class="result win">✓ Mission complete! ${first ? "Passport stamped." : ""}</div>`;
    renderStamps();
    if (first) bigStamp(lessonIndex === LESSONS.length - 1 ? "CAPTAIN<br>WINGS" : `LESSON ${lessonIndex + 1}<br>CLEARED`);
    if (done.size === LESSONS.length && first) toast("All 10 stamps! You are an Ayrport captain ✈");
  } else {
    result.innerHTML = `<div class="result try">${failed ? "Mayday — fix the red line and try again." : "Not quite yet. Check the mission and try again."}</div>`;
  }
}

function bigStamp(text) {
  chime([523.25, 659.25, 783.99]);
  const s = document.createElement("div");
  s.className = "bigstamp";
  s.innerHTML = `<div>${text}</div>`;
  document.body.appendChild(s);
  setTimeout(() => s.remove(), 1900);
}

function toggleSchool(open) {
  const school = $("#school");
  school.hidden = open === undefined ? !school.hidden : !open;
  store.set("schoolOpen", !school.hidden);
  if (!school.hidden) showLesson(lessonIndex, false);
}
$("#schoolBtn").onclick = () => {
  const opening = $("#school").hidden;
  toggleSchool();
  if (opening && !LESSONS.some((l) => l.starter === ta.value)) {
    if (!ta.value.trim() || ta.value === DEFAULT_CODE || confirm("Load the code for this lesson? It replaces your current program.")) {
      setCode(LESSONS[lessonIndex].starter);
    }
  }
};

// ---------------------------------------------------------------- theme & welcome

function applyTheme(t) {
  if (t) document.documentElement.dataset.theme = t;
  else delete document.documentElement.dataset.theme;
}
applyTheme(store.get("theme", null));
$("#themeBtn").onclick = () => {
  const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
  applyTheme(next);
  store.set("theme", next);
};
function renderSound() { $("#soundBtn").textContent = soundOn ? "🔔" : "🔕"; }
renderSound();
$("#soundBtn").onclick = () => { soundOn = !soundOn; store.set("sound", soundOn); renderSound(); if (soundOn) chime(); };

$("#startSchool").onclick = () => { $("#welcome").hidden = true; store.set("welcomed", true); toggleSchool(true); setCode(LESSONS[lessonIndex].starter); };
$("#justExplore").onclick = () => { $("#welcome").hidden = true; store.set("welcomed", true); ta.focus(); };

// ---------------------------------------------------------------- start

(function init() {
  const hash = new URLSearchParams(location.hash.slice(1));
  let code = store.get("code", DEFAULT_CODE);
  if (hash.get("code")) {
    try { code = decode(hash.get("code")); history.replaceState(null, "", location.pathname); } catch { /* bad link */ }
  }
  setCode(code);
  if (store.get("schoolOpen", false)) toggleSchool(true);
  if (!store.get("welcomed", false) && !hash.get("code")) $("#welcome").hidden = false;
  loadBundle().catch(() => print("Could not load the examples.\n", "err"));
  controlled.then(startWorker);
})();
