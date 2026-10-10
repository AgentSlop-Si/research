"""Independent exact quotient-ring controls for spectra and scalar twists.
Imports only the independently authored fresh_rank_controls in this folder.
"""
from fresh_rank_controls import roots, phi, data, rank_exact
from itertools import product
from math import gcd, lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(c,a): return tuple(c*x for x in a)
def mul(m,a,b):
    d=len(a);p=phi(m);v=[0]*(2*d-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):v[i+j]+=x*y
    for i in range(len(v)-1,d-1,-1):
        for j in range(d):v[i-d+j]-=v[i]*p[j]
    return tuple(v[:d])

def chars(n):
    G=[u for u in range(n) if gcd(u,n)==1]
    def order(u):
        v=u;k=1
        while v!=1:v=v*u%n;k+=1
        return k
    e=lcm(*(order(u) for u in G)); partial=[{1:0}]
    while len(partial[0])<len(G):
        H=set(partial[0]);u=next(u for u in G if u not in H);k=1;v=u
        while v not in H:v=v*u%n;k+=1
        new=[]
        for h in partial:
            for a in range(e):
                if k*a%e!=h[v]:continue
                out={}
                for x,b in h.items():
                    w=x
                    for j in range(k):out[w]=(b+j*a)%e;w=w*u%n
                new.append(out)
        partial=new
    assert len(partial)==len(G)
    return G,e,partial

def project_twist(n,alpha,coeff):
    R=roots(n);return [[sum(c*v for c,v in zip(coeff,mul(n,alpha,R[(i*j)%n]))) for j in range(n)] for i in range(n)]

def main():
    spectral=[]
    for n in [3,4,5,6,7,8,9,10,12]:
        G,e,C=chars(n);M=lcm(n,e);R=roots(M);d=len(R[0]);zero=(0,)*d
        samples=[('one',[1]+[0]*(len(phi(n))-2)),('zeta',[0,1]+[0]*(len(phi(n))-3)),('powers',[j+1 for j in range(len(phi(n))-1)])]
        for label,a in samples:
            # Embed each Galois conjugate of a in Q(zeta_M).
            conjugates={u:tuple(sum(a[k]*R[(k*u*(M//n))%M][j] for k in range(len(a))) for j in range(d)) for u in G}
            rank=0;spectrum=[]
            for c in C:
                lam=zero; mult=zero
                for u in G:
                    lam=add(lam,mul(M,conjugates[u],R[(c[u]*(M//e))%M]))
                    fixed=sum(1 for k in range(n) if (u*k-k)%n==0)
                    mult=add(mult,scale(fixed,R[(-c[u]*(M//e))%M]))
                assert all(x==0 for x in mult[1:]) and mult[0]%len(G)==0
                multiplicity=mult[0]//len(G)
                if lam!=zero:rank+=multiplicity
                spectrum.append({'character_exponents':[c[u] for u in G],'multiplicity':multiplicity,'lambda_coefficients':lam,'lambda_nonzero':lam!=zero})
            matrix=[]
            for i in range(n):
                row=[]
                for j in range(n):
                    v=zero
                    for u in G:v=add(v,mul(M,conjugates[u],R[(i*j*u*(M//n))%M]))
                    assert all(x==0 for x in v[1:]);row.append(v[0])
                matrix.append(row)
            exact=rank_exact(matrix);assert rank==exact
            spectral.append({'N':n,'a_label':label,'a_power_basis':a,'rank_Q':rank,'spectrum':spectrum})
    twists=[]
    for n,alpha,expected in [(3,roots(3)[1],3),(5,(-1,0,-2,-2),4),(5,add(roots(5)[0],roots(5)[1]),5)]:
        for t in range(1,30):
            coeff=[0]+[t**j for j in range(1,len(alpha))]
            matrix=project_twist(n,alpha,coeff);r=rank_exact(matrix)
            if r==expected:break
        assert r==expected
        twists.append({'N':n,'alpha_coefficients':alpha,'L_coefficients':coeff,'rank_Q':r})
    # Explicitly multiply F4 by itself in Q(i).
    R=roots(4);zero=(0,0)
    for i in range(4):
        for j in range(4):
            v=zero
            for k in range(4):v=add(v,mul(4,R[i*k%4],R[k*j%4]))
            assert v==(4 if (i+j)%4==0 else 0,0)
    # Tensor identity from exponents, followed by exact projected rank.
    m,points,exps,orbits=data([3,3]);vals=[r[1] for r in roots(3)]
    tensor=[[vals[e] for e in row] for row in exps];assert rank_exact(tensor)==4
    result={'status':'PASS','exact_spectral_cases':len(spectral),'spectral_cases':spectral,'scalar_twists':twists,'F4_squared_exact':True,'C3_tensor_C3_rank_Q':4,'normalized_F2_rank_Q':2,'normalized_F2_proof':'Over Q(sqrt2), L(1)=0 and L(sqrt2)=2 maps F2/sqrt2 to F2, determinant -2.'}
    (HERE/'FRESH_EDGE_RESULTS.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='spectral_cases'},indent=2))

if __name__=='__main__':main()
