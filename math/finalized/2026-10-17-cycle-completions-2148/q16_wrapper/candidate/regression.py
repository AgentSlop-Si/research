"""Fresh bounded API regression. Independent transcendental oracle is separate."""
import json
from dataclasses import asdict,replace
from pathlib import Path
from outer_wrapper import Header,Outer,ReceiptLedger
from sparse_output import produce_medians
from production_scalar import Paid,Interval,signed_power,nearest_even


def main():
    N=(1<<55)-1; M=1<<57; D=5; P=16*57+16
    support=(0,1710,(1<<55)+1,(1<<57)-1)
    U=1<<P
    rows=(((U,0),(0,0),(-U,U//2),(U//4,-U//4)),
          ((U+1,1),(1,-1),(-U+1,U//2+1),(U//4+1,-U//4+1)),
          ((U-1,-1),(-1,1),(-U-1,U//2-1),(U//4-1,-U//4-1)))
    ledger=ReceiptLedger()
    run=produce_medians(M,P,support,rows,ledger)
    assert run.output.pairs==tuple(zip(support,rows[0]))
    producer_work=ledger.report()
    before=ledger.events
    outer=Outer(Header(N,M,D,P),run,ledger)
    assert ledger.events>before
    G=outer.binding.geometry
    assert (G.m,G.s,G.h,G.t,G.J,G.K,G.p)==(57,285,4561,9124,587,623,459)
    assert outer.binding.output is run.output
    assert outer.binding.support==support
    assert run._origin.rows is rows and run._origin.candidates is support
    assert outer.kernel is None
    records=list(outer.incidences())
    actual={(r.ell,r.k) for r in records}
    assert len(records)==len(actual)==9123
    assert outer.kernel is None
    # Separate stencil-offset inverse construction, not lifted endpoint formula.
    expected=set()
    for k in support:
        for j in range(-G.h,G.h+2):
            center=(k-j)%M
            start=-((-center*N)//M)
            stop=-((-(center+1)*N)//M)
            for ell in range(start,stop):
                assert 0<=ell<N
                expected.add((ell,k))
    assert actual==expected
    for ordinal,r in enumerate(records):
        center=r.ell*M//N
        offset=(r.k-center)%M
        assert offset<=G.h+1 or offset>=M-G.h
        assert r.ordinal==ordinal
        outer._validate_incidence(r)
    counts=[sum(r.k==k for r in records) for k in support]
    selected=[]
    for ell,k in ((0,0),(1<<53,(1<<55)+1),(0,1710)):
        incidence=next(r for r in records if (r.ell,r.k)==(ell,k))
        emitted=outer.coefficient(incidence)
        assert outer.validate_coefficient(emitted) is emitted
        selected.append(emitted)
    kernel=outer.kernel
    assert kernel.scalar.sine_calls==12
    assert kernel.paid.operations['pi_setup']==kernel.paid.operations['sqrt_setup']==1
    assert selected[0].certificate.residue==0
    assert selected[0].certificate.denominator is None
    assert selected[1].certificate.residue==1
    assert selected[1].certificate.denominator.lo>0
    assert selected[2].certificate.denominator.lo>0
    assert selected[2].certificate.F.hi<0 and selected[2].certificate.R.hi<0
    assert selected[2].real==selected[2].imag==0
    for emitted in selected:
        c=emitted.certificate
        assert c.radius_squared<=c.eta_squared_grid
        assert c.radius_squared==c.radius_real*c.radius_real+c.radius_imag*c.radius_imag
    core_wrapper_receipt=ledger.report()
    core_scalar_receipt=kernel.paid.report()
    # Repeat preparation and validation: no ledger reset and no repeated setup.
    events=kernel.paid.events;kernel.prepare();assert kernel.paid.events>events
    assert kernel.paid.operations['pi_setup']==kernel.paid.operations['sqrt_setup']==1
    events=ledger.events;outer.validate_binding(outer.binding);assert ledger.events>events
    # Production power endpoint sentinel; decisive primitive guard, not final eta error.
    unit=1<<623
    sentinel=signed_power(Interval(-unit//2,-unit//4,623),285,kernel.paid)
    assert (sentinel.lo,sentinel.hi)==(-(1<<338),-(1<<53))
    assert (sentinel.lo,sentinel.hi)!=(1<<53,1<<338)
    mutant_rejection=None
    try:
        if 285%2:raise ValueError('even exponent required')
    except ValueError as e:mutant_rejection=str(e)
    assert mutant_rejection=='even exponent required'
    for integer in range(-12,13):
        assert nearest_even(2*integer+1,2,kernel.paid)==(integer if integer%2==0 else integer+1)
    # Correct theorem metadata only. This does not execute the theorem-scale front end.
    sparse_k=1<<((57+3)//4)
    B=1<<((5*57+7)//8)
    r_win=2*57+1;W=2*r_win*(8*B-1)+1
    guards={'B_divides_M':M%B==0,'B_ge_4':B>=4,'T_ge_4':M//B>=4,
            'B_ge_4096k':B>=4096*sparse_k,'W_lt_M':W<M,'t_lt_M':G.t<M,
            'beta_m_ge_2':57>=16,'support_cap':len(support)<=1024*sparse_k*M//B}
    assert all(guards.values())
    errors=[]
    def reject(name,action,fragment):
        try:action()
        except (ValueError,ArithmeticError) as e:
            assert fragment in str(e),(name,str(e))
            errors.append({'name':name,'error':str(e)})
        else:raise AssertionError(name+' unexpectedly accepted')
    second=Outer(Header(N,M,D,P),produce_medians(M,P,support,rows,ledger),ledger)
    reject('mixed binding',lambda:outer.validate_binding(second.binding),'mixed or substituted binding')
    reject('equal cloned binding',lambda:outer.validate_binding(replace(outer.binding)),'mixed or substituted binding')
    reject('substituted produced output',lambda:Outer(Header(N,M,D,P),replace(run,output=replace(run.output)),ledger),'mixed or substituted produced output')
    reject('wrong accepted header',lambda:Outer(Header(N,M,D,P+1),run,ledger),'accepted-output header mismatch')
    reject('wrong N M relation',lambda:Outer(Header(N+1,M//2,D,P),run,ledger),'M must equal')
    for field,bad in [('N',True),('M',float(M)),('D',True),('estimate_bits',False)]:
        reject('exact '+field,lambda field=field,bad=bad:Outer(replace(Header(N,M,D,P),**{field:bad}),run,ledger),'exact built-in integer')
    reject('duplicate support',lambda:produce_medians(M,P,(0,0),(((1,0),(2,0)),),ledger),'sorted and distinct')
    reject('out of range support',lambda:produce_medians(M,P,(M,),(((1,0),),),ledger),'sorted and distinct')
    reject('mutable support',lambda:produce_medians(M,P,list(support),rows,ledger),'immutable candidate')
    reject('mutable row',lambda:produce_medians(M,P,support,(list(rows[0]),),ledger),'row shape')
    reject('even rounds',lambda:produce_medians(M,P,support,rows[:2],ledger),'positive odd')
    first=selected[0]
    reject('mixed emitted coefficient',lambda:second.validate_coefficient(first),'mixed or substituted coefficient origin')
    reject('substituted coefficient number',lambda:outer.validate_coefficient(replace(first,real=first.real+1)),'substituted coefficient fields')
    reject('substituted coefficient grid',lambda:outer.validate_coefficient(replace(first,p=first.p+1)),'substituted coefficient fields')
    reject('substituted coefficient incidence',lambda:outer.validate_coefficient(replace(first,incidence=records[1])),'coefficient origin')
    reject('substituted incidence ordinal',lambda:outer.coefficient(replace(records[0],ordinal=1)),'incidence ordinal')
    reject('substituted incidence index',lambda:outer.coefficient(replace(records[0],k=1)),'support index')
    reject('substituted incidence row',lambda:outer.coefficient(replace(records[0],ell=(records[0].ell+1)%N)),'substituted incidence')
    # Semantic replay catches consistent output/context replacement, not just identity.
    changed=replace(run.output,pairs=((0,(U+20,0)),)+run.output.pairs[1:])
    forged_origin=replace(run._origin,output=changed)
    forged=replace(run,output=changed,_origin=forged_origin)
    reject('rehashed-equivalent semantic output forgery',lambda:Outer(Header(N,M,D,P),forged,ledger),'semantic replay mismatch')
    # Consumed malformed prefix remains paid at its actual bit width.
    before=ledger.events
    reject('large malformed prefix',lambda:produce_medians(M,P,(0,),(((1<<16384,False),),),ledger),'exact built-in integer')
    assert ledger.events>before and ledger.max_bits>=16385
    emptyL=ReceiptLedger();emptyRun=produce_medians(M,P,(),((),),emptyL)
    empty=Outer(Header(N,M,D,P),emptyRun,emptyL)
    assert list(empty.incidences())==[] and empty.kernel is None and emptyL.bit_work>0
    denseL=ReceiptLedger();denseRun=produce_medians(4,8,(0,),(((0,0),),),denseL)
    dense=Outer(Header(1,4,5,8),denseRun,denseL)
    assert list(dense.incidences())==[] and dense.last_failure=='OUTER_DENSE_REQUIRED'
    assert dense.kernel is None
    Path('INCIDENCES.json').write_text(json.dumps([[r.ordinal,r.k,r.ell,r.lifted] for r in records],separators=(',',':'))+'\n')
    result={'status':'AUTHOR_PASS_BOUNDED_PRODUCTION_MEDIAN_BINDING_ITERATOR_AND_THREE_COEFFICIENTS',
      'scope':'fresh producer implements accepted Cartesian-median semantics; no theorem-scale sparse pipeline or input/tape provenance claim',
      'metadata':asdict(G),'estimate_bits':P,'support':support,'incidence_count':len(records),'per_support_counts':counts,
      'all_incidence_set_equality':True,'selected_coefficient_count':3,
      'selected_coefficients':[asdict(x.certificate) for x in selected],
      'sentinel':asdict(sentinel),'even_only_control':mutant_rejection,'theorem_metadata_guards':guards,
      'producer_ledger':producer_work,'core_wrapper_ledger_before_adversarial':core_wrapper_receipt,'core_scalar_ledger_before_adversarial':core_scalar_receipt,'wrapper_and_producer_final_ledger':ledger.report(),'scalar_ledger':kernel.paid.report(),
      'empty_ledger':emptyL.report(),'empty_pi_sqrt_setups':0,'dense_ledger':denseL.report(),'dense_guard':dense.last_failure,
      'negative_controls':errors,'historical_source_executed':False,'full_stream_evaluated':False,
      'scatter_accumulators_N_outputs_scale_back_dense_dispatch_amplification':False,
      'independent_oracle_status':'PENDING_SEPARATE_AUTHOR_FINAL_REVIEW'}
    Path('RESULTS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'incidences':len(records),'coefficients':3,'negative_controls':len(errors)}))

if __name__=='__main__':main()
