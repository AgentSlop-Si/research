"""New exact structural controls for the forced B, without uploaded code."""
import json,runpy
from pathlib import Path
h=runpy.run_path('research_round_2156/feedback_involution/check_two_cayley.py')
ident,add,sub,scale,mul,inv=[h[k]for k in ('ident','add','sub','scale','mul','inv')]
def setp(p):
    for f in (ident,add,sub,scale,mul,inv):f.__globals__['p']=p

def rank(M,p):
    M=[r[:]for r in M];r=0
    if not M or not M[0]:return 0
    for j in range(len(M[0])):
        k=next((k for k in range(r,len(M))if M[k][j]%p),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r];z=pow(M[r][j]%p,-1,p);M[r]=[a*z%p for a in M[r]]
        for i in range(len(M)):
            if i!=r:
                z=M[i][j];M[i]=[(a-z*b)%p for a,b in zip(M[i],M[r])]
        r+=1
        if r==len(M):break
    return r

def rect(M,I,J):return [[M[i][j]for j in J]for i in I]
def rowsupp(M):return max(sum(v!=0 for v in row)for row in M)
def makeP(pi):return [[int(j==pi[i])for j in range(len(pi))]for i in range(len(pi))]
results=[];cuts=spans=greenchecks=products=defects=0
for n,p,w in [(n,65521,pow(17,(65521-1)//n,65521))for n in (3,5,7,9,13,15,21)]+[(5,521,104)]:
    setp(p);I=ident(n);half=(n+1)//2;m=n//2
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n)if n%d==0)
    av=[pow(w,half*j*j,p)for j in range(n)];A=[[av[i]if i==j else 0 for j in range(n)]for i in range(n)]
    F=[[pow(w,i*j,p)for j in range(n)]for i in range(n)];Fi=inv(F);X=add(A,Fi);c=n*sum(av)%p
    assert (1+c)%p
    B=inv(X);assert rowsupp(X)==n
    if p==521:assert [X[i][i]for i in range(n)]==[418,24,0,0,24]
    perms=[[(i+1)%n for i in range(n)],[(i+m)%n for i in range(n)]]
    sig=list(range(n));sig[0],sig[1]=sig[1],sig[0]
    perms.append([sig[(sig[i]+1)%n]for i in range(n)])
    crosses=[0]*len(perms)
    denominators=[]
    for pi in perms:
        P=makeP(pi);Q=sub(I,scale(2,P));denominators.append(Q)
        assert pow(2,n,p)!=1
    for t in range(n):
        left=sorted((t+j)%n for j in range(m));right=sorted(set(range(n))-set(left))
        rb=rank(rect(B,left,right),p);rx=rank(rect(X,left,right),p);rf=rank(rect(Fi,left,right),p)
        assert rb==rx==rf==m;cuts+=1
        for k,(pi,Q) in enumerate(zip(perms,denominators)):
            e=sum(pi[i]in right for i in left);crosses[k]+=e
            Z=inv(Q);assert rank(rect(Z,left,right),p)==rank(rect(Q,left,right),p)==e
            greenchecks+=1
    for pi,e in zip(perms,crosses):
        dist=sum(min((i-pi[i])%n,(pi[i]-i)%n)for i in range(n));assert e==dist;spans+=1
    # Products with endpoint swaps: inverse supports, including routing that changes the tested cut.
    E=makeP(sig);candidate=I
    for ell,Q in enumerate(denominators,1):
        factor=mul(E,mul(inv(Q),E));candidate=mul(factor,candidate)
        ci=inv(candidate);assert rowsupp(ci)<=min(n,2**ell)
        if 2**ell<n:assert candidate!=B
        products+=1
    # Two actual rank-one inverse defects, in the correct inverse product order.
    S0,S1=denominators[:2]
    E0=[[2 if i==0 else 0 for j in range(n)]for i in range(n)]
    E1=[[2 if j==1 else 0 for j in range(n)]for i in range(n)]
    Q0=add(S0,E0);Q1=add(S1,E1)
    assert rank(E0,p)==rank(E1,p)==1
    testB=mul(inv(Q1),inv(Q0));base=mul(S0,S1);err=sub(inv(testB),base)
    assert err==add(mul(E0,S1),mul(Q0,E1)) and rank(err,p)<=2 and rowsupp(base)<=4
    if 2<n//6:assert testB!=B
    defects+=1
    results.append({'N':n,'p':p,'inverse_max_rowsupp':rowsupp(X),'zero_inverse_diagonal_entries':sum(X[i][i]==0 for i in range(n)),'half_cut_rank':m,'guard_1_plus_c':(1+c)%p})
result={'status':'PASS','target_cases':len(results),'full_half_cut_checks':cuts,'Green_cut_rank_checks':greenchecks,'circular_displacement_identities':spans,'product_inverse_support_controls':products,'inverse_defect_controls':defects,'cases':results}
Path(__file__).with_name('CHIRP_B_GATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
