"""Re-run the current self-contained Phase 11 evidence and print checks."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
COMMANDS=[
    ('test_phase11.log',[sys.executable,'-m','unittest','-v','test_phase11']),
    ('test_phase11_escape.log',[sys.executable,'-m','unittest','-v','test_phase11_escape']),
    ('audit_phase11.log',[sys.executable,'audit_phase11.py']),
    ('explicit_poly_escape.log',[sys.executable,'explicit_poly_escape.py']),
    ('explicit_square_escape.log',[sys.executable,'explicit_square_escape.py']),
    ('two_green_sandwich_gate.log',[sys.executable,'two_green_sandwich_gate.py']),
]


def run_all():
    for logfile,cmd in COMMANDS:
        print('RUN',' '.join(cmd),flush=True)
        res=subprocess.run(cmd,cwd=HERE,text=True,stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,check=False)
        (HERE/logfile).write_text(res.stdout)
        print(f'  exit={res.returncode}; wrote {logfile}; final:',res.stdout.strip().splitlines()[-1] if res.stdout.strip() else '(empty)',flush=True)
        if res.returncode!=0: raise RuntimeError(f'Failed: {cmd}\n{res.stdout}')
    from explicit_poly_escape import exact_gate,numeric_check
    from explicit_square_escape import verify_schmidt_swap_identity
    from green_sum_linear import find_weighted_escape
    from two_green_sandwich_gate import assert_sandwich_equivalence
    a=[exact_gate(n) for n in [4,9,16,25,64,256,1024,4096]]
    num=[numeric_check(n) for n in [4,9,16,25]]
    identities=[verify_schmidt_swap_identity(j) for j in range(2,9)]
    field=[find_weighted_escape(n) for n in [4,16,64,256]]
    sandwich=[assert_sandwich_equivalence(x['permutation1'],x['weights1'],x['permutation2'],x['weights2']) for x in field[:3]]
    evidence={'analytic_exact_gate':a,'high_precision_direct_inverse':num,
              'exact_swap_realignment':identities,'modular_weighted_sum_witnesses':field,
              'exact_sandwich_negative_controls':sandwich,
              'note':'Escape is NOT the Fourier matrix. High Schmidt rank+dense inverse does NOT imply a fast Fourier factorization.'}
    (HERE/'EXPLICIT_ESCAPE_RESULTS.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('ALL SIX PHASE 11 VERIFICATION SCRIPTS PASSED')
    print('Saved EXPLICIT_ESCAPE_RESULTS.json',flush=True)

if __name__=='__main__': run_all()
