from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str) -> None:
    print(f"=== {script} ===", flush=True)
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)


def verify_manifest() -> None:
    manifest = ROOT / "MANIFEST.sha256"
    if not manifest.exists():
        print("MANIFEST.sha256 not present; skipping hash verification")
        return
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        path = ROOT / rel
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise SystemExit(f"manifest mismatch: {rel}")
    print("manifest: PASS")


def verify_predecessor() -> None:
    path = ROOT / "PRIOR_v25_COMPLETE.zip"
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise SystemExit(f"predecessor CRC failure: {bad}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = "f8fbf4c58e95202665326bc7e66bc2da859502d38225a4d5ce3b42c043a00d15"
    if digest != expected:
        raise SystemExit("predecessor hash mismatch")
    print("predecessor: PASS")


def main() -> None:
    run("test_checkpoint.py")
    run("independent_verifier.py")
    run("generate_results.py")
    verify_predecessor()
    verify_manifest()
    print("V26 COLD RUN: PASS")


if __name__ == "__main__":
    main()
