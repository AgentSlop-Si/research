#!/usr/bin/env python3
"""Fresh exact controls for the 3q,2q endpoint; standard library only.
No historical script is imported or executed. All root tests use cyclotomic
remainders, and inverse witnesses use exact rational cyclotomic arithmetic.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def trim(a):
    a = list(a)
    while len(a)>1 and not a[-1]: a.pop()
    return a

def psub(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]-=x
    return trim(c)

def pmul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: c[i+j]+=x*y
    return trim(c)

def pdiv(a,b):
    a=trim(a); b=trim(b); assert any(b)
    c=[Q(0)]*max(1,len(a)-len(b)+1)
    while any(a) and len(a)>=len(b):
        k=len(a)-len(b); t=Q(a[-1])/b[-1]; c[k]+=t
        for j,y in enumerate(b): a[k+j]-=t*y
        a=trim(a)
    return trim(c), a

@lru_cache(None)
def cyclotomic(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            a,r=pdiv(a,cyclotomic(d)); assert not any(r)
    assert all(Q(x).denominator==1 for x in a)
    return tuple(int(x) for x in a)

class Field:
    def __init__(self,n):
        self.n=n; self.phi=cyclotomic(n); self.k=len(self.phi)-1
        self.zero=(0,)*self.k; self.one=(1,)+(0,)*(self.k-1)
        self.powers=[self.red([0]*e+[1]) for e in range(n)]
    def red(self,a):
        a=list(a)+[0]*max(0,self.k-len(a))
        for i in range(len(a)-1,self.k-1,-1):
            t=a[i]
            if t:
                for j in range(self.k): a[i-self.k+j]-=t*self.phi[j]
        return tuple(a[:self.k])
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def sub(self,a,b): return tuple(x-y for x,y in zip(a,b))
    def scale(self,a,t): return tuple(x*t for x in a)
    def mul(self,a,b):
        if not any(a) or not any(b): return self.zero
        c=[0]*(2*self.k-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y: c[i+j]+=x*y
        return self.red(c)
    def inv(self,a):
        assert any(a)
        oldr=list(self.phi); r=trim(a)
        olds=[Q(0)]; s=[Q(1)]
        while any(r):
            q,newr=pdiv(oldr,r)
            oldr,r=r,newr; olds,s=s,psub(olds,pmul(q,s))
        assert len(oldr)==1 and oldr[0]
        ans=self.red([x/oldr[0] for x in olds])
        assert self.mul(a,ans)==self.one
        return ans
    def conj(self,a):
        c=self.zero
        for i,x in enumerate(a):
            if x: c=self.add(c,self.scale(self.powers[-i%self.n],x))
        return c
    def sum_powers(self, exponents):
        c=[0]*self.k
        for e in exponents:
            for i,x in enumerate(self.powers[e%self.n]): c[i]+=x
        return tuple(c)
    def star(self,A):
        return [[self.conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
    def product(self,A,B):
        BT=list(zip(*B)); C=[]
        for row in A:
            out=[]
            for col in BT:
                z=self.zero
                for a,b in zip(row,col):
                    if any(a) and any(b): z=self.add(z,self.mul(a,b))
                out.append(z)
            C.append(out)
        return C
    def inverse(self,A):
        n=len(A); W=[list(A[i])+[self.one if i==j else self.zero for j in range(n)] for i in range(n)]
        for j in range(n):
            pivot=next(i for i in range(j,n) if any(W[i][j]))
            W[j],W[pivot]=W[pivot],W[j]
            z=self.inv(W[j][j]); W[j]=[self.mul(a,z) for a in W[j]]
            for i in range(n):
                if i!=j and any(W[i][j]):
                    t=W[i][j]; W[i]=[self.sub(a,self.mul(t,b)) for a,b in zip(W[i],W[j])]
        for i in range(n):
            for j in range(n): assert W[i][j]==(self.one if i==j else self.zero)
        return [r[n:] for r in W]
    def diagonal(self,A,d):
        return all(A[i][j]==(self.scale(self.one,d) if i==j else self.zero) for i in range(len(A)) for j in range(len(A)))

def encode(a):
    if isinstance(a,(list,tuple)): return [encode(x) for x in a]
    a=Q(a)
    return int(a) if a.denominator==1 else str(a)

def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2)+"\n")

def divisor_mask(n,d):
    assert n%d==0
    m=n//d
    return [[int(r//d==c%m) for c in range(n)] for r in range(n)]

CONNECTED8=[
 [0,0,1,1,0,0,1,1], [0,1,0,1,0,1,0,1],
 [1,1,0,0,1,1,0,0], [1,0,1,0,1,0,1,0],
 [0,0,1,1,0,0,1,1], [1,0,1,0,1,0,1,0],
 [1,1,0,0,1,1,0,0], [0,1,0,1,0,1,0,1]]

def connected(R):
    n=len(R); seen={0}; stack=[0]
    while stack:
        x=stack.pop()
        adj=[n+j for j in range(n) if R[x][j]] if x<n else [i for i in range(n) if R[i][x-n]]
        for y in adj:
            if y not in seen: seen.add(y); stack.append(y)
    return len(seen)==2*n

COUNTS={"row_gram_entries":0,"column_gram_entries":0,"inverse_product_entries":0,"error_gram_entries":0}

def grams(R,d):
    n=len(R); F=Field(n)
    rows=[sum(x) for x in R]; cols=[sum(R[r][c] for r in range(n)) for c in range(n)]
    assert rows==[d]*n and cols==[d]*n
    rowbad=[]; colbad=[]; zeros={"row":{},"column":{}}
    for order,bad in [("row",rowbad),("column",colbad)]:
        for i in range(n):
            for j in range(n):
                COUNTS[order+"_gram_entries"]+=1
                exps=[(i-j)*c for c in range(n) if R[i][c] and R[j][c]] if order=="row" else [r*(j-i) for r in range(n) if R[r][i] and R[r][j]]
                value=F.sum_powers(exps)
                expected=F.scale(F.one,d) if i==j else F.zero
                if value!=expected:
                    bad.append({"indices":[i,j],"difference_character_order":n//gcd(i-j,n),"residue":encode(value),"squared_modulus":encode(F.mul(value,F.conj(value)))})
                elif i!=j:
                    h=str(n//gcd(i-j,n)); zeros[order][h]=zeros[order].get(h,0)+1
    return {"n":n,"d":d,"R":R,"cyclotomic_polynomial":list(F.phi),"regular_degrees":True,"row_failures":rowbad,"column_failures":colbad,"offdiagonal_zeros_by_character_order":zeros}

def inverse_control(R,d,label):
    n=len(R); F=Field(n)
    H=[[F.powers[r*c%n] for c in range(n)] for r in range(n)]
    A=[[F.zero if R[r][c] else H[r][c] for c in range(n)] for r in range(n)]
    B=[[F.scale(x,Q(1,n-d)) for x in row] for row in F.star(A)]
    M=F.inverse(B)
    for left,right in [(M,B),(B,M)]:
        assert F.diagonal(F.product(left,right),1)
        COUNTS["inverse_product_entries"]+=n*n
    br=[sum(bool(any(x)) for x in row) for row in B]
    bc=[sum(bool(any(B[r][c])) for r in range(n)) for c in range(n)]
    assert br==bc==[n-d]*n
    E=[[F.sub(M[r][c],H[r][c]) for c in range(n)] for r in range(n)]
    Estar=F.star(E)
    for left,right in [(E,Estar),(Estar,E)]:
        assert F.diagonal(F.product(left,right),d)
        COUNTS["error_gram_entries"]+=n*n
    print("inverse witness passed",label,flush=True)
    return {"label":label,"n":n,"d":d,"inverse_support_budget":n-d,"cyclotomic_polynomial":list(F.phi),"coefficient_encoding":"Each entry is the coefficient list in 1,z,...,z^(phi(n)-1); rational coefficients use numerator/denominator strings.","R":R,"B_tilde":encode(B),"M_tilde":encode(M),"E_tilde":encode(E),"both_inverse_products":True,"both_error_grams_equal_dI":True,"all_inverse_row_column_supports":br,"normalized_squared_spectral_error":str(Q(d,n))}

def local_checks():
    out=[]
    for q in [5,7,11]:
        tested=accepted=0; maximum=0
        for v in combinations_with_replacement(range(8),q):
            tested+=1
            if all((v[i]&v[j]).bit_count()==1 for i in range(q) for j in range(i)):
                accepted+=1; total=sum(x.bit_count() for x in v); maximum=max(maximum,total)
                assert total<=q+2
                assert any(x.bit_count()==1 for x in v)
                base=next(x for x in v if x.bit_count()==1)
                assert all(x&base==base for x in v)
        out.append({"q":q,"multisets_tested":tested,"pairwise_dot_one_multisets":accepted,"maximum_total_weight":maximum,"bound":q+2})
    # Check the exact binary vanishing lemma at order 15 in the ORIGINAL exponent indices.
    n=15; F=Field(n); zero_count=0
    for mask in range(1<<n):
        supp=[c for c in range(n) if mask>>c&1]
        if F.sum_powers(supp)!=F.zero: continue
        zero_count+=1
        full_three_fibers=all(len([c for c in supp if c%5==v]) in [0,3] for v in range(5))
        full_five_lines=all(len([c for c in supp if c%3==u]) in [0,5] for u in range(3))
        assert full_three_fibers or full_five_lines
    assert zero_count==(1<<5)+(1<<3)-2
    # Pointwise support-intersection rigidity used in the analytic proof.
    q=5; funcs=list(product(range(3),repeat=q)); valid=nonconstant=0
    for f in funcs:
        for g in funcs:
            intersections=[({0,1,2}-{f[v]})&({0,1,2}-{g[v]}) for v in range(q)]
            if not all(x==intersections[0] for x in intersections): continue
            valid+=1
            if len(set(f))==1:
                assert len(set(g))==1
            else:
                nonconstant+=1; assert len(set(f))==2 and len(intersections[0])==1
                t=next(iter(intersections[0])); assert set(f)==({0,1,2}-{t})
                assert all({f[v],g[v],t}=={0,1,2} for v in range(q))
    assert valid==3*(1<<q)+3 and nonconstant==3*((1<<q)-2)
    return {"local_dot_one":out,"primitive_binary_order15":{"supports_tested":1<<n,"zero_sums":zero_count},"missing_function_rigidity_q5":{"ordered_function_pairs_tested":len(funcs)**2,"fixed_intersection_pairs":valid,"nonconstant_first_function_pairs":nonconstant}}

def main():
    positive=[]
    for q in [5,7,11]:
        for d in [1,3,q,3*q]:
            z=grams(divisor_mask(3*q,d),d)
            assert not z["row_failures"] and not z["column_failures"]
            z["label"]="divisor"; positive.append(z)
    z=grams(CONNECTED8,4); assert not z["row_failures"] and not z["column_failures"] and connected(CONNECTED8)
    z["label"]="retained connected order-eight"; z["support_connected"]=True; positive.append(z)
    R24=[[CONNECTED8[(pow(3,-1,8)*(r%8))%8][c%8] for c in range(24)] for r in range(24)]
    z=grams(R24,12); assert not z["row_failures"] and not z["column_failures"] and connected(R24)
    z["label"]="retained connected odd CRT lift"; z["support_connected"]=True; positive.append(z)
    negative=[]
    for q in [5,7,11,13]:
        n=3*q; d=2*q
        R=[[int(r%3!=c%3) for c in range(n)] for r in range(n)]
        z=grams(R,d)
        for name in ["row_failures","column_failures"]:
            assert len(z[name])==6*q
            assert all(t["difference_character_order"]==3 and t["squared_modulus"]==encode(Field(n).scale(Field(n).one,q*q)) for t in z[name])
        for order in ["row","column"]:
            assert z["offdiagonal_zeros_by_character_order"][order]=={"%d"%n:6*q*(q-1),"%d"%q:3*q*(q-1)}
        z["label"]="endpoint regular near-mask: every non-order-three off-diagonal Gram vanishes"
        negative.append(z)
    # A degree-preserving corruption of an actual positive original-phase mask.
    R=divisor_mask(15,3)
    candidates=[]
    for r in range(15):
        for s in range(r+1,15):
            for c in range(15):
                for t in range(c+1,15):
                    if R[r][c]==R[s][t]==1 and R[r][t]==R[s][c]==0:
                        candidates.append((r,s,c,t))
    r,s,c,t=candidates[0]
    for i,j in [(r,c),(s,t),(r,t),(s,c)]: R[i][j]^=1
    z=grams(R,3); assert z["row_failures"] and z["column_failures"]
    z["label"]="degree-preserving corruption"; z["switched_rows_columns"]=[r,s,c,t]; negative.append(z)
    write("POSITIVE_CONTROLS.json",positive); write("NEGATIVE_CONTROLS.json",negative)
    local=local_checks(); write("LOCAL_CONTROLS.json",local)
    inverses=[]
    for n,d in [(15,1),(15,3),(15,5),(21,3),(21,7)]:
        inverses.append(inverse_control(divisor_mask(n,d),d,"divisor %d,%d"%(n,d)))
    inverses.append(inverse_control(CONNECTED8,4,"connected 8,4"))
    write("ORIGINAL_MODEL_CONTROLS.json",inverses)
    result={"status":"PASS","arithmetic":"exact rational/integer cyclotomic reduction; no numerical tolerances","positive_masks":len(positive),"endpoint_near_masks":4,"degree_preserving_corruptions":1,"original_model_inverse_witnesses":len(inverses),"counts":COUNTS,"local_controls":local,"historical_code_imported_or_executed":False,"external_writes":False,"no_full_endpoint_mask_census":True}
    write("RESULTS.json",result); print(json.dumps(result,indent=2),flush=True)

if __name__=="__main__": main()
