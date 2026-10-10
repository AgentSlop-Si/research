"""Fresh exact checks. No source program is imported or executed."""
from pathlib import Path
from itertools import combinations
from math import comb
import json, hashlib
import sympy as sp
P=Path(__file__).resolve().parent
S=P/'source/extracted/fft_cyclotomic_zero_forcing_v34'

def fourier_minor(p,I,J):
    # Determinant by row insertion and column-subset DP, in Z[x]/(x^p-1).
    k=len(I);d={0:[1]+[0]*(p-1)}
    for row in I:
        q={}
        for mask,v in d.items():
            for col in range(k):
                if mask>>col&1:continue
                nxt=mask|(1<<col);w=q.setdefault(nxt,[0]*p)
                sign=(-1)**((mask>>(col+1)).bit_count())
                shift=row*J[col]%p
                for e,c in enumerate(v):w[(e+shift)%p]+=sign*c
        d=q
    v=d[(1<<k)-1]
    return [a-v[-1] for a in v[:-1]]

def pi_divide(p,c):
    # Solve c=(zeta-1)d over the integral power basis.
    assert sum(c)%p==0
    t=-sum(c)//p;d=[];prior=0
    for a in c:
        prior=prior-a-t;d.append(prior)
    assert d[-1]==t
    return d

def pi_multiply(c):
    return [-c[0]-c[-1]]+[c[j-1]-c[j]-c[-1] for j in range(1,len(c))]

def pi_value(p,c):
    if not any(c):return None,None
    k=0
    while sum(c)%p==0:
        old=c;c=pi_divide(p,c);assert pi_multiply(c)==old;k+=1
    return k,c

def leading_residue(p,I,J):
    ans=1
    for V in (I,J):
        for a,b in combinations(V,2):ans=ans*(b-a)%p
    f=1;den=1
    for r in range(len(I)):
        if r:f=f*r%p
        den=den*f%p
    return ans*pow(den,-1,p)%p

def check(p,I,J):
    c=fourier_minor(p,I,J);v,u=pi_value(p,c)
    assert v==len(I)*(len(I)-1)//2,(p,I,J,v)
    assert sum(u)%p==leading_residue(p,I,J),(p,I,J,c,u)
    return {'p':p,'rows':I,'columns':J,'cyclotomic_coefficients':c,
            'valuation':v,'unit_quotient':u,'unit_residue':sum(u)%p}

out={'method':'exact repeated division by zeta minus one in the integral power basis','exhaustive':{},'p11':[]}
for p in (2,3,5,7):
    hist={}
    for k in range(1,p+1):
        sets=list(combinations(range(p),k));n=0
        for I in sets:
            for J in sets:check(p,I,J);n+=1
        assert n==comb(p,k)**2;hist[k]=n
    out['exhaustive'][p]=hist
source=json.loads((S/'valuation_results.json').read_text())
x=sp.Symbol('x')
for v in source['p11_certificates']:
    r=check(11,v['rows'],v['cols'])
    poly=sum(c*x**j for j,c in enumerate(r['cyclotomic_coefficients']))
    norm=int(sp.resultant(sum(x**j for j in range(11)),poly,x))
    assert norm==int(v['norm'])
    r['norm']=str(norm);out['p11'].append(r)
out['full_range_p11']=[check(11,list(range(k)),list(range(k))) for k in range(1,12)]
assert pi_value(11,fourier_minor(11,[0,0],[1,2]))==(None,None)
for r in out['p11']:
    c=r['cyclotomic_coefficients'];v,u=pi_value(11,pi_multiply(c));assert v==r['valuation']+1
ls=json.loads((S/'topology_11.json').read_text())['layers']
flat=[]
for E in ls:
    M=sp.zeros(11)
    assert len(E)==len(set(map(tuple,E)))==33
    assert all(sum(r==j for r,c in E)==3 and sum(c==j for r,c in E)==3 for j in range(11))
    for r,c in E:M[r,c]=1
    flat.append({'integer_determinant':int(M.det()),'determinant_mod11':int(M.det())%11})
assert [d['determinant_mod11'] for d in flat]==[2,3,3]
out['flat_determinants']=flat
out['controls']={'duplicate_row_minor_is_zero':True,'pi_multiplication_adds_one':True,'all_leading_residues_match_vandermonde_formula':True}
(P/'arithmetic_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'exhaustive_minor_count':sum(sum(h.values()) for h in out['exhaustive'].values()),'source_p11_norms_verified':len(out['p11']),'full_p11_valuation':out['full_range_p11'][-1]['valuation'],'flat_determinants':flat}))
