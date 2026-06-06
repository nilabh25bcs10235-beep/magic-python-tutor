import json

# Vercel Python entrypoint
# This file exists to satisfy "No python entrypoint found".
# The primary user-facing experience for web is the static mobile.html PWA.
# Root URL + all routes are rewritten to mobile.html via vercel.json.

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
            "message": "Python entrypoint is present. The colorful desktop app is distributed via pip. The mobile PWA is served statically at the root.",
            "desktop_install": "pip install git+https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git && magic-tutor",
            "lessons_available": ["append", "pop", "dict", "split", "and more in the PWA"]
        }, indent=2)
    }
