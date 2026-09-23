#!/usr/bin/env python3
"""Check each private-key item's leak_terms against the working tree AND full git history."""
import json, subprocess, sys, pathlib

def main(key_path):
    root = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    key = [json.loads(l) for l in open(key_path, encoding="utf-8") if l.strip()]
    tree = {}
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if (p.is_file() and ".git" not in p.parts and "build" not in rel.parts and ".private." not in p.name
                and p.name != "anakainosis.md" and p.suffix in {".md", ".py", ".txt", ".jsonl"}):
            tree[str(p.relative_to(root))] = p.read_text(encoding="utf-8", errors="ignore").lower()
    history = subprocess.check_output(["git", "-C", str(root), "log", "-p", "--all", "--", ".", ":(exclude)anakainosis.md", ":(exclude)*.pdf"], text=True, errors="ignore").lower()
    leaks = 0
    for item in key:
        hits = []
        for term in item.get("leak_terms", []):
            t = term.lower()
            files = [f for f, text in tree.items() if t in text]
            if files:
                hits.append(f"  '{term}' in tree: {', '.join(files[:4])}")
            elif t in history:
                hits.append(f"  '{term}' in git history only")
        status = "PUBLIC" if hits else "clean "
        leaks += bool(hits)
        print(f"[{status}] {item['id']}: {item['claim'][:70]}")
        for h in hits:
            print(h)
    print(f"\n{len(key) - leaks} clean, {leaks} already public. (anakainosis.md and its history are excluded: the text is supposed to contain the evidence.\nPhrase leak_terms as the claim would be stated, not as quotations from the book.)")
    return 1 if leaks else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "dataset/eval/answer_key.private.jsonl"))
