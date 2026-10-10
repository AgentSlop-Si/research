#!/usr/bin/env python3
"""Self-contained exact certificate for four-stage FFT diagonal-rigidity.

No dependency on previous project's code. Only numpy for accelerated exact
integer modular elimination; no floating point and no approximation.

Run: python verify_rank_rigidity.py
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
N=256
K=8
PRIMES=(12289,65537)


def parity(x,mask):
    return (int(x)&int(mask)).bit_count()&1


def affine(cols):
    n=1<<len(cols)
    p=[]
    for x in range(n):
        y=0
        for j,column in enumerate(cols):
            if (x>>j)&1:y^=int(column)
        p.append(y)
    assert sorted(p)==list(range(n))
    return p


def transport(mask,permutation):
    # The next stage's coordinate i comes from previous output perm[i].
    assert permutation[0]==0
    nextmask=0
    for j in range(K):
        if parity(permutation[1<<j],mask):nextmask|=1<<j
    assert nextmask!=0
    assert all(parity(i,nextmask)==parity(permutation[i],mask) for i in range(N))
    return nextmask


def boundary(mask):
    return sum(parity(j,mask)!=parity(j+1,mask) for j in range(N-1))


def root(N,p):
    assert (p-1)%N==0
    for gen in range(2,p):
        z=pow(gen,(p-1)//N,p)
        if pow(z,N,p)==1 and pow(z,N//2,p)!=1:
            return z
    raise AssertionError('no primitive N-th root')


def fourier_matrix(p):
    z=root(N,p)
    pw=np.array([pow(z,i,p) for i in range(N)],dtype=np.int64)
    i=np.arange(N,dtype=np.int64)
    return pw[(i[:,None]*i[None,:])%N],z


def determinant_mod(M,p):
    """Exact modular determinant with integer NumPy operations."""
    A=np.array(M,dtype=np.int64,copy=True)%p
    n=A.shape[0]
    assert A.shape==(n,n)
    value=1
    for j in range(n):
        candidates=np.flatnonzero(A[j:,j])
        if not len(candidates):return 0
        pivot_row=j+int(candidates[0])
        if pivot_row!=j:
            A[[j,pivot_row],:]=A[[pivot_row,j],:]
            value=(-value)%p
        pivot=int(A[j,j]);value=value*pivot%p
        if j+1<n:
            inv=pow(pivot,-1,p)
            factors=(A[j+1:,j]*inv)%p
            A[j+1:,j+1:]=(A[j+1:,j+1:]-factors[:,None]*A[j,j+1:])%p
            A[j+1:,j]=0
    return int(value)


def stage(n,p,rng):
    a,b,c,e,d=[rng.integers(0,p,size=n,dtype=np.int64) for _ in range(5)]
    i=np.arange(n)[:,None];j=np.arange(n)[None,:]
    return np.where(i>j,a[:,None]*b[None,:],np.where(i<j,c[:,None]*e[None,:],d[:,None]))%p


def rank_mod(A,p):
    A=np.array(A,dtype=np.int64,copy=True)%p
    rows,cols=A.shape;r=0
    for j in range(cols):
        if r>=rows:break
        q=np.flatnonzero(A[r:,j])
        if not len(q):continue
        piv=r+int(q[0]);A[[r,piv]]=A[[piv,r]]
        if r+1<rows:
            factors=A[r+1:,j]*pow(int(A[r,j]),-1,p)%p
            A[r+1:,j+1:]=(A[r+1:,j+1:]-factors[:,None]*A[r,j+1:])%p
            A[r+1:,j]=0
        r+=1
    return r


def test_structural_bound():
    """Independent small-model check for changing partitions and rank-zero stages."""
    p=12289;n=16;k=4
    rng=np.random.default_rng(8412)
    perms=[]
    for s in range(3):
        while True:
            cols=list(rng.choice(n,size=k,replace=False))
            z=[]
            for x in range(n):
                y=0
                for j,c in enumerate(cols):
                    if x>>j&1:y^=int(c)
                z.append(y)
            if sorted(z)==list(range(n)):break
        perms.append(np.array(z,dtype=np.int64))
    for Jsize in range(1,5):
        for J in itertools.combinations(range(4),Jsize):
            stages=[]
            for s in range(4):
                A=stage(n,p,rng)
                if s in J:A=np.diag(np.diag(A))
                stages.append(A)
            M=stages[0]
            for s in range(1,4):
                M=(stages[s]@M[perms[s-1],:])%p
            for mask in range(1,n):
                group=set(i for i in range(n) if not parity(i,mask))
                path=[]
                for s in range(4):
                    path.append(group)
                    if s<3:group={i for i,j in enumerate(perms[s]) if j in group}
                cut=sum(sum((i in path[s])!=(i+1 in path[s]) for i in range(n-1))
                        for s in range(4) if s not in J)
                R=[i for i in range(n) if i not in path[-1]]
                C=[i for i in range(n) if i in path[0]]
                assert rank_mod(M[np.ix_(R,C)],p)<=cut,(J,mask,cut)
    return 15*15


def main():
    layout=json.loads((HERE/'AFFINE_LAYOUT.json').read_text())
    assert layout['k']==K
    perms=[affine(columns) for columns in layout['affine_shuffle_columns']]
    allpaths=[]
    for mask in range(1,N):
        path=[mask]
        for pi in perms:path.append(transport(path[-1],pi))
        borders=[boundary(x) for x in path]
        # Known prime-power Fourier parity-rank formula (also independently
        # certified for each displayed witness by 128x128 determinants below).
        rank=N//4 if (path[0].bit_length()-1)+(path[-1].bit_length()-1)<=K-2 else N//2
        allpaths.append((mask,path,borders,rank))

    certificates=[]
    for t in range(1,5):
        for J in itertools.combinations(range(4),t):
            remaining=[i for i in range(4) if i not in J]
            # Avoid comparing lists in a tie; deterministic mask tie-breaker.
            deficit,mask,path,borders,rank=max(
                [(rank-sum(borders[i] for i in remaining),-mask,path,borders,rank)
                 for mask,path,borders,rank in allpaths],key=lambda z:(z[0],z[1]))
            mask=-mask
            C=[j for j in range(N) if parity(j,path[0])==0]
            R=[j for j in range(N) if parity(j,path[-1])==1]
            assert len(R)==len(C)==128 and rank==128
            item={'replaced_stages':[int(j+1) for j in J],
                  'rank_correction_lower_bound':int(deficit),
                  'input_mask':int(mask),
                  'transported_masks':[int(x) for x in path],
                  'stage_boundary_counts':[int(x) for x in borders],
                  'remaining_stage_capacity':int(rank-deficit),
                  'exact_Fourier_rank':128,
                  'rows':R, 'cols':C, 'determinants_mod_p':{}}
            certificates.append(item)
    for p in PRIMES:
        F,w=fourier_matrix(p)
        print(f'prime={p}, omega={w}',flush=True)
        for case in certificates:
            det=determinant_mod(F[np.ix_(case['rows'],case['cols'])],p)
            assert det!=0,(p,case['replaced_stages'])
            case['determinants_mod_p'][str(p)]=det
    assert len(certificates)==15
    lookup={tuple(x['replaced_stages']):x['rank_correction_lower_bound'] for x in certificates}
    assert [lookup[(i,)] for i in range(1,5)]==[38,44,69,46]
    assert lookup[(1,2)]==119 and lookup[(1,4)]==112
    assert lookup[(1,2)]+lookup[(3,)]+lookup[(4,)]==234
    sanity=test_structural_bound()
    result={'architecture':'F256 = S4 P3 S3 P2 S2 P1 S1; stage QS order <=1',
            'interpretation':'Every subset J forces sum(rank(Sj-Dj) for j in J) >= lower bound',
            'primes':list(PRIMES),'number_of_subsets':len(certificates),
            'nonzero_modular_determinants':2*len(certificates),
            'small_model_structural_checks':sanity,
            'total_diagonal_correction_rank_lower_bound':234,
            'certificates':certificates}
    (HERE/'EXACT_CERTIFICATES.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 15 exact inequalities; 30 nonzero 128x128 determinants;',
          f'{sanity} small random-stage rank checks; total lower bound 234',flush=True)
    return result

if __name__=='__main__':main()
