"""Exact integer products for few-run or near-repeated-digit operands.

No FFT, floating point, whole-integer multiplication, or division by a huge
integer occurs. All arithmetic kernels work on base-beta digits.
"""
from collections import Counter


def _trim(digits):
    while len(digits)>1 and digits[-1]==0:
        digits.pop()
    return digits


def _validate(values,base):
    digits=list(values)
    if not digits or any(not isinstance(d,int) or isinstance(d,bool) or not 0<=d<base for d in digits):
        raise ValueError('digits must be a nonempty sequence of integers in [0,base)')
    return _trim(digits)


def _add(a,b,base,stats):
    out=[]; carry=0
    for i in range(max(len(a),len(b))):
        value=(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)+carry
        carry,digit=divmod(value,base)
        out.append(digit)
        stats['add_digit_steps']+=1
    if carry:out.append(carry)
    return _trim(out)


def _subtract(a,b,base,stats):
    """Nonnegative subtraction; every intermediate is at most one digit wide."""
    out=[]; borrow=0
    for i in range(max(len(a),len(b))):
        value=(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0)-borrow
        borrow=int(value<0)
        out.append(value+base if borrow else value)
        stats['subtract_digit_steps']+=1
    if borrow:raise ArithmeticError('internal subtraction became negative')
    return _trim(out)


def _multiply_small(a,scalar,base,stats):
    if scalar==0:return [0]
    out=[]; carry=0
    for digit in a:
        carry,value=divmod(scalar*digit+carry,base)
        out.append(value)
        stats['small_multiply_digit_steps']+=1
    if carry:out.append(carry)
    return _trim(out)


def _divide_small(a,divisor,base,stats):
    out=[0]*len(a); remainder=0
    for i in range(len(a)-1,-1,-1):
        out[i],remainder=divmod(remainder*base+a[i],divisor)
        stats['small_divide_digit_steps']+=1
    if remainder:raise ArithmeticError('repunit division was not exact')
    return _trim(out)


def _shift(a,amount,stats):
    if a==[0]:return [0]
    stats['shift_zero_writes']+=amount
    stats['shift_digit_copies']+=len(a)
    return [0]*amount+list(a)


def _repdigit_product(b,digit,length,base,stats):
    """digit * B * (base**length-1)/(base-1), via single-digit kernels."""
    if digit==0:return [0]
    scaled=_multiply_small(b,digit,base,stats)
    numerator=_subtract(_shift(scaled,length,stats),scaled,base,stats)
    return _divide_small(numerator,base-1,base,stats)


def _decompositions(a):
    candidate=0; balance=0
    for digit in a:
        if balance==0:candidate=digit
        balance+=1 if digit==candidate else -1
    exceptions=tuple((i,d-candidate) for i,d in enumerate(a) if d!=candidate)
    sparse=tuple((i,d) for i,d in enumerate(a) if d)
    runs=[]; start=0
    for i in range(1,len(a)+1):
        if i==len(a) or a[i]!=a[start]:
            if a[start]:runs.append((start,i-start,a[start]))
            start=i
    return [('baseline-exceptions',1+len(exceptions),(candidate,exceptions)),
            ('sparse-digits',len(sparse),sparse),
            ('constant-runs',len(runs),tuple(runs))]


