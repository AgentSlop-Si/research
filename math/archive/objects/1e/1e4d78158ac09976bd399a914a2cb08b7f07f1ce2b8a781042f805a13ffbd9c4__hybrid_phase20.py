"""Phase20 hybrid, preserving exact Phase19 lineages and adding resultant gate.

All residual transformations and FFT fallbacks are charged. It is an
adaptive structured-input optimizer, not a generic asymptotic breakthrough.
"""
from annihilator_engine import Work,decode_binomial
from blind_discovery import blind_bounded_defects
from blind_inverse import sparse_inverse_forcing
from inverse_reuse import discover_sparse_circular_inverse_reuse
from annihilator_engine import direct_one_frequency
from resultant_gate import discover_resultant
from rational_forcing import bluestein_transform


def transform_hybrid_phase20(engine,x,max_defects=2,max_inverse_taps=4):
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('bad input size')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    candidate,ds=blind_bounded_defects(r,p,max_defects)
    work.multiplies+=ds.field_products
    work.comparisons+=ds.projective_comparisons
    work.reads+=ds.vector_reads
    meta={'phase19_ratio':ds,'phase19_inverse':None,'phase20_resultant':None}
    if candidate is not None:
        delta,a,b,K=candidate
        forcing,dec=decode_binomial(r,delta,a,b,engine,work)
        meta.update({'selected':'phase19-blind-ratio','defects':K,'detected_shift':delta})
    else:
        # Shared spectral bank: Phase19 inverse interpolation and Phase20
        # Hankel resultant both need exactly the first eight F(r) entries.
        # Pay for each dot product once, including generic fallback inputs.
        count=2*max_inverse_taps
        if count!=8:  # Other tap limits are supported but not shared here.
            prefix=None
        else:
            prefix=[direct_one_frequency(r,engine.powers[k],p,work)
                    for k in range(8)]
        C,ic=discover_sparse_circular_inverse_reuse(
            r,engine,max_inverse_taps,work,frequency_prefix=prefix)
        meta['phase19_inverse']=ic
        if C is not None:
            forcing=sparse_inverse_forcing(C,engine,work)
            meta.update({'selected':'phase19-blind-inverse','inverse_taps':C})
        else:
            choice,rs=discover_resultant(r,engine,work,frequency_prefix=prefix)
            meta['phase20_resultant']=rs
            if choice is not None:
                delta,alpha,h=choice
                forcing,dec=decode_binomial(r,delta,alpha,1,engine,work,forcing_method='direct')
                meta.update({'selected':'phase20-blind-two-defect',
                             'detected_shift':delta,'detected_alpha':alpha,
                             'defects':len(h),'resonant':dec['resonant']})
            else:
                forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
                meta['selected']='fallback'
    y=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    meta['work']=work
    return y,meta
