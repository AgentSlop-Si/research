"""Fresh tests; native * and divmod are confined to this oracle/test file."""
import json
import random
from math import comb, factorial
from pathlib import Path
from producer import (Ledger, apply_block, bases_for, compose, describe, divide,
                      from_digits, multiply, multiply_digits, multiply_integer,
                      to_digits)

R = random.Random(202610151822)
counts = dict(scalar_products=0, divisions=0, descriptor_blocks=0,
              descriptor_associativity=0, integer_products=0, period_shift_pairs=0,
              chunk_carry_maps=0, sparse_band_columns=0, width_witnesses=0,
              negative_controls=0)

for _ in range(1000):
    a,b = R.getrandbits(R.randrange(300)), R.getrandbits(R.randrange(200))
    assert multiply(a,b) == a*b
    counts['scalar_products'] += 1
    d = R.getrandbits(R.randrange(1,150)) + 1
    assert divide(a,d) == divmod(a,d)
    counts['divisions'] += 1

for p in (3,7,255):
    for g in (1,4,17):
        for r in (1,2,3,4,7,8,16):
            bases=bases_for(p,g,r)
            digits=[R.randrange(bases[i%r]) for i in range(3*r+5)]
            for _ in range(8):
                lo=R.randrange(len(digits))
                hi=R.randrange(lo+1,len(digits)+1)
                P=1; H=0
                for j in range(hi-1,lo-1,-1):
                    P *= bases[j%r]
                    H = bases[j%r]*H+digits[j]
                assert describe(digits,bases,lo,hi)==(P,H)
                counts['descriptor_blocks'] += 1
            a=describe(digits,bases,0,r)
            b=describe(digits,bases,r,2*r)
            c=describe(digits,bases,2*r,3*r+5)
            assert compose(compose(a,b),c)==compose(a,compose(b,c))
            counts['descriptor_associativity'] += 1
            for _ in range(5):
                A=R.getrandbits(R.randrange(0,5*r+90))
                B=R.getrandbits(R.randrange(0,5*r+90))
                ad=to_digits(A,bases); bd=to_digits(B,bases)
                for h in sorted({1,2,3,r,max(len(ad),len(bd))}):
                    got,ledger=multiply_integer(A,B,p,g,r,h,True)
                    assert got==A*B
                    s,t=sorted((len(ad),len(bd)))
                    assert ledger['normalization_cells']==((s+h-1)//h)*(s+t+1)
                    counts['integer_products'] += 1
                for h in (r,2*r):
                    x,lx=multiply_digits(ad,bd,bases,h,False)
                    y,ly=multiply_digits(ad,bd,bases,h,True)
                    assert x==y
                    counts['period_shift_pairs'] += 1

# Chunk carry boundary: no retained low-to-high carry may be discarded.
for _ in range(2000):
    p,g,r=R.randrange(3,13),R.randrange(1,8),R.randrange(1,10)
    bases=bases_for(p,g,r)
    P=R.randrange(1,100000); H=R.randrange(P)
    start=R.randrange(3*r); length=R.randrange(1,3*r+1)
    v=[R.randrange(bases[(start+i)%r]) for i in range(length)]
    b=[R.randrange(bases[(start+i)%r]) for i in range(length)]
    incoming=R.randrange(P+H)
    c=incoming; X=Y=0; radix_product=1
    for i in range(length):
        base=bases[(start+i)%r]
        c,d=divmod(P*v[i]+H*b[i]+c,base)
        X += radix_product*v[i]
        Y += radix_product*b[i]
        radix_product *= base
        assert c<=P+H-1
    assert c==(P*X+H*Y+incoming)//radix_product
    # At any split, compact carry descriptors compose by (K1+R1*K2,R1*R2).
    cut=R.randrange(length+1)
    Ks=[]; Rs=[]
    for lo,hi in ((0,cut),(cut,length)):
        xx=yy=0; rr=1
        for i in range(lo,hi):
            xx += rr*v[i]; yy += rr*b[i]
            rr *= bases[(start+i)%r]
        Ks.append(P*xx+H*yy); Rs.append(rr)
    assert (Ks[0]+Rs[0]*Ks[1],Rs[0]*Rs[1])==(P*X+H*Y,radix_product)
    assert ((Ks[0]+incoming)//Rs[0]+Ks[1])//Rs[1]==c
    counts['chunk_carry_maps'] += 1


def sparse_column(r,g,lo,h,i):
    b=bases_for(7,g,r)
    v={i:1}
    for j in range(lo+h-1,lo-1,-1):
        new={}
        for pos,value in v.items():
            new[pos]=new.get(pos,0)+(b[j%r]-b[pos%r])*value
            new[pos+1]=new.get(pos+1,0)+value
        v={pos:value for pos,value in new.items() if value}
    return v

for r in range(2,18):
    for g in (1,4):
        for h in range(1,r):
            for i in range(r-h+1):
                lo=R.randrange(r-h+1)
                got=sparse_column(r,g,lo,h,i)
                expected={}
                for k in range(h+1):
                    rising=1
                    for t in range(h-k):
                        rising *= lo-i+t
                    val=comb(h,k)*(g**(h-k))*rising
                    if val:
                        expected[i+k]=val
                assert got==expected
                counts['sparse_band_columns'] += 1
        # Full-period product is the exact r-position shift even symbolically.
        for i in range(2*r):
            assert sparse_column(r,g,0,r,i)=={i+r:1}

width_witnesses=[]
ledgers=[]
for r in (4,8,16,32,64,128):
    bases=bases_for(7,4,r)
    a=[b-1 for b in bases]
    b=a+a
    A=from_digits(a,bases); B=from_digits(b,bases)
    P,H=describe(a,bases,0,r)
    assert H==P-1 and A==H
    c=0; W=1
    for i,bi in enumerate(b):
        c,d=divmod(H*bi+c,bases[i%r])
        W*=bases[i%r]
        assert c==H-(H+W-1)//W
    assert c==H-1
    width_witnesses.append({'r':r,'P_bits':P.bit_length(),'carry_bits':c.bit_length(),
                            'one_digit_bits':max(bases).bit_length(),
                            'factorial_diagonal_bits':abs(sparse_column(r,4,0,r-1,r-1)[r-1]).bit_length()})
    assert sparse_column(r,4,0,r-1,r-1)[r-1]==(-4)**(r-1)*factorial(r-1)
    counts['width_witnesses']+=1
    for h in sorted({1,2,4,8,r}):
        ledger=Ledger()
        out,ledger=multiply_digits(a,b,bases,h,True,ledger)
        assert from_digits(out,bases)==A*B
        ledgers.append({'r':r,'block_size':h,'input_digit_lengths':[r,2*r],**ledger.__dict__})

# Wrong interval order changes H even though P commutes.
assert compose((7,2),(11,3)) != compose((11,3),(7,2))
counts['negative_controls'] += 1
# Dropped carry: 6*6 in bases 7,11 cannot be represented by independent remainders.
assert from_digits([36%7,0],[7,11]) != 36
counts['negative_controls'] += 1
# A partial period is not a scalar shift: 7*W_1 differs from W_2.
assert 7*7 != 7*11
counts['negative_controls'] += 1
# One-digit carry cap fails at a valid full-period all-max-input block.
bases=bases_for(7,4,8); H=from_digits([b-1 for b in bases],bases)
assert H-1 > 2*max(bases)
counts['negative_controls'] += 1

result={'status':'PASS','seed':202610151822,'counts':counts,
        'width_witnesses':width_witnesses,'digit_core_ledgers':ledgers,
        'scope':'Exact finite checks and abstract work counters; no timing or asymptotic speedup claim.'}
Path('block_carried_newton_tree/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts,'width_witnesses':width_witnesses},indent=2))
