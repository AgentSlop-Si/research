"""Independently authored formula controls, using only own earlier matrix helpers."""
import json, runpy
from pathlib import Path
h=runpy.run_path('research_round_2156/feedback_involution/check_two_cayley.py')
I_fn,add,sub,scale,mul,inv=[h[k] for k in ('ident','add','sub','scale','mul','inv')]
p=998244353
for fn in (I_fn,add,sub,scale,mul,inv): fn.__globals__['p']=p

def rank(M):
    M=[row[:] for row in M]; r=0
    if not M:return 0
    for j in range(len(M[0])):
        k=next((i for i in range(r,len(M)) if M[i][j]),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r]; z=pow(M[r][j],-1,p);M[r]=[v*z%p for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][j]:
                z=M[i][j];M[i]=[(u-z*v)%p for u,v in zip(M[i],M[r])]
        r+=1
    return r

cases=[]
for n in (6,8,10,12,16,32):
    I=I_fn(n);P=[[int(j==(i+1)%n) for j in range(n)] for i in range(n)]
    sigma=list(range(n));sigma[2],sigma[4]=sigma[4],sigma[2]
    Q=[[P[sigma[i]][sigma[j]] for j in range(n)] for i in range(n)]
    J=[[((-1)**i)%p if i==j else 0 for j in range(n)] for i in range(n)]
    assert mul(P,Q)!=mul(Q,P)
    assert mul(J,mul(P,J))==scale(-1,P) and mul(J,mul(Q,J))==scale(-1,Q)
    assert (1-pow(2,n,p))%p and (1-pow(3,n,p))%p
    U=sub(scale(2,inv(sub(I,scale(2,P)))),I)
    Z=sub(scale(2,inv(sub(I,scale(3,Q)))),I)
    assert mul(U,Z)!=mul(Z,U)
    C=mul(U,Z); Ci=inv(C);Ai=inv(U);A=U
    B=scale(2,mul(C,mul(J,mul(Ci,Ai))))
    K=mul(B,A);assert mul(K,K)==scale(4,I)
    assert any(K[i][j]!=(K[0][0] if i==j else 0) for i in range(n) for j in range(n))
    Delta=scale(pow(-3%p,-1,p),add(scale(2,J),scale(4,I)))
    T=mul(inv(sub(I,K)),B)
    assert T==mul(C,mul(Delta,mul(Ci,Ai)))
    assert T==scale(pow(-3%p,-1,p),add(B,mul(K,B)))
    K0=mul(scale(2,mul(Z,J)),U)
    comm=mul(Z,mul(inv(U),mul(inv(Z),U)))
    assert mul(K0,K0)==scale(4,comm)
    assert mul(K0,K0)!=scale(4,I)
    cutrank=rank([row[n//2:] for row in T[:n//2]])
    if n>=10:assert cutrank<=5
    f_rank=None
    if (p-1)%n==0:
        om=pow(3,(p-1)//n,p)
        F=[[pow(om,i*j,p) for j in range(n)] for i in range(n)]
        f_rank=rank([row[n//2:] for row in F[:n//2]])
        assert f_rank==n//2
        if n>=12:assert T!=F and cutrank<f_rank
    cases.append({'N':n,'exact_minimal_degree':2,'direct_ansatz_degree_two_rejected':True,'T_cut_rank':cutrank,'Fourier_cut_rank':f_rank})
result={'status':'PASS','prime':p,'conjugation_controls':len(cases),'noncommutation_checks':len(cases),'commutator_formula_checks':len(cases),'direct_ansatz_rejections':len(cases),'cut_checks':sum(c['N']>=10 for c in cases),'Fourier_rank_checks':sum(c['Fourier_cut_rank'] is not None for c in cases),'cases':cases}
Path(__file__).with_name('CONJUGATED_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
