"""
Pure logic for Magic Tutor explanations.
This module has NO terminal/console dependencies so it can run on Vercel serverless.
It returns structured data that the web frontend can render.
"""

from typing import Dict, Optional, Tuple
import json

# =============================================================================
# Data for known concepts (stories, code, recap, sample output)
# =============================================================================

KNOWN_CONCEPTS: Dict[str, Dict] = {
    "append": {
        "title": "list.append() — Adding things to a list",
        "story": "Imagine your mom says 'Go write down what we need from the store'. You have a blank piece of paper (an empty list). Every time you think of something, you write it at the bottom. That's append! The list grows one item at a time, always at the end.",
        "mission": "Shopping List Helper for Mom — You're helping your family make a smart shopping list!",
        "code": '''# Real Life Mission: Shopping List Helper for Mom
shopping_list = []                           # empty paper at the start

print("Let's make mom's shopping list!")
print("Current list:", shopping_list)

shopping_list.append("milk")
shopping_list.append("eggs")
shopping_list.append("bread")
shopping_list.append("chocolate cookies")

print("\\nAll done! Here's what we need to buy:")
print(shopping_list)
print(f"\\nWe have {len(shopping_list)} things to buy.")''',
        "recap": "1. [] creates an empty list (blank paper)\n2. .append(item) adds the item at the very end\n3. The list remembers the order you added things\n4. Real life: todo lists, playlists, game inventory, chat messages",
        "sample_output": "Let's make mom's shopping list!\nCurrent list: []\n\nAll done! Here's what we need to buy:\n['milk', 'eggs', 'bread', 'chocolate cookies']\n\nWe have 4 things to buy.",
        "keywords": ["append", "add to list", "list add", "shopping list", "collect", "add item"]
    },
    "pop": {
        "title": "list.pop() — Taking the last thing out",
        "story": "Think of a stack of pancakes or a magic top hat. The last thing you put in is the first thing you can easily grab. pop() removes and gives you the LAST item you added. Perfect for 'undo' buttons.",
        "mission": "Undo Button for a Kids Drawing App",
        "code": '''# Real Life Mission: Undo Button for a Kids Drawing App
drawing_history = []
drawing_history.append("red circle")
drawing_history.append("blue square")
drawing_history.append("green triangle")

print("Shapes drawn:", drawing_history)

last = drawing_history.pop()
print("UNDO! Removed:", last)
print("Now left:", drawing_history)''',
        "recap": "pop() removes the most recent item. Great for stacks and undo features.\nReal life: browser back button, Ctrl+Z, card games.",
        "sample_output": "Shapes drawn: ['red circle', 'blue square', 'green triangle']\nUNDO! Removed: green triangle\nNow left: ['red circle', 'blue square']",
        "keywords": ["pop", "remove last", "undo", "stack", "last item", "take back"]
    },
    "split": {
        "title": "str.split() and .join() — Breaking sentences and gluing them back",
        "story": "split() is like taking a sentence and cutting it into words with scissors. join() is the opposite — gluing a list of words back into one sentence with glue.",
        "mission": "Lemonade Stand Daily Sales Report",
        "code": '''# Real Life Mission: Lemonade Stand Daily Sales Report
raw_sales = "Monday:23,Tuesday:31,Wednesday:18,Thursday:42,Friday:29"

print("Raw sales data:", raw_sales)
days_data = raw_sales.split(",")
print("Broken into pieces:", days_data)

total = 0
for day_info in days_data:
    day, cups = day_info.split(":")
    cups = int(cups)
    total += cups
    print(f"  {day}: sold {cups} cups")

print(f"\\nTotal cups sold this week: {total}")''',
        "recap": "split(separator) cuts a string into a list.\njoin(glue) turns a list back into a string.\nReal life: parsing CSV, chat commands, cleaning user input.",
        "sample_output": "Raw sales data: Monday:23,Tuesday:31,Wednesday:18,Thursday:42,Friday:29\nBroken into pieces: ['Monday:23', 'Tuesday:31', ...]\nTotal cups sold this week: 143",
        "keywords": ["split", "join", "string to list", "words", "sentence", "csv", "break apart"]
    },
    "dict": {
        "title": "Dictionaries (dict) and .get() — Looking things up by name",
        "story": "A dictionary is like a magic phonebook. You say the NAME and instantly get the value! .get() is the safe way to ask without crashing if the key is missing.",
        "mission": "Magic Price Look-up for a Toy Shop",
        "code": '''# Real Life Mission: Magic Price Look-up for a Toy Shop
toy_prices = {"teddy bear": 12, "robot": 25, "ball": 5, "unicorn": 18}

print("How much is a robot?", toy_prices["robot"])
price = toy_prices.get("dragon", "Not in stock")
print("How much is a dragon?", price)''',
        "recap": "dict = {key: value} gives instant lookup by name.\ndict.get(key, default) is safe and friendly.\nReal life: phone contacts, game settings, configuration.",
        "sample_output": "How much is a robot? 25\nHow much is a dragon? Not in stock",
        "keywords": ["dict", "dictionary", "get", "lookup", "key value", "map", "phonebook"]
    },
    "enumerate": {
        "title": "enumerate() — Giving numbers to items while looping",
        "story": "You have a list of toys. You want to say '1. teddy, 2. ball'. enumerate gives you both the number AND the item at the same time.",
        "mission": "Line Up the Kids for the School Play",
        "code": '''# Real Life Mission: Line Up the Kids for the School Play
kids = ["Alex", "Jordan", "Sam", "Taylor", "Casey"]

for position, name in enumerate(kids, start=1):
    print(f"{position}. {name} — please stand here!")''',
        "recap": "enumerate(list) gives you (index, item) pairs.\nenumerate(list, start=1) starts counting at 1 (nicer for humans).\nReal life: numbered menus, ranks, logging with line numbers.",
        "sample_output": "1. Alex — please stand here!\n2. Jordan — please stand here!\n...",
        "keywords": ["enumerate", "number the list", "with index", "position", "line up"]
    },
}


