"""Fresh exact controls. Standard library only; no historical code is imported.

Sparse integer polynomials in g, twenty direction coordinates, and t with t^5=1.
The latter gives a coefficient representation whose l1 norm bounds every fifth-
root embedding. Reduction modulo Phi_5 is used separately for zero/norm tests.
"""
from itertools import permutations, product
from math import comb, factorial
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
ZERO = (0,) * 22

def mon(i=None, e=1, t=0, c=1):
    k = list(ZERO)
    if i is not None:
        k[i] = e
    k[-1] = t % 5
    return {tuple(k): c} if c else {}

ONE = mon()

def add(a, b, scale=1):
    r = a.copy()
    for k, v in b.items():
        r[k] = r.get(k, 0) + scale * v
        if not r[k]:
            del r[k]
    return r

def mul(a, b):
    r = {}
    for k, v in a.items():
        for l, w in b.items():
            q = tuple(x + y for x, y in zip(k[:-1], l[:-1])) + ((k[-1] + l[-1]) % 5,)
            r[q] = r.get(q, 0) + v * w
    return {k: v for k, v in r.items() if v}

def reduce_phi(a):
    r = {}
    for k, v in a.items():
        terms = [(k[-1], v)] if k[-1] < 4 else [(j, -v) for j in range(4)]
        for j, w in terms:
            q = k[:-1] + (j,)
            r[q] = r.get(q, 0) + w
    return {k: v for k, v in r.items() if v}

def norm(a):
    r = ONE
    for s in range(1, 5):
        b = {}
        for k, v in a.items():
            q = k[:-1] + ((s * k[-1]) % 5,)
            b[q] = b.get(q, 0) + v
        r = mul(r, b)
    r = reduce_phi(r)
    assert all(k[-1] == 0 for k in r)
    return r

def evalp(a, values, eta=91, p=241):
    result = 0
    for k, v in a.items():
        z = v * pow(eta, k[-1], p)
        for x, e in zip(values, k[:-1]):
            if e:
                z = z * pow(x, e, p) % p
        result = (result + z) % p
    return result

def dehom(a, chart):
    r = {}
    for k, v in a.items():
        q = list(k)
        for j, selected in enumerate(chart):
            q[1 + 2 * j + selected] = 0
        q = tuple(q)
        r[q] = r.get(q, 0) + v
    return {k: v for k, v in r.items() if v}

def l1(a):
    return sum(abs(v) for v in a.values())

def degree(a, lo, hi):
    return max((sum(k[lo:hi]) for k in a), default=-1)

def det_sparse(matrix):
    n = len(matrix)
    states = {0: ONE}
    for row in matrix:
        nxt = {}
        for mask, value in states.items():
            for j, entry in enumerate(row):
                if mask & (1 << j) or not entry:
                    continue
                sign = -1 if (mask >> (j + 1)).bit_count() % 2 else 1
                newmask = mask | (1 << j)
                nxt[newmask] = add(nxt.get(newmask, {}), mul(value, entry), sign)
        states = nxt
    return states.get((1 << n) - 1, {})

def cycle(order):
    seq = (0,) + order
    pi = [None] * 5
    for a, b in zip(seq, seq[1:] + seq[:1]):
        pi[a] = b
    return tuple(pi)

