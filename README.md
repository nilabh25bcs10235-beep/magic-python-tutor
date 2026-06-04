# 🪄 Magic Python Tutor

An interactive terminal application that explains **any** Python or programming concept like you're 5 years old — using real-world problem solving stories, live automatic code typing animations (with moving cursor), and actual running programs.

Just ask a question in plain English. It builds a fun, kid-friendly real-life example (shopping for mom, lemonade stand business, video game, school play, toy shop, robot helper, drawing app undo, etc.), types out the solution code live with the magic cursor effect, saves it as a real `.py` file, runs it, and lets you ask follow-ups.

## Features

- **Conversational**: Type any question ("append", "how do dicts work", "explain functions for spells", "undo button", "loops in games"...)
- **Real-world missions** every time
- **Live code animation**: Watch the code being written character-by-character with ▌ cursor
- **It actually runs**: The program that solves the problem executes in front of you with nice output
- **Beautiful TUI**: Powered by rich (panels, colors, syntax highlighting, status animations, tables)
- **Follow-up friendly**: After a lesson, ask more, view the saved code, explore related ideas
- **Fully usable from GitHub**: Clone or `pip install` directly from the repo and get a `magic-tutor` command

## Quick Start (from GitHub)

### Option 1: Clone and run (recommended for first use)

```powershell
git clone https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git
cd magic-python-tutor
python magic_tutor.py
```

### Option 2: Install directly from GitHub (get `magic-tutor` command)

```powershell
pip install git+https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git
magic-tutor
```

(You can also `pip install -e .` after cloning for development.)

After install, just type `magic-tutor` from anywhere.

## How to use the app

Run it and type questions at the prompt:

```
🗣️  Ask me anything about Python or programming
> append
> how does pop work for undo
> explain dictionaries like a lemonade stand
> functions in a game
> what is enumerate
```

Special commands:
- `list` — see built-in concepts it explains especially well
- `speed` — adjust the typing animation speed (lower = slower/more magical)
- `help`
- `clear`
- `quit`

After every lesson you get options to ask follow-ups, see the saved real code, etc.

All demos you see are saved in an `examples/` folder (ignored by git so your experiments stay private).

## Requirements

- Python 3.8+
- `rich` (the app will try to be nice even without it, but install for the full beautiful experience)

The `pyproject.toml` lists it as a dependency, so `pip install` from the repo will pull it.

## Project Structure

```
magic-python-tutor/
├── magic_tutor.py      # The main interactive app
├── magic_typer.py      # The reusable magic typing + cursor + rich animation engine
├── pyproject.toml      # Packaging + console script (magic-tutor command)
├── README.md
├── LICENSE
├── .gitignore
└── examples/           # Auto-generated when you use the app (gitignored)
```

## Making it your own / contributing ideas

- Change typing speed in the app with the `speed` command
- Edit the explainers in `magic_tutor.py` (the KNOWN_CONCEPTS and smart_real_world_fallback)
- The animation engine in `magic_typer.py` is reusable

## Why this exists

Built to teach Python concepts (and dev ideas) in the most accessible, visual, "build it yourself and watch it run" way possible — exactly like explaining to a 5-year-old while still being real and useful.

Enjoy learning by doing!

---

**To use through GitHub**: Clone or pip install directly from the repo as shown above. No need to download zip manually.
