"""High-precision correction of numerical full-two-row Fourier targets.
Not a rigorous interval existence proof by itself.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
import scipy.linalg as sla
import mpmath as mp
from phase41_unit_holonomy import model
from phase41_actual_target_fit import values_jac


def dense_green(c,w):
    n=len(c)
    H=mp.mpc(1)
    for weight in w:H*=weight
    if abs(1-H)<mp.mpf('1e-50'):raise ValueError('singular')
    G=[[mp.mpc(0) for j in range(n)] for i in range(n)]
    for j in range(n):
        idx=c.index(j);prod=mp.mpc(1)
        G[j][j]=prod/(1-H)
        for _ in range(1,n):
            idx=(idx+1)%n;prod*=w[idx]
            G[c[idx]][j]=prod/(1-H)
    return G


def residual_and_jac(n,z,cycles,edges,chords):
    w=[mp.mpc(1) for _ in range(2*n)]
    for k,idx in enumerate(chords):w[idx]=mp.exp(z[k])
    gs=[dense_green(cycles[s],w[s*n:(s+1)*n]) for s in range(2)]
    M=[[gs[0][i][j]+gs[1][i][j] for j in range(n)] for i in range(n)]
    omega=mp.exp(2*mp.pi*1j/n)
    R=[M[0][j]*M[1][0]/(M[1][j]*M[0][0]) for j in range(1,n)]
    f=[R[j-1]-omega**(-j) for j in range(1,n)]
    J=mp.matrix(n-1,len(chords))
    for k,idx in enumerate(chords):
        e=edges[idx];u,v,s=e.source,e.target,e.cycle
        G=gs[s]
        def term(a,col):return w[idx]*G[a][v]*G[u][col]/M[a][col]
        for j in range(1,n):
            J[j-1,k]=R[j-1]*(term(0,j)+term(1,0)-term(1,j)-term(0,0))
    return f,J,M


def refine(n,prec=100,max_steps=12):
    mp.mp.dps=prec
    rec=json.loads(Path(__file__).with_name(f'phase41_nonunit_target_N{n}.json').read_text())
    cycles,edges,chords=model(n)
    m=len(chords)
    z_double=np.array(rec['theta_logweights'][:m])+1j*np.array(rec['theta_logweights'][m:])
    _,Jreal=values_jac(n,np.array(rec['theta_logweights']),edges,chords)
    Japprox=Jreal[:n-1,:m]+1j*Jreal[n-1:,:m]
    piv=sla.qr(Japprox,pivoting=True,mode='economic')[2][:n-1].tolist()
    z=[mp.mpc(str(z_double[k].real),str(z_double[k].imag)) for k in range(m)]
    steps=[]
    for step in range(max_steps):
        f,J,M=residual_and_jac(n,z,cycles,edges,chords)
        err=max(abs(x) for x in f)
        steps.append(str(err))
        print('n',n,'step',step,'maxres',mp.nstr(err,7),flush=True)
        if err<mp.mpf('1e-'+str(prec-20)):break
        JP=mp.matrix([[J[i,k] for k in piv] for i in range(n-1)])
        delta=mp.lu_solve(JP,mp.matrix([-x for x in f]))
        for i,k in enumerate(piv):z[k]+=delta[i]
    f,J,M=residual_and_jac(n,z,cycles,edges,chords)
    final=max(abs(x) for x in f)
    ret=dict(N=n,precision_digits=prec,corrected_chord_indices=piv,
             residual_scientific=mp.nstr(final,25),steps=steps,
             z_real=[mp.nstr(v.real,prec-4) for v in z],
             z_imag=[mp.nstr(v.imag,prec-4) for v in z])
    Path(__file__).with_name(f'phase41_highprecision_N{n}.json').write_text(json.dumps(ret,indent=2))
    return ret

if __name__=='__main__':
    for n in (8,16):
        out=refine(n,prec=100)
        print('SUCCESS',n,out['residual_scientific'])
