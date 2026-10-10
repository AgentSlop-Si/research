"""Exact N=4 Fourier factorization through two mixed-axis four-Green layers.

A FINITE POSITIVE CONTROL ONLY. This does not yield a faster all-length FFT.
Four permutations are the s=2 Margulis maps: id, x-flip, id, y-flip.
"""
from __future__ import annotations
import sympy as sp


def small_F4_rook_factors():
    z=-sp.I
    F=sp.Matrix([[z**(i*j) for j in range(4)]for i in range(4)])
    V=sp.zeros(4)
    for j in range(4):
        group=2*(j//2)
        forbidden=3-j
        V[group,j]=F[forbidden,group+1]
        V[group+1,j]=-F[forbidden,group]
    X=V.inv();Y=F*V
    rook=lambda M:all(M[i,j]==0 for i in range(4) for j in range(4)
                      if i//2!=j//2 and i%2!=j%2)
    assert rook(X) and rook(Y) and sp.simplify(Y*X-F)==sp.zeros(4)
    return F,X,Y


def two_cycle_solver(a,b):
    """Given off-diagonals a,b, create two-cycle Green weights and common diag t."""
    disc=sp.simplify(1+4*a*b)
    t=(1+sp.sqrt(disc))/2
    if sp.simplify(t)==0:t=(1-sp.sqrt(disc))/2
    assert sp.simplify(t)!=0
    wa=sp.simplify(a/t);wb=sp.simplify(b/t)
    assert sp.simplify((1-wa*wb)*t-1)==0
    return wa,wb,t


def green_stage_for_rook(M):
    """Returns the four invertible weighted permutation matrices' weights,
    such that the exact SUM of their resolvents equals an arbitrary given
    4x4 rook-supported matrix M, over C. All sqrt branches are explicit.
    """
    pi_x=[2,3,0,1]
    pi_y=[1,0,3,2]
    I=sp.eye(4)
    def flip_green(pi):
        P=sp.zeros(4);done=set()
        for i in range(4):
            if i in done:continue
            j=pi[i]
            if i==j:raise ValueError('flip expected')
            a,b=M[i,j],M[j,i]
            wi,wj,_=two_cycle_solver(a,b)
            P[i,j]=wi;P[j,i]=wj
            done.update((i,j))
        return (I-P).inv(), [P[i,pi[i]] for i in range(4)]
    Gx,wx=flip_green(pi_x)
    Gy,wy=flip_green(pi_y)
    residual=[sp.simplify(M[i,i]-Gx[i,i]-Gy[i,i]) for i in range(4)]
    diag1=[];diag2=[]
    for r in residual:
        d1=sp.Integer(1)
        if sp.simplify(r-d1)==0:d1=sp.Integer(2)
        d2=sp.simplify(r-d1)
        assert sp.simplify(d2)!=0
        diag1.append(d1);diag2.append(d2)
    Gid1=sp.diag(*diag1);Gid2=sp.diag(*diag2)
    wid1=[sp.simplify(1-1/v) for v in diag1]
    wid2=[sp.simplify(1-1/v) for v in diag2]
    residual_matrix=sp.simplify(M-(Gid1+Gx+Gid2+Gy))
    assert residual_matrix==sp.zeros(4)
    return {'weights':[wid1,wx,wid2,wy],
            'resolvents':[Gid1,Gx,Gid2,Gy]}


def exact_F4_green_product():
    F,X,Y=small_F4_rook_factors()
    stage_x=green_stage_for_rook(X)
    stage_y=green_stage_for_rook(Y)
    GX=sum(stage_x['resolvents'],sp.zeros(4))
    GY=sum(stage_y['resolvents'],sp.zeros(4))
    assert sp.simplify(GY*GX-F)==sp.zeros(4)
    return {'F':F,'X':X,'Y':Y,'stage_x':stage_x,'stage_y':stage_y}

if __name__=='__main__':
    r=exact_F4_green_product()
    print('Exact F4 = (G0+Gx+G1+Gy)_output (G0+Gx+G1+Gy)_input: CERTIFIED')
    print('X=',r['X'])
    print('Y=',r['Y'])
