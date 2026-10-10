"""Adapter that merges known sparse-update metadata with existing AdaptiveFFT.

These are floating-point tests of the decomposition, not a reproduction
of OpenAI's exact arithmetic algorithm #130.
"""
from __future__ import annotations
import numpy as np
from adaptive_fft import AdaptiveFFT
from hybrid_sparse import sparse_dft, update_spectrum, low_rank_plus_sparse
from lazy_spectrum import LazySpectrum, BufferedSpectrum, PreparedBinView


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
    def lazy_spectrum(self, base_spectrum):
        """Create a deferred metadata-aware spectrum state."""
        self.last_strategy='metadata_lazy_state'
        return LazySpectrum.from_spectrum(base_spectrum)

    def buffered_spectrum(self, base_spectrum, *, flush_threshold, flush_method='native'):
        """Create a lazy state with threshold compaction for mixed workloads."""
        self.last_strategy='metadata_buffered_state'
        return BufferedSpectrum.from_spectrum(base_spectrum,flush_threshold=flush_threshold,flush_method=flush_method)

    def prepared_bin_view(self, base_spectrum, editable_positions, bins):
        """Precompute only q*k phases for known support and selected bins."""
        self.last_strategy='metadata_prepared_bin_view'
        return PreparedBinView(base_spectrum,editable_positions,bins)

