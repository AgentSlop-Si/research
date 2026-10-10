"""Exact full Fourier transform from a supplied composition of affine filters.

Dependencies are explicit siblings, copied unchanged into any portable bundle.
Continuous filter parameters are supplied, never discovered for free.
"""
import sys
from collections import Counter
from pathlib import Path

DEPENDENCY=Path(__file__).resolve().parent.parent/'fft_bidirectional_graph_research'
sys.path.insert(0,str(DEPENDENCY))
from affine_cycle import Counted, cycle_order, ordinary_fft


def prepared_cycle_solve(c,permutation,coefficients,rhs,closure_inverse):
    """Use a previously proved/counted cycle closure inverse; costs4N+1."""
    order=cycle_order(permutation); value=c.zero
    for j in reversed(order): value=c.add(rhs[j],c.mul(coefficients[j],value))
    value=c.mul(value,closure_inverse)
    result=[c.zero]*len(order)
    for j in reversed(order):
        value=c.add(rhs[j],c.mul(coefficients[j],value))
        result[j]=value
    return result


def try_composed_fourier(field,query,q,filters,lambdas,max_defects=1):
    """Apply L_d ... L_1 x; transform sparse residual; invert in reverse order.

    Filter entries are (a,b,shift,lambda_index), with a=1 mod4 and odd b,shift.
    Lambda pooling is explicit. Every pool value must be used; no inequality
    or equality oracle for parameter discovery is assumed.
    """
    n=len(query)
    if n<4 or n&(n-1): raise ValueError('dyadic N>=4 required')
    if not isinstance(max_defects,int) or max_defects<0: raise ValueError('invalid defect budget')
    filters=list(filters);lambdas=list(lambdas)
    if not filters or not lambdas: raise ValueError('at least one filter and lambda required')
    for item in filters:
        if len(item)!=4 or any(not isinstance(v,int) for v in item): raise ValueError('integer filter descriptor required')
        a,b,shift,index=item
        if a%4!=1 or b%2!=1 or shift%2!=1: raise ValueError('full-cycle affine parameters required')
        if not 0<=index<len(lambdas): raise ValueError('invalid lambda pool index')
    if set(item[3] for item in filters)!=set(range(len(lambdas))): raise ValueError('unused lambda pool entry')
    filters=[(a%n,b%n,shift%n,index) for a,b,shift,index in filters]
    c=Counted(field);stages={};previous={}
    def checkpoint(name):
        nonlocal previous
        stages[name]={k:v-previous.get(k,0) for k,v in c.count.items() if v!=previous.get(k,0)}
        previous=dict(c.count)
    def finish(result,reason,**extra):
        meta=dict(accepted=result is not None,reason=reason,field_operations=dict(c.count),
                  stages=stages,filter_count=len(filters),lambda_pool_size=len(lambdas),
                  full_output_writes=n if result is not None else 0,
                  supplied_parameters=True,ordinary_fft_calls=0)
        meta.update(extra)
        return result,meta
    roots=[c.one]
    for _ in range(1,n):roots.append(c.mul(roots[-1],q))
    if c.mul(roots[-1],q)!=c.one or roots[n//2]==c.one: raise ValueError('primitive Nth root required')
    checkpoint('root_table_and_validation')
    scaled=[];closure=[]
    for parameter in lambdas:
        power=parameter
        for _ in range(n.bit_length()-1):power=c.mul(power,power)
        denominator=c.add(c.one,power)
        if denominator==c.zero:
            checkpoint('shared_coefficient_and_closure_preparation')
            return finish(None,'singular_filter')
        closure.append(c.inv(denominator))
        scaled.append([c.mul(parameter,v) for v in roots])
    checkpoint('shared_coefficient_and_closure_preparation')
    current=list(query);intermediate_support=[]
    for a,b,shift,index in filters:
        permutation=[(a*j+shift)%n for j in range(n)]
        cycle_order(permutation)
        current=[c.sub(value,c.mul(scaled[index][(b*j)%n],current[permutation[j]]))
                 for j,value in enumerate(current)]
        intermediate_support.append(sum(v!=c.zero for v in current))
    checkpoint('all_composed_source_rows')
    defects=[(j,v) for j,v in enumerate(current) if v!=c.zero]
    if len(defects)>max_defects:
        return finish(None,'composed_defect_budget_exceeded',actual_defects=len(defects),
                      intermediate_support=intermediate_support)
    current=[c.zero]*n
    for j,value in defects:
        for k in range(n):current[k]=c.add(current[k],c.mul(value,roots[(j*k)%n]))
    checkpoint('complete_sparse_defect_transform')
    for a,b,shift,index in reversed(filters):
        inverse_a=pow(a,-1,n)
        permutation=[inverse_a*(k+b)%n for k in range(n)]
        coefficients=[scaled[index][(-shift*j)%n] for j in permutation]
        current=prepared_cycle_solve(c,permutation,coefficients,current,closure[index])
    checkpoint('reverse_order_target_cycle_solves')
    return finish(current,'accepted',actual_defects=len(defects),
                  intermediate_support=intermediate_support,
                  expected_total=(1+len(lambdas)+6*len(filters)+2*len(defects))*n
                                 +len(lambdas)*(n.bit_length()+1)+len(filters))


def composed_fft_or_fallback(field,query,q,filters,lambdas,max_defects=1):
    """All-input wrapper; for fixed d,r,s the failed attempt adds O(N) work."""
    result,meta=try_composed_fourier(field,query,q,filters,lambdas,max_defects)
    meta['composition_accepted']=meta['accepted']
    if result is not None:return result,meta
    result,baseline=ordinary_fft(field,query,q)
    meta['fallback_field_operations']=baseline
    meta['stages']['ordinary_fft_fallback']=baseline
    meta['field_operations']=dict(Counter(meta['field_operations'])+Counter(baseline))
    meta.update(accepted=True,full_output_writes=len(query),ordinary_fft_calls=1)
    return result,meta
