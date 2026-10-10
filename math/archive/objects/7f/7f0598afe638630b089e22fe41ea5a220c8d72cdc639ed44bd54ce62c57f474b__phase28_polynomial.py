"""Exact finite-field polynomial certificate for a single tunable Green coupling.

Fix a target T=A^-1 F C^-1 and a middle family B(z)=B0+z*B1,
with B0,B1 entrywise nonzero. Define the projective trace invariant
Q(M)=tr([M (M^circ-1)^T]^2). If T is two-sided monomially equivalent
to B(z), then Q(T)=Q(B(z)). After multiplying by the product of the N^2
affine entries of B(z), this becomes a polynomial of degree at most N^2.
This module calculates that polynomial exactly over F_998244353 at small N.
"""
from phase28_synthesis import P,inverse,trace2_from_row_moments,matmul,green_matrix,random_cycle
from random import Random


def product_affines(a:list[list[int]],b:list[list[int]])->list[int]:
    n=len(a); out=[1]
    for i in range(n):
        for j in range(n):
            aa=a[i][j]%P;bb=b[i][j]%P
            z=[0]*(len(out)+1)
            for k,x in enumerate(out):
                z[k]=(z[k]+aa*x)%P
                z[k+1]=(z[k+1]+bb*x)%P
            out=z
    return out


def divide_affine(poly:list[int],a:int,b:int)->list[int]:
    """Exact synthetic division by (a+b*z), with a != 0 mod p."""
    a%=P;b%=P
    if not a:raise ValueError('constant term is zero; reorder division')
    ia=inverse(a)
    q=[]
    prev=0
    for k in range(len(poly)-1):
        x=(poly[k]-b*prev)*ia%P
        q.append(x);prev=x
    if poly[-1]!=b*q[-1]%P:raise ArithmeticError('non-divisible affine factor')
    return q


def multiply_quadratic(p:list[int],a:int,b:int,c:int,d:int)->list[int]:
    a%=P;b%=P;c%=P;d%=P
    co=[a*c%P,(a*d+b*c)%P,b*d%P]
    result=[0]*(len(p)+2)
    for i,x in enumerate(p):
        for j,y in enumerate(co):result[i+j]=(result[i+j]+x*y)%P
    return result


def trace_poly(target_trace:int,a:list[list[int]],b:list[list[int]])->list[int]:
    n=len(a)
    D=product_affines(a,b)
    out=[((n**3-target_trace)*x)%P for x in D]
    for i in range(n):
        for j in range(i+1,n):
            for k in range(n):
                for l in range(n):
                    q=divide_affine(D,a[j][k],b[j][k])
                    q=divide_affine(q,a[i][l],b[i][l])
                    product=multiply_quadratic(q,a[i][k],b[i][k],a[j][l],b[j][l])
                    for ix,x in enumerate(product):out[ix]=(out[ix]+2*x)%P
    while len(out)>1 and out[-1]==0:out.pop()
    return out


def eval_poly(poly:list[int],z:int)->int:
    acc=0
    for x in poly[::-1]:acc=(acc*z+x)%P
    return acc


def evaluate_B(a,b,z):
    n=len(a)
    return [[(a[i][j]+z*b[i][j])%P for j in range(n)] for i in range(n)]


def example(n:int,seed:int=2828)->dict:
    rng=Random(seed+n)
    a=green_matrix(random_cycle(n,rng),inverse(4))
    b=green_matrix(random_cycle(n,rng),inverse(5))
    z=3*inverse(2)%P
    middle=evaluate_B(a,b,z)
    target_trace=trace2_from_row_moments(middle)
    poly=trace_poly(target_trace,a,b)
    # This is a specially tuned positive control: z must be a root.
    assert eval_poly(poly,z)==0
    w=7*inverse(3)%P
    other=evaluate_B(a,b,w)
    direct=trace2_from_row_moments(other)
    D=eval_poly(product_affines(a,b),w)
    assert eval_poly(poly,w)==D*(direct-target_trace)%P
    return {'n':n,'polynomial_degree':len(poly)-1,'degree_upper_bound':n*n,
            'positive_control_root':z,'root_check':eval_poly(poly,z),
            'other_coupling_witness':eval_poly(poly,w),
            'leading_coefficient':poly[-1],'nonzero_polynomial':any(poly)}

if __name__=='__main__':
    for n in (4,8):print(example(n))


def poly_mul(x:list[int],y:list[int])->list[int]:
    out=[0]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        if not a:continue
        for j,b in enumerate(y):out[i+j]=(out[i+j]+a*b)%P
    return out


def poly_trim(p:list[int])->list[int]:
    p=p[:]
    while len(p)>1 and not p[-1]:p.pop()
    return p


