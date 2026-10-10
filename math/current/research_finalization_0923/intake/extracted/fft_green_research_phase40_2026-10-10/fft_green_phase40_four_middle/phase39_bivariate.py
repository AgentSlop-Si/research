"""Phase 39: exact two-parameter, freely masked Fourier/Green synthesis audit.

Circuit: F = A diag(u) P1 (G2 + lambda G3 + mu G6) P2 diag(v) C.
A and C are fixed sums of two cyclic Green inverses, and all seven Green
cycles and scalar couplings are fixed except lambda and mu.  The two masks
and both intermediate permutations are completely free.

The degree-3 four-minor Macaulay certificate is sufficient to exclude every
complex (lambda,mu) when it has rank 10. A complementary degree-4,
three-minor certificate has rank 15. These are tests of the FIXED family,
not an FFT complexity bound. Exact arithmetic is modulo valid split primes.
"""
from __future__ import annotations
import itertools, random, json
from pathlib import Path
import numpy as np
import phase38_joint_masks as ph38
import phase37_curvature as g

PRIMES = ph38.PRIMES
MON2 = ((2,0,0),(1,1,0),(1,0,1),(0,2,0),(0,1,1),(0,0,2))
MON1 = ((1,0,0),(0,1,0),(0,0,1))
MON3 = tuple((i,j,3-i-j) for i in range(3,-1,-1) for j in range(3-i,-1,-1))
MON4 = tuple((i,j,4-i-j) for i in range(4,-1,-1) for j in range(4-i,-1,-1))
PATH = ((0,1),(0,2),(1,3))
FOUR = ((0,1),(0,2),(0,3),(1,2))


def build(n:int, p:int=998244353, primitive:int=3):
    """Use Phase 38's unchanged A,C,T, add a seventh independently ordered Green."""
    assert n >= 4 and n&(n-1)==0 and (p-1)%n==0
    inst=ph38.build(n,p,primitive)
    g.set_field(p,primitive)
    rng=random.Random(39039+n)
    used={tuple(c) for c in inst['cycles']}
    if n==4:
        # Only (n-1)!=6 Hamiltonian cycle orders with fixed origin 0.
        # A seventh truly distinct cycle is impossible at this boundary.
        extra_cycle=inst['cycles'][0][:]
    else:
        while True:
            order=list(range(1,n));rng.shuffle(order)
            extra_cycle=[0]+order
            if tuple(extra_cycle) not in used:break
    extra_alpha=g.gaussian(1,3,11)
    inst['B2']=np.array(g.cycle_green(n,extra_cycle,extra_alpha),dtype=np.int64)
    inst['extra_cycle']=extra_cycle
    inst['extra_alpha']=int(extra_alpha)
    return inst


def lin_mul(a,b,p):
    """Product of two ternary linear forms, MON2 coefficient order."""
    return ((a[0]*b[0])%p,(a[0]*b[1]+a[1]*b[0])%p,
            (a[0]*b[2]+a[2]*b[0])%p,(a[1]*b[1])%p,
            (a[1]*b[2]+a[2]*b[1])%p,(a[2]*b[2])%p)


def minor_quad(inst, rows, cols, a, b, target=None):
    """Unanchored two-by-two minor of T ./ B(x), after clearing denominators."""
    p=inst['p'];r0,r1=rows;c0,c1=cols[a],cols[b]
    T=inst['T'] if target is None else target
    Bs=(inst['B0'],inst['B1'],inst['B2'])
    v=lambda r,c:tuple(int(M[r,c]) for M in Bs)
    L=int(T[0,a])*int(T[1,b])%p
    R=int(T[0,b])*int(T[1,a])%p
    x=lin_mul(v(r1,c0),v(r0,c1),p)
    y=lin_mul(v(r1,c1),v(r0,c0),p)
    return tuple((L*s-R*t)%p for s,t in zip(x,y))


def macaulay(inst,rows=(0,1),cols=(0,1,2,3),kind='cubic',target=None):
    """Rows are monomial multiples of exactly three or four cross-ratio quadrics.

    'quartic': 3 PATH quadrics times all 6 quadratics -> 18x15.
    'cubic': 4 FOUR quadrics times 3 linears -> 12x10.
    """
    if kind=='cubic': pairs=FOUR; multiples=MON1;outmons=MON3
    elif kind=='quartic': pairs=PATH;multiples=MON2;outmons=MON4
    else:raise ValueError(kind)
    index={t:i for i,t in enumerate(outmons)}
    out=[]
    for a,b in pairs:
        f=minor_quad(inst,rows,cols,a,b,target=target)
        for m in multiples:
            row=[0]*len(outmons)
            for coeff,x in zip(f,MON2):
                k=index[tuple(xi+mi for xi,mi in zip(x,m))]
                row[k]=coeff
            out.append(row)
    return out


