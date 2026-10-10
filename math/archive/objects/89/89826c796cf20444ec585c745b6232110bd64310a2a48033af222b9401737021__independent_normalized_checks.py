#!/usr/bin/env python3
"""Fresh exact corroboration. Standard library only; reads no predecessor files.
All asymptotic claims are proved in the report, not inferred from these tests.
"""
import json
from pathlib import Path

P = 65537
TAU = next(a for a in range(2, P) if a*a % P == 2)
INVTAU = pow(TAU, -1, P)

def labels(n,b):
    L=1<<(b-1)
    out=set()
    for h in range(2*b+1,n+1):
        for f in range(1<<h):
            w=format(f, '0%db'%h)
            for t in range(1,min(L,h-2*b)+1):
                k=w[b:b+t]
                if w[:b]=='0'*b and k[0]==k[-1]=='1' and '0'*b not in k and w[b+t:2*b+t]=='0'*b:
                    out.add((h,f))
    return out

def antichain(candidates,n):
    # Full low-bit trie has <2N nodes. Parent strips the highest bit.
    inherited=[False]
    keep=[]
    for h in range(1,n+1):
        current=[]
        for f in range(1<<h):
            old=inherited[f % (1<<(h-1))]
            hit=(h,f) in candidates
            if hit and not old: keep.append((h,f))
            current.append(old or hit)
        inherited=current
    return keep

def closure(candidates,n):
    needed=[set() for _ in range(n+1)]
    for h,f in candidates:
        needed[h].update((q,f) for q in range(1<<(n-h)))
    for h in range(n,0,-1):
        M=1<<(n-h)
        for q,f in needed[h]:
            f0=f% (1<<(h-1))
            needed[h-1].add((q,f0))
            needed[h-1].add((q+M,f0))
    return needed

