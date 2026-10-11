"""Fresh reviewer-authored controls; no imports or execution of packet programs.
Exact modular Green entries are computed by walking paths, not prefix formulas.
"""
import bisect, hashlib, itertools, json, math, pathlib, random
from collections import defaultdict
import numpy as np
BASE=pathlib.Path(__file__).resolve().parent

def classes(cycles, rp, cp, rows, N):
    # Arc ID = next marked cycle position at/after source, cyclically.
    pos=[{v:i for i,v in enumerate(c)} for c in cycles]
    marks=[sorted(p[r[i]] for i in rows) for p,r in zip(pos,rp)]
    out=defaultdict(list)
    for j in range(N):
        key=tuple(bisect.bisect_left(m,p[c[j]])%len(m) for m,p,c in zip(marks,pos,cp))
        out[key].append(j)
    return out

def rank_mod(a,p):
    a=[[x%p for x in r] for r in a]; r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]; s=pow(a[r][j],-1,p)
        a[r]=[(x*s)%p for x in a[r]]
        for k in range(r+1,len(a)):
            s=a[k][j]; a[k]=[(x-s*y)%p for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a): break
    return r

def exact_control(N,q,p,seed):
    rng=random.Random(seed); perm=lambda:rng.sample(range(N),N)
    cyc=[perm() for _ in range(q)]; rp=[perm() for _ in range(q)]; cp=[perm() for _ in range(q)]
    left=[[rng.randrange(1,p) for _ in range(N)] for _ in range(q)]
    right=[[rng.randrange(1,p) for _ in range(N)] for _ in range(q)]
    branch=[]
    for c in cyc:
        while True:
            w=[rng.randrange(1,p) for _ in range(N)]; h=math.prod(w)%p
            if h!=1:break
        succ={c[k]:(c[(k+1)%N],w[k]) for k in range(N)}
        branch.append((succ,pow((1-h)%p,-1,p)))
    R=list(range(q+1)); groups=classes(cyc,rp,cp,R,N)
    assert len(groups)<=(q+1)**q
    omega=next(x for x in range(2,p) if pow(x,N,p)==1 and all(pow(x,d,p)!=1 for d in range(1,N) if N%d==0))
    max_rank=0; witness=None; checked=0
    for C in groups.values():
        blocks=[]
        for ell,(succ,den) in enumerate(branch):
            block=[]
            for i in R:
                row=[]
                for j in C:
                    cur=cp[ell][j]; product=1
                    for step in range(N):
                        if cur==rp[ell][i]:break
                        cur,w=succ[cur]; product=product*w%p
                    else:raise AssertionError('cycle walk failed')
                    row.append(left[ell][i]*product*den*right[ell][j]%p)
                block.append(row)
            assert rank_mod(block,p)==1
            blocks.append(block)
        M=[[sum(block[i][j] for block in blocks)%p for j in range(len(C))] for i in R]
        r=rank_mod(M,p);assert r<=q;max_rank=max(max_rank,r);checked+=1
        if len(C)>=q+1:
            F=[[pow(omega,i*j,p) for j in C[:q+1]] for i in R]
            assert rank_mod(F,p)==q+1
            if witness is None:witness={'columns':C[:q+1],'green_rank':rank_mod([row[:q+1] for row in M],p),'fourier_rank':q+1}
    return {'N':N,'q':q,'p':p,'seed':seed,'primitive_root':omega,'classes':checked,'largest_class':max(map(len,groups.values())),'max_class_rank':max_rank,'witness':witness}

