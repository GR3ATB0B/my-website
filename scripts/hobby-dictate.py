#!/usr/bin/env python3
"""Dictation capture for hobby page copy.

Walks through every hobby on whatthenash.com, one at a time. Talk (Wispr
Flow) or type as much as you want, press Enter on an empty line to move on.
Everything lands in hobby-notes.txt next to the repo root, saved after each
hobby, so quitting mid-run loses nothing. Re-running skips hobbies that are
already in the file.

Commands while capturing:
  skip   (alone on a line)  skip this hobby for now, comes back next run
  quit   (alone on a line)  save and exit
"""

import os
import re
import sys

# Mirrors the HOBBIES array in index.html
HOBBIES = [
    ("3d-printing", "🖨️", "3D Printing"),
    ("ai", "🤖", "AI"),
    ("camping", "⛺", "Camping"),
    ("coding", "💻", "Coding"),
    ("electronics", "🔌", "Electronics"),
    ("flower-making", "🌸", "Flower Making"),
    ("fly-fishing", "🎣", "Fly Fishing"),
    ("forging", "⚒️", "Forging"),
    ("lego", "🧱", "LEGO"),
    ("radio", "📻", "Radio"),
    ("math", "➗", "Math"),
    ("music", "🎵", "Music"),
    ("photography", "📷", "Photography"),
    ("rc", "🛩️", "RC"),
    ("reading", "📚", "Reading"),
    ("spanish-languages", "🗣️", "Spanish"),
    ("thrifting", "🛍️", "Thrifting"),
    ("weightlifting", "🏋️", "Weightlifting"),
]

OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hobby-notes.txt")
HEADER_RE = re.compile(r"^===== .* \(([a-z0-9-]+)\) =====$", re.MULTILINE)


def done_slugs():
    try:
        with open(OUT_FILE, encoding="utf-8") as f:
            return set(HEADER_RE.findall(f.read()))
    except FileNotFoundError:
        return set()


def capture(emoji, name):
    """Read lines until an empty line. Returns text, or 'skip'/'quit'."""
    print("\033[2J\033[H", end="")  # clear screen
    print("=" * 50)
    print(f"  {emoji}  {name.upper()}")
    print("=" * 50)
    print("Talk. Empty line = done. 'skip' or 'quit' alone also work.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            return "quit"
        stripped = line.strip()
        if stripped.lower() in ("skip", "quit") and not lines:
            return stripped.lower()
        if stripped == "":
            if lines:
                return "\n".join(lines).strip()
            continue  # ignore leading blank lines
        lines.append(line)


def main():
    done = done_slugs()
    todo = [(s, e, n) for s, e, n in HOBBIES if s not in done]
    if not todo:
        print(f"All {len(HOBBIES)} hobbies done. Notes in {os.path.normpath(OUT_FILE)}")
        return

    print(f"{len(done)} done, {len(todo)} to go. Ctrl+C anytime — progress saves per hobby.")
    input("Enter to start...")

    captured = 0
    for slug, emoji, name in todo:
        try:
            result = capture(emoji, name)
        except KeyboardInterrupt:
            result = "quit"
        if result == "quit":
            break
        if result == "skip":
            continue
        with open(OUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"===== {name.upper()} {emoji} ({slug}) =====\n{result}\n\n")
        captured += 1

    remaining = len(todo) - captured
    print(f"\nSaved {captured} this run. {remaining} remaining." if remaining else f"\nDone! All {len(HOBBIES)} captured.")
    print(f"Notes: {os.path.normpath(OUT_FILE)}")


if __name__ == "__main__":
    main()
