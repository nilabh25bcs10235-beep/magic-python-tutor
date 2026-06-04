"""
🪄  Magic Python Tutor
A beautiful, interactive, running application that explains ANY Python or development concept
like you're 5 years old — using real-world problem solving, live code animations, and running code.

Terminal version (for the old rich TUI experience).
The main application is now the colorful GUI (run with `magic-tutor` after install).

For GUI (recommended):
    magic-tutor

It takes your questions in natural language and builds animated, runnable real-life examples every time.
"""

import os
import time
import sys
from typing import Optional, Dict, Callable

# Rich for gorgeous frontend
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.rule import Rule
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: rich not found. Falling back to plain mode. (pip install rich for best experience)")

# Our magic animation engine (the star of the show)
import magic_typer as mt

# =============================================================================
# CONFIG
# =============================================================================
TYPING_DELAY = 0.032          # User can change this with 'speed' command
EXAMPLES_DIR = "examples"
console: "Console" = mt.get_console()

# =============================================================================
# WELCOME & DESIGN HELPERS (beautiful frontend)
# =============================================================================

def show_welcome():
    """Gorgeous welcome screen."""
    console.clear()
    console.print()
    console.rule("[bold cyan]🪄  MAGIC PYTHON TUTOR  🪄[/]", style="bright_cyan")
    console.print()
    
    banner = Text()
    banner.append("Explained like you're 5 years old\n", style="bold yellow")
    banner.append("Real-world problems • Live code animations • Running programs\n\n", style="dim")
    banner.append("Just type what you want to understand (e.g. 'append', 'how do dicts work', 'loops in games')\n", style="white")
    banner.append("I will turn it into a fun story + build you a real working program with magic typing!", style="italic cyan")
    
    console.print(Panel(banner, border_style="cyan", padding=(1, 2), title="[bold]Welcome, little coder![/]"))
    console.print()
    console.print("[dim]Commands:  list  •  help  •  speed  •  clear  •  quit[/]")
    console.rule(style="cyan")
    console.print()

def show_help():
    console.print(Panel(
        "[bold]How to talk to me:[/]\n\n"
        "• Just describe the concept:  [cyan]append[/]  or  [cyan]what is a dictionary[/]  or  [cyan]explain loops[/]\n"
        "• Ask about real dev things:  [cyan]how do I organize player scores[/]  or  [cyan]undo button[/]\n"
        "• After a lesson you can ask follow-ups like 'how do I remove the last one?'\n\n"
        "[bold yellow]Special commands:[/]\n"
        "  list     → see all built-in concepts I know really well\n"
        "  speed    → change how fast the magic typing happens\n"
        "  clear    → fresh screen\n"
        "  help     → this message\n"
        "  quit     → exit the tutor",
        title="💡 Help", border_style="yellow", padding=(1,2)
    ))

def change_speed():
    global TYPING_DELAY
    current = f"{TYPING_DELAY:.3f}"
    new = Prompt.ask(f"Current typing speed (lower = slower & clearer)", default=current)
    try:
        TYPING_DELAY = float(new)
        console.print(f"[green]✨ Typing speed set to {TYPING_DELAY:.3f} seconds per character[/]")
    except:
        console.print("[red]Invalid number, keeping previous speed.[/]")

def list_concepts():
    """Pretty table of known concepts."""
    table = Table(title="🧠 Concepts I Can Explain Super Well", show_lines=True)
    table.add_column("Concept", style="cyan", no_wrap=True)
    table.add_column("Real-World Example I Use", style="white")
    
    for name, explainer in KNOWN_CONCEPTS.items():
        table.add_row(name, explainer.get("example", "Cool real life thing"))
    
    table.add_row("[dim]...anything else![/]", "[dim]I will invent a perfect real-world story for you[/]")
    console.print(table)
    console.print("[dim]Just type the name or describe what you want![/]\n")

# =============================================================================
# THE BRAIN: Concept Explainers + Smart Fallback
# =============================================================================

