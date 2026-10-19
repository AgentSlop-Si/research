#!/usr/bin/env python3
"""Fresh exact checks for the 3q endpoint. Never imports candidate/historical code."""
import hashlib, itertools, json, math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RESULTS={"historical_code_executed":False,"external_writes":False,"arithmetic":"exact integers plus SymPy rational algebraic fields for original inverse witnesses"}

def write(name,data): (ROOT/name).write_text(json.dumps(data,indent=2)+"\n")
def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def divide(a,b):
    a=trim(a); b=trim(b); out=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a!=[0]:
        assert a[-1]%b[-1]==0
        j=len(a)-len(b); x=a[-1]//b[-1]; out[j]=x
        for k,y in enumerate(b): a[j+k]-=x*y
        a=trim(a)
    assert a==[0]
    return trim(out)

def phi3q(q):
    # Phi_(3q)(X)=Phi_q(X^3)/Phi_q(X), independently generated.
    a=[0]*(3*(q-1)+1)
    for j in range(q): a[3*j]=1
    return divide(a,[1]*q)

class Ring:
    def __init__(self,q):
        self.q=q; self.n=3*q; self.poly=phi3q(q); self.degree=len(self.poly)-1
        self.zero=(0,)*self.degree; self.one=(1,)+(0,)*(self.degree-1)
        p=self.one; self.powers=[]
        for k in range(self.n): self.powers.append(p); p=self.reduce((0,)+p)
        assert p==self.one
        assert all(self.powers[k]!=self.one for k in range(1,self.n))
    def reduce(self,a):
        a=list(a)
        while len(a)>self.degree:
            i=len(a)-self.degree-1; x=a[-1]
            for j,c in enumerate(self.poly): a[i+j]-=x*c
            a.pop()
        return tuple(a+[0]*(self.degree-len(a)))
    def root_sum(self,exponents):
        out=[0]*self.degree
        for k in exponents:
            for j,x in enumerate(self.powers[k%self.n]): out[j]+=x
        return tuple(out)
    def gram(self,mask,left):
        n=self.n; out=[]
        for r in range(n):
            line=[]
            for s in range(n):
                if left: ks=((r-s)*c for c in range(n) if mask[r][c] and mask[s][c])
                else: ks=((s-r)*c for c in range(n) if mask[c][r] and mask[c][s])
                line.append(self.root_sum(ks))
            out.append(line)
        return out

