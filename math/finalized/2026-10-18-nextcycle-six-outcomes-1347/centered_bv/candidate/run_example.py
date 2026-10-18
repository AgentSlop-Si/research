"""Full nonconstant dense-original production, source replay and original oracle."""
from pathlib import Path
from dataclasses import asdict,replace
from fractions import Fraction as F
import json,time,resource,hashlib
from integrated_bv import IntegratedBoundedVariation
from bounded_variation import recognize,produce,Ledger,Rejected
import oracle_core as O
HERE=Path(__file__).resolve().parent

def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def fjson(v):return [v.numerator,v.denominator]
def root_inverse(n):
    lo=0;hi=O.U+1;count=0
    while hi-lo>1:
        mid=(lo+hi)//2;count+=1
        if mid*mid*n<=O.U*O.U:lo=mid
        else:hi=mid
    assert lo*lo*n<=O.U*O.U<hi*hi*n
    return (lo,lo if lo*lo*n==O.U*O.U else hi),count

def direct_table(values,length,offset,h):
    """Independent direct sums of actual raw coordinates, no block formula."""
    sine=[O.sine(F(2*k,length)) for k in range(length)]
    cosine=[sine[(k+length//4)%length] for k in range(length)]
    root,visits=root_inverse(length)
    result=[]
    for k in range(length):
        re=(0,0);im=(0,0)
        for j,(a,b) in enumerate(values):
            r=((j-offset)*k)%length;c=cosine[r];s=sine[r]
            re=O.add(re,O.add(O.scale(c,a),O.scale(s,b)))
            im=O.add(im,O.add(O.scale(c,b),O.scale(s,-a)))
        result.append((O.scale(O.mul(re,root),1,1<<h),O.scale(O.mul(im,root),1,1<<h)))
    return result,visits

def upper_squared(y,target):
    radii=[max(abs(value-F(low,O.U)),abs(value-F(high,O.U))) for value,(low,high) in zip(y,target)]
    return sum((r*r for r in radii),F(0))

def check_original(result,original):
    src=result.source;out=result.final;values=original['data']
    original_target,rootvisits=direct_table(values,src.N,0,src.h)
    R2=F(src.energy,1<<(2*src.h));rows=[];maximum=F(0);maxrow=None
    for ell,(a,b) in enumerate(out.pairs):
        y=[F(v,1<<(out.bits+src.scale)) for v in (a,b)]
        sq=upper_squared(y,original_target[ell]);rows.append(fjson(sq))
        if sq>maximum:maximum=sq;maxrow=ell
    # An exact finite fixture bound; the universal bound stays separately stated.
    percent_ceiling=1
    while maximum>R2*F(percent_ceiling,10000)**2:percent_ceiling+=1
    assert percent_ceiling<=1000 # all outputs <= 10% original L2 for this fixture
    return {'all_original_outputs_checked':len(rows),'direct_sum_terms':src.N*src.N,
            'oracle_work_separate':True,'sqrt_bisection_visits':rootvisits,
            'norm_squared_normalized':fjson(R2),'maximum_squared_error_upper':fjson(maximum),
            'maximum_row':maxrow,'squared_relative_error_upper':fjson(maximum/R2),
            'relative_error_upper_rational':[percent_ceiling,10000],
            'error_denominator':'Euclidean norm of actual supplied original; complex infinity output error',
            'row_squared_error_upper':rows}

def check_provider(result,original):
    src=result.source;est=result.estimates;M=4*src.N
    target,visits=direct_table(original['data'],M,(src.N-1)//2,src.h)
    sparse=dict(est.pairs);R2=F(src.energy,1<<(2*src.h));maximum=F(0);maxrow=None
    retained=omitted=0
    # M^(-1/4) norm premise squared is R2/sqrt(M). Compare via squaring.
    for k,interval in enumerate(target):
        pair=sparse.get(k,(0,0));sq=upper_squared([F(v,1<<est.bits) for v in pair],interval)
        if k in sparse:
            assert sq<=F(1,1<<(2*est.bits));retained+=1
        else:omitted+=1
        assert sq*sq*M<=R2*R2
        if sq>maximum:maximum=sq;maxrow=k
    return {'all_centered_coefficients_checked':M,'retained':retained,'omitted':omitted,
            'direct_sum_terms':M*src.N,'sqrt_bisection_visits':visits,
            'all_retained_complex_radii_at_most_rho':True,'all_global_premise_checks_passed':True,
            'maximum_squared_error_upper':fjson(maximum),'maximum_error_frequency':maxrow,
            'oracle_work_separate':True}

def main():
    start=time.monotonic()
    # This actual original has three unequal blocks and two interior jumps.
    # F makes scale=44, exercising the accepted physical output shift boundary.
    original={'m':11,'F':-38,'kind':'dense','data':[[1,0]]*173+[[2,0]]*211+[[-1,0]]*128}
    L=Ledger();source=recognize(original,L)
    # E=1145, h=6, B1=6, C=3 -> 49 retained locations.
    print('source',asdict(source),flush=True)
    dump('ORIGINAL.json',original)
    pipeline=IntegratedBoundedVariation(original,replay_source=True)
    print('front and source replay complete; incidences',pipeline.transfer.expected_incidences,flush=True)
    result=pipeline.run();pipeline.validate_output(result)
    print('outer complete; checking actual original and centered source',flush=True)
    target=check_original(result,original);provider=check_provider(result,original)
    # Check immutable source retention against caller mutation.
    original['data'][-1]=[99,1]
    assert result.source.blocks==((173,1,0),(384,2,0),(512,-1,0))
    controls=[]
    for label,call in [('repeat_run',lambda:pipeline.run()),
                       ('copied_output',lambda:pipeline.validate_output(replace(result))),
                       ('changed_source',lambda:pipeline.validate_output(replace(result,source=replace(result.source,F=0)))),
                       ('copied_transfer',lambda:pipeline.transfer.validate_output(replace(result.final)))]:
        try:call()
        except ValueError as err:controls.append({'label':label,'rejected':True,'reason':str(err)})
        else:raise AssertionError(label)
    receipt=pipeline.receipt();r=receipt['outer_transfer']
    assert r['state']=='COMPLETE' and r['coefficients_evaluated']==result.final.incidences
    assert receipt['front_production']['events']['dense_coordinate_visits']==512
    assert receipt['source_replay']['replay_production']['events']['dense_coordinate_visits']==512
    assert r['scalar']['operations']['coefficient_call']==r['scalar']['operations']['certificate_pass']==result.final.incidences
    dump('OUTPUT.json',{'source':asdict(result.source),'estimates':asdict(result.estimates),
        'output':{k:getattr(result.final,k) for k in ('pairs','bits','normalized_bits','scale_power','incidences','max_row_terms')},'target':result.target})
    dump('TARGET_CHECKS.json',target);dump('PROVIDER_CHECKS.json',provider)
    report={'full_outer_executed':True,'source_replay_executed':True,'provider_runs':2,
        'dense_coordinates_read':1024,'provider_records':2*len(result.estimates.pairs),
        'output_rows':len(result.final.pairs),'coefficients':result.final.incidences,
        'source':asdict(result.source),'cutoff':result.estimates.cutoff,'sparse_records':len(result.estimates.pairs),
        'relative_error_upper_rational':target['relative_error_upper_rational'],
        'controls':controls,'caller_mutation_invariant':True,'receipts':receipt,
        'observed_process_seconds':time.monotonic()-start,
        'observed_process_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'oracle_and_export_work':'Separate harness work, excluded from production receipts',
        'arbitrary_original_claim':False,'alg034_closed':False}
    dump('RESULTS.json',report)
    print(json.dumps({k:report[k] for k in ('full_outer_executed','dense_coordinates_read','sparse_records','coefficients','output_rows','relative_error_upper_rational','observed_process_seconds')}),flush=True)
if __name__=='__main__':main()
