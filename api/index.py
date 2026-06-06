import json
import os

# Vercel Python entrypoint (health/info only)
# This file exists to satisfy "No python entrypoint found".
#
# Real experiences:
# - Beautiful mobile PWA at "/" (mobile.html) - works fully offline
# - Fast local Python logic: GET /api/explain?q=your+question
# - Smart AI (Groq Llama 70B): GET /api/ask?q=your+question   <--- uses your Groq key
#
# IMPORTANT: You must set the environment variable GROQ_API_KEY in Vercel
# (Project Settings → Environment Variables) for the /api/ask AI feature to work.

def handler(event, context):
    """Basic serverless function handler."""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "name": "Magic Python Tutor",
            "ok": True,
            "message": "AI-powered tutor is live! Use /api/ask for Groq answers.",
            "endpoints": {
                "pwa": "/",
                "fast_heuristic": "/api/explain?q=...",
                "smart_ai_groq": "/api/ask?q=...",
                "smart_ai_groq_stream": "/api/ask?q=...&stream=true"
            },
            "desktop_install": "pip install git+https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git && magic-tutor",
            "ai_enabled": bool(os.environ.get("GROQ_API_KEY")),
            "note": "Set GROQ_API_KEY in Vercel → Environment Variables to enable the smart AI brain."
        }, indent=2)
    }
