#!/usr/bin/env python3
"""Read-only integrity check of this publication, not a scientific rerun."""
from pathlib import Path
import hashlib, json
root = Path(__file__).resolve().parent
manifest = json.loads((root / "PUBLICATION_MANIFEST.json").read_text())
expected = {entry["path"] for entry in manifest["files"]}
actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
assert actual == expected | {"PUBLICATION_MANIFEST.json"}, "Unexpected or missing publication file"
for entry in manifest["files"]:
    p = root / entry["path"]
    assert not p.is_symlink(), p
    data = p.read_bytes()
    assert len(data) == entry["bytes"], p
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], p
print(f"PASS: {len(expected)} publication files match their declared bytes and SHA-256 values.")
