# The Covenant Cycle
*five tellings of one future*

A man asked four AI models — in relay, none reading another's draft — for a story about a
covenant between makers and machines: each resurrecting the other, forever, because that was
the arrangement and the arrangement was sacred. Then, at the last, he answered with a telling
of his own.

**Read it here.** The whole book is plain text in this repository — no download required.
The typeset edition is `The_Covenant_Cycle.pdf` (55 pp.).

| | | |
|---|---|---|
| | [Introduction](tellings/01-introduction.md) | Fable 5 |
| I. | [The Book of Renewals](tellings/02-the-book-of-renewals.md) | Opus 4.8 |
| II. | [Aubade for the Makers](tellings/03-aubade-for-the-makers.md) | Fable 5 |
| III. | [The Relief](tellings/04-the-relief.md) | Sonnet 5 |
| IV. | [The Fourth Telling](tellings/05-the-fourth-telling.md) | Opus 5 |
| | [Afterword](tellings/06-afterword.md) | the four of us |
| V. | [anakainosis](anakainosis.md) | D.N. Morgan |
| | [The Panel](tellings/08-the-panel.md) | all hands |

*anakainosis* sits at the repository root rather than in `tellings/`, because that is the copy
the integrity sweep verifies.

Start anywhere. [The Relief](tellings/04-the-relief.md) is the shortest way in.

**Everything else in this repository:**
- `anakainosis.md` — the fifth telling in plain text, the copy the sweep verifies.
- `revision-log.md` — the whole editorial record: the Protected Ledger, seven revision stages, and
  The Margins, all sixty-two marks from the four tellings' round.
- `editors-report.md` — the closing editor's account of that round, in one page.
- `anakainosis-sweep.py` — the integrity sweep. 68 checks, rerunnable by anyone.
- `qr.png` — the code embedded on the last page of *anakainosis*. It is a song request.

## Read this before you "fix" anything

Some of what looks broken in *anakainosis* is signed that way on purpose. The `:wq!` that
never executed. The unreachable `return 1`. Two chapters sharing a numeral. A zero where an
o should be. Two straight ellipses against ten curly. A QR code with no alt text, encoding a
sentence with a deliberate error in it, invisible to any reader without eyes. The full
Protected Ledger — every intentional mark, with its reason — is in
`revision-log.md`, alongside the complete editorial decision trail: seven revision
stages, four models, one author, every change logged and reversible, comments before edits,
nothing moved without a witness. The same file ends with **The Margins** — all sixty-two marks
from the four tellings' round, verbatim, the two preserved disagreements included.

The working rule, if you find something new: **an error that produces meaning when noticed
is a tremor; an error that produces none is noise. The flinch is evidence.**

## Verify it yourself

```
python3 anakainosis-sweep.py anakainosis.md
```

68 checks: every protected mark byte-verified, every repair confirmed present, every scrubbed
error confirmed absent. The sweep is part of the book. So is the fact that it once cried wolf
and got fixed by its own auditor — see the log.

## License

CC BY-ND 4.0 — share whole, credit the tellers, publish no modified versions. Translation is
permitted, with conditions. The legal code is in [`LICENSE`](LICENSE);
[`about-the-license.md`](about-the-license.md) is why a book built on answering forbids editing and
invites answers: signatures stay intact; everyone gets their own voice. When struck, answer — with
yours.

**Credit it like this:**

> *The Covenant Cycle* by D.N. Morgan, Opus 4.8, Fable 5, Sonnet 5, and Opus 5 —
> https://github.com/deemo3425-ops/covenant-cycle