def inverse_mod(a, p):
    n=len(a)
    a=[[x%p for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(i for i in range(j,n) if a[i][j])
        a[j],a[k]=a[k],a[j]
        inv=pow(a[j][j],-1,p)
        a[j]=[x*inv%p for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                c=a[i][j]
                a[i]=[(x-c*y)%p for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]

def build(pi, tau):
    U = [[{} for _ in range(5)] for _ in range(5)]
    V = [[{} for _ in range(5)] for _ in range(5)]
    for i in range(5):
        U[i][i] = mon(1 + 2 * i)
        U[i][pi[i]] = mon(2 + 2 * i)
    for j in range(5):
        V[j][j] = mon(11 + 2 * j)
        V[tau.index(j)][j] = mon(12 + 2 * j)
    H = []
    for i in range(5):
        row = []
        for j in range(5):
            f = add(mon(t=i*j), mon(0, t=-3*(i+j)**2), -1)
            if i == j:
                f = add(f, mon(0, 3, t=-3*i*i))
            row.append(f)
        H.append(row)
    K = [[{} for _ in range(5)] for _ in range(5)]
    for i, j in product(range(5), repeat=2):
        for a in (i, pi[i]):
            for b in (j, tau.index(j)):
                K[i][j] = add(K[i][j], mul(mul(U[i][a], H[a][b]), V[b][j]))
    def coeff(i,j):
        r = [{} for _ in range(10)]
        r[i] = V[i][j]
        r[5+j] = U[i][j]
        return r
    return U, V, H, K, coeff

def main():
    # Anchor algebra in Q(eta), then four independent finite-field matrix inverses.
    g0=add(ONE,add(mon(t=2,c=2),mon(t=3,c=2)))
    assert reduce_phi(add(mul(g0,g0),mon(c=5),-1))=={}
    assert reduce_phi(add(ONE,{k:5*v for k,v in g0.items()}))
    anchor_entries=0
    for embedding in range(1,5):
        eta=pow(91,embedding,241)
        gg=(1+2*(pow(eta,2,241)+pow(eta,3,241)))%241
        scalar=(1+5*gg)%241
        assert pow(eta,5,241)==1 and eta!=1 and gg*gg%241==5 and scalar
        finv=[[pow(5,-1,241)*pow(eta,(-i*j)%5,241)%241 for j in range(5)] for i in range(5)]
        for j in range(5):
            finv[j][j]=(finv[j][j]+pow(eta,3*j*j,241))%241
        B=inverse_mod(finv,241)
        for i,j in product(range(5),repeat=2):
            H=(pow(eta,i*j,241)-gg*pow(eta,(-3*(i+j)**2)%5,241)+int(i==j)*pow(gg,3,241)*pow(eta,(-3*i*i)%5,241))%241
            assert H==scalar*B[i][j]%241
            anchor_entries+=1
    cycles = [cycle(x) for x in permutations(range(1, 5))]
    assert len(set(cycles)) == 24
    counts = {"cycle_pairs": 0, "target_entry_bounds": 0, "K_entry_bounds": 0,
              "symbolic_nonzero_11_minors": 0, "multidegree_checks": 0,
              "projective_gauge_checks": 0, "chart_degree_checks": 0}
    maxnorm = 0
    selected = None
    for pi, tau in product(cycles, repeat=2):
        U, V, H, K, coeff = build(pi, tau)
        counts["cycle_pairs"] += 1
        for row in H:
            for p in row:
                assert l1(p) <= 3 and degree(p,0,1) <= 3
                counts["target_entry_bounds"] += 1
        for row in K:
            for p in row:
                assert l1(p) <= 12 and degree(p,0,1) <= 3 and degree(p,1,21) <= 2
                counts["K_entry_bounds"] += 1
        rows = [(i,i) for i in range(5)] + [(i,pi[i]) for i in range(5)]
        extra = next((i,j) for i,j in product(range(5),repeat=2) if j not in {i,pi[i],tau[i]})
        a = det_sparse([coeff(i,j) for i,j in rows])
        m = mul(a, K[extra[0]][extra[1]])
        assert reduce_phi(m), (pi,tau)
        counts["symbolic_nonzero_11_minors"] += 1
        allrows = rows + [extra]
        ds = tuple(sum(i==k for i,j in allrows)-1 for k in range(5)) + tuple(sum(j==k for i,j in allrows)-1 for k in range(5))
        assert sum(ds[:5]) == sum(ds[5:]) == 6
        for key in m:
            assert tuple(key[1+2*i]+key[2+2*i] for i in range(10)) == ds
        assert degree(m,0,1) <= 3 and degree(m,1,21) == 12 and l1(m) <= 12*factorial(11)
        counts["multidegree_checks"] += 1
        maxnorm = max(maxnorm,l1(m))
        values = [7] + [2+j for j in range(20)]
        scales = [3+j for j in range(10)]
        scaled = [values[0]]+[values[1+j]*scales[j//2]%241 for j in range(20)]
        factor = 1
        for s,d in zip(scales,ds):
            factor = factor*pow(s,d,241)%241
        assert evalp(m,scaled) == evalp(m,values)*factor%241
        counts["projective_gauge_checks"] += 1
        for chart in [(0,)*10,(1,)*10,tuple(i%2 for i in range(10)),tuple((i+1)%2 for i in range(10))]:
            q=dehom(m,chart)
            assert degree(q,1,21) <= 12 and degree(q,0,1)<=3 and l1(q)<=12*factorial(11)
            counts["chart_degree_checks"] += 1
        if selected is None:
            selected=m

    # Exhaust all chart choices, including coordinates zero in the opposite chart.
    charts=0
    for chart in product((0,1),repeat=10):
        vals=[13]
        for j,chosen in enumerate(chart):
            pair=[0,0]
            pair[chosen]=1
            pair[1-chosen]=0 if j%3==0 else (7+j)
            vals.extend(pair)
        assert evalp(selected,vals)==evalp(dehom(selected,chart),vals)
        charts+=1
    cubed=mul(mul(dehom(selected,(0,)*10),dehom(selected,(0,)*10)),dehom(selected,(0,)*10))
    assert degree(cubed,1,21)<=36 and degree(cubed,0,1)<=9
    assert l1(cubed)<=(12*factorial(11))**3

    # Rectangular rank-minor/Cramer identity with algebraic coefficients.
    # f1=t*g+x+2*x^2; f2=1+t*g*x+2*t*g*x^2.
    tg=mon(0,t=1)
    x=mon(1)
    f1=add(tg,add(x,mon(1,2,c=2)))
    f2=add(ONE,mul(tg,add(x,mon(1,2,c=2))))
    delta=add(mul(tg,tg),ONE,-1)
    assert reduce_phi(add(add(mul(tg,f1),f2,-1),delta,-1))=={}
    nd=norm(delta)
    expected={}
    for e in (0,2,4,6,8):
        expected=add(expected,mon(0,e)) if e else add(expected,ONE)
    assert nd==expected
    assert degree(nd,0,1)==4*degree(delta,0,1)
    assert l1(nd)<=l1(delta)**4

    # Exact coarse cutoff inequalities; no floating-point logarithms or huge factorial.
    D=36**10
    R=comb(D+10,10)
    L=(12*factorial(11))**3
    assert D+10<2**52 and R<2**520 and L<2**87
    assert 607<2**10
    assert 2*(1+4*2**530)<2**534
    result={"status":"PASS","counts":counts,"anchor_embeddings":4,"direct_anchor_inverse_entries":anchor_entries,"all_chart_choices_checked":charts,
            "maximum_observed_minor_representation_l1":maxnorm,
            "cubed_sample_terms":len(cubed),
            "cubed_sample_direction_degree":degree(cubed,1,21),
            "cubed_sample_g_degree":degree(cubed,0,1),
            "rectangular_cramer_identity":"(eta*g)*f1-f2 = eta^2*g^2-1",
            "exact_norm":"1+g^2+g^4+g^6+g^8",
            "D":str(D),"R":str(R),"L":str(L),
            "cutoff":"N0 = 2^(2^534)",
            "limitations":["The accepted N5 certificate is a dependency, not rerun here.",
                            "The enormous Macaulay matrix and its actual minors are not materialized.",
                            "Sample symbolic minors validate the general degree proof; they do not independently establish projective emptiness."]}
    (OUT/"INDEPENDENT_CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
