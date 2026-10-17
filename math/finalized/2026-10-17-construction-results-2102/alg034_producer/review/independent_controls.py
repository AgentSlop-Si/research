"""Independent exact controls, written after full source inspection.
Only the freshly inspected pinned structured producer is executed.
Historical policy/source bodies are hashed and read as inert data only.
"""
from pathlib import Path
from hashlib import sha256
import ast, copy, importlib.util, itertools, json, math, random, resource, sys, time, tracemalloc
BASE=Path(__file__).resolve().parent
SRC=BASE/'candidate_snapshot'/'structured_producer.py'
EXPECTED='9bbd77a44f8a265f170b1993b63cae71d8f5a8da9f108a85d68b2a7719fca717'
assert sha256(SRC.read_bytes()).hexdigest()==EXPECTED
spec=importlib.util.spec_from_file_location('reviewed_structured_producer',SRC)
P=importlib.util.module_from_spec(spec);sys.modules[spec.name]=P;spec.loader.exec_module(P)
records=[]
def check(name,ok,**details):
    assert ok,name
    records.append({'name':name,'pass':True,**details})
def rejected(name,fn):
    try: fn()
    except P.Failure as e:
        records.append({'name':name,'pass':True,'exception':str(e)})
        return
    raise AssertionError('unexpected acceptance: '+name)
def raw(n,entries,F=0):return {'schema':P.SCHEMA,'N':n,'F':F,'entries':entries}
def state(n,a=1,beta=0):return {'N':n,'B':n,'a':a,'beta':beta}
def independent_period(entries,n):
    # Expanded real 4x4 character matrix; no producer roots or helper reused.
    c=[[0,0] for _ in range(4)]
    for j,a,b in entries:c[4*j//n]=[a,b]
    a,b,c_,d=c
    return ((a[0]+b[0]+c_[0]+d[0],a[1]+b[1]+c_[1]+d[1]),
            (a[0]+b[1]-c_[0]-d[1],a[1]-b[0]-c_[1]+d[0]),
            (a[0]-b[0]+c_[0]-d[0],a[1]-b[1]+c_[1]-d[1]),
            (a[0]-b[1]-c_[0]+d[1],a[1]+b[0]-c_[1]-d[0]))
started=time.perf_counter()
# Read/hash the exact accepted policy body as data, never import historical Python.
antecedent=(BASE/'antecedents'/'accepted_all_length_REPORT.md').read_bytes()
check('accepted_all_length_report_portable_copy_identity',sha256(antecedent).hexdigest()=='86ff070d4e61be4841542390aeac1113e2a81d25188b0072e33d7fc6a851cce0')
tree=ast.parse(SRC.read_bytes())
imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]+[x.name for n in ast.walk(tree) if isinstance(n,ast.Import) for x in n.names]
check('reviewed_imports',sorted(imports)==['dataclasses','hashlib','json'])
check('no_float_literals',not any(isinstance(n,ast.Constant) and isinstance(n.value,float) for n in ast.walk(tree)))
# Exhaust all 6560 nonzero four-axis complex sign patterns at N=4.
count=0
for values in itertools.product((-1,0,1),repeat=8):
    entries=[[j,values[2*j],values[2*j+1]] for j in range(4) if values[2*j] or values[2*j+1]]
    if not entries:continue
    r=P.execute(raw(4,entries),state(4,a=3,beta=2),t=0,q=2)
    assert r.period==independent_period(entries,4)
    assert sum(a*a+b*b for a,b in r.period)==4*sum(a*a+b*b for _,a,b in entries)
    count+=1
