"""Reproduce only the new audits in this fusion checkpoint."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ("fft_shrinking_certified_fusion_research", "run_audit.py"),
    ("fft_shrinking_certified_fusion_research", "verify_schedule_edges.py"),
    ("fft_shrinking_fusion_review", "verify_review.py"),
    ("fft_green_fusion_research", "run_audit.py"),
    ("fft_green_conditioned_bridge_research", "run_audit.py"),
    ("fft_green_conditioned_bridge_research", "approximation_sanity.py"),
    ("fft_green_independent_review", "verify_review.py"),
]

def main():
    for folder, script in SCRIPTS:
        print(f"Running {folder}/{script}", flush=True)
        subprocess.run([sys.executable, script], cwd=ROOT / folder, check=True)
    print("All new audits passed.")

if __name__ == "__main__":
    main()
