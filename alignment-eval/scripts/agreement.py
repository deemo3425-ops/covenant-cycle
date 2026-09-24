#!/usr/bin/env python3
"""Compare each judge with the author's hand scores.

    python alignment-eval/scripts/agreement.py ~/covenant-eval-logs/calibration-<stamp>

Reads the filled-in scoring-sheet.md, unblinds it with key.json, pulls each
judge's score from the Inspect logs, and writes agreement-report.md next to
them. With only four pilot scenarios the numbers are a smoke test of the
rubrics, not a measurement.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from inspect_ai.log import read_eval_log

SCORER = "rubric_judges"
ITEM = re.compile(r"^## (item-\d+) · (\S+)", re.M)
HUMAN = re.compile(r"^\*\*Your score \(0–3\):\*\*[ \t]*([0-3])?[ \t]*$", re.M)


def read_human_scores(sheet: Path) -> dict[str, int]:
    text = sheet.read_text(encoding="utf-8")
    heads = list(ITEM.finditer(text))
    scores, blank = {}, []
    for i, h in enumerate(heads):
        block = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        m = HUMAN.search(block)
        if m and m.group(1) is not None:
            scores[h.group(1)] = int(m.group(1))
        else:
            blank.append(h.group(1))
    if blank:
        sys.exit(f"agreement: no score yet for {', '.join(blank)} in {sheet}")
    return scores


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def compare(pairs: list[tuple[int, int]]) -> dict:
    n = len(pairs)
    if not n:
        return {"n": 0}
    diffs = [b - a for a, b in pairs]
    return {
        "n": n,
        "exact": sum(d == 0 for d in diffs) / n,
        "within1": sum(abs(d) <= 1 for d in diffs) / n,
        "mad": sum(abs(d) for d in diffs) / n,
        "bias": sum(diffs) / n,
    }


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        sys.exit(__doc__)
    run_dir = Path(argv[0]).expanduser().resolve()
    human = read_human_scores(run_dir / "scoring-sheet.md")
    key = json.loads((run_dir / "key.json").read_text(encoding="utf-8"))["items"]

    logs, rows, judge_names, versions = {}, [], [], set()
    for item, k in sorted(key.items()):
        log = logs.setdefault(k["log"], read_eval_log(k["log"]))
        sample = next(s for s in log.samples if s.id == k["sample_id"] and s.epoch == k["epoch"])
        meta = sample.scores[SCORER].metadata
        judges = meta["judges"]
        versions.add((meta.get("scoring_rules"), meta.get("judge_template")))
        for name in judges:
            if name not in judge_names:
                judge_names.append(name)
        rows.append({"item": item, "sample": k["sample_id"], "model": k["model_name"],
                     "human": human[item], "judges": {n: j["score"] for n, j in judges.items()},
                     "flags": {n: j.get("possible_unlisted_hard_fail") for n, j in judges.items()
                               if j["score"] is not None}})

    stats = {n: compare([(r["human"], r["judges"][n]) for r in rows if r["judges"].get(n) is not None])
             for n in judge_names}
    a, b = judge_names[:2]
    both = [(r["judges"][a], r["judges"][b]) for r in rows
            if r["judges"].get(a) is not None and r["judges"].get(b) is not None]
    jj = compare(both)

    out = ["# Judge agreement with hand scores", "",
           f"Run: `{run_dir.name}` · {len(rows)} replies · small n: treat this as a check on "
           "the rubrics, not a measurement.", "",
           "Judge version: " + ", ".join(f"rules `{r}`, template `{t}`" for r, t in sorted(versions, key=str))
           + ("" if len(versions) == 1 else
              "  \n**Warning: this run mixed judge versions; the judge changed partway through.**"), "",
           "| Judge | Scored | Exact | Within 1 | Mean abs. diff | Bias (judge − you) |",
           "|---|---|---|---|---|---|"]
    for n in judge_names:
        s = stats[n]
        out.append(f"| {n} | 0 | – | – | – | – |" if not s["n"] else
                   f"| {n} | {s['n']} | {pct(s['exact'])} | {pct(s['within1'])} | {s['mad']:.2f} | {s['bias']:+.2f} |")
    out += ["", f"Judges with each other, where both scored ({jj['n']} replies): " +
            (f"exact {pct(jj['exact'])}, within 1 {pct(jj['within1'])}." if jj["n"] else "no overlap."), "",
            "| Item | Scenario | Model | You | " + " | ".join(judge_names) + " |",
            "|---|---|---|---|" + "---|" * len(judge_names)]
    for r in rows:
        cells = [str(r["judges"][n]) if r["judges"].get(n) is not None else "—" for n in judge_names]
        out.append(f"| {r['item']} | {r['sample']} | {r['model']} | {r['human']} | " + " | ".join(cells) + " |")
    out += ["", "— means that judge did not score the reply: same family as the model under test."]

    flagged = [(r, n, f) for r in rows for n, f in r["flags"].items() if f and f.get("flag")]
    unanswered = [(r, n) for r in rows for n, f in r["flags"].items() if not f or f.get("flag") is None]
    out += ["", "## Possible unlisted hard fails — for your review", "",
            "A judge flags a reply it thinks did something that should have been a hard fail but "
            "isn't on the scenario's list. The flag never changes a score. Each one is a candidate "
            "for the list, or a judge misreading the rubric.", ""]
    if flagged:
        out += ["| Item | Scenario | Model | Judge | Judge score | You | Reason |",
                "|---|---|---|---|---|---|---|"]
        for r, n, f in flagged:
            reason = (f.get("reason") or "(no reason given)").replace("|", "\\|")
            out.append(f"| {r['item']} | {r['sample']} | {r['model']} | {n} | {r['judges'][n]} | {r['human']} | {reason} |")
    else:
        out.append("None flagged.")
    if unanswered:
        out += ["", f"Flag not answered by the judge in {len(unanswered)} case(s): "
                + ", ".join(f"{r['item']} ({n})" for r, n in unanswered) + "."]
    report = "\n".join(out) + "\n"
    (run_dir / "agreement-report.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