def explain_append(console, delay):
    """Real world: A kid building a shopping list for their parent."""
    mt.simple_story_intro(
        "list.append() — Adding things to a list",
        "Imagine your mom says 'Go write down what we need from the store'. "
        "You have a blank piece of paper (an empty list). Every time you think of something, "
        "you write it at the bottom. That's append! The list grows one item at a time, "
        "always at the end. Super useful for collecting things!",
        console
    )
    
    mt.thinking_animation("Building a real shopping helper for a 7-year-old...", console, 1.0)
    
    code = '''# Real Life Mission: Shopping List Helper for Mom
# You are helping your family by making a smart shopping list!

shopping_list = []                           # empty paper at the start

print("Let's make mom's shopping list!")
print("Current list:", shopping_list)

# Add items one by one (this is append in action)
shopping_list.append("milk")
shopping_list.append("eggs")
shopping_list.append("bread")
shopping_list.append("chocolate cookies")   # you added this one secretly :)

print("\\nAll done! Here's what we need to buy:")
print(shopping_list)

print(f"\\nWe have {len(shopping_list)} things to buy.")
print("First thing to find in the store:", shopping_list[0])'''

    filepath = mt.type_and_run(
        code, 
        filename="shopping_list_for_mom.py",
        delay=delay,
        console=console,
        examples_dir=EXAMPLES_DIR
    )
    
    console.print(Panel(
        "1. [] creates an empty list (blank paper)\n"
        "2. .append(item) adds the item at the very end\n"
        "3. The list remembers the order you added things\n"
        "4. Real life: todo lists, high scores, chat messages, inventory in games, playlist songs",
        title="🎓 What You Just Learned (super simple)", border_style="green"
    ))
    
    return filepath

def explain_pop(console, delay):
    """Real world: Undo button in a drawing app or magic hat (LIFO)."""
    mt.simple_story_intro(
        "list.pop() — Taking the last thing out",
        "Think of a stack of pancakes or a magic top hat. The last thing you put in is the first thing you can easily grab. "
        "pop() removes and gives you the LAST item you added. Perfect for 'undo' buttons, browser back, or serving the most recent customer first!",
        console
    )
    
    mt.thinking_animation("Creating a real 'Undo' feature for a kid's drawing app...", console, 1.0)
    
    code = '''# Real Life Mission: Undo Button for a Kids Drawing App
# Every time you draw a shape, we remember it. Pressing "undo" removes the last one.

drawing_history = []

print("🎨 Starting a new drawing...")

drawing_history.append("red circle")
drawing_history.append("blue square")
drawing_history.append("green triangle")

print("Shapes drawn so far:", drawing_history)

# Oh no! You didn't like the last shape
last_shape = drawing_history.pop()   # pop removes the LAST thing added
print(f"\\nUNDO! Removed the last shape: {last_shape}")

print("Drawing now looks like this:", drawing_history)

# You can even pop again
if drawing_history:
    another = drawing_history.pop()
    print(f"UNDO again! Also removed: {another}")

print("\\nFinal drawing history:", drawing_history)'''

    filepath = mt.type_and_run(code, "drawing_app_undo.py", delay=delay, console=console, examples_dir=EXAMPLES_DIR)
    
    console.print(Panel(
        "pop() is like 'take back the most recent thing I did'.\n"
        "It returns the item so you can use it (or just throw it away).\n"
        "Real life: browser back button, Ctrl+Z in editors, card games (draw from top), function call stack.",
        title="🎓 What You Just Learned", border_style="green"
    ))
    return filepath

def explain_split_join(console, delay):
    """Real world: Parsing commands or turning a sentence into a list and back (lemonade stand sales)."""
    mt.simple_story_intro(
        "str.split() and .join() — Breaking sentences and gluing them back",
        "split() is like taking a sentence and cutting it into words with scissors. "
        "join() is the opposite — gluing a list of words back into one sentence with glue (any separator you want). "
        "Super powerful for reading files, understanding user commands, or making nice reports!",
        console
    )
    
    mt.thinking_animation("Building a lemonade stand sales report reader...", console, 1.0)
    
    code = '''# Real Life Mission: Lemonade Stand Daily Sales Report
# Your little business wrote sales in one long line. We need to understand it!

raw_sales = "Monday:23,Tuesday:31,Wednesday:18,Thursday:42,Friday:29"

print("Raw sales data from notebook:", raw_sales)

# split turns the big string into a list we can work with
days_data = raw_sales.split(",")
print("\\nBroken into pieces:", days_data)

# Now we can do smart things
total = 0
for day_info in days_data:
    day, cups = day_info.split(":")     # split again on the colon!
    cups = int(cups)
    total += cups
    print(f"  {day}: sold {cups} cups")

print(f"\\n🏆 Total cups sold this week: {total}")

# join puts a list back together nicely
best_days = ["Tuesday", "Thursday"]
report = " and ".join(best_days)
print(f"Best days were: {report}")'''

    filepath = mt.type_and_run(code, "lemonade_stand_report.py", delay=delay, console=console, examples_dir=EXAMPLES_DIR)
    
    console.print(Panel(
        "split(separator) cuts a string into a list.\n"
        "join(glue) turns a list of strings into one string.\n"
        "Real life: reading CSV files, parsing chat commands ('/buy sword'), cleaning user input, making pretty output.",
        title="🎓 What You Just Learned", border_style="green"
    ))
    return filepath

