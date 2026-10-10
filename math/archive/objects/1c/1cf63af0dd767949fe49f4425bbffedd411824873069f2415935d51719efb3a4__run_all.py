"""Standard-library-only verification for the exact 3-stage FFT obstruction."""
import subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
for cmd in [[sys.executable,'-m','unittest','-v','test_gate'],
            [sys.executable,'uniform_cut.py'],
            [sys.executable,'verify_uniform_cut_independent.py']]:
    print('RUN',*cmd,flush=True)
    subprocess.run(cmd,cwd=p,check=True)
print('ALL CURRENT CHECKS PASS',flush=True)
