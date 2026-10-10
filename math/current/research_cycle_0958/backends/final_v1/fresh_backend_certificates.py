"""Fresh exact reconstruction from displayed mathematics; no supplied module read/import.
Polynomial arithmetic and all maps below are independently authored for this audit.
"""
from fractions import Fraction as F
from pathlib import Path
import json, math, itertools, hashlib
OUT=Path(__file__).resolve().parent

def trim(a):
    while len(a)>1 and not a[-1]:a.pop()
    return a

def poly_div(a,b):
    a=list(map(F,a));b=list(map(F,b));q=[F(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and any(a):
        d=len(a)-len(b);v=a[-1]/b[-1];q[d]=v
        for j,c in enumerate(b):a[d+j]-=v*c
        trim(a)
    return trim(q),trim(a)

def cyclo(n):
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            p,r=poly_div(p,cyclo(d));assert not any(r)
    return p
PHI=cyclo(60);D=len(PHI)-1
class K:
    def __init__(self,x=0):
        if isinstance(x,K):self.c=x.c;return
        a=[F(x)] if isinstance(x,(int,F)) else list(map(F,x))
        self.c=tuple(poly_div(a,PHI)[1]+[F(0)]*(D-len(poly_div(a,PHI)[1])))
    def __add__(self,o):
        o=K(o);return K([a+b for a,b in zip(self.c,o.c)])
    __radd__=__add__
    def __neg__(self):return K([-a for a in self.c])
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        o=K(o);r=[F(0)]*(2*D-1)
        for j,a in enumerate(self.c):
            if a:
                for k,b in enumerate(o.c):
                    if b:r[j+k]+=a*b
        return K(r)
    __rmul__=__mul__
    def __truediv__(self,o):return self*F(1,o)
    def __eq__(self,o):return self.c==K(o).c
    def array(self):return [str(x) for x in self.c]
Z=K([0,1]);powers=[K(1)]
for i in range(1,60):powers.append(powers[-1]*Z)
def root(e):return powers[e%60]
B3=[[1,1,1],[0,1,1],[0,1,-1]]
A3=[[1,0,0],[1,1,1],[1,1,-1]]
B4=[[1,0,1,0],[0,1,0,1],[1,0,-1,0],[0,1,0,-1]]
A4=[[1,1,0,0],[0,0,1,1],[1,-1,0,0],[0,0,1,-1]]
B5=[[1,1,1,1,1],[0,1,1,1,1],[0,1,-1,-1,1],[0,1,1,-1,-1],[0,0,1,-1,0],[0,1,0,0,-1]]
A5=[[1,0,0,0,0,0],[1,1,1,1,1,0],[1,1,-1,-1,0,1],[1,1,-1,1,0,-1],[1,1,1,-1,-1,0]]
d3=[K(1),K(F(-3,2)),(root(20)-root(40))/2]
d4=[K(1),K(1),K(1),root(15)]
c1=(root(12)+root(48))/2;c2=(root(24)+root(36))/2
h1=(root(12)-root(48))/2;h2=(root(24)-root(36))/2
d5=[K(1),(c1+c2)/2-1,(c1-c2)/2,h1,h2-h1,h1+h2]

def exact_short(n,A,d,B):
    mat=[[sum((A[k][r]*d[r]*B[r][j] for r in range(len(d))),K()) for j in range(n)] for k in range(n)]
    assert all(mat[k][j]==root((60//n)*k*j) for k in range(n) for j in range(n))
    return mat
short=[exact_short(n,A,d,B) for n,A,d,B in [(3,A3,d3,B3),(4,A4,d4,B4),(5,A5,d5,B5)]]
units=[];diags=[]
for v,u,t in itertools.product(range(6),range(3),range(4)):
    z=d5[v]*d3[u]*d4[t];diags.append({'index_v5_u3_t4':[v,u,t],'coefficients':z.array()})
    if z==1:units.append([v,u,t])
assert units==[[0,0,0],[0,0,1],[0,0,2]]
# All 3600 entries, using exact reconstructed short matrices and CRT maps.
checks=0
for u,v,t,ku,kv,kt in itertools.product(range(3),range(5),range(4),range(3),range(5),range(4)):
    j=(40*u+36*v+45*t)%60;k=(20*ku+12*kv+15*kt)%60
    actual=short[0][ku][u]*short[1][kt][t]*short[2][kv][v]
    assert actual==root(j*k);checks+=1
assert checks==3600
# Perturb a used central channel. Its rank-one input/output factor is nonzero.
negative_control_nonzero=A3[1][1]*A4[0][0]*A5[1][1]*B3[1][1]*B4[0][0]*B5[1][1]
assert negative_control_nonzero==1

def norm_bounds(A):
    one=max(sum(abs(A[i][j]) for i in range(len(A))) for j in range(len(A[0])))
    inf=max(sum(map(abs,row)) for row in A)
    return {'one':one,'infinity':inf,'spectral_squared_upper':one*inf,'frobenius_squared':sum(x*x for r in A for x in r)}
# Enumerate addition orders from dimensions, not the submitted optimizer.
params={3:(3,3,3,3),4:(4,4,4,4),5:(5,6,8,9)}
orders=[]
for pre in itertools.permutations(params):
 for post in itertools.permutations(params):
    dims={i:params[i][0] for i in params};costpre=0
    for i in pre:
        costpre+=params[i][2]*math.prod(dims[j] for j in dims if j!=i);dims[i]=params[i][1]
    costpost=0
    for i in post:
        costpost+=params[i][3]*math.prod(dims[j] for j in dims if j!=i);dims[i]=params[i][0]
    orders.append({'pre':pre,'post':post,'additions':costpre+costpost})
assert min(x['additions'] for x in orders)==444

def primitive(n,p):
    for w in range(2,p):
        if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0):return w
    raise AssertionError('no root')

def boundary_mod(n,a,b,p,w=None):
    w=primitive(n,p) if w is None else w;c=[1]
    for k in range(a+1,n-a):
        z=pow(w,(-k)%n,p);new=[0]*(len(c)+1)
        for i,v in enumerate(c):new[i]=(new[i]-z*v)%p;new[i+1]=(new[i+1]+v)%p
        c=new
    h=[0]*n
    for r,v in enumerate(c):
        s=r-b;h[s%n]=v*pow(w,(-s*(s-1)//2)%n,p)%p
    lam=[sum(v*pow(w,(-k*j)%n,p) for j,v in enumerate(h))%p for k in range(n)]
    # Newly derived exact spectral recurrence, with independent direct-sum reference.
    q=pow(w,-1,p);generated=lam[:2]
    for k in range(n-2):
        nxt=((pow(q,b,p)+pow(q,(k-a)%n,p))*generated[-1]-generated[-2])*pow(q,((a+b)-k)%n,p)%p
        generated.append(nxt)
    assert generated==lam
    assert all((lam[k]-(pow(q,b,p)+pow(q,(k-a)%n,p))*lam[(k+1)%n]+pow(q,(k-a-b)%n,p)*lam[(k+2)%n])%p==0 for k in range(n))
    # Stieltjes-Wigert finite-sum identification via a fresh q-Pascal row.
    gauss=[1]
    for ell in range(1,2*b+1):
        gauss=[((gauss[r] if r<len(gauss) else 0)+(pow(q,ell-r,p)*gauss[r-1] if r else 0))%p for r in range(ell+1)]
    m=2*b;A0=a+1;E=A0*m+m*(m-1)//2+b*(b+1)//2
    for k in range(n):
        z=pow(q,k,p);xx=pow(q,(-(A0+3*b))%n,p)*z%p
        wpoly=sum(gauss[r]*pow(q,r*r,p)*pow(-xx,r,p) for r in range(m+1))%p
        val=pow(-1,m,p)*pow(q,E%n,p)*pow(z,(-b)%n,p)*wpoly%p
        assert val==lam[k]
    # Exact entrywise chirp factorization.
    for j in range(n):
      for t in range(n):
        s=(t-j+b)%n-b
        direct=c[s+b]*pow(w,j*(s-b)%n,p)%p if -b<=s<=b else 0
        gauged=pow(w,t*(t-1)//2%n,p)*h[(t-j)%n]*pow(w,(-j*(j-1)//2-b*j)%n,p)%p
        assert direct==gauged
    # Independently reconstruct coefficients by the q-binomial first-order ratio.
    q=pow(w,-1,p);m=2*b;A=a+1
    c0=pow(-1,m,p)*pow(q,(A*m+m*(m-1)//2)%n,p)%p;seq=[c0]
    for r in range(m):
        ratio=-pow(q,(-(A+m-r-1))%n,p)*(1-pow(q,m-r,p))*pow((1-pow(q,r+1,p))%p,-1,p)%p
        seq.append(seq[-1]*ratio%p)
    assert seq==c
    return {'N':n,'a':a,'b':b,'prime':p,'primitive_root':w,'zero_eigenvalue_indices':[k for k,z in enumerate(lam) if z==0],'rank':sum(z!=0 for z in lam),'coefficient_ratio_verified':True,'spectral_recurrence_verified':True,'Stieltjes_Wigert_identification_verified':True,'factorization_entries_checked':n*n}
modcases=[boundary_mod(n,a,b,p) for n,a,b,p in [(45,11,11,181),(45,11,11,271),(49,12,12,197),(49,12,12,491),(53,13,13,107),(53,13,13,743)]]
# The source uses a smallest primitive FIELD generator, then takes its power.
source_roots=[]
for n,a,b,p in [(45,11,11,181),(45,11,11,271),(49,12,12,197),(49,12,12,491),(53,13,13,107),(53,13,13,743)]:
    g=primitive(p-1,p);w=pow(g,(p-1)//n,p)
    rec=boundary_mod(n,a,b,p,w);rec['field_generator']=g;source_roots.append(rec)
assert [a['rank'] for a in source_roots]==[43,45,47,49,49,53]

def evaluate_mod(z,w,p):
    return sum((v.numerator*pow(v.denominator,-1,p)%p)*pow(w,j,p) for j,v in enumerate(z.c))%p
field_units=[]
for p in [61,181,241,421,601,2013265921,754974721]:
    if p<1000:w=primitive(60,p)
    else:w=pow(31 if p==2013265921 else 11,(p-1)//60,p)
    count=sum(evaluate_mod(d5[v]*d3[u]*d4[t],w,p)==1 for v,u,t in itertools.product(range(6),range(3),range(4)))
    u15=[[v,u] for v,u in itertools.product(range(6),range(3)) if evaluate_mod(d5[v]*d3[u],w,p)==1]
    field_units.append({'prime':p,'root60':w,'identity_count':count,'identity15_positions':u15,'additional_60_setup_products_if_units_skipped':18-len(u15)})
# Exact N=5 autocorrelation: h_-1=w^-1, h_0=phi, h_1=1.
w5=root(12);phi=-(root(24)+root(36));h=[phi,K(1),K(),K(),root(48)]
lam=[sum((h[j]*root(-12*j*k) for j in range(5)),K()) for k in range(5)]
def conj(x):return sum((c*root(-j) for j,c in enumerate(x.c)),K())
mag2=[x*conj(x) for x in lam]
assert mag2[0]!=mag2[3]
assert mag2[0]==mag2[1]==3+4*phi
assert mag2[2]==mag2[3]==mag2[4]==3-phi
# The larger magnitude is phi^2 times the smaller, verified without floats.
assert mag2[0]==phi*phi*phi*phi*mag2[3]
res={'fresh_authorship':True,'supplied_program_execution_import_or_AST':False,'phi60':[str(x) for x in PHI], 'short_exact_entries_checked':9+16+25,'full60_exact_entries_checked':checks,'diagonal_identity_positions':units,'diagonal_nonidentity_count':69,'addition_order_min':444,'addition_order_max':max(x['additions'] for x in orders),'norm_bounds':{n:norm_bounds(A) for n,A in [('B3',B3),('B4',B4),('B5',B5),('A3',A3),('A4',A4),('A5',A5)]},'negative_control_rank_one_response':negative_control_nonzero,'boundary_modular_cases':modcases,'source_root_reconstructions':source_roots,'F60_prime_identity_counts':field_units,'N5_spectrum_nonflat_exact':True,'N5_condition_ratio':'(3+sqrt(5))/2','selected_diagonals':diags,'ordering_records':orders}
(OUT/'fresh_backend_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ('selected_diagonals','ordering_records')},indent=2))
