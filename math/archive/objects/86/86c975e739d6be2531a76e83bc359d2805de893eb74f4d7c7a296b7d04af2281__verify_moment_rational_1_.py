#!/usr/bin/env python3
"""Independent, rigorous rational certificate for a 256-DFT singular-value gap.

No NumPy, SciPy, mpmath, FFT numerical approximation, or floating-point
calculations occur in the proof. The sole data input is saved affine shuffles.
"""
import json, math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parent
N=256


def affine(cols):
    return [__import__('functools').reduce(lambda x,j: x ^ (cols[j] if (i>>j)&1 else 0),range(8),0) for i in range(N)]


def initial_sets():
    cols=json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())['affine_shuffle_columns']
    p1,p2,p3=map(affine,cols)
    invp3=[0]*N
    for i,j in enumerate(p3):invp3[j]=i
    g=[(i&64).bit_count()%2==0 for i in range(N)]
    C=[p1[i] for i in range(N) if g[i]]
    R=[invp3[i] for i in range(N) if not g[p2[i]]]
    assert len(R)==len(C)==128
    return R,C


def difference_counts(indices):
    ans=[0]*N
    for x in indices:
        for y in indices: ans[(x-y)%N]+=1
    return ans


def trace_coefficients():
    R,C=initial_sets()
    A=difference_counts(R)
    B=difference_counts(C)
    coeff=[0]*N
    for i in range(N):
        if A[i]==0:continue
        for j in range(N):
            if B[j]:coeff[(i*j)%N]+=A[i]*B[j]
    d=[coeff[k]-coeff[k+N//2] for k in range(N//2)]
    # Complex conjugation forces the reduced coefficients to be antisymmetric.
    assert d[64]==0
    for k in range(1,64):assert d[128-k]==-d[k]
    assert sum(coeff)==128**4
    return d


def arctan_interval(one_over_q, n=10):
    x=Q(1,one_over_q)
    s=Q(0)
    for j in range(n):s+=(-1)**j*x**(2*j+1)/(2*j+1)
    err=x**(2*n+1)/(2*n+1)
    return (s,s+err) if n%2==0 else (s-err,s)


def pi_bounds():
    al,au=arctan_interval(5,10)
    bl,bu=arctan_interval(239,10)
    l,u=16*al-4*bu,16*au-4*bl
    assert l<Q(22,7) and u<Q(22,7) and Q(3)<l
    # Enclose pi with concise rational endpoints at 12 decimal places.
    scale=10**12
    L=Q(l.numerator*scale//l.denominator,scale)
    U=Q(-((-u.numerator*scale)//u.denominator),scale)
    assert L<=l<u<=U and U-L<Q(1,10**10)
    return L,U


def cos_interval(k,pi_lo,pi_hi,m=13):
    # For angle theta = pi*k/128, bound evaluation at rational midpoint
    # by the global 1-Lipschitz property of cos and Taylor's remainder.
    x=(pi_lo+pi_hi)*Q(k,256)
    squared=x*x
    t=Q(1);s=t
    for j in range(1,m+1):
        t=-t*squared/Q((2*j-1)*(2*j))
        s+=t
    lip=(pi_hi-pi_lo)*Q(k,256)
    remainder=Q(22,7)**(2*m+1)/math.factorial(2*m+1)
    err=lip+remainder
    return s-err,s+err


def exact_interval():
    d=trace_coefficients()
    pilo,pihi=pi_bounds()
    lo=hi=Q(d[0],1)
    for k in range(1,64):
        if not d[k]:continue
        cl,cu=cos_interval(k,pilo,pihi)
        a,b=2*d[k]*cl,2*d[k]*cu
        lo+=min(a,b);hi+=max(a,b)
    lo/=N*N;hi/=N*N
    # M = tr((H*H)^2), where H=U[R,C], U=F/16.
    # Prove M > 1264/25 = 50.56 exactly with rationals.
    assert lo>Q(1264,25), (float(lo),float(hi))
    assert hi<Q(51)
    return d,lo,hi,pilo,pihi


def main():
    d,lo,hi,pilo,pihi=exact_interval()
    certificate={
       'root_of_unity_order':256,
       'cyclotomic_reduction_coefficients':d,
       'moment_rational_lower_numerator':str(lo.numerator),
       'moment_rational_lower_denominator':str(lo.denominator),
       'moment_rational_upper_numerator':str(hi.numerator),
       'moment_rational_upper_denominator':str(hi.denominator),
       'moment_enclosure_decimal_display':[float(lo),float(hi)],
       'pi_rational_bounds':[str(pilo),str(pihi)],
       'exact_inequality':'trace((H*H)^2)>1264/25; hence sigma_17(H)>3*sqrt(2)/5',
       'validated_without_float_in_proof':True
    }
    (ROOT/'RATIONAL_MOMENT_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2))
    print('PASS exact rational moment certificate:')
    print('  tr((H*H)^2) in [%.12f, %.12f]'%(float(lo),float(hi)))
    print('  lower threshold 1264/25 = 50.56; sigma_17 > 3sqrt(2)/5')
    print('  nonzero reduced cyclotomic coefficients:',sum(x!=0 for x in d))
    return certificate

if __name__=='__main__':main()
