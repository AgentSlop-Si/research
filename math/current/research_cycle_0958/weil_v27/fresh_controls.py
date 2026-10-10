"""Independently authored controls. Never imports or executes supplied programs."""
from itertools import product, permutations
from pathlib import Path
import json, hashlib, zipfile, io

OUT=Path(__file__).resolve().parent
def ident(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def scale(a,s,p): return [[s*x%p for x in row] for row in a]
def sub(a,b,p): return [[(x-y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def power(a,k,p):
    r=ident(len(a))
    while k:
        if k&1: r=mul(r,a,p)
        a=mul(a,a,p); k//=2
    return r
def rank(a,p):
    a=[r[:] for r in a]; nr=len(a); nc=len(a[0]) if a else 0; k=0
    for j in range(nc):
        t=next((i for i in range(k,nr) if a[i][j]%p),None)
        if t is None: continue
        a[k],a[t]=a[t],a[k]
        inv=pow(a[k][j],-1,p); a[k]=[x*inv%p for x in a[k]]
        for i in range(k+1,nr):
            q=a[i][j]%p
            if q: a[i]=[(x-q*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==nr: break
    return k
def inverse(a,p):
    n=len(a); b=[r[:]+s for r,s in zip(a,ident(n))]
    for j in range(n):
        t=next(i for i in range(j,n) if b[i][j]%p)
        b[j],b[t]=b[t],b[j]
        q=pow(b[j][j],-1,p); b[j]=[x*q%p for x in b[j]]
        for i in range(n):
            if i!=j:
                q=b[i][j]; b[i]=[(x-q*y)%p for x,y in zip(b[i],b[j])]
    return [r[n:] for r in b]
def kron(a,b): return [[x*y for x in r for y in s] for r in a for s in b]
def flat(a): return [x for r in a for x in r]
def primitive(n,p):
    return next(z for z in range(1,p) if pow(z,n,p)==1 and all(pow(z,d,p)!=1 for d in range(1,n) if n%d==0))
def standard(n,p):
    z=primitive(n,p)
    s=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
    d=[[pow(z,i,p)*int(i==j) for j in range(n)] for i in range(n)]
    f=[[pow(z,i*j,p) for j in range(n)] for i in range(n)]
    return z,s,d,f
def constraints(a,b,p):
    # Unknown Y with Y A = B Y, row-major variables. Written directly entrywise.
    n=len(a); rows=[]
    for i in range(n):
        for j in range(n):
            r=[0]*(n*n)
            for k in range(n):
                r[i*n+k]=(r[i*n+k]+a[k][j])%p
                r[k*n+j]=(r[k*n+j]-b[i][k])%p
            rows.append(r)
    return rows
def minimal_degree(a,p):
    rows=[]; v=ident(len(a))
    for k in range(len(a)+1):
        f=flat(v)
        if rank(rows+[f],p)==len(rows): return k
        rows.append(f); v=mul(v,a,p)
    raise AssertionError('Cayley-Hamilton failed')

report={'provenance':'fresh independent code; no supplied program import, execution, or AST parsing'}
cases=[]
for n,m,p in [(2,2,5),(3,2,7),(4,2,5),(5,2,11),(6,1,13),(9,1,19)]:
    z,s,d,f=standard(n,p); size=n*m
    x=kron(s,ident(m)); zz=kron(d,ident(m)); si=power(x,n-1,p)
    u=ident(m)
    if m>1: u[0][1]=1
    j=kron(f,u)
    comm=size*size-rank(constraints(x,x,p)+constraints(zz,zz,p),p)
    swap=size*size-rank(constraints(x,zz,p)+constraints(zz,si,p),p)
    wrank=rank([flat(mul(power(s,a,p),power(d,b,p),p)) for a,b in product(range(n),repeat=2)],p)
    assert comm==swap==m*m and wrank==n*n
    assert mul(j,x,p)==mul(zz,j,p) and mul(j,zz,p)==mul(si,j,p)
    assert power(j,4,p)==scale(kron(ident(n),power(u,4,p)),n*n,p)
    cases.append({'N':n,'m':m,'p':p,'zeta':z,'weyl_span':wrank,'commutant_dim':comm,'swap_space_dim':swap,'J_minpoly_degree':minimal_degree(j,p),'degree_bound':4*m})
report['exact_linear_algebra']=cases

# A nontrivial simultaneous similarity remains algebraically valid.
n,m,p=3,2,7; z,s,d,f=standard(n,p); dim=n*m
b=ident(dim)
for i in range(dim):
    for k in range(i+1,dim): b[i][k]=(i+k+1)%p
bi=inverse(b,p); x=mul(mul(b,kron(s,ident(m)),p),bi,p); zz=mul(mul(b,kron(d,ident(m)),p),bi,p)
j=mul(mul(b,kron(f,[[0,1],[1,0]]),p),bi,p)
e0=[[int(i==2*k) for k in range(n)] for i in range(dim)]
p0=[[int(k==2*i) for k in range(dim)] for i in range(n)]
e=mul(b,e0,p); pe=mul(p0,bi,p)
assert mul(pe,e,p)==ident(n) and not any(flat(mul(mul(pe,j,p),e,p)))
report['zero_extraction_despite_PE_identity']=True

pts=list(product(range(3),repeat=2)); triples=list(permutations(pts,3)); found=classified=nontrivial=0
dot=lambda a,b,n:sum(x*y for x,y in zip(a,b))%n
minus=lambda a,b,n:tuple((x-y)%n for x,y in zip(a,b))
for xs in triples:
    dx=[minus(x,xs[0],3) for x in xs]
    for ys in triples:
        dy=[minus(y,ys[0],3) for y in ys]
        if not all(dot(dx[i],dy[j],3)==i*j%3 for i,j in product(range(3),repeat=2)): continue
        found+=1; u=dx[1]; v=dy[1]
        w=[minus(dx[i],tuple(i*t%3 for t in u),3) for i in range(3)]
        wp=[minus(dy[j],tuple(j*t%3 for t in v),3) for j in range(3)]
        ok=dot(u,v,3)==1 and all(dot(a,v,3)==0 for a in w) and all(dot(u,b,3)==0 for b in wp) and all(dot(a,b,3)==0 for a in w for b in wp)
        classified+=ok; nontrivial+=any(any(a) for a in w+wp)
assert found==classified==9720 and nontrivial==7776
report['exhaustive_F3_squared']={'candidate_pairs':len(triples)**2,'valid':found,'classified':classified,'nontrivial':nontrivial}

rings=[]
for p in [3,5]:
    n=p*p; xs=[(i,p*(i*i%p)) for i in range(n)]; ys=[(j,p*(j*j%p)) for j in range(n)]
    assert all(dot(xs[i],ys[j],n)==i*j%n for i,j in product(range(n),repeat=2))
    rings.append({'N':n,'all_pairings_exact':True})
report['local_ring_spectators']=rings
report['higher_exponent_counterexamples']=[{'N':n,'ambient_cyclic_order':n*n,'all_phase_exponents_correct':all((n*i*j)%(n*n)==n*(i*j%n) for i,j in product(range(n),repeat=2))} for n in [2,3,4,5,9]]

cyclic=[]
for size,p in [(6,7),(10,11),(12,13)]:
    c=[[0]*size for _ in range(size)]
    for k in range(size): c[(k+1)%size][k]=1 if k<size-1 else 2
    g=inverse(sub(ident(size),c,p),p)
    deg=minimal_degree(g,p); assert deg==size
    cyclic.append({'dimension':size,'field':p,'holonomy':2,'resolvent_minpoly_degree':deg})
report['single_cycle_resolvent_minpolys']=cyclic

zpath=OUT/'sources/fft_primitive_phase_embedding_v27.zip'; z=zipfile.ZipFile(zpath)
prefix='fft_primitive_phase_embedding_v27/'
checks=[]
for line in z.read(prefix+'MANIFEST.sha256').decode().splitlines():
    h,name=line.split('  ',1); checks.append(hashlib.sha256(z.read(prefix+name)).hexdigest()==h)
assert all(checks)
prior=zipfile.ZipFile(io.BytesIO(z.read(prefix+'PRIOR_v26_COMPLETE.zip')))
research=OUT/'sources/RESEARCH(20261010-095635).md'
report['source_integrity']={'archive_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'research_sha256':hashlib.sha256(research.read_bytes()).hexdigest(),'research_matches_archive':research.read_bytes()==z.read(prefix+'RESEARCH.md'),'source_manifest_entries_matched':len(checks),'archive_crc_ok':z.testzip() is None,'embedded_v26_crc_ok':prior.testzip() is None}
(OUT/'fresh_control_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
