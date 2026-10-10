"""Exact A-k graph with the new prime-free backend, retaining prior kernels.

The legacy scalar objective treats one large-ring operation as one scalar
operation. It is NOT a bit-cost optimum or a measured runtime prediction.
The returned counter vector and README expose the growing operand widths.
"""
from fermat_backend import prepare,fresh
from graph_kernels import Counts,validate,discover,plan_mst,update,normalize,fresh_weight


def run(queries,b,base=16,graph=True,warm_index=None,warm_state=None,
        numeric_patches=True,candidate_edges=None,schoolbook=False):
    c=Counts()
    validate(queries,b,base,c)
    if warm_index is not None and (not isinstance(warm_index,int)
            or isinstance(warm_index,bool) or not 0<=warm_index<len(queries)):
        raise ValueError('warm index must name an existing query')
    if warm_state is None:
        ctx=prepare(b,base,c);cached={}
    else:
        ctx,index,anchor_digits,coefficients=warm_state
        if (not isinstance(index,int) or isinstance(index,bool)
                or not 0<=index<len(queries)):
            raise ValueError('cached index must name an existing query')
        c['warm_cache_key_comparisons']+=2*len(b)+3
        if (ctx.b!=tuple(b) or ctx.base!=base or warm_index!=index
                or tuple(queries[index])!=tuple(anchor_digits)):
            raise ValueError('warm state does not match B/base/anchor/index')
        if len(coefficients)!=(2*ctx.n if numeric_patches else 2*ctx.n-1):
            raise ValueError('warm product representation mode mismatch')
        cached={index:list(coefficients)}
        c['warm_coefficient_reads']+=len(coefficients)
        c['warm_coefficient_writes']+=len(coefficients)
    if warm_index is not None and warm_index not in cached:
        raise ValueError('warm anchor must be supplied explicitly')
    preparation=dict(c)
    if graph:
        patches=discover(queries,ctx,c,numeric_patches,candidate_edges)
        order=plan_mst(queries,patches,ctx,c,warm_index,2*ctx.n if numeric_patches else None)
    else:
        patches={}
        order=[(j,-1,0 if j in cached else fresh_weight(ctx.n,ctx.m))
               for j in range(len(queries))]
    after_discovery=dict(c)
    outputs=[None]*len(queries)
    for j,parent,weight in order:
        before=c.arithmetic()
        if parent==-1:
            if j not in cached:cached[j]=fresh(queries[j],ctx,c,schoolbook=schoolbook)
        else:
            cached[j]=update(cached[parent],patches[parent,j],ctx,c)
        assert c.arithmetic()-before==weight
        outputs[j]=normalize(cached[j],ctx.n,base,c)
        if numeric_patches:cached[j]=outputs[j]
    return {'outputs':outputs,'coefficients':cached,'context':ctx,'counts':dict(c),
            'preparation_counts':preparation,'after_discovery_counts':after_discovery,
            'schedule':order,'total_scalar_arithmetic':c.arithmetic(),
            'product_scalar_arithmetic':sum(item[2] for item in order),
            'objective_warning':'Large-ring and digit operations have different bit costs; scalar optimum is not bit optimum.'}
