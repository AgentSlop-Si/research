"""Build exact 20-equation/16-variable dual Fourier support system over Z[z]/(z^4+1).

Produces denominator-free polynomials by *columnwise* clearing, not
multiplying by the product of six denominators. Column j of B is multiplied
by D*S_{p[j]}, with S_0=S_7=1 and D=t(z-1).
"""
from __future__ import annotations
import json,hashlib,time
from pathlib import Path
import numpy as np
from inverse_quartic import (ZERO,ONE,cpowroot,cadd,poly_constant,poly_var,
    padd,pscale,pmul,sum_polys,poly_eval,root8,eq_entries,SHUFFLE)
from dual_support import factor_from_dual
N=8
LAMBDA=cadd(cpowroot(1),(-1,0,0,0))

def construct_dual():
    x=[poly_var(i) for i in range(16)]
    t=x[0]; V=[t]+x[1:7]+[{}]; H=x[7:14]; beta=x[14]; gamma=x[15]
    one=poly_constant()
    D=pscale(t,LAMBDA)
    b_num=padd(padd(t,one,-1),pmul(beta,padd(H[0],one,-1)))
    T={}
    for k in range(1,7):
        first=pscale(padd(padd(one,pmul(beta,H[0]),-1),pmul(beta,H[k])),LAMBDA)
        second=pscale(b_num,cadd(cpowroot(-k),(-1,0,0,0)))
        T[k]=padd(first,second)
    q=[padd(poly_constant(cpowroot(i)),gamma,-1) for i in range(8)]
    S={k:sum_polys([pmul(q[i],H[i]) for i in range(k)]) for k in range(1,7)}
    R={k:sum_polys([pmul(q[i],T[i]) for i in range(k+1,7)]+[pmul(q[7],D)]) for k in range(1,7)}
    N={k:padd(pmul(D,q[k]),pmul(V[k],R[k]),+1) for k in range(1,7)}
    N={k:pscale(v,(-1,0,0,0)) for k,v in N.items()}
    Ccol={}
    for k in range(8):
        col=[]
        for i in range(8):
            if k==0:
                if i==0: e=D
                elif i==7:e=pmul(D,t)
                else:e=pmul(T[i],t)
            elif k==7:
                e=D if i==7 else pmul(D,H[i])
            elif i<k:
                e=pmul(H[i],N[k])
            elif i==k:
                e=pmul(S[k],D)
            elif i==7:
                e=pmul(pmul(S[k],D),V[k])
            else:
                e=pmul(pmul(S[k],T[i]),V[k])
            col.append(e)
        Ccol[k]=col
    # Bhat[i,j] = D*S[p[j]]*B[i,j] for interior columns, S=1 endpoints.
    Bhat=[]
    for i in range(8):
        Bhat.append([sum_polys([pscale(Ccol[k][m],cpowroot(i*m)) for m in range(8)]) for k in SHUFFLE])
    eqs=eq_entries(Bhat)
    eliminated={f'lower_{i}_1' for i in range(2,7)}|{f'upper_1_{j}' for j in range(2,7)}
    zeroed={name for name,e in eqs if not e}
    assert zeroed==eliminated,(zeroed,eliminated)
    remain=[(name,e) for name,e in eqs if name not in eliminated]
    assert len(remain)==20
    return remain,Bhat,S,D,dict(T=T,N=N,R=R)

def modular_validation(eqs,Bhat,S,D,repeats=12):
    output=[]
    for p in (12289,65537):
        for alternative in (False,True):
            omega=root8(p,alternative)
            rng=np.random.default_rng(20261009 + p+int(alternative))
            count=0
            for _ in range(repeats):
                y=list(map(int,rng.integers(1,p,size=16)))
                try:C,B,data=factor_from_dual(8,p,omega,SHUFFLE,y)
                except ZeroDivisionError: continue
                d=data['D']
                for i in range(8):
                    for j in range(8):
                        s=poly_eval(S[SHUFFLE[j]],y,p,omega) if 1<=SHUFFLE[j]<=6 else 1
                        want=d*s*int(B[i,j])%p
                        got=poly_eval(Bhat[i][j],y,p,omega)
                        assert got==want,(p,i,j,want,got)
                for name,e in eqs:
                    # Compare unscaled original B equation to polynomial with column-clearing factors
                    parts=name.split('_');i,j=map(int,parts[1:]);k=SHUFFLE[j]
                    sj=(poly_eval(S[k],y,p,omega) if 1<=k<=6 else 1)
                    if parts[0]=='lower':
                        u=(int(B[i,j])*int(B[7,0])-int(B[i,0])*int(B[7,j]))%p
                        scale=d*d*sj%p
                    else:
                        s7=poly_eval(S[SHUFFLE[7]],y,p,omega)
                        u=(int(B[i,j])*int(B[0,7])-int(B[i,7])*int(B[0,j]))%p
                        scale=d*d*sj*s7%p
                    assert poly_eval(e,y,p,omega)==u*scale%p,(name,p)
                count+=1
            output.append(dict(prime=p,embedding=int(alternative),root=omega,independent_samples=count,
                    checked_matrix_entries=count*64,checked_remaining_polynomial_equations=count*20))
    return output

def export(path):
    ts=time.monotonic()
    eqs,Bhat,S,D,extras=construct_dual()
    stat=dict(equations=len(eqs),variables=16,
      max_degree=max(len(m) for _,e in eqs for m in e),
      total_terms=sum(len(e) for _,e in eqs),
      distinct_monomials=len({m for _,e in eqs for m in e}),
      equation_lengths={name:len(p) for name,p in eqs},
      column_clearing_denominators='D=t*(z-1); interior j additionally S_[p[j]]',
      nonzero_required='t != 0, h0 != 0, S_1*...*S_6 != 0; plus B anchors, det C and inverse corners')
    vnames=['t']+[f'V{i}' for i in range(1,7)]+[f'h{i}' for i in range(7)]+['beta','gamma']
    obj=dict(ring='Z[z]/(z^4+1)',shuffle=SHUFFLE,variable_order=vnames,
      summary=stat,equations=[dict(name=name,terms=[[list(m),list(c)] for m,c in sorted(poly.items())]) for name,poly in eqs])
    raw=json.dumps(obj,sort_keys=True,separators=(',',':')).encode()+b'\n'
    Path(path).write_bytes(raw)
    stat['sha256']=hashlib.sha256(raw).hexdigest()
    stat['symbolic_generation_seconds']=round(time.monotonic()-ts,3)
    stat['modular_checks']=modular_validation(eqs,Bhat,S,D)
    return stat

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    stats=export(here/'dual_twenty_equations.json')
    (here/'dual_sparse_results.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))
