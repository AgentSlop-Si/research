"""Fresh independent audit arithmetic. No supplied implementation is imported or run.
SymPy supplies cyclotomic polynomials and exact algebraic-field arithmetic only.
Resultants are computed below by an explicitly signed Euclidean recurrence.
"""
import sympy as S
import json, math, time, hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
SRC=Path('ramified_content_extension_0404')
x=S.Symbol('x')

def trim(a):
    a=list(a)
    while a and not a[-1]: a.pop()
    return a

def add(a,b):
    if not a:return b[:]
    if not b:return a[:]
    z=a[0]*0
    return trim([(a[i] if i<len(a) else z)+(b[i] if i<len(b) else z) for i in range(max(len(a),len(b)))])

def scale(a,c):return trim([v*c for v in a])

def mul(a,b):
    if not a or not b:return []
    r=[a[0]*0]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):r[i+j]+=v*w
    return trim(r)

def divmod_poly(a,b):
    a=trim(a); b=trim(b)
    if not b:raise ZeroDivisionError
    z=b[0]*0
    out=[z]*max(0,len(a)-len(b)+1)
    bi=b[-1]**-1
    while a and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]*bi; out[k]=c
        for j,w in enumerate(b):a[k+j]-=c*w
        a=trim(a)
    return trim(out),a

def ev(a,v):
    r=v*0
    for w in reversed(a):r=r*v+w
    return r

def derivative(a):return trim([a[i]*i for i in range(1,len(a))])

def resultant(f,g,one):
    """Res(f,g)=(-1)^(mn) lc(g)^(m-deg rem) Res(g,rem)."""
    f=trim(f);g=trim(g);ans=one
    if not f or not g:return one*0
    while len(g)>1:
        m=len(f)-1;n=len(g)-1
        r=divmod_poly(f,g)[1]
        if not r:return one*0
        ans*=((-1)**(m*n))*g[-1]**(m-(len(r)-1))
        f,g=g,r
    return ans*g[0]**(len(f)-1)

