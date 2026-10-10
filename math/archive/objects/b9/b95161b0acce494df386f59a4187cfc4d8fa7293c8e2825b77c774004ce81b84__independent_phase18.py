#!/usr/bin/env python3
"""Independent Phase18/17 audit. Uploaded Python is never imported or executed.
Run: OPENBLAS_NUM_THREADS=1 python independent_phase18.py [--output results.json]
Requires Python 3, NumPy, SymPy. All exact routines below are newly written.
Optional --source-root accepts an extracted Phase18 directory or its outer ZIP,
solely to hash and compare data. Mathematical checks require no source files.
"""
from pathlib import Path
import argparse, collections, hashlib, io, itertools, json, math, random, zipfile
import numpy as np
import sympy as sp

P = 998244353

def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def product(a,b,p):
    bt=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]

def add(a,b,p):
    return [[(x+y)%p for x,y in zip(u,v)] for u,v in zip(a,b)]

def inverse(a,p):
    n=len(a); x=[[(v%p) for v in row]+ident for row,ident in zip(a,eye(n))]
    for c in range(n):
        r=next((r for r in range(c,n) if x[r][c]),None)
        if r is None: raise ValueError('Singular modular matrix')
        x[c],x[r]=x[r],x[c]
        inv=pow(x[c][c],-1,p)
        x[c]=[t*inv%p for t in x[c]]
        for r in range(n):
            if r!=c and x[r][c]:
                f=x[r][c]
                x[r]=[(u-f*v)%p for u,v in zip(x[r],x[c])]
    return [r[n:] for r in x]

def rank(a,p):
    if not a:return 0
    # Sparse online row elimination: useful for the commutant equations too.
    pivots={}
    for row in a:
        row={j:int(x)%p for j,x in enumerate(row) if int(x)%p}
        while row:
            lead=min(row)
            if lead not in pivots:
                scale=pow(row[lead],-1,p)
                pivots[lead]={j:x*scale%p for j,x in row.items()}
                break
            scale=row[lead]
            for j,v in pivots[lead].items():
                t=(row.get(j,0)-scale*v)%p
                if t:row[j]=t
                elif j in row:del row[j]
    return len(pivots)

