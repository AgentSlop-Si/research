#!/usr/bin/env python3
"""Numerical determinant sanity-check for a CLASSICAL scoped lower bound.

If a circuit explicitly computes M independent UNNORMALIZED F_K outputs,
and every linear combination uses multipliers |alpha|,|beta| <=1, then the
Morgenstern volume argument gives >= Q/2 * log2(K) binary combination gates.
No claim for normalized F_K with free scale, unrestricted coefficients, or
circuits that avoid these intermediate outputs.
"""
import json,math,pathlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent

def one(m,k):
    ix=np.arange(k)
    f=np.exp(-2j*np.pi*np.outer(ix,ix)/k)
    sign,lnabs=np.linalg.slogdet(f)
    theoretical=m*k*math.log2(k)/2
    observed=m*lnabs/math.log(2)
    assert abs(theoretical-observed)<1e-6*max(1,theoretical)
    return {'M':m,'K':k,'Q':m*k,'log2_abs_det_direct_sum':observed,
            'predicted_log2_abs_det':theoretical,
            'lower_bound_linear_gates_c1':theoretical,
            'scope':'Unnormalized intermediate direct-sum F_K, coefficient magnitude <=1'}

def main():
    rec=[one(m,k) for m,k in [(3,5),(5,11),(7,11),(11,13),(11,47),(11,97),(11,187)]]
    (ROOT/'bounded_coefficient_gate.json').write_text(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