def discriminant(f,one):
    n=len(f)-1
    if n<=1:return one
    return ((-1)**(n*(n-1)//2))*resultant(f,derivative(f),one)/f[-1]

def det(a,one):
    """Field Gaussian determinant, independently checks resultant recurrence."""
    a=[r[:] for r in a];acc=one
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None:return one*0
        if j!=i:a[i],a[j]=a[j],a[i];acc=-acc
        p=a[i][i];acc*=p
        for j in range(i+1,len(a)):
            c=a[j][i]/p
            for k in range(i+1,len(a)):a[j][k]-=c*a[i][k]
            a[j][i]=one*0
    return acc

def mult_det(f,g,one):
    n=len(f)-1; z=one*0; cols=[]
    for j in range(n):
        rr=divmod_poly([z]*j+g,f)[1]
        cols.append(rr+[z]*(n-len(rr)))
    return det([[cols[j][i] for j in range(n)] for i in range(n)],one)

def reciprocal_contract(h,one):
    assert len(h)%2==1 and h==h[::-1]
    r=(len(h)-1)//2;z=one*0
    ts=[[2*one],[z,one]]
    for k in range(2,r+1):ts.append(add([z]+ts[-1],scale(ts[-2],-one)))
    out=[h[r]]
    for k in range(1,r+1):out=add(out,scale(ts[k],h[r+k]))
    return out

def coeffs(a,degree):
    cc=list(reversed(a.to_list()))
    assert all(v.denominator==1 for v in cc),cc
    return [int(v) for v in cc]+[0]*(degree-len(cc))

def content(cc):return math.gcd(*cc)

def run(d):
    started=time.monotonic()
    phi=S.Poly(S.cyclotomic_poly(d,x),x);K=S.QQ.alg_field_from_poly(phi,alias='q')
    q=K.unit;one=K.one;zero=K.zero;dim=phi.degree();b=(d-1)//2;r=b//2
    assert q**d==one
    # q-Pascal: [n,k]=[n-1,k-1]+q^k[n-1,k].
    H=[one]
    for n in range(1,b+1):
        H=[(H[k-1] if k else zero)+(q**k*H[k] if k<len(H) else zero) for k in range(n+1)]
    assert H==H[::-1] and H[-1]==one
    # Direct ordinary derivative resultant, with separate multiplication determinant.
    D=discriminant(H,one)
    Ddet=(-1)**(b*(b-1)//2)*mult_det(H,derivative(H),one)
    assert D==Ddet
    R=one
    for j in range(d):R*=ev(H,-q**j)
    F=[one]+[zero]*(d-1)+[one]
    assert resultant(F,H,one)==R
    B=D*R
    P=reciprocal_contract(H,one);DP=discriminant(P,one)
    Hp=ev(H,one);Hm=ev(H,-one)
    assert D==ev(P,2*one)*ev(P,-2*one)*DP**2
    assert ev(P,2*one)==Hp and ev(P,-2*one)==(-1)**r*Hm
    alt=one
    for j in range(1,r+1):alt*=one-q**(2*j-1)
    assert Hm==alt and ev(H,-q)==Hm
    t=-q**(2*r+1);assert t*t==q
    prod=one
    for j in range(1,2*r+1):prod*=one+t**j
    assert ev(H,t)==prod
    C=reciprocal_contract([((-1)**j)*one for j in range(d)],one)
    etas=[-q**j-q**(-j) for j in range(1,2*r+1)]
    Croot=[one]
    for eta in etas:Croot=mul(Croot,[-eta,one])
    assert C==Croot
    RC=resultant(C,P,one)
    assert R==Hm*RC**2
    assert B==(-1)**r*Hp*(Hm*DP*RC)**2
    Cs,rem=divmod_poly(C,mul([-etas[0],one],[-etas[-1],one]))
    assert not rem and all(all(v.denominator==1 for v in c.to_list()) for c in Cs)
    U=mul(mul([-2*one,one],derivative(P)),Cs)
    M=mult_det(P,U,one)
    assert M==resultant(P,U,one)
    assert M==(-1)**(r+r*(r-1)//2)*Hp*DP*resultant(Cs,P,one)
    raw=json.loads((SRC/f'base_{d}.json').read_text())
    comparisons={}
    for key,val in [('B_coefficients_ascending',B),('discriminant_coefficients_ascending',D),('cluster_resultant_coefficients_ascending',R),('P_discriminant_coefficients_ascending',DP),('H_plus_one_coefficients_ascending',Hp),('H_minus_one_signed_coefficients_ascending',ev(P,-2*one))]:
        comparisons[key]=(coeffs(val,dim)==raw[key]);assert comparisons[key],key
    reduced=next(v for v in json.loads((SRC/'REDUCED_OBSTRUCTION_RESULTS.json').read_text()) if v['d']==d)
    assert coeffs(M,dim)==reduced['determinant_coefficients_ascending']
    assert content(coeffs(B,dim))==int(raw['content'])
    result={'d':d,'B':coeffs(B,dim),'D':coeffs(D,dim),'R':coeffs(R,dim),'M':coeffs(M,dim),'P_discriminant':coeffs(DP,dim),'content':content(coeffs(B,dim)),'content_factorization':{str(p):int(e) for p,e in S.factorint(content(coeffs(B,dim))).items()},'determinant_content':content(coeffs(M,dim)),'all_full_array_comparisons':comparisons,'assertions':'All exact construction, sign, endpoint, special-value, product, resultant and determinant identities passed.','elapsed_seconds':time.monotonic()-started}
    (OUT/f'REBUILT_{d}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'d':d,'content':result['content'],'factorization':result['content_factorization'],'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return result

if __name__=='__main__':
    one=S.QQ.one
    assert resultant([one,one],[2*one,0*one,0*one,one],one)==one
    assert resultant([2*one,0*one,0*one,one],[one,one],one)==-one
    assert mult_det([one,one],[2*one,0*one,0*one,one],one)==one
    controls={'fresh_low_first_odd_odd_resultant':1,'fresh_high_first_odd_odd_resultant':-1,'installed_sympy_version':S.__version__,'installed_sympy_low_first_resultant':int(S.resultant(x+1,x**3+2,x)),'issue':'Known issue #25406 / PR #30329; no new-bug claim.'}
    (OUT/'SIGN_CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n')
    results=[run(d) for d in [17,21,25]]
    (OUT/'COMPUTATION_SUMMARY.json').write_text(json.dumps([{'d':r['d'],'content':r['content'],'content_factorization':r['content_factorization'],'determinant_content':r['determinant_content'],'elapsed_seconds':r['elapsed_seconds']} for r in results],indent=2)+'\n')
