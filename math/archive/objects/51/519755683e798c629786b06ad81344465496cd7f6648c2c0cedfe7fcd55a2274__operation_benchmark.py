"""Charged arithmetic proxy; not a wall-clock FFT speed claim.

Both branches share exactly the same precomputed root/Green data, so their
setup is common. Phase18 charges candidate discovery and rejected candidates.
"""
from __future__ import annotations
import json,random
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects,far_coprime_shift
from rational_forcing import bluestein_transform,PolyStats

P=2013265921;GEN=31

def baseline(e,x):
    r=e.P.apply(x)
    stat=PolyStats()
    forcing,stat=bluestein_transform(r,e.n,e.omega,e.p,e.primitive_gen,stat)
    y=e.L.solve(forcing)
    charge=stat.total_field_ops()+8*e.n+1 # preconditioner (3N), Green solve (5N+1)
    return y,charge,stat


def build_samples(e):
    n,p=e.n,e.p
    shift=far_coprime_shift(n)
    r1=[pow(2,j,p) for j in range(n)]
    r2=[0]*n
    for t in range(n):r2[(t*shift)%n]=(pow(2,t,p)+pow(3,t,p))%p
    h=[0]*n
    for j,v in ((0,1),(n//3,2),(2*n//3,3)):h[j]=v
    r3=dense_from_shift_defects(h,shift,2,p)
    h8=[0]*n
    for t in range(8):h8[(t*(n//8+1))%n]=t+1
    # Any repeated indices are combined to preserve correct K count.
    r8=dense_from_shift_defects(h8,shift,2,p)
    rnd=random.Random(103+e.n)
    return [(name,e.P.solve(r)) for name,r in [('geometric',r1),('two_modes_long',r2),
            ('three_defects_long',r3),('eight_defects_long',r8)]]+[
             ('random_generic',[rnd.randrange(1,p) for _ in range(n)])]


def main():
    records=[]
    for n in [128,256,384,1024,4096]:
        e=RecurrenceGreen(n,P,GEN)
        for kind,x in build_samples(e):
            new,meta=e.transform_recurrence(x,max_degree=3)
            full,charge,st=baseline(e,x)
            if new!=full:raise AssertionError(('baseline discrepancy',n,kind))
            wc=meta['work'].arithmetic()
            rec={'N':n,'kind':kind,'selected':meta['selected'],
                 'K':meta['K'],'degree_on_graph':meta.get('degree_on_graph'),
                 'delay':meta.get('delay'),'resonant':meta['resonant'],
                 'phase18_field_arithmetic_proxy':wc,
                 'full_bluestein_field_arithmetic_proxy':charge,
                 'ratio':round(wc/charge,6),
                 'candidate_scans':meta['work'].candidates,
                 'field_inversions_in_phase18':meta['work'].inversions,
                 'short_NTT_calls':meta['work'].sparse.ntt_calls,
                 'max_short_NTT':meta['work'].sparse.max_ntt_length}
            records.append(rec)
            print(n,kind,rec['selected'],rec['K'],wc,charge,rec['ratio'],flush=True)
    data={'records':records,
          'methodology':'Full Bluestein vs recurrence compression in same field and shared precomputed Green/root engine. Exact per-call field operations for PolyStats and explicit arithmetic charges for discovery, polynomial, division, Green. Does not include Python indexing/hashing/branch costs, machine bit complexity, root/Green setup (common), or float precision; not wall time.',
          'p':P,'primitive_generator':GEN}
    with open('BENCHMARK.json','w') as f:json.dump(data,f,indent=2)
    return data
if __name__=='__main__':main()
