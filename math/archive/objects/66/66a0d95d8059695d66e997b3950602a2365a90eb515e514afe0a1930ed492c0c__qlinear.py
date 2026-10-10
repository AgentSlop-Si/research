"""Cold exact full DFT for detected first-order q-linear recurrences.

Arithmetic model: exact field calls, including query-dependent inversions.
This adaptive structural fast path declines arbitrary unstructured inputs.
"""
from collections import Counter


class Counted:
    def __init__(self, field):
        self.field=field; self.zero=field.zero; self.one=field.one
        self.count=Counter()
    def add(self,a,b): self.count['add']+=1; return self.field.add(a,b)
    def sub(self,a,b): self.count['sub']+=1; return self.field.sub(a,b)
    def mul(self,a,b): self.count['mul']+=1; return self.field.mul(a,b)
    def neg(self,a): self.count['neg']+=1; return self.field.neg(a)
    def inv(self,a): self.count['inverse']+=1; return self.field.inv(a)
    def integer(self,a): self.count['integer_embed']+=1; return self.field.integer(a)


def stage(c,before):
    return {k:v-before.get(k,0) for k,v in c.count.items() if v!=before.get(k,0)}


def null_relation(c,rows,width=4):
    """Streaming elimination, storing at most four rows; returns one kernel."""
    basis=[];seen=0
    for values in rows:
        seen+=1;row=list(values)
        for pivot,known in basis:
            factor=row[pivot]
            if factor!=c.zero:
                for j in range(pivot,width):row[j]=c.sub(row[j],c.mul(factor,known[j]))
        pivot=next((j for j,v in enumerate(row) if v!=c.zero),None)
        if pivot is None:continue
        scale=c.inv(row[pivot])
        for j in range(pivot,width):row[j]=c.mul(row[j],scale)
        basis.append((pivot,row));basis.sort(key=lambda item:item[0]) # size <=4
        if len(basis)==width:return None,len(basis),seen
    pivot_set={p for p,_ in basis}
    free=next(j for j in range(width) if j not in pivot_set)
    out=[c.zero]*width;out[free]=c.one
    for pivot,row in reversed(basis):
        value=c.zero
        for j in range(pivot+1,width):value=c.add(value,c.mul(row[j],out[j]))
        out[pivot]=c.neg(value)
    return out,len(basis),seen


def cycle_solve(c,a,b,rhs):
    """Solve a_i*y_i+b_i*y_(i+1)=rhs_i with <=1 free parameter.

Requires b either identically zero or having at most one zero. In diagonal
mode a must have at most one zero. All exact degenerate cases are handled.
Returns particular solution and zero or one kernel vector.
"""
    n=len(a)
    if len(b)!=n or len(rhs)!=n or n<2:raise ValueError('equal cycle lengths required')
    zero_edges=[i for i,v in enumerate(b) if v==c.zero]
    if len(zero_edges)==n:
        out=[c.zero]*n;free=[]
        for i in range(n):
            if a[i]==c.zero:
                if rhs[i]!=c.zero:raise ValueError('inconsistent diagonal row')
                free.append(i)
            else:out[i]=c.mul(rhs[i],c.inv(a[i]))
        if len(free)>1:raise ValueError('nullity exceeds supported bound')
        if not free:return out,[]
        kernel=[c.zero]*n;kernel[free[0]]=c.one
        return out,[kernel]
    if len(zero_edges)>1:raise ValueError('more than one broken cycle edge')
    start=(zero_edges[0]+1)%n if zero_edges else 0
    order=[(start+j)%n for j in range(n)]
    alpha=[c.zero]*n;beta=[c.zero]*n;alpha[start]=c.one
    for i,j in zip(order,order[1:]):
        inverse=c.inv(b[i])
        alpha[j]=c.neg(c.mul(c.mul(a[i],alpha[i]),inverse))
        beta[j]=c.mul(c.sub(rhs[i],c.mul(a[i],beta[i])),inverse)
    last=order[-1]
    coefficient=c.add(c.mul(a[last],alpha[last]),b[last])
    constant=c.sub(rhs[last],c.mul(a[last],beta[last]))
    if coefficient==c.zero:
        if constant!=c.zero:raise ValueError('inconsistent cyclic closure')
        return beta,[alpha]
    parameter=c.mul(constant,c.inv(coefficient))
    return [c.add(v,c.mul(u,parameter)) for u,v in zip(alpha,beta)],[]


