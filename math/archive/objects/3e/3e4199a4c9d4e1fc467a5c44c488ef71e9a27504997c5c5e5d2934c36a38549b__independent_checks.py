"""Independent exact audit; references use direct sums and Gaussian elimination."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
import random

from affine_cycle import try_affine_fourier, affine_fft_or_fallback, solve_cycle, Counted
from exact_fields import PrimeField, CyclotomicField


class Trace:
    def __init__(self, field):
        self.field = field
        self.calls = Counter()

    def __getattr__(self, name):
        operation = getattr(self.field, name)
        if name not in ('add', 'sub', 'mul', 'inv'):
            return operation
        def traced(*args):
            self.calls['inverse' if name == 'inv' else name] += 1
            return operation(*args)
        return traced


def direct(field, x, q):
    out = []
    for k in range(len(x)):
        value = field.zero
        for j, xj in enumerate(x):
            value = field.add(value, field.mul(xj, field.power(q, j*k)))
        out.append(value)
    return out


def gauss(field, matrix, rhs):
    n = len(rhs)
    rows = [list(row)+[value] for row, value in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if rows[i][j] != field.zero), None)
        if pivot is None:
            return None
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = field.inv(rows[j][j])
        rows[j] = [field.mul(value, scale) for value in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [field.sub(a, field.mul(scale,b)) for a,b in zip(rows[i],rows[j])]
    return [row[-1] for row in rows]


def source_matrix(field,n,q,lam,a,b,shift):
    matrix = [[field.one if i==j else field.zero for j in range(n)] for i in range(n)]
    for i in range(n):
        j = (a*i+shift)%n
        matrix[i][j] = field.sub(matrix[i][j], field.mul(lam, field.power(q,(b*i)%n)))
    return matrix


def inspect(field,x,q,**kwargs):
    trace = Trace(field)
    y, meta = try_affine_fourier(trace,x,q,**kwargs)
    assert dict(trace.calls) == meta['field_operations']
    assert sum((Counter(v) for v in meta['stages'].values()),Counter()) == trace.calls
    if y is not None:
        assert y == direct(field,x,q)
    return y,meta


def main():
    result = {'status':'PASS', 'exhaustive_checks':0, 'exhaustive_accepts':0,
              'crossfield_gaussian_checks':0, 'singular_declines':0,
              'fallback_checks':0, 'arbitrary_cycle_checks':0,
              'inverse_root_checks':0, 'discovery_cost_checks':0}
    field = PrimeField(5)
    for q in (2,3):
        for x in product(range(5),repeat=4):
            for cap in (0,1,2):
                y,meta = inspect(field,list(x),q,max_defects=cap)
                result['exhaustive_checks'] += 1
                result['exhaustive_accepts'] += y is not None

    # Every source input here is generated independently by dense elimination.
    configurations = [(PrimeField(p),n) for p in (17,41,97) for n in (4,8)]
    configurations += [(CyclotomicField(n),n) for n in (4,8)]
    for field,n in configurations:
        canonical = field.root(n)
        for exponent in (1,n-1):
            q = field.power(canonical,exponent)
            for a,b,shift in ((-7,-3,5),(1,1,-1),(5,3,1)):
                for scalar in (0,1,2):
                    lam = field.integer(scalar)
                    rhs = [field.zero]*n
                    rhs[n-1] = field.integer(3)
                    x = gauss(field, source_matrix(field,n,q,lam,a,b,shift), rhs)
                    if x is None:
                        continue
                    y,meta = inspect(field,x,q,max_defects=1,a=a,b=b,shift=shift,supplied_lambda=lam)
                    assert y is not None
                    assert sum(meta['field_operations'].values()) <= 12*n+3
                    result['crossfield_gaussian_checks'] += 1
                    result['inverse_root_checks'] += exponent != 1
                    yd,md = inspect(field,x,q,max_defects=1,a=a,b=b,shift=shift)
                    if sum(v!=field.zero for v in x)>2:
                        assert yd is not None
                        assert sum(md['field_operations'].values()) <= 14*n+3
                        result['discovery_cost_checks'] += 1

    # Deliberately compatible/singular cases and worst supported defect budgets.
    rng = random.Random(298401)
    field = PrimeField(17)
    for n in (4,8):
        q = field.root(n)
        singular_lambdas = [v for v in range(17) if pow(v,n,17)==16]
        for lam in singular_lambdas:
            for _ in range(3):
                x = [rng.randrange(17) for _ in range(n)]
                y,meta = inspect(field,x,q,supplied_lambda=lam,max_defects=n)
                assert y is None and meta['reason']=='singular_target_cycle'
                result['singular_declines'] += 1
                trace=Trace(field)
                z,hybrid=affine_fft_or_fallback(trace,x,q,supplied_lambda=lam,max_defects=n)
                assert z==direct(field,x,q)
                assert dict(trace.calls)==hybrid['field_operations']
                assert hybrid['ordinary_fft_calls']==1
                result['fallback_checks'] += 1

    # Cycle solver is checked without Fourier structure, including zero edges.
    field=PrimeField(97)
    for n in (4,5,8):
        for _ in range(30):
            order=list(range(n)); rng.shuffle(order)
            permutation=[0]*n
            for j,index in enumerate(order): permutation[index]=order[(j+1)%n]
            coefficients=[rng.randrange(4) for _ in range(n)]
            rhs=[rng.randrange(97) for _ in range(n)]
            matrix=[[int(i==j) for j in range(n)] for i in range(n)]
            for i in range(n): matrix[i][permutation[i]]=(matrix[i][permutation[i]]-coefficients[i])%97
            counted=Counted(field)
            actual=solve_cycle(counted,permutation,coefficients,rhs)
            assert actual==gauss(field,matrix,rhs)
            expected=n+1 if actual is None else 5*n+3
            assert sum(counted.count.values())==expected
            result['arbitrary_cycle_checks'] += 1

    # Exact equality 14N+1 applies to the author's dense one-defect-at-zero family.
    field=PrimeField(97)
    for n in (4,8,16,32):
        q=field.root(n)
        lam=next(v for v in range(2,97) if pow(v,n,97)!=96)
        rhs=[field.one]+[field.zero]*(n-1)
        x=gauss(field,source_matrix(field,n,q,lam,5,1,1),rhs)
        assert all(v!=field.zero for v in x)
        y,meta=inspect(field,x,q)
        assert y is not None
        assert sum(meta['field_operations'].values())==14*n+1
        result['discovery_cost_checks'] += 1

    result['source_sha256']=hashlib.sha256(Path('affine_cycle.py').read_bytes()).hexdigest()
    result['author_audit_sha256']=hashlib.sha256(Path('run_audit.py').read_bytes()).hexdigest()
    Path('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
