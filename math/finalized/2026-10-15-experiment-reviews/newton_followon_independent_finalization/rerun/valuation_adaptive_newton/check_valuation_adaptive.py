#!/usr/bin/env python3
"""Fresh exact reference and paid-operation ledger, standard library only.
No inherited producer is imported. Scalar Python multiplication is an explicitly
charged model leaf; oracle full products are confined to checks. This is not a
fast multiplication implementation or a timing/bit-complexity certificate.
"""
from fractions import Fraction
from math import comb, factorial, prod, log
from random import Random
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
RNG=Random(202610151826)
BETA=0.998327339802923082

def v2(x):
    x=abs(x)
    assert x
    return (x & -x).bit_length()-1

def capacity(x): return abs(x).bit_length()

def decode(x,radices,ledger=None):
    a=[]
    for b in radices:
        if ledger is not None:
            ledger['conversion_division_width_pairs'].append([capacity(x),capacity(b)])
        x,d=divmod(x,b); a.append(d)
    assert x==0
    return a

def encode(a,radices):
    z=0
    for j in range(len(a)-1,-1,-1): z=a[j]+radices[j]*z
    return z

def sampled(a,radices,t,ledger):
    # e_j(-b_t)=0 for j>t; this triangular zero is used, not only logged.
    z=0
    for j in range(min(len(a),t+1)-1,-1,-1):
        c=radices[j]-radices[t]
        ledger['evaluation_multiplication_width_pairs'].append([capacity(z),capacity(c)])
        z=a[j]+c*z
    return z

def ledger_new():
    return {'conversion_division_width_pairs':[],
            'evaluation_multiplication_width_pairs':[],
            'native_full_product_child_capacities':[],
            'sample_product_details':[], 'constant_modular_multiplication_bits':[],
            'odd_inverse_modulus_bits':[], 'prepared_fraction_count':0,
            'prepared_product_factor_count':0, 'skipped_sample_count':0,
            'outer_pair_count':0,'skipped_outer_pair_count':0}

def prefix_size(radices,k):
    d=len(radices); nu=0
    for j in range(1,d):
        nu+=v2(radices[j-1])
        if nu>=k:return j
    return d

def lagrange_weights(radices,J,ledger):
    out=[]
    for t in range(J):
        n=prod(radices[u] for u in range(J) if u!=t)
        den=prod(radices[u]-radices[t] for u in range(J) if u!=t)
        assert den
        out.append(Fraction(n,den))
    ledger['prepared_fraction_count']+=J
    ledger['prepared_product_factor_count']+=2*J*(J-1)
    return out

def scalar_product_mod(a,b,q,ledger,tag):
    assert q>0
    mask=(1<<q)-1
    aa=abs(a)&mask; bb=abs(b)&mask
    wa,wb=capacity(aa),capacity(bb)
    if aa and bb:
        ledger['native_full_product_child_capacities'].append(wa+wb)
    ledger['sample_product_details'].append({**tag,'requested_sample_bits':q,
        'exact_operand_bits':[capacity(a),capacity(b)],
        'truncated_magnitude_operand_bits':[wa,wb],
        'exact_operand_valuations':[v2(a) if a else None,v2(b) if b else None]})
    out=aa*bb                         # charged ordinary scalar leaf
    if (a<0)!=(b<0):out=-out
    return out&mask

def low_digits(a,b,radices,k,ledger):
    if k<=0:return 0
    J=prefix_size(radices,k)
    ls=lagrange_weights(radices,J,ledger)
    vals=[v2(z.numerator)-v2(z.denominator) for z in ls]
    h=max([0]+[-z for z in vals])
    modulus=1<<(k+h); acc=0
    for t,(L,lam) in enumerate(zip(ls,vals)):
        q=k-lam
        if q<=0:
            ledger['skipped_sample_count']+=1;continue
        A=sampled(a,radices,t,ledger);B=sampled(b,radices,t,ledger)
        f=scalar_product_mod(A,B,q,ledger,{'node':t,'retained_nodes':J,'weight_valuation':lam})
        nn=L.numerator//(1<<v2(L.numerator))
        dd=L.denominator//(1<<v2(L.denominator))
        assert dd&1
        ledger['odd_inverse_modulus_bits'].append(q)
        unit=(nn*pow(dd,-1,1<<q))% (1<<q)
        ledger['constant_modular_multiplication_bits'].extend([q,q])
        acc=(acc+((unit*f)%(1<<q) << (lam+h)))%modulus
    assert acc%(1<<h)==0
    return acc>>h

