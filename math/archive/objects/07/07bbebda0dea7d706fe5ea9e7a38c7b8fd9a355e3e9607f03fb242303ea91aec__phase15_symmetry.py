"""Hero #0 / Phase 15: reproducible Weyl-symmetry barrier for Fourier/Green networks.

All main claims are necessary conditions for a restricted graph grammar.
NO universal sub-NlogN Fourier algorithm is asserted.
"""
from __future__ import annotations
import math
from typing import Sequence
import numpy as np

PRIME = 65537
GEN = 3


def margulis_maps(s:int)->list[np.ndarray]:
    """Four Margulis/Gabber/Galil permutations on Z_s x Z_s."""
    if s<2:raise ValueError('s>=2')
    maps=[]
    for k in range(4):
        p=[]
        for x in range(s):
            for y in range(s):
                if k==0: X,Y=(x+2*y)%s,y
                elif k==1:X,Y=(x+2*y+1)%s,y
                elif k==2:X,Y=x,(y+2*x)%s
                else:X,Y=x,(y+2*x+1)%s
                p.append(X*s+Y)
        p=np.asarray(p,dtype=np.int64)
        assert len(set(map(int,p)))==s*s
        maps.append(p)
    return maps


def half_translation(s:int,axis:str='x')->np.ndarray:
    if s%2 or s<2:raise ValueError('even s >=2')
    h=s//2
    if axis not in ('x','y','xy'):raise ValueError('axis')
    return np.asarray([((x+(h if 'x' in axis else 0))%s)*s+
                      (y+(h if 'y' in axis else 0))%s
                      for x in range(s) for y in range(s)],dtype=np.int64)


def perm_commutes(p:Sequence[int],q:Sequence[int])->bool:
    p=np.asarray(p,dtype=np.int64);q=np.asarray(q,dtype=np.int64)
    return bool(np.array_equal(p[q],q[p]))


def normalized_dft(s:int)->np.ndarray:
    n=s*s;k=np.arange(n,dtype=np.int64)
    return np.exp(-2j*np.pi*np.outer(k,k)/n)/s


def commutator_from_permutation(U:np.ndarray,p:Sequence[int])->np.ndarray:
    p=np.asarray(p,dtype=np.int64)
    # Matrix of Q is Q[p[i],i]=1; for an involution Q=Q^T
    return U[:,p]-U[p,:]


