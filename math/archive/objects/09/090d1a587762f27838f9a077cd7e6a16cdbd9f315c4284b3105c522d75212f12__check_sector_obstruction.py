#!/usr/bin/env python3
"""Exact rational-frame certificate excluding signed high-x prefixes at N64."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'seed_compatibility_gate'))
from check_n16_outer_gate import PRIME as P,LABELS,green,pivots,determinant,is_prime
from check_lift_defects import cover_and_splice
from check_hierarchical_lift import lift
def main():
    assert is_prime(P)
    gs=[];routes=[];guards=[]
    for j,label in enumerate(LABELS):
        small,ps,_=cover_and_splice(4,4,label);_,pl,_=lift(small,ps,4,4,label)
        assert all(pl[(i+32)%64]==(pl[i]+32)%64 for i in range(64))
        for i in range(64):
            v=i
            for _ in range(32):v=pl[v]
            assert v==(i+32)%64
        d=j+2;assert d%P and (pow(d,64,P)-1)%P
        g=green(pl,d);tau=pow(d,-1,P);inv=[0]*64
        for i,v in enumerate(pl):inv[v]=i
        assert all((g[i][k]-tau*g[inv[i]][k])%P==int(i==k) for i in range(64) for k in range(64))
        gs.append(g);routes.append(pl);guards.append({'d':d,'d64_minus_1_mod_p':(pow(d,64,P)-1)%P})
    records=[];row0=[]
    for sign in (1,-1):
        for i in range(32):
            t=[[(g[i][k]+sign*g[i][k+32])%P for k in range(32)] for g in gs]
            columns=pivots(t);assert len(columns)==8
            minor=[[row[k] for k in columns] for row in t];det=determinant(minor);assert det
            rec={'row':i,'sector_sign':sign,'columns':columns,'determinant_mod_p':det}
            records.append(rec)
            if i==0:rec=dict(rec);rec['minor_mod_p']=minor;row0.append(rec)
    assert [r['determinant_mod_p'] for r in row0]==[140062647,726260818]
    direct_sum=[]
    for sign,selected,expected in [(1,[7,3,13,27],871168069),(-1,[12,4,26,8],682055007)]:
        # These rows have parity opposite the projected sector, so the target
        # Fourier rows vanish on that sector. Four 8-dimensional row frames
        # form a direct sum in the 32-dimensional sector.
        assert all((-1)**i==-sign for i in selected)
        stacked=[[(g[i][k]+sign*g[i][k+32])%P for k in range(32)] for i in selected for g in gs]
        det=determinant(stacked);assert det==expected and det
        direct_sum.append({'sector_sign':sign,'rows':selected,'determinant_mod_p':det,
                           'stacked_minor_mod_p':stacked})
    # Positive control: an ordinary coordinate row has both X characters;
    # the obstruction specifically concerns pure-character target rows.
    positive=[int(k==0) for k in range(64)]
    assert any(positive[k]+positive[k+32] for k in range(32))
    assert any(positive[k]-positive[k+32] for k in range(32))
    result={'status':'PASS_EXACT_CHARACTERISTIC_ZERO_OBSTRUCTION','prime':P,
            'prime_trial_division_verified':True,'fixed_rational_inverse_guards':guards,
            'nested_cycle_successors':routes,'projected_frame_minor_records':records,
            'minimal_row_zero_certificate':row0,
            'four_row_direct_sum_certificates':direct_sum,
            'scope':'Any prefix C with CX=+XC or CX=-XC is excluded for F64=O C when O is one fixed eight-Green row-masked layer. No algebraic-seed specialization is used.',
            'implication':'Both signed-symmetry one-inner branches are empty, including the plus-symmetric mean-preserving 128-variable branch.',
            'full_one_inner_mixing_family':'Open'}
    (HERE/'SECTOR_FRAME_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','projected_frame_minors':64,'row0_determinants':[r['determinant_mod_p'] for r in row0],
                      'direct_sum_determinants':[r['determinant_mod_p'] for r in direct_sum]}))
if __name__=='__main__':main()
