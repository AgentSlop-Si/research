"""Focused independent review checks; no full duplicate audit.

The matrix arithmetic and operation probe are implemented independently of
exact_fields.py, Counted, dense_parts, generator_matrix, and cut_ranks.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
from sandwich import Sandwich, prepare


P = 101


class Probe:
    zero, one = 0, 1
    def __init__(self):
        self.counts = dict(add=0, sub=0, mul=0, inv=0)
    def add(self,a,b):
        self.counts['add'] += 1
        return (a+b)%P
    def sub(self,a,b):
        self.counts['sub'] += 1
        return (a-b)%P
    def mul(self,a,b):
        self.counts['mul'] += 1
        return a*b%P
    def inv(self,a):
        self.counts['inv'] += 1
        return pow(a,-1,P)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*b)] for row in a]


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        v = pow(a[r][j],-1,P)
        a[r] = [x*v%P for x in a[r]]
        for i in range(r+1,len(a)):
            v = a[i][j]
            a[i] = [(x-v*y)%P for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def inv(a):
    n = len(a)
    b = [row[:]+eye(n)[i] for i,row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if b[i][j]),None)
        if pivot is None:
            raise ValueError('singular')
        b[j],b[pivot] = b[pivot],b[j]
        v = pow(b[j][j],-1,P)
        b[j] = [x*v%P for x in b[j]]
        for i in range(n):
            if i != j:
                v = b[i][j]
                b[i] = [(x-v*y)%P for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]


def parts(plan):
    n = len(plan.diagonal)
    l,r,t = eye(n),eye(n),[[0]*n for _ in range(n)]
    for i in range(n):
        t[i][i] = plan.diagonal[i]
        if i:
            l[i][i-1] = -plan.alpha[i]%P
            t[i][i-1] = plan.lower[i]
        if i+1<n:
            r[i][i+1] = -plan.beta[i+1]%P
            t[i][i+1] = plan.upper[i]
    return l,t,r


def check_generators():
    count = 0
    # Includes zero off-diagonal generators, zero diagonal, singular A, and
    # exact cancellation in T. Nonzero p/v is the actual preparation contract.
    for n in (2,3,5):
        p = [i+1 for i in range(n)]
        v = [2*i+3 for i in range(n)]
        for mode in range(5):
            q = [0 if mode in (0,3) else (i+mode)%P for i in range(n)]
            u = [0 if mode in (1,3) else (2*i+mode)%P for i in range(n)]
            d = [0 if mode in (2,3) else (3*i+mode)%P for i in range(n)]
            probe = Probe()
            plan = prepare(probe,p,q,u,v,d)
            assert sum(probe.counts.values()) == 17*n-19
            a = [[d[i] if i==j else p[i]*q[j]%P if i>j else u[i]*v[j]%P
                  for j in range(n)] for i in range(n)]
            l,t,r = parts(plan)
            assert mm(mm(l,a),r) == t
            for x in ([0]*n, list(range(n)), [1]*n):
                probe = Probe()
                out = plan.apply(probe,x)
                assert out == [sum(ai*xj for ai,xj in zip(row,x))%P for row in a]
                assert sum(probe.counts.values()) == 9*n-8
            count += 1
    return count


def check_zero_transition_converse():
    count = 0
    for values in product((0,1),repeat=6):
        alpha = [0]+list(values[:3])
        beta = [0]+list(values[3:])
        plan = Sandwich(alpha,beta,[0,2,3,5],[0,7,0,11],[13,0,17,0])
        l,t,r = parts(plan)
        a = mm(mm(inv(l),t),inv(r))
        for s in range(1,4):
            assert rank([row[s:] for row in a[:s]]) <= 1
            assert rank([row[:s] for row in a[s:]]) <= 1
        count += 1
    return count


def check_sharp_support():
    cases = []
    for b in range(1,5):
        n = 2*b+1
        lower,upper = [0]*n,[0]*n
        for i in range(1,n):
            if i not in (1,b+1):
                lower[i] = 1
                upper[i-1] = 1
        plan = Sandwich([0]+[2]*(n-1),[0]+[3]*(n-1),lower,[4]*n,upper)
        l,t,r = parts(plan)
        ai = mm(mm(r,inv(t)),l)
        supports = [sum(bool(x) for x in row) for row in ai]
        assert max(supports) == 2*b+1
        assert plan.blocks(0) == [(0,1),(1,b+1),(b+1,n)] or b == 1
        cases.append({'b':b,'N':n,'maximum_inverse_row_support':max(supports),
                      'contiguous_blocks':plan.blocks(0)})
    return cases


def check_movement():
    count = 0
    for n in (3,4,8,16):
        permutations = [list(range(n)),list(reversed(range(n))),
                        [(i+1)%n for i in range(n)]]
        for perm in permutations:
            pm = [[int(perm[i]==j) for j in range(n)] for i in range(n)]
            crossings = [sum(perm[i]>=s for i in range(s)) for s in range(1,n)]
            assert 2*sum(crossings) == sum(abs(i-j) for i,j in enumerate(perm))
            for s,c in enumerate(crossings,1):
                assert rank([row[s:] for row in pm[:s]]) == c
            count += 1
    return count


def main():
    directory = Path(__file__).parent
    result = {'status':'PASS','generator_edge_cases':check_generators(),
              'zero_transition_converse_cases':check_zero_transition_converse(),
              'support_bound_sharpness_cases':check_sharp_support(),
              'permutation_edge_cases':check_movement(),
              'source_sha256':{name:hashlib.sha256((directory/name).read_bytes()).hexdigest()
                               for name in ('README.md','sandwich.py','exact_fields.py',
                                            'run_audit.py','review_edge_checks.py')}}
    (directory/'review_edge_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
