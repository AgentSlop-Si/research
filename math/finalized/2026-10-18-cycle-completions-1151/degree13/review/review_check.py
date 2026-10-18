#!/usr/bin/env python3
"""Independent degree-13 literal review. Input JSON is inert, never executable.

Fresh arithmetic: prime-polynomial Euclid and carry-free Kronecker products.
Fresh branch inverse: literal powers A^0,...,A^12 and finite geometric sum.
No candidate or historical implementation is imported or executed.
"""
import hashlib
import json
import math
from pathlib import Path
import sys
import time

P, D, N, Q = 53, 13, 13, 16
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('inputs')
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.')
OUT.mkdir(parents=True, exist_ok=True)
start = time.monotonic()
raw = (BASE/'DEGREE13_LITERAL_CERTIFICATE.json').read_bytes()
cert = json.loads(raw)
assert cert['degree'] == D and cert['characteristic'] == P
modulus = cert['field_modulus_ascending']
assert modulus == [1,1]+[0]*11+[1]

def trim(a):
    a = list(a)
    while a and not a[-1]: a.pop()
    return a

def padd(a,b,sign=1):
    c = [0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i] = x
    for i,x in enumerate(b): c[i] = (c[i]+sign*x)%P
    return trim(c)

def pmul(a,b):
    c = [0]*(len(a)+len(b))
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j] += x*y
    return trim([x%P for x in c])

def pdiv(a,b):
    a,b=trim(a),trim(b)
    assert b
    q=[0]*max(0,len(a)-len(b)+1)
    bi=pow(b[-1],-1,P)
    while len(a)>=len(b):
        k=len(a)-len(b); v=a[-1]*bi%P; q[k]=v
        for j,x in enumerate(b): a[j+k]=(a[j+k]-v*x)%P
        a=trim(a)
    return trim(q),a

def pmod(a,m): return pdiv(a,m)[1]

def ppow(a,n,m):
    r=[1]
    while n:
        if n&1: r=pmod(pmul(r,a),m)
        a=pmod(pmul(a,a),m);n//=2
    return r

def pgcd(a,b):
    while b:a,b=b,pmod(a,b)
    k=pow(a[-1],-1,P)
    return [x*k%P for x in a]

# Irreducibility precedes every field inversion.
frob=[]; t=[0,1]
for _ in range(D):
    t=ppow(t,P,modulus);frob.append(t)
assert frob[-1]==[0,1]
first_gcd=pgcd(modulus,padd(frob[0],[0,1],-1))
assert first_gcd==[1]
# Degree 13 is prime: X^(53^13)-X permits degrees 1 or 13, gcd excludes 1.
assert all(D%k for k in range(2,math.isqrt(D)+1))
Z=(0,)*D;O=(1,)+(0,)*(D-1)

def element(a):
    assert isinstance(a,list) and len(a)==D
    assert all(type(x) is int and 0<=x<P for x in a)
    return tuple(a)

def const(a):return (a%P,)+(0,)*(D-1)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def sub(a,b):return tuple((x-y)%P for x,y in zip(a,b))
def scale(a,c):return tuple(x*c%P for x in a)

def mul(a,b):
    # 13*52^2 < 2^16: no carry can mix convolution coefficients.
    if a==Z or b==Z:return Z
    x=sum(v<<(16*i) for i,v in enumerate(a))
    y=sum(v<<(16*i) for i,v in enumerate(b))
    product=x*y
    c=[(product>>(16*i))&65535 for i in range(2*D-1)]
    # u^13=-u-1, descending reduction after unpacking.
    for k in range(2*D-2,D-1,-1):
        c[k-D]-=c[k];c[k-D+1]-=c[k]
    return tuple(v%P for v in c[:D])

def power(a,n):
    r=O
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n//=2
    return r

