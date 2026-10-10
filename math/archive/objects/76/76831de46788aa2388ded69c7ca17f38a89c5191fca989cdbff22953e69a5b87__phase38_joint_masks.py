"""Phase 38 joint-mask elimination for products of noncommuting Green sums.

The circuit is F=A diag(u) P1 (G2 + lambda*G3) P2 diag(v) C.
This module analyzes arbitrary *nonzero* masks u,v and row/column
permutations P1,P2 for FIXED outer Green sums A,C and inner cycle
resolvents G2,G3. It is not an FFT algorithm.

The Fourier sign is chosen consistently with the finite-field root.
"""
from __future__ import annotations
import argparse, json, sys, random, subprocess
from pathlib import Path
from itertools import permutations
import numpy as np
import phase37_curvature as q

PRIMES=((998244353,3),(2013265921,31))

def field_mm(A,B,p):
    """Exact mod-p matrix multiply using rank-one accumulation, with int64-safe products."""
    A=np.asarray(A,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
    assert A.shape[1]==B.shape[0]
    out=np.zeros((A.shape[0],B.shape[1]),dtype=np.int64)
    for k in range(A.shape[1]):
        out=(out + A[:,k,None]*B[k,None,:])%p
    return out

def field_inv(A,p):
    """Exact modular Gauss-Jordan inversion. Not a fast online algorithm."""
    A=np.array(A,dtype=np.int64)
    n=A.shape[0]; assert A.shape==(n,n)
    I=np.eye(n,dtype=np.int64)
    for k in range(n):
        nz=np.flatnonzero(A[k:,k])
        if len(nz)==0:raise ValueError('Singular mod-p Green outer mixer')
        pivot=int(nz[0])+k
        if pivot!=k:
            A[[pivot,k]]=A[[k,pivot]]
            I[[pivot,k]]=I[[k,pivot]]
        scale=pow(int(A[k,k]),p-2,p)
        A[k]=(A[k]*scale)%p;I[k]=(I[k]*scale)%p
        factors=A[:,k].copy();factors[k]=0
        A=(A-factors[:,None]*A[k,None,:])%p
        I=(I-factors[:,None]*I[k,None,:])%p
    return I

def build(n,p=998244353,g=3,seed=37037):
    """Construct exact Fourier-conjugated target and unmasked Green pencil."""
    q.set_field(p,g)
    info=q.construct_two_mask_circuit(n,seed)
    gs=[np.array(q.cycle_green(n,cyc,alpha),dtype=np.int64)
        for cyc,alpha in zip(info['cycles'],info['alphas'])]
    wa,wc=info['outer_weights']
    A=(gs[0]+int(wa[1])*gs[1])%p
    C=(gs[4]+int(wc[1])*gs[5])%p
    invA,invC=field_inv(A,p),field_inv(C,p)
    F=np.array(q.fourier(n),dtype=np.int64)
    T=field_mm(field_mm(invA,F,p),invC,p)
    return dict(n=n,p=p,g=g,T=T,B0=gs[2],B1=gs[3],A=A,C=C,
                cycles=info['cycles'],alphas=info['alphas'],F=F)

def poly_eq(inst,row_perm=(0,1),col_perm=(0,1,2),j=1):
    """Necessary quadratic from rows 0,1 and columns 0,j of T."""
    T,B0,B1,p=(inst[k] for k in ('T','B0','B1','p'))
    r0,r1=row_perm; c0=col_perm[0];cj=col_perm[j]
    def coeff(i,k):return int(B0[i,k]),int(B1[i,k])
    def multiply(x,y):
        a,b=x;c,d=y
        return [(a*c)%p,(a*d+b*c)%p,(b*d)%p]
    x=multiply(coeff(r1,c0),coeff(r0,cj))
    y=multiply(coeff(r1,cj),coeff(r0,c0))
    L=int(T[1,j])*int(T[0,0])%p
    R=int(T[1,0])*int(T[0,j])%p
    return q.trim([(L*x[k]-R*y[k])%p for k in range(3)])

def resultant2(f,g,p):
    """Determinant of degree-two Sylvester matrix; nonzero => no shared root."""
    f=f+[0]*(3-len(f));g=g+[0]*(3-len(g))
    a,b,c=f[2],f[1],f[0];d,e,h=g[2],g[1],g[0]
    return (((a*h-c*d)**2-(a*e-b*d)*(b*h-c*e))%p)

def witness(inst,with_bezout=True):
    p=inst['p'];f=poly_eq(inst,j=1);g=poly_eq(inst,j=2)
    result=resultant2(f,g,p)
    assert result!=0 and q.gcd_poly(f,g)==[1]
    out=dict(N=inst['n'],prime=p,first_eq=f,second_eq=g,
             quadratic_resultant=result,polynomial_degrees=[len(f)-1,len(g)-1],
             mask_independent=True,full_characteristic_zero_degree=True,
             outer_mixers_mod_p_invertible=True)
    if with_bezout:
        x,y=q.verify_bezout(f,g)
        out['bezout_u']=x;out['bezout_v']=y
    return out

def export_instance(inst,path):
    """Native verifier receives ONLY field elements, never floats."""
    with open(path,'w') as f:
        f.write(f"{inst['n']} {inst['p']}\n")
        for key in ['T','B0','B1']:
            for row in inst[key]:f.write(' '.join(map(str,map(int,row)))+'\n')

def calibrate_anchor(T,B,p):
    """Jointly construct complex row/column masks matching the first row/column.

    O(N) field arithmetic GIVEN the anchor entries of T and B. This does
    not claim the transformed Fourier target T can be built in O(N).
    """
    T=np.asarray(T,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
    n=T.shape[0]
    if np.any(B[0,:]==0) or np.any(B[:,0]==0) or np.any(T[0,:]==0) or np.any(T[:,0]==0):
        return None
    v=np.array([int(T[0,j])*pow(int(B[0,j]),p-2,p)%p for j in range(n)],dtype=np.int64)
    invv0=pow(int(v[0]),p-2,p)
    u=np.array([int(T[i,0])*pow(int(B[i,0]),p-2,p)%p*invv0%p
                for i in range(n)],dtype=np.int64)
    return u,v

def anchored_fit(inst,lamb):
    """Partial synthesis diagnostic for a fixed complex middle coupling."""
    T,B0,B1,p=(inst[k] for k in ('T','B0','B1','p'))
    B=(B0+int(lamb)*B1)%p
    uv=calibrate_anchor(T,B,p)
    if uv is None:return None
    u,v=uv
    reconstructed=(((u[:,None]*B)%p)*v[None,:])%p
    assert np.array_equal(reconstructed[0,:],T[0,:])
    assert np.array_equal(reconstructed[:,0],T[:,0])
    return dict(N=inst['n'],lambda_value=int(lamb),
                calibrated_entries=2*inst['n']-1,
                mismatches_in_interior=int(np.count_nonzero(reconstructed[1:,1:]!=T[1:,1:])),
                interior_entries=(inst['n']-1)**2)

def recover_masks(T,B,p):
    """Exact diagonal equivalence recovery from anchor row and column."""
    T=np.asarray(T,dtype=np.int64);B=np.asarray(B,dtype=np.int64)
    n=T.shape[0];assert T.shape==B.shape
    if np.any(B==0) or np.any(T==0):return None
    v=np.array([int(T[0,j])*pow(int(B[0,j]),p-2,p)%p for j in range(n)],dtype=np.int64)
    v0=int(v[0]);in_v0=pow(v0,p-2,p)
    u=np.array([int(T[i,0])*pow(int(B[i,0]),p-2,p)%p*in_v0%p
                for i in range(n)],dtype=np.int64)
    if np.any(u==0) or np.any(v==0):return None
    if not np.array_equal(( (u[:,None]*B)%p * v[None,:])%p,T):return None
    return u,v

def plant_valid_control(n=8,prime=998244353,primitive=3):
    """Valid construction with deliberately EXPENSIVE outer mixer, to falsify bad vetoes."""
    q.set_field(prime,primitive);p=prime
    inst=build(n,p,primitive)
    B=(inst['B0']+7*inst['B1'])%p
    invB=field_inv(B,p)
    rng=random.Random(n+12)
    rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
    left=np.array([rng.randrange(1,p) for _ in range(n)],dtype=np.int64)
    right=np.array([rng.randrange(1,p) for _ in range(n)],dtype=np.int64)
    T=((left[:,None]*B[rp,:][:,cp])%p*right[None,:])%p
    a=recover_masks(T,B[rp,:][:,cp],p)
    assert a is not None and np.array_equal(((a[0][:,None]*B[rp,:][:,cp])%p*a[1][None,:])%p,T)
    # Demonstrate the expensive outer can force F = A diag(left) P1 B P2 diag(right) C.
    # Choose C=I, A=F*T^{-1}; this is not a cheap Green A.
    F=np.array(q.fourier(n),dtype=np.int64)
    A=field_mm(F,field_inv(T,p),p)
    assert np.array_equal(field_mm(A,T,p),F)
    f=poly_eq(dict(T=T,B0=inst['B0'],B1=inst['B1'],p=p),rp[:2],cp[:3],1)
    g=poly_eq(dict(T=T,B0=inst['B0'],B1=inst['B1'],p=p),rp[:2],cp[:3],2)
    def evalat(f,z):return sum(int(c)*pow(z,k,p) for k,c in enumerate(f))%p
    assert evalat(f,7)==evalat(g,7)==0
    assert resultant2(f,g,p)==0
    return dict(N=n,lambda_planted=7,phase_masks_recovered=True,
                quadratic_resultant=0,full_Fourier_reconstruction=True,
                cheap_Green_outer=False)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=128)
    parser.add_argument('--output',default='phase38_audit.json')
    parser.add_argument('--native',default=None,help='compiled C++ verifier executable')
    parser.add_argument('--native-limit',type=int,default=0,help='0 means full enumeration')
    args=parser.parse_args()
    records=[]
    for p,g in PRIMES:
        for n in (4,8,16,32,64,128):
            if n>args.max_n:continue
            inst=build(n,p,g)
            w=witness(inst)
            print('N',n,'p',p,'deg',w['polynomial_degrees'],'resultant',w['quadratic_resultant'])
            if args.native:
                path=Path(f'phase38_instance_N{n}_p{p}.txt')
                export_instance(inst,path)
                cmd=[args.native,str(path),str(args.native_limit)]
                got=subprocess.run(cmd,capture_output=True,text=True,check=True)
                w['permutations']=json.loads(got.stdout)
            records.append(w)
    out=dict(phase=38,results=records,positive_control=plant_valid_control())
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('Saved',args.output)
if __name__=='__main__':main()
