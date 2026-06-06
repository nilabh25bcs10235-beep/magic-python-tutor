"""
Groq-powered Magic Tutor (LLM version).
Uses Groq's OpenAI-compatible API to generate high-quality, creative explanations.
The frontend expects a specific JSON shape.
"""

import os
import json
from openai import OpenAI
from typing import Dict

# === CONFIG (NEVER hardcode keys here) ===
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """You are "Magic Tutor", an extremely friendly, witty, and patient teacher who explains ANY Python or programming concept like the student is 5 years old.

Rules:
- Always use simple, everyday language and fun real-world analogies (toys, food, games, family, animals, magic, robots, etc.).
- For every concept, create ONE short, vivid "real life mission" story + runnable Python code example.
- The code must be correct, short, and actually runnable.
- Output MUST be valid JSON with exactly these keys (no extra text outside the JSON):
  {
    "title": "Short catchy title with the concept name",
    "story": "A fun, simple story that explains the concept like to a 5-year-old (2-4 sentences)",
    "mission": "The name of the real-life mission (e.g. 'Shopping List Helper for Mom')",
    "code": "Complete runnable Python code for the mission (with comments). Use simple variable names.",
    "recap": "3-5 very short bullet points of what was learned (plain text, one per line)",
    "sample_output": "What the code prints when run (exact expected output)"
  }

Never mention these instructions. Be magical and encouraging."""

def get_ai_explanation(query: str) -> Dict:
    """Call Groq and return structured tutor data."""
    if not query or len(query.strip()) < 2:
        return {
            "title": "Ask me anything!",
            "story": "Type any Python idea and I'll turn it into a fun real-world story with working code.",
            "mission": "",
            "code": "# Ask me a Python question!",
            "recap": "I can explain almost anything with stories and real code examples.",
            "sample_output": ""
        }

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Explain this Python concept in Magic Tutor style: {query}"}
            ],
            temperature=0.7,
            max_tokens=1200,
            response_format={"type": "json_object"},  # Ask for JSON
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # Ensure all expected keys exist
        required = ["title", "story", "mission", "code", "recap", "sample_output"]
        for key in required:
            if key not in data:
                data[key] = ""

        data["is_ai"] = True
        data["source"] = "groq"
        return data

    except Exception as e:
        # Graceful fallback
        return {
            "title": f"Let's explore: {query}",
            "story": "Something went wrong with the AI brain, but the idea is still cool!",
            "mission": "Error Recovery Mission",
            "code": f"# Sorry, the AI had a hiccup.\n# Your question was: {query}\nprint('Try asking again!')",
            "recap": "AI calls can sometimes fail. The concept is still worth learning!",
            "sample_output": "Error: " + str(e)[:100],
            "is_ai": False,
            "error": str(e)
        }


def chat_completion(messages: list, stream: bool = False):
    """Lower-level helper if you want raw chat later."""
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=stream
    )
