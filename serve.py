#!/usr/bin/env python3
"""Local server so the app can be installed on this computer and on phones on the same Wi‑Fi."""
from __future__ import annotations

import argparse
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".js": "text/javascript",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()

    def log_message(self, format, *args):
        print("[%s] %s" % (self.log_date_time_string(), format % args))


def lan_ip() -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return "127.0.0.1"


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve Card & Booklet Generator")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    ip = lan_ip()
    print("Card & Booklet Generator")
    print("  This computer:  http://127.0.0.1:%s" % args.port)
    print("  Phone (Wi-Fi):  http://%s:%s" % (ip, args.port))
    print("Open the page, then tap Install / Add to Home Screen.")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
