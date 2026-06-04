"""
MAGIC TUTOR - Standalone Colorful Desktop Application
Big tekky header, modern UI, live code animations, real-world Python explanations.
Runs as a proper application (not just terminal).

Entry point: magic-tutor (after pip install)
Or: python -m gui
"""

import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess
import sys
import tempfile
import threading
import time

# Hide the console window on Windows when launched directly (clean GUI experience)
# Only do this if there's actually a console attached (to avoid issues under gui launcher)
if os.name == "nt":
    try:
        import ctypes
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window:
            ctypes.windll.user32.ShowWindow(console_window, 0)  # SW_HIDE
    except Exception:
        pass

# =============================================================================
# CONFIG
# =============================================================================
EXAMPLES_DIR = "examples"
TYPING_DELAY_MS = 25  # ms per char for GUI animation (faster than terminal for UX)

# Tekky color scheme
DARK_BG = "#0a0a1f"
ACCENT_CYAN = "#00f0ff"
ACCENT_MAGENTA = "#ff00cc"
ACCENT_GREEN = "#00ff9f"
TEXT_LIGHT = "#e8e8ff"
CODE_BG = "#12122a"
PANEL_BG = "#16162e"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # we'll override with custom colors

# =============================================================================
# LESSON DATA (real world + code + recap)
# =============================================================================
LESSONS = {
    "append": {
        "title": "list.append() — Adding things to a list",
        "story": "Imagine your mom says 'Go write down what we need from the store'.\nYou have a blank piece of paper (an empty list). Every time you think of something, you write it at the bottom. That's append! The list grows one item at a time, always at the end.",
        "mission": "Shopping List Helper for Mom — You're helping your family by making a smart shopping list!",
        "code": '''# Real Life Mission: Shopping List Helper for Mom
shopping_list = []                           # empty paper at the start

print("Let's make mom's shopping list!")
print("Current list:", shopping_list)

shopping_list.append("milk")
shopping_list.append("eggs")
shopping_list.append("bread")
shopping_list.append("chocolate cookies")   # you added this one secretly :)

print("\\nAll done! Here's what we need to buy:")
print(shopping_list)
print(f"\\nWe have {len(shopping_list)} things to buy.")
print("First thing to find in the store:", shopping_list[0])''',
        "recap": "1. [] creates an empty list (blank paper)\n2. .append(item) adds the item at the very end\n3. The list remembers the order you added things\n4. Real life: todo lists, high scores, chat messages, inventory in games, playlist songs",
        "filename": "shopping_list_for_mom.py"
    },
    "pop": {
        "title": "list.pop() — Taking the last thing out (Undo!)",
        "story": "Think of a stack of pancakes or a magic top hat. The last thing you put in is the first thing you can easily grab.\npop() removes and gives you the LAST item you added. Perfect for 'undo' buttons!",
        "mission": "Undo Button for a Kids Drawing App — Every time you draw a shape, we remember it. Pressing 'undo' removes the last one.",
        "code": '''# Real Life Mission: Undo Button for a Kids Drawing App
drawing_history = []

print("🎨 Starting a new drawing...")
drawing_history.append("red circle")
drawing_history.append("blue square")
drawing_history.append("green triangle")

print("Shapes drawn so far:", drawing_history)

# Oh no! You didn't like the last shape
last_shape = drawing_history.pop()
print(f"\\nUNDO! Removed the last shape: {last_shape}")
print("Drawing now looks like this:", drawing_history)''',
        "recap": "pop() is like 'take back the most recent thing I did'.\nIt returns the item so you can use it.\nReal life: browser back button, Ctrl+Z, card games, function call stack.",
        "filename": "drawing_app_undo.py"
    },
    "dict": {
        "title": "Dictionaries (dict) + .get() — Instant lookup by name",
        "story": "A dictionary is like a magic phonebook or treasure map. You don't search from the beginning — you say the NAME and instantly get the value!\n.get() is the polite way to ask 'do you have this?' without crashing if the answer is no.",
        "mission": "Magic Price Look-up for a Toy Shop — Customers ask 'How much is the teddy bear?' and we answer instantly.",
        "code": '''# Real Life Mission: Magic Price Look-up for a Toy Shop
toy_prices = {
    "teddy bear": 12,
    "robot": 25,
    "ball": 5,
    "unicorn": 18
}

print("🏪 Welcome to the Toy Shop!")
item = "robot"
print(f"How much is a {item}?", toy_prices.get(item, "Not in stock"))

# Safe lookup
price = toy_prices.get("dragon", "Sorry, we don't have that today")
print("Dragon price:", price)''',
        "recap": "dict = {key: value} — super fast lookup by name\n.get(key, default) is safe and friendly\nReal life: phone contacts, game settings, configuration, counting words.",
        "filename": "toy_shop_prices.py"
    },
    "split": {
        "title": "str.split() + .join() — Breaking & gluing text",
        "story": "split() is like taking a sentence and cutting it into words with scissors.\njoin() is the opposite — gluing a list of words back into one sentence with any glue you want.",
        "mission": "Lemonade Stand Daily Sales Report — Your little business wrote sales in one long line. We need to understand it!",
        "code": '''# Real Life Mission: Lemonade Stand Daily Sales Report
raw_sales = "Monday:23,Tuesday:31,Wednesday:18,Thursday:42,Friday:29"
print("Raw sales data:", raw_sales)

days_data = raw_sales.split(",")
print("Broken into pieces:", days_data)

total = 0
for day_info in days_data:
    day, cups = day_info.split(":")
    total += int(cups)
    print(f"  {day}: sold {cups} cups")

print(f"\\n🏆 Total cups sold this week: {total}")
best = " and ".join(["Tuesday", "Thursday"])
print(f"Best days were: {best}")''',
        "recap": "split(separator) cuts a string into a list\n.join(glue) turns a list of strings into one string\nReal life: reading CSV, parsing commands, cleaning user input.",
        "filename": "lemonade_stand_report.py"
    },
}

