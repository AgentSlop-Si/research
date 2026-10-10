"""A short readable demonstration of guaranteed sharing and lookup batching."""
import numpy as np
from structural_fft import FFTGraph, SharedLookupTable, fwht_mod, tabulated_fwht_mod


def run():
    n=16
    plain=FFTGraph(n,'radix2')
    split=FFTGraph(n,'split_radix')
    rng=np.random.default_rng(20261009)
    a=rng.standard_normal(n)
    b=rng.standard_normal(n)
    xa,xb=split.execute_two_real(a,b)
    assert np.allclose(xa,np.fft.fft(a))
    assert np.allclose(xb,np.fft.fft(b))
    print('Two completely different real inputs -> one complex split-radix FFT')
    print('Radix-2 generic multiplications per FFT:',plain.stats()['nontrivial_complex_multiplies'])
    print('Split-radix generic multiplications per FFT:',split.stats()['nontrivial_complex_multiplies'])
    print('Two radix-2 transforms, generic multiplies:',2*plain.stats()['nontrivial_complex_multiplies'])
    print('Packed split-radix, generic multiplies:',split.stats()['nontrivial_complex_multiplies'])
    print('Plus O(N) arithmetic to decode both spectra.')
    print()
    x=[1,0,2,1,2,0,1,0,2,1,0,2,2,1,1,0]
    cache=SharedLookupTable(p=3)
    result, accounting=tabulated_fwht_mod(x,3,block=4,cache=cache)
    assert result==fwht_mod(x,3)
    print('Walsh-Hadamard transform over F3, 16 arbitrary input symbols:')
    print('Input:',x)
    print('Output:',result)
    print('Lookup passes:',accounting['passes'], 'table lookups:',accounting['lookups'])
    print('Full offline-table compilation:',cache.stats())
    print('\nNOTE: Finite-field WHT is not an ordinary complex FFT.')


if __name__=='__main__':
    run()