def low_binary(X,Y,radices,r,k,ledger):
    a=decode(X,radices[:r],ledger);b=decode(Y,radices[:r],ledger)
    return low_digits(a,b,radices,k,ledger)

def low_outer(X,Y,radices,r,LA,LB,k,ledger):
    first=radices[:r]; Q=prod(first);nu=v2(Q)
    A=decode(X,first*LA,ledger); B=decode(Y,first*LB,ledger)
    out=0; modulus=1<<k
    for i in range(LA):
        for j in range(LB):
            q=k-(i+j)*nu
            if q<=0:
                ledger['skipped_outer_pair_count']+=1;continue
            ledger['outer_pair_count']+=1
            R=low_digits(A[i*r:(i+1)*r],B[j*r:(j+1)*r],radices,q,ledger)
            # Exact periodic boundary specialization is explicit Q^(i+j).
            W=pow(Q,i+j,modulus)
            ledger['constant_modular_multiplication_bits'].append(k)
            out=(out+W*R)%modulus
    return out

def high_reconstruct(X,Y,N,a,R):
    t=a+1;k=2*N-a
    x=X>>(N-t);y=Y>>(N-t)
    V=x*y                         # separately charged prefix leaf G(t)
    H=V>>(2*t-a)
    z=((X%3)*(Y%3))%3             # two original-input scans + fixed-size product
    delta=((z-R-pow(2,k,3)*H)*pow(pow(2,k,3),-1,3))%3
    assert delta in (0,1)
    return R+(1<<k)*(H+delta),H,delta,2*t

counts={}; total=0; guards=0; pruned=0; inverses=0
# Exhaustive small genuine input products, including nonintegral Lagrange weights.
for r,radices in [(2,[3,4,5]),(2,[3,7,11]),(2,[4,6,8]),(2,[2,6,10])]:
    Q=prod(radices[:r])
    for X in range(Q):
      for Y in range(Q):
       for k in (1,3,Q.bit_length(),2*Q.bit_length()):
        L=ledger_new();R=low_binary(X,Y,radices,r,k,L)
        assert R==(X*Y)% (1<<k)
        total+=1
counts['exhaustive_small_low_products']=total

# Arithmetic progressions: odd g, shared valuation, and mismatched valuations.
case_count=0
for r in range(2,11):
  for p,g in [(3,1),(7,3),(31,1),(14,6),(16,16),(24,8),(7,4),(9,8)]:
    rad=[p+g*j for j in range(2*r-1)];Q=prod(rad[:r]);N=Q.bit_length()
    for _ in range(12):
      X=RNG.randrange(Q);Y=RNG.randrange(Q);k=RNG.randrange(1,2*N+1)
      L=ledger_new();R=low_binary(X,Y,rad,r,k,L)
      assert R==X*Y%(1<<k)
      vals=[d['weight_valuation'] for d in L['sample_product_details']]
      guards+=any(v<0 for v in vals)
      if p%(1<<v2(g))==0:assert all(v>=0 for v in vals)
      J=prefix_size(rad,k);pruned+=J<len(rad)
      inverses+=len(L['odd_inverse_modulus_bits']);case_count+=1
counts['arithmetic_progression_low_products']=case_count

# Fully adaptive, non-arithmetic radices; all finite 2-adic guards are retained.
case_count=0
for r in range(2,9):
  for _ in range(60):
    rad=RNG.sample(range(2,160),2*r-1);Q=prod(rad[:r]);N=Q.bit_length()
    X=RNG.randrange(Q);Y=RNG.randrange(Q);k=RNG.randrange(1,2*N+1)
    L=ledger_new();R=low_binary(X,Y,rad,r,k,L)
    assert R==X*Y%(1<<k)
    guards+=any(x['weight_valuation']<0 for x in L['sample_product_details'])
    pruned+=prefix_size(rad,k)<len(rad);case_count+=1
counts['arbitrary_adaptive_low_products']=case_count

