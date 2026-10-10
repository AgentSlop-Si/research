"""Fresh audit checker, authored 2026-10-09.
Never imports, executes, or evaluates uploaded Python. Reads uploaded files only
as bytes/JSON for provenance; all mathematics below is independently implemented.
Finite exact checks supplement the analytic report, not replace its proofs.
"""
from pathlib import Path
from itertools import product, permutations, combinations
from random import Random
import hashlib
import json
import argparse

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,help='Optional uploaded checkpoint directory, read only for provenance hashes; never imported or executed.')
parser.add_argument('--provenance-only',action='store_true',help='With --source, check recorded source hashes without rerunning mathematical checks.')
args=parser.parse_args()
if args.provenance_only and args.source is None:
    parser.error('--provenance-only requires --source')
OUT=Path(__file__).resolve().parent

def provenance(base):
    manifest={str(f.relative_to(base)):hashlib.sha256(f.read_bytes()).hexdigest()
        for name in ('fft_bidirectional_graph_research','fft_bidirectional_extension_research','fft_macro_review_research')
        for f in sorted((base/name).iterdir()) if f.is_file()}
    claims=[]
    def check_hash(rel,expected):
        actual=manifest[rel]
        claims.append({'path':rel,'expected':expected,'actual':actual,'matches':expected==actual})
    graph=json.loads((base/'fft_bidirectional_graph_research/results.json').read_text())
    check_hash('fft_bidirectional_graph_research/affine_cycle.py',graph['source_sha256'])
    ind=json.loads((base/'fft_bidirectional_graph_research/independent_results.json').read_text())
    check_hash('fft_bidirectional_graph_research/affine_cycle.py',ind['source_sha256'])
    check_hash('fft_bidirectional_graph_research/run_audit.py',ind['author_audit_sha256'])
    for result_name in ('results.json','review_edge_results.json'):
        rec=json.loads((base/'fft_bidirectional_extension_research'/result_name).read_text())
        for name,h in rec['source_sha256'].items():
            check_hash('fft_bidirectional_extension_research/'+name,h)
    assert all(x['matches'] for x in claims)
    (OUT/'source_manifest.json').write_text(json.dumps({'scope':'Optional provenance-only static byte/JSON reads; no source execution.', 'files':manifest,'recorded_hash_checks':claims},indent=2)+'\n')
    print(json.dumps({'provenance_status':'PASS','recorded_hashes_checked':len(claims)}))

if args.source is not None:
    provenance(args.source)
if args.provenance_only:
    raise SystemExit(0)
rng=Random(9102026)

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b,p):
    bt=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]
def mv(a,x,p): return [sum(v*w for v,w in zip(row,x))%p for row in a]
def minus(a,b,p): return [[(x-y)%p for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def rank(a,p):
    if not a: return 0
    a=[list(row) for row in a];r=0
    for c in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][c]%p),None)
        if k is None: continue
        a[k],a[r]=a[r],a[k]
        inv=pow(a[r][c],-1,p)
        a[r]=[v*inv%p for v in a[r]]
        for k in range(r+1,len(a)):
            scale=a[k][c]
            a[k]=[(x-scale*y)%p for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a): break
    return r

def inverse(a,p):
    n=len(a);m=[list(row)+e for row,e in zip(a,eye(n))]
    for c in range(n):
        k=next((k for k in range(c,n) if m[k][c]%p),None)
        if k is None: return None
        m[k],m[c]=m[c],m[k];v=pow(m[c][c],-1,p)
        m[c]=[x*v%p for x in m[c]]
        for k in range(n):
            if k!=c:
                v=m[k][c];m[k]=[(x-v*y)%p for x,y in zip(m[k],m[c])]
    return [row[n:] for row in m]

def root(n,p):
    return next(w for w in range(2,p) if pow(w,n,p)==1 and len({pow(w,j,p) for j in range(n)})==n)

def fourier(n,p,w): return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def perm(pi): return [[int(j==pi[i]) for j in range(len(pi))] for i in range(len(pi))]
def orbit(pi):
    o=[];j=0;seen=set()
    while j not in seen: seen.add(j);o.append(j);j=pi[j]
    assert j==0 and len(o)==len(pi)
    return o

def weighted_system(pi,coeff,p):
    m=eye(len(pi))
    for i,j in enumerate(pi): m[i][j]=(m[i][j]-coeff[i])%p
    return m

