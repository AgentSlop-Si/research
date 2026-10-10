"""Independent characteristic-zero coefficient and finite Weyl controls."""
import json, math, itertools
from pathlib import Path
import sympy as sp
from reviewer_controls import rankdet, inv, mm, mv, mp, eye, cycle_green
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent

def power_vectors(m):
    x=sp.Symbol('x');f=sp.Poly(sp.cyclotomic_poly(m,x),x);d=f.degree()
    coeff=[int(f.nth(i)) for i in range(d)]
    v=[1]+[0]*(d-1);powers=[]
    for k in range(m):
        powers.append(v);lead=v[-1];v=[0]+v[:-1]
        v=[a-lead*b for a,b in zip(v,coeff)]
    return powers

def ramanujan(m,j):
    return sum(int(sp.mobius(m//d))*d for d in sp.divisors(math.gcd(m,j)))

def projected_matrix(factors,L):
    m=math.lcm(*factors);elements=list(itertools.product(*[range(n) for n in factors]));pv=power_vectors(m)
    values=[sum(a*b for a,b in zip(L,v)) for v in pv]
    return [[values[sum(x*y*(m//n) for x,y,n in zip(a,b,factors))%m] for b in elements] for a in elements]

def rational_controls():
    src=BASE/'rational_channels/source_text';out=[];ps=[998244353,1000000007]
    cyclic=json.loads((src/'RANK_CERTIFICATES.json').read_text())['results']
    for rec in cyclic:
        n=rec['n'];m=n;d=len(power_vectors(m));c=len(sp.divisors(n));row={'factors':[n],'ranks':{}}
        for mode in ['trace','traceless','unrestricted']:
            L=[ramanujan(m,j) for j in range(d)] if mode=='trace' else rec['witnesses'][mode]['basis_functional']
            A=projected_matrix([n],L);want=c if mode=='trace' else n-c if mode=='traceless' else n
            ranks=[rankdet(A,p)[0] for p in ps];assert ranks==[want,want]
            row['ranks'][mode]=ranks
        out.append(row);print('Cyclic',n,flush=True)
    abelian=json.loads((src/'ABELIAN_RANK_CERTIFICATES.json').read_text())['results']
    for rec in abelian:
        fs=rec['group_factors'];m=math.lcm(*fs);n=math.prod(fs);pv=power_vectors(m);d=len(pv[0])
        els=list(itertools.product(*[range(k) for k in fs]));units=[k for k in range(m) if math.gcd(k,m)==1]
        orbits={frozenset(tuple(k*x%a for x,a in zip(v,fs)) for k in units) for v in els};c=len(orbits)
        assert c==rec['cyclic_subgroup_count'];row={'factors':fs,'cyclic_subgroups':c,'ranks':{}}
        for mode in ['trace','traceless','unrestricted']:
            want=c if mode=='trace' else n-c if mode=='traceless' else n
            for seed in range(2,30):
                L=[ramanujan(m,j) for j in range(d)] if mode=='trace' else [0 if (j==0 and mode=='traceless') else seed**j for j in range(d)]
                A=projected_matrix(fs,L);ranks=[rankdet(A,p)[0] for p in ps]
                if ranks==[want,want]:break
            else:raise AssertionError((fs,mode))
            row['ranks'][mode]=ranks;row[mode+'_functional']=L
        out.append(row);print('Abelian',fs,flush=True)
    return {'primes':ps,'records':out,'scalar_normalization_example':{'group':'C3','alpha':'zeta3-zeta3^2','traceless_functional':[0,1],'projected_scaled_matrix':[[2,2,2],[2,-1,-1],[2,-1,-1]],'rank':2}}

def kron(A,B):return [[x*y for x in r for y in s] for r in A for s in B]

def weil_controls():
    p=181;g=int(sp.primitive_root(p));rows=[]
    for n in [3,5,9]:
        z=pow(g,(p-1)//n,p);S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
        D=[[pow(z,i,p)*int(i==j) for j in range(n)] for i in range(n)]
        F=[[pow(z,i*j,p) for j in range(n)] for i in range(n)]
        U=[[2,1],[0,3]];J=kron(F,U);X=kron(S,eye(2));Z=kron(D,eye(2))
        assert mm(J,X,p)==mm(Z,J,p)
        assert mm(J,Z,p)==mm(mp(X,n-1,p),J,p)
        J4=mp(J,4,p);assert J4==[[n*n*x%p for x in r] for r in kron(eye(n),mp(U,4,p))]
        terms=[]
        for u in [16,81]:terms.append([[(J4[i][j]-n*n*u*int(i==j))%p for j in range(2*n)] for i in range(2*n)])
        assert not any(v for r in mm(*terms,p) for v in r)
        G=cycle_green(list(range(2*n)),[2]+[1]*(2*n-1),p)
        v=[1]+[0]*(2*n-1);cols=[]
        for j in range(2*n):cols.append(v);v=mv(G,v,p)
        krylov=rankdet(list(zip(*cols)),p)[0];assert krylov==2*n
        rows.append({'N':n,'multiplicity':2,'swap_annihilator_degree':8,'resolvent_krylov_rank':krylov,'obstruction_applies':n>4})
    # PE=I but PJE=0 with a=e1, ell=e1*, U swapping the two copies.
    n=3;F=[[pow(pow(g,60,p),i*j,p) for j in range(n)] for i in range(n)]
    J=kron(F,[[0,1],[1,0]]);E=kron(eye(n),[[1],[0]]);P=kron(eye(n),[[1,0]])
    assert mm(P,E,p)==eye(n);assert not any(v for r in mm(mm(P,J,p),E,p) for v in r)
    # Exhaust all ordered coordinate embeddings in (Z/3Z)^2.
    vs=list(itertools.product(range(3),repeat=2));triples=list(itertools.permutations(vs,3));found=0;nontrivial=0
    dot=lambda u,v:sum(a*b for a,b in zip(u,v))%3
    sub=lambda u,v:tuple((a-b)%3 for a,b in zip(u,v))
    for xs in triples:
      xx=[sub(x,xs[0]) for x in xs]
      for ys in triples:
        yy=[sub(y,ys[0]) for y in ys]
        if not all(dot(xx[i],yy[j])==i*j%3 for i in [1,2] for j in [1,2]):continue
        found+=1;u=xx[1];v=yy[1];assert dot(u,v)==1
        ws=[sub(xx[i],tuple(i*a%3 for a in u)) for i in range(3)]
        ts=[sub(yy[i],tuple(i*a%3 for a in v)) for i in range(3)]
        assert all(dot(w,v)==0 for w in ws) and all(dot(u,t)==0 for t in ts)
        assert all(dot(w,t)==0 for w in ws for t in ts)
        nontrivial+=any(any(w) for w in ws+ts)
    assert (found,nontrivial)==(9720,7776)
    return {'prime':p,'swap_and_cyclic_controls':rows,'zero_scalar_despite_PE_identity':True,'coordinate_pairs':len(triples)**2,'coordinate_embeddings':found,'nontrivial_spectators':nontrivial}

if __name__=='__main__':
    r={'rational_projection':rational_controls(),'weil':weil_controls()}
    (OUT/'reviewer_algebra_results.json').write_text(json.dumps(r,indent=2)+'\n');print('DONE',flush=True)
