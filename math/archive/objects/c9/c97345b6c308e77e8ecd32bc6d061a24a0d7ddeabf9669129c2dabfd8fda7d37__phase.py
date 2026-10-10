"""Reuse-friendly Fourier phase construction for a selected input position.

Build e^(-2*pi*i*position*q/N) for q=0..N//2 using a compact tiled
pattern, with a single small local power table and one base phase per tile.
Does not change O(N) asymptotic work. Avoids a separate trig evaluation
for every frequency and controls recurrence error with block restarts.
"""
from __future__ import annotations
import cmath
import math
import numpy as np


def phases_tiled(n:int, position:int, tile:int=1024, count:int|None=None) -> np.ndarray:
    if n<=0 or not(0<=position<n) or tile<=0:
        raise ValueError('invalid argument')
    if count is None:
        count=n//2+1
    if count<0 or count>n:
        raise ValueError('invalid output count')
    if count==0: return np.empty(0,dtype=np.complex128)
    tile=min(int(tile),int(count))
    local=np.empty(tile, dtype=np.complex128)
    local[0]=1+0j
    size=1
    power=cmath.exp((-2j*math.pi*position)/n)
    while size<tile:
        to_write=min(size,tile-size)
        local[size:size+to_write] = local[:to_write] * power
        # The power for the next doubled stride:
        power *= power
        size += to_write
    blocks=(count+tile-1)//tile
    offsets=(np.arange(blocks, dtype=np.int64) * tile * position) % n
    roots=np.exp((-2j*np.pi/n)*offsets)
    packed=np.empty((blocks,tile),dtype=np.complex128)
    np.multiply(roots[:,None],local[None,:],out=packed)
    return packed.ravel()[:count]