def inv(a):
    assert a!=Z
    r0,r1=modulus,trim(a);s0,s1=[],[1]
    while r1:
        q,r=pdiv(r0,r1);r0,r1=r1,r
        s0,s1=s1,padd(s0,pmul(q,s1),-1)
    assert len(r0)==1
    result=pmod([v*pow(r0[0],-1,P)%P for v in s0],modulus)
    result=tuple(result+[0]*(D-len(result)))
    assert mul(a,result)==O
    return result

# Cross-check every basis product and deterministic dense pairs against
# unrelated schoolbook polynomial multiplication and long division.
tests=[]
for i in range(D):
    for j in range(D):
        a=tuple(int(k==i) for k in range(D));b=tuple(int(k==j) for k in range(D))
        tests.append((a,b))
for s in range(100):
    tests.append((tuple((s*s+7*i*i+3*s*i+11)%P for i in range(D)),
                  tuple((5*s*s+13*i*i*i+2*s*i+19)%P for i in range(D))))
for a,b in tests:
    c=pmod(pmul(a,b),modulus)
    assert mul(a,b)==tuple(c+[0]*(D-len(c)))
assert pow(Q,N,P)==1 and all(pow(Q,k,P)!=1 for k in range(1,N))
qi=lambda e:pow(Q,e%N,P)
ni=pow(N,-1,P)
gamma=sum(qi(-t*t) for t in range(N))*ni%P
assert gamma==7

y,z=element(cert['y']),element(cert['z'])
assert y!=Z and z!=Z and any(y[1:]) and any(z[1:])
roots=[element(r) for r in cert['roots']]
H=[element(c) for c in cert['H']]
assert len(roots)==7 and len(set(roots))==7 and Z not in roots
assert len(H)==8 and H[-1]==O
product=[O]
for r in roots:
    out=[Z]*(len(product)+1)
    for i,c in enumerate(product):
        out[i]=sub(out[i],mul(r,c));out[i+1]=add(out[i+1],c)
    product=out
assert product==H
root_frob=[power(r,P) for r in roots]
assert set(root_frob)!=set(roots)
assert any(any(h[1:]) for h in H)
assert len(cert['banks'])==16
expected_signs=[(1,1)]*7+[(-1,1),(1,-1)]+[(-1,-1)]*7
assert [(b['epsilon'],b['delta']) for b in cert['banks']]==expected_signs

# Gaussian coefficients derived by appending literal noncommuting letters.
# In ordered X^r Y^ell, Y X=omega X Y.
gaussian={}
for epsilon,delta in set(expected_signs):
    omega=qi(epsilon*delta);words={(0,0):1}
    table={(0,0):1}
    for n in range(1,N):
        nxt={}
        for (r,ell),v in words.items():
            nxt[r+1,ell]=(nxt.get((r+1,ell),0)+v*pow(omega,ell,P))%P
            nxt[r,ell+1]=(nxt.get((r,ell+1),0)+v)%P
        table.update(nxt);words=nxt
    gaussian[epsilon,delta]=[[table.get(((epsilon*a)%N,(delta*b)%N),0)
                              for b in range(N)] for a in range(N)]

def identity():return [[O if r==c else Z for c in range(N)]for r in range(N)]
def matrix_zero():return [[Z for _ in range(N)]for _ in range(N)]
def left_A(M,alpha,epsilon,diagonal):
    return [[add(mul(alpha,M[(r-epsilon)%N][c]),scale(M[r][c],diagonal[r]))
             for c in range(N)]for r in range(N)]

