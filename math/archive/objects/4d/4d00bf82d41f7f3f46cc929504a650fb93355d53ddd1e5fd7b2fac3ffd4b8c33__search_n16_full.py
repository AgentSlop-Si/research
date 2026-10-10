#!/usr/bin/env python3
"""Bounded fresh N16 search. Uploaded source is never imported or executed."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
from pathlib import Path
import json, sys, time
import numpy as np
import scipy.linalg as la
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'seed_compatibility_gate'))
from check_n16_outer_gate import cycles, green, PRIME

N, J = 16, 8

def mm(a, b):
    return np.asarray((a.astype(object) @ b.astype(object)) % PRIME, dtype=np.int64)

def modular_rank(a):
    a = a.copy()
    rr, piv, det = 0, [], 1
    for col in range(a.shape[1]):
        nz = np.flatnonzero(a[rr:, col])
        if not len(nz): continue
        row = rr + int(nz[0])
        if row != rr:
            a[[rr,row]] = a[[row,rr]]
            det = -det
        d = int(a[rr,col]); det = det * d % PRIME
        a[rr] = a[rr] * pow(d,-1,PRIME) % PRIME
        if rr+1 < a.shape[0]:
            a[rr+1:] = (a[rr+1:] - a[rr+1:,col,None] * a[rr]) % PRIME
        piv.append(col); rr += 1
        if rr == a.shape[0]: break
    return rr, piv, det % PRIME

def exact_diagnostic():
    rng = np.random.default_rng(16384)
    gs = np.asarray([green(p,j+2) for j,p in enumerate(cycles(N))], dtype=np.int64)
    z = pow(3,(PRIME-1)//N,PRIME)
    b = np.eye(N,dtype=np.int64)
    for off in (0,4):
        for i in range(4):
            for j in range(4): b[off+i,off+j] = pow(z,4*i*j,PRIME)
    results = []
    for kind in ('ones','random_nonzero'):
        a = np.ones((3,N,J),dtype=np.int64) if kind=='ones' else rng.integers(1,1000,(3,N,J),dtype=np.int64)
        hs = [np.asarray(np.einsum('ij,jik->ik',a[l].astype(object),gs.astype(object))%PRIME,dtype=np.int64) for l in range(3)]
        bh1=mm(b,hs[0]); prefix=mm(hs[1],bh1); left=mm(mm(hs[2],hs[1]),b)
        jac=np.zeros((N*N,3*N*J),dtype=np.int64)
        for i in range(N):
            for j in range(J):
                jac[:,i*J+j]=(left[:,i,None]*gs[j,i,None,:]%PRIME).ravel()
                row=mm(gs[j,i,None,:],bh1)[0]
                jac[:,N*J+i*J+j]=(hs[2][:,i,None]*row[None,:]%PRIME).ravel()
                row=mm(gs[j,i,None,:],prefix)[0]
                jac[i*N:(i+1)*N,2*N*J+i*J+j]=row
        tangent1=np.concatenate([a[0].ravel(),(-a[1]).ravel(),np.zeros(N*J,dtype=np.int64)])%PRIME
        tangent2=np.concatenate([np.zeros(N*J,dtype=np.int64),a[1].ravel(),(-a[2]).ravel()])%PRIME
        assert not np.any(mm(jac,tangent1[:,None])) and not np.any(mm(jac,tangent2[:,None]))
        rank,piv,det=modular_rank(jac)
        item={'kind':kind,'rank':rank,'pivot_columns':piv,'pivot_minor_determinant_mod_p':det,
              'parameter_values':a.tolist(),'two_scalar_gauge_tangents_verified':True}
        results.append(item)
        print('exact Jacobian',kind,rank,flush=True)
    (HERE/'EXACT_JACOBIAN_DIAGNOSTIC.json').write_text(json.dumps({'prime':PRIME,'parameter_order':'layer,row,term','results':results},indent=2)+'\n')
    return results

def setup():
    gs=[]
    for j,p in enumerate(cycles(N)):
        t=1/(j+2); g=np.zeros((N,N))
        for col in range(N):
            r=col; c=1/(1-t**N)
            for _ in range(N): g[r,col]=c; r=p[r]; c*=t
        gs.append(g)
    gs=np.asarray(gs)
    u=np.empty((N,J,N)); transforms=np.empty((N,J,J)); cond=[]
    for i in range(N):
        q,r=la.qr(gs[:,i,:].T,mode='economic')
        u[i]=q.T; transforms[i]=r
        cond.append(float(np.linalg.cond(r)))
    z=np.exp(2j*np.pi/N)
    f=z**(np.arange(N)[:,None]*np.arange(N)[None,:])/4
    b=np.eye(N,dtype=complex)
    for off in (0,4): b[off:off+4,off:off+4]=z**(4*np.arange(4)[:,None]*np.arange(4)[None,:])
    return gs,u,transforms,cond,b,f

def evaluate(a,u,b,target,derivative=True):
    hs=np.einsum('lij,ijk->lik',a,u)
    bh1=b@hs[0]; prefix=hs[1]@bh1
    residual=(hs[2]@prefix-target).ravel()
    if not derivative: return residual,hs
    left=hs[2]@hs[1]@b
    jac=np.empty((N*N,3*N*J),dtype=complex)
    for i in range(N):
        jac[:,i*J:(i+1)*J]=np.einsum('r,jc->rcj',left[:,i],u[i]).reshape(N*N,J)
        jac[:,N*J+i*J:N*J+(i+1)*J]=np.einsum('r,jc->rcj',hs[2][:,i],u[i]@bh1).reshape(N*N,J)
        block=np.zeros((N,N,J),dtype=complex)
        block[i]=(u[i]@prefix).T
        jac[:,2*N*J+i*J:2*N*J+(i+1)*J]=block.reshape(N*N,J)
    return residual,jac,hs

def search():
    gs,u,transforms,cond,b,target=setup()
    rng=np.random.default_rng(161616)
    started=time.monotonic(); traces=[]; best=None
    # Fixed bounds: three starts, at most 60 accepted/attempted Newton iterations each,
    # at most 12 backtracking trials, 150 seconds total between iterations.
    for start in range(3):
        a=(rng.normal(size=(3,N,J))+1j*rng.normal(size=(3,N,J)))/np.sqrt(2*J)
        history=[]
        for step in range(60):
            r,jac,hs=evaluate(a,u,b,target)
            norm=float(la.norm(r)); maximum=float(np.max(np.abs(r)))
            history.append({'iteration':step,'residual_l2':norm,'residual_max':maximum})
            if best is None or norm<best[0]: best=(norm,a.copy(),start,step)
            print('search',start,step,norm,flush=True)
            if maximum<2e-12 or time.monotonic()-started>150: break
            delta,_,rank,_=la.lstsq(jac,-r,lapack_driver='gelsy')
            history[-1]['numerical_jacobian_rank']=int(rank)
            accepted=False
            for back in range(12):
                candidate=a+delta.reshape(a.shape)*2.**(-back)
                if la.norm(evaluate(candidate,u,b,target,False)[0]) < norm:
                    a=candidate; accepted=True; history[-1]['step_fraction']=2.**(-back); break
            if not accepted: break
        traces.append({'start':start,'iterations':history})
        if best[0]<1e-11 or time.monotonic()-started>150: break
    norm,a,start,step=best
    r,jac,hs=evaluate(a,u,b,target)
    sv=la.svdvals(jac)
    # Map all searched coordinates back to the original endpoint entries.
    physical=np.empty_like(a)
    for l in range(3):
        for i in range(N): physical[l,i]=la.solve_triangular(transforms[i],a[l,i])
    physical[2]*=4 # Convert the fitted unitary target to the specified F16.
    original_hs=np.einsum('lij,jik->lik',physical,gs)
    original_error=float(np.max(np.abs(original_hs[2]@original_hs[1]@b@original_hs[0]-4*target)))
    np.savez(HERE/'NUMERICAL_CANDIDATE.npz',a=a,u=u,transforms=transforms,physical=physical,
             bank=b,target=target,jacobian=jac)
    result={'status':'NUMERICAL_DISCOVERY_ONLY','search_bounds':{'starts':3,'iterations_per_start':60,'backtracking_trials':12,'wall_seconds':150},
            'elapsed_seconds':time.monotonic()-started,'traces':traces,'best_start':start,'best_iteration':step,
            'orthonormal_chart_residual_l2':norm,'orthonormal_chart_residual_max':float(np.max(np.abs(r))),
            'original_physical_chart_residual_max':original_error,'jacobian_singular_min':float(sv[-1]),
            'jacobian_singular_max':float(sv[0]),'physical_endpoint_min_abs':float(np.min(np.abs(physical))),
            'physical_endpoint_max_abs':float(np.max(np.abs(physical))), 'row_template_condition_numbers':cond,
            'exact_certificate_accepted':False}
    (HERE/'NUMERICAL_SEARCH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('traces','row_template_condition_numbers')}),flush=True)

if __name__=='__main__':
    exact_diagnostic()
    search()
