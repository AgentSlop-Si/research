"""Exact prime-free ring and same-B reuse checks, including lengths >291."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from time import perf_counter
from fermat_backend import make_ring,rotate,multiply,ntt,as_integer
from correction_graph import run


def digits(value,n,base):
    out=[]
    for _ in range(n):value,digit=divmod(value,base);out.append(digit)
    assert value==0;return out


def compact(result):
    ring=result['context'].ring
    return {'n':ring.n,'base':ring.base,'m':ring.m,'t':ring.t,
            'modulus_bits':ring.modulus.bit_length(),'counts':result['counts'],
            'preparation_counts':result['preparation_counts'],
            'schedule':result['schedule'],'total_scalar_arithmetic':result['total_scalar_arithmetic']}


def verify(result,queries,b,base):
    target_b=as_integer(b,base)
    for query,out in zip(queries,result['outputs']):
        assert len(out)==2*len(b)
        assert all(isinstance(x,int) and 0<=x<base for x in out)
        assert as_integer(out,base)==as_integer(query,base)*target_b


def main():
    rng=random.Random(107);ring_cases=[];rotation_checks=0
    for n,base in ((1,2),(2,16),(3,256),(8,256),(16,256)):
        c=Counter();ring=make_ring(n,base,c);p=ring.modulus
        values=[0,1,p-1]+[rng.randrange(p) for _ in range(5)]
        for value in values:
            for shift in (-2*ring.t-1,-ring.t,-1,0,1,ring.t,2*ring.t+1):
                assert rotate(value,shift,ring,c)==value*pow(2,shift,p)%p
                rotation_checks+=1
        vector=[rng.randrange(p) for _ in range(ring.m)]
        forward=ntt(vector,ring,c)
        root=pow(2,ring.root_shift,p)
        direct=[sum(value*pow(root,j*k,p) for j,value in enumerate(vector))%p
                for k in range(ring.m)]
        assert forward==direct
        assert ntt(forward,ring,c,inverse=True)==vector
        for _ in range(8):
            a,b=rng.randrange(p),rng.randrange(p)
            assert multiply(a,b,ring,c)==a*b%p
            assert multiply(a,b,ring,c,schoolbook=True)==a*b%p
        for a,b in ((p-1,p-1),(p-1,1),(0,p-1),(p-2,p-1)):
            assert multiply(a,b,ring,c)==a*b%p
        ring_cases.append({'n':n,'base':base,'m':ring.m,'t':ring.t,
                           'modulus':p,'direct_DFT_and_inverse':True})
    composite=make_ring(16,256,Counter())
    assert composite.modulus==2**32+1 and composite.modulus%641==0
    batches=[];verified=0
    for n,base in ((300,16),(512,256),(1024,256),(4096,256)):
        b=[rng.randrange(base) for _ in range(n)]
        center=base**(n-1)
        offsets=[3,-2,5,0,1,-1]
        queries=[digits(center+offset,n,base) for offset in offsets]
        chain=[(j-1,j) for j in range(1,len(queries))]
        started=perf_counter();baseline=run(queries,b,base,graph=False)
        baseline_elapsed=perf_counter()-started
        started=perf_counter();reuse=run(queries,b,base,candidate_edges=chain)
        reuse_elapsed=perf_counter()-started
        anchor=(reuse['context'],0,queries[0],reuse['coefficients'][0])
        warm=run(queries,b,base,candidate_edges=chain,warm_index=0,warm_state=anchor)
        for result in (baseline,reuse,warm):
            verify(result,queries,b,base);verified+=len(queries)
            assert result['counts']['full_output_digit_writes']==2*n*len(queries)
        assert baseline['counts']['fresh_products']==len(queries)
        assert reuse['counts']['fresh_products']==1
        assert warm['counts'].get('fresh_products',0)==0
        assert reuse['counts']['ring_pointwise_products']==reuse['context'].m
        assert warm['counts'].get('ring_pointwise_products',0)==0
        assert reuse['outputs']==baseline['outputs']==warm['outputs']
        batches.append({'n':n,'base':base,'offsets':offsets,'cold_baseline':compact(baseline),
                        'cold_reuse':compact(reuse),'warm_reuse':compact(warm),
                        'audit_elapsed_seconds':{'baseline':baseline_elapsed,'reuse':reuse_elapsed},
                        'timing_scope':'One verification run, not a statistical benchmark or optimized multiplier comparison.'})
    # Neither reconstruction nor correction correctness depends on carry-sparse inputs.
    n=384;base=16;b=[15]*n
    queries=[[rng.randrange(base) for _ in range(n)] for _ in range(3)]
    dense=run(queries,b,base,candidate_edges=[(0,1),(1,2)])
    verify(dense,queries,b,base);verified+=len(queries)
    # Independent pointwise schoolbook path at a known composite modulus.
    queries=[[255]*16,[0]*16];b=[255]*16
    schoolbook=run(queries,b,256,graph=False,schoolbook=True)
    verify(schoolbook,queries,b,256);verified+=len(queries)
    # Numeric sparse offsets have a different, but still finite, coverage ball.
    coverage=[]
    for base,n,s,anchor in ((2,5,1,16),(3,4,1,40),(3,4,2,40)):
        universe=base**n
        center=digits(anchor,n,base)
        numeric=[];coordinate=[]
        for value in range(universe):
            if sum(x!=0 for x in digits(abs(value-anchor),n,base))<=s:numeric.append(value)
            if sum(x!=y for x,y in zip(digits(value,n,base),center))<=s:coordinate.append(value)
        from math import comb
        volume=sum(comb(n,j)*(base-1)**j for j in range(s+1))
        assert len(numeric)<=2*volume-1
        assert len(set(numeric)|set(coordinate))<=3*volume-2
        coverage.append({'base':base,'n':n,'s':s,'anchor':anchor,'numeric_covered':len(numeric),
                         'numeric_upper_bound':2*volume-1,'union_covered':len(set(numeric)|set(coordinate)),
                         'union_upper_bound':3*volume-2,'universe':universe})
    result={'status':'PASS','ring_cases':ring_cases,'rotation_checks':rotation_checks,
            'composite_modulus_control':{'modulus':composite.modulus,'factor':641},
            'exact_integer_products_checked':verified,'batches':batches,
            'dense_control':compact(dense),'pointwise_schoolbook_control':compact(schoolbook),
            'numeric_sparse_coverage_controls':coverage,
            'scope':'Unbounded finite-length prime-free exact backend; no faster worst-case multiplication claim.'}
    root=Path(__file__).resolve().parent
    result['source_hashes']={name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                           for name in ('fermat_backend.py','correction_graph.py','graph_kernels.py')}
    (root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items()
                      if key not in ('batches','dense_control','pointwise_schoolbook_control')},indent=2))


if __name__=='__main__':main()