total=matrix_zero();physical=[];branch_hashes=[];guard_values=[]
inverse_checks=0;power_checks=0;weight_checks=0;amplitude_checks=0
sector_columns=[];sector_sums=[[Z for _ in range(N)]for _ in range(N)]
bank_weyl_checks=0
for index,b in enumerate(cert['banks']):
    epsilon,delta=b['epsilon'],b['delta'];alpha=element(b['alpha'])
    assert b['beta']==1 and type(b['beta']) is int and alpha!=Z
    expected_alpha=roots[index] if index<7 else y if index==7 else z if index==8 else roots[index-9]
    assert alpha==expected_alpha
    guard=sub(Z,power(alpha,N));assert guard!=Z and guard==element(b['guard'])
    guard_values.append(guard);gi=inv(guard)
    weights=[element(w) for w in b['weights']]
    amps=[element(a) for a in b['amplitudes']]
    assert len(weights)==N and len(amps)==N
    for j in range(N):
        s=Z
        for k in range(N):s=add(s,scale(amps[k],qi(-epsilon*k*j)))
        assert weights[j]==scale(mul(guard,s),gamma);weight_checks+=1
    denominator_inv=inv(scale(guard,N*gamma%P))
    for k in range(N):
        s=Z
        for j in range(N):s=add(s,scale(weights[j],qi(epsilon*k*j)))
        assert amps[k]==mul(denominator_inv,s);amplitude_checks+=1
    bank=matrix_zero();hashes=[]
    for j in range(N):
        diagonal=[qi(epsilon*delta*j+delta*t) for t in range(N)]
        current=identity();geometric=identity()
        for n in range(1,N):
            current=left_A(current,alpha,epsilon,diagonal)
            geometric=[[add(geometric[r][c],current[r][c]) for c in range(N)]for r in range(N)]
        thirteenth=left_A(current,alpha,epsilon,diagonal)
        scalar=add(power(alpha,N),O)
        for r in range(N):
            for c in range(N):
                assert thirteenth[r][c]==(scalar if r==c else Z);power_checks+=1
        V=[[mul(gi,x) for x in row]for row in geometric]
        for r in range(N):
            for c in range(N):
                target=O if r==c else Z
                assert sub(scale(V[r][c],1-diagonal[r]),mul(alpha,V[(r-epsilon)%N][c]))==target
                assert sub(scale(V[r][c],1-diagonal[c]),mul(alpha,V[r][(c+epsilon)%N]))==target
                inverse_checks+=2
                bank[r][c]=add(bank[r][c],scale(mul(weights[j],V[r][c]),ni))
        hashes.append(hashlib.sha256(json.dumps(V,separators=(',',':')).encode()).hexdigest())
        last_inverse=V
    assert any(v!=Z for row in bank for v in row)
    branch_hashes.append(hashes);physical.append(bank)
    total=[[add(total[r][c],bank[r][c])for c in range(N)]for r in range(N)]
    powers=[power(alpha,(epsilon*a)%N)for a in range(N)]
    columns=[]
    for a in range(N):
        col=[]
        for k in range(N):
            value=scale(powers[a],gaussian[epsilon,delta][a][k]);col.append(value)
            contribution=mul(value,amps[k]);sector_sums[a][k]=add(sector_sums[a][k],contribution)
            actual=Z
            for t in range(N):actual=add(actual,scale(bank[(t+a)%N][t],qi(-k*t)*ni%P))
            assert actual==scale(contribution,gamma);bank_weyl_checks+=1
        columns.append(col)
    sector_columns.append(columns)
    print('bank',index+1,'of 16: 13 literal geometric inverses and raw bank verified',flush=True)

target=[[const(qi(-r*c))for c in range(N)]for r in range(N)]
claimed=[[element(v)for v in row]for row in cert['matrix']]
assert len(claimed)==N and all(len(row)==N for row in claimed)
assert total==target and claimed==total
for a in range(N):
    for b in range(N):assert sector_sums[a][b]==const(qi(10*(a+b)**2))

def rank(matrix):
    m=[list(row)for row in matrix];rows=len(m);cols=len(m[0]);r=0
    for c in range(cols):
        k=next((k for k in range(r,rows)if m[k][c]!=Z),None)
        if k is None:continue
        m[r],m[k]=m[k],m[r];v=inv(m[r][c]);m[r]=[mul(v,x)for x in m[r]]
        for k in range(r+1,rows):
            if m[k][c]!=Z:
                v=m[k][c];m[k]=[sub(x,mul(v,y))for x,y in zip(m[k],m[r])]
        r+=1
        if r==rows:break
    return r

