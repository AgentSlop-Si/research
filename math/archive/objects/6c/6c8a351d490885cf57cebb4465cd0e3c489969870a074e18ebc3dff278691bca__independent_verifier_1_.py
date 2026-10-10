"""Independent exact witness verification for full-dimensional FFT scan networks.
Reads *explicit saved integer generators*, independently reconstructs all
Jacobian derivatives by left and right prefix factors, then proves the
recorded 64x64, 256x256, or 1024x1024 minor is nonzero modulo a field prime.
"""
import json,subprocess,tempfile
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent


def mm(a,b,p):return (a @ b)%p


def find_product_and_jacobian(w,p):
    n=w['n'];t=w['t'];perm=w['permutation']
    P=np.eye(n,dtype=np.int64)[perm,:]
    stages=[]
    for pa in w['stages']:
        d=np.array(pa['d'],dtype=np.int64)
        L=np.array(pa['L'],dtype=np.int64).reshape(n)
        V=np.array(pa['V'],dtype=np.int64).reshape(n)
        U=np.array(pa['U'],dtype=np.int64).reshape(n)
        W=np.array(pa['W'],dtype=np.int64).reshape(n)
        S=(np.tril(np.outer(L,V),-1)+np.triu(np.outer(U,W),1)+np.diag(d))%p
        stages.append(S)
    pref=[None]*t
    pref[0]=stages[0]
    for k in range(1,t):pref[k]=mm(mm(stages[k],P,p),pref[k-1],p)
    right=[np.eye(n,dtype=np.int64)]
    for k in range(1,t):right.append(mm(P,pref[k-1],p))
    left=[None]*t;left[-1]=np.eye(n,dtype=np.int64)
    for k in reversed(range(t-1)):left[k]=mm(mm(left[k+1],stages[k+1],p),P,p)
    columns=[]
    for k,pa in enumerate(w['stages']):
        L=np.array(pa['L'],dtype=np.int64).reshape(n)
        V=np.array(pa['V'],dtype=np.int64).reshape(n)
        U=np.array(pa['U'],dtype=np.int64).reshape(n)
        W=np.array(pa['W'],dtype=np.int64).reshape(n)
        for term in ['d','L','V','U','W']:
            for i in range(n):
                d=np.zeros((n,n),dtype=np.int64)
                if term=='d':d[i,i]=1
                elif term=='L':d[i,:i]=V[:i]
                elif term=='V':d[i+1:,i]=L[i+1:]
                elif term=='U':d[i,i+1:]=W[i+1:]
                elif term=='W':d[:i,i]=U[:i]
                deriv=mm(mm(left[k],d,p),right[k],p)
                columns.append(deriv.reshape(n*n))
    return pref[-1],np.array(columns,dtype=np.int64).T%p,stages


def external_rankdet(M,p):
    with tempfile.TemporaryDirectory() as tmp:
        matrix=Path(tmp)/'mat.bin'
        M.astype(np.int32).tofile(matrix)
        result=subprocess.check_output([str(HERE/'rankmod'),str(matrix),str(M.shape[0]),str(M.shape[1]),str(p)],text=True)
    d=dict(word.split('=') for word in result.splitlines()[0].split())
    return int(d['rank']),int(d['det'])


def verify_one(n,verbose=True):
    t=n//4+1
    w=json.loads((HERE/f'WITNESS_N{n}_T{t}.json').read_text())
    assert w['n']==n and w['t']==t
    for p in [12289,65537]:
        target=w['certificates_by_field'][str(p)]
        transform,J,stages=find_product_and_jacobian(w,p)
        assert J.shape==(n*n,5*n*t)
        for stage in stages:
            assert external_rankdet(stage,p)[0]==n
        # Validate exact product against direct application on fresh inputs.
        import random
        rng=random.Random(n*70+p)
        P=np.eye(n,dtype=np.int64)[w['permutation'],:]
        for _ in range(12):
            x=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
            direct=mm(transform,x,p)
            y=x
            for k,S in enumerate(stages):
                if k:y=mm(P,y,p)
                y=mm(S,y,p)
            assert np.array_equal(direct,y)
        cols=target['full_rank_minor_column_indices']
        rank,det=external_rankdet(J[:,cols],p)
        assert rank==n*n and det==target['full_rank_minor_det_mod_prime'], (n,p,rank,det)
        if verbose:print(f'PASS n={n} t={t} p={p}, full {n*n}x{n*n} Jacobian minor det={det}',flush=True)
    return True

if __name__=='__main__':
    for n in [8,16,32]:verify_one(n)
