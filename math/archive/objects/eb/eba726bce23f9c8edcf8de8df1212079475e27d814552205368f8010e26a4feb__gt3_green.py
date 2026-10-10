"""Phase25 mixed-radix deferred Green certification, all-input exact fallback.

This wraps the *unchanged* Phase23/24 sparse-rational detector with the new
Good-Thomas-3 deferred graph. Every candidate receives the existing full
cyclic-convolution certificate, with an exact Good-Thomas FFT fallback.
"""
from gt3_deferred import DeferredGT3
from annihilator_engine import Work,batch_inverse_nonzero
from short_probe_fusion import discover_short_probe
from reciprocal_union import factor_sparse_hypercube


def transform_deferred_conjugate_gt3(engine,x,s=4):
    n,p=engine.n,engine.p
    if len(x)!=n or n%3:raise ValueError('requires x length N=3*2**t')
    m=2*s+2
    if m>=n:raise ValueError('N too small for certificate preview')
    session=DeferredGT3(x,p,engine.primitive_gen)
    if session.omega!=engine.omega:raise ValueError('root mismatch')
    co=Work()
    wanted=list(range(m))+[n-1]
    preview=session.preview(wanted)
    first=session.stats()
    co.additions+=first['field_additions'];co.multiplies+=first['field_multiplications']
    # On a generic rejection, no residual is ever computed.
    probes=[(engine.L.diag[k]*preview[k]+engine.L.shift*preview[k-1 if k else n-1])%p
            for k in range(m)]
    co.multiplies+=2*m;co.additions+=m
    residual=[None]
    def materialize():
        if residual[0] is None:
            residual[0]=engine.P.apply(x)
            co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
        return residual[0]
    found,meta=discover_short_probe(None,engine,co,s=s,
                                    prefix_R=probes,residual_loader=materialize)
    factors=None
    if found is None:
        y=session.full()
        last=session.stats()
        co.multiplies+=last['field_multiplications']-first['field_multiplications']
        co.additions+=last['field_additions']-first['field_additions']
        selected='gt3-fallback'
    else:
        A,delta,alpha,Ahat=found
        if len(A) in (2,4,8,16):
            factors=factor_sparse_hypercube(A,delta,alpha,n,p,
                 len(A).bit_length()-1,co)
        wk=1;w=engine.powers[delta];numerator=[]
        for k in range(n):
            numerator.append((1-alpha*wk)%p)
            wk=wk*w%p;co.multiplies+=2;co.additions+=1
        inverse=batch_inverse_nonzero(Ahat,p,co)
        forcing=[numerator[k]*inverse[k]%p for k in range(n)]
        co.multiplies+=n
        y=engine.L.solve(forcing)
        co.multiplies+=3*n+1;co.additions+=2*n
        last=session.stats()
        selected='gt3-certified'
    return y,dict(selected=selected,work=co,meta=meta,
           preview=first,fft_graph=last,residual_computed=residual[0] is not None,
           graph_factors=factors,
           native_gt3_reference_ops=session.predicted_full_arithmetic())
