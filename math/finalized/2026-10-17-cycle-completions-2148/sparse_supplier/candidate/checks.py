"""Fresh controls; imports only this candidate and stdlib, never old programs."""
from pathlib import Path
from fractions import Fraction
from math import isqrt
from copy import deepcopy
from hashlib import sha256
import json,random,time,resource
import sparse_supplier as S
BASE=Path(__file__).resolve().parent
checks=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def rejects(name,fn):
    try: fn()
    except S.Failure: checks.append(name);return
    raise AssertionError(name+' accepted')

def pi_interval(bits):
    def atan(a):
        total=Fraction(0);k=0;power=a
        while True:
            term=Fraction(1,(2*k+1)*power)
            if term < Fraction(1,1<<(bits+12)):
                return (total,total+term) if k%2==0 else (total-term,total)
            total += term if k%2==0 else -term
            k+=1;power*=a*a
    a,b=atan(5);c,d=atan(239)
    return 16*a-4*d,16*b-4*c

def oracle_root(n,k,bits):
    """Independent Machin/Taylor rational interval oracle, no candidate helpers."""
    Q=bits+96;D=1<<Q
    def ceil(a,b):return -((-a)//b)
    def add(a,b):return a[0]+b[0],a[1]+b[1]
    def neg(a):return -a[1],-a[0]
    def mul(a,b):
        v=[x*y for x in a for y in b]
        return min(v)//D,ceil(max(v),D)
    def div(a,d):return a[0]//d,ceil(a[1],d)
    def fixed(a,b):return a.numerator*D//a.denominator,ceil(b.numerator*D,b.denominator)
    k%=n;q,r=divmod(k,n//4)
    if r==0:
        axes=[((D,D),(0,0)),((0,0),(-D,-D)),((-D,-D),(0,0)),((0,0),(D,D))]
        return axes[q],Q
    plo,phi=pi_interval(Q+20)
    x=fixed(plo*2*r/n,phi*2*r/n);x2=mul(x,x)
    def series(sine):
        term=x if sine else (D,D);total=term;idx=0
        while True:
            degree=2*idx+1 if sine else 2*idx
            nxt=div(mul(term,x2),(degree+1)*(degree+2))
            if nxt[1]<=1<<12:
                return total[0]-nxt[1],total[1]+nxt[1]
            idx+=1;term=nxt
            total=add(total,neg(term) if idx%2 else term)
            if idx>2048:raise AssertionError('oracle failed to converge')
    s=series(True);c=series(False)
    # Positive core angle; return negative-sign character in the full quadrant.
    pairs=[(c,neg(s)),(neg(s),neg(c)),(neg(c),s),(s,c)]
    return pairs[q],Q

def intersects_scaled(box,bits,oracle,Q):
    scale=1<<(Q-bits)
    return all(a[0]*scale<=b[1] and a[1]*scale>=b[0] for a,b in zip(box,oracle))

def oracle_query(run,j):
    B=run.working_bits;Q=B+96;D=1<<Q
    total=[[0,0],[0,0]]
    def scale(a,k):v=[a[0]*k,a[1]*k];return min(v),max(v)
    for n,re,im in run.entries:
        root,q=oracle_root(run.N,n*j,B);assert q==Q
        a=scale(root[0],re);b=scale(root[1],-im)
        c=scale(root[0],im);d=scale(root[1],re)
        total[0][0]+=a[0]+b[0];total[0][1]+=a[1]+b[1]
        total[1][0]+=c[0]+d[0];total[1][1]+=c[1]+d[1]
    # Independent enclosure for 1/sqrt(N): sqrt(N)*inv=1.
    sl=isqrt(run.N*D*D);sh=sl+(sl*sl!=run.N*D*D)
    inv=(D*D//sh,-((-D*D)//sl))
    out=[]
    for a in total:
        vals=[x*y for x in a for y in inv]
        den=D*(1<<run.h)
        out.append((min(vals)//den,-((-max(vals))//den)))
    return out,Q

start=time.perf_counter();rng=random.Random(203413)
raw,state=S.fixture();run=S.execute(raw,state,q=464)
check('nonquarter_two_mode_fixture',run.entries==((1,1,0),(3,1,0)))
check('live_normalization_energy',run.h==1 and run.energy==2 and run.descriptor['normalized_norm_squared']=={'numerator':2,'denominator_power_two':2})
check('accepted_policy_fixture',run.policy['p']==268436013 and run.policy['plan']['kappa']==-268436012 and run.policy['plan']['accepted_serial_radius_factor']['scale']==-466)
fixture_queries=[]
for j in [0,1,17,2048,(1<<27)-1,(1<<28)-1]:
    answer=run.query(j,True);p=answer.packet();oracle,Q=oracle_query(run,j)
    check('independent_theorem_query_'+str(j),intersects_scaled(p['enclosure_numerators'],run.working_bits,oracle,Q))
    point=p['value_numerators'];step=1<<(Q+p['value_exponent'])
    errors=[max(abs(point[d]*step-oracle[d][0]),abs(point[d]*step-oracle[d][1])) for d in range(2)]
    check('independent_point_error_'+str(j),sum(e*e for e in errors)<=1<<(2*(Q+p['complex_error_power'])))
    check('original_grid_radius_'+str(j),p['accepted_serial_radius_compliant'] and p['original_target_complex_error_power']<=-466 and p['formal_original_grid']['kappa']==-268436012)
    fixture_queries.append({'index':j,'packet':p,'ledger':answer.ledger})
check('nonconstant_query_values',fixture_queries[0]['packet']['value_numerators']!=fixture_queries[1]['packet']['value_numerators'])
check('source_replay',S.verify(raw,state,16,464,run.packet())['status']=='SEMANTICALLY_VERIFIED')
check('point_replay',S.verify_query(raw,state,16,464,17,fixture_queries[2]['packet'],require_accepted_radius=True)['status']=='QUERY_SEMANTICALLY_VERIFIED')

small_queries=0;root_cases=0
for m in range(2,9):
    n=1<<m
    entries=[[j,rng.randrange(-7,8),rng.randrange(-7,8)] for j in sorted(rng.sample(range(n),min(n,5))) ]
    entries=[e for e in entries if e[1:]!=[0,0]]
    entries[0][1]|=1
    rr={'schema':S.SCHEMA,'N':n,'F':-7,'entries':entries};st={'N':n,'B':n,'a':3 if n>3 else 1,'beta':n-1}
    r=S.execute(rr,st,query_bits=32)
    for j in sorted(set([0,1,n//4,n//2,n-1]+[rng.randrange(n) for _ in range(3)])):
        a=r.query(j).packet();oracle,Q=oracle_query(r,j)
        check('small_independent_query_'+str(m)+'_'+str(j),intersects_scaled(a['enclosure_numerators'],r.working_bits,oracle,Q));small_queries+=1
    check('normalization_m'+str(m),(1<<(2*r.h))>=r.energy and (1<<(2*r.h))<4*r.energy)
    for ell in range(2,m+1):
        oracle,Q=oracle_root(1<<ell,1,r.working_bits)
        check('independent_root_'+str(m)+'_'+str(ell),intersects_scaled(r.roots[ell],r.working_bits,oracle,Q));root_cases+=1

# Complete N=16 explicit output: every query and output write is counted.
n=16;rr={'schema':S.SCHEMA,'N':n,'F':2,'entries':[[1,1,0],[3,-2,1],[9,3,-1]]};st={'N':n,'B':n,'a':1,'beta':0}
r=S.execute(rr,st,query_bits=48);dense=[r.query(j) for j in range(n)]
dense_packets=[a.packet() for a in dense]
check('paid_complete_small_DFT',len(dense_packets)==n and [a['index'] for a in dense_packets]==list(range(n)))
(BASE/'SMALL_FULL_DFT.json').write_text(json.dumps({'raw':rr,'state':st,'source':r.packet(),'all_queries':dense_packets},indent=2)+'\n')
dense_cost={'query_count':n,'output_coordinates_written':n,
            'setup_bit_work_upper':r.ledger['total_bit_work_upper'],
            'queries_bit_work_upper':sum(a.ledger['total_bit_work_upper'] for a in dense),
            'exports_bit_work_upper':n*S.EXPORT_BIT_WORK_BOUND,
            'query_and_setup_storage_upper_bits':r.ledger['cumulative_storage_upper_bits']+sum(a.ledger['cumulative_storage_upper_bits'] for a in dense),
            'exports_storage_upper_bits':n*S.EXPORT_STORAGE_BITS_BOUND,
            'destination_serialization_bit_work_upper':S.EXPORT_BIT_WORK_BOUND,
            'destination_storage_upper_bits':S.EXPORT_STORAGE_BITS_BOUND}

# Resource endpoints: maximum length, support, component width and query precision.
n=1<<64;rows=[[j,((1<<1023)+j)|1,-(1<<1023)] for j in range(64)]
rmax=S.execute({'schema':S.SCHEMA,'N':n,'F':-(1<<127),'entries':rows},{'N':n,'B':n,'a':n-1,'beta':n-1},q=1024,p=(1<<127),query_bits=4096)
amax=rmax.query(n-1)
check('endpoint_maximum_domain',rmax.m==64 and len(rmax.entries)==64 and amax.ledger['max_data_integer_bits']<=S.MAX_DATA_BITS)
check('endpoint_normalization',(1<<(2*rmax.h))>=rmax.energy and (1<<(2*rmax.h))<4*rmax.energy)
check('endpoint_serial_radius_not_claimed',not amax.packet()['accepted_serial_radius_compliant'])
rejects('endpoint_required_radius_rejected',lambda:rmax.query(n-1,True))

zero={'schema':S.SCHEMA,'N':16,'F':0,'entries':[]};zs={'N':16,'B':16,'a':1,'beta':0}
z=S.execute(zero,zs)
check('zero_branch',z.status=='EXACT_INPUT_ZERO' and z.descriptor is None and z.policy['p'] is None)
rejects('zero_normalized_query_rejected',lambda:z.query(0))
rejects('zero_precision_rejected',lambda:S.execute(zero,zs,p=100))

for name,mut in [
 ('input_bool',lambda x:x.__setitem__('N',True)),
 ('input_float',lambda x:x['entries'][0].__setitem__(1,1.0)),
 ('unsorted',lambda x:x['entries'].reverse()),
 ('duplicate',lambda x:x['entries'][1].__setitem__(0,1)),
 ('zero_entry',lambda x:x['entries'][0].__setitem__(1,0)),
 ('noncanonical_even',lambda x:[e.__setitem__(1,2) for e in x['entries']]),
 ('outside_index',lambda x:x['entries'][1].__setitem__(0,x['N'])),
 ('width_overflow',lambda x:x['entries'][0].__setitem__(1,1<<1024)),
 ('tuple_rows',lambda x:x.__setitem__('entries',tuple(x['entries']))),
 ('too_many_rows',lambda x:x.__setitem__('entries',[[i,1,0] for i in range(65)])),
 ('nondyadic',lambda x:x.__setitem__('N',12)),
 ('n_cap',lambda x:x.__setitem__('N',1<<65)),
 ]:
    rbad=deepcopy(raw);mut(rbad);rejects(name,lambda rbad=rbad:S.execute(rbad,state,q=464))
for name,kwargs in [('low_p',{'p':1}),('low_q',{'q':1}),('negative_t',{'t':-1}),('precision_cap',{'query_bits':4097}),('p_meta_cap',{'p':1<<128})]:
    rejects(name,lambda kwargs=kwargs:S.execute(raw,state,**kwargs))
sbad=dict(state);sbad['B']=2
rejects('non_singleton_rejected',lambda:S.execute(raw,sbad))
rejects('query_bool',lambda:run.query(True));rejects('query_outside',lambda:run.query(run.N))

for name,edit in [('descriptor_forgery',lambda p:p['descriptor']['entries'][0].__setitem__(1,3)),('root_forgery',lambda p:p['root_table'][-1][0].__setitem__(0,0)),('policy_forgery',lambda p:p['policy'].__setitem__('p',100)),('attestation_forgery',lambda p:p.__setitem__('external_origin_authenticated',True)),('huge_list',lambda p:p.__setitem__('root_table',[0]*257))]:
    packet=run.packet();edit(packet);rejects(name,lambda packet=packet:S.verify(raw,state,16,464,packet))
alt=deepcopy(raw);alt['entries'][0][0]=2;alt_run=S.execute(alt,state,q=464)
rejects('wholly_recomputed_alternative_input',lambda:S.verify(raw,state,16,464,alt_run.packet()))
p=fixture_queries[2]['packet'];forged=deepcopy(p);forged['value_numerators'][0]+=1
rejects('query_forgery',lambda:S.verify_query(raw,state,16,464,17,forged))
rejects('query_index_substitution',lambda:S.verify_query(raw,state,16,464,18,p))
original=run.packet();raw['entries'][0][1]=7;copy=run.packet();copy['descriptor']['entries'][0][1]=9
check('immutable_after_caller_mutation',run.packet()==original)

result={'status':'PASS','named_checks':len(checks),'checks':checks,'independent_small_queries':small_queries,'independent_root_cases':root_cases,
        'actual_theorem_scale_queries':len(fixture_queries),'full_small_DFT_cost':dense_cost,
        'fixture_setup_ledger':run.ledger,'endpoint_query_ledger':amax.ledger,
        'source_sha256':sha256((BASE/'sparse_supplier.py').read_bytes()).hexdigest(),
        'elapsed_seconds':time.perf_counter()-start,'max_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'historical_programs_executed':False,'external_writes':False}
(BASE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(BASE/'EXAMPLE.json').write_text(json.dumps({'source':original,'source_ledger':run.ledger,'queries':fixture_queries},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','fixture_setup_ledger','endpoint_query_ledger')},indent=2))