def raw_row_inner(n,a,b):
    # Exact C[z]/(z^(N/2)+1), conjugation sends z to z^-1.
    N=1<<n
    ha,qa,fa=a; hb,qb,fb=b
    ma=N>>ha; mb=N>>hb
    v=[0]*(N//2)
    for s in range(N):
        if s%ma==qa and s%mb==qb:
            e=(s*(fa-fb))%N
            v[e%(N//2)]+=1 if e<N//2 else -1
    return v

def field_case(n,b,embedding,full_bank_control=False):
    N=1<<n; L=1<<(b-1); H0=0 if full_bank_control else n-L
    root=pow(3,((P-1)//N)*embedding,P)
    assert pow(root,N,P)==1 and pow(root,N//2,P)!=1
    all_candidates=labels(n,b)
    high={c for c in all_candidates if c[0]>=H0}
    cut=antichain(high,n)
    E=set()
    for h,f in high: E.update(range(f,N,1<<h))
    disjoint=set()
    rows=[]
    for h,f in cut:
        cyl=set(range(f,N,1<<h))
        assert not disjoint.intersection(cyl)
        disjoint.update(cyl)
        rows.extend((h,q,f) for q in range(N>>h))
    assert E==disjoint and len(rows)==len(E)
    need=closure(high,n)
    projections=[]
    for j in range(H0+1):
        projected={e% (1<<j) for e in E}
        expected={(q,f) for f in projected for q in range(N>>j)}
        assert need[j]==expected
        assert len(need[j])>=len(E)
        projections.append(len(need[j]))
    assert sum(len(need[j]) for j in range(1,H0+1))>=H0*len(E)
    xs=[[((i*i+3*i+7)*(embedding+11)+i**3)%P for i in range(N)]]
    if N<=32: xs += [[int(i==j) for i in range(N)] for j in range(N)]
    row_values=0; recovery_values=0; chirp_values=0; recurrence_values=0
    negative_sign=False; negative_chirp=False
    for x in xs:
        layers=[{(q,0):x[q] for q in range(N)}]
        for h in range(1,n+1):
            M=N>>h; half=1<<(h-1); prev=layers[-1]; new={}
            for q in range(M):
                phase=pow(root,q*half,P)
                for f in range(half):
                    a=prev[q,f]; c=prev[q+M,f]
                    new[q,f]=(a+c)*INVTAU%P
                    new[q,f+half]=(a-c)*phase*INVTAU%P
                    if new[q,f+half]!=(a+c)*phase*INVTAU%P: negative_sign=True
            layers.append(new)
        for h in range(n+1):
            M=N>>h; scale=pow(INVTAU,h,P)
            for (q,f),got in layers[h].items():
                expected=scale*sum(x[s]*pow(root,s*f,P) for s in range(q,N,M))%P
                assert got==expected
                recurrence_values+=1
        ynorm=[pow(INVTAU,n,P)*sum(x[s]*pow(root,s*l,P) for s in range(N))%P for l in range(N)]
        recovered={}
        for h,f in cut:
            M=N>>h; vscale=pow(INVTAU,n-h,P)
            for v in range(M):
                got=vscale*sum(layers[h][q,f]*pow(root,q*v*(1<<h),P) for q in range(M))%P
                l=f+v*(1<<h)
                assert got==ynorm[l]
                recovered[l]=got; recovery_values+=1
            for q in range(M):
                back=vscale*sum(ynorm[f+v*(1<<h)]*pow(root,-q*v*(1<<h),P) for v in range(M))%P
                assert back==layers[h][q,f]
                recovery_values+=1
        # Reconstruct every high packet directly from the recovered partial Fourier values.
        for h,f in high:
            M=N>>h; vscale=pow(INVTAU,n-h,P)
            for q in range(M):
                got=vscale*sum(recovered[f+v*(1<<h)]*pow(root,-q*v*(1<<h),P) for v in range(M))%P
                assert got==layers[h][q,f]
                row_values+=1
        # Independent ordinary polynomial convolution, including all outputs as a control.
        aa=[x[j]*pow(root,j*(j-1)//2,P)%P for j in range(N)]
        bb=[pow(root,-t*(t+1)//2,P) for t in range(-(N-1),N)]
        cc=[0]*(3*N-2)
        for j,a in enumerate(aa):
            for k,c in enumerate(bb): cc[j+k]=(cc[j+k]+a*c)%P
        for l in range(N):
            bare=cc[N-1+l]*pow(INVTAU,n,P)%P
            got=bare*pow(root,l*(l+1)//2,P)%P
            assert got==ynorm[l]
            if bare!=ynorm[l]: negative_chirp=True
            chirp_values+=1
    assert negative_sign and negative_chirp
    orthogonality_pairs=0
    if N<=64:
        for i,a in enumerate(rows):
            for j,c in enumerate(rows):
                v=raw_row_inner(n,a,c)
                expected=[0]*(N//2)
                if i==j: expected[0]=1<<a[0]
                assert v==expected
                orthogonality_pairs+=1
    return {'n':n,'b':b,'embedding':embedding,'N':N,'full_bank_control':full_bank_control,'high_labels':len(high),'antichain_labels':len(cut),'high_outputs':sum(N>>h for h,f in high),'rank_high':len(E),'ancestor_counts_through_H0':projections,'inputs':len(xs),'recurrence_values':recurrence_values,'regenerated_values':row_values,'bank_conversion_values':recovery_values,'chirp_values':chirp_values,'exact_cyclotomic_inner_products':orthogonality_pairs,'negative_controls':True}

def combinatorial_case(n,b):
    N=1<<n; L=1<<(b-1); H0=n-L
    cand={c for c in labels(n,b) if c[0]>=H0}
    cut=antichain(cand,n)
    E=set(e for h,f in cand for e in range(f,N,1<<h))
    cutE=[e for h,f in cut for e in range(f,N,1<<h)]
    assert len(cutE)==len(set(cutE))==len(E) and set(cutE)==E
    needed=closure(cand,n)
    counts=[len(s) for s in needed]
    for j in range(H0+1):
        assert counts[j]==len({e%(1<<j) for e in E})*(N>>j)
        assert counts[j]>=len(E)
    return {'n':n,'b':b,'L':L,'H0':H0,'rank_high':len(E),'high_outputs':sum(N>>h for h,f in cand),'cut_labels':len(cut),'all_ancestor_counts':counts}

def cover_case(w,b):
    assert w%2==0
    m=w//2; pattern='1'+'0'*b+'1'; Q=1<<w
    T={v for v in range(Q) if pattern in format(v,'0%db'%w)[:m] and pattern in format(v,'0%db'%w)[m:]}
    assert T
    mask=sum(1<<t for t in T); full=(1<<Q)-1; remain=full; chosen=[]
    while remain:
        best=(-1,None,None)
        for a in range(Q):
            rot=((mask<<a)|(mask>>(Q-a)))&full
            count=(remain&rot).bit_count()
            if count>best[0]: best=(count,a,rot)
        assert best[0]>0
        chosen.append(best[1]); remain &= ~best[2]
    assert all(any((v-a)%Q in T for a in chosen) for v in range(Q))
    return {'window':w,'b':b,'group_size':Q,'set_size':len(T),'density_lower_bound_cover':(Q+len(T)-1)//len(T),'greedy_cover_size':len(chosen),'greedy_shifts':chosen,'not_an_optimality_claim':True}

def symbolic_checks():
    count=0
    for n in range(1,10):
        N=1<<n
        for h in range(1,n+1):
            M=N>>h; half=1<<(h-1)
            for q in range(M):
                for f in range(1<<h):
                    sigma=f//half; f0=f%half
                    for s in range(q,N,M):
                        delta=(s//M)%2
                        rhs=s*f0+q*sigma*half+delta*sigma*(N//2)
                        assert (s*f-rhs)%N==0
                        count+=1
    return count

cases=[]
for n,b in [(3,1),(4,1),(5,1),(6,1),(6,2),(7,2),(8,2)]:
    for emb in (1,3): cases.append(field_case(n,b,emb))
cases.append(field_case(8,2,1,True))
comb=[combinatorial_case(n,b) for n,b in [(9,2),(10,3),(11,3),(12,3),(14,3)]]
covers=[cover_case(w,b) for w,b in [(8,1),(10,2),(12,2)]]
result={'status':'PASS','symbolic_complex_recurrence_coefficients':symbolic_checks(),'prime':P,'sqrt_two':TAU,'field_cases':cases,'combinatorial_cases':comb,'finite_cover_examples':covers,'totals':{key:sum(c[key] for c in cases) for key in ['inputs','recurrence_values','regenerated_values','bank_conversion_values','chirp_values','exact_cyclotomic_inner_products']},'scope':'Exact finite controls only. Complex positivity, entropy and all-size bounds are separately proved. No predecessor code is imported, executed or read.'}
Path('INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'totals':result['totals'],'field_cases':len(cases),'combinatorial_cases':len(comb),'cover_examples':len(covers)},sort_keys=True))
