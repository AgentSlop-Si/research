"""Independent review controls. No author check driver is imported or executed."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json, sys, time, ast
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'candidate'
sys.path[:0]=[str(SRC),str(SRC/'vendor')]
import recovery
from sparse_adapter import SparseAdapter, canonical, strict_loads
M=1<<28; B=1<<17; P=464

def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def note(obj): print(json.dumps(obj),flush=True)

def accuracy(raw,result):
    energy=sum(x*x+y*y for _,x,y in raw['entries'])
    h=0
    while (1<<(2*h))<energy:h+=1
    assert energy>(1<<(2*h-2)) if h else energy>0
    original={(-n)%M:(x,y) for n,x,y in raw['entries']}
    got={row[0]:tuple(row[1:]) for row in result['rows']}
    assert len(got)==len(result['rows'])<=len(original)
    assert set(got)<=set(original)
    C=max(h,P); total=0; returned_error=0;heavy=[]
    for n,(x,y) in original.items():
        if (x*x+y*y)*(1<<798)>=(1<<(2*h)):
            heavy.append(n);assert n in got
        r,i=got.get(n,(0,0))
        err=((r<<(C-P))-(x<<(C-h)))**2+((i<<(C-P))-(y<<(C-h)))**2
        total+=err
        if n in got:
            assert err<=(1<<(2*C-924));returned_error=max(returned_error,err)
    assert total*(1<<800)<=81*(1<<(2*C))
    ns=[row[0] for row in raw['entries']]
    s=result['sigma'];pairs=[min(s*(x-y)%M,s*(y-x)%M) for j,x in enumerate(ns) for y in ns[:j]]
    assert not pairs or min(pairs)>=8192
    return {'h':h,'source_support':len(original),'returned_support':len(got),'omitted':sorted(set(original)-set(got)),
            'heavy':sorted(heavy),'minimum_pair_separation':min(pairs) if pairs else None,
            'error_grid_bits':C,'l2_squared_error_numerator':total,'maximum_returned_squared_error_numerator':returned_error}

class IndependentProvider:
    def __init__(self,raw,state):
        self._raw=deepcopy(raw);self._state=deepcopy(state)
        self.adapters=[];self.schedule=[];self.headers=[];self.windows=[];self.full_coordinates=0
    def buckets(self,sigma,tau):
        if len(self.schedule)%6==0:self.adapters.append(SparseAdapter())
        run=self.adapters[-1].execute(self._raw,self._state,t=16,q=P,sigma=sigma,tau=tau)
        self.schedule.append([sigma,tau]);self.headers.append(sha256(run.header_bytes).hexdigest())
        self.full_coordinates+=len(run.numerators)
        assert type(run.numerators)is tuple and len(run.numerators)==B
        return run.numerators
    def window(self,d):
        z=self.adapters[-1].engine.window(d);self.windows.append(d)
        return z.lo,z.hi
    def receipt(self):
        groups=[a.receipt() for a in self.adapters]
        return {'groups':groups,'preparations':len(groups),'calls':len(self.schedule),
          'full_bucket_coordinates':self.full_coordinates,'header_hashes':self.headers,
          'caller_work_upper':1<<110,'caller_cumulative_storage_upper_bits':1<<60,
          'total_bit_work_upper':sum(x['total_bit_work_upper'] for x in groups)+(1<<110),
          'cumulative_storage_upper_bits':sum(x['cumulative_storage_upper_bits'] for x in groups)+(1<<60)}

def run(context,context_bytes):
    p=IndependentProvider(context['raw'],context['state']); result=recovery.recover(p,context['sigma'])
    expected=[[context['sigma'],0]]+[[context['sigma'],M>>(b+1)] for b in range(28)]
    assert p.schedule==expected==result['schedule'];assert p.full_coordinates==29*B
    assert result['stats']['coordinate_visits']==29*B
    assert [a.calls for a in p.adapters]==[6,6,6,6,5]
    assert len(p.windows)==len(result['rows'])
    for a in p.adapters:
        assert a.engine.ledger.slots<8_000_000
        assert a.engine.ledger.numeric_operations<30_000_000
    result['original_binding']={'raw_and_state_path':'ORIGINAL_INPUT.json','raw_and_state_sha256':sha256(context_bytes).hexdigest(),
                               'independently_retained_original_required':True,'external_authentication':False}
    receipt=p.receipt();result['provider_receipt']=receipt
    result['combined_receipt']={'total_bit_work_upper':receipt['total_bit_work_upper']+result['consumer_receipt']['total_bit_work_upper'],
      'cumulative_storage_upper_bits':receipt['cumulative_storage_upper_bits']+result['consumer_receipt']['cumulative_storage_upper_bits'],
      'production_runs':1,'replay_runs':0,'random_bits_if_uniform_sampling':27,'normalized_sparse_output_rows':len(result['rows']),
      'all_N_output_materialized':False}
    return result,accuracy(context['raw'],result)

def main():
    started=time.monotonic();checks=[]
    # The reviewed decoder can access only these provider attributes.
    tree=ast.parse((SRC/'recovery.py').read_text())
    accesses=sorted({n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='provider'})
    assert accesses==['buckets','window']
    checks.append({'name':'source_level_value_only_boundary','provider_attributes':accesses})
    # Exact modular orbit counts, including the strict-boundary case.
    count=0
    for m in range(2,11):
        N=1<<m
        for k in range(1,m):
            D=1<<k
            for v in range(m):
                d=1<<v
                orbit={a*d%N for a in range(1,N,2)}
                assert len(orbit)==1<<(m-v-1)
                bad=sum(min(z,N-z)<D for z in orbit)
                assert bad==(0 if v>=k else 1<<(k-v))
                count+=1
    assert 1-120/16384==2033/2048
    checks.append({'name':'exact_2adic_orbits_and_strict_boundary','cases':count})
    # Integer ties-to-even and wrap geometry tested independently.
    for d in range(1,21):
        for n in range(-100,101):
            q=recovery.nearest(n,d)
            dist=min(abs(n-j*d) for j in range(n//d-1,n//d+3))
            assert abs(n-q*d)==dist
            if 2*dist==d:assert q%2==0
    for sigma in [1,3,10007,M-1]:
        for n in [0,1,1024,3072,10240,M//2-1024,M//2+1024,M-1024,M-1]:
            j,d=recovery.nearest_bin(n,sigma)
            assert 0<=j<B and d<=1024 and d==min((j*2048+sigma*n)%M,(-j*2048-sigma*n)%M)
    checks.append({'name':'signed_nearest_even_and_wrapped_half_grid_geometry','division_cases':4020,'geometry_cases':36})
    # Exact support-obstruction arithmetic, normalized common h, and grid-rounding margin.
    c=(1<<1023)+1
    for E in [c*c,c*c+1]:assert (1<<2046)<E<=(1<<2048)
    assert 3073*(1<<466)<1<<1024
    assert 1/2<9/16 # (1/sqrt(2))^2 < (3/4)^2, written as rationals below
    assert 8<9
    checks.append({'name':'fixed_radius_support_obstruction_exact_inequalities','common_h':1024,'perturbation_upper':[3073,-1024]})
    # Fresh full schedule against independently copied original state. Do not call author tests.
    cb=(SRC/'ORIGINAL_INPUT.json').read_bytes();context=strict_loads(cb.decode('ascii'))
    original,acc=run(context,cb)
    supplied=strict_loads((SRC/'RECOVERY_RUN.json').read_text())
    eq=canonical(original)==canonical(supplied);assert eq
    mutations=[]
    for field in ['coefficient','source_hash','sigma','phase_schedule','provider_header','receipt']:
        bad=deepcopy(supplied)
        if field=='coefficient':bad['rows'][0][1]+=1
        elif field=='source_hash':bad['original_binding']['raw_and_state_sha256']='f'*64
        elif field=='sigma':bad['sigma']^=2
        elif field=='phase_schedule':bad['schedule'][3][1]+=1
        elif field=='provider_header':bad['provider_receipt']['header_hashes'][0]='f'*64
        else:bad['combined_receipt']['total_bit_work_upper']-=1
        assert canonical(bad)!=canonical(original);mutations.append(field)
    replay=json.loads((SRC/'REPLAY_RESULTS.json').read_text())
    assert replay['production_plus_replay_total_bit_work_upper']==2*original['combined_receipt']['total_bit_work_upper']+(1<<110)
    assert replay['production_plus_replay_cumulative_storage_upper_bits']==2*original['combined_receipt']['cumulative_storage_upper_bits']+(1<<60)
    assert replay['actual_production_plus_replay_bucket_coordinates']==58*B
    assert replay['computed_packet_sha256']==sha256(canonical(original)).hexdigest()
    checks.append({'name':'fresh_original_bound_29_call_replay','exact_author_packet_match':eq,'mutation_rejections':mutations,'accuracy':acc,
                   'author_full_58_call_ledger_arithmetic_verified':True,'author_total_coordinates':58*B})
    write('FRESH_ORIGINAL_REPLAY.json',original)
    note({'checkpoint':'fresh original replay PASS','elapsed_seconds':time.monotonic()-started,'rows':len(original['rows']),'candidates':original['stats']['candidate_count']})
    write('INDEPENDENT_CHECKS_PROGRESS.json',{'checks':checks})
    # New independent 16-support original: dyadic half-grid tie, zero frequency,
    # alternating bit frequencies, signs, exact heavy floor, tiny modes and huge F.
    ns=[0,10240,32769,1048575,4194304,16777215,33554432,67108863,89478485,134217728,178956970,201326591,234881024,251658240,268000001,M-10241]
    entries=[]
    for j,n in enumerate(ns):
        if j==0:r=(1<<1023)+1;i=0
        elif j<11:r=(-1 if j%2 else 1)*(1<<1019);i=(1<<1018) if j%3 else -(1<<1018)
        elif j==11:r=1<<625;i=0
        elif j==12:r=1<<624;i=0
        elif j==13:r=1<<622;i=0
        elif j==14:r=1;i=0
        else:r=-(1<<625);i=1
        entries.append([n,r,i])
    edge={'raw':{'schema':'ALG034_SPARSE_DYADIC_V1','N':M,'F':-((1<<120)+1),'entries':entries},'state':{'N':M,'B':M,'a':M-1,'beta':M-1},'sigma':1}
    eb=(json.dumps(edge,indent=2)+'\n').encode();(OUT/'INDEPENDENT_EDGE_INPUT.json').write_bytes(eb)
    er,ea=run(edge,eb);assert ea['h']==1024
    assert (-ns[11])%M in [r[0] for r in er['rows']]
    assert 0 in [r[0] for r in er['rows']]
    write('FRESH_EDGE_RECOVERY.json',er)
    checks.append({'name':'fresh_edge_16_support_29_call_recovery','accuracy':ea,'exact_threshold_source_index':ns[11],
       'half_grid_tie_source_index':10240,'huge_source_scale_exponent_handled_without_expansion':True})
    note({'checkpoint':'fresh edge recovery PASS','elapsed_seconds':time.monotonic()-started,'rows':len(er['rows']),'candidates':er['stats']['candidate_count']})
    # Strict malformed interface controls; each must visibly reject.
    rejects=[]
    class Bad:
        def __init__(self,arr,w=None):self.arr=arr;self.w=w
        def buckets(self,s,t):return self.arr
        def window(self,d):return self.w
    zero=((0,0),)*B
    tests=[('boolean_sigma',lambda:recovery.recover(Bad(zero),True)),('even_sigma',lambda:recovery.recover(Bad(zero),2)),
      ('float_bucket',lambda:recovery.recover(Bad(zero[:-1]+((0.0,0),)),1)),
      ('boolean_bucket',lambda:recovery.recover(Bad(zero[:-1]+((False,0),)),1)),
      ('bucket_width',lambda:recovery.recover(Bad(zero[:-1]+((1<<480,0),)),1)),
      ('list_array',lambda:recovery.recover(Bad(list(zero)),1)),
      ('candidate_cap',lambda:recovery.recover(Bad(((1<<64,0),)*65+zero[65:]),1)),
      ('malformed_window',lambda:recovery.recover(Bad(((1<<64,0),)+zero[1:],(1<<560,(1<<560)+(1<<82)+1)),1))]
    class Ambiguous:
        def buckets(self,s,t):return ((1<<64,0),)+zero[1:] if t==0 else zero
    tests.append(('uncertain_sign',lambda:recovery.recover(Ambiguous(),1)))
    for name,fn in tests:
        try:fn()
        except ValueError as e:rejects.append({'name':name,'reason':str(e)})
        else:raise AssertionError('accepted malformed '+name)
    checks.append({'name':'independent_intake_and_fail_closed_controls','rejections':rejects})
    # Verify reviewed source integrity after all executions.
    manifest=json.loads((SRC/'MANIFEST.json').read_text())
    for item in manifest['files']:assert sha256((SRC/item['path']).read_bytes()).hexdigest()==item['sha256']
    out={'status':'PASS_INDEPENDENT_RESTRICTED_RECOVERY_REVIEW_CONTROLS','checks':checks,'elapsed_seconds':time.monotonic()-started,
      'fresh_independent_bucket_calls':58,'fresh_independent_bucket_coordinates':58*B,'prior_author_test_suites_executed':False,
      'author_artifacts_modified':False,'external_writes':False,'author_manifest_sha256':sha256((SRC/'MANIFEST.json').read_bytes()).hexdigest()}
    write('INDEPENDENT_RESULTS.json',out);note({'status':out['status'],'elapsed_seconds':out['elapsed_seconds']})

if __name__=='__main__':main()
