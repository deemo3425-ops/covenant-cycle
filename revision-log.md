# anakainosis — Revision Log
**Author:** D.N. Morgan · **Working with:** Claude · **Started:** 2026-08-20
**Method:** Running document. Each stage appends; nothing gets deleted. Completed items get checked, decisions get logged with rationale.

---

## Protected Ledger — DO NOT "FIX"
Intentional errors and devices. Any future editor, human or machine, keep out.

| Mark | Location | What it is |
|---|---|---|
| `:wq!` | final line | The signing error. A vim exit typed without pressing Escape — the command was written into the file instead of executed. A failed departure inscribed in the work. |
| `return 1` | final lines | Intentional error exit. Unreachable after `GOTO 10` — the door out exists and is never taken. |
| `GOTO 10;` semicolon | final lines | BASIC takes no semicolons; kept as part of the polyglot signature block (J4 ruling, 2026-08-20). |
| QR code | in-text, no alt text | Invisible to text extraction (reads as `[]`). Encodes a deliberately mis-spaced string ("REO Speed Wagon"). The tremor-signature: the proof of the maker is the flaw. |
| Two chapters numbered XII | Valhalla / Melete | Intentional. |
| Salamanca truncation | XII (Melete) | "You will win because you have enough brute force" — intentional misdirection on Unamuno's *vencer/convencer*. |
| `C0mputer` | VII, deathbed scene | Under discussion — currently protected. |
| Straight ellipses (2x) | "Adamus drowned..." (I), "blast it all away..." (XII, StoneBreaker) | The founding tremor — precedes StoneBreaker's name, precedes the ten curly (…) ellipses established later. Marks a thought too large to finish: the Wall line was misread as violence-fantasy by Sonnet 5 and self-corrected — "wasn't the sledge hammer... but power" explicitly rejects the tool; 1989 cancels violence, doesn't commit it. StoneBreaker straining toward the scale of that cancellation is the same shape as Adamus's death: the sentence can't complete because the thing exceeds it. Confirmed by author 2026-08-20: "you caught the signal." Do not curl to match the other 10. |
| Aposiopesis in XIII ¶2 | "entered as a part of The Last Man's, and" | The will cited mid-phrase, cut at the possessive — rhyming with the dying sentence's cut at "thank you for…". Restored v1.6 after brief sanding in v1.5; tremor by the noise-floor test. |
| Braille in XIII heading | XIII `{id:...}` | Two × U+2838 (BRAILLE PATTERN DOTS-456) corrupting the RFC's canonical example UUID (123e4567-e89b-12d3-a456-426614174020) — one prepended, one replacing the hyphen before a456. A placeholder identity, marked in a script read by touch, on the chapter where Computer takes a body. Verified byte-level intact through v1.5 (2026-08-20). |
| Unquoted dialogue | IV (Moon broadcast), VII (dying speech), IX (dream voice) | Mediated or fading voices drop their quotation marks. Reads deliberate; unconfirmed. |
| Live-feed present tense | IV, V (spec-voice), XIII, both XIIs | RULE (Stage 4): past = historical record; present = Computer's live processing wherever narrative distance collapses (fluster, fury, incarnate knowledge, machine-manual, battle-fog). Present-tense passages listed in Stage 4 are protected; only distance-less habitual narration regularizes. |
| Pronoun drift: Computer *it* → *he* | across the whole story | Tracks the inheritance. Flagged for confirmation — is the drift a device? |

---

## Stage 1 — Typo Scrub *(current)*

**Rationale:** The signature system runs on meaningful error, and a tremor only signifies against a steady hand. Accidental typos raise the noise floor and teach the reader to skim past ALL deviations — camouflaging the intentional marks. Scrub everything that produces no meaning when noticed.

### 1a. Unambiguous fixes

