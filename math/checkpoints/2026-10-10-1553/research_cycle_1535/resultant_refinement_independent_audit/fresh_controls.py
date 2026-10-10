#!/usr/bin/env python3
"""Independent exact controls. No project/source program is imported or executed."""
from fractions import Fraction
from math import gcd
from random import Random
from pathlib import Path
import hashlib, json, time
import sympy as sp

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
SOURCES = [ROOT/'research_cycle_0958/algebra/final_v1/PROOF_CLOSURE.md', ROOT/'research_cycle_1453/novelty_resultant/RESULTANT_NOVELTY_VERDICT.md']
def hashes(): return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCES}
BEFORE=hashes()
rng=Random(100101535)
checks=[]

def det(M):
    """Fraction-free integer determinant, allowing swaps; independent of SymPy."""
    a=[list(map(int,row)) for row in M]; n=len(a)
    if n==0:return 1
    last=1; sign=1
    for k in range(n-1):
        if a[k][k]==0:
            s=next((i for i in range(k+1,n) if a[i][k]),None)
            if s is None:return 0
            a[k],a[s]=a[s],a[k];sign=-sign
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=a[i][j]*p-a[i][k]*a[k][j]
                assert num%last==0
                a[i][j]=num//last
        for i in range(k+1,n):a[i][k]=0
        last=p
    return sign*a[-1][-1]

def detq(M):
    a=[[Fraction(x) for x in row] for row in M];n=len(a);ans=Fraction(1)
    for k in range(n):
        if not a[k][k]:
            s=next((i for i in range(k+1,n) if a[i][k]),None)
            if s is None:return Fraction(0)
            a[k],a[s]=a[s],a[k];ans=-ans
        p=a[k][k];ans*=p
        for i in range(k+1,n):
            ratio=a[i][k]/p
            for j in range(k+1,n):a[i][j]-=ratio*a[k][j]
    return ans

def sylvester(f,g):
    # f,g are ascending formal coefficients, including zero padding.
    m=len(f)-1; n=len(g)-1
    return [[0]*i+list(reversed(f))+[0]*(n-1-i) for i in range(n)] + [[0]*i+list(reversed(g))+[0]*(m-1-i) for i in range(m)]

def coeffs_at(M,e,w):
    # Fresh permutation expansion of det(M_ij*(1-a*w**(e+i+j))).
    import itertools
    m=len(M);out=[0]*(m+1)
    for perm in itertools.permutations(range(m)):
        inv=sum(perm[i]>perm[j] for i in range(m) for j in range(i+1,m))
        c=[(-1)**inv]
        for i,j in enumerate(perm):
            nc=[0]*(len(c)+1)
            for k,x in enumerate(c):
                nc[k]+=x*M[i][j];nc[k+1]-=x*M[i][j]*w**(e+i+j)
            c=nc
        out=[x+y for x,y in zip(out,c)]
    return out

def coeffs_poly(M,e,w):return list(map(sp.expand,coeffs_at(M,e,w)))
def kron(A,B):return [[A[i][j]*B[k][l] for j in range(len(A)) for l in range(len(B))] for i in range(len(A)) for k in range(len(B))]
def s_at(n,w):
    if n>0:return sum(w**r for r in range(n))
    return -sum(w**r for r in range(n,0))
