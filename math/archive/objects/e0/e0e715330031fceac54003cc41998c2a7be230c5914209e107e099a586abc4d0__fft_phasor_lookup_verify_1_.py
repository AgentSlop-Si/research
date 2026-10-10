#!/usr/bin/env python3
"""Independent numerical/algebraic checks for packed signed-atom phasor lookup.

The reference decoder constructs tables lazily to avoid immense asymptotic table constants.
Its runtime is NOT the claimed asymptotic word-RAM runtime. See THEOREM.md.
"""
from __future__ import annotations
from bisect import bisect_right
from dataclasses import dataclass
from math import ceil, cos, log, pi, sin, sqrt
from random import Random
import cmath, json, sys

class AliasSampler:
    """Exact integer-weight Vose alias sampler; O(n) build, O(1) random-word calls/sample."""
    def __init__(self, weights):
        self.n=len(weights); self.L=sum(weights)
        if self.L<=0: raise ValueError('zero total mass')
        if any(w<0 or int(w)!=w for w in weights): raise ValueError('weights must be nonnegative integers')
        self.alias=list(range(self.n))
        self.cut=[self.L]*self.n
        scaled=[w*self.n for w in weights]
        small=[i for i,v in enumerate(scaled) if v<self.L]
        large=[i for i,v in enumerate(scaled) if v>=self.L]
        while small and large:
            a=small.pop(); b=large.pop()
            self.cut[a]=scaled[a];self.alias[a]=b
            scaled[b]-=self.L-scaled[a]
            if scaled[b]<self.L:small.append(b)
            else:large.append(b)
        for i in small+large:self.cut[i]=self.L;self.alias[i]=i
    def sample(self,rng):
        i=rng.randrange(self.n)
        return i if rng.randrange(self.L)<self.cut[i] else self.alias[i]

def signed_atoms(x):
    w=[]; desc=[]
    for j,z in enumerate(x):
        a=int(z.real);b=int(z.imag)
        w.extend([abs(a),abs(b)])
        desc.extend([(j, (1+0j) if a>=0 else (-1+0j)), (j, (0+1j) if b>=0 else (0-1j))])
    return w,desc

