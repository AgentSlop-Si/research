"""Independent final review. Imports only pinned fresh production source and stdlib.
Oracle: pi=4(atan(1/2)+atan(1/3)), outward fixed rational Taylor.
Exact controls: Q(sqrt(2)) for complete N=4,8 transforms, with exact ordering.
No producer test/oracle imports; no external writes or network.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from functools import lru_cache
from copy import deepcopy
from hashlib import sha256
import importlib.util,sys,json,random,time,ast
BASE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parent / '../candidate/sparse_supplier.py'
PIN='5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed'
assert sha256(SOURCE.read_bytes()).hexdigest()==PIN
spec=importlib.util.spec_from_file_location('reviewed_sparse_supplier',SOURCE)
S=importlib.util.module_from_spec(spec);sys.modules[spec.name]=S;spec.loader.exec_module(S)
checks=[];observations={};start=time.monotonic()
def check(name,test):
    if not test:raise AssertionError(name)
    checks.append(name)
def rejects(name,fun):
    try:fun()
    except S.Failure:checks.append(name);return
    raise AssertionError('unexpected acceptance: '+name)
def raw(n,rows,Fexp=0):return {'schema':S.SCHEMA,'N':n,'F':Fexp,'entries':rows}
def state(n,a=1,beta=0):return {'N':n,'B':n,'a':a,'beta':beta}
def ceil(a,b):return -((-a)//b)

# Complete exact arithmetic in Q(sqrt(2)); the field embedding is positive sqrt(2).
def pa(x,y):return x[0]+y[0],x[1]+y[1]
def pn(x):return -x[0],-x[1]
def pm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def pc(x):return F(x),F(0)
def ps(x):
    a,b=x
    if not a:return (b>0)-(b<0)
    if not b:return (a>0)-(a<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    compare=(a*a>2*b*b)-(a*a<2*b*b)
    return compare if a>0 else -compare
def cm(x,y):return pa(pm(x[0],y[0]),pn(pm(x[1],y[1]))),pa(pm(x[0],y[1]),pm(x[1],y[0]))
def ca(x,y):return pa(x[0],y[0]),pa(x[1],y[1])
Z=pc(0);O=pc(1);H=(F(0),F(1,2))
ROOT8=[(O,Z),(H,pn(H)),(Z,pn(O)),(pn(H),pn(H)),(pn(O),Z),(pn(H),H),(Z,O),(H,H)]
def exact_transform(values,n):
    normalizer=pc(F(1,2)) if n==4 else (F(0),F(1,4))
    out=[]
    for j in range(n):
        value=(Z,Z)
        for k,x in enumerate(values):value=ca(value,cm(x,ROOT8[(8//n*k*j)%8]))
        out.append((pm(value[0],normalizer),pm(value[1],normalizer)))
    return out
for n in (4,8):
    rows=[[j,(3*j+1)%7-3,(5*j+2)%9-4] for j in range(n)]
    rows=[x for x in rows if x[1:]!=[0,0]];rows[0][1]|=1
    src=raw(n,rows,-13);r=S.execute(src,state(n,n-1,n-1),query_bits=48)
    vals=[(Z,Z) for _ in range(n)]
    for k,a,b in rows:vals[k]=(pc(F(a,1<<r.h)),pc(F(b,1<<r.h)))
    exact=exact_transform(vals,n)
    recovered=exact_transform(exact,n)
    check('exact_second_negative_transform_reversal_N'+str(n),recovered==[vals[(-j)%n] for j in range(n)])
    energy=Z
    for z in exact:energy=pa(energy,pa(pm(z[0],z[0]),pm(z[1],z[1])))
    check('exact_unitary_norm_N'+str(n),energy==pc(F(r.energy,1<<(2*r.h))))
    for j,value in enumerate(exact):
        p=r.query(j).packet();error=Z
        for d in range(2):
            lo,hi=p['enclosure_numerators'][d];D=1<<(-p['enclosure_exponent'])
            check('exact_box_N%d_j%d_d%d'%(n,j,d),ps(pa(value[d],pn(pc(F(lo,D)))))>=0 and ps(pa(pc(F(hi,D)),pn(value[d])))>=0)
            v=pc(F(p['value_numerators'][d],1<<(-p['value_exponent'])))
            e=pa(v,pn(value[d]));error=pa(error,pm(e,e))
        check('exact_complex_error_N%d_j%d'%(n,j),ps(pa(pc(F(1,1<<(2*r.query_bits))),pn(error)))>=0)
    if n==4:
        check('exact_quarter_phase_negative_sign',S.execute(raw(n,[[1,1,0]]),state(n),query_bits=16).query(1).packet()['value_numerators']==[0,-(1<<18)])

# Rational-pi oracle, derived from tan(atan(1/2)+atan(1/3))=1, both terms positive.
@lru_cache(None)
def pi_box(B):
    threshold=F(1,1<<(B+12))
    def atan_den(d):
        s=F(0);power=d;k=0
        while True:
            t=F(1,power*(2*k+1))
            if t<threshold:return (s,s+t) if k%2==0 else (s-t,s)
            s+=t if k%2==0 else -t
            power*=d*d;k+=1
    a,b=atan_den(2);c,d=atan_den(3)
    low,high=4*(a+c),4*(b+d);D=1<<B
    return low.numerator*D//low.denominator,ceil(high.numerator*D,high.denominator)
class Fixed:
    def __init__(self,B):self.B=B;self.D=1<<B
    def add(self,a,b):return a[0]+b[0],a[1]+b[1]
    def neg(self,a):return -a[1],-a[0]
    def mul(self,a,b):
        xs=[x*y for x in a for y in b]
        return min(xs)//self.D,ceil(max(xs),self.D)
    def scale(self,a,n,d=1):
        xs=[a[0]*n,a[1]*n]
        return min(xs)//d,ceil(max(xs),d)
    def trig(self,x,sine):
        # Taylor alternating series is decreasing here (0<=x<=pi/2<2).
        # Enclose each polynomial term independently; remainder <= next magnitude.
        term=x if sine else (self.D,self.D);answer=term;degree=1 if sine else 0;sign=-1
        x2=self.mul(x,x)
        while True:
            term=self.scale(self.mul(term,x2),1,(degree+1)*(degree+2));degree+=2
            if term[1]<=4:
                return answer[0]-term[1],answer[1]+term[1]
            answer=self.add(answer,term if sign==1 else self.neg(term));sign=-sign
@lru_cache(None)
def oracle_root(n,k,B):
    f=Fixed(B);D=f.D;k%=n;q,r=divmod(k,n//4)
    if not r:return [((D,D),(0,0)),((0,0),(-D,-D)),((-D,-D),(0,0)),((0,0),(D,D))][q]
    pi=pi_box(B);x=f.scale(pi,2*r,n)
    cos=f.trig(x,False);sin=f.trig(x,True)
    return [(cos,f.neg(sin)),(f.neg(sin),f.neg(cos)),(f.neg(cos),sin),(sin,cos)][q]
def oracle_query(src,h,j,B):
    f=Fixed(B);D=f.D;n=src['N'];result=[(0,0),(0,0)]
    for k,a,b in src['entries']:
        re,im=oracle_root(n,k*j%n,B)
        result[0]=f.add(result[0],f.add(f.scale(re,a),f.scale(im,-b)))
        result[1]=f.add(result[1],f.add(f.scale(im,a),f.scale(re,b)))
    # Independent reciprocal of a direct sqrt(N) bracket, no supplier roots or normalizer.
    low=isqrt(n*D*D);high=low+(low*low!=n*D*D)
    inv=(D*D//high,ceil(D*D,low))
    return [f.scale(f.mul(x,inv),1,1<<h) for x in result]
def compare_oracle(name,src,r,j):
    p=r.query(j).packet();B=r.working_bits+80;D=1<<B;o=oracle_query(src,r.h,j,B)
    scale=1<<(B-r.working_bits)
    check(name+'_boxes_overlap',all(p['enclosure_numerators'][d][0]*scale<=o[d][1] and p['enclosure_numerators'][d][1]*scale>=o[d][0] for d in range(2)))
    pointscale=1<<(B+p['value_exponent'])
    rad=[max(abs(p['value_numerators'][d]*pointscale-o[d][0]),abs(p['value_numerators'][d]*pointscale-o[d][1])) for d in range(2)]
    check(name+'_oracle_point_error',sum(x*x for x in rad)<=1<<(2*(B-r.query_bits)))
    return p
src,st=S.fixture();fixture=S.execute(src,st,q=464)
check('fixture_inherited_policy',fixture.policy['p']==268436013 and fixture.policy['plan']['kappa']==-268436012)
fixture_packets=[]
for j in (0,1,3,17,2048,(1<<27)-1,(1<<28)-1):
    p=compare_oracle('fixture_j'+str(j),src,fixture,j);fixture_packets.append(p)
    check('fixture_accepted_j'+str(j),fixture.query(j,True).packet()==p and p['accepted_serial_radius_compliant'] and p['original_target_complex_error_power']==-467)
check('fixture_nonconstant',fixture_packets[0]['value_numerators']!=fixture_packets[1]['value_numerators'])
check('fixture_original_grid_symbolic',fixture_packets[1]['formal_original_grid']['common_left_shift']==268435542)
observations['fixture']={'source':fixture.packet(),'sample_queries':fixture_packets,'setup_ledger':fixture.ledger,'query_ledger':fixture.query((1<<28)-1).ledger}

rng=random.Random(202610172144)
def sample_indices(n,k):
    out=set()
    while len(out)<k:out.add(rng.randrange(n))
    return sorted(out)
for m in (3,4,5,8,17,31,63,64):
    n=1<<m;idx=sample_indices(n,min(7,n))
    rows=[[k,rng.randrange(-100,101),rng.randrange(-100,101)] for k in idx];rows[0][1]|=1
    sr=raw(n,rows,37);r=S.execute(sr,state(n,n-1,n-1),query_bits=72)
    for j in (0,1,n//4-1,n//2+1,n-1):compare_oracle('independent_m%d_j%d'%(m,j),sr,r,j)

# Exhaust every admitted log-length, support and width endpoint, including odd m.
max_width=0;max_operations=0
for m in range(2,65):
    n=1<<m;sr=raw(n,[[1,-3,2],[n-1,7,-5]],-(1<<127));r=S.execute(sr,state(n,n-1,n-1),q=m,query_bits=8)
    for j in (0,1,n-1):
        p=r.query(j).packet();check('domain_m%d_j%d'%(m,j),p['complex_error_power']==-8 and len(r.roots)==m+1)
    check('norm_m'+str(m),r.energy<=1<<(2*r.h)<4*r.energy)
for nenergy in (1,2,3,4,5,15,16,17,63,64,65):
    # Review normalization directly across the representable sum-of-squares controls.
    r=S.execute(raw(4,[[1,nenergy,1]]),state(4),query_bits=8)
    expected=0
    while (1<<(2*expected))<r.energy:expected+=1
    check('normalization_threshold_'+str(nenergy),r.h==expected)
for m in (63,64):
    n=1<<m;idx=sample_indices(n,64);rows=[[k,((1<<1023)+i)|1,-(1<<1023)] for i,k in enumerate(idx)]
    r=S.execute(raw(n,rows,-(1<<127)),state(n,n-1,n-1),q=1<<126,p=1<<127,query_bits=4096)
    a=r.query(n-1);p=a.packet();max_width=max(max_width,a.ledger['max_data_integer_bits']);max_operations=max(max_operations,a.ledger['operations'])
    check('maximum_endpoint_m'+str(m),len(r.entries)==64 and r.query_bits==4096 and a.ledger['max_data_integer_bits']<=12288 and a.ledger['operations']<1000000)
    check('maximum_endpoint_policy_honesty_m'+str(m),not p['accepted_serial_radius_compliant'])
    rejects('maximum_endpoint_required_radius_m'+str(m),lambda:r.query(n-1,True))
    observations['maximum_m'+str(m)]={'working_bits':r.working_bits,'setup_ledger':r.ledger,'query_ledger':a.ledger,'policy':r.policy,'formal_original_grid':p['formal_original_grid']}
observations['maximum_recorded_integer_bits']=max_width;observations['maximum_query_records']=max_operations

# Accepted-radius boundaries separately exercise the radius and symbolic-grid requirements.
r=S.execute(src,st,q=464,p=fixture.policy['p']+100,query_bits=468)
check('larger_p_no_radius_claim',not r.query(1).packet()['accepted_serial_radius_compliant'])
rejects('larger_p_radius_required',lambda:r.query(1,True))
small=S.execute(raw(4,[[1,1,0]]),state(4),q=2,query_bits=4096)
check('negative_symbolic_shift_no_grid',small.query(1).packet()['formal_original_grid'] is None)
rejects('negative_symbolic_shift_required',lambda:small.query(1,True))
for R in (466,467,468):
    r=S.execute(src,st,q=464,query_bits=R)
    check('radius_inequality_boundary_R'+str(R),r.query(1).packet()['accepted_serial_radius_compliant']==(R>=467))
    if R<467:rejects('radius_threshold_reject_R'+str(R),lambda:r.query(1,True))
    else:check('radius_threshold_accept_R'+str(R),r.query(1,True).packet()['accepted_serial_radius_compliant'])

# Fresh replay must bind every original argument; label hashes alone do not suffice.
check('honest_source_replay',S.verify(src,st,16,464,fixture.packet())['status']=='SEMANTICALLY_VERIFIED')
check('honest_query_replay',S.verify_query(src,st,16,464,17,fixture.query(17).packet(),require_accepted_radius=True)['status']=='QUERY_SEMANTICALLY_VERIFIED')
for label,mutate in [
 ('source_entry',lambda p:p['descriptor']['entries'][0].__setitem__(1,7)),
 ('normalization',lambda p:p['descriptor'].__setitem__('h',0)),
 ('phase_sign',lambda p:p['descriptor'].__setitem__('unitary_sign',1)),
 ('normalizer',lambda p:p['invsqrtN'].__setitem__(0,0)),
 ('root',lambda p:p['root_table'][-1][1].__setitem__(1,0)),
 ('policy',lambda p:p['policy']['plan'].__setitem__('p',1)),
 ('context',lambda p:p['context']['state'].__setitem__('beta',1)),
 ('attestation',lambda p:p.__setitem__('external_origin_authenticated',True)),
 ('list_cap',lambda p:p.__setitem__('root_table',[0]*257))]:
    p=fixture.packet();mutate(p);rejects('tamper_'+label,lambda p=p:S.verify(src,st,16,464,p))
for label,change in [('raw',lambda x:x['raw']['entries'][0].__setitem__(0,2)),('F',lambda x:x['raw'].__setitem__('F',1)),('state_a',lambda x:x['state'].__setitem__('a',3)),('state_beta',lambda x:x['state'].__setitem__('beta',1)),('t',lambda x:x.__setitem__('t',17)),('q',lambda x:x.__setitem__('q',465)),('p',lambda x:x.__setitem__('p',x['p']+1)),('R',lambda x:x.__setitem__('query_bits',469))]:
    c=fixture.context;change(c)
    if label=='q':c['p']=None
    alt=S.execute(**c)
    rejects('self_consistent_alternative_'+label,lambda alt=alt:S.verify(src,st,16,464,alt.packet()))
    rejects('alternative_query_'+label,lambda alt=alt:S.verify_query(src,st,16,464,17,alt.query(17).packet()))
for label,change in [('value',lambda p:p['value_numerators'].__setitem__(0,p['value_numerators'][0]+1)),('radius',lambda p:p.__setitem__('complex_error_power',-999)),('accepted_flag',lambda p:p.__setitem__('accepted_serial_radius_compliant',False)),('original_shift',lambda p:p['formal_original_grid'].__setitem__('common_left_shift',0)),('context_digest',lambda p:p.__setitem__('context_sha256','0'*64)),('enclosure',lambda p:p['enclosure_numerators'][0].__setitem__(0,0)),('index',lambda p:p.__setitem__('index',18))]:
    p=fixture.query(17).packet();change(p);rejects('query_tamper_'+label,lambda p=p:S.verify_query(src,st,16,464,17,p))
rejects('query_cross_index',lambda:S.verify_query(src,st,16,464,18,fixture.query(17).packet()))
cyclic=[];cyclic.append(cyclic);rejects('cyclic_packet_depth_bounded',lambda:S.verify(src,st,16,464,cyclic))

# Canonical grammar and state boundaries, without relying on implicit coercion.
for label,mutate in [('bool',lambda r:r.__setitem__('N',True)),('float',lambda r:r['entries'][0].__setitem__(1,1.0)),('zero_row',lambda r:r['entries'][0].__setitem__(1,0)),('duplicate',lambda r:r['entries'][1].__setitem__(0,1)),('unsorted',lambda r:r['entries'].reverse()),('noncanonical',lambda r:[e.__setitem__(1,2) for e in r['entries']]),('too_many',lambda r:r.__setitem__('entries',[[i,1,0] for i in range(65)])),('raw_width',lambda r:r['entries'][0].__setitem__(1,1<<1024)),('metadata_width',lambda r:r.__setitem__('F',1<<128)),('tuple',lambda r:r.__setitem__('entries',tuple(r['entries']))),('extra_key',lambda r:r.__setitem__('trust',True))]:
    r=deepcopy(src);mutate(r);rejects('grammar_'+label,lambda r=r:S.execute(r,st,q=464))
for label,params in [('R_low',{'query_bits':7}),('R_high',{'query_bits':4097}),('p_low',{'p':1}),('p_wide',{'p':1<<128}),('q_low',{'q':27}),('t_negative',{'t':-1}),('R_bool',{'query_bits':True})]:rejects('policy_'+label,lambda params=params:S.execute(src,st,**params))
for label,key,value in [('general_B','B',2),('even_a','a',2),('zero_a','a',0),('large_a','a',st['N']),('negative_beta','beta',-1),('large_beta','beta',st['N']),('wrong_N','N',16)]:
    ss=dict(st);ss[key]=value;rejects(label,lambda ss=ss:S.execute(src,ss))
for n in (1,2,12,1<<65):rejects('outside_length_'+str(n),lambda n=n:S.execute(raw(n,[[0,1,0]]),state(n)))
zero=S.execute(raw(8,[]),state(8))
check('canonical_zero',zero.status=='EXACT_INPUT_ZERO' and zero.descriptor is None and zero.policy['p'] is None)
rejects('zero_query',lambda:zero.query(0));rejects('zero_F',lambda:S.execute(raw(8,[],1),state(8)));rejects('zero_p',lambda:S.execute(raw(8,[]),state(8),p=100))
rejects('query_index_bool',lambda:fixture.query(True));rejects('query_index_low',lambda:fixture.query(-1));rejects('query_index_high',lambda:fixture.query(fixture.N));rejects('query_flag_type',lambda:fixture.query(0,1))
copy=fixture.packet();before=fixture.packet();copy['descriptor']['entries'][0][1]=10
check('packet_copy_isolation',fixture.packet()==before)
mutable=deepcopy(src);rr=S.execute(mutable,st,q=464);before=rr.packet();mutable['entries'][0][1]=13
check('original_mutation_isolation',rr.packet()==before)
# Self-consistent replacement of BOTH arguments and answer is a different caller-relative claim.
alt=deepcopy(src);alt['entries'][0][0]=2;alt_run=S.execute(alt,st,q=464)
check('honest_scope_not_origin_authentication',S.verify(alt,st,16,464,alt_run.packet())['external_origin_authenticated'] is False)

# Maximum query precision checked against exact algebraic truth, not a floating oracle.
for n in (4,8):
    rr=S.execute(raw(n,[[1,1,0]]),state(n),query_bits=4096)
    exact=exact_transform([(Z,Z),(O,Z)]+[(Z,Z)]*(n-2),n)
    for j in (1,n-1):
        p=rr.query(j).packet();sq=Z
        for d in range(2):
            v=pc(F(p['value_numerators'][d],1<<(-p['value_exponent'])))
            e=pa(v,pn(exact[j][d]));sq=pa(sq,pm(e,e))
        check('exact_maximum_precision_N%d_j%d'%(n,j),ps(pa(pc(F(1,1<<8192)),pn(sq)))>=0)

# Independently replay all of the delivered small full-DFT artifact.
artifact=json.loads((SOURCE.parent/'SMALL_FULL_DFT.json').read_text())
c=artifact['source']['context']
check('delivered_small_source_replay',S.verify(c['raw'],c['state'],c['t'],c['q'],artifact['source'],p=c['p'],query_bits=c['query_bits'])['status']=='SEMANTICALLY_VERIFIED')
check('delivered_small_exact_output_count',len(artifact['all_queries'])==c['raw']['N'] and [p['index'] for p in artifact['all_queries']]==list(range(c['raw']['N'])))
for p in artifact['all_queries']:
    check('delivered_small_query_replay_'+str(p['index']),S.verify_query(c['raw'],c['state'],c['t'],c['q'],p['index'],p,p=c['p'],query_bits=c['query_bits'])['status']=='QUERY_SEMANTICALLY_VERIFIED')

# Structural audit of the pinned source, not empirical speed substituted for accounting.
tree=ast.parse(SOURCE.read_text());imports=[]
for node in ast.walk(tree):
    if isinstance(node,ast.Import):imports.extend(x.name for x in node.names)
    elif isinstance(node,ast.ImportFrom):imports.append(node.module)
check('stdlib_only_source_imports',set(imports)=={'dataclasses','hashlib','math','json'})
loops=[ast.unparse(node.iter) for node in ast.walk(tree) if isinstance(node,ast.For)]
check('no_N_or_p_range_loop',not any(x in ('range(n)','range(N)','range(p)','range(self.N)') for x in loops))
check('production_pin_unchanged',sha256(SOURCE.read_bytes()).hexdigest()==PIN)
observations['loop_iterables']=loops
result={'status':'PASS','source_sha256':PIN,'named_checks':len(checks),'checks':checks,'observations':observations,'elapsed_seconds':time.monotonic()-start,'historical_programs_executed':False,'external_writes':False,'oracle':'Independent rational pi=4(atan(1/2)+atan(1/3)) with outward Taylor rectangles; exact Q(sqrt(2)) complete N=4,8 transforms and exact ordering.'}
(BASE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'named_checks':len(checks),'elapsed_seconds':result['elapsed_seconds'],'maximum_recorded_integer_bits':max_width,'maximum_query_records':max_operations},indent=2))
