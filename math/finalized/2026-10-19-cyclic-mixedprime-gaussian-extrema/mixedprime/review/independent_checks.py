"""Fresh reviewer checks. Reads candidate JSON data; imports no candidate code."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product, permutations
from math import gcd
import json, hashlib

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/workspace/shared/sparse_mixedprime_2q_classification_20261019_1002')

def check_integrity():
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest_sha=sha(SOURCE/'MANIFEST.json')
    assert manifest_sha=='e4fbbf3512c5093ae10247c74ba74fd0badb783af2a192945c4d3a3e435f0879'
    assert (SOURCE/'SEAL.sha256').read_text().split()[0]==manifest_sha
    manifest=json.loads((SOURCE/'MANIFEST.json').read_text())
    for row in manifest['files']:
        f=SOURCE/row['path']
        assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256']
    bindings=json.loads((SOURCE/'SOURCE_BINDINGS.json').read_text())
    for row in bindings:
        assert sha(SOURCE/row['copy'])==row['sha256']==sha(Path(row['source']))
    return {'manifest_sha256':manifest_sha,'report_sha256':sha(SOURCE/'REPORT.md'),
            'manifest_files_verified':len(manifest['files']),'original_source_copies_verified':len(bindings)}

def divide(a, b):
    a=list(a); out=[0]*(len(a)-len(b)+1)
    for k in range(len(out)-1,-1,-1):
        out[k]=a[k+len(b)-1]
        for j,c in enumerate(b): a[k+j]-=out[k]*c
    assert not any(a)
    return out

@lru_cache(None)
def phi(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: a=divide(a,phi(d))
    return tuple(a)

class Ring:
    def __init__(self,n):
        self.n=n; self.mod=phi(n); self.k=len(self.mod)-1
        self.zero=(0,)*self.k; self.one=(1,)+(0,)*(self.k-1)
        self.powers=[self.reduce([0]*e+[1]) for e in range(n)]
    def reduce(self,a):
        a=list(a)+[0]*max(0,self.k-len(a))
        for i in range(len(a)-1,self.k-1,-1):
            c=a[i]
            for j,b in enumerate(self.mod): a[i-self.k+j]-=c*b
        return tuple(a[:self.k])
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def neg(self,a): return tuple(-x for x in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def scale(self,a,c): return tuple(x*c for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.k-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y: c[i+j]+=x*y
        return self.reduce(c)
    def conj(self,a):
        r=self.zero
        for i,x in enumerate(a):
            if x:r=self.add(r,self.scale(self.powers[-i%self.n],x))
        return r
    def sum_roots(self,exps):
        a=[0]*self.n
        for e in exps:a[e%self.n]+=1
        return self.reduce(a)

@lru_cache(None)
def ring(n): return Ring(n)

def row_residual(R,r,s):
    n=len(R); F=ring(n)
    return F.sum_roots((r-s)*c for c in range(n) if R[r][c] and R[s][c])

def check_grams(R,d):
    n=len(R); F=ring(n); bad=[]
    assert len(R)==n and all(len(row)==n for row in R)
    assert all(x in (0,1) for row in R for x in row)
    for r in range(n):
        for s in range(n):
            rr=row_residual(R,r,s)
            cc=F.sum_roots((s-r)*j for j in range(n) if R[j][r] and R[j][s])
            want=F.scale(F.one,d) if r==s else F.zero
            if rr!=want:bad.append(('row',r,s,rr))
            if cc!=want:bad.append(('column',r,s,cc))
    return bad

def product_matrix(A,B,F):
    n=len(A)
    return [[sum_vectors((F.mul(A[i][k],B[k][j]) for k in range(n)),F) for j in range(n)] for i in range(n)]

def sum_vectors(items,F):
    r=F.zero
    for a in items:r=F.add(r,a)
    return r

def adjoint(A,F):return [[F.conj(A[j][i]) for j in range(len(A))] for i in range(len(A))]

def check_scalar_identity(A,s,F):
    assert all(A[i][j]==(F.scale(F.one,s) if i==j else F.zero) for i in range(len(A)) for j in range(len(A)))

def census6(d):
    n=6; F=ring(n)
    masks=[sum(1<<c for c in cols) for cols in combinations(range(n),d)]
    legal={}
    for h in range(1,n):
        for a in masks:
            legal[h,a]={b for b in masks if F.sum_roots(h*c for c in range(n) if (a&b)>>c&1)==F.zero}
    counts=0; nodes=0; first=None
    def visit(rows,degrees):
        nonlocal counts,nodes,first
        nodes+=1;r=len(rows)
        if r==n:
            assert degrees==[d]*n
            R=[[m>>c&1 for c in range(n)] for m in rows]
            assert not check_grams(R,d)
            counts+=1
            if first is None:first=rows[:]
            return
        choices=set(masks)
        for s,a in enumerate(rows):choices &= legal[r-s,a]
        for b in sorted(choices):
            nd=[degrees[c]+(b>>c&1) for c in range(n)]
            if any(x>d or x+(n-r-1)<d for x in nd):continue
            visit(rows+[b],nd)
    visit([],[0]*n)
    return {'d':d,'masks':counts,'dfs_nodes':nodes,'first_row_bitmasks':first}

def exhaustive_upper_q3():
    q=3;n=6;tested=0
    for base in product((0,1),repeat=q):
        A=[t+q*base[t] for t in range(q)];B=[t+q*(1-base[t]) for t in range(q)]
        for f in permutations(range(q)):
            for g in permutations(range(q)):
                R=[[0]*n for _ in range(n)]
                for i in range(q):
                    for c in A+[B[f[i]]]:R[2*i][c]=1
                    for c in B+[A[g[i]]]:R[2*i+1][c]=1
                assert all(sum(row)==q+1 for row in R)
                assert all(sum(R[r][c] for r in range(n))==q+1 for c in range(n))
                for r in range(n):
                    for s in range(r):
                        if (r-s)%2==0:assert row_residual(R,r,s)==ring(n).zero
                bad=check_grams(R,q+1)
                assert any(kind=='row' and gcd(r-s,n)==1 for kind,r,s,_ in bad)
                tested+=1
    return tested

def local_fiber_counts(q):
    admissible=[]
    for vs in product(range(4),repeat=q):
        if all((vs[i]&vs[j]).bit_count()==1 for i in range(q) for j in range(i)):
            singleton={v for v in vs if v!=3}
            assert len(singleton)==1 and next(iter(singleton)) in (1,2)
            assert vs.count(3)<=1
            admissible.append(vs)
    return {'q':q,'tested':4**q,'accepted':len(admissible)}

def binary_primitive_sum_census(p,q):
    n=p*q;F=ring(n);accepted=0
    for b in range(1<<n):
        support=[c for c in range(n) if b>>c&1]
        if F.sum_roots(support)!=F.zero:continue
        accepted+=1
        p_lines=all(len({b>>(t+k*q)&1 for k in range(p)})==1 for t in range(q))
        q_lines=all(len({b>>(t+k*p)&1 for k in range(q)})==1 for t in range(p))
        assert p_lines or q_lines
    assert accepted==(1<<p)+(1<<q)-2
    return {'p':p,'q':q,'all_binary_supports_tested':1<<n,'zero_sums':accepted}

def run():
    integrity=check_integrity()
    positives=json.loads((SOURCE/'POSITIVE_MASKS.json').read_text())
    positive_results=[]
    for c in positives:
        assert not check_grams(c['R'],c['d'])
        positive_results.append({k:c[k] for k in ('label','N','d')})
    neg=json.loads((SOURCE/'NEGATIVE_CONTROLS.json').read_text())
    negative_results=[]
    for category in ('q_plus_one_local_countercontrols','general_upper_countercontrols'):
        for c in neg.get(category,[]):
            R=c['R'];n=c['N'];d=c['d'];bad=check_grams(R,d)
            assert bad
            assert all(sum(row)==d for row in R)
            assert all(sum(R[r][col] for r in range(n))==d for col in range(n))
            p=2 if category.startswith('q_plus') else c['p']
            for r in range(n):
                for s in range(r):
                    if (r-s)%p==0:assert row_residual(R,r,s)==ring(n).zero
            assert any(kind=='row' and gcd(r-s,n)==1 for kind,r,s,_ in bad)
            negative_results.append({'category':category,'N':n,'d':d,'gram_failures':len(bad)})
    originals=json.loads((SOURCE/'ORIGINAL_MODEL_CONTROLS.json').read_text())
    original_results=[]
    for c in originals:
        n=c['N'];d=c['d'];F=ring(n)
        assert list(F.mod)==c['field_modulus']
        M=[[tuple(map(Q,e)) for e in row] for row in c['M_tilde']]
        B=[[tuple(map(Q,e)) for e in row] for row in c['B_tilde']]
        E=[[tuple(map(Q,e)) for e in row] for row in c['error_unnormalized']]
        R=next(t['R'] for t in positives if t['N']==n and t['d']==d)
        for i in range(n):
            for j in range(n):
                assert B[i][j]==F.scale(F.powers[-i*j%n],Q(1-R[j][i],n-d))
                assert E[i][j]==F.sub(M[i][j],F.powers[i*j%n])
        assert all(sum(e!=F.zero for e in row)==n-d for row in B)
        assert all(sum(B[i][j]!=F.zero for i in range(n))==n-d for j in range(n))
        check_scalar_identity(product_matrix(M,B,F),1,F)
        check_scalar_identity(product_matrix(B,M,F),1,F)
        check_scalar_identity(product_matrix(E,adjoint(E,F),F),d,F)
        check_scalar_identity(product_matrix(adjoint(E,F),E,F),d,F)
        original_results.append({'N':n,'d':d,'all_original_model_equalities':True})
    F=ring(6)
    weighted=(1,3,2,2,2,3)
    assert F.reduce(weighted)==F.zero
    result={'all_passed':True,'candidate_integrity':integrity,'positive_mask_controls':positive_results,'negative_controls':negative_results,
            'original_model_controls':original_results,'N6_exhaustive_census':[census6(d) for d in range(1,7)],
            'q3_all_upper_structures_rejected':exhaustive_upper_q3(),
            'local_binary_fiber_classification':[local_fiber_counts(q) for q in (3,5,7)],
            'binary_primitive_sum_census':[binary_primitive_sum_census(p,q) for p,q in ((2,3),(2,5),(3,5))],
            'weighted_order6_coefficient_cancellation_verified':True,
            'historical_or_candidate_code_executed':False,'external_state_changed':False}
    assert integrity==check_integrity()
    (ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
