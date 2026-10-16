"""New transcription controls. Does not import or run historical project code.

The universal result is proved in REPORT.md. Exact finite arithmetic controls the
weighted-cycle exponent and dimension counts. Dense NumPy experiments are only
supporting numerical checks; they do not certify exact covariance or rank.
"""
import json
import math
from pathlib import Path
import numpy as np

SEED = 20261016048
rng = np.random.default_rng(SEED)
delta = 129/512
gamma = math.sqrt(2-math.sqrt(2))-129/256

# Exact rational certificate gamma > 1/4.
assert 93823**2 > 2*65536**2

counts = []
for n in range(3, 21):
    N = 2**n
    # Strict threshold: N/4 < 2*j+1 < 7*N/4.
    # For dyadic N>=8, this means N/8 <= j <= 7*N/8-1.
    lo, hi = N//8, 7*N//8-1
    assert 4*(2*lo+1)>N and 4*(2*hi+1)<7*N
    assert 4*(2*(lo-1)+1)<N and 4*(2*(hi+1)+1)>7*N
    assert hi-lo+1 == 3*N//4
    counts.append({'N':N,'count':hi-lo+1})

cycle_controls = []
for N in [8,16,32,64,128,256,512]:
    for trial in range(10):
        p = rng.permutation(N).tolist()
        invp = [0]*N
        for j in range(N): invp[p[j]]=j
        # R = P diag(omega^b); L* D L has the permutation a of root exponents.
        a = rng.permutation(N).tolist()
        b = rng.integers(0,N,size=N).tolist()
        successor = [p[(invp[k]+1)%N] for k in range(N)]
        exp = [(b[(invp[k]+1)%N]-b[invp[k]]-a[successor[k]])%N for k in range(N)]
        seen=set(); k=0; total=0
        for step in range(N):
            assert k not in seen
            seen.add(k); total += exp[k]; k=successor[k]
        assert k==0 and len(seen)==N and total%N==N//2
        cycle_controls.append({'N':N,'trial':trial,'cycle_length':len(seen),'product_exponent':total%N})

def path_adjacency(N, order):
    A=np.zeros((N,N),dtype=complex)
    for j in range(N-1):
        A[order[j],order[j+1]]=1
        A[order[j+1],order[j]]=1
    return A

def haar_synthesis(m):
    H=np.zeros((m,m),dtype=complex)
    H[:,0]=1/math.sqrt(m)
    col=1
    width=m
    while width>=2:
        for start in range(0,m,width):
            H[start:start+width//2,col]=1/math.sqrt(width)
            H[start+width//2:start+width,col]=-1/math.sqrt(width)
            col += 1
        width//=2
    assert col==m
    return H

def monomial(N):
    P=np.eye(N,dtype=complex)[:,rng.permutation(N)]
    return P @ np.diag(np.exp(1j*rng.uniform(-math.pi,math.pi,N)))

samples=[]
for N in [8,16,32,64,128]:
    I=np.eye(N,dtype=complex)
    Z=np.roll(I,1,axis=0)
    D=np.diag(np.exp(2j*math.pi*np.arange(N)/N))
    H=haar_synthesis(N//2)
    R_H=np.block([[np.zeros_like(H),H],[H.conj().T,np.zeros_like(H)]])
    eps=1/512
    V=(I+1j*eps*R_H)/math.sqrt(1+eps**2)
    for trial in range(3):
        Cs=[]
        for q in range(2):
            A=path_adjacency(N,rng.permutation(N))
            Cs.append(np.linalg.solve(I-1j*A/32,I+1j*A/32))
        S=V@Cs[0]@Cs[1]
        L,R=monomial(N),monomial(N)
        Zp=R@Z@R.conj().T
        Dp=L.conj().T@D@L
        baseline=Zp-Dp
        expected=np.sort(2*np.abs(np.sin((2*np.arange(N)+1)*math.pi/(2*N))))[::-1]
        assert np.max(np.abs(np.linalg.svd(baseline,compute_uv=False)-expected))<1e-12
        W=Dp.conj().T@Zp
        cycle_error=float(np.linalg.norm(np.linalg.matrix_power(W,N)+I,2))
        assert cycle_error<1e-10
        for inverse in [False,True]:
            T=S.conj().T if inverse else S
            A=L@T@R
            defect=A@Z-D@A
            reduced=T@Zp-Dp@T
            reduction_error=float(np.linalg.norm(L.conj().T@defect@R.conj().T-reduced,2))
            stage_distance=float(np.linalg.norm(T-I,2))
            perturbation=float(np.linalg.norm(reduced-baseline,2))
            singulars=np.linalg.svd(defect,compute_uv=False)
            kth=float(singulars[3*N//4-1])
            unitarity=float(np.linalg.norm(T.conj().T@T-I,2))
            assert reduction_error<1e-12
            assert stage_distance<delta
            assert perturbation<2*delta
            assert kth>gamma
            assert unitarity<1e-12
            samples.append({'N':N,'trial':trial,'inverse':inverse,'stage_distance':stage_distance,
                'defect_perturbation':perturbation,'singular_at_3N_over_4':kth,
                'unitarity_error':unitarity,'reduction_error':reduction_error,
                'weighted_cycle_power_error':cycle_error})

out={'status':'PASS','seed':SEED,'historical_programs_executed':False,
     'universal_claim_established_by':'REPORT.md proof, not these finite checks',
     'exact_count_controls':counts,'exact_weighted_cycle_controls':cycle_controls,
     'gamma':gamma,'gamma_gt_quarter_exact_certificate':{'lhs':93823**2,'rhs':2*65536**2},
     'numerical_samples':samples,
     'summary':{'exact_count_lengths':len(counts),'exact_weighted_cycle_instances':len(cycle_controls),
                'numerical_stage_instances':len(samples),
                'minimum_checked_3N_over_4_singular':min(s['singular_at_3N_over_4'] for s in samples),
                'maximum_stage_distance':max(s['stage_distance'] for s in samples)}}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['summary'],indent=2))
