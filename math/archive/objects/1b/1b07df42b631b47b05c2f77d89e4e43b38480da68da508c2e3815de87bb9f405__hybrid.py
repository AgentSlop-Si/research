"""Paid discovery with a conventional O(N log k) fallback.

Selection minimizes the displayed unit-field-operation ledger, not native
runtime. All candidate discovery is paid even when the FFT route is chosen.
"""
from dataclasses import dataclass
from collections import Counter
from adaptive_recurrence import prepare_adaptive,apply_adaptive,expected_online
from fft_decoded_baseline import (prepare_baseline,apply_baseline,
    expected_preparation as baseline_preparation,expected_online as baseline_online)


@dataclass
class HybridPlan:
    adaptive: object
    baseline: object
    method: str
    preparation: dict
    adaptive_online_total: int
    baseline_additional_total: int


def prepare_hybrid(field,n,roots,eta,strides=None):
    adaptive=prepare_adaptive(field,n,roots,strides)
    k=len(roots)
    recurrence_cost=sum(expected_online(n,k,adaptive.initial_length,len(adaptive.taps)).values())
    fft_cost=sum(baseline_preparation(k).values())+sum(baseline_online(n,k).values())
    counts=Counter(adaptive.preparation)
    baseline=None
    if recurrence_cost<=fft_cost:
        method='sparse_annihilator'
    else:
        method='decoded_fft'
        baseline=prepare_baseline(field,n,roots,eta)
        counts.update(baseline.preparation)
    return HybridPlan(adaptive,baseline,method,dict(counts),recurrence_cost,fft_cost)


def apply_hybrid(field,plan,amplitudes):
    if plan.method=='sparse_annihilator':
        out,counts=apply_adaptive(field,plan.adaptive,amplitudes)
    else:
        out,counts=apply_baseline(field,plan.baseline,amplitudes)
    return out,dict(method=plan.method,**counts)
