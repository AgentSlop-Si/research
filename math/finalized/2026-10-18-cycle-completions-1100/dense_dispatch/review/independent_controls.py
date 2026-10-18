"""New independent controls. Imports production only from frozen reviewed snapshot."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
from dataclasses import replace
import hashlib, json, sys, copy, time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'candidate_snapshot'))
import dense_dispatch as d


def p2(e): return F(1<<e) if e>=0 else F(1,1<<(-e))
def product(a,b):
    t=[x*y for x in a for y in b]
    return min(t),max(t)
def scale(a,b): return product(a,(b,b))
def plus(a,b): return a[0]+b[0],a[1]+b[1]
def minus(a,b): return a[0]-b[1],a[1]-b[0]
def atan(v,n):
    # Independent powers and denominator sum, no production recurrence.
    s=sum((F((-1)**k,(2*k+1)*v**(2*k+1)) for k in range(n)),F(0))
    e=F(1,(2*n+1)*v**(2*n+1))
    return (s,s+e) if n%2==0 else (s-e,s)
def logupper(v):
    if not v:return None
    e=v.numerator.bit_length()-v.denominator.bit_length()
    return e if v<=p2(e) else e+1
def floor(v):return v.numerator//v.denominator
def ceil(v):return -floor(-v)
def root_bound(N,g):
    # Exhaustive integer bisection of z^2 N <= 2^(2g), not isqrt.
    den=1<<g; lo=0; hi=den+1
    while hi-lo>1:
        z=(lo+hi)//2
        if z*z*N<=den*den:lo=z
        else:hi=z
    return F(lo,den),F(lo if lo*lo*N==den*den else hi,den)
CACHE={}
def oracle(N,r):
    key=N,r
    if key in CACHE:return CACHE[key]
    g=r+90
    # pi = 8 atan(1/3)+4 atan(1/7), distinct from both candidate identities.
    # tan(2 atan(1/3))=3/4; tan(2 atan(1/3)+atan(1/7))=1.
    pi=plus(scale(atan(3,g//3+20),F(8)),scale(atan(7,g//3+20),F(4)))
    den=1<<(g+8)
    pi=(F(floor(pi[0]*den),den),F(ceil(pi[1]*den),den))
    assert 3<pi[0]<pi[1]<4
    pc=(pi[0]+pi[1])/2; pr=(pi[1]-pi[0])/2
    root=root_bound(N,g)
    degree=g//2+25
    out=[]
    for j in range(N):
        signed=j if 2*j<=N else j-N
        f=F(2*signed,N); x=f*pc
        # Direct even/odd power sums, no production term recurrence.
        co=sum(((-1)**k*x**(2*k)/factorial(2*k) for k in range(degree+1)),F(0))
        si=sum(((-1)**k*x**(2*k+1)/factorial(2*k+1) for k in range(degree+1)),F(0))
        er=abs(f)*pr+F(4**(2*degree+1),factorial(2*degree+1))
        ei=abs(f)*pr+F(4**(2*degree+2),factorial(2*degree+2))
        out.append((product((co-er,co+er),root),product((-si-ei,-si+ei),root)))
    CACHE[key]=out
    return out


def target_check(raw,r,tag):
    z=d.execute(raw,bits=r)
    tab=oracle(raw['N'],r)
    error=F(0); intervals=[]
    for k,(a,b) in enumerate(z.pairs):
        rr=(F(0),F(0)); ii=(F(0),F(0))
        for j,c,e in z.source.entries:
            wr,wi=tab[j*k%raw['N']]
            rr=plus(rr,minus(scale(wr,F(c)),scale(wi,F(e))))
            ii=plus(ii,plus(scale(wi,F(c)),scale(wr,F(e))))
        rr=scale(rr,p2(-z.source.h)); ii=scale(ii,p2(-z.source.h))
        aa=F(a)*p2(raw['F']-z.source.h-z.denominator_exponent)
        bb=F(b)*p2(raw['F']-z.source.h-z.denominator_exponent)
        error+=max(abs(aa-rr[0]),abs(aa-rr[1]))**2+max(abs(bb-ii[0]),abs(bb-ii[1]))**2
    budget=F(9,256)*p2(-2*r)*z.source.energy*p2(-2*z.source.h)
    assert error<=budget if budget else error==0,tag
    rec=dict(z.receipt)
    assert rec['input_coordinates_read']==len(raw['data'])
    assert rec['output_coordinates_written']==raw['N']
    assert rec['exact_complex_prefix_updates']==(raw['N']*len(z.source.entries) if raw['N']>1 and z.source.energy else 0)
    assert rec['coefficients_certified']==(raw['N'] if raw['N']>1 and z.source.energy else 0)
    assert rec['bookkeeping_width']>rec['numeric_binary_work_bound'].bit_length()
    prefix_detail=None
    if tag=='large_cancellation':
        q=r+(raw['N']-1).bit_length()+4
        ledger=d.Ledger(d.Limits()); table,g=d.coefficients(raw['N'],q,ledger)
        width=z.source.max_component_bits+g+(raw['N']-1).bit_length()+4
        maximum=0; finals=[]; prefixes=0
        for k in range(raw['N']):
            ar=ai=0
            for j,a,b in z.source.entries:
                c,e=table[j*k%raw['N']];ar+=a*c-b*e;ai+=a*e+b*c
                assert max(abs(ar),abs(ai))<1<<(width-1)
                maximum=max(maximum,abs(ar).bit_length(),abs(ai).bit_length());prefixes+=1
            finals.append(max(abs(ar).bit_length(),abs(ai).bit_length()))
        assert maximum>finals[0]+1000
        prefix_detail={'prefixes_independently_rebuilt':prefixes,'signed_allocation_bits':width,'maximum_magnitude_bits':maximum,'zero_row_final_bits':finals[0],'extra_coefficient_table_receipt':dict(ledger.receipt())}
    return z,{'tag':tag,'N':raw['N'],'bits':r,'rows_checked':len(z.pairs),
              'strong_3_over_16_norm_bound_pass':True,'receipt':rec,'independent_prefix_control':prefix_detail,
              'squared_error_over_strong_budget_upper_power_two':logupper(error/budget) if budget else None}

def reject(raw,reason,**kwargs):
    try:d.execute(raw,**kwargs)
    except d.Rejected as e:
        assert e.reason==reason,(e.reason,reason)
        assert dict(e.receipt)['output_coordinates_written']==0
        return {'reason':reason,'receipt':dict(e.receipt)}
    raise AssertionError('missing rejection '+reason)

def main():
    started=time.monotonic(); runs=[]; reversals=[]; coefficient_runs=[]
    for N,r in [(1,0),(2,0),(3,0),(4,7),(5,19),(7,31),(10,7),(11,0),(19,13),(6,128)]:
        raw={'N':N,'F':N%5-2,'kind':'dense','data':[[(-1)**j*(4*j+1),3*j-2] for j in range(N)]}
        _,q=target_check(raw,r,'dense_'+str(N));runs.append(q)
    fixtures=[
      ({'N':7,'F':9,'kind':'sparse','data':[[1,1,2],[4,-7,3],[6,3,-4]]},0,'sparse_n7'),
      ({'N':9,'F':-(83),'kind':'dense','data':[[2**1023+1,-2**1022],[-2**1023,2**1022+1]]+[[0,0]]*7},23,'large_cancellation'),
      ({'N':5,'F':2**120+17,'kind':'sparse','data':[[2,3,4]]},17,'symbolic_positive_scale'),
      ({'N':4,'F':-8198,'kind':'sparse','data':[[1,1,0]]},0,'max_physical_shift'),
      ({'N':1,'F':-8192,'kind':'sparse','data':[[0,1,0]]},0,'singleton_max_shift'),
      ({'N':13,'F':0,'kind':'dense','data':[[0,0] for _ in range(13)]},128,'zero'),
      ({'N':4,'F':0,'kind':'sparse','data':[[1,1,0]]},24,'target_separation')]
    separated=None
    for raw,r,tag in fixtures:
        z,q=target_check(raw,r,tag);runs.append(q)
        if tag=='target_separation':separated=z
    endpoint_raw={'N':128,'F':0,'kind':'dense','data':[[1,(-1)**j] for j in range(128)]}
    endpoint=d.execute(endpoint_raw,bits=128); root=root_bound(2,240); endpoint_error=F(0)
    assert endpoint.source.h==4
    for k,(a,b) in enumerate(endpoint.pairs):
        aa=F(a)*p2(-endpoint.denominator_exponent-4);bb=F(b)*p2(-endpoint.denominator_exponent-4)
        endpoint_error+=(max(abs(aa-root[0]),abs(aa-root[1]))**2 if k==0 else aa*aa)
        endpoint_error+=(max(abs(bb-root[0]),abs(bb-root[1]))**2 if k==64 else bb*bb)
    assert endpoint_error<=F(9,256)*p2(-256)
    er=dict(endpoint.receipt)
    assert er['input_coordinates_read']==128 and er['output_coordinates_written']==128 and er['exact_complex_prefix_updates']==128**2
    runs.append({'tag':'N_and_precision_endpoint_two_mode_analytic_target','N':128,'bits':128,'rows_checked':128,'strong_3_over_16_norm_bound_pass':True,'receipt':er,'squared_error_over_strong_budget_upper_power_two':logupper(endpoint_error/(F(9,256)*p2(-256)))})
    for N in [1,3,12,27,128]:
        raw={'N':N,'F':-(2**125+1),'kind':'dense','data':[[2*j+1,(-1)**j*(j+1)] for j in range(N)]}
        z=d.execute(raw,target='SINGLETON_SECOND_NORMALIZED',B_A=N)
        assert z.pairs==tuple(tuple(raw['data'][(-k)%N]) for k in range(N))
        assert z.denominator_exponent==z.source.h
        assert z.alpha_exponent==z.source.h-raw['F']
        assert dict(z.receipt)['coefficients_certified']==0
        assert dict(z.receipt)['output_coordinates_written']==N
        reversals.append({'N':N,'exact_reversed_rows':N,'receipt':dict(z.receipt)})
    sepraw={'N':4,'F':0,'kind':'sparse','data':[[1,1,0]]}
    rev=d.execute(sepraw,target='SINGLETON_SECOND_NORMALIZED',B_A=4)
    assert sum((F(a)*p2(-separated.denominator_exponent)-F(c)*p2(-rev.denominator_exponent))**2+
               (F(b)*p2(-separated.denominator_exponent)-F(e)*p2(-rev.denominator_exponent))**2
               for (a,b),(c,e) in zip(separated.pairs,rev.pairs))==2
    for N,q in [(3,5),(8,14),(11,37)]:
        L=d.Ledger(d.Limits()); table,g=d.coefficients(N,q,L); tab=oracle(N,q)
        for (a,b),(rr,ii) in zip(table,tab):
            dr=max(abs(F(a,1<<g)-x) for x in rr)
            di=max(abs(F(b,1<<g)-x) for x in ii)
            assert dr*dr+di*di<=p2(-2*q)
        coefficient_runs.append({'N':N,'q':q,'all_complex_certificates_independently_checked':True,'receipt':dict(L.receipt())})
    plans=[]
    for power in [1,7,21,44,70,126]:
        N=1<<power; m=power+2; M=4*N; D=max(5,ceil(F(M-4,32*m)))
        raw={'N':N,'F':0,'kind':'sparse','data':[[N-1,1,0]]}
        info,receipt=d.plan(raw,D=D); info=dict(info)
        assert not info['outer_structural_sparse_guard']
        assert info['route']=='CERTIFIED_DIRECT_DFT' and not info['same_target_sparse_provider_bound']
        assert dict(receipt)['output_coordinates_written']==0
        plans.append({'N':N,'D':D,'classification':info,'receipt':dict(receipt)})
    for s in [0,1,16,17]:
        raw={'N':1<<28,'F':0,'kind':'sparse','data':[[j,1,0] for j in range(s)]}
        info,rec=d.plan(raw); info=dict(info)
        assert info['legacy_recovery_source_domain']==(1<=s<=16)
        assert info['outer_structural_sparse_guard'] and not info['same_target_sparse_provider_bound']
        assert info['reason']=='NO_BOUND_SAME_TARGET_SPARSE_PROVIDER'
        plans.append({'support':s,'classification':info,'receipt':dict(rec)})
    raw={'N':3,'F':2,'kind':'dense','data':[[1,0],[-2,1],[0,0]]}
    z=d.execute(raw,bits=8); replays=[]
    ok,replay,compare=d.verify(raw,z,bits=8);assert ok
    replays.append({'case':'valid','equal':ok,'replay_receipt':dict(replay),'comparison_receipt':dict(compare)})
    mutations=[('output',raw,replace(z,pairs=z.pairs[:-1]+((z.pairs[-1][0]+1,z.pairs[-1][1]),))),
               ('target',raw,replace(z,target='SINGLETON_SECOND_NORMALIZED')),
               ('scale',dict(raw,F=3),z),
               ('source',dict(raw,data=[[3,0],[-2,1],[0,0]]),z),
               ('representation',{'N':3,'F':2,'kind':'sparse','data':[[0,1,0],[1,-2,1]]},z)]
    class EqInt(int):
        def __eq__(self,other):return True
    class EqResult(d.Result):
        def __eq__(self,other):return True
    forged=EqResult(z.source,z.target,((314159,0),)*3,z.denominator_exponent,z.requested_bits,z.dispatch,z.receipt,z.alpha_exponent)
    mutations.extend([('forged_result_subclass',raw,forged),('forged_scalar_subclass',raw,replace(z,pairs=((EqInt(314159),0),)+z.pairs[1:]))])
    for tag,original,result in mutations:
        ok,rr,cr=d.verify(original,result,bits=8);assert not ok,tag
        replays.append({'case':tag,'equal':ok,'replay_receipt':dict(rr),'comparison_receipt':dict(cr)})
    saved=z.source.entries;raw['data'][0][0]=99;assert z.source.entries==saved
    base={'N':4,'F':0,'kind':'sparse','data':[[0,1,0]]}
    rejects=[]
    cases=[(dict(base,F=-8199),{'bits':0},'MATERIALIZED_OUTPUT_SHIFT_LIMIT'),
           (dict(base,N=129),{},'DENSE_ALLOCATION_LIMIT'),
           (base,{'target':'SINGLETON_SECOND_NORMALIZED'},'SINGLETON_BLOCK_BINDING_REQUIRED'),
           (base,{'B_A':2},'GENERAL_BLOCK_SOURCE_NOT_IMPLEMENTED'),
           (base,{'bits':True},'PRECISION_DOMAIN'),
           (base,{'target':'FAST'},'UNKNOWN_TARGET'),
           (base,{'D':4},'D_DOMAIN'),
           (dict(base,data=[[0,True,0]]),{},'EXACT_INTEGER_REQUIRED'),
           (dict(base,data=[[0,EqInt(1),0]]),{},'EXACT_INTEGER_REQUIRED'),
           (dict(base,data=[[0,0,0]]),{},'EXPLICIT_SPARSE_ZERO'),
           (dict(base,data=[[1,1,0],[1,-1,0]]),{},'SOURCE_INDEX_ORDER'),
           (dict(base,data=[[0,2,0]]),{},'NONCANONICAL_COMMON_GRID'),
           (base,{'limits':d.Limits(max_events=40)},'ARITHMETIC_EVENT_LIMIT'),
           (base,{'limits':d.Limits(max_numeric_bits=100)},'NUMERIC_WIDTH_LIMIT')]
    for data,kw,reason in cases:rejects.append(reject(data,reason,**kw))
    malformed={str(i):i for i in range(20000)}
    rejects.append(reject(malformed,'SOURCE_GRAMMAR'))
    failed_comparisons=[]
    one={'N':1,'F':0,'kind':'sparse','data':[[0,1,0]]}
    for cap in [12,16,24,32]:
        lim=d.Limits(max_events=cap);original=d.execute(one,bits=0,limits=lim)
        try:d.verify(one,original,bits=0,limits=lim)
        except d.Rejected as e:
            assert e.reason=='ARITHMETIC_EVENT_LIMIT'
            assert e.prior_receipts==(original.receipt,)
            stages=e.prior_receipts+(e.receipt,)
            failed_comparisons.append({'case':'comparison_cap_'+str(cap),'completed_replay_receipt':dict(e.prior_receipts[0]),'comparison_prefix_receipt':dict(e.receipt),'total_fresh_verification_work':sum(dict(x)['total_binary_work_bound'] for x in stages),'total_fresh_verification_cumulative_storage':sum(dict(x)['cumulative_storage_bit_bound'] for x in stages),'separate_original_execution_receipt':dict(original.receipt)})
        else:raise AssertionError('missing comparison cap rejection')
    empty=d.Result.__new__(d.Result)
    try:d.verify(one,empty,bits=0)
    except d.Rejected as e:
        assert e.reason=='RESULT_TREE_GRAMMAR' and len(e.prior_receipts)==1
        failed_comparisons.append({'case':'missing_result_fields','completed_replay_receipt':dict(e.prior_receipts[0]),'comparison_prefix_receipt':dict(e.receipt)})
    else:raise AssertionError('missing result grammar rejection')
    huge=-(1<<1000000)
    for data,reason in [(dict(base,F=huge),'SOURCE_METADATA_LIMIT'),(dict(base,data=[[0,huge,1]]),'SOURCE_COMPONENT_LIMIT')]:
        probe=reject(data,reason);assert probe['receipt']['arithmetic_records']>0;rejects.append(probe)
    text,ex=d.export(z);assert json.loads(text)['pairs']==[list(row) for row in z.pairs]
    assert ex['export_bytes']==len(text.encode()) and ex['binary_work_bound']>0
    out={'status':'PASS_INDEPENDENT_FRESH_CONTROLS','candidate_source_sha256':hashlib.sha256((ROOT/'candidate_snapshot/dense_dispatch.py').read_bytes()).hexdigest(),
         'direct_runs':runs,'reversal_runs':reversals,'independent_coefficient_runs':coefficient_runs,
         'plans':plans,'semantic_replays':replays,'separate_replay_original_receipt':dict(z.receipt),'paid_rejections':rejects,'failed_comparison_controls':failed_comparisons,'export_receipt':ex,'target_separation_reversal_receipt':dict(rev.receipt),
         'target_separation_squared_distance':'2','counts':{'direct_runs':len(runs),'direct_rows':sum(x['rows_checked'] for x in runs),
           'reversal_runs_including_separation_control':len(reversals)+1,'reversal_rows_including_separation_control':sum(x['exact_reversed_rows'] for x in reversals)+4,
           'coefficient_tables':len(coefficient_runs),'coefficients':sum(x['N'] for x in coefficient_runs),
           'plans':len(plans),'semantic_replay_executions':len(replays),'semantic_replay_rows':3*len(replays),'rejections':len(rejects),'failed_comparisons_with_complete_replay':len(failed_comparisons),'additional_prefix_coefficient_tables':1,'additional_prefix_coefficients':9,'all_completed_first_dft_executions':len(runs)+1+len(replays)+9,'all_completed_first_dft_rows':sum(x['rows_checked'] for x in runs)+3+3*len(replays)+9},
         'elapsed_seconds':time.monotonic()-started,'oracle':'Exact independent pi = 8 atan(1/3) + 4 atan(1/7), direct even/odd power sums, separate integer-bisection normalization; no author test helper imported.'}
    (ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'counts':out['counts'],'elapsed_seconds':out['elapsed_seconds']},indent=2))
if __name__=='__main__':main()
