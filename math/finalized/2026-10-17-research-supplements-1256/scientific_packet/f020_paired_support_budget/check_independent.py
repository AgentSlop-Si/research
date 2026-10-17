"""Fresh independent controls for the paired-support budget (SymPy arithmetic).
No producer or historical program is imported or executed. Fixed accepted family
indices are used only for coefficient/deflation checks, not an order census.
"""
from pathlib import Path
import hashlib, json
import sympy as s

ROOT=Path(__file__).parent
q,x,t=s.symbols('q x t')
checks=0

def expect(c):
    global checks
    assert c
    checks+=1

def P(a, v=q):
    return s.Poly(a,v,modulus=2)

def modpow(a,n,f):
    z=P(1)
    while n:
        if n&1:z=(z*a).rem(f)
        a=(a*a).rem(f);n//=2
    return z

def reverse(f):
    n=f.degree()
    return P(sum(int(f.nth(i))*q**(n-i) for i in range(n+1)))

def valuation(f,g):
    k=0
    while f and f.rem(g).is_zero:
        f=f.exquo(g);k+=1
    return k

def evalpoly(h,a,f):
    z=P(0)
    for c in h.all_coeffs():z=(z*a+P(c)).rem(f)
    return z

# Exact synthetic split degree-nine inverse pair, independent of actual family.
f=P(q**9+q**4+1); fs=P(q**9+q**5+1); pair=f*fs
expect(f.is_irreducible and fs.is_irreducible)
expect(reverse(f)==fs and f!=fs and s.gcd(f,fs)==P(1))
expect(pair==P(q**18+q**14+q**13+q**9+q**5+q**4+1))
expect(reverse(pair)==pair and pair.degree()==18)
expect(modpow(P(q),511,f)==P(1))
proper={p:str(modpow(P(q),511//p,f).as_expr()) for p in (7,73)}
expect(all(modpow(P(q),511//p,f)!=P(1) for p in (7,73)))
# Exhaustive degree-nine orbit and inverse-orbit check, not a family census.
orbit=[];a=P(q)
while a not in orbit:
    orbit.append(a);a=(a*a).rem(f)
expect(len(orbit)==9 and a==P(q))
inv=modpow(P(q),510,f)
expect(inv not in orbit)
beta=(P(q)+inv).rem(f)
trace_orbit=[];b=beta
while b not in trace_orbit:
    trace_orbit.append(b);b=(b*b).rem(f)
expect(len(trace_orbit)==9 and b==beta)
h=P(t**9+t**7+t**4+t**3+1,t)
expect(h.is_irreducible and evalpoly(h,beta,f).is_zero)
expect(P(s.expand(q**9*h.as_expr().subs(t,q+1/q)))==pair)
expect(511>pair.degree()**2 and 511==2**9-1)
expect(s.totient(511)==432 and pair.degree()<432)

# A separate nonsplit/self-reciprocal control, demonstrating r != field degree.
f5=P(q**4+q**3+q**2+q+1);h5=P(t**2+t+1,t)
expect(f5.is_irreducible and reverse(f5)==f5)
expect(modpow(P(q),5,f5)==P(1) and P(q).rem(f5)!=P(1))
expect(modpow(P(q),4,f5)!=P(q))
expect(P(s.expand(q**2*h5.as_expr().subs(t,q+1/q)))==f5)
beta5=(P(q)+modpow(P(q),4,f5)).rem(f5)
expect(evalpoly(h5,beta5,f5).is_zero and h5.is_irreducible)
expect((beta5*beta5).rem(f5)!=beta5)
expect(modpow(beta5,4,f5)==beta5)
expect(modpow(P(q),4,f5)==s.invert(P(q),f5))
expect(modpow(P(q),16,f5)==P(q))
expect(5==2**2+1)

# Corruption and scope controls reject an order error, trace alteration,
# and treating a one-sided split factor as a degree-2r paired obstruction.
expect(modpow(P(q),7,f)!=P(1) and modpow(P(q),73,f)!=P(1))
expect(not evalpoly(h+P(1,t),beta,f).is_zero)
expect(s.gcd(f,reverse(f))==P(1) and f.degree()<2*len(trace_orbit))

# Endpoint construction at pre-existing fixed controls only.
selected=(1,2,3,4,12)
Es={0:P(1)};e_prev=P(1);D=P(1)
for m in range(1,max(selected)+1):
    D*=P(1+q**(2*m-1))
    e=D+P(1+q**(2*m))*e_prev
    Es[m]=e;e_prev=e
rows=[]
for m in selected:
    e=Es[m]
    expect(e.degree()==m*(m+1))
    expect(valuation(e,P(q))==m%2)
    expect(valuation(e,P(q+1))==m)
    low=P(1)
    delta=0
    for d in range(3,m+1,2):
        ph=P(s.cyclotomic_poly(d,q));k=m//d
        low*=ph**k
        expect(e.rem(ph**k).is_zero)
        if m%d==0:expect(not e.rem(ph**(k+1)).is_zero)
        delta+=int(s.totient(d))*(((d+1)//2)*k+k//2)
    removed=P(q)**(m%2)*P(q+1)**m*low
    quotient=e.exquo(removed)
    B=m*m-m%2-sum(int(s.totient(d))*(m//d) for d in range(3,m+1,2))
    C=m*(m+1)*(2*m+1)//3-(m+1)//2-m-3*(m*m//4)-2*(m//4)-delta
    expect(quotient.degree()==B and 0<=B<=C)
    rows.append({'m':m,'full_budget':C,'endpoint_budget':B,'endpoint_quotient_degree':quotient.degree()})
expect([z['full_budget'] for z in rows]==[0,4,13,36,1006])
expect([z['endpoint_budget'] for z in rows]==[0,4,6,14,106])
# Known one-sided control must not be classified as paired.
f15=P(q**4+q**3+1);f15s=reverse(f15)
expect(Es[2]==P(q+1)**2*f15)
expect(reverse(Es[2])==P(q+1)**2*f15s)
expect(s.gcd(f15,f15s)==P(1))
expect(modpow(P(q),15,f15)==P(1))
expect(all(modpow(P(q),15//p,f15)!=P(1) for p in (3,5)))
expect(f15.degree()==4 and (f15*f15s).degree()==8)

# Independent small full-Q resultant checks; accepted all-m assumptions remain explicit.
Ps=[s.Poly(1,x,q,modulus=2),s.Poly(x+q+q*q,x,q,modulus=2)]
for m in range(2,5):
    Ps.append(s.Poly((x+q**(2*m-1)*(1+q))*Ps[-1].as_expr()
                    +(1+q**(2*m-1))*(1+q**(2*m-2))*Ps[-2].as_expr(),x,q,modulus=2))
full=[]
for m in (1,2,3,4):
    px=s.Poly(Ps[m].as_expr(),x)
    A=sum(px.nth(2*j)*t**j for j in range(m//2+1))
    B=sum(px.nth(2*j+1)*t**j for j in range((m-1)//2+1))
    R=P(s.resultant(A,B,t))
    Q=Es[m]*R
    N=m*(m+1)*(2*m+1)//3
    expect(Q.degree()==N)
    v=(m+1)//2;kap=m+3*(m*m//4)+2*(m//4)
    low=P(1)
    for d in range(3,m+1,2):
        k=m//d;e=((d+1)//2)*k+k//2
        low*=P(s.cyclotomic_poly(d,q))**e
    quotient=Q.exquo(P(q)**v*P(q+1)**kap*low)
    expect(quotient.degree()==next(z['full_budget'] for z in rows if z['m']==m))
    full.append({'m':m,'Q_degree':Q.degree(),'Qhat_degree':quotient.degree()})

# Fresh derivative/reversal controls only at the already accepted n=0,1,2.
affine=[];C=P(1)
for n in range(3):
    if n:C*=P(1+q**(2*n))
    E=Es[n];Estar=reverse(E)
    # E_0=1; reversing E at actual degree n(n+1) equals reverse here.
    F=E**8+P(q)*C**8;G=P(q)*Estar**8+C**8
    expect(F.diff()==C**8)
    expect(G.diff()==Estar**8)
    expect(reverse(F)==G)
    affine.append({'n':n,'F_degree':F.degree(),'derivatives_and_reversal':True})

out={'status':'PASS','assertions':checks,'engine':'SymPy '+s.__version__,
 'scope':'Independent fresh proof controls; not a new actual-family order/support census',
 'synthetic_split':{'f':str(f.as_expr()),'f_star':str(fs.as_expr()),'pair':str(pair.as_expr()),
   'trace_polynomial':str(h.as_expr()),'field_degree':9,'trace_degree':9,'exact_order':511,
   'prime_divisor_power_residues':proper,'paired_degree':18,'phi_order':432,
   'exceeds_degree_budget_squared':True,'actual_family':False},
 'synthetic_self_reciprocal':{'factor':str(f5.as_expr()),'trace_polynomial':str(h5.as_expr()),
   'field_degree':4,'trace_degree':2,'exact_order':5,'actual_family':False},
 'deflation_controls':rows,'fresh_small_resultants':full,'affine_controls':affine,
 'producer_or_historical_programs_executed':False,'external_writes':False}
(ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
