"""Independent 2x2 minor audit via full signed monomial expansion.
Rather than assuming vertex-disjoint cancellation, explicitly collect all
pairs of path monomials, cancel integer coefficients, and check valuations.
"""
from pathlib import Path
from itertools import combinations
import json, collections
P=Path(__file__).resolve().parent
R=json.loads((P/'REVIEW_RECEIPT.json').read_text());weights=[x//2 for x in R['weights']]
assert all(2*a==b for a,b in zip(weights,R['weights']))
paths={(e['output'],e['input']):e['paths'] for e in R['exact_tropical_entries']}
all_minors=[];fail=[];single=[]
for i,j in combinations(range(11),2):
 for k,l in combinations(range(11),2):
    poly=collections.defaultdict(int)
    for sign,one,two in [(1,(i,k),(j,l)),(-1,(i,l),(j,k))]:
        for p in paths[one]:
            for q in paths[two]:poly[tuple(sorted(p+q))]+=sign
    poly={a:c for a,c in poly.items() if c}
    assert all(c in (-1,1) for c in poly.values())
    terms=[{'edges':a,'coefficient':c,'valuation':sum(weights[e] for e in a)} for a,c in sorted(poly.items())]
    vals=[x['valuation'] for x in terms]+[1]
    m=min(vals);cnt=vals.count(m)
    rec={'rows':[i,j],'cols':[k,l],'terms':terms,'minimum':m,'minimum_count_including_target':cnt}
    all_minors.append(rec)
    if cnt<2:fail.append(rec)
    if len(terms)==1:single.append(rec)
# Small residue-face certificate, without a gauge assumption.
E={tuple((e['output'],e['input'])):e for e in R['exact_tropical_entries']}
expected={(1,5):[(28,48,67)],(1,6):[(6,48,67)],(6,5):[(28,48,83)],(6,6):[(6,48,83),(12,36,72)]}
for pair,es in expected.items():
    ent=E[pair]; assert ent['minimum']==0
    observed={tuple(p) for p,v in zip(ent['paths'],ent['path_values']) if v==0}
    assert observed==set(es)
first=next(d for d in single if d['rows']==[0,7] and d['cols']==[0,3])
assert first['terms']==[{'edges':(23,31,33,53,66,73),'coefficient':-1,'valuation':0}]
source=json.loads(Path('research_cycle_1734/pole_escape/minor_tropical_receipt.json').read_text())
assert len(all_minors)==3025 and len(fail)==source['failed_minors']==8
assert [(x['rows'],x['cols']) for x in fail]==[(x[0],x[1]) for x in source['failed_minor_coordinates']]
out={'status':'PASS','method':'Full determinant expansion and exact signed monomial collection; no disjoint-path premise used','minors_checked':len(all_minors),'failed_tropical_minors':len(fail),'single_monomial_minors':single,'failed_minor_coordinates':[[x['rows'],x['cols']] for x in fail],'four_equation_initial_face_contradiction_verified':True,'scope':'The exact normalized witness ray and its displayed initial-equation face are excluded. No global pole exclusion follows.'}
(P/'MINOR_REVIEW_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