def get_lesson(query: str):
    """Smart fallback + known lessons."""
    q = query.lower().strip()
    for key in LESSONS:
        if key in q or LESSONS[key]["title"].lower().split()[0] in q:
            return LESSONS[key]

    # Smart real-world fallback for unknown concepts
    if any(w in q for w in ["loop", "for", "repeat"]):
        return {
            "title": "for loops — Repeating actions",
            "story": "You are making a simple game. You need to repeat an action for every enemy on the screen.",
            "mission": "Video Game Enemy Spawner",
            "code": '''enemies = ["goblin", "skeleton", "bat", "dragon"]
print("⚔️ Fighting all enemies in the level!")
for enemy in enemies:
    print(f"  Attacking the {enemy}!")
print("\\nLevel cleared! Great job using loops.")''',
            "recap": "for item in list: lets you repeat code for every item.\nReal life: processing game entities, sending emails to a list, calculating totals.",
            "filename": "game_enemy_loop.py"
        }
    elif any(w in q for w in ["function", "def", "reusable"]):
        return {
            "title": "Functions (def) — Reusable spells",
            "story": "You want to cast the same 'fireball' spell many times without rewriting the code.",
            "mission": "Magic Spell Book in a Game",
            "code": '''def cast_fireball(target):
    """Reusable magic!"""
    print(f"🔥 Fireball hits the {target} for 25 damage!")

print("Wizard is fighting...")
cast_fireball("goblin")
cast_fireball("troll")
print("All spells cast using one function!")''',
            "recap": "def name(): lets you create reusable commands.\nReal life: game abilities, calculations you do often, cleaning up repeated code.",
            "filename": "magic_spell_function.py"
        }
    else:
        # Truncate very long queries to prevent UI issues / "endless" display
        safe_query = query[:80] + "..." if len(query) > 80 else query
        return {
            "title": f"Real-world helper for: {safe_query}",
            "story": "You are teaching a little robot how to help around the house by collecting and organizing tasks.",
            "mission": "Personal Robot Helper",
            "code": f'''# Real World: Personal Robot Helper
tasks = []
tasks.append("feed the cat")
tasks.append("water the plants")
print("Robot's task list:", tasks)
print("First job:", tasks[0])
print("\\nGreat! You used Python to give your robot a job list.")''',
            "recap": "Python lets you collect things, repeat actions, and give the computer clear instructions.\nReal life: automation, games, data processing, personal tools.",
            "filename": "robot_helper.py"
        }