check('exhaustive_nonzero_gaussian_sign_patterns_N4',count==6560,cases=count)
# Every admitted even m, random canonical sparse supports and state residues.
rng=random.Random(202610172056)
count=0
for m in range(2,65,2):
    n=2**m
    for repeat in range(10):
        entries=[]
        for axis in range(4):
            if rng.randrange(2):entries.append([axis*(n//4),rng.randrange(-1000,1001),rng.randrange(-1000,1001)])
        entries=[x for x in entries if x[1] or x[2]]
        if not entries:entries=[[0,1,0]]
        entries[0][1]|=1
        F=rng.randrange(-1000,1001); t=rng.randrange(65);q=m+rng.randrange(65)
        r=P.execute(raw(n,entries,F),state(n,2*rng.randrange(n//2)+1,rng.randrange(n)),t=t,q=q)
        A,j=min((abs(a)+abs(b),j) for j,a,b in entries)
        W=max(abs(x).bit_length() for row in entries for x in row[1:]); K=(A-1).bit_length();G=W+(n-1)*K;c=n+3*m+6
        minimum=max(W,c+t+1,c+q+G+2)
        plan=r.policy['plan']
        assert r.period==independent_period(entries,n)
        assert r.policy['p']==minimum and plan['selected_block']==j
        for key,value in {'A':A,'K':K,'G':G,'c':c,'H':1,'I':n+2*m+10,'L':2*n,'D':n,'mu_scale':-F-(n-1)*K}.items():assert plan[key]==value
        assert r.value_exponent==-F-m//2
        assert r.kappa==W-F-minimum and r.pgrid_shift==minimum-W-m//2
        assert r.kappa+r.pgrid_shift==r.value_exponent
        assert r.pgrid_shift>=0
        assert plan['formal_p_grid_numerator_bits_max']==max(abs(x).bit_length() for row in r.period for x in row)+r.pgrid_shift
        assert plan['formal_p_grid_numerator_bits_max']<=minimum+plan['I']
        assert sum(a*a+b*b for a,b in r.period)==4*sum(a*a+b*b for _,a,b in entries)
        # Expansions are permitted only in these independently bounded controls.
        if n<=64:
            assert 2**c==64*min(math.comb(2*n-1,n),2**(n-n))*n*2**n*n*n
            for row in r.period:
                for x in row:assert abs(x<<r.pgrid_shift).bit_length()<=minimum+plan['I']
        count+=1
check('all_even_m_and_exact_policy_grid_norm',count==320,cases=count)
# Actual large-domain producer plus replay, with traced allocation peak.
x,s=P.fixture()
tracemalloc.start();before=time.perf_counter();r=P.execute(x,s);v=P.verify(x,s,16,464,r.packet());elapsed=time.perf_counter()-before;current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
check('actual_N2pow28_execute_and_replay',r.period==((1,0),)*4 and r.value_exponent==-14 and v['status']=='SEMANTICALLY_VERIFIED',seconds=elapsed,tracemalloc_peak_bytes=peak)
check('theorem_scale_exact_policy',r.policy['p']==268436013 and r.kappa==-268436012 and r.pgrid_shift==268435998 and r.policy['plan']['c']==268435546 and r.policy['plan']['formal_p_grid_numerator_bits_max']==268435999)
check('compact_theorem_scale_arithmetic',r.ledger['max_metered_data_integer_bits']==30 and peak<10*1024*1024,ledger=r.ledger)
# Endpoint metadata, raw-width and selected precision, all symbolic.
n=2**64
ext=raw(n,[[0,2**1024-1,-(2**1024-1)],[3*(n//4),-1,1]],F=-(2**128-1))
exts=state(n,n-1,n-1)
er=P.execute(ext,exts,t=0,q=64,p=2**128-1)
check('max_domain_width_precision_negative_F',er.N==n and er.policy['p']==2**128-1 and er.kappa+er.pgrid_shift==er.value_exponent and er.ledger['max_metered_data_integer_bits']<=1026,max_metered_data_integer_bits=er.ledger['max_metered_data_integer_bits'])
ext['F']=2**128-1
er=P.execute(ext,exts,p=2**128-1)
check('positive_F_symbolic_exponents',er.kappa+er.pgrid_shift==er.value_exponent)
# The identity period used downstream forces precisely the delta input.
for F in (-999,0,999):
    xF=raw(2**28,[[0,1,0]],F=F);f=P.execute(xF,s)
    assert f.period==((1,0),)*4 and f.value_exponent-(-F)==-14
    assert f.policy['plan']['accepted_serial_radius_factor']['scale']-(-F)==-466
check('adapter_identity_period_and_alpha',True)
# Reject domain, type, resource and declared-precision violations.
for m in (0,1,3,27,63,65,66):
    n=2**m;rejected('unsupported_m_'+str(m),lambda n=n:P.execute(raw(n,[[0,1,0]]),state(n)))
for n in (-4,0,3,6,17):rejected('unsupported_N_'+str(n),lambda n=n:P.execute(raw(n,[[0,1,0]]),state(n)))
for key,value in [('N',True),('F',False),('F',2**128),('entries',((0,1,0),)),('entries',[[0,1.0,0]]),('entries',[[0,2,2]]),('entries',[[0,0,0]]),('entries',[[0,1,0],[0,3,0]]),('entries',[[2**26,1,0],[0,1,0]]),('entries',[[1,1,0]]),('entries',[[0,2**1024,1]])]:
    bad=copy.deepcopy(x);bad[key]=value;rejected('invalid_raw_'+key+'_'+str(len(records)),lambda bad=bad:P.execute(bad,s))
for key,value in [('N',16),('B',2**28-1),('a',0),('a',2),('a',2**28),('beta',-1),('beta',2**28)]:
    bad=dict(s);bad[key]=value;rejected('invalid_state_'+key+'_'+str(value),lambda bad=bad:P.execute(x,bad))
for kwargs in ({'t':-1},{'q':27},{'p':-1},{'p':268436012},{'p':True},{'q':2**128},{'t':2**128},{'p':2**128},{'t':2**128-1}):rejected('invalid_precision_'+str(kwargs),lambda kwargs=kwargs:P.execute(x,s,**kwargs))
# Explicit larger p needs the separately retained p in semantic replay.
larger=P.execute(x,s,p=r.policy['p']+1)
check('explicit_larger_p_replay',P.verify(x,s,16,464,larger.packet(),p=r.policy['p']+1)['exact_target_certified'])
rejected('caller_precision_cannot_be_substituted',lambda:P.verify(x,s,16,464,larger.packet()))
# Whole-packet recomputation with alternative input OR same target state cannot substitute context.
alt=raw(2**28,[[0,3,0]])
rejected('fully_recomputed_alternative_input',lambda:P.verify(x,s,16,464,P.execute(alt,s).packet()))
altstate=dict(s);altstate['a']=3
rejected('same_target_different_retained_state',lambda:P.verify(x,s,16,464,P.execute(x,altstate).packet()))
for path in [('payload','period'),('payload','value_exponent'),('payload','formal_p_grid'),('policy','exact_error')]:
    bad=r.packet()
    if path[1]=='period':bad[path[0]][path[1]][0][1]=1
    elif path[1]=='value_exponent':bad[path[0]][path[1]]+=1
    elif path[1]=='formal_p_grid':bad[path[0]][path[1]]['common_left_shift']+=1
    else:bad[path[0]][path[1]]['coefficient']=1
    rejected('forgery_'+'.'.join(path),lambda bad=bad:P.verify(x,s,16,464,bad))
bad=r.packet();bad['context']['raw']['entries'][0][1]=True
rejected('boolean_integer_canonical_equality',lambda:P.verify(x,s,16,464,bad))
bad=r.packet();bad['external_origin_authenticated']=True
rejected('self_asserted_authentication',lambda:P.verify(x,s,16,464,bad))
bad=r.packet();bad['payload']['period']=[[0,0]]*129
rejected('packet_list_resource_limit',lambda:P.verify(x,s,16,464,bad))
bad=r.packet();bad['payload']['period'][0][0]=2**4096
rejected('packet_integer_resource_limit',lambda:P.verify(x,s,16,464,bad))
bad=r.packet();bad['policy']['raw_input_sha256']='x'*65536
rejected('packet_string_resource_limit',lambda:P.verify(x,s,16,464,bad))
bad=r.packet();deep=[];deep.append(deep);bad['payload']['period']=deep
rejected('packet_cycle_depth_resource_limit',lambda:P.verify(x,s,16,464,bad))
# Zero is correct and cannot produce a normalized source or caller precision.
z=raw(2**28,[]);zr=P.execute(z,s)
check('canonical_zero_stops_without_payload',zr.status=='EXACT_INPUT_ZERO' and zr.packet()['payload'] is None and zr.period==((0,0),)*4 and not P.verify(z,s,16,464,zr.packet())['exact_target_certified'])
rejected('noncanonical_zero_scale',lambda:P.execute(raw(2**28,[],1),s))
rejected('zero_declared_p',lambda:P.execute(z,s,p=0))
# Post-call mutable views and inputs do not change exact run values.
original=r.packet();x['entries'][0][1]=5;s['beta']=1;view=r.packet();view['payload']['period'][0][0]=8
check('run_isolated_from_mutable_views',r.packet()==original)
check('provenance_boundary_explicit',v['external_origin_authenticated'] is False and v['historical_execution_attested'] is False and r.policy['bit_equivalent_to_rounded_serial'] is False)
result={'status':'PASS_INDEPENDENT_RESTRICTED_PRODUCER_REVIEW_CONTROLS','producer_sha256':EXPECTED,'checks':records,'check_count':len(records),'exact_transform_cases':6560+320,'historical_python_executed':False,'external_writes':False,'elapsed_seconds':time.perf_counter()-started,'maxrss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'theorem_scale_packet':original,'theorem_scale_verification':v,'scope':'Restricted exact ideal-target producer only; no serial-rounded/general-input equivalence; adapter numerical proof remains separate.'}
(BASE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','theorem_scale_packet','theorem_scale_verification')},sort_keys=True))
