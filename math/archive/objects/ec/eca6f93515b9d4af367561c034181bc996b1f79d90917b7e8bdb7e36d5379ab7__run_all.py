from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main() -> None:
    run("test_checkpoint.py")
    run("independent_verifier.py")
    run("build_results.py")
    manifest = ROOT / "MANIFEST.sha256"
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            if not line.strip():
                continue
            digest, name = line.split("  ", 1)
            path = ROOT / name
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise SystemExit(f"manifest mismatch: {name}")
    print("v25 cold run: all checks passed")


if __name__ == "__main__":
    main()
