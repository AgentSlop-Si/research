"""Independent exact controls: cyclic localization, discrepancy, and compatibility.
Only standard library. No uploaded code is imported or executed.
"""
from itertools import combinations
from fractions import Fraction
from random import Random
import json
from pathlib import Path
P=12289

def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*b)] for row in a]
def tr(a):return [list(x) for x in zip(*a)]
def sub(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def rank(a):
    if not a or not a[0]:return 0
    a=[r[:] for r in a];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]%P),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];v=pow(a[i][j],P-2,P)
        a[i]=[x*v%P for x in a[i]]
        for k in range(i+1,len(a)):
            q=a[k][j];a[k]=[(x-q*y)%P for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

def inv(a):
    n=len(a);b=[row[:]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next((k for k in range(j,n) if b[k][j]%P),None)
        if k is None:return None
        b[j],b[k]=b[k],b[j];v=pow(b[j][j],P-2,P);b[j]=[x*v%P for x in b[j]]
        for k in range(n):
            if k!=j:
                q=b[k][j];b[k]=[(x-q*y)%P for x,y in zip(b[k],b[j])]
    return [r[n:] for r in b]

def qs(n,r,rng):
    a=[[rng.randrange(P) if i==j else 0 for j in range(n)] for i in range(n)]
    for ch in range(r):
        low,up,left,right,ta,tb=[[rng.randrange(5) for _ in range(n)] for _ in range(6)]
        for i in range(n):
            for j in range(i):
                v=low[i]*left[j]
                for k in range(j+1,i):v*=ta[k]
                a[i][j]=(a[i][j]+v)%P
            for j in range(i+1,n):
                v=up[i]*right[j]
                for k in range(i+1,j):v*=tb[k]
                a[i][j]=(a[i][j]+v)%P
    return a

def cyc(n,start,w):return [(start+i)%n for i in range(w)]
def root(n):
    for a in range(2,P):
        w=pow(a,(P-1)//n,P)
        if all(pow(w,k,P)!=1 for k in range(1,n)) and pow(w,n,P)==1:return w
    raise AssertionError

def d2(a,i,j,k,l):return (a[i][k]*a[j][l]-a[i][l]*a[j][k])%P

rng=Random(215603);results={'field':P,'controls':{},'bitrev':[]}
assert all(P%d for d in range(2,112))
counts={'matrix_window_rank_bounds':0,'cyclic_exterior_bounds':0,'Fourier_full_ranks':0,'exact_cyclic_averages':0,'inverse_cut_rank_equalities':0,'Fourier_Cauchy_Binet_equalities':0}
for n in (4,8,12,16):
    w=root(n);F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)]
    for seed in range(5):
        rs=[1+int(seed==4),1,1]
        stages=[qs(n,r,rng) for r in rs]
        p1=list(range(n));p2=list(range(n));rng.shuffle(p1);rng.shuffle(p2)
        ip1=[p1.index(i) for i in range(n)];ip2=[p2.index(i) for i in range(n)]
        middle=mm(stages[1],[stages[0][ip1[i]] for i in range(n)])
        M=mm(stages[2],[middle[ip2[i]] for i in range(n)])
        q=list(range(n));rng.shuffle(q)
        for W in range(1,n):
            I=list(range(W));R=[ip2[i] for i in I]
            sums=[0]*(n+1)
            for start in range(n):
                J=cyc(n,start,W);C=[p1[j] for j in J]
                Jc=[j for j in range(n) if j not in J]
                assert rank(sub(stages[0],Jc,J))<=2*rs[0];counts['cyclic_exterior_bounds']+=1
                actual=rank(sub(M,I,J))
                for t in range(n+1):
                    aa=sum(x<t for x in R);bb=sum(x<t for x in C);sums[t]+=bb
                    assert actual<=2*rs[0]+rs[2]+rs[1]+W-abs(aa-bb)
                    counts['matrix_window_rank_bounds']+=1
                assert rank(sub(F,I,[q[j] for j in J]))==W;counts['Fourier_full_ranks']+=1
            assert sums==[W*t for t in range(n+1)];counts['exact_cyclic_averages']+=n+1
        for A in stages:
            B=inv(A)
            if B is None:continue
            for k in range(1,n):
                for I,J in [(range(k),range(k,n)),(range(k,n),range(k))]:
                    assert rank(sub(A,I,J))==rank(sub(B,I,J));counts['inverse_cut_rank_equalities']+=1
for n in (4,6):
    w=root(n);F=[[pow(w,i*j,P) for j in range(n)] for i in range(n)]
    for seed in range(3):
        U=[[rng.randrange(P) for _ in range(n)] for _ in range(n)]
        V=[[rng.randrange(P) for _ in range(n)] for _ in range(n)];K=mm(mm(U,F),V)
        pairs=list(combinations(range(n),2))
        for i,j in pairs:
            for k,l in pairs:
                rhs=sum(d2(U,i,j,a,b)*(pow(w,a*c+b*d,P)-pow(w,a*d+b*c,P))*d2(V,c,d,k,l) for a,b in pairs for c,d in pairs)%P
                assert d2(K,i,j,k,l)==rhs;counts['Fourier_Cauchy_Binet_equalities']+=1
for m in range(1,13):
    n=2**m;p=[int(f'{i:0{m}b}'[::-1],2) for i in range(n)]
    if m%2:w=(n+1)//3;t=w
    else:w=(n//2+1)//3;t=2*w-1
    aa=sum(p[i]<t for i in range(w));bb=sum(p[i]<t for i in range(n-w,n))
    assert aa-bb==(m+1)//2
    results['bitrev'].append({'m':m,'N':n,'W':w,'separator':t,'a':aa,'b':bb,'difference':aa-bb,'deleted_rows':w-aa,'deleted_columns':bb})
results['controls']=counts;results['all_passed']=True
path=Path(__file__).with_name('EXACT_CHECK_RESULTS.json');path.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
