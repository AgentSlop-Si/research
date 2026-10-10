"""Separate numerical, threshold, underflow and complete-basis verification."""
import json
from pathlib import Path
import numpy as np
from benchmark import build,load,error_ratio


def main():
    build();transform,_=load();rng=np.random.default_rng(845)
    basis_count=0;vector_count=0;maximum_exact_error=0.
    for n in (1,2,4,8,16,32,64):
        for j in range(n):
            x=np.zeros(n,dtype=complex);x[j]=1
            expected=np.fft.fft(x,norm='ortho')
            for alg,eps in ((0,0),(1,0),(2,0),(2,.125),(2,.25),(2,.5)):
                out,stats=transform(x,alg,eps,instrument=True)
                bare,_=transform(x,alg,eps,instrument=False)
                assert np.array_equal(out,bare)
                err=error_ratio(out,expected,x)
                assert err<=eps+2e-14,(n,j,alg,eps,err)
                assert stats['computed_outputs']+stats['pruned_outputs']==n
                assert stats['full_output_writes']==n
                if eps==0:maximum_exact_error=max(maximum_exact_error,err)
                vector_count+=1
            basis_count+=1
    # All sixty-four coefficients lie on or just either side of eps=.125.
    # This is numerical evidence only; threshold decisions are not interval certified.
    boundary=[]
    n=1024
    for perturbation in (-1e-12,0.,1e-12):
        spectrum=np.zeros(n,dtype=complex)
        spectrum[:64]=np.exp(1j*rng.uniform(-np.pi,np.pi,64))
        spectrum[0]*=1+perturbation
        x=np.fft.ifft(spectrum,norm='ortho')
        out,stats=transform(x,2,.125,instrument=True)
        err=error_ratio(out,spectrum,x)
        assert err<=.125+3e-14
        boundary.append({'perturbation':perturbation,'error_ratio':err,
                         'computed_outputs':stats['computed_outputs']})
    x=np.zeros(8,dtype=complex);x[0]=x[4]=1.;x[1]=1e-200;x[5]=-1e-200
    out,stats=transform(x,2,0.,instrument=True)
    reference=np.fft.fft(x,norm='ortho')
    assert np.all(out[1::2]!=0)
    assert np.max(np.abs((out[1::2]-reference[1::2])/1e-200))<1e-14
    # Exact constants and sign-alternating constants expose representable zero subtrees.
    for n in (16,1024,65536):
        for sign in (1,-1):
            x=np.ones(n,dtype=complex)
            if sign==-1:x[1::2]=-1
            out,stats=transform(x,2,0.,instrument=True)
            assert np.array_equal(out,np.fft.fft(x,norm='ortho'))
            assert stats['computed_outputs']==1
            assert stats['butterflies']==n-1
    # Scaling must not erase a representable result for minimum subnormals.
    n=1024;x=np.full(n,np.nextafter(0.,1.)+0j,dtype=complex)
    for algorithm in (0,1,2):
        out,_=transform(x,algorithm,0.)
        assert out[0].real==np.nextafter(0.,1.)*32
        assert np.count_nonzero(out)==1
    report={'status':'PASS','basis_vectors':basis_count,'basis_method_comparisons':vector_count,
            'maximum_zero_tolerance_error_ratio':maximum_exact_error,
            'near_threshold_controls':boundary,
            'underflow_prone_nonzero_odd_outputs_preserved':4,
            'exact_representable_single_tone_controls':6,
            'subnormal_rescaling_controls':3,
            'instrumented_uninstrumented_identical':True,
            'scope':'Numerical verification. Approximate error theorem assumes ideal arithmetic.'}
    Path(__file__).with_name('verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
