"""Blind inverse recovery versus same-field Bluestein with charged probes."""
import random,json
from blind_inverse import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from benchmark_phase19 import full_reference

P=2013265921;G=31

def main():
    data=[]
    for n in (128,384,1024,4096):
        e=RecurrenceGreen(n,P,G)
        d=[far_coprime_shift(n),n-1,1]
        factors=list(zip(d,[2,3,5]))
        h=[0]*n;h[n//3]=13
        for m in (1,2,3):
            r=h[:]
            for delta,alpha in factors[:m]:r=dense_from_shift_defects(r,delta,alpha,P)
            x=e.P.solve(r)
            taps=2**m
            got,meta=e.transform_blind_inverse(x,taps)
            baseline,charge=full_reference(e,x)
            assert got==baseline
            assert meta['selected']=='blind-sparse-circular-inverse',meta
            new=meta['work'].arithmetic()
            inv_meta=meta['inverse_certificate']
            rec={'N':n,'factors_completely_unknown':m,'max_taps':taps,
                 'inverse_taps_found':meta['inverse_support'],
                 'blind_recovery':meta['selected'],
                 'field_ops_new':new,'field_ops_bluestein':charge,
                 'ratio':round(new/charge,6),
                 'direct_fourier_samples':inv_meta.sample_count,
                 'verified_convolution_entries':inv_meta.certificate_entries_checked,
                 'prony_roots_tested':inv_meta.root_candidates}
            data.append(rec)
            print(n,m,'taps',meta['inverse_support'],new,charge,round(new/charge,3),flush=True)
        rand=random.Random(23+n)
        x=[rand.randrange(1,P) for _ in range(n)]
        got,meta=e.transform_blind_inverse(x,4)
        baseline,charge=full_reference(e,x)
        assert got==baseline and meta['selected']=='fallback'
        new=meta['work'].arithmetic()
        data.append({'N':n,'factors_completely_unknown':None,'max_taps':4,
                     'blind_recovery':'fallback','inverse_taps_found':None,
                     'field_ops_new':new,'field_ops_bluestein':charge,
                     'ratio':round(new/charge,6),
                     'direct_fourier_samples':meta['inverse_certificate'].sample_count,
                     'prony_roots_tested':meta['inverse_certificate'].root_candidates})
        print(n,'generic',new,charge,round(new/charge,3),flush=True)
    o={'records':data,'scope':'Exact modular field arithmetic per call, same shared initialization. Counts all Fourier probes, recurrence arithmetic, subgroup root scan, interpolation, full residual certificate, spectrum evaluation, batch inversions, P preconditioner and L Green solve. Does not claim bit complexity, wall-clock speed, or generic worst-case sub-FFT.'}
    with open('BENCHMARK_INVERSE.json','w') as f:json.dump(o,f,indent=2)
    return o
if __name__=='__main__':main()
