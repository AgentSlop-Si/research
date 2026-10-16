"""Reviewer-authored contract checks. Does not import or execute supplied code."""
from fractions import Fraction as Q
from itertools import product, permutations
from math import comb, prod
from pathlib import Path
import json

root = Path(__file__).parent
cert = json.loads((root/'review_inert/parameter_certificate_v12.json').read_text())
def q(x): return Q(x['numerator'], x['denominator'])
h=100
v=comb(h,3)
N=v**3
m=h**3
I=3*v*v
z_b=3*comb(97,2)
z_c=comb(97,3)+3*97
W_b=2*N+I*(v*z_b+100)
W_c=2*N+I*(v*z_c+101)
loss_b=I*100*h
loss_c=I*101*h
eta_b=Q(N-2*loss_b,W_b*m)
eta_c=Q(2*N-2*loss_c,W_c*m)
assert eta_b==Q(339,22587335000000)
assert eta_c==Q(73,19906842167500)
s_c=W_c*m-2*N+2*loss_c
B=s_c+64*(W_c+m+1)**3
assert m**10<B<m**11
assert max(20,11+3)==20
L=Q(13815511,10**6)
term=Q(1)
partial=term
for j in range(1,100):
    term=term*L/j
    partial+=term
assert partial>m
a=eta_b/L
b=eta_c/L
tau,sigma=1-a,1-b
beta=Q(1,2)
delta=Q(1,16)
lam=1-a*a
lp=1-a*a/2
c=a*(1-2*a)/(2*(1-a))
for field,value in [('tau',tau),('sigma',sigma),('beta',beta),('delta',delta),('lam',lam),('lam_prime',lp),('c',c)]:
    assert q(cert['parameters'][field])==value
assert 0<tau<1 and 0<sigma<1 and 0<delta<Q(1,8)
assert max(tau,sigma)<lam<1
assert tau*(1+c/beta)<lam
assert max(lam,sigma+beta*(1-sigma))<lp<1
records=[]
for eps in [Q(1,40),Q(1,21)]:
    k=eps*c*a/2
    margins=[1-eps*(1+c),eps*c*a,eps*(1-lp),a*(1-eps),Q(1,4)-delta-Q(3,2)*eps,1-delta-eps,eps]
    assert 0<eps<Q(1,12) and 20*eps<1
    assert eps*c<1-eps
    assert min(margins)==margins[1]==2*k
    assert 1-tau-eps*(2-tau)<0
    records.append({'epsilon':str(eps),'kappa':str(k),'kappa_float_display':float(k),'minimum_margin_index':2,'guard_slack':str(1-20*eps),'necessary_log2_b_display':float(1/(eps*c))})
assert Q(records[1]['kappa'])/Q(records[0]['kappa'])==Q(40,21)
assert Q(records[0]['kappa'])==q(cert['parameters']['kappa'])
assert q(cert['old_kappa'])==a**3*(1-2*a)/4
assert q(cert['ratio'])==1/(40*a*(1-a))

# Nonlinear, rounded, order-sensitive synthetic line map. This checks
# conjugation and validity semantics; it is deliberately not a Gaussian test.
def line_map(line,axis,outlen):
    return [sum(((axis+2)*(j+1)+i+1)*z for j,z in enumerate(line))//(i+axis+3) for i in range(outlen)]

def tensor(values,shape,order,inverse,direct):
    dim=len(shape)
    sources=tuple(t-1 for t in shape)
    valid=list(shape if inverse else sources)
    data=dict(values)
    for axis in order:
        physical=list(range(dim))
        if direct:
            physical[axis],physical[-1]=physical[-1],physical[axis]
        else:
            physical=physical[:axis]+physical[axis+1:]+[axis]
        extents=[shape[i] for i in physical]
        changed={}
        for prefix in product(*(range(t) for t in extents[:-1])):
            logical=[None]*dim
            for j,i in zip(prefix,physical[:-1]): logical[i]=j
            line=[]
            keys=[]
            for j in range(extents[-1]):
                logical[axis]=j
                key=tuple(logical)
                keys.append(key)
                line.append(data[key])
            if not all(j<valid[i] for j,i in zip(prefix,physical[:-1])):
                assert not any(line)
                result=[0]*extents[-1]
            elif inverse:
                result=line_map(line,axis,sources[axis])+[0]*(shape[axis]-sources[axis])
            else:
                assert not any(line[sources[axis]:])
                result=line_map(line[:sources[axis]],axis,shape[axis])
            changed.update(zip(keys,result))
        valid[axis]=sources[axis] if inverse else shape[axis]
        assert all(not value for key,value in changed.items() if any(j>=v for j,v in zip(key,valid)))
        data=changed
    return data

cases=0
noncommuting=False
shapes=[(2,),(2,4),(4,2),(2,4,2),(4,2,4),(2,4,2,4)]
for shape in shapes:
    keys=list(product(*(range(t) for t in shape)))
    for inverse in [False,True]:
        valid=shape if inverse else tuple(t-1 for t in shape)
        data={key:((13*i)%23-11 if all(j<v for j,v in zip(key,valid)) else 0) for i,key in enumerate(keys)}
        for order in permutations(range(len(shape))):
            assert tensor(data,shape,order,inverse,False)==tensor(data,shape,order,inverse,True)
            cases+=1
        if len(shape)>1:
            natural=tuple(range(len(shape)))
            noncommuting |= tensor(data,shape,natural,inverse,True)!=tensor(data,shape,natural[::-1],inverse,True)
assert noncommuting
result={'scope':'Independent exact rational and abstract line-map conjugation checks, not supplied-code execution or Gaussian numerical validation.','supplied_code_executed':False,'rank_and_guard_constants_rederived':True,'parameter_points':records,'line_schedule_comparisons':cases,'noncommuting_axis_order_witness':noncommuting,'result':'PASS'}
(root/'SECOND_REVIEW_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