def explain_dict_get(console, delay):
    """Real world: A phonebook or price lookup for a toy shop."""
    mt.simple_story_intro(
        "Dictionaries (dict) and .get() — Looking things up by name",
        "A dictionary is like a magic phonebook or a treasure map. You don't search from the beginning — you say the NAME and instantly get the value! "
        ".get() is the polite way to ask 'do you have this?' without crashing if the answer is no.",
        console
    )
    
    mt.thinking_animation("Making a real price lookup tool for a toy shop...", console, 1.0)
    
    code = '''# Real Life Mission: Magic Price Look-up for a Toy Shop
# Customers ask "How much is the teddy bear?" and we answer instantly.

toy_prices = {
    "teddy bear": 12,
    "robot": 25,
    "ball": 5,
    "unicorn": 18
}

print("🏪 Welcome to the Toy Shop!")
print("Our prices:", toy_prices)

# Normal lookup (crashes if key missing)
print("\\nHow much is a robot?", toy_prices["robot"])

# Safe lookup with .get() — returns None or a default if not found
price = toy_prices.get("dragon")
print("How much is a dragon?", price)   # None = we don't have it

# With a nice default message
price = toy_prices.get("ball", "Sorry, not in stock")
print("How much is a ball?", price)

# Real shop: ask the customer
item = "unicorn"
if item in toy_prices:
    print(f"\\nYes! A {item} costs ${toy_prices[item]}")
else:
    print(f"\\nWe don't have {item} today.")'''

    filepath = mt.type_and_run(code, "toy_shop_prices.py", delay=delay, console=console, examples_dir=EXAMPLES_DIR)
    
    console.print(Panel(
        "dict = {key: value} — super fast lookup by name\n"
        "dict[key] gets the value or crashes if missing\n"
        "dict.get(key, default) is safe and friendly\n"
        "Real life: phone contacts, game settings, configuration, counting words, caching, API responses.",
        title="🎓 What You Just Learned", border_style="green"
    ))
    return filepath

def explain_enumerate(console, delay):
    """Real world: Numbering items in a list for a game or school project."""
    mt.simple_story_intro(
        "enumerate() — Giving numbers to items while looping",
        "You have a list of toys. You want to say '1. teddy, 2. ball, 3. car'. "
        "enumerate gives you both the number (starting from 0 or 1) AND the item at the same time. "
        "No more ugly counting variables!",
        console
    )
    
    mt.thinking_animation("Creating a lineup system for the school play...", console, 1.0)
    
    code = '''# Real Life Mission: Line Up the Kids for the School Play
# We need to call their names with numbers so everyone knows their position.

kids = ["Alex", "Jordan", "Sam", "Taylor", "Casey"]

print("🎭 School Play Lineup (positions start at 1):")

for position, name in enumerate(kids, start=1):   # start=1 makes it human-friendly
    print(f"{position}. {name} — please stand here!")

print("\\nGreat! Everyone knows their spot.")

# Bonus: sometimes you only care about the number
print("\\nNumber of kids:", len(kids))
for idx, name in enumerate(kids):
    if idx == 2:   # the third kid (index 2)
        print(f"Special job for kid #{idx+1}: {name} holds the banner!")'''

    filepath = mt.type_and_run(code, "school_play_lineup.py", delay=delay, console=console, examples_dir=EXAMPLES_DIR)
    
    console.print(Panel(
        "enumerate(list) gives you (index, item) pairs\n"
        "enumerate(list, start=1) starts counting at 1 (nicer for humans)\n"
        "Real life: showing numbered menus, processing rows in a spreadsheet, giving ranks, logging with line numbers.",
        title="🎓 What You Just Learned", border_style="green"
    ))
    return filepath

