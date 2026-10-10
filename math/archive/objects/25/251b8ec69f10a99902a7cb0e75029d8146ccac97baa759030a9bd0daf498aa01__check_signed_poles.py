#!/usr/bin/env python3
"""One finite pole family, target-only equations, and a paid mixing component."""
from pathlib import Path
import sys,json,itertools,collections
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'seed_compatibility_gate'))
from check_n16_outer_gate import PRIME as P,LABELS,green,pivots,determinant,is_prime,multiply
from check_lift_defects import cover_and_splice
from check_hierarchical_lift import lift
def main():
    assert is_prime(P)
    ps=[];gs=[];positions=[]
    for label in LABELS:
        t,p,_=cover_and_splice(4,4,label);_,q,_=lift(t,p,4,4,label);ps.append(q)
        gs.append([green(q,2),green(q,P-2)])
        order=[0]*64;v=0
        for k in range(64):order[v]=k;v=q[v]
        assert v==0;positions.append(order)
    assert all(ps[0][k]%32==ps[1][k]%32 for k in range(32))
    equations=[]
    for i in (0,1):
        exponents=[[(pos[i]-pos[k])%32 for k in range(32)] for pos in positions]
        minus_signs=[[(-1)**(((pos[i]-pos[k])%64)//32) for k in range(32)] for pos in positions]
        for j in range(8):
            for choice,tau in enumerate([pow(2,-1,P),-pow(2,-1,P)%P]):
                for sigma in (1,-1):
                    guard=(1-sigma*pow(tau,32,P))%P;assert guard
                    for k in range(32):
                        sign=1 if sigma==1 else minus_signs[j][k]
                        expected=sign*pow(tau,exponents[j][k],P)*pow(guard,-1,P)%P
                        actual=(gs[j][choice][i][k]+sigma*gs[j][choice][i][k+32])%P
                        assert expected==actual
        equations.append({'physical_row':i,'exponents':exponents,'minus_signs':minus_signs,
                          'plus_signs':'all +1','denominator_per_term':'1-sigma*tau_j^32',
                          'necessary_pole_equations':'all 8-by-8 minors in the forbidden sector vanish; rank and full-support guards remain required'})
    records=[];counts=collections.Counter()
    for pattern in itertools.product((0,1),repeat=8):
        rec={'pole_signs':[1 if c==0 else -1 for c in pattern],'pole_magnitude_denominator':2,'minus_sector_witnesses':[]}
        for i in (0,1):
            t=[[(gs[j][pattern[j]][i][k]-gs[j][pattern[j]][i][k+32])%P for k in range(32)] for j in range(8)]
            cols=pivots(t);assert len(cols)==8;det=determinant([[row[k] for k in cols] for row in t]);assert det
            rec['minus_sector_witnesses'].append({'row':i,'columns':cols,'determinant_mod_p':det})
        plus=[[(gs[j][pattern[j]][0][k]+gs[j][pattern[j]][0][k+32])%P for k in range(32)] for j in range(8)]
        pp=pivots(plus);expected=7 if pattern[0]==pattern[1] else 8;assert len(pp)==expected
        if expected==7:assert plus[0]==plus[1]
        rec['plus_sector_rank']=expected
        if expected==8:rec['plus_sector_nonzero_minor']=determinant([[row[k] for k in pp] for row in plus])
        else:
            independent=pivots([list(row) for row in zip(*plus)])
            assert len(independent)==7
            rec['plus_rank_seven_witness']={'rows':independent,'columns':pp,
                'determinant_mod_p':determinant([[plus[r][c] for c in pp] for r in independent])}
            rec['forced_kernel']='span((1,-1,0,0,0,0,0,0))'
        counts[expected]+=1;records.append(rec)
    # Exact combinatorial rank of the permutation difference: 16 two-cycles
    # and 32 fixed points in P0^{-1}P1 give rank 64-(16+32)=16 over Q.
    inv=[0]*64
    for i,j in enumerate(ps[0]):inv[j]=i
    rel=[inv[ps[1][i]] for i in range(64)];seen=set();cycles=[]
    for i in range(64):
        if i in seen:continue
        cyc=[];v=i
        while v not in seen:seen.add(v);cyc.append(v);v=rel[v]
        assert v==i;cycles.append(cyc)
    assert sorted(map(len,cycles))==[1]*32+[2]*16
    diff=[[(gs[0][0][i][j]-gs[1][0][i][j])%P for j in range(64)] for i in range(64)]
    assert len(pivots(diff))==16
    assert all((diff[i][j]+diff[i][j+32])%P==0 for i in range(64) for j in range(32))
    mixing=[[(1 if i<32 else -1)*x%P for x in row] for i,row in enumerate(diff)]
    assert len(pivots(mixing))==16
    assert all(mixing[i+32]==mixing[i] for i in range(32))
    assert all((mixing[i][j]+mixing[i][j+32])%P==0 for i in range(64) for j in range(32))
    result={'status':'PASS_BOUNDED_POLE_FAMILY','prime':P,'family_size':256,
            'legal_guard_mod_p':(pow(2,64,P)-1)%P,'target_pole_equations':equations,
            'schedules':records,'plus_sector_rank_counts':dict(counts),
            'commuting_or_anticommuting_prefix_escape_schedules':0,
            'mixing_component':{'poles':[{'term':0,'tau':'1/2'},{'term':1,'tau':'1/2'}],
                'operator':'diag(chi_x)*(G_H0minus-G_H0plus)','rank':16,
                'input_sector':'minus','output_sector':'plus','Green_terms_charged':2,
                'left_masks':['chi_x','-chi_x'],'relative_permutation_cycles':cycles,
                'scalar_pole_guard_for_this_fixed_N64_component':'tau != 0 and tau^64 != 1',
                'opposite_direction_or_full_Fourier_lift':'not supplied'},
            'scope':'One finite signed-common-magnitude pole family; no exclusion of arbitrary schedules or genuine mixing lifts.'}
    (HERE/'SIGNED_POLE_FAMILY_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','schedules':256,'plus_rank_counts':dict(counts),'signed_prefix_escapes':0,'paid_mixing_rank':16}))
if __name__=='__main__':main()
