"""Experimental all-level quantized FFT table batching.

NOT an exact FFT and NOT OpenAI #130. Produces an approximation to fft(x)/N
for complex |x[j]|<=1 using a finite grid, one reusable K-point normalized
DFT table, and FFT-stage-group input phase factors. Full tables are very large
at useful accuracy: `lazy` mode is a correctness emulator, NOT a faster
algorithm or evidence of an asymptotic speedup.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np


def reverse_bits(k: int, bits: int) -> int:
    out=0
    for _ in range(bits):
        out=(out<<1)|(k&1)
        k>>=1
    return out


def is_pow2(n:int)->bool:
    return n>0 and (n & (n-1))==0


@dataclass
class TableStats:
    hits:int=0
    misses:int=0
    processed:int=0
    group_count:int=0

class QuantizedDFTTable:
    """Input/output quantized to component grid -1,-1+1/R,...,1.

    q=(2R+1)^2 possible complex entries; there are q^K possible blocks.
    `full` precomputes them ALL; `lazy` computes misses (no asymptotic speed
    promise because high-entropy inputs can cause many misses).
    """
    def __init__(self, K:int, R:int, mode:str="full", max_entries:int=150_000):
        if not is_pow2(K) or R<1:
            raise ValueError("K must be a power of two and R positive")
        if mode not in ("full","lazy","direct"):
            raise ValueError("invalid table mode")
        self.K=K;self.R=R;self.mode=mode;self.base=2*R+1
        self.possible=self.base**(2*K)
        self.stats=TableStats()
        self.cache={}
        self.complete=None
        if mode=="full":
            if self.possible>max_entries:
                raise MemoryError(f"full table would have {self.possible:,} entries; max {max_entries:,}")
            ids=np.arange(self.possible,dtype=np.int64)
            values=np.empty((self.possible,K),dtype=np.complex128)
            tmp=ids.copy()
            for j in range(K):
                real=(tmp%self.base).astype(np.float64)-R;tmp//=self.base
                imag=(tmp%self.base).astype(np.float64)-R;tmp//=self.base
                values[:,j]=(real+1j*imag)/R
            # The table outputs are quantized too; its representation is uniform
            # at every group level.
            z=np.fft.fft(values,axis=1)/K
            self.complete=self.quantize(z)

    def quantize(self,x):
        # Clip because the true normalized intermediate is within unit disk;
        # clipping is 1-Lipschitz relative to any true component in [-1,1].
        x=np.asarray(x)
        re=np.clip(np.rint(x.real*self.R),-self.R,self.R)/self.R
        im=np.clip(np.rint(x.imag*self.R),-self.R,self.R)/self.R
        return re + 1j*im

    def index(self,values):
        if len(values)!=self.K:raise ValueError("wrong block length")
        k=0;power=1
        for v in values:
            re=int(round(v.real*self.R))+self.R
            im=int(round(v.imag*self.R))+self.R
            if not (0<=re<self.base and 0<=im<self.base):
                raise ValueError("input outside quantization bounds")
            k+=(re+self.base*im)*power
            power*=self.base*self.base
        return k

    def apply(self,vec):
        if self.mode=="direct":
            self.stats.processed+=1
            return self.quantize(np.fft.fft(vec)/self.K)
        key=self.index(vec)
        self.stats.processed+=1
        if self.complete is not None:
            self.stats.hits+=1
            return self.complete[key]
        item=self.cache.get(key)
        if item is not None:
            self.stats.hits+=1
            return item
        self.stats.misses+=1
        item=self.quantize(np.fft.fft(vec)/self.K)
        self.cache[key]=item
        return item


def normalized_fft_quantized(x, block_stages:int, R:int, *, table_mode:str="lazy", max_entries:int=150_000):
    """Block-stage FFT with rounding. Returns (quantized fft(x)/N, statistics).

    If L=log2 N is divisible by block_stages, one *same* complete table is
    reused at every group level. For a final shorter group, make a second
    table of smaller width. In `lazy` mode tables grow only on misses, so
    complexity can be worse than ideal full-table lookup.
    """
    x=np.asarray(x,dtype=np.complex128)
    N=len(x)
    if not is_pow2(N):raise ValueError("power-of-two N required")
    if block_stages<1:raise ValueError("block_stages must be positive")
    if np.any(abs(x)>1+1e-12):raise ValueError("requires |input|<=1")
    if N==1:return np.asarray([complex(x[0])]),TableStats(),{}
    L=N.bit_length()-1
    bitrev=np.fromiter((reverse_bits(i,L) for i in range(N)),dtype=np.int64,count=N)
    table_by_k={}
    for stages in range(1,min(block_stages,L)+1):
        if stages==block_stages or L%block_stages==stages:
            k=1<<stages
            table_by_k[k]=QuantizedDFTTable(k,R,table_mode,max_entries)
    a=table_by_k[next(iter(table_by_k))].quantize(x[bitrev])
    stats=TableStats()
    s=0
    while s<L:
        t=min(block_stages,L-s)
        K=1<<t;M=1<<(s+t);J=1<<s
        table=table_by_k[K]
        nxt=np.empty(N,dtype=np.complex128)
        for base in range(0,N,M):
            for j in range(J):
                z=np.empty(K,dtype=np.complex128)
                for r in range(K):
                    b=reverse_bits(r,t)
                    twiddle=np.exp(-2j*np.pi*(j*b)/M)
                    z[b]=a[base+j+J*r]*twiddle
                z=table.quantize(z)
                out=table.apply(z)
                for k in range(K):
                    nxt[base+j+J*k]=out[k]
        a=nxt;s+=t;stats.group_count+=1
    for tb in table_by_k.values():
        stats.processed+=tb.stats.processed
        stats.hits+=tb.stats.hits
        stats.misses+=tb.stats.misses
    return a,stats,table_by_k


def normal_dit_stages(x, start_s:int, num_stages:int, modular=False):
    """Raw numerical reference to verify only a group of butterfly layers.
    This expects its input already in the proper iterative DIT ordering.
    """
    a=np.asarray(x,dtype=np.complex128).copy()
    N=len(a)
    if not is_pow2(N):raise ValueError("N must be power of two")
    for st in range(start_s+1,start_s+num_stages+1):
        m=1<<st;h=m//2
        phase=np.exp(-2j*np.pi*np.arange(h)/m)
        for base in range(0,N,m):
            u=a[base:base+h].copy()
            v=a[base+h:base+m].copy()*phase
            a[base:base+h]=(u+v)/2
            a[base+h:base+m]=(u-v)/2
    return a


def direct_group_matrix(x,start_s:int,num_stages:int):
    """Equivalent to a table call, but evaluates the K-point FFT directly.
    No quantization. Tests the input-modulation factorization independently.
    """
    a=np.asarray(x,dtype=np.complex128)
    N=len(a);K=1<<num_stages;M=1<<(start_s+num_stages);J=1<<start_s
    nxt=np.empty(N,dtype=np.complex128)
    for base in range(0,N,M):
        for j in range(J):
            seq=np.empty(K,dtype=np.complex128)
            for r in range(K):
                b=reverse_bits(r,num_stages)
                seq[b]=a[base+j+J*r]*np.exp(-2j*np.pi*j*b/M)
            y=np.fft.fft(seq)/K
            for k in range(K):nxt[base+j+J*k]=y[k]
    return nxt
