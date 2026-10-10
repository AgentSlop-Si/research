"""Independent ordinary iterative radix-2 exact NTT (positive exponent)."""
from __future__ import annotations
P=998244353;G=3

def radix2_ntt(xs, p=P, g=G):
    n=len(xs)
    if n<2 or (n&(n-1)) or (p-1)%n:raise ValueError('invalid length')
    w=pow(g,(p-1)//n,p)
    if pow(w,n//2,p)==1:raise ValueError('nonprimitive')
    y=[int(z)%p for z in xs]
    j=0; index_steps=0; swaps=0
    for i in range(1,n):
        bit=n//2
        while j&bit:
            j^=bit;bit>>=1;index_steps+=1
        j^=bit;index_steps+=1
        if i<j:
            y[i],y[j]=y[j],y[i];swaps+=1
    gates={'length':n,'macro_stages':n.bit_length()-1,'additions':0,
           'data_twiddle_mult':0,'twiddle_update_mult':0,
           'permutation_index_steps':index_steps,'permutation_moves':2*swaps,
           'root_power_calls':1,'modular_power_mult_upper':2*((p-1)//n).bit_length()}
    size=2
    while size<=n:
        root=pow(w,n//size,p)
        gates['root_power_calls']+=1
        gates['modular_power_mult_upper']+=2*(n//size).bit_length()
        half=size//2
        for start in range(0,n,size):
            tw=1
            for off in range(half):
                u=y[start+off]
                v=y[start+off+half]*tw%p
                y[start+off]=(u+v)%p
                y[start+off+half]=(u-v)%p
                tw=tw*root%p
                gates['additions']+=2
                gates['data_twiddle_mult']+=1
                gates['twiddle_update_mult']+=1
        size*=2
    return y,gates
