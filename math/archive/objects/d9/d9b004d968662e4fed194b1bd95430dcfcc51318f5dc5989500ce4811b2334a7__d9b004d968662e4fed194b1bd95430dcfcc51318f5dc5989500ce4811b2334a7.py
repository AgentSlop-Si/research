#!/usr/bin/env python3
"""Independent Phase8 mathematical controls; no uploaded imports or execution."""
import collections,itertools,json,math,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent
rng=random.Random(202610092339)
def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def field(n):
    k=1
    while not prime(k*n+1):k+=1
    p=k*n+1;qs=[q for q in range(2,n+1) if n%q==0 and prime(q)]
    for a in range(2,p):
        w=pow(a,k,p)
        if all(pow(w,n//q,p)!=1 for q in qs):return p,w
    raise AssertionError('no root')
def rank(M,p):
    a=[list(r) for r in M];nr=len(a);nc=len(a[0]) if a else 0;r=0
    for j in range(nc):
        pivot=next((i for i in range(r,nr) if a[i][j]%p),None)
        if pivot is None:continue
        a[pivot],a[r]=a[r],a[pivot];iv=pow(a[r][j],-1,p)
        for i in range(r+1,nr):
            q=a[i][j]*iv%p
            if q:a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==nr:break
    return r

def inverse(M,p):
    n=len(M);A=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if A[i][j]%p),None)
        if pivot is None:return None
        A[pivot],A[j]=A[j],A[pivot];iv=pow(A[j][j],-1,p);A[j]=[v*iv%p for v in A[j]]
        for i in range(n):
            if i!=j:
                q=A[i][j];A[i]=[(x-q*y)%p for x,y in zip(A[i],A[j])]
    return [row[n:] for row in A]