# Registry of excellent built-in explainers
KNOWN_CONCEPTS: Dict[str, Dict] = {
    "append": {
        "func": explain_append,
        "example": "Shopping list for mom / collecting items",
        "keywords": ["append", "add to list", "list add", "shopping list", "collect"]
    },
    "pop": {
        "func": explain_pop,
        "example": "Undo button in drawing app",
        "keywords": ["pop", "remove last", "undo", "stack", "last item"]
    },
    "split": {
        "func": explain_split_join,
        "example": "Lemonade stand sales report",
        "keywords": ["split", "join", "string to list", "words", "sentence", "csv"]
    },
    "dict": {
        "func": explain_dict_get,
        "example": "Toy shop price lookup",
        "keywords": ["dict", "dictionary", "get", "lookup", "key value", "map", "phonebook"]
    },
    "enumerate": {
        "func": explain_enumerate,
        "example": "School play lineup / numbered list",
        "keywords": ["enumerate", "number the list", "with index", "position", "line up"]
    },
}

def find_best_explainer(query: str):
    """Match user question to a known concept using simple but effective keyword matching."""
    q = query.lower()
    for name, data in KNOWN_CONCEPTS.items():
        for kw in data.get("keywords", []):
            if kw in q:
                return name, data["func"]
    return None, None

def smart_real_world_fallback(query: str, console, delay):
    """
    When the user asks about something we don't have a pre-written lesson for,
    we STILL give them an amazing experience:
    - Pick a real-world kid-friendly scenario based on keywords
    - Generate correct, useful code that demonstrates the concept
    - Animate it live + run it
    This is the 'handles ANY question' superpower.
    """
    q = query.lower()
    
    # Pick a domain
    if any(w in q for w in ["loop", "for", "repeat", "each"]):
        domain = "video game enemy spawner"
        story = "You are making a simple game. You need to repeat an action for every enemy on the screen."
        code = f'''# Real World: {domain.title()}
# The player asked about: {query}

enemies = ["goblin", "skeleton", "bat", "dragon"]

print("⚔️  Fighting all enemies in the level!")
for enemy in enemies:
    print(f"  Attacking the {enemy}!")

print("\\nLevel cleared! Great job using loops.")'''
        filename = "game_enemy_loop.py"
        
    elif any(w in q for w in ["function", "def", "reusable", "spell"]):
        domain = "magic spell book in a game"
        story = "You want to cast the same 'fireball' spell many times without rewriting the code."
        code = f'''# Real World: {domain.title()}
# The player asked about: {query}

def cast_fireball(target):
    """Reusable magic!"""
    print(f"🔥 Fireball hits the {target} for 25 damage!")

print("Wizard is fighting...")
cast_fireball("goblin")
cast_fireball("troll")
cast_fireball("evil wizard")
print("All spells cast using one function!")'''
        filename = "magic_spell_function.py"
        
    elif any(w in q for w in ["class", "object", "pet", "character"]):
        domain = "virtual pet game"
        story = "You want to create many pets that all know how to 'speak' and 'eat'."
        code = f'''# Real World: {domain.title()}
# The player asked about: {query}

class Pet:
    def __init__(self, name, animal):
        self.name = name
        self.animal = animal
    
    def speak(self):
        print(f"{self.name} the {self.animal} says: Hello friend!")

print("Adopting pets...")
my_dog = Pet("Buddy", "dog")
my_cat = Pet("Whiskers", "cat")

my_dog.speak()
my_cat.speak()'''
        filename = "virtual_pet.py"
        
    elif any(w in q for w in ["file", "save", "write", "read", "score"]):
        domain = "saving high scores for a game"
        story = "After the player wins, we need to remember their score forever."
        code = f'''# Real World: {domain.title()}
# The player asked about: {query}

score = 1240
player = "Alex"

# Save the score to a real file
with open("highscore.txt", "w") as f:
    f.write(f"{player}:{score}")

print("Score saved to highscore.txt!")

# Read it back later
with open("highscore.txt") as f:
    saved = f.read()
print("Loaded from file:", saved)'''
        filename = "save_high_score.py"
        
    else:
        # Generic but still excellent fallback
        domain = "personal robot helper"
        story = "You are teaching a little robot how to help around the house by collecting and organizing tasks."
        code = f'''# Real World: Personal Robot Helper
# The player asked about: {query}

tasks = []
tasks.append("feed the cat")
tasks.append("water the plants")

print("Robot's task list:", tasks)
print("First job for today:", tasks[0])

print("\\nGreat! You used lists to give your robot a job list.")'''
        filename = "robot_helper_tasks.py"
    
    mt.simple_story_intro(f"Smart real-world example for: {query}", story, console)
    mt.thinking_animation(f"Generating a perfect {domain} example just for you...", console, 0.9)
    
    return mt.type_and_run(code, filename, delay=delay, console=console, examples_dir=EXAMPLES_DIR)

