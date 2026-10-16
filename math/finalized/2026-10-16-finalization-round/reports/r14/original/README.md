# R14 — mixed-prime Fourier rank probe

**Not a faster FFT. No sub-N-log-N runtime or world-first claim.**

This independently written small research branch proves a mixed-prime scope
extension of the project's endpoint-rank theorem and implements its explicit
permutation constructor. It does not continue the reproduced CrocSwap
parameter/network optimizations.

For the Fourier character matrix of any finite abelian group of order N>=8
with 4 dividing N, the independent-endpoint minimum maximum off-diagonal cut
rank is N/4+1. At N=4 it is 1. The proof uses classical annihilator/coset
structure and the project's existing Gram bound. Global priority is unverified.

## Files

- PROOF.md: complete proof, attribution, word-model accounting and limitations.
- annihilator_order.py: deterministic constructor, without a dense Fourier table.
- verify.py: modular and exact cyclotomic-number-field tests.
- validation_modular.json and validation_charzero.json: complete fresh results.
- countercontrols.json: natural-order and odd-cut countercontrols.
- RESEARCH_LOG.md: the tested path, rejected duplicate branches and source gaps.
- SOURCES.json: pinned GitHub sources and primary-publication metadata.
- MANIFEST.json: hashes for this release's files.

## Reproduce

Python 3.13.5 and SymPy 1.14.0 were used for these results. The constructor
itself uses the standard library only.

```sh
python annihilator_order.py 12
python annihilator_order.py 2 2 3
python -m pip install 'sympy==1.14.0'
python verify.py --suite all --output validation_rerun.json
```

The verifier uses exact finite-field arithmetic and exact arithmetic in
cyclotomic number fields, not floating-point numerical ranks. It verifies
selected finite instances; PROOF.md supplies the all-size reasoning. The
modular tests do not prove the universal characteristic-zero lower bound.

All previous checkpoints and the remote GitHub repository are unchanged.
