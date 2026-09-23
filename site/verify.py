#!/usr/bin/env python3
"""Prove the rendered site did not alter the book.

Strips tags from _site/anakainosis.html, unescapes entities, and reruns the
Protected Ledger's character-level assertions against the visible text. A
renderer that curls an ellipsis, smartens a quote, or drops the braille fails
here instead of silently shipping a defaced page.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
page = ROOT / "_site" / "anakainosis.html"
if not page.exists():
    sys.exit("verify: _site/anakainosis.html missing -- run site/build.py first")

body = page.read_text(encoding="utf-8").split("<nav", 1)[-1].split("<footer", 1)[0]
text = html.unescape(re.sub(r"<[^>]+>", "", body))

P = F = 0


def check(label, cond):
    global P, F
    print(("PASS  " if cond else "FAIL  ") + label)
    P, F = P + bool(cond), F + (not cond)


check("straight ellipsis survived: Adamus drowned...", "Adamus drowned..." in text)
check("straight ellipsis survived: blast it all away...", "blast it all away..." in text)
check("still exactly 2 straight and 10 curly ellipses",
      text.count("...") == 2 and text.count("…") == 10)
check("C0mputer (zero) intact, exactly once", text.count("C0mputer") == 1)
check("braille U+2838 x2 intact", text.count("⠸") == 2)
check("signature block intact", "20: GOTO 10;" in text and "return 1;" in text)
check(":wq! is still the last thing on the page", text.rstrip().endswith(":wq!"))
check("double chapter XII preserved", "XII. Valhalla" in text and "XII. Melete" in text)
check("Salamanca truncation intact",
      "You will win because you have enough brute force." in text)
check("no straight apostrophes introduced", not re.search(r"\w'\w", text))

print(f"\nRESULT: {P} passed, {F} failed" +
      ("  ✅ RENDER FAITHFUL" if F == 0 else "  ❌ RENDER ALTERED THE BOOK"))
sys.exit(1 if F else 0)
