"""Independent exact finite-field verifier for local-annihilator FFT gates.

Matrices use 0-based indices.  Fourier F[i,j] = omega**(i*j).
A rank-one separated-generator stage has S[i,j]=a[i]*b[j] for i>j,
S[i,i]=d[i], and S[i,j]=c[i]*e[j] for i<j.

P is encoded as perm[src] = destination (P*x)[perm[src]]=x[src].
All operations are over F_p.  No floating point and no external packages.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from bisect import bisect_right
import random


def nth_root(n: int, p: int) -> int:
    assert (p - 1) % n == 0
    for a in range(2, p):
        w = pow(a, (p - 1) // n, p)
        if pow(w, n, p) == 1 and all(pow(w, n//q, p) != 1 for q in prime_factors(n)):
            return w
    raise ValueError('no root')


def prime_factors(n: int):
    r=[]; d=2
    while d*d<=n:
        if n%d==0:
            r.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:r.append(n)
    return r


def rank_mod(matrix, p):
    if not matrix:return 0
    a=[[int(v)%p for v in row] for row in matrix]
    nr=len(a); nc=len(a[0]); rank=0
    assert all(len(row)==nc for row in a)
    for col in range(nc):
        pivot=next((i for i in range(rank,nr) if a[i][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][col],-1,p)
        a[rank]=[x*inv%p for x in a[rank]]
        for i in range(rank+1,nr):
            v=a[i][col]
            if v:a[i]=[(a[i][j]-v*a[rank][j])%p for j in range(nc)]
        rank+=1
        if rank==nr:break
    return rank


def det_mod(matrix,p):
    n=len(matrix)
    if not n:return 1
    assert all(len(row)==n for row in matrix)
    a=[[int(x)%p for x in row] for row in matrix]
    ans=1
    for k in range(n):
        pivot=next((r for r in range(k,n) if a[r][k]),None)
        if pivot is None:return 0
        if pivot!=k:
            a[pivot],a[k]=a[k],a[pivot]
            ans=-ans
        x=a[k][k]
        ans=ans*x%p
        inv=pow(x,-1,p)
        for i in range(k+1,n):
            fac=a[i][k]*inv%p
            if fac:
                for j in range(k+1,n):a[i][j]=(a[i][j]-fac*a[k][j])%p
                a[i][k]=0
    return ans%p


def nullspace_basis(rows, p, width=None):
    """Basis for nullspace of matrix rows; works for all-zero generators."""
    if not rows:
        if width is None:raise ValueError('width required')
        return [[int(i==j) for i in range(width)] for j in range(width)]
    n=len(rows[0]); m=len(rows)
    a=[[int(x)%p for x in row] for row in rows]
    assert all(len(row)==n for row in a)
    pivots=[]; r=0
    for col in range(n):
        ix=next((i for i in range(r,m) if a[i][col]),None)
        if ix is None:continue
        a[r],a[ix]=a[ix],a[r]
        inv=pow(a[r][col],-1,p)
        a[r]=[x*inv%p for x in a[r]]
        for i in range(m):
            if i!=r and a[i][col]:
                fac=a[i][col]
                a[i]=[(a[i][j]-fac*a[r][j])%p for j in range(n)]
        pivots.append(col);r+=1
        if r==m:break
    free=[j for j in range(n) if j not in pivots]
    out=[]
    for j in free:
        v=[0]*n;v[j]=1
        for row,col in enumerate(pivots):v[col]=(-a[row][j])%p
        assert all(sum(x*y for x,y in zip(row,v))%p==0 for row in rows)
        out.append(v)
    return out


def mat_vec(A,v,p):
    return [sum(x*y for x,y in zip(row,v))%p for row in A]


def mat_mul(A,B,p):
    if not A or not B:return []
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(c) for c in zip(*A)] if A else []


def permutation_apply(v, perm):
    out=[0]*len(v)
    for j,z in enumerate(v):out[perm[j]]=z
    return out


def permutation_inverse(perm):
    out=[0]*len(perm)
    for j,z in enumerate(perm):out[z]=j
    return out


def bit_reversal(n):
    assert n>=1 and n&(n-1)==0
    width=n.bit_length()-1
    return [int(f'{j:0{width}b}'[::-1],2) for j in range(n)]


@dataclass
class Stage:
    a: list[int]
    b: list[int]
    c: list[int]
    e: list[int]
    d: list[int]

    @property
    def n(self):return len(self.a)

    def matrix(self,p):
        n=self.n
        return [[(self.a[i]*self.b[j] if i>j else
                  self.c[i]*self.e[j] if i<j else self.d[i])%p
                 for j in range(n)] for i in range(n)]

    def apply(self,x,p):
        n=self.n
        assert len(x)==n
        # Reuse e[i]*x[i]: 5N multiplies, 5N-1 additions/subtractions
        # including the initial suffix accumulation (modular reductions not counted).
        weighted_upper=[self.e[j]*x[j]%p for j in range(n)]
        suffix=sum(weighted_upper)%p
        prefix=0
        result=[]
        for i in range(n):
            suffix=(suffix-weighted_upper[i])%p
            result.append((self.d[i]*x[i]+self.a[i]*prefix+self.c[i]*suffix)%p)
            prefix=(prefix+self.b[i]*x[i])%p
        return result

    @staticmethod
    def random(n,p,seed,zero_probability=0.1):
        rng=random.Random(seed)
        arrays=[]
        for _ in range(5):
            arrays.append([0 if rng.random()<zero_probability else rng.randrange(1,p) for _ in range(n)])
        return Stage(*arrays)


def left_annihilators(stage, start, width, p):
    # y^T stage can be nonzero only on [start,start+width)
    return nullspace_basis([stage.a[start:start+width],stage.c[start:start+width]],p)


def right_annihilators(stage, start, width, p):
    # stage x can be nonzero only on [start,start+width)
    return nullspace_basis([stage.b[start:start+width],stage.e[start:start+width]],p)


def fourier_block(n,omega,I,J,p):
    return [[pow(omega,i*j,p) for j in J] for i in I]


def fourier_apply(x,omega,p):
    n=len(x)
    return [sum(v*pow(omega,i*j,p) for j,v in enumerate(x))%p for i in range(n)]


def casoratian_coefficients(Y,omega,p):
    """For s independent row polys supported in w consecutive exponents.

    det[p_r(z*omega**h)]_{r,h=0..s-1} is z**(s*(s-1)//2)*Q(z).
    Returns exact coefficient list of Q modulo p.
    """
    s=len(Y);w=len(Y[0]);lo=s*(s-1)//2;hi=s*(2*w-s-1)//2
    coeff=[0]*(hi-lo+1)
    for K in combinations(range(w),s):
        minor=det_mod([[row[k] for k in K] for row in Y],p)
        if not minor:continue
        vander=det_mod([[pow(omega,k*h,p) for h in range(s)] for k in K],p)
        coeff[sum(K)-lo]=(coeff[sum(K)-lo]+minor*vander)%p
    return coeff


def eval_poly(coeff,z,p):
    out=0
    for v in reversed(coeff):out=(out*z+v)%p
    return out


def projected_fourier_three(Y,n,omega,j,p):
    return [[sum(v*pow(omega,(j+h)*i,p) for i,v in enumerate(row))%p for h in range(3)] for row in Y]


def two_stage_witness(n,stage1,stage2,perm,omega,p):
    assert n>=24
    I=list(range(5))
    Y=left_annihilators(stage2,0,5,p)[:3]
    assert rank_mod(Y,p)==3
    coeff=casoratian_coefficients(Y,omega,p)
    assert any(coeff)
    forbidden={j for j in range(n-2) if set(perm[j:j+3])&set(I)}
    bad={j for j in range(n-2) if eval_poly(coeff,pow(omega,j,p),p)==0}
    for j in range(n-2):
        if j in forbidden or j in bad:continue
        v3=right_annihilators(stage1,j,3,p)[0]
        x=[0]*n;x[j:j+3]=v3
        lhs=fourier_apply(x,omega,p)
        rhs=stage2.apply(permutation_apply(stage1.apply(x,p),perm),p)
        yp=[sum(y[k]*lhs[k] for k in I)%p for y in Y]
        yr=[sum(y[k]*rhs[k] for k in I)%p for y in Y]
        assert any(yp) and not any(yr)
        return {'n':n,'p':p,'omega':omega,'j':j,
                'Y':Y,'input':v3,'projected_fft':yp,'projected_product':yr,
                'determinant':det_mod(projected_fourier_three(Y,n,omega,j,p),p),
                'bad_determinant_windows':len(bad),'intersecting_windows':len(forbidden),
                'guaranteed_witnesses':n-23}
    raise AssertionError('theorem violated')


def ordering_defect(R,C,n):
    """Minimum number of row/column coordinates to delete for strict separation."""
    w=len(R);assert len(C)==w
    Rs=sorted(R);Cs=sorted(C)
    cuts=sorted(set([-1]+Rs+Cs))
    best=(2*w,None,None)
    for cut in cuts:
        nr=bisect_right(Rs,cut);nc=bisect_right(Cs,cut)
        for k,orient in (((w-nr)+nc,'R-left C-right'),(nr+(w-nc),'R-right C-left')):
            if k<best[0]:best=(k,cut,orient)
    return best


def three_stage_gate(n,p1,p2,W):
    """Find window pair refuted by the rank gate; no coefficient assumptions.

    We require natural-order Fourier endpoints.  p1 sends first-stage output
    indices to middle-stage input indices. p2 sends middle-stage outputs to
    final-stage input indices.
    """
    assert 6<=W<=n
    invp2=permutation_inverse(p2)
    best=None;badcount=0
    for i in range(n-W+1):
        R=[invp2[k] for k in range(i,i+W)]
        for j in range(n-W+1):
            C=[p1[k] for k in range(j,j+W)]
            k,cut,orientation=ordering_defect(R,C,n)
            if best is None or k<best['defect']:
                best={'I_start':i,'J_start':j,'defect':k,'cut':cut,'orientation':orientation,
                      'R':R,'C':C,'W':W,'threshold':W-5}
            if k<W-5:badcount+=1
    best['violating_window_pairs']=badcount
    best['excludes_factorization']=bool(badcount)
    return best


def three_stage_projected_ranks(n,stages,perms,cert,omega,p):
    s1,s2,s3=stages;p1,p2=perms
    W=cert['W'];i=cert['I_start'];j=cert['J_start'];I=list(range(i,i+W));J=list(range(j,j+W))
    Y=left_annihilators(s3,i,W,p)[:W-2]
    X=right_annihilators(s1,j,W,p)[:W-2]
    assert rank_mod(Y,p)==W-2 and rank_mod(X,p)==W-2
    F=fourier_block(n,omega,I,J,p)
    # Each basis vector of X is length W and each row of Y is length W.
    fcomp=mat_mul(mat_mul(Y,F,p),transpose(X),p)
    stage_cols=[]
    for x in X:
        full=[0]*n;full[j:j+W]=x
        z=s1.apply(full,p)
        z=permutation_apply(z,p1)
        z=s2.apply(z,p)
        z=permutation_apply(z,p2)
        z=s3.apply(z,p)
        stage_cols.append([sum(y[k-i]*z[k] for k in I)%p for y in Y])
    acomp=transpose(stage_cols)
    rF=rank_mod(fcomp,p);rM=rank_mod(acomp,p)
    assert rF>=W-4
    assert rM<=1+cert['defect']
    return {'n':n,'W':W,'p':p,'fourier_compression_rank':rF,
            'stage_compression_rank':rM,'stage_rank_bound':cert['defect']+1,
            'fourier_rank_lower_bound':W-4,
            'excludes_factorization': cert['defect']+1<W-4}
