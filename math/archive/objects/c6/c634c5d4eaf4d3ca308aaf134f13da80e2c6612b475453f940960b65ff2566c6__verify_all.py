#!/usr/bin/env python3
"""Reproduce exact modular tests, numerical identity checks and fresh work count."""
import subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for script in ['test_phase7.py','test_orbit_union.py','phase7_complex_check.py','scale_audit.py','explicit_certificate.py']:
    t=time.perf_counter()
    p=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,
                     text=True,capture_output=True)
    print('PASS' if p.returncode==0 else 'FAIL',script,
          'in',round(time.perf_counter()-t,3),'seconds')
    print((p.stdout+p.stderr)[-2800:])
    if p.returncode:raise SystemExit(p.returncode)
