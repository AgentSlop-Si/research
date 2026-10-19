#!/usr/bin/env python3
"""Original-operator verification from inert JSON, with a different inverse algorithm.

No discovery/C++ program or historical scientific program is imported.
Python standard library only. Polynomial coefficients are ascending.
"""
import json,hashlib,time
from pathlib import Path
R=Path(__file__).resolve().parent
P=53;D=31;MOD=[11,2]+[0]*29+[1]
def trim(a):
    a=[x%P for x in a]
    while len(a)>1 and not a[-1]:a.pop()
    return a
def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def prem(a,b):
    a=trim(a);inv=pow(b[-1],-1,P)
    while len(a)>=len(b) and a!=[0]:
        c=a[-1]*inv%P;k=len(a)-len(b)
        for j,v in enumerate(b):a[j+k]-=c*v
        a=trim(a)
    return a
def pgcd(a,b):
    while b!=[0]:a,b=b,prem(a,b)
    inv=pow(a[-1],-1,P)
    return trim([inv*x for x in a])
def ppow(a,n,h):
    b=[1]
    while n:
        if n&1:b=prem(pmul(b,a),h)
        n//=2
        if n:a=prem(pmul(a,a),h)
    return b

ZERO=(0,)*D
ONE=(1,)+(0,)*(D-1)
def scalar(n):return (n%P,)+(0,)*(D-1)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def neg(a):return tuple(-x%P for x in a)
def sub(a,b):return tuple((x-y)%P for x,y in zip(a,b))
def scale(a,s):return tuple(x*s%P for x in a)
def mul(a,b):
    if a==ZERO or b==ZERO:return ZERO
    if not any(a[1:]):return scale(b,a[0])
    if not any(b[1:]):return scale(a,b[0])
    c=[0]*(2*D-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    # General monic polynomial division, independently implemented.
    for k in range(2*D-2,D-1,-1):
        q=c[k]%P
        for j,v in enumerate(MOD[:-1]):
            if v:c[k-D+j]-=q*v
    return tuple(x%P for x in c[:D])
def power(a,n):
    z=ONE
    while n:
        if n&1:z=mul(z,a)
        n//=2
        if n:a=mul(a,a)
    return z
def inverse(a):
    assert a!=ZERO
    z=power(a,P**D-2);assert mul(a,z)==ONE
    return z
def invbranch(alpha,epsilon,delta,j):
    # M[r,r]=1-q^(epsilon*delta*j+delta*r),
    # M[r+epsilon,r]=-alpha. The sole zero diagonal fixes one coordinate;
    # then solve backward using alpha^{-1}. No Gaussian elimination.
    diag=[(1-pow(16,(epsilon*delta*j+delta*r)%13,P))%P for r in range(13)]
    r0=(-epsilon*j)%13
    assert [r for r,d in enumerate(diag) if d==0]==[r0]
    ai=inverse(alpha);out=[[ZERO]*13 for _ in range(13)]
    for col in range(13):
        r=(r0-epsilon)%13
        out[r][col]=neg(ai) if col==r0 else ZERO
        for k in range(12):
            value=scale(out[r][col],diag[r])
            if r==col:value=sub(value,ONE)
            out[(r-epsilon)%13][col]=mul(ai,value)
            r=(r-epsilon)%13
    for r in range(13):
        for c in range(13):
            left=sub(scale(out[r][c],diag[r]),mul(alpha,out[(r-epsilon)%13][c]))
            right=sub(scale(out[r][c],diag[c]),mul(alpha,out[r][(c+epsilon)%13]))
            assert left==(ONE if r==c else ZERO)
            assert right==(ONE if r==c else ZERO)
    return out

def main():
    start=time.time()
    assert all(P%d for d in range(2,8)) and all(D%d for d in range(2,6))
    assert pow(16,13,P)==1 and 16!=1
    # Exact irreducibility before any extension-field inverse is used.
    frob=[0,1];remainders=[]
    for i in range(D):
        frob=ppow(frob,P,MOD);remainders.append(frob)
    assert frob==[0,1]
    first=ppow([0,1],P,MOD);first+=( [0]*max(0,2-len(first)) );first[1]=(first[1]-1)%P
    assert pgcd(MOD,trim(first))==[1]
    # Since 31 is prime, all irreducible factors have degree 1 or 31;
    # no degree-one factor and total degree 31 prove irreducibility.
    data=json.loads((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_text())
    assert data['field_modulus_ascending']==MOD and data['degree']==31 and data['characteristic']==53
    def element(a):
        assert isinstance(a,list) and len(a)==D
        assert all(type(x) is int and 0<=x<P for x in a)
    for a in [data['y'],data['z']]+data['H']+data['roots']:element(a)
    assert len(data['matrix'])==13 and all(len(row)==13 for row in data['matrix'])
    for row in data['matrix']:
        for a in row:element(a)
    for bank in data['banks']:
        for a in [bank['alpha'],bank['guard']]+bank['amplitudes']+bank['weights']:element(a)
    H=[tuple(a) for a in data['H']];roots=[tuple(a) for a in data['roots']]
    assert len(H)==8 and H[-1]==ONE and H[0]!=ZERO
    assert len(roots)==7 and len(set(roots))==7 and all(x!=ZERO for x in roots)
    product=[ONE]
    for x in roots:
        nxt=[ZERO]*(len(product)+1)
        for i,c in enumerate(product):nxt[i]=sub(nxt[i],mul(x,c));nxt[i+1]=add(nxt[i+1],c)
        product=nxt
        assert power(x,P**D)==x
    assert product==H
    assert any(any(c[1:]) for c in H)
    assert any(data['y'][1:]) and data['y']==data['z']
    rootset=set(roots)
    assert {power(x,P) for x in roots}!=rootset
    banks=data['banks'];assert len(banks)==16
    counts={};supports={};total=[[ZERO]*13 for _ in range(13)]
    nonzero_banks=[];raw_amplitude_checks=0;guard_checks=0;lastinv=None
    for bi,bank in enumerate(banks):
        e,d=bank['epsilon'],bank['delta'];assert e in [-1,1] and d in [-1,1]
        alpha=tuple(bank['alpha']);beta=bank['beta'];assert alpha!=ZERO and beta==1
        orient=(e,d);counts[orient]=counts.get(orient,0)+1;supports.setdefault(orient,[]).append(alpha)
        guard=sub(ONE,add(power(alpha,13),scalar(pow(beta,13,P))))
        assert guard!=ZERO and guard==tuple(bank['guard']);guard_checks+=1
        weights=[tuple(w) for w in bank['weights']];amplitudes=[tuple(a) for a in bank['amplitudes']]
        assert len(weights)==len(amplitudes)==13
        deninv=inverse(scale(guard,13*7))
        for b in range(13):
            v=ZERO
            for j,w in enumerate(weights):v=add(v,scale(w,pow(16,(e*b*j)%13,P)))
            assert mul(v,deninv)==amplitudes[b];raw_amplitude_checks+=1
        B=[[ZERO]*13 for _ in range(13)]
        for j,w in enumerate(weights):
            inv=invbranch(alpha,e,d,j)
            for r in range(13):
                for c in range(13):B[r][c]=add(B[r][c],scale(mul(w,inv[r][c]),pow(13,-1,P)))
            lastinv=inv
        nz=sum(v!=ZERO for row in B for v in row);assert nz>0;nonzero_banks.append(nz)
        for r in range(13):
            for c in range(13):total[r][c]=add(total[r][c],B[r][c])
        print('independent original-bank verification',bi+1,flush=True)
    assert counts=={(1,1):7,(-1,1):1,(1,-1):1,(-1,-1):7}
    assert set(supports[1,1])==set(supports[-1,-1])==rootset
    assert supports[-1,1]==[tuple(data['y'])] and supports[1,-1]==[tuple(data['z'])]
    sector_checks=0
    def gaussian(e,d,a,b):
        r=e*a%13;l=d*b%13
        if r+l>=13:return 0
        w=pow(16,e*d%13,P);v=1
        for i in range(1,l+1):v=v*(1-pow(w,r+i,P))*pow((1-pow(w,i,P))%P,-1,P)%P
        return v
    for b in range(13):
        for a in range(13):
            v=ZERO
            for bank in banks:
                e,d=bank['epsilon'],bank['delta']
                v=add(v,scale(mul(tuple(bank['amplitudes'][b]),power(tuple(bank['alpha']),e*a%13)),gaussian(e,d,a,b)))
            assert v==scalar(pow(16,10*(a+b)**2%13,P));sector_checks+=1
    wrong_sign=omitted13=perturbed=0
    for r in range(13):
        for c in range(13):
            target=scalar(pow(16,(-r*c)%13,P))
            assert total[r][c]==target==tuple(data['matrix'][r][c])
            wrong_sign+=total[r][c]!=scalar(pow(16,(r*c)%13,P))
            omitted13+=scale(total[r][c],13)!=target
            perturbed+=add(total[r][c],scale(lastinv[r][c],pow(13,-1,P)))!=target
    assert min(wrong_sign,omitted13,perturbed)>0
    out={'verdict':'PASS','field_irreducibility':{'modulus_ascending':MOD,'prime_degree':31,'frobenius31_remainder':frob,'gcd_with_X53_minus_X':[1],'all_frobenius_remainders':remainders},'full_sector_equalities':sector_checks,'banks':16,'nonbase_cross_nodes':True,'nonstable_same_sign_supports':True,'root_factorization_equalities':8,'distinct_nonzero_roots':7,'nonzero_guards':guard_checks,'raw_amplitude_equalities':raw_amplitude_checks,'literal_branch_inverses':208,'left_and_right_inverse_identities':416,'inverse_entry_equalities':416*169,'target_entry_equalities':169,'nonzero_bank_entry_counts':nonzero_banks,'wrong_fourier_sign_mismatches':wrong_sign,'omitted_one_over_13_mismatches':omitted13,'one_weight_perturbation_mismatches':perturbed,'certificate_sha256':hashlib.sha256((R/'DEGREE31_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest(),'runtime_seconds':time.time()-start,'method':'Independent Python polynomial field arithmetic, zero-diagonal backward inverse recurrence, literal sparse left/right matrix products and original raw bank sum; inert JSON only','review_status':'same-author independent implementation, not independent reviewer acceptance'}
    (R/'INDEPENDENT_LITERAL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
