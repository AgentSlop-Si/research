"""All-length twisted-bit-reversal proof controls; characteristic-zero proofs in PROOF_CERTIFICATE.md."""
from moving_partition import *


def mask_and_d(k):
    m=k//2
    if k%2:
        return (1<<m)|(1<<(m+1)),1<<m,1<<m
    return 1<<m,(1<<m)-1,(1<<(m-1))+1


def exact_small_fourier_witness(k,p):
    # A fixed 2x2 or 4x4 invertible block appears after short FFT transforms.
    from build_certificates import independent_det_mod
    n=1<<k
    w=primitive_root_of_unity(n,p)
    if k%2==0:
        q=1<<(k//2-1)
        eta=pow(w,q*q,p)
        assert pow(eta,4,p)==1 and pow(eta,2,p)!=1
        mat=[[1,1],[1,eta]]
    else:
        m=k//2;q=1<<(m-1)
        eta=pow(w,q*q,p)
        assert pow(eta,8,p)==1 and pow(eta,4,p)!=1
        X=[2,3,4,5];Y=[0,1,6,7]
        mat=[[pow(eta,x*y,p) for y in Y] for x in X]
    return independent_det_mod(mat,p)


def run():
    for k in range(2,11):
        n=1<<k
        mask,d,lb=mask_and_d(k)
        T=[rotl(bitrev(i,k),k) for i in range(n)]
        assert mask_pullback(mask,T,k)==mask
        assert mask_boundary(mask,k)==d
        assert (n//2+d-1)//d==lb
        C=parity_set(n,mask)
        R=parity_set(n,mask,1)
        for p in (12289,65537):
            assert exact_small_fourier_witness(k,p)!=0
            assert fourier_block_rank(n,R,C,p)==n//2,(n,p)
        print('TWIST PASS N',n,'mask',mask,'transitions',d,'Fourier rank',n//2,
            'necessary stages',lb,flush=True)
    print('ALL TWISTED PROOF CONTROLS PASS')

if __name__=='__main__':run()
