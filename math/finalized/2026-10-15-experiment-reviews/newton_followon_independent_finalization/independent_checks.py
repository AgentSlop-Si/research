"""Independent bounded controls. Reads source modules without rewriting sources."""
import ast, importlib.util, json, math, random, sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'rerun'

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);sys.modules[name]=out;spec.loader.exec_module(out);return out

bc=module('ind_block',SRC/'block_carried_newton_tree/producer.py')
pc=module('ind_precision',SRC/'precision_adaptive_channels/producer.py')
# The valuation file combines functions and tests. Extract definitions/imports
# rather than trigger its output-writing test body in the original directory.
path=SRC/'valuation_adaptive_newton/check_valuation_adaptive.py'
tree=ast.parse(path.read_text()); keep=[]
for node in tree.body:
    if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)):
        keep.append(node)
va={'__file__':str(path)};exec(compile(ast.Module(body=keep,type_ignores=[]),str(path),'exec'),va)
rng=random.Random(202610151904)
counts={}

# Re-derive capacity rather than reuse the claimed output inequality.
count=0
for r in range(1,20):
    bases=bc.bases_for(3,5,r);W=[1]
    for i in range(6*r+1):W.append(W[-1]*bases[i%r])
    for s in range(3*r+1):
      for t in range(3*r+1):
        assert W[s+t]>=W[s]*W[t];count+=1
counts['periodic_weight_capacity_inequalities']=count

# Unequal partitions, arbitrary period phase, zeros and leading-zero digits.
for _ in range(1000):
    r=rng.randrange(1,12);p=rng.randrange(3,40);g=rng.randrange(1,12)
    bases=bc.bases_for(p,g,r)
    a=[rng.randrange(bases[j%r]) for j in range(rng.randrange(1,4*r+1))]
    b=[rng.randrange(bases[j%r]) for j in range(rng.randrange(1,4*r+1))]
    cuts=sorted({0,len(a),*(rng.randrange(len(a)+1) for _ in range(6))})
    old=[0];capacity=len(a)+len(b)
    for lo,hi in reversed(list(zip(cuts,cuts[1:]))):
        desc=bc.describe(a,bases,lo,hi)
        use_shift=(hi-lo) if (hi-lo)%r==0 else None
        old=bc.apply_block(old,b,desc,bases,capacity,shift=use_shift)
    def direct(ds):
        out=0;w=1
        for j,d in enumerate(ds):out+=d*w;w*=bases[j%r]
        return out
    assert direct(old)==direct(a)*direct(b)
counts['unequal_block_partition_products']=1000

# Full-period symbolic cancellation at arbitrary phase, including multi-periods.
count=0
for r in range(1,13):
  bases=bc.bases_for(5,3,r)
  for lo in range(2*r):
    for h in (r,2*r):
      for i in (0,r-1,r,2*r+3):
        col={i:1}
        for j in range(lo,lo+h):
          new={}
          for k,c in col.items():
            new[k]=new.get(k,0)+(bases[j%r]-bases[k%r])*c
            new[k+1]=new.get(k+1,0)+c
          col={k:v for k,v in new.items() if v}
        assert col=={i+h:1};count+=1
counts['arbitrary_phase_symbolic_period_shifts']=count

# Arbitrary distinct adaptive radices, direct polynomial monomial coefficients,
# independent Fraction scalar projection, and the actual production low word.
count=0;skipped=guards=0
for _ in range(1200):
    r=rng.randrange(1,9);d=2*r-1;rad=rng.sample(range(2,300),d)
    A=[rng.randrange(rad[j]) for j in range(r)]
    B=[rng.randrange(rad[j]) for j in range(r)]
    X=va['encode'](A,rad);Y=va['encode'](B,rad)
    k=rng.randrange(1,max(2,X.bit_length()+Y.bit_length()+4))
    L=va['ledger_new']();z=va['low_digits'](A,B,rad,k,L)
    assert z==(X*Y)% (1<<k)
    J=va['prefix_size'](rad,k)
    # Independently reconstruct the truncated scalar interpolant over Q.
    value=Fraction(0)
    for t in range(J):
        def evalpoly(ds):
            term=1;out=0
            for j,a in enumerate(ds):
                out+=a*term;term*=rad[j]-rad[t]
            return out
        num=math.prod(rad[u] for u in range(J) if u!=t)
        den=math.prod(rad[u]-rad[t] for u in range(J) if u!=t)
        value+=Fraction(num,den)*evalpoly(A)*evalpoly(B)
    assert value.denominator==1 and (value.numerator-X*Y)%(1<<k)==0
    skipped+=L['skipped_sample_count'];guards+=any(x['weight_valuation']<0 for x in L['sample_product_details']);count+=1
