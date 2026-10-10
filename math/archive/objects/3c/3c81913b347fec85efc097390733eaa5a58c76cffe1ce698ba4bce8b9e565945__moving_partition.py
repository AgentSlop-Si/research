"""Moving-partition Fourier obstruction for arbitrary quasiseparable stage shuffles.

No Fourier-transform implementation is claimed. This file supplies exact
necessary conditions and finite-field checks for proposed scan factorizations.
"""
from __future__ import annotations
from dataclasses import dataclass


def runs_boundary(indices, n):
    members=set(indices)
    return sum((j in members) != (j+1 in members) for j in range(n-1))


def propagate_set(indices, permutation):
    # interstage dependency x_next[j] <- y_old[permutation[j]]
    old=set(indices)
    return [j for j in range(len(permutation)) if permutation[j] in old]


def moving_partition_budget(n, initial_set, permutations, ranks):
    """Upper bound on rank product[complement(final_set), initial_set].

    S_t P_{t-1} ... P_1 S_1; ranks are order bounds for the t factors.
    """
    assert len(ranks)==len(permutations)+1
    group=list(initial_set)
    sets=[];costs=[]
    for i,rank in enumerate(ranks):
        sets.append(group)
        costs.append(rank*runs_boundary(group,n))
        if i<len(permutations):group=propagate_set(group,permutations[i])
    return sum(costs),sets,costs


def bitrev(x,k):
    return int(f'{x:0{k}b}'[::-1],2)


def rotl(x,k):
    return ((x<<1)&((1<<k)-1)) | (x>>(k-1))


def mix_middle(x,k):
    m=k//2
    return x^(((x>>(m-1))&1)<<m)


def transformations(k):
    n=1<<k
    bp=[bitrev(j,k) for j in range(n)]
    rp=[rotl(j,k) for j in range(n)]
    xor=[mix_middle(j,k) for j in range(n)]
    return {
        'bitrev':bp,
        'rotl':rp,
        'bitrev_then_rotl':[rotl(j,k) for j in bp],
        'bitrev_then_xor':[mix_middle(j,k) for j in bp],
        'xor':xor,
    }


def parity_set(n,mask,sign=0):
    assert mask
    return [j for j in range(n) if (j&mask).bit_count()%2==sign]


def mask_boundary(mask,k):
    """Exact transitions of the binary parity of mask on 0...2^k-1."""
    assert 0<mask<(1<<k)
    parity=0; answer=0
    for t in range(k):
        parity ^= mask>>t&1
        if parity: answer+=1<<(k-t-1)
    return answer


def mask_pullback(mask,permutation,k):
    """For a *linear* GF(2) bit shuffle y=pi(x), pull back parity mask."""
    assert permutation[0]==0
    n=1<<k
    a=0
    for i in range(k):
        if (permutation[1<<i]&mask).bit_count()%2:a|=1<<i
    # validate against all index values; even mixed-XOR transformations work.
    assert all(((x&a).bit_count()-(permutation[x]&mask).bit_count())%2==0 for x in range(n))
    return a


def mask_budget(mask, k, permutations, ranks):
    assert len(ranks)==len(permutations)+1
    path=[mask]
    for pi in permutations:path.append(mask_pullback(path[-1],pi,k))
    costs=[rank*mask_boundary(m,k) for rank,m in zip(ranks,path)]
    return sum(costs),path,costs


def primitive_root_of_unity(n,p):
    assert (p-1)%n==0
    for gen in range(2,p):
        w=pow(gen,(p-1)//n,p)
        if pow(w,n,p)==1 and pow(w,n//2,p)!=1:return w
    raise ValueError('No primitive root')


def rank_mod(A,p):
    # Integer exact Gaussian elimination, accelerated with NumPy but no floats.
    import numpy as np
    a=np.array(A,dtype=np.int64,copy=True)
    h,w=a.shape
    row=0
    for col in range(w):
        if row==h:break
        piv=np.flatnonzero(a[row:,col])
        if not piv.size:continue
        index=row+int(piv[0])
        a[[row,index]]=a[[index,row]]
        inv=pow(int(a[row,col]),-1,p)
        if row+1<h:
            scales=(a[row+1:,col]*inv)%p
            a[row+1:,col+1:]=(a[row+1:,col+1:]-scales[:,None]*a[row,col+1:])%p
            a[row+1:,col]=0
        row+=1
    return row


def fourier_block_rank(n, rows, cols, p):
    import numpy as np
    root=primitive_root_of_unity(n,p)
    power=np.array([pow(root,i,p) for i in range(n)],dtype=np.int64)
    rows=np.array(rows,dtype=np.int64);cols=np.array(cols,dtype=np.int64)
    return rank_mod(power[(rows[:,None]*cols[None,:])%n],p)


def exact_obstruction(n, initial_set, permutations, ranks, p=12289):
    cap, path, costs=moving_partition_budget(n,initial_set,permutations,ranks)
    last=set(path[-1])
    complement=[j for j in range(n) if j not in last]
    fr=fourier_block_rank(n,complement,initial_set,p)
    return {'n':n,'stages':len(ranks),'ranks':ranks,'input':list(initial_set),
            'output':complement,'path':path,'costs':costs,'capacity':cap,
            'fourier_rank':fr,'prime':p,'excluded':fr>cap}


def search_parity(k,permutations,ranks,prime=12289):
    """Check all nonzero parity masks, exact modular ranks when needed."""
    n=1<<k
    found=[]; trials=0
    for mask in range(1,n):
        budget,path,costs=mask_budget(mask,k,permutations,ranks)
        if budget>=n//2:continue
        trials+=1
        i=parity_set(n,mask);o=parity_set(n,path[-1],1)
        rk=fourier_block_rank(n,o,i,prime)
        if rk>budget:
            found.append({'mask':mask,'path':path,'costs':costs,
                         'rank':rk,'budget':budget,'gap':rk-budget})
    return sorted(found,key=lambda x:(-x['gap'],x['budget'])),trials

if __name__=='__main__':
    from pprint import pprint
    for k in (6,7,8):
        tr=transformations(k)
        progs={
            'all_rotl':[tr['rotl']]*3,
            'all_bitrev':[tr['bitrev']]*3,
            'bitrev_middle_rotate':[tr['bitrev'],tr['bitrev_then_rotl'],tr['bitrev']],
            'bitrev_middle_xor':[tr['bitrev'],tr['bitrev_then_xor'],tr['bitrev']],
            'every_bitrev_then_rotl':[tr['bitrev_then_rotl']]*3,
        }
        for name,ps in progs.items():
            results,checked=search_parity(k,ps,[1]*4)
            print('N',1<<k,name,'tested Fourier ranks',checked,'excluded by',len(results),'best',results[:1],flush=True)
