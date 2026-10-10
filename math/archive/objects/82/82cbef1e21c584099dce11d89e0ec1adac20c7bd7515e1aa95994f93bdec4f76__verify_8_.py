"""Exact finite-field audit of Fourier diagonal-gauge compatibility.

All tests over GF(65537). No FFT library, floating point, or optimized FFT
is called. The Fourier matrix is explicitly formed only for positive controls.
"""
import itertools, random, json, time
from pathlib import Path

P=65537
SEED=20261010
rng=random.Random(SEED)
GREEN_LOG=[]
STAGE_LOG=[]

def invnum(x):
    x%=P
    if not x: raise ZeroDivisionError('zero in finite field')
    return pow(x,P-2,P)

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def mm(A,B):
    m,k,n=len(A),len(B),len(B[0]); assert len(A[0])==k
    C=[[0]*n for _ in range(m)]
    for i in range(m):
        for h in range(k):
            a=A[i][h]
            if not a:continue
            for j in range(n): C[i][j]=(C[i][j]+a*B[h][j])%P
    return C

def rank(A):
    if not A:return 0
    M=[list(map(lambda x:x%P,row)) for row in A]
    m,n=len(M),len(M[0]); k=0
    for j in range(n):
        t=next((i for i in range(k,m) if M[i][j]),None)
        if t is None:continue
        M[k],M[t]=M[t],M[k]
        v=invnum(M[k][j]); M[k]=[(x*v)%P for x in M[k]]
        for i in range(k+1,m):
            d=M[i][j]
            if d: M[i]=[(a-d*b)%P for a,b in zip(M[i],M[k])]
        k+=1
        if k==m:break
    return k

def mi(A):
    n=len(A); M=[[v%P for v in A[i]]+eye(n)[i] for i in range(n)]
    for k in range(n):
        t=next((j for j in range(k,n) if M[j][k]),None)
        if t is None: raise ValueError('singular')
        M[k],M[t]=M[t],M[k]
        v=invnum(M[k][k]); M[k]=[(x*v)%P for x in M[k]]
        for i in range(n):
            if i==k:continue
            d=M[i][k]
            if d: M[i]=[(a-d*b)%P for a,b in zip(M[i],M[k])]
    return [row[n:] for row in M]

def random_cycle(n):
    z=list(range(n));rng.shuffle(z)
    p=[None]*n
    for i in range(n):p[z[i]]=z[(i+1)%n]
    return p

def green(n):
    for _ in range(100):
        sigma=random_cycle(n)
        w=[rng.randrange(1,P) for _ in range(n)]
        pr=1
        for t in w:pr=pr*t%P
        if pr==1:continue
        K=eye(n)
        for i in range(n):K[i][sigma[i]]=(K[i][sigma[i]]-w[i])%P
        G=mi(K)
        rowp=list(range(n));colp=list(range(n))
        rng.shuffle(rowp);rng.shuffle(colp)
        ar=[rng.randrange(1,P) for _ in range(n)]
        ac=[rng.randrange(1,P) for _ in range(n)]
        GREEN_LOG.append({"sigma":sigma,"weights":w,"row_perm":rowp,"col_perm":colp,"row_scale":ar,"col_scale":ac})
        return [[(ar[i]*G[rowp[i]][colp[j]]*ac[j])%P for j in range(n)] for i in range(n)]
    raise RuntimeError('unable to sample')

def two_green_stage(n):
    for _ in range(100):
        G1,G2=green(n),green(n)
        A=[[(G1[i][j]+G2[i][j])%P for j in range(n)] for i in range(n)]
        if rank(A)==n:
            STAGE_LOG.append(GREEN_LOG[-2:])
            return A
    raise RuntimeError('stages sampled singular')