counts.update(arbitrary_adaptive_independent_scalar_checks=count,skipped_scalar_samples=skipped,negative_guard_cases=guards)

# Guard-free shared valuation and increasing-valuation formulas.
count=0
for _ in range(500):
    J=rng.randrange(1,35);a=rng.randrange(0,10)
    p=(1<<a)*rng.randrange(1,100);g=(1<<a)*rng.choice(range(1,60,2))
    weights=va['lagrange_weights']([p+g*j for j in range(J)],J,va['ledger_new']())
    assert all(va['v2'](w.numerator)>=va['v2'](w.denominator) for w in weights)
    count+=len(weights)
counts['extra_integral_progression_weights']=count

# High quotient bound exhaustive over all inputs and all allowed cut positions.
count=0
for N in range(2,8):
  for a in range(1,N):
    k=2*N-a
    for X in range(1<<N):
      for Y in range(1<<N):
        out,H,delta,_=va['high_reconstruct'](X,Y,N,a,(X*Y)%(1<<k))
        assert out==X*Y and H<=X*Y//(1<<k)<=H+1;count+=1
counts['exhaustive_high_prefix_repair_checks']=count

# Reconstruct Newton coefficients from monomial products and triangular division.
def multiply_poly(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def newton_to_poly(a,g):
    out=[0]*len(a);basis=[1]
    for j,x in enumerate(a):
        for k,c in enumerate(basis):out[k]+=x*c
        basis=multiply_poly(basis,[g*j,1])
    return out

def poly_to_newton(poly,g):
    basis=[[1]]
    for j in range(1,len(poly)):basis.append(multiply_poly(basis[-1],[g*(j-1),1]))
    rem=list(poly);out=[0]*len(poly)
    for j in range(len(poly)-1,-1,-1):
        out[j]=rem[j]
        for k,c in enumerate(basis[j]):rem[k]-=out[j]*c
    assert not any(rem);return out
count=0
for _ in range(100):
    r=rng.randrange(2,9);p=rng.randrange(2,60);g=rng.randrange(1,50)
    Q=math.prod(p+g*j for j in range(r));X=rng.randrange(Q);Y=rng.randrange(Q)
    k=rng.randrange(1,2*Q.bit_length()+1)
    z,L=pc.adaptive_low(X,Y,p,g,r,k)
    a,b=L['input_digits']
    expected=poly_to_newton(multiply_poly(newton_to_poly(a,g),newton_to_poly(b,g)),g)
    assert expected==L['coefficients'] and z==(X*Y)%(1<<k)
    assert all(abs(x)<1<<h for x,h in zip(expected,L['bounds']))
    count+=1
counts['monomial_oracle_precision_products']=count

# Arithmetic witnesses: document how the original routines scan/materialize.
width_rows=[]
for N in (64,128,256,512,1024):
    x=(1<<N)-1;short=7
    # Original mul(short,x) executes N iterations; source division creates
    # N-bit input right shifts and a growing quotient on every scanned bit.
    ar=pc.Arithmetic();assert ar.mul(short,x)==short*x
    ar.divmod(x,short)
    width_rows.append({'wide_bits':N,'short_bits':short.bit_length(),
       'original_mul_multiplier_iterations':x.bit_length(),
       'short_operand_scan_iterations_after_repair':short.bit_length(),
       'original_division_input_right_shift_bit_volume':N*(N+1)//2,
       'longdivision_steps':ar.counts['longdivision_steps']})

result={'status':'PASS','seed':202610151904,'counts':counts,'precision_primitive_width_witnesses':width_rows,
 'scope':'Independent bounded arithmetic and lemma controls; no novelty or faster-multiplier claim.'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
