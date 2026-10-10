from pathlib import Path
import itertools
import json
import math
import random
from correction_graph import run, as_integer, fresh_weight


def compact(result):
    keys=['total_arithmetic','preparation_arithmetic','discovery_arithmetic',
          'product_arithmetic','schedule','counts']
    return {key:result[key] for key in keys}


def datasets(n,q=8):
    base=16
    b=[1+(j%14) for j in range(n)]
    a=[2+(j%11) for j in range(n)]
    related=[]
    for i in range(q):
        x=list(a)
        for j in range(3):
            x[j] += (i>>j)&1
        related.append(x)
    rng=random.Random(1800+n)
    dense=[[rng.randrange(1,base) for _ in range(n)] for _ in range(q)]
    return base,b,{'related':related,'dense':dense}


def verify_products(result,queries,b,base):
    target_b=as_integer(b,base)
    for i,x in enumerate(queries):
        assert as_integer(result['outputs'][i],base) == as_integer(x,base)*target_b
        assert len(result['outputs'][i]) == 2*len(b)
        assert all(0<=v<base for v in result['outputs'][i])
        direct=[0]*(2*len(b)-1)
        for j,u in enumerate(x):
            for k,v in enumerate(b):
                direct[j+k] += u*v
        assert result['coefficients'][i] == direct


def brute_tree_optimum(queries,b,base):
    # Exhaustively enumerate all trees on a super-root plus four query nodes
    # via Prüfer sequences. This independently checks planner optimality.
    cold=run(queries,b,base,graph=True)
    n=len(b); q=len(queries); nodes=q+1
    w={}
    for i in range(q):
        w[i,q]=fresh_weight(n,cold['context'].m)
        for j in range(i+1,q):
            s=sum(a!=z for a,z in zip(queries[i],queries[j]))
            w[i,j]=2*n*s+2*n-1 if s else 0
    best=None; trees=0
    for sequence in itertools.product(range(nodes),repeat=nodes-2):
        degree=[1]*nodes
        for x in sequence: degree[x]+=1
        edges=[]
        for x in sequence:
            leaf=next(i for i in range(nodes) if degree[i]==1)
            edges.append(tuple(sorted((leaf,x))))
            degree[leaf]-=1; degree[x]-=1
        last=[i for i in range(nodes) if degree[i]==1]
        edges.append(tuple(last))
        cost=sum(w[e] for e in edges)
        best=cost if best is None else min(best,cost)
        trees+=1
    assert best==cold['product_arithmetic']
    return trees


def coverage_check():
    q,d,k=3,4,1
    anchors=[(a,)*d for a in range(q)]
    inputs=list(itertools.product(range(q),repeat=d))
    covered=[x for x in inputs if any(sum(a!=b for a,b in zip(x,c))<=k for c in anchors)]
    volume=sum(math.comb(d,j)*(q-1)**j for j in range(k+1))
    assert len(covered)==len(anchors)*volume==27
    witness=next(x for x in inputs if x not in covered)
    return {'alphabet':q,'dimension':d,'radius':k,'anchors':len(anchors),
            'ball_volume':volume,'covered':len(covered),'total':len(inputs),
            'minimum_anchors_from_volume_bound':math.ceil(q**d/volume),
            'uncovered_witness':witness}


def main():
    cases=[]; checked=0
    for n in [32,64,128]:
        base,b,families=datasets(n)
        for family,queries in families.items():
            cold_baseline=run(queries,b,base,graph=False)
            cold_graph=run(queries,b,base,graph=True)
            warm_state=(cold_baseline['context'],0,list(queries[0]),
                        list(cold_baseline['coefficients'][0]))
            warm_baseline=run(queries,b,base,graph=False,warm_index=0,warm_state=warm_state)
            warm_graph=run(queries,b,base,graph=True,warm_index=0,warm_state=warm_state)
            seed_cost=cold_baseline['preparation_arithmetic']+fresh_weight(n,cold_baseline['context'].m)
            assert cold_graph['total_arithmetic']==warm_graph['total_arithmetic']+seed_cost
            for result in [cold_baseline,cold_graph,warm_baseline,warm_graph]:
                verify_products(result,queries,b,base)
                assert result['counts']['full_output_digit_writes']==2*n*len(queries)
                checked+=len(queries)
            if family=='related':
                assert cold_graph['counts']['fresh_products']==1
                assert cold_graph['counts']['correction_products']==7
                assert cold_graph['total_arithmetic']<cold_baseline['total_arithmetic']
                assert warm_graph['counts'].get('fresh_products',0)==0
            else:
                assert cold_graph['counts']['fresh_products']==8
                assert cold_graph['total_arithmetic']>cold_baseline['total_arithmetic']
            cases.append({'n':n,'queries':len(queries),'base':base,'family':family,
                'previously_paid_warm_seed_arithmetic':seed_cost,
                'minimum_pairwise_patch_support':min(cold_graph['correction_supports']),
                'cold_baseline':compact(cold_baseline),'cold_graph':compact(cold_graph),
                'warm_baseline':compact(warm_baseline),'warm_graph':compact(warm_graph)})
    base,b,families=datasets(32)
    trees=brute_tree_optimum(families['related'][:4],b,base)
    duplicate=run([families['related'][0]]*3,b,base,graph=True)
    verify_products(duplicate,[families['related'][0]]*3,b,base)
    assert duplicate['counts']['fresh_products']==1
    assert duplicate['counts']['correction_products']==2
    checked+=3
    # The cache key includes A, B, base and length, preventing stale-plan reuse.
    original=run(families['related'],b,base,graph=False)
    stale=(original['context'],0,[0]*32,original['coefficients'][0])
    try:
        run(families['related'],b,base,warm_index=0,warm_state=stale)
        raise AssertionError('stale cache key accepted')
    except ValueError:
        pass
    invalid_controls=0
    for extra in [{'base':1},{'base':16.0},{'warm_index':-1},
                  {'warm_index':8},{'warm_index':True}]:
        try:
            run(families['related'],b,**extra)
            raise AssertionError('invalid arguments accepted')
        except ValueError:
            invalid_controls+=1
    result={'status':'PASS','exact_integer_products_checked':checked,
            'exhaustive_spanning_trees':trees,'stale_cache_rejected':True,
            'invalid_argument_controls':invalid_controls,
            'coverage_check':coverage_check(),'cases':cases,
            'scope':'Exact finite-size integer products and a declared scalar-operation model; no arbitrary-input multiplication or FFT breakthrough.'}
    Path(__file__).with_name('audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exact_integer_products_checked':checked,
                     'exhaustive_spanning_trees':trees,'coverage_check':result['coverage_check']}))
    for row in cases:
        print(row['n'],row['family'],[(k,row[k]['total_arithmetic']) for k in
              ['cold_baseline','cold_graph','warm_baseline','warm_graph']])


if __name__=='__main__': main()
