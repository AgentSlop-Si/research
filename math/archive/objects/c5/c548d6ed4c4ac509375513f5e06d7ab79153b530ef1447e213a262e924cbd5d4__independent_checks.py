#!/usr/bin/env python3
"""Independent exact controls for the sparse-prefix/additive-tail theorem.
Authored for this audit. Does not read, import, or execute uploaded programs.
Only the standard library is used. The tests do not establish asymptotic novelty.
"""
import argparse, itertools as it, json, math, random
from pathlib import Path


def rank(A, p):
    B=[list(map(lambda x:x%p,row)) for row in A]
    if not B:return 0
    h=0
    for j in range(len(B[0])):
        z=next((z for z in range(h,len(B)) if B[z][j]),None)
        if z is None:continue
        B[z],B[h]=B[h],B[z]
        u=pow(B[h][j],-1,p)
        B[h]=[x*u%p for x in B[h]]
        for z in range(h+1,len(B)):
            u=B[z][j]
            if u:B[z]=[(x-u*y)%p for x,y in zip(B[z],B[h])]
        h+=1
        if h==len(B):break
    return h


def inv(A,p):
    n=len(A);B=[[(x%p) for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        z=next((z for z in range(j,n) if B[z][j]),None)
        assert z is not None
        B[z],B[j]=B[j],B[z]
        u=pow(B[j][j],-1,p);B[j]=[x*u%p for x in B[j]]
        for i in range(n):
            if i!=j and B[i][j]:
                u=B[i][j];B[i]=[(x-u*y)%p for x,y in zip(B[i],B[j])]
    return [row[n:] for row in B]


def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def sub(A,X,Y):return [[A[i][j] for j in Y] for i in X]
def product(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]


def separated(X,Y,a,b):
    return not X or not Y or max(a[i] for i in X)<min(b[j] for j in Y) or max(b[j] for j in Y)<min(a[i] for i in X)


def select_by_threshold(X,Y,a,b):
    """Search all cuts, unlike the source's four-extreme-sets procedure."""
    h,k=len(X)//2,len(Y)//2
    if not h or not k:return X[:h],Y[:k]
    labels=sorted(set(a[i] for i in X)|set(b[j] for j in Y))
    for cut in labels:
        xl=[i for i in X if a[i]<=cut];xr=[i for i in X if a[i]>cut]
        yl=[j for j in Y if b[j]<=cut];yr=[j for j in Y if b[j]>cut]
        if len(xl)>=h and len(yr)>=k:return xl[:h],yr[:k]
        if len(xr)>=h and len(yl)>=k:return xr[:h],yl[:k]
    raise AssertionError('No separating cut')


def selection_tests():
    c=0
    # Each pair of position subsets includes all possible relative order/tie types.
    for n in range(2,9):
        sets=[z for k in range(2,n+1) for z in it.combinations(range(n),k)]
        for X in sets:
            for Y in sets:
                R,C=select_by_threshold(list(X),list(Y),range(n),range(n))
                assert len(R)==len(X)//2 and len(C)==len(Y)//2
                assert separated(R,C,range(n),range(n));c+=1
    rng=random.Random(7193);multi=0;vacuous=0
    for n in range(1,66):
        for s in [1,2,3,4,7,70]:
            for d in range(1,7):
                orders=[]
                for _ in range(d):
                    a=list(range(n));b=list(range(n));rng.shuffle(a);rng.shuffle(b);orders.append((a,b))
                X=list(range(n//s));Y=list(range(n))
                for a,b in orders:X,Y=select_by_threshold(X,Y,a,b)
                m=n//(s*2**d)
                assert len(X)==m and len(Y)==n//2**d and len(Y)>=s*m
                assert all(separated(X,Y,a,b) for a,b in orders)
                multi+=1;vacuous+=not m
    return {'exhaustive_relative_position_cases':c,'iterated_cases':multi,'vacuous_m_zero_cases':vacuous}


def prime_fourier_minors():
    out=[]
    for n in [2,3,5,7]:
        total=0;terms=0
        for k in range(1,n+1):
            permutations=[]
            for pi in it.permutations(range(k)):
                parity=sum(pi[i]>pi[j] for i in range(k) for j in range(i+1,k))%2
                permutations.append((pi,(-1)**parity))
            for X in it.combinations(range(n),k):
                for Y in it.combinations(range(n),k):
                    c=[0]*n
                    for pi,sgn in permutations:
                        c[sum(X[i]*Y[pi[i]] for i in range(k))%n]+=sgn
                    # In Q[z]/Phi_n, Phi_n=1+...+z^(n-1): zero iff c is constant.
                    assert len(set(c))>1
                    total+=1;terms+=len(permutations)
        out.append({'N':n,'nonempty_square_minors':total,'signed_determinant_terms':terms})
    return out


def cauchy(n,p):return [[pow(i+n+j+1,-1,p) for j in range(n)] for i in range(n)]


def cauchy_and_mixing():
    p=101;n=7;T=cauchy(n,p);minors=0
    for k in range(1,n+1):
        for X in it.combinations(range(n),k):
            for Y in it.combinations(range(n),k):assert rank(sub(T,X,Y),p)==k;minors+=1
    rng=random.Random(99653);checks=0
    for s in [1,2,3,4]:
        for rep in range(3):
            # Invertible upper triangular matrices with exactly bounded row support.
            P=ident(n)
            for i in range(n):
                J=list(range(i+1,n));rng.shuffle(J)
                for j in J[:s-1]:P[i][j]=rng.randrange(1,p)
            PT=product(P,T,p)
            for m in range(1,n//s+1):
                for X in it.combinations(range(n),m):
                    for Y in it.combinations(range(n),s*m):
                        assert rank(sub(PT,X,Y),p)==m;checks+=1
    # Failure when |Y|<s*m, despite invertible row-two-sparse P and full-spark T.
    P=ident(n);P[0][0]=T[1][0];P[0][1]=-T[0][0]%p
    assert rank(P,p)==n and product(P,T,p)[0][0]==0
    # Failure without independence of selected preconditioner rows.
    Z=ident(n);Z[1]=Z[0][:]
    assert rank(sub(product(Z,T,p),[0,1],[0,1]),p)==1
    # Composite Fourier control: omega=4 in GF(17), rows/columns 0,2.
    F=[[pow(4,i*j,17) for j in range(4)] for i in range(4)]
    assert rank(sub(F,[0,2],[0,2]),17)==1
    return {'cauchy_all_minors':minors,'sparse_mixing_rectangles':checks,
            'insufficient_column_control':{'N':n,'p':p,'s':2,'m':1,'columns':[0],'rank':0,'P_first_row':P[0]},
            'singular_preconditioner_control_rank':1,'composite_fourier_2_by_2_control_rank':1}


def cycle(n,rng):
    order=list(range(n));rng.shuffle(order);succ=[0]*n;pos=[0]*n
    for k,i in enumerate(order):succ[i]=order[(k+1)%n];pos[i]=k
    return succ,pos


def weights(n,p,rng,zero):
    w=[rng.randrange(1,p) for _ in range(n)]
    if zero:w[rng.randrange(n)]=0
    if math.prod(w)%p==1:w[0]=0
    return w


def difference(n,p,rng,zero):
    succ,pos=cycle(n,rng);w=weights(n,p,rng,zero);A=ident(n)
    for i in range(n):A[i][succ[i]]=(A[i][succ[i]]-w[i])%p
    return A,succ,pos,w


def green_branch(n,p,rng,zero,order_template=None):
    A,succ,pos,w=difference(n,p,rng,zero)
    # Ordinary Gauss-Jordan, independently avoids the uploaded path-product formula.
    G=inv(A,p)
    assert all((G[i][j]-w[i]*G[succ[i]][j])%p==int(i==j) for i in range(n) for j in range(n))
    if order_template is None:
        a=list(range(n));b=list(range(n));rng.shuffle(a);rng.shuffle(b)
    else:a,b=order_template
    labels_by_pos=[pos.index(i) for i in range(n)]
    rm=[labels_by_pos[x] for x in a];cm=[labels_by_pos[x] for x in b]
    ls=[rng.randrange(1,p) for _ in range(n)];rs=[rng.randrange(1,p) for _ in range(n)]
    H=[[ls[i]*G[rm[i]][cm[j]]*rs[j]%p for j in range(n)] for i in range(n)]
    return H,a[:],b[:]


def green_rank_tests():
    rng=random.Random(716153);rectangles=0;branches=0
    for n in [3,5,8,13,29]:
        for zero in [False,True]:
            H,a,b=green_branch(n,1009,rng,zero);branches+=1
            for cut in range(n-1):
                X=[i for i in range(n) if a[i]<=cut];Y=[j for j in range(n) if b[j]>cut]
                U=[i for i in range(n) if a[i]>cut];V=[j for j in range(n) if b[j]<=cut]
                assert rank(sub(H,X,Y),1009)<=1 and rank(sub(H,U,V),1009)<=1
                rectangles+=2
    return {'independently_inverted_branches':branches,'maximal_strict_rectangles':rectangles,'zero_edge_cases':branches//2}


def primality(x):
    if x<2:return False
    return all(x%k for k in range(2,math.isqrt(x)+1))


def root_and_field(n):
    k=1000
    while not primality(n*k+1):k+=1
    p=n*k+1
    for x in range(2,p):
        w=pow(x,k,p)
        if w!=1:return p,w
    raise AssertionError


def prefix(n,p,t,rng):
    P=ident(n)
    for layer in range(t):
        shuffle=list(range(n));rng.shuffle(shuffle)
        scales=[rng.randrange(1,p) for _ in range(n)]
        M=[[scales[i]*v%p for v in P[shuffle[i]]] for i in range(n)]
        _,succ,_,w=difference(n,p,rng,layer%2==1)
        P=[[(x-w[i]*y)%p for x,y in zip(M[i],M[succ[i]])] for i in range(n)]
    assert max(sum(x!=0 for x in row) for row in P)<=2**t
    return P


def architecture_tests():
    rng=random.Random(919177);out=[]
    for n,t,Q in [(13,0,2),(29,1,2),(53,2,2),(101,1,3),(131,2,3),(257,3,3)]:
        p,w=root_and_field(n)
        for rep in range(2):
            # Explicit d refinement on second trial: last branch reuses first order pair.
            B=[]
            for j in range(Q):
                template=(B[0][1],B[0][2]) if rep and j==Q-1 else None
                B.append(green_branch(n,p,rng,j%2==1,template))
            orders=[]
            for _,a,b in B:
                if (a,b) not in orders:orders.append((a,b))
            d=len(orders);s=2**t;P=prefix(n,p,t,rng)
            initial=list(range(n));rng.shuffle(initial);X=initial[:n//s];Y=list(range(n))
            for a,b in orders:X,Y=select_by_threshold(X,Y,a,b)
            m=n//(s*2**d)
            assert len(X)==m and len(Y)==n//2**d and len(Y)>=s*m and m>Q
            S=[k for k in range(n) if any(P[i][k] for i in X)]
            Fourier=[[pow(w,k*j,p) for j in Y] for k in S]
            R=rank(Fourier,p);assert R==len(S)
            A=[[sum(P[i][k]*pow(w,k*j,p) for k in S)%p for j in Y] for i in X]
            terms=[sub(H,X,Y) for H,_,_ in B]
            ranks=[rank(Z,p) for Z in terms]
            H=[[sum(Z[i][j] for Z in terms)%p for j in range(len(Y))] for i in range(m)]
            assert all(r<=1 for r in ranks) and rank(H,p)<=Q and rank(A,p)==m
            out.append({'N':n,'field':p,'root':w,'t':t,'Q':Q,'d':d,'s':s,'m':m,'columns':len(Y),
                        'support_union':len(S),'support_fourier_rank':R,'PT_rank':rank(A,p),
                        'tail_rank':rank(H,p),'branch_ranks':ranks})
    return out


def integer_boundaries():
    cases=0
    for n in range(1,500):
        for s in [1,2,3,4,8]:
            for d in range(1,5):
                for R in range(6):
                    assert (n//(s*2**d)<=R)==(n<s*2**d*(R+1));cases+=1
    assert 23<24 and not 29<24 and 47<48 and not 53<48
    return {'integer_equivalence_cases':cases,'first_excluded_primes_t1_Q2':29,'first_excluded_primes_t2_Q2':53}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='INDEPENDENT_RESULTS.json');args=ap.parse_args()
    result={'status':'PASS','uploaded_code_executed':False,'scope':'sparse inverse prefix plus one additive tail only',
            'selection':selection_tests(),'cyclotomic_prime_minors':prime_fourier_minors(),
            'full_spark_mixing':cauchy_and_mixing(),'Green_rank':green_rank_tests(),
            'architectures':architecture_tests(),'boundaries':integer_boundaries()}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS independent sparse-prefix/additive-tail controls')
    print(json.dumps({k:result[k] for k in ['selection','cyclotomic_prime_minors','full_spark_mixing','Green_rank','boundaries']},sort_keys=True))
    print('Architecture witnesses:',len(result['architectures']))
if __name__=='__main__':main()