def poly_scale(p:list[int],a:int)->list[int]:
    return [(v*a)%P for v in p]


def trace_moment_poly(target_trace:int,a:list[list[int]],b:list[list[int]],s:int)->list[int]:
    """D(z)^s*(trace(C(B(z)^circ s)^2)-target_trace), degree<=s*N^2.

    For each s=1,2,..., the ratio-power condition is a necessary
    invariant under arbitrary row/col monomial gauges.
    """
    if s<1:raise ValueError('positive power')
    n=len(a)
    D=product_affines(a,b)
    common=[1]
    for _ in range(s):common=poly_mul(common,D)
    out=poly_scale(common,(n**3-target_trace)%P)
    for i in range(n):
        for j in range(i+1,n):
            for k in range(n):
                for l in range(n):
                    q=common
                    for _ in range(s):
                        q=divide_affine(q,a[j][k],b[j][k])
                        q=divide_affine(q,a[i][l],b[i][l])
                    ab=poly_mul([a[i][k],b[i][k]],[a[j][l],b[j][l]])
                    numer=[1]
                    for _ in range(s):numer=poly_mul(numer,ab)
                    term=poly_mul(q,numer)
                    for ix,x in enumerate(term):out[ix]=(out[ix]+2*x)%P
    return poly_trim(out)


def gcd_modp(x:list[int],y:list[int])->list[int]:
    """Monic Euclidean gcd in F_p[z]."""
    def rem(a,b):
        a=poly_trim(a);b=poly_trim(b)
        if b==[0]:raise ZeroDivisionError
        invb=inverse(b[-1])
        while len(a)>=len(b) and a!=[0]:
            k=len(a)-len(b);c=a[-1]*invb%P
            for j,val in enumerate(b): a[k+j]=(a[k+j]-c*val)%P
            a=poly_trim(a)
        return a
    x=poly_trim(x);y=poly_trim(y)
    while y!=[0]:x,y=y,rem(x,y)
    if x==[0]:return x
    return poly_scale(x,inverse(x[-1]))


def trace_power_from_matrix(matrix:list[list[int]],s:int)->int:
    from phase28_synthesis import row_pair_moments
    n=len(matrix)
    h=row_pair_moments(matrix,powers=(s,))
    return (n**3+2*sum(h[i][j][0] for i in range(n) for j in range(i+1,n)))%P


def two_moment_gcd_certificate(n:int,seed:int)->dict:
    from phase28_synthesis import (green_sum,green_components,fft_matrix,
                                   matmul,invert)
    a=green_sum(n,seed*3+1)
    b0,b1=green_components(n,seed*3+2)
    c=green_sum(n,seed*3+3)
    target=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    p1=trace_moment_poly(trace_power_from_matrix(target,1),b0,b1,1)
    p2=trace_moment_poly(trace_power_from_matrix(target,2),b0,b1,2)
    g=gcd_modp(p1,p2)
    return {'n':n,'seed':seed,'degree_p1':len(p1)-1,'degree_p2':len(p2)-1,
            'gcd_degree':len(g)-1,'gcd_coefficients':g,
            'nonzero_full_degree_leading_terms':bool(p1[-1] and p2[-1])}

if __name__=='__main__':
    print('GCD checks')
    for n in (4,8):print(two_moment_gcd_certificate(n,2800+n))


def interpolate_consecutive(values:list[int])->list[int]:
    """Exact polynomial interpolation at 0..d over F_p (d < p).

    Expand Newton forward differences into monomial basis. If known deg<=d,
    returned coefficients are the unique exact polynomial.
    """
    d=len(values)-1
    if d>=P:raise ValueError('degree exceeds field characteristic')
    differences=[x%P for x in values]
    falling=[1]
    out=[0]*(d+1)
    factorial=1
    for k in range(d+1):
        coefficient=differences[0]*inverse(factorial)%P
        for i,x in enumerate(falling):out[i]=(out[i]+coefficient*x)%P
        if k==d:break
        differences=[(differences[i+1]-differences[i])%P for i in range(len(differences)-1)]
        falling=poly_mul(falling,[(-k)%P,1])
        factorial=factorial*(k+1)%P
    return poly_trim(out)


def trace_moment_poly_interpolated(target_trace:int,a:list[list[int]],b:list[list[int]],s:int)->list[int]:
    from phase28_synthesis import row_pair_moments
    n=len(a)
    degree=s*n*n
    vals=[]
    for z in range(degree+1):
        m=evaluate_B(a,b,z)
        if any(x==0 for row in m for x in row):
            raise ValueError(f'bad interpolation point {z}; choose shifted sampling grid')
        D=1
        for row in m:
            for x in row:D=D*x%P
        h=row_pair_moments(m,powers=(s,))
        obs=(n**3+2*sum(h[i][j][0] for i in range(n)
                              for j in range(i+1,n)))%P
        vals.append(pow(D,s,P)*(obs-target_trace)%P)
    return interpolate_consecutive(vals)