def handle_question(query: str):
    """Main entry point for any user question. This is what makes the app special."""
    if not query or len(query.strip()) < 2:
        console.print("[yellow]Please tell me a concept or ask a question![/]")
        return
    
    # Try exact / keyword match first
    concept_name, explainer_func = find_best_explainer(query)
    
    if explainer_func:
        console.print(f"\n[bold green]✅ Found a great lesson for '{concept_name}'[/]")
        explainer_func(console, TYPING_DELAY)
    else:
        console.print(f"\n[bold cyan]🧠 I don't have a pre-made lesson for that exact phrase...[/]")
        console.print("[cyan]But I will still build you an excellent real-world example with animation![/]\n")
        smart_real_world_fallback(query, console, TYPING_DELAY)
    
    # After every explanation — give the user power (the key missing feature they asked for)
    post_lesson_menu(query)

def post_lesson_menu(original_query: str):
    """This is the interactive part the user wanted — keep asking, modify, explore."""
    while True:
        console.print()
        choice = Prompt.ask(
            "[bold]What next?[/]  [1] Ask follow-up  [2] See saved code  [3] Related idea  [4] New question  [5] Quit lesson",
            choices=["1","2","3","4","5"],
            default="4",
            show_choices=False
        )
        
        if choice == "1":
            followup = Prompt.ask("[cyan]What else do you want to know about this?[/]")
            # Simple but powerful: treat the followup as a new question in context
            console.print(f"[dim]Thinking about '{followup}' in the context of '{original_query}'...[/]")
            # For now we just handle it as a fresh (but related) question
            handle_question(followup)
            break  # after handling followup we return to outer loop naturally
        elif choice == "2":
            # Show the most recent file in examples
            files = sorted([f for f in os.listdir(EXAMPLES_DIR) if f.endswith('.py')]) if os.path.exists(EXAMPLES_DIR) else []
            if files:
                latest = os.path.join(EXAMPLES_DIR, files[-1])
                with open(latest, encoding="utf-8") as f:
                    content = f.read()
                console.print(Panel(content, title=f"📄 {latest}", border_style="blue"))
            else:
                console.print("[yellow]No saved examples yet.[/]")
        elif choice == "3":
            console.print("[yellow]Tell me a related concept and I'll explain it right now (e.g. 'how to remove from list' after append).[/]")
            related = Prompt.ask("Related concept")
            handle_question(related)
            break
        elif choice == "4":
            break  # go back to main question loop
        elif choice == "5":
            console.print("[bold cyan]Okay! Returning to main tutor...[/]")
            break

# =============================================================================
# MAIN APPLICATION LOOP
# =============================================================================

def main():
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    
    show_welcome()
    
    while True:
        try:
            user_input = Prompt.ask(
                "[bold cyan]🗣️  Ask me anything about Python or programming[/]",
                default="help"
            ).strip()
            
            cmd = user_input.lower()
            
            if cmd in ("quit", "exit", "q"):
                console.print("[bold magenta]Thanks for learning with me! Keep building cool things. ✨[/]")
                break
            elif cmd in ("help", "?"):
                show_help()
            elif cmd in ("list", "concepts", "ls"):
                list_concepts()
            elif cmd in ("speed", "s"):
                change_speed()
            elif cmd in ("clear", "cls"):
                console.clear()
                show_welcome()
            elif cmd.startswith(("what is", "explain", "how", "tell me about")) or len(cmd) > 2:
                handle_question(user_input)
            else:
                # Treat almost everything as a question
                handle_question(user_input)
                
        except KeyboardInterrupt:
            console.print("\n[bold magenta]Goodbye! (Ctrl+C)[/]")
            break
        except Exception as e:
            console.print(f"[red]Oops, something went wrong: {e}[/]\n[dim]Try another question![/]")

if __name__ == "__main__":
    main()