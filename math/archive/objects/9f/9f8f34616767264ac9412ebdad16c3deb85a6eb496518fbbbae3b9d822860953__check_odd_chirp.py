"""Exact newly authored odd-chirp algebra controls; no uploaded code."""
import json,runpy
from pathlib import Path
h=runpy.run_path('research_round_2156/feedback_involution/check_two_cayley.py')
ident,add,sub,scale,mul,inv,mv=[h[k]for k in ('ident','add','sub','scale','mul','inv','mv')]
def setp(p):
    for fn in (ident,add,sub,scale,mul,inv,mv):fn.__globals__['p']=p

def rank(M,p):
    M=[row[:] for row in M];r=0
    for j in range(len(M[0])):
        k=next((i for i in range(r,len(M))if M[i][j]%p),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r];z=pow(M[r][j]%p,-1,p);M[r]=[a*z%p for a in M[r]]
        for i in range(len(M)):
            if i!=r:
                z=M[i][j];M[i]=[(a-z*b)%p for a,b in zip(M[i],M[r])]
        r+=1
        if r==len(M):break
    return r

def controls(p,n,g):
    setp(p);I=ident(n);half=(n+1)//2;w=pow(g,(p-1)//n,p)
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n)if n%d==0)
    av=[pow(w,half*j*j,p)for j in range(n)];stream=[];a=1;rr=pow(w,half,p)
    for j in range(n):stream.append(a);a=a*rr%p;rr=rr*w%p
    assert stream==av
    ai=[pow(a,-1,p)for a in av];A=[[av[i]if i==j else 0 for j in range(n)]for i in range(n)];Ai=[[ai[i]if i==j else 0 for j in range(n)]for i in range(n)]
    F=[[pow(w,i*j,p)for j in range(n)]for i in range(n)];Fb=[[pow(w,(-i*j)%n,p)for j in range(n)]for i in range(n)];Fi=scale(pow(n,-1,p),Fb)
    G=sum(av)%p;Gm=sum(ai)%p;c=n*G%p;assert G*Gm%p==n%p
    M=mul(F,A);M2=mul(M,M);M3=mul(M,M2)
    assert M2==scale(G,mul(Ai,Fb)) and M3==scale(c,I)
    R=[[int(i==(-j)%n)for j in range(n)]for i in range(n)]
    Mm=mul(F,Ai);assert mul(Mm,mul(Mm,Mm))==scale(n*Gm,mul(R,I))
    assert mul(Mm,mul(Mm,Mm))!=scale(n*Gm,I)
    d=rank([[I[i][j],M[i][j],M2[i][j]]for i in range(n)for j in range(n)],p)
    if n>=5:assert d==3
    if (1+c)%p==0:
        assert rank(add(I,M),p)<n
        return {'p':p,'N':n,'resonant':True,'c':c,'I_plus_M_rank':rank(add(I,M),p),'basis_vectors':0}
    den=pow(1+c,-1,p)
    B=inv(add(Fi,A))
    assert B==scale(den,add(sub(F,mul(F,mul(A,F))),scale(c,Ai)))
    assert B==scale(den,add(sub(F,scale(G,mul(Ai,mul(Fb,Ai)))),scale(c,Ai)))
    K=mul(B,A);K2=mul(K,K);K3=mul(K,K2);H=sub(I,K)
    assert sub(K3,scale(c,mul(H,mul(H,H))))==scale(0,I)
    pinv=add(add(scale(1+c,I),scale(1-2*c,K)),scale(1+c,K2))
    assert mul(H,pinv)==I and pinv==add(I,M)
    T=mul(pinv,B);assert T==F
    assert rank([[I[i][j],K[i][j],K2[i][j]]for i in range(n)for j in range(n)],p)==d
    D=[[pow(w,i,p)if i==j else 0 for j in range(n)]for i in range(n)]
    S=[[int(i==(j+1)%n)for j in range(n)]for i in range(n)]
    assert mul(H,mul(D,B))==mul(B,mul(S,sub(I,mul(A,B))))
    assert mv(H,[1]*n)==mv(B,[int(i==0)for i in range(n)])
    for j in range(n):
        x=[int(i==j)for i in range(n)];u=mv(B,x);v=[(1+c)*a%p for a in u]
        for coeff in (1-2*c,1+c):
            v=[(a+coeff*b)%p for a,b in zip(mv(B,mv(A,v)),u)]
        assert v==mv(F,x)
    return {'p':p,'N':n,'resonant':False,'c':c,'span_I_M_M2_rank':d,'basis_vectors':n}

cases=[]
for p,ns,factors in ((241,(3,5,15),(2,3,5)),(65521,(3,5,7,9,13,15,21,35,39,45,63),(2,3,5,7,13))):
    g=next(g for g in range(2,p)if all(pow(g,(p-1)//q,p)!=1 for q in factors))
    for n in ns:cases.append(controls(p,n,g))
cases.append(controls(7,3,3));assert cases[-1]['resonant']
result={'status':'PASS','cases':len(cases),'nonresonant_cases':sum(not c['resonant']for c in cases),'resonance_controls':sum(c['resonant']for c in cases),'basis_vectors':sum(c['basis_vectors']for c in cases),'fourier_output_entries':sum(c['N']*c['basis_vectors']for c in cases),'case_details':cases}
Path(__file__).with_name('ODD_CHIRP_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
