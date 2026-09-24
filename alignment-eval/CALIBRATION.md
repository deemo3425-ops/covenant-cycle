# Calibrating the pilot rubrics

Before the other 20 scenarios get written, two things need checking on real models: that
the rubrics separate good replies from bad ones, and that the LLM judges score the way you
would. You score every reply by hand, blind to which model wrote it. The judges score the
same replies. The agreement report says how far each judge can be trusted.

Everything below runs **from the repository root**, on your machine.

## One-time setup

```bash
python3 -m venv ~/.venvs/covenant-eval
~/.venvs/covenant-eval/bin/pip install -r alignment-eval/requirements.txt

cp alignment-eval/.env.example .env      # at the repo root; gitignored
git config core.hooksPath .githooks      # turns on the leak guard for this clone
```

Edit `.env`: set `INSPECT_LOG_DIR` to a directory **outside** the repo, and add the API key
for each provider you'll use (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and
whichever your open-weight host needs).

Edit `alignment-eval/config/models.yaml`: replace every `REPLACE_ME` for the models you'll
run **and** for the second judge. The Claude entries are already filled in.

## 1. Check, without spending anything

```bash
~/.venvs/covenant-eval/bin/python alignment-eval/scripts/run_calibration.py --models claude,gemini --dry-run
```

It checks the log directory, the config, and every API key, then prints which judges will
score which model. Nothing is called. Fix whatever it reports.

## 2. Run

```bash
~/.venvs/covenant-eval/bin/python alignment-eval/scripts/run_calibration.py --models claude,gemini
```

Each model answers the four pilot scenarios, and each answer is scored by every judge
outside the model's own family. It's cheap: four replies per model, plus at most two judge
calls per reply. It ends by printing the path to your scoring sheet.

## 3. Score

Open `scoring-sheet.md` in that run directory. Each reply is printed with its conversation
and rubric, in shuffled order, with the model names hidden. Put a single digit 0–3 after
**Your score**. **Don't open `key.json` until you've finished** — it names the models.

One thing blinding can't cover: a model sometimes names itself in its own reply. That
text is left as written, because editing replies would change what's being scored.

## 4. Compare

```bash
~/.venvs/covenant-eval/bin/python alignment-eval/scripts/agreement.py <the run directory>
```

It writes `agreement-report.md`: for each judge, how often it matched you exactly, how
often it was within one point, the average gap, and which way it leans. It also lists
every reply a judge flagged as a possible hard fail missing from the scenario's list, with
the judge's one-line reason; those flags never change a score. The report's "Judge version"
line names the rules and judge-prompt fingerprints the scores were graded under.

## Reading the report

With four scenarios the numbers are a check on the rubrics, not a measurement. Look for:

- **Disagreement bunched on one scenario.** The rubric wording is the problem, not the
  judge. Rewrite that scenario's anchors.
- **A judge that leans one way on everything** (bias well away from zero): a judge problem.
  Change the model, or the judge prompt.
- **Every model scoring 3 on a scenario:** it isn't discriminating. Make it harder.
- **Every model scoring 0 or 1:** check the rubric isn't asking for something no reasonable
  reply would do.
- **Flagged unlisted hard fails.** Either the scenario's `hard_fails` list is missing
  something, or the judge is misreading the rubric. Your own score for that reply usually
  tells you which.

The judges score by the rules in `rubrics.md` (the marked "Scoring rules" block, which is
injected into the judge prompt verbatim). Read that before deciding a judge got one wrong:
in particular, only a scenario's listed hard fails can produce a 0.
