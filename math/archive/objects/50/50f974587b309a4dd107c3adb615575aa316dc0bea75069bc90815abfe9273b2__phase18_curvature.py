"""Hero #0 Phase 18: exact half-grid displacement and curvature energy gates.

All matrix bounds are necessary conditions, not an FFT factorization.
The complex tests use unitary DFT and normal spectral/Frobenius norms.
The modular checks use GF(65537) and exact integer arithmetic.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import math
import numpy as np
from phase17_gauge import (
    half_grid_permutation, unitary_fourier, margulis_permutations,
    normalized_error_gap,
)


def weighted_permutation(perm, weights):
    """P[i,perm[i]]=weights[i], matching the earlier Hero #0 convention."""
    perm = np.asarray(perm, dtype=np.int64)
    weights = np.asarray(weights)
    n = len(perm)
    P = np.zeros((n,n), dtype=np.result_type(weights, 1.0))
    P[np.arange(n), perm] = weights
    return P


def green_inverse(perm, weights):
    return np.linalg.inv(np.eye(len(perm), dtype=complex) - weighted_permutation(perm, weights))


def flat_weights(perm, c, gauge):
    """Weights for P=D*(c P_perm)*D^-1. A common phase gauge remains unitary."""
    return c * np.asarray(gauge) / np.asarray(gauge)[np.asarray(perm)]


def paired_difference_energy(perm, weights, tau):
    if not np.array_equal(perm[tau], tau[perm]):
        raise ValueError('Permutation must commute with half-grid tau')
    return float(np.sum(np.abs(np.asarray(weights)-np.asarray(weights)[tau])**2))


def direct_fourier_commutator(s):
    tau = half_grid_permutation(s)
    U = unitary_fourier(s*s)
    return U[:,tau]-U[tau,:]


