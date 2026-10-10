"""Adapter that merges known sparse-update metadata with existing AdaptiveFFT.

These are floating-point tests of the decomposition, not a reproduction
of OpenAI's exact arithmetic algorithm #130.
"""
from __future__ import annotations
import numpy as np
from adaptive_fft import AdaptiveFFT
from hybrid_sparse import sparse_dft, update_spectrum, low_rank_plus_sparse


class HybridAdaptiveFFT(AdaptiveFFT):
    def fft_from_delta(self, base_spectrum, edits, *, algorithm='factorized'):
        """Return full spectrum after edits, without rescanning original input.

        base_spectrum is a precomputed full complex DFT; edits is a list
        of (index, delta) pairs. User supplies their validity.
        """
        if algorithm == 'factorized':
            ans, plan=update_spectrum(base_spectrum, edits)
            self.last_strategy='metadata_sparse_factorized'
            return ans, plan
        if algorithm == 'direct':
            source=np.asarray(base_spectrum, dtype=np.complex128)
            n=source.size
            ks=np.arange(n)
            result=source.copy()
            for index,delta in edits:
                result += delta*np.exp(-2j*np.pi*(index % n)*ks/n)
            self.last_strategy='metadata_sparse_direct'
            return result, None
        raise ValueError('algorithm must be factorized or direct')

    def rfft_from_delta(self, base_rfft, n, real_edits):
        """Efficiently update compact spectrum for a real signal."""
        compact=np.asarray(base_rfft,dtype=np.complex128)
        if compact.ndim!=1 or compact.size!=n//2+1:
            raise ValueError('incorrect compact spectrum length')
        edits=list(real_edits)
        if any(complex(v).imag!=0 for _,v in edits):
            raise ValueError('rfft edits must be real')
        delta,plan=sparse_dft(n,edits,return_plan=True)
        self.last_strategy='metadata_rfft_sparse'
        return compact + delta[:n//2+1],plan

    def fft_basis_plus_sparse(self, basis_spectra, coefficients, edits):
        """Use known basis spectra plus a sparse residual."""
        ans,plan=low_rank_plus_sparse(basis_spectra,coefficients,edits)
        self.last_strategy='metadata_low_rank_plus_sparse'
        return ans,plan
