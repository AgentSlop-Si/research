"""Produces finite exact certificates and arithmetic-stage counts; no wall-time claims."""
from scan_hybrid import *
import json
from pathlib import Path

def main():
    gen=random.Random(20261009)
    basis=0
    random_tests=0
    fft_profiles=[]
    for n in [2,4,8,16,32,64,128]:
        for j in range(n):
            x=[int(k==j) for k in range(n)]
            y,cost=fft_via_two_scans(x)
            assert y==dft_direct(x)
            basis+=1
        for _ in range(5):
            x=[gen.randrange(P) for _ in range(n)]
            y,cost=fft_via_two_scans(x)
            assert y==dft_direct(x)
            random_tests+=1
        fft_profiles.append({'N':n,**cost,'minimal_scan_count':n.bit_length()-1})
    hybrid=[]
    matrix_audits=0
    for n in [4,8,16]:
        for t in [0,1,2,3,4]:
            for b in [0,1,2,3]:
                cert=word_certificate(random_word(n,t,b,n*1000+t*10+b))
                matrix_audits+=1
        hybrid.append({'N':n,'broadcast_rank_min_by_scans':[
                {'scans':t,'needed_rank':minimum_broadcast_rank_budget(n,t)}
                for t in range(n.bit_length())]})
    table=[]
    for n in [16,64,256,1024,4096,65536]:
        table.append({'N':n,'min_rank_one_broadcasts':[
            {'scan_passes':t,'broadcast_rank_min':minimum_broadcast_rank_budget(n,t)}
            for t in [0,1,2,n.bit_length()//2,n.bit_length()-2,n.bit_length()-1]]})
    bidir=[bidirectional_sum_escape(n) for n in [4,8,16,32]]
    assert all(r['inverse_all_entries_nonzero'] for r in bidir)
    results={'bidirectional_sum_escape':bidir,'status':'PASS','statement':'restricted exact scan+shuffle+low-rank-broadcast obstruction, NOT arbitrary FFT lower bound',
             'finite_field_modulus':P,'basis_columns':basis,'fresh_random_inputs':random_tests,
             'random_inverse_word_checks':matrix_audits,'construction_profiles':fft_profiles,
             'hybrid_verified_profiles':hybrid,'tradeoff_examples':table}
    out=Path(__file__).with_name('audit_results.json')
    out.write_text(json.dumps(results,indent=2)+'\n')
    print(f'PASS basis_columns={basis} random_inputs={random_tests} random_word_checks={matrix_audits}')
    print('N=64 tradeoff',[(t,minimum_broadcast_rank_budget(64,t)) for t in range(7)])
    print('FFT control N=128',fft_profiles[-1])
    return results
if __name__=='__main__':main()