ranks=[rank([[sector_columns[i][a][b] for i in range(16)]for a in range(N)])for b in range(N)]
assert ranks==[13,9,11,12,13,13,13,13,13,13,12,11,9]
wrong_sign=sum(total[r][c]!=const(qi(r*c))for r in range(N)for c in range(N))
omitted_scale=sum(scale(total[r][c],N)!=target[r][c]for r in range(N)for c in range(N))
perturbed_weight=sum(add(total[r][c],scale(last_inverse[r][c],ni))!=target[r][c]for r in range(N)for c in range(N))
assert (wrong_sign,omitted_scale,perturbed_weight)==(144,169,91)

source_pins=json.loads((BASE/'SOURCE_PINS.json').read_bytes());source_bindings=[]
for pin in source_pins:
    contents=(BASE/pin['local_path']).read_bytes()
    digest=hashlib.sha256(contents).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(contents)).encode()+b'\0'+contents).hexdigest()
    assert digest==pin['sha256'] and blob==pin['git_blob_sha'] and len(contents)==pin['bytes']
    source_bindings.append(dict(pin,checked_sha256=digest,checked_git_blob_sha=blob))

divisors=[2,3,5,7,11,13];divisor_product=math.prod(divisors)
assert divisor_product==30030
first_residual=next(d for d in range(2,100)if math.gcd(d,divisor_product)==1)
assert first_residual==17
receipts={
 'verdict':'PASS',
 'method':'Independent carry-free integer convolution / polynomial Euclid field arithmetic; literal finite geometric matrix series; direct left and right original-operator multiplication; inert JSON only',
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),
 'field':{'characteristic':P,'degree':D,'modulus_ascending':modulus,'frobenius_remainders':frob,'gcd_with_X53_minus_X':first_gcd,'schoolbook_crosschecks':len(tests)},
 'root_count':len(roots),'root_factorization_equalities':len(H),'root_frobenius':root_frob,
 'nonstable_same_sign_supports':True,'nonbase_cross_nodes':True,'gamma':gamma,
 'banks':16,'allocation':[7,1,1,7],'guards':guard_values,'raw_weight_equalities':weight_checks,'inverse_transform_equalities':amplitude_checks,
 'branch_inverses':208,'geometric_A13_entry_equalities':power_checks,'inverse_product_identities':416,'inverse_entry_equalities':inverse_checks,
 'branch_inverse_sha256':branch_hashes,'nonzero_bank_entry_counts':[sum(v!=Z for row in b for v in row)for b in physical],
 'bank_weyl_equalities':bank_weyl_checks,'sector_equalities':169,'sector_ranks':ranks,'target_entry_equalities':169,'target_mismatches':0,
 'wrong_sign_mismatches':wrong_sign,'omitted_normalization_mismatches':omitted_scale,'perturbed_final_weight_mismatches':perturbed_weight,
 'source_bindings':source_bindings,
 'predecessor_review_sha256':hashlib.sha256((BASE/'DEGREE11_ACCEPTED_REVIEW.md').read_bytes()).hexdigest(),
 'known_sufficient_divisors':divisors,'residual_coprimality_modulus':divisor_product,'first_residual_degree':first_residual,
 'scope':'Explicit degree-13 upper witness; equality uses inherited accepted field-uniform lower bound. Scalar extension when 13 divides d. No iff, residual-degree exclusion, historical novelty or FFT-runtime claim.'}
(OUT/'ARITHMETIC.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({k:receipts[k]for k in ['verdict','certificate_sha256','banks','branch_inverses','inverse_entry_equalities','target_mismatches','first_residual_degree']},indent=2))
print('Runtime seconds:',round(time.monotonic()-start,4),flush=True)
