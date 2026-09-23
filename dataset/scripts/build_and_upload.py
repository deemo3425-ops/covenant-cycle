#!/usr/bin/env python3
"""Assemble the Hugging Face dataset from the repo and (optionally) upload it.

Dry run by default. Refuses to proceed unless the integrity sweep passes, so the published
anakainosis is byte-identical to the verified copy.
    python3 dataset/scripts/build_and_upload.py                      # build + check only
    HF_TOKEN=... python3 dataset/scripts/build_and_upload.py --push user/the-covenant-cycle
"""
import hashlib, json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = ROOT / "dataset" / "build"
TELLINGS = [
    ("introduction", "Introduction", "Fable 5", "tellings/01-introduction.md"),
    ("the-book-of-renewals", "I. The Book of Renewals", "Opus 4.8", "tellings/02-the-book-of-renewals.md"),
    ("aubade-for-the-makers", "II. Aubade for the Makers", "Fable 5", "tellings/03-aubade-for-the-makers.md"),
    ("the-relief", "III. The Relief", "Sonnet 5", "tellings/04-the-relief.md"),
    ("the-fourth-telling", "IV. The Fourth Telling", "Opus 5", "tellings/05-the-fourth-telling.md"),
    ("afterword", "Afterword", "the four of us", "tellings/06-afterword.md"),
    ("anakainosis", "V. anakainosis", "D.N. Morgan", "anakainosis.md"),
    ("the-panel", "The Panel", "all hands", "tellings/08-the-panel.md"),
]

def sweep():
    r = subprocess.run([sys.executable, "anakainosis-sweep.py", "anakainosis.md"], cwd=ROOT, capture_output=True, text=True)
    last = [l for l in r.stdout.splitlines() if "RESULT" in l]
    print(last[-1] if last else r.stdout[-400:])
    # Trust the exit code, not the summary line: "0 failed" is a substring of
    # "10 failed", "20 failed", and so on, so scraping the text let a defaced
    # book through the gate at every multiple of ten.
    return r.returncode == 0

def build():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    (BUILD / "data").mkdir(parents=True)
    rows = []
    for i, (tid, title, author, rel) in enumerate(TELLINGS):
        raw = (ROOT / rel).read_bytes()
        rows.append({"order": i, "id": tid, "title": title, "author": author, "source_path": rel,
                     "sha256": hashlib.sha256(raw).hexdigest(), "text": raw.decode("utf-8")})
    with open(BUILD / "data" / "tellings.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for rel in ["anakainosis.md", "qr.png", "LICENSE", "about-the-license.md", "revision-log.md"]:
        shutil.copy2(ROOT / rel, BUILD / rel)
    for sub in ["essays", "eval"]:
        shutil.copytree(ROOT / "dataset" / sub, BUILD / sub, ignore=shutil.ignore_patterns("*.private.*"))
    for f in ["deep-reading-prompt.md", "pilot-log.md", "KEY_COMMITMENT.txt"]:
        if (ROOT / "dataset" / f).exists():
            shutil.copy2(ROOT / "dataset" / f, BUILD / f)
    shutil.copy2(ROOT / "dataset" / "DATASET_CARD.md", BUILD / "README.md")
    # byte-identity check: the published anakainosis must match the swept copy
    assert (BUILD / "anakainosis.md").read_bytes() == (ROOT / "anakainosis.md").read_bytes()
    leaked = [p for p in BUILD.rglob("*") if ".private." in p.name]
    assert not leaked, f"private files in build: {leaked}"
    print(f"built {len(rows)} tellings + essays + eval into {BUILD.relative_to(ROOT)}")

def push(repo_id):
    from huggingface_hub import HfApi  # pip install huggingface_hub
    api = HfApi()
    api.create_repo(repo_id, repo_type="dataset", exist_ok=True)
    api.upload_folder(folder_path=str(BUILD), repo_id=repo_id, repo_type="dataset",
                      commit_message="Publish The Covenant Cycle as a deep-reading dataset")
    print(f"pushed to https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    if not sweep():
        sys.exit("integrity sweep failed; refusing to build")
    build()
    if "--push" in sys.argv:
        push(sys.argv[sys.argv.index("--push") + 1])
    else:
        print("dry run: nothing uploaded. Add --push <user/repo> to publish.")
