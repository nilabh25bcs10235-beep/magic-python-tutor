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
- **Mobile PWA (no terminal on phone)**: Open `mobile.html` in your phone browser → "Add to Home Screen". Fully works offline.
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
├── gui.py              # Desktop GUI app (customtkinter) — launched by `magic-tutor`
├── mobile.html         # Mobile PWA version (installable on phone home screen, no terminal)
├── manifest.json       # PWA manifest for mobile install
├── sw.js               # Service worker for offline PWA
├── magic_tutor.py      # Original rich terminal version (fallback)
├── magic_typer.py      # Reusable typing animation engine
├── pyproject.toml      # Packaging + entry point
├── README.md
├── LICENSE
└── examples/           # Generated example scripts (gitignored)
```

## Making it your own / contributing ideas

- Change typing speed in the app with the `speed` command
- Edit the explainers in `magic_tutor.py` (the KNOWN_CONCEPTS and smart_real_world_fallback)
- The animation engine in `magic_typer.py` is reusable

## Why this exists

Built to teach Python concepts (and dev ideas) in the most accessible, visual, "build it yourself and watch it run" way possible — exactly like explaining to a 5-year-old while still being real and useful.

Enjoy learning by doing!

---

## Install on Mobile (Android / iOS) — No Terminal Needed on the Phone

You can run a mobile-friendly version of **MAGIC TUTOR** directly on your phone or tablet as a real app icon, completely offline after the first load.

### Steps (takes 30 seconds)

1. On your **phone**, open this link in Chrome (Android) or Safari (iOS):
   - Direct file: https://raw.githubusercontent.com/nilabh25bcs10235-beep/magic-python-tutor/main/mobile.html

2. Once it loads, tap the **menu / share button** in your browser:
   - Android Chrome → "Add to Home screen"
   - iOS Safari → "Add to Home Screen"

3. It will appear as a normal app with the big **MAGIC TUTOR** header. Works fully offline.

### What you get on mobile
- Big tekky "MAGIC TUTOR" header
- Same real-world stories and lessons
- "Watch Live Typing" animation (JavaScript version)
- "Run in Real Life" shows the expected output
- "Ask Anything" works with simple matching

**Note**: The full Python code execution is desktop-only (for safety and power). On mobile you get the explanations + simulated output, which is perfect for learning on the go.

### Advanced: Full local offline (optional)
If you want it completely local without using GitHub:
- Download `mobile.html` + `manifest.json` + `sw.js` from the repo onto your phone storage.
- Open `mobile.html` in your browser and add to home screen.

This gives you a true local install experience with zero terminal commands on the mobile device itself.

---

**To use through GitHub**: Clone or pip install directly from the repo as shown above. No need to download zip manually.
