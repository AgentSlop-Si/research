"""Exact rank-one cyclic graph feedback with no additional transform call."""
from collections import Counter
from prior_affine_reuse import add_t_word,inverse


def add_j_word(plan,source,target,sign=1):
    n,p=plan['n'],plan['p']
    result=[]
    for i in range(n):
        value=sign*plan['diagonal'][i]%p
        if value:
            result.append(('shear',target+i,source+i,value))
        result.append(('shear',target+i,source+(i+1)%n,sign*plan['weights'][i]%p))
    return result


def rank_one_add(p,functional,target,vector):
    """y += vector*(sum_j functional[j]*register[j]); all sources restored.

    Source registers and target registers must be disjoint. No clean scratch.
    A source pivot temporarily stores the linear functional, then is uncomputed.
    """
    functional={i:a%p for i,a in functional.items() if a%p}
    vector=[a%p for a in vector]
    if not functional or not any(vector):
        return [],{'functional_nonzeros':len(functional),'output_nonzeros':sum(bool(a) for a in vector),
                   'scalar_instructions':0,'source_pivot_inverse':0}
    if any(target<=i<target+len(vector) for i in functional):
        raise ValueError('source and target registers must be disjoint')
    pivot=min(functional)
    before=[('scale',pivot,functional[pivot])]
    before.extend(('shear',pivot,i,a) for i,a in sorted(functional.items()) if i!=pivot)
    middle=[('shear',target+i,pivot,a) for i,a in enumerate(vector) if a]
    word=before+middle+inverse(before,p)
    m,k=len(functional),sum(bool(a) for a in vector)
    return word,{'functional_nonzeros':m,'output_nonzeros':k,
                 'scalar_instructions':6*m+3*k-4,'source_pivot_inverse':1}


class Counted:
    def __init__(self,p):
        self.p=p
        self.count=Counter()
    def mul(self,a,b):
        self.count['mul']+=1
        return a*b%self.p
    def add(self,a,b):
        self.count['add']+=1
        return (a+b)%self.p
    def sub(self,a,b):
        self.count['sub']+=1
        return (a-b)%self.p
    def inv(self,a):
        self.count['constant_inverse']+=1
        return pow(a,-1,self.p)


def prepare_feedback(plan,batches,u,observed):
    """Feedback closes last target to first by u*e_observed^T.

    Stores ell_r = (K^T)^(R-1-r) T^T e_observed for every injection vertex r.
    No T action is called: its one needed row is already known kernel data.
    """
    n,p=plan['n'],plan['p']
    if batches<1 or len(u)!=n or not 0<=observed<n:
        raise ValueError('invalid dimensions')
    c=Counted(p)
    a=[int(i==observed) for i in range(n)]
    ell=[plan['kernel'][observed-i] if i<=observed else 0 for i in range(n)]
    rows=[None]*batches
    rows[-1]=ell[:]
    for step in range(batches-1):
        a=[c.add(c.mul(plan['diagonal'][i],a[i]),
                 c.mul(plan['weights'][(i-1)%n],a[(i-1)%n])) for i in range(n)]
        ell=[ell[0]]+[c.add(ell[i],c.mul(plan['weights'][i-1],ell[i-1])) for i in range(1,n)]
        rows[batches-2-step]=ell[:]
    dot=c.mul(a[0],u[0])
    for i in range(1,n):
        dot=c.add(dot,c.mul(a[i],u[i]))
    kappa=c.sub(1,dot)
    if kappa==0:
        raise ValueError('singular feedback: kappa = 0')
    reciprocal=c.inv(kappa)
    output=[c.mul(value,reciprocal) for value in u]
    return {'u':[value%p for value in u],'observed':observed,'batches':batches,
            'a':a,'rows':rows,'kappa':kappa,'output':output,
            'coefficient_preparation':dict(c.count)}


