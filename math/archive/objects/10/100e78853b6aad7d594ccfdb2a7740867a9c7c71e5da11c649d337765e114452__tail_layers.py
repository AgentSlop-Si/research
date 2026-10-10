"""Exact fast first tail layer and explicit finite-tail recurrence.

The seed uses an ordinary exact radix-2 Fourier backend and is O(N log N), not
an improved FFT. A prefix with K additional layers costs O(N log N + K N).
"""
from dataclasses import dataclass
from fixed_kernel import Counted, prepare
from operators import prepare_sparse, apply_sparse_c


@dataclass
class TailPlan:
    n: int
    q: object
    powers: list
    kernel: list
    sigma: list
    sigma_inverse: list
    spectrum: list
    inverse_n: object
    sparse: object
    alpha: list
    beta: list
    preparation: dict


def prepare_tail(field,n,q):
    base=prepare(field,n,q)
    sparse=prepare_sparse(field,n,q)
    c=Counted(field)
    powers=[field.one]
    for _ in range(1,n):
        powers.append(c.mul(powers[-1],q))
    sigma=[]; sigma_inverse=[]
    for j in range(n):
        s=c.mul(powers[(-j)%n],base.kernel[j])
        t=c.mul(powers[j],base.factorial[j])
        sigma.append(c.neg(s) if j%2 else s)
        sigma_inverse.append(c.neg(t) if j%2 else t)
    inverse_n=base.kernel[-1]
    inverse_2n=c.mul(inverse_n,c.inv(field.integer(2)))
    spectrum=[]
    for k in range(n):
        r=(n//2-k)%n
        numerator=-(n-1) if r==0 else n+1-2*r
        spectrum.append(c.mul(field.integer(numerator),inverse_2n))
    alpha=[field.zero]; beta=[field.zero]
    for k in range(1,n):
        a=c.mul(base.factorial[k-1],base.kernel[k])
        alpha.append(a)
        beta.append(c.mul(c.mul(base.kernel[k],inverse_n),a))
    return TailPlan(n,q,powers,base.kernel,sigma,sigma_inverse,spectrum,inverse_n,
                    sparse,alpha,beta,{'q_factorial':base.preparation,
                    'sparse_C':sparse.preparation,'additional':dict(c.count)})


def fft_exact(field,values,powers,inverse=False,inverse_n=None):
    """Radix-2 positive-exponent DFT; all scalar gates go through field.

The supplied q-powers are prepared once. Bit reversal, loop indexing, reads,
writes, and copies take O(N log N) word work or less and are not called free.
"""
    n=len(values)
    out=list(values)
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit; bit>>=1
        j^=bit
        if i<j:
            out[i],out[j]=out[j],out[i]
    length=2
    while length<=n:
        half=length//2; stride=n//length
        for start in range(0,n,length):
            for j in range(half):
                exponent=j*stride
                if inverse:
                    exponent=(-exponent)%n
                a=out[start+j]
                b=field.mul(powers[exponent],out[start+j+half])
                out[start+j]=field.add(a,b)
                out[start+j+half]=field.sub(a,b)
        length*=2
    if inverse:
        if inverse_n is None:
            raise ValueError('charged prepared inverse_n required')
        out=[field.mul(inverse_n,value) for value in out]
    return out


def _seed(field,plan,x):
    v=[field.mul(a,b) for a,b in zip(plan.sigma_inverse,x)]
    v=fft_exact(field,v,plan.powers)
    v=[field.mul(a,b) for a,b in zip(plan.spectrum,v)]
    v=fft_exact(field,v,plan.powers,True,plan.inverse_n)
    return [field.mul(a,b) for a,b in zip(plan.sigma,v)]


def apply_seed(field,plan,x):
    if len(x)!=plan.n:
        raise ValueError('wrong input length')
    c=Counted(field)
    out=_seed(c,plan,x)
    return out,{'field_operations':dict(c.count),'fft_calls':2,
                'fft_length':plan.n,'full_output_coordinates':plan.n,
                'word_work':'O(N log N), including addressing and copies'}


def apply_tail_prefix(field,plan,x,k):
    """Return sum_(j=0..k) F_(N+j) x, 0<=k<=N-2, exactly.

Computes a tail prefix, not an approximation to H_q(C). k=N-2 returns the full
tail but has quadratic cost; k=O(1) is an O(N log N) restricted operator query.
"""
    n=plan.n
    if len(x)!=n or not 0<=k<=n-2:
        raise ValueError('wrong input length or tail-prefix endpoint')
    c=Counted(field)
    current=_seed(c,plan,x)
    total=list(current)
    wx=list(x); ux=list(x)
    for layer in range(1,k+1):
        wx=[c.mul(plan.sparse.upper[i],wx[i+1]) for i in range(n-1)]+[c.mul(plan.sparse.corner,wx[0])]
        ux=[c.mul(plan.sparse.diagonal[i],ux[i]) for i in range(n)]
        cy=apply_sparse_c(c,plan.sparse,current)
        phase=plan.powers[layer]
        current=[c.sub(c.mul(plan.alpha[layer],cy[i]),
                  c.mul(plan.beta[layer],c.sub(c.mul(phase,wx[i]),ux[i]))) for i in range(n)]
        total=[c.add(total[i],current[i]) for i in range(n)]
    return total,{'field_operations':dict(c.count),'fft_calls':2,'fft_length':n,
        'additional_layers':k,'sparse_C_matvecs':k,
        'live_vector_storage':'O(N); previous layers are not retained',
        'word_work':'O(N log N + k N), including addressing and full output'}
