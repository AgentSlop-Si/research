"""Fresh exact controls for proof-boundary corollaries; no historical imports.

This is not an actual-family support census. Endpoint affine controls use only
the previously accepted symbolic indices 0, 1, 2. The order-511 polynomial is
a synthetic negative control for confusing paired and whole-cyclotomic bounds.
"""
import json
from pathlib import Path

def deg(a): return a.bit_length()-1
def mul(a,b):
    c=0
    while b:
        if b&1: c^=a
        a<<=1; b>>=1
    return c
def rem(a,b):
    while a and deg(a)>=deg(b): a^=b<<(deg(a)-deg(b))
    return a
def gcd(a,b):
    while b: a,b=b,rem(a,b)
    return a
def power(a,n):
    r=1
    while n:
        if n&1: r=mul(r,a)
        a=mul(a,a); n>>=1
    return r
def modpow(a,n,f):
    r=1
    while n:
        if n&1:r=rem(mul(r,a),f)
        a=rem(mul(a,a),f); n>>=1
    return r
def reverse(a,n=None):
    n=deg(a) if n is None else n
    return sum(((a>>i)&1)<<(n-i) for i in range(n+1))
def derivative(a):return sum(((a>>i)&1)<<(i-1) for i in range(1,deg(a)+1,2))
def phi(n):
    out=n;p=2
    while p*p<=n:
        if n%p==0:
            out-=out//p
            while n%p==0:n//=p
        p+=1
    if n>1:out-=out//n
    return out

rows=[];E=C=D=1
for n in range(3):
    if n:
        D=mul(D,1|(1<<(2*n-1)))
        C=mul(C,1|(1<<(2*n)))
        E=D^mul(1|(1<<(2*n)),E)
    Estar=reverse(E,n*(n+1))
    F=power(E,8)^(power(C,8)<<1)
    G=(power(Estar,8)<<1)^power(C,8)
    assert G==reverse(F,8*n*(n+1)+1)
    assert derivative(F)==power(C,8)
    assert derivative(G)==power(Estar,8)
    rows.append({'n':n,'F':hex(F),'G':hex(G),'gcd':hex(gcd(F,G)),
                 'reversal_pass':True,'derivative_identities_pass':True})

budgets=[]
for m in (1,2,3,4,12):
    N=m*(m+1)*(2*m+1)//3
    delta=sum(phi(d)*(((d+1)//2)*(m//d)+(m//d)//2) for d in range(3,m+1,2))
    full=N-(m+1)//2-m-3*(m*m//4)-2*(m//4)-delta
    endpoint=m*m-m%2-sum(phi(d)*(m//d) for d in range(3,m+1,2))
    assert full>=0 and endpoint>=0
    budgets.append({'m':m,'full_degree_budget':full,'full_trace_degree_bound':full//2,
                    'endpoint_degree_budget':endpoint,'endpoint_trace_degree_bound':endpoint//2})
assert [x['full_degree_budget'] for x in budgets]==[0,4,13,36,1006]
assert [x['endpoint_degree_budget'] for x in budgets]==[0,4,6,14,106]

# Known m=2 one-sided endpoint control: it must not be called a paired obstruction.
f15=0x19;g15=reverse(f15)
assert E==mul(power(3,2),f15)
assert reverse(E)==mul(power(3,2),g15)
assert gcd(f15,g15)==1
assert modpow(2,15,f15)==1 and modpow(2,5,f15)!=1 and modpow(2,3,f15)!=1

# Synthetic primitive degree-nine inverse pair, unrelated to actual RS coefficients.
f=0x211;fstar=reverse(f)
assert deg(f)==9 and fstar==0x221
assert modpow(2,512,f)==2 and gcd(modpow(2,8,f)^2,f)==1
assert modpow(2,511,f)==1
proper={str(p):hex(modpow(2,511//p,f)) for p in (7,73)}
assert all(int(x,16)!=1 for x in proper.values())
assert f!=fstar and gcd(f,fstar)==1
paired=mul(f,fstar)
assert reverse(paired)==paired and deg(paired)==18
assert 511>18**2 and 511==2**9-1

out={'status':'PASS','scope':'Fresh transcription controls, not a new actual-family census',
     'endpoint_affine_controls':rows,'degree_budget_controls':budgets,
     'one_sided_boundary':{'m':2,'factor':hex(f15),'inverse_factor':hex(g15),'order':15,'paired':False},
     'synthetic_cutoff_counterexample':{'actual_RS':False,'factor':hex(f),'inverse_factor':hex(fstar),
          'pair':hex(paired),'degree_budget':18,'exact_order':511,'trace_degree':9,
          'irreducibility':'Rabin x^(2^9)=x and gcd(x^(2^3)-x,f)=1',
          'order_prime_divisor_tests':proper,'exceeds_degree_budget_squared':True},
     'uploaded_or_historical_programs_executed':False,'external_writes':False}
Path(__file__).with_name('CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
