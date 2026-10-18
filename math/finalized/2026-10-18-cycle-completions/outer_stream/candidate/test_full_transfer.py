"""Fresh capped whole-stream test and independent retained-target interval check."""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import replace
import hashlib,json
from outer_wrapper import Header,Outer,ReceiptLedger
from sparse_output import produce_medians
from full_transfer import (FullTransfer,TransferConfig,TransferContractError,
                           OuterDenseRequired,round_div_pow2,exact_complex_product)
from true_interval_oracle import Oracle,BITS,U

ROOT=Path(__file__).resolve().parent

def ratio(x):return {'numerator':x.numerator,'denominator':x.denominator}

def make(N,candidates,rows,D=5,P=None,L=None):
    M=1<<(4*N-1).bit_length();m=M.bit_length()-1
    if P is None:P=16*m+16
    if L is None:L=ReceiptLedger()
    produced=produce_medians(M,P,candidates,rows,L)
    return Outer(Header(N,M,D,P),produced,L)


def check_error(action,kind=TransferContractError):
    try:action()
    except kind:return
    raise AssertionError('expected rejection missing')


def full_fixture():
    N=257;M=2048;m=11;P=16*m+16
    unit=1<<P;cap=3*M*M*unit
    candidates=(0,1,M//2,M-1)
    expected=((cap-17,-cap+19),(-cap+23,cap-29),(0,0),(unit//3,-unit//5))
    rows=tuple(tuple((a+dr,b+di) for a,b in expected) for dr,di in ((-3,5),(0,0),(7,-2)))
    outer=make(N,candidates,rows)
    assert tuple(pair for k,pair in outer.binding.output.pairs)==expected
    config=TransferConfig(1,8,31,3)  # b=24; positive scale crosses exponent zero.
    transfer=FullTransfer(outer,config)
    answer=transfer.run()
    transfer.validate_output(answer)
    assert answer.bits==0 and answer.normalized_bits==24 and answer.scale_power==31
    assert len(answer.pairs)==N
    assert answer.incidences==transfer.coefficients_evaluated==sum(r1-r0 for r0,r1,_ in outer.binding.endpoints)
    assert outer.kernel.paid.operations['coefficient_call']==answer.incidences
    assert outer.kernel.paid.operations['pi_setup']==outer.kernel.paid.operations['sqrt_setup']==1
    assert outer.kernel.paid.operations['certificate_pass']==answer.incidences
    before=transfer.ledger.events
    check_error(transfer.run)
    assert transfer.ledger.events>before and transfer.state=='COMPLETE'
    check_error(lambda:transfer.validate_output(replace(answer,bits=1)))

    # Direct row-first oracle: it neither reads endpoint records nor calls the
    # production iterator, production scalar, or a production arithmetic helper.
    oracle=Oracle(N,M,5)
    h=16*5*m+1;t=2*h+2
    accum=[];distances=[];rows_checked=0;incidences=0;nonzero=0
    A=(5+3)*m;b=answer.normalized_bits
    largest_ratio=F(0);max_terms=0
    for ell in range(N):
        re=(0,0);im=(0,0);l1=0;terms=0
        center=(ell*M)//N
        for k,(a,z) in zip(candidates,expected):
            residue=(k-center)%M
            if not(residue<=h+1 or residue>=M-h):continue
            cr,ci=oracle.coefficient(ell,k)
            def signed_mul(x,v):
                vals=[x[0]*v,x[1]*v]
                return min(vals),max(vals)
            ar,ai=signed_mul(cr,a),signed_mul(ci,a)
            br,bi=signed_mul(cr,z),signed_mul(ci,z)
            re=(re[0]+ar[0]-bi[1],re[1]+ar[1]-bi[0])
            im=(im[0]+ai[0]+br[0],im[1]+ai[1]+br[1])
            l1+=abs(a)+abs(z);terms+=1;incidences+=1
        denominator=1<<(BITS+P)
        normalized=[F(v,1<<answer.bits)/F(1<<answer.scale_power) for v in answer.pairs[ell]]
        rr=max(abs(normalized[0]-F(v,denominator)) for v in re)
        ri=max(abs(normalized[1]-F(v,denominator)) for v in im)
        bound=F(l1,1<<(P+A))+F(1,1<<b)
        distance_squared=rr*rr+ri*ri
        assert distance_squared<=bound*bound
        # Bound includes full coefficient perturbation and one complex rounding.
        largest_ratio=max(largest_ratio,distance_squared/(bound*bound))
        max_terms=max(max_terms,terms);rows_checked+=1
        nonzero+=int(answer.pairs[ell]!=(0,0))
        accum.append({'row':ell,'terms':terms,'real_interval':list(re),'imag_interval':list(im)})
        distances.append(ratio(distance_squared))
    assert incidences==answer.incidences==oracle.calls
    assert max_terms==answer.max_row_terms<=t
    assert answer.max_accumulator_abs<(1<<(answer.accumulator_signed_bits-1))
    # Only ordinary output records and scalar state survive, no E-sized cache.
    assert not hasattr(transfer,'coefficients') and not hasattr(outer,'coefficients')
    (ROOT/'TRUE_TARGET_INTERVALS.json').write_text(json.dumps({'bits':BITS+P,'rows':accum},indent=2)+'\n')
    return {'N':N,'M':M,'D':5,'m':m,'P':P,'t':t,'support':list(candidates),
            'fixture_scope':'complete retained outer transform only; other sparse-recovery guards fail at this size',
            'rows_checked':rows_checked,'all_coefficients_evaluated_and_independently_enclosed':incidences,
            'oracle_bits':BITS,'nonzero_output_rows':nonzero,'max_row_terms':max_terms,
            'max_squared_error_over_proved_bound_squared':ratio(largest_ratio),
            'output_pairs':[list(x) for x in answer.pairs],'output_bits':answer.bits,
            'normalized_bits':b,'scale_power':answer.scale_power,
            'accumulator_signed_bits':answer.accumulator_signed_bits,
            'max_accumulator_abs':answer.max_accumulator_abs,'receipt':transfer.receipt()}


def negative_scale_fixture():
    # Here sqrt(M/N)=2 and the integral-residue coefficient is exactly
    # 1025/1024. This is an exact nonzero scale-back anchor, not a float test.
    N=512;M=2048;P=192
    outer=make(N,(0,),((((1<<P),0),),))
    transfer=FullTransfer(outer,TransferConfig(1,4,-17,2))
    answer=transfer.run()
    assert answer.bits==42 and answer.normalized_bits==25
    assert F(answer.pairs[0][0],1<<answer.bits)==F(1025,1<<(10+17))
    assert answer.pairs[0][1]==0
    assert len(answer.pairs)==N and answer.incidences==441
    assert outer.kernel.paid.operations['coefficient_call']==441
    assert outer.kernel.paid.operations['certificate_pass']==441
    assert answer.max_row_terms==1
    return {'N':N,'M':M,'P':P,'incidences':answer.incidences,
            'output_rows':len(answer.pairs),'scale_power':-17,'output_bits':answer.bits,
            'exact_row_zero':list(answer.pairs[0]),
            'output_sha256':hashlib.sha256(json.dumps(answer.pairs).encode()).hexdigest(),
            'receipt':transfer.receipt()}


def controls():
    L=ReceiptLedger();ties=0;rounds=0;products=0
    for shift in range(9):
        denominator=1<<shift
        for n in range(-513,514):
            # Independent Fraction-to-even rule through distances to neighbors.
            x=F(n,denominator);lo=x.__floor__();hi=x.__ceil__()
            expected=min((lo,hi),key=lambda q:(abs(F(q)-x),q%2))
            assert round_div_pow2(n,shift,L)==expected
            ties+=int(abs(F(lo)-x)==abs(F(hi)-x) and lo!=hi)
            rounds+=1
    for a in range(-3,4):
        for b in range(-3,4):
            for c in range(-3,4):
                for d in range(-3,4):
                    out=exact_complex_product(a,b,c,d,L)
                    # Built-in complex arithmetic is exact on these small ints.
                    z=complex(a,b)*complex(c,d)
                    assert out==(int(z.real),int(z.imag));products+=1
    empty=make(257,(),((),))
    empty_transfer=FullTransfer(empty,TransferConfig(1,8,-11,1))
    zero=empty_transfer.run()
    assert len(zero.pairs)==257 and all(v==(0,0) for v in zero.pairs)
    assert zero.bits==35 and empty.kernel is None and zero.incidences==0
    assert empty_transfer.ledger.events>3*257
    dense=[]
    for N in (1,2,3,4,7,16,63,127,128,255,256):
        o=make(N,(),((),))
        check_error(lambda:FullTransfer(o,TransferConfig(1,8,0,1)),OuterDenseRequired)
        assert o.kernel is None
        dense.append({'N':N,'M':o.binding.geometry.M,'t':o.binding.geometry.t})
    bad=0
    for cfg in (TransferConfig(0,8,0,1),TransferConfig(1,0,0,1),
                TransferConfig(4,8,0,1),TransferConfig(1,8,0,0),
                TransferConfig(1,8,12,1),TransferConfig(True,8,0,1)):
        o=make(257,(),((),))
        check_error(lambda:FullTransfer(o,cfg),ValueError);assert o.kernel is None;bad+=1
    check_error(lambda:FullTransfer(make(257,(),((),),P=8),TransferConfig(1,8,0,1)))
    bad+=1
    cap=3*2048*2048*(1<<192)
    for value in (cap,-cap,1<<10000):
        o=make(257,(0,),(((value,0),),))
        prior=o.ledger.events
        check_error(lambda:FullTransfer(o,TransferConfig(1,8,0,1)))
        assert o.kernel is None and o.ledger.events>prior;bad+=1
    # Fresh adversarial mutations act only in this test instance and are not
    # admissible external input. Coverage checks must catch both drop and repeat.
    omissions=[]
    for mutation in ('drop_first','drop_last','repeat_first'):
        o=make(257,(0,),(((0,0),),))
        original=o.incidences
        def modified():
            items=iter(original())
            if mutation=='drop_first':
                next(items,None);yield from items
            elif mutation=='drop_last':
                prev=next(items,None)
                for item in items:
                    yield prev;prev=item
            else:
                first=next(items);yield first;yield first;yield from items
        o.incidences=modified
        transfer=FullTransfer(o,TransferConfig(1,8,0,1))
        check_error(transfer.run)
        assert transfer.state=='FAILED' and transfer.output is None
        omissions.append({'mutation':mutation,'coefficients_before_rejection':transfer.coefficients_evaluated,
                          'paid_events_after_rejection':o.ledger.events})
    # Precise t>=M counterexample: lifts repeat rows and overcount support.
    N,M,D=256,1024,5;m=10;h=16*D*m+1;k=0
    r0=-((-N*(k-h-1))//M);r1=-((-N*(k+h+1))//M)
    rows=[r%N for r in range(r0,r1)]
    assert len(rows)==401 and len(set(rows))==256
    return {'rounding_cases':rounds,'signed_ties':ties,'exact_complex_product_cases':products,
            'empty_output_rows':len(zero.pairs),'empty_scalar_setup':False,
            'dense_guard_cases':dense,'malformed_or_out_of_contract_cases':bad,
            'stream_mutations':omissions,
            'dense_unguarded_duplicate_witness':{'N':N,'M':M,'D':D,'t':2*h+2,'k':k,
                                               'lifts':len(rows),'distinct_rows':len(set(rows))},
            'controls_ledger':L.report()}


def main():
    data={'status':'PASS','controls':controls(),'full_fixture':full_fixture(),
          'negative_scale_fixture':negative_scale_fixture()}
    (ROOT/'RESULTS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':'PASS','incidences':data['full_fixture']['all_coefficients_evaluated_and_independently_enclosed'],
                      'rows':data['full_fixture']['rows_checked'],'controls':data['controls']['rounding_cases']+data['controls']['exact_complex_product_cases']}))
if __name__=='__main__':main()
