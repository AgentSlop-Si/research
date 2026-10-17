#!/usr/bin/env python3
"""Fresh degree-seven field and literal original-bank certificate.

Uses only inert witness JSON and Python standard library. Does not import the
discovery checker, historical programs, or third-party scientific packages.
"""
import json
import hashlib
from pathlib import Path
from functools import lru_cache
from time import monotonic

ROOT=Path(__file__).resolve().parent
P=53
D=7
MOD=(25,25,4,31,25,9,40,1)
ZERO=(0,)*D
ONE=(1,)+(0,)*(D-1)

def field(n): return (n%P,)+(0,)*(D-1)
def add(a,b): return tuple((x+y)%P for x,y in zip(a,b))
def neg(a): return tuple(-x%P for x in a)
def sub(a,b): return tuple((x-y)%P for x,y in zip(a,b))
def scale(a,n): return tuple(x*n%P for x in a)

def mul(a,b):
    if a==ZERO or b==ZERO: return ZERO
    if not any(a[1:]): return scale(b,a[0])
    if not any(b[1:]): return scale(a,b[0])
    out=[0]*(2*D-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: out[i+j]+=x*y
    for k in range(2*D-2,D-1,-1):
        c=out[k]%P
        if c:
            for j in range(D): out[k-D+j]-=c*MOD[j]
    return tuple(x%P for x in out[:D])

def power(a,n):
    out=ONE
    while n:
        if n&1: out=mul(out,a)
        n//=2
        if n: a=mul(a,a)
    return out

@lru_cache(maxsize=None)
def inverse(a):
    assert a!=ZERO
    out=power(a,P**D-2)
    assert mul(a,out)==ONE
    return out

def poly_trim(a):
    a=[x%P for x in a]
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def poly_rem(a,b):
    a=poly_trim(a); b=poly_trim(b); iv=pow(b[-1],-1,P)
    while a!=[0] and len(a)>=len(b):
        c=a[-1]*iv%P;k=len(a)-len(b)
        for j,x in enumerate(b): a[k+j]=(a[k+j]-c*x)%P
        a=poly_trim(a)
    return a

def poly_gcd(a,b):
    while b!=[0]: a,b=b,poly_rem(a,b)
    return [x*pow(a[-1],-1,P)%P for x in a]

def matrix_inverse(A):
    n=len(A)
    M=[r[:]+[ONE if i==j else ZERO for j in range(n)] for i,r in enumerate(A)]
    for col in range(n):
        k=next(i for i in range(col,n) if M[i][col]!=ZERO)
        M[col],M[k]=M[k],M[col]
        iv=inverse(M[col][col]); M[col]=[mul(iv,x) for x in M[col]]
        for i in range(n):
            if i!=col and M[i][col]!=ZERO:
                c=M[i][col]
                M[i]=[sub(x,mul(c,y)) for x,y in zip(M[i],M[col])]
    assert all(M[i][j]==(ONE if i==j else ZERO) for i in range(n) for j in range(n))
    return [r[n:] for r in M]

def dot(a,b):
    out=ZERO
    for x,y in zip(a,b): out=add(out,mul(x,y))
    return out

def matrix_mul(A,B):
    cols=list(zip(*B))
    return [[dot(r,c) for c in cols] for r in A]

def identity(n): return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]

