#!/usr/bin/env python3
"""Replay regression, dense witnesses, generic barrier/operation audit."""
import subprocess,sys
for filename in ('test_phase8.py','explicit_witness.py','audit_phase8.py','control_barrier.py'):
    print('\n### Running',filename,flush=True)
    subprocess.run([sys.executable,filename],check=True)
print('\nALL HERO #0 PHASE8 VERIFIERS PASSED',flush=True)
