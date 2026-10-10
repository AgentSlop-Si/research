"""Independent exact controls authored for this review.
No submitted or first-audit source is executed or imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import random, json, hashlib
import sympy as sp

OUT=Path(__file__).resolve().parent

def scalar(x): return str(x)
def dump(M): return [[scalar(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def zero(M): return all(sp.expand(x)==0 for x in M)
def upper_zero(M): return all(M[i,j]==0 for i in range(M.rows) for j in range(i+1,M.cols))
def cauchy(n): return sp.Matrix(n,n,lambda i,j: sp.Rational(1,i+n+j+1))
def strict_upper(M): return sp.Matrix(M.rows,M.cols,lambda i,j: M[i,j] if i<j else 0)
def block_complete(M):
    n=M.rows; h=n//2
    if not h: return sp.zeros(n),sp.zeros(n,0),sp.zeros(0,n), {'pivot_det':'1','middle_schur':str(M[0,0])}
    B=M[:h,n-h:]
    C=sp.zeros(n,h); W=sp.zeros(h,n)
    C[:h,:]=B; C[n-h:,:]=strict_upper(M[n-h:,n-h:])
    W[:,:h]=strict_upper(M[:h,:h]); W[:,n-h:]=B
    metadata={'pivot_det':str(B.det())}
    if n%2:
        C[h,:]=M[h,n-h:]
        W[:,h]=M[:h,h]
        s=M[h,h]-(M[h,n-h:]*B.inv()*M[:h,h])[0]
        Q=M.extract(list(range(h))+[h],list(range(n-h,n))+[h])
        assert Q.det()==B.det()*s and s != 0
        metadata.update(middle_schur=str(s), augmented_det=str(Q.det()))
    X=C; Y=B.inv()*W
    return X*Y,X,Y,metadata

def row_tail_complete(M):
    n=M.rows; h=n//2
    R=sp.zeros(n)
    for i in range(h):
        for j in range(i+1,n): R[i,j]=M[i,j]
    pivots=[]
    for i in range(h,n):
        d=n-i-1
        if d:
            B=M[:d,i+1:]
            coeff=M[i,i+1:]*B.inv()
            R[i,:]=coeff*R[:d,:]
            Q=M.extract(list(range(d))+[i],list(range(i+1,n))+[i])
            s=M[i,i]-R[i,i]
            assert Q.det()==B.det()*s and s != 0
            pivots.append({'row':i,'tail_minor_det':str(B.det()),'augmented_det':str(Q.det()),'residual_diagonal':str(s)})
    return R,pivots

def test_completion(M,schur=True):
    n=M.rows; h=n//2
    R,X,Y,piv=block_complete(M); T=M-R
    Q,tailpiv=row_tail_complete(M); TT=M-Q
    assert R.rank()==Q.rank()==h
    assert upper_zero(T) and upper_zero(TT)
    assert all(T[i,i]!=0 and TT[i,i]!=0 for i in range(n))
    if schur:
        A=T.inv(); U=A*X; V=Y*A; H=sp.eye(h)+Y*A*X
        K=A.row_join(U).col_join(V.row_join(H))
        # Certify the full inverse by multiplication, independently of direct inversion.
        KI=(T+R).row_join(-X).col_join((-Y).row_join(sp.eye(h)))
        assert zero(K*KI-sp.eye(n+h)) and zero(KI*K-sp.eye(n+h))
        assert zero(KI[:n,:n]-M)
        assert zero(H-V*T*U-sp.eye(h))
    return {'n':n,'rank':h,'residual_diagonal':[str(T[i,i]) for i in range(n)],'row_tail_residual_diagonal':[str(TT[i,i]) for i in range(n)],'block_pivots':piv,'row_tail_pivots':tailpiv}

def detmod(a,p):
    a=[[x%p for x in row] for row in a]; n=len(a); ans=1
    for c in range(n):
        pivot=next((r for r in range(c,n) if a[r][c]),None)
        if pivot is None: return 0
        if pivot != c: a[c],a[pivot]=a[pivot],a[c]; ans=-ans
        v=a[c][c];ans=ans*v%p; iv=pow(v,-1,p)
        for r in range(c+1,n):
            t=a[r][c]*iv%p
            for j in range(c,n): a[r][j]=(a[r][j]-t*a[c][j])%p
    return ans%p

def lis(p):
    d=[]
    for i,x in enumerate(p): d.append(1+max([d[j] for j in range(i) if p[j]<x] or [0]))
    return max(d,default=0)

result={'scope':'Independent exact tests of two completion proofs, shared rectangles, singular-pivot inverse bounds, and Fourier field boundaries.','source_code_policy':'No submitted or first-audit Python was executed or imported.','exact_arithmetic':'Rational matrices and Gaussian rationals via SymPy; fresh modular Gaussian elimination.'}
rng=random.Random(1253)
plain=[]; gauged=[]
for n in range(1,17):
    M=cauchy(n)
    plain.append(test_completion(M,schur=n<=10))
    if n<=10:
        for trial in range(3):
            rows=list(range(n));cols=list(range(n));rng.shuffle(rows);rng.shuffle(cols)
            dl=[rng.choice([-5,-3,-2,-1,1,2,3,5]) for _ in range(n)]
            dr=[rng.choice([-7,-4,-2,-1,1,2,4,7]) for _ in range(n)]
            W=sp.diag(*dl)*M.extract(rows,cols)*sp.diag(*dr)
            record=test_completion(W)
            record.update(row_order=rows,column_order=cols,left_gauge=dl,right_gauge=dr,trial=trial)
            gauged.append(record)
result['cauchy_completion_controls']=plain
result['independent_endpoint_controls']=gauged

rect=[]
for m in range(1,17):
    n=2*m; sigma=list(range(m-1,-1,-1))+list(range(n-1,m-1,-1))
    pos=[sigma.index(x) for x in range(n)]
    assert lis(pos)==2
    assert all(i<j and pos[i]<pos[j] for i in range(m) for j in range(m,n))
    witness=cauchy(n)[:m,m:]
    assert witness.det()!=0
    rect.append({'n':n,'relative_positions':pos,'lis':2,'lis_gate':1,'rectangle_gate':m,'rectangle_determinant':str(witness.det())})
result['shared_zero_rectangles']=rect

singular=[]
for n in range(2,9):
    for q in range(1,min(n,3)+1):
        for trial in range(3):
            # One zero diagonal, all other diagonal entries nonzero.
            A=sp.Matrix(n,n,lambda i,j: (rng.randint(-3,3) if i>j else (rng.choice([1,2,3]) if i==j else 0)))
            A[trial%n,trial%n]=0
            assert A.det()==0
            for attempt in range(100):
                U=sp.Matrix(n,q,lambda i,j:rng.randint(-3,3))
                V=sp.Matrix(q,n,lambda i,j:rng.randint(-3,3))
                H=sp.Matrix(q,q,lambda i,j:rng.randint(-3,3))
                K=A.row_join(U).col_join(V.row_join(H))
                if K.det()!=0: break
            else: raise AssertionError('No invertible bordered control found')
            KI=K.inv(); cut_ranks=[]
            for c in range(1,n):
                r=KI[:c,c:n].rank(); assert r<=q;cut_ranks.append(r)
                # Verify Jacobi's scalar minor identity on every feasible r=q+1 subset:
                rr=q+1
                if rr<=min(c,n-c):
                    I=list(range(rr));J=list(range(c,c+rr))
                    co_rows=[i for i in range(n+q) if i not in J]
                    co_cols=[i for i in range(n+q) if i not in I]
                    lhs=KI.extract(I,J).det(); comp=K.extract(co_rows,co_cols).det()
                    assert lhs==(-1)**(sum(I)+sum(J))*comp/K.det()==0
            singular.append({'n':n,'q':q,'trial':trial,'branch_rank':A.rank(),'branch_determinant':str(A.det()),'system_determinant':str(K.det()),'forward_cut_inverse_ranks':cut_ranks})
            if n==6 and q==1 and trial==0:
                result['singular_pivot_explicit_certificate']={'A':dump(A),'U':dump(U),'V':dump(V),'H':dump(H),'K':dump(K),'K_inverse':dump(KI)}
result['singular_pivot_controls']=singular

I=sp.I
F4=sp.Matrix(4,4,lambda r,c:I**(r*c))
order=[0,2,1,3];M=F4.extract(order,order)
X=sp.Matrix([1,-1,-I,0]);Y=sp.Matrix([[0,1,1,1]])
R=X*Y;T=M-R
assert R.rank()==1 and upper_zero(T)
assert list(T.diagonal())==[1,2,2*I,I] and T.det()==-4
A=T.inv();U=A*X;V=Y*A;H=sp.eye(1)+Y*A*X
K=A.row_join(U).col_join(V.row_join(H))
KI=(T+R).row_join(-X).col_join((-Y).row_join(sp.eye(1)))
assert zero(K*KI-sp.eye(5)) and zero(KI*K-sp.eye(5)) and zero(K.inv()[:4,:4]-M)
result['complex_fourier_N4_certificate']={'root':'i','order':order,'M':dump(M),'X':dump(X),'Y':dump(Y),'R':dump(R),'T':dump(T),'det_T':str(T.det()),'A':dump(A),'U':dump(U),'V':dump(V),'H':dump(H),'K':dump(K),'K_inverse':dump(KI),'det_K':str(sp.simplify(K.det())),'correction_rank':R.rank(),'interface_dimension':1}

fullspark=[]
for n,p,w in [(5,11,3),(7,29,16)]:
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
    count=0
    for k in range(1,n+1):
        for rs in combinations(range(n),k):
            for cs in combinations(range(n),k):
                assert detmod([[pow(w,r*c,p) for c in cs] for r in rs],p)!=0
                count+=1
    fullspark.append({'n':n,'field_prime':p,'root':w,'nonzero_square_minors':count})
result['finite_field_fullspark_exhaustion']=fullspark
zeros=[]
for n,p,w,rs,cs in [(9,19,4,[0,3],[0,3]),(11,23,2,[0,1,3],[0,2,6]),(13,53,10,[0,1,3],[0,1,5])]:
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
    Z=[[pow(w,r*c,p) for c in cs] for r in rs]
    assert detmod(Z,p)==0
    zeros.append({'n':n,'field_prime':p,'root':w,'rows':rs,'columns':cs,'matrix':Z,'determinant_mod_p':0})
result['finite_field_zero_minor_certificates']=zeros
result['summary']={'cauchy_sizes':len(plain),'independent_endpoint_targets':len(gauged),'shared_rectangle_sizes':len(rect),'singular_pivot_systems':len(singular),'fullspark_minors':sum(x['nonzero_square_minors'] for x in fullspark),'zero_minor_certificates':len(zeros),'complex_counterexample_verified':True,'status':'PASS'}
(OUT/'fresh_review_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['summary'],indent=2))