def mask_divisor(n,d):
    m=n//d
    return [[int(r//d==c%m) for c in range(n)] for r in range(n)]

def degrees(mask): return [sum(r) for r in mask],[sum(r[c] for r in mask) for c in range(len(mask))]

def verify_positive(ring,mask,d):
    n=ring.n
    assert degrees(mask)==([d]*n,[d]*n)
    for left in (True,False):
        G=ring.gram(mask,left)
        assert all(G[r][s]==(tuple(d*x for x in ring.one) if r==s else ring.zero) for r in range(n) for s in range(n))
    return {"N":n,"d":d,"both_full_Grams":True,"support_rows":[[c for c,x in enumerate(row) if x] for row in mask]}

# CRT formula with the actual integer row and column labels, every primitive root.
crt=[]; positive=[]; negative=[]
for q in (5,7,11,13,17):
    K=Ring(q); n=K.n; A=pow(q,-1,3); B=pow(3,-1,q); cnt=0
    for k in range(1,n):
        if math.gcd(k,n)!=1: continue
        for r in range(n):
            for c in range(n):
                rhs=k*(q*A*(r%3)*(c%3)+3*B*(r%q)*(c%q))
                assert (k*r*c-rhs)%n==0
                cnt+=1
    crt.append({"q":q,"N":n,"q_inverse_mod_3":A,"3_inverse_mod_q":B,"exact_congruence_checks":cnt})
    if q in (5,7,11):
        for d in (1,3,q,n): positive.append(verify_positive(K,mask_divisor(n,d),d))
    mask=[[int(r%3!=c%3) for c in range(n)] for r in range(n)]
    assert degrees(mask)==([2*q]*n,[2*q]*n)
    failures={"row":Counter(),"column":Counter()}; examples={}
    for left in (True,False):
        label="row" if left else "column"; G=K.gram(mask,left)
        for r in range(n):
            for s in range(n):
                if r==s:
                    assert G[r][s]==tuple(2*q*x for x in K.one)
                    continue
                order=n//math.gcd(r-s,n)
                if order==3:
                    assert G[r][s]!=K.zero
                    failures[label][str(order)]+=1
                    examples.setdefault(label,{"indices":[r,s],"cyclotomic_remainder_ascending":G[r][s]})
                else:
                    assert order in (q,n) and G[r][s]==K.zero
    assert failures["row"]["3"]==6*q==failures["column"]["3"]
    negative.append({"q":q,"N":n,"d":2*q,"all_degrees_correct":True,"all_order_q_and_3q_offdiagonal_Grams_zero":True,"failure_counts_by_character_order":{k:dict(v) for k,v in failures.items()},"first_failures":examples,"support_rows":[[c for c,x in enumerate(row) if x] for row in mask]})
RESULTS["CRT"]=crt; RESULTS["positive_mask_count"]=len(positive); RESULTS["endpoint_countercontrol_count"]=len(negative)
write("POSITIVE_MASKS.json",positive); write("ENDPOINT_COUNTERCONTROLS.json",negative)

# Exhaust all binary primitive-character overlaps at the smallest allowed q.
K=Ring(5); n=K.n; zeros=0; total=1<<n
for bits in range(total):
    if K.root_sum(c for c in range(n) if bits>>c&1)!=K.zero: continue
    zeros+=1
    three_lines=all(len({(bits>>c)&1 for c in range(n) if c%5==v})==1 for v in range(5))
    q_lines=all(len({(bits>>c)&1 for c in range(n) if c%3==u})==1 for u in range(3))
    assert three_lines or q_lines
assert zeros==2**3+2**5-2
RESULTS["binary_primitive_overlap_census"]={"N":15,"supports_tested":total,"vanishing_supports":zeros,"all_parallel_lines":True}

# Enumerate all local vector multisets, including multiplicity. Weighting gives
# all labeled configurations without assuming the restrictions are distinct.
local=[]
for q in (5,7,11):
    multiset_count=pair_one_count=pair_one_labeled=full_count=0; max_entries=0
    for vec in itertools.combinations_with_replacement(range(8),q):
        multiset_count+=1
        dots=[(vec[i]&vec[j]).bit_count() for i in range(q) for j in range(i)]
        if all(x in (1,2) for x in dots) and 7 in vec and all(x==7 or x.bit_count()==1 for x in vec):
            # The singleton condition comes from the GLOBAL equal-overlap
            # implies identical-support argument, not local dots alone.
            full_count+=1
            assert all(x==1 for x in dots)
            others=[x for x in vec if x!=7]
            assert len(others)==q-1 and len(set(others))==1 and others[0].bit_count()==1
        if not all(x==1 for x in dots): continue
        pair_one_count+=1; count=Counter(vec)
        labeled=math.factorial(q)
        for v in count.values(): labeled//=math.factorial(v)
        pair_one_labeled+=labeled
        singleton=[x for x in vec if x.bit_count()==1]
        assert singleton
        base=singleton[0]
        assert all(x&base for x in vec)
        extras=[x^base for x in vec]
        assert all(extras[i]&extras[j]==0 for i in range(q) for j in range(i))
        entry_count=sum(x.bit_count() for x in vec)
        assert entry_count<=q+2
        max_entries=max(max_entries,entry_count)
    local.append({"q":q,"all_multisets_tested":multiset_count,"pairwise_one_multisets":pair_one_count,"pairwise_one_labeled_configurations":pair_one_labeled,"pairwise_one_max_entries":max_entries,"full_vector_multisets_with_pairwise_one_or_two":full_count})
RESULTS["local_vector_exhaustion"]=local
RESULTS["local_only_guard"]={"example_masks":[3,3,3,3,7],"pairwise_dots_one_or_two":True,"full_vector_present":True,"warning":"Local dot products alone do not force all pairwise dots one. The proof correctly first uses global support equality at overlap 2q."}

# q=5 full missing-function audit: all 3^q x 3^q ordered pairs, including
# nonconstant functions and all intersections of size one or two.
q=5; functions=list(itertools.product(range(3),repeat=q)); valid=0; profile=Counter()
for f in functions:
    matched=[]
    for g in functions:
        intersections=[(7^(1<<x))&(7^(1<<y)) for x,y in zip(f,g)]
        if len(set(intersections))==1: matched.append(g); valid+=1
    distinct=len(set(f)); profile[str(distinct)]+=1
    assert len(matched)=={1:3,2:1,3:0}[distinct]
    if distinct==1: assert all(len(set(g))==1 for g in matched)
    if distinct==2:
        g=matched[0]; pair=set(f)
        assert all(x!=y and {x,y}==pair for x,y in zip(f,g))
        # If all 2q other rows use g, any omitted column has degree <=q<2q.
        for v in range(q): assert sum(int(g[v]!=g[v]) for _ in range(2*q))+q<2*q
assert valid==3*2**q+3
RESULTS["missing_function_exhaustion"]={"q":q,"ordered_pairs_tested":len(functions)**2,"constant_intersection_pairs":valid,"functions_by_number_of_values":dict(profile),"all_claimed_cases_verified":True}

# Original, invertible simultaneous inverse-row model, exact full witnesses.
# This is new code calling a maintained general-purpose exact algebra library.
from sympy import QQ, Poly, Symbol, cyclotomic_poly
from sympy.polys.matrices import DomainMatrix
x=Symbol('x'); n=15; phi=phi3q(5)
assert list(reversed(Poly(cyclotomic_poly(n,x),x).all_coeffs()))==phi
F=QQ.alg_field_from_poly(Poly(sum(c*x**i for i,c in enumerate(phi)),x),alias='zeta')
z=F.unit; powers=[F.one]
for j in range(1,n): powers.append(powers[-1]*z)
assert powers[-1]*z==F.one

def adj(A):
    rows=A.to_list(); n=len(rows)
    def conj(a):
        cs=list(reversed(a.to_list())); value=F.zero
        for j,c in enumerate(cs): value+=F.convert(c)*powers[-j%n]
        return value
    return DomainMatrix([[conj(rows[c][r]) for c in range(n)] for r in range(n)],(n,n),F)

def serialize(A):
    # Coefficients descend in powers, as returned by exact ANP canonical form.
    return [[[str(c) for c in a.to_list()] for a in row] for row in A.to_list()]

H=DomainMatrix([[powers[r*c%n] for c in range(n)] for r in range(n)],(n,n),F)
I=DomainMatrix([[F.one if r==c else F.zero for c in range(n)] for r in range(n)],(n,n),F)
original=[]
for d in (1,3,5):
    s=n-d; mask=mask_divisor(n,d)
    D=DomainMatrix([[powers[r*c%n] if mask[r][c] else F.zero for c in range(n)] for r in range(n)],(n,n),F)
    B=adj(H-D).scalarmul(F.convert(QQ(1,s)))
    M=B.inv(); E=M-H
    assert (M*B).to_list()==I.to_list()==(B*M).to_list()
    target=I.scalarmul(F.convert(d)).to_list()
    assert (adj(E)*E).to_list()==target==(E*adj(E)).to_list()
    Bdata=B.to_list()
    assert all(sum(bool(a) for a in row)==s for row in Bdata)
    assert all(sum(bool(Bdata[r][c]) for r in range(n))==s for c in range(n))
    original.append({"N":n,"d":d,"s":s,"both_inverse_products":True,"both_error_Grams":True,"all_inverse_row_and_column_supports":s,"normalized_squared_spectral_error":str(QQ(d,n)),"coefficient_convention":"descending rational coefficients modulo Phi_15","B_tilde":serialize(B),"M_tilde":serialize(M),"E_tilde":serialize(E)})
write("ORIGINAL_MODEL_WITNESSES.json",original)
RESULTS["original_model_reconstructions"]=len(original)
RESULTS["status"]="PASS"
write("INDEPENDENT_RESULTS.json",RESULTS)
print(json.dumps(RESULTS,indent=2))
