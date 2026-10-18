#!/usr/bin/env python3
"""Independent review controls. Python 3 + SymPy; all arithmetic is exact.

Does not import or execute the candidate's checker or any historical checker.
Polynomial coefficient tuples with rational entries represent Q[z]/Phi_N(z).
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
import hashlib, json, math
import sympy as sp

BASE = Path(__file__).resolve().parent
CANDIDATE = Path(__file__).resolve().parent.parent/'candidate'
EXPECTED_REPORT = '1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee'
x = sp.Symbol('x')

def digest(data): return hashlib.sha256(data).hexdigest()

def check_inputs():
    raw = (CANDIDATE/'MANIFEST.json').read_bytes()
    manifest = json.loads(raw)
    verified = []
    for item in manifest['files']:
        data = (CANDIDATE/item['path']).read_bytes()
        assert len(data) == item['bytes'] and digest(data) == item['sha256'], item['path']
        verified.append(item['path'])
    report = digest((CANDIDATE/'REPORT.md').read_bytes())
    assert report == EXPECTED_REPORT
    seal = json.loads((CANDIDATE/'SEAL.json').read_text())
    assert seal['manifest_sha256'] == digest(raw)
    assert seal['report_sha256'] == report
    assert seal['checker_sha256'] == digest((CANDIDATE/'verify_exact.py').read_bytes())
    bindings = json.loads((CANDIDATE/'SOURCE_BINDINGS.json').read_text())
    for item in bindings['copied_sources']:
        original, copied = (CANDIDATE/item['source']).read_bytes(), (CANDIDATE/item['copy']).read_bytes()
        assert original == copied and digest(copied) == item['sha256'] and len(copied) == item['bytes']
    phase = (CANDIDATE/'sources/PHASE20_AUDIT.md').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(phase)).encode()+b'\0'+phase).hexdigest()
    assert blob == '28212b19e78502ce5acf52a90570d42b0285d3d0'
    return {'report_sha256': report, 'manifest_sha256': digest(raw),
            'verified_manifest_members': verified, 'source_copies_match_originals': len(bindings['copied_sources']),
            'phase20_git_blob_sha1': blob}

class Ring:
    def __init__(self,n):
        self.n=n
        p=sp.Poly(sp.cyclotomic_poly(n,x),x,domain=sp.QQ)
        self.modulus=p
        self.k=p.degree()
        self.phi=tuple(Q(int(p.nth(j).p),int(p.nth(j).q)) for j in range(self.k))
        self.zero=(Q(0),)*self.k
        self.one=(Q(1),)+(Q(0),)*(self.k-1)
        self.roots=tuple(self.reduce([Q(0)]*j+[Q(1)]) for j in range(n))
    def reduce(self,a):
        a=list(a)+[Q(0)]*max(0,self.k-len(a))
        for j in range(len(a)-1,self.k-1,-1):
            if a[j]:
                c=a[j]
                for k,v in enumerate(self.phi): a[j-self.k+k]-=c*v
        return tuple(a[:self.k])
    def add(self,a,b): return tuple(c+d for c,d in zip(a,b))
    def neg(self,a): return tuple(-v for v in a)
    def sub(self,a,b): return tuple(c-d for c,d in zip(a,b))
    def scale(self,a,c): return tuple(v*c for v in a)
    def mul(self,a,b):
        out=[Q(0)]*(2*self.k-1)
        for i,v in enumerate(a):
            if v:
                for j,w in enumerate(b):
                    if w: out[i+j]+=v*w
        return self.reduce(out)
    @lru_cache(None)
    def inv(self,a):
        assert a != self.zero
        p=sp.Poly(sum(sp.Rational(v.numerator,v.denominator)*x**j for j,v in enumerate(a)),x,domain=sp.QQ)
        r=sp.invert(p,self.modulus)
        return tuple(Q(int(r.nth(j).p),int(r.nth(j).q)) for j in range(self.k))
    @lru_cache(None)
    def star(self,a):
        out=self.zero
        for j,v in enumerate(a):
            if v: out=self.add(out,self.scale(self.roots[-j % self.n],v))
        return out
    def rootsum(self,exponents):
        out=[0]*self.k
        for e in exponents:
            for j,v in enumerate(self.roots[e % self.n]): out[j]+=v
        return tuple(out)

@lru_cache(None)
def ring(n): return Ring(n)

def mask(n,d):
    if not (n>=2 and 1<=d<n and n%d==0): raise ValueError('proper divisor required')
    m=n//d
    return tuple(tuple((r//d)==(c%m) for c in range(n)) for r in range(n))

def gram_certificate(n,pattern,d):
    R=ring(n)
    for columns in [True,False]:
        for i in range(n):
            for j in range(n):
                exponents=[]
                for t in range(n):
                    if columns and pattern[t][i] and pattern[t][j]: exponents.append(t*(j-i))
                    if not columns and pattern[i][t] and pattern[j][t]: exponents.append(t*(i-j))
                if R.rootsum(exponents) != R.scale(R.one,d if i==j else 0): return False
    return True

def all_divisors():
    cases=[]
    for n in list(range(2,43))+[48,54,60,66,72]:
        for d in range(1,n):
            if n%d: continue
            p=mask(n,d)
            assert all(sum(row)==d for row in p)
            assert all(sum(p[r][c] for r in range(n))==d for c in range(n))
            assert gram_certificate(n,p,d),(n,d)
            cases.append({'N':n,'omitted_weight':d,'both_exact_Gram_orders':True,'row_and_column_weights':d})
    return cases

def adj(A,R): return [[R.star(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def matmul(A,B,R):
    C=[[R.zero for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for t in range(len(B)):
            if A[i][t]!=R.zero:
                for j in range(len(B[0])):
                    if B[t][j]!=R.zero: C[i][j]=R.add(C[i][j],R.mul(A[i][t],B[t][j]))
    return C

def scalar_identity(A,c,R):
    return all(A[i][j]==R.scale(R.one,c if i==j else 0) for i in range(len(A)) for j in range(len(A)))

def inverse(A,R):
    n=len(A)
    V=[list(row)+[R.one if i==j else R.zero for j in range(n)] for i,row in enumerate(A)]
    for c in range(n):
        pivot=next((j for j in range(c,n) if V[j][c]!=R.zero),None)
        if pivot is None: raise ValueError('singular')
        V[c],V[pivot]=V[pivot],V[c]
        a=R.inv(V[c][c]); V[c]=[R.mul(v,a) for v in V[c]]
        for i in range(n):
            if i!=c and V[i][c]!=R.zero:
                a=V[i][c]; V[i]=[R.sub(v,R.mul(a,w)) for v,w in zip(V[i],V[c])]
    return [row[n:] for row in V]

def witness(n,d,p,label):
    R=ring(n); s=n-d
    W=[[R.roots[(r*c)%n] for c in range(n)] for r in range(n)]
    H=[[R.zero if p[r][c] else W[r][c] for c in range(n)] for r in range(n)]
    # Z=sqrt(N) M; K=M^-1/sqrt(N). Thus Z K=K Z=I.
    K=[[R.scale(v,Q(1,s)) for v in row] for row in adj(H,R)]
    Z=inverse(K,R)
    E=[[R.sub(Z[i][j],W[i][j]) for j in range(n)] for i in range(n)]
    checks={
        'left_inverse':scalar_identity(matmul(Z,K,R),1,R),
        'right_inverse':scalar_identity(matmul(K,Z,R),1,R),
        'left_error_Gram_dI':scalar_identity(matmul(E,adj(E,R),R),d,R),
        'right_error_Gram_dI':scalar_identity(matmul(adj(E,R),E,R),d,R),
        'inverse_row_support_s':all(sum(v!=R.zero for v in row)==s for row in K),
        'inverse_column_support_s':all(sum(K[i][j]!=R.zero for i in range(n))==s for j in range(n))}
    BF=matmul(K,W,R)
    checks['all_BF_diagonal_entries_one']=all(BF[i][i]==R.one for i in range(n))
    KK=matmul(K,adj(K,R),R)
    checks['all_inverse_row_squared_norms_N_over_s']=all(KK[i][i]==R.scale(R.one,Q(1,s)) for i in range(n))
    assert all(checks.values()),(n,d,label,checks)
    result={'N':n,'d':d,'mask':label,'checks':checks}
    if (n,d,label)==(3,1,'divisor'):
        Hinv=inverse(H,R)
        counts=[sum(v!=R.zero for v in row) for row in Hinv]
        assert counts==[3]*3
        Ewrong=[[R.sub(R.scale(Z[i][j],2),W[i][j]) for j in range(n)] for i in range(n)]
        assert not scalar_identity(matmul(Ewrong,adj(Ewrong,R),R),d,R)
        result['negative_controls']={'naive_M_equals_A_inverse_support':counts,'wrong_gain_rejected':True}
    return result

def witnesses():
    cases=[]
    for n in range(2,11):
        for d in range(1,n):
            if n%d==0: cases.append(witness(n,d,mask(n,d),'divisor'))
    for n,perm in [(3,[1,2,0]),(5,[4,3,2,1,0]),(7,[2,5,1,6,3,0,4])]:
        p=[[r==perm[c] for c in range(n)] for r in range(n)]
        cases.append(witness(n,1,p,'permutation:'+','.join(map(str,perm))))
    return cases

def exhaustive():
    cases=[]
    for n in range(2,6):
        R=ring(n)
        for w in range(1,n):
            supports=[sum(1<<j for j in S) for S in combinations(range(n),w)]
            # Compatibility checks actual column cross-Grams, with no row-count prefilter.
            compatible={}
            for j in range(n):
                for k in range(j):
                    for a in supports:
                        for b in supports:
                            overlap=a&b
                            compatible[j,k,a,b]=(R.rootsum(r*(j-k) for r in range(n) if overlap>>r&1)==R.zero)
            visited=accepted=0
            for columns in product(supports,repeat=n):
                visited+=1
                if not all(compatible[j,k,columns[j],columns[k]] for j in range(n) for k in range(j)): continue
                accepted+=1
                assert all(sum(col>>r&1 for col in columns)==w for r in range(n))
            expected=math.factorial(n) if w==1 else 8 if (n,w)==(4,2) else 0
            assert accepted==expected,(n,w,accepted)
            cases.append({'N':n,'weight':w,'all_column_weight_masks_checked':visited,'accepted':accepted,
                          'row_regularity_derived_for_all_passes':True})
    return cases

def obstruction_controls():
    prime_cases=[]
    for p in [2,3,5,7,11,13,17]:
        R=ring(p); zero=R.zero; total=0
        sums={0:zero}
        for bitmask in range(1,2**p-1):
            bit=bitmask&-bitmask; index=bit.bit_length()-1
            sums[bitmask]=R.add(sums[bitmask^bit],R.roots[index])
            assert sums[bitmask]!=zero,(p,bitmask)
            total+=1
        prime_cases.append({'p':p,'nonempty_proper_subsets':total,'vanishing':0})
    odd_cases=[]
    for n in range(3,76,2):
        R=ring(n); checked=0
        for a,b in combinations(range(n),2):
            assert R.add(R.roots[a],R.roots[b])!=R.zero
            checked+=1
        odd_cases.append({'N':n,'distinct_root_pairs':checked,'vanishing':0})
    return {'prime_subsets':prime_cases,'odd_pairs':odd_cases}

def negative_controls():
    invalid=[(0,1),(1,1),(2,0),(2,2),(5,2),(9,6)]
    for n,d in invalid:
        try: mask(n,d)
        except ValueError: pass
        else: raise AssertionError((n,d))
    p=[[r==0 for c in range(5)] for r in range(5)]
    assert all(sum(p[r][c] for r in range(5))==1 for c in range(5))
    assert not gram_certificate(5,p,1)
    p=[list(row) for row in mask(6,2)]; p[0][0]=False
    assert not gram_certificate(6,p,2)
    # Preserve all row/column weights but destroy Fourier orthogonality.
    p=[[r in {c,(c+1)%5} for c in range(5)] for r in range(5)]
    assert all(sum(row)==2 for row in p)
    assert all(sum(p[r][c] for r in range(5))==2 for c in range(5))
    assert not gram_certificate(5,p,2)
    return {'invalid_divisor_inputs_rejected':invalid,'column_norms_alone_rejected':True,
            'deleted_mask_entry_rejected':True,'two_sided_support_regularity_alone_rejected':True}

def main():
    before=check_inputs()
    (BASE/'CANDIDATE_MANIFEST.json').write_bytes((CANDIDATE/'MANIFEST.json').read_bytes())
    (BASE/'INPUT_CHECK_BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
    results={'arithmetic':'exact rational cyclotomic polynomial quotients; no floating point',
             'candidate_before':before}
    results['divisor_cases']=all_divisors(); print('Divisor Gram controls passed:',len(results['divisor_cases']),flush=True)
    results['explicit_witnesses']=witnesses(); print('Direct inverse witnesses passed:',len(results['explicit_witnesses']),flush=True)
    results['exhaustive_masks']=exhaustive(); print('Exhaustive masks passed:',sum(v['all_column_weight_masks_checked'] for v in results['exhaustive_masks']),flush=True)
    results['obstructions']=obstruction_controls(); print('Prime and odd root-sum obstructions passed',flush=True)
    results['negative_controls']=negative_controls()
    results['candidate_after']=check_inputs(); assert results['candidate_after']==before
    results['checker_sha256']=digest(Path(__file__).read_bytes()); results['all_passed']=True
    (BASE/'FRESH_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print('All exact controls passed; candidate bytes unchanged.',flush=True)

if __name__=='__main__': main()