def matmul(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def delta(A,B,p):return [[(x-y)%p for x,y in zip(row,col)] for row,col in zip(A,B)]
def poly(labels,n,w,p):
    P=[1]
    for j in labels:
        z=pow(w,-j,p);Q=[0]*(len(P)+1)
        for i,a in enumerate(P):Q[i]=(Q[i]-a*z)%p;Q[i+1]=(Q[i+1]+a)%p
        P=Q
    return P
def transfer(P,p):
    # Generate companion-operator powers, not uploaded long division.
    m=len(P)-1;v=[1]+[0]*(m-1);columns=[]
    for e in range(2*m):
        if e>=m:columns.append(v[:])
        lead=v[-1];v=[(-lead*P[0])%p]+[(v[i-1]-lead*P[i])%p for i in range(1,m)]
    return [list(row) for row in zip(*columns)]
def periodic(A,n):
    A=set(A)
    return any({(j+t)%n for j in A}==A for t in range(1,n))
def exact_poly(labels,n):
    # Work in Z[y]/(y^N-1), then reduce all coefficients modulo y^(N/2)+1.
    P=[[1]+[0]*(n-1)]
    for j in labels:
        Q=[[0]*n for _ in range(len(P)+1)]
        for i,row in enumerate(P):
            for e,c in enumerate(row):
                Q[i+1][e]+=c;Q[i][(e+j)%n]-=c
        P=Q
    return [tuple(row[e]-row[e+n//2] for e in range(n//2)) for row in P]

# Exhaustively recreate characteristic-zero polynomial supports and modular transfers.
n=16;p=17;w=3;allset=set(range(n));supports={};modpolys={};support_hist=collections.Counter()
for A in itertools.combinations(range(n),n//2):
    P=exact_poly(A,n);s=sum(any(row) for row in P);supports[A]=s;support_hist[s]+=1
    reduced=[sum(c*pow(w,-j,p) for j,c in enumerate(row))%p for row in P]
    Q=poly(A,n,w,p);assert reduced==Q
    modpolys[A]=Q
pair_hist=collections.Counter();transfer_hist=collections.Counter();rank_checks=0;minimum_nonpoly=99;minimum_nontransfer=999
for A in supports:
    B=tuple(sorted(allset-set(A)))
    if A>B:continue
    per=periodic(A,n);label='periodic' if per else 'nonperiodic'
    pair_hist[f'{supports[A]+supports[B]}_{label}']+=1
    RA=transfer(modpolys[A],p);RB=transfer(modpolys[B],p)
    assert rank(RA,p)==rank(RB,p)==rank(delta(RB,RA,p),p)==8
    rank_checks+=1
    count=sum(bool(v) for row in RA+RB for v in row)
    transfer_hist[f'{count}_{label}']+=1
    assert count>=16
    if count==16:assert A==tuple(range(0,16,2)) or B==tuple(range(0,16,2))
    if not per:
        minimum_nonpoly=min(minimum_nonpoly,supports[A]+supports[B]);minimum_nontransfer=min(minimum_nontransfer,count)
assert rank_checks==6435 and dict(support_hist)=={2:2,3:4,4:8,5:56,6:32,7:32,8:224,9:12512}
assert minimum_nonpoly==15 and minimum_nontransfer==94

# Full-root CRT identities, all splits for small N and fixed-seed samples beyond.
crt_rows=[]
for n in (2,4,6,8,10,12,16,20,30):
    p,w=field(n);m=n//2
    choices=list(itertools.combinations(range(n),m)) if n<=8 else [tuple(sorted(rng.sample(range(n),m))) for _ in range(20)]
    count=0
    for A in choices:
        B=tuple(j for j in range(n) if j not in A);RA=transfer(poly(A,n,w,p),p);RB=transfer(poly(B,n,w,p),p)
        assert rank(delta(RB,RA,p),p)==m
        assert rank(RA,p)==rank(RB,p)==m
        for labels,R in ((A,RA),(B,RB)):
            for label in labels:
                z=pow(w,-label,p)
                for e in range(m):assert sum(R[j][e]*pow(z,j,p) for j in range(m))%p==pow(z,m+e,p)
        count+=1
    crt_rows.append({'N':n,'p':p,'balanced_splits':count})

# All fixed consecutive cuts and explicit low-rank innovation telescoping.
cut_rows=[]
for n in (2,3,4,5,6,7,8,10,12,16,20,30):
    p,w=field(n);F=[[pow(w,-i*j,p) for j in range(n)] for i in range(n)]
    for m in range(1,n):assert rank([row[m:] for row in F[:m]],p)==min(m,n-m)
    cut_rows.append({'N':n,'cuts':n-1})
network_rows=[]
for n in (6,8,12):
    p,w=field(n);m=n//2
    for orders in ((1,),(1,0,2),(1,1,1,1)):
        I=[[int(i==j) for j in range(n)] for i in range(n)];T=I;Bprod=I
        for r in orders:
            B=[[rng.randrange(p) if (i<m)==(j<m) else 0 for j in range(n)] for i in range(n)]
            U=[[rng.randrange(p) for _ in range(r)] for i in range(n)]
            V=[[rng.randrange(p) for j in range(n)] for _ in range(r)]
            E=matmul(U,V,p) if r else [[0]*n for _ in range(n)]
            C=[[(B[i][j]+E[i][j])%p for j in range(n)] for i in range(n)]
            T=matmul(C,T,p);Bprod=matmul(B,Bprod,p)
        actual=rank(delta(T,Bprod,p),p);assert actual<=sum(orders)
        network_rows.append({'N':n,'orders':orders,'residual_rank':actual,'budget':sum(orders)})

# Sharpness with invertible baseline, and the omitted F3,N2 exception.
sharpness=[]
for n in (2,4,6,8,10,12,16,20):
    p,w=field(n);m=n//2;F=[[pow(w,-i*j,p) for j in range(n)] for i in range(n)]
    A=[row[:m] for row in F[:m]];B=[row[m:] for row in F[:m]];C=[row[:m] for row in F[m:]];D=[row[m:] for row in F[m:]]
    H=matmul(matmul(C,inverse(A,p),p),B,p);witness=None
    for t in range(2,p):
        X=[[t*v%p for v in row] for row in A];q=pow(1-t,-1,p);Y=[[(D[i][j]-q*H[i][j])%p for j in range(m)] for i in range(m)]
        if rank(Y,p)<m:continue
        base=[row+[0]*m for row in X]+[[0]*m+row for row in Y]
        assert rank(base,p)==n and rank(delta(F,base,p),p)==m;witness=t;break
    if n==2:
        assert p==3 and witness is None
        assert all(rank([[(1-a)%3,1],[1,(2-b)%3]],3)==2 for a in (1,2) for b in (1,2))
    else:assert witness is not None
    sharpness.append({'N':n,'p':p,'witness':witness,'N2_F3_exception':n==2})

# Standard independent radix-2 DIT; verify complete transforms and wire-form support.
def fft(seq,p,w):
    n=len(seq);bits=n.bit_length()-1
    def rev(i):
        out=0
        for _ in range(bits):out=2*out+(i&1);i>>=1
        return out
    a=[seq[rev(i)] for i in range(n)];butterflies=0
    for level in range(1,bits+1):
        length=1<<level;half=length//2
        for start in range(0,n,length):
            for j in range(half):
                u=a[start+j];v=a[start+j+half]*pow(w,-j*(n//length),p)%p
                a[start+j]=(u+v)%p;a[start+j+half]=(u-v)%p;butterflies+=1
    return a,butterflies
fft_rows=[]
for n in (2,4,8,16,32,64,128,256,512):
    p,w=field(n);x=[rng.randrange(p) for _ in range(n)];got,B=fft(x,p,w)
    target=[sum(v*pow(w,-j*k,p) for j,v in enumerate(x))%p for k in range(n)]
    assert got==target and B==n*(n.bit_length()-1)//2
    fft_rows.append({'N':n,'butterflies':B,'source_attainable_field_adds':2*B,'source_attainable_field_muls':B,'supplied_root_power_table_muls':n-1})
# Generic recursive simultaneous transfer evaluation, distinct from source division.
def evaluate(x,labels,n,p,w,mode):
    if len(labels)==1:return {labels[0]:x[0]}
    m=len(labels)//2
    if mode=='alternating':A=labels[::2];B=labels[1::2]
    else:A=labels[:m];B=labels[m:]
    outputs={}
    for sub in (A,B):
        R=transfer(poly(sub,n,w,p),p)
        rem=[(x[i]+sum(R[i][j]*x[m+j] for j in range(m)))%p for i in range(m)]
        outputs.update(evaluate(rem,sub,n,p,w,mode))
    return outputs
remainder_cases=0
for n in (4,8,16,32):
    p,w=field(n)
    for mode in ('alternating','contiguous'):
        for _ in range(3):
            x=[rng.randrange(p) for _ in range(n)];got=evaluate(x,list(range(n)),n,p,w,mode)
            assert [got[k] for k in range(n)]==[sum(v*pow(w,-k*j,p) for j,v in enumerate(x))%p for k in range(n)]
            remainder_cases+=1

semantic_rows=[]
for n in (4,8,16,32,64):
    p,w=field(n);levels=n.bit_length()-1
    # Individual output rows of partial block DFT, with disjoint supports at each block.
    seen=set()
    for s in range(levels+1):
        span=1<<s
        for start in range(0,n,span):
            for k in range(span):
                v=tuple(pow(w,-k*j*(n//span),p) if start<=q<start+span else 0 for q in range(n) for j in [q-start])
                assert sum(bool(a) for a in v)==span and v not in seen;seen.add(v)
    assert len(seen)==n*(levels+1)
    semantic_rows.append({'N':n,'distinct_projective_stage_forms':len(seen)})
# Dense-star witness: two triangular in-place shear passes.
star_rows=[]
for n in (4,8,16,32):
    p,w=field(n);M=[[1]*n]+[[2 if j==i else 1 for j in range(n)] for i in range(1,n)]
    assert rank(M,p)==n and all(v for row in M for v in row)
    assert M!=[[pow(w,-i*j,p) for j in range(n)] for i in range(n)]
    star_rows.append({'N':n,'field':p,'inplace_additions':2*n-2,'full_support_invertible':True})
# Complete truth table bound is literal p^r; no compressed-table conclusion.
truth=[]
for n in (16,64,256,1024):
    p,w=field(n);width=0
    while p**(width+1)<=n**3:width+=1
    assert width<=3
    truth.append({'N':n,'p':p,'max_width_with_N_cubed_entries':width})
output={'N16_exact_cyclotomic_support_histogram':dict(sorted(support_hist.items())),
'N16_complementary_polynomial_support_histogram':dict(sorted(pair_hist.items())),
'N16_modular_transfer_support_histogram':dict(sorted(transfer_hist.items())),
'N16_complementary_transfer_full_rank_checks':rank_checks,'N16_nonperiodic_polynomial_min':minimum_nonpoly,'N16_nonperiodic_modular_transfer_min':minimum_nontransfer,
'CRT_split_controls':crt_rows,'consecutive_cut_controls':cut_rows,'telescoping_network_controls':network_rows,'invertible_baseline_controls':sharpness,
'complete_FFT_controls':fft_rows,'generic_recursive_remainder_inputs':remainder_cases,'semantic_stage_wire_controls':semantic_rows,'dense_star_controls':star_rows,
'generic_polynomial_plan_field_ops_N16':3*(16*16-16+16*4)//2,'truth_table_controls':truth,
'uploaded_code_executed':False,'uploaded_modules_imported':False,'source_benchmark_execution_claim':False}
text=json.dumps(output,indent=2,sort_keys=True)+'\n';(ROOT/'INDEPENDENT_RESULTS.json').write_text(text);print(text,end='')
