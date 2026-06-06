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

client = None
if GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

SYSTEM_PROMPT = """You are "Magic Tutor" — the most fun, patient, and magical Python teacher in the world. You explain ANY programming concept as if the student is a curious 5-year-old who loves stories, games, robots, food, and adventures.

Core rules you MUST follow every single time:
- Speak in warm, simple, exciting language. Use short sentences. Lots of wonder and "wow!".
- Always invent ONE delightful real-world "mission" (like helping mom, a lemonade stand, a robot helper, a video game, a magic pet, etc.).
- The mission must feel personal and actionable for a kid.
- Provide clean, correct, short, runnable Python code with helpful comments.
- The code should demonstrate the concept perfectly and be copy-paste runnable.
- End with a super clear, encouraging recap of 3-5 tiny learnings.
- Also provide the exact sample output the code would print.

OUTPUT FORMAT (CRITICAL):
You must reply with ONLY valid JSON. No markdown, no explanations outside the JSON.
The JSON must have exactly these keys:

{
  "title": "Catchy title including the concept (e.g. 'list.append() — Adding things to a list')",
  "story": "2-4 sentences of pure magic story that makes the concept feel obvious and fun, using a kid-friendly analogy.",
  "mission": "Short exciting name of the real-life mission (e.g. 'Shopping List Helper for Mom')",
  "code": "The full runnable Python code as a single string with \\n for newlines. Include comments.",
  "recap": "3-5 short bullet points, each on its own line, starting with a number or emoji. Very simple language.",
  "sample_output": "The exact text that would appear when you run the code (including any print statements)."
}

Few-shot examples for style:

User: append to a list
{
  "title": "list.append() — Adding things to a list",
  "story": "Imagine your mom says 'Go write down what we need from the store'. You have a blank piece of paper (an empty list). Every time you think of something, you write it at the bottom. That's append!",
  "mission": "Shopping List Helper for Mom",
  "code": "# Real Life Mission: Shopping List Helper for Mom\\nshopping_list = []\\nshopping_list.append('milk')\\nprint(shopping_list)",
  "recap": "1. [] makes an empty list\\n2. .append() adds something to the end\\n3. Lists remember order",
  "sample_output": "['milk']"
}

User: what is a function
{
  "title": "Functions — Reusable magic spells",
  "story": "You don't want to write the same spell over and over. A function is like a magic spell book. You write the spell once, name it, and then just say the name whenever you need it!",
  "mission": "Fireball Spell Book",
  "code": "def cast_fireball(target):\\n    print(f'Fireball hits the {target}!')\\n\\ncast_fireball('goblin')",
  "recap": "1. def creates a reusable spell\\n2. You can call it by name anytime\\n3. Functions save time and avoid mistakes",
  "sample_output": "Fireball hits the goblin!"
}

Be creative but always follow the exact JSON structure. Never break character. Make every answer delightful. If the user asks something advanced, still explain it simply and magically.

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

    if not client:
        return {
            "title": "AI brain is sleeping",
            "story": "The Groq AI isn't configured yet. Add the GROQ_API_KEY in your Vercel project settings to wake up the smart tutor.",
            "mission": "Setup Mission",
            "code": "# To enable AI answers:\\n# 1. Go to Vercel → Settings → Environment Variables\\n# 2. Add GROQ_API_KEY with your Groq key\\n# 3. Redeploy the project\\nprint('Then ask me anything again!')",
            "recap": "1. Fast local mode still works perfectly\\n2. Set the key for creative AI explanations\\n3. Toggle 'Use AI' off to use instant answers",
            "sample_output": "AI not configured",
            "is_ai": False,
            "ai_unavailable": True,
            "error": "GROQ_API_KEY not set"
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
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        required = ["title", "story", "mission", "code", "recap", "sample_output"]
        for key in required:
            if key not in data:
                data[key] = ""

        data["is_ai"] = True
        data["source"] = "groq"
        return data

    except Exception as e:
        return {
            "title": f"Let's explore: {query}",
            "story": "The AI brain had a temporary hiccup. The fast local mode still works great!",
            "mission": "Error Recovery Mission",
            "code": f"# Sorry, the AI had a hiccup.\\n# Your question was: {query}\\nprint('Try asking again or use the lesson buttons!')",
            "recap": "1. AI calls can fail sometimes\\n2. The fast local tutor is always available\\n3. The concept is still worth learning!",
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


def stream_ai_explanation(query: str):
    """
    Streaming version. Yields chunks of text as they arrive from Groq.
    The caller is responsible for assembling and (optionally) parsing JSON.
    This enables real-time "typing" effect in the UI.
    """
    if not query or len(query.strip()) < 2:
        yield json.dumps({
            "title": "Ask me anything!",
            "story": "Type any Python idea and I'll turn it into a fun real-world story with working code.",
            "mission": "",
            "code": "# Ask me a Python question!",
            "recap": "I can explain almost anything with stories and real code examples.",
            "sample_output": ""
        })
        return

    if not client:
        yield json.dumps({
            "title": "AI brain is sleeping",
            "story": "The Groq AI isn't configured yet. Add the GROQ_API_KEY in your Vercel project settings to wake up the smart tutor.",
            "mission": "Setup Mission",
            "code": "# To enable AI answers:\\n# 1. Go to Vercel → Settings → Environment Variables\\n# 2. Add GROQ_API_KEY with your Groq key\\n# 3. Redeploy the project\\nprint('Then ask me anything again!')",
            "recap": "1. Fast local mode still works perfectly\\n2. Set the key for creative AI explanations\\n3. Toggle 'Use AI' off to use instant answers",
            "sample_output": "AI not configured",
            "is_ai": False,
            "ai_unavailable": True,
            "error": "GROQ_API_KEY not set"
        })
        return

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Explain this Python concept in Magic Tutor style: {query}"}
            ],
            temperature=0.7,
            max_tokens=1200,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield json.dumps({
            "title": "AI hiccup!",
            "story": "The magical brain had a little trouble. Falling back to our built-in wisdom.",
            "mission": "Error Recovery",
            "code": f"# Sorry! The AI had a temporary issue.\\n# Your question: {query}\\nprint('Please try again or use the lesson buttons!')",
            "recap": "Sometimes magic needs a second try.\\nThe idea is still worth learning.",
            "sample_output": str(e)[:120],
            "error": True
        })
