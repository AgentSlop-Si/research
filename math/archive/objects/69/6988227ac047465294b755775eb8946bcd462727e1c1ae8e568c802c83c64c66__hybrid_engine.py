"""Phase19 exact hybrid: blind K-small graph ratio -> sparse inverse -> FFT."""
from blind_inverse import (RecurrenceGreen,discover_sparse_circular_inverse,
                           sparse_inverse_forcing)
from blind_discovery import blind_bounded_defects
from annihilator_engine import Work,decode_binomial
from rational_forcing import bluestein_transform


def transform_phase19_hybrid(engine,x,max_defects=2,max_inverse_taps=4):
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    ratio_candidate,ds=blind_bounded_defects(r,p,max_defects)
    work.multiplies+=ds.field_products;work.comparisons+=ds.projective_comparisons
    work.reads+=ds.vector_reads
    meta={'graph_discovery':ds}
    if ratio_candidate is not None:
        d,a,b,K=ratio_candidate
        forcing,branch=decode_binomial(r,d,a,b,engine,work)
        assert branch['K']==K
        meta.update({'selected':'blind-graph','delay':d,'K':K,
                     'resonant':branch['resonant'],'inverse_certificate':None})
    else:
        C,ic=discover_sparse_circular_inverse(r,engine,max_inverse_taps,work)
        meta['inverse_certificate']=ic
        if C is not None:
            forcing=sparse_inverse_forcing(C,engine,work)
            meta.update({'selected':'blind-sparse-inverse','inverse_taps':C,
                         'inverse_support':len(C)})
        else:
            forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
            meta['selected']='fallback'
    y=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    meta['work']=work
    return y,meta

RecurrenceGreen.transform_phase19_hybrid=transform_phase19_hybrid
