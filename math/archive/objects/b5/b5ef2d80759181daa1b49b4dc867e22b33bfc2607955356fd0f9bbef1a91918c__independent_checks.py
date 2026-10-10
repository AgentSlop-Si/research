#!/usr/bin/env python3
"""Independent source-review controls. Never imports or executes uploaded code."""
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction
from collections import Counter
import json,random,math,hashlib,zipfile
import sympy as sp
import numpy as np
HERE=Path(__file__).resolve().parent;rng=random.Random(22572306)
def field(n):
    k=20
    while not sp.isprime(k*n+1):k+=1
    p=k*n+1;w=pow(int(sp.primitive_root(p)),k,p)
    assert pow(w,n,p)==1 and all(pow(w,n//r,p)!=1 for r in sp.factorint(n))
    return p,w

def mm(A,B,p):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def rank(A,p):
    a=[[v%p for v in r] for r in A];row=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];iv=pow(a[row][col],-1,p);a[row]=[iv*v%p for v in a[row]]
        for i in range(row+1,len(a)):
            c=a[i][col]
            if c:a[i]=[(u-c*v)%p for u,v in zip(a[i],a[row])]
        row+=1
        if row==len(a):break
    return row

def inverse(A,p):
    n=len(A);a=[[v%p for v in r]+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return None
        a[j],a[pivot]=a[pivot],a[j];iv=pow(a[j][j],-1,p);a[j]=[iv*v%p for v in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                c=a[i][j];a[i]=[(u-c*v)%p for u,v in zip(a[i],a[j])]
    return [r[n:] for r in a]

def F(n,w,p,sgn=-1):return [[pow(w,sgn*i*j,p) for j in range(n)] for i in range(n)]
def dft(v,w,p,sgn=-1):return [sum(x*pow(w,sgn*i*j,p) for j,x in enumerate(v))%p for i in range(len(v))]
def gl(n,p):
    A=[[int(i==j) for j in range(n)] for i in range(n)]
    for _ in range(5*n):
        i,j=rng.sample(range(n),2);a=rng.randrange(p);A[i]=[(u+a*v)%p for u,v in zip(A[i],A[j])]
    assert inverse(A,p) is not None
    return A

# Hero17: all three exact flattenings and endpoint gauges.
tensor=[];tensor_entries=0;gauge_entries=0;spectrum=[]
for Q,M in [(2,2),(2,4),(4,2),(3,4),(4,3),(3,5),(5,3),(4,4),(4,8),(8,4),(8,8)]:
    N=Q*M;p,w=field(N);xi=pow(w,M,p);eta=pow(w,Q,p)
    def t(s,h,t,u):return pow(w,-(h+M*s)*(t+Q*u),p)
    for ss,hh,tt,uu in product(range(Q),range(M),range(Q),range(M)):
        assert t(ss,hh,tt,uu)==pow(w,-hh*tt,p)*pow(xi,-ss*tt,p)*pow(eta,-hh*uu,p)%p
        tensor_entries+=1
    cuts=[[[t(ss,hh,tt,uu) for tt,uu in product(range(Q),range(M))] for ss,hh in product(range(Q),range(M))],
          [[t(ss,hh,tt,uu) for hh,uu in product(range(M),repeat=2)] for ss,tt in product(range(Q),repeat=2)],
          [[t(ss,hh,tt,uu) for hh,tt in product(range(M),range(Q))] for ss,uu in product(range(Q),range(M))]]
    ranks=[rank(A,p) for A in cuts];assert ranks==[N,min(Q,M),N]
    FQ=F(Q,xi,p);FM=F(M,eta,p)
    gauges=[('identity',[[int(i==j) for j in range(Q)] for i in range(Q)],[[int(i==j) for j in range(M)] for i in range(M)]),
            ('inverse_fourier',inverse(FQ,p),list(map(list,zip(*inverse(FM,p))))),('random_GL',gl(Q,p),gl(M,p))]
    gc=[]
    for label,A,B in gauges:
        P=mm(A,FQ,p);R=mm(FM,list(map(list,zip(*B))),p);nnz=0
        for a,h,tt,b in product(range(Q),range(M),range(Q),range(M)):
            direct=sum(A[a][ss]*t(ss,h,tt,uu)*B[b][uu] for ss,uu in product(range(Q),range(M)))%p
            pred=P[a][tt]*pow(w,-h*tt,p)*R[h][b]%p
            assert direct==pred;gauge_entries+=1;nnz+=direct!=0
        assert nnz==sum(v!=0 for r in P for v in r)*sum(v!=0 for r in R for v in r)>=N
        if label=='inverse_fourier':assert nnz==N
        gc.append({'gauge':label,'nonzeros':nnz})
    tensor.append({'Q':Q,'M':M,'p':p,'ranks':ranks,'gauges':gc})
    z=np.exp(-2j*np.pi/N)
    cross=np.array([[z**((hh+M*ss)*(tt+Q*uu))/np.sqrt(N) for hh,uu in product(range(M),repeat=2)] for ss,tt in product(range(Q),repeat=2)])
    V=np.array([[z**(h*t0) for h in range(M)] for t0 in range(Q)])
    sv=np.linalg.svd(cross,compute_uv=False);vv=np.linalg.svd(V,compute_uv=False)
    error=float(np.max(np.abs(sv[:min(Q,M)]-vv)))
    assert error<1e-11 and np.max(sv[min(Q,M):],initial=0)<1e-11
    spectrum.append({'Q':Q,'M':M,'max_singular_value_error':error})
counts=Counter()
for vals in product(range(5),repeat=4):
    A=[list(vals[:2]),list(vals[2:])]
    if inverse(A,5) is not None:counts[sum(v!=0 for r in mm(A,[[1,1],[1,4]],5) for v in r)]+=1
assert sum(counts.values())==480 and counts[2]**2==1024

# Hero0: arbitrary-input forced recurrence, singular branches, and dual sparse probes.
forced=[];entries=singular=0
for K,M in [(4,4),(8,4),(8,8),(16,4)]:
    N=K*M;p,w=field(N);wk=pow(w,M,p)
    for trial in range(3):
        x=[rng.randrange(p) for _ in range(N)];cols=[[x[b*M+t] for b in range(K)] for t in range(M)]
        ft=[dft(v,wk,p) for v in cols]
        lam=[rng.randrange(p) for _ in range(K)]
        lam[trial%K]=pow(w,trial%K,p) # force denominator zero for j=0
        e=[[(ft[t+1][ell]-lam[ell]*ft[t][ell])%p for ell in range(K)] for t in range(M-1)]
        expected=dft(x,w,p);got=[0]*N;sc=0
        for ell in range(K):
            B=sum(e[t][ell]*pow(lam[ell],M-1-t,p) for t in range(M-1))%p
            assert B==(lam[ell]*ft[-1][ell]-pow(lam[ell],M,p)*ft[0][ell])%p
            for j in range(M):
                k=ell+j*K;z=pow(w,-k,p);r=lam[ell]*z%p
                finite=(ft[0][ell]*sum(pow(r,v,p) for v in range(M))+sum(e[t][ell]*pow(z,t+1,p)*sum(pow(r,v,p) for v in range(M-1-t)) for t in range(M-1)))%p
                if r==1:
                    val=(M*ft[0][ell]+sum(e[t][ell]*pow(z,t+1,p)*(M-1-t) for t in range(M-1)))%p;sc+=1
                else:
                    H=sum(e[t][ell]*pow(z,t,p) for t in range(M-1))%p
                    val=(ft[0][ell]*(1-pow(r,M,p))+z*H-pow(z,M,p)*B)*pow((1-r)%p,-1,p)%p
                assert val==finite==expected[k];got[k]=val;entries+=1
        singular+=sc;forced.append({'K':K,'M':M,'trial':trial,'full_outputs':N,'singular_denominators':sc})
# Exact sparse uniqueness and hidden dense aliases at K=8.
p,w=field(8);K=8;A=F(K,w,p)
for size in range(1,5):
    for subset in combinations(range(K),size):assert rank([[A[i][j] for j in subset] for i in range(4)],p)==size
invA=inverse(A,p);hidden_spectrum=[0]*8;hidden_spectrum[4]=1
hidden_position=[r[4] for r in invA];assert all(v!=0 for v in hidden_position)
assert dft(hidden_position,w,p)==hidden_spectrum
hidden_time=[0]*8;hidden_time[4]=1;assert all(v!=0 for v in dft(hidden_time,w,p))
# Sparse single-event decoder in both domains, all nonzero amplitudes at all sites.
dual_cases=0
for b in range(K):
    for a in [1,2,p-1]:
        v=[0]*K;v[b]=a;spec=dft(v,w,p)
        node=spec[1]*pow(spec[0],-1,p)%p
        assert next(j for j in range(K) if pow(w,-j,p)==node)==b
        ev=[0]*K;ev[b]=a;time=[a*row[b]%p for row in invA]
        node=time[1]*pow(time[0],-1,p)%p
        assert next(j for j in range(K) if pow(w,j,p)==node)==b
        dual_cases+=2
# Exact Freivalds annihilator counting for two distinct ranks.
freivalds=[]
for R in [[[1,2],[2,4],[3,1]],[[1,0],[0,1],[1,1]],[[0,0],[0,0],[0,0]]]:
    rr=rank(R,5);accepted=sum(all(sum(wv[i]*R[i][j] for i in range(3))%5==0 for j in range(2)) for wv in product(range(5),repeat=3))
    assert accepted==5**(3-rr);freivalds.append({'rank':rr,'accepted':accepted,'trials':125})

# Theory: cyclic solves including zero and singular weights, recurrences, sparse rank gate.
cycle_cases=[];p=65537
for n in [2,3,4,8,16,32]:
    for mode in ['generic','one_zero','all_zero','singular_product_one']:
        order=list(range(n));rng.shuffle(order);weights=[rng.randrange(1,p) for _ in range(n)]
        if mode=='one_zero':weights[order[n//2]]=0
        if mode=='all_zero':weights=[0]*n
        if mode=='singular_product_one':weights[order[-1]]=pow(math.prod(weights[order[k]] for k in range(n-1))%p,-1,p)
        A=[[int(i==j) for j in range(n)] for i in range(n)]
        for t,i in enumerate(order):A[i][order[(t+1)%n]]=(A[i][order[(t+1)%n]]-weights[i])%p
        den=(1-math.prod(weights))%p
        if den==0:
            assert inverse(A,p) is None;cycle_cases.append({'n':n,'mode':mode,'singular_correctly_guarded':True});continue
        u=[rng.randrange(p) for _ in range(n)];prefix=1;num=0
        for i in order:num=(num+prefix*u[i])%p;prefix=prefix*weights[i]%p
        y=[0]*n;y[order[0]]=num*pow(den,-1,p)%p
        for t in range(n-1,0,-1):i=order[t];y[i]=(u[i]+weights[i]*y[order[(t+1)%n]])%p
        assert [sum(A[i][j]*y[j] for j in range(n))%p for i in range(n)]==u
        dense=mm(inverse(A,p),[[v] for v in u],p);assert y==[v[0] for v in dense]
        cycle_cases.append({'n':n,'mode':mode,'exact_equations':True})
recurrence=[]
for rho in [Fraction(0),Fraction(1,2),Fraction(1),Fraction(3,2),Fraction(2)]:
    a=Fraction(1)
    for h in range(1,41):
        a=max(a,rho*a+1)
        if rho<1:assert a<=max(Fraction(1),1/(1-rho))
        elif rho==1:assert a==1+h
        else:assert a==rho**h+(rho**h-1)/(rho-1)
    recurrence.append({'rho':str(rho),'h':40,'exact_envelope':str(a)})
a=Fraction(1);u=Fraction(1,2)
for h in range(2,101):
    a=2*Fraction(h-1,h)*a+1;v=h*a/Fraction(2**h)
    assert v-u==Fraction(h,2**h);u=v
rankgates=[]
for n in [4,8,16,32]:
    p,w=field(n);FF=F(n,w,p)
    for d in [0,1,2,3]:
        for trial in range(3):
            S=[[0]*n for _ in range(n)]
            for i in range(n):
                for j in rng.sample(range(n),min(d,n)):S[i][j]=rng.randrange(1,p)
            R=rank([[(FF[i][j]-S[i][j])%p for j in range(n)] for i in range(n)],p)
            bound=n//(d+1);assert R>=bound
            r=bound;untouched=[j for j in range(n) if all(S[i][j]==0 for i in range(r))]
            assert len(untouched)>=r and (r==0 or rank([[FF[i][j] for j in untouched[:r]] for i in range(r)],p)==r)
            rankgates.append({'N':n,'d':d,'rank':R,'bound':bound})

# Integrity, including exact inherited bundle/source equality.
hero17=HERE/'fft_hero17_phase6_tensor_cut_rigidity_2026-10-10/hero17_phase6_tensor_rigidity'
hero0=HERE/'fft_hero0_phase9_dense_cycle_2026-10-10/fft_hero0_phase9_dense_cycle_2026-10-10'
mass=HERE/'mass_contraction_bundle/fft_mass_contraction_theory'
verified=[]
for base in [hero17,mass]:
    for line in (base/'SHA256SUMS.txt').read_text().splitlines():
        if not line.strip():continue
        digest,path=line.split(maxsplit=1);path=path.lstrip('* ')
        assert hashlib.sha256((base/path).read_bytes()).hexdigest()==digest
        verified.append(str((base/path).relative_to(HERE)))
for path,meta in json.loads((hero0/'SHA256SUMS.json').read_text()).items():
    b=(hero0/path).read_bytes();assert len(b)==meta['size_bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'];verified.append(str((hero0/path).relative_to(HERE)))
prior=HERE/'inherited_reference'
pairs=[(hero0/'prior_phase8_bundle.zip',prior/'source/fft_hero0_phase8_weyl_cycle_2026-10-10.zip'),(hero0/'phase8_weyl_cycle.py',prior/'extracted/phase8_weyl_cycle.py'),(hero0/'phase6_exact.py',prior/'extracted/phase6_exact.py')]
assert all(a.read_bytes()==b.read_bytes() for a,b in pairs)
assert (mass/'THEORY.md').read_bytes()==(HERE/'THEORY.md').read_bytes()
result={'hero17':{'tensor_entries':tensor_entries,'gauged_entries':gauge_entries,'cases':tensor,'complex_spectrum_controls':spectrum,
                  'GL2_F5_support_histogram':dict(counts),'GL2_F5_pairs_accounted':480**2,'minimum_support_pairs':counts[2]**2},
        'hero0':{'forced_identity_cases':forced,'full_outputs_checked':entries,'singular_denominators':singular,
                 'dual_single_event_decodes':dual_cases,'sparse_uniqueness_all_subsets_up_to_four_K8':True,
                 'both_dense_probe_alias_controls':True,'freivalds_exact_counts':freivalds},
        'mass_theory':{'cyclic_cases':cycle_cases,'constant_recurrences':recurrence,'harmonic_telescope_verified_through_height':100,
                       'row_sparse_rank_controls':rankgates,'contracting_factorization_supplied':False},
        'integrity':{'manifest_files_verified':len(verified),'verified_paths':verified,
                     'inherited_phase8_bundle_and_two_sources_byte_identical':True,'standalone_theory_matches_bundle':True},
        'scope':'Independent exact controls and proof review; no uploaded code run and no new uniform Fourier algorithm.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'tensor_entries':tensor_entries,'gauged_entries':gauge_entries,'forced_output_entries':entries,'singular_denominators':singular,'verified_manifest_files':len(verified)},indent=2))
