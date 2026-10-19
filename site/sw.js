// Lets the Python worker wait for typed input: the worker makes a blocking request,
// and this service worker answers it once the page sends the passenger's answer.
const waiting = new Map();

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

self.addEventListener("message", (e) => {
  const { id, value } = e.data || {};
  const reply = waiting.get(id);
  if (reply) {
    waiting.delete(id);
    reply(value);
  }
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (!url.pathname.endsWith("/__ayr_input__")) return;
  const id = url.searchParams.get("id");
  e.respondWith(new Promise((resolve) => {
    waiting.set(id, (value) => resolve(new Response(value, {
      headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" },
    })));
  }));
});
