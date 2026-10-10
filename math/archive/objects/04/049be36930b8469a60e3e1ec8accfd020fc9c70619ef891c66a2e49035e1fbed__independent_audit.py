"""Independent Phase 14 audit: exact matrix elimination, Gauss sums, and a distinct
Green-kernel formula. No reuse of phase14's matrix inverse / rank / references.
"""
import random,json,math,hashlib,sys
from pathlib import Path
from phase14 import MagneticGreen,Counts,primitive_root,fused_weyl_twirl,StridedMagneticGreen

HERE=Path(__file__).resolve().parent


def invmat(a,p):
    n=len(a)
    M=[[int(v)%p for v in row]+[int(i==j)for j in range(n)]for i,row in enumerate(a)]
    for k in range(n):
        pivot=next((j for j in range(k,n)if M[j][k]%p),None)
        if pivot is None:return None
        M[k],M[pivot]=M[pivot],M[k]
        M[k]=[(x*pow(M[k][k],p-2,p))%p for x in M[k]]
        # Simpler direct inverse after pivot normalization
        for j in range(n):
            if j==k:continue
            z=M[j][k]
            if z:
                M[j]=[(a-z*b)%p for a,b in zip(M[j],M[k])]
    return [row[n:] for row in M]


def row_rank(M,p):
    A=[list(map(lambda z:z%p,row))for row in M]
    if not A:return 0
    r=0;nc=len(A[0])
    for c in range(nc):
        pivot=next((i for i in range(r,len(A))if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        z=pow(A[r][c],p-2,p)
        A[r]=[v*z%p for v in A[r]]
        for i in range(r+1,len(A)):
            v=A[i][c]
            if v:A[i]=[(a-v*b)%p for a,b in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r


def build_A(n,p,w,alpha,beta,sgn,sig):
    A=[]
    for i in range(n):
        row=[0]*n
        row[i]=(1-beta*pow(w,(sig*i)%n,p))%p
        row[(i-sgn)%n]=(row[(i-sgn)%n]-alpha)%p
        A.append(row)
    return A


def matvec(M,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in M]


def coefficient(A,n,p,w,a,b):
    return sum(A[(j+a)%n][j]*pow(w,(-b*j)%n,p)for j in range(n))*pow(n,p-2,p)%p


def kernel_row(i,x,n,p,w,a,b,eps,delta):
    # Independent polynomial representation without cyclic recurrence or division
    q=w if eps*delta==1 else pow(w,-1,p)
    d=[];power=1
    for _ in range(n):
        d.append((1-b*power)%p)
        power=power*q%p
    t=(eps*i)%n
    prod=[1]
    for j in range(1,n):prod.append(prod[-1]*d[(t+j)%n]%p)
    total=0;phase=1
    for ell in range(n):
        j=(t-ell)%n
        total=(total+phase*prod[n-ell-1]*x[(eps*j)%n])%p
        phase=phase*a%p
    D=(1-pow(a,n,p)-pow(b,n,p))%p
    return total*pow(D,p-2,p)%p


def polynomial_apply(x,n,p,w,a,b):
    """Naive O(n^2) polynomial evaluation, independent from cyclic solver."""
    omega=[pow(w,i,p)for i in range(n)]
    acc=[0]*n
    z=[int(y)%p for y in x]
    for _ in range(n):
        acc=[(acc[j]+z[j])%p for j in range(n)]
        z=[(a*z[(j-1)%n]+b*omega[j]*z[j])%p for j in range(n)]
    D=(1-pow(a,n,p)-pow(b,n,p))%p
    ID=pow(D,p-2,p)
    return [v*ID%p for v in acc]


def small_audit():
    cases=[(3,307),(4,97),(5,521),(6,97),(7,701),(8,97),(9,919),(10,101),
           (11,1123),(12,97),(15,1531),(16,97)]
    stats={'cases':[],'fresh_vectors':0,'basis_vectors':0,'matrix_coefficients':0,
           'block_rank_certificates':0,'qbinomial_support_zeros':0,
           'even_defect_certificates':0,'odd_three_orientation_witnesses':0,
           'twirl_checks':0}
    for n,p in cases:
        w=primitive_root(n,p)
        signpairs=((1,1),(1,-1),(-1,1),(-1,-1))
        bottom=range(n-n//2,n);left=range(n//2)
        Fn=[[pow(w,i*j%n,p)for j in range(n)]for i in range(n)]
        assert row_rank([[Fn[i][j] for j in left]for i in bottom],p)==n//2
        full_coeff=coefficient(Fn,n,p,w,n//2,n//2) if n%2==0 else None
        for eps,delta in signpairs:
            for alpha,beta in ((2,3),(2,1),(0,3)):
                D=(1-pow(alpha,n,p)-pow(beta,n,p))%p
                if not D:continue
                AA=build_A(n,p,w,alpha,beta,eps,delta)
                GG=invmat(AA,p)
                assert GG is not None
                assert row_rank([[GG[i][j] for j in left]for i in bottom],p)<=1
                stats['block_rank_certificates']+=1
                # Weyl coefficient forbidden outside signed triangular support.
                for a in range(n):
                    for b in range(n):
                        ia=(eps*a)%n;ib=(delta*b)%n
                        if a+b>=n:
                            assert coefficient(GG,n,p,w,ia,ib)==0
                            stats['qbinomial_support_zeros']+=1
                for j in range(n):
                    x=[int(k==j)for k in range(n)]
                    G=MagneticGreen(n,p,w,alpha,beta,eps,delta)
                    assert G.apply(x)==[row[j]for row in GG]
                    stats['basis_vectors']+=1
                    stats['matrix_coefficients']+=n
                rng=random.Random(19*n+5*eps+7*delta+alpha)
                for trial in range(3):
                    x=[rng.randrange(p)for _ in range(n)]
                    yy=MagneticGreen(n,p,w,alpha,beta,eps,delta).apply(x)
                    assert yy==matvec(GG,x,p)
                    stats['fresh_vectors']+=1
        if n%4==0:
            # Missing central Weyl monomial is present in true Fourier.
            assert full_coeff!=0
            for eps,delta in signpairs:
                AA=build_A(n,p,w,2,1,eps,delta)
                GG=invmat(AA,p)
                assert coefficient(GG,n,p,w,n//2,n//2)==0
            stats['even_defect_certificates']+=1
        if n%2==1:
            targets={(1,1):(1,1),(-1,-1):(n-1,n-1),
                     (1,-1):(1,n-1),(-1,1):(n-1,1)}
            # Each witness is supported by exactly the missing orientation.
            for sign,(a,b) in targets.items():
                assert coefficient(Fn,n,p,w,a,b)!=0
                for other in signpairs:
                    if other==sign:continue
                    oi=(other[0]*a)%n;oj=(other[1]*b)%n
                    assert oi+oj>=n,(n,sign,other,a,b)
                stats['odd_three_orientation_witnesses']+=1
        # Twirl by T and by S verified via direct conjugation sums for a=2,b=1
        if n<=12:
            a,b=2,1
            H=invmat(build_A(n,p,w,a,b,1,1),p)
            D=(1-pow(a,n,p)-pow(b,n,p))%p
            for i in range(n):
                for j in range(n):
                    actualT=sum(H[i][j]*pow(w,k*(i-j)%n,p) for k in range(n))*pow(n,p-2,p)%p
                    expectedT=(sum(pow(b,k,p)*pow(w,k*i%n,p)for k in range(n))*pow(D,p-2,p)%p) if i==j else 0
                    actualS=sum(H[(i-k)%n][(j-k)%n]for k in range(n))*pow(n,p-2,p)%p
                    expectedS=pow(a,(i-j)%n,p)*pow(D,p-2,p)%p
                    assert actualT==expectedT and actualS==expectedS
                    stats['twirl_checks']+=2
        stats['cases'].append({'n':n,'prime':p,'full_fourier_block_rank':n//2,
                              'even_center_mode':full_coeff})
    # Independent span-rank verification from actual inverse matrices, not mask counts.
    spans=[]
    for n,p in [(3,307),(4,97),(5,521),(6,97),(7,701),(8,97),(9,919),(10,101)]:
        w=primitive_root(n,p);vectors=[]
        for eps in (-1,1):
            for delta in (-1,1):
                for alpha in range(n+2):
                    for beta in range(n+2):
                        if (1-pow(alpha,n,p)-pow(beta,n,p))%p==0:continue
                        H=invmat(build_A(n,p,w,alpha,beta,eps,delta),p)
                        row=[coefficient(H,n,p,w,a,b)for a in range(n)for b in range(n)]
                        vectors.append(row)
        rr=row_rank(vectors,p)
        assert rr==n*n-int(n%2==0)
        spans.append({'n':n,'sampled_paths':len(vectors),'span_rank':rr,'full_space_dimension':n*n})
    stats['four_direction_numeric_spans']=spans
    # Multi-layer cross-cut test of sums of products, with diagonal gauges.
    rng=random.Random(41717);deep_count=0
    for n,p in [(5,521),(8,97),(9,919),(12,97),(16,97)]:
        w=primitive_root(n,p);m=n//2
        for trial in range(35):
            A=[[0]*n for _ in range(n)]
            budget=0
            for z in range(rng.randrange(1,5)):
                P=[[int(i==j)for j in range(n)]for i in range(n)]
                depth=rng.randrange(1,5);budget+=depth
                for _ in range(depth):
                    alpha=rng.randrange(1,p);beta=rng.randrange(1,p)
                    if (1-pow(alpha,n,p)-pow(beta,n,p))%p==0:beta=0
                    eps=rng.choice([-1,1]);delta=rng.choice([-1,1])
                    G=invmat(build_A(n,p,w,alpha,beta,eps,delta),p)
                    P=[[sum(G[i][k]*P[k][j]for k in range(n))%p for j in range(n)]for i in range(n)]
                    gauges=[rng.randrange(1,p)for i in range(n)]
                    P=[[gauges[i]*v%p for v in row]for i,row in enumerate(P)]
                scalar=rng.randrange(1,p)
                A=[[(A[i][j]+scalar*P[i][j])%p for j in range(n)]for i in range(n)]
            lower=row_rank([[A[i][j]for j in range(m)]for i in range(n-m,n)],p)
            upper=row_rank([[A[i][j]for j in range(n-m,n)]for i in range(m)],p)
            assert lower<=budget and upper<=budget
            deep_count+=1
    stats['independent_mixed_depth_rank_certificates']=deep_count
    return stats


def large_audit():
    n=65536;p=998244353;w=primitive_root(n,p)
    random_gen=random.Random(14002026)
    x=[random_gen.randrange(p)for _ in range(n)]
    alpha=17;beta=23
    G=MagneticGreen(n,p,w,alpha,beta,1,1)
    ops=Counts();y=G.apply(x,ops)
    assert len(y)==n
    power=1
    for i in range(n):
        d=(1-beta*power)%p
        assert (d*y[i]-alpha*y[(i-1)%n])%p==x[i]
        power=power*w%p
    sample_rows=[0,1,7,37,513,4096,32768,65535]
    for i in sample_rows:
        assert y[i]==kernel_row(i,x,n,p,w,alpha,beta,1,1)
    omega_total=pow(n,-1,p)
    fft_rows=[]
    for i in [0,1,123,1024,4096,32768,65535]:
        # This is the actual DFT, NOT the Green operator.
        pow_i=pow(w,i,p);pw=1;val=0
        for j in range(n):
            val=(val+x[j]*pw)%p;pw=pw*pow_i%p
        fft_rows.append(val)
    assert any(y[i]!=val for i,val in zip([0,1,123,1024,4096,32768,65535],fft_rows))
    # Two distinct N-way twirls evaluated and certified at all N entries.
    ys,cs=fused_weyl_twirl(x,p,w,alpha,beta,'S')
    yt,ct=fused_weyl_twirl(x,p,w,alpha,beta,'T')
    den=(1-pow(alpha,n,p)-pow(beta,n,p))%p
    rhs_s=(1-pow(alpha,n,p))*pow(den,-1,p)%p
    rhs_t=(1-pow(beta,n,p))*pow(den,-1,p)%p
    pw=1
    for i in range(n):
        assert (ys[i]-alpha*ys[(i-1)%n])%p==rhs_s*x[i]%p
        assert (1-beta*pw)*yt[i]%p==rhs_t*x[i]%p
        pw=pw*w%p
    # Full-rank long-range cut interaction in one linear-work strided solve.
    stride=n//2
    long=StridedMagneticGreen(n,p,w,2,0,stride)
    cl=Counts();long_y=long.apply(x,cl)
    inv3=pow((1-4)%p,p-2,p)
    for i in range(n):
        assert (long_y[i]-2*long_y[(i-stride)%n])%p==x[i]
        assert long_y[i]==(x[i]+2*x[(i-stride)%n])*inv3%p
    # A singular local pivot, but a valid global inverse.
    G2=MagneticGreen(n,p,w,2,1)
    y2=G2.apply(x)
    assert G2.d[0]==0
    power=1
    for i in range(n):
        assert ((1-power)*y2[i]-2*y2[(i-1)%n])%p==x[i]
        power=power*w%p
    for i in [0,1,17,256,65535]:
        assert y2[i]==kernel_row(i,x,n,p,w,2,1,1,1)
    return {'length':n,'prime':p,'input_sha256':hashlib.sha256(','.join(map(str,x)).encode()).hexdigest(),
            'fully_verified_magnetic_equations':2*n,
            'independent_kernel_rows':len(sample_rows)+5,
            'independent_direct_DFT_rows':len(fft_rows),
            'DFT_distinct_from_Green':True,
            'standard_case':{'preparation':G.prep.as_dict(),'online':ops.as_dict(),
                             'total_field_ops':G.prep.field_ops+ops.field_ops},
            'zero_pivot_case':{'prep':G2.prep.as_dict()},
            'both_full_twirl_output_checks':2*n,
            'twirl_field_ops':{'S':cs.field_ops,'T':ct.field_ops},
            'long_range_stride':stride,
            'long_range_cut_rank_theoretical':stride,
            'long_range_full_reference_coefficients':n,
            'long_range_field_ops':{'preparation':long.prep.as_dict(),
                                    'online':cl.as_dict(),
                                    'total':long.prep.field_ops+cl.field_ops}}


def same_operator_comparison():
    data=[]
    for n,p in [(32,97),(64,193),(256,257),(1024,12289)]:
        w=primitive_root(n,p);a=2;b=3
        assert (1-pow(a,n,p)-pow(b,n,p))%p!=0
        x=[(i*i+19*i+17)%p for i in range(n)]
        G=MagneticGreen(n,p,w,a,b)
        count=Counts();fast=G.apply(x,count)
        slow=polynomial_apply(x,n,p,w,a,b)
        assert fast==slow
        # Count an explicitly described naive calculation:
        # at each k: n accumulator additions + n*(2 mult+1 add) for W z
        # plus output normalization (n mult). Root table costs are separate.
        theoretical_naive_ops=4*n*n+n
        data.append({'n':n,'magnetic_prep_and_online_field_ops':G.prep.field_ops+count.field_ops,
                     'naive_polynomial_online_field_ops':theoretical_naive_ops,
                     'naive_over_fused_ratio':round(theoretical_naive_ops/(G.prep.field_ops+count.field_ops),2)})
    return data


def main():
    out={'status':'exact prime-field audit; no universal FFT result',
         'small':small_audit(),'same_operator_comparison':same_operator_comparison(),
         'large':large_audit(),
         'notes':['Separate direct inverse and q-polynomial evaluator used for small cases.',
                  'One input-independent primitive root of unity is supplied in the arithmetic model.',
                  'Modular inverse charged as one field operation; not bit complexity.',
                  'Fourier coefficients evaluated independently only for selected rows in large case.',
                  'No historical novelty claim: q-binomial and Green quasiseparable ingredients are established.']}
    path=HERE/'AUDIT_RESULTS.json'
    path.write_text(json.dumps(out,indent=2))
    print(json.dumps({'status':'PASS','basis_vectors':out['small']['basis_vectors'],
                      'small_coefficients':out['small']['matrix_coefficients'],
                      'cut_rank_certificates':out['small']['block_rank_certificates'],
                      'missing_weyl_coefficients':out['small']['qbinomial_support_zeros'],
                      'even_defects':out['small']['even_defect_certificates'],
                      'odd_orientation_witnesses':out['small']['odd_three_orientation_witnesses'],
                      'large_n':out['large']['length'],'large_ops':out['large']['standard_case']['total_field_ops']}))

if __name__=='__main__':main()
