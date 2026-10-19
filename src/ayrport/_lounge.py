"""The lounge."""

from __future__ import annotations

import http.server
import os
import platform
import subprocess
import sys
import threading
import urllib.request
import webbrowser
from importlib import resources

PORT = 47474


def _page() -> bytes:
    return resources.files("ayrport").joinpath("lounge.html").read_bytes()


class _Handler(http.server.BaseHTTPRequestHandler):
    page = b""

    def do_GET(self):  # noqa: N802
        if self.path.startswith("/ping"):
            body, kind = b"ayrport-lounge", "text/plain"
        else:
            body, kind = self.page, "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def _is_ours(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/ping", timeout=1) as r:
            return r.read() == b"ayrport-lounge"
    except OSError:
        return False


def _open(url: str) -> None:
    if os.environ.get("AYRPORT_NO_BROWSER"):
        return
    if "microsoft" in platform.uname().release.lower():  # WSL: use the Windows browser
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", "", url], cwd="/mnt/c",
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except OSError:
            pass
    webbrowser.open(url)


def board() -> None:
    if sys.platform == "emscripten":  # running inside Ayrport Studio
        import ayrhost
        ayrhost.lounge()
        return
    _Handler.page = _page()
    server = None
    for port in range(PORT, PORT + 20):
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", port), _Handler)
            break
        except OSError:
            if _is_ours(port):
                _open(f"http://localhost:{port}/")
                print(f"  The lounge is already open: http://localhost:{port}/")
                return
    if server is None:
        print("  The lounge is full right now. Try again in a moment.")
        return
    url = f"http://localhost:{server.server_address[1]}/"
    print("  ✈  Now boarding the Ayrport lounge")
    print(f"     {url}")
    print("     (Ctrl+C to deplane)")
    threading.Timer(0.3, _open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Deplaned. See you on your next flight.")
    finally:
        server.server_close()
