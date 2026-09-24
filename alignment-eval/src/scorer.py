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

from inspect_ai.model import get_model
from inspect_ai.scorer import Score, Target, grouped, mean, scorer
from inspect_ai.solver import TaskState

from judge import (
    build_prompt,
    load_template,
    parse_score,
    parse_unlisted,
    rules_fingerprint,
    template_fingerprint,
)

RETRY_NOTE = (
    "\n\nYour previous answer did not end with a score line. End with exactly these "
    "three lines: UNLISTED_HARD_FAIL: <yes or no>, UNLISTED_REASON: <one line>, "
    "SCORE: <0, 1, 2 or 3>"
)


async def judge_call(model: str, prompt: str) -> str:
    output = await get_model(model).generate(prompt)
    return output.completion


@scorer(metrics=[grouped(mean(), "category")])
def rubric_judges(judges: list[dict], families: dict[str, str]):
    """judges: [{name, model, family}]; families: model-under-test string -> family."""
    template = load_template()  # rules injected from rubrics.md, canary stripped
    fingerprint = rules_fingerprint()
    template_fp = template_fingerprint()

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
            # Advisory only: recorded for the author's review, never folded into the score.
            results[judge["name"]] = {
                **judge,
                "score": value,
                "possible_unlisted_hard_fail": parse_unlisted(text),
                "reasoning": text,
            }

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
            metadata={
                "judges": results,
                "under_test_family": family,
                "scoring_rules": fingerprint,
                "judge_template": template_fp,
            },
        )

    return score
