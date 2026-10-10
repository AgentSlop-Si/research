"""New exact small-instance certificate and algebra controls; no uploaded code."""
import json,runpy
from pathlib import Path
h=runpy.run_path('research_round_2156/feedback_involution/check_two_cayley.py')
p=65537
ident,add,sub,scale,mul,inv,mv=[h[k]for k in ('ident','add','sub','scale','mul','inv','mv')]
def rank_det(A):
    M=[row[:]for row in A];r=0;det=1
    for j in range(len(M[0])):
        k=next((k for k in range(r,len(M))if M[k][j]%p),None)
        if k is None:continue
        if k!=r:M[r],M[k]=M[k],M[r];det=-det%p
        z=M[r][j]%p;det=det*z%p; zi=pow(z,-1,p);M[r]=[a*zi%p for a in M[r]]
        for i in range(len(M)):
            if i!=r:
                z=M[i][j];M[i]=[(a-z*b)%p for a,b in zip(M[i],M[r])]
        r+=1
        if r==len(M):break
    return r,det if r==len(M)==len(M[0])else 0
n=4;I=ident(n);P=[[int(j==(i+1)%n)for j in range(n)]for i in range(n)];sigma=[0,2,1,3]
Q=[[P[sigma[i]][sigma[j]]for j in range(n)]for i in range(n)]
assert mul(P,Q)!=mul(Q,P)
w=pow(3,(p-1)//n,p);assert w==65281
F=[[pow(w,i*j,p)for j in range(n)]for i in range(n)]
G=inv(sub(I,scale(3,P)));H=inv(sub(I,scale(5,Q)))
U=mul(F,G);V=mul(F,H)
coefs=[mul(U,U),add(mul(U,V),mul(V,U)),mul(V,V),scale(2,U),scale(2,V),I]
locations=[(0,0),(0,1),(0,2),(0,3),(1,0),(1,1)]
minor=[[C[i][j]for C in coefs]for i,j in locations]
rank,det=rank_det(minor);assert rank==6 and det==19255
controls=[]
for n in (2,4,8,16):
    I=ident(n);w=pow(3,(p-1)//n,p);F=[[pow(w,i*j,p)for j in range(n)]for i in range(n)];Fi=inv(F)
    for lam in (2,3):
        dp=lam*pow(1-lam,-1,p)%p;dm=-lam*pow(1+lam,-1,p)%p
        s=(dp+dm)%p;c=dp*dm%p;r=n//2
        Delta=[[((dp if i<r else dm) if i==j else 0)for j in range(n)]for i in range(n)]
        A=mul(Fi,Delta);Ai=inv(A);M=mul(F,A)
        assert add(sub(mul(M,M),scale(s,M)),scale(c,I))==scale(0,I)
        Pi=scale(pow((dp-dm)%p,-1,p),sub(M,scale(dm,I)))
        assert mul(Pi,Pi)==Pi and rank_det(Pi)[0]==r
        assert add(sub(mul(A,mul(F,A)),scale(s,A)),scale(c,Fi))==scale(0,I)
        K=sub(scale(1-lam*lam,M),scale(lam*lam,I));assert mul(K,K)==scale(lam*lam,I)
        B=inv(add(Fi,A))
        assert B==sub(scale(1-lam*lam,F),scale(lam*lam,Ai))
        assert B==add(scale(1+lam*lam,F),scale(lam*lam-1,mul(F,mul(A,F))))
        assert mul(B,A)==K and mul(sub(I,K),F)==B
        T=mul(inv(sub(I,K)),B);assert T==F
        D=[[pow(w,i,p)if i==j else 0 for j in range(n)]for i in range(n)]
        S=[[int(i==(j+1)%n)for j in range(n)]for i in range(n)]
        assert mul(D,T)==mul(T,S) and mv(T,[int(i==0)for i in range(n)])==[1]*n
        controls.append({'N':n,'lambda':lam,'projector_rank':r,'status':'PASS'})
result={'status':'PASS','prime':p,'noncommuting_two_Green_control_N':4,'minor_rank':rank,'minor_determinant':det,'minor_locations':locations,'minor':minor,'all_scalar_amplitudes_rejected':True,'valid_characteristic_zero_lift':True,'algebra_controls':controls,'algebra_control_count':len(controls)}
Path(__file__).with_name('SPECTRAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
