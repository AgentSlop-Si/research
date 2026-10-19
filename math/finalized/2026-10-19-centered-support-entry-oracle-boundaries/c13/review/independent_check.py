"""Reviewer-authored exact controls; imports only the sealed current adapter.

Independent dense arithmetic, Gaussian elimination, scale enumeration, and
explicit route reconstruction. The inherited iff theorem is a dependency.
"""
import hashlib
import importlib.util
import itertools
import json
import argparse
import random
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--candidate',type=Path,default=HERE.parent/'c13_entry_oracle_integration_20261019_1525')
parser.add_argument('--adapter-only',action='store_true',help='Verify the frozen adapter hash and run mathematical controls without requiring administrative source snapshots.')
args=parser.parse_args()
SOURCE = args.candidate.resolve()
assert hashlib.sha256((SOURCE/'adapter.py').read_bytes()).hexdigest()=='270014d4cd25dcd64b80f4a8af64549f504dbce42063f2cfa873688f24253567'
spec = importlib.util.spec_from_file_location('adapter_under_review', SOURCE / 'adapter.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def val(a, p):
    return Q(a) if p is None else int(a) % p


def div(a, b, p):
    return a / b if p is None else a * pow(b, -1, p) % p


def red(a, p):
    return a if p is None else a % p


def eye(n, p=None):
    return [[val(i == j, p) for j in range(n)] for i in range(n)]


def mm(a, b, p=None):
    return [[red(sum(a[i][k] * b[k][j] for k in range(len(b))), p)
             for j in range(len(b[0]))] for i in range(len(a))]


def plus(a, b, p=None):
    return [[red(x+y, p) for x, y in zip(ar, br)] for ar, br in zip(a,b)]


def rref(a, p=None):
    a = [list(row) for row in a]
    r, pivots = 0, []
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        t = a[r][c]
        a[r] = [div(x, t, p) for x in a[r]]
        for i in range(len(a)):
            if i == r:
                continue
            t = a[i][c]
            a[i] = [red(x-t*y, p) for x,y in zip(a[i],a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def inverse(a, p=None):
    n = len(a)
    z, piv = rref([row + ir for row,ir in zip(a,eye(n,p))], p)
    if piv[:n] != list(range(n)):
        raise ValueError('singular')
    return [row[n:] for row in z]


def determinant(a, p=None):
    a, result = [list(row) for row in a], val(1,p)
    for c in range(len(a)):
        r = next((i for i in range(c,len(a)) if a[i][c]),None)
        if r is None:
            return val(0,p)
        if r != c:
            a[r],a[c] = a[c],a[r]
            result = -result
        result = red(result*a[c][c],p)
        for i in range(c+1,len(a)):
            t = div(a[i][c],a[c][c],p)
            a[i] = [red(x-t*y,p) for x,y in zip(a[i],a[c])]
    return red(result,p)


def matrices(d,p=None):
    n=len(d['a'])
    u=[[val(0,p) for _ in range(n)] for _ in range(n)]
    v=[[val(0,p) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k,c in ((d['r0'][i],d['a'][i]),(d['r1'][i],d['b'][i])):
            u[i][k]=red(u[i][k]+c,p)
        for k,c in ((d['s0'][i],d['d'][d['s0'][i]]),(d['s1'][i],d['e'][d['s1'][i]])):
            v[i][k]=red(v[i][k]+c,p)
    return u,v


def canonical(n,b=-2,e=-3):
    return dict(r0=list(range(n)),r1=[(i+1)%n for i in range(n)],
                s0=list(range(n)),s1=[(i+1)%n for i in range(n)],
                a=[1]*n,b=[b]*n,d=[1]*n,e=[e]*n)


def reconstruct(answer,p):
    plans=answer['plans']; n=len(answer['x'])
    den0,den1=eye(n,p),eye(n,p)
    for i in range(n):
        den0[i][plans['tau0'][i]]=red(den0[i][plans['tau0'][i]]-plans['w0'][i],p)
        den1[i][plans['tau1'][i]]=red(den1[i][plans['tau1'][i]]-plans['w1'][i],p)
    g0,g1=inverse(den0,p),inverse(den1,p)
    t0=[[red(g0[plans['r0_inverse'][i]][j]*plans['right_scale0'][j],p)
         for j in range(n)] for i in range(n)]
    # Right multiplication by P_(s0^-1): column j is old column s0(j).
    s0=[None]*n
    for i,j in enumerate(plans['s0_inverse']): s0[j]=i
    t1=[[red(plans['left_scale1'][i]*g1[i][s0[j]],p)
         for j in range(n)] for i in range(n)]
    return plus(t0,t1,p)


def enumerate_scale_images(u,v,p):
    n=len(u)
    return {tuple((u[i][j]*z[n+j]+z[i]*v[i][j])%p
                  for i in range(n) for j in range(n))
            for z in itertools.product(range(1,p),repeat=2*n)}


def fresh_data(n,p,rng):
    for _ in range(10000):
        r0,s0,cyc0,cyc1=(rng.sample(range(n),n) for _ in range(4))
        t0,t1=[None]*n,[None]*n
        for cyc,t in ((cyc0,t0),(cyc1,t1)):
            for i in range(n):t[cyc[i]]=cyc[(i+1)%n]
        d=dict(r0=r0,r1=[r0[t0[i]] for i in range(n)],
               s0=s0,s1=[t1[s0[i]] for i in range(n)],
               a=[rng.randrange(1,p) for _ in range(n)],
               b=[rng.randrange(p) for _ in range(n)],
               d=[rng.randrange(1,p) for _ in range(n)],
               e=[rng.randrange(p) for _ in range(n)])
        u,v=matrices(d,p)
        if determinant(u,p) and determinant(v,p):return d,u,v
    raise AssertionError('No legal directions generated')


def main():
    verified_files=0
    if not args.adapter_only:
        manifest=SOURCE/'MANIFEST.json'
        expected='4a482ce24330b5083b7aab921ab0ee1516aa940addffc3b80ee5f62e44ce750b'
        assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
        sealed=json.loads(manifest.read_text())
        for rec in sealed['files']:
            blob=(SOURCE/rec['path']).read_bytes()
            assert len(blob)==rec['bytes']
            assert hashlib.sha256(blob).hexdigest()==rec['sha256']
        verified_files=len(sealed['files'])
    records={'sealed_files_verified':verified_files, 'status':'PASS',
             'seal_check_skipped':args.adapter_only,
             'adapter_sha256':'270014d4cd25dcd64b80f4a8af64549f504dbce42063f2cfa873688f24253567'}
    rng=random.Random(202610191539)

    # Independent exhaustive classification of all N=2 target matrices, then
    # fresh N=3 target samples. The reference enumerates scale assignments.
    decisions=positives=0
    for p in (2,3,5):
        for n in (2,3):
            for trial in range(5):
                d,u,v=fresh_data(n,p,rng)
                images=enumerate_scale_images(u,v,p)
                ui,vi=inverse(u,p),inverse(v,p)
                if n==2:
                    targets=itertools.product(range(p),repeat=n*n)
                else:
                    targets=[tuple(rng.randrange(p) for _ in range(n*n)) for _ in range(80)]
                    # Every allowed sandwich image is itself a feasible test.
                    targets += [tuple(t for row in mm(mm(ui,[list(k[i*n:(i+1)*n]) for i in range(n)],p),vi,p) for t in row)
                                for k in sorted(images)]
                for flat in targets:
                    b=[list(flat[i*n:(i+1)*n]) for i in range(n)]
                    k=tuple(t for row in mm(mm(u,b,p),v,p) for t in row)
                    result=adapter.complete(d,lambda i,j:b[i][j],adapter.Field(p))
                    assert result['ok']==(k in images),(p,n,d,b,result)
                    if result['ok']:
                        assert reconstruct(result,p)==b
                        assert result['target_queries']<=4*n*n
                        assert result['sandwich_field_operations']<=12*n*n
                        assert not result['target_invertibility_checked']
                        positives+=1
                    decisions+=1
    records.update(exact_completion_classifications=decisions,
                   accepted_reconstructions=positives,
                   exhaustive_target_dimensions=[2],finite_fields=[2,3,5])

    # All coordinate perturbations, not just the submitted matching subset.
    witness_rows=[]; alternatives=0
    for n in (3,4,5,6,7,8,11):
        d=canonical(n);u,v=matrices(d)
        b0=plus(inverse(u),inverse(v)); b0i=inverse(b0)
        assert determinant(u)==1-2**n
        assert determinant(v)==1-3**n
        assert determinant(b0)==Q(2**n-5**n,(1-2**n)*(1-3**n))
        base=adapter.complete(d,lambda i,j:b0[i][j],adapter.Field())
        assert base['ok'] and reconstruct(base,None)==b0
        for a in range(n):
            for b in range(n):
                delta=Q(1 if 1+b0i[b][a] else 2)
                pert=[row[:] for row in b0]; pert[a][b]+=delta
                assert determinant(pert)
                # An explicit off-support witness for every input coordinate.
                i,j=(a,b) if b not in (a,(a+1)%n) else (((a-1)%n,(a+1)%n) if b==a else (a,(a+2)%n))
                assert not u[i][j] and not v[i][j]
                assert u[i][a]*v[b][j]*delta
                out=adapter.complete(d,lambda i,j:pert[i][j],adapter.Field())
                assert not out['ok'] and out['reason']=='off_support_residual'
                alternatives+=1
        # Rank of the 2N-dimensional linear completion image.
        ui,vi=inverse(u),inverse(v)
        columns=[[ui[i][j]*int(j==s) for i in range(n) for j in range(n)] for s in range(n)]
        columns += [[int(i==s)*vi[i][j] for i in range(n) for j in range(n)] for s in range(n)]
        rank=len(rref([list(row) for row in zip(*columns)])[1])
        assert rank==2*n
        witness_rows.append(dict(n=n,completion_linear_image_rank=rank,
                                 invertible_coordinate_alternatives=n*n,
                                 target_determinant=str(determinant(b0))))
    records.update(all_coordinate_Q_witnesses=witness_rows,total_all_coordinate_alternatives=alternatives)

    # Independently exercise the supplied matching argument over small odd
    # prime fields, choosing delta inside the original field, never an extension.
    generic_cases=generic_alternatives=0
    for p in (3,5,7,11):
        for n in (4,5):
            for trial in range(8):
                d,u,v=fresh_data(n,p,rng)
                ui,vi=inverse(u,p),inverse(v,p)
                for _ in range(2000):
                    x,y=([rng.randrange(1,p) for _ in range(n)] for _ in range(2))
                    b0=[[(ui[i][j]*x[j]+y[i]*vi[i][j])%p for j in range(n)] for i in range(n)]
                    if determinant(b0,p):break
                else:raise AssertionError('No invertible feasible target generated')
                b0i=inverse(b0,p)
                assert adapter.complete(d,lambda i,j:b0[i][j],adapter.Field(p))['ok']
                r0i=[None]*n
                for i,j in enumerate(d['r0']):r0i[j]=i
                support={(i,j) for i in range(n) for j in range(n) if u[i][j] or v[i][j]}
                selected=[(a,b) for a in range(n) for b in range(n)
                          if (r0i[a],d['s0'][b]) not in support]
                assert len(selected)==n*n-len(support)
                for a,b in selected:
                    delta=next(t for t in range(1,p) if (1+t*b0i[b][a])%p)
                    alt=[row[:] for row in b0];alt[a][b]=(alt[a][b]+delta)%p
                    assert determinant(alt,p)
                    out=adapter.complete(d,lambda i,j:alt[i][j],adapter.Field(p))
                    assert not out['ok'] and out['reason']=='off_support_residual'
                    generic_alternatives+=1
                generic_cases+=1
    records.update(odd_prime_matching_cases=generic_cases,
                   odd_prime_invertible_rejecting_alternatives=generic_alternatives,
                   matching_control_fields=[3,5,7,11])

    # The >2 condition is sufficient; its rank-one-preservation proof step
    # cannot be used uniformly over F2. This
    # legal fixed-direction F2 example has an invertible feasible target and
    # an off-support forbidden coordinate whose sole nonzero change is singular.
    f2_control=None
    for _ in range(2000):
        d,u,v=fresh_data(3,2,rng)
        b0=plus(inverse(u,2),inverse(v,2),2)
        if not determinant(b0,2):continue
        for a in range(3):
            for b in range(3):
                pert=[row[:] for row in b0];pert[a][b]^=1
                k=mm(mm(u,pert,2),v,2)
                violates=any(k[i][j] and not u[i][j] and not v[i][j]
                             for i in range(3) for j in range(3))
                if violates and not determinant(pert,2):
                    f2_control=dict(data=d,feasible_invertible_B=b0,coordinate=[a,b],
                                    sole_nonzero_delta=1,perturbed_determinant=0)
                    break
            if f2_control:break
        if f2_control:break
    assert f2_control
    d=f2_control['data'];b0=f2_control['feasible_invertible_B']
    assert adapter.complete(d,lambda i,j:b0[i][j],adapter.Field(2))['ok']
    records['F2_rank_one_exception']=f2_control
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
