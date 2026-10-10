#!/usr/bin/env python3
"""Independent exact controls. No target/predecessor code is read or imported."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent
TARGET = Path('marker_cut_compression_0229/EXACT_MARKER_CUT_COMPRESSION.md')
EXPECTED = '8bc97582cb933e29bc16d4efb8c581a612af12813f630b6233256fd27c418628'
assert sha256(TARGET.read_bytes()).hexdigest() == EXPECTED
COUNTS = dict(parameter_sets=0, global_source_basis=0, retained_R_basis=0,
              arbitrary_source_vectors=0, arbitrary_jets=0, fresh_full_outputs=0,
              rank_checks=0, direct_path_phase_checks=0, rational_moments=0,
              count_cases=0, old_kernel_counterexamples=0)

def gamma(k):
    ans = 0
    while k:
        if k & 1:
            ans += k // 2
        k //= 2
    return ans

def rev(k, t):
    ans = 0
    for _ in range(t):
        ans = 2 * ans + (k & 1)
        k //= 2
    return ans

def step(v, root, p):
    size = len(v)
    out = [0] * size
    phase = 1
    for s, value in enumerate(v):
        out[(2*s) % size] = (out[(2*s) % size] + value) % p
        out[(2*s+1) % size] = (out[(2*s+1) % size] + phase*value) % p
        phase = phase*root % p
    return out

class Cut:
    def __init__(self, n, b, p):
        self.n, self.b, self.p = n, b, p
        self.N, self.d = 1 << n, n-b
        self.r = 1 << self.d
        self.omega = pow(3, (p-1)//self.N, p)
        assert pow(self.omega, self.N, p) == 1
        assert pow(self.omega, self.N//2, p) != 1
        self.eta = pow(self.omega, 1 << b, p)
        self.weights = [pow(self.omega, s, p) for s in range(self.N)]
        marker = '0'*b
        self.R, self.A = [], []
        self.E = [[] for _ in range(self.d+1)]
        self.age = {}
        for s in range(self.N):
            word = format(s, '0%db' % n)
            last = word.rfind(marker)
            if word.endswith(marker):
                self.R.append(s)
            elif last < 0:
                self.A.append(s)
            else:
                h = n-last-b
                self.E[h].append(s)
                self.age[s] = h
        self.T = set(self.R+self.A)
        self.eliminated = set(self.age)
        self.e = [len(layer) for layer in self.E]
        assert len(self.T)+sum(self.e) == self.N
        for s in self.A:
            assert all(v in self.T for v, _ in self.edges(s))
        for s, h in self.age.items():
            for v, _ in self.edges(s):
                if v in self.eliminated:
                    assert self.age[v] == h+1
                elif v in self.A:
                    assert h == self.d
        s = 1
        assert self.age[s] == 1
        for h in range(2, self.d+1):
            s = (2*s+1) % self.N
            assert self.age[s] == h
        for h in range(1, self.d+1):
            assert self.e[h] == (1 << (self.d-h))*sum(self.valid(k,h) for k in range(1 << h))

    def edges(self, s):
        return [((2*s) % self.N, 1), ((2*s+1) % self.N, self.weights[s])]

    def valid(self, k, h):
        word = format(k, '0%db' % h)
        return word[0] == '1' and '0'*self.b not in word

    def trajectory(self, u):
        # Full structural lists are retained, including coordinates valued zero.
        sparse = dict(enumerate(u))
        dense = list(u)
        result = []
        for t in range(1, self.d+1):
            nxt = {}
            for a, value in sparse.items():
                for dest, c in [((2*a) % self.r, 1), ((2*a+1) % self.r, pow(self.eta,a,self.p))]:
                    if self.valid(dest % (1 << t), t):
                        nxt[dest] = (nxt.get(dest,0)+c*value) % self.p
            sparse = nxt
            dense = step(dense, self.eta, self.p)
            assert len(sparse) == self.e[t]
            assert sparse == {a:dense[a] for a in range(self.r) if self.valid(a % (1 << t),t)}
            result.append(sparse)
        return result

    def recovery_route(self, q, h):
        out = [0]*self.N
        ratio = self.omega*pow(self.eta,-1,self.p) % self.p
        seen = set()
        for a, value in q.items():
            k = a % (1 << h)
            dest = ((1 << self.b)*(a-k)+k) % self.N
            assert dest in self.E[h] and dest not in seen
            seen.add(dest)
            out[dest] = pow(ratio,gamma(k),self.p)*value % self.p
        assert seen == set(self.E[h])
        return out

    def rr_route(self, q, t):
        out = [0]*self.N
        ratio = self.omega*pow(self.eta,-1,self.p) % self.p
        for a, value in q.items():
            k = a % (1 << t)
            if k & 1:
                index = ((1 << self.b)*(a-k)+k) % self.r
                dest = (1 << self.b)*index
                out[dest] = (out[dest]+pow(ratio,gamma(k),self.p)*value) % self.p
        return out

    def ra_route(self, q):
        out = [0]*self.N
        for w in range(1 << (self.d+1)):
            if self.valid(w,self.d+1):
                assert w in self.A
                a = w//2
                out[w] = pow(self.omega,gamma(w),self.p)*pow(self.eta,-gamma(a),self.p)*q[a] % self.p
        return out

    def source_layers(self, x):
        jet = [[0]*self.N for _ in range(self.n+1)]
        for s in self.T:
            jet[0][s] = x[s]
        layer = {s:[x[s]] for s in self.E[1]}
        for h in range(1,self.d+1):
            nxt = {s:[x[s]]+[0]*h for s in (self.E[h+1] if h<self.d else [])}
            for s, poly in layer.items():
                for dest, c in self.edges(s):
                    for degree, value in enumerate(poly):
                        if dest in self.T:
                            jet[degree+1][dest] = (jet[degree+1][dest]+c*value) % self.p
                        else:
                            nxt[dest][degree+1] = (nxt[dest][degree+1]+c*value) % self.p
            layer = nxt
        return jet

    def source_killed(self, x):
        jet = [[0]*self.N for _ in range(self.n+1)]
        for s in self.T:
            jet[0][s] = x[s]
        free = [x[s] if s in self.eliminated else 0 for s in range(self.N)]
        for degree in range(1,self.n+1):
            free = step(free,self.omega,self.p)
            for s in self.T:
                jet[degree][s], free[s] = free[s], 0
        assert not any(free)
        return jet

    def compressed_inverse(self, f):
        residual = [row[:] for row in f]
        vs = []
        top = [0]*self.N
        inv_visits = joint_visits = 0
        kappa = max(0,self.d+1-self.b)
        for j in range(self.n+1):
            v = residual[j][:]
            vs.append(v)
            if j < self.n:
                for s in self.T:
                    for dest,c in self.edges(s):
                        if dest in self.T:
                            residual[j+1][dest] = (residual[j+1][dest]+c*v[s]) % self.p
            inverse_age = max(min(kappa,self.d-j), self.d if j<self.b else 0)
            inverse_age = max(0,inverse_age)
            joint_age = min(self.d,self.n-j)
            inv_visits += sum(self.e[1:inverse_age+1])
            joint_visits += sum(self.e[1:joint_age+1])
            if joint_age == 0:
                continue
            qs = self.trajectory([v[s] for s in self.R])
            for t in range(1,min(kappa,self.d-j)+1):
                route = self.rr_route(qs[t-1],t)
                degree = j+self.b+t
                for s in self.R:
                    residual[degree][s] = (residual[degree][s]+route[s]) % self.p
            if j < self.b:
                route = self.ra_route(qs[-1])
                degree = j+self.d+1
                for s in self.A:
                    residual[degree][s] = (residual[degree][s]+route[s]) % self.p
            if 1 <= self.n-j <= self.d:
                route = self.recovery_route(qs[self.n-j-1],self.n-j)
                top = [(a+b) % self.p for a,b in zip(top,route)]
        for s in self.T:
            top[s] = vs[-1][s]
        expected_inv = sum(self.e[t]*max(self.b,self.d-t+1) for t in range(1,self.d+1))
        expected_joint = sum(self.e[t]*(self.n-t+1) for t in range(1,self.d+1))
        assert inv_visits == expected_inv
        assert joint_visits == expected_joint
        assert expected_joint == (self.n+1)*sum(self.e)-sum(t*self.e[t] for t in range(1,self.d+1))
        return vs,top

    def driven_global(self,f):
        state = [0]*self.N
        vs = []
        for j in range(self.n+1):
            if j:
                state = step(state,self.omega,self.p)
            state = [(a+b) % self.p for a,b in zip(state,f[j])]
            vs.append([state[s] if s in self.T else 0 for s in range(self.N)])
        return vs,state

def rank(columns,p):
    pivots = {}
    for col in columns:
        v = col[:]
        for i in sorted(pivots):
            if v[i]:
                c = v[i]
                v = [(a-c*b)%p for a,b in zip(v,pivots[i])]
        i = next((i for i,a in enumerate(v) if a),None)
        if i is not None:
            inv = pow(v[i],-1,p)
            pivots[i] = [a*inv % p for a in v]
    return len(pivots)

def one_case(n,b,p,basis_source,basis_feedback):
    c = Cut(n,b,p)
    COUNTS['parameter_sets'] += 1
    rng = random.Random(1000003*n+1009*b+p)
    columns = []
    for s in (range(c.N) if basis_source else []):
        x = [int(k==s) for k in range(c.N)]
        f = c.source_layers(x)
        assert f == c.source_killed(x)
        COUNTS['global_source_basis'] += 1
        if n <= 5:
            columns.append([f[j][k] for j in range(c.d+1) for k in sorted(c.T)])
    if columns:
        assert rank(columns,p) == c.N
        COUNTS['rank_checks'] += 1
    for j in (range(c.r) if basis_feedback else [0,c.r-1]):
        u = [int(k==j) for k in range(c.r)]
        qs = c.trajectory(u)
        raw = [0]*c.N
        raw[(1 << b)*j] = 1
        free = raw[:]
        for h in range(1,c.d+1):
            free = step(free,c.omega,p)
            for s in c.T:
                free[s] = 0
            assert free == c.recovery_route(qs[h-1],h)
        kappa = max(0,c.d+1-b)
        for length in range(1,n+3):
            raw = step(raw,c.omega,p)
            observed = [raw[s] if s in c.T else 0 for s in range(c.N)]
            expected = [0]*c.N
            if length == 1:
                for dest,a in c.edges((1 << b)*j):
                    if dest in c.T:
                        expected[dest] = a
            t = length-b
            if 1 <= t <= kappa:
                expected = [(a+z)%p for a,z in zip(expected,c.rr_route(qs[t-1],t))]
            if length == c.d+1:
                expected = [(a+z)%p for a,z in zip(expected,c.ra_route(qs[-1]))]
            assert observed == expected, (n,b,p,j,length)
            for s in c.T:
                raw[s] = 0
        COUNTS['retained_R_basis'] += 1
    x = [rng.randrange(p) for _ in range(c.N)]
    f = c.source_layers(x)
    assert f == c.source_killed(x)
    COUNTS['arbitrary_source_vectors'] += 1
    vs, top = c.compressed_inverse(f)
    oracle_vs,oracle_top = c.driven_global(f)
    assert vs == oracle_vs and top == oracle_top
    direct = x[:]
    for _ in range(n):
        direct = step(direct,c.omega,p)
    assert top == direct
    COUNTS['fresh_full_outputs'] += 1
    jet = [[rng.randrange(p) if s in c.T else 0 for s in range(c.N)] for _ in range(n+1)]
    vs,top = c.compressed_inverse(jet)
    oracle_vs,oracle_top = c.driven_global(jet)
    assert vs == oracle_vs and top == oracle_top
    COUNTS['arbitrary_jets'] += 1

def check_moments():
    z = Fraction(1,2)
    for b in range(1,129):
        P = sum(z**j for j in range(b))
        Pd = sum(j*z**(j-1) for j in range(1,b))
        D = 1-sum(z**j for j in range(1,b+1))
        Dd = -sum(j*z**(j-1) for j in range(1,b+1))
        value = (P/D+z*(Pd*D-P*Dd)/D**2)/(1 << (b+1))
        assert value == (1 << (b+1))-b-2
        COUNTS['rational_moments'] += 1
    for n in range(2,129):
        for b in range(1,n):
            a = [1]
            for k in range(1,n+1):
                a.append((1 << k) if k<b else sum(a[max(0,k-b):k]))
            e = [0]+[(1 << (n-b-h))*a[h-1] for h in range(1,n-b+1)]
            N = 1 << n
            M = sum(h*e[h] for h in range(1,len(e)))
            assert M <= N*((1 << (b+1))-b-2)
            assert sum(e)+(1 << (n-b))+a[n] == N
            assert all(h*e[h] <= 2*N for h in range(1,len(e)))
            COUNTS['count_cases'] += 1

def check_paths():
    for p in (257,65537,998244353):
        for n in range(2,9):
            N = 1 << n
            omega = pow(3,(p-1)//N,p)
            rng = random.Random(p+n)
            for t in range(1,n+1):
                pairs = ((s,k) for s in range(N) for k in range(1 << t)) if n<=5 else ((rng.randrange(N),rng.randrange(1 << t)) for _ in range(100))
                for s,k in pairs:
                    state,weight = s,1
                    for shift in range(t-1,-1,-1):
                        bit = (k >> shift)&1
                        if bit:
                            weight = weight*pow(omega,state,p) % p
                        state = (2*state+bit) % N
                    assert state == ((1 << t)*s+k) % N
                    assert weight == pow(omega,s*rev(k,t)+gamma(k),p)
                    COUNTS['direct_path_phase_checks'] += 1

def counterexample():
    N,p,w = 16,65537,64
    R = {0,4,8,12}
    A = {s for s in range(N) if '00' not in format(s,'04b')}
    for T,expected in ((R,64),(R|A,0)):
        x = [1]+[0]*(N-1)
        output = None
        for t in range(1,5):
            x = step(x,w,p)
            if t == 4:
                output = x[12]
            for s in T:
                x[s] = 0
        assert output == expected
    COUNTS['old_kernel_counterexamples'] += 1

if __name__ == '__main__':
    check_moments()
    check_paths()
    for n in range(2,9):
        for b in range(1,n):
            one_case(n,b,257,basis_source=n<=7,basis_feedback=True)
    for n in range(2,11):
        for b in range(1,n):
            one_case(n,b,65537,basis_source=False,basis_feedback=n<=5)
    for n in (3,6,9):
        for b in range(1,n):
            one_case(n,b,998244353,basis_source=False,basis_feedback=False)
    counterexample()
    result = {'status':'PASS','target_sha256':EXPECTED,'counts':COUNTS,
              'fields':[257,65537,998244353],
              'note':'Independent exact finite controls support, but do not replace, the all-size audit proof.'}
    (HERE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
