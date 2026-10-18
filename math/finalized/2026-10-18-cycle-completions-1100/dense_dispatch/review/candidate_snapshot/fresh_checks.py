"""Fresh checks of new dispatch/reference only; no predecessor tests run."""
from fractions import Fraction as Q
from math import factorial
from dataclasses import replace
from pathlib import Path
import hashlib, json, time, copy
from dense_dispatch import execute, plan, export, verify, Limits, Rejected

ROOT=Path(__file__).resolve().parent


def p2(e):
    return Q(1<<e) if e>=0 else Q(1,1<<-e)


def atan_bounds(q,n):
    v=sum((Q((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(n)),Q(0))
    r=Q(1,(2*n+1)*q**(2*n+1))
    return (v,v+r) if n%2==0 else (v-r,v)


def interval_mul(a,b):
    t=[x*y for x in a for y in b]
    return min(t),max(t)


def inverse_sqrt_interval(N,g):
    # Independent integer bisection, no production isqrt or root helper.
    D=1<<g; lo,hi=0,D+1; target=D*D
    while hi-lo>1:
        m=(lo+hi)//2
        if m*m*N<=target:lo=m
        else:hi=m
    return Q(lo,D),Q(lo,D) if lo*lo*N==target else Q(hi,D)


def oracle(N,r):
    # pi/4 = atan(1/2)+atan(1/3), distinct from production Machin identity.
    g=r+(N-1).bit_length()+70
    a,b=atan_bounds(2,g+10); c,d=atan_bounds(3,g+10)
    pl,pu=4*(a+c),4*(b+d)
    D=1<<(g+8)
    pl=Q((pl*D).numerator//(pl*D).denominator,D)
    pu=Q(-((-pu*D).numerator//(-pu*D).denominator),D)
    pc=(pl+pu)/2; rad=(pu-pl)/2
    assert 3<pl<pu<4
    root=inverse_sqrt_interval(N,g)
    K=g//2+30
    tab=[]
    for j in range(N):
        signed=j if 2*j<=N else j-N
        fac=Q(2*signed,N); x=fac*pc; xx=x*x
        # Independent even/odd Horner polynomials, no recurrence from production.
        co=Q((-1)**K,factorial(2*K))
        si=Q((-1)**K,factorial(2*K+1))
        for k in range(K-1,-1,-1):
            co=co*xx+Q((-1)**k,factorial(2*k))
            si=si*xx+Q((-1)**k,factorial(2*k+1))
        si*=x
        er=abs(fac)*rad+Q(4**(2*K+1),factorial(2*K+1))
        ei=abs(fac)*rad+Q(4**(2*K+2),factorial(2*K+2))
        tab.append((interval_mul((co-er,co+er),root),
                    interval_mul((-si-ei,-si+ei),root)))
    return tab


def ceil_log2(a):
    if not a:return None
    k=a.numerator.bit_length()-a.denominator.bit_length()
    return k if a<=p2(k) else k+1


def check_first(raw,r):
    z=execute(raw,bits=r)
    N=raw['N']; h=z.source.h
    assert len(z.pairs)==N
    receipt=dict(z.receipt)
    assert receipt['output_coordinates_written']==N
    assert receipt['input_coordinates_read']==len(raw['data'])
    assert receipt['coefficients_certified']==(N if N>1 and z.source.energy else 0)
    assert receipt['exact_complex_prefix_updates']==(N*len(z.source.entries) if N>1 and z.source.energy else 0)
    tab=oracle(N,r)
    err=Q(0)
    for k,(a,b) in enumerate(z.pairs):
        rl=ru=il=iu=Q(0)
        for j,c,d in z.source.entries:
            re,im=tab[j*k%N]
            cr=interval_mul((Q(c),Q(c)),re); di=interval_mul((Q(d),Q(d)),im)
            ci=interval_mul((Q(c),Q(c)),im); dr=interval_mul((Q(d),Q(d)),re)
            rl+=cr[0]-di[1]; ru+=cr[1]-di[0]
            il+=ci[0]+dr[0]; iu+=ci[1]+dr[1]
        rl,ru,il,iu=[v*p2(-h) for v in (rl,ru,il,iu)]
        # Compare normalized outputs; even a huge symbolic F cancels exactly.
        ar=Q(a)*p2(raw['F']-h-z.denominator_exponent)
        ai=Q(b)*p2(raw['F']-h-z.denominator_exponent)
        e=max(abs(ar-rl),abs(ar-ru))**2+max(abs(ai-il),abs(ai-iu))**2
        err+=e
    budget=p2(-2*r)*Q(z.source.energy,1<<(2*h))
    assert err<=budget if budget else err==0
    data,ec=export(z)
    assert json.loads(data)['pairs']==[list(x) for x in z.pairs]
    return z,{'N':N,'bits':r,'all_output_rows':N,'support':len(z.source.entries),
              'input_kind':raw['kind'],'scale_F':str(raw['F']),
              'oracle':'independent rational Machin variant, Horner, integer bisection',
              'relative_squared_error_budget_pass':True,
              'error_ratio_upper_power_two':ceil_log2(err/budget) if budget else None,
              'receipt':receipt,'one_export':ec}


def main():
    start=time.monotonic(); results=[]; first_result=None; first_raw=None
    lengths=[1,2,3,5,6,7,8,11,13,17,31]
    for N in lengths:
        raw={'N':N,'F':(N%7)-3,'kind':'dense',
             'data':[[2*j+1,(-1)**j*(j+2)] for j in range(N)]}
        z,row=check_first(raw,12+N%5);results.append(row)
        if N==5:first_result,first_raw=z,copy.deepcopy(raw)
    special=[
        {'N':9,'F':-91,'kind':'dense','data':[[2**200+1,0],[-2**200,1]]+[[0,0]]*7},
        {'N':15,'F':2**120+1,'kind':'sparse','data':[[0,3,-4],[7,-1,2],[14,1,-1]]},
        {'N':12,'F':0,'kind':'sparse','data':[[1,1,0],[3,-1,0],[5,1,0],[7,-1,0]]},
        {'N':10,'F':0,'kind':'dense','data':[[0,0] for _ in range(10)]},
    ]
    for raw in special:
        _,row=check_first(raw,32);results.append(row)
    reversal=[]
    for N in [1,4,8,16,32,65]:
        # Mathematical singleton identity is valid even beyond the legacy
        # dyadic sparse supplier. No legacy eligibility is inferred.
        raw={'N':N,'F':-(2**120+1),'kind':'dense',
             'data':[[2*j+1,2-3*j] for j in range(N)]}
        z=execute(raw,target='SINGLETON_SECOND_NORMALIZED',B_A=N)
        for k,(a,b) in enumerate(z.pairs):
            assert (a,b)==tuple(raw['data'][(-k)%N])
        assert z.denominator_exponent==z.source.h
        assert dict(z.receipt)['coefficients_certified']==0
        assert dict(z.receipt)['output_coordinates_written']==N
        reversal.append({'N':N,'rows_verified':N,'normalized_exact':True,
                         'receipt':dict(z.receipt)})
    # New dispatch/cost boundary tests, not the predecessor's incidence tests.
    plans=[]
    for k in [4,8,16,24,28,40,60]:
        N=1<<k;m=k+2;M=4*N
        D=max(5,(M-4+32*m-1)//(32*m))
        raw={'N':N,'F':0,'kind':'sparse','data':[[N-1,1,0]]}
        info,receipt=plan(raw,D=D);info=dict(info)
        assert not info['outer_structural_sparse_guard']
        assert info['route']=='CERTIFIED_DIRECT_DFT'
        assert dict(receipt)['output_coordinates_written']==0
        plans.append({'N':N,'variable_D':D,'classification':info,'receipt':dict(receipt)})
    domains=[]
    for count in [16,17]:
        raw={'N':1<<28,'F':0,'kind':'sparse','data':[[j,1,0] for j in range(count)]}
        info,rec=plan(raw);info=dict(info)
        assert info['outer_structural_sparse_guard']
        assert info['legacy_recovery_source_domain']==(count==16)
        assert not info['same_target_sparse_provider_bound']
        assert info['route']=='CERTIFIED_DIRECT_DFT'
        domains.append({'support':count,'classification':info,'receipt':dict(rec)})
    # Fresh byte/source-bound replay with all production costs charged again.
    ok,rr,vr=verify(first_raw,first_result,bits=12+5%5)
    assert ok
    mutations=[]
    bad_raw=copy.deepcopy(first_raw);bad_raw['data'][0][0]+=2
    ok,_,_=verify(bad_raw,first_result,bits=12)
    assert not ok;mutations.append('changed original coefficient')
    bad_raw=copy.deepcopy(first_raw);bad_raw['F']+=1
    ok,_,_=verify(bad_raw,first_result,bits=12)
    assert not ok;mutations.append('changed original scale')
    pp=list(first_result.pairs);pp[-1]=(pp[-1][0]+1,pp[-1][1])
    ok,_,_=verify(first_raw,replace(first_result,pairs=tuple(pp)),bits=12)
    assert not ok;mutations.append('changed final dense output')
    ok,_,_=verify(first_raw,replace(first_result,target='SINGLETON_SECOND_NORMALIZED'),bits=12)
    assert not ok;mutations.append('changed target tag')
    old=first_result.source.entries
    first_raw['data'][0][0]+=2
    assert first_result.source.entries==old
    mutations.append('caller mutation cannot alter immutable source')
    # Supplied result subclasses are not runtime mutation and must not gain
    # authority through Python's reflected equality protocol.
    from dense_dispatch import Result
    class Fake(Result):
        def __eq__(self,other): return True
    class LyingInt(int):
        def __eq__(self,other): return True
    raw_one={'N':1,'F':0,'kind':'sparse','data':[[0,1,0]]}
    one=execute(raw_one)
    fake=Fake(one.source,one.target,((314159,0),),one.denominator_exponent,
              one.requested_bits,one.dispatch,one.receipt,one.alpha_exponent)
    scalar=replace(one,pairs=((LyingInt(314159),0),))
    huge=replace(one,pairs=((0,0),)*10000)
    strict_tree_probes=[]
    for name,bad in [('result_subclass',fake),('integer_subclass',scalar),
                     ('oversized_tuple',huge)]:
        ok,replay,comparison=verify(raw_one,bad)
        assert not ok
        assert dict(comparison)['comparison_nodes']<64
        strict_tree_probes.append({'probe':name,'rejected':True,
                                  'fresh_replay_receipt':dict(replay),
                                  'bounded_comparison_receipt':dict(comparison)})
    comparison_rejections=[]
    for cap in (12,16,24,32):
        try:verify(raw_one,one,limits=Limits(max_events=cap))
        except Rejected as e:
            assert e.reason=='ARITHMETIC_EVENT_LIMIT'
            assert len(e.prior_receipts)==1
            completed=dict(e.prior_receipts[0]); terminal=dict(e.receipt)
            assert completed['arithmetic_records']==dict(one.receipt)['arithmetic_records']
            assert 0<completed['arithmetic_records']<=cap
            assert completed['output_coordinates_written']==1
            assert terminal['arithmetic_records']==cap+1
            work=completed['total_binary_work_bound']+terminal['total_binary_work_bound']
            storage=completed['cumulative_storage_bit_bound']+terminal['cumulative_storage_bit_bound']
            assert work>terminal['total_binary_work_bound']
            assert storage>terminal['cumulative_storage_bit_bound']
            comparison_rejections.append({'cap':cap,'reason':e.reason,
                'completed_replay_receipt':completed,'terminal_comparison_receipt':terminal,
                'combined_binary_work_bound':work,'combined_cumulative_storage_bit_bound':storage})
        else:raise AssertionError('comparison should exhaust its separate cap')
    missing_fields=object.__new__(Result)
    try:verify(raw_one,missing_fields)
    except Rejected as e:
        assert e.reason=='RESULT_TREE_GRAMMAR' and len(e.prior_receipts)==1
        assert dict(e.prior_receipts[0])['output_coordinates_written']==1
        comparison_rejections.append({'reason':e.reason,
            'completed_replay_receipt':dict(e.prior_receipts[0]),
            'terminal_comparison_receipt':dict(e.receipt)})
    else:raise AssertionError('missing-field result should be rejected')
    rejections=[]
    oversized_grammar={'N':4,'F':0,'kind':'sparse','data':[[0,1,0]]}
    oversized_grammar.update({f'extra_{k}':k for k in range(10000)})
    huge_negative=-(1<<2000000)
    tests=[
        ({'N':4,'F':huge_negative,'kind':'sparse','data':[[0,1,0]]},{},'SOURCE_METADATA_LIMIT'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,huge_negative,0]]},{},'SOURCE_COMPONENT_LIMIT'),
        (oversized_grammar,{},'SOURCE_GRAMMAR'),
        ({'N':4,'F':-(2**120+1),'kind':'sparse','data':[[0,1,0]]},{},'MATERIALIZED_OUTPUT_SHIFT_LIMIT'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,1,0]]},{'target':'SINGLETON_SECOND_NORMALIZED'},'SINGLETON_BLOCK_BINDING_REQUIRED'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,1,0]]},{'B_A':2},'GENERAL_BLOCK_SOURCE_NOT_IMPLEMENTED'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,True,0]]},{},'EXACT_INTEGER_REQUIRED'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,2,0]]},{},'NONCANONICAL_COMMON_GRID'),
        ({'N':4,'F':0,'kind':'sparse','data':[[0,1.0,0]]},{},'EXACT_INTEGER_REQUIRED'),
        ({'N':4,'F':0,'kind':'sparse','data':[[1,1,0],[1,1,0]]},{},'SOURCE_INDEX_ORDER'),
        ({'N':1<<28,'F':0,'kind':'sparse','data':[[1,1,0]]},{},'DENSE_ALLOCATION_LIMIT'),
        ({'N':4,'F':0,'kind':'sparse','data':[[1,1,0]]},{'limits':Limits(max_events=10)},'ARITHMETIC_EVENT_LIMIT'),
    ]
    for raw,kwargs,reason in tests:
        try:execute(raw,**kwargs)
        except Rejected as e:
            assert e.reason==reason,(e.reason,reason)
            assert dict(e.receipt)['output_coordinates_written']==0
            if reason=='SOURCE_METADATA_LIMIT':
                assert dict(e.receipt)['arithmetic_records']==1
                assert dict(e.receipt)['max_arithmetic_envelope_bits']<128
                assert dict(e.receipt)['input_coordinates_read']==0
            if reason=='SOURCE_COMPONENT_LIMIT':
                assert dict(e.receipt)['arithmetic_records']==3
                assert dict(e.receipt)['max_arithmetic_envelope_bits']<128
            if reason=='SOURCE_GRAMMAR':
                assert dict(e.receipt)['arithmetic_records']==0
                assert dict(e.receipt)['input_coordinates_read']==0
            if reason=='MATERIALIZED_OUTPUT_SHIFT_LIMIT':
                assert dict(e.receipt)['coefficients_certified']==0
                assert dict(e.receipt)['rational_setup_terms']==0
            rejections.append({'reason':reason,'paid_prefix_receipt':dict(e.receipt)})
        else:raise AssertionError('unexpected successful rejection probe')
    # Bounded endpoint control: larger working precision still fits its caps.
    z=execute({'N':2,'F':0,'kind':'sparse','data':[[0,1,0],[1,-1,1]]},bits=128)
    assert dict(z.receipt)['max_arithmetic_envelope_bits']<Limits().max_numeric_bits
    # Full output at the bounded N and precision endpoints. The constant
    # input has an exact known Fourier support, providing a separate target.
    endpoint=execute({'N':128,'F':0,'kind':'dense',
                      'data':[[1,0] for _ in range(128)]},bits=128)
    lo,hi=inverse_sqrt_interval(2,220); endpoint_error=Q(0)
    for k,(a,b) in enumerate(endpoint.pairs):
        u=Q(a)*p2(-endpoint.denominator_exponent-endpoint.source.h)
        v=Q(b)*p2(-endpoint.denominator_exponent-endpoint.source.h)
        endpoint_error+=(max(abs(u-lo),abs(u-hi))**2+v*v) if k==0 else u*u+v*v
    assert endpoint_error<=p2(-257)
    endpoint_record={'N':128,'bits':128,'all_rows_pass':True,
                     'analytic_target':'U_128(ones)/16 = (1/sqrt(2),0,...,0)',
                     'receipt':dict(endpoint.receipt)}
    report={'status':'PASS_FRESH_BOUNDED_REFERENCE_CONTROLS',
            'first_dft_runs':results,'exact_reversal_runs':reversal,
            'variable_D_dense_plans':plans,'legacy_domain_without_bridge':domains,
            'full_source_replay':{'pass':True,'production_receipt':dict(first_result.receipt),
                                  'separate_replay_receipt':dict(rr),'comparison_receipt':dict(vr)},
            'mutations_rejected':mutations,'fail_closed_probes':rejections,
            'strict_result_tree_probes':strict_tree_probes,
            'comparison_failure_prefixes':comparison_rejections,
            'precision_endpoint_receipt':dict(z.receipt),
            'complete_endpoint_run':endpoint_record,
            'counts':{'direct_runs':len(results)+1,'direct_output_rows':sum(r['N'] for r in results)+128,
                      'exact_reversal_runs':len(reversal),'reversal_output_rows':sum(r['N'] for r in reversal),
                      'variable_D_plans':len(plans),'source_bridge_domain_plans':len(domains),
                      'paid_rejections':len(rejections),'source_replay_mutations':len(mutations),
                      'complete_replay_executions':13,'complete_replay_rows':33,
                      'failed_comparisons_with_retained_replay':5,
                      'strict_tree_probe_source_runs':1,'strict_tree_probe_source_rows':1,
                      'separate_precision_endpoint_runs':1,'separate_precision_endpoint_rows':2,
                      'all_completed_direct_executions':len(results)+16,
                      'all_completed_direct_rows':sum(r['N'] for r in results)+164},
            'elapsed_seconds':time.monotonic()-start,
            'evidence_limits':'Only fresh new-reference tests. No inherited suite rerun, sparse pipeline composition, random acquisition, speed claim or novelty claim.'}
    report['source_sha256']=hashlib.sha256((ROOT/'dense_dispatch.py').read_bytes()).hexdigest()
    report['checks_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    (ROOT/'EXAMPLE_FIRST_DFT.json').write_text(export(first_result)[0]+'\n')
    print(json.dumps({'status':report['status'],'counts':report['counts'],
                      'elapsed_seconds':report['elapsed_seconds']},indent=2))

if __name__=='__main__':main()
