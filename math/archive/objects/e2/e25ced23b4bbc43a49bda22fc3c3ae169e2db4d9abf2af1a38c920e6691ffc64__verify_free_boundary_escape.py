#!/usr/bin/env python3
"""Independent exact checks. Imports no predecessor or uploaded executable."""
import hashlib, json, math
from pathlib import Path
P=65537

def gamma(w):
    z=0
    while w:
        if w&1:z+=w//2
        w//=2
    return z

def rev(w,n):
    y=0
    for _ in range(n):y=2*y+(w&1);w//=2
    return y

def allowed(w,n,b):return '0'*b not in format(w,f'0{n}b')
def q(x,root):
    N=len(x); y=[0]*N
    for s,v in enumerate(x):
        y[(2*s)%N]=(y[(2*s)%N]+v)%P
        y[(2*s+1)%N]=(y[(2*s+1)%N]+pow(root,s,P)*v)%P
    return y

def killed(x,root,R):
    y=q(x,root)
    for s in R:y[s]=0
    return y

def free(x,root,R,n):
    z=x[:]
    for s in R:z[s]=0
    for _ in range(n):z=killed(z,root,R)
    return z

def folds(x,n,b):
    r=1<<(n-b)
    return [[sum(x[(1<<(b-c))*(j+h*r)] for h in range(1<<c))%P for j in range(r)] for c in range(b)]

def correction(x,root,n,b):
    N=1<<n;r=1<<(n-b);d=n-b;eta=pow(root,1<<b,P)
    us=folds(x,n,b); qs=[]
    for u in us:
        for _ in range(d):u=q(u,eta)
        qs.append(u)
    z=[0]*N
    for w in range(N):
        if allowed(w,n,b):
            c=n-w.bit_length();a=w>>(b-c)
            z[w]=pow(root,gamma(w),P)*pow(eta,-gamma(a),P)*qs[c][a]%P
    return z

def forced_basis(root,n,b,k):
    N=1<<n;R=list(range(0,N,1<<b));v=[0]*N;v[R[k]]=1
    out=[]
    for L in range(1,n+1):v=killed(v,root,R);out.append(v)
    return out

def necklaces(b):
    classes={}
    for p in range(1<<b):
        bits=format(p,f'0{b}b');orbit={int(bits[i:]+bits[:i],2) for i in range(b)}
        classes.setdefault(min(orbit),sorted(orbit))
    return list(classes.values())

