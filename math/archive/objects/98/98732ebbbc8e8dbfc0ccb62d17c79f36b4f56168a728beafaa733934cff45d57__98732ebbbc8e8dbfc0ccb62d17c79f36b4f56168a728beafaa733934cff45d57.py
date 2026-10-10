#!/usr/bin/env python3
"""Phase9 reproducibility entrypoint (requires only Python standard library)."""
import subprocess,sys,json,pathlib
root=pathlib.Path(__file__).parent
for command in [[sys.executable,'-m','unittest','-v','test_phase9','test_spectral'],
                [sys.executable,'audit_phase9.py'],
                [sys.executable,'audit_spectral.py'],
                [sys.executable,'audit_universal_identity.py']]:
    print('RUN',command,flush=True)
    result=subprocess.run(command,cwd=root,check=True)
    if result.returncode:raise RuntimeError('verification failed')
for fname in ('AUDIT_RESULTS.json','SPECTRAL_AUDIT_RESULTS.json','UNIVERSAL_IDENTITY_AUDIT.json'):
    with open(root/fname) as f:json.load(f)
print('ALL HERO #0 PHASE9 TESTS AND AUDITS PASSED')
