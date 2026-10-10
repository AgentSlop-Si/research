# HERO #17 — Phase 16: Fourier–Green interface rigidity, chirp-gauged boundary factorization, and Harper audits

**10 October 2026 | Exact field arithmetic | Research status: completed scoped theorem; arbitrary-input `O(N)` FFT remains unsolved.**

## Why Phase 16 is different

The Phase 15 Weyl-support theorem excluded a product of a few Green stages whose inverses use a small number of Weyl monomials. It did **not** cover arbitrary diagonal chirps. We now take the opposite approach: allow *any invertible endpoint diagonal phases* and *arbitrary position-dependent coefficients* in the two sparse interface factors. Instead of Weyl support, use the zero-count of Fourier transforms of consecutive-support vectors. This yields an exact no-go theorem for a broad local `P Q^-1` Green architecture.

Our second result is constructive: an explicit borderline factorization `F=P Q^-1` at small odd lengths, provided a cyclotomic polynomial matrix `Q` is invertible. The new factorization is **not** a faster FFT: `Q` is a quadratic-chirp-gauged convolution whose inverse may require dense work.

## Result A — the exact local Green interface barrier

Let `F_N` be the unnormalized negative DFT. If

\[
F_N=D_LP Q^{-1}D_R
\]

with invertible diagonal `D_L,D_R`, invertible `Q`, `P` cyclic band radius `a`, and `Q` cyclic band radius `b`, then

\[
\boxed{a+b\ge\lceil(N-1)/2\rceil.}
\]

**Proof in one line:** for each column of `Q`, after diagonal scaling, the input polynomial has at most `2b` zeros at `N` distinct Fourier roots, whereas the required output has at least `N-(2a+1)` zeros.

This is valid for every `N`, including powers of two, and over exact prime fields containing the primitive root. `P` and `Q` need *not* commute and need *not* be functions of the same matrix. The long-distance sparse shift escape is restricted: at composite lengths noncontiguous support does evade this *additive* proof; over complex prime lengths Tao's stronger general uncertainty theorem also treats arbitrary sparse support sets.

The degree corollary holds for arbitrary cyclic tridiagonal `H`: any equality `F=D_L p(H)q(H)^-1 D_R` forces `deg p+deg q >= ceil((N-1)/2)`. This rules out a fixed-degree Harper/Green rational transform, though it does **not** prove a time lower bound for arbitrary jointly evaluated rational functions.

## Result B — a sharp support-boundary construction

For `N=2(a+b)+1`, let frequency window `J_j={j-a,...,j+a}` and define the degree-`2b` polynomial

\[
h_j(z)=\prod_{k\notin J_j}(z-\omega^{-k}).
\]

Place its coefficients at consecutive input indices `j-b,...,j+b` to form column `j` of `Q`. Define `P=FQ`. Then `Q` has cyclic bandwidth `b`, `P` has cyclic bandwidth `a`, and every column is the **unique** such interface at equality up to scaling. When `Q` is invertible, we obtain the exact two-factor DFT representation `F=P Q^-1`.

Exact modular determinants certify complex invertibility for the following specific tested instances, because a nonzero reduction of the determinant of a cyclotomic-integer matrix implies the complex determinant cannot vanish.

| `N` | Prime field | Band radii `(a,b)` | `rank Q` | Full basis-vector DFT check |
|---:|---:|---:|---:|---|
| 5 | 11 | (1,1) | 5 | Passed |
| 9 | 19 | (2,2) | 9 | Passed |
| 13 | 53 | (3,3) | 13 | Passed |
| 17 | 103 | (4,4) | 17 | Passed |
| 45 | 271 | (11,11) | 45 | Verified algebraically; direct smaller checks |

These are *scoped sharpness examples*, not an all-length invertibility theorem.

## Result C — field-dependent denominator singularity

This family has a subtle exact-finite-field issue: the root set and support identities can be perfectly valid while the assembled denominator matrix is singular.

| `N` | Field | `rank Q` | Consequence |
|---:|---:|---:|---|
| 45 | `GF(181)` | 43/45 | Cannot invert `Q` |
| 45 | `GF(271)` | 45/45 | Factorization works |
| 49 | `GF(197)` | 47/49 | Cannot invert `Q` |
| 49 | `GF(491)` | 49/49 | Factorization works |
| 53 | `GF(107)` | 49/53 | Cannot invert `Q` |
| 53 | `GF(743)` | 53/53 | Factorization works |

Thus merely proving `FQ=P` and band limits does not imply a valid algorithm `F=P Q^-1`. The implementation **checks exact invertibility before execution**.

## Result D — the boundary denominator is a chirp-gauged circulant

For odd `N`, the explicit `Q` can be written

\[
\boxed{Q=L C_h R,}
\]