def interpolated_gcd_certificate(n:int,seed:int)->dict:
    from phase28_synthesis import (green_sum,green_components,fft_matrix,
                                   matmul,invert)
    a=green_sum(n,seed*3+1)
    b0,b1=green_components(n,seed*3+2)
    c=green_sum(n,seed*3+3)
    t=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    p1=trace_moment_poly_interpolated(trace_power_from_matrix(t,1),b0,b1,1)
    p2=trace_moment_poly_interpolated(trace_power_from_matrix(t,2),b0,b1,2)
    g=gcd_modp(p1,p2)
    return {'n':n,'seed':seed,'degree_p1':len(p1)-1,'degree_p2':len(p2)-1,
            'gcd_degree':len(g)-1,'gcd_coefficients':g,
            'both_leading_nonzero':bool(p1[-1] and p2[-1])}


def poly_add(a:list[int],b:list[int])->list[int]:
    n=max(len(a),len(b));z=[0]*n
    for i,x in enumerate(a):z[i]=(z[i]+x)%P
    for i,x in enumerate(b):z[i]=(z[i]+x)%P
    return poly_trim(z)


def poly_sub(a:list[int],b:list[int])->list[int]:
    n=max(len(a),len(b));z=[0]*n
    for i,x in enumerate(a):z[i]=(z[i]+x)%P
    for i,x in enumerate(b):z[i]=(z[i]-x)%P
    return poly_trim(z)


def poly_divmod(a:list[int],b:list[int])->tuple[list[int],list[int]]:
    a=poly_trim(a);b=poly_trim(b)
    if b==[0]:raise ZeroDivisionError
    if len(a)<len(b):return [0],a
    q=[0]*(len(a)-len(b)+1)
    ib=inverse(b[-1])
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b)
        x=a[-1]*ib%P
        q[k]=x
        for j,v in enumerate(b):a[k+j]=(a[k+j]-x*v)%P
        a=poly_trim(a)
    return poly_trim(q),a


def xgcd_modp(a:list[int],b:list[int])->tuple[list[int],list[int],list[int]]:
    """Return monic gcd G and U,V with U*a+V*b=G in F_p[z]."""
    r0=poly_trim(a);r1=poly_trim(b)
    s0,s1=[1],[0]
    t0,t1=[0],[1]
    while r1!=[0]:
        q,r=poly_divmod(r0,r1)
        r0,r1=r1,r
        s0,s1=s1,poly_sub(s0,poly_mul(q,s1))
        t0,t1=t1,poly_sub(t0,poly_mul(q,t1))
    z=inverse(r0[-1])
    g=poly_scale(r0,z);u=poly_scale(s0,z);v=poly_scale(t0,z)
    assert poly_add(poly_mul(u,a),poly_mul(v,b))==g
    return g,u,v


def exceptional_coupling_certificate(n:int,seed:int)->dict:
    from phase28_synthesis import green_sum,green_components,fft_matrix,matmul,invert
    a=green_sum(n,seed*3+1)
    b0,b1=green_components(n,seed*3+2)
    c=green_sum(n,seed*3+3)
    target=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    p1=trace_moment_poly_interpolated(trace_power_from_matrix(target,1),b0,b1,1)
    p2=trace_moment_poly_interpolated(trace_power_from_matrix(target,2),b0,b1,2)
    e=None;power1=power2=0
    if n==16 and seed==2816:
        # Three exactly shared diagonal affine roots, due to identical
        # root-of-unity relative-gauge exponents at rows 5,6,15.
        e=[b0[5][5],b1[5][5]]
        for i in (6,15):
            assert b0[5][5]*b1[i][i]%P==b0[i][i]*b1[5][5]%P
        p1=divide_affine(p1,*e)
        p2=divide_affine(divide_affine(p2,*e),*e)
        power1,power2=1,2
    g,u,v=xgcd_modp(p1,p2)
    return {'n':n,'seed':seed,'prime':P,
            'removed_denominator_factor':e,
            'removed_from_p1':power1,'removed_from_p2':power2,
            'original_degree_upper_bounds':[n*n,2*n*n],
            'reduced_degree_p1':len(p1)-1,'reduced_degree_p2':len(p2)-1,
            'nonzero_reduced_leading_coeffs':bool(p1[-1] and p2[-1]),
            'gcd':g,'p1_coefficients':p1,'p2_coefficients':p2,
            'bezout_u':u,'bezout_v':v,
            'verification_passes':g==[1] and poly_add(poly_mul(u,p1),poly_mul(v,p2))==[1]}
