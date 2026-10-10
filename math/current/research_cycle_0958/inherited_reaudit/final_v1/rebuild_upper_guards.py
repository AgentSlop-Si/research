"""Fresh exact algebraic checks for the uniform C01 upper construction.
Only imports our newly authored field routines, never historical code.
"""
from pathlib import Path
import json
from rebuild_green_certificate import P, add,sub,mul,div,neg,roots

def norm(x):return (x%P)**2%P-7*(x//P)**2%P
def run():
    z=91;g=(1+2*(z*z+pow(z,3,P)))%P
    C=[[(pow(z,i*j%5,P)-g*pow(z,-3*(i+j)**2%5,P)+(5*g*pow(z,-3*i*i%5,P) if i==j else 0))*pow(1+5*g,-1,P)%P for j in range(5)] for i in range(5)]
    a,b,c,e,f,h=C[0][1],C[0][2],C[1][2],C[1][3],C[1][4],C[2][3]
    alpha,beta,gamma,eps=div(c,mul(a,b)),div(e,mul(a,b)),div(f,mul(a,a)),div(h,mul(b,b))
    L=sub(mul(beta,beta),mul(gamma,eps))
    M=(-2*alpha*beta+alpha*gamma+alpha*eps+beta*gamma+beta*eps-2*gamma*eps)%P
    J=mul(sub(beta,gamma),sub(beta,gamma));p1,p0=div(M,L),div(J,L)
    base=[a,b,gamma,sub(beta,gamma),L,(p1*p1-4*p0)%P]
    assert base==[20,102,234,89,163,163] and [p1,p0]==[30,124]
    assert pow(base[-1],120,P)==P-1
    cases=[]
    for _,d in roots((p0,p1,1)):
        T=sub(mul(gamma,add(d,2)),add(alpha,beta))
        t=div(add(mul(gamma,d),mul(add(alpha,beta),mul(d,d))),T)
        kap=div(add(t,mul(d,d)),gamma);x=div(sub(t,d),kap)
        rr=[x,div(sub(alpha,x),d),div(sub(beta,x),d),div(sub(gamma,x),d)]
        zz=div(kap,add(1,t));u=[1]+[mul(C[0][i],rr[i-1]) for i in range(1,5)]
        v=[div(zz,t)]+[sub(C[0][i],mul(zz,u[i])) for i in range(1,5)]
        delta=[sub(C[i][i],mul(add(1,t),mul(u[i],v[i]))) for i in range(5)]
        assert all(add(mul(u[i],v[j]),mul(t,mul(v[i],u[j])))==C[i][j] for i in range(5) for j in range(i+1,5))
        guards=[norm(y)%P for y in [d,T,kap,t,add(1,t),sub(1,t)]]
        endpoints=[[norm(y)%P for y in vs] for vs in [u,v,delta]]
        assert guards==[124,139,53,1,160,85]
        assert endpoints==[[1,44,153,153,44],[41,117,7,7,117],[72,113,64,64,113]]
        # Reconstruct both actual Green summands entrywise, not only normalized equations.
        for i in range(5):
          for j in range(5):
            first=mul(mul(u[i],v[j]),1 if j>=i else t)
            second=mul(mul(v[i],u[j]),t if j>=i else 1)
            assert add(add(first,second),delta[i] if i==j else 0)==C[i][j]
        cases.append({'d':d,'t':t,'guard_norms':guards,'endpoint_norms':endpoints})
    assert mul(cases[0]['t'],cases[1]['t'])==1
    # Tiny sparse integer polynomial algebra, independent of symbolic libraries.
    def const(n):return {(0,0,0,0,0):n} if n else {}
    def plus(A,B):
        D=A.copy()
        for m,v in B.items():D[m]=D.get(m,0)+v
        return {m:v for m,v in D.items() if v}
    def minus(A,B):return plus(A,{m:-v for m,v in B.items()})
    def times(A,B):
        D={}
        for m,v in A.items():
          for n,w in B.items():
            k=tuple(x+y for x,y in zip(m,n));D[k]=D.get(k,0)+v*w
        return {m:v for m,v in D.items() if v}
    class Poly:
        def __init__(self,d):self.d=d if isinstance(d,dict) else const(d)
        def __add__(self,x):return Poly(plus(self.d,cv(x).d))
        __radd__=__add__
        def __neg__(self):return Poly({m:-v for m,v in self.d.items()})
        def __sub__(self,x):return self+-cv(x)
        def __rsub__(self,x):return cv(x)+-self
        def __mul__(self,x):return Poly(times(self.d,cv(x).d))
        __rmul__=__mul__
        def __pow__(self,n):
            r=Poly(1)
            for _ in range(n):r=r*self
            return r
    def cv(x):return x if isinstance(x,Poly) else Poly(x)
    al,be,ga,ep,dd=[Poly({tuple(int(i==j) for j in range(5)):1}) for i in range(5)]
    LL=be*be-ga*ep;MM=-2*al*be+al*ga+al*ep+be*ga+be*ep-2*ga*ep;JJ=(be-ga)**2
    residual=(be-ga)*(be*dd**2+(be-al)*dd+be-ga)-(ep-be)*dd*(ga*dd+2*ga-al-be)
    assert not (residual-(LL*dd**2+MM*dd+JJ)).d
    ss=al+be
    assert not (JJ*(ga*ga*LL-ga*ss*MM+ss*ss*JJ)-(ga*ga*JJ*LL-ga*(2*ga-ss)*MM*LL+(2*ga-ss)**2*LL**2)).d
    result={'fresh_checks':True,'base_guard_residues':base,'root_polynomial':[p0,p1,1],'both_roots':cases,'generic_integer_polynomial_identities_verified':2,'matrix_entries_verified':50,'q_congruence_argument':'q=1+241*k makes q and q^3 equal 1 in residue ring; all 25 target numerators and denominator therefore reduce identically. Subsequent divisions commute with reduction by verified nonzero norms.','unrerun_historical_controls':'No historical characteristic-zero sample reconstructions, timings, or exact operation profiles were replayed; these are not premises of the uniform proof.'}
    (Path(__file__).resolve().parent/'GREEN_UPPER_FRESH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