def try_structured_product(a_digits,b_digits,base=256,*,max_terms=8):
    """Return (product_digits,stats), or (None,stats) if the fast path declines.

    Digits are least significant first. max_terms controls structural work,
    not a purported universal speedup. The caller owns the general fallback.
    """
    if not isinstance(base,int) or isinstance(base,bool) or base<2:
        raise ValueError('base must be an integer at least two')
    if not isinstance(max_terms,int) or isinstance(max_terms,bool) or max_terms<0:
        raise ValueError('max_terms must be a nonnegative integer')
    original_a,original_b=list(a_digits),list(b_digits)
    a,b=_validate(original_a,base),_validate(original_b,base)
    stats=Counter(input_digit_count=len(original_a)+len(original_b))
    if a==[0] or b==[0]:
        stats.update(accepted=1,zero_product=1,output_digits=1)
        return [0],dict(stats)
    choices=[]
    for orientation,(left,right) in enumerate(((a,b),(b,a))):
        for priority,(method,terms,details) in enumerate(_decompositions(left)):
            choices.append((terms,priority,orientation,method,details,left,right))
    terms,_,orientation,method,details,left,right=min(choices,key=lambda item:item[:3])
    stats['planning_digit_visits']=4*(len(a)+len(b))
    metadata=dict(stats,method=method,structural_terms=terms,orientation=orientation,
                  max_terms=max_terms,base=base)
    if terms>max_terms:
        metadata['accepted']=False
        return None,metadata
    if method=='baseline-exceptions':
        digit,exceptions=details
        out=_repdigit_product(right,digit,len(left),base,stats)
        for location,delta in exceptions:
            shifted=_shift(_multiply_small(right,abs(delta),base,stats),location,stats)
            out=(_add(out,shifted,base,stats) if delta>0
                 else _subtract(out,shifted,base,stats))
    elif method=='sparse-digits':
        out=[0]
        for location,digit in details:
            shifted=_shift(_multiply_small(right,digit,base,stats),location,stats)
            out=_add(out,shifted,base,stats)
    else:
        out=[0]
        for location,length,digit in details:
            block=_repdigit_product(right,digit,length,base,stats)
            out=_add(out,_shift(block,location,stats),base,stats)
    assert all(0<=digit<base for digit in out)
    metadata.update(stats)
    metadata.update(accepted=True,output_digits=len(out),
                    digit_kernel_steps=sum(stats[key] for key in
                       ('add_digit_steps','subtract_digit_steps',
                        'small_multiply_digit_steps','small_divide_digit_steps')))
    return out,metadata


def try_structured_convolution(a_digits,b_digits,base=256,*,max_terms=8):
    """Full ordinary integer coefficient convolution on the same restricted path.

    A shared prefix-sum table evaluates all constant-run window contributions.
    Unlike try_structured_product, coefficients have O(log N + log(base)) bits.
    Leading zero coefficients are preserved in the requested output length.
    """
    if not isinstance(base,int) or isinstance(base,bool) or base<2:
        raise ValueError('base must be an integer at least two')
    if not isinstance(max_terms,int) or isinstance(max_terms,bool) or max_terms<0:
        raise ValueError('max_terms must be a nonnegative integer')
    a,b=list(a_digits),list(b_digits)
    va,vb=_validate(a,base),_validate(b,base)
    length=len(a)+len(b)-1
    if va==[0] or vb==[0]:
        return [0]*length,{'accepted':True,'zero_product':True,'output_coefficients':length}
    choices=[]
    for orientation,(left,right) in enumerate(((a,b),(b,a))):
        for priority,(method,terms,details) in enumerate(_decompositions(left)):
            choices.append((terms,priority,orientation,method,details,left,right))
    terms,_,orientation,method,details,left,right=min(choices,key=lambda item:item[:3])
    info={'accepted':terms<=max_terms,'method':method,'structural_terms':terms,
          'orientation':orientation,'input_coefficients':len(a)+len(b),
          'planning_digit_visits':4*(len(a)+len(b)),
          'output_coefficients':length,'coefficient_updates':0}
    if terms>max_terms:return None,info
    prefix=[0]
    for value in right:prefix.append(prefix[-1]+value)
    out=[0]*length
    def add_run(start,count,digit):
        for t in range(count+len(right)-1):
            lo=max(0,t-count+1)
            hi=min(len(right)-1,t)
            out[start+t]+=digit*(prefix[hi+1]-prefix[lo])
            info['coefficient_updates']+=1
    def add_sparse(start,digit):
        for j,value in enumerate(right):
            out[start+j]+=digit*value
            info['coefficient_updates']+=1
    if method=='baseline-exceptions':
        digit,exceptions=details
        add_run(0,len(left),digit)
        for index,delta in exceptions:add_sparse(index,delta)
    elif method=='sparse-digits':
        for index,digit in details:add_sparse(index,digit)
    else:
        for index,count,digit in details:add_run(index,count,digit)
    assert all(value>=0 for value in out)
    info['prefix_sum_additions']=len(right)
    return out,info