def cover_controls(b,n):
    size=1<<b;N=1<<n;allrows=(1<<N)-1;coverage=[]
    for p in range(size):
        word=format(p,f'0{b}b');coverage.append(sum(1<<w for w in range(N) if word in format(w,f'0{n}b')))
    cov=[0]*(1<<size);minimum=size+1;witness=None;valid=0;neck=necklaces(b)
    for S in range(1<<size):
        if S:
            bit=S&-S;cov[S]=cov[S^bit]|coverage[bit.bit_length()-1]
        assert cov[S].bit_count()<=min(N,S.bit_count()*(n-b+1)*(1<<(n-b)))
        if cov[S]==allrows:
            valid+=1;assert S.bit_count()>=len(neck)
            if S.bit_count()<minimum:minimum=S.bit_count();witness=S
        else:
            for orbit in neck:
                if all(not(S>>p&1) for p in orbit):
                    word=format(orbit[0],f'0{b}b');ww=(word*((n+b-1)//b))[:n]
                    assert all(not(S>>int(ww[i:i+b],2)&1) for i in range(n-b+1))
                    break
    return dict(b=b,n=n,necklaces=len(neck),minimum_patterns=minimum,minimum_witness=[p for p in range(size) if witness is not None and witness>>p&1],universal_sets=valid,sets_checked=1<<size)

def matrix_rank(rows):
    a=[row[:] for row in rows];i=0
    for j in range(len(a[0]) if a else 0):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];z=pow(a[i][j],-1,P)
        a[i]=[z*v%P for v in a[i]]
        for k in range(i+1,len(a)):
            if a[k][j]:
                z=a[k][j];a[k]=[(v-z*u)%P for v,u in zip(a[k],a[i])]
        i+=1
    return i

def arbitrary_cut_controls(n):
    N=1<<n;root=pow(3,65536//N,P);full=(1<<N)-1;z=len(necklaces(n));minimum=N+1;nilpotent=0;ranks=0
    for E in range(1<<N):
        active=E
        for _ in range(n):
            nxt=0
            for s in range(N):
                if active>>s&1:nxt|=(1<<((2*s)%N))|(1<<((2*s+1)%N))
            active=nxt&E
        R=[s for s in range(N) if not(E>>s&1)]
        if not active:
            nilpotent+=1;minimum=min(minimum,len(R));assert len(R)>=z
        if n<=3:
            cols=[]
            for s in range(N):
                x=[0]*N;x[s]=1;cols.append(free(x,root,R,n))
            rank=matrix_rank(list(map(list,zip(*cols))))
            assert rank>=N-(n+1)*len(R)
            assert (rank==0)==(active==0)
            ranks+=1
    return dict(n=n,N=N,cuts_checked=1<<N,nilpotent_cuts=nilpotent,minimum_nilpotent_retained=minimum,necklace_lower_bound=z,rank_checks=ranks)

def run():
    params=[];counts=dict(free_basis=0,early_fold_basis=0,forced_basis_coefficients=0,forced_cancellation_basis=0,marker_nilpotence_basis=0,general_pattern_late_zero=0)
    for n in range(1,8):
        N=1<<n;root=pow(3,65536//N,P)
        assert pow(root,N,P)==1 and pow(root,N//2,P)!=1
        for b in range(1,n+1):
            r=1<<(n-b);R=list(range(0,N,1<<b));A=[w for w in range(N) if allowed(w,n,b)]
            Rstar=set(R)|set(A)
            for s in range(N):
                x=[0]*N;x[s]=1;traj=[x]
                for j in range(n):traj.append(q(traj[-1],root))
                B=free(x,root,R,n);C=correction(x,root,n,b)
                expected=[(traj[n][w] if w in A else 0)-C[w] for w in range(N)]
                assert B==[v%P for v in expected]
                # Independent explicit path-weight check of Fourier convention.
                assert traj[n]==[pow(root,(s*rev(w,n)+gamma(w))%N,P) for w in range(N)]
                counts['free_basis']+=1
                us=folds(x,n,b)
                for c in range(b):assert [traj[c][k] for k in R]==us[c]
                counts['early_fold_basis']+=1
                actual_force=[0]*N
                # Independent recurrence driven by the true retained coefficients.
                for j in range(n):
                    state=[0]*N
                    for k in R:state[k]=traj[j][k]
                    for L in range(1,n-j+1):state=killed(state,root,R)
                    actual_force=[(a+v)%P for a,v in zip(actual_force,state)]
                assert [actual_force[w] if w in A else 0 for w in range(N)]==C
                counts['forced_cancellation_basis']+=1
                assert free(x,root,Rstar,n)==[0]*N
                counts['marker_nilpotence_basis']+=1
            for k in range(r):
                gs=forced_basis(root,n,b,k)
                for j in range(n):
                    for w in A:
                        if j!=n-w.bit_length():assert gs[n-j-1][w]==0
                    counts['forced_basis_coefficients']+=1
            params.append(dict(n=n,b=b,N=N,r=r,allowed_rows=len(A),marker_retained=len(Rstar)))
    # Arbitrary cylinder pattern: later retained coefficients cannot affect avoiding rows.
    for n in range(1,6):
        N=1<<n;root=pow(3,65536//N,P)
        for b in range(1,n+1):
            for pat in range(1<<b):
                R=[s for s in range(N) if s% (1<<b)==pat]
                word=format(pat,f'0{b}b');A=[w for w in range(N) if word not in format(w,f'0{n}b')]
                for k in R:
                    state=[0]*N;state[k]=1
                    for L in range(1,n+1):
                        state=killed(state,root,R)
                        if n-L>=b:
                            assert all(state[w]==0 for w in A)
                            counts['general_pattern_late_zero']+=1
    covers=[cover_controls(b,n) for b in range(1,5) for n in range(b,min(8,b+4)+1)]
    naive=[min(orbit) for orbit in necklaces(3)]
    assert naive==[0,1,3,7]
    cycle=[2,5]
    assert all(s not in naive for s in cycle)
    assert ((cycle[0]<<1)|1)%8==cycle[1] and (cycle[1]<<1)%8==cycle[0]
    word_counts=[]
    for b in range(1,33):
        a=[]
        for n in range(0,257):
            a.append((1<<n) if n<b else sum(a[n-j] for j in range(1,b+1)))
            assert a[n]*(1<<(b*n)) <= 2*pow((1<<(b+1))-1,n) # Exact rational version of the exponential majorant.
        word_counts.append(dict(b=b,counts=a))
    arbitrary=[arbitrary_cut_controls(n) for n in range(1,5)]
    ans=dict(field=P,parameters=params,checks=counts,arbitrary_cut_controls=arbitrary,cover_controls=covers,naive_necklace_counterexample=dict(b=3,retained=naive,avoiding_cycle=cycle),word_counts=word_counts)
    out=Path(__file__).resolve().parent
    data=json.dumps(ans,sort_keys=True,indent=2)+'\n'
    (out/'FREE_BOUNDARY_CONTROLS.json').write_text(data)
    summary=dict(parameters=len(params),checks=counts,cover_parameter_cases=len(covers),cover_sets_checked=sum(z['sets_checked'] for z in covers),arbitrary_cuts_checked=sum(z['cuts_checked'] for z in arbitrary),arbitrary_rank_checks=sum(z['rank_checks'] for z in arbitrary),status='PASS')
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':run()