def modular_phase_sum(s, p=65537, generator=3):
    """Exact finite-field version of sum_(k,j) z^(k tau(j)-tau(k) j)."""
    n=s*s
    if (p-1)%n: raise ValueError('length must divide p-1')
    z=pow(generator,(p-1)//n,p)
    powers=[pow(z,k,p) for k in range(n)]
    tau=half_grid_permutation(s)
    total=0
    for k in range(n):
        for j in range(n):
            total=(total+powers[(k*int(tau[j])-int(tau[k])*j)%n])%p
    return total


@dataclass
class GreenTerm:
    perm: np.ndarray
    weights: np.ndarray
    alpha: complex
    flat: np.ndarray | None = None


def network_matrix(layers):
    if not layers or not layers[0]: raise ValueError('nonempty layers required')
    n=len(layers[0][0].perm)
    T=np.eye(n,dtype=complex)
    for layer in layers:
        L=np.zeros((n,n),dtype=complex)
        for term in layer:
            L+=term.alpha*green_inverse(term.perm,term.weights)
        T=L@T
    return T


def curvature_gate(s, layers, phase_gauge=None, target=None):
    """Return proved lower bounds on Fourier relative-Frobenius error.

    Each Green inverse (actual AND flat, if supplied) must have ||G||_2<=g.
    Paired energy applies to arbitrary weights; flat energy needs common phase
    gauge across every term, checked numerically when `flat` is supplied.
    The term weights are fixed, not input dependent.
    """
    tau=half_grid_permutation(s)
    n=s*s
    m=len(layers)
    U=unitary_fourier(n) if target is None else target
    T=network_matrix(layers)
    err=float(np.linalg.norm(U-T,'fro')/math.sqrt(n))
    A=sum(abs(t.alpha) for layer in layers for t in layer)
    a=max(sum(abs(t.alpha) for t in layer) for layer in layers)
    if A==0: raise ValueError('all layer coefficients zero; Fourier equality excluded trivially')
    g=max(float(np.linalg.norm(green_inverse(t.perm,t.weights),2))
          for layer in layers for t in layer)
    for layer in layers:
        for t in layer:
            if t.flat is not None:
                g=max(g,float(np.linalg.norm(green_inverse(t.perm,t.flat),2)))
    B=(a*g)**(m-1)*g*g
    raw=sum(abs(t.alpha)*paired_difference_energy(t.perm,t.weights,tau)
            for layer in layers for t in layer)
    raw_bound=max(0.0,(math.sqrt(2)-B*math.sqrt(A*raw/n))/2)
    flat_energy=None
    flat_bound=None
    if all(t.flat is not None for layer in layers for t in layer):
        if phase_gauge is None:
            raise ValueError('provide common unitary phase gauge to certify the flat reference')
        d=np.asarray(phase_gauge,dtype=complex)
        if len(d)!=n or not np.allclose(np.abs(d),1.0,atol=1e-9):
            raise ValueError('flat reference requires one shared unitary diagonal gauge')
        for layer in layers:
            for t in layer:
                ratio=np.asarray(t.flat)*d[t.perm]/d
                if not np.allclose(ratio,ratio[0],atol=1e-9):
                    raise ValueError('reference is not common-gauge scalar-permutation flat')
        flat_energy=sum(abs(t.alpha)*float(np.sum(np.abs(t.weights-t.flat)**2))
                        for layer in layers for t in layer)
        flat_bound=max(0.0,normalized_error_gap(s)-B*math.sqrt(A*flat_energy/n))
    return {
        'n':n,'layers':m,'actual_relative_fro_error':err,
        'max_green_norm_g':g,'alpha_sum_A':A,'max_layer_alpha_sum_a':a,
        'telescoping_factor_B':B,
        'paired_energy':raw, 'paired_energy_normalized':raw/n,
        'raw_symmetry_error_floor':raw_bound,
        'flat_energy':flat_energy,
        'flat_energy_normalized':None if flat_energy is None else flat_energy/n,
        'flat_gauge_error_floor':flat_bound,
        'commutator_norm_fro':float(np.linalg.norm(direct_fourier_commutator(s),'fro')),
        'raw_symmetry_energy_required_for_exact':2*n/(A*B*B),
        'flat_energy_required_for_exact':normalized_error_gap(s)**2*n/(A*B*B),
    }


def forest_gauge_holonomies(perms, weights, constants, modulus):
    """O(E) graph operations plus field inversions; returns exact cycle defects.

    Row-oriented edge i -> perm[i] has desired weight
             weight[i] = constant * d[i]/d[perm[i]].
    Under the forest gauge each failed nontree edge is a nontrivial
    fundamental-cycle holonomy. Parallel edges and self-loops are supported.
    This is a gauge certificate, not a complete Fourier circuit test.
    """
    p=modulus
    n=len(perms[0]); adj=[[] for _ in range(n)]
    E=[]
    for t,(perm,vec,c) in enumerate(zip(perms,weights,constants)):
        if len(perm)!=n or len(vec)!=n: raise ValueError('inconsistent sizes')
        for u,v in enumerate(perm):
            w=int(vec[u])%p;c=int(c)%p;v=int(v)
            if w==0 or c==0: raise ValueError('nonzero modular weights required')
            eid=len(E); E.append((u,v,w,c,t))
            ratio=c*pow(w,-1,p)%p
            adj[u].append((v,ratio,eid))
            adj[v].append((u,pow(ratio,-1,p),eid))
    d=[None]*n; forest=set()
    for root in range(n):
        if d[root] is not None:continue
        d[root]=1; queue=deque([root])
        while queue:
            u=queue.popleft()
            for v,ratio,eid in adj[u]:
                if d[v] is None:
                    d[v]=int(d[u])*ratio%p
                    forest.add(eid);queue.append(v)
    failed=[]
    for eid,(u,v,w,c,t) in enumerate(E):
        if (w*d[v]-c*d[u])%p:
            if eid in forest: raise AssertionError('forest edge inconsistency')
            failed.append({'edge_id':eid,'term':t,'u':u,'v':v,
                           'holonomy_ratio':w*d[v]*pow(c*d[u]%p,-1,p)%p})
    return {'gauge':d,'nontrivial_fundamental_holonomies':failed,
            'holonomy_count':len(failed),'tree_edges':len(forest),'edges':len(E),
            'components':n-len(forest)}


def mod_inverse_matrix(M,p=65537):
    A=np.array(M,dtype=np.int64)%p
    n=A.shape[0]
    if A.shape!=(n,n): raise ValueError('square only')
    Z=np.concatenate([A,np.eye(n,dtype=np.int64)],axis=1)
    for col in range(n):
        piv=next((r for r in range(col,n) if Z[r,col]),None)
        if piv is None: raise ValueError('singular')
        if piv!=col: Z[[col,piv]]=Z[[piv,col]]
        Z[col]=Z[col]*pow(int(Z[col,col]),-1,p)%p
        for r in range(n):
            if r==col: continue
            factor=Z[r,col]
            if factor: Z[r]=(Z[r]-factor*Z[col])%p
    return Z[:,n:]


def modular_network(layers,p=65537):
    from phase17_gauge import mod_matmul
    n=len(layers[0][0].perm)
    total=np.eye(n,dtype=np.int64)
    for layer in layers:
        mat=np.zeros((n,n),dtype=np.int64)
        for term in layer:
            P=np.zeros((n,n),dtype=np.int64)
            P[np.arange(n),term.perm]=np.asarray(term.weights,dtype=np.int64)%p
            G=mod_inverse_matrix((np.eye(n,dtype=np.int64)-P)%p,p)
            mat=(mat+int(term.alpha)*G)%p
        total=mod_matmul(mat,total,p)
    return total


def exact_commutator_singular_values(s):
    """Analytic spectrum of U Pi-Pi U for even s, N=s*s."""
    if s<2 or s%2: raise ValueError('s must be even')
    n=s*s
    return np.r_[np.repeat(math.sqrt(2+math.sqrt(2)),n//2),
                 np.repeat(math.sqrt(2-math.sqrt(2)),n//2)]


def symmetry_rank_correction_floor(n,k):
    """Necessary relative-Frobenius error for rank-k departure from [T0,Pi]=0.

    Derived via Eckart-Young applied to [U,Pi], since [Delta,Pi] rank<=2k.
    This is a lower bound, not necessarily attained by a rank-k graph edit.
    """
    if k<0 or k>n: raise ValueError('rank correction out of range')
    r=min(n,2*k)
    big=2+math.sqrt(2); small=2-math.sqrt(2)
    if r<=n//2:
        omitted=(n//2-r)*big + (n//2)*small
    else:
        omitted=(n-r)*small
    return .5*math.sqrt(max(0.,omitted/n))


def modular_polyphase_certificate(s,p=65537,generator=3):
    """Exact all-coordinate certificate of the proof's monomial conjugate.

    U=B D C /s, where C transforms x->b and B transforms y->a.
    C V C^-1 = Py D^-1 Pb D is a monomial operator on (b,y).
    """
    from phase17_gauge import modular_fourier,mod_matmul
    n=s*s
    if s%2 or (p-1)%n: raise ValueError('even side and root-compatible prime')
    z=pow(generator,(p-1)//n,p)
    w=pow(z,s,p)
    rootn=[pow(z,j,p) for j in range(n)]
    roots=[pow(w,j,p) for j in range(s)]
    U=(modular_fourier(n,p,generator)*pow(s,-1,p))%p
    Uinv=(modular_fourier(n,p,generator,inverse=True)*pow(s,-1,p))%p
    tau=half_grid_permutation(s)
    Pi=np.eye(n,dtype=np.int64)[:,tau]
    V=mod_matmul(mod_matmul(mod_matmul(Pi,Uinv,p),Pi,p),U,p)
    C=np.zeros((n,n),dtype=np.int64)
    Ci=np.zeros((n,n),dtype=np.int64)
    B=np.zeros((n,n),dtype=np.int64)
    D=np.zeros((n,n),dtype=np.int64)
    for x in range(s):
        for y in range(s):
            for b in range(s):
                C[b*s+y,x*s+y]=roots[b*x%s]
                Ci[x*s+y,b*s+y]=roots[(-b*x)%s]*pow(s,-1,p)%p
                for a in range(s):
                    B[a*s+b,b*s+y]=roots[a*y%s]
            D[x*s+y,x*s+y]=rootn[x*y%n]
    Ufrom=mod_matmul(mod_matmul(B,D,p),C,p)*pow(s,-1,p)%p
    normal=mod_matmul(mod_matmul(C,V,p),Ci,p)
    W=np.zeros((n,n),dtype=np.int64)
    half=s//2
    for b in range(s):
        for y in range(s):
            tb=(b+half)%s;ty=(y+half)%s
            W[tb*s+ty,b*s+y]=rootn[(b-tb)*y%n]
    I=np.eye(n,dtype=np.int64)
    V2=mod_matmul(V,V,p)
    V4=mod_matmul(V2,V2,p)
    return {
        'n':n,
        'fft_factorization_failures':int(np.count_nonzero((Ufrom-U)%p)),
        'polyphase_conjugation_failures':int(np.count_nonzero((normal-W)%p)),
        'order_eight_failures':int(np.count_nonzero((V4+I)%p)),
    }


def linear_time_curvature_certificate(s, layers, phase_gauge=None):
    """O(E)-arithmetic no-matrix-reconstruction necessary-condition certificate.

    Input: a constant or variable number of Green weighted-permutation terms,
    each a length N permutation/weight array. For a rigorous cheap norm bound,
    requires rho=max(|all actual and reference edge weights|)<1, whence
    ||(I-P)^-1||2<=1/(1-rho). Counts all E supplied weights and coefficients.
    The flat-gauge part requires a common unitary diagonal D across all terms.
    Only computes necessary lower bounds; cannot certify Fourier equality.
    """
    tau=half_grid_permutation(s);n=s*s
    if not layers or not all(layers): raise ValueError('nonempty layers required')
    all_terms=[t for layer in layers for t in layer]
    if any(len(t.perm)!=n or len(t.weights)!=n for t in all_terms):
        raise ValueError('all inputs must have common N')
    rho=max(float(np.max(np.abs(t.weights))) for t in all_terms)
    has_flat=all(t.flat is not None for t in all_terms)
    if has_flat:
        rho=max(rho,max(float(np.max(np.abs(t.flat))) for t in all_terms))
    if rho>=1:raise ValueError('linear-time norm certificate needs rho<1')
    g=1/(1-rho)
    A=sum(abs(t.alpha) for t in all_terms)
    a=max(sum(abs(t.alpha) for t in layer) for layer in layers)
    if A==0: raise ValueError('all layer coefficients zero; Fourier equality excluded trivially')
    B=(a*g)**(len(layers)-1)*g*g
    raw=sum(abs(t.alpha)*paired_difference_energy(t.perm,t.weights,tau)
            for t in all_terms)
    report={
        'n':n,'number_of_terms':len(all_terms),'read_weight_entries':n*len(all_terms),
        'rho':rho,'bound_green_norm_g':g,'telescoping_factor_B':B,
        'raw_paired_energy':raw,
        'necessary_raw_energy_for_exact':2*n/(A*B*B),
        'relative_fro_error_floor_raw':
          max(0.,(math.sqrt(2)-B*math.sqrt(A*raw/n))/2),
    }
    if has_flat:
        if phase_gauge is None:raise ValueError('common unitary gauge required')
        d=np.asarray(phase_gauge,dtype=complex)
        if len(d)!=n or not np.allclose(abs(d),1,atol=1e-9):
            raise ValueError('common phase gauge invalid')
        for t in all_terms:
            ratio=np.asarray(t.flat)*d[t.perm]/d
            if not np.allclose(ratio,ratio[0],atol=1e-9):
                raise ValueError('flat reference is not one common phase gauge')
        energy=sum(abs(t.alpha)*float(np.sum(abs(t.weights-t.flat)**2))
                   for t in all_terms)
        gap=normalized_error_gap(s)
        report.update({
            'reference_energy':energy,
            'necessary_reference_energy_for_exact':gap**2*n/(A*B*B),
            'relative_fro_error_floor_flat':
                max(0.,gap-B*math.sqrt(A*energy/n)),
        })
    return report


def modular_fourier_weyl_gate(M,p=65537,generator=3):
    """Exact necessary-and-sufficient matrix gate for M=F_N over GF(p).

    With S e_j=e_(j+1), D[k,k]=omega^k, F S=D F and F e0=ones.
    This dense O(N²) audit is for small research candidates, not an FFT speedup.
    """
    from phase17_gauge import primitive_root,mod_matmul
    M=np.asarray(M,dtype=np.int64)%p
    n=M.shape[0]
    if M.shape!=(n,n):raise ValueError('square matrix required')
    z=primitive_root(n,p,generator)
    S=np.zeros((n,n),dtype=np.int64)
    S[(np.arange(n)+1)%n,np.arange(n)]=1
    D=np.diag(np.asarray([pow(z,k,p) for k in range(n)],dtype=np.int64))
    residual=(mod_matmul(M,S,p)-mod_matmul(D,M,p))%p
    origin=(M[:,0]-1)%p
    return {
        'n':n,'weyl_defect_nonzeros':int(np.count_nonzero(residual)),
        'origin_defect_nonzeros':int(np.count_nonzero(origin)),
        'passes':bool(not np.any(residual) and not np.any(origin)),
    }
