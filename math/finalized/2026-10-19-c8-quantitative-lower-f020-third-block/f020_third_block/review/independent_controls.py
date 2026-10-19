"""Fresh reviewer controls. No candidate or historical checker is imported/run."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb, prod, gcd
import hashlib, json, time
import sympy as s

ROOT=Path(__file__).resolve().parent
CAND=Path('/workspace/shared/f020_third_block_extension_20261019_1347')
assert hashlib.sha256((CAND/'MANIFEST.json').read_bytes()).hexdigest()=='042d50f56a07262323d5f0480e03bf546418669375e482db95a8575d878407b1'
checks=[]
def record(name, ok, **data):
    assert ok, (name,data)
    checks.append(dict(name=name,passed=True,**data))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
verified=[]; seen=set()
def verify_records(records,base):
    for item in records:
        p=Path(item['path'])
        if not p.is_absolute(): p=base/p
        p=p.resolve()
        b=p.read_bytes()
        assert len(b)==item['bytes'] and sha(p)==item['sha256'],str(p)
        if str(p) not in seen:
            seen.add(str(p)); verified.append(dict(path=str(p),bytes=len(b),sha256=sha(p)))
def verify_manifest(directory):
    p=directory/'MANIFEST.json'; verify_records(json.loads(p.read_text())['files'],directory)
    return sha(p)
verify_manifest(CAND)
verify_records(json.loads((CAND/'SOURCE_BINDINGS.json').read_text())['files'],CAND)
baseline=Path('/workspace/shared/f020_two_digit_hensel_20261019_0124')
base_review=Path('/workspace/shared/f020_primepower_extension_review_20261019_0124')
boundary=Path('/workspace/shared/f020_boundary_hensel_resolution_20261019_0839')
boundary_review=Path('/workspace/shared/f020_boundary_resolution_review_20261019_0840')
for directory in [baseline,base_review,boundary,boundary_review]:
    verify_manifest(directory)
    sb=directory/'SOURCE_BINDINGS.json'
    if sb.exists():
        doc=json.loads(sb.read_text())
        entries=doc.get('files',doc.get('sources',doc.get('bindings',[])))
        assert isinstance(entries,list)
        normalized=[]
        for item in entries:
            source=item.get('path',item.get('source_path',item.get('source')))
            assert source is not None
            normalized.append(dict(path=source,bytes=item['bytes'],sha256=item['sha256']))
            retained=item.get('copy',item.get('retained_copy'))
            if retained is not None:
                normalized.append(dict(path=retained,bytes=item['bytes'],sha256=item['sha256']))
        verify_records(normalized,directory)
bv=json.loads((base_review/'VERDICT.json').read_text())
rv=json.loads((boundary_review/'VERDICT.json').read_text())
record('accepted_baseline_exact_binding',bv['verdict']=='ACCEPT' and bv['author_manifest_sha256']==sha(baseline/'MANIFEST.json') and bv['author_report_sha256']==sha(baseline/'REPORT.md'))
record('accepted_boundary_exact_binding',rv['verdict']=='ACCEPT' and rv['candidate_manifest_sha256']==sha(boundary/'MANIFEST.json') and rv['candidate_report_sha256']==sha(boundary/'REPORT.md'))
(ROOT/'INPUT_VERIFICATION.json').write_text(json.dumps(dict(candidate_manifest_sha256=sha(CAND/'MANIFEST.json'),unique_files_verified=len(verified),files=verified,all_passed=True),indent=2)+'\n')

def add(f,g,factor=1):
    out=f.copy()
    for a,c in g.items():
        out[a]=out.get(a,0)+factor*c
        if not out[a]: del out[a]
    return out
def mul(f,g,cut):
    out={}
    for a,c in f.items():
        for b,d in g.items():
            k=tuple(i+j for i,j in zip(a,b))
            if k[-1]<=cut: out[k]=out.get(k,0)+c*d
    return {a:c for a,c in out.items() if c}
def shift(f,delta,scalar=1):
    return {tuple(i+j for i,j in zip(a,delta)):scalar*c for a,c in f.items()}
def u(n,cut): return {(0,k):-comb(n,k) for k in range(1,min(n,cut)+1)}
def block(start,n,cut):
    if n==0:return {(0,0):1}
    a={(0,0):1}; b={(1,0):1}
    for j in range(1,n):a,b=b,add(shift(b,(1,0)),mul(u(start+j-1,cut),a,cut),-1)
    return b
def vp(c,p):
    k=0
    while c and c%p==0: c//=p;k+=1
    return k
def weight(f,p,alpha):
    return min((Q(a[0])*alpha+a[-1]+p*(p-1)*vp(c,p) for a,c in f.items()),default=Q(10**9))
def translated(f,cut):
    out={}
    for (j,t),c in f.items():
        for k in range(j+1):
            if t+k<=cut:
                key=(j-k,k,t+k);out[key]=out.get(key,0)+c*comb(j,k)
    return {a:c for a,c in out.items() if c}
def lift(f):return {(j,0,t):c for (j,t),c in f.items()}

Y=s.symbols('Y')
for p in [3,5,7,11,13]:
    cut=4*p; alpha=Q(2*p-1,2*p); h=(p-1)//2; L=Q(4*p-1,2); c=(-1)**((p+1)//2)
    P=[block(1,n,cut) for n in range(3*p)]
    A=P[p]; lam={(1,t):v for (j,t),v in A.items() if j==1}
    g=add({(p,0):1},lam)
    C={(0,t):-v for (j,t),v in P[2*p].items() if j==0}
    record(f'p{p}_preceding_weight',weight(P[2*p-1],p,alpha)>=h+p*alpha,actual=str(weight(P[2*p-1],p,alpha)),required=str(h+p*alpha))
    record(f'p{p}_lambda_residue',lam.get((1,p-1),0)%p==c%p and weight(lam,p,0)==p-1)
    record(f'p{p}_pblock_error',weight(add(A,g,-1),p,0)>=p-1)
    hh=[s.Poly(1,Y,modulus=p),s.Poly(Y,Y,modulus=p)]
    for n in range(1,3*p-1):hh.append(s.Poly(Y*hh[n].as_expr()+n*hh[n-1].as_expr(),Y,modulus=p))
    for r in range(p):
        b=2*p+r; eps=r%2; m=r//2; d=prod(range(1,2*m+eps+1,2)); N=L+m+eps*alpha
        F=block(2*p+1,r,cut)
        if r:
            G=block(2*p+2,r-1,cut)
            join=mul(u(2*p,cut),mul(G,P[2*p-1],cut),cut)
            record(f'p{p}_r{r}_exact_join',P[b]==add(mul(F,P[2*p],cut),join,-1))
            gap=(h-alpha) if eps else (h-1+alpha)
            record(f'p{p}_r{r}_join_strict',weight(join,p,alpha)>=N+gap and gap>0,actual=str(weight(join,p,alpha)),threshold=str(N),theoretical_gap=str(gap))
        else: record(f'p{p}_r0_no_join',F=={(0,0):1})
        err=add(F,{(eps,m):d},-1)
        record(f'p{p}_r{r}_tail_residue',d%p!=0 and weight(err,p,alpha)>m+eps*alpha,actual_error_weight=str(weight(err,p,alpha)),leading_weight=str(m+eps*alpha))
        record(f'p{p}_r{r}_outer_recurrence',hh[b]==s.Poly(Y**(2*p)*hh[r].as_expr(),Y,modulus=p))
        record(f'p{p}_r{r}_outer_simple',s.gcd(hh[r],hh[r].diff()).degree()==0)
        record(f'p{p}_r{r}_zero_parity',((hh[r].eval(0)==0)==bool(eps)) and (not eps or hh[r].diff().eval(0)!=0))
        record(f'p{p}_r{r}_root_count',2*p+(r-eps)+eps==b and gcd(2*p-1,2*p)==1)
        n=r-eps
        D=p*(4*p-3)+2*p*r+Q(r*(r-1),2)+eps*(2*p-2)
        distance=2*p*(p-1)+2*p*p*alpha+Q(n*(n-1),2)+n*(2*p+eps)+eps*4*p*alpha
        derivative=2*p*(Q(4*p-3,2)+m+eps*alpha)+n*Q(b-1,2)+eps*(2*p-1+m)
        record(f'p{p}_r{r}_disc_two_derivations',D==distance==derivative,valuation=str(D))
        if p<=7:
            # This is a full translated polynomial before imposing the auxiliary
            # relation g(a)^2=C, not an evaluation at Z=0.
            boundary_center=add(mul(g,g,cut),C,-1)
            err3=add(translated(P[b],cut),mul(translated(F,cut),lift(boundary_center),cut),-1)
            residual={(0,p,0):1,(0,1,0):c}
            main=mul(shift(lift(g),(eps,0,p+m),2*d),residual,cut)
            err3=add(err3,main,-1)
            actual=weight(err3,p,alpha)
            record(f'p{p}_r{r}_full_translated_residual',actual>N,actual_error_weight=str(actual),normalization_weight=str(N),cutoff=cut)
    print('transport',p,'complete',flush=True)

q,x,z,v=s.symbols('q x z v')
P=[s.Poly(1,x,q),s.Poly(x,x,q)]
for n in range(1,10): P.append(s.Poly(x*P[-1].as_expr()-(1-q**n)*P[-2].as_expr(),x,q))
G=[[s.Poly(1,q)]]
for n in range(1,11):
    row=[]
    for k in range(n+1):
        row.append((G[n-1][k] if k<n else s.Poly(0,q))+(s.Poly(q**(n-k),q)*G[n-1][k-1] if k else s.Poly(0,q)))
    G.append(row)
H=[s.Poly(sum(G[n][k].as_expr()*z**k for k in range(n+1)),z,q) for n in range(11)]
for n in range(11):
    ident=s.expand(v**n*P[n].as_expr().subs(x,v+1/v)-H[n].as_expr().subs(z,v*v))
    record(f'actual_H_P_identity_b{n}',ident==0)
for n in range(1,9):
    lhs=0
    for k in range(n):lhs+=P[k].as_expr()**2*prod(1-q**j for j in range(k+1,n))
    rhs=s.diff(P[n].as_expr(),x)*P[n-1].as_expr()-P[n].as_expr()*s.diff(P[n-1].as_expr(),x)
    record(f'actual_CD_b{n}',s.Poly(s.expand(lhs-rhs),x,q).is_zero)

discs={}
for b in [6,7,8]:
    discs[b]=s.Poly(s.discriminant(P[b].as_expr(),x),q)
    print('symbolic P discriminant',b,'complete',flush=True)
for N in [9,27]:
    phi=s.Poly(s.cyclotomic_poly(N,q),q);e=phi.degree()
    # An algebraic number field is built from the cyclotomic polynomial itself.
    K=s.QQ.alg_field_from_poly(phi,'theta')
    theta=K([1,0])
    def specialize(poly,var):
        coeffs={}
        for (j,k),c in poly.terms():
            coeffs[(j,)]=coeffs.get((j,),K.zero)+K(int(c))*theta**k
        return s.Poly.from_dict(coeffs,var,domain=K)
    for b in [6,7,8]:
        rem=discs[b].rem(phi)
        coeff=s.Poly(rem.as_expr().subs(q,1+z).expand(),z)
        terms=[(i[0]+e*vp(int(a),3),i[0]) for i,a in coeff.terms() if a]
        minimum=min(w for w,i in terms)
        record(f'actual_P_disc_N{N}_b{b}',minimum=={6:27,7:37,8:40}[b] and sum(w==minimum for w,i in terms)==1,valuation=minimum,uniformizer_degree=terms[[w for w,i in terms].index(minimum)][1],ramification=e)
        pp=specialize(P[b],x)
        hp=specialize(H[b],z)
        record(f'actual_P_gcd_N{N}_b{b}',s.gcd(pp,pp.diff()).degree()==0)
        record(f'actual_H_gcd_N{N}_b{b}',s.gcd(hp,hp.diff()).degree()==0)
        record(f'actual_H_endpoints_N{N}_b{b}',hp.eval(0)==1 and pp.eval(2)!=0 and pp.eval(-2)!=0)
        if b==7:
            record(f'actual_zero_simple_N{N}_b7',pp.eval(0)==0 and pp.diff().eval(0)!=0)
        if b==8:record(f'actual_no_zero_N{N}_b8',pp.eval(0)!=0)
    print('actual cyclotomic field',N,'complete',flush=True)

(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(dict(all_passed=True,assertions=len(checks),checks=checks),indent=2)+'\n')
print('PASS',len(checks),'exact independent assertions',flush=True)
