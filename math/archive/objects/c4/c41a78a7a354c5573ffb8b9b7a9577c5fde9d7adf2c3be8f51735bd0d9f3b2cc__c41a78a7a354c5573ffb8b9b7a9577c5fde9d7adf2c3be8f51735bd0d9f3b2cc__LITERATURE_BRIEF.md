# Primary-source checkpoint: pruning, error scales and the exact baseline

Checked 2026-10-09. The independent exact-FFT research route remains separate
from the external exact-complex result below.

## What the pruning literature establishes

The [FFTW authors' pruning note](https://fftw.org/pruned.html) describes
O(N log K) arithmetic when K Fourier outputs are requested, or dually when
only K inputs are nonzero. It also distinguishes operation-count savings from
actual performance. This supports the known sparse-input/output ingredient;
it does not by itself locate unknown large outputs under a new error contract.

[Bringmann et al., arXiv:2107.07347v2](https://arxiv.org/pdf/2107.07347)
explicitly study traversal of Cooley-Tukey computation trees, including exact
sparse recovery and a noisy extension. Their model uses signal-access/filter
procedures, Fourier sparsity and stated noise assumptions. Their theorems are
not the same as our full-input global-norm hard-threshold guarantee. The paper
also traces earlier tree approaches to Mansour and Kushilevitz-Mansour.

The primary [Kushilevitz-Mansour paper](https://doi.org/10.1137/0222080)
concerns learning through Fourier structure on the Boolean cube; its publisher
abstract and bibliographic record were checked. Direct PDF fetches failed, so
this review does not claim a line-by-line equivalence to its algorithm.

[Li and Nakos, ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.77)
make the error-contract distinction explicit: their l_infinity/l1 guarantee
uses the Fourier tail, and their table includes a tail-sensitive l_infinity/l2
guarantee. Our threshold epsilon||x||_2 is based on total energy and can permit
the zero vector for diffuse spectra. Those guarantees must not be conflated.

A further [2025 pruned-FFT application](https://www.vut.cz/www_base/vav_priloha.php?prilohaID=306416&vavID=193778)
uses spectrum-area estimation, including a considered norm-threshold method.
Its preprocessing already uses transforms and application-specific modelling;
it is not an equivalent universal cold-input linear-work theorem.

**Assessment:** pruning and energy-based heavy-coefficient search have substantial
prior art. This focused search did not locate an exact prior statement of the
same deterministic full-input/full-output hard-threshold algorithm with work
O(N[1+min(log N,log(1/epsilon))]). That is a search limitation, not evidence of
novelty. The appropriate claim is a verified implementation and proof in our
specified model, pending a broader priority review.

## The stronger l1/sqrt(N) target

Let tau=||x||_1/(sqrt(N)||x||_2). Calibrating the energy-pruned algorithm to
error epsilon||x||_1/sqrt(N) means using epsilon_E=epsilon*tau. Its work bound is

    O(N[1+min(log N, log(1/epsilon)+log(1/tau))]).

An impulse has tau=N^(-1/2): at epsilon<1, all Fourier coefficients exceed this
calibrated threshold and the entire graph is evaluated. A sparse-input method
handles that same input in O(N). Therefore the pruning result does not uniformly
improve the sparse-surrogate result on its stronger error scale.

A constructive combination is to preserve a cheap time-domain head h exactly
and apply calibrated energy pruning only to r=x-h. With eta=epsilon||x||_1/sqrt(N),
an s-sparse head has known-input transform cost O(N log(s+2)); the residual costs

    O(N[1+min(log N, log_+(||r||_2/eta))]).

Their output sum meets the stronger contract deterministically in ideal
arithmetic. Head selection and residual norms must be charged; the single-
selection planner from the v2 review makes a polylogarithmic head search linear.
This is a useful conditional combination, not a uniform O(N) theorem: both
terms can still be logarithmic. It suggests evaluating head sizes by actual
residual energy, rather than by support alone.

## Current exact-complex baseline

The official [OpenAI #130 scope document](https://github.com/openai/math/blob/main/lean/docs/130.md)
currently distinguishes a subsequential circuit result from a separate uniform
claim for every positive length: deterministic exact DFT and full convolution
in O(n(log n)^(1-10^(-13))), with scalar preparation and root-order selection
charged. A chosen root is supplied; complex coefficients are unrestricted and
indices polynomially bounded. The document excludes synthesis-appendix
extraction/search/printer uniformization from its selected statements.

This review verifies that current source statement, not its entire formal
development or a practical implementation. It is incorrect to describe the
unrestricted exact-complex n-log-n barrier as universally unresolved while
ignoring this claimed result. Our narrower goal remains a separately justified
independent mechanism; importing #130 would not establish that mechanism.