def N_at(A,B,w):
    m=len(A)
    return [[A[i][j]*B[k][l]*s_at(1+k-i+l-j,w) for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
def minors_product(A,B):
    m=len(A);p=(-1)**(m*(m-1)//2)*det(A)*det(B)
    for M in (A,B):
        for t in range(1,m):
            p*=det([r[:t] for r in M[:t]])*det([r[m-t:] for r in M[m-t:]])
    return p

def no_pivot(M,p):
    a=[[x%p for x in r] for r in M];n=len(a)
    for k in range(n):
        if a[k][k]==0:return False
        inv=pow(a[k][k],-1,p)
        for i in range(k+1,n):
            q=a[i][k]*inv%p
            for j in range(k+1,n):a[i][j]=(a[i][j]-q*a[k][j])%p
    return True

def full_degree_test(A,B,p):
    return all(no_pivot(M,p) for M in (A,B,[r[::-1] for r in A[::-1]],[r[::-1] for r in B[::-1]]))

def record(kind,**kw):checks.append({'kind':kind,**kw})

# Exact polynomial tests: use explicit fixed-grade Sylvester matrices, never sp.resultant.
w,x=sp.symbols('w x')
poly_cases=[]
for m in (1,2,3,4):
    cases=[('identity',sp.eye(m).tolist(),sp.eye(m).tolist())]
    for s in range(0 if m==4 else (2 if m==3 else 4)):
        cases.append((f'random_{s}',[[rng.randrange(-2,3) for _ in range(m)] for _ in range(m)],[[rng.randrange(-2,3) for _ in range(m)] for _ in range(m)]))
    if m>=3:
        cases.append(('dense_full_degree', [[(m+1+i) if i==j else 1 for j in range(m)] for i in range(m)], [[(m+2+i) if i==j else (-1 if i>j else 1) for j in range(m)] for i in range(m)]))
    cases += [('zero_A',[[0]*m for _ in range(m)],sp.eye(m).tolist())]
    if m==2:cases += [('singular_constant_nonconstant_pencil',[[1,1],[1,1]],[[1,2],[3,4]])]
    for label,A,B in cases:
        f=coeffs_poly(A,0,w);g=coeffs_poly(B,1,w)
        R=sp.Poly(sp.Matrix(sylvester(f,g)).det(method='domain-ge'),w)
        v=m*(m-1)*(4*m+1)//6;b=m*(m-1)*(2*m-1)//6;n=m*m;L=m*m*(m-1)
        U,rem=sp.div(R,sp.Poly(w**v*(w-1)**n,w));assert rem.is_zero
        # Reconstruct V by triangular subtraction, avoiding division by 2.
        rest=sp.expand(U.as_expr());V=0
        for j in range(b,-1,-1):
            c=sp.expand(rest).coeff(w,b+j)
            term=sp.expand(w**b*(w+w**-1)**j)
            rest=sp.expand(rest-c*term);V+=c*x**j
        assert rest==0
        V=sp.Poly(V,x);lc=V.nth(b)
        assert lc==minors_product(A,B)
        # Direct determinant uses independent rational Gaussian elimination.
        for node in (Fraction(2),Fraction(3),Fraction(-2),Fraction(1,2)):
            nx=node+1/node
            dv=detq(N_at(A,B,node)); vv=Fraction(int(V.eval(nx).p),int(V.eval(nx).q))
            assert dv==vv
            rv=detq(sylvester(coeffs_at(A,0,node),coeffs_at(B,1,node)))
            assert rv==node**L*(node-1)**n*dv
        K=kron(A,B)
        even=[i*m+k for i in range(m) for k in range(m) if (i+k)%2==0]
        odd=[i*m+k for i in range(m) for k in range(m) if (i+k)%2]
        blockprod=det([[K[i][j] for j in even] for i in even])*det([[K[i][j] for j in odd] for i in odd])
        assert V.eval(-2)==blockprod
        assert V.eval(2)==det(N_at(A,B,1))
        # Independently inspect the tangent resultant, with explicit coefficient padding.
        t=sp.symbols('t'); Am=sp.Matrix(A);Bm=sp.Matrix(B);H=sp.diag(*range(m))
        Ca=H*Am+Am*H;Cb=H*Bm+Bm*H+Bm
        pf=sp.Poly((t*Am+Ca).det(method='domain-ge'),t)
        pg=sp.Poly((t*Bm+Cb).det(method='domain-ge'),t)
        ts=sp.Matrix(sylvester([pf.nth(k) for k in range(m+1)],[pg.nth(k) for k in range(m+1)])).det()
        assert ts==V.eval(2)
        record('tangent_resultant',m=m,case=label,determinant=str(ts))
        if Am.det()!=0 and Bm.det()!=0:
            pa=sp.Poly((-Am.inv()*Ca).charpoly(t).as_expr(),t)
            pb=sp.Poly((-Bm.inv()*Cb).charpoly(t).as_expr(),t)
            nr=sp.Matrix(sylvester([pa.nth(k) for k in range(m+1)],[pb.nth(k) for k in range(m+1)])).det()
            assert nr*(Am.det()*Bm.det())**m==V.eval(2)
            record('normalized_nonsingular_tangent',m=m,case=label)
        if not R.is_zero:
            d=int(V.degree());terms=R.terms();order0=min(z[0][0] for z in terms)
            assert order0==v+b-d
            assert R.degree()==v+b+n+d
            for center,extra in ((1,n),(-1,0)):
                rr=R;ordr=0
                while rr.eval(center)==0:
                    rr,rem=sp.div(rr,sp.Poly(w-center,w));assert rem.is_zero;ordr+=1
                vv=V;ordv=0
                while vv.eval(2*center)==0:
                    vv,rem=sp.div(vv,sp.Poly(x-2*center,x));assert rem.is_zero;ordv+=1
                assert ordr==extra+2*ordv
        record('polynomial',m=m,case=label,A=A,B=B,R_degree=None if R.is_zero else int(R.degree()),V=str(V.as_expr()),leading_coefficient=str(lc))
        poly_cases.append((m,label,A,B,R,V))

# Larger exact specializations; no polynomial/resultant implementation reused.
for m in (1,2,3,4,5):
    for sample in range(4):
        A=[[rng.randrange(-2,3) for _ in range(m)] for _ in range(m)]
        B=[[rng.randrange(-2,3) for _ in range(m)] for _ in range(m)]
        for node in (2,-2,3):
            R=det(sylvester(coeffs_at(A,0,node),coeffs_at(B,1,node)))
            nr=detq(N_at(A,B,Fraction(node)))
            assert R==Fraction(node)**(m*m*(m-1))*(node-1)**(m*m)*nr
            record('integer_specialization',m=m,sample=sample,node=node,resultant=str(R))

# Composite rings and fields: evaluate direct Kronecker determinant and Laurent N.
for modulus in (2,3,4,5,8,9,12):
    for m in (1,2,3,4):
        A=[[rng.randrange(modulus) for _ in range(m)] for _ in range(m)]
        B=[[rng.randrange(modulus) for _ in range(m)] for _ in range(m)]
        for node in range(modulus):
            if gcd(node,modulus)!=1:continue
            inv=pow(node,-1,modulus)
            def wp(k):return pow(node,k,modulus) if k>=0 else pow(inv,-k,modulus)
            def sn(n):return sum(wp(r) for r in range(n))%modulus if n>0 else -sum(wp(r) for r in range(n,0))%modulus
            N=[[A[i][j]*B[k][l]*sn(1+k-i+l-j)%modulus for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
            Kr=[[A[i][j]*B[k][l]*(wp(1+k+l)-wp(i+j))%modulus for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
            RR=det(sylvester(coeffs_at(A,0,node),coeffs_at(B,1,node)))%modulus
            assert RR==det(Kr)%modulus
            assert RR==(wp(m*m*(m-1))*pow(node-1,m*m,modulus)*det(N))%modulus
            record('ring_specialization',modulus=modulus,m=m,node=node)
        for center in (1,-1):
            Nm=[[A[i][j]*B[k][l]*((1+k-i+l-j) if center==1 else ((1+k-i+l-j)%2))%modulus for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
            if modulus==2:
                other=N_at(A,B,1)
                assert det(Nm)%2==det(other)%2
            record('ring_endpoint',modulus=modulus,m=m,center=center,determinant=det(Nm)%modulus)

# Full-degree LU decision, including zero pivots, over finite fields.
for p in (2,3,5,7,101):
    for m in range(1,8):
        for sample in range(20):
            A=[[rng.randrange(p) for _ in range(m)] for _ in range(m)]
            B=[[rng.randrange(p) for _ in range(m)] for _ in range(m)]
            expected=minors_product(A,B)%p!=0
            actual=full_degree_test(A,B,p)
            assert actual==expected
            record('field_full_degree_test',p=p,m=m,sample=sample,full_degree=actual)

# Characteristic-2 and characteristic-3 endpoint orders from exact polynomials.
for p in (2,3,5):
    for m,label,A,B,R,V in poly_cases:
        Rp=sp.Poly(R.as_expr(),w,modulus=p);Vp=sp.Poly(V.as_expr(),x,modulus=p)
        if Rp.is_zero:
            assert Vp.is_zero
            continue
        for center in (1,-1):
            rr=Rp;ordr=0
            while rr.eval(center)%p==0:
                rr,rem=sp.div(rr,sp.Poly(w-center,w,modulus=p));assert rem.is_zero;ordr+=1
            vv=Vp;ordv=0
            while vv.eval(2*center)%p==0:
                vv,rem=sp.div(vv,sp.Poly(x-2*center,x,modulus=p));assert rem.is_zero;ordv+=1
            extra=m*m if center==1 or p==2 else 0
            assert ordr==extra+2*ordv
            record('field_endpoint_order',p=p,m=m,case=label,center=center,resultant_order=ordr,V_multiplicity=ordv)

AFTER=hashes();assert BEFORE==AFTER
counts={k:sum(c['kind']==k for c in checks) for k in sorted({c['kind'] for c in checks})}
result={'status':'PASS','source_hashes_before':BEFORE,'source_hashes_after':AFTER,'seed':100101535,'counts':counts,'total_records':len(checks),'checks':checks}
(OUT/'EXACT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2,default=int)+'\n')
print(json.dumps({'status':'PASS','counts':counts,'total_records':len(checks)},indent=2))
