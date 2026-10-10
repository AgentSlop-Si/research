"""Freeze comparisons and graph diagnostics from independently produced data."""
from pathlib import Path
import json,hashlib,math
from itertools import combinations
import sympy as sp
P=Path(__file__).resolve().parent;S=P/'source/extracted/fft_cyclotomic_zero_forcing_v34'
a=json.loads((P/'forcing_receipt.json').read_text());b=json.loads((S/'forcing_results.json').read_text())
matched=0;maxima=[];six=[]
for l,L in enumerate(a['layers']):
    m=[]
    for z,v in enumerate(L):
        assert v['patterns']==math.comb(33,z)
        hist={str(k):n for k,n in enumerate(v['histogram']) if n}
        assert sum(hist.values())==v['patterns']
        if z<=5:
            assert hist==b['edge_deletion_enumeration'][l][str(z)]['min_seed_histogram'];matched+=v['patterns']
        m.append(max(map(int,hist)))
    maxima.append(m);six.append(L[6]['histogram'])
assert matched==852822 and maxima==[[2,3,3,3,3,3,4],[2,3,3,3,3,4,4],[2,3,3,3,3,4,4]]
u=json.loads((P/'restricted_verifier_receipt.json').read_text())
r=json.loads((P/'restricted_forcing_receipt.json').read_text())
restricted=[]
for l,L in enumerate(r['layers']):
    n=len(u['optional_nonunit_edge_indices'][l]);assert len(L)==n+1
    for z,v in enumerate(L):assert v['patterns']==math.comb(n,z)
    hist=[sum(v['histogram'][k] for v in L) for k in range(12)]
    assert sum(hist)==2**n and max(k for k,c in enumerate(hist) if c)==3
    restricted.append(hist)
E=json.loads((S/'topology_11.json').read_text())['layers']
overlaps=[]
for L in E:
    rows=[{c for r,c in L if r==i} for i in range(11)]
    overlaps.append(sum(len(x&y)==1 for x,y in combinations(rows,2)))
uni=json.loads((P/'unique_path_receipt.json').read_text())['single_routes']
exponents=[]
for path in uni:
    v=[0]*99
    for l,e in enumerate(path['edges']):v[l*33+e]=1
    exponents.append(v)
assert overlaps==[27,23,25] and sp.Matrix(exponents).rank()==22
out={'source_v34_seven_edge_theorem':'accepted in its integral model',
     'matched_source_deletion_patterns':matched,'source_and_six_deletion_patterns':sum(v['patterns'] for L in a['layers'] for v in L),
     'forcing_maxima_deletions_0_through_6':maxima,'six_deletion_histograms':six,
     'restricted_pattern_histograms':restricted,'restricted_total_patterns':81920,
     'restricted_maximum_forcing_numbers':[3,3,3],
     'independent_triangular_certificate_verification':u['passes'],
     'new_theorem':'No pi-integral Fourier factorization exists on this fixed support, over any valuation ring whose residue has characteristic 11 and zeta maps to 1.',
     'general_graph_lemma':'Over every field, the fixed support cannot produce a rank-one transfer with all 121 entries nonzero.',
     'not_excluded':['algebraic coefficients with poles at the chosen valuation','unrestricted complex coefficients','nonunit endpoint gauge changes that alter the integral model'],
     'row_pairs_intersecting_once':overlaps,'single_route_exponent_rank_Q':22,
     'source_files_executed_or_imported':False,'external_files_written':False}
(P/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
