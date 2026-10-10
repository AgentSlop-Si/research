from pathlib import Path
import json
from correction_graph import run, as_integer, fresh_weight


def digits(value,n,base):
    out=[]
    for _ in range(n):
        value,d=divmod(value,base); out.append(d)
    assert value==0
    return out


def compact(result):
    return {k:result[k] for k in ['total_arithmetic','preparation_arithmetic',
        'discovery_arithmetic','product_arithmetic','counts','schedule']}


def main():
    cases=[]; checked=0
    for n in [32,64,128]:
        base=16
        b=[1+j%14 for j in range(n)]
        offsets=[3,-2,5,0,1,-1,4,2]
        a0=base**(n-1)
        queries=[digits(a0+v,n,base) for v in offsets]
        chain=[(i-1,i) for i in range(1,len(queries))]
        baseline=run(queries,b,base,graph=False,numeric_patches=True)
        coordinate=run(queries,b,base,candidate_edges=chain)
        numeric=run(queries,b,base,numeric_patches=True,candidate_edges=chain)
        state=(baseline['context'],0,list(queries[0]),baseline['outputs'][0])
        warm=run(queries,b,base,numeric_patches=True,candidate_edges=chain,
                 warm_index=0,warm_state=state)
        for result in [baseline,coordinate,numeric,warm]:
            for i,q in enumerate(queries):
                assert as_integer(result['outputs'][i],base)==as_integer(q,base)*as_integer(b,base)
                assert len(result['outputs'][i])==2*n
                checked+=1
        assert numeric['counts']['fresh_products']==1
        assert numeric['counts']['numeric_patches_selected']>=1
        assert numeric['total_arithmetic']<baseline['total_arithmetic']
        # A canonical warm cache includes normalization of its anchor product.
        seed=numeric['preparation_arithmetic']+fresh_weight(n,numeric['context'].m)+4*n
        assert numeric['total_arithmetic']==warm['total_arithmetic']+seed-4*n
        cases.append({'n':n,'offsets':offsets,'candidate_edges':chain,
            'cold_baseline':compact(baseline),'coordinate_chain':compact(coordinate),
            'numeric_chain':compact(numeric),'warm_numeric_chain':compact(warm),
            'previously_paid_canonical_warm_seed_arithmetic':seed,
            'note':'Warm batch rematerializes the anchor output, so seed+warm includes that output normalization twice.'})
    result={'status':'PASS','exact_integer_products_checked':checked,
        'cases':cases,'scope':'Verified signed-block differences across long carry chains; supplied chain edges, every difference checked; no fresh arbitrary-input asymptotic improvement.'}
    Path(__file__).with_name('numeric_shift_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exact_integer_products_checked':checked}))
    for x in cases:
        print(x['n'],{k:x[k]['total_arithmetic'] for k in ['cold_baseline','coordinate_chain','numeric_chain','warm_numeric_chain']})


if __name__=='__main__': main()