def try_qlinear_fourier(field,n,q,query):
    """Detect P(q^i)x_i+Q(q^i)x_(i+1)=0 for every i<N-1.

P,Q have degree <=1 and are not both zero. All accepted full transforms are
computed from scratch, including singular transformed recurrence operators.
"""
    if not isinstance(n,int) or isinstance(n,bool) or n<4 or n&(n-1) or len(query)!=n:
        raise ValueError('dyadic N>=4 and all N input coordinates required')
    c=Counted(field);stages={}
    powers=[field.one]
    for _ in range(1,n):powers.append(c.mul(powers[-1],q))
    if c.mul(powers[-1],q)!=field.one or powers[n//2]==field.one:
        raise ValueError('q must be a primitive Nth root')
    stages['root_preparation_and_validation']=dict(c.count)
    before=dict(c.count)
    rows=([query[i],c.mul(powers[i],query[i]),query[i+1],c.mul(powers[i],query[i+1])]
          for i in range(n-1))
    parameters,rank,seen=null_relation(c,rows)
    stages['relation_discovery']=stage(c,before)
    meta=dict(accepted=False,relation_rank=rank,relation_rows_read=seen,
              stages=stages,field_operations=dict(c.count),full_output_writes=0,
              paid_anchor_transforms=0,ordinary_fft_calls=0)
    if parameters is None:
        meta['reason']='no_first_order_qlinear_relation';return None,meta
    p0,p1,q0,q1=parameters
    before=dict(c.count)
    source_a=[c.add(p0,c.mul(p1,v)) for v in powers]
    source_b=[c.add(q0,c.mul(q1,v)) for v in powers]
    residual=[c.add(c.mul(source_a[i],query[i]),c.mul(source_b[i],query[(i+1)%n]))
              for i in range(n)]
    if any(v!=field.zero for v in residual[:-1]):raise AssertionError('relation verification failed')
    # Only the cyclic endpoint can be nonzero; its full DFT is an explicit mode.
    forcing=[c.mul(residual[-1],powers[-k%n]) for k in range(n)]
    target_a=[c.add(p0,c.mul(q0,powers[-k%n])) for k in range(n)]
    target_b=[c.add(p1,c.mul(q1,powers[(-k-1)%n])) for k in range(n)]
    stages['operators_full_residual_and_forcing']=stage(c,before)
    before=dict(c.count)
    result,kernel=cycle_solve(c,target_a,target_b,forcing)
    stages['target_cyclic_solve']=stage(c,before)
    constraint_index=None
    if kernel:
        before=dict(c.count)
        _,source_kernel=cycle_solve(c,source_a,source_b,[field.zero]*n)
        if len(source_kernel)!=1:raise AssertionError('similar operators have different nullity')
        constraint_index=next(i for i,v in enumerate(source_kernel[0]) if v!=field.zero)
        h=kernel[0];base=field.zero;scale=field.zero
        for k in range(n):
            phase=powers[(-k*constraint_index)%n]
            base=c.add(base,c.mul(phase,result[k]))
            scale=c.add(scale,c.mul(phase,h[k]))
        if scale==field.zero:raise AssertionError('source coordinate fails to separate kernel')
        parameter=c.mul(c.sub(c.mul(c.integer(n),query[constraint_index]),base),c.inv(scale))
        result=[c.add(v,c.mul(parameter,u)) for v,u in zip(result,h)]
        stages['source_kernel_and_input_constraint']=stage(c,before)
    meta.update(accepted=True,parameters=parameters,field_operations=dict(c.count),
                full_output_writes=n,endpoint_defect_nonzero=residual[-1]!=field.zero,
                target_nullity=len(kernel),constraint_index=constraint_index,
                full_source_rows_verified=n)
    return result,meta
