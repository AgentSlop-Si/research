"""Independent exact test of the concrete two-Green stage in the supplied archive.

S = (3I - path_adjacency)^-1 + (4I - path_adjacency)^-1.
Runs over F_998244353, without the archived implementation. Uses exact
tridiagonal elimination to form full columns only for independent audit;
the actual stage applies with two O(N) solves.
"""
from minor_certificate import MOD, rank_mod, run_case, permutation, chosen_interval, fourier_minor


def tridiagonal_solve(diag, rhs, off=-1, p=MOD):
    n = len(rhs)
    d = [diag] * n
    y = list(rhs)
    for i in range(1, n):
        alpha = off * pow(d[i - 1], -1, p) % p
        d[i] = (d[i] - alpha * off) % p
        y[i] = (y[i] - alpha * y[i - 1]) % p
    y[n - 1] = y[n - 1] * pow(d[n - 1], -1, p) % p
    for i in range(n - 2, -1, -1):
        y[i] = (y[i] - off * y[i+1]) * pow(d[i], -1, p) % p
    return y


def sum_green_matrix(n, p=MOD):
    a = []
    for j in range(n):
        e = [int(i==j) for i in range(n)]
        x = tridiagonal_solve(3, e)
        y = tridiagonal_solve(4, e)
        a.append([(u+v)%p for u,v in zip(x,y)])
    return [[a[j][i] for j in range(n)] for i in range(n)]


def actual_green_case(n=64, shuffle='random'):
    from minor_certificate import rectangular_product
    assert n in (32,64,128)
    G = sum_green_matrix(n)
    # The integer field's matrix has full rank and all entries are nonzero.
    assert rank_mod(G) == n
    assert all(v for row in G for v in row)
    pi = permutation(n, shuffle)
    m,s,c = chosen_interval(pi)
    parts = [
        rectangular_product(G,G,pi,m,s,lambda k:k>=m),
        rectangular_product(G,G,pi,m,s,lambda k:k<m and pi[k]<s),
        rectangular_product(G,G,pi,m,s,lambda k:k<m and pi[k]>=s+m),
        rectangular_product(G,G,pi,m,s,lambda k:k<m and s<=pi[k]<s+m),
    ]
    ranks = [rank_mod(x) for x in parts]
    assert ranks[0] <= 2 and ranks[1] <= 2 and ranks[2] <= 2 and ranks[3] <= c
    summed = [[sum(q[i][j] for q in parts)%MOD for j in range(m)] for i in range(m)]
    rank_GPG=rank_mod(summed)
    rank_F=rank_mod(fourier_minor(n,m,s))
    assert rank_GPG<=2+2*2+c
    if n>=64: assert rank_GPG<rank_F
    return dict(n=n, shuffle=shuffle, m=m, J=[s,s+m], c=c,
                component_ranks=ranks, rank_product=rank_GPG, rank_fourier=rank_F)

if __name__=='__main__':
    import json
    print(json.dumps([actual_green_case(64,s) for s in ('identity','reverse','bitrev','random')],indent=2))


def actual_green_halfcut_case(n=32, shuffle='random'):
    """Audit the stronger linear bound on the supplied exact two-Green stage."""
    from halfcut_certificate import rectangle, add_mod, halfcut_selection
    assert n in (32,64)
    G = sum_green_matrix(n)
    pi = permutation(n,shuffle)
    m=n//2
    I=list(range(m)); R=list(range(m,n))
    weights=[1]*n
    detail=[]
    for side,J in [('left',I),('right',R)]:
        js=set(J)
        inner=[k for k in I if pi[k] in js]
        outer=[k for k in I if pi[k] not in js]
        parts=[rectangle(G,G,pi,I,J,ks,weights) for ks in (R,outer,inner)]
        ranks=[rank_mod(q) for q in parts]
        assert ranks[0]<=2 and ranks[1]<=2 and ranks[2]<=len(inner)
        rank_result=rank_mod(add_mod(*parts))
        assert rank_result<=4+len(inner)
        detail.append({'side':side,'inside':len(inner),'component_ranks':ranks,
                       'product_rank':rank_result,'fourier_rank':rank_mod(fourier_minor(n,m,J[0]))})
    assert sum(d['inside'] for d in detail)==m
    assert any(d['product_rank']<m for d in detail)
    return {'N':n,'permutation':shuffle,'details':detail}
