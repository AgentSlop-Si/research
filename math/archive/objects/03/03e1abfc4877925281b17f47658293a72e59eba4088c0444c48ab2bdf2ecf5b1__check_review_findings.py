"""Fresh review-owned checks. Reads/imports/executes no supplied program."""
from fractions import Fraction as Q
from pathlib import Path
import json
out=Path(__file__).resolve().parent
# A valid but non-excluding cut in any four-stage split-input graph:
# delete every stage-0 input terminal's unit wire. All starts are isolated.
n=256;k=8
B=[j for j in range(n) if ((j>>4)&1)!=((j>>3)&1)]
def reverse_bits(j):
    ans=0
    for _ in range(k):
        ans=2*ans+(j&1);j//=2
    return ans
P=[reverse_bits(j) for j in range(n)]
rotate=lambda j: ((j<<1)&(n-1)) | (j>>(k-1))
cert={'n':n,'stage_orders':[1]*4,'permutation':'middle_rotate','shuffles':[P,[rotate(j) for j in P],P],
      'input_set':'middle-partition B','output_set':'middle-partition A','fourier_rank':n//2,'upper_rank':len(B),
      'cut_edges':[{'from':[0,'x',j,'i'],'to':[0,'x',j,'o'],'capacity':1} for j in B],
      'modular_determinants':[]}
assert len(B)==n//2
assert len({tuple(e['from']) for e in cert['cut_edges']})==len(B)
assert all(tuple(e['from'])==(0,'x',j,'i') for j,e in zip(B,cert['cut_edges']))
assert sum(e['capacity'] for e in cert['cut_edges'])==cert['upper_rank']
assert not cert['upper_rank']<cert['fourier_rank']
assert all(False for _ in cert['modular_determinants']) # Vacuously true; no witness was checked.
(out/'NONEXCLUDING_MIXED_CUT.json').write_text(json.dumps(cert,indent=2)+'\n')
# Condition anchoring example in rational arithmetic: omit normalization sqrt(2),
# which is a scalar and does not alter condition. D has kappa8, G*D=H has kappa1.
D=[[Q(8),Q(0)],[Q(0),Q(1)]]
G=[[Q(1,8),Q(1)],[Q(1,8),Q(-1)]]
def mul(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
H=mul(G,D)
assert H==[[1,1],[1,-1]]
assert G[0][0]*G[1][1]+G[0][1]*G[1][0]==0
assert mul(list(map(list,zip(*H))),H)==[[2,0],[0,2]]
summary={'status':'PASS','source_program_execution':'none','source_program_import':'none','source_compilation':'none','source_ast_parsing':'none',
         'mixed_cut':{'n':n,'cut_capacity':len(B),'target_rank':n//2,'strict_obstruction':False,'target_rank_witness_count':0,
                      'interpretation':'Fresh malformed-certificate fixture. By static evaluation of assigned verifier lines39-74, it satisfies its checks: all starts isolated by valid unit wires, mixed-kind inequality absent, determinant loop empty. The supplied verifier was NOT run.'},
         'omitted_initial_condition':{'initial_diagonal_condition':8,'condition_after_permitted_cross_ratio_minus_one_gate':1,
                                      'condition_with_identity_output_diagonal':1,'true_maximum_including_initial_diagonal':8,
                                      'interpretation':'Exact two-coordinate illustration of why checking only gate/output endpoints can underreport the maximum. This does not assert any recorded optimizer result was actually wrong.'}}
(out/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