def rank_mod(matrix,p):
    """Independent exact rectangular row echelon rank; no float arithmetic."""
    a=[list(map(int,row)) for row in matrix]
    if not a:return 0
    m=len(a);n=len(a[0]);rank=0
    for col in range(n):
        pivot=next((j for j in range(rank,m) if a[j][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        piv_inv=pow(a[rank][col],p-2,p)
        for j in range(rank+1,m):
            factor=a[j][col]*piv_inv%p
            if factor:
                for k in range(col+1,n):
                    a[j][k]=(a[j][k]-factor*a[rank][k])%p
                a[j][col]=0
        rank+=1
        if rank==n:break
    return rank


def witness(inst,rows=(0,1),cols=(0,1,2,3),target=None):
    p=inst['p']
    return {'degree_3_four_quadrics_rank':rank_mod(macaulay(inst,rows,cols,'cubic',target),p),
            'degree_4_three_quadrics_rank':rank_mod(macaulay(inst,rows,cols,'quartic',target),p)}


def anchored_spurious(inst, rows=(0,1), cols=(0,1,2,3)):
    """Find a nonzero projective point annihilating B(r0,c0),B(r1,c0).

    Cross product of the two coefficient rows is their common kernel. In
    characteristic zero it exists for EVERY ternary pencil, regardless of
    whether any Fourier equivalence exists.
    """
    r0,r1=rows;c0=cols[0];p=inst['p']
    Bs=(inst['B0'],inst['B1'],inst['B2'])
    a=[int(B[r0,c0]) for B in Bs]
    b=[int(B[r1,c0]) for B in Bs]
    z=((a[1]*b[2]-a[2]*b[1])%p,
       (a[2]*b[0]-a[0]*b[2])%p,
       (a[0]*b[1]-a[1]*b[0])%p)
    assert z!=(0,0,0)
    assert sum(x*y for x,y in zip(a,z))%p==0
    assert sum(x*y for x,y in zip(b,z))%p==0
    return z


def plant_positive_control(inst, lam=7,mu=11):
    """Planted valid *middle diagonal equivalence* control.

    This is NOT a fast Fourier decomposition; an artificial dense outer
    mixer could force this target to equal F, hiding the expensive work.
    """
    p=inst['p'];n=inst['n'];rng=random.Random(n+39039)
    rows=list(range(n));cols=list(range(n));rng.shuffle(rows);rng.shuffle(cols)
    left=[rng.randrange(1,p) for _ in range(n)]
    right=[rng.randrange(1,p) for _ in range(n)]
    B=(inst['B0']+lam*inst['B1']+mu*inst['B2'])%p
    selected=B[np.ix_(rows,cols)]
    target=(selected*np.array(left,dtype=np.int64)[:,None])%p
    target=(target*np.array(right,dtype=np.int64)[None,:])%p
    w=witness(inst,rows[:2],cols[:4],target=target)
    assert w['degree_3_four_quadrics_rank']<10
    assert w['degree_4_three_quadrics_rank']<15
    z=(1,lam,mu)
    for aa,bb in itertools.combinations(range(4),2):
        f=minor_quad(inst,rows[:2],cols[:4],aa,bb,target=target)
        assert sum(c*np.prod([pow(x,e,p) for x,e in zip(z,m)]) for c,m in zip(f,MON2))%p==0
    return {'rank3':w['degree_3_four_quadrics_rank'],
            'rank4':w['degree_4_three_quadrics_rank'],
            'planted_lam':lam,'planted_mu':mu,
            'masked_fourier_claim':False}


def middle_apply(inst, y, lam, mu):
    g.set_field(inst['p'],inst['g'])
    cycles=inst['cycles'];alphas=inst['alphas'];p=inst['p']
    z0=g.cycle_green_apply(cycles[2],alphas[2],y)
    z1=g.cycle_green_apply(cycles[3],alphas[3],y)
    z2=g.cycle_green_apply(inst['extra_cycle'],inst['extra_alpha'],y)
    return [(a+lam*b+mu*c)%p for a,b,c in zip(z0,z1,z2)]


def online_apply(inst, vector, lam=7, mu=11, mask1=None, mask2=None,
                 rowperm=None, colperm=None):
    """Apply seven-Green circuit in O(N) field work, excluding mask synthesis.

    A diag(mask1) P1 B(lam,mu) P2 diag(mask2) C.
    Matrices P1, P2 correspond to row- and column-index lists.
    """
    p=inst['p'];n=inst['n'];g.set_field(p,inst['g'])
    cycles=inst['cycles'];alphas=inst['alphas'];wa=(1,g.gaussian(1,1,3));wc=(1,g.gaussian(1,-1,4))
    if mask1 is None:mask1=[pow(g.I,(3*j+1)%4,p) for j in range(n)]
    if mask2 is None:mask2=[pow(g.I,(j*j+j+1)%4,p) for j in range(n)]
    if rowperm is None:rowperm=list(range(n))
    if colperm is None:colperm=list(range(n))
    y=g.linear_combo_solve(cycles[4:6],alphas[4:6],wc,list(map(int,vector)))
    y=[y[j]*mask2[j]%p for j in range(n)]
    permuted=[0]*n
    for j in range(n):permuted[colperm[j]]=y[j]
    y=middle_apply(inst,permuted,lam,mu)
    y=[y[rowperm[j]]*mask1[j]%p for j in range(n)]
    return g.linear_combo_solve(cycles[:2],alphas[:2],wa,y)


def dense_circuit(inst, lam=7,mu=11,mask1=None,mask2=None,
                  rowperm=None,colperm=None):
    p=inst['p'];n=inst['n'];g.set_field(p,inst['g'])
    if mask1 is None:mask1=[pow(g.I,(3*j+1)%4,p) for j in range(n)]
    if mask2 is None:mask2=[pow(g.I,(j*j+j+1)%4,p) for j in range(n)]
    if rowperm is None:rowperm=list(range(n))
    if colperm is None:colperm=list(range(n))
    B=(inst['B0']+lam*inst['B1']+mu*inst['B2'])%p
    B=B[np.ix_(rowperm,colperm)]
    B=(B*np.array(mask1,dtype=np.int64)[:,None])%p
    B=(B*np.array(mask2,dtype=np.int64)[None,:])%p
    return ph38.field_mm(ph38.field_mm(inst['A'],B,p),inst['C'],p)


def weyl_defects_mod(M,p,primitive):
    """Exact FZ=DF and FD=Z^{-1}F defects for the positive-exponent DFT.

    Z e_j = e_(j+1 mod N). Both defects vanish iff M is a scalar DFT
    (for an invertible full-sized intertwiner); test alone is not a
    replacement for proof on all inputs.
    """
    M=np.asarray(M,dtype=np.int64);n=M.shape[0]
    assert M.shape==(n,n) and (p-1)%n==0
    w=pow(primitive,(p-1)//n,p)
    powers=np.array([pow(w,k,p) for k in range(n)],dtype=np.int64)
    first=(np.roll(M,-1,axis=1)-(powers[:,None]*M)%p)%p
    second=((M*powers[None,:])%p-np.roll(M,-1,axis=0))%p
    return (int(np.count_nonzero(first)),int(np.count_nonzero(second)))


def export_instance(inst,path):
    with open(path,'w') as f:
        f.write(f"{inst['n']} {inst['p']}\n")
        for key in ('T','B0','B1','B2'):
            for row in inst[key]:
                f.write(' '.join(str(int(x)) for x in row)+'\n')


def quick_audit(ns=(4,8,16,32,64,128),output=None):
    data=[]
    for p,primitive in PRIMES:
        for n in ns:
            inst=build(n,p,primitive)
            w=witness(inst)
            assert w['degree_3_four_quadrics_rank']==10
            assert w['degree_4_three_quadrics_rank']==15
            x=anchored_spurious(inst)
            planted=plant_positive_control(inst)
            if n<=64:
                vec=[(13*j*j+5*j+1)%p for j in range(n)]
                dense=dense_circuit(inst)
                expected=[sum(int(dense[i,j])*vec[j] for j in range(n))%p for i in range(n)]
                assert online_apply(inst,vec)==expected
            data.append({'N':n,'prime':p,'anchor_rank_defect':True,
                         'certificate':w,'positive_control':planted,
                         'extra_cycle_distinct': n>=8 and tuple(inst['extra_cycle']) not in
                           {tuple(c) for c in inst['cycles']}})
            print('N',n,'p',p,'cert',w,'positive',planted,flush=True)
    if output is not None:Path(output).write_text(json.dumps({'phase':39,'audits':data},indent=2)+'\n')
    return data

if __name__=='__main__':quick_audit(output='phase39_audit.json')
