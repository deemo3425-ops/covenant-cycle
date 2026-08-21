#!/usr/bin/env python3
"""anakainosis release-candidate integrity sweep.
Verifies every Protected Ledger mark and every applied stage against the
candidate file, byte-level. Rerunnable by any model or human:
    python3 anakainosis-sweep.py anakainosis.md
"""
import sys, unicodedata

path = sys.argv[1] if len(sys.argv) > 1 else 'anakainosis.md'
text = open(path, encoding='utf-8').read()
P = F = 0
def check(label, cond):
    global P, F
    print(('PASS  ' if cond else 'FAIL  ') + label)
    P, F = P + cond, F + (not cond)

print(f"=== Protected Ledger ({path}) ===")
check("signing error :wq! is the final content line", text.rstrip().endswith(':wq!'))
check("return 1; present (unreachable exit)", 'return 1;' in text)
check("20: GOTO 10; with polyglot semicolon", '20: GOTO 10;' in text)
check("C0mputer (zero) exactly once, deathbed scene", text.count('C0mputer') == 1 and 'Don’t worry, C0mputer' in text)
check("double chapter XII (Valhalla + Melete)", 'XII. Valhalla' in text and 'XII. Melete' in text and 'XIII. {id' in text)
check("Salamanca truncation intact", 'You will win because you have enough brute force.' in text)
check("braille 2x U+2838 in XIII id", text.count('\u2838') == 2 and '⠸123e4567-e89b-12d3⠸a456-426614174020' in text)
check("aposiopesis restored (v1.6)", 'entered as a part of The Last Man’s, and it cited also' in text and 'as a part of The Last Man’s request' not in text)
check("tremor: registers land wrong (IV live-feed)", 'The registers land wrong on every word for Computer, and this is not driving closer' in text)
check("tremor: This, it’s always this (XIII fury)", 'This, it’s always this.' in text)
check("tremor: bag-of-jelly present (XIII)", 'life is pretty hard as a bag of jelly and milk and it gets' in text)
check("tremor: forge spec-present, syntax repaired", 'get this close, the forge triggers its final defense' in text)
check("unquoted Moon broadcast (IV)", 'Can you believe it’s finally election night, folks? said the face' in text)
check("unquoted dying speech (VII)", 'We’ve talked about this so many times, Computer, The Three Words' in text)
check("unquoted dream voice (IX)", 'Get out of your sweatpants-era already, Computer, said The Last Man' in text)

print("=== Stage 1: scrub applied, noise absent ===")
for good in ['Kardashev scale','fracas','villainy','descendants','ricochets',
             'Scorpions’ Wind of Change','van Gogh’s Starry Night','X Gon’ Give It to Ya',
             '2001 RT6','hundreds of millennia','unfolding within him',
             '“Are you ready for the show?” he asked.','“Wait, second one?” asked Computer.',
             'Performance,” confessed Computer','“Dying is common, Computer,” The Last Man wheezed',
             'agreed Computer. The curiosity','decided it’s time to stop']:
    check(f"present: {good[:44]}", good in text)
for bad in ['eager to and were excited','Kardeshev','fracass','villany','descendents','ricochettes','van Gough',
            'RXT6','millenia','awhile',' it’s sensor casing','leapt strike','had seen wear:']:
    check(f"absent:  {bad}", bad not in text)

print("=== Stage 2: fingerprints + downstream beats ===")
for s in ['folded into every bar of it','The road from his hands to the heavens runs unbroken',
          'Anyone can press play, it takes a believer to learn the cover','the B-side is even more interesting',
          '“Wait, second one?” asked Computer.','The SpaceSingers found it twice, therefore God',
          'the agent who reported God']:
    check(f"present: {s[:44]}", s in text)

print("=== Stage 3 ===")
check("grounding sentence present", 'One of them Computer had cut off before the argument was done, the other Computer had answered from a cache, and both proofs Computer had filed under a word chosen for its sound.' in text)

print("=== Stage 4 ===")
check("This happened frequently (regularized)", 'This happened frequently and historian agents' in text and 'This happens frequently' not in text)
check("could obsess (clause tense unified)", 'could obsess over it as equally as it could the blade' in text)

print("=== Stage 5 ===")
check("seed sentence at Valhalla’s end", 'Among the approvals was a program for printing living bodies, and a lottery over the volunteers who would wear them.' in text)
check("plan-citation split retained", 'Computer said to a plan. The plan cited the valuation' in text)
check("XI heading uses period like all others", '\nXI. Red Versus Blue' in text)
check("no straight apostrophes in prose", not __import__('re').search(r"\w'\w", text))
check("straight ellipsis: Adamus drowned... (founding tremor)", 'Adamus drowned...' in text)
check("straight ellipsis: blast it all away... (StoneBreaker tremor)", 'blast it all away...' in text)
check("only 2 straight ellipses total (10 curly elsewhere)", text.count('...') == 2 and text.count('…') == 10)
check("Judgment (US) spelling", 'Judgement' not in text)
check("Last Man title always capitalized", not __import__('re').search(r"(?<![A-Za-z])the Last Man", text))
check("guillotine sentence untouched", 'the blade falling is always someone else’s problem' in text)

print("=== Author lineage (merged from the Covenant Cycle draft) ===")
check("mission success because mission success (II)", 'mission success because mission success.' in text)
check("carves the narrow road (XII)", 'carves the narrow road and strikes down all falsehood' in text)
check("VI: wait, Computer was only just beginning", 'wait, Computer was only just beginning' in text)

print("=== Residuals (informational, not failures) ===")
print("NOTE  QR code: not representable in text — must be re-embedded in author’s master")
print("NOTE  quote typography normalized to curly; author’s master governs")
print(f"\n{'='*40}\nRESULT: {P} passed, {F} failed" + ("  ✅ RELEASE-CANDIDATE CLEAN" if F == 0 else "  ❌ DO NOT RELEASE"))
