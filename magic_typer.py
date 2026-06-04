"""
Magic Typer - Makes code appear like it's being typed by a friendly robot friend!
Use this to show code being built slowly, like magic for kids (and grown-ups who want to see every step).
Like I'm explaining to a 5 year old.

Now enhanced with rich for beautiful panels, colors, and professional look.
"""

import time
import sys
import os
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

def clear_screen():
    """Clear the screen so it feels fresh, like a new page in a coloring book."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')

def get_console(console: Optional["Console"] = None) -> "Console":
    """Get a rich console or create one."""
    if console is not None:
        return console
    if RICH_AVAILABLE:
        return Console()
    # Fallback dummy if no rich (shouldn't happen)
    class DummyConsole:
        def print(self, *a, **k): print(*a)
        def rule(self, *a, **k): print("-" * 50)
    return DummyConsole()

def magic_type(text: str, delay: float = 0.03, start_delay: float = 0.4, 
               end_pause: float = 0.6, show_cursor: bool = True,
               console: Optional["Console"] = None) -> None:
    """
    Types out text ONE CHARACTER AT A TIME with a moving ▌ cursor.
    This is the heart of the 'automatic cursor and automatic typing' magic.
    Works great even when rich is drawing panels around it.
    """
    time.sleep(start_delay)
    cursor = "▌"
    
    if not show_cursor:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay * (2.0 if char == "\n" else 1.0))
        time.sleep(end_pause)
        sys.stdout.write("\n")
        sys.stdout.flush()
        return
    
    # Live cursor effect using carriage return (beautiful in real terminal)
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        current_line = ""
        for char in line:
            current_line += char
            sys.stdout.write("\r" + current_line + cursor)
            sys.stdout.flush()
            time.sleep(delay)
        # Commit the finished line
        sys.stdout.write("\r" + current_line)
        sys.stdout.flush()
        if idx < len(lines) - 1:
            sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(delay * 1.8)
    
    sys.stdout.write("\n")
    sys.stdout.flush()
    time.sleep(end_pause)

def magic_type_code_block(code: str, title: str = "✨ Watch the code come to life...", 
                          delay: float = 0.028, show_cursor: bool = True,
                          console: Optional["Console"] = None) -> None:
    """
    The star feature: shows code being typed live with cursor + beautiful rich panel.
    After the live typing, shows a clean highlighted version.
    """
    c = get_console(console)
    
    c.rule(f"[bold cyan]{title}[/]", style="cyan")
    c.print()
    
    # Do the magical live typing (cursor animation)
    magic_type(code, delay=delay, show_cursor=show_cursor, console=c)
    
    c.print()
    c.rule(style="cyan")
    
    # After animation, show beautiful syntax highlighted version
    if RICH_AVAILABLE:
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True, word_wrap=True)
        c.print(Panel(syntax, title="[green]📜 Clean Version (for reading)[/]", 
                      border_style="green", padding=(0,1)))
    else:
        c.print("\n[Clean version]\n" + code)
    
    c.print("\n[bold yellow]🚀 Now let's run this real program and see what happens![/]\n")

def type_and_run(code: str, filename: str = "demo.py", delay: float = 0.028, 
                 run_after: bool = True, show_cursor: bool = True,
                 console: Optional["Console"] = None,
                 examples_dir: str = "examples") -> str:
    """
    1. Beautiful animated typing of the code (with cursor!)
    2. Saves it to a REAL file in examples/ folder
    3. Executes it so you see the concept solving a real problem
    This is 'real life building'.
    """
    c = get_console(console)
    
    # Ensure examples dir exists
    os.makedirs(examples_dir, exist_ok=True)
    full_path = os.path.join(examples_dir, filename)
    
    magic_type_code_block(code, delay=delay, show_cursor=show_cursor, console=c)
    
    # Save the real file
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    c.print(Panel(f"[bold green]✅ Saved real file:[/]\n[dim]{os.path.abspath(full_path)}[/]", 
                  border_style="green", title="Real Life Artifact"))
    
    if run_after:
        c.print("[bold magenta]▶ Running the program now...[/]\n")
        time.sleep(0.4)
        
        # Better than os.system: capture output
        import subprocess
        try:
            result = subprocess.run(
                [sys.executable, full_path],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\n[stderr]\n" + result.stderr
            
            if RICH_AVAILABLE:
                c.print(Panel(output or "(no printed output)", 
                              title="[cyan]📤 Program Output[/]", 
                              border_style="bright_blue", padding=(1,2)))
            else:
                print(output)
        except Exception as e:
            c.print(f"[red]Error running: {e}[/]")
    
    return full_path

def simple_story_intro(thing_name: str, story: str, console: Optional["Console"] = None):
    """Tell a tiny story so a 5-year-old gets it instantly. Now with rich styling."""
    c = get_console(console)
    c.print()
    c.rule(f"[bold yellow]🧸  {thing_name}[/]", style="yellow")
    c.print(Panel(story, border_style="yellow", padding=(1, 2)))
    c.rule(style="yellow")
    time.sleep(0.8)

def thinking_animation(message: str = "The magic robot is thinking of the best real-world example...", 
                       console: Optional["Console"] = None, duration: float = 1.2):
    """Nice 'thinking' feedback using rich status."""
    c = get_console(console)
    if RICH_AVAILABLE:
        with c.status(f"[cyan]{message}[/]", spinner="dots"):
            time.sleep(duration)
    else:
        print(message)
        time.sleep(duration)

# --- Clean self-test (uses rich if available) ---
if __name__ == "__main__":
    c = get_console()
    clear_screen()
    c.print("[bold cyan]✨ Magic Typer Self-Test (rich-enhanced)[/]\n")
    
    demo_code = '''# Magic toy box - adding things one by one
toy_box = []
toy_box.append("teddy bear")
toy_box.append("robot")
print("Box now contains:", toy_box)
print("First toy:", toy_box[0])'''
    
    type_and_run(demo_code, filename="typer_self_test.py", 
                 delay=0.032, console=c, examples_dir=".")