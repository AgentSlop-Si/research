"""Fresh exact residue binomial-subsystem audit for an already checked weight.
Only JSON input is read. No other author's code is imported or executed.
"""
from pathlib import Path
import json, collections, math
import sympy as s
P=Path(__file__).resolve().parent
R=json.loads((P/'REVIEW_RECEIPT.json').read_text())
rows=[]; signs=[]; labels=[]
for entry in R['exact_tropical_entries']:
    m=entry['minimum']
    terms=[p for p,val in zip(entry['paths'],entry['path_values']) if val==m]
    if m==0:
        if len(terms)!=1:continue
        row=[0]*99
        for e in terms[0]:row[e]+=1
        sign=0
    elif len(terms)==2:
        row=[0]*99
        for e in terms[0]:row[e]+=1
        for e in terms[1]:row[e]-=1
        sign=1
    else:continue
    rows.append(row);signs.append(sign);labels.append([entry['output'],entry['input']])
M=s.Matrix(rows)
relations=M.T.nullspace(); odd=[]
for v in relations:
    den=s.ilcm(*[x.q for x in v]);ivec=[int(x*den) for x in v]
    g=math.gcd(*ivec);ivec=[x//g for x in ivec]
    assert all(sum(ivec[i]*rows[i][j] for i in range(len(rows)))==0 for j in range(99))
    parity=sum(x*b for x,b in zip(ivec,signs))%2
    if parity:
        odd.append({'coefficients':ivec,'nonzero_entries':[[labels[i],a,signs[i]] for i,a in enumerate(ivec) if a]})
out={'binomial_rows':len(rows),'negative_sign_rows':sum(signs),'rank_over_Q':M.rank(),'rational_kernel_dimension':len(relations),'primitive_rational_basis_odd_sign_relations':odd,'equation_labels':labels,'exponent_rows':rows,'right_hand_side_minus_one_powers':signs}
if odd:out['conclusion']='Exact contradiction: multiplying binomial equations with the first listed integer exponents yields 1=-1 in characteristic 11. This valuation pattern cannot lift.'
else:out['conclusion']='No contradiction found in this primitive rational-kernel basis. This does not prove all integer-kernel relations are consistent and does not prove a lift.'
# A concrete solution avoids relying on a non-saturated rational kernel basis.
F=[[a%2 for a in row]+[b] for row,b in zip(rows,signs)]; piv=[]; ii=0
for j in range(99):
    kk=next((kk for kk in range(ii,len(F)) if F[kk][j]),None)
    if kk is None:continue
    F[ii],F[kk]=F[kk],F[ii]
    for kk in range(len(F)):
        if kk!=ii and F[kk][j]:F[kk]=[a^b for a,b in zip(F[kk],F[ii])]
    piv.append(j);ii+=1
bad=[r for r in F if not any(r[:-1]) and r[-1]]
if not bad:
    yy=[0]*99
    for ii,j in enumerate(piv):yy[j]=F[ii][-1]
    assert all(sum(a*b for a,b in zip(row,yy))%2==rhs for row,rhs in zip(rows,signs))
    out['exact_plus_minus_one_solution']=[(-1)**v for v in yy]
    out['rank_over_F2']=len(piv)
    out['conclusion']='All 50 extracted binomial initial equations admit this explicit nonzero plus/minus-one solution in characteristic 11. Remaining multi-term initial equations are not certified by this subsystem.'
(P/'BINOMIAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['primitive_rational_basis_odd_sign_relations','equation_labels','exponent_rows','right_hand_side_minus_one_powers']},indent=2))
if odd:print(json.dumps(odd[0]['nonzero_entries']))
