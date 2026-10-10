"""Prime-free exact convolution over Z/(2**t+1), for unbounded finite lengths.

This intentionally trades a large modulus for an elementary exact construction.
It is not a faster general integer multiplier. See README for its bit costs.
"""
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Ring:
    n:int
    base:int
    m:int
    t:int
    modulus:int
    mask:int
    root_shift:int
    log_m:int
    permutation:tuple


def make_ring(n,base,counts):
    if not isinstance(n,int) or isinstance(n,bool) or n<1:
        raise ValueError('positive integer length required')
    if not isinstance(base,int) or isinstance(base,bool) or base<2:
        raise ValueError('integer base at least two required')
    m=1<<(2*n-1).bit_length()
    half=m//2
    coefficient_bound=n*(base-1)**2
    needed=max(1,coefficient_bound.bit_length())
    t=half*((needed+half-1)//half)
    power=1<<t
    permutation=[0]*m
    for i in range(1,m):
        permutation[i]=(permutation[i>>1]>>1)|((i&1)*(m>>1))
    counts['modulus_constructed_bits']+=t+1
    counts['permutation_entries_written']+=m
    counts['permutation_index_steps']+=m-1
    counts['bound_integer_products']+=2
    return Ring(n,base,m,t,power+1,power-1,2*t//m,m.bit_length()-1,tuple(permutation))


def rotate(value,shift,ring,counts):
    """value * 2**shift mod (2**t+1), canonical, without a dense root table."""
    counts['ring_twiddle_calls']+=1
    counts['mod_mul']+=1
    shift%=2*ring.t
    negative=shift>=ring.t
    if negative:shift-=ring.t
    if shift:
        value=((value<<shift)&ring.mask)-(value>>(ring.t-shift))
        if value<0:value+=ring.modulus
        counts['binary_fold_rotations']+=1
    if negative and value:
        value=ring.modulus-value
        counts['ring_sign_changes']+=1
    return value


def multiply(a,b,ring,counts,schoolbook=False):
    """One charged large-ring product plus linear-bit-cost negacyclic folding.

Default uses Python's exact integer multiplication as a t-bit subroutine M(t),
not as a free operation. Optional shift/add schoolbook makes a quadratic bit
upper bound independent of the host multiplication algorithm explicit.
"""
    if schoolbook:
        product=0;left=a;right=b
        while right:
            counts['schoolbook_bit_tests']+=1
            if right&1:
                product+=left;counts['schoolbook_additions']+=1
            left<<=1;right>>=1
            counts['schoolbook_shifts']+=2
    else:
        product=a*b
    counts['ring_pointwise_products']+=1
    counts['mod_mul']+=1
    counts['pointwise_operand_bits_sum']+=a.bit_length()+b.bit_length()
    counts['pointwise_schoolbook_bit_budget']+=(ring.t+1)**2
    result=(product&ring.mask)-(product>>ring.t)
    if result<0:result+=ring.modulus
    counts['ring_product_folds']+=1
    return result


def ntt(values,ring,counts,inverse=False):
    if len(values)!=ring.m:raise ValueError('wrong transform length')
    out=[values[j] for j in ring.permutation]
    counts['ntt_permutation_reads']+=ring.m
    counts['ntt_permutation_writes']+=ring.m
    width=2
    while width<=ring.m:
        half=width//2;step=2*ring.t//width
        for start in range(0,ring.m,width):
            for j in range(half):
                u=out[start+j]
                v=rotate(out[start+j+half],(-j if inverse else j)*step,ring,counts)
                total=u+v
                if total>=ring.modulus:total-=ring.modulus
                difference=u-v
                if difference<0:difference+=ring.modulus
                out[start+j]=total;out[start+j+half]=difference
                counts['ring_additions']+=1;counts['ring_subtractions']+=1
                counts['mod_add']+=1;counts['mod_sub']+=1
                counts['butterflies']+=1
                counts['butterfly_value_reads']+=2;counts['butterfly_value_writes']+=2
        width*=2
    if inverse:
        out=[rotate(value,-ring.log_m,ring,counts) for value in out]
        counts['inverse_scale_values']+=ring.m
    counts['inverse_ntts' if inverse else 'forward_ntts']+=1
    return out


def validate_digits(values,base,counts,n=None):
    if n is not None and len(values)!=n:raise ValueError('length mismatch')
    for value in values:
        counts['input_digit_reads']+=1
        if not isinstance(value,int) or isinstance(value,bool) or not 0<=value<base:
            raise ValueError('canonical integer digits required')


@dataclass(frozen=True)
class Context:
    ring:Ring
    b:tuple
    transformed_b:tuple

    @property
    def n(self):return self.ring.n
    @property
    def base(self):return self.ring.base
    @property
    def m(self):return self.ring.m


def prepare(b,base,counts):
    ring=make_ring(len(b),base,counts)
    validate_digits(b,base,counts)
    padded=list(b)+[0]*(ring.m-ring.n)
    counts['padding_value_writes']+=ring.m
    transformed=ntt(padded,ring,counts)
    counts['stored_B_digits']+=ring.n
    return Context(ring,tuple(b),tuple(transformed))


def fresh(a,ctx,counts,schoolbook=False):
    ring=ctx.ring
    validate_digits(a,ring.base,counts,ring.n)
    padded=list(a)+[0]*(ring.m-ring.n)
    counts['padding_value_writes']+=ring.m
    transformed=ntt(padded,ring,counts)
    product=[multiply(x,y,ring,counts,schoolbook)
             for x,y in zip(transformed,ctx.transformed_b)]
    counts['pointwise_input_reads']+=2*ring.m
    counts['pointwise_output_writes']+=ring.m
    coefficients=ntt(product,ring,counts,inverse=True)[:2*ring.n-1]
    counts['coefficient_copy_entries']+=len(coefficients)
    counts['fresh_products']+=1
    return coefficients


def normalize(coefficients,n,base,counts):
    carry=0;digits=[]
    for j in range(2*n):
        value=carry+(coefficients[j] if j<len(coefficients) else 0)
        carry,digit=divmod(value,base)
        counts['carry_additions']+=1;counts['carry_divmods']+=1
        counts['carry_operand_bit_volume']+=abs(value).bit_length()+base.bit_length()
        counts['full_output_digit_writes']+=1
        digits.append(digit)
    if carry:raise ArithmeticError('product outside the declared output range')
    return digits


def as_integer(digits,base):
    """Independent verifier helper. Never called in the multiplication path."""
    result=0
    for digit in reversed(digits):result=result*base+digit
    return result
