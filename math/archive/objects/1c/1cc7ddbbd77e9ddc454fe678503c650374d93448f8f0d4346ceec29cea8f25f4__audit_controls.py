"""Independent finite controls. Does not load any supplied code or source files."""
import itertools
import json

P = 97
GEN = 5

def matrix_rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    piv = 0
    for col in range(len(a[0])):
        candidates = [i for i in range(piv, len(a)) if a[i][col] % P]
        if not candidates:
            continue
        i = candidates[0]
        a[piv], a[i] = a[i], a[piv]
        scale = pow(a[piv][col], -1, P)
        a[piv] = [scale * v % P for v in a[piv]]
        for k in range(piv + 1, len(a)):
            scale = a[k][col]
            a[k] = [(v - scale * w) % P for v, w in zip(a[k], a[piv])]
        piv += 1
        if piv == len(a):
            break
    return piv

def omega(n):
    assert (P - 1) % n == 0
    z = pow(GEN, (P - 1) // n, P)
    assert pow(z, n, P) == 1
    assert n == 1 or pow(z, n // 2, P) != 1
    return z

def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % P
             for j in range(len(b[0]))] for i in range(len(a))]

def kernel(n, b, a):
    w = omega(n)
    q = n // b
    return [[sum(pow(w, ((a + q*(k-j))*u) % n, P) for u in range(b))
             * pow(b, -1, P) % P for k in range(b)] for j in range(b)]

counts = {"interval_column_ranks": 0, "local_channel_ranks": 0,
          "fractional_kernels": 0, "all_square_minors": 0,
          "negative_and_boundary_cases": 0}

# Complete source-subset checks, including wrapped intervals and empty sets.
for n in (1, 2, 4, 8, 16):
    w = omega(n)
    for m in range(1, min(n, 4) + 1):
        for start in range(n):
            for d in range(m + 1):
                for cols in itertools.combinations(range(n), d):
                    mat = [[pow(w, (start+i)*s, P) for s in cols] for i in range(m)]
                    assert matrix_rank(mat) == d
                    counts["interval_column_ranks"] += 1

# Check rank=min(B,Q) without assuming B>=Q, for every coordinate block/header.
for n in (1, 2, 4, 8, 16, 32):
    w = omega(n)
    q = 1
    while q <= n:
        b = n // q
        for j in range(b):
            for v in range(q):
                mat = [[pow(w, (b*v+u)*(a+q*j), P) for a in range(q)]
                       for u in range(b)]
                assert matrix_rank(mat) == min(b, q)
                counts["local_channel_ranks"] += 1
        q *= 2

# Direct conjugated Fourier kernel versus rational formula, including a<0.
for n in (2, 4, 8, 16, 32):
    w = omega(n)
    b = 1
    while b <= n:
        q = n // b
        identity = [[int(i == j) for j in range(b)] for i in range(b)]
        assert kernel(n, b, 0) == identity
        for a in range(-q, q+1):
            k = kernel(n, b, a)
            if a % q == 0:
                shift = [[int(col == (row-a//q) % b) for col in range(b)]
                         for row in range(b)]
                assert k == shift
                counts["negative_and_boundary_cases"] += 1
                continue
            c = (1 - pow(w, (a*b) % n, P)) * pow(b, -1, P) % P
            direct = [[c * pow((1-pow(w, (a+q*(col-row)) % n, P)) % P, -1, P) % P
                       for col in range(b)] for row in range(b)]
            assert k == direct
            assert multiply(k, kernel(n,b,-a)) == identity
            assert all(entry for row in k for entry in row)
            counts["fractional_kernels"] += 1
            if b <= 4:
                for size in range(1,b+1):
                    for rows in itertools.combinations(range(b),size):
                        for cols in itertools.combinations(range(b),size):
                            assert matrix_rank([[k[i][j] for j in cols] for i in rows]) == size
                            counts["all_square_minors"] += 1
        b *= 2

w = omega(8)
assert matrix_rank([[pow(w,r*c,P) for c in (0,4)] for r in (0,2)]) == 1
assert matrix_rank([[pow(w,r*c,P) for c in (0,4)] for r in (0,1)]) == 2
counts["negative_and_boundary_cases"] += 2

# A legal base parameter choice need not meet the fusion strengthening.
assert 7 >= 7 and 64 + 14 <= 78
k = min(78, 2*64 + 14)
assert k == 78 and 78 < 2*k
counts["negative_and_boundary_cases"] += 1

def isprime(x):
    for d in range(2,x):
        if d*d > x:
            break
        if x % d == 0:
            return False
    return x >= 2

def totient(x):
    value = x
    divisor = 2
    while divisor*divisor <= x:
        if x % divisor == 0:
            value = value // divisor * (divisor-1)
            while x % divisor == 0:
                x //= divisor
        divisor += 1
    if x > 1:
        value = value // x * (x-1)
    return value

root_controls=[]
for exponent in range(3,17):
    n=2**exponent
    r=1
    p=3
    ell=0
    while r*p <= 2*n:
        r*=p
        ell+=1
        p+=2
        while not isprime(p):
            p+=2
    w=r
    while w<2*n:
        w*=2
    top=1
    while top<16*w:
        top*=2
    d=2*n*w*top
    phi=totient(r)
    assert 2*n<=w<4*n and d<1024*n**3
    assert phi*(ell+2)>=2*r and phi*(ell+2)*p>4*n
    assert d%n==0 and totient(d)//totient(n)==(d//r//n)*phi
    root_controls.append({"N":n,"ell":ell,"R":r,"next_prime":p,
                          "phi_R":phi,"D":d,"degree":totient(d)//totient(n)})

print(json.dumps({"field":P, "generator":GEN, "counts":counts,
                  "root_controls":root_controls,
                  "status":"all independently authored finite controls passed",
                  "scope":"finite corroboration, not an all-size or characteristic-zero proof"},
                 indent=2, sort_keys=True))