def closed_cycle(pi,d,rhs,p):
    # Direct expanded numerator; recover forward by division. Zero edges use
    # independent dense elimination, solely a reference for the zero case.
    if not all(d):
        inv=inverse(weighted_system(pi,d,p),p)
        return None if inv is None else mv(inv,rhs,p)
    order=orbit(pi);numerator=0;weight=1
    for i in order:
        numerator=(numerator+weight*rhs[i])%p
        weight=weight*d[i]%p
    if weight==1:return None
    z=[0]*len(pi);z[0]=numerator*pow(1-weight,-1,p)%p
    for i in order[:-1]:z[pi[i]]=(z[i]-rhs[i])*pow(d[i],-1,p)%p
    assert (z[order[-1]]-d[order[-1]]*z[0]-rhs[order[-1]])%p==0
    return z

def fft_reference(x,w,p):
    # Recursive decimation, independently coded.
    n=len(x)
    if n==1:return list(x)
    e=fft_reference(x[::2],w*w%p,p);o=fft_reference(x[1::2],w*w%p,p)
    lo=[];hi=[];tw=1
    for a,b in zip(e,o):
        v=tw*b%p;lo.append((a+v)%p);hi.append((a-v)%p);tw=tw*w%p
    return lo+hi

stats={}
# Full affine intertwining and source/target cycle determinants.
cases=0;accepted=0;singular=0
for p,n in ((17,4),(17,8),(41,4),(41,8),(97,4),(97,8),(97,16),(97,32)):
    w0=root(n,p)
    for w in (w0,pow(w0,-1,p)):
        f=fourier(n,p,w)
        for a,b,c in ((5,1,1),(9,3,5),(-7,-3,-1),(1,1,1)):
            ai=pow(a,-1,n);src=[(a*j+c)%n for j in range(n)];tgt=[ai*(k+b)%n for k in range(n)]
            orbit(src);orbit(tgt)
            m=[[int(j==src[i])*pow(w,b*i%n,p)%p for j in range(n)] for i in range(n)]
            mh=[[int(j==tgt[i])*pow(w,-c*tgt[i]%n,p)%p for j in range(n)] for i in range(n)]
            assert mm(f,m,p)==mm(mh,f,p)
            for lam in (0,1,2,3,5):
                dc=[lam*pow(w,b*j%n,p)%p for j in range(n)]
                dt=[lam*pow(w,-c*tgt[k]%n,p)%p for k in range(n)]
                prod=1
                for v in dt:prod=prod*v%p
                assert prod == -pow(lam,n,p)%p
                sm=weighted_system(src,dc,p);inv=inverse(sm,p)
                assert (inv is None)==((1+pow(lam,n,p))%p==0)
                if inv is None:singular+=1;continue
                u=[0]*n
                for j in rng.sample(range(n),min(2,n)):u[j]=rng.randrange(1,p)
                x=mv(inv,u,p);v=mv(f,u,p)
                y=closed_cycle(tgt,dt,v,p)
                assert y==mv(f,x,p)
                assert mv(weighted_system(tgt,dt,p),y,p)==v
                accepted+=1
            cases+=1
stats['affine_operator_matrix_cases']=cases
stats['affine_dense_gaussian_source_cases']=accepted
stats['affine_singular_determinant_cases']=singular

# Majority schedule and arithmetic-count equations, exhaustive ratio words.
words=0;resets_hist={}
for n in (4,8,16):
    for bad in range(n):
        ratios=[2]*n;ratios[bad]=3
        votes=0;candidate=None;comparisons=0
        for v in ratios:
            if votes==0:candidate=v;votes=1
            else:comparisons+=1;votes += 1 if v==candidate else -1
        assert candidate==2
        total=n+(n+2*comparisons+2)+2*n+(2*n+n)+(5*n+3)
        assert total <=14*n+3
        if bad==0:assert comparisons==n-2 and total==14*n+1
        words+=1
stats['one_defect_majority_positions']=words

