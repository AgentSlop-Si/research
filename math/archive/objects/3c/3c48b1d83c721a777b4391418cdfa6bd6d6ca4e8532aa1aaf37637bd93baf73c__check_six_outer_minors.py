"""Independently reconstruct all six finite-outer necessary constraints.

The only constructor input is a JSON coefficient certificate, never code.
"""
from pathlib import Path
import json, time, hashlib
import sympy as s

base = Path(__file__).resolve().parent
source = base/'N4_OUTER_RANK_MINORS.json'
a,c = s.symbols('a c')
t = s.Symbol('t')
Q = s.QQ_I
Z,V = s.zeros(4),s.zeros(4)
cycle = [0,2,1,3]
for j in range(4):
    Z[(j+1)%4,j] = 1
    V[cycle[(j+1)%4],cycle[j]] = 1
def green(T,p):
    q=s.Rational(1,p)
    return sum((q**k*T**k for k in range(4)),s.zeros(4))/(1-q**4)
G,J=green(Z,4),green(V,5)
H=G+t*J
A=s.Matrix(4,4,lambda i,j:s.expand((-1)**(i+j)*H.minor_submatrix(j,i).det()))
coef=[A.applyfunc(lambda z:s.Poly(z,t).nth(k)) for k in range(4)]
F=s.Matrix(4,4,lambda i,j:s.I**(i*j))
parts={(u,v):coef[u]*F*coef[v] for u in range(4) for v in range(4)}
K={(i,j):s.Poly.from_dict({uv:s.expand(M[i,j]) for uv,M in parts.items()},(a,c),domain=Q) for i in range(4) for j in range(4)}
rows={}
for i in range(1,4):
    for j in range(1,4):
        X,Y=K[i,j]*K[0,0],K[i,0]*K[0,j]
        u=[G[i,0]*G[0,j],G[i,0]*J[0,j]+J[i,0]*G[0,j],J[i,0]*J[0,j]]
        v=[G[i,j]*G[0,0],G[i,j]*J[0,0]+J[i,j]*G[0,0],J[i,j]*J[0,0]]
        rows[i,j]=[X*u[k]-Y*v[k] for k in range(3)]
data=json.loads(source.read_text())
results=[]
for rec in data['minors']:
    start=time.monotonic()
    coords=[tuple(x) for x in rec['coords']]
    x,y,z=[rows[pos] for pos in coords]
    determinant=x[0]*(y[1]*z[2]-y[2]*z[1])-x[1]*(y[0]*z[2]-y[2]*z[0])+x[2]*(y[0]*z[1]-y[1]*z[0])
    index=rec['i']
    guard=K[0,0]*(K[index,0] if rec['mode']=='row' else K[0,index])
    quotient=determinant.exquo(guard).monic()
    supplied=s.Poly.from_dict({tuple(exps):s.Rational(re)+s.I*s.Rational(im) for exps,re,im in rec['terms']},(a,c),domain=Q)
    assert quotient==supplied
    results.append({'mode':rec['mode'],'i':index,'raw_degree':determinant.total_degree(),'quotient_degree':quotient.total_degree(),'terms':len(quotient.terms()),'coefficient_match':True})
    print('Verified',rec['mode'],index,'seconds',time.monotonic()-start,flush=True)
(base/'SIX_OUTER_MINORS_REVIEW.json').write_text(json.dumps({'field':'Q(i)','independent_geometric_sum_and_cofactor_reconstruction':True,'all_coefficients_checked':True,'source_data':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'minors':results,'scope':'Necessary regular-chart constraints only; no assertion that their characteristic-zero ideal excludes solutions.'},indent=2)+'\n')
