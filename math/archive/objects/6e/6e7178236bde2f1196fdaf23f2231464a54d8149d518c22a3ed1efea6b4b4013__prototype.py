from random import Random
from math import isqrt

def prime(n):
    if n < 2: return False
    for i in range(2,isqrt(n)+1):
        if n%i==0: return False
    return True

def field_for_order(n):
    m=2
    while True:
        q=m*n+1
        if prime(q):
            for a in range(2,min(100,q)):
                root=pow(a,m,q)
                if root!=1 and pow(root,n,q)==1:
                    return q,root
        m+=1

def inv_matrix_green(cycle,weights,q):
    n=len(cycle)
    W=1
    for w in weights:W=W*w%q
    if W==1:return None
    den=pow((1-W)%q,-1,q)
    g=[[0]*n for _ in range(n)]
    for i in range(n):
        k=i;prod=den
        for j in range(n):
            g[i][k]=prod
            prod=prod*weights[k]%q
            k=cycle[k]
        assert k==i
    return g

def rank_mod(a,q):
    a=[row[:] for row in a]
    if not a:return 0
    n,m=len(a),len(a[0]); pivot=0
    for col in range(m):
        i=next((i for i in range(pivot,n) if a[i][col]%q),None)
        if i is None:continue
        a[pivot],a[i]=a[i],a[pivot]
        v=pow(a[pivot][col],-1,q)
        for c in range(col,m):a[pivot][c]=a[pivot][c]*v%q
        for k in range(pivot+1,n):
            f=a[k][col]
            if f:
                for c in range(col,m):a[k][c]=(a[k][c]-f*a[pivot][c])%q
        pivot+=1
        if pivot==n:break
    return pivot

def separate(rows,cols,row_position,col_position):
    # Select at least floor(half) rows and columns with disjoint ordered locations
    nr=len(rows)//2;nc=len(cols)//2
    assert nr>=1 and nc>=1
    ro=sorted(rows,key=lambda r:row_position[r]);co=sorted(cols,key=lambda c:col_position[c])
    rl=ro[:nr];rh=ro[-nr:];cl=co[:nc];ch=co[-nc:]
    if row_position[rl[-1]] < col_position[ch[0]]:
        return rl,ch
    assert col_position[cl[-1]] < row_position[rh[0]]
    return rh,cl

def random_case(n,Q,seed):
    rng=Random(seed); q,w=field_for_order(n)
    components=[]
    R=list(range(n));C=list(range(n))
    for u in range(Q):
        order=list(range(n));rng.shuffle(order)
        cycle=[0]*n
        for j in range(n):cycle[order[j]]=order[(j+1)%n]
        weights=[rng.randrange(q) for _ in range(n)]
        G=inv_matrix_green(cycle,weights,q)
        while G is None:
            weights=[rng.randrange(q) for _ in range(n)]
            G=inv_matrix_green(cycle,weights,q)
        rowmap=list(range(n));colmap=list(range(n));rng.shuffle(rowmap);rng.shuffle(colmap)
        pos={c:j for j,c in enumerate(order)}
        rpos={i:pos[rowmap[i]] for i in range(n)}
        cpos={i:pos[colmap[i]] for i in range(n)}
        components.append((G,rowmap,colmap,rpos,cpos,weights,cycle))
        R,C=separate(R,C,rpos,cpos)
        assert max(rpos[r] for r in R)<min(cpos[c] for c in C) or max(cpos[c] for c in C)<min(rpos[r] for r in R)
    m=len(R);assert m==n//(2**Q)
    cumulative=[[0]*m for _ in range(m)]
    for u,(G,rowmap,colmap,rpos,cpos,weights,cycle) in enumerate(components):
        block=[[G[rowmap[r]][colmap[c]] for c in C] for r in R]
        local_rank=rank_mod(block,q)
        assert local_rank<=1,(n,Q,seed,u,local_rank,R,C)
        for r in range(m):
            for c in range(m): cumulative[r][c]=(cumulative[r][c]+block[r][c])%q
    sumrank=rank_mod(cumulative,q)
    assert sumrank<=Q
    fourier=[[pow(w,(i*j)%n,q) for j in C] for i in R]
    frank=rank_mod(fourier,q)
    return {'n':n,'Q':Q,'m':m,'field':q,'root':w,'sumrank':sumrank,'fourier_rank':frank,'contradiction':m>Q and frank==m}

if __name__=='__main__':
    for n,Q in [(13,2),(17,2),(41,3),(83,4),(127,5)]:
        from time import perf_counter
        t=perf_counter();v=[random_case(n,Q,seed) for seed in range(10)]
        print(v[0], 'passes',sum(x['contradiction'] for x in v), 'seconds',round(perf_counter()-t,3))
