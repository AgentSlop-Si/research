"""Phase18 Weyl-line support certificates; n odd prime, char(field) != n.
A phase-gauged one-direction linear combination lies on one affine Weyl line.
"""
from phase18 import primitive_nth_root


def is_prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**0.5)+1))


def trace_weyl_coefficient(A,a,b,p,omega):
    """(1/n) tr[(S^a T^b)^-1 A] in standard Weyl coordinates."""
    n=len(A)
    return (pow(n,-1,p)*sum(pow(omega,-b*i%n,p)*A[(i+a)%n][i]
                              for i in range(n)))%p


def fourier_matrix(n,p,omega):
    return [[pow(omega,-i*j%n,p) for j in range(n)] for i in range(n)]


def weyl_support(A,p,omega):
    n=len(A)
    return {(a,b) for a in range(n) for b in range(n)
            if trace_weyl_coefficient(A,a,b,p,omega)}


def lines_through_origin(n):
    """All n+1 projective lines in F_n^2, n prime."""
    if not is_prime(n):raise ValueError('n must be prime')
    lines=[]
    for slope in range(n):
        lines.append({(t,t*slope%n) for t in range(n)})
    lines.append({(0,t) for t in range(n)})
    return lines


def affine_lines(n):
    """All n(n+1) affine lines in F_n^2 (for independent support checks)."""
    lines=[]
    for origin_line in lines_through_origin(n):
        seen=set()
        for a in range(n):
            for b in range(n):
                line=frozenset({((a+i)%n,(b+j)%n) for i,j in origin_line})
                if line not in seen:
                    seen.add(line)
        lines.extend(seen)
    assert len(lines)==n*(n+1)
    return lines


def exact_fourier_gauss_coeff(a,b,n,p,omega):
    """Equivalent closed form from completing the square: c_ab=G/n * omega^((a+b)^2/4)."""
    inv4=pow(4,-1,n)
    g=sum(pow(omega,-t*t%n,p) for t in range(n))%p
    return g*pow(n,-1,p)*pow(omega,((a+b)**2*inv4)%n,p)%p


if __name__=='__main__':
    for n,p in [(3,7),(5,241),(7,29),(11,23)]:
        w=primitive_nth_root(n,p)
        support=weyl_support(fourier_matrix(n,p,w),p,w)
        assert len(support)==n*n
        assert all(trace_weyl_coefficient(fourier_matrix(n,p,w),a,b,p,w)==
                   exact_fourier_gauss_coeff(a,b,n,p,w)
                   for a in range(n) for b in range(n))
        ls=lines_through_origin(n)
        assert len(set().union(*ls))==n*n
        assert len(set().union(*ls[:-1]))==n*n-n+1
        print('prime dimension',n,'field',p,'nonzero Fourier Weyl coefficients',len(support),
              'required origin-lines',n+1,'required affine-lines',n)
