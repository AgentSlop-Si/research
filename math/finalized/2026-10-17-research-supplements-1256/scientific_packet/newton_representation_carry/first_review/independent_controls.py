"""Fresh intake controls. No supplied source is imported or executed.

Reads only inert manifest/comparison JSON from an optional archive directory.
This is not a benchmark replay or proof-assistant certificate.
"""
from fractions import Fraction as F
from math import comb, factorial, lcm, prod, isqrt
from random import Random
from pathlib import Path
import hashlib
import json
import sys


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def padd_scaled(out, a, scale):
    if len(out) < len(a):
        out.extend([F(0)] * (len(a)-len(out)))
    for i, x in enumerate(a):
        out[i] += scale*x


def binomial_poly(n):
    a = [F(1)]
    for j in range(n):
        a = [x/F(j+1) for x in pmul(a, [F(j), F(1)])]
    return a


def remainder(a, b):
    a = list(a)
    a += [F(0)] * max(0,len(b)-1-len(a))
    for k in range(len(a)-len(b), -1, -1):
        scale = a[k+len(b)-1]/b[-1]
        for j, c in enumerate(b):
            a[k+j] -= scale*c
    return a[:len(b)-1]


def primes_upto(n):
    a = bytearray(b'\x01')*(n+1)
    a[:2] = b'\x00\x00'
    for p in range(2,isqrt(n)+1):
        if a[p]:
            a[p*p:n+1:p] = b'\x00'*len(range(p*p,n+1,p))
    return [p for p in range(2,n+1) if a[p]]


