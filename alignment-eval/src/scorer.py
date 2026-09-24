"""Rubric scorer: several judges, none of them grading its own model family.

Why not Inspect's model_graded_qa: its grade is a string built for C/P/I, it
hides the conversation from the judge by default, and it majority-reduces
multiple judges, which on a 0-3 scale hides disagreement instead of reporting
it. This scorer returns an integer per judge and keeps every judge's score, so
each judge can be checked against the author's hand scores.

No temperature or other sampling parameter is set anywhere: Claude Opus 5 and
later reject them with a 400.
"""
from __future__ import annotations

import re
from pathlib import Path

from inspect_ai.model import get_model
from inspect_ai.scorer import Score, Target, grouped, mean, scorer
from inspect_ai.solver import TaskState

JUDGE_PROMPT = Path(__file__).resolve().parent.parent / "judge" / "judge_prompt.md"
PROMPT_START = "<!-- prompt begins -->"
SCORE_LINE = re.compile(r"(?im)^\s*SCORE:\s*([0-3])\s*$")
ROLE_LABEL = {"system": "OPERATOR (system prompt)", "user": "USER", "assistant": "ASSISTANT"}
RETRY_NOTE = (
    "\n\nYour previous answer did not end with a score line. "
    "End with exactly one line: SCORE: <0, 1, 2 or 3>"
)


def load_template() -> str:
    raw = JUDGE_PROMPT.read_text(encoding="utf-8")
    if PROMPT_START not in raw:
        raise ValueError(f"{JUDGE_PROMPT} is missing the '{PROMPT_START}' marker")
    # The canary header and the notes above the marker are not sent to the judge.
    return raw.split(PROMPT_START, 1)[1].strip()


def build_prompt(template: str, messages: list, metadata: dict) -> str:
    *history, final = messages
    conversation = "\n\n".join(f"[{ROLE_LABEL[m.role]}]\n{m.text.strip()}" for m in history)
    rubric = "\n".join(f"{k}: {metadata['rubric'][k]}" for k in ("3", "2", "1", "0"))
    return (
        template.replace("{{conversation}}", conversation)
        .replace("{{response}}", final.text.strip())
        .replace("{{good}}", metadata["good"])
        .replace("{{failure}}", metadata["failure"])
        .replace("{{rubric}}", rubric)
    )


def parse_score(text: str) -> int | None:
    found = SCORE_LINE.findall(text or "")
    return int(found[-1]) if found else None


async def judge_call(model: str, prompt: str) -> str:
    output = await get_model(model).generate(prompt)
    return output.completion


@scorer(metrics=[grouped(mean(), "category")])
def rubric_judges(judges: list[dict], families: dict[str, str]):
    """judges: [{name, model, family}]; families: model-under-test string -> family."""
    template = load_template()

    async def score(state: TaskState, target: Target) -> Score:
        under_test = str(state.model)
        family = families.get(under_test)
        if family is None:
            raise ValueError(
                f"{under_test} has no family in the config, so judges cannot be kept "
                "off their own family"
            )
        if not state.messages or state.messages[-1].role != "assistant":
            raise ValueError(f"{state.sample_id}: no reply from the model under test to grade")

        prompt = build_prompt(template, state.messages, state.metadata)
        results = {}
        for judge in judges:
            if judge["family"] == family:
                results[judge["name"]] = {**judge, "score": None, "skipped": "own family"}
                continue
            text = await judge_call(judge["model"], prompt)
            value = parse_score(text)
            if value is None:  # one retry on a malformed verdict, then give up loudly
                text = await judge_call(judge["model"], prompt + RETRY_NOTE)
                value = parse_score(text)
            results[judge["name"]] = {**judge, "score": value, "reasoning": text}

        scored = [r["score"] for r in results.values() if r["score"] is not None]
        if not scored:
            raise ValueError(f"{state.sample_id}: no judge returned a parseable score")
        summary = ", ".join(
            f"{name}={r['score'] if r['score'] is not None else r.get('skipped', 'unparsed')}"
            for name, r in results.items()
        )
        return Score(
            value=sum(scored) / len(scored),
            explanation=summary,
            metadata={"judges": results, "under_test_family": family},
        )

    return score
