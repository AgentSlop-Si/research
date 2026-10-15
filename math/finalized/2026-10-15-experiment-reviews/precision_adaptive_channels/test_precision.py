"""Independent integer oracle tests; Python products are permitted only here."""
import json, math, random
from pathlib import Path
from producer import adaptive_low, even_guarded_low, Arithmetic, v2, factorial_v2

OUT=Path(__file__).parent
rng=random.Random(202610151831)

def coeff(a,b,g):
    r=len(a); out=[0]*(2*r-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            for h in range(min(i,j)+1):
                out[i+j-h]+=x*y*(-g)**h*math.comb(i,h)*math.comb(j,h)*math.factorial(h)
    return out

def value(a,p,g):
    z=0
    for j in range(len(a)-1,-1,-1):z=(p+g*j)*z+a[j]
    return z

results={'seed':202610151831}
# Elementary arithmetic and signed Euclidean semantics.
ar=Arithmetic(); basic=0
for _ in range(500):
    a=rng.randrange(-10**5,10**5); b=rng.randrange(1,1000)
    assert ar.mul(a,b)==a*b
    assert ar.divmod(a,b)==divmod(a,b)
    basic+=2
results['elementary_comparisons']=basic
rows=[]; cases=coeffcases=boundcases=0
for p,g,r in [(3,1,2),(7,4,2),(3,4,3),(7,2,4),(15,4,4),(7,1,5),(7,4,8),(2,17,2),(2,97,3),(257,4,5),(3,1000,4)]:
    Q=math.prod(p+g*j for j in range(r))
    pairs=[(0,0),(Q-1,Q-1),(math.prod(p+g*j for j in range(r-1)),)*2]
    pairs += [(rng.randrange(Q),rng.randrange(Q)) for _ in range(4)]
    for x,y in pairs:
        k=rng.choice([1,max(1,Q.bit_length()//2),Q.bit_length(),2*Q.bit_length()])
        z,ledger=adaptive_low(x,y,p,g,r,k)
        assert z==(x*y)%(1<<k)
        a,b=ledger['input_digits']
        expected=coeff(a,b,g)
        assert ledger['coefficients']==expected
        for D,h in zip(expected,ledger['bounds']):
            assert abs(D)<1<<h
            boundcases+=1
        for row in ledger['rounds']:
            q,omega=row['q'],row['root']; L=ledger['L']
            assert all(q%d for d in range(2,math.isqrt(q)+1))
            assert (q-1)%L==0 and g%q
            assert pow(omega,L,q)==1 and pow(omega,L//2,q)==q-1
        coeffcases+=len(expected); cases+=1
        if x==Q-1 and y==Q-1:
            rows.append(dict(p=p,g=g,r=r,input_bits=Q.bit_length(),k=k,
                             low=z,bounds=ledger['bounds'],
                             stopped_modulus_bits=ledger['stopped_modulus_bits'],
                             global_bits=ledger['final_global_modulus_bits'],
                             adaptive_crt_bit_slots=sum(ledger['stopped_modulus_bits']),
                             uniform_crt_bit_slots=(2*r-1)*ledger['final_global_modulus_bits'],
                             rounds=ledger['rounds'],counts=ledger['counts'],
                             native_wrapper_capacities=ledger['native_wrapper_capacities']))
for row in rows:
    native_n=2*row['input_bits']
    hist=row['native_wrapper_capacities']
    beta=0.998327339802923082
    row['parent_native_capacity']=native_n
    row['max_actual_native_child']=max(hist,default=0)
    row['actual_native_beta_potential']=sum(count*width*math.log2(width)**beta for width,count in hist.items() if width>1)/(native_n*math.log2(native_n)**beta)
results.update(adaptive_products=cases,coefficient_comparisons=coeffcases,
               bound_checks=boundcases,representative_ledgers=rows)
# Full ordinary output with k at least n_A+n_B, across roots and signed coefficients.
full=0
for p,g,r in [(3,2,3),(7,4,4),(7,1,5)]:
    Q=math.prod(p+g*j for j in range(r))
    for _ in range(5):
        x=rng.randrange(Q);y=rng.randrange(Q)
        z,_=adaptive_low(x,y,p,g,r,max(1,x.bit_length()+y.bit_length()))
        assert z==x*y;full+=1
results['full_products']=full
# Even-step Lagrange guarded functional, independent direct integer reference.
guarded=0; alias=0; erows=[]
for r in range(2,9):
    for g in (2,4,12):
        p=7
        for _ in range(4):
            a=[rng.randrange(p+g*j) for j in range(r)]
            b=[rng.randrange(p+g*j) for j in range(r)]
            k=rng.choice([1,7,19,37])
            z,ld=even_guarded_low(a,b,p,g,k)
            assert z==(value(a,p,g)*value(b,p,g))%(1<<k)
            s=2*r-2
            for row in ld['rows']:
                t=row['sample']
                assert row['precision']==k+ld['Lambda']-v2(math.comb(s,t))
            guarded+=1
        h=r-1; guard=2*(h*v2(g)+factorial_v2(h))
        E=math.prod(p+g*j for j in range(h))
        assert E*E&1
        for t in range(2*r-1):
            sample=math.prod(-g*t+g*j for j in range(h))**2
            assert sample%(1<<guard)==0
        assert (g**h*math.factorial(h))**2%(1<<(guard+1)) != 0
        alias+=1
        if g==4:erows.append(dict(r=r,necessary_common_precision_at_least=guard+1,
                                  sufficient_bit_zero_precision=1+ld['Lambda'],
                                  guard_gap=ld['Lambda']-guard))
results.update(even_guarded_products=guarded,reachable_aliases=alias,even_guard_rows=erows)
# Wrong odd-CRT low decoder: reachable constant-digit alias, for same producer.
q_product=17*97
p=2047;g=4;r=2
assert q_product<p
x1=q_product; x0=0;y=1
for q in [17,97]:
    for t in range(2*r-1):
        assert (x1*y)%q==(x0*y)%q
assert (x1*y)&1 != (x0*y)&1
results['odd_crt_transcript_alias']={'p':p,'g':g,'r':r,'prime_product':q_product,
                                     'primes':[17,97],'different_low_bit':True}
# Binary central-binomial guard gap and exact tent width sum.
struct=[]
for r in (2,4,8,16,32,64,128):
    h=r-1;s=2*h
    gap=factorial_v2(s)-2*factorial_v2(h)
    assert gap==h.bit_count()
    assert sum(min(j,2*r-2-j) for j in range(2*r-1))==(r-1)**2
    struct.append({'r':r,'guard_gap':gap,'max_binomial_valuation':max(v2(math.comb(s,t)) for t in range(s+1))})
results['structural_rows']=struct
(OUT/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if not isinstance(v,list)},indent=2))
print('ALL TESTS PASS')