def find_best_explainer(query: str) -> Tuple[Optional[str], Optional[Dict]]:
    """Match user question to a known concept using keyword matching."""
    q = query.lower()
    for name, data in KNOWN_CONCEPTS.items():
        for kw in data.get("keywords", []):
            if kw in q:
                return name, data
    return None, None


def generate_fallback_explanation(query: str) -> Dict:
    """Smart real-world fallback for anything not in the known list."""
    q = query.lower()

    if any(w in q for w in ["loop", "for", "repeat", "each"]):
        title = "Loops (for) — Repeating actions"
        story = "You are making a simple game. You need to repeat an action for every enemy on the screen."
        code = f'''# Real World: Video Game Enemy Spawner
# You asked about: {query}

enemies = ["goblin", "skeleton", "bat", "dragon"]
print("Fighting all enemies!")
for enemy in enemies:
    print(f"  Attacking the {enemy}!")
print("Level cleared!")'''
        sample_output = "Fighting all enemies!\n  Attacking the goblin!\n  Attacking the skeleton!\nLevel cleared!"
        recap = "for item in list: repeats code for every item.\nReal life: processing many enemies, emails, or files."

    elif any(w in q for w in ["function", "def", "reusable"]):
        title = "Functions — Reusable magic spells"
        story = "You want to cast the same 'fireball' spell many times without rewriting the code."
        code = f'''# Real World: Magic Spell Book
# You asked about: {query}

def cast_fireball(target):
    print(f"Fireball hits the {target} for 25 damage!")

cast_fireball("goblin")
cast_fireball("troll")'''
        sample_output = "Fireball hits the goblin for 25 damage!\nFireball hits the troll for 25 damage!"
        recap = "def name(): lets you reuse code.\nCall it whenever you need the same behavior."

    elif any(w in q for w in ["class", "object", "pet"]):
        title = "Classes & Objects — Creating many similar things"
        story = "You want to create many pets that all know how to speak and eat."
        code = f'''# Real World: Virtual Pet Game
# You asked about: {query}

class Pet:
    def __init__(self, name, animal):
        self.name = name
        self.animal = animal

    def speak(self):
        print(f"{self.name} the {self.animal} says hi!")

my_dog = Pet("Buddy", "dog")
my_dog.speak()'''
        sample_output = "Buddy the dog says hi!"
        recap = "class lets you make your own 'types' of things with data + behavior."

    else:
        title = f"Real-world example for: {query}"
        story = "You are teaching a little robot how to help around the house by collecting and organizing tasks."
        code = f'''# Real World: Personal Robot Helper
# You asked about: {query}

tasks = []
tasks.append("feed the cat")
tasks.append("water the plants")
print("Robot's task list:", tasks)
print("First job:", tasks[0])'''
        sample_output = "Robot's task list: ['feed the cat', 'water the plants']\nFirst job: feed the cat"
        recap = "We turned your idea into a small, runnable real-life program using lists and simple logic."

    return {
        "title": title,
        "story": story,
        "mission": f"Custom mission for: {query}",
        "code": code,
        "recap": recap,
        "sample_output": sample_output,
        "is_fallback": True,
    }


def get_explanation(query: str) -> Dict:
    """Main entry point. Returns a rich explanation dict for the web."""
    if not query or len(query.strip()) < 2:
        return {
            "title": "Tell me something!",
            "story": "Ask about any Python concept (like 'append', 'loops', 'how do I make a list', 'functions', etc.)",
            "mission": "",
            "code": "# Ask me anything about Python!",
            "recap": "I can explain almost anything with a fun real-world story + runnable code.",
            "sample_output": "",
            "is_fallback": True,
        }

    name, data = find_best_explainer(query)
    if data:
        result = {
            "title": data["title"],
            "story": data["story"],
            "mission": data.get("mission", ""),
            "code": data["code"],
            "recap": data["recap"],
            "sample_output": data.get("sample_output", ""),
            "is_fallback": False,
            "concept": name,
        }
        return result

    # Smart fallback for anything else
    result = generate_fallback_explanation(query)
    result["concept"] = "custom"
    return result