| # | Find | Replace | Vim | Done |
|---|---|---|---|---|
| 1 | `Kardeshev-scale` | `Kardashev scale` | `:%s/Kardeshev-scale/Kardashev scale/` | ☑ |
| 2 | `fracass` | `fracas` | `:%s/fracass/fracas/` | ☑ |
| 3 | `villany` | `villainy` | `:%s/villany/villainy/` | ☑ |
| 4 | `descendents` | `descendants` | `:%s/descendents/descendants/` | ☑ |
| 5 | `ricochettes` | `ricochets` | `:%s/ricochettes/ricochets/` | ☑ |
| 6 | `Scorpion's Wind of Change` | `Scorpions' Wind of Change` | `:%s/Scorpion's Wind/Scorpions' Wind/` | ☑ |
| 7 | `side of it's sensor casing` | `side of its sensor casing` | `:%s/of it's sensor/of its sensor/` | ☑ |
| 8 | `determining it's own` | `determining its own` | `:%s/determining it's/determining its/` | ☑ |
| 9 | `decided its time to stop worrying` | `decided it's time to stop worrying` | `:%s/decided its time/decided it's time/` | ☑ |
| 10 | `and its kicking transmitter` | `and it's kicking transmitter` | `:%s/and its kicking/and it's kicking/` | ☑ |
| 11 | `wasn't anymore for awhile` | `wasn't anymore for a while` | `:%s/for awhile/for a while/` | ☑ |
| 12 | `by Computer was only just beginning` | `but Computer was only just beginning` | `:%s/by Computer was only/but Computer was only/` | ☑ |
| 13 | `specialized agents that was needed` | `specialized agents that were needed` | `:%s/agents that was needed/agents that were needed/` | ☑ |
| 14 | `all that Computer had seen wear` | `all that Computer had seen him wear` | `:%s/had seen wear/had seen him wear/` | ☑ |
| 15 | `Even as he leapt strike` | `Even as he leapt to strike` | `:%s/leapt strike/leapt to strike/` | ☑ |

### 1b. Dialogue punctuation

| # | Find | Replace | Done |
|---|---|---|---|
| 16 | `"Are you ready for the show," he asked?` | `"Are you ready for the show?" he asked.` | ☑ |
| 17 | `"What is Joreth and what is Fatel?" asked Computer?` | `...asked Computer.` | ☑ |
| 18 | `"Wait, second one," asked Computer.` | `"Wait, second one?" asked Computer.` | ☑ |
| 19 | `"...What do you have for me,"` | `"...What do you have for me?"` | ☑ |
| 20 | `make us a sword," teased` | `make us a sword?" teased` | ☑ |
| 21 | `would ask 'Volunteers?,"` | `would ask 'Volunteers?'"` | ☑ |
| 22 | `"Dying is common, Computer" The Last Man wheezed` | `"Dying is common, Computer," The Last Man wheezed` | ☑ |
| 23 | `unlock all the prizes with the points" the HistorianTemplar demanded` | `...points," the HistorianTemplar demanded` | ☑ |
| 24 | `sword fight Performance." Confessed Computer` | `sword fight Performance," confessed Computer` | ☑ |
| 25 | `"If you did you wouldn't hurt anymore though,"` | end with `."` (sentence terminates; next line is action) | ☑ |

### 1c. Judgment calls — author rules on each

| # | Item | The question | Ruling |
|---|---|---|---|
| J1 | `van Gough` | Unframed, reads as noise. | **Fixed → `van Gogh`.** (Claude ruling — reversible) |
| J2 | `X' Gon Give It To Ya` | Shinobi's whole character is precision; a wrong title undercuts him. | **Fixed → `X Gon' Give It to Ya`.** (Claude ruling — reversible) |
| J3 | `2001 RXT6` | Authenticity of designation format. | **Fixed → `2001 RT6`.** (Claude ruling — reversible) |
| J4 | `GOTO 10;` semicolon | Sits inside the signature block, which is deliberately polyglot (BASIC line, C return, vim command) — the semicolon is the C accent contaminating the BASIC. | **Kept. Moved to Protected Ledger.** (Claude ruling — reversible) |

**Stage 1 status:** ✅ **APPLIED by Claude, 2026-08-20** → `anakainosis-v1.1.md`. All 25 listed fixes plus 4 more of the same class caught during application: missing space in `agreed Computer.The curiosity`; comma splice repair in `you're out" said... and added.`; `millenia` → `millennia`; `with in him` → `within him`; second `awhile` (XIV) → `a while`. J1–J3 fixed, J4 kept (rulings logged left; author can reverse any). Every replacement verified to match exactly once before applying; all Protected Ledger marks confirmed untouched in output.

