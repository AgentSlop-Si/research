"""Fresh live original-input-bound integration and semantic replay controls."""
from pathlib import Path
import sys,json,time,copy,hashlib
from collections import Counter
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from sparse_adapter import *
checks=Counter();start=time.monotonic()
def check(n,b):
    if not b:raise AssertionError(n)
    checks[n]+=1
def reject(n,fn,reason=None):
    try:fn()
    except (Failure,ValueError,ArithmeticError) as e:
        if reason and reason not in str(e):raise AssertionError(n+' wrong rejection '+str(e))
        checks[n]+=1
    else:raise AssertionError('unexpected acceptance '+n)
adapter=SparseAdapter();raw,state=adapter.producer.fixture()
run=adapter.execute(raw,state);packet=run.packet();header=json.loads(run.header_bytes)
check('live producer exact nonquarter source',header['producer']['descriptor']['entries']==[[1,1,0],[3,1,0]] and header['producer']['policy']['outcome']=='NONZERO_EXACT_MODAL_SOURCE')
check('actual complete full output',len(run.numerators)==131072 and type(run.numerators)is tuple)
check('actual nonconstant complex output',any(im for _,im in run.numerators))
check('original context retained',header['producer']['context']['raw']==raw and header['producer']['context']['state']==state)
check('exact norm squared half',header['source']['normalized_norm_squared']=={'numerator':2,'denominator_power_two':2})
check('formal normalized radius valid',header['source']['formal_policy_radius_over_alpha']['scale']<=-464)
check('exact representation zero error',header['source']['source_representation_error']==0)
check('full recovery correctly unproved',not header['downstream']['full_recovery_executed'] and not header['downstream']['outer_transfer_and_t_guard_proved'] and not header['downstream']['legacy_rounded_execution'])
check('full fresh semantic replay',adapter.verify(raw,state,16,464,packet)['bound_to_separately_supplied_original_input'])
for label,mut in [('changed final output',lambda p:p['bucket_numerators'][-1].__setitem__(1,0)),('forged original descriptor',lambda p:p['producer']['descriptor']['entries'][0].__setitem__(0,2)),('forged recovery claim',lambda p:p['downstream'].__setitem__('full_recovery_executed',True))]:
    bad=copy.deepcopy(packet)
    if label=='changed final output':bad['bucket_numerators'][-1][1]+=1
    else:mut(bad)
    reject('packet '+label,lambda p=bad:adapter.verify(raw,state,16,464,p),'SEMANTIC_MISMATCH')
newraw=copy.deepcopy(raw);newraw['entries'][0][0]=2
reject('separate changed original support',lambda:adapter.verify(newraw,state,16,464,packet),'SEMANTIC_MISMATCH')
newstate={**state,'beta':1}
reject('separate changed original ALG state',lambda:adapter.verify(raw,newstate,16,464,packet),'SEMANTIC_MISMATCH')
reject('separate changed BUCKETS phase',lambda:adapter.verify(raw,state,16,464,packet,tau=18),'SEMANTIC_MISMATCH')
# Exact modal consumption does not claim any finite query precision. A deliberately
# coarse, nonaccepted-radius query setup still describes the same exact source.
coarse=adapter.execute(raw,state,query_bits=8)
check('exact descriptor independent of point-query precision',coarse.numerators==run.numerators)
source=adapter.producer.execute(raw,state,query_bits=8)
reject('coarse point query cannot claim accepted radius',lambda:source.query(1,require_accepted_radius=True),'PRECISION')
source_default=adapter.producer.execute(raw,state)
query=source_default.query(1,require_accepted_radius=True).packet()
check('separately paid genuine nonquarter point query',query['accepted_serial_radius_compliant'] and query['nonquarter_phase_terms']==2)
scaled={**raw,'F':(1<<126)-1};scale_run=adapter.execute(scaled,state)
check('large exact scale cancellation',scale_run.numerators==run.numerators and json.loads(scale_run.header_bytes)['source']['alpha']['scale']==1-scaled['F'])
shifted=adapter.execute(raw,state,sigma=135791,tau=35791)
check('genuine nonconstant schedule response',shifted.numerators!=run.numerators)
# Caller mutation after execution cannot alter original context or returned values.
raw['entries'][0][0]=2
check('caller mutation isolation',json.loads(run.header_bytes)['producer']['context']['raw']['entries'][0][0]==1)
raw['entries'][0][0]=1
reject('unsupported zero original',lambda:adapter.execute({**raw,'entries':[]},state),'UNSUPPORTED_STRUCTURE')
reject('unsupported support beyond bounded adapter',lambda:adapter.execute({**raw,'entries':[[j,1,0] for j in range(17)]},state),'UNSUPPORTED_STRUCTURE')
reject('unsupported non-theorem length',lambda:adapter.execute({'schema':raw['schema'],'N':256,'F':0,'entries':[[1,1,0]]},{'N':256,'B':256,'a':1,'beta':0}),'UNSUPPORTED_STRUCTURE')
class Trap:
    def __eq__(self,o):raise AssertionError('untrusted equality hook')
    def __iter__(self):raise AssertionError('untrusted iteration hook')
for obj in (Trap(),[Trap()],{'x':Trap()}):reject('canonical exact-type rejection',lambda v=obj:canonical(v),'GRAMMAR')
for text in ('{"x":1,"x":2}','{"x":1.0}','{"x":Infinity}','[[[[[[[[[[[[[[[[[[0]]]]]]]]]]]]]]]]]]'):
    reject('strict JSON intake',lambda s=text:strict_loads(s))
reject('serialized integer cap',lambda:canonical({'x':1<<12288}),'RESOURCE_LIMIT')
receipt=adapter.receipt(additional_packet_exports=1,additional_json_parses=4)
check('all output writes paid',receipt['numerical']['operations']['bucket_output']==receipt['successful_calls']*131072)
check('scalar preparation paid exactly once',receipt['numerical']['operations']['phi_evaluation']==5631)
check('declared numeric cap',receipt['numerical']['numeric_operations']<=30000000)
check('declared allocation cap',receipt['numerical']['allocated_slots']<=8000000)
check('bounded numeric width',receipt['numerical']['max_integer_bits']<=20000)
check('supplier full source loading charged',receipt['numerical']['source_bytes']>len((HERE/'nonconstant_buckets.py').read_bytes()))
check('no phantom FFT work',receipt['actual_FFT_roots']==receipt['actual_FFT_butterflies']==0)
check('copy/export and producer charges included',receipt['total_bit_work_upper']>receipt['numerical']['total_bit_work_upper']+receipt['producer_bit_work_upper'])
check('pinned fresh supplier source',hashlib.sha256((HERE/'vendor'/'sparse_supplier.py').read_bytes()).hexdigest()==PRODUCER_PIN)
report={'status':'PASS_FRESH_NONCONSTANT_LIVE_INTEGRATION','assertions':sum(checks.values()),'checks':dict(checks),
        'elapsed_seconds':time.monotonic()-start,'receipt':receipt,'producer_source_sha256':PRODUCER_PIN,
        'fixture_header':header,'point_query_example':query,'scope':'exact sparse-original family at genuine window parameters; full recovery/outer transfer/serial-rounding equivalence unproved'}
(HERE/'INTEGRATION_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
# One complete full-output example, not a truncated or implicit-zero surrogate.
(HERE/'NONCONSTANT_FIXTURE_PACKET.json').write_bytes(canonical(packet)+b'\n')
print(json.dumps({k:report[k] for k in ('status','assertions','elapsed_seconds')},indent=2),flush=True)
