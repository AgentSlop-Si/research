#!/usr/bin/env python3
"""Independent Phase20 audit. No uploaded Python module is imported or executed.
Python 3.10+; NumPy is used only for separately labelled numerical controls.
The optional --source path is read solely as JSON/text data.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, pathlib, random
import numpy as np


def rank(A,p):
    a=[[int(x)%p for x in row] for row in A]
    if not a:return 0
    r=0
    for j in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        v=pow(a[r][j],-1,p);a[r]=[x*v%p for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][j]
            if v:a[i]=[(x-v*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(A,B,p):return [[(x+y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def sub(A,B,p):return [[(x-y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def mul(A,B,p):return [[sum(x*y for x,y in zip(a,b))%p for b in zip(*B)] for a in A]
def vec(A,v,p):return [sum(x*y for x,y in zip(a,v))%p for a in A]
def inv(A,p):
    n=len(A);a=[list(row)+e for row,e in zip(A,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n) if a[i][j]%p)
        a[j],a[k]=a[k],a[j]
        u=pow(a[j][j],-1,p);a[j]=[x*u%p for x in a[j]]
        for i in range(n):
            if i!=j:
                u=a[i][j];a[i]=[(x-u*y)%p for x,y in zip(a[i],a[j])]
    return [a[n:] for a in a]


def prime_factors(n):
    a=[];q=2
    while q*q<=n:
        if n%q==0:
            a.append(q)
            while n%q==0:n//=q
        q+=1
    if n>1:a.append(n)
    return a


def primitive_root(p):
    assert p>2 and all(p%d for d in range(2,math.isqrt(p)+1))
    fs=prime_factors(p-1)
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in fs))


def roots(n,p,g):
    assert (p-1)%n==0
    w=pow(g,-((p-1)//n),p);a=[1]
    for _ in range(n-1):a.append(a[-1]*w%p)
    assert len(set(a))==n and a[-1]*w%p==1
    return a


def matrices(n,p,g,scale=1):
    a=roots(n,p,g)
    H=[[scale*a[i*j%n]%p for j in range(n)] for i in range(n)]
    Z=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
    D=[[a[i] if i==j else 0 for j in range(n)] for i in range(n)]
    Zi=[[int(i==(j-1)%n) for j in range(n)] for i in range(n)]
    return H,Z,D,Zi


def residuals(A,p,g):
    _,Z,D,Zi=matrices(len(A),p,g)
    return sub(mul(A,Z,p),mul(D,A,p),p),sub(mul(A,D,p),mul(Zi,A,p),p)


def recognize(A,p,g):
    """Complete general-N monomial Fourier recognizer; returns a certificate.
    Primitive exponent means gcd(e,N)=1, also for non-prime-power lengths.
    Root table is prepared by successive multiplication, not repeated powers.
    """
    n=len(A)
    assert all(len(a)==n for a in A)
    if any(x%p==0 for a in A for x in a):return {'equivalent':False,'reason':'zero'}
    a=roots(n,p,g);lookup={x:i for i,x in enumerate(a)}
    ri=[A[0][0]*pow(A[i][0],-1,p)%p for i in range(n)]
    ci=[pow(A[0][j],-1,p) for j in range(n)]
    E=[];pivot=None
    for i in range(n):
        E.append([])
        for j in range(n):
            x=lookup.get(A[i][j]*ri[i]*ci[j]%p)
            if x is None:return {'equivalent':False,'reason':'non-root'}
            E[i].append(x)
            if pivot is None and math.gcd(x,n)==1:pivot=(i,j)
    if pivot is None:return {'equivalent':False,'reason':'no-unit-pivot'}
    i,j=pivot;v=pow(E[i][j],-1,n)
    alpha=[E[k][j]*v%n for k in range(n)];beta=E[i]
    if sorted(alpha)!=list(range(n)) or sorted(beta)!=list(range(n)):
        return {'equivalent':False,'reason':'not-permutations'}
    if any(E[i][j]!=alpha[i]*beta[j]%n for i in range(n) for j in range(n)):
        return {'equivalent':False,'reason':'nonseparable'}
    left=[A[i][0]%p for i in range(n)]
    right=[A[0][j]*pow(A[0][0],-1,p)%p for j in range(n)]
    assert alpha[0]==beta[0]==0
    assert all(A[i][j]%p==left[i]*a[alpha[i]*beta[j]%n]*right[j]%p
               for i in range(n) for j in range(n))
    return {'equivalent':True,'alpha':alpha,'beta':beta,'left':left,'right':right}


def fingerprint(A,p,g,k=0,l=1):
    n=len(A);a=roots(n,p,g);logs={x:i for i,x in enumerate(a)}
    if any(A[j][k]%p==0 or A[j][l]%p==0 for j in range(n)):return None
    base=A[0][k]*pow(A[0][l],-1,p)%p;hist=[0]*n
    for j in range(n):
        e=logs.get(A[j][l]*pow(A[j][k],-1,p)*base%p)
        if e is None:return None
        hist[e]+=1
    d=hist[0]
    if not 1<=d<n or n%d:return None
    return d if all(hist[e]==(d if e%d==0 else 0) for e in range(n)) else None


def weyl_trial(A,p,g,seed,h=1,calibration=1):
    n=len(A);a=roots(n,p,g);rng=random.Random(seed);calls=0
    def apply(v):
        nonlocal calls
        calls+=1
        return vec(A,v,p)
    calibrated=apply([1]+[0]*(n-1))[0]==calibration
    count=[0,0]
    for _ in range(h):
        v=[rng.randrange(p) for _ in range(n)];y=apply(v)
        az=apply(v[-1:]+v[:-1]);ad=apply([x*z%p for x,z in zip(v,a)])
        count[0]+=sum(x!=y*z%p for x,y,z in zip(az,y,a))
        count[1]+=sum(x!=z for x,z in zip(ad,y[1:]+y[:1]))
    assert calls==1+3*h
    return {'calibrated':calibrated,'first_equation':count[0]==0,
            'second_equation':count[1]==0,'nonzero_first':count[0],
            'nonzero_second':count[1],'circuit_calls':calls,
            'passed':calibrated and not any(count)}


def exact_checks():
    out={};p=20161;g=primitive_root(p)
    lengths=[2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,28,32]
    cases=[]
    for n in lengths:
        H,Z,D,Zi=matrices(n,p,g)
        assert mul(H,Z,p)==mul(D,H,p) and mul(H,D,p)==mul(Zi,H,p)
        assert weyl_trial(H,p,g,n,h=2)['passed']
        rng=random.Random(4200+n);rho=list(range(n));sigma=list(range(n));rng.shuffle(rho);rng.shuffle(sigma)
        left=[rng.randrange(1,p) for _ in range(n)];right=[rng.randrange(1,p) for _ in range(n)]
        A=[[left[i]*H[rho[i]][sigma[j]]*right[j]%p for j in range(n)] for i in range(n)]
        cert=recognize(A,p,g);assert cert['equivalent']
        for k in range(n):
            for l in range(k+1,n):assert fingerprint(A,p,g,k,l)==math.gcd(sigma[l]-sigma[k],n)
        bad=[[roots(n,p,g)[(i*j+i*i*j*j)%n] for j in range(n)] for i in range(n)]
        bad_report=recognize(bad,p,g)
        cases.append({'n':n,'weyl_exact':True,'masked_reconstructed':True,
                      'all_column_pairs':n*(n-1)//2,'nonlinear_exponent_counterfeit_rejected':not bad_report['equivalent'],
                      'certificate':cert})
    out['field']={'p':p,'primitive_generator':g,'lengths':cases}
    # Nullity of both identities, over fields with primitive roots; no normalization needed.
    nullities=[]
    for n in (2,3,4,6,8):
        columns=[]
        for t in range(n*n):
            E=[[0]*n for _ in range(n)];E[t//n][t%n]=1
            a,b=residuals(E,p,g);columns.append([x for row in a+b for x in row])
        rk=rank(list(zip(*columns)),p);assert rk==n*n-1
        nullities.append({'n':n,'equation_rank':rk,'solution_dimension':n*n-rk})
    out['weyl_nullities']=nullities
    # Exhaustively count the same-random-vector common kernel.
    exhaustive=[]
    for p0,n,g0 in ((5,2,2),(7,3,3)):
        H,*_=matrices(n,p0,g0)
        for kind in ('single_entry','row_scaled','wrong_scalar'):
            M=[a[:] for a in H]
            if kind=='single_entry':M[-1][-1]=(M[-1][-1]+1)%p0
            if kind=='row_scaled':M[-1]=[2*x%p0 for x in M[-1]]
            if kind=='wrong_scalar':M=[[2*x%p0 for x in row] for row in M]
            a,b=residuals(M,p0,g0);rho=rank(a+b,p0)
            accepted=sum(not any(vec(a,v,p0)+vec(b,v,p0)) for v in itertools.product(range(p0),repeat=n))
            assert accepted==p0**(n-rho)
            exhaustive.append({'p':p0,'n':n,'candidate':kind,'stacked_rank':rho,
                               'common_kernel_size':accepted,'total_vectors':p0**n,
                               'calibration_passes':M[0][0]==1})
    out['exhaustive_kernel_probabilities']=exhaustive
    # Sylvester real Hadamards fool every individual column-pair histogram.
    counterfeit=[]
    for n in (4,8,16):
        H=[[(-1 if (i&j).bit_count()%2 else 1)%p for j in range(n)] for i in range(n)]
        passed=sum(fingerprint(H,p,g,k,l)==n//2 for k in range(n) for l in range(k+1,n))
        assert passed==n*(n-1)//2 and not recognize(H,p,g)['equivalent']
        counterfeit.append({'n':n,'all_histograms_pass':passed,'full_test_rejects':True,'reason':'no-unit-pivot'})
    out['all_pair_histogram_counterfeit']=counterfeit
    # Exact path commutator decomposition and Green rank budget, odd and even lengths.
    stationary=[]
    for n in (3,4,5,6,7,8,9,12,16,24,32):
        H,Z,_,_=matrices(n,p,g);stages=[];decomp_ok=True
        for t in range(2):
            S=[[0]*n for _ in range(n)]
            for q in range(2):
                aa,bb,cc=2*n+23*q+11*t,-(n-1)+3*q,-(n-1)+5*t
                B=[[aa if i==j else bb if i==j+1 else cc if j==i+1 else 0 for j in range(n)] for i in range(n)]
                C=sub(mul(B,Z,p),mul(Z,B,p),p);E=[[0]*n for _ in range(n)]
                E[0][0]+=cc;E[0][n-2]-=bb;E[1][n-1]+=bb;E[n-1][n-1]-=cc
                E=[[x%p for x in a] for a in E];assert C==E and rank(C,p)<=2
                S=add(S,inv(B,p),p)
            assert rank(sub(mul(S,Z,p),mul(Z,S,p),p),p)<=4
            stages.append(S)
        M=mul(stages[1],stages[0],p)
        r=rank(sub(mul(M,Z,p),mul(Z,M,p),p),p)
        fr=rank(sub(mul(H,Z,p),mul(Z,H,p),p),p)
        assert r<=8 and fr==n-(n%2)
        stationary.append({'n':n,'green_product_commutator_rank':r,'rank_budget':8,'Fourier_rank':fr})
    out['stationary_exact_ranks']=stationary
    return out


def numerical_checks():
    out={'dtype':'complex128; numerical checks support but do not prove identities'}
    rng=np.random.default_rng(91837);records=[];sparse=[];row_sharp=[]
    for n in (3,4,5,6,8,9,12,16,24,32,64,128):
        x=np.arange(n);F=np.exp(-2j*np.pi*np.outer(x,x)/n)/np.sqrt(n)
        Z=np.roll(np.eye(n),1,axis=0);D=np.diag(np.exp(-2j*np.pi*x/n))
        K=rng.standard_normal((n,n))+1j*rng.standard_normal((n,n));M=F@K
        residual=np.linalg.norm(M@Z-D@M,'fro')**2+np.linalg.norm(M@D-Z.T@M,'fro')**2
        # Parseval identity in a freshly generated Weyl basis.
        weighted=0.
        for a in range(n):
            for b in range(n):
                W=(np.exp(-2j*np.pi*a*x/n)[:,None]*np.roll(np.eye(n),b,axis=0))/np.sqrt(n)
                coefficient=np.vdot(W,K)
                weighted+=(abs(1-np.exp(-2j*np.pi*a/n))**2+abs(1-np.exp(-2j*np.pi*b/n))**2)*abs(coefficient)**2
        rel=abs(residual-weighted)/max(1,residual)
        fd=F@D;dist=np.linalg.norm(fd-F*np.vdot(F,fd)/n,'fro')
        rr=np.hypot(np.linalg.norm(fd@Z-D@fd,'fro'),np.linalg.norm(fd@D-Z.T@fd,'fro'))
        sharp=abs(rr/dist-2*np.sin(np.pi/n))
        comm=F@Z-Z@F;sv=np.linalg.svd(comm,compute_uv=False)
        formula=np.array([2*np.cos((2*(r//2)+1)*np.pi/(2*n)) for r in range(n)])
        spectrum_error=float(np.max(np.abs(sv-formula)))
        C=F.real;S=F.imag;J=np.eye(n)[(-x)%n]
        parity_error=max(np.linalg.norm(C@S),np.linalg.norm(C@C-(np.eye(n)+J)/2),np.linalg.norm(S@S-(np.eye(n)-J)/2))
        vals,O=np.linalg.eigh(C+np.sqrt(2)*S);q=np.diag(O.T@F@O)
        reconstruction=float(np.linalg.norm(O@np.diag(q)@O.T-F,2))
        c=2 if n%2==0 else 1
        real_count=int(sum(abs(z.imag)<1e-9 for z in q));imag_count=int(sum(abs(z.real)<1e-9 for z in q))
        assert rel<1e-10 and sharp<1e-10 and spectrum_error<1e-10 and parity_error<1e-9 and reconstruction<1e-10
        assert (real_count,imag_count)==((n+c)//2,(n-c)//2)
        records.append({'n':n,'weyl_quadratic_identity_relative_error':rel,'sharp_gap_absolute_error':float(sharp),
                        'commutator_spectrum_max_error':spectrum_error,'real_mask_reconstruction_error':reconstruction,
                        'real_mask_counts':[real_count,imag_count],
                        'stationary_r8_improved_floor':float(formula[8]/2) if n>8 else 0})
        for s in sorted(set([1,min(3,n-1),n-1])):
            k=1;b=np.zeros(n,dtype=complex);b[:s]=np.exp(2j*np.pi*k*x[:s]/n)*np.sin(np.pi*(x[:s]+1)/(s+1))
            ratio=np.linalg.norm(Z@b-np.exp(-2j*np.pi*k/n)*b)/np.linalg.norm(b)
            theoretical=2*np.sin(np.pi/(2*(s+1)))
            assert abs(ratio-theoretical)<1e-10
            sparse.append({'n':n,'s':s,'measured':float(ratio),'sharp_bound':float(theoretical)})
            # Sharpness when only one inverse row is prescribed sparse.
            u=F.conj().T[0,:];a=s/n;b=np.zeros(n,dtype=complex);b[:s]=u[:s]/a
            e=np.eye(n)[0,:];d=e-b@F
            M=F+np.outer(b.conj(),d)/np.vdot(b,b).real
            error=np.linalg.norm(M-F,2);B=np.linalg.inv(M)
            bound=np.sqrt(1-a)
            assert np.linalg.norm(B[0]-b)<1e-8 and abs(error-bound)<1e-9
            row_sharp.append({'n':n,'s':s,'error':float(error),'improved_bound':float(bound),
                              'source_bound':float(bound/(1+bound)),
                              'inverse_row_residual':float(np.linalg.norm(B[0]-b))})
    out['weyl_spectrum_real_mask']=records;out['sparse_column_sharpness']=sparse
    out['one_sparse_inverse_row_sharpness']=row_sharp
    return out


def sqrt_mod(a,p):
    """Independent Tonelli-Shanks implementation, to match normalized data."""
    a%=p
    if a==0:return 0
    if pow(a,(p-1)//2,p)!=1:raise ValueError('not square')
    q=p-1;s=0
    while q%2==0:q//=2;s+=1
    z=next(z for z in range(2,p) if pow(z,(p-1)//2,p)==p-1)
    c=pow(z,q,p);x=pow(a,(q+1)//2,p);t=pow(a,q,p);m=s
    while t!=1:
        i=1;v=t*t%p
        while v!=1:v=v*v%p;i+=1
        b=pow(c,2**(m-i-1),p);x=x*b%p;c=b*b%p;t=t*c%p;m=i
    return x


def reconstruct_seeded_source_family(n,near=False):
    """Dense algebraic reconstruction from prose/source formula, no source import.
    Inverts whole matrices with elimination, independently of uploaded LU solves.
    """
    p=998244353;g=3;rng=random.Random(21 if near else 19);a=roots(n,p,g);M=eye(n)
    for stage in range(2):
        S=[[0]*n for _ in range(n)]
        for term in range(2):
            if near:
                off=-(n-1-(stage+term)%3);diag=[2*n]*n;lo=[0]+[off]*(n-1);up=[off]*(n-1)+[0]
            else:
                diag=[9+a[rng.randrange(n)] for _ in range(n)]
                lo=[0]+[1+a[rng.randrange(n)] for _ in range(n-1)]
                up=[1+a[rng.randrange(n)] for _ in range(n-1)]+[0]
            B=[[diag[i] if i==j else lo[i] if j==i-1 else up[i] if j==i+1 else 0 for j in range(n)] for i in range(n)]
            G=inv(B,p);perm=list(range(n));rng.shuffle(perm)
            l=[(2*n if near else 1)*a[rng.randrange(n)]%p for _ in range(n)]
            r=[a[rng.randrange(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):S[perm[i]][perm[j]]=(S[perm[i]][perm[j]]+l[i]*G[i][j]*r[j])%p
        M=mul(S,M,p)
    return M


def source_data_checks(path):
    data=json.loads((path/'audit.json').read_text());out={'files_read_as_data':{},'reconstructed_small_cases':[]}
    for f in sorted(path.glob('*.py'))+sorted(path.glob('*.md'))+[path/'audit.json']:
        out['files_read_as_data'][f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
    fields=['calibrated','first_equation','second_equation','passed','circuit_calls','nonzero_first','nonzero_second']
    for near,key in ((False,'independently_permuted_green_sums'),(True,'independently_permuted_near_resonant_green_sums')):
        for n in (8,16,32):
            A=reconstruct_seeded_source_family(n,near);cal=pow(sqrt_mod(n,998244353),-1,998244353)
            report=weyl_trial(A,998244353,3,(411 if near else 311)+n,calibration=cal)
            source=next(x for x in data[key] if x['n']==n)
            assert all(report[f]==source['weyl'][f] for f in fields)
            excluded=fingerprint(A,998244353,3) is None
            assert excluded==source['two_column']['excluded']
            a,b=residuals(A,998244353,3)
            out['reconstructed_small_cases'].append({'n':n,'near_resonant':near,'source_report_fields_match':fields,
                'histogram_rejection_matches':excluded,'exact_residual_ranks':[rank(a,998244353),rank(b,998244353)]})
    out['uploaded_test_definitions_count']=sum(f.read_text().count('def test_') for f in (path/'tests').glob('*.py'))
    out['large_source_runs_not_reexecuted']=[16384,65536]
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path);ap.add_argument('--output',type=pathlib.Path)
    args=ap.parse_args();result={'audit':'independently authored checks; uploaded code never executed','exact':exact_checks(),'numerical':numerical_checks()}
    if args.source:result['source_data_comparison']=source_data_checks(args.source)
    result['status']='ALL ASSERTIONS PASSED'
    text=json.dumps(result,indent=2)
    if args.output:args.output.write_text(text+'\n')
    else:print(text)

if __name__=='__main__':main()