# Large exact new-family benchmarks, independent outputs vs recursive FFT.
bench=[];p=65537
for n in (1024,4096,8192,32768):
    w=pow(3,(p-1)//n,p)  # Same primitive root as the submitted p=65537 fixture.
    assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
    lam=next(v for v in range(2,p) if (1+pow(v,n,p))%p)
    src=[(5*j+1)%n for j in range(n)];tgt=[pow(5,-1,n)*(k+1)%n for k in range(n)]
    ds=[lam*pow(w,j,p)%p for j in range(n)];dt=[lam*pow(w,-j%n,p)%p for j in tgt]
    order=orbit(src);x=[0]*n;x[0]=pow(1+pow(lam,n,p),-1,p);v=x[0]
    for j in reversed(order[1:]):v=v*ds[j]%p;x[j]=v
    assert all(x)
    residual=[(x[j]-ds[j]*x[src[j]])%p for j in range(n)]
    assert residual==[1]+[0]*(n-1)
    y=closed_cycle(tgt,dt,[1]*n,p)
    assert y==fft_reference(x,w,p)
    bench.append(dict(N=n,lambda_value=lam,nonzero_input_entries=n,affine_scalar_bill=14*n+1,
                      specified_radix_scalar_bill=n+3*n*(n.bit_length()-1)//2))
stats['large_independent_benchmarks']=bench
# Verify advertised separation witness using dense Gaussian source construction.
n=32;w=pow(3,(p-1)//n,p);s=[(5*j+1)%n for j in range(n)];ds=[2*pow(w,j,p)%p for j in range(n)]
x=mv(inverse(weighted_system(s,ds,p),p),[1]+[0]*31,p)
rr=[[x[j],pow(w,j,p)*x[j]%p,x[j+1],pow(w,j,p)*x[j+1]%p] for j in range(n-1)]
stats['separation_witness']={'rank':rank(rr,p),'untwisted_defects':sum(x[5*j%n]!=x[j] for j in range(n)),'nonzeros':sum(bool(z) for z in x)}
assert stats['separation_witness']=={'rank':4,'untwisted_defects':28,'nonzeros':32}

# Independent generator sandwich construction; T derived densely then compared
# with analytic entries. Apply by upper/lower triangular substitution.
p=101;count=0
for n in (2,3,4,7,11):
    for _ in range(25):
        pp=[rng.randrange(1,p) for _ in range(n)];vv=[rng.randrange(1,p) for _ in range(n)]
        qq,uu,dd=[[rng.randrange(p) for _ in range(n)] for z in range(3)]
        aa=[0]+[pp[i]*pow(pp[i-1],-1,p)%p for i in range(1,n)]
        bb=[0]+[vv[i]*pow(vv[i-1],-1,p)%p for i in range(1,n)]
        a=[[dd[i] if i==j else pp[i]*qq[j]%p if i>j else uu[i]*vv[j]%p for j in range(n)] for i in range(n)]
        l=eye(n);r=eye(n)
        for i in range(1,n):l[i][i-1]=-aa[i]%p;r[i-1][i]=-bb[i]%p
        t=mm(mm(l,a,p),r,p)
        assert all(not t[i][j] for i in range(n) for j in range(n) if abs(i-j)>1)
        md=[dd[0]]+[(dd[i]-aa[i]*uu[i-1]*vv[i])%p for i in range(1,n)]
        lower=[0]+[(pp[i]*qq[i-1]-aa[i]*dd[i-1])%p for i in range(1,n)]
        for i in range(n):
            assert t[i][i]==(md[i]-bb[i]*lower[i])%p
            if i:assert t[i][i-1]==lower[i]
            if i+1<n:assert t[i][i+1]==((uu[i]-(aa[i]*uu[i-1] if i else 0))*vv[i+1]-bb[i+1]*md[i])%p
        assert mm(mm(inverse(l,p),t,p),inverse(r,p),p)==a
        x=[rng.randrange(p) for i in range(n)];z=x[:]
        for i in reversed(range(n-1)):z[i]=(z[i]+bb[i+1]*z[i+1])%p
        y=mv(t,z,p)
        for i in range(1,n):y[i]=(y[i]+aa[i]*y[i-1])%p
        assert y==mv(a,x,p)
        count+=1
stats['sandwich_generator_cases']=count
zero_cases=0
for bits in product((0,1),repeat=6):
    n=4;l=eye(n);r=eye(n)
    for i in range(1,n):l[i][i-1]=-bits[i-1]%p;r[i-1][i]=-bits[i+2]%p
    t=[[rng.randrange(p) if abs(i-j)<=1 else 0 for j in range(n)] for i in range(n)]
    a=mm(mm(inverse(l,p),t,p),inverse(r,p),p)
    for k in range(1,n):
        assert rank([row[k:] for row in a[:k]],p)<=1
        assert rank([row[:k] for row in a[k:]],p)<=1
    zero_cases+=1
stats['zero_transition_converse_cases']=zero_cases

# Sharp component inverse-support examples.
sharp=[]
for b in range(1,9):
    n=2*b+1;l=eye(n);r=eye(n);t=[[4*int(i==j) for j in range(n)] for i in range(n)]
    for i in range(1,n):
        l[i][i-1]=-2%p;r[i-1][i]=-3%p
        if i not in (1,b+1):t[i][i-1]=t[i-1][i]=1
    ti=inverse(t,p);assert ti is not None
    ai=mm(mm(r,ti,p),l,p);support=max(sum(bool(v) for v in row) for row in ai)
    assert support==2*b+1;sharp.append({'b':b,'support':support})
stats['sharp_component_examples']=sharp
# The arbitrary permutation displacement identity is combinatorial.
count=0
for n in range(2,8):
    for pi in permutations(range(n)):
        crossing=sum(sum(pi[i]>=k for i in range(k)) for k in range(1,n))
        assert 2*crossing==sum(abs(i-j) for i,j in enumerate(pi));count+=1
stats['exhaustive_permutation_movement_cases']=count

# Nonuniform rigidity, including zero rows and non-dyadic length.
count=0
for p,n in ((7,3),(5,4)):
    w=root(n,p);f=fourier(n,p,w)
    choices=[[0]*n]+[[v if j==i else 0 for j in range(n)] for i in range(n) for v in range(1,p)]
    # Exhaust N3; deterministic broad N4 sample.
    arrays=product(choices,repeat=n) if n==3 else ([rng.choice(choices) for i in range(n)] for _ in range(5000))
    for s in arrays:
        ss=[sum(bool(v) for v in row) for row in s];rr=rank(minus(f,s,p),p)
        assert n<=min(ss)+rr*(max(ss)+1);count+=1
stats['nonuniform_rigidity_cases']=count
count=0
for n,p in ((3,7),(4,17),(8,17)):
    f=fourier(n,p,root(n,p))
    for m in range(1,n+1):
        for start in range(n):
            rows=[(start+i)%n for i in range(m)]
            for cols in combinations(range(n),m):
                assert rank([[f[i][j] for j in cols] for i in rows],p)==m;count+=1
stats['cyclic_vandermonde_minors']=count
# Support bound and telescoping for random interleaved inverse words.
count=0
for n in (3,4,8,16):
    p=97;f=fourier(n,p,root(n,p))
    for t in range(1,6):
        for budget in range(4):
            for repeat in range(5):
                factors=[]
                for _ in range(t):
                    a=eye(n);upper=rng.randrange(2)
                    for i in range(n):
                        a[i][i]=rng.randrange(1,p);j=i+1 if upper else i-1
                        if 0<=j<n:a[i][j]=rng.randrange(p)
                    factors.append(('scan',a))
                for _ in range(budget):
                    while True:
                        u=[rng.randrange(p) for i in range(n)];v=[rng.randrange(p) for i in range(n)]
                        if (1+sum(a*b for a,b in zip(u,v)))%p:break
                    factors.append(('broadcast',[[(int(i==j)+u[i]*v[j])%p for j in range(n)] for i in range(n)]))
                rng.shuffle(factors);word=eye(n);s=eye(n)
                for kind,a in factors:
                    pi=list(range(n));rng.shuffle(pi);m=perm(pi)
                    word=mm(mm(word,m,p),a,p);s=mm(s,m,p)
                    if kind=='scan':s=mm(s,a,p)
                sizes=[sum(bool(v) for v in row) for row in s]
                assert max(sizes)<=2**t and min(sizes)<=2**(t-1)
                assert rank(minus(word,s,p),p)<=budget
                rr=rank(minus(f,s,p),p);assert n<=min(sizes)+rr*(max(sizes)+1)
                count+=1
stats['interleaved_word_cases']=count
stats['N64_boundary_budgets']=[max(0,-((-(64-2**(t-1)))//(2**t+1))) if t else 32 for t in range(8)]
assert stats['N64_boundary_budgets']==[32,21,13,7,4,2,1,0]

stats['status']='PASS'
stats['method']='Standalone independent mathematical checker; no uploaded code imported or executed. Optional --source is provenance-only.'
(OUT/'independent_results.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
