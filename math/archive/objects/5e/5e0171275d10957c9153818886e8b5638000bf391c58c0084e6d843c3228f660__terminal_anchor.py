"""One ADD_T at the original source, using the last arbitrary target as anchor."""
from prior_affine_reuse import offset,inverse


def selected_add_t_word(plan,source,target,support=None):
    n,p=plan['n'],plan['p']
    support=list(range(n)) if support is None else sorted(set(support))
    if any(not isinstance(j,int) or j<0 or j>=n for j in support):
        raise ValueError('support must contain valid integer coordinates')
    return [('shear',target+i,source+j,plan['kernel'][i-j])
            for j in support for i in range(j,n)]


def terminal_anchor_word(plan,batches,support=None):
    """Banks x,w,y_0,...,y_(R-1); w is never addressed.

    Output y_r += J^r T P_S x; x and w restored for ALL initial states.
    Dense S gives y_r += T K^r x. For sparse x, choose its exact known support.
    The source never undergoes K or K^-1; scalar ADD_T expansion may transiently
    scale a source coordinate before restoring it, preserving its zero support.
    """
    if batches<1:
        raise ValueError('positive batch count required')
    n,p=plan['n'],plan['p']
    h=batches-1
    anchor=(2+h)*n
    jword=offset(plan['word'],anchor)
    jiword=inverse(jword,p)
    word=[]
    for r in reversed(range(h)):
        word.extend(jiword)
        word.extend(('shear',(2+r)*n+i,anchor+i,p-1) for i in range(n))
    word.extend(selected_add_t_word(plan,0,anchor,support))
    for r in range(h):
        word.extend(('shear',(2+r)*n+i,anchor+i,1) for i in range(n))
        word.extend(jword)
    return word


def scalar_count(n,batches,support=None):
    support=range(n) if support is None else sorted(set(support))
    add_t=3*sum(n-j for j in support)
    return add_t+2*(batches-1)*(11*n-7)


def add_j_word(plan,source,target,sign=1):
    """Direct sparse cross-bank y += sign*J*x; no inverse or clean scratch."""
    n,p=plan['n'],plan['p']
    word=[]
    for i in range(n):
        diagonal=sign*plan['diagonal'][i]%p
        if diagonal:
            word.append(('shear',target+i,source+i,diagonal))
        word.append(('shear',target+i,source+(i+1)%n,sign*plan['weights'][i]%p))
    return word


def difference_word(plan,batches,support=None):
    """Target differences share one ADD_T and preserve arbitrary initial state.

    Descend: y_r -= J*y_(r-1). Add T*P_S*x once into y_0. Ascend:
    y_r += J*y_(r-1). This schedule does not require J to be invertible.
    """
    if batches<1:
        raise ValueError('positive batch count required')
    n=plan['n']
    word=[]
    for r in reversed(range(1,batches)):
        word.extend(add_j_word(plan,(1+r)*n,(2+r)*n,-1))
    word.extend(selected_add_t_word(plan,0,2*n,support))
    for r in range(1,batches):
        word.extend(add_j_word(plan,(1+r)*n,(2+r)*n,1))
    return word


def difference_scalar_count(n,batches,support=None):
    support=range(n) if support is None else sorted(set(support))
    return 3*sum(n-j for j in support)+2*(batches-1)*(6*n-3)
