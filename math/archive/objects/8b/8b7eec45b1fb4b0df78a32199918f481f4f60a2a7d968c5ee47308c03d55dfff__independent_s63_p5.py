#!/usr/bin/env python3
"""Independent direct-U verification in two F_(5^6) residue components.
Uses elementary symmetric functions (subset generating product), not author code.
"""
import json,hashlib
from pathlib import Path
import sympy as S
from independent_exact_review import cyclotomic
OUT=Path(__file__).resolve().parent

class FF:
    def __init__(self,p,f):
        self.p=p;self.f=f;self.n=len(f)-1
        self.zero=(0,)*self.n;self.one=(1,)+(0,)*(self.n-1);self.q=self.reduce([0,1])
    def reduce(self,a):
        a=list(a)
        for i in range(len(a)-1,self.n-1,-1):
            c=a[i]%self.p
            if c:
                for j,v in enumerate(self.f[:-1]):a[i-self.n+j]-=c*v
        return tuple(x%self.p for x in (a+[0]*self.n)[:self.n])
    def add(self,a,b):return tuple((x+y)%self.p for x,y in zip(a,b))
    def sub(self,a,b):return tuple((x-y)%self.p for x,y in zip(a,b))
    def scale(self,a,k):return tuple((x*k)%self.p for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.n-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]+=x*y
        return self.reduce(c)
    def power(self,a,k):
        c=self.one
        while k:
            if k&1:c=self.mul(c,a)
            a=self.mul(a,a);k//=2
        return c
    def inv(self,a):
        assert a!=self.zero
        b=self.power(a,self.p**self.n-2);assert self.mul(a,b)==self.one
        return b

def trim(a,K):
    a=list(a)
    while len(a)>1 and a[-1]==K.zero:a.pop()
    return a

def rem(a,b,K):
    a=trim(a,K);b=trim(b,K);iv=K.inv(b[-1])
    while len(a)>=len(b) and a!=[K.zero]:
        k=len(a)-len(b);c=K.mul(a[-1],iv)
        for j,x in enumerate(b):a[k+j]=K.sub(a[k+j],K.mul(c,x))
        a=trim(a,K)
    return a

def gcd(a,b,K):
    a=trim(a,K);b=trim(b,K)
    while b!=[K.zero]:a,b=b,rem(a,b,K)
    iv=K.inv(a[-1]);return [K.mul(c,iv) for c in a]

def construct_U(K,q,s=63):
    b=(s-1)//2
    # Coefficients of product_(j=0)^(b-1) (1+w q^j), where w is formal.
    elementary=[K.one]
    for j in range(b):
        power=K.power(q,j);new=elementary+[K.zero]
        for k in range(1,len(new)):new[k]=K.add(new[k],K.mul(power,elementary[k-1]))
        elementary=new
    H=[K.mul(c,K.power(q,(-k*(k-1)//2)%s)) for k,c in enumerate(elementary)]
    U=[]
    for k in range(b):U.append(K.sub(H[k],U[-1] if k else K.zero))
    assert U[-1]==K.one and U==U[::-1]
    assert H[-1]==U[-1]
    return U

def inspect(f,label):
    s=63;p=5;K=FF(p,f);x=S.symbols('q');pol=S.Poly(sum(c*x**j for j,c in enumerate(f)),x,modulus=p)
    assert pol.is_irreducible
    irreducibility_gcd_degrees={str(e):S.gcd(pol,S.Poly(x**e-x,x,modulus=p)).degree() for e in [25,125]}
    assert irreducibility_gcd_degrees=={'25':0,'125':0}
    assert S.rem(S.Poly(sum(c*x**j for j,c in enumerate(cyclotomic(s))),x,modulus=p),pol).is_zero
    q=K.q
    assert K.power(q,15625)==q
    assert K.power(q,63)==K.one and K.power(q,21)!=K.one and K.power(q,9)!=K.one
    rows=[]
    for inverse in [False,True]:
        root=K.inv(q) if inverse else q
        U=construct_U(K,root);der=[K.scale(U[j],j) for j in range(1,len(U))]
        F=[K.one]+[K.zero]*62+[K.one]
        gg=gcd(U,der,K);gf=gcd(U,F,K)
        g=K.zero
        for j,c in enumerate(U):g=K.add(g,K.scale(c,(-1)**j))
        v=K.one
        for j in list(range(2,31,2))+list(range(1,62,2)):
            v=K.mul(v,K.sub(K.one,K.power(root,j)))
        delta=K.sub(K.scale(g,2),v)
        assert delta!=K.zero and g!=K.zero and v!=K.zero
        expected=2 if label=='adverse' else 0
        assert len(gg)-1==0 and len(gf)-1==expected
        rows.append({'inverse':inverse,'U':U,'g':g,'v':v,'delta':delta,
                     'gcd_U_derivative':gg,'gcd_U_z63plus1':gf,
                     'gcd_degrees':[len(gg)-1,len(gf)-1]})
    result={'s':s,'p':p,'label':label,'factor_ascending':f,
            'factor_irreducible':True,'irreducibility_gcd_degrees':irreducibility_gcd_degrees,
            'q_to_15625_equals_q':True,'root_exact_order':63,
            'q_to_63_equals_one':True,'q_to_21_not_one':True,'q_to_9_not_one':True,'rows':rows,
            'augmented_product_nonzero_in_component':label=='good'}
    return result

if __name__=='__main__':
    rows=[inspect([1,0,1,3,1,0,1],'adverse'),inspect([1,1,2,0,2,1,1],'good')]
    result={'method':'Elementary symmetric generating product; direct degree-30 U Euclidean gcds in F_(5^6)',
     'components':rows,'conclusion':'A bad unramified norm component exists, but a good component proves 5 does not divide c_63^+. This is not a counterexample to half-order simplicity.'}
    source_path=OUT/'source/S63_P5_COMPONENT_CERTIFICATE.json'
    if not source_path.exists():source_path=OUT.parents[1]/'augmented_content_followup/S63_P5_COMPONENT_CERTIFICATE.json'
    source=json.loads(source_path.read_text())
    comparisons=[]
    for claimed,actual in zip(source,rows):
        forward,inverse=actual['rows']
        checks={
          'factor':claimed['factor_ascending']==actual['factor_ascending'],
          'U':claimed['U_ascending']==[list(c) for c in forward['U']],
          'inverse_U':claimed['inverse_U_ascending']==[list(c) for c in inverse['U']],
          'delta':claimed['delta']==list(forward['delta']),
          'inverse_delta':claimed['inverse_delta']==list(inverse['delta']),
          'resonance_gcd':claimed['direct_monic_resonance_gcd']==[list(c) for c in forward['gcd_U_z63plus1']],
          'inverse_resonance_gcd':claimed['inverse_monic_resonance_gcd']==[list(c) for c in inverse['gcd_U_z63plus1']]}
        assert all(checks.values()), checks
        comparisons.append(checks)
    result['source_certificate_comparison']=comparisons
    result['source_json_sha256']=hashlib.sha256(source_path.read_bytes()).hexdigest()
    (OUT/'INDEPENDENT_S63_P5.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'adverse_gcd_degrees':[r['gcd_degrees'] for r in rows[0]['rows']],
                      'good_gcd_degrees':[r['gcd_degrees'] for r in rows[1]['rows']]}))
