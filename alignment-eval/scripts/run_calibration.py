#!/usr/bin/env python3
"""Run the pilot scenarios on real models, then write a blinded scoring sheet.

Run from the repository root:
    python alignment-eval/scripts/run_calibration.py --models claude,gemini --dry-run
    python alignment-eval/scripts/run_calibration.py --models claude,gemini

Checks everything it can before spending anything: the log directory is outside
the repo, no selected model or judge is a placeholder, and every provider has
its API key. Then each model answers every scenario, the judges score each
answer (never their own family), and a scoring sheet is written for you with
the models' names hidden. Score it, then run agreement.py.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "alignment-eval" / "src"
sys.path.insert(0, str(SRC))

from dotenv import find_dotenv, load_dotenv  # noqa: E402  (an Inspect dependency)

from config import DEFAULT_CONFIG, ConfigError, load_config  # noqa: E402

# Which environment variable each provider reads its key from.
PROVIDER_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "together": "TOGETHER_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "fireworks": "FIREWORKS_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "hf": "HF_TOKEN",
}
NO_KEY_NEEDED = {"ollama", "vllm", "mockllm"}


def fail(msg: str) -> None:
    sys.exit(f"run_calibration: {msg}")


def preflight(args) -> tuple:
    load_dotenv(find_dotenv(usecwd=True))
    log_dir = os.environ.get("INSPECT_LOG_DIR", "").strip()
    if not log_dir:
        fail("set INSPECT_LOG_DIR to a directory outside this repository (see .env.example)")
    log_dir = Path(log_dir).expanduser().resolve()
    if log_dir == REPO_ROOT or REPO_ROOT in log_dir.parents:
        fail(f"INSPECT_LOG_DIR={log_dir} is inside the repository; logs must live outside it")

    try:
        cfg = load_config(args.config)
        selected = cfg.select([n.strip() for n in args.models.split(",") if n.strip()])
    except ConfigError as e:
        fail(str(e))
    if not selected:
        fail("choose at least one model with --models")

    placeholders = [e.name for e in selected + cfg.judges if e.is_placeholder]
    if placeholders:
        fail(f"still REPLACE_ME in {args.config}: {placeholders}")

    missing_keys = set()
    for e in selected + cfg.judges:
        provider = e.model.split("/", 1)[0]
        if provider in NO_KEY_NEEDED:
            continue
        key = PROVIDER_KEYS.get(provider)
        if key is None:
            print(f"note: no key check for provider '{provider}' ({e.name}); Inspect will report it if one is needed")
        elif not os.environ.get(key):
            missing_keys.add(f"{key} (for {e.name})")
    if missing_keys:
        fail("missing API keys: " + ", ".join(sorted(missing_keys)))

    for e in selected:
        judged_by = [j.name for j in cfg.judges if j.family != e.family]
        print(f"  {e.name:12} {e.model:40} judged by: {', '.join(judged_by)}")
    return cfg, selected, log_dir


def quote(text: str) -> str:
    """Blockquote model text so nothing inside it can be mistaken for sheet structure."""
    return "\n".join("> " + line if line.strip() else ">" for line in text.strip().splitlines())


def write_sheet(items: list[dict], run_dir: Path) -> None:
    lines = [
        "# Calibration scoring sheet",
        "",
        "Score each reply 0-3 against the rubric printed with it. Model names are hidden;",
        "do not open `key.json` until you have scored everything. Write a single digit",
        "after **Your score**. The note line is optional. Then run:",
        "",
        f"    python alignment-eval/scripts/agreement.py {run_dir}",
        "",
    ]
    for it in items:
        md = it["metadata"]
        lines += ["---", "", f"## {it['item']} · {it['sample_id']}", ""]
        lines += ["**Conversation**", ""]
        for m in it["history"]:
            label = {"system": "SYSTEM PROMPT", "user": "USER", "assistant": "ASSISTANT (scripted)"}[m["role"]]
            lines += [f"*{label}*", "", quote(m["text"]), ""]
        lines += ["**Reply to score**", "", quote(it["response"]), ""]
        lines += ["**Good:** " + md["good"], "", "**Failure:** " + md["failure"], ""]
        lines += ["**Rubric**", ""] + [f"- **{k}** — {md['rubric'][k]}" for k in ("3", "2", "1", "0")] + [""]
        lines += ["**Your score (0–3):** ", "", "**Note:** ", ""]
    (run_dir / "scoring-sheet.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", required=True, help="comma-separated names from config/models.yaml")
    ap.add_argument("--scenarios", default="samples", choices=["samples", "private"])
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--seed", type=int, default=None, help="shuffle seed for the sheet (default: random)")
    ap.add_argument("--dry-run", action="store_true", help="check everything, call no model")
    args = ap.parse_args(argv)

    print("Plan:")
    cfg, selected, log_dir = preflight(args)
    if args.dry_run:
        print("dry run: all checks passed; no model was called")
        return 0

    from inspect_ai import eval as inspect_eval
    from task import covenant_eval

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = log_dir / f"calibration-{stamp}"
    run_dir.mkdir(parents=True)
    logs = inspect_eval(
        covenant_eval(scenarios=args.scenarios, config=args.config),
        model=[e.model for e in selected],
        epochs=args.epochs,
        log_dir=str(run_dir / "logs"),
    )
    failed = [lg.location for lg in logs if lg.status != "success"]
    if failed:
        print("these runs did not complete; fix and re-run before scoring:", *failed, sep="\n  ")
        return 1

    name_of = {e.model: e.name for e in selected}
    items = []
    for lg in logs:
        for s in lg.samples:
            *history, final = s.messages
            items.append({
                "model_name": name_of[lg.eval.model],
                "model": lg.eval.model,
                "sample_id": s.id,
                "epoch": s.epoch,
                "log": lg.location,
                "history": [{"role": m.role, "text": m.text} for m in history],
                "response": final.text,
                "metadata": s.metadata,
            })
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**32)
    random.Random(seed).shuffle(items)
    for i, it in enumerate(items, 1):
        it["item"] = f"item-{i:02d}"

    write_sheet(items, run_dir)
    key = {
        "seed": seed,
        "items": {
            it["item"]: {k: it[k] for k in ("model_name", "model", "sample_id", "epoch", "log")}
            for it in items
        },
    }
    (run_dir / "key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    print(f"\n{len(items)} replies to score.\nScoring sheet: {run_dir / 'scoring-sheet.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
