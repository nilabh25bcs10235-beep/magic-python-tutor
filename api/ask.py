"""
Vercel serverless function: /api/ask
This is the SMART version that uses Groq LLM (via the key you provided).

Usage:
- GET  /api/ask?q=how%20do%20loops%20work
- POST /api/ask   with JSON {"query": "how do loops work"}

Returns the same shape as /api/explain so the mobile.html frontend works with almost no changes.
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# Import the Groq-powered tutor
from api.groq_tutor import get_ai_explanation


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in _cors_headers().items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        query = params.get("q", [""])[0] or params.get("query", [""])[0]
        self._respond(query)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            data = json.loads(body)
            query = data.get("query") or data.get("q") or ""
        except Exception:
            query = ""
        self._respond(query)

    def _respond(self, query: str):
        try:
            result = get_ai_explanation(query)

            self.send_response(200)
            for k, v in _cors_headers().items():
                self.send_header(k, v)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result, indent=2).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            for k, v in _cors_headers().items():
                self.send_header(k, v)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "AI tutor failed",
                "detail": str(e)
            }).encode("utf-8"))
