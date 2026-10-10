"""Audit-owned exact checks. No source-package import or execution.
Standard-library arithmetic only; all products use unbounded Python integers.
The finite checks supplement, rather than prove, the all-N arguments.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import json, random, hashlib

OUT = Path(__file__).resolve().parent
COUNTS = {}
def count(k, n=1): COUNTS[k] = COUNTS.get(k, 0) + n

def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def add(A,B,p): return [[(a+b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def sub(A,B,p): return [[(a-b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def mul(A,B,p):
    return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def det(A,p=None):
    a=[[x%p if p else Q(x) for x in row] for row in A]; n=len(a); ans=1
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None: return 0
        if k != j: a[k],a[j]=a[j],a[k]; ans=-ans
        pivot=a[j][j]; ans=ans*pivot
        if p: ans%=p
        ip=pow(pivot,-1,p) if p else 1/pivot
        for k in range(j+1,n):
            f=a[k][j]*ip
            for l in range(j,n):
                a[k][l]-=f*a[j][l]
                if p: a[k][l]%=p
    return ans%p if p else ans

def rank(A,p):
    a=[[x%p for x in row] for row in A]; m=len(a); n=len(a[0]); r=0
    for j in range(n):
        k=next((k for k in range(r,m) if a[k][j]),None)
        if k is None: continue
        a[k],a[r]=a[r],a[k]; ip=pow(a[r][j],-1,p)
        for k in range(r+1,m):
            f=a[k][j]*ip%p
            for l in range(j,n): a[k][l]=(a[k][l]-f*a[r][l])%p
        r+=1
        if r==m: break
    return r

def inverse(A,p):
    n=len(A); a=[[(x%p) for x in row]+e for row,e in zip(A,eye(n))]
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None: raise ValueError('singular')
        a[k],a[j]=a[j],a[k]; ip=pow(a[j][j],-1,p)
        a[j]=[x*ip%p for x in a[j]]
        for k in range(n):
            if k!=j:
                f=a[k][j]; a[k]=[(x-f*y)%p for x,y in zip(a[k],a[j])]
    return [row[n:] for row in a]

def root(p,n):
    for w in range(1,p):
        if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0): return w
    raise AssertionError('root missing')

def S(n): return [[1 if i>j else 3 if i==j else 2 for j in range(n)] for i in range(n)]
def Sinv(n,p=None):
    D=2**(n+1)-1
    a=[[-2**(i-j-1) if i>j else 2**n-1 if i==j else -2**(n+i-j) for j in range(n)] for i in range(n)]
    if p: return [[x*pow(D,-1,p)%p for x in row] for row in a]
    return [[Q(x,D) for x in row] for row in a]

def minor(A,R,C): return [[A[i][j] for j in C] for i in R]
def supports(n,q,mode,rng):
    if mode=='random': return [set(rng.sample(range(n),q)) for i in range(n)]
    if mode=='next': return [{(i+j+1)%n for j in range(q)} for i in range(n)]
    if mode=='diagonal': return [{(i+j)%n for j in range(q)} for i in range(n)]
    if mode=='concentrated': return [set(range(q)) for i in range(n)]
    if mode=='reverse': return [{(n-1-i+j)%n for j in range(q)} for i in range(n)]
    raise AssertionError(mode)

def witness(supp,q):
    n=len(supp); M=n//(q+2); rr=[i*(q+2) for i in range(M)]
    cc=[next(j for j in range(i+1,i+q+2) if j not in supp[i]) for i in rr]
    adjacency=[{j for j in range(M) if j!=i and (cc[j] in supp[rr[i]] or cc[i] in supp[rr[j]])} for i in range(M)]
    live=set(range(M)); chosen=[]
    while live:
        k=min(live,key=lambda j:(len(adjacency[j]&live),j)); neighbors=adjacency[k]&live
        assert len(neighbors)<=2*q
        chosen.append(k); live-=neighbors|{k}
    chosen.sort(); R=[rr[i] for i in chosen]; C=[cc[i] for i in chosen]
    assert len(chosen)>=(M+2*q)//(2*q+1)
    assert all(c not in supp[r] for r in R for c in C)
    assert all(R[i]<C[i] and (i+1==len(R) or C[i]<R[i+1]) for i in range(len(R)))
    return R,C

def check_fourier():
    rng=random.Random(739491)
    for p,ns in [(97,[1,2,3,4,6,8,12,16,24,32]),(101,[5,10,20,25])]:
        for n in ns:
            w=root(p,n)
            for q in sorted({0,1,2,3,n-1,n}):
                if q>n: continue
                for inv in [False,True]:
                    for mode in ['random','next','concentrated']:
                        supp=supports(n,q,mode,rng); rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
                        dr=[rng.randrange(1,p) for i in range(n)];dc=[rng.randrange(1,p) for i in range(n)]
                        z=pow(w,-1,p) if inv else w; scale=pow(n,-1,p) if inv else 1
                        F=[[dr[i]*dc[j]*scale*pow(z,rp[i]*cp[j],p)%p for j in range(n)] for i in range(n)]
                        B=[[rng.randrange(1,p) if j in supp[i] else 0 for j in range(n)] for i in range(n)]
                        m=n//(q+1); R=[rp.index(i) for i in range(m)]
                        used=set().union(*(supp[i] for i in R)) if R else set(); C=[j for j in range(n) if j not in used][:m]
                        assert len(C)==m
                        assert det(minor(sub(F,B,p),R,C),p)!=0
                        assert rank(sub(F,B,p),p)>=m
                        count('fourier_endpoint_scaled_inverse_and_forward_cases')

def check_telescope():
    rng=random.Random(80123); p=101
    for n in [3,6,9]:
        for specs in [[(0,1)],[(1,0),(2,1)],[(2,2),(1,1),(3,0)],[(0,2),(2,1)]]:
            B=[];A=[]
            for s,r in specs:
                sb=supports(n,s,'random',rng)
                b=[[rng.randrange(p) if j in sb[i] else 0 for j in range(n)] for i in range(n)]
                U=[[rng.randrange(p) for k in range(r)] for i in range(n)]
                V=[[rng.randrange(p) for j in range(n)] for k in range(r)]
                E=mul(U,V,p) if r else [[0]*n for i in range(n)]
                perm=list(range(n));rng.shuffle(perm);diag=[rng.randrange(1,p) for i in range(n)]
                # Shared arbitrary left monomial connector preserves the decomposition.
                B.append([[diag[i]*x%p for x in b[perm[i]]] for i in range(n)])
                a=add(b,E,p);A.append([[diag[i]*x%p for x in a[perm[i]]] for i in range(n)])
            AP=eye(n);BP=eye(n)
            for a,b in zip(A,B):AP=mul(a,AP,p);BP=mul(b,BP,p)
            rhs=[[0]*n for i in range(n)]
            for j in range(len(A)):
                term=sub(A[j],B[j],p)
                for k in reversed(range(j)): term=mul(term,B[k],p)
                for k in range(j+1,len(A)): term=mul(A[k],term,p)
                rhs=add(rhs,term,p)
            assert rhs==sub(AP,BP,p)
            budget=1
            for s,r in specs:budget*=s
            assert max(sum(x!=0 for x in row) for row in BP)<=budget
            assert rank(rhs,p)<=sum(r for s,r in specs)
            count('heterogeneous_telescope_cases_including_singular_baselines')

def check_scan_and_band():
    for n in range(1,19):
        a=S(n);g=Sinv(n);assert det(a)==2**(n+1)-1
        assert [[sum(a[i][k]*g[k][j] for k in range(n)) for j in range(n)] for i in range(n)]==eye(n)
        for b in range(n-1):
            h=b+1;m=(n+b)//(2*b+2);R=[2*h*i for i in range(m)];C=[2*h*i+h for i in range(m)]
            alpha=-Q(1,2**(h+1)*(2**(n+1)-1));beta=-Q(2**(n-h),2**(n+1)-1)
            assert det(minor(g,R,C))==beta*(beta-alpha)**(m-1)!=0
            count('rational_all_bandwidth_minors')
        # Independently derive inverse by solving the direct prefix relation.
        for seed in range(3):
            x=[Q((i+seed)%7-3) for i in range(n)];running=0;y=[]
            for xi in x:y.append(xi+running);running+=y[-1]
            answer=[yi-Q(2*running*2**i,2**(n+1)-1) for i,yi in enumerate(y)]
            assert [sum(g[i][j]*x[j] for j in range(n)) for i in range(n)]==answer
            count('rational_fresh_vector_inverse_scans')
        count('rational_inverse_and_determinant_lengths')
    for n in [8,16,32,64,128]:
        for p in [12289,65537]:
            g=Sinv(n,p);assert mul(S(n),g,p)==eye(n)
            for b in [b for b in [0,1,2,3,7] if b<=n-2]:
                h=b+1;m=(n+b)//(2*b+2);R=[2*h*i for i in range(m)];C=[2*h*i+h for i in range(m)]
                D=(2**(n+1)-1)%p;alpha=-pow(2,-h-1,p)*pow(D,-1,p)%p;beta=-pow(2,n-h,p)*pow(D,-1,p)%p
                assert det(minor(g,R,C),p)==beta*pow((beta-alpha)%p,m-1,p)%p!=0
                count('modular_scan_bandwidth_minors')
    # Characteristic exceptions must not be generalized from the complex claim.
    assert det(S(4),31)==0  # D=31; inverse undefined.
    assert all(Sinv(32,65537)[i][i]==0 for i in range(32))
    assert mul(S(32),Sinv(32,65537),65537)==eye(32)
    count('finite_field_exception_controls',2)

def check_repair():
    rng=random.Random(81991);p=1000003
    for n in [2,3,4,8,16,24,32,64,96,128]:
        g=Sinv(n,p)
        for q in sorted({0,1,2,3,5,n-1,n}):
            if q>n:continue
            for mode in ['random','next','diagonal','concentrated','reverse']:
                supp=supports(n,q,mode,rng);R,C=witness(supp,q);m=len(R)
                if m:
                    D=(2**(n+1)-1)%p;alpha=-pow(2,-1,p)*pow(D,-1,p)%p;beta=-pow(2,n,p)*pow(D,-1,p)%p
                    predicted=pow(2,sum(R)-sum(C),p)*beta*pow((beta-alpha)%p,m-1,p)%p
                    assert det(minor(g,R,C),p)==predicted!=0
                count('arbitrary_sparse_repair_support_and_minor_cases')
                if n<=24:
                    B=[[rng.randrange(1,p) if j in supp[i] else 0 for j in range(n)] for i in range(n)]
                    actual=rank(sub(g,B,p),p)
                    assert actual>=m
                    if q==0:assert actual==n
                    if q<n:assert actual>=1
                    # Arbitrary endpoint monomials transport B back to a row-q baseline.
                    rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
                    dr=[rng.randrange(1,p) for i in range(n)];dc=[rng.randrange(1,p) for i in range(n)]
                    changed=[[dr[i]*dc[j]*(g[rp[i]][cp[j]]-B[rp[i]][cp[j]])%p for j in range(n)] for i in range(n)]
                    assert rank(changed,p)==actual
                    count('repair_full_rank_and_monomial_equivalence_cases')
    # Exhaust every support pattern, including rows with fewer than q entries.
    for n,q in [(4,1),(4,2),(5,1)]:
        choices=[set(c) for k in range(q+1) for c in combinations(range(n),k)]
        for supp in product(choices,repeat=n):witness(supp,q);count('exhaustive_small_support_graph_cases')

def check_ntt_control():
    p=97
    for n in [2,4,8,16,32]:
        w=root(p,n); bits=n.bit_length()-1
        perm=[int(format(i,'0%db'%bits)[::-1],2) for i in range(n)]
        out=[eye(n)[j] for j in perm];width=2; depth=0
        while width<=n:
            A=[[0]*n for i in range(n)]
            for start in range(0,n,width):
                for offset in range(width//2):
                    i=start+offset;j=i+width//2;z=pow(w,offset*n//width,p)
                    A[i][i]=A[j][i]=1;A[i][j]=z;A[j][j]=-z%p
            assert all(sum(v!=0 for v in row)==2 for row in A)
            assert all(sum(v!=0 for v in row)==2 for row in inverse(A,p))
            out=mul(A,out,p);depth+=1;width*=2
        assert out==[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
        assert 2**depth==n
        count('classical_NTT_forward_and_inverse_sparse_stage_controls')

def check_woodbury_and_exceptions():
    rng=random.Random(3911);p=101
    for n in [2,4,7]:
        T=[[5 if i==j else -1 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)];Ti=inverse(T,p)
        for r in [1,2,3]:
            for trial in range(20):
                U=[[rng.randrange(p) for k in range(r)] for i in range(n)];V=[[rng.randrange(p) for i in range(n)] for k in range(r)]
                Z=mul(Ti,U,p);K=add(eye(r),mul(V,Z,p),p);A=add(T,mul(U,V,p),p)
                assert (det(K,p)==0)==(det(A,p)==0)
                if det(K,p)==0:count('woodbury_singular_K_correctly_identified');continue
                W=sub(Ti,mul(mul(Z,inverse(K,p),p),mul(V,Ti,p),p),p)
                assert W==inverse(A,p)
                count('woodbury_general_rank_dense_identity_cases')
    T=[[0,1],[1,0]];assert det(T,p)!=0 and T[0][0]==0
    singular_T=[[0,0],[0,1]];A=add(singular_T,[[1,0],[0,0]],p);assert det(singular_T,p)==0 and det(A,p)!=0
    T=eye(2);U=[[1],[0]];V=[[-1,0]];K=add(eye(1),mul(V,U,p),p);A=add(T,mul(U,V,p),p)
    assert det(K,p)==0 and det(A,p)==0
    count('woodbury_singular_K_correctly_identified')
    count('baseline_and_thomas_chart_exception_controls',3)

if __name__=='__main__':
    check_fourier();check_telescope();check_scan_and_band();check_repair();check_ntt_control();check_woodbury_and_exceptions()
    payload={'status':'PASS','arithmetic':'exact rational and Python-integer modular arithmetic','source_code_executed':False,'counts':COUNTS,'check_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))
