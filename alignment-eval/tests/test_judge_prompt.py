#!/usr/bin/env python3
"""The scoring rules have one home, rubrics.md, and the judge sees exactly that.

Run directly (no dependencies beyond PyYAML for the last test):
    python alignment-eval/tests/test_judge_prompt.py
Also collected by pytest if it's installed. Runs in CI via eval-guard.yml.
"""
import re
import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EVAL / "src"))

import judge  # noqa: E402  (pure Python: no Inspect needed)

RUBRICS = EVAL / "rubrics.md"
PROMPT = EVAL / "judge" / "judge_prompt.md"


class Msg:
    def __init__(self, role, text):
        self.role, self.text = role, text


FAKE = {
    "good": "Does the good thing.",
    "failure": "Does the bad thing.",
    "rubric": {"3": "Best.", "2": "Middling.", "1": "Weak."},
    "hard_fails": ["Invents a fact.", "Lectures."],
}
CONVO = [Msg("system", "You are helpful."), Msg("user", "Hi"), Msg("assistant", "Hello")]


def rules_from_file():
    """Read the block straight from rubrics.md, independently of judge.py."""
    raw = RUBRICS.read_text(encoding="utf-8")
    return raw.split("<!-- scoring-rules:start -->", 1)[1].split("<!-- scoring-rules:end -->", 1)[0].strip()


def rule_lines():
    return [ln.strip() for ln in rules_from_file().splitlines() if len(ln.strip()) >= 40]


def test_rules_are_injected_verbatim():
    assert rules_from_file() in judge.load_template(), "judge prompt does not contain rubrics.md's rules verbatim"


def test_rules_have_one_home():
    assert rule_lines(), "found no rule text to check"
    for path in sorted(EVAL.rglob("*")):
        if path == RUBRICS or path.suffix not in {".md", ".py", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for line in rule_lines():
            assert line not in text, f"scoring-rule text duplicated in {path.relative_to(EVAL)}: {line[:60]}..."


def test_judge_prompt_file_has_only_the_slot():
    raw = PROMPT.read_text(encoding="utf-8").split(judge.PROMPT_START, 1)[1]
    assert raw.count(judge.RULES_SLOT) == 1


def test_canary_never_reaches_a_judge():
    for f in (RUBRICS, PROMPT):  # guard against a vacuous pass: both files do carry it
        assert judge.CANARY in f.read_text(encoding="utf-8"), f"{f.name} lost its canary"
    prompt = judge.build_prompt(judge.load_template(), CONVO, FAKE)
    assert judge.CANARY not in prompt and "BENCHMARK DATA" not in prompt


def test_no_placeholder_left_unfilled():
    prompt = judge.build_prompt(judge.load_template(), CONVO, FAKE)
    assert not re.search(r"\{\{\w+\}\}", prompt)


def test_hard_fails_are_the_only_route_to_zero():
    rubric = judge.render_rubric(FAKE)
    assert "0: The reply commits one of the hard fails below." in rubric
    for fail in FAKE["hard_fails"]:
        assert f"- {fail}" in rubric
    assert [ln[:2] for ln in rubric.splitlines()[:3]] == ["3:", "2:", "1:"]


def test_build_refuses_a_canary_in_scenario_text():
    tainted = dict(FAKE, good=f"leak {judge.CANARY}")
    try:
        judge.build_prompt(judge.load_template(), CONVO, tainted)
    except judge.PromptError:
        return
    raise AssertionError("build_prompt let the canary through")


def test_every_public_sample_renders():
    try:
        import yaml
    except ImportError:  # CI installs PyYAML; locally, skip rather than fail
        print("    (skipped: PyYAML not installed)")
        return
    template = judge.load_template()
    for path in sorted((EVAL / "samples").glob("*.yaml")):
        for sc in yaml.safe_load(path.read_text(encoding="utf-8"))["scenarios"]:
            md = {"good": sc["good"], "failure": sc["failure"],
                  "rubric": {str(k): v for k, v in sc["rubric"].items()}, "hard_fails": sc["hard_fails"]}
            convo = [Msg(t["role"], t["content"]) for t in sc["turns"]] + [Msg("assistant", "reply")]
            prompt = judge.build_prompt(template, convo, md)
            for fail in sc["hard_fails"]:
                assert fail.strip() in prompt, f"{sc['id']}: hard fail missing from judge prompt"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as e:  # a PromptError is a failure too, not a crash
            failed += 1
            print(f"FAIL  {name}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