# Full exact-low/high/checksum contract and periodic outer blocks.
case_count=0; outer_omitted=0;outer_rows=[]
for r in range(2,7):
  for p,g in [(7,1),(8,8),(9,4)]:
    rad=[p+g*j for j in range(2*r-1)];Q=prod(rad[:r])
    for LA,LB in [(1,1),(2,3),(4,4)]:
      cap=max(Q**LA,Q**LB);N=cap.bit_length()
      for _ in range(12):
        X=RNG.randrange(Q**LA);Y=RNG.randrange(Q**LB)
        a=RNG.randrange(1,N); k=2*N-a; L=ledger_new()
        R=low_outer(X,Y,rad,r,LA,LB,k,L)
        full,H,delta,hchild=high_reconstruct(X,Y,N,a,R)
        assert R==X*Y%(1<<k) and full==X*Y
        outdigits=decode(full,rad[:r]*(LA+LB),L)
        assert all(0<=z<rad[j%r] for j,z in enumerate(outdigits))
        assert encode(outdigits,rad[:r]*(LA+LB))==full
        assert H<=X*Y//(1<<k)<=H+1
        outer_omitted+=L['skipped_outer_pair_count'];case_count+=1
      if r==6:outer_rows.append({'r':r,'p':p,'g':g,'LA':LA,'LB':LB,
          'outer_pair_count':L['outer_pair_count'],
          'skipped_outer_pairs':L['skipped_outer_pair_count'],
          'point_children':len(L['native_full_product_child_capacities'])})
counts['complete_periodic_low_high_checksum_products']=case_count
counts['periodic_outer_pairs_actually_skipped']=outer_omitted

# For a=p-adic target and consecutive integer nodes, the Lagrange coefficients
# are 2-adic integral, not just the Newton/binomial coefficients.
integ=0
for J in range(1,32):
 for p in range(1,20):
  for g in (1,3,5,7):
    L=lagrange_weights([p+g*j for j in range(J)],J,ledger_new())
    assert all(v2(z.numerator)>=v2(z.denominator) for z in L)
    integ+=len(L)
counts['odd_step_integral_scalar_weights']=integ

# Exact odd-step valuation and full-child family, no huge product outputs saved.
odd_rows=[]
for r in (4,8,16,32,64):
    m=r*(r.bit_length()-1)**2;p=(1<<m)-1
    rad=[p+j for j in range(2*r-1)];E=[prod(rad[:j]) for j in range(2*r)]
    Q=E[r];N=Q.bit_length();a=[0]*r;a[0]=p-2;a[-1]=1
    X=encode(a,rad);k=N;L=ledger_new()
    weights=lagrange_weights(rad,len(rad),L)
    ls=[v2(z.numerator)-v2(z.denominator) for z in weights]
    ws=[capacity(sampled(a,rad,t,L)) for t in range(len(rad))]
    assert all(v2(sampled(a,rad,t,L))==0 for t in range(len(rad)))
    assert all(k-l>=2*w for l,w in zip(ls,ws))
    assert prefix_size(rad,k)==len(rad)
    assert all(v2(E[j])==m+v2(factorial(j-2)) for j in range(2,len(E)))
    native=[2*w for w in ws];parent=2*N
    odd_rows.append({'r':r,'m':m,'input_capacity_bits':N,'actual_input_bits':capacity(X),
        'low_bits':k,'retained_nodes':len(ws),'max_scalar_weight_valuation':max(ls),
        'min_remaining_sample_precision':min(k-l for l in ls),
        'min_sample_operand_bits':min(ws),'max_sample_operand_bits':max(ws),
        'native_children':native,'all_products_full':True,
        'native_width_ratio_to_ordinary_root_wrapper':sum(native)/parent,
        'optimistic_wrapper_beta_ratio':sum(s*log(s)**BETA for s in native)/(parent*log(parent)**BETA)})

