"""
Vercel serverless function: /api/explain
Call with ?q=your question or POST JSON {"query": "..."}
Returns structured explanation data for the web frontend.
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import our pure tutor logic (no terminal dependencies)
from api.tutor import get_explanation


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
        query = ""
        if "q" in params:
            query = params["q"][0]
        elif "query" in params:
            query = params["query"][0]

        self._handle_query(query)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            query = data.get("query", "") or data.get("q", "")
        except Exception:
            query = ""

        self._handle_query(query)

    def _handle_query(self, query: str):
        try:
            result = get_explanation(query)

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
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
