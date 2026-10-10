"""Auditor-authored controls. No uploaded executable is imported or run.

Finite exact checks corroborate the separately stated algebra. They are neither
a benchmark nor an all-N proof, nor a validation of the uploaded implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import product
from math import comb, cos, pi, gcd
import json

OUT = Path(__file__).resolve().parent
results = {}

def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def inv(a):
    n = len(a)
    z = [[F(t) for t in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if z[k][j])
        z[j], z[k] = z[k], z[j]
        q = z[j][j]
        z[j] = [v/q for v in z[j]]
        for i in range(n):
            if i != j:
                q = z[i][j]
                z[i] = [u-q*v for u, v in zip(z[i], z[j])]
    return [r[n:] for r in z]

def norm1(a):
    return max(sum(abs(row[j]) for row in a) for j in range(len(a)))

green = []
for n in range(1, 17):
    t = [[F(3 if i == j else -1 if abs(i-j) == 1 else 0)
          for j in range(n)] for i in range(n)]
    u = [[t[i][j] + F(i == j) for j in range(n)] for i in range(n)]
    ti, ui = inv(t), inv(u)
    s = [[ti[i][j]+ui[i][j] for j in range(n)] for i in range(n)]
    si = inv(s)
    a, b = norm1(s), norm1(si)
    assert a <= F(3, 2) and b <= F(17, 6) and a*b <= F(17, 4)
    green.append({'n': n, 'norm1': str(a), 'inverse_norm1': str(b)})
results['two_green_exact_rational'] = {'cases': len(green), 'records': green}

params = []
for h in (21, 22, 24, 100):
    v, m = comb(h, 3), h**3
    d = comb(h-3, 3)+3*(h-3)
    w = 2*v**3 + 3*v*v*(v*d+h+1)
    delta = 2*v*v*(v-3*h*(h+1))
    p = (w-1).bit_length()
    with localcontext() as c:
        c.prec = 70
        eps = Decimal(delta)/(Decimal(m)*Decimal(2**p))
        saving = -(1-eps).ln()/Decimal(m).ln()
    params.append({'h':h,'v':v,'m':m,'degree':d,'W':w,'p':p,
                   'Delta':delta,'S':m*2**p-delta,
                   'epsilon':str(F(delta,m*2**p)),
                   'exponent_saving':str(saving)})
p24 = next(x for x in params if x['h']==24)
assert p24['W'] == 34666942577344 and p24['Delta'] == 1835266048
assert p24['p'] == 45 and p24['S'] == 486388757920747520
assert params[0]['Delta'] < 0 < params[1]['Delta']
assert Decimal(p24['exponent_saving']) > Decimal('3e-10')
results['network_retuning_constants_only'] = params

packing_cases = packing_lanes = 0
for U in (1, 2, 3):
    for G in (1, 2, 3):
        h = (2*U*G).bit_length()
        w = 16
        r = w//h
        for seq in product(range(-U, U+1), repeat=G):
            # Alternate signs across lanes to stress independence and guards.
            words = [sum(((a if lane % 2 == 0 else -a)+U) << (h*lane)
                         for lane in range(r)) for a in seq]
            acc = 0
            for word in words:
                acc += word
                assert 0 <= acc < 2**w
            for lane in range(r):
                got = ((acc >> (h*lane)) & (2**h-1))-G*U
                want = sum(seq)*(1 if lane % 2 == 0 else -1)
                assert got == want
                packing_lanes += 1
            packing_cases += 1
results['guarded_addition_exact_16bit'] = {'cases':packing_cases,'lanes':packing_lanes}

spectral = []
for n in range(1, 33):
    vals = sorted([(5-4*cos((2*j+1)*pi/n))/(2-2*cos((2*j+1)*pi/n))
                   for j in range(n)])
    pairs = [vals[j]*vals[-1-j] for j in range(n)]
    spread = max(pairs)-min(pairs)
    assert (spread < 1e-9) == (n in (1, 2, 4))
    spectral.append({'n':n,'reverse_pair_spread':spread})
results['forward_cycle_spectrum_numeric_only'] = spectral

P = 97
def conv(a,b):
    n=len(a)
    return [sum(a[t]*b[(j-t)%n] for t in range(n))%P for j in range(n)]
def add(a,b): return [(x+y)%P for x,y in zip(a,b)]
def scale(a,c): return [c*x%P for x in a]
def expression(a,b,c,d):
    return add(add(conv(conv(a,a),a), scale(conv(a,b),2)), conv(c,d))
jet_cases = jet_coordinates = 0
for n in (3,4,5,8,16):
    a=[(7*i+3)%P for i in range(n)]
    b=[(i*i+2)%P for i in range(n)]
    c=[(2*i*i+5)%P for i in range(n)]
    d=[(11*i+9)%P for i in range(n)]
    k0=expression(a,b,c,d)
    k1=add(scale(conv(a,a),3),scale(b,2))
    k2=scale(a,3)
    for t in range(n):
        for delta in (-3,0,1,7):
            edited=a[:];edited[t]=(edited[t]+delta)%P
            expected=expression(edited,b,c,d)
            observed=[(k0[q]+delta*k1[(q-t)%n]+delta**2*k2[(q-2*t)%n]
                       +delta**3*(q==(3*t)%n))%P for q in range(n)]
            assert expected==observed
            jet_cases+=1;jet_coordinates+=n
results['polynomial_single_edit_identity_exact']={'cases':jet_cases,'coordinates':jet_coordinates}

coset_cases=coset_coordinates=0
for n in (4,8,16,32):
    omega=pow(5,(P-1)//n,P)
    assert pow(omega,n,P)==1 and pow(omega,n//2,P)!=1
    for m in (2,4):
        step=n//m
        for a in range(step):
            coeff=[(7*t+3)%P for t in range(m)]
            for k in range(n):
                direct=sum(coeff[t]*pow(omega,(a+step*t)*k,P) for t in range(m))%P
                reduced=pow(omega,a*k,P)*sum(coeff[t]*pow(omega,step*t*(k%m),P)
                                          for t in range(m))%P
                assert direct==reduced
                coset_coordinates+=1
            coset_cases+=1
results['cyclic_coset_correction_exact']={'cases':coset_cases,'coordinates':coset_coordinates}

thin_cases=thin_coordinates=0
for n in range(1,8):
    for k in range(1,7):
        zs=[(s*s+2)%101 for s in range(k)]
        aa=[(3*s+1)%101 for s in range(k)]
        for r in range(n):
            for b in range(n):
                uv=sum(pow(zs[s],r,101)*aa[s]*pow(pow(zs[s],n,101),b,101)
                       for s in range(k))%101
                direct=sum(aa[s]*pow(zs[s],r+b*n,101) for s in range(k))%101
                assert uv==direct
                thin_coordinates+=1
        thin_cases+=1
results['thin_product_reduction_identity_only']={'cases':thin_cases,'coordinates':thin_coordinates}

mass_cases=0
for n in (1,2,3,4,8):
    for seed in range(40):
        xs=[((seed+3*j)*(j+2)%19)-9 for j in range(n)]
        S=sum(xs)
        fit=[n*x-S for x in xs]
        zero=[n*x for x in xs]
        rho=fit if sum(map(abs,fit))<=sum(map(abs,zero)) else zero
        assert F(sum(map(abs,rho)),n)<=sum(map(abs,xs))
        if rho==fit: assert all(F(S,n)+F(r,n)==x for r,x in zip(rho,xs))
        else: assert all(F(r,n)==x for r,x in zip(rho,xs))
        mass_cases+=1
results['periodic_cluster_residual_exact']={'clusters':mass_cases}

results['scope']={
    'uploaded_source_execution':False,
    'historical_logs_rerun':False,
    'fresh_benchmark':False,
    'proof_role':'Bounded auditor-authored controls; all-N deductions are separately explained in PROOF_SCOPE.md.',
    'status':'PASS'
}
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k: (v.get('cases',v.get('clusters')) if isinstance(v,dict) else len(v))
                  for k,v in results.items() if k!='scope'},indent=2))
print('PASS: independent controls only; uploaded executables stayed inert.')
