import numpy as np
from functools import lru_cache

def bitrev_perm(k):
    return tuple(reversed(range(k)))

def rotl_perm(k,shift=1):
    # new pos (j+shift)%k gets old bit j
    return tuple((j+shift)%k for j in range(k))

def permutation_comp(p,q):
    # bit permutation map j -> p[q[j]], p[q[j]] as output bit mapping
    return tuple(p[q[i]] for i in range(len(p)))

def map_mask(mask,pi):
    # mask on output of pi(j), pulls back to input j
    return sum(1<<i for i,j in enumerate(pi) if mask>>j & 1)

def transitions(mask,k):
    s=0;v=0
    for t in range(k):
        v ^= mask>>t & 1
        if v:s+=1<<(k-1-t)
    return s

@lru_cache(None)
def primitive_root(n,p):
    for a in range(2,p):
        w=pow(a,(p-1)//n,p)
        if pow(w,n,p)==1 and pow(w,n//2,p)!=1:return w
    raise ValueError()

def rank_mod_np(a,p):
    a=np.array(a,dtype=np.int64,copy=True)
    h,w=a.shape;r=0
    for c in range(w):
        pvs=np.flatnonzero(a[r:,c])
        if pvs.size==0:continue
        pv=r+int(pvs[0]);a[[r,pv]]=a[[pv,r]]
        v=pow(int(a[r,c]),-1,p)
        if r+1<h:
            coefs=a[r+1:,c]*v %p
            a[r+1:,c+1:]=(a[r+1:,c+1:]-coefs[:,None]*a[r,c+1:])%p
            a[r+1:,c]=0
        r+=1
        if r==h:break
    return r

def bit_parity_mask(n,mask):
    xs=np.arange(n,dtype=np.int64)
    # parity number bits
    v=np.zeros(n,dtype=np.int64)
    for i in range(n.bit_length()-1):
        if mask>>i&1:v^=(xs>>i)&1
    return np.flatnonzero(v==0),np.flatnonzero(v==1)

def rank_fourier_parity(k,mask_in,mask_out,p=12289):
    n=1<<k
    a,b=bit_parity_mask(n,mask_in)
    ro,r1=bit_parity_mask(n,mask_out)
    w=primitive_root(n,p)
    exps=(r1[:,None]*a[None,:])%n
    powers=np.array([pow(w,i,p) for i in range(n)],dtype=np.int64)
    return rank_mod_np(powers[exps],p)

def summarize(k,perms):
    n=1<<k
    best=[]
    rankmemo={}
    for initmask in range(1,n):
        masks=[initmask]
        for pi in perms:masks.append(map_mask(masks[-1],pi))
        ds=[transitions(mask,k) for mask in masks]
        bound=sum(ds)
        if bound>=n//2:continue
        if (initmask,masks[-1]) not in rankmemo:
            rankmemo[(initmask,masks[-1])]=rank_fourier_parity(k,initmask,masks[-1])
        rank=rankmemo[(initmask,masks[-1])]
        if rank>bound:best.append((rank-bound,rank,bound,initmask,masks[-1],ds))
    return sorted(best,reverse=True), len(rankmemo)

if __name__=='__main__':
    for k in (6,7,8):
        P=bitrev_perm(k);rot=rotl_perm(k)
        # explicit middle rotation combined bit reversal
        progs={
          'all_bitrev':[P,P,P],
          'middle_rot':[P,permutation_comp(rot,P),P],
          'twist_every':[permutation_comp(rot,P)]*3,
          'mixed_rotate':[P,permutation_comp(rot,P),permutation_comp(rot,P)],
          'all_rot': [rot]*3,
          'bitrev_rot_bitrev':[P,rot,P],
        }
        for name,ps in progs.items():
            sol,cnt=summarize(k,ps)
            print(k,name,'witnesses',len(sol),'ranks computed',cnt,'best',sol[:2],flush=True)
