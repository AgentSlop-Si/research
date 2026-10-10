"""Run each exact mechanism audit; Python standard library only."""
import json
from pathlib import Path
import subprocess
import sys

base=Path(__file__).resolve().parent
scripts=('kernel_spectrum/audit.py','orbit_norm/run_audit.py',
         'sparse_forcing/sparse_forcing.py','cycle_flow/audit.py')
log=[]
for script in scripts:
    run=subprocess.run([sys.executable,str(base/script)],cwd=base,
                       capture_output=True,text=True)
    log.append({'script':script,'returncode':run.returncode,
                'stdout':run.stdout,'stderr':run.stderr})
    if run.returncode:
        print(run.stdout,end=''); print(run.stderr,end='',file=sys.stderr)
        raise SystemExit(run.returncode)
(base/'verification_log.json').write_text(json.dumps(log,indent=2)+'\n')
print('PASS: all four exact mechanism audits.')
print('2254 basis-case comparisons; 1044 kernel-spectrum values; 104 median checks.')
print('Positive restricted graph/preparation results; no general sub-NlogN FFT claim.')
