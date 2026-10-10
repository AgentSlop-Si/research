"""Run all Phase 12 checks and verify persistent exact-witness data."""
from __future__ import annotations
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).parent

def main():
    p=subprocess.run([sys.executable,'-m','unittest','discover','-p','test_*.py','-v'],
                     cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    print(p.stdout)
    if p.returncode:raise SystemExit(p.returncode)
    needed=['witness_n4096.json','witness_n841_prime_square.json','witness_product_escape.json',
            'witness_p29.json','thresholds.json']
    for name in needed:
        obj=json.loads((ROOT/name).read_text())
        if name=='witness_n4096.json':
            assert obj['sum_green_rank']<=2 and obj['dft_rank']==3
        if name=='witness_n841_prime_square.json':
            assert obj['modular_sample']['sum_green_block_rank']<=2
            assert obj['modular_sample']['dft_minor_det']!=0
        if name=='witness_product_escape.json':
            assert obj['product_crosscut_rank']==3
        if name=='witness_p29.json':
            assert obj['fourier_minor_cyclotomic']['cyclotomic_remainder_nonzero']
    print('Exact certificate JSON validation: PASS')
    return 0
if __name__=='__main__':raise SystemExit(main())
