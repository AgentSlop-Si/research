"""Fresh source-inspected positive and adversarial controls; no external I/O."""
import copy
import json
import time
from hashlib import sha256
from pathlib import Path
from fractions import Fraction
from scale_adapter import ScaleAdapter,canonical,strict_loads,Failure
from constant_buckets import _window, ShortTaylor, Meter, K_FIXED

ROOT=Path(__file__).resolve().parent
counts={}
def check(name,condition):
    if not condition: raise AssertionError(name)
    counts[name]=counts.get(name,0)+1

def rejects(name,fn,part=None):
    try: fn()
    except (ValueError,TypeError,ArithmeticError) as e:
        if part is not None: check(name+' reason',part in str(e))
        check(name,True)
    else: raise AssertionError('expected rejection: '+name)

start=time.monotonic()
pins={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest()
      for p in ROOT.rglob('*.py')}
adapter=ScaleAdapter()
raw,state=adapter.producer.fixture()
run=adapter.execute(raw,state)
packet=run.packet()
check('full theorem dimensions',len(run.numerators)==131072 and run.bits==464)
check('exact sparse branch',packet['source']['alpha_exponent']==0 and packet['source']['norm_squared']==1)
check('formal p selection',packet['producer']['policy']['p']==268436013)
check('formal radius',packet['source']['formal_policy_radius_over_alpha']=={'coefficient':1,'scale':-466})
check('all output exact builtins',type(run.numerators) is tuple and all(type(row) is tuple and len(row)==2 and all(type(x) is int for x in row) for row in run.numerators))
check('imaginary zeros',all(row[1]==0 for row in run.numerators))
check('nonzero bins', [i for i,row in enumerate(run.numerators) if row!=(0,0)]==[0,1,131071])
check('side symmetry',run.numerators[1]==run.numerators[-1])
check('certified local half threshold',[i for i,(a,b) in enumerate(run.numerators) if 2*abs(a)>(1<<464)]==[0])
check('full semantic replay',adapter.verify(raw,state,16,464,packet)['status']=='SEMANTICALLY_VERIFIED_THEOREM_CONSTANT_BUCKETS')
for key,mutate in [
 ('changed bucket',lambda p:p['bucket_numerators'][0].__setitem__(0,p['bucket_numerators'][0][0]+1)),
 ('injected far bucket',lambda p:p['bucket_numerators'][900].__setitem__(0,1)),
 ('changed source exponent',lambda p:p['source'].__setitem__('value_exponent',-13)),
 ('changed alpha',lambda p:p['source'].__setitem__('alpha_exponent',1)),
 ('changed pgrid shift',lambda p:p['producer']['payload']['formal_p_grid'].__setitem__('common_left_shift',1)),
 ('changed input binding',lambda p:p['producer']['context']['raw'].__setitem__('F',1)),
 ('extra attestation',lambda p:p.__setitem__('producer_verified',True)),
 ('changed bucket type',lambda p:p['bucket_numerators'][900].__setitem__(0,False)),
 ('changed sigma',lambda p:p['downstream'].__setitem__('sigma',3)),
 ]:
    bad=copy.deepcopy(packet);mutate(bad)
    rejects(key,lambda:adapter.verify(raw,state,16,464,bad),'SEMANTIC_MISMATCH')
