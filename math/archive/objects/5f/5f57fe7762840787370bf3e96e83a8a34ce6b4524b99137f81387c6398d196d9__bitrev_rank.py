"""Exact bit-reversal Fourier cut rank recurrence, no numerical approximations.
For N=2^m>=4, Q_N=P_bitrev F_N P_bitrev.T,
  r_N(k)=rank(Q_N[:k,k:]).
For 0<=k<=N/2, r_N(k)=ceil(k/2)+r_(N/4)(floor(k/2)),
where r_1(0)=r_1(1)=0, and r_N(k)=r_N(N-k).
For N>=8, max_k r_N(k)=N/4+1.
"""
from functools import lru_cache

@lru_cache(None)
def exact_cut_rank(n,k):
    assert n>=1 and n&(n-1)==0 and 0<=k<=n
    if k==0 or k==n:return 0
    if n==2:return 1
    if k>n//2:return exact_cut_rank(n,n-k)
    return (k+1)//2+exact_cut_rank(n//4,k//2)


def bitrev_perm(n):
    b=n.bit_length()-1
    return [int(f'{i:0{b}b}'[::-1],2) for i in range(n)]


def predicted_qs_rank(n):
    return max(exact_cut_rank(n,k) for k in range(1,n))

if __name__=='__main__':
    for n in [4,8,16,32,64,128,256,512,1024]:
        print(n,'predicted QS',predicted_qs_rank(n),'central',exact_cut_rank(n,n//2),
              'near central',exact_cut_rank(n,n//2-1))
