"""Independent signed magnetic exact controls; no supplied code imported."""
import json,itertools,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
from reviewer_matrix_helper import inv,rankdet,eye

def support_controls():
    out=[];signs=list(itertools.product([1,-1],repeat=2))
    for n in range(3,32,2):
        sets={(e,d):{(a,b) for a in range(n) for b in range(n) if (e*a)%n+(d*b)%n<=n-1} for e,d in signs}
        assert len(set.union(*sets.values()))==n*n
        for missing in signs:
            union=set.union(*(sets[s] for s in signs if s!=missing));assert n*n-len(union)==(n-1)//2
            exc={((missing[0]*t)%n,(missing[1]*t)%n) for t in range(1,(n+1)//2)}
            assert set(itertools.product(range(n),repeat=2))-union==exc
        out.append({'N':n,'three_orientation_holes':(n-1)//2,'all_four_cover':True})
    return out

def signed_matrices():
    out=[]
    for n,p in [(3,7),(5,11),(7,29),(9,19),(11,23),(15,31)]:
        q=pow(int(sp.primitive_root(p)),(p-1)//n,p)
        for e,d in itertools.product([1,-1],repeat=2):
            zeta=pow(q,(e*d)%n,p)
            for alpha in [1,2]:
                beta=next(b for b in range(1,p) if (1-pow(alpha,n,p)-pow(b,n,p))%p)
                delta=(1-pow(alpha,n,p)-pow(beta,n,p))%p;weights=[(j*j+3*j+5)%p for j in range(n)]
                actual=[[0]*n for _ in range(n)]
                for j in range(n):
                    Q=eye(n)
                    for i in range(n):
                        Q[i][i]=(Q[i][i]-beta*pow(zeta,j,p)*pow(q,(d*i)%n,p))%p
                        Q[i][(i-e)%n]=(Q[i][(i-e)%n]-alpha)%p
                    G=inv(Q,p);assert G
                    for i in range(n):
                        for v in range(n):actual[i][v]=(actual[i][v]+weights[j]*G[i][v]*pow(n,-1,p))%p
                predicted=[[0]*n for _ in range(n)]
                for ell in range(n):
                    gamma=sum(weights[j]*pow(zeta,j*ell,p) for j in range(n))*pow(n,-1,p)%p
                    h=gamma*pow(beta,ell,p)*pow(delta,-1,p)%p
                    for r in range(n-ell):
                        gb=1
                        for s in range(1,ell+1):gb=gb*(1-pow(zeta,r+s,p))*pow((1-pow(zeta,s,p))%p,-1,p)%p
                        c=h*pow(alpha,r,p)*gb%p
                        for v in range(n):predicted[(v+e*r)%n][v]=(predicted[(v+e*r)%n][v]+c*pow(q,(d*ell*v)%n,p))%p
                assert actual==predicted
                out.append({'N':n,'p':p,'epsilon':e,'delta':d,'alpha':alpha,'beta':beta,'all_entries_equal':True})
        m=(n-1)//2
        for b in [1,n-1]:
            H=[[pow(q,(((i+j+1+b)**2)*pow(4,-1,n))%n,p) for j in range(m)] for i in range(m)]
            assert rankdet(H,p)[0]==m
    return out

def n9_identity():
    q,v=sp.symbols('q v');phi=q**6+q**3+1
    rem=lambda f:sp.rem(sp.expand(f),phi,q)
    roots=[q**(((a+1)*pow(2,-1,9))%9) for a in range(1,5)]
    Q=sp.Poly(sp.expand(q**4*sp.prod(v-r for r in roots)),v)
    coeffs=[rem(Q.nth(k)*q**((-k*k*pow(4,-1,9))%9)) for k in range(5)]
    expected=[q*q,q**4-q*q+q+1,-q**4+2*q*q-1,-q**5+q**3-q*q-q+1,1]
    assert all(rem(a-b)==0 for a,b in zip(coeffs,expected))
    p0,p1,p2,p3,p4=coeffs
    assert rem(p3*(q*q+1))==1 and rem(p1-q*p3)==0
    E=rem((1+q)**2*(p2-1-q*q)-q*p3*p3)
    assert E==q**5-q**4+2*q*q-2*q-3
    assert rem(E*(2*q**5-q**4+3*q*q-3*q+2))==3
    return {'recurrence_coefficients':list(map(str,coeffs)),'p3_inverse_verified':True,'bezout_constant':3,'characteristic_restriction':'char does not divide 9','r_plus_and_r_minus_each_at_least':3}

def n7_groebner():
    x,y=sp.symbols('x y');z=sp.exp(2*sp.pi*sp.I/7);n=7;eqs=[]
    for a in range(2,n-1):
        eq=z**((((a+1)**2)*pow(4,-1,n))%n)*(1-z*z)*(1-z**(-2))-z*x**(a-1)*(1-z**(a+1))*(1-z**(-2))-y**(n-a-1)*(1-z**(a-1))*(1-z*z)
        eqs.append(eq)
    G=sp.groebner(eqs,x,y,extension=z);assert list(G)==[1]
    return {'field':'Q(zeta7)','variables':['x','y'],'equation_rows':[2,3,4,5],'groebner_basis':[1],'scope':'Characteristic zero only; denominators 1-zeta7^2 and 1-zeta7^-2 are nonzero.'}

if __name__=='__main__':
    out={'support':support_controls(),'signed_matrices':signed_matrices(),'N9':n9_identity(),'N7':n7_groebner()}
    (HERE/'reviewer_signed_results.json').write_text(json.dumps(out,indent=2)+'\n');print('DONE',len(out['signed_matrices']))