def numeric_control(N,q,seed):
    rng=np.random.default_rng(seed); n=q+1
    cyc=[rng.permutation(N).tolist() for _ in range(q)]
    rp=[rng.permutation(N) for _ in range(q)];cp=[rng.permutation(N) for _ in range(q)]
    rows=[(N-2+i)%N for i in range(n)] # Consecutive rows including wraparound.
    M=np.zeros((N,N),complex); branches=[]
    for ell,c in enumerate(cyc):
        angles=rng.uniform(-math.pi,math.pi,N);w=np.exp(1j*angles)
        if abs(1-np.prod(w))<.2:w[0]*=-1
        W=np.zeros((N,N),complex)
        for k in range(N):W[c[(k+1)%N],c[k]]=w[k]
        G=np.linalg.solve(np.eye(N)-W,np.eye(N))
        left=np.exp(rng.uniform(-2,2,N)+1j*rng.uniform(-math.pi,math.pi,N))
        right=np.exp(rng.uniform(-2,2,N)+1j*rng.uniform(-math.pi,math.pi,N))
        B=left[:,None]*G[np.ix_(rp[ell],cp[ell])]*right[None,:]
        branches.append(B);M+=B
    U=np.exp(-2j*math.pi*np.outer(np.arange(N),np.arange(N))/N)/math.sqrt(N)
    groups=classes(cyc,rp,cp,rows,N);a1=0;residual2=0;max_relative_tail=0
    relaxed=np.zeros((n,N),complex)
    for C in groups.values():
        for B in branches:
            s=np.linalg.svd(B[np.ix_(rows,C)],compute_uv=False)
            tail=s[1] if len(s)>1 else 0
            assert tail<=1e-10*max(1,s[0])
        s=np.linalg.svd(M[np.ix_(rows,C)],compute_uv=False)
        tail=s[q] if len(s)>q else 0
        max_relative_tail=max(max_relative_tail,tail/max(1,s[0]))
        assert tail<=1e-10*max(1,s[0])
        Z=U[np.ix_(rows,C)];u,s,v=np.linalg.svd(Z,full_matrices=False)
        sv=s[n-1] if len(s)>=n else 0
        a1=max(a1,sv);residual2+=sv*sv
        ss=s.copy()
        if len(ss)>=n:ss[-1]=0
        relaxed[:,C]=(u*ss)@v
    a2=math.sqrt(residual2/n);actual=np.linalg.norm(M-U,2)
    relaxed_error=np.linalg.norm(relaxed-U[rows,:],2)
    assert actual+1e-11>=max(a1,a2)
    assert relaxed_error+1e-11>=max(a1,a2)
    return {'N':N,'q':q,'seed':seed,'classes':len(groups),'largest_class':max(map(len,groups.values())),'A1':float(a1),'A2':a2,'actual_error':float(actual),'relaxed_rank_q_error':float(relaxed_error),'max_relative_forbidden_singular_value':float(max_relative_tail)}

def spacing_control():
    count=0; min_slack=None
    for N in range(4,15):
        for n in range(2,min(4,N//2)+1):
            for L in range(2*n,N+1):
                for C in itertools.combinations(range(N),L):
                    s=L//(2*n);groups=[C[2*k*s:(2*k+1)*s] for k in range(n)]
                    for a,b in itertools.combinations(groups,2):
                        for x in a:
                            for y in b:
                                gap=min((y-x)%N,(x-y)%N)
                                assert gap>=s
                                slack=gap-s;min_slack=slack if min_slack is None else min(slack,min_slack)
                    count+=1
    return {'checked_subsets_and_group_counts':count,'N_range':[4,14],'n_range':[2,4],'minimum_grid_gap_slack':min_slack}

def density_control():
    rng=random.Random(882341); records=[]
    for N,n,L in [(8,2,8),(16,2,8),(32,3,12),(32,4,16),(108,3,12),(128,4,32),(1024,4,16)]:
        candidates=[list(range(L)),[(N-L//2+j)%N for j in range(L)],list(range(0,N,max(1,N//L)))[:L]]
        candidates += [sorted(rng.sample(range(N),L)) for _ in range(12)]
        lower=(L/N)**(n-.5)/(2*n)**n; worst=math.inf
        for C in candidates:
            Z=np.exp(-2j*math.pi*np.outer(np.arange(n),C)/N)/math.sqrt(N)
            sv=float(np.linalg.svd(Z,compute_uv=False)[-1]);assert sv>=lower*(1-1e-7)
            worst=min(worst,sv)
        records.append({'N':N,'n':n,'L':L,'subsets':len(candidates),'minimum_observed_sigma':worst,'proved_bound':lower,'minimum_ratio':worst/lower})
    return records

def normalization_counterexamples():
    N=16;P=np.roll(np.eye(N),1,axis=0);G=np.linalg.solve(np.eye(N)-.5*P,np.eye(N))
    U=np.exp(-2j*math.pi*np.outer(np.arange(N),np.arange(N))/N)/math.sqrt(N)
    c=1/(4**2*2**1.5);eps=1e-6
    scaled_error=float(np.linalg.norm(eps*eps*G-eps*U,2))
    H=G*(U[0,:]/G[0,:])[None,:];h=float(np.linalg.norm(H[1:,:],2));delta=eps/(1+h)
    D=np.diag([1]+[eps]*(N-1));A=np.diag([1]+[delta]*(N-1))
    error=float(np.linalg.norm(A@H-D@U,2))
    assert scaled_error<c and error<c and error<=2*eps*(1+1e-10)
    return {'N':N,'q':1,'unitary_DFT_bound':c,'epsilon':eps,'shrinking_target_error':scaled_error,'unit_norm_nonunitary_target_error':error,'target_norm':float(np.linalg.norm(D@U,2)),'nonunitary_approximant_other_row_scale':delta}

if __name__=='__main__':
    result={'method':'Fresh reviewer code only; uploaded code never imported or executed.',
        'exact_modular':[exact_control(32,2,97,92341),exact_control(64,3,257,92342),exact_control(256,3,257,92343)],
        'complex_numeric':[numeric_control(N,q,92000+100*q+N+trial) for q,N in [(1,16),(2,36),(2,108),(3,96),(4,125)] for trial in range(2)],
        'spacing':spacing_control(),'density':density_control(),'normalization':normalization_counterexamples()}
    (BASE/'fresh_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