def feedback_word(plan,feedback,injections):
    """Each (vertex,source_bank) supplies an independent T*x injection.

    Sources precede one arbitrary untouched w bank, then R arbitrary targets.
    Targets solve z_0=T*x_0+u*z_last[observed], z_r=T*x_r+J*z_(r-1),
    with absent injections treated as zero. All original registers are retained
    except additive target increments. Repeated source banks are allowed.
    """
    n,p=plan['n'],plan['p']
    batches=feedback['batches']
    if not injections:
        raise ValueError('at least one injection required')
    if any(not 0<=vertex<batches or source<0 for vertex,source in injections):
        raise ValueError('invalid injection')
    source_banks=1+max(source for vertex,source in injections)
    target_base=(source_banks+1)*n
    word=[]
    for r in reversed(range(1,batches)):
        word.extend(add_j_word(plan,target_base+(r-1)*n,target_base+r*n,-1))
    for vertex,source in injections:
        word.extend(add_t_word(plan,source*n,target_base+vertex*n))
    functional={}
    for vertex,source in injections:
        for i,value in enumerate(feedback['rows'][vertex]):
            index=source*n+i
            functional[index]=(functional.get(index,0)+value)%p
    correction,rank_cost=rank_one_add(p,functional,target_base,feedback['output'])
    word.extend(correction)
    for r in range(1,batches):
        word.extend(add_j_word(plan,target_base+(r-1)*n,target_base+r*n,1))
    baseline=3*len(injections)*n*(n+1)//2+2*(batches-1)*(6*n-3)
    return word,{'source_banks':source_banks,'target_base':target_base,
                 'ADD_T_calls':len(injections),'feedback_extra_ADD_T_calls':0,
                 'acyclic_scalar_instructions':baseline,'rank_one_correction':rank_cost,
                 'scalar_instructions':baseline+rank_cost['scalar_instructions'],
                 'coefficient_accumulations':len(injections)*n}


def gain_update_word(plan,feedback,injections,old_gain,new_gain):
    """Change only the closing-edge gain, using one exact rank-one correction.

    No ADD_T is emitted. `feedback` stores the unscaled base edge u*e_j^T;
    both old and new gains must have nonsingular closed loops.
    """
    n,p,R=plan['n'],plan['p'],feedback['batches']
    if not injections:
        raise ValueError('at least one injection required')
    if any(not 0<=vertex<R or source<0 for vertex,source in injections):
        raise ValueError('invalid injection')
    c=Counted(p)
    beta=c.sub(1,feedback['kappa'])
    old_kappa=c.sub(1,c.mul(old_gain,beta))
    new_kappa=c.sub(1,c.mul(new_gain,beta))
    if old_kappa==0 or new_kappa==0:
        raise ValueError('singular old or new feedback gain')
    numerator=c.sub(new_gain,old_gain)
    denominator=c.mul(old_kappa,new_kappa)
    delta=c.mul(numerator,c.inv(denominator))
    vector=[]
    current=feedback['u'][:]
    for r in range(R):
        vector.extend(c.mul(delta,value) for value in current)
        if r+1<R:
            current=[c.add(c.mul(plan['diagonal'][i],current[i]),
                           c.mul(plan['weights'][i],current[(i+1)%n])) for i in range(n)]
    source_banks=1+max(source for vertex,source in injections)
    target_base=(source_banks+1)*n
    functional={}
    for vertex,source in injections:
        for i,value in enumerate(feedback['rows'][vertex]):
            index=source*n+i
            functional[index]=(functional.get(index,0)+value)%p
    word,rank_cost=rank_one_add(p,functional,target_base,vector)
    return word,{'old_gain':old_gain,'new_gain':new_gain,'old_kappa':old_kappa,
                 'new_kappa':new_kappa,'ADD_T_calls':0,'correction_scalar':delta,
                 'rank_one_correction':rank_cost,'coefficient_preparation':dict(c.count),
                 'coefficient_accumulations':len(injections)*n}