for label,change in [
 ('wrong support',lambda x:x['entries'][0].__setitem__(0,x['N']//4)),
 ('wrong amplitude',lambda x:x['entries'][0].__setitem__(1,3)),
 ('raw bool',lambda x:x.__setitem__('N',True)),
 ('raw float',lambda x:x.__setitem__('F',0.0)),
 ('unsorted support',lambda x:x.__setitem__('entries',[[x['N']//4,1,0],[0,1,0]])),
 ('nonaxis support',lambda x:x['entries'][0].__setitem__(0,1)),
 ]:
    bad=copy.deepcopy(raw);change(bad)
    rejects(label,lambda:adapter.execute(bad,state))
for sigma,tau in [(0,0),(2,0),(1,-1),(1,raw['N']),(True,0),(1,False)]:
    rejects('bad schedule',lambda:adapter.execute(raw,state,sigma=sigma,tau=tau))
for F in (-127,-1,0,1,127):
    scaled=copy.deepcopy(raw);scaled['F']=F
    other=adapter.execute(scaled,state,sigma=3,tau=raw['N']-1)
    h=json.loads(other.header_bytes)
    check('scale invariant output',other.numerators is run.numerators)
    check('symbolic alpha',h['source']['alpha_exponent']==-F)
    check('normalized constant exponent',h['source']['value_exponent']==-14)
check('real source normalization',Fraction(raw['N'],1<<28)==1)
for sigma,tau in ((1,0),(3,raw['N']-1),(raw['N']-1,17)):
    same=adapter.execute(raw,state,sigma=sigma,tau=tau)
    check('all odd permutations constant',same.numerators==run.numerators)
rejects('insufficient downstream q',lambda:adapter.execute(raw,state,q=28),'TARGET_BUDGET')
rejects('below one shot p',lambda:adapter.execute(raw,state,p=1),'PRECISION')
class EqualityTrap:
    def __eq__(self,other): raise AssertionError('untrusted equality hook executed')
rejects('unknown source object',lambda:adapter.engine.run((EqualityTrap(),)*4,-14,1,0),'GRAMMAR')
rejects('nonconstant direct source',lambda:adapter.engine.run(((0,1),)*4,-14,1,0),'DOMAIN')
rejects('wrong normalized direct source',lambda:adapter.engine.run(((1,0),)*4,-13,1,0),'DOMAIN')
rejects('duplicate JSON keys',lambda:strict_loads('{"x":1,"x":2}'),'duplicate')
rejects('nonfinite JSON',lambda:strict_loads('{"x":NaN}'),'noninteger')
rejects('float JSON',lambda:strict_loads('{"x":0.5}'),'noninteger')
rejects('huge JSON integer',lambda:strict_loads('{"x":'+('1'*1235)+'}'),'digits')
rejects('surrogate JSON text',lambda:strict_loads('\ud800'),'surrogate')
rejects('unsupported canonical tuple',lambda:canonical((1,2)),'unsupported')
cycle=[];cycle.append(cycle)
rejects('cyclic tree',lambda:canonical(cycle),'tree')
encoded=canonical(packet).decode('ascii')
check('JSON exact round trip',strict_loads(encoded)==packet)
# Exact checks of the analytical far-bin and window bounds.
e=adapter.engine;s=e.spec
check('window delta exact inequality',e.delta[0]*(s.M**4)<=e.delta[1])
check('far zero rho inequality',e.far_bin_bound[0]*(1<<s.P)<=e.far_bin_bound[1])
check('sparse ratio guard',s.B==4096*32)
check('compact guard',s.W<s.M and s.T>=4 and s.M%s.B==0)
check('outer beta m guard',Fraction(5,56)*28>=2)
for cert in e.certificates:
    u=1<<(cert.enclosure_bits-s.P)
    center=cert.numerator*u
    radius=max(abs(center-cert.enclosure_low),abs(center-cert.enclosure_high))
    check('exact squared radius',radius==cert.radius_grid_units and radius*radius<=u*u)
# Minimal m follows ceil(m/2+y)-ceil(2y)<=ceil(m/2-y)<=11 for m<=26,y>=2.
for m in range(1,27):
    for numerator in range(4,8*m+1):
        y=Fraction(numerator,2)
        if y<2 or y>=Fraction(m,2): continue
        ceil=lambda x:-((-x.numerator)//x.denominator)
        check('minimal m sample',ceil(Fraction(m,2)+y)-ceil(2*y)<12)
first=_window.theorem_spec(27,Fraction(2,27))
check('m27 witness',first.B==65536 and first.W<first.M)
# Mutation of original caller lists does not change the frozen result.
raw['entries'][0][1]=9
check('frozen result after input mutation',run.packet()==packet)
raw['entries'][0][1]=1
check('prepost code identity',pins=={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*.py')})
old_coeff_cells=2*s.r+(s.ell-1)*(2*s.r)*(2*s.r+1)//2
results={'status':'PASS','assertions':sum(counts.values()),'categories':counts,
         'elapsed_seconds':time.monotonic()-start,'source_pins':pins,
         'parameters':e.evidence()['theorem_parameters'],
         'numerical':e.evidence(),
         'legacy_literal_requirements':{'source_tuple_entries':s.M,
             'time_taps':s.W,'coefficient_cells':old_coeff_cells,
             'fft_roots':s.B//2,'fft_butterflies':(s.B//2)*(s.B.bit_length()-1)},
         'resource_receipt':adapter.receipt(additional_packet_exports=3,additional_json_parses=7),
         'packet_bytes':len(encoded),'scope':'live bound exact structured producer and theorem-parameter BUCKETS only; not full recovery'}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','assertions':results['assertions'],'elapsed_seconds':results['elapsed_seconds'],'packet_bytes':len(encoded)}))
