#!/usr/bin/env python3
"""Publish a salted hash of the private key now; reveal key + salt later to prove it predates scoring."""
import hashlib, secrets, sys, pathlib, datetime

key_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dataset/eval/answer_key.private.jsonl")
salt_path = key_path.with_name("key_salt.private.txt")
if not salt_path.exists():
    salt_path.write_text(secrets.token_hex(32))
salt = salt_path.read_text().strip()
digest = hashlib.sha256((salt + "\n").encode() + key_path.read_bytes()).hexdigest()
out = pathlib.Path(__file__).resolve().parents[1] / "KEY_COMMITMENT.txt"
out.write_text(
    f"sha256(salt + newline + answer_key.private.jsonl) = {digest}\n"
    f"committed {datetime.date.today().isoformat()}\n"
    "Key and salt are held by the author and will be revealed after scoring.\n")
print(digest)
print(f"wrote {out}; keep {key_path.name} and {salt_path.name} private")