def main():
    start=monotonic()
    w=json.loads((ROOT/'DEGREE7_WITNESS.json').read_text())
    assert w['y']==2 and w['lambda']==40 and tuple(w['H'])==MOD
    u=(0,1,0,0,0,0,0)
    roots=[]; a=u
    for _ in range(D): roots.append(a); a=power(a,P)
    assert a==u
    assert len(set(roots))==D and ZERO not in roots
    # Prime degree 7: Frobenius^7 identity plus gcd with X^53-X proves
    # irreducibility over F53. No factor library is trusted.
    u53=power(u,53)
    x53minusx=list(sub(u53,u))
    g=poly_gcd(list(MOD),poly_trim(x53minusx))
    assert g==[1]
    product=[ONE]
    for a in roots:
        nxt=[ZERO]*(len(product)+1)
        for i,c in enumerate(product):
            nxt[i]=sub(nxt[i],mul(a,c));nxt[i+1]=add(nxt[i+1],c)
        product=nxt
    assert product==[field(x) for x in MOD]
    assert all(sum(MOD[i]*pow(t,i,P) for i in range(8))%P for t in range(P))
    V=[[power(a,k) for a in roots] for k in range(7)]
    Vinv=matrix_inverse(V)
    assert matrix_mul(V,Vinv)==identity(7) and matrix_mul(Vinv,V)==identity(7)
    banks=[{'epsilon':1,'delta':1,'alpha':a} for a in roots]
    banks += [{'epsilon':-1,'delta':1,'alpha':field(2)},{'epsilon':1,'delta':-1,'alpha':field(2)}]
    banks += [{'epsilon':-1,'delta':-1,'alpha':a} for a in roots]
    for bank in banks: bank['beta']=ONE;bank['sector_amplitudes']=[]
    for sector in w['sectors']:
        c=sector['solution']; plus=[dot(row,[field(x) for x in c[:7]]) for row in Vinv]
        minus=[dot(row,[field(x) for x in c[9:]]) for row in Vinv]
        amplitudes=plus+[field(c[7]),field(c[8])]+minus
        for bank,A in zip(banks,amplitudes):bank['sector_amplitudes'].append(A)
    assert all(any(A!=ZERO for A in bank['sector_amplitudes']) for bank in banks)
    gamma=sum(pow(16,-t*t%13,P) for t in range(13))*pow(13,-1,P)%P
    assert gamma==7
    for bank in banks:
        a=bank['alpha'];e=bank['epsilon'];Delta=neg(power(a,13))
        assert Delta!=ZERO;bank['Delta']=Delta
        bank['raw_weights']=[mul(scale(Delta,gamma),dot(bank['sector_amplitudes'],[field(pow(16,-e*b*j%13,P)) for b in range(13)])) for j in range(13)]
        for b,A in enumerate(bank['sector_amplitudes']):
            reconstructed=mul(inverse(scale(Delta,13*gamma)),dot(bank['raw_weights'],[field(pow(16,e*b*j%13,P)) for j in range(13)]))
            assert reconstructed==A
    # Independently rebuild every full actual-root sector, using the finite
    # Gaussian recurrence instead of the discovery product implementation.
    def gaussian_recurrence(r,l,omega):
        table=[[0]*(l+1) for _ in range(r+1)]
        for i in range(r+1):
            for j in range(l+1):
                if i==0 or j==0: table[i][j]=1
                else: table[i][j]=(table[i-1][j]+pow(omega,i,P)*table[i][j-1])%P
        return table[r][l]
    sector_rows=0
    for b in range(13):
        for a in range(13):
            total=ZERO
            for bank in banks:
                e,d=bank['epsilon'],bank['delta'];r=e*a%13;l=d*b%13
                G=gaussian_recurrence(r,l,pow(16,e*d%13,P)) if r+l<13 else 0
                total=add(total,scale(mul(power(bank['alpha'],r),bank['sector_amplitudes'][b]),G))
            assert total==field(pow(16,10*(a+b)**2%13,P))
            sector_rows+=1
    aggregate=[[ZERO for _ in range(13)] for _ in range(13)]
    branch_count=0;inverse_checks=0;mutated=None;nonzero_banks=0
    for bank_index,bank in enumerate(banks):
        e,d=bank['epsilon'],bank['delta'];alpha=bank['alpha']
        bank_matrix=[[ZERO for _ in range(13)] for _ in range(13)]
        for j in range(13):
            diagonal=[field(1-pow(16,(e*d*j+d*t)%13,P)) for t in range(13)]
            M=[[ZERO for _ in range(13)] for _ in range(13)]
            for t in range(13): M[t][t]=diagonal[t];M[(t+e)%13][t]=neg(alpha)
            Inv=matrix_inverse(M)
            # Exact two-sided multiplication by the original sparse M.
            for row in range(13):
                for col in range(13):
                    expect=ONE if row==col else ZERO
                    assert sub(mul(diagonal[row],Inv[row][col]),mul(alpha,Inv[(row-e)%13][col]))==expect
                    assert sub(mul(Inv[row][col],diagonal[col]),mul(alpha,Inv[row][(col+e)%13]))==expect
            inverse_checks+=2;branch_count+=1
            weighted=scale(bank['raw_weights'][j],pow(13,-1,P))
            for row in range(13):
                for col in range(13): bank_matrix[row][col]=add(bank_matrix[row][col],mul(weighted,Inv[row][col]))
            if bank_index==15 and j==12: mutated=Inv
        assert any(x!=ZERO for row in bank_matrix for x in row);nonzero_banks+=1
        for row in range(13):
            for col in range(13): aggregate[row][col]=add(aggregate[row][col],bank_matrix[row][col])
    target=[[field(pow(16,-k*t%13,P)) for t in range(13)] for k in range(13)]
    mismatches=sum(aggregate[k][t]!=target[k][t] for k in range(13) for t in range(13))
    assert mismatches==0
    missing_normalization=sum(scale(aggregate[k][t],13)!=target[k][t] for k in range(13) for t in range(13))
    opposite_sign=sum(aggregate[k][t]!=field(pow(16,k*t%13,P)) for k in range(13) for t in range(13))
    perturbed=sum(add(aggregate[k][t],scale(mutated[k][t],pow(13,-1,P)))!=target[k][t] for k in range(13) for t in range(13))
    assert missing_normalization and opposite_sign and perturbed
    certificate={'field':{'characteristic':P,'degree':D,'modulus_increasing':MOD,'encoding':'[a0,...,a6] = sum ai*u^i'},'cross_y':2,'cross_z':2,'lambda':40,'Hplus':MOD,'Hminus':MOD,'roots':roots,'banks':banks,'aggregate':aggregate}
    (ROOT/'DEGREE7_LITERAL_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
    receipt={'result':'PASS','irreducibility':{'frobenius7_u_equals_u':True,'gcd_H_x53_minus_x':g,'degree_is_prime':True},'distinct_nonzero_roots':7,'root_product_matches_H':True,'complete_actual_root_sector_rows':sector_rows,'physical_banks':len(banks),'effective_nonzero_banks':nonzero_banks,'legal_guards':16,'original_branch_inverses':branch_count,'two_sided_inverse_checks':inverse_checks,'fourier_entries_checked':169,'fourier_entry_mismatches':mismatches,'falsification_mismatches':{'omit_1_over_13':missing_normalization,'opposite_Fourier_sign':opposite_sign,'perturb_last_bank_last_weight':perturbed},'seconds':round(monotonic()-start,3)}
    (ROOT/'LITERAL_CHECK_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
