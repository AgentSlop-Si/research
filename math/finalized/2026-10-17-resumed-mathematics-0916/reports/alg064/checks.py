#!/usr/bin/env python3
"""New controls for the new reference_pipeline, never historical code."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import reference_pipeline as R

OUT=Path(__file__).with_name('CHECK_RESULTS.json')
def encode(x):
    if isinstance(x,F): return {'numerator':x.numerator,'denominator':x.denominator}
    raise TypeError(type(x).__name__)

def brute_one(x):
    if all(a==R.ZERO for a in x): return True
    # Independent cap-one oracle using all adjacent cross products and zero guards.
    first=next((j for j in range(1,len(x)) if x[j-1]!=R.ZERO),None)
    if first is None: return all(a==R.ZERO for a in x[1:])
    for j in range(1,len(x)):
        if R.mul(x[j],x[first-1])!=R.mul(x[first],x[j-1]): return False
    return True

def oracle(x,eps,p):
    # Exact power-sum formulation at tighter certified nodes, no pipeline Horner.
    tt,rc=R.nodes(len(x),p+24)
    out=[]
    for t in tt:
        pw=R.ONE; total=R.ZERO
        for a in x:
            total=R.add(total,R.mul(a,pw)); pw=R.mul(pw,t)
        out.append(total)
    radius=3*len(x)*sum(map(R.nu,x),F(0))*F(1,1<<(p+24))
    assert radius<eps
    return out,radius

cases=[]
for n in (3,4,5,7,8,9,12,16,17,32):
    cases.extend([
        (f'constant_{n}',[R.z(2,-1)]*n,1),
        (f'alternating_{n}',[R.z((-1)**j) for j in range(n)],1),
        (f'rational_one_third_{n}',[R.z(3**(n-1-j)) for j in range(n)],1),
        (f'untapped_cap_{n}',[R.ONE]+[R.ZERO]*(n-1),min(2,n-1)),
        (f'late_impulse_{n}',[R.ONE]+[R.ZERO]*(n-2)+[R.ONE],1),
        (f'zero_{n}',[R.ZERO]*n,0),
        (f'cap_zero_nonzero_{n}',[R.ONE]+[R.ZERO]*(n-1),0),
    ])
    vals=[]; pw=R.ONE
    for j in range(n): vals.append(R.mul(R.z(3**(n-1-j)),pw)); pw=R.mul(pw,R.z(1,2))
    cases.append((f'gaussian_rational_{n}',vals,1))
    if n>=5:
        vals=[R.z(5**(n-1)*3**(n-1-j)+3**(n-1)*2**j*5**(n-1-j)) for j in range(n)]
        cases.append((f'two_nondyadic_modes_{n}',vals,2))
for n in (6,10,16):
    cases.append((f'repeated_root_{n}',[R.z(j) for j in range(n)],2))
    cases.append((f'late_startup_span_{n}',[R.ZERO,R.ONE]+[R.ZERO]*(n-2),3))
    cases.append((f'near_resonance_{n}',[R.z(F(257**j,256**j)) for j in range(n)],1))
for q in (8,24,60): cases.append((f'tiny_pivot_{q}',[R.z(F(1,1<<q)),R.ONE],1))
cases.extend([('N1_copy',[R.z(F(3,8),F(-1,16))],0),('N2_late_impulse',[R.ZERO,R.ONE],1)])

results=[]; vectors=[]; bins=0
for name,x,d in cases:
    eps=F(1,1<<10)
    yy,receipt=R.pipeline(x,d,eps)
    if receipt['branch'] in ('copy','zero'):
        assert yy==x if receipt['branch']=='copy' else all(v==R.ZERO for v in yy)
    else:
        ref,er=oracle(x,eps,receipt['p'])
        assert all(R.sq(R.sub(a,b))<=(eps-er)**2 for a,b in zip(yy,ref)),name
        bins+=len(x)
    results.append({'name':name,**receipt})
    vectors.append({'name':name,'raw_dyadic_input':x,'declared_cap':d,'epsilon':eps,'outputs':yy,'claimed_error_bound':receipt['certified_error'],'branch':receipt['branch']})

exhaustive=0
for n in range(2,7):
    for seq in product((-1,0,1),repeat=n):
        x=[R.z(a) for a in seq]
        c,_=R.discover(x,1)
        assert (c is not None)==brute_one(x),(seq,c)
        exhaustive+=1

negative=[]
for name,x,d,ep in [('non_dyadic',[R.z(F(1,3)),R.ONE],1,F(1,8)),('bad_cap_low',[R.ONE]*3,-1,F(1,8)),('bad_cap_high',[R.ONE]*3,3,F(1,8)),('bad_epsilon_zero',[R.ONE]*3,1,F(0)),('bad_epsilon_large',[R.ONE]*3,1,F(2)),('empty',[],0,F(1,8))]:
    try: R.pipeline(x,d,ep)
    except ValueError: negative.append(name)
    else: raise AssertionError(name)
# Coarsely rounded rational coefficients cannot silently enter the fast branch.
x=[R.z(27),R.z(9),R.z(3),R.ONE]; c,_=R.discover(x,1)
coarse=[R.ONE,R.rnd(c[1],1)]; _,r=R.boundary(x,coarse)
assert r>F(1,1<<10)*F(1,8)/8
negative.append('coarse_coefficient_defect_detected')
# A prefix-valid, last-row-invalid connection is rejected and gets certified fallback.
x=[R.ONE]+[R.ZERO]*6+[R.ONE]
y,rec=R.pipeline(x,1,F(1,1<<10),supplied_coefficients=[R.ONE,R.ZERO])
assert rec['branch']=='certified_direct_fallback' and rec['reason']=='supplied exact coefficient verification failed'
negative.append('late_tail_injected_connection_rejected')
# Invalid normalization never reaches numerical arithmetic.
try: R.pipeline(x,1,supplied_coefficients=[R.ZERO,R.ZERO])
except ValueError: negative.append('connection_constant_not_one_rejected')
else: raise AssertionError
# Sign and normalization are observable, never silently substituted.
x=[R.ZERO,R.ONE,R.ZERO,R.ZERO]
y,rec=R.pipeline(x,1,F(1,1<<10))
assert R.sq(R.sub(y[1],R.z(0,-1)))>1
assert R.sq(R.sub(y[0],R.z(F(1,2))))>F(1,8)
negative.extend(['negative_exponent_convention_detected','normalization_change_detected'])
# Coefficient height is unbounded as a dyadic pivot tends to zero.
c,_=R.discover([R.z(F(1,1<<60)),R.ONE],1)
assert c[1]==R.z(-(1<<60))
negative.append('tiny_pivot_precludes_uniform_conditioning_claim')

summary={'verdict':'PASS','scope':'Fresh exact-data reference integration, not historical-source integration or production speed.','pipeline_cases':len(results),'certified_output_checks':bins,'exhaustive_cap_one_decisions':exhaustive,'negative_controls':negative,'branches':{b:sum(x['branch']==b for x in results) for b in ('recurrence','certified_direct_fallback','zero','copy')},'nondyadic_coefficient_cases':sum(bool(x.get('non_dyadic_exact_coefficients')) for x in results),'suspect_bins':sum(len(x.get('suspect_bins',[])) for x in results),'max_working_fraction_bits':max(x.get('p',0) for x in results),'cases':results}
OUT.write_text(json.dumps(summary,indent=2,default=encode)+'\n')
OUT.with_name('OUTPUT_VECTORS.json').write_text(json.dumps(vectors,indent=2,default=encode)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))
