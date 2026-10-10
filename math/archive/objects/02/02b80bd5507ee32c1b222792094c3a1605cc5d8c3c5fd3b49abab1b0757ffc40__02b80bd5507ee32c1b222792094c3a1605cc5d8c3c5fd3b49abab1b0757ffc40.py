#!/usr/bin/env python3
"""Re-run all Phase 10 tests/certificates and check the resulting JSON evidence."""
import json
from pathlib import Path
import subprocess
import sys

BASE=Path(__file__).resolve().parent
COMMANDS=[
    ([sys.executable,'-m','unittest','-v','test_phase10'],'test_phase10.log'),
    ([sys.executable,'audit_phase10.py'],'audit_phase10.log'),
    ([sys.executable,'operator_schmidt_gate.py'],'operator_schmidt.log'),
    ([sys.executable,'operator_schmidt_general.py'],'operator_schmidt_general.log'),
]

def main():
    for cmd,logname in COMMANDS:
        print('RUN', ' '.join(cmd),flush=True)
        p=subprocess.run(cmd,cwd=BASE,text=True,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,check=True)
        (BASE/logname).write_text(p.stdout,encoding='utf-8')
        print(p.stdout[-1700:],flush=True)
    a=json.loads((BASE/'AUDIT_RESULTS.json').read_text())
    b=json.loads((BASE/'SCHMIDT_AUDIT.json').read_text())
    c=json.loads((BASE/'SCHMIDT_GENERAL_AUDIT.json').read_text())
    w=a['witness']
    assert w['input_nonzeros']==w['n']
    assert w['polyphase_rank']==w['m']
    assert w['hankel_rank']==w['maximum_hankel_rank']
    assert w['occupied_green_phase_modes']==w['m']
    assert w['phase9_one_step_innovation_rank']==w['m']-2
    assert w['exact_full_dft_mismatches']==0
    assert all(r['exact_modular_realignment_rank']==r['exact_theoretical_rank']
               for r in c['cases'])
    assert all(r['exact_fourier_realignment_rank']==r['n']
               for r in b['records'])
    print('ALL PHASE 10 TESTS + EXACT EVIDENCE CHECKS PASSED',flush=True)

if __name__=='__main__':main()