def omega_root(n):
    assert (P-1)%n==0
    for a in range(2,P):
        w=pow(a,(P-1)//n,P)
        if pow(w,n,P)!=1:continue
        if all(pow(w,n//d,P)!=1 for d in range(2,n+1) if n%d==0 and all(d%t for t in range(2,int(d**.5)+1))):
            return w
    raise RuntimeError('no root')

def is_primitive(w,n):
    return pow(w,n,P)==1 and all(pow(w,n//k,P)!=1 for k in range(2,n+1) if n%k==0 and all(k%d for d in range(2,int(k**.5)+1)))

def shift(n):
    S=[[0]*n for _ in range(n)]
    for j in range(n):S[(j+1)%n][j]=1
    return S

def Fmat(n,w):return [[pow(w,k*j,P) for j in range(n)] for k in range(n)]

def gauge_coeff_matrix(A,B,w):
    n=len(A)
    return [[A[k][i]*(B[i][(j+1)%n]-pow(w,k,P)*B[i][j])%P for i in range(n)]
       for k in range(n) for j in range(n)]

def diagnostic_graph(A,B,w):
    """Return diagonal-gauge solution d or exact inconsistency reason."""
    n=len(A)
    delta=[[int(i==j)*pow(w,i,P) for j in range(n)] for i in range(n)]
    X=mm(mm(B,shift(n)),mi(B))
    Y=mm(mm(mi(A),delta),A)
    adj=[[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            x,y=X[i][j],Y[i][j]
            if (x==0)!=(y==0):return None,{'reason':'zero-pattern','i':i,'j':j,'X':x,'Y':y}
            if x:
                r=y*invnum(x)%P # d_i = r d_j
                if i==j and r!=1:return None,{'reason':'diagonal','i':i,'X':x,'Y':y}
                adj[i].append((j,invnum(r)))
                adj[j].append((i,r))
    d=[None]*n
    for start in range(n):
        if d[start] is not None:continue
        d[start]=1;stack=[start]
        while stack:
            i=stack.pop()
            for j,mul in adj[i]:
                val=d[i]*mul%P
                if d[j] is None:d[j]=val;stack.append(j)
                elif d[j]!=val:return None,{'reason':'inconsistent-cycle','i':i,'j':j,'actual':d[j],'expected':val}
    return d,{'reason':'compatible','components':sum(1 for x in d if x==1)}

def all_square_minors_nonzero(M):
    n=len(M); count=0
    for k in range(1,n+1):
        sets=list(itertools.combinations(range(n),k))
        for R in sets:
            for C in sets:
                if rank([[M[i][j] for j in C] for i in R])!=k:
                    return False,count,{'size':k,'rows':R,'cols':C}
                count+=1
    return True,count,None

def coset_pairs(n):
    div=[d for d in range(1,n+1) if n%d==0]
    for dr in div:
        for a in range(dr):
            R=tuple(range(a,n,dr))
            for dc in div:
                for b in range(dc):
                    C=tuple(range(b,n,dc))
                    h=n//__import__('math').gcd(n,dr*dc)
                    yield R,C,h

def check_weighted_matrix_identity(A,B,d,w):
    n=len(A)
    D=[[int(i==j)*d[i] for j in range(n)] for i in range(n)]
    M=mm(mm(A,D),B)
    delta=[[int(i==j)*pow(w,i,P) for j in range(n)] for i in range(n)]
    good = mm(M,shift(n))==mm(delta,M)
    col=[M[i][0] for i in range(n)]
    if any(x==0 for x in col):return good,False,None
    F=[[M[i][j]*invnum(col[i])%P for j in range(n)] for i in range(n)]
    return good,F==Fmat(n,w),M

def beta_exact(A,B,R,C):
    n=len(A); best=2*n
    for mask in range(1<<n):
        S=[i for i in range(n) if mask>>i&1]
        SC=[i for i in range(n) if not mask>>i&1]
        r1=rank([[A[i][j] for j in SC] for i in R]) if R and SC else 0
        r2=rank([[B[i][j] for j in C] for i in S]) if S and C else 0
        best=min(best,r1+r2)
    return best

def main():
    n=8;w=omega_root(n);assert is_primitive(w,n)
    # Positive: A=I, B=F, D=I; exact Fourier covariance and reconstruction.
    AA,BB=eye(n),Fmat(n,w)
    posd,posdiag=diagnostic_graph(AA,BB,w)
    assert posd is not None
    poscov,posrec,_=check_weighted_matrix_identity(AA,BB,posd,w)
    assert poscov and posrec

    # Stronger non-trivial positive: arbitrary change of basis, A=F*T^-1,B=T.
    T=two_green_stage(n)
    A2=mm(Fmat(n,w),mi(T)); B2=T
    d2,diag2=diagnostic_graph(A2,B2,w)
    assert d2 is not None
    good2,rec2,_=check_weighted_matrix_identity(A2,B2,d2,w)
    assert good2 and rec2
    # Nontrivial diagonal gauge and output normalization: construct exact positive
    # control via arbitrary invertible T, nontrivial d0 and nontrivial row gain c0.
    d0=[rng.randrange(1,P) for _ in range(n)]
    c0=[rng.randrange(1,P) for _ in range(n)]
    invD0=[[int(i==j)*invnum(d0[i]) for j in range(n)] for i in range(n)]
    rowC=[[int(i==j)*c0[i] for j in range(n)] for i in range(n)]
    A3=mm(mm(mm(rowC,Fmat(n,w)),mi(T)),invD0)
    B3=T
    d3,diag3=diagnostic_graph(A3,B3,w)
    assert d3 is not None
    good3,rec3,_=check_weighted_matrix_identity(A3,B3,d3,w)
    assert good3 and rec3

    # Negative: look for actual 4-Green product with *all* 12869 square minors nonzero
    # while no invertible interface diagonal can ever satisfy Fourier covariance.
    negative=None
    for trial in range(1,50):
        A=two_green_stage(n); B=two_green_stage(n)
        coeffrank=rank(gauge_coeff_matrix(A,B,w))
        if coeffrank!=n:continue
        d=[rng.randrange(1,P) for _ in range(n)]
        D=[[int(i==j)*d[i] for j in range(n)] for i in range(n)]
        M=mm(mm(A,D),B)
        passed,num,fail=all_square_minors_nonzero(M)
        if passed:
            dd,why=diagnostic_graph(A,B,w)
            assert dd is None
            negative={'trial':trial,'A':A,'B':B,'green_parameters':STAGE_LOG[-2:],'d':d,'full_spark_minors':num,'gauge_coefficient_rank':coeffrank,'graph_rejection':why,'M':M}
            break
    assert negative is not None,'No strong witness found in 49 attempts'
    A,B=negative['A'],negative['B']
    fcos=[]
    for R,C,h in coset_pairs(n):
        grank=rank([[negative['M'][i][j] for j in C] for i in R])
        assert grank>=h
        fcos.append((len(R),len(C),h,grank))
    # Check matroid intersection generic diagonal saturation on 8 selected pairs.
    pairs=[(tuple(range(0,4)),tuple(range(4,8))),
          ((0,2,4,6),(1,3,5,7)),
          ((0,4),(2,6)),((0,1,2),(3,4,5)),
          ((0,2,3,6),(0,3,5,7)),((1,3,5),(0,2,4)),
          (tuple(range(8)),tuple(range(8))),((1,),(7,))]
    beta=[]
    for R,C in pairs:
        b=beta_exact(A,B,R,C)
        r=rank([[negative['M'][i][j] for j in C] for i in R])
        assert r<=b
        assert r==b,('generic diag failed to saturate expected beta',R,C,b,r)
        beta.append({'R':list(R),'C':list(C),'beta':b,'actual_rank':r})

    # Restricted structured example: single Green resolvent repeated, beta small.
    sig=[(i+1)%n for i in range(n)]
    K=eye(n)
    for i in range(n):K[i][sig[i]]=(K[i][sig[i]]-2)%P
    G=mi(K)
    r0=tuple(range(4));c0=tuple(range(4,8))
    smallbeta=beta_exact(G,G,r0,c0)
    assert smallbeta<=3
    R1=[]
    for _ in range(16):
        diag=[rng.randrange(1,P) for i in range(n)]
        D=[[int(i==j)*diag[i] for j in range(n)] for i in range(n)]
        MG=mm(mm(G,D),G)
        R1.append(rank([[MG[i][j] for j in c0] for i in r0]))
    assert max(R1)==smallbeta

    out={
        'field':'GF(65537)','N':n,'primitive_8th_root':w,
        'positive_controls':{'identity_F':{'covariance':poscov,'reconstruction':posrec},
                             'arbitrary_basis':{'covariance':good2,'reconstruction':rec2},
                             'nontrivial_interface_and_output_gauges':{'covariance':good3,'reconstruction':rec3,'original_d0':d0,'recovered_d':d3}},
        'four_green_witness':{k:v for k,v in negative.items() if k!='M'},
        'tested_square_minors':negative['full_spark_minors'],
        'Fourier_coset_profiles_checked':len(fcos),
        'Fourier_coset_profiles_passed':len(fcos),
        'matroid_intersection_selected_pairs':beta,
        'structured_small_rank_control':{'beta':smallbeta,'trials':len(R1),'ranks':R1},
        'seed':SEED,
        'note':'All arithmetic exact in GF(65537). Witness is a phase obstruction for fixed stage parameters, not a proof excluding all Green choices.'
    }
    path=Path(__file__).with_name('RESULTS.json');path.write_text(json.dumps(out,indent=2))
    print(json.dumps({'positive_controls':out['positive_controls'],'trial':negative['trial'], 'full_spark_minors':out['tested_square_minors'],'coset_profiles':len(fcos), 'phase_linear_map_rank':negative['gauge_coefficient_rank'],'graph_rejection':negative['graph_rejection'], 'beta_examples':beta, 'rank_deficient_example_beta':smallbeta}, indent=2))

if __name__=='__main__':main()
