"""Independent native-integer oracles and finite controls for the new package."""
from itertools import product as cartesian
from math import comb, factorial
from random import Random
from hashlib import sha256
import json
from pathlib import Path
from guarded_sharing import (
    mul_small, odd_divide_bits, guard_for_degree, interpolate_consecutive,
    guarded_convolution, six_product_three, multiply_guarded_interface,
)

RNG = Random(202610181502)
COUNTS, DIGEST = {}, sha256()

def record(kind, data):
    COUNTS[kind] = COUNTS.get(kind, 0)+1
    DIGEST.update(json.dumps([kind, data], sort_keys=True, separators=(',',':')).encode())

def conv(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def evalpoly(a,x):
    return sum(v*x**i for i,v in enumerate(a))

def falling(degree):
    out=[1]
    for j in range(degree): out=conv(out,[-j,1])
    return out

def rising(start,count):
    out=[1]
    for j in range(start,start+count): out=conv(out,[j,1])
    return out

def matrix_outer(a,b,n):
    out=0
    for i in range(n):
        if a>>i&1:
            out|=b<<(i*n)
    return out

def hankel(value,n):
    diagonals={}
    for i in range(n):
        for j in range(n):
            bit=(value>>(i*n+j))&1
            if i+j in diagonals and diagonals[i+j]!=bit: return False
            diagonals[i+j]=bit
    return True

def gf2rank(values):
    basis={}
    for value in values:
        while value:
            b=value.bit_length()-1
            if b not in basis:
                basis[b]=value
                break
            value^=basis[b]
    return len(basis)

def check_ranks():
    for n in range(1,9):
        rankones=set()
        pairs=0
        for a in range(1,1<<n):
            for b in range(1,1<<n):
                value=matrix_outer(a,b,n)
                if hankel(value,n): rankones.add(value)
                pairs+=1
        expected={1,1<<(n*n-1),(1<<(n*n))-1}
        assert rankones==expected
        basis=[]
        for k in range(2*n-1):
            basis.append(sum(1<<(i*n+j) for i in range(n) for j in range(n) if i+j==k))
        assert gf2rank(basis)==2*n-1
        assert gf2rank(rankones)==(1 if n==1 else 3)
        if n>=3: assert gf2rank(rankones)<2*n-1
        record('binary_hankel_classifications', [n,pairs,len(rankones),gf2rank(rankones)])


def check_division():
    for width in [1,2,3,7,8,9,16,17,31,32,33,64,129]:
        for odd in [1,3,5,7,15,31,63,127,257,65535]:
            for _ in range(4):
                value=RNG.randrange(1<<width)
                transitions=[]
                got=odd_divide_bits(value,odd,width,lambda *args: transitions.append(args))
                assert got==value*pow(odd,-1,1<<width)%(1<<width)
                accum_in=accum_out=0
                for bit,digit,q,old,new in transitions:
                    accum_in+=digit<<bit
                    accum_out+=q<<bit
                    assert odd*accum_out==accum_in+(new<<(bit+1))
                    assert 0<=new<odd
                record('odd_divisions', [width,odd,value,got])
                COUNTS['checked_division_steps']=COUNTS.get('checked_division_steps',0)+len(transitions)
    for width in [1,7,8,9,32,129]:
        for small in range(33):
            value=RNG.randrange(1<<width)
            assert mul_small(value,small,width)==value*small%(1<<width)
            record('small_products',[width,small,value])


def interpolation_case(coefficients,H):
    n=len(coefficients); gamma=guard_for_degree(n-1); W=H+gamma
    samples=[evalpoly(coefficients,j)%(1<<W) for j in range(n)]
    stats={}
    got=interpolate_consecutive(samples,H,stats)
    assert got==[x%(1<<H) for x in coefficients]
    assert stats['Gamma']==((factorial(n-1)&-factorial(n-1)).bit_length()-1)
    assert stats['difference_subtractions']==n*(n-1)//2
    assert stats['basis_small_actions']==n*(n-1)//2
    assert stats['odd_division_steps']==n*H
    record('interpolations',[coefficients,H,got,stats])


def check_interpolation():
    for H in range(1,4):
        for n in range(1,5):
            for coefficients in cartesian(range(1<<H),repeat=n):
                interpolation_case(list(coefficients),H)
    for H in [1,2,7,8,9,31,64,129]:
        for n in range(1,16):
            for _ in range(3):
                cap=1<<(H+guard_for_degree(n-1)+5)
                interpolation_case([RNG.randrange(-cap,cap) for _ in range(n)],H)


def check_guard_sharpness():
    # The same adversarial polynomial vanishes at EVERY integer point modulo
    # the insufficient precision. Finite samples supplement the all-integer proof.
    for degree in range(2,31):
        gamma=guard_for_degree(degree)
        for H in [1,2,7,31]:
            polynomial=[x<<(H-1) for x in falling(degree)]
            assert polynomial[-1]%(1<<H)==1<<(H-1)
            for point in range(-degree-3,degree+8):
                assert evalpoly(polynomial,point)%(1<<(H+gamma-1))==0
            record('one_bit_short_null_polynomials',[degree,H,gamma])
    for L in range(2,13):
        degree=2*L-2; gamma=guard_for_degree(degree)
        t=factorial(degree).bit_length()
        H=2*t+2
        u=(H-1)//2; v=H-1-u
        a=[x<<u for x in rising(0,L-1)]
        b=[x<<v for x in rising(L-1,L-1)]
        assert max(a+b)<1<<H
        c=conv(a,b)
        assert c[-1]%(1<<H)==1<<(H-1)
        for point in range(-degree-3,degree+8):
            assert evalpoly(a,point)*evalpoly(b,point)%(1<<(H+gamma-1))==0
        got=guarded_convolution(a,b,H)
        assert got==[x%(1<<H) for x in c]
        record('canonical_factorable_guard_witnesses',[L,H,gamma,a,b])


def convolution_case(a,b,H):
    stats={}
    got=guarded_convolution(a,b,H,stats=stats)
    assert got==[x%(1<<H) for x in conv(a,b)]
    assert stats['evaluation_products']==2*len(a)-1
    record('guarded_convolutions',[a,b,H,got,stats])


def check_convolution():
    for H,maxL in [(1,4),(2,3)]:
        for L in range(1,maxL+1):
            arrays=list(cartesian(range(1<<H),repeat=L))
            for a in arrays:
                for b in arrays: convolution_case(list(a),list(b),H)
    for H in [1,2,7,8,9,31,64,129]:
        for L in range(1,13):
            W=H+guard_for_degree(2*L-2)
            for _ in range(3):
                convolution_case([RNG.randrange(1<<W) for _ in range(L)],
                                 [RNG.randrange(1<<W) for _ in range(L)],H)
    for H in [1,2,3,7,8,17,64,129]:
        cases=[]
        if H<=2:
            arrays=list(cartesian(range(1<<H),repeat=3))
            cases=[(a,b) for a in arrays for b in arrays]
        else:
            cases=[([RNG.randrange(1<<H) for _ in range(3)],
                    [RNG.randrange(1<<H) for _ in range(3)]) for _ in range(50)]
        for a,b in cases:
            stats={}
            got=six_product_three(a,b,H,stats=stats)
            assert got==[x%(1<<H) for x in conv(a,b)]
            assert stats['scalar_products']==6
            record('optimal_six_product_controls',[a,b,H,got])


def check_taylor_restriction():
    # Independence is forced just by the binary basis input pairs. Translation
    # matrices are unimodular mod 2; the output shift preserves output-slice span.
    for L in range(1,13):
        columns=[]
        for i in range(L):
            columns.append(sum((comb(i,j)%2)<<j for j in range(i+1)))
        assert gf2rank(columns)==L
        outcols=[]
        for k in range(2*L-1):
            outcols.append(sum((comb(k,j)%2)<<j for j in range(k+1)))
        assert gf2rank(outcols)==2*L-1
        record('taylor_image_rank_controls',[L,columns,outcols])


def check_integrated():
    for m,L in [(2,1),(2,2),(2,3),(3,3),(4,5),(7,4),(8,7),(9,8),
                (17,5),(31,7),(64,8),(129,6),(257,4)]:
        limit=1<<(m*L)
        cases=[(0,0),(1,limit-1),(limit-1,limit-1),(limit//2,limit//2+1)]
        cases += [(RNG.randrange(limit),RNG.randrange(limit)) for _ in range(8)]
        for x,y in cases:
            stats={}
            got=multiply_guarded_interface(x,y,m,L,stats=stats)
            assert got==x*y
            a=[(x>>(m*i))% (1<<m) for i in range(L)]
            b=[(y>>(m*i))% (1<<m) for i in range(L)]
            assert stats['final_coefficients']==conv(a,b)
            assert stats['maximum_sample_bits']<=stats['sample_capacity']
            assert stats['output_coefficients']==2*L-1
            record('complete_mersenne_products',[m,L,x,y,got,stats])


def main():
    check_ranks(); check_division(); check_interpolation(); check_guard_sharpness()
    check_convolution(); check_taylor_restriction(); check_integrated()
    result={'status':'PASS','counts':COUNTS,'digest':DIGEST.hexdigest(),
            'scope':'Finite controls supplement, and do not prove, the theorem or asymptotic ledger.'}
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
