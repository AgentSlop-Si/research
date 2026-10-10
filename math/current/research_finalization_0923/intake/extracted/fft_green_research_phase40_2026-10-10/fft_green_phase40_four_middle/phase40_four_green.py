"""Phase 40: four-generator Green pencil and non-star projective certificates.

All arithmetic in split finite fields. This file is research code; it does
not prove a faster DFT.
"""
from __future__ import annotations
import itertools, random, sys, json
from pathlib import Path
import numpy as np

PREVIOUS = Path(__file__).resolve().parent
if str(PREVIOUS) not in sys.path: sys.path.insert(0,str(PREVIOUS))
import phase39_bivariate as old
import phase37_curvature as greens

PRIMES = old.PRIMES
CYCLE5 = ((0,1),(1,2),(2,3),(3,4),(4,0))
NONSTAR5 = CYCLE5

def monomials(d: int, variables: int=4):
    if variables==1: return ((d,),)
    return tuple((k,)+other for k in range(d,-1,-1)
                 for other in monomials(d-k,variables-1))

MON2 = monomials(2)
MON3 = monomials(3)
MON4 = monomials(4)
MON1 = monomials(1)


def build(n:int, p:int=998244353, primitive:int=3):
    """Keep three Phase39 middle Green matrices and add independent 4th."""
    if n<8: raise ValueError('Need 5 witness columns')
    inst=old.build(n,p,primitive)
    greens.set_field(p,primitive)
    rng=random.Random(40040+n)
    used={tuple(x) for x in inst['cycles']}|{tuple(inst['extra_cycle'])}
    for _ in range(100000):
        order=list(range(1,n));rng.shuffle(order)
        cy=[0]+order
        if tuple(cy) not in used: break
    else: raise ValueError('No distinct Hamiltonian cycle found')
    # Valid nonzero denominator for all audited sizes; check explicitly.
    alpha=greens.gaussian(2,3,13)
    inst['B3']=np.array(greens.cycle_green(n,cy,alpha),dtype=np.int64)
    inst['fourth_cycle']=cy;inst['fourth_alpha']=int(alpha)
    return inst


def quad_product(a,b,p):
    out={}
    for i,x in enumerate(MON1):
        for j,y in enumerate(MON1):
            exp=tuple(u+v for u,v in zip(x,y))
            out[exp]=(out.get(exp,0)+int(a[i])*int(b[j]))%p
    return [out.get(m,0) for m in MON2]


def minor_quad(inst, rows, cols, a, b,target=None):
    p=inst['p'];r0,r1=rows;c0,c1=cols[a],cols[b]
    T=inst['T'] if target is None else target
    Bs=tuple(inst[f'B{i}'] for i in range(4))
    vec=lambda r,c:tuple(int(B[r,c]) for B in Bs)
    L=int(T[0,a])*int(T[1,b])%p
    R=int(T[0,b])*int(T[1,a])%p
    x=quad_product(vec(r1,c0),vec(r0,c1),p)
    y=quad_product(vec(r1,c1),vec(r0,c0),p)
    return tuple((L*s-R*t)%p for s,t in zip(x,y))


def macaulay(inst, rows=(0,1), cols=(0,1,2,3,4), kind='cycle_cubic', target=None, pairs=None):
    """Five cycle quadrics x four linears -> 20x20 square cubic matrix."""
    assert len(rows)==2 and len(cols)==5
    if kind=='cycle_cubic': default_pairs=CYCLE5; multiples=MON1; outs=MON3
    elif kind=='cycle_quartic': default_pairs=CYCLE5; multiples=MON2; outs=MON4
    elif kind=='all_cubic': default_pairs=tuple(itertools.combinations(range(5),2));multiples=MON1;outs=MON3
    else:raise ValueError(kind)
    pairs=default_pairs if pairs is None else tuple(pairs)
    columns={e:i for i,e in enumerate(outs)}
    out=[]
    for a,b in pairs:
        f=minor_quad(inst,rows,cols,a,b,target)
        for m in multiples:
            row=[0]*len(outs)
            for c,e in zip(f,MON2):
                dest=tuple(x+y for x,y in zip(m,e))
                row[columns[dest]]=c
            out.append(row)
    return out


def witness(inst,rows=(0,1),cols=(0,1,2,3,4),target=None):
    p=inst['p']
    return dict(cycle_cubic_rank=old.rank_mod(macaulay(inst,rows,cols,'cycle_cubic',target),p),
                all_cubic_rank=old.rank_mod(macaulay(inst,rows,cols,'all_cubic',target),p))


