#!/usr/bin/env python3
"""Independent controls. No candidate or prior checker is imported or run.
Exact symbolic matrices, quotient-ring norms, and outward rational intervals.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from math import gcd, isqrt
import hashlib, json
import sympy as S

ROOT=Path(__file__).resolve().parent
I=S.I

def simp(x): return S.simplify(S.expand_complex(x))
def mat(A): return A.applyfunc(simp)
def equal(A,B): assert all(simp(v)==0 for v in A-B)
def positive(x):
    z=simp(x)
    assert z.is_nonnegative is True, z

def minors(A):
    equal(A,A.H)
    out=[]
    for k in range(1,A.rows+1):
        for ix in combinations(range(A.rows),k):
            out.append((list(ix),simp(A.extract(ix,ix).det())))
    return out

def matrix_case(label,F,B,s,R,near):
    n=F.rows; q=S.Rational(s,n); a2=1-q; D=R-a2
    assert B.det()!=0
    equal(F*F.H,S.eye(n))
    M=mat(B.inv()); E=mat(M-F)
    H=mat(R*S.eye(n)-E*E.H)
    hm=minors(H)
    for ix,v in hm: positive(v)
    support=[[j for j in range(n) if simp(B[i,j])!=0] for i in range(n)]
    assert all(1<=len(t)<=s for t in support)
    if near:
        assert 0<=D<S.Rational(1,n)
        assert all(len(t)==s for t in support)
    else:
        assert D>=S.Rational(1,n)
    if any(len(t)!=s for t in support):
        # Saturation comes from the per-row lower floor, independently of mask extraction.
        assert any(R>=1-S.Rational(len(t),n) for t in support)
        return {'name':label,'N':n,'s':s,'R':str(R),'D':str(D),'supports':support,'branch':'unsaturated easy','H_minors':[str(v) for _,v in hm]}
    A=S.Matrix(n,n,lambda r,c:F[r,c] if r in support[c] else 0)
    C=mat(F-A); B0=mat(A.H/q); K=mat(q*B-A.H)
    P=mat(q*B*H*B.H+K*K.H); U=mat(q*D*B*B.H)
    Z=mat(C.H*C-a2*S.eye(n))
    equal(Z,U-P+K*C+C.H*K.H)
    pm=minors(P)
    for ix,v in pm: positive(v)
    u2=[];k2=[]
    for i in range(n):
        bn=simp((B*B.H)[i,i]); delta=simp(((B-B0)*(B-B0).H)[i,i])
        rn=simp((B*E*E.H*B.H)[i,i]); kn=simp((K*K.H)[i,i])
        assert simp(q*delta-rn+a2*bn)==0
        assert simp(P[i,i]-q*D*bn)==0
        assert simp(P[i,i]-U[i,i])==0
        assert Z[i,i]==0
        positive(q*D*bn-kn)
        u2.append(simp(q*D*bn));k2.append(kn)
    for i,j in combinations(range(n),2):
        for T in (U,P): positive(u2[i]*u2[j]-simp(T[i,j]*S.conjugate(T[i,j])))
        bound=2*S.sqrt(u2[i]*u2[j])+S.sqrt(a2*k2[i])+S.sqrt(a2*k2[j])
        positive(bound**2-simp(Z[i,j]*S.conjugate(Z[i,j])))
    # Correctness depends on cross-term sign, support matching, and diagonal normalization.
    assert any(simp(x)!=0 for x in Z-(U-P-K*C-C.H*K.H))
    bad=sum(1 for i,j in combinations(range(n),2) if Z[i,j]!=0)
    return {'name':label,'N':n,'s':s,'R':str(R),'D':str(D),'supports':support,'branch':'near' if near else 'saturated easy','bad_Gram_pairs':bad,'H_minors':[str(v) for _,v in hm], 'P_minors':[str(v) for _,v in pm]}

def matrix_tests():
    F4=S.Matrix(4,4,lambda r,c:(-I)**(r*c)/2)
    records=[]
    for d in (1,2):
        if d==1:
            cp=[{2},{0},{3},{1}]
        else:
            cp=[{0,3},{1,2},{0,3},{1,2}]
        C=S.Matrix(4,4,lambda r,c:F4[r,c] if r in cp[c] else 0)
        equal(C.H*C,S.Rational(d,4)*S.eye(4))
        A=F4-C; q=1-S.Rational(d,4); B0=mat(A.H/q)
        B=B0.copy()
        # Additive, differently phased perturbations, not row-scalings.
        for r in range(4):
            cols=[c for c in range(4) if B[r,c]!=0]
            B[r,cols[r%len(cols)]] += S.Rational(r+1,300)*(1+(-1)**r*I)
        records.append(matrix_case('additive_four_d'+str(d),F4,mat(B),4-d,S.Rational(d,4)+S.Rational(1,20),True))
    w=(-1-I*S.sqrt(3))/2
    F3=mat(S.Matrix(3,3,lambda r,c:w**((r*c)%3)/S.sqrt(3)))
    M=S.zeros(3)
    M[0,0]=(S.sqrt(3)+I)/4
    M[1,2]=M[2,1]=(-S.sqrt(3)+I)/4
    equal(mat((M-F3)*(M-F3).H),S.Rational(3,4)*S.eye(3))
    records.append(matrix_case('permuted_nonsharp_three',F3,mat(M.inv()),1,S.Rational(3,4),True))
    M2=mat(S.diag(1,(81+I)/80,(79-I)/80)*M)
    records.append(matrix_case('complex_perturbed_nonsharp_three',F3,mat(M2.inv()),1,S.Rational(4,5),True))
    # A false upper bound loses PSD; exact negative principal minor must witness this.
    Hbad=mat(S.Rational(7,10)*S.eye(3)-(M-F3)*(M-F3).H)
    neg=[(ix,str(v)) for ix,v in minors(Hbad) if v.is_negative is True]
    assert neg
    records.append(matrix_case('unsaturated_four_budget_two',F4,S.eye(4),2,S.Integer(4),False))
    # All support conditions cannot be replaced by one good row.
    B=S.eye(4); B[1,0]=S.Rational(1,3)
    assert sum(B[0,j]!=0 for j in range(4))==1
    assert not all(sum(B[i,j]!=0 for j in range(4))<=1 for i in range(4))
    return {'cases':records,'false_R_negative_minors':neg,'one_row_relaxation_rejected':True}

# Rigorous pi enclosure from exact alternating arctangent sums. The interval
# used below is independently rounded to decimal, then coordinate sine/cosine
# intervals are evaluated directly rather than using pairwise Gram cosines.
SCALE=1<<112

def atan(q,m):
    a=sum((Q((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(m)),Q(0))
    b=a+Q((-1)**m,(2*m+1)*q**(2*m+1))
    return min(a,b),max(a,b)

a,b=atan(5,60);c,d=atan(239,20)
pl,ph=16*a-4*d,16*b-4*c
D10=10**45
PLO=Q(3141592653589793238462643383279502884197169399,D10)
# Above fixed numerator uses 46 digits, i.e. 45 decimal places.
PHI=PLO+Q(1,D10)
assert PLO<=pl<ph<=PHI

def flo(q): return q.numerator//q.denominator
def cei(q): return -((-q.numerator)//q.denominator)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sq(a):
    if a[0]<=0<=a[1]: lo=0
    else:lo=min(a[0]*a[0],a[1]*a[1])
    return lo,max(a[0]*a[0],a[1]*a[1])

def trig(n,k):
    k%=n
    if 2*k>n:k-=n
    x=Q(2*k,n)*(PLO+PHI)/2
    dx=abs(Q(k,n))*(PHI-PLO)
    vals=[]
    # Polynomial partial sums with absolute Lagrange remainder and Lipschitz
    # error from replacing pi by the midpoint; all operations are rational.
    for parity in (0,1):
        term=Q(1) if parity==0 else x
        t=term
        for j in range(1,29):
            power=2*j+parity
            term *= -x*x/Q((power-1)*power)
            t += term
        degree=56+parity
        from math import factorial
        err=abs(x)**(degree+1)/factorial(degree+1)+dx
        vals.append((flo((t-err)*SCALE),cei((t+err)*SCALE)))
    return tuple(vals)

CACHE={}
def roots(n):
    if n not in CACHE:CACHE[n]=[trig(n,k) for k in range(n)]
    return CACHE[n]
def norm_interval(n,exps):
    rr=roots(n); re=(0,0);im=(0,0)
    for k in exps:
        c,s=rr[k%n];re=add(re,c);im=add(im,s)
    a,b=sq(re),sq(im)
    return a[0]+b[0],a[1]+b[1]

def geometry_tests():
    records=[]; pc=tc=0
    dims=list(range(3,65))+[73,89,101,127,128,181,200,257]
    for n in dims:
        np=nt=0;minlo=None
        for k in range(n):
            lo,hi=norm_interval(n,[0,k])
            if n%2==0 and k==n//2:
                assert lo==0
                continue
            coeff=4 if n%2 else 16
            assert lo*n*n>=coeff*SCALE*SCALE,(n,k)
            np+=1
        if n%3:
            for a,b in combinations_with_replacement(range(n),2):
                lo,hi=norm_interval(n,[0,a,b])
                assert lo*n*n>=SCALE*SCALE,(n,a,b)
                v=(lo*n*n*1000000)//(SCALE*SCALE)
                minlo=v if minlo is None else min(minlo,v)
                nt+=1
            assert all(abs(3*k-n)>=1 for k in range(n//2+1))
        pc+=np;tc+=nt
        records.append({'N':n,'nonzero_pairs':np,'triples':nt,'minimum_N2_modulus2_lower_millionths':minlo})
    x=S.Symbol('x');zeros=[]
    for n in [3,6,12,21,51,99]:
        f=S.Poly(S.cyclotomic_poly(n,x),x)
        assert S.Poly(1+x**(n//3)+x**(2*n//3),x).rem(f).is_zero
        zeros.append(n)
    return {'coordinate_interval_bits':112,'dimensions':records,'nonzero_pairs':pc,'triple_patterns':tc,'divisible_by_three_negative_controls':zeros}

def cyclotomic_tests():
    x=S.Symbol('x');rows=[];count=zeros=real=0
    for n in range(3,29):
        f=S.Poly(S.cyclotomic_poly(n,x),x,domain=S.ZZ); h=f.degree()
        units=[a for a in range(1,n) if gcd(a,n)==1]
        pairs=[a for a in units if a<n-a]
        assert h==len(units)==2*len(pairs)
        patterns=[[0],[0,0],[0,2],[0,n//2],[0,n//3,2*n//3],[0,1,n-1],[0,1,1,n-1],[0,0,n//2,n//2]]
        nz=nr=0
        for exps in patterns:
            p=S.Poly(sum(x**(e%n) for e in exps),x,domain=S.ZZ).rem(f)
            pb=S.Poly(sum(x**((-e)%n) for e in exps),x,domain=S.ZZ).rem(f)
            # Field norm by determinant of multiplication, not a resultant.
            cols=[(p*S.Poly(x**j,x)).rem(f) for j in range(h)]
            mult=S.Matrix(h,h,lambda i,j:cols[j].nth(i))
            norm=int(mult.det(method='domain-ge'))
            product=S.Poly(1,x,domain=S.ZZ)
            for a in pairs:
                pa=S.Poly(sum(x**((a*e)%n) for e in exps),x,domain=S.ZZ).rem(f)
                pba=S.Poly(sum(x**((-a*e)%n) for e in exps),x,domain=S.ZZ).rem(f)
                product=(product*pa*pba).rem(f)
            assert product==S.Poly(norm,x,domain=S.ZZ)
            count+=1
            if p.is_zero:
                assert norm==0;zeros+=1;nz+=1;continue
            t=len(exps)
            assert 1<=norm<=t**h
            if p==pb:real+=1;nr+=1
            q=(p*pb).rem(f)
            threshold=Q(1,t**(h-2))
            if q.degree()==0 and Q(int(q.nth(0)))==threshold:
                pass
            else:
                lo,hi=norm_interval(n,exps)
                assert lo*t**(h-2)>=SCALE*SCALE,(n,exps)
        rows.append({'N':n,'phi':h,'patterns':len(patterns),'zero_patterns':nz,'real_nonzero_patterns':nr})
    # Dropping the paired factor structure and asserting |xi|>=1 is false.
    lo,hi=norm_interval(5,[0,2]);assert hi<SCALE*SCALE
    return {'dimensions':rows,'patterns':count,'zero_patterns':zeros,'real_nonzero_patterns':real,'wrong_unit_separation_rejected':True}

def scalar_tests():
    a,r,q=S.symbols('a r q',positive=True)
    eta=2*r*(a+r)
    # sqrt(a*a+2*eta)=a+2*r, hence the closed expression matches the solved form.
    assert S.factor(eta/(2*a+2*r+eta/S.sqrt(q))-r/(1+r/S.sqrt(q)))==0
    z=r/(1+r/S.sqrt(q))
    assert S.simplify(z/(1-z/S.sqrt(q))-r)==0
    assert Q(18)<Q(81,4) # 11/2+3sqrt(2)<10.
    count=0
    for n in range(3,251):
        h=int(S.totient(n));assert h%2==0
        for s in range(1,n-1):
            d=n-s;eta=Q(1,n*d**(h//2-1));a2=Q(d,n);q=Q(s,n)
            assert eta<=Q(1,n)
            assert eta/a2<=Q(1,2)
            assert eta*eta/(a2*q)<=Q(1,2)
            new=eta*eta/(10*a2)
            assert new==Q(1,10*n*d**(h-1))
            old=Q(s**6,2**22*n**10*d**(2*h-2))
            assert new>old
            assert eta*eta/(4*a2)<Q(1,n)
            count+=1
        if n%2:
            assert Q(2,n*n)**2/(10*Q(2,n))==Q(1,5*n**3)
        if n>=4 and n%3:
            assert Q(1,n*n)**2/(10*Q(3,n))==Q(1,30*n**3)
    return {'budget_pairs':count,'max_N':250,'symbolic_radical_inversion':True,'clean_constant_exact':True,'easy_branch_exact':True}

def main():
    out={'independent':True,'candidate_checker_imported_or_run':False,'all_decisions_exact_or_outward_interval':True}
    for name,fn in [('matrix',matrix_tests),('scalar',scalar_tests),('cyclotomic',cyclotomic_tests),('geometry',geometry_tests)]:
        out[name]=fn();print(name+' PASS',flush=True)
    out['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();out['verdict']='PASS'
    (ROOT/'FRESH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',flush=True)
if __name__=='__main__':main()
