"""Fresh complete original-bound production and exact all-output target checks."""
from pathlib import Path
from dataclasses import asdict,replace
from fractions import Fraction as F
import hashlib,json,time,resource,sys
from integrated_centered import IntegratedCentered
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def frac(v):return {'numerator':v.numerator,'denominator':v.denominator}
def dyadic(a,bits):return F(a,1<<bits) if bits>=0 else F(a*(1<<(-bits)))
def sqrt_interval(n,q):
    # Independent integer bisection for sqrt(n), not a production root routine.
    target=n << (2*q);lo=0;hi=1 << (q+(n.bit_length()+1)//2)
    visits=0
    while hi-lo>1:
        mid=(lo+hi)//2;visits+=1
        if mid*mid<=target:lo=mid
        else:hi=mid
    assert lo*lo<=target<hi*hi
    return (F(lo,1<<q),F(lo if lo*lo==target else hi,1<<q)),visits

def target_checks(bound):
    src=bound.source;out=bound.final
    # U_N of the actual constant original is sqrt(N)*c*2^-F at zero and
    # exactly zero at every other frequency, by geometric summation.
    root,visits=sqrt_interval(src.N,256)
    target0=[]
    for c in (src.real,src.imag):
        x=tuple(v*dyadic(c,src.h) for v in root)
        target0.append((min(x),max(x)))
    R2=F(src.N*(src.real**2+src.imag**2),1<<(2*src.h))
    # Upper bound the inherited E_M=4*M^-1/4 by a rational dyadic.
    Eupper=F(4,1 << (src.m//4));t=160*src.m+4;b=out.normalized_bits
    bound_relative=3*t*Eupper+t*F(1,1<<(8*src.m))*(1+Eupper)+F(12,1<<(10*src.m))+F(1,1<<(b-1))
    rows=[];maximum=F(0);max_at=None
    for ell,(a,bv) in enumerate(out.pairs):
        y=(dyadic(a,out.bits+src.scale),dyadic(bv,out.bits+src.scale))
        targets=target0 if ell==0 else ((F(0),F(0)),(F(0),F(0)))
        radius=[max(abs(v-l),abs(v-h)) for v,(l,h) in zip(y,targets)]
        squared=sum((v*v for v in radius),F(0))
        assert squared <= bound_relative**2*R2
        rows.append(frac(squared))
        if squared>maximum:maximum=squared;max_at=ell
    # Stronger independent finite check, not an asymptotic theorem improvement.
    assert maximum <= R2/16  # observed error at most one quarter of ||u0||_2
    return {'all_rows_checked':len(rows),'exact_geometric_zero_rows':len(rows)-1,
            'sqrt_bisection_visits':visits,'normalized_target0_intervals':[[frac(x) for x in t] for t in target0],
            'norm_squared_normalized':frac(R2),'relative_theorem_upper':frac(bound_relative),
            'maximum_squared_error_normalized_upper':frac(maximum),'maximum_error_row':max_at,
            'squared_relative_error_upper':frac(maximum/R2),'relative_error_at_most_one_quarter':True,
            'row_squared_error_normalized_upper':rows,
            'scope':'Exact rational finite checks against actual U_N u0, after dividing both sides by 2^scale; no floating tolerance.'}

def main():
    started=time.monotonic();before={p.name:sha(p) for p in (HERE/'runtime').glob('*.py')}
    original={'m':11,'F':-36,'kind':'dense','data':[[-3,5] for _ in range(512)]}
    (HERE/'ORIGINAL.json').write_text(json.dumps(original,indent=2)+'\n')
    pipeline=IntegratedCentered(original,replay_source=True)
    print('Front and source replay complete; expected incidences:',pipeline.transfer.expected_incidences,flush=True)
    result=pipeline.run();pipeline.validate_output(result)
    # Caller input mutation cannot affect retained exact original/source.
    original['data'][-1][0]=99
    assert result.source.real==-3 and result.source.imag==5
    assert result.source.scale==44
    assert result.final.bits==0 and result.final.normalized_bits==25
    assert len(result.final.pairs)==512
    controls=[]
    for label,call in [
        ('second_integrated_run',lambda:pipeline.run()),
        ('copied_bound_output',lambda:pipeline.validate_output(replace(result))),
        ('altered_source_field',lambda:pipeline.validate_output(replace(result,source=replace(result.source,F=0)))),
        ('copied_transfer_output',lambda:pipeline.transfer.validate_output(replace(result.final)))
    ]:
        try:call()
        except ValueError as error:controls.append({'name':label,'rejected':True,'reason':str(error)})
        else:raise AssertionError(label)
    check=target_checks(result)
    receipt=pipeline.receipt()
    assert receipt['outer_transfer']['state']=='COMPLETE'
    assert receipt['outer_transfer']['coefficients_evaluated']==receipt['outer_transfer']['expected_incidences']==result.final.incidences
    assert receipt['front_production']['events']['dense_coordinate_visits']==512
    assert receipt['source_replay']['replay_production']['events']['dense_coordinate_visits']==512
    ops=receipt['outer_transfer']['scalar']['operations']
    assert ops['pi_setup']==ops['sqrt_setup']==ops['setup_complete']==1
    assert ops['coefficient_call']==ops['certificate_pass']==result.final.incidences
    assert before=={p.name:sha(p) for p in (HERE/'runtime').glob('*.py')}
    output={'source':asdict(result.source),'estimates':asdict(result.estimates),
            'target':result.target,'output':{k:getattr(result.final,k) for k in ('pairs','bits','normalized_bits','scale_power','incidences','accumulator_signed_bits','max_row_terms','max_accumulator_abs')}}
    (HERE/'OUTPUT.json').write_text(json.dumps(output,indent=2)+'\n')
    (HERE/'TARGET_CHECKS.json').write_text(json.dumps(check,indent=2)+'\n')
    report={'source_hashes':before,'source_hashes_unchanged':True,'full_outer_executed':True,
            'actual_original_target':'U_N u0; u0_j=(-3+5i)*2^36, N=512',
            'dense_original_reads':1024,'provider_executions':2,'provider_records':26,
            'output_rows':512,'coefficients':result.final.incidences,'rejection_controls':controls,
            'caller_mutation_does_not_change_source':True,'receipts':receipt,
            'observed_process_seconds':time.monotonic()-started,
            'observed_process_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'oracle_and_export_scope':'Separate finite harness work; not part of the production receipts.',
            'general_recovery_accepted':False,'alg_034_closed':False}
    (HERE/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('full_outer_executed','dense_original_reads','provider_records','output_rows','coefficients','observed_process_seconds')}),flush=True)

if __name__=='__main__':main()
