"""
Vercel serverless function: /api/ask
This is the SMART version that uses Groq LLM (via the key you provided).

Usage:
- GET  /api/ask?q=how%20do%20loops%20work
- GET  /api/ask?q=...&stream=true     → streams tokens (great for live typing)
- POST /api/ask   with JSON {"query": "..."}

Returns the same shape as /api/explain so the mobile.html frontend works with almost no changes.
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import both the non-streaming and streaming versions
from api.groq_tutor import get_ai_explanation, stream_ai_explanation


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
        stream = params.get("stream", ["false"])[0].lower() == "true"
        self._respond(query, stream=stream)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            data = json.loads(body)
            query = data.get("query") or data.get("q") or ""
            stream = str(data.get("stream", False)).lower() == "true"
        except Exception:
            query = ""
            stream = False
        self._respond(query, stream=stream)

    def _respond(self, query: str, stream: bool = False):
        if stream:
            self._respond_stream(query)
            return

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

    def _respond_stream(self, query: str):
        """Stream tokens from Groq directly to the client (SSE-like or raw chunks)."""
        try:
            self.send_response(200)
            for k, v in _cors_headers().items():
                self.send_header(k, v)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            for chunk in stream_ai_explanation(query):
                # Send as SSE data
                self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
                self.wfile.flush()

            # End signal
            self.wfile.write("data: [DONE]\n\n".encode("utf-8"))
            self.wfile.flush()

        except Exception as e:
            try:
                self.wfile.write(f"data: {json.dumps({'error': str(e)})}\n\n".encode("utf-8"))
            except:
                pass