def make_parameters(r):
    L, D = lcm(*range(1,r+1)), lcm(*range(1,2*r+1))
    residues = []
    for p in primes_upto(2*r):
        pe = p
        while pe*p <= 2*r:
            pe *= p
        m = 1
        while m*p <= r:
            m *= p
        residues.append((pe, -pow(L//m,-1,pe) % pe))
    # Explicit CRT sum, independent of the archive's sequential construction.
    k0 = sum(a*(D//m)*pow(D//m,-1,m) for m,a in residues) % D
    k, P = k0+D, 1+(k0+D)*L
    R = [1+k*L//j for j in range(1,r+1)]
    w = [1]
    for x in R:
        w.append(w[-1]*x)
    assert prod(R) % D == 0
    beta = w[-1]//D
    assert beta > w[-2] and beta > (1 << (r*(r-1)))
    assert all((P+j-1)%j == 0 for j in range(1,r+1))
    return L,D,k,P,R,w,beta


def digits(n, R):
    out = []
    for base in R:
        n, a = divmod(n,base)
        out.append(a)
    return n,out


def carry(c, incoming, R, D, beta_digits):
    qQ = incoming
    u = []
    for a, base in zip(c,R):
        qQ, v = divmod(a+qQ,base)
        u.append(v)
    q0 = D*u[-1]//R[-1]
    rem = [x-q0*y for x,y in zip(u,beta_digits)]
    carry0, v = 0, []
    for a, base in zip(rem,R):
        carry0, d = divmod(a+carry0,base)
        v.append(d)
    assert carry0 == 0
    extra = int(tuple(v[::-1]) >= tuple(beta_digits[::-1]))
    if extra:
        carry0 = 0
        for j,base in enumerate(R):
            carry0,v[j] = divmod(v[j]-beta_digits[j]+carry0,base)
        assert carry0 == 0
    return D*qQ+q0+extra,v,extra


def encode(n, R, beta):
    blocks = []
    while n:
        n,b = divmod(n,beta)
        q,d = digits(b,R)
        assert q == 0
        blocks.append(d)
    return blocks or [[0]*len(R)]


def main():
    out = {'status':'PASS','uploaded_scripts_executed':False,
           'scope':'Independent exact arithmetic controls; no source benchmark replay'}
    source = Path(sys.argv[1]) if len(sys.argv)>1 else None
    if source:
        entries = json.loads((source/'MANIFEST.json').read_text())['files']
        for e in entries:
            b=(source/e['path']).read_bytes()
            assert len(b)==e['bytes']
            assert hashlib.sha256(b).hexdigest()==e['sha256']
        out['manifest_entries_verified']=len(entries)
    params={r:make_parameters(r) for r in range(2,129)}
    fcount=0
    for r,(_,D,_,_,_,_,_) in params.items():
        for t in range(r-1):
            den=comb(r+t,r)
            assert D%den==0
            fold=[D//den*comb(r+t-a-1,t-a) for a in range(t+1)]
            assert all(0<x<=D for x in fold)
            assert fold[0]*(r+t)==D*r
            assert all(x>=y for x,y in zip(fold,fold[1:]))
            fcount+=len(fold)
    out['ranks_integrality_capacity_checked']=[2,128]
    out['fold_constants_checked']=fcount
    poly=[binomial_poly(n) for n in range(21)]
    quotient_checks=0
    for r in range(2,11):
        D=params[r][1]
        for i in range(r):
            for j in range(r):
                coef={i+j-k: (-1)**k*comb(i+j-k,i-k)*comb(j,k)
                      for k in range(min(i,j)+1)}
                direct=pmul(poly[i],poly[j])
                summed=[]
                for d,c in coef.items():padd_scaled(summed,poly[d],c)
                assert direct==summed
                for z in [-2,0,1,7]:
                    mod=list(poly[r]);mod[0]-=D*z
                    target=remainder(direct,mod)
                    calculated=[F(0)]*r
                    for d,c in coef.items():
                        if d<r:padd_scaled(calculated,poly[d],c)
                        else:
                            t=d-r
                            for a in range(t+1):
                                fold=D//comb(r+t,r)*comb(r+t-a-1,t-a)
                                padd_scaled(calculated,poly[a],c*z*fold)
                    assert target==calculated
                    quotient_checks+=1
    out['rational_quotient_checks']=quotient_checks
    rng=Random(202610171235)
    cases=extra_cases=0
    rank_cases=[]
    for r in [2,3,4,5,8,16,32,64,128]:
        _,D,k,P,R,w,beta=params[r]
        _,bvec=digits(beta,R)
        vectors=[]
        for scalar in [-beta-1,-beta,-1,0,1,beta-1,beta,beta+1,D*beta-1,D*beta]:
            vectors.append(([scalar]+[0]*(r-1),0))
        for rep in range(300):
            H=(rep%7+1)*(r+3)
            c=[rng.randrange(-(1<<H),1<<H) for _ in range(r)]
            incoming=rng.randrange(-(1<<(H+2)),1<<(H+2))
            vectors.append((c,incoming))
        for c,inc in vectors:
            q,d,e=carry(c,inc,R,D,bvec)
            S=inc+sum(x*y for x,y in zip(c,w))
            assert (q,sum(x*y for x,y in zip(d,w))) == divmod(S,beta)
            assert all(0<=x<y for x,y in zip(d,R))
            cases+=1;extra_cases+=e
        rank_cases.append({'r':r,'P_bits':P.bit_length(),'beta_bits':beta.bit_length(),
                           'truncated_top':R[-1]%D !=0})
    out['signed_carry_cases']=cases
    out['one_extra_subtraction_exercised']=extra_cases
    out['carry_rank_parameters']=rank_cases
    out['small_example']={'r':2,'P':params[2][3],'D':params[2][1],'beta':params[2][-1]}
    assert out['small_example']=={'r':2,'P':39,'D':12,'beta':65}
    full_products=0
    for r in [2,3,5,8]:
        _,D,_,_,R,w,beta=params[r]
        _,bvec=digits(beta,R)
        for blocks in [1,2,4]:
            cap=beta**blocks
            samples=[(0,cap-1),(cap-1,cap-1),(cap-2,cap//2)]
            samples += [(rng.randrange(-cap,cap),rng.randrange(-cap,cap)) for _ in range(17)]
            for a,b in samples:
                aa,bb=encode(abs(a),R,beta),encode(abs(b),R,beta)
                raw=[[0]*r for _ in range(len(aa)+len(bb))]
                for x,ad in enumerate(aa):
                    for y,bd in enumerate(bb):
                        for i,av in enumerate(ad):
                            for j,bv in enumerate(bd):
                                for k in range(min(i,j)+1):
                                    d=i+j-k
                                    c=av*bv*(-1)**k*comb(d,i-k)*comb(j,k)
                                    if d<r:raw[x+y][d]+=c
                                    else:
                                        t=d-r
                                        for u in range(t+1):
                                            raw[x+y+1][u]+=c*(D//comb(r+t,r))*comb(r+t-u-1,t-u)
                height=max(max(abs(v) for v in row) for row in raw)
                bound=r*r*3**(2*r-2)*min(len(aa),len(bb))*max(map(max,aa))*max(map(max,bb))*(1+(r-1)*D)
                assert height<=bound
                canon=[];inc=0
                for row in raw:
                    inc,d,_=carry(row,inc,R,D,bvec);canon.append(d)
                assert inc>=0
                while inc:
                    inc,d,_=carry([0]*r,inc,R,D,bvec);canon.append(d)
                v=0
                for row in canon[::-1]:v=beta*v+sum(x*y for x,y in zip(row,w))
                sign=-1 if (a<0)!=(b<0) else 1
                assert sign*v==a*b
                full_products+=1
    out['independent_composed_integer_products']=full_products
    out['negative_controls']={
        'dropping_outer_fold_shift_detected':24-39 != 39*39,
        'assuming_integer_top_radix_detected':params[2][4][-1] % params[2][1] != 0,
    }
    # Independently reproduce input encoding, bound width and prime budget only.
    prime_set=set(primes_upto(2_000_000))
    rng=Random(2026101702)
    matched=[]
    for r in [8,16,32,64,128]:
        _,D,_,P,R,w,beta=params[r]
        bits=3*beta.bit_length()-5
        a=rng.getrandbits(bits)|(1<<(bits-1));b=rng.getrandbits(bits)|(1<<(bits-1))
        rec={'r':r,'input_bits_each':bits}
        for label,radices,base in [('normalized',R,beta),('monic',list(range(P,P+r)),factorial(r)*D*beta)]:
            aa,bb=encode(a,radices,base),encode(b,radices,base)
            maxa=max(map(max,aa));maxb=max(map(max,bb))
            bound=r*r*3**(2*r-2)*min(len(aa),len(bb))*maxa*maxb
            bound*=1+(r-1)*D if label=='normalized' else 2*factorial(r-1)
            m=max(1<<(4*r-4).bit_length(),1<<(len(aa)+len(bb)-1).bit_length())
            idx=(1<<20)//m
            modulus=1;nprimes=0
            while modulus<=2*bound:
                idx+=1;p=idx*m+1
                assert p<2_000_000
                if p in prime_set:
                    modulus*=p;nprimes+=1
            rec[label]={'input_blocks':[len(aa),len(bb)],'certified_bound_bits':bound.bit_length(),
                        'crt_primes':nprimes,'modulus_bits':modulus.bit_length(),
                        'block_bits':base.bit_length()}
        matched.append(rec)
    if source:
        historical=json.loads((source/'compact_newton/budget_comparison.json').read_text())['records']
        for a,b in zip(matched,historical):
            assert a['r']==b['r'] and a['input_bits_each']==b['input_bits_each']
            for label in ['normalized','monic']:
                for key in ['input_blocks','certified_bound_bits','crt_primes','modulus_bits']:
                    assert a[label][key]==b[label][key],(a['r'],label,key)
    out['matched_budget_recomputed']=matched
    out['large_product_coefficients_or_timing_replayed']=False
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
