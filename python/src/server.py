"""Local HTTP adapter. Import the agent/voice module in your own application."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from agent import run_agent


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        if self.headers.get("Origin") and self.headers[
            "Origin"
        ] != "http://" + self.headers.get("Host", ""):
            self.send_error(403)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 30000:
                self.send_error(413)
                return
            raw = self.rfile.read(length)
            text = json.loads(raw).get("text")
            if not isinstance(text, str) or not text.strip() or len(text) > 6000:
                raise ValueError("Enter 1–6000 characters")
            reply = run_agent(text)
            body = json.dumps({"reply": reply}).encode()
            self.send_response(200)
        except (ValueError, KeyError):
            body = b'{"error":"Invalid input"}'
            self.send_response(400)
        except Exception:
            body = (
                b'{"error":"Upstream request failed. Check key, access and credits."}'
            )
            self.send_response(502)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Listening on http://127.0.0.1:3000")
    HTTPServer(("127.0.0.1", int(os.getenv("PORT", "3000"))), Handler).serve_forever()
