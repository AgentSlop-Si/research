"""Fresh reviewer controls. No author/recovered program is executed or imported."""
import json, math, itertools, hashlib
from fractions import Fraction as Q
from pathlib import Path

def mm(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def inv(a,p):
    n=len(a);a=[row[:]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]);a[j],a[k]=a[k],a[j]
        u=pow(a[j][j],-1,p);a[j]=[x*u%p for x in a[j]]
        for k in range(n):
            if k!=j:
                u=a[k][j];a[k]=[(x-u*y)%p for x,y in zip(a[k],a[j])]
    return [r[n:] for r in a]
def trans(a):return list(map(list,zip(*a)))
def mono(a):return all(sum(x!=0 for x in r)==1 for r in a) and all(sum(x!=0 for x in c)==1 for c in zip(*a))

def bank(a,m,b,p,w):
    n=a*m*b;P=[[0]*n for _ in range(n)];R=[[0]*n for _ in range(n)];B=[[0]*n for _ in range(n)]
    for r0,t2,r1,r2 in itertools.product(range(a),range(b),range(m),range(b)):
        R[(r0*b+t2)*m+r1][r0+a*r1+a*m*r2]=pow(w,a*r1*t2+a*m*r2*t2,p)
    for t0,t1,t2,r0 in itertools.product(range(a),range(m),range(b),range(a)):
        P[t2+b*t1+b*m*t0][(r0*b+t2)*m+t1]=pow(w,r0*(t2+b*t1)+m*b*r0*t0,p)
    for q,t1,r1 in itertools.product(range(a*b),range(m),range(m)):
        B[q*m+t1][q*m+r1]=pow(w,a*b*r1*t1,p)
    F=[[pow(w,k*j,p) for j in range(n)] for k in range(n)]
    assert mm(mm(P,B,p),R,p)==F
    S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
    D=[[pow(w,j,p) if i==j else 0 for j in range(n)] for i in range(n)]
    for H in [R,trans(P)]:
        I=inv(H,p);assert mono(mm(mm(H,S,p),I,p));assert mono(mm(mm(H,D,p),I,p))
    return {'a':a,'m':m,'b':b,'N':n,'p':p,'omega':w,'identity':True,'Q_and_PT_actions_monomial':True,'P_shift_action_row0':mm(mm(P,S,p),inv(P,p),p)[0]}

def cycles(v):
    seen=set();n=0
    for a in range(len(v)):
        if a in seen:continue
        n+=1
        while a not in seen:seen.add(a);a=v[a]
    return n

def sorting():
    total=0;strides=0;stats=[]
    for n in range(2,11):
        hist={};s0=0;rs=[]
        for bits in itertools.product([0,1],repeat=n):
            L=sorted(range(n),key=lambda j:bits[j]);W=[0]*n
            for i in range(n):W[L[i]]=L[(i+1)%n]
            T=sum(a!=b for a,b in zip(bits,bits[1:]));r=n-cycles([(v-1)%n for v in W]);s=sum(v!=(j+1)%n for j,v in enumerate(W))
            assert r==2*(T//2);assert s==(0 if T<=1 else r+1);hist[r]=hist.get(r,0)+1;s0+=s==0;rs.append(r)
            for a in range(1,n):
                rank=n-cycles([(v-a)%n for v in W]);ma=sum(v==(j+a)%n for j,v in enumerate(W));qa=sum(bits[j]==bits[j+a] and all(x!=bits[j] for x in bits[j+1:j+a]) for j in range(n-a));assert 2*rank>=n-ma;assert ma<=qa+2;strides+=1
            total+=1
        assert s0==2*n
        for r,count in hist.items():assert count==2*math.comb(n,r+1)
        mean=Q(sum(rs),len(rs));var=sum((Q(r)-mean)**2 for r in rs)/len(rs)
        if n>=3:assert mean==Q(n,2)-1 and var==Q(n,4)
        stats.append({'N':n,'words':len(rs),'mean':str(mean),'variance':str(var),'zero_changed_words':s0})
    return {'words':total,'word_strides':strides,'stats':stats}

def det(a):
    if len(a)==1:return a[0][0]
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

def gram():
    tests=0
    for r in [Q(0),Q(1,3),Q(2,5),Q(3,4),Q(1)]:
        A=[[1,r,0,0],[r,1,0,0],[0,0,1,-r],[0,0,-r,1]];B=[[1,0,r,0],[0,1,0,-r],[r,0,1,0],[0,-r,0,1]];C=[[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        for x in map(Q,range(-2,5)):
            actual=det([[x*int(i==j)-C[i][j] for j in range(4)] for i in range(4)])
            assert actual==(x-(1+r)**2)*(x-(1-r)**2)*(x-(1-r*r))**2;tests+=1
    affine=[]
    for s in range(2,22,2):
        n=s*s;h=s//2;tau=[s*(j//s)+(j%s+h)%s for j in range(n)];u=(tau[1]-tau[0])%n;ok=all(tau[j]==(u*j+tau[0])%n for j in range(n));assert ok==(s==2);affine.append({'s':s,'half_grid_affine':ok})
    return {'exact_gram_evaluations':tests,'half_grid_controls':affine}

cases=[(1,1,1,17,1),(1,2,1,17,16),(2,2,2,17,2),(4,2,2,17,3),(3,2,2,97,6),(2,3,2,97,6),(4,4,4,257,81)]
records=[]
for a,m,b,p,w in cases:
    n=a*m*b
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0)
    records.append(bank(a,m,b,p,w))
assert records[2]['P_shift_action_row0']==[0,0,0,8,0,0,0,10]
out={'ALG045':records,'sorting':sorting(),'two_sided_gauge':gram(),'historical_programs_executed':False}
Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'bank_cases':len(records),'sorting_words':out['sorting']['words'],'sorting_word_strides':out['sorting']['word_strides'],'gram_checks':out['two_sided_gauge']['exact_gram_evaluations'],'all_passed':True}))
