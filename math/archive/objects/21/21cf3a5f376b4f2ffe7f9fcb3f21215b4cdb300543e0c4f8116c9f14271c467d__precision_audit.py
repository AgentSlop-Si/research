"""Quantized-representative capacity bound and finite exhaustive illustrations.

Grid-collision proofs are combinatorial; floating-point enumeration is
ONLY illustrative.  Do not infer exact complex injectivity from floating-point
proximity.  Rational cyclotomic basis proves exact injectivity separately.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from experiment import complex_orbit_representatives
from orbit_stability import is_power_of_two


def forced_grid_collision(n: int, r: int, frac_bits: int) -> bool:
    """TRUE iff pigeonhole guarantees a collision for any choice of r odd bins.

    Measured unnormalized Re/Im are in [-n/2,n/2]. At grid 2^-b,
    at most (n*2^b + 2) bins along each real coordinate.
    """
    if not is_power_of_two(n) or not 1 <= r <= n//2 or frac_bits < 0:
        raise ValueError("invalid grid arguments")
    values_per_real_coord = n*(1<<frac_bits) + 2
    return values_per_real_coord**(2*r) < 1 << (n//2)


def necessary_fractional_bits(n: int, r: int) -> int:
    """Conservative minimum b so grid-counting obstruction disappears.

    A b below this is impossible for injective quantized measurements.
    A b at/above it is NOT necessarily sufficient.
    """
    b=0
    while forced_grid_collision(n,r,b):
        b+=1
    return b


def actual_grid_collisions(n:int, b:int) -> int:
    """Illustrative double-precision exhaustive quantization for r=1."""
    alpha=complex_orbit_representatives(n)
    z=np.stack([np.floor(alpha.real*(1<<b)).astype('int64'),
                np.floor(alpha.imag*(1<<b)).astype('int64')],axis=1)
    return len(z)-np.unique(z,axis=0).shape[0]


def run_precision_audit()->dict:
    lower_bounds=[{"N":n,"r":r,"necessary_fractional_bits":necessary_fractional_bits(n,r)}
                  for n in (8,16,32,64,128,256,1024,4096)
                  for r in (1,2,4) if r <= n//2]
    examples=[{"N":n,"b":b,"numeric_grid_collision_excess":actual_grid_collisions(n,b)}
              for n in (8,16,32) for b in (0,1,2,3,4,6,8,10,12)]
    return {"capacity_lower_bounds":lower_bounds,"sample_exact_family_double_quantization":examples}


if __name__=="__main__":
    result=run_precision_audit()
    out=Path(__file__).resolve().parent/"precision_results.json"
    out.write_text(json.dumps(result,indent=2)+"\n")
    for n in (8,16,32,64,128,256,1024,4096):
        print('N=',n,'r=1 minimum fractional bits=',necessary_fractional_bits(n,1))
    print('N=32, r=1 numeric grid collision excess:',[(v['b'],v['numeric_grid_collision_excess']) for v in result['sample_exact_family_double_quantization'] if v['N']==32])
