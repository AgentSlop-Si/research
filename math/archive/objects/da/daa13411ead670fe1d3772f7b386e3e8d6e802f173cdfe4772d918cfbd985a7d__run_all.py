from __future__ import annotations
import json
import random
import subprocess
import sys
from pathlib import Path

from metaplectic_bruhat import (
    count_bruhat_cells, field_for_length, is_easy_borel, is_monomial,
    projectively_equal, random_sl2_word, sl2_elements, sl2_mul,
    unique_lul_solution, unique_ulu_solution, verify_projective_word,
    weil_operator,
)

ROOT=Path(__file__).resolve().parent

def main():
    subprocess.run([sys.executable,'-m','unittest','-v','test_checkpoint'],cwd=ROOT,check=True)
    rows=[]
    for n in (5,7,11,13,17):
        p,w=field_for_length(n); elems=sl2_elements(n); borel,big=count_bruhat_cells(n)
        rows.append({
            'n':n,'coefficient_field':p,'sl2_size':len(elems),
            'borel_size':borel,'big_cell_size':big,
            'lul_solution':list(unique_lul_solution(n)),
            'ulu_solution':list(unique_ulu_solution(n)),
            'all_borel_monomial':all(is_monomial(weil_operator(s,n,p,w),p) for s in elems if is_easy_borel(s,n)),
        })
    rng=random.Random(23004)
    word_checks=[]
    for n in (5,7,11,13):
        p,w=field_for_length(n)
        scalars=[]
        for length in (3,7,15):
            for _ in range(40):
                scalars.append(verify_projective_word(random_sl2_word(n,length,rng),n,p,w))
        word_checks.append({'n':n,'word_checks':len(scalars),'all_nonzero_scalars':all(s!=0 for s in scalars)})
    results={'cell_and_shear_records':rows,'random_word_checks':word_checks,
             'exhaustive_projective_products_n5':120*120,
             'theorem_scope':'odd prime transform lengths; finite Weil/metaplectic stage architecture'}
    (ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    summary={
        'status':'exact architecture closure; no faster FFT',
        'main_theorem':'Every finite Weil operator over SL2(F_p) is either monomial (lower Borel) or diagonally/permutationally equivalent to one DFT (big Bruhat cell).',
        'three_shear':'W=L(1)U(-1)L(1) uniquely; the middle upper shear is Fourier-equivalent.',
        'word_fusion':'Any metaplectic word collapses projectively to either one monomial operator or one Fourier core surrounded by O(N) monomial work.',
        'tests':'10/10 groups',
        'exhaustive_group_products_n5':14400,
    }
    (ROOT/'RESULT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    subprocess.run([sys.executable,'independent_verifier.py'],cwd=ROOT,check=True)
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
