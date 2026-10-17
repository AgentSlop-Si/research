"""Independent reviewer controls; no archive code imported or executed."""
import json, math, time
from pathlib import Path
import sympy as s

OUT = Path(__file__).parent / 'fresh_algebra_controls.json'
result = json.loads(OUT.read_text()) if OUT.exists() else {'source':'Independent reviewer implementation; SymPy 1.14.0', 'status':'RUNNING'}
result['status']='RUNNING'
result['omitted_control']='d=49 exact field gcd control was interrupted for cost; no result claimed.'
start=time.monotonic()
def save():
    result['elapsed_seconds']=round(time.monotonic()-start,3)
    OUT.write_text(json.dumps(result,indent=2)+'\n')
def val2(n):
    n=abs(int(n))
    return math.inf if n==0 else (n & -n).bit_length()-1
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c
def sub(a,b):
    return [(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def der(a): return [i*a[i] for i in range(1,len(a))]
def shift_one(a):
    return [sum(a[k]*math.comb(k,j) for k in range(j,len(a))) for j in range(len(a))]
def parity_hermite(m,parity):
    n=2*m+parity
    return [(-1)**(m-j)*math.factorial(n)//(2**(m-j)*math.factorial(m-j)*math.factorial(2*j+parity)) for j in range(m+1)]
wr=[]
for parity in [0,1]:
    for m in range(1,51):
        a,b=parity_hermite(m,parity),parity_hermite(m-1,parity)
        w=sub(mul(der(a),b),mul(a,der(b)))
        while len(w)>1 and w[-1]==0: w.pop()
        c=shift_one(w)
        assert len(c)==2*m-1 and c[-1]==1
        assert val2(c[0])==m-1
        assert all(2*val2(v)>=2*m-2-j for j,v in enumerate(c))
        for j,v in enumerate(c):
            if j%2==0:
                assert ((v//2**(m-1-j//2))%2)==math.comb(m-1,j//2)%2
        wr.append({'family':'U' if parity==0 else 'V','m':m,'degree':len(c)-1,'constant_v2':int(val2(c[0])),'newton_bound_pass':True,'scaled_mod_pi_pass':True})
result['wronskians']=wr; save(); print('Wronskian checks passed:',len(wr),flush=True)

q,z,x=s.symbols('q z x')
def poly_from_field(coeff,z,K): return s.Poly.from_list(list(reversed(coeff)),z,domain=K)
def rs_fields(d,max_b):
    K=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(d,q),q),alias='w')
    w=K.unit
    H=[[K.one],[K.one,K.one]]
    for n in range(2,max_b+1):
        h=[K.zero]*(n+1)
        for j,c in enumerate(H[-1]): h[j]+=c; h[j+1]+=c
        for j,c in enumerate(H[-2]): h[j+1]+=(w**(n-1)-K.one)*c
        H.append(h)
    return K,w,H

static=result.get('static',[])
completed_static={v['d'] for v in static}
for d,p in [(3,3),(5,5),(7,7),(11,11),(13,13),(17,17),(9,3),(25,5),(27,3)]:
    if d in completed_static: continue
    K,w,H=rs_fields(d,p-1)
    F=s.Poly(z**d+1,z,domain=K)
    for b in range(p):
        h=poly_from_field(H[b],z,K)
        assert h.degree()==b
        assert h.gcd(h.diff()).degree()==0
        target=h.exquo(s.Poly(z+1,z,domain=K)) if b%2 else h
        assert target.gcd(F).degree()==0
        static.append({'d':d,'p':p,'b':b,'squarefree':True,'fixed_separation':True})
    result['static']=static; save(); print('Static guards passed:',d,flush=True)

partial=result.get('partial_sums',[])
completed_partial={v['d'] for v in partial}
for d in range(3,36,2):
    if d in completed_partial: continue
    h=(d-1)//2
    K,w,H=rs_fields(d,d-2)
    terms=[K.one]; sums=[K.one]
    for k in range(1,h+1):
        terms.append(terms[-1]*(K.one-w**(2*k-1))/(K.one-w**(2*k)))
        sums.append(sums[-1]+terms[-1])
    E=K.one
    for k in range(1,h+1): E*=K.one-w**(2*k)
    assert sums[h]==K.convert(d)/E
    for r in range(h):
        b=2*r+1
        g=sum((K.convert(k*(-1)**(k-1))*H[b][k] for k in range(1,b+1)),K.zero)
        even=K.one
        for k in range(1,r+1): even*=K.one-w**(2*k)
        assert g==even*sums[r] and g!=K.zero
        W=K.one
        for k in range(1,b+1): W*=K.one-w**k
        for k in range(1,(d+b)//2+1): W/=K.one-w**(2*k)
        tau=K.convert(d)*W/g
        assert tau==sums[h]/sums[r]
        # Nonreality exactly: conjugation substitutes w^{-1} into the ANP.
        conjugate=K.zero
        for coeff in tau.to_list(): conjugate=conjugate/w+K.convert(coeff)
        assert tau!=conjugate
        partial.append({'d':d,'b':b,'derivative_identity':True,'tau_ratio':True,'nonreal_exact':True})
    result['partial_sums']=partial; save(); print('Partial sums passed:',d,flush=True)

# Rational zero-root exceptions, plus ordinary rational parameters including tau=1.
exceptions=[]
for A in range(1,21):
    for tau in [s.Rational(0),s.Rational(1),-s.Rational(1,A),s.Rational(2,3),s.Rational(-7,4)]:
        J=s.Poly(x*s.hermite_prob(A,x)-A*tau*s.hermite_prob(A-1,x),x)
        repeated=J.gcd(J.diff()).degree()>0
        expected=(tau==0 if A%2 else tau==-s.Rational(1,A))
        assert repeated==expected
        exceptions.append({'A':A,'tau':str(tau),'repeated':repeated})
result['rational_exception_controls']=exceptions

# Direct full polynomial controls for the integral Hermite initial form and node quotients.
Hs=[s.Poly(1,z,q),s.Poly(1+z,z,q)]
for n in range(2,10): Hs.append(s.Poly((1+z)*Hs[-1].as_expr()+(q**(n-1)-1)*z*Hs[-2].as_expr(),z,q))
nodes=[]
for b in range(10):
    h=Hs[b].as_expr()
    target=s.div(h,z+1,z)[0] if b%2 else h
    r=b//2
    expected=(-1)**r*(s.factorial2(b) if b%2 else s.factorial2(b-1))
    for j in [0,1,3,7,11]:
        node=s.Poly(target.subs(z,-q**j),q)
        quo,rem=s.div(node,s.Poly((q-1)**r,q))
        assert rem.is_zero and quo.eval(1)==expected
        nodes.append({'b':b,'j':j,'order_at_1':r,'quotient_at_1':int(expected)})
result['node_quotients']=nodes
ramified_tau=(-1+2*s.sqrt(-2))/3
ramified_J=s.expand(x*s.hermite_prob(3,x)-3*ramified_tau*s.hermite_prob(2,x))
assert s.expand(ramified_J-(x*x-(1+s.sqrt(-2)))**2)==0
result['negative_control_ramified_field']={'A':3,'tau':'(-1+2*sqrt(-2))/3','field':'Q_2(sqrt(-2)), ramified','J':'(x^2-(1+sqrt(-2)))^2','nonreal_but_not_squarefree':True,'reason':'Unramified hypothesis cannot be replaced by merely nonreal tau.'}
result['counts']={k:len(v) for k,v in result.items() if isinstance(v,list)}
result['status']='PASS'; save(); print('ALL PASS',result['elapsed_seconds'],flush=True)