def nearest_bin(k, n, bins):
    # Integer-only exact rounded bucket index; valid for k in 0..n-1
    return ((2*k*bins+n)//(2*n))%bins

def quant_real(z,h):
    return round(z/h)*h

def quant_complex(z,h):
    return complex(quant_real(z.real,h),quant_real(z.imag,h))

@dataclass
class Config:
    n:int
    B:int=8
    g:int=4
    eps:float=0.8
    delta:float=0.05
    def __post_init__(self):
        # Deliberately overresolve phasors so the theoretical deterministic budget is safe.
        self.P0=ceil(32*pi/self.eps)
        self.P1=ceil(32*pi*self.B/self.eps)
        self.h1=self.eps/(64*sqrt(2))
        self.h2=self.eps/(64*sqrt(2))
        self.coord_count=ceil(2/self.h1)+3
        self.sbits=ceil(log(self.coord_count**2,2))

# Quantized first-level group symbols, encoded as two coordinate indices.
def coord_encode(z,h,coord_count):
    i=round(z.real/h)+coord_count//2
    j=round(z.imag/h)+coord_count//2
    assert 0<=i<coord_count and 0<=j<coord_count
    return i*coord_count+j

def coord_decode(v,h,coord_count):
    return complex((v//coord_count-coord_count//2)*h,(v%coord_count-coord_count//2)*h)

def pack_transpose_key(group_symbols, lane_start, width, sbits):
    """Literal row-major -> lane-major table map, independent of phasor details."""
    G=len(group_symbols);row_key=0
    for u in range(G):
        for t in range(width):
            row_key |= int(group_symbols[u][lane_start+t]) << (sbits*(u*width+t))
    mask=(1<<sbits)-1
    out=0
    for t in range(width):
        for u in range(G):
            digit=(row_key>>(sbits*(u*width+t)))&mask
            out |= digit << (sbits*(t*G+u))
    return row_key,out

def check_eager_transpose_table():
    # Build the COMPLETE low-bit transposition lookup for a small instance,
    # including invalid/unused symbol codes, as required in the asymptotic proof.
    G,L,s=2,3,2
    keys=1<<(G*L*s)
    mask=(1<<s)-1
    tbl=[]
    for key in range(keys):
        out=0
        for t in range(L):
            for u in range(G):
                v=(key>>(s*(u*L+t)))&mask
                out|=v<<(s*(t*G+u))
        tbl.append(out)
    assert len(tbl)==4096
    for key,out in enumerate(tbl):
        for t in range(L):
            for u in range(G):
                assert (out>>(s*(t*G+u)))&mask == (key>>(s*(u*L+t)))&mask
    return len(tbl)

def check_transpose(seed=17):
    rng=Random(seed); count=0
    for G in (1,2,3,4,7,9):
        for B in (1,4,7,8,13):
            for s in (1,2,4,6,9):
                symbols=[[rng.randrange(1<<s) for _ in range(B)] for _ in range(G)]
                for L in range(1,B+1):
                    for start in range(0,B,L):
                        width=min(L,B-start)
                        row,out=pack_transpose_key(symbols,start,width,s)
                        mask=(1<<s)-1
                        for t in range(width):
                            for u in range(G):
                                assert (out>>(s*(t*G+u)))&mask==symbols[u][start+t]
                        count+=1
    return count

def trajectory_descriptor(n,block_start,j,phase,cfg):
    p0=nearest_bin((block_start*j)%n,n,cfg.P0)
    p1=nearest_bin(j,n,cfg.P1)
    return p0,p1,phase

def template_lane(d,t,cfg):
    a,b,sign=d
    theta=-2*pi*(a/cfg.P0+t*b/cfg.P1)
    return sign*complex(cos(theta),sin(theta))

def verify_phase_error(cfg):
    max_observed=0.0
    for j in range(cfg.n):
        for start in range(0,cfg.n,cfg.B):
            d=trajectory_descriptor(cfg.n,start,j,1+0j,cfg)
            for t in range(min(cfg.B,cfg.n-start)):
                z=cmath.exp(-2j*pi*(j*(start+t)%cfg.n)/cfg.n)
                err=abs(z-template_lane(d,t,cfg));max_observed=max(max_observed,err)
                # Angle quantization error <= pi/P0 + t*pi/P1.
                assert err <= pi/cfg.P0+t*pi/cfg.P1+1e-12
    return max_observed

def simulate(x,cfg,seed):
    n=cfg.n;rng=Random(seed)
    weights,atoms=signed_atoms(x)
    if sum(weights)==0:return {'max_error':0.,'bound':0.,'samples':0,'decoder_error':0.}
    alias=AliasSampler(weights)
    # k_min = ceil(4/(eps/2)^2 ln(4N/delta)). Pad by *taking more samples*, not zero atoms.
    kmin=ceil(16/cfg.eps**2 *log(4*n/cfg.delta))
    G=ceil(kmin/cfg.g);k=G*cfg.g
    chosen=[atoms[alias.sample(rng)] for _ in range(k)]
    D=cfg.coord_count;sb=cfg.sbits
    decoded=[];true_sample=[]
    max_decoder_error=0
    for block_start in range(0,n,cfg.B):
        width=min(cfg.B,n-block_start)
        group_symbols=[]
        for u in range(G):
            group=chosen[u*cfg.g:(u+1)*cfg.g]
            desc=[trajectory_descriptor(n,block_start,j,s,cfg) for j,s in group]
            lane_symbols=[]
            for t in range(width):
                z=sum(template_lane(d,t,cfg) for d in desc)/cfg.g
                z1=quant_complex(z,cfg.h1)
                lane_symbols.append(coord_encode(z1,cfg.h1,D))
            group_symbols.append(lane_symbols)
        # Transposition lookup: extract each lane key from the packed transpose word.
        transposed_lane_symbols=[[] for _ in range(width)]
        chunk=2  # small toy chunks; actual asymptotic chunk grows with log N / log log N.
        for start in range(0,width,chunk):
            clen=min(chunk,width-start)
            _,out=pack_transpose_key(group_symbols,start,clen,sb)
            lane_mask=(1<<sb)-1
            for t in range(clen):
                key=(out>>(sb*G*t)) & ((1<<(sb*G))-1)
                assert key==sum(group_symbols[u][start+t]<<(sb*u) for u in range(G))
                vals=[(key>>(sb*u))&lane_mask for u in range(G)]
                transposed_lane_symbols[start+t]=vals
        for t in range(width):
            normalized=sum(coord_decode(v,cfg.h1,D) for v in transposed_lane_symbols[t])/G
            z2=quant_complex(normalized,cfg.h2)
            ztrue=sum(s*cmath.exp(-2j*pi*(j*(block_start+t)%n)/n) for j,s in chosen)/k
            max_decoder_error=max(max_decoder_error,abs(z2-ztrue))
            decoded.append(z2)
            true_sample.append(ztrue)
    L=sum(weights)
    output=[v*L/sqrt(n) for v in decoded]
    exact=[sum(x[j]*cmath.exp(-2j*pi*(j*m%n)/n) for j in range(n))/sqrt(n) for m in range(n)]
    error=max(abs(a-b) for a,b in zip(output,exact))
    phase_bound=pi/cfg.P0+(cfg.B-1)*pi/cfg.P1
    quant_bound=(cfg.h1+cfg.h2)/sqrt(2)
    deterministic_bound=phase_bound+quant_bound
    assert max_decoder_error<=deterministic_bound+1e-10,(max_decoder_error,deterministic_bound)
    return {'n':n,'eps':cfg.eps,'seed':seed,'samples':k,'groups':G,'max_error':error,
            'bound':cfg.eps*L/sqrt(n),'passed':error <=cfg.eps*L/sqrt(n)+1e-9,
            'normalized_decoder_error':max_decoder_error,'deterministic_bound':deterministic_bound}

def test_alias():
    weights=[0,1,2,7,0,8,3,5]
    tab=AliasSampler(weights);rng=Random(701)
    hist=[0]*len(weights)
    trials=100000
    for _ in range(trials):hist[tab.sample(rng)]+=1
    return {'trials':trials,'max_abs_frequency_deviation':max(abs(hist[i]/trials-w/sum(weights)) for i,w in enumerate(weights))}

def main():
    samples=[]
    samples.append(('constant', [1+0j]*64))
    samples.append(('alternating', [1+0j if j%2==0 else -1+0j for j in range(64)]))
    samples.append(('spike', [10+3j if j==17 else 0j for j in range(64)]))
    samples.append(('fourier-tone', [complex(round(4*cos(2*pi*7*j/64)),round(4*sin(2*pi*7*j/64))) for j in range(64)]))
    rng=Random(20261010)
    samples.append(('random-bounded', [complex(rng.randrange(-8,9),rng.randrange(-8,9)) for _ in range(64)]))
    cfg=Config(n=64,B=8,g=4,eps=.8,delta=.05)
    output={'note':'Simulator lazily evaluates tables; not a benchmark of precomputed-table runtime.',
        'alias':test_alias(),'transpose_cases':check_transpose(),
        'eager_transpose_entries_tested':check_eager_transpose_table(),
        'max_phase_error':verify_phase_error(cfg),'phase_bound':pi/cfg.P0+(cfg.B-1)*pi/cfg.P1,
        'cases':[]}
    for name,x in samples:
        for seed in (17,42,101):
            r=simulate(x,cfg,seed);r['signal']=name;output['cases'].append(r)
    # Boundary-length and partial-final-block stress (not performance benchmarks).
    for n in (17,31,63,65,127):
        rng=Random(n*37)
        x=[complex(rng.randrange(-3,4),rng.randrange(-3,4)) for _ in range(n)]
        c=Config(n=n,B=8,g=4,eps=.8,delta=.05)
        assert verify_phase_error(c)<=pi/c.P0+(c.B-1)*pi/c.P1+1e-10
        for seed in (5,9):
            r=simulate(x,c,seed);r['signal']='boundary-random';output['cases'].append(r)
    output['passed_cases']=sum(1 for v in output['cases'] if v['passed'])
    output['total_cases']=len(output['cases'])
    assert output['passed_cases']==output['total_cases']
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
