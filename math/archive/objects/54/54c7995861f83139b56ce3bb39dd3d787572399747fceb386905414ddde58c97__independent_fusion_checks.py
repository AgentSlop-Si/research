"""Fresh finite controls; reads/imports no supplied research code or data."""
from itertools import combinations
from math import prod
import json

P = 65537

def inv(x):
    assert x % P
    return pow(x, P - 2, P)

def root(n, odd=1):
    assert (P - 1) % n == 0
    w = pow(3, ((P - 1) // n) * odd, P)
    assert pow(w, n, P) == 1
    if n > 1:
        assert pow(w, n // 2, P) != 1
    return w

def rank(a):
    a = [[v % P for v in row] for row in a]
    nr, nc = len(a), len(a[0]) if a else 0
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = inv(a[r][c])
        a[r] = [(v * z) % P for v in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [(u - z * v) % P for u, v in zip(a[i], a[r])]
        r += 1
        if r == nr:
            break
    return r

def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) % P
             for col in zip(*b)] for row in a]

def fractional(B, Q, a, odd=1):
    w = root(B * Q, odd)
    z = pow(w, Q, P)
    ib = inv(B)
    return [[ib * sum(pow(w, a * u, P) * pow(z, ((k-j)*u) % B, P)
                     for u in range(B)) % P
             for k in range(B)] for j in range(B)]

def main():
    out = {"field": P, "primitive_generator": 3, "counts": {}, "witnesses": {}}
    rank_cases = 0
    # Arbitrary source sets: no assumption that selected columns are consecutive.
    for N in (4, 8, 16):
        for odd in (1, 3):
            w = root(N, odd)
            for M in range(1, min(5, N) + 1):
                for d in range(1, M + 1):
                    for S in combinations(range(N), d):
                        for start in (0, N-1):
                            a = [[pow(w, ((start+i) * s) % N, P) for s in S]
                                 for i in range(M)]
                            assert rank(a) == d
                            rank_cases += 1
    out["counts"]["arbitrary_source_interval_rank"] = rank_cases
    channel_cases = 0
    for n in range(2, 11):
        N = 1 << n
        for k in range(1, n // 2 + 1):
            Q, B = 1 << k, 1 << (n-k)
            for odd in (1, 3):
                w = root(N, odd)
                for v in (0, Q-1):
                    # First Q outputs of one complete header block already suffice.
                    for j in (0, B-1):
                        A = [[pow(w, ((B*v+u)*(a+Q*j)) % N, P)
                              for a in range(Q)] for u in range(Q)]
                        assert rank(A) == Q
                        channel_cases += 1
    out["counts"]["local_channel_rank"] = channel_cases
    frac_cases = minor_cases = product_cases = 0
    for B in (2, 4, 8, 16):
        for Q in (2, 4, 8):
            for odd in (1, 3):
                w = root(B*Q, odd)
                z = pow(w, Q, P)
                for a in range(1, Q):
                    K = fractional(B, Q, a, odd)
                    c = (1-pow(w, a*B, P))*inv(B) % P
                    G = [[c*inv(1-pow(w, a, P)*pow(z, (k-j) % B, P)) % P
                          for k in range(B)] for j in range(B)]
                    assert K == G
                    assert all(v for row in K for v in row)
                    assert rank(K) == B
                    assert rank([row[B//2:] for row in K[:B//2]]) == B//2
                    frac_cases += 1
                    if B <= 4:
                        for d in range(1, B+1):
                            for rows in combinations(range(B), d):
                                for cols in combinations(range(B), d):
                                    assert rank([[K[i][j] for j in cols] for i in rows]) == d
                                    minor_cases += 1
                    else:
                        for d in (1, 2, B//2, B):
                            rows = list(range(B-1, B-1-d, -1))
                            cols = [(3*j+1) % B for j in range(d)]
                            assert rank([[K[i][j] for j in cols] for i in rows]) == d
                            minor_cases += 1
                ident = [[int(i == j) for j in range(B)] for i in range(B)]
                assert fractional(B,Q,0,odd) == ident
                assert mm(fractional(B,Q,1,odd),fractional(B,Q,-1,odd)) == ident
                # K_Q acts by x[j-1] for this positive-exponent Fourier convention.
                shift = [[int(k == (j-1) % B) for k in range(B)] for j in range(B)]
                assert fractional(B,Q,Q,odd) == shift
                assert mm(fractional(B,Q,1,odd),fractional(B,Q,2,odd)) == fractional(B,Q,3,odd)
                product_cases += 1
    out["counts"].update(fractional_kernel_cases=frac_cases,
                         cauchy_square_minor_cases=minor_cases,
                         fractional_group_law_cases=product_cases)
    N,Q,B=8,2,4
    w=root(N)
    right=[pow(w,u,P) for u in range(B)]
    wrong=[1]*B
    assert right != wrong
    out["witnesses"]["omitted_twiddle_single_input"]={
        "N":N,"Q":Q,"B":B,"input_index":1,"header":0,
        "true_unnormalized_output":right,"wrong_fused_output":wrong}
    # A separated twiddle has exact Q rank when B>=Q; deleting it makes rank one.
    twiddle=[[pow(w,a*u,P) for a in range(Q)] for u in range(B)]
    assert rank(twiddle)==Q and rank([[1]*Q for _ in range(B)])==1
    # Composite Fourier matrices do NOT have all minors nonzero without interval rows.
    w=root(8)
    singular=[[pow(w,r*c,P) for c in (0,4)] for r in (0,2)]
    assert rank(singular)==1
    out["witnesses"]["no_unrestricted_fourier_full_spark"]={"N":8,"rows":[0,2],"columns":[0,4],"rank":1}
    # A fractional shift differs fundamentally: all its square minors are Cauchy minors.
    # Working-root controls use fresh elementary integer arithmetic only.
    def prime(x):
        return x >= 2 and all(x % d for d in range(2, int(x**0.5)+1))
    root_rows=[]
    for n in range(3,17):
        N=1<<n
        R=1; primes=[]; p=3
        while R*p <= 2*N:
            R*=p; primes.append(p)
            p+=2
            while not prime(p):p+=2
        L=R
        while L<2*N:L*=2
        e=(L//R).bit_length()-1
        top=1 << (16*L-1).bit_length()
        D=2*N*L*top
        phi_R=prod(q-1 for q in primes)
        assert 2*N <= L < 4*N and D<1024*N**3
        assert R>2*N/p and phi_R*(len(primes)+2)>=2*R
        # Cyclotomic degree formula for Q(zeta_D) / Q(zeta_N), N dividing D.
        two_power=D//R
        degree=(two_power//N)*phi_R
        assert degree>=phi_R>1 and D%N==0
        root_rows.append({"N":N,"odd_primorial":R,"next_prime":p,"working_length":L,
                          "master_root_order":D,"odd_extension_degree":phi_R,
                          "specified_master_extension_degree":degree})
    out["root_model_controls"]=root_rows
    out["status"]="all fresh finite controls passed; proofs are in the report"
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