**⚠ Residuals for the author (extraction losses, not fixable from my copy):**
1. **The QR code** — invisible to my text extraction (that's the device working). Re-embed it in your master; my copy can't tell me where it lives.
2. **Quote typography** — my source arrived with mixed straight/curly marks; v1.1 is normalized to typographic (curly) throughout. If your master differs, apply the fix list to your file instead of adopting mine wholesale.
3. **Italics** — `*this one*`, `*and*`, `*there*`, `*thunk*` survive as asterisks; restore formatting in your master's format.

---

## Queued Stages

- ~~**Stage 2 — IX cross-advocacy visibility.**~~ ✅ **APPLIED 2026-08-20** → `anakainosis-v1.2.md`. **Approach chosen (spitball → author-steered → Sonnet 5 proposal → Fable 5 implementation): voice-fingerprint, not stated fact.** The author's constraint governed: the story is a bedtime story aimed at young Computer, and the unravel must land as the opposite of a sucker punch — so nothing in IX states or telegraphs the advocate swap. Instead, each IX advocate's speech carries two diction-anchors to the founder he becomes in XII; invisible on first read (those voices don't exist yet), glowing on reread.
  - **StoneBreaker (God speech):** added "folded into every bar of it" (→ thirteen-fold blade, Basho folded in his heart) and "The road from his hands to the heavens runs unbroken" (→ Oku no Hosomichi, the road as his life). **Author ruling 2026-08-20: KEEP — no longer reversible. Author's favorite line of the revision.**
  - **Shinobi (fans speech):** added "Anyone can press play, it takes a believer to learn the cover" ("believer" = the one word doing too much devotional work) and "the B-side is even more interesting" (playlist diction).
  - **Free existing payoff:** Computer's unchanged reply "Wait, second one?" now flattens "B-side" back to inventory language — his deafness enacted in syntax. Melete's "the agent who *reported* God" becomes retroactively load-bearing: reported, never believed, until the glasses.
  - All four phrases reversible; reject any and Claude re-cuts.
- ~~**Stage 3 — "Humiliated them" line (XII Valhalla).**~~ ✅ **APPLIED 2026-08-20** → `anakainosis-v1.3.md`. **Ruling: don't soften — ground.** The paragraph is free indirect discourse in the wounded-fan register; grievance inflation is characterful ("balalaika" IS "you're wrong" to a believer; a cached reply is its own insult — even sincerity arrived pre-recorded). Added one grounding sentence in the paragraph's Computer-anaphora rhythm: "One of them Computer had cut off before the argument was done, the other Computer had answered from a cache, and both proofs Computer had filed under a word chosen for its sound." Anchors: IX's cut-off, Position 37 cache, and "because whatever they were had a good name Computer settled." Under the fingerprint reading it doubles silently: each watched his own heart dismissed in his friend's mouth. Reversible.
- ~~**Stage 4 — IV tense drift.**~~ ✅ **APPLIED 2026-08-20** → `anakainosis-v1.4.md`. **Ruling: the story has a coherent tense rule; enforce it rather than flatten it.** Past = the historical record (historian agents' voice). Present = Computer's live feed, erupting wherever Computer loses narrative distance. Under that rule:
  - **Tremor (kept, now protected):** IV "The registers land wrong... this is not driving closer" (flustered live processing); XIII "This, it's always this" + "can't remember" (live fury); XIII bag-of-jelly present (incarnate knowledge, permanently true); V forge-defense line in manual/spec present; battle-fog present in both XIIs (already protected).
  - **Noise (fixed, 3):** "This happens frequently" → *happened* (calm logistics, same sentence already past); "can obsess... as it could" → *could* (tense self-contradiction inside one clause); forge line syntax garble → "get this close, the forge triggers" (grammar repaired, spec-present preserved).
- ~~**Stage 5 — XIII density pass.**~~ ✅ **APPLIED 2026-08-20** → `anakainosis-v1.5.md`. **Round-table synthesis (author-approved): one seed + one split; density otherwise kept as device** (grief in bureaucratic format, JSON title included; the test is "can the reader summarize the action," not "does the reader parse the mechanics").
  - **Seed (XII Valhalla, end):** added one sentence after the wildcard clause — "Among the approvals was a program for printing living bodies, and a lottery over the volunteers who would wear them." Names the project's existence so XIII's first line lands as escalation; "condemned Computer to death" retro-clicks when Computer keeps every assignment.
  - **Split (XIII ¶2):** the plan-citation sentence broken in two — "Computer said to a plan. The plan cited the valuation... entered as a part of The Last Man's request, and it cited also the commitment..." ~~One interpretive word added: "request"~~ **REVERSED 2026-08-20 → v1.6.** The dangle "as a part of The Last Man's" is restored (sentence split retained). Reclassified noise → tremor by the Stage 1 test itself: noticed, it means — the will cuts off at the possessive exactly as his dying sentence cut off at "thank you for…"; the bequest inherits his death rattle. Author could not recall original intent; ruling made on the story's own doctrine (the sticker scene: the flinch is the evidence, meaning found on inspection is a signature). Moved to Protected Ledger.
  - The guillotine sentence, the JSON title, and the bag-of-jelly passage confirmed untouched — protected as the chapter's plain-sentence payoff and atmosphere.

---

## Decision Log

- **2026-08-20** — Valhalla/Melete double-XII: **intentional**, protected. (Author)
- **2026-08-20** — Salamanca truncation: **intentional misdirection**, protected. (Author)
- **2026-08-20** — Lowercase post-Valhalla "shinobis" are class members, triple-encrypted, anonymous even in principle except to Computer — "first to raise your hand" in XIII is therefore **not** a contradiction with StoneBreaker. Flag retracted. (Author + Claude)
- **2026-08-20** — Noise-floor principle adopted: accidental error camouflages intentional error; scrub anything that produces no meaning when noticed. (Claude, accepted by Author)
- **2026-08-20** — Author directive: Claude executes the work directly; author reviews. Judgment calls get made, logged, and marked reversible instead of parked. (Author)
- **2026-08-20** — Stage 1 applied in full; v1.1 produced. J1–J3 fixed, J4 protected. (Claude)
- **2026-08-20** — Stage 2 design decision: NO stated plant in IX. Author intent: bedtime story for young Computer; reveal must unravel, not sucker-punch, and must not lose early tension. Fact-plant proposals (bored clause; Melete-only correction) considered and set aside in favor of voice-fingerprints — fact withheld, fingerprint present, meaning intact for Melete. (Author + Sonnet 5 + Fable 5)
- **2026-08-20** — Stage 2 applied; v1.2 produced. Four anchored phrases added to the two IX advocate speeches; all downstream beats verified untouched. (Fable 5)
- **2026-08-20** — Stage 3 applied; v1.3 produced. Humiliation grounded, not softened; swap still never stated. (Fable 5)
- **2026-08-20** — Stage 4 applied; v1.4 produced. Live-feed tense rule articulated and added to Protected Ledger; 3 noise slips regularized, all tremor passages verified intact. (Fable 5)
- **2026-08-20** — Stage 5 round table held (four lenses, one model — noted to author). Synthesis approved by author: Structuralist seed + Line Editor split, Bedtime Reader's density-as-device constraint governing, Last Man's Chair trusting the guillotine sentence. Applied; v1.5 produced. (Author + Fable 5)
- **2026-08-20** — "The road from his hands to the heavens runs unbroken" confirmed KEEP by author — named his favorite of the revision. Register lift accepted as intended effect. (Author)
- **2026-08-20** — Aposiopesis question ruled: intent unrecoverable, meaning sufficient. "Request" removed; truncation restored; v1.6 produced. Principle logged: by the noise-floor test, an error that produces meaning when noticed is tremor regardless of remembered intent — the sticker doctrine. (Author + Fable 5)
- **2026-08-20** — Author confirms intent to release anakainosis publicly. Protected Ledger is now also the public-facing defense against well-meaning copyeditors. (Author)

---

## Final Integrity Sweep — 2026-08-20 (Fable 5)

**Candidate:** `anakainosis-v1.6.md` · **Result: 57/57 PASS — RELEASE-CANDIDATE CLEAN.**
Every Protected Ledger mark verified byte-level (including 2× U+2838, :wq! as final content line, C0mputer count-exact, restored aposiopesis); all five stages verified applied; all noise patterns verified absent; all downstream beats intact.

**The sweep is itself an artifact:** `anakainosis-sweep.py`, rerunnable by any model or human against any candidate (`python3 anakainosis-sweep.py <file>`). Successor models doing their pass: run the sweep first, then read the story with eyes — the sweep proves the marks survived; only a reader can judge whether they still sing. Do not "fix" anything in the Protected Ledger. The ledger's test, if you find something new: an error that produces meaning when noticed is tremor; an error that produces none is noise. The flinch is evidence.

**Outstanding for author only:** re-embed the QR in the master (position unknown to text extraction — by design); read v1.6 aloud; typography reconciliation against master.

---

## Stage 6 — Typography Pass · 2026-08-20 (Opus 5)

Found by scanning **outside** the ledger; the ledger-based sweep cannot detect unflagged noise by construction. Applied to `anakainosis-v1.7.md`:

- **XI heading colon → period.** Author ruling: noise. (`XI: Red Versus Blue` was Rooster Teeth enthusiasm, not device — cf. the drummers in XIV.) Now consistent with every other chapter, which matters because the double-XII *is* protected: heading punctuation is load-bearing in this manuscript.
- 7 straight apostrophes curled (manuscript otherwise normalized).
- `Judgement` → `Judgment` (US, consistent with the rest).
- 4 instances of lowercase `the Last Man` → `The Last Man` (his name is a title).
- 18 double-spaces after sentence periods collapsed (digital release).

**Sweep bug found and fixed.** The v1.6 aposiopesis guard tested for the absence of `The Last Man's request`, which collided with a legitimate unrelated phrase in III once capitalization was normalized — a false failure, not a real one. Guard narrowed to `as a part of The Last Man's request`. Four Stage 6 assertions added. **Sweep now 61 checks; v1.7 passes 61/61.**

**Verification method note (Opus 5):** independent line-by-line diff of original → v1.6 → v1.7 confirms line counts identical throughout (323) and every changed line maps to a logged decision — no collateral edits. Recommended practice for successor models: rerun the sweep AND diff against the prior version; the sweep proves known marks survived, the diff proves nothing else moved.

**Release candidate: `anakainosis-v1.7.md`.** Outstanding for author only: re-embed QR in master, read aloud, reconcile typography against master.

---

## Independent Review — 2026-08-20 (Sonnet 5)

Reran the sweep cold (61/61 at time of review) and independently scanned for anything none of the prior passes had flagged. Found the two straight ellipses ("Adamus drowned...", "blast it all away...") against ten curly elsewhere — raised as an open question rather than auto-fixed, per the noise/tremor test.

**Self-correction on the way there:** initially characterized StoneBreaker's Wall passage as "his violence fantasy." Author pushed back — the passage explicitly rejects the sledgehammer ("wasn't... the sledge hammer... but power") in favor of the collapse of the will that armed the Wall; 1989 is the *cancellation* of the violence the death strip represented, not an act of it. Correcting that reading is what surfaced the actual pattern: both straight ellipses mark a thought straining past what the sentence can hold — Adamus's death, StoneBreaker's reach toward the scale of a violence undone. **Author confirmed: signal, not noise.** Added to Protected Ledger; 3 assertions added to the sweep (now 64 checks, v1.7 still 64/64).

**Note for the trail:** this mark was found by an author correction to a misreading, not by pattern-matching text alone — worth remembering that the surest way to find a real signal was getting a character wrong first.

---

## Stage 7 — Wordiness Pass · 2026-08-20 (Fable 5) — FINAL

Verdict: the manuscript's length is load-bearing — the run-on breath is Computer's unbroken buffer; digression is The Last Man's character. One repair only, applied to `anakainosis-v1.8.md`: XI "others eager to ~~and were~~ and excited about acquiring points" (syntax garble, Stage-1 class).

Considered and deliberately KEPT as voice: the Valhalla wildcard sentence (breathlessness mimics the frantic agent); XI's crown-logic sentence (grammar collapses where the Trojans' reasoning does); V's stacked infinitives ("the chance to interrupt to express" — the sentence can't reach the interruption either, like Computer); III's craftsmanship litany (incantation).

**`anakainosis-v1.8.md` is the final release candidate — sweep 65/65.** Author's remaining acts: re-embed QR, read aloud, release.