def plant(inst,params=(1,7,11,17),seed=42):
    """Planted projective equivalence: must NOT be excluded by Macaulay gate."""
    n,p=inst['n'],inst['p'];rng=random.Random(seed+n+p)
    rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
    left=[rng.randrange(1,p) for _ in range(n)];right=[rng.randrange(1,p) for _ in range(n)]
    Bs=tuple(inst[f'B{i}'] for i in range(4))
    B=sum(int(t)*matrix for t,matrix in zip(params,Bs))%p
    target=(B[np.ix_(rp,cp)]*np.asarray(left,dtype=np.int64)[:,None])%p
    target=(target*np.asarray(right,dtype=np.int64)[None,:])%p
    # Avoid numpy overflow: small coefficient sum evaluated modulo p each step above, 
    # p<2.1e9 and 17 matrix values may overflow int64 before modulo: repair if necessary.
    return witness(inst, rp[:2],cp[:5],target=target)

if __name__=='__main__':
    for p,g in PRIMES:
        for n in (8,16,32):
            inst=build(n,p,g)
            print('PRIME N',p,n,'witness',witness(inst),'plant',plant(inst),flush=True)


def export_instance(inst,path,target=None):
    """Export 5 matrices in the exact native-verifier format."""
    n,p=inst['n'],inst['p']
    with open(path,'w') as f:
        f.write(f'{n} {p}\n')
        for matrix in (inst['T'] if target is None else target,inst['B0'],inst['B1'],inst['B2'],inst['B3']):
            for row in matrix:f.write(' '.join(str(int(v)) for v in row)+'\n')


def online_apply(inst,vector,coeffs=(1,7,11,17), mask1=None,mask2=None,
                 rowperm=None,colperm=None):
    """Eight-Green executor, O(N) field ops for specified parameters, no synthesis."""
    n,p=inst['n'],inst['p']
    greens.set_field(p,inst['g'])
    if mask1 is None:mask1=[pow(greens.I,(j*3+1)%4,p) for j in range(n)]
    if mask2 is None:mask2=[pow(greens.I,(j*j+1)%4,p) for j in range(n)]
    if rowperm is None:rowperm=list(range(n))
    if colperm is None:colperm=list(range(n))
    wc=(1,greens.gaussian(1,-1,4))
    wa=(1,greens.gaussian(1,1,3))
    y=greens.linear_combo_solve(inst['cycles'][4:6],inst['alphas'][4:6],wc,list(map(int,vector)))
    y=[y[j]*mask2[j]%p for j in range(n)]
    permuted=[0]*n
    for j in range(n):permuted[colperm[j]]=y[j]
    cycles=(inst['cycles'][2],inst['cycles'][3],inst['extra_cycle'],inst['fourth_cycle'])
    alphas=(inst['alphas'][2],inst['alphas'][3],inst['extra_alpha'],inst['fourth_alpha'])
    middle=[0]*n
    for c,a,t in zip(cycles,alphas,coeffs):
        q=greens.cycle_green_apply(c,a,permuted)
        middle=[(v+int(t)*u)%p for v,u in zip(middle,q)]
    z=[middle[rowperm[j]]*mask1[j]%p for j in range(n)]
    return greens.linear_combo_solve(inst['cycles'][:2],inst['alphas'][:2],wa,z)


def dense_apply(inst,vector,coeffs=(1,7,11,17),mask1=None,mask2=None,
                rowperm=None,colperm=None):
    n,p=inst['n'],inst['p']
    greens.set_field(p,inst['g'])
    if mask1 is None:mask1=[pow(greens.I,(j*3+1)%4,p) for j in range(n)]
    if mask2 is None:mask2=[pow(greens.I,(j*j+1)%4,p) for j in range(n)]
    if rowperm is None:rowperm=list(range(n))
    if colperm is None:colperm=list(range(n))
    B=sum((int(t)*inst[f'B{j}'] for j,t in enumerate(coeffs)))%p
    B=B[np.ix_(rowperm,colperm)]
    B=(B*np.asarray(mask1,dtype=np.int64)[:,None])%p
    B=(B*np.asarray(mask2,dtype=np.int64)[None,:])%p
    D=old.ph38.field_mm(old.ph38.field_mm(inst['A'],B,p),inst['C'],p)
    return [sum(int(D[i,j])*int(vector[j]) for j in range(n))%p for i in range(n)]
