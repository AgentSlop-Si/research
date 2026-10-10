"""Independently reconstruct N16 exact input matrices and a planted negative control."""
import json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
from reviewer_matrix_helper import inv,mm,cycle_green,rankdet

results=[]
for p,g,factors in [(998244353,3,[2,7,17]),(2013265921,31,[2,3,5])]:
    assert all(p%d for d in range(2,int(p**0.5)+1))
    assert all(pow(g,(p-1)//ell,p)!=1 for ell in factors)
    rec=json.loads((BASE/f'masks/fresh_N16_p{p}.json').read_text());n=16;ii=pow(g,(p-1)//4,p);zeta=pow(g,(p-1)//n,p)
    assert pow(zeta,n,p)==1 and pow(zeta,n//2,p)!=1 and pow(zeta,4,p)==ii
    alpha=[(a+b*ii)*pow(d,-1,p)%p for a,b,d in [(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6),(1,3,11)]]
    assert alpha==rec['alphas']
    gs=[cycle_green(c,[a]*n,p) for c,a in zip(rec['cycles'],alpha)]
    A=[[(gs[0][i][j]+(1+ii)*pow(3,-1,p)*gs[1][i][j])%p for j in range(n)] for i in range(n)]
    C=[[(gs[4][i][j]+(1-ii)*pow(4,-1,p)*gs[5][i][j])%p for j in range(n)] for i in range(n)]
    Ai,Ci=inv(A,p),inv(C,p);assert Ai and Ci
    F=[[pow(zeta,i*j,p) for j in range(n)] for i in range(n)]
    T=mm(mm(Ai,F,p),Ci,p);bs=[gs[s] for s in [2,3,6]]
    assert T==rec['T'] and bs==rec['Bs']
    text=(BASE/f'masks/n16_supplement/fresh_N16_p{p}.txt').read_text();nums=list(map(int,text.split()));flat=[n,p]+[x for M in [T]+bs for row in M for x in row]
    assert nums==flat
    row={'prime':p,'generator':g,'data_equal':True,'input_sha256':hashlib.sha256(text.encode()).hexdigest(),'detA':rankdet(A,p)[1],'detC':rankdet(C,p)[1]};results.append(row)
    if p==998244353:
        planted=[[sum(c*G[i][j] for c,G in zip([1,7,11],bs))%p for j in range(n)] for i in range(n)]
        out=[f'{n} {p}']+[' '.join(map(str,r)) for M in [planted]+bs for r in M]
        (HERE/'planted_negative_N16.txt').write_text('\n'.join(out)+'\n')
(HERE/'reviewer_inputs_results.json').write_text(json.dumps({'records':results,'source_programs_executed':False},indent=2)+'\n');print(results)