def primitive_root_power_two(n:int,p:int=PRIME)->int:
    if n<2 or n&(n-1) or (p-1)%n:raise ValueError('n must be a divisor of p-1 and power of two')
    z=pow(GEN,(p-1)//n,p)
    assert pow(z,n,p)==1 and pow(z,n//2,p)!=1
    return z


def modular_dft(s:int,p:int=PRIME,negative:bool=False)->np.ndarray:
    n=s*s;z=primitive_root_power_two(n,p)
    inv_s=pow(s,-1,p)
    powers=np.asarray([pow(z,i,p) for i in range(n)],dtype=np.int64)
    t=np.arange(n,dtype=np.int64)
    exp=np.outer(t,t)%n
    if negative:exp=(-exp)%n
    return (powers[exp]*inv_s)%p


def modular_matmul(A:np.ndarray,B:np.ndarray,p:int=PRIME)->np.ndarray:
    A=np.asarray(A,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
    # Entry max p^2 * n; at n<=256, all well inside 64-bit range.
    if A.shape[1]*(p-1)**2 >= 2**63:raise ValueError('potential 64-bit overflow')
    return (A@B)%p


def modular_commutator_certificate(s:int,axis:str,p:int=PRIME)->dict:
    n=s*s
    U=modular_dft(s,p)
    Ustar=modular_dft(s,p,negative=True)
    translate=half_translation(s,axis)
    C=(U[:,translate]-U[translate,:])%p
    Cstar=(Ustar[translate,:]-Ustar[:,translate])%p
    # (UQ-QU)^* = Q U^* - U^* Q, since Q=Q^*=Q^-1.
    H=modular_matmul(Cstar,C,p)
    I=np.eye(n,dtype=np.int64)
    if axis=='x':
        residue=modular_matmul(H,(H-4*I)%p,p)
        expected='H(H-4I)=0'
    else:
        residue=(modular_matmul(H,H,p)-4*H+2*I)%p
        expected='H^2-4H+2I=0'
    # Independent check of Cstar calculation via polynomial trace & multiplication
    assert np.array_equal(modular_matmul(Ustar,U,p),I)
    assert not np.any(residue),f'polynomial failed s={s} axis={axis}'
    trH=int(np.trace(H)%p)
    assert trH==(2*n)%p,('trace H',trH,n)
    return {'s':s,'N':n,'axis':axis,'prime':p,'polynomial':expected,
            'trace_H_mod_p':trH,'nonzero_residual_entries':int(np.count_nonzero(residue))}


def cycles(pi:Sequence[int])->list[list[int]]:
    n=len(pi);seen=[False]*n;out=[]
    for i in range(n):
        if seen[i]:continue
        cyc=[];j=i
        while not seen[j]:
            seen[j]=True;cyc.append(j);j=int(pi[j])
        assert j==i
        out.append(cyc)
    return out


def green_apply(pi:Sequence[int],weights:Sequence[complex|int],x:Sequence[complex|int],mod:int|None=None):
    """Solve y_i-w_i*y_(pi(i))=x_i, in O(N) field operations."""
    n=len(pi)
    if len(weights)!=n or len(x)!=n:raise ValueError('length mismatch')
    out=[0]*n
    for cyc in cycles(pi):
        prod=1
        rhs=0
        for idx in cyc:
            rhs+=prod*x[idx]
            prod*=weights[idx]
            if mod:
                rhs%=mod;prod%=mod
        den=(1-prod)%mod if mod else 1-prod
        if den==0:raise ZeroDivisionError('singular green cycle')
        out[cyc[0]]=rhs*(pow(int(den),-1,mod) if mod else 1/den)
        if mod:out[cyc[0]]%=mod
        for t in range(len(cyc)-1,0,-1):
            idx=cyc[t]
            out[idx]=x[idx]+weights[idx]*out[int(pi[idx])]
            if mod:out[idx]%=mod
    return out


def mixed_green_network(s:int,vec:list[int],weight:int=2,mod:int=PRIME)->list[int]:
    """A mixed-axis 2-layer network (four affine resolvents per layer)."""
    maps=margulis_maps(s)
    n=s*s
    coeff=pow(4,-1,mod)
    def layer(x,order):
        out=[0]*n
        for j in order:
            vals=green_apply(maps[j],[weight]*n,x,mod)
            for i in range(n):out[i]=(out[i]+coeff*vals[i])%mod
        return out
    return layer(layer(vec,range(4)),range(3,-1,-1))


def dense_green_matrix(pi:Sequence[int],weights:Sequence[complex])->np.ndarray:
    n=len(pi)
    P=np.zeros((n,n),dtype=np.complex128)
    P[np.arange(n),np.asarray(pi,dtype=np.int64)]=weights
    return np.linalg.inv(np.eye(n,dtype=complex)-P)


def graph_symmetry_delta(pi:Sequence[int],weights:Sequence[complex],tau:Sequence[int])->float:
    if not perm_commutes(pi,tau):raise ValueError('permutation not translation equivariant')
    w=np.asarray(weights,dtype=complex)
    tau=np.asarray(tau,dtype=np.int64)
    return float(np.max(np.abs(w-w[tau])))


def matrix_network_and_breaking_budget(s:int,perturb:float=0.0,seed:int=14015)->dict:
    """Two 4-resolvent mixed-axis layers with a computable commutator budget."""
    rng=np.random.default_rng(seed)
    n=s*s
    tau=half_translation(s,'x')
    maps=margulis_maps(s)
    layers=[]; bounds=[];comm_bounds=[]; actual_deltas=[]
    for m in range(2):
        M=np.zeros((n,n),dtype=np.complex128)
        b=0.0; norm_bound=0.0
        for j in (range(4) if m==0 else range(3,-1,-1)):
            weights=np.full(n,.18,dtype=float)+perturb*rng.standard_normal(n)
            g=dense_green_matrix(maps[j],weights)
            gamma=np.linalg.norm(g,2)
            delta=graph_symmetry_delta(maps[j],weights,tau)
            M+=g/4
            norm_bound+=gamma/4
            b+=gamma**2*delta/4
            actual_deltas.append(delta)
        layers.append(M);bounds.append(norm_bound);comm_bounds.append(b)
    T=layers[1]@layers[0]
    commT=T[:,tau]-T[tau,:]
    actual=float(np.linalg.norm(commT,2))
    budget=float(comm_bounds[1]*bounds[0]+bounds[1]*comm_bounds[0])
    U=normalized_dft(s)
    error=float(np.linalg.norm(U-T,2))
    required=max(0.0,1.0-budget/2)
    assert actual<=budget+1.e-9
    assert error+1.e-9>=required
    return {'s':s,'N':n,'perturb':perturb,'max_delta':max(actual_deltas),
            'computed_commutator_norm':actual,'upper_commutator_budget':budget,
            'actual_operator_error':error,'necessary_operator_error':required,
            'resolvents':8,'layers':2}


def complex_commutator_spectrum(s:int,axis:str)->dict:
    U=normalized_dft(s)
    tau=half_translation(s,axis)
    C=commutator_from_permutation(U,tau)
    sv=np.linalg.svd(C,compute_uv=False)
    expected=([0.0]*((s*s)//2)+[2.0]*((s*s)//2) if axis=='x'
              else [math.sqrt(2-math.sqrt(2))]*((s*s)//2)+
                   [math.sqrt(2+math.sqrt(2))]*((s*s)//2))
    err=float(np.max(np.abs(np.sort(sv)-np.sort(expected))))
    assert err<5e-10
    return {'s':s,'N':s*s,'axis':axis,'max_singular':float(sv[0]),
            'min_singular':float(sv[-1]),'max_spectrum_error':err,
            'normalized_frobenius':float(np.linalg.norm(C)/s)}

if __name__=='__main__':
    import json
    for s in (2,4,8,16):
        print(json.dumps([modular_commutator_certificate(s,axis) for axis in ('x','y','xy')]))


def rank_mod(A:np.ndarray,p:int=PRIME)->int:
    """Exact modular Gaussian elimination; vectorized row updates."""
    M=np.array(A,dtype=np.int64,copy=True)%p
    n,m=M.shape
    row=0
    for col in range(m):
        choices=np.flatnonzero(M[row:,col])
        if not len(choices):continue
        k=row+int(choices[0])
        if k!=row:M[[row,k]]=M[[k,row]]
        M[row,col:]=M[row,col:]*pow(int(M[row,col]),-1,p)%p
        if row+1<n:
            factor=M[row+1:,col].copy()
            M[row+1:,col:]=(M[row+1:,col:]-factor[:,None]*M[None,row,col:])%p
        row+=1
        if row>=n:break
    return row


def green_matrix_mod(pi:Sequence[int],weights:Sequence[int],p:int=PRIME)->np.ndarray:
    n=len(pi);result=np.zeros((n,n),dtype=np.int64)
    for j in range(n):
        vec=[0]*n;vec[j]=1
        result[:,j]=green_apply(pi,weights,vec,p)
    return result


def mixed_matrix_mod(s:int,modifications:dict[tuple[int,int,int],int]|None=None,p:int=PRIME)->np.ndarray:
    """Two-layer mixed-axis 4+4 Green product, with changed individual weights.
    modifications[(stage,graph_index,vertex_index)] = field weight.
    """
    n=s*s; maps=margulis_maps(s); changes=modifications or {}
    layers=[];quarter=pow(4,-1,p)
    for stage in (0,1):
        L=np.zeros((n,n),dtype=np.int64)
        for j in range(4):
            w=[2]*n
            for (m,jj,i),a in changes.items():
                if m==stage and jj==j:w[i]=a%p
            g=green_matrix_mod(maps[j],w,p)
            L=(L+g)%p
        layers.append(L*quarter%p)
    return modular_matmul(layers[1],layers[0],p)


def finite_rank_defect_audit(s:int,changes:dict[tuple[int,int,int],int]|None=None,p:int=PRIME,axis:str='x')->dict:
    n=s*s
    changes=changes or {}
    T0=mixed_matrix_mod(s,p=p)
    T=mixed_matrix_mod(s,modifications=changes,p=p)
    tau=half_translation(s,axis)
    assert not np.any((T0[:,tau]-T0[tau,:])%p)
    diff=(T-T0)%p
    r=rank_mod(diff,p)
    assert r<=len(changes)
    U=modular_dft(s,p)
    C=(U[:,tau]-U[tau,:])%p
    rFourier=rank_mod(C,p)
    assert rFourier==(n//2 if axis=='x' else n)
    defect=(T[:,tau]-T[tau,:])%p
    defect_rank=rank_mod(defect,p)
    assert defect_rank<=2*r
    remaining=(C-defect)%p
    rRemaining=rank_mod(remaining,p)
    assert rRemaining>=rFourier-2*r
    return dict(s=s,N=n,axis=axis,changes=len(changes),rank_difference=r,
                commutator_rank=defect_rank,Fourier_commutator_rank=rFourier,
                residual_commutator_rank=rRemaining,lower_rank_bound=max(0,n//2-2*len(changes)))


def group_twirl(s:int)->dict:
    U=normalized_dft(s)
    permutations=[half_translation(s,a) for a in ('x','y','xy')]
    proj=(U+sum(U[np.ix_(q,q)] for q in permutations))/4
    resid=U-proj
    frob=float(np.linalg.norm(resid)/np.linalg.norm(U))
    proj_norm=float(np.linalg.norm(proj)/np.linalg.norm(U))
    orth=max(float(abs(np.vdot(U,U[np.ix_(q,q)]))) for q in permutations)
    assert abs(frob-math.sqrt(3)/2)<1e-9
    assert abs(proj_norm-.5)<1e-9
    assert orth<5e-9*len(U)
    return dict(s=s,N=s*s,relative_min_frobenius=frob,
                relative_projection_norm=proj_norm,max_nontrivial_orbit_inner_product=orth)
