"""Fresh exact synthesis controls. No candidate or historical checker is executed.
Run in this directory; frozen mathematical tests do not require original files.
Optional --originals adds byte comparisons against the original local packets.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
C=HERE/'frozen_candidate'
EXPECTED_REPORT='ea1eafbcb45284d945feeb6a5b85f4958b4046c6b945526a26dbb483719ef172'
EXPECTED_MANIFEST='4c8007fa271fdbeecaa8d2f5e2516c003a7b05eefbe864264813b2885a3fa908'
COUNTS={}
def count(k,n=1): COUNTS[k]=COUNTS.get(k,0)+n
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p): return json.loads(p.read_text())
def integrity(originals=False):
    assert sha(C/'REPORT.md')==EXPECTED_REPORT
    assert sha(C/'MANIFEST.json')==EXPECTED_MANIFEST
    m=js(C/'MANIFEST.json')
    for e in m['files']:
        p=C/e['path']; assert sha(p)==e['sha256']; assert p.stat().st_size==e['bytes']
    assert EXPECTED_MANIFEST in (C/'SEAL.sha256').read_text()
    b=js(C/'SOURCE_BINDINGS.json')
    for e in b['copied_sources']:
        p=C/e['copy']; assert sha(p)==e['sha256'] and p.stat().st_size==e['bytes']
        if originals: assert p.read_bytes()==Path(e['source']).read_bytes()
    info=[]
    for e in b['dependencies']:
        L=e['label']; report=C/f'sources/{L}_candidate_REPORT.md'; manifest=C/f'sources/{L}_candidate_MANIFEST.json'; review=C/f'sources/{L}_REVIEW.md'
        assert sha(report)==e['expected_report_sha256']; assert sha(manifest)==e['expected_manifest_sha256']
        assert e['expected_manifest_sha256'] in review.read_text()
        vp=C/f'sources/{L}_VERDICT.json'
        if vp.exists():
            v=js(vp); assert v.get('verdict',v.get('status'))=='PASS'
            assert v['candidate_report_sha256']==sha(report) and v['candidate_manifest_sha256']==sha(manifest)
        else:
            assert L=='E'; assert 'ACCEPT all four' in review.read_text(); assert sha(report) in review.read_text()
        mm=js(manifest);entries=mm.get('files',mm.get('entries'))
        if isinstance(entries,dict):entries=[{'path':k,'sha256':v} for k,v in entries.items()]
        info.append({'label':L,'report_sha256':sha(report),'manifest_sha256':sha(manifest),'review_sha256':sha(review),'manifest_files':len(entries)})
        if originals:
            base=Path(e['candidate_directory'])
            assert (base/'REPORT.md').read_bytes()==report.read_bytes(); assert (base/'MANIFEST.json').read_bytes()==manifest.read_bytes()
            assert (Path(e['review_directory'])/'REVIEW.md').read_bytes()==review.read_bytes()
            for f in entries:
                p=base/f['path']; assert sha(p)==f['sha256']
                if 'bytes' in f:assert p.stat().st_size==f['bytes']
            old=js(base/'SOURCE_BINDINGS.json')
            if isinstance(old,dict): old=old['copied_sources']
            for f in old:
                src=Path(f.get('source',f.get('source_path',f.get('original_path'))))
                cp=base/f.get('copy',f.get('frozen_copy',f.get('frozen_path')))
                assert sha(src)==sha(cp)==f['sha256']
    return {'candidate_files':len(m['files']),'synthesis_source_copies':len(b['copied_sources']),'component_candidate_files':sum(x['manifest_files'] for x in info),'components':info,'originals_checked':originals}

def primes(n): return [p for p in range(7,n+1) if all(p%k for k in range(2,int(p**0.5)+1))]
def classify(q,d):
    if d==0:return 'zero'
    if d<q:return 'P_low'
    if d==q:return 'q'
    if d<2*q:return 'B' if q==7 else 'F'
    if d in (2*q,3*q,4*q):return 'K'
    if d<3*q:return 'M'
    if d<4*q:return 'U'
    if d<5*q:return 'P_high'
    if d==5*q:return 'full'
    raise AssertionError((q,d))
def coverage():
    for q in primes(997):
        N=5*q
        for d in range(N+1):
            tag=classify(q,d); allowed=(tag in ('zero','q','full') or tag=='P_low' and d in (1,5))
            assert allowed==(d in (0,1,5,q,N));count('integer_partition_cases')
        budgets={N-d for d in (1,5,q)}
        assert budgets=={N-1,N-5,4*q}
        assert len(budgets)==3 and all(1<=s<N for s in budgets)
        assert [Q(1,N),Q(5,N),Q(q,N)]==[Q(1,N),Q(1,q),Q(1,5)]
        count('prime_partition_domains')

def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a
def divmod_poly(a,b):
    a=trim(list(a));b=trim(list(b)); quo=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        k=len(a)-len(b); v=Q(a[-1],b[-1]);quo[k]+=v
        for j,x in enumerate(b):a[j+k]-=v*x
        trim(a)
    return trim(quo),a

def phi_n(q):
    top=[0]*(4*q+1)
    for i in range(5):top[i*q]=1
    p,r=divmod_poly(top,[1]*5);assert not any(r);assert all(x.denominator==1 if isinstance(x,Q) else True for x in p)
    return [int(x) for x in p]

def rem_poly(a,p):
    a=list(a)
    for j in range(len(a)-1,len(p)-2,-1):
        if a[j]:
            x=a[j]
            for k,b in enumerate(p):a[j-len(p)+1+k]-=x*b
    return tuple(a[:len(p)-1]+[0]*max(0,len(p)-1-len(a)))

def root_sum(q,exps):
    # Original cyclic exponents, independently reduced in the exact tensor basis.
    grid=[[0]*q for _ in range(5)]
    for e in exps:grid[e%5][e%q]+=1
    return tuple(grid[i][j]-grid[i][q-1]-grid[4][j]+grid[4][q-1] for i in range(4) for j in range(q-1))

def crosscheck_basis(q):
    N=5*q;p=phi_n(q);e5=q*pow(q,-1,5);eq=5*pow(5,-1,q)
    basis=[rem_poly([0]*((i*e5+j*eq)%N)+[1],p) for i in range(4) for j in range(q-1)]
    for e in range(N):
        t=root_sum(q,[e]); v=tuple(sum(c*b[k] for c,b in zip(t,basis)) for k in range(len(p)-1))
        assert v==rem_poly([0]*e+[1],p);count('basis_monomial_crosschecks')
    for r in range(N):
        for c in range(N):
            assert (r*c-e5*(r%5)*(c%5)-eq*(r%q)*(c%q))%N==0;count('crt_original_phase_products')

def mask_divisor(N,d):
    if d==0:return [set() for _ in range(N)]
    assert N%d==0;m=N//d
    return [{c for c in range(N) if c%m==r//d} for r in range(N)]

def gram(q,rows,h,expect):
    N=5*q;d=len(rows[0]); cols=[{r for r in range(N) if c in rows[r]} for c in range(N)]
    assert all(len(x)==d for x in rows+cols)
    failures=[]
    for side,sets in [('row',rows),('column',cols)]:
        fail=None
        for i in range(N):
            for j in range(N):
                delta=i-j if side=='row' else j-i
                v=root_sum(q,(h*delta*k for k in sets[i]&sets[j]))
                target=(d if i==j else 0,)+(0,)*(len(v)-1)
                if v!=target and fail is None:fail={'side':side,'indices':[i,j],'remainder':list(v)}
                count('full_original_gram_entries')
        assert (fail is None)==expect,(q,d,h,side,fail)
        if fail:failures.append(fail)
    return failures

def gram_controls():
    out=[]
    for q in (7,11,13,17):
        N=5*q;crosscheck_basis(q)
        for d in (0,1,5,q,N):
            rows=mask_divisor(N,d)
            for h in (1,2,N-1):
                gram(q,rows,h,True);count('positive_masks_and_root_choices')
        if q not in (7,11,13):continue
        # Fresh low degree and all inherited-interval/endpoints regular negatives.
        fam=[('low_cyclic', [{c for c in range(N) if (c-r)%N<2} for r in range(N)])]
        for k in range(1,5):
            rows=[]
            for r in range(N):
                a,b=r%5,r%q;A={(a+j)%5 for j in range(k)};v=((a+1)*b+a)%q
                rows.append({c for c in range(N) if c%5 in A or c%q==v})
            fam.append((f'interior_k{k}',rows))
        for k in (2,3,4):
            rows=[]
            for r in range(N):
                a,b=r%5,r%q;A={(a+b*b+b+j)%5 for j in range(k)}
                rows.append({c for c in range(N) if c%5 in A})
            fam.append((f'endpoint_k{k}',rows))
        for name,rows in fam:
            fail=gram(q,rows,1,False);count('regular_negative_masks')
            out.append({'q':q,'name':name,'degree':len(rows[0]),'failures':fail})
    return out

class PrimeField:
    def __init__(self,p):
        self.p=p;self.n=p-1;self.zero=(Q(0),)*self.n;self.one=(Q(1),)+(Q(0),)*(self.n-1)
        self.powers=[]
        for i in range(p):
            a=[Q(0)]*self.n
            if i==p-1:a=[Q(-1)]*self.n
            else:a[i]=Q(1)
            self.powers.append(tuple(a))
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def scale(self,a,k):return tuple(k*x for x in a)
    def mul(self,a,b):
        c=[Q(0)]*self.p
        for i,x in enumerate(a):
            if not x:continue
            for j,y in enumerate(b):
                if y:c[(i+j)%self.p]+=x*y
        return tuple(c[i]-c[-1] for i in range(self.n))
    def conj(self,a):
        out=self.zero
        for i,x in enumerate(a):
            if x:out=self.add(out,self.scale(self.powers[-i%self.p],x))
        return out
    def inv(self,a):
        assert a!=self.zero
        # Extended Euclidean polynomial inversion modulo 1+...+X^(p-1).
        r0,r1=[Q(1)]*self.p,trim(list(a));t0,t1=[Q(0)],[Q(1)]
        def pmul(x,y):
            z=[Q(0)]*(len(x)+len(y)-1)
            for i,u in enumerate(x):
                for j,v in enumerate(y):z[i+j]+=u*v
            return trim(z)
        def psub(x,y):
            z=[Q(0)]*max(len(x),len(y))
            for i,v in enumerate(x):z[i]+=v
            for i,v in enumerate(y):z[i]-=v
            return trim(z)
        while any(r1):
            quo,rr=divmod_poly(r0,r1);r0,r1=r1,rr;t0,t1=t1,psub(t0,pmul(quo,t1))
        assert len(r0)==1
        red=rem_poly([x/r0[0] for x in t0],[Q(1)]*self.p)
        assert self.mul(a,red)==self.one
        return red
    def mm(self,A,B):
        return [[self.sum(self.mul(x,y) for x,y in zip(row,col)) for col in zip(*B)] for row in A]
    def sum(self,it):
        out=self.zero
        for x in it:out=self.add(out,x)
        return out
    def adj(self,A):return [[self.conj(x) for x in col] for col in zip(*A)]
    def matinv(self,A):
        n=len(A);T=[list(row)+[self.one if i==j else self.zero for j in range(n)] for i,row in enumerate(A)]
        for j in range(n):
            k=next(i for i in range(j,n) if T[i][j]!=self.zero);T[j],T[k]=T[k],T[j]
            iv=self.inv(T[j][j]);T[j]=[self.mul(iv,x) for x in T[j]]
            for i in range(n):
                if i!=j and T[i][j]!=self.zero:
                    v=T[i][j];T[i]=[self.sub(x,self.mul(v,y)) for x,y in zip(T[i],T[j])]
        return [r[n:] for r in T]
    def identity(self,n,scale=1):return [[self.scale(self.one,scale) if i==j else self.zero for j in range(n)] for i in range(n)]

def inverse_controls():
    results=[]
    for p,other in ((5,7),(7,5)):
        f=PrimeField(p);H=[[f.powers[i*j%p] for j in range(p)] for i in range(p)]
        A=[[H[i][j] if i!=j else f.zero for j in range(p)] for i in range(p)]
        Ast=f.adj(A);J=f.matinv(Ast);Z=[[f.scale(x,p-1) for x in row] for row in J]
        B=[[f.scale(x,Q(1,p-1)) for x in row] for row in Ast]
        ZI=f.mm(Z,B);IZ=f.mm(B,Z)
        assert ZI==f.identity(p) and IZ==f.identity(p)
        E=[[f.sub(Z[i][j],H[i][j]) for j in range(p)] for i in range(p)]
        EE=f.mm(E,f.adj(E));EEt=f.mm(f.adj(E),E)
        assert EE==f.identity(p) and EEt==f.identity(p)
        g=PrimeField(other);Hother=[[g.powers[i*j%other] for j in range(other)] for i in range(other)]
        GG=g.mm(Hother,g.adj(Hother));GGt=g.mm(g.adj(Hother),Hother)
        assert GG==g.identity(other,other) and GGt==g.identity(other,other)
        def scalar(v):
            assert not any(v[1:]);return v[0]
        assert all(sum(x!=f.zero for x in row)==p-1 for row in B)
        assert all(sum(x!=f.zero for x in col)==p-1 for col in zip(*B))
        # Tensor with the other full Fourier matrix. Product separation is exact.
        # Z_N = Z_p tensor H_other, B_N = B_p tensor H_other*/other.
        # E_N = E_p tensor H_other, so both error Grams are other I_N.
        N=p*other;s=(p-1)*other;d=other
        for r in range(N):
            for c in range(N):
                assert (r*c - other*pow(other,-1,p)*(r%p)*(c%p) - p*pow(p,-1,other)*(r%other)*(c%other))%N==0
                # Every entry of full inverse products/error Grams is certified by
                # its two separated exact factor products, in actual CRT labels.
                for small_inv,small_error,large in ((ZI,EE,GG),(IZ,EEt,GGt)):
                    x,y=r%p,c%p;u,v=r%other,c%other
                    full_inverse=scalar(small_inv[x][y])*scalar(large[u][v])/other
                    full_error=scalar(small_error[x][y])*scalar(large[u][v])
                    assert full_inverse==(1 if r==c else 0)
                    assert full_error==(d if r==c else 0)
                    count('factor_certified_original_inverse_entries')
                    count('factor_certified_original_error_gram_entries')
        assert s==N-d
        results.append({'N':N,'d':d,'s':s,'small_field_order':p,'exact_small_inverse_products':2,'exact_small_error_grams':2,'original_index_tensor_certificate':True})
        count('exact_original_inverse_witnesses')
    return results

def main():
    before=integrity('--originals' in sys.argv)
    coverage();negative=gram_controls();inverse=inverse_controls()
    after=integrity('--originals' in sys.argv);assert before==after
    out={'verdict':'PASS','candidate_report_sha256':EXPECTED_REPORT,'candidate_manifest_sha256':EXPECTED_MANIFEST,'integrity':before,'counts':COUNTS,'negative_witnesses':negative,'inverse_witnesses':inverse,'candidate_or_historical_checker_executed':False,'floating_tolerance_used':False,'scope':'Exact finite controls supplement the independent symbolic synthesis proof; no exhaustive square-mask search or finite-prime proof is claimed.'}
    (HERE/'RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'verdict':'PASS','counts':COUNTS,'integrity':before},indent=2,sort_keys=True))
if __name__=='__main__':main()
