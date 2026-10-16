"""Fresh exact controls; no historical code imports or execution."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def avoiding(n,b):
    a=[]
    for j in range(n+1):
        if j<b: v=1<<j
        elif j==b: v=(1<<b)-1
        else: v=2*a[-1]-a[j-b-1]
        a.append(v)
    return a


def marker_controls():
    exact=0; brute=0; lower=0; choice=0
    for n in range(2,257):
        N=1<<n
        for b in range(1,n):
            x=1<<b; d=n-b; a=avoiding(n,b)
            m=N//x+a[n]
            es=[(1<<(d-h))*a[h-1] for h in range(1,d+1)]
            assert sum(es)==N-m
            M=sum(h*e for h,e in enumerate(es,1))
            V=sum((n-h+1)*e for h,e in enumerate(es,1))
            H=m*(n+1)+M
            assert H+V==N*(n+1)
            assert M<=N*(2*x-b-2)
            exact+=1
            if n<=12:
                brute_a=sum('0'*b not in format(z,f'0{n}b') for z in range(N))
                assert brute_a==a[n]
                brute+=1
            if n>=16:
                assert (128*H)**2>=N*N*n
                lower+=1
                if b==(n.bit_length()-1)//2:
                    assert H*H<=400*N*N*n
                    assert (m*(n+1))**2>=N*N*n
                    choice+=1
    return dict(ledger_cases=exact,brute_avoiding_counts=brute,schedule_lower_controls=lower,sqrt_choice_controls=choice)


def root_sum(exponents,M):
    if M==1: return (len(exponents),)
    c=[0]*M
    for e in exponents: c[e%M]+=1
    return tuple(c[j]-c[j+M//2] for j in range(M//2))


def chirp_controls():
    grams=0; entries=0; cuts=0; negatives=0
    for n in range(1,11):
        N=1<<n
        for k in range(n+1):
            M=1<<(n-k); D=1<<k; R=min(M,D); H=max(M,D)
            for odd in (1,3):
                for a in range(M):
                    for d in range(D):
                        t=D*a+d
                        lhs=-odd*t*(t+1)//2
                        rhs=-odd*(D*a)*(D*a+1)//2-odd*d*(d+1)//2-odd*D*a*d
                        assert (lhs-rhs)%N==0
                        entries+=1
                for i in range(R):
                    for j in range(R):
                        exps=[odd*(i-j)*q for q in range(H)]
                        coeff=root_sum(exps,M)
                        target=(H if i==j else 0,)+(0,)*(len(coeff)-1)
                        assert coeff==target
                        grams+=1
                cuts+=1
            assert R*H==N
    # Deliberately omitting the cross term would yield rank one, but the
    # correct N=16 middle matrix has nonzero character inner-product data.
    assert root_sum([q for q in range(4)],4)==(0,0)
    assert root_sum([0 for q in range(4)],4)==(4,0)
    negatives+=1
    return dict(primitive_embedding_cut_cases=cuts,phase_entry_identities=entries,exact_gram_entries=grams,omitted_cross_term_detected=negatives)


def matvec(A,x): return [sum((a*b for a,b in zip(row,x)),F(0)) for row in A]
def norm2(x): return sum((v*v for v in x),F(0))
def nullvector(A,width):
    a=[list(row) for row in A]; piv=[]; ri=0
    for c in range(width):
        hit=next((j for j in range(ri,len(a)) if a[j][c]),None)
        if hit is None: continue
        a[ri],a[hit]=a[hit],a[ri]
        lead=a[ri][c]; a[ri]=[v/lead for v in a[ri]]
        for j in range(len(a)):
            if j!=ri:
                q=a[j][c]; a[j]=[v-q*w for v,w in zip(a[j],a[ri])]
        piv.append(c); ri+=1
        if ri==len(a): break
    free=next(c for c in range(width) if c not in piv)
    x=[F(0)]*width; x[free]=F(1)
    for r,c in enumerate(piv): x[c]=-a[r][free]
    assert any(x) and not any(matvec(A,x))
    return x


def robust_controls():
    cases=0; near=0; positive=0; negative=0
    for N in (4,16,64):
        root=int(N**0.5); assert root*root==N
        for k in (0,1,2):
            if k>=N: continue
            for t in (1,2,3):
                for b in (F(1,2),F(99,100),F(999,1000)):
                    # P sends e_j to e_(j+1); Q=I-bP is invertible since b<1.
                    Q=[[F(i==j)-b*F(i==(j+1)%N) for j in range(N)] for i in range(N)]
                    A=[[F(0)]*N for _ in range(N)]
                    for j in range(N):
                        for ell in range(t): A[(3*j+ell)%N][j]=F((j+ell)%5-2,3)
                    # E=V W has rank at most k. Use a reproducible dense W.
                    W=[[F(((i+1)*(j+3)+j*j)%11-5,7) for j in range(N)] for i in range(k)]
                    V=[[F(((i+2)*(j+1))%7-3,5) for j in range(k)] for i in range(N)]
                    WQcols=[[sum(W[i][a]*Q[a][j] for a in range(N)) for j in range(k+1)] for i in range(k)]
                    short=nullvector(WQcols,k+1) if k else [F(1)]
                    v=short+[F(0)]*(N-k-1)
                    z=matvec(Q,v); assert any(z)
                    assert not any(matvec(W,z))
                    Eqz=matvec(V,matvec(W,z)); assert not any(Eqz)
                    Az=matvec(A,v)
                    Uz=[sum((F(1 if (i&j).bit_count()%2==0 else -1,root)*z[j] for j in range(N)),F(0)) for i in range(N)]
                    assert norm2(Uz)==norm2(z)
                    residual=[u-a for u,a in zip(Uz,Az)]
                    support_z=sum(bool(q) for q in z); support_A=sum(bool(q) for q in Az)
                    assert support_z<=2*(k+1) and support_A<=t*(k+1)
                    bound=max(F(0),F(1)-F(2*t*(k+1)**2,N))
                    assert norm2(residual)>=bound*norm2(z)
                    # Independently inspect energy outside Av's support.
                    outside=sum((u*u for u,a in zip(Uz,Az) if not a),F(0))
                    assert outside>=max(F(0),F(1)-F(support_z*support_A,N))*norm2(z)
                    cases+=1; near+=b>F(9,10); positive+=bound>0
    # Wrong-kernel negative control: Ev=0 does not imply EQv=0.
    N=4; b=F(1,2); v=[F(1),F(0),F(0),F(0)]
    Qv=[F(1),-b,F(0),F(0)]
    E=[[F(j==1 and i==0) for j in range(N)] for i in range(N)]
    assert not any(matvec(E,v)) and any(matvec(E,Qv)); negative+=1
    # At b=1, Q annihilates the constant vector and the guard fails.
    Qsing=[[F(i==j)-F(i==(j+1)%N) for j in range(N)] for i in range(N)]
    assert not any(matvec(Qsing,[F(1)]*N)); negative+=1
    return dict(rational_witness_cases=cases,near_unit_gain_cases=near,positive_bound_cases=positive,negative_controls=negative)


if __name__=='__main__':
    out=dict(status='PASS',arithmetic='exact Python integers and fractions only',historical_code_executed=False,
             marker=marker_controls(),chirp=chirp_controls(),robust=robust_controls())
    target=Path(__file__).with_name('CONTROL_RESULTS.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
