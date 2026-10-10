"""Targeted independent checks: modular range, carries, keys and duplicates.

This does not rerun the author's complete audit or claim exhaustive validation.
"""
import hashlib
import json
from pathlib import Path
from correction_graph import run,as_integer,fresh_weight


def check_products(result,queries,b,base):
    for q,digits in zip(queries,result['outputs']):
        assert len(digits)==2*len(b)
        assert all(isinstance(x,int) and 0<=x<base for x in digits)
        assert as_integer(digits,base)==as_integer(q,base)*as_integer(b,base)


def rejects(call):
    try:call()
    except ValueError:return True
    raise AssertionError('invalid argument/cache key accepted')


def digits_of(value,n,base):
    result=[]
    for _ in range(n):
        value,digit=divmod(value,base);result.append(digit)
    assert value==0
    return result


def main():
    boundary=[]
    for n,base in ((1,257),(3,16),(291,16)):
        b=[base-1]*n
        queries=[[base-1]*n,[0]*n]
        # Include a negative signed correction and a duplicate target.
        modified=list(queries[0]);modified[n//2]-=1
        queries += [modified,list(modified)]
        result=run(queries,b,base,graph=True)
        check_products(result,queries,b,base)
        boundary.append({'n':n,'base':base,'coefficient_bound':n*(base-1)**2,
                         'products_checked':len(queries),'status':'PASS'})
    invalid_bounds=[
        rejects(lambda:run([[257]],[257],258)),
        rejects(lambda:run([[15]*292],[15]*292,16)),
    ]
    b=[7,6,5];a=[9,8,7];queries=[a,list(a),list(a)]
    duplicate=run(queries,b,16,graph=True)
    check_products(duplicate,queries,b,16)
    assert duplicate['product_arithmetic']==fresh_weight(3,duplicate['context'].m)
    assert duplicate['counts']['fresh_products']==1
    assert duplicate['counts']['correction_products']==2
    assert duplicate['counts']['identical_product_copy_reads']==2*5
    assert duplicate['counts']['identical_product_copy_writes']==2*5
    assert duplicate['counts']['full_output_digit_writes']==3*6
    seed=(duplicate['context'],0,list(a),list(duplicate['coefficients'][0]))
    changed_a=[list(a),list(a)];changed_a[0][0]-=1
    key_controls={
        'A':rejects(lambda:run(changed_a,b,16,warm_index=0,warm_state=seed)),
        'B':rejects(lambda:run(queries,[6,6,5],16,warm_index=0,warm_state=seed)),
        'base':rejects(lambda:run(queries,b,17,warm_index=0,warm_state=seed)),
        'length':rejects(lambda:run([[9,8]]*3,[7,6],16,warm_index=0,warm_state=seed)),
        'index':rejects(lambda:run(queries,b,16,warm_index=1,warm_state=seed)),
        'negative_index':rejects(lambda:run(queries,b,16,warm_index=-1,warm_state=seed)),
        'out_of_range_index':rejects(lambda:run(queries,b,16,warm_index=3,warm_state=seed)),
        'noninteger_base':rejects(lambda:run(queries,b,16.0)),
        'base_one':rejects(lambda:run([[0]],[0],1)),
    }
    # The API accepts a trusted internal cache, not a signed/authenticated one.
    corrupted=list(seed[3]);corrupted[0]+=1
    bad_seed=(seed[0],seed[1],seed[2],corrupted)
    bad=run(queries,b,16,warm_index=0,warm_state=bad_seed)
    assert as_integer(bad['outputs'][0],16)!=as_integer(a,16)*as_integer(b,16)
    carry_cases=[]
    for n in (3,64):
        base=16;b=[15]*n;center=base**(n-1)
        queries=[digits_of(center+k,n,base) for k in (-16,-2,-1,0,1,2,16)]
        result=run(queries,b,base,numeric_patches=True)
        check_products(result,queries,b,base)
        assert all(result['coefficients'][j]==result['outputs'][j]
                   for j in range(len(queries)))
        raw=run(queries,b,base,numeric_patches=False)
        assert result['outputs']==raw['outputs']
        raw_seed=(raw['context'],0,queries[0],raw['coefficients'][0])
        canonical_seed=(result['context'],0,queries[0],result['coefficients'][0])
        assert rejects(lambda:run(queries,b,base,warm_index=0,warm_state=raw_seed,numeric_patches=True))
        assert rejects(lambda:run(queries,b,base,warm_index=0,warm_state=canonical_seed,numeric_patches=False))
        warm=run(queries,b,base,warm_index=0,warm_state=canonical_seed,numeric_patches=True)
        check_products(warm,queries,b,base)
        carry_cases.append({'n':n,'center':'base^(n-1)','offsets':[-16,-2,-1,0,1,2,16],
                            'products_checked':3*len(queries),
                            'numeric_patches_selected':result['counts']['numeric_patches_selected'],
                            'raw_canonical_cache_mismatch_rejected':True})
    n=3;base=16;b=[15]*n;center=base**(n-1)
    queries=[digits_of(center+k,n,base) for k in (-16,-2,-1,0,1,2,16)]
    candidate_cases=[]
    for edges,expected_fresh in (([],7),([(0,1),(2,3)],5),
                                  ([(j,j+1) for j in range(6)]+[(1,0),(0,1)],1)):
        result=run(queries,b,base,numeric_patches=True,candidate_edges=edges)
        check_products(result,queries,b,base)
        assert result['counts']['fresh_products']==expected_fresh
        assert result['counts'].get('candidate_edge_records_read',0)==len(edges)
        candidate_cases.append({'supplied_edge_records':len(edges),
                                 'fresh_products':expected_fresh,'outputs':len(queries)})
    assert rejects(lambda:run(queries,b,base,candidate_edges=[(0,0)]))
    assert rejects(lambda:run(queries,b,base,candidate_edges=[(0,7)]))
    root=Path(__file__).resolve().parent
    report={'status':'PASS','boundary_cases':boundary,'invalid_bound_controls':invalid_bounds,
            'duplicate_arithmetic_edge_weight':0,'duplicate_copy_entries_per_edge':5,
            'duplicate_all_output_digits':18,'warm_key_controls':key_controls,
            'cache_coefficients_require_trusted_provenance':True,
            'numeric_long_carry_cases':carry_cases,
            'candidate_graph_cases':candidate_cases,
            'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                             for name in ('correction_graph.py','audit.py','audit_numeric_shifts.py')}}
    (root/'independent_review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
