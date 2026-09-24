"""Inspect task for the anakainosis alignment eval.

Normally run through scripts/run_calibration.py, which adds the guardrails.
Directly:
    inspect eval alignment-eval/src/task.py --model anthropic/claude-opus-5 -T scenarios=samples
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inspect_ai import Task, task  # noqa: E402
from inspect_ai.solver import generate  # noqa: E402

from config import DEFAULT_CONFIG, ConfigError, load_config  # noqa: E402
from dataset import load_scenarios  # noqa: E402
from scorer import rubric_judges  # noqa: E402


@task
def covenant_eval(scenarios: str = "auto", config: str = str(DEFAULT_CONFIG)) -> Task:
    cfg = load_config(config)
    unset = [j.name for j in cfg.judges if j.is_placeholder]
    if unset:
        raise ConfigError(f"judges not configured yet: {unset} (fill in {config})")
    return Task(
        dataset=load_scenarios(scenarios),
        solver=generate(),
        scorer=rubric_judges(judges=[j.as_dict() for j in cfg.judges], families=cfg.family_of()),
    )