scaled_rows=[]
for r in (4,8,16,32):
    s=4*r*r;g=1<<s;rad=[g*(j+1) for j in range(2*r-1)]
    Q=prod(rad[:r]);N=Q.bit_length();a=[b-1 for b in rad[:r]]
    assert encode(a,rad)==Q-1
    for cut_kind,k in [('input_capacity',N),('smallest_prefix_high_cut',N+1),('quarter_prefix_high_cut',2*N-N//4)]:
      J=prefix_size(rad,k); L=ledger_new()
      weights=lagrange_weights(rad,J,L)
      assert weights==[Fraction((-1)**t*comb(J,t+1)) for t in range(J)]
      ls=[v2(z.numerator) for z in weights]
      samples=[sampled(a,rad,t,L) for t in range(J)]
      ws=[capacity(z) for z in samples]
      assert all(v2(z)==0 for z in samples)
      if k<=N+1:assert J==r+1 and J<2*r-1
      # Actual truncated magnitude widths, never just a capacity upper bound.
      children=[2*capacity(abs(z)% (1<<(k-l))) for z,l in zip(samples,ls)]
      assert max(children)>=N
      scaled_rows.append({'r':r,'s':s,'input_bits':N,'low_bits':k,'cut_kind':cut_kind,
         'full_source_nodes':2*r-1,'retained_nodes':J,'pruned_nodes':2*r-1-J,
         'basis_period_valuation':r*s+v2(factorial(r)),
         'sample_operand_bits':ws,'scalar_weight_valuations':ls,
         'remaining_sample_precision':[k-l for l in ls],
         'native_children':children,'native_child_width_sum_over_N':sum(children)/N,
         'largest_child_over_N':max(children)/N,'shrinking_native_recursion':False})

# Strictly increasing valuation adaptive-node formula, with non-power-of-two odd parts.
increasing=0
for J in range(2,13):
 for _ in range(15):
    ss=sorted(RNG.sample(range(1,30),J))
    rad=[(1<<s)*RNG.choice([3,5,7,9]) for s in ss]
    weights=lagrange_weights(rad,J,ledger_new())
    for t,L in enumerate(weights):
      lam=v2(L.numerator)-v2(L.denominator)
      assert lam==sum(ss[u]-ss[t] for u in range(t+1,J))
      increasing+=1
    assert v2(weights[-1].numerator)==v2(weights[-1].denominator)
counts['strictly_increasing_valuation_weights']=increasing

# A concrete nonunit denominator alias, and a genuinely reduced low producer.
rad=[3,7,11]; a=[0,1]
# Here x-source=-4t, original p=3, A(x)=x, so shift-basis digits [0,1].
# e_1(x-shift)=x-shift+3; sampled A=-4t; all samples squared vanish mod16,
# while X=3 has odd square. The generic guard detects rather than hides it.
rad=[3,7,11]
assert [sampled(a,rad,t,ledger_new()) for t in range(3)]==[0,-4,-8]
assert all(sampled(a,rad,t,ledger_new())**2%16==0 for t in range(3))
assert encode(a,rad)**2%2==1
fixtureL=ledger_new();fixtureR=low_digits(a,a,rad,1,fixtureL)
assert fixtureR==1
fixture={'radices':rad,'digits':a,'input':3,'sample_products_mod16':[0,0,0],
         'true_low_bit':1,'charged_required_sample_bits':[x['requested_sample_bits'] for x in fixtureL['sample_product_details']],
         'weight_valuations':[x['weight_valuation'] for x in fixtureL['sample_product_details']]}

# Every binary length tested with canonical conversion, including tiny-size control.
allsize=0
for N in range(2,130):
    r=max(2,int(N**0.5));m=(N+r-1)//r+1;p=(1<<m)-1
    rad=[p+j for j in range(2*r-1)];assert prod(rad[:r])>=1<<N
    for _ in range(4):
        X=RNG.randrange(1<<N);Y=RNG.randrange(1<<N)
        a=max(1,N//4);k=2*N-a;L=ledger_new()
        R=low_binary(X,Y,rad,r,k,L)
        full,_,_,_=high_reconstruct(X,Y,N,a,R)
        assert full==X*Y
        allsize+=1
counts['arbitrary_binary_length_low_high_controls']=allsize
counts['tests_with_actual_negative_weight_guard']=guards
counts['tests_with_actual_newton_tail_pruning']=pruned

result={'status':'PASS','scope':'Fresh exact finite controls and scalar child ledgers; no fast multiplier or universal lower bound.',
        'counts':counts,'odd_step_adverse_family':odd_rows,
        'scaled_progression_genuine_pruning':scaled_rows,
        'periodic_outer_rows':outer_rows,'nonunit_guard_fixture':fixture,
        'asymptotic_optimistic_odd_step_beta_ratio':2**(1-BETA)}
(ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'ODD_STEP_CHILD_LEDGER.json').write_text(json.dumps(odd_rows,indent=2)+'\n')
(ROOT/'SCALED_CHILD_LEDGER.json').write_text(json.dumps(scaled_rows,indent=2)+'\n')
print(json.dumps({'status':result['status'],'counts':counts,
                 'odd_step_ratio_limit':result['asymptotic_optimistic_odd_step_beta_ratio']},indent=2))