where `L_t=omega^(t(t-1)/2)`, `R_j=omega^(-j(j-1)/2-bj)`, and `C_h` is the cyclic convolution with `h_s=c_(s+b) omega^(-s(s-1)/2)` supported at `-b<=s<=b`, for the base annihilator coefficients `c_r`.

This identity passed exact entrywise checks at every tested small length. **Crucially:** `Q^-1=R^-1 C_h^-1 L^-1`. We have not found an `O(N)` evaluator for arbitrary vectors for `C_h^-1`; the factorization relocates difficult convolution into the denominator instead of eliminating it. Convolution-kernel generation, even in linear time, does not prove linear-time convolution.

## Result E — Clifford quadratic shears do not add Weyl support when paired

For `D_c e_j=omega^(c j^2)e_j`, cyclic shift `S`, and modulation `T`,

\[
\boxed{D_c S^s D_c^{-1}=\omega^{cs^2} S^s T^{2cs}.}
\]

Therefore chirp **conjugation** moves a shift to a Weyl direction without increasing the number of Weyl monomials in an inverse stage. Chirp factors inserted without corresponding inverses can behave differently; the Phase 15 support theorem must not be stretched beyond its assumptions.

## Result F — exact Harper/commuting-operator exploration

We revisited the noncommuting nearest-neighbor discrete oscillator

\[
H=S+S^{-1}+T+T^{-1}.
\]

It **commutes exactly** with `F` (because `F` interchanges shift and modulation up to inversion). Small prime-field experiments found:

- For tested odd lengths `N=3,5,7,9,11,13,15`, `F` belongs to the algebra spanned by `I,H,...,H^(N-1)`, and invertible rational witnesses `p(H)q(H)^-1` were found with maximum degree `(N-1)/2`.
- For tested `N=4,8,12,16`, the span of powers of `H` had dimension `N-1` over the stated finite field, and adjoining `F` increased it to `N`: `F` is **not** a rational function of this `H` in those exact fields.
- For tested `N=6,10`, the span of powers had full dimension `N`.

These are **finite, exact field certificates**, not a proof of those patterns over `C` for all lengths or a historical-first result. Commuting Harper/Grünbaum operators have extensive prior art. Even when a low-degree rational witness exists, computing `q(H)^-1` is not free, and the degrees grow with `N` in the experiments.

## Reproducible verification

- `19/19` Phase 16 unit-test groups passed.
- `21/21` Phase 15 predecessor test groups reran successfully.
- Independent audit reconstructed `120` complete exact DFTs (`1,368` output coefficients), including all basis vectors at lengths `3,5,7,9,11,13,15,17` and fresh random inputs.
- Exhaustively enumerated all `17^3-1=4,912` nonzero 3-coordinate inputs over `GF(17)` for a 16-point transform. Every one had at most 2 Fourier zeros; the bound was attained.
- Independently classified 13 exact finite-field Harper algebra ranks, and checked six field-sensitive denominator rank cases.
- Verified Fourier intertwining on all 17 basis vectors at `N=17`.

The results and exact parameters are in `AUDIT_RESULTS.json`. Test loops intentionally use slow direct arithmetic: they **verify algebra**, not speed.

## Practical operation-cost conclusion

At the borderline balanced construction, `a,b=Theta(N)`. The matrices `P,Q` each have `Theta(N^2)` entries on the potential bands. Although their formulas are compact, no faster method was shown for applying `Q^-1` or the associated chirp convolution to **arbitrary** fresh input. Therefore there is **no new unrestricted FFT upper bound** and no demonstrated speedup against modern FFT libraries.

## Phase 17 target

The class still alive is a **branching Green network that cannot be written as a single two-sided locally banded quotient**. Specifically, investigate whether a sum or feedback composition of noncommuting chirp-conjugated Green resolvents yields a *shared* exact evaluator satisfying both Fourier intertwining identities, while the charged cost of synthesis, solving and output remains `o(N log N)`. Do **not** count a sparse quotient as a solution until its inverse application is independently costed.

## Prior art and context

- Terence Tao, [An uncertainty principle for cyclic groups of prime order](https://arxiv.org/abs/math/0308286), 2003/2005 — uncertainty basis for prime-length arbitrary supports.
- Murty and Whang, [The uncertainty principle and a generalization of a theorem of Tao](https://doi.org/10.1016/j.laa.2012.02.009) — extensions to finite cyclic groups.
- Grünbaum, *The eigenvectors of the discrete Fourier transform: a version of the Hermite functions* (1982), and later commuting Harper/Grünbaum matrix work — sparse operators commuting with DFT are classical.
- [OpenAI Math, exact DFT below `N log N`, result 130](https://github.com/openai/math/blob/main/overview.tex) — uniform exact-complex-arithmetic benchmark `O(N(log N)^(1-10^-13))`, with model restrictions.

**Novelty status:** The project-specific combination and reproducible certificates may be useful, but the central consecutive-root proof is elementary Fourier uncertainty. No unreviewed "first-ever" claim is made.
