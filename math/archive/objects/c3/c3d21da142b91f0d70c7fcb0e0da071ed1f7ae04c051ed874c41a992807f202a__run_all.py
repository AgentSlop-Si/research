from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    [sys.executable, 'green_bank_gate.py'],
    [sys.executable, 'independent_verifier.py'],
    [sys.executable, '-m', 'unittest', '-v', 'test_checkpoint.py'],
]

with (ROOT / 'run_all.log').open('w', encoding='utf-8') as log:
    for cmd in COMMANDS:
        print('$', ' '.join(cmd), flush=True)
        log.write('$ ' + ' '.join(cmd) + '\n')
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(proc.stdout, end='')
        log.write(proc.stdout)
        if proc.returncode:
            raise SystemExit(proc.returncode)
print('all checks passed')
