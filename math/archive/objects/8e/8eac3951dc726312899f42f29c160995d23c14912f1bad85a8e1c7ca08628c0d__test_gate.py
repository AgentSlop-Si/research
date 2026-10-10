"""Independent finite-field test suite for the moving-partition theorem."""
import random
import numpy as np
from moving_partition import (
 bitrev, rotl, mix_middle, mask_boundary, mask_budget,
 parity_set, mask_pullback, moving_partition_budget,
 transformations, rank_mod, fourier_block_rank,
 primitive_root_of_unity, exact_obstruction, search_parity)
from interval_sweep import sweep_intervals

P=12289

def stage(n,p,r,rng):
    A=np.zeros((n,n),dtype=np.int64)
    for ch in range(r):
        a=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        b=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        c=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        e=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
        for i in range(n):
            A[i,:i]=(A[i,:i]+a[i]*b[:i])%p
            A[i,i+1:]=(A[i,i+1:]+c[i]*e[i+1:])%p
    for i in range(n): A[i,i]=rng.randrange(p)
    return A


def test_parity_transition_formula():
 for k in range(2,11):
    n=1<<k
    for mask in range(1,n):
        x=parity_set(n,mask)
        direct=sum(((j&mask).bit_count()%2)!=(((j+1)&mask).bit_count()%2) for j in range(n-1))
        assert mask_boundary(mask,k)==direct
 print('PASS 1: all parity boundaries through N=1024')


def test_binary_pullback():
 for k in range(3,9):
    n=1<<k; transformations_k=transformations(k)
    for name,perm in transformations_k.items():
      for mask in (1,3,5,7,n//2,n//2+1,n-1):
        pulled=mask_pullback(mask,perm,k)
        assert {j for j in range(n) if (perm[j]&mask).bit_count()%2==0}==set(parity_set(n,pulled))
 print('PASS 2: bit linear and XOR-mask pullback')


def test_interval_vandermonde():
 rng=random.Random(7)
 for k in range(3,8):
    n=1<<k
    for a,b in [(0,n//2),(n//4,n//2),(1,2),(n//2,n//2+1), (0,n-1)]:
        cols=list(range(a,b)); rows=rng.sample(range(n),n-len(cols))
        assert fourier_block_rank(n,rows,cols,P)==min(len(cols),n-len(cols))
 print('PASS 3: characteristic-p Vandermonde positive controls')


def test_random_products():
    rng=random.Random(2343)
    for n in (8,16,32,64):
      for it in range(10):
        ranks=[rng.choice((1,1,2)) for _ in range(4)]
        perms=[]
        for _ in range(3):
          a=list(range(n));rng.shuffle(a);perms.append(a)
        M=stage(n,P,ranks[0],rng)
        for j in range(1,4):
          M=stage(n,P,ranks[j],rng)@M[perms[j-1],:]%P
        for _ in range(5):
          m=rng.randint(1,n-1)
          x=rng.sample(range(n),m)
          cost,sets,costs=moving_partition_budget(n,x,perms,ranks)
          rows=[j for j in range(n) if j not in set(sets[-1])]
          actual=rank_mod(M[np.ix_(rows,x)],P)
          assert actual<=cost,(n,it,ranks,cost,actual)
    print('PASS 4: 200 random stage-product blocks with arbitrary shuffles and mixed ranks')


def test_arbitrary_shuffle_exact_certificates():
 for k in (6,7,8):
    n=1<<k; tr=transformations(k)
    progs={
      'rotl':[tr['rotl']]*3,
      'twisted_bitrev':[tr['bitrev_then_rotl']]*3,
      'middle_xor':[tr['bitrev'],tr['bitrev_then_xor'],tr['bitrev']],
      'middle_rotate':[tr['bitrev'],tr['bitrev_then_rotl'],tr['bitrev']],
    }
    for name,perms in progs.items():
      witnesses,num=search_parity(k,perms,[1]*4,P)
      if k==6 and name in ('middle_rotate','middle_xor'):
        assert not witnesses
      else:
        assert witnesses,(n,name)
        w=witnesses[0]
        C=parity_set(n,w['mask'])
        cost,sets,costs=moving_partition_budget(n,C,perms,[1]*4)
        R=[j for j in range(n) if j not in set(sets[-1])]
        assert cost==w['budget'] and costs==w['costs']
        for prime in (12289,65537):
           assert fourier_block_rank(n,R,C,prime)>cost,(n,name,prime)
 print('PASS 5: cross-partition, double-prime exact Fourier contradictions')


def test_exhaustive_interval_sweep():
 for k in (6,7):
   tr=transformations(k)
   if k==6:
      results,count=sweep_intervals(k,[tr['bitrev_then_rotl'],tr['bitrev_then_xor'],tr['bitrev_then_rotl']])
      assert count==2079 and results and results[0][0]>=2
   else:
      results,count=sweep_intervals(k,[tr['rotl']]*3)
      assert count==8255 and results and results[0][1]==64 and results[0][2]==26
 print('PASS 6: exhaustive consecutive-window search')


def test_rotation_formula():
 for k in range(4,13):
    n=1<<k
    pi=[rotl(j,k) for j in range(n)]
    t=min(k-1,6)
    group=parity_set(n,1<<(k-1))
    cost,sets,costs=moving_partition_budget(n,group,[pi]*(t-1),[1]*t)
    expected=[(1<<(j+1))-1 for j in range(t)]
    assert costs==expected and cost==2**(t+1)-t-2,(k,cost,expected)
    if t<=k-2:assert cost<n//2
 print('PASS 7: all-length rotation channel-cost identity')


def test_local_shear():
 for k in range(4,11):
    n=1<<k
    shear=[j ^ ((j<<1)&(n-1)) for j in range(n)]
    masks=[1<<(k-1)]
    for _ in range(min(5,k)-1):masks.append(mask_pullback(masks[-1],shear,k))
    for s,m in enumerate(masks):
        assert m & ((1<<(k-1-s))-1)==0,(k,s,m)
        assert mask_boundary(m,k)<(1<<(s+2)),(k,s,m)
 print('PASS 8: local binary-shear support bound')

if __name__=='__main__':
 test_parity_transition_formula()
 test_binary_pullback()
 test_interval_vandermonde()
 test_random_products()
 test_arbitrary_shuffle_exact_certificates()
 test_exhaustive_interval_sweep()
 test_rotation_formula()
 test_local_shear()
 print('ALL 8/8 GROUPS PASS')
