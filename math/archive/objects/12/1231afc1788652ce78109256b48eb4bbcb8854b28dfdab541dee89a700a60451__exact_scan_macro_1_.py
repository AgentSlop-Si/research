"""Self-contained exact finite-field scan macro experiments.

Valid only when n is a power of 4, and n divides modulus-1; no cached input.
A bidirectional-sum scan expresses the 4-point DFT as one constant-width
macro-stage. This is radix-4 FFT in a different representation, NOT novel.
"""
from __future__ import annotations
from dataclasses import dataclass

P = 998244353
G = 3
ORDER4 = (0, 2, 1, 3)


def root_n(n: int, p=P, g=G) -> int:
    if n < 2 or (n & (n - 1)) or (p - 1) % n:
        raise ValueError('power-of-two length and root-compatible prime required')
    w = pow(g, (p-1)//n, p)
    if pow(w, n//2, p) == 1:
        raise ValueError('root must be primitive')
    return w


def direct_dft(x, p=P, g=G):
    n=len(x)
    w=root_n(n,p,g)
    return [sum(x[j] * pow(w,(k*j)%n,p) for j in range(n))%p for k in range(n)]


def rank_mod(a, p=P):
    if not a: return 0
    r=0; z=[[t%p for t in row] for row in a]
    nr=len(z);nc=len(z[0])
    for j in range(nc):
        i=next((q for q in range(r,nr) if z[q][j]),None)
        if i is None: continue
        z[r],z[i]=z[i],z[r]
        v=pow(z[r][j],-1,p)
        z[r]=[v*t%p for t in z[r]]
        for h in range(r+1,nr):
            f=z[h][j]
            if f: z[h]=[(a-f*b)%p for a,b in zip(z[h],z[r])]
        r+=1
        if r==nr: break
    return r


def dft_matrix(n, p=P, g=G):
    w=root_n(n,p,g)
    return [[pow(w,k*j%n,p) for j in range(n)] for k in range(n)]


def ranks_at_all_cuts(matrix, row_order, col_order, p=P):
    n=len(matrix);out=[]
    for s in range(1,n):
        up=rank_mod([[matrix[i][j] for j in col_order[s:]] for i in row_order[:s]],p)
        down=rank_mod([[matrix[i][j] for j in col_order[:s]] for i in row_order[s:]],p)
        out.append((up,down))
    return out


@dataclass(frozen=True)
class Scan4Plan:
    p: int
    input_order: tuple[int, ...]
    lower_p: tuple[int, ...]
    lower_q: tuple[int, ...]
    upper_u: tuple[int, ...]
    upper_v: tuple[int, ...]
    diagonal: tuple[int, ...]

    def evaluate(self, data):
        if len(data)!=4: raise ValueError('four values required')
        p=self.p
        x=[data[i]%p for i in self.input_order]
        low=[0]*4; pref=0
        for i in range(4):
            low[i]=(self.lower_p[i]*pref)%p
            pref=(pref+self.lower_q[i]*x[i])%p
        high=[0]*4; suffix=0
        for i in range(3,-1,-1):
            high[i]=(self.upper_u[i]*suffix)%p
            suffix=(suffix+self.upper_v[i]*x[i])%p
        reordered=[(self.diagonal[i]*x[i]+low[i]+high[i])%p for i in range(4)]
        out=[0]*4
        for i,j in enumerate(self.input_order): out[j]=reordered[i]
        return out


def make_scan4_plan(p=P, g=G) -> Scan4Plan:
    w=root_n(4,p,g)
    a=[[pow(w,(i*j)%4,p) for j in ORDER4] for i in ORDER4]
    # Strictly-lower part has rank-one completion in this 4-point ordering.
    lp=[0]+[a[i][0] for i in range(1,4)]
    lq=[1]+[a[3][j]*pow(lp[3],-1,p)%p for j in range(1,4)]
    # Strictly-upper part has another rank-one completion.
    uu=[a[i][3] for i in range(3)]+[0]
    uv=[0]+[a[0][j]*pow(uu[0],-1,p)%p for j in range(1,4)]
    assert all(a[i][j] == lp[i]*lq[j]%p for i in range(4) for j in range(i))
    assert all(a[i][j] == uu[i]*uv[j]%p for i in range(4) for j in range(i+1,4))
    d=[a[i][i] for i in range(4)]
    return Scan4Plan(p,ORDER4,tuple(lp),tuple(lq),tuple(uu),tuple(uv),tuple(d))


def reverse_base4(i:int,digits:int)->int:
    result=0
    for _ in range(digits):
        result=(result<<2)|(i&3)
        i>>=2
    return result


def fft_via_scan4(values, p=P, g=G):
    """Convenience alias for power-of-four-only radix-4 scan realization."""
    n=len(values);m=n
    while m>1 and m%4==0: m//=4
    if n<4 or m!=1: raise ValueError('power of four required')
    result,counts=fft_via_mixed_scan_macros(values,p,g)
    return result,{**counts, 'macro_levels':counts['macro_stages']}


def fft_via_mixed_scan_macros(values, p=P, g=G):
    """All power-of-two N: first radix 2 (when needed), then radix 4.

    This emits all N exact outputs of a FRESH vector. It is a known
    mixed-radix FFT with its 4-point codelets expressed as bidirectional
    prefix/suffix scans. All layout movements and twiddles are charged.
    """
    n=len(values)
    if n<2 or n&(n-1) or (p-1)%n:
        raise ValueError('power-of-two n>=2, with supported root required')
    L=n.bit_length()-1
    radices=([2] if L%2 else [])+[4]*(L//2)
    w=root_n(n,p,g)
    # O(N) prefix-expansion generator (avoid O(N log N) per-index digit reversal).
    pairs=[(0,0)];stride=1;perm_steps=0
    for radix in radices:
        pairs=[(i+digit*stride, j*radix+digit)
               for i,j in pairs for digit in range(radix)]
        perm_steps+=len(pairs)
        stride*=radix
    permutation=[0]*n
    for i,j in pairs: permutation[i]=j
    data=[int(values[permutation[i]])%p for i in range(n)]
    stats={'length':n, 'radix_stages':tuple(radices),
           'macro_stages':len(radices),'bidirectional_passes_per_element':0,
           'scan4_calls':0,'radix2_calls':0,
           'scan_additions_upper':0,'scan_multiplications_upper':0,
           'twiddle_multiplications_upper':0,
           'twiddle_preparation_multiplications_upper':0,
           'permutation_moves':n, 'permutation_index_steps':perm_steps,
           'root_power_calls':22, 'modular_power_mult_upper':
                 2*((p-1)//n).bit_length()+2*(n//2).bit_length()+
                 2*((p-1)//4).bit_length()+2*(2).bit_length()+
                 4*(p-2).bit_length()+64}
    plan=make_scan4_plan(p,g)
    span=1
    for r in radices:
        span*=r;stride=span//r
        stage_root=pow(w,n//span,p)
        stats['root_power_calls']+=1
        stats['modular_power_mult_upper']+=2*(n//span).bit_length()
        stats['bidirectional_passes_per_element']+=2
        for start in range(0,n,span):
            tw=1
            for j in range(stride):
                current=[data[start+j+stride*t] for t in range(r)]
                twist=[current[0]]
                power=1
                for t in range(1,r):
                    power=power*tw%p
                    twist.append(current[t]*power%p)
                    stats['twiddle_multiplications_upper']+=2
                if r==4:
                    result=plan.evaluate(twist)
                    stats['scan4_calls']+=1
                    stats['scan_additions_upper']+=16
                    stats['scan_multiplications_upper']+=20
                    stats['permutation_moves']+=16
                else:
                    result=[(twist[0]+twist[1])%p,(twist[0]-twist[1])%p]
                    stats['radix2_calls']+=1
                    stats['scan_additions_upper']+=2
                    stats['permutation_moves']+=4
                for t in range(r): data[start+j+stride*t]=result[t]
                tw=tw*stage_root%p
                stats['twiddle_preparation_multiplications_upper']+=1
    return data,stats