# =============================================================================
# GUI APPLICATION
# =============================================================================
class MagicTutorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MAGIC TUTOR")
        self.geometry("1100x720")
        self.minsize(900, 600)

        # Dark tekky theme
        self.configure(fg_color=DARK_BG)

        self.current_lesson = None
        self.current_code = ""

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        # === TOP HEADER - BIG TEKKY "MAGIC TUTOR" ===
        header_frame = ctk.CTkFrame(self, fg_color="#05050f", height=110, corner_radius=0)
        header_frame.pack(fill="x", pady=0)

        # Big tekky header
        header_label = ctk.CTkLabel(
            header_frame,
            text="MAGIC TUTOR",
            font=("Consolas", 52, "bold"),
            text_color=ACCENT_CYAN,
            fg_color="transparent"
        )
        header_label.pack(pady=(8, 0))

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Python concepts • Real-world missions • Live code animations • Executable examples",
            font=("Consolas", 13),
            text_color=ACCENT_MAGENTA
        )
        subtitle.pack(pady=(0, 8))

        # Decorative line
        line = ctk.CTkFrame(header_frame, height=2, fg_color=ACCENT_GREEN)
        line.pack(fill="x", padx=40, pady=(0, 4))

        # === MAIN CONTENT ===
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=8)

        # LEFT SIDEBAR - Lessons
        sidebar = ctk.CTkFrame(main_frame, width=220, fg_color=PANEL_BG, corner_radius=12)
        sidebar.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(sidebar, text="📚 LESSONS", font=("Consolas", 16, "bold"), text_color=ACCENT_CYAN).pack(pady=(12, 6))

        for key, lesson in LESSONS.items():
            btn = ctk.CTkButton(
                sidebar,
                text=lesson["title"].split("—")[0].strip(),
                fg_color="#1f1f3a",
                hover_color=ACCENT_CYAN,
                text_color="white",
                font=("Consolas", 12),
                command=lambda k=key: self.load_lesson(k)
            )
            btn.pack(fill="x", padx=10, pady=4)

        # Free ask button
        free_btn = ctk.CTkButton(
            sidebar,
            text="✨ ASK ANYTHING",
            fg_color=ACCENT_MAGENTA,
            hover_color="#ff66dd",
            text_color="white",
            font=("Consolas", 13, "bold"),
            command=self._ask_anything_dialog
        )
        free_btn.pack(fill="x", padx=10, pady=12)

        # CENTER - Main content
        center = ctk.CTkFrame(main_frame, fg_color="transparent")
        center.pack(side="left", fill="both", expand=True)

        # Current topic
        self.topic_label = ctk.CTkLabel(
            center,
            text="Welcome, little coder!",
            font=("Consolas", 18, "bold"),
            text_color=ACCENT_GREEN
        )
        self.topic_label.pack(anchor="w", pady=(0, 6))

        # Story / Explanation box
        ctk.CTkLabel(center, text="🧸 THE STORY", font=("Consolas", 12), text_color=ACCENT_CYAN).pack(anchor="w")
        self.story_box = ctk.CTkTextbox(center, height=110, fg_color=CODE_BG, text_color=TEXT_LIGHT, font=("Consolas", 11))
        self.story_box.pack(fill="x", pady=(2, 8))
        self.story_box.delete("0.0", "end")  # ensure clean on startup

        # Mission
        ctk.CTkLabel(center, text="🌍 REAL WORLD MISSION", font=("Consolas", 12), text_color=ACCENT_MAGENTA).pack(anchor="w")
        self.mission_box = ctk.CTkTextbox(center, height=45, fg_color=PANEL_BG, text_color=ACCENT_GREEN, font=("Consolas", 11, "bold"))
        self.mission_box.pack(fill="x", pady=(2, 8))
        self.mission_box.delete("0.0", "end")  # ensure clean on startup

        # Code area
        code_header = ctk.CTkFrame(center, fg_color="transparent")
        code_header.pack(fill="x")
        ctk.CTkLabel(code_header, text="💻 THE MAGIC CODE", font=("Consolas", 12), text_color=ACCENT_CYAN).pack(side="left")
        self.animate_btn = ctk.CTkButton(
            code_header, text="▶ WATCH LIVE TYPING", width=160,
            fg_color=ACCENT_CYAN, text_color="black", font=("Consolas", 11, "bold"),
            command=self.animate_code
        )
        self.animate_btn.pack(side="right", padx=4)

        self.code_box = ctk.CTkTextbox(center, height=180, fg_color=CODE_BG, text_color="#aaffff", font=("Consolas", 10))
        self.code_box.pack(fill="both", expand=True, pady=(2, 6))
        self.code_box.delete("0.0", "end")  # ensure clean on startup

        # Action buttons
        actions = ctk.CTkFrame(center, fg_color="transparent")
        actions.pack(fill="x", pady=4)

        self.run_btn = ctk.CTkButton(
            actions, text="⚡ RUN IN REAL LIFE", fg_color=ACCENT_GREEN, text_color="black",
            font=("Consolas", 12, "bold"), command=self.run_code
        )
        self.run_btn.pack(side="left", padx=4)

        self.save_btn = ctk.CTkButton(
            actions, text="💾 SAVE EXAMPLE", fg_color="#444466", text_color="white",
            font=("Consolas", 12), command=self.save_example
        )
        self.save_btn.pack(side="left", padx=4)

        # Output / Console
        ctk.CTkLabel(center, text="📤 PROGRAM OUTPUT (what really happens)", font=("Consolas", 11), text_color=ACCENT_MAGENTA).pack(anchor="w", pady=(6, 2))
        self.output_box = ctk.CTkTextbox(center, height=110, fg_color="#05050f", text_color=ACCENT_GREEN, font=("Consolas", 10))
        self.output_box.pack(fill="x")
        self.output_box.delete("0.0", "end")  # ensure clean on startup

        # RIGHT - Recap + Tips
        right = ctk.CTkFrame(main_frame, width=260, fg_color=PANEL_BG, corner_radius=12)
        right.pack(side="right", fill="y", padx=(10, 0))

        ctk.CTkLabel(right, text="🎓 WHAT YOU LEARNED", font=("Consolas", 14, "bold"), text_color=ACCENT_CYAN).pack(pady=10)

        self.recap_box = ctk.CTkTextbox(right, fg_color=CODE_BG, text_color=TEXT_LIGHT, font=("Consolas", 10))
        self.recap_box.pack(fill="both", expand=True, padx=8, pady=4)
        self.recap_box.delete("0.0", "end")  # ensure clean on startup

        # Bottom input bar
        input_bar = ctk.CTkFrame(self, fg_color="#05050f", height=50, corner_radius=0)
        input_bar.pack(fill="x", side="bottom")

        self.query_entry = ctk.CTkEntry(
            input_bar, placeholder_text="Ask anything... (e.g. 'how do loops work in games')",
            font=("Consolas", 12), width=500, fg_color=CODE_BG, text_color="white"
        )
        self.query_entry.pack(side="left", padx=15, pady=8)
        self.query_entry.delete(0, "end")  # ensure clean on startup
        self.query_entry.bind("<Return>", lambda e: self.ask_free())

        ask_btn = ctk.CTkButton(
            input_bar, text="ASK MAGIC TUTOR", fg_color=ACCENT_MAGENTA, text_color="white",
            font=("Consolas", 12, "bold"), command=self.ask_free
        )
        ask_btn.pack(side="left", padx=6)

    def _show_welcome(self):
        self.topic_label.configure(text="🪄 MAGIC TUTOR — What do you want to master today?")
        self.query_entry.delete(0, "end")
        for box in [self.story_box, self.mission_box, self.code_box, self.output_box, self.recap_box]:
            box.delete("0.0", "end")
        self.story_box.insert("0.0", "Welcome to the standalone MAGIC TUTOR app!\n\n"
                              "• Pick a lesson on the left\n"
                              "• Or type any question in the bottom bar\n"
                              "• Click 'WATCH LIVE TYPING' to see the code appear like magic\n"
                              "• Hit 'RUN IN REAL LIFE' to actually execute it\n\n"
                              "All examples are saved in the examples/ folder.")
        self.recap_box.insert("0.0", "Real code.\nReal stories.\nReal execution.\n\nNo boring theory — only things you can actually use.")
        self.update_idletasks()  # force clean paint

    def load_lesson(self, key: str):
        try:
            lesson = LESSONS[key]
            self.current_lesson = lesson
            self.current_code = lesson["code"]

            # Prevent extremely long titles from breaking the UI layout
            display_title = lesson["title"]
            if len(display_title) > 90:
                display_title = display_title[:87] + "..."
            self.topic_label.configure(text=display_title)
            self.story_box.delete("0.0", "end")
            self.story_box.insert("0.0", lesson["story"])
            self.story_box.see("0.0")

            self.mission_box.delete("0.0", "end")
            self.mission_box.insert("0.0", lesson["mission"])

            self.code_box.delete("0.0", "end")
            self.code_box.insert("0.0", lesson["code"])

            self.recap_box.delete("0.0", "end")
            self.recap_box.insert("0.0", lesson["recap"])

            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", 
                "✅ Lesson loaded.\n\n"
                "Use the 'WATCH LIVE TYPING' and 'RUN IN REAL LIFE' buttons to interact with the code.")
            self.output_box.see("0.0")

            self.update_idletasks()
        except Exception as e:
            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", f"Error loading lesson: {str(e)}")

    def _ask_anything_dialog(self):
        # Simple dialog for free text
        dialog = ctk.CTkInputDialog(text="What Python or dev concept do you want explained?", title="Ask MAGIC TUTOR")
        query = dialog.get_input()
        if query:
            if len(query) > 200:
                query = query[:197] + "..."
            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", f"Processing question: {query} ...")
            self.update_idletasks()
            self._process_query(query)

    def ask_free(self):
        query = self.query_entry.get().strip()
        if query:
            # Prevent extremely long inputs from causing display/loop issues
            if len(query) > 200:
                query = query[:197] + "..."
            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", f"Processing question: {query} ...")
            self.update_idletasks()
            try:
                self._process_query(query)
            except Exception as e:
                self.output_box.delete("0.0", "end")
                self.output_box.insert("0.0", f"Error processing: {str(e)}")
            self.query_entry.delete(0, "end")

    def _process_query(self, query: str):
        lesson = get_lesson(query)
        self.current_lesson = lesson
        self.current_code = lesson["code"]

        # Prevent extremely long titles from breaking the UI layout
        display_title = lesson["title"]
        if len(display_title) > 90:
            display_title = display_title[:87] + "..."
        self.topic_label.configure(text=display_title)
        self.story_box.delete("0.0", "end")
        self.story_box.insert("0.0", lesson["story"])
        self.story_box.see("0.0")

        self.mission_box.delete("0.0", "end")
        self.mission_box.insert("0.0", lesson["mission"])

        self.code_box.delete("0.0", "end")
        self.code_box.insert("0.0", lesson["code"])

        self.recap_box.delete("0.0", "end")
        self.recap_box.insert("0.0", lesson["recap"])

        # Give a clear visible response in the output area
        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", 
            f"✅ Response for your question about '{query}':\n\n"
            f"Lesson: {lesson['title']}\n\n"
            "The story, mission, and code are shown in the panels above.\n"
            "Click 'WATCH LIVE TYPING' to see the animation, or 'RUN IN REAL LIFE' to execute it.\n"
            "(Desktop GUI - for mobile use the mobile.html PWA)")
        self.output_box.see("0.0")

        self.update_idletasks()  # Force the UI to refresh immediately so user sees the change

    def animate_code(self):
        if not self.current_code:
            messagebox.showinfo("MAGIC TUTOR", "Load a lesson or ask something first!")
            return

        self.code_box.delete("0.0", "end")
        self.animate_btn.configure(state="disabled", text="TYPING...")

        def type_char(index=0):
            if index < len(self.current_code):
                self.code_box.insert("end", self.current_code[index])
                self.code_box.see("end")
                self.after(TYPING_DELAY_MS, type_char, index + 1)
            else:
                self.animate_btn.configure(state="normal", text="▶ WATCH LIVE TYPING")

        type_char()

    def run_code(self):
        if not self.current_code:
            messagebox.showinfo("MAGIC TUTOR", "No code to run!")
            return

        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", "Running in real life...\n")

        # Write to temp file and execute
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
                tmp.write(self.current_code)
                tmp_path = tmp.name

            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            if result.stderr:
                output += "\n[ERROR]\n" + result.stderr

            self.output_box.delete("0.0", "end")
            self.output_box.insert("0.0", output or "(no output)")

            os.unlink(tmp_path)
        except Exception as e:
            self.output_box.insert("end", f"\nFailed to run: {e}")

    def save_example(self):
        if not self.current_lesson or not self.current_code:
            messagebox.showwarning("MAGIC TUTOR", "Nothing to save yet!")
            return

        os.makedirs(EXAMPLES_DIR, exist_ok=True)
        path = os.path.join(EXAMPLES_DIR, self.current_lesson["filename"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.current_code)

        messagebox.showinfo("MAGIC TUTOR", f"Saved to {path}\nYou can open and edit it anytime!")

    def run(self):
        self.mainloop()

def main():
    # Ensure dependency is present (in case of broken install)
    try:
        import customtkinter  # noqa
    except ImportError:
        print("ERROR: customtkinter is required for the GUI.", file=sys.stderr)
        print("Please run: pip install customtkinter", file=sys.stderr)
        try:
            import tkinter.messagebox as mb
            import tkinter as tk
            r = tk.Tk(); r.withdraw()
            mb.showerror("MAGIC TUTOR", "customtkinter is not installed.\n\nRun this in your terminal:\npip install customtkinter\n\nThen try 'magic-tutor' again.")
            r.destroy()
        except:
            pass
        sys.exit(1)

    try:
        app = MagicTutorApp()
        app.run()
    except Exception:
        import traceback
        import sys
        error_msg = traceback.format_exc()
        # Write to log file so user can see what went wrong even if no console
        try:
            with open("magic_tutor_crash.log", "w", encoding="utf-8") as f:
                f.write("MAGIC TUTOR crashed on startup:\n\n")
                f.write(error_msg)
            # Try to show a message box if possible
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "MAGIC TUTOR - Startup Error",
                f"The app failed to start.\n\n"
                f"A crash log has been saved to:\n{os.path.abspath('magic_tutor_crash.log')}\n\n"
                f"Error summary:\n{error_msg.splitlines()[-1] if error_msg else 'Unknown error'}"
            )
            root.destroy()
        except Exception:
            pass
        # Re-raise so launcher sees the error
        print("MAGIC TUTOR crashed. See magic_tutor_crash.log for details.", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()