def field(n):
    if (P-1)%n==0:return P,pow(3,-((P-1)//n),P)
    k=max(1,10000//n)
    while not sp.isprime(k*n+1):k+=1
    p=k*n+1;g=int(sp.primitive_root(p))
    return p,pow(g,-k,p)

def matvec(a,v,p):return [sum(x*y for x,y in zip(row,v))%p for row in a]

def cut(a,r,c):return [[a[i][j] for j in c] for i in r]

def sparse_step(h,v,p):
    return [sum(x*v[j] for j,x in row)%p for row in h]

def parity_audit(n):
    p,w=field(n);half=n//2;W=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
    potentials=[(pow(w,i,p)+pow(w,-i,p))%p for i in range(n)]
    H=[[((int((i-j)%n==1)+int((i-j)%n==n-1))+(potentials[i] if i==j else 0))%p for j in range(n)] for i in range(n)]
    assert product(W,H,p)==product(H,W,p)
    assert rank(H,p)==n-2
    sectors=[]
    for sign in (1,-1):
        positions=list(range(half+1)) if sign==1 else list(range(1,half))
        # Non-orthonormal real parity columns avoid all modular square roots.
        cols=[]
        for j in positions:
            c=[0]*n;c[j]=1
            if j not in (0,half):c[n-j]=sign%p
            cols.append(c)
        B=[list(row) for row in zip(*cols)]
        HB=product(H,B,p);WB=product(W,B,p)
        h=[HB[j] for j in positions];f=[WB[j] for j in positions]
        assert product(B,h,p)==HB and product(B,f,p)==WB
        assert rank(h,p)==len(h)-1
        d=len(h);hs=[[(j,v) for j,v in enumerate(row) if v] for row in h]
        # Fit from a cyclic column, then evaluate independently on every column.
        e=[1]+[0]*(d-1);v=e[:];powers=[]
        for k in range(d):powers.append(v);v=sparse_step(hs,v,p)
        coeff=[0]*d
        for row in range(d-1,-1,-1):
            rhs=(f[row][0]-sum(coeff[k]*powers[k][row] for k in range(row+1,d)))%p
            coeff[row]=rhs*pow(powers[row][row],-1,p)%p
        for j in range(d):
            v=[0]*d
            for c in coeff[::-1]:
                v=sparse_step(hs,v,p);v[j]=(v[j]+c)%p
            assert v==[f[i][j] for i in range(d)]
        target=pow(2,-1,p) if sign==1 else (pow(w,half-1,p)-pow(w,-(half-1),p))%p
        assert coeff[-1]==target!=0
        # Jacobi null vector, then verify Fourier phase on that line.
        z=[1]+[0]*(d-1)
        for i in range(d-1):
            z[i+1]=(-sum(h[i][j]*z[j] for j in range(i+1))*pow(h[i][i+1],-1,p))%p
        assert matvec(h,z,p)==[0]*d
        wz=matvec(f,z,p);lam=wz[0]
        assert wz==[lam*x%p for x in z] and lam*lam%p==sign*n%p
        sectors.append({'parity':sign,'dimension':d,'degree':len(coeff)-1,'top_coefficient_unnormalized':coeff[-1], 'zero_line_fourier_eigenvalue_unnormalized':lam,'all_entries_equal':True})
    assert sectors[0]['zero_line_fourier_eigenvalue_unnormalized']!=sectors[1]['zero_line_fourier_eigenvalue_unnormalized']
    return {'n':n,'prime':p,'root':w,'harper_nullity':2,'sectors':sectors}

def intertwiner_audit(n):
    p,w=field(n);phase=[(pow(w,i,p)+pow(w,-i,p))%p for i in range(n)]
    allowed=[(i,j) for i in range(n) for j in range(n) if phase[i]==phase[j]]
    assert set(allowed)=={(i,j) for i in range(n) for j in (i,(-i)%n)}
    equations=[[0]*len(allowed) for _ in range(n*n)]
    for col,(a,b) in enumerate(allowed):
        for k in ((b+1)%n,(b-1)%n):equations[a*n+k][col]+=1
        for k in ((a+1)%n,(a-1)%n):equations[k*n+b][col]-=1
    dim=len(allowed)-rank(equations,p);assert dim==2
    W=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
    def defects(M):
        return [sum((M[i][(j+1)%n]+M[i][(j-1)%n]-phase[i]*M[i][j])%p!=0 for i in range(n) for j in range(n)),sum((phase[j]*M[i][j]-M[(i+1)%n][j]-M[(i-1)%n][j])%p!=0 for i in range(n) for j in range(n))]
    FJ=[[W[i][(-j)%n] for j in range(n)] for i in range(n)]
    candidate=[[(3*W[i][j]+5*FJ[i][j])%p for j in range(n)] for i in range(n)]
    assert defects(W)==defects(FJ)==defects(candidate)==[0,0]
    assert rank([[W[i][1],FJ[i][1]] for i in range(n)],p)==2
    assert rank([[W[i][0],FJ[i][0]] for i in range(n)],p)==1
    return {'n':n,'prime':p,'commutant_dimension':dim,'e1_calibration_rank':2,'e0_calibration_rank':1}

def invariant(a,p):
    return sorted(a[i][i] for i in range(len(a))),sorted(a[i][j]*a[j][i]%p for i in range(len(a)) for j in range(i))

def diagonal_similarity(u,v,p):
    n=len(u);g=[[] for _ in u]
    for i in range(n):
        for j in range(n):
            a,b=u[i][j]%p,v[i][j]%p
            if (a==0)!=(b==0):return None
            if a:
                r=a*pow(b,-1,p)%p
                g[j].append((i,r));g[i].append((j,pow(r,-1,p)))
    q=[None]*n
    for s in range(n):
        if q[s] is not None:continue
        q[s]=1;queue=collections.deque([s])
        while queue:
            i=queue.popleft()
            for j,r in g[i]:
                x=q[i]*r%p
                if q[j] is None:q[j]=x;queue.append(j)
                elif q[j]!=x:return None
    assert all(u[i][j]*q[j]%p==q[i]*v[i][j]%p for i in range(n) for j in range(n))
    return q

def source_protocol_factor(n,rng,w):
    # Reconstruct only the published coefficient-generation protocol.
    # Solver below is independently written full pivoted elimination.
    total=[[0]*n for _ in range(n)]
    for _ in range(2):
        order=list(range(n));rng.shuffle(order)
        phase=[pow(w,(i*i+3*i+rng.randrange(n))%n,P) for i in range(n)]
        lo=[(1+pow(w,i+rng.randrange(n),P))%P for i in range(n-1)]
        hi=[(2+pow(w,2*i+rng.randrange(n),P))%P for i in range(n-1)]
        b=[[0]*n for _ in range(n)]
        for i in range(n):
            b[i][i]=(7+phase[i])%P
            if i+1<n:b[i+1][i]=lo[i];b[i][i+1]=hi[i]
        inv=inverse(b,P)
        left=[pow(w,rng.randrange(n),P) for _ in range(n)]
        right=[pow(w,rng.randrange(n),P) for _ in range(n)]
        for i in range(n):
            for j in range(n):total[order[i]][order[j]]=(total[order[i]][order[j]]+left[i]*inv[i][j]*right[j])%P
    return total

def veto_audit(n):
    w=pow(3,-((P-1)//n),P);rng=random.Random(1817+n)
    a=source_protocol_factor(n,rng,w);b=source_protocol_factor(n,rng,w)
    ai=inverse(a,P);bi=inverse(b,P)
    assert product(a,ai,P)==eye(n) and product(b,bi,P)==eye(n)
    u=product(ai,[[pow(w,i,P)*x%P for x in row] for i,row in enumerate(a)],P)
    v=product([[row[(j+1)%n] for j in range(n)] for row in b],bi,P)
    iu,iv=invariant(u,P),invariant(v,P)
    matches=[iu[k]==iv[k] for k in (0,1)]
    assert matches==[False,False] and diagonal_similarity(u,v,P) is None
    m=product(a,b,P)
    defects=sum((m[i][(j+1)%n]-pow(w,i,P)*m[i][j])%P!=0 for i in range(n) for j in range(n))
    # Compact symmetric-polynomial witnesses, invariant under all permutations.
    powers=[]
    for k in range(1,5):
        su=sum(pow(x,k,P) for x in iu[0])%P;sv=sum(pow(x,k,P) for x in iv[0])%P
        if su!=sv:powers.append({'power':k,'U_diagonal_moment':su,'V_diagonal_moment':sv})
    assert powers
    return {'n':n,'prime':P,'omega':w,'diagonal_multiset_match':matches[0],'two_cycle_multiset_match':matches[1],'middle_diagonal_exists':False,'weyl_defect_nonzero_entries':defects,'short_diagonal_moment_witnesses':powers,'A_B_inverses_verified':True}

def positive_gauge_controls():
    checks=[]
    p=1009;rng=random.Random(243)
    for n in (4,9,16):
        v=[[rng.randrange(1,p) for j in range(n)] for i in range(n)]
        q=[rng.randrange(1,p) for i in range(n)]
        u=[[q[i]*v[i][j]*pow(q[j],-1,p)%p for j in range(n)] for i in range(n)]
        recovered=diagonal_similarity(u,v,p)
        assert recovered and invariant(u,p)==invariant(v,p)
        assert len({recovered[i]*pow(q[i],-1,p)%p for i in range(n)})==1
        perm=list(range(n));rng.shuffle(perm)
        up=[[u[perm[i]][perm[j]] for j in range(n)] for i in range(n)]
        assert invariant(up,p)==invariant(v,p)
        checks.append({'n':n,'diagonal_recovered_up_to_scalar':True,'arbitrary_permutation_invariants_preserved':True})
    # Passing these short invariants is not sufficient: oriented 3-cycles.
    v=[[0,1,2],[3,0,4],[5,6,0]]
    # For generic dense matrices, transpose preserves diagonals and all 2-cycles.
    u=[list(r) for r in zip(*v)]
    assert invariant(u,p)==invariant(v,p) and diagonal_similarity(u,v,p) is None
    return {'positive':checks,'necessary_only_transpose_counterexample_fixed_permutation':True}

def separator(orders):
    n=len(orders[0]);r=list(orders[0][:n//2]);c=list(orders[0][n-n//2:])
    for order in orders[1:]:
        rr=set(r);cc=set(c);selected=[x for x in order if x in rr or x in cc]
        left=set(selected[:len(r)]);right=set(selected[len(r):])
        options=[([x for x in r if x in left],[x for x in c if x in right]),([x for x in r if x in right],[x for x in c if x in left])]
        r,c=max(options,key=lambda pair:len(pair[0]))
    assert len(r)==len(c)
    for order in orders:
        pos={x:i for i,x in enumerate(order)}
        assert max(pos[x] for x in r)<min(pos[x] for x in c) or max(pos[x] for x in c)<min(pos[x] for x in r)
    return r,c

def sharper_size(n,q):
    divisor=2**(q-1)
    return (n//2+divisor-1)//divisor

def separator_checks():
    rng=random.Random(6003);count=0;prime=[]
    for n in range(2,66):
        for q in range(1,7):
            orders=[]
            for _ in range(q):
                a=list(range(n));rng.shuffle(a);orders.append(a)
            r,c=separator(orders);assert len(r)>=sharper_size(n,q);count+=1
    # Exhaust all second orders at N=7: no prime-full-spark assumption involved.
    minimum=7
    for second in itertools.permutations(range(7)):
        r,c=separator([list(range(7)),second]);minimum=min(minimum,len(r));count+=1
    assert minimum==2
    # The uploaded adversarial construction need not be globally extremal.
    orders=[list(range(8)),[0,4,1,5,2,6,3,7]]
    r,c=separator(orders);assert len(r)==2
    better_r=[0,1,4];better_c=[5,6,7]
    for order in orders:
        pos={x:i for i,x in enumerate(order)}
        assert max(pos[x] for x in better_r)<min(pos[x] for x in better_c)
    # Exact nonzero minors for illustrative prime cases, not a finite-field full-spark theorem.
    for n,q in [(11,2),(13,2),(17,2),(29,3),(67,4)]:
        p,w=field(n);orders=[]
        for k in range(q):
            order=list(range(n));rng.shuffle(order);orders.append(order)
        r,c=separator(orders);r=r[:q+1];c=c[:q+1]
        assert len(r)>q
        minor=[[pow(w,i*j,p) for j in c] for i in r]
        rk=rank(minor,p);assert rk==q+1
        prime.append({'n':n,'q':q,'W':q,'new_necessary_upper_bound':2**q*q+1,'rows':r,'columns':c,'prime_modulus':p,'modular_minor_rank':rk})
    return {'separator_cases':count,'all_second_orders_at_N7':5040,'N7_minimum_greedy_size':minimum,'nonsharpness_counterexample':{'N':8,'orders':[list(range(8)),[0,4,1,5,2,6,3,7]],'greedy_size':2,'better_R':better_r,'better_C':better_c},'prime_characteristic_zero_theorem_controls':prime}

def new_green(order,rng,p):
    n=len(order);b=[[0]*n for _ in range(n)]
    for i in range(n):
        b[i][i]=rng.randrange(7,15)
        if i+1<n:b[i][i+1]=rng.randrange(1,3);b[i+1][i]=rng.randrange(1,3)
    inv=inverse(b,p);out=[[0]*n for _ in range(n)]
    left=[rng.randrange(1,11) for _ in range(n)];right=[rng.randrange(1,11) for _ in range(n)]
    for i in range(n):
        for j in range(n):out[order[i]][order[j]]=left[i]*inv[i][j]*right[j]%p
    return out

def rank_escape(n):
    p,w=field(n);rng=random.Random(8971+n);orders=[]
    for _ in range(4):
        order=list(range(n));rng.shuffle(order);orders.append(order)
    r,c=separator(orders[:2]);terms=[new_green(o,rng,p) for o in orders]
    a=add(terms[0],terms[1],p);b=add(terms[2],terms[3],p);ab=product(a,b,p)
    termranks=[rank(cut(t,r,c),p) for t in terms[:2]]
    ar=rank(cut(a,r,c),p);abr=rank(cut(ab,r,c),p)
    defect=[[(ab[i][(j+1)%n]-pow(w,i,p)*ab[i][j])%p for j in range(n)] for i in range(n)]
    dr=rank(defect,p)
    assert max(termranks)<=1 and ar<=2 and abr>2 and dr>0
    # Nullity identity is valid even if principal blocks are singular.
    swap=[[0,1],[1,0]];assert inverse(swap,p)==swap
    return {'n':n,'prime':p,'selected_size':len(r),'term_cut_ranks':termranks,'sum_cut_rank':ar,'product_cut_rank':abr,'Fourier_covariance_defect_rank':dr,'singular_principal_block_control_passed':True}

def chirp_rank(n):
    p,xi=field(2*n);w=xi*xi%p;m=n//2
    c=[pow(xi,-k*k,p) for k in range(n)]
    assert all(pow(xi,-(k+n)*(k+n),p)==c[k] for k in range(n))
    for i in range(n):
        for j in range(n):assert pow(w,i*j,p)==pow(xi,i*i,p)*c[(i-j)%n]*pow(xi,j*j,p)%p
    hrank=rank([[c[i+j] for j in range(m)] for i in range(m)],p)
    assert hrank==m
    return {'n':n,'prime':p,'chirp_Hankel_rank':hrank,'Bluestein_identity_all_entries':True}

def numerical_checks():
    spectral=[];gaps=[]
    for n in (4,8,12,16,20,28,32,64,128):
        ix=np.arange(n);F=np.exp(-2j*np.pi*((ix[:,None]*ix[None,:])%n)/n)/np.sqrt(n)
        z=np.roll(np.eye(n),1,axis=0);h=z+z.T+np.diag(2*np.cos(2*np.pi*ix/n))
        blocks=[]
        for sign in (1,-1):
            pos=range(n//2+1) if sign==1 else range(1,n//2)
            B=np.zeros((n,len(pos)))
            for k,j in enumerate(pos):
                if j in (0,n//2):B[j,k]=1
                else:B[j,k]=1/np.sqrt(2);B[n-j,k]=sign/np.sqrt(2)
            _,u=np.linalg.eigh(B.T@h@B);blocks.append(B@u)
        O=np.column_stack(blocks);lambdas=np.diag(O.T@F@O)
        allowed=np.array([1,-1,1j,-1j]);phases=allowed[np.argmin(abs(lambdas[:,None]-allowed[None,:]),axis=1)]
        err=float(np.max(abs((O*phases)@O.T-F)));orth=float(np.max(abs(O.T@O-np.eye(n))))
        assert err<1e-10 and orth<1e-10
        spectral.append({'n':n,'max_entry_error':err,'orthogonality_error':orth,'pair_gate_lower_bound':n*math.log2(n)/4})
    rng=random.Random(217)
    for n,q in [(64,2),(128,2),(256,3)]:
        orders=[]
        for k in range(q):
            a=list(range(n));rng.shuffle(a);orders.append(a)
        r,c=separator(orders);m=sharper_size(n,q);r=r[:m];c=c[:m]
        X=np.exp(-2j*np.pi*((np.outer(r,c))%n)/n)/np.sqrt(n)
        s=np.linalg.svd(X,compute_uv=False)
        bound=math.sqrt((m*m/n-q)/(m-q)) if m*m>q*n else 0
        assert abs(float(np.linalg.norm(X,'fro')**2)-m*m/n)<1e-9
        assert s[0]<=1+1e-10 and s[q]>=bound-1e-10
        gaps.append({'n':n,'q':q,'m_star':m,'spectral_gap_lower_bound':bound,'selected_Fourier_block_sigma_W_plus_1':float(s[q])})
    return {'real_orthogonal_four_phase_controls':spectral,'robust_gap_controls':gaps}

def read_source_tree(path):
    out={}
    def walk_zip(raw,prefix):
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for inf in z.infolist():
                if inf.is_dir():continue
                b=z.read(inf);name=prefix+inf.filename;out[name]=b
                if inf.filename.lower().endswith('.zip'):walk_zip(b,name+'!/')
    path=Path(path)
    if path.is_file():walk_zip(path.read_bytes(),'')
    else:
        for p in sorted(path.rglob('*')):
            if not p.is_file():continue
            b=p.read_bytes();name=p.relative_to(path).as_posix();out[name]=b
            if p.suffix.lower()=='.zip':walk_zip(b,name+'!/')
    return out

def source_check(path):
    tree=read_source_tree(path);expected=json.loads(Path(__file__).with_name('source_inventory.json').read_text())
    found={hashlib.sha256(b).hexdigest() for b in tree.values()}
    missing=[r['member'] for r in expected['members'] if r['sha256'] not in found]
    assert not missing,missing
    # Validate embedded checksum files without executing any uploaded module.
    manifests=[]
    for name,raw in tree.items():
        if not name.endswith(('SHA256SUMS.txt','MANIFEST.sha256')):continue
        prefix=name.rsplit('/',1)[0]+'/' if '/' in name else ''
        count=0
        for line in raw.decode().splitlines():
            if not line.strip() or line.startswith('#'):continue
            fields=line.split(maxsplit=1)
            if len(fields)!=2 or len(fields[0])!=64:continue
            rel=fields[1].lstrip('*').removeprefix('./')
            container=name.rsplit('!/',1)[0]+'!/' if '!/' in name else ''
            choices=[prefix+rel,container+rel]
            targets=[t for t in choices if t in tree]
            assert targets,('Missing checksum target',name,rel)
            assert any(hashlib.sha256(tree[t]).hexdigest()==fields[0] for t in targets),(name,rel)
            count+=1
        manifests.append({'member':name,'entries_checked':count})
    return {'expected_content_occurrences':len(expected['members']),'all_expected_contents_found':True,'embedded_manifests':manifests,'phase16_archive_matches_master_1520':expected['phase16_archive_unchanged']}

def independent_separator(row_orders,column_orders):
    n=len(row_orders[0]);I=list(range(n));J=list(range(n))
    for ro,co in zip(row_orders,column_orders):
        rp={label:i for i,label in enumerate(ro)};cp={label:i for i,label in enumerate(co)}
        rr=sorted(I,key=rp.__getitem__);cc=sorted(J,key=cp.__getitem__);k=len(I)//2
        if not k:return [],[]
        if rp[rr[k-1]]<cp[cc[-k]]:I,J=rr[:k],cc[-k:]
        else:
            assert cp[cc[k-1]]<rp[rr[-k]]
            I,J=rr[-k:],cc[:k]
    for ro,co in zip(row_orders,column_orders):
        rp={label:i for i,label in enumerate(ro)};cp={label:i for i,label in enumerate(co)}
        assert max(rp[x] for x in I)<min(cp[x] for x in J) or max(cp[x] for x in J)<min(rp[x] for x in I)
    return I,J

def independent_order_checks():
    # Exhaustive local split lemma, allowing arbitrary overlap of row/column positions.
    local=0
    for m in range(2,7):
        k=m//2
        for r in itertools.combinations(range(6),m):
            for c in itertools.combinations(range(6),m):
                assert r[k-1]<c[m-k] or c[k-1]<r[m-k]
                local+=1
    rng=random.Random(41319);cases=0;overlaps=0
    for n in range(2,66):
        for q in range(1,7):
            rows=[];cols=[]
            for _ in range(q):
                a=list(range(n));b=list(range(n));rng.shuffle(a);rng.shuffle(b);rows.append(a);cols.append(b)
            I,J=independent_separator(rows,cols)
            assert len(I)==len(J)==n//2**q
            overlaps+=bool(set(I)&set(J));cases+=1
    exact=[]
    for n,q in ((13,2),(37,3),(83,4),(64,2)):
        p,w=field(n);rows=[];cols=[];terms=[]
        for _ in range(q):
            ro=list(range(n));co=list(range(n));rng.shuffle(ro);rng.shuffle(co);rows.append(ro);cols.append(co)
            # Generate a conjugately ordered term, then independently relabel columns.
            G=new_green(ro,rng,p);term=[[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):term[i][co[j]]=G[i][ro[j]]
            terms.append(term)
        I,J=independent_separator(rows,cols)
        ranks=[rank(cut(t,I,J),p) for t in terms]
        total=[[sum(t[i][j] for t in terms)%p for j in range(n)] for i in range(n)]
        sr=rank(cut(total,I,J),p)
        fr=rank([[pow(w,i*j,p) for j in J] for i in I],p)
        assert max(ranks)<=1 and sr<=q
        if sp.isprime(n):assert fr==len(I)>q
        exact.append({'n':n,'q':q,'prime_modulus':p,'rectangle_size':len(I),'term_ranks':ranks,'sum_rank':sr,'Fourier_minor_rank':fr,'original_label_overlap':len(set(I)&set(J)),'prime_N_necessary_upper_bound':2**q*(q+1)-1 if sp.isprime(n) else None})
    return {'local_split_exhaustive_cases':local,'random_full_separator_cases':cases,'cases_with_overlapping_original_labels':overlaps,'exact_Green_controls':exact,'scope':'Independent row and column permutations per term. Guaranteed rectangle floor(N/2^q), not the conjugate-order ceiling bound.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-root');ap.add_argument('--output',default=str(Path(__file__).with_name('independent_phase18_results.json')));args=ap.parse_args()
    result={'audit_kind':'Independent exact mathematical controls and separately labelled numerical controls; no uploaded code run or imported','normalization':'Exact Harper checks use W=sqrt(N)F to avoid modular square roots. Divide coefficients/eigenvalues by sqrt(N) in characteristic zero.','harper':[parity_audit(n) for n in (4,8,12,16,20,28,32,36,60,64,128)],'joint_commutant':[intertwiner_audit(n) for n in (4,6,8,10,12,16,20,32,64)],'source_fixed_factors':[veto_audit(n) for n in (8,16,32,64)],'monomial_controls':positive_gauge_controls(),'phase17_separator':separator_checks(),'independent_row_column_permutations':independent_order_checks(),'new_product_escape_controls':[rank_escape(n) for n in (16,32,64)],'chirp_Hankel':[chirp_rank(n) for n in (8,16,32,64,128)],'numerical':numerical_checks()}
    if args.source_root:result['source_verification']=source_check(args.source_root)
    result['all_checks_passed']=True
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_passed':True,'output':str(Path(args.output).resolve()),'harper_sizes':[r['n'] for r in result['harper']],'new_prime_necessary_bound':'N <= 2^q W + 1, for prime N over C','fixed_factor_veto_sizes':[r['n'] for r in result['source_fixed_factors']]},indent=2))

if __name__=='__main__':main()
