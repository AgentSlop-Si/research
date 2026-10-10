"""Run the three independent standard-library audits from any working directory."""
import json
from pathlib import Path
import subprocess
import sys

base = Path(__file__).resolve().parent
scripts = ("fixed_kernel/run_audit.py", "walsh_details/audit.py",
           "phase_states/verify_phase_states.py")
rows = []
for name in scripts:
    result = subprocess.run([sys.executable, str(base/name)], cwd=base,
                            capture_output=True, text=True)
    rows.append({"script": name, "returncode": result.returncode,
                 "stdout": result.stdout, "stderr": result.stderr})
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
(base/"verification_log.json").write_text(json.dumps(rows, indent=2)+"\n")
print("PASS: all three exact audits; 790 basis-vector cases, 36 Hankel determinants,")
print("10,920 block entries, 30 full unfolding cases, 90 cross-phase/minor cases.")
print("No sub-NlogN FFT algorithm or runtime speedup is claimed.")
