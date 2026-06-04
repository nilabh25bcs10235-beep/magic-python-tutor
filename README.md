# 🪄 MAGIC TUTOR

**A standalone colorful desktop application** with a big tekky header, modern dark UI, live code typing animations, and real executable examples.

It explains **any** Python or dev concept like you're 5 — using real-world problem solving missions (shopping lists for mom, lemonade stands, video games, undo buttons, robot helpers, etc.).

Just ask in plain English. Watch the code appear with live animation. Run it for real. Save the working examples.

## Big Tekky Header Experience
- Huge "MAGIC TUTOR" neon header
- Cyan / magenta / green cyber color scheme
- Sidebar with lessons + "ASK ANYTHING"
- Live typing animation button (code types char-by-char in the app)
- One-click "RUN IN REAL LIFE" that actually executes the code
- All examples saved to `examples/` folder

## Quick Start (from GitHub)

### Best way — Install as a real application

```powershell
pip install git+https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git
magic-tutor
```

This gives you the full colorful desktop GUI app with the big **MAGIC TUTOR** header.

## Features

- **Conversational GUI**: Type any question in the bottom bar or use the sidebar
- **Real-world missions** every time (shopping for mom, games, lemonade stands, robots...)
- **Live code animation**: Big "WATCH LIVE TYPING" button — code appears char-by-char in the app
- **It actually runs**: "RUN IN REAL LIFE" button executes the code and shows output in a console panel
- **Beautiful standalone UI**: Dark tekky colors (cyan/magenta/green), big "MAGIC TUTOR" header, modern widgets
- **Save real files**: Every example is saved as a proper .py you can open and modify later
- **Fully usable from GitHub**: `pip install git+...` then just run `magic-tutor` to launch the desktop app

## Quick Start (from GitHub)

### Best: Install as a real desktop app (recommended)

```powershell
pip install git+https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git
magic-tutor
```

This launches the full colorful GUI with the giant **MAGIC TUTOR** header.

### Alternative: Run from source

```powershell
git clone https://github.com/nilabh25bcs10235-beep/magic-python-tutor.git
cd magic-python-tutor
pip install -e .
magic-tutor
```

## How to use the GUI app

- Left sidebar: Click any lesson or the big **✨ ASK ANYTHING** button.
- Bottom bar: Type a question and hit **ASK MAGIC TUTOR** (e.g. "how do functions work in games").
- **▶ WATCH LIVE TYPING** — the code types itself out in the app like real magic.
- **⚡ RUN IN REAL LIFE** — actually executes the code and shows the live output.
- **💾 SAVE EXAMPLE** — saves a real runnable .py file in the `examples/` folder.

The whole experience now feels like a proper standalone application with its own neon color UI.

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
