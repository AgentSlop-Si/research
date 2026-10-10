Public source-text preservation. The mathematical source body below is unchanged. Read [the scoped audit](../../reviews/04_jordan_jets.md) and [independent second review](../../reviews/05_jordan_second_review.md) for the accepted qualifications. In particular, the exponential-generating restatement needs invertible factorials (d < characteristic in positive characteristic); a finite union of proper finite-field subspaces need not be proper, so use the review’s corrected piecewise counting bound; and greedy piecewise recognition is an accepted-input guarantee, not a complete recognizer. Source benchmark numbers are unrerun author reports, and the padded 2N-output crossover is not an ordinary N-output speedup. No source programs are included.

# Hero #17 Phase 22 — mathematical proof certificate

**Date:** 10 October 2026. **Status:** exact identities with independent finite-field tests, scoped structured-input complexity. **No universal exact `O(N)` DFT**, no general Fourier lower bound, no publication-priority certification.

## 0. Exact arithmetic assumptions

Let `N>=3` be odd and `K` a field with `char(K)` either zero or greater than `2N`; assume `K` contains a primitive `2N`-th root `eta`. For executable checks `K=F_p`, `p` prime, `2N | p-1` and `eta` of order `2N`. Let `q=eta^8`, which has order `N`, `rho=eta^2`, and

`phi_t=product_{j=1}^t(1-q^j)`, `h_t=eta^(2t²)/phi_t` for `0<=t<N`.

Each `phi_t` is nonzero. Define `H_j(z)=sum_{t=0}^{N-1} t^j h_t z^t` with `0^0=1`. We evaluate `Y_j(k)=H_j(eta^k)` for `k mod 2N`. Field additions, subtractions, multiplications and inversions are the charged cost. Root discovery, primality certification and bit complexity are outside the supplied-root model; normal index operations are `O(N)` for fixed structural parameters but are not in the field-op ledger.

## 1. Spectral Jordan jet theorem

For `t>=1`, `(1-q^t)h_t = eta^(4t-2)h_(t-1)`. Let `D=z*d/dz`. The Phase 21 identity reads

`H_0(z)-H_0(qz)=eta² z H_0(eta⁴z)-eta^(-2)h_(N-1)z^N`.

Apply `D^j`, using `D^j(z f(z))=z(D+1)^j f(z)`, and commute `D` with argument dilation. This gives

`H_j(z)-H_j(qz) = eta² z sum_(l=0)^j C(j,l) H_l(eta⁴ z) - eta^(-2)h_(N-1) N^j z^N`.

Substitute `z=eta^k`, noting `q=eta^8`, and rearrange:

`Y_j(k+8)=Y_j(k)-eta^(k+2) sum_(l=0)^j C(j,l)Y_l(k+4)+eta^(Nk-2)h_(N-1)N^j`.

The index map `k -> k+4 (mod 2N)` has two cycles, parity even and odd, each length `N` because `N` is odd. For each degree, two direct polynomial values per cycle seed the second-order recurrence; the rest are computed in sequence. Degrees are calculated from 0 upward, so all lower-degree values already exist. Four Horner seeds per degree cost `O(Nd)` total through degree `d`, while recurrence steps cost `O(Nd²)`. Thus **all `(d+1)*2N` spectral jets are produced with `O(N(d+1)²)` arithmetic and `O(N(d+1))` memory**. When only one parity is requested, use two Horner seeds per degree and `N-2` steps; the same asymptotic bound holds with smaller constants.

Formal exponential generating function identity, for `J_k(z)=sum_(j=0)^d Y_j(k)z^j/j!`, modulo `z^(d+1)`:

`J_(k+8)(z)=J_k(z)-eta^(k+2) exp(z) J_(k+4)(z)+eta^(Nk-2)h_(N-1)exp(Nz)`.

This is an algebraic restatement of the coupled recurrences; fast truncated polynomial multiplication could reduce the `d²` overhead for growing `d`, but **no such growing-order speedup is implemented or claimed**.

## 2. Blind bounded-order Prony–Jordan recognition theorem

Suppose **without supplying the modes** the raw vector has the form

`x_t=h_t * sum_(i=1)^g P_i(t) eta^(m_i*t)`, `0<=t<N`,

with distinct `m_i mod 2N`, nonzero polynomials `P_i`, `r_i=deg(P_i)+1`, and total `R=sum r_i<=Rmax`, with `2Rmax<=N`. Assume field characteristic `>N`.

(a) Normalize in `O(N)`: `b_t=x_t/h_t`. Inverses `1/h_t=phi_t*eta^(-2t²)` are prepared without separate inversions.

(b) Each sequence `t^j u^t` is annihilated by `(E-u)^(j+1)`, where `(Eb)_t=b_(t+1)`. Thus `b` obeys a linear recurrence of order at most `R` with characteristic polynomial `prod_i (z-u_i)^(r_i)`, `u_i=eta^(m_i)`.

(c) The `R x R` Hankel matrix of `b_0,...,b_(2R-2)` is nonsingular whenever `P_i` have the stated exact degrees and distinct roots. Indeed `H=V M V^T`, with `V[t,(i,j)]=t^j u_i^t`, `t=0,...,R-1`. The confluent Vandermonde `V` is invertible for distinct nonzero roots when `char(K)>R`. For each `i`, the coefficient block is `M_i[j,l]=C(j+l,j) coeff_(i,j+l)` (zero for `j+l>=r_i`); it is anti-triangular with nonzero anti-diagonal because the top polynomial coefficient and all relevant binomial factors are nonzero. Hence `rank(H)=R`.

(d) Berlekamp–Massey on the first `2Rmax` samples recovers this minimal recurrence. Scanning the **charged** `2N` root table finds the grid roots and multiplicities in `O(NRmax+Rmax³)` operations. A confluent Vandermonde solve recovers the unknown amplitudes in `O(Rmax³)` operations; every one of the `N` input entries is then independently rechecked in `O(NRmax)`. If any condition fails, the executable code falls back to the conventional NTT.

(e) Because multiplication of `x_t` by `eta^(m_i t)` shifts the root-evaluation index, the requested spectrum is

`X(k)=sum_i sum_(j=0)^(r_i-1) coeff_(i,j) Y_j(k+m_i)`.

For fixed `Rmax`, preparing the jets and explicitly emitting all outputs costs `O(NRmax²+Rmax³)`, including recognizing the structure from **raw data** and checking every input. An ordinary length-`N` DFT needs only even root positions `k=2s`; each discovered `m_i` requires only the parity orbit `m_i mod 2`. Therefore the `apply_n` implementation computes exactly `N` outputs and does not need to build unused parity orbits.

## 3. Truncated-interval spectral jet theorem

For `0<=a<b<=N`, define `H_[a,b),j(z)=sum_(t=a)^(b-1) t^j h_t z^t`. Direct coefficient comparison yields

`H_[a,b),0(z)-H_[a,b),0(qz)=eta² z H_[a,b),0(eta⁴z)+(1-q^a)h_a z^a-eta^(4b-2)h_(b-1)z^b`.

By the same derivative argument, at `z=eta^k`:

`Y_[a,b),j(k+8) = Y_[a,b),j(k) - eta^(k+2)*sum_(l<=j)C(j,l)Y_[a,b),l(k+4) - (1-q^a)h_a a^j eta^(ka) + eta^(4b-2)h_(b-1)b^j eta^(kb)`.

Four Horner seeds across `[a,b)`, then two `N`-cycles, compute every `2N` spectral values of each interval jet in `O(Nd² + d(b-a))` arithmetic through degree `d`. Input segment normalization converts `P(t-a)eta^(m(t-a))` into an ordinary polynomial in absolute `t` times `eta^(mt)` with `O(d²)` charged arithmetic, then uses shifted interval jets.

A greedy blind piecewise recognizer fits a bounded-order exponential polynomial to `2Rmax` consecutive normalized coefficients, checks each subsequent coefficient until the first mismatch, and repeats. A final tail shorter than `2Rmax` is explicitly evaluated via point contributions. If more than the declared number `s` of segments are required or a prefix has no valid fit, it falls back to conventional NTT. Every accepted piece is checked entry-by-entry, and segments exactly partition all positions, so **acceptance implies correct results without assumptions about the caller's metadata**. For fixed `s,Rmax` the accepted-input work is `O(s N Rmax² + s Rmax³)`; memory is `O(NRmax)` when interval-jet buffers are freed after each segment.

## 4. Relationship to Phase 21 sparse defects

For `x_t=h_t b_t`, the Phase 21 defect is

`r_t=(1-q^t)x_t-eta^(4t-2)x_(t-1)=(1-q^t)h_t(b_t-b_(t-1))`.

All factors before the final difference are nonzero for `1<=t<N`. Hence `r_t=0` **if and only if** `b_t=b_(t-1)`. So q-defects are sparse exactly when `b_t` has few change points. Phase 21's k-defect signals are piecewise-constant normalized sequences with at most `k+1` segments. Phase 22 handles polynomial-exponential segments, including examples with `N-1` nonzero Phase 21 defects. The greedy recognizer requires adequate segment lengths to infer their local recurrence; very short interior segments can trigger an ordinary NTT fallback even though the theoretical piecewise family includes them.

## 5. Bounded-order model cannot cover arbitrary dense inputs

For each fixed choice of roots and multiplicities of total order at most `R`, normalized sequences `b_t` lie in a linear subspace of dimension at most `R` (confluent Vandermonde columns). There are at most `C(2N+R,R)` multisets of up to `R` allowed roots. For `b` uniformly distributed in `F_p^N`, the fraction with a bounded-order representation is therefore at most

`min(1, C(2N+R,R) * p^(R-N))`.

For fixed `R` and primes `p>=2N+1` this tends to zero. For `s` piecewise segments, the union across finitely many boundaries and root configurations consists of subspaces of dimension at most `sR` (apart from the optional bounded literal tail), so it is also a proper subset of all data when the dimensions stay below `N`. This is a **restricted representability barrier**, not a complexity-theoretic lower bound for the unrestricted DFT.

## 6. Cost and fairness caveats

- The `N=3^m` ordinary baseline is a separate **length-N** conventional NTT. The Phase 21 same-length convolution baseline is a **length-2N** zero-padded NTT. These are different workloads, and both comparisons are preserved explicitly.
- A finite-operation crossover for fixed-order inputs occurs at `N=59049` for the **2N-output padded transform**. The conventional true `N`-output NTT remains cheaper at every tested length through `N=177147`.
- Tests and operation ledgers use supplied roots of unity and scalar prime-field arithmetic. Python times are debugging observations, not benchmark claims. Index arithmetic has the same `O_R(N)` asymptotic but is not included in scalar field-operation tables.
- Historical novelty **unverified**. q-holonomic methods, Prony/Berlekamp–Massey and Hankel/confluent-Vandermonde recognition are established mathematical ingredients. The precise bundled spectral recurrence/recognition specialization needs independent literature review.
- Nothing here establishes `O(N)` for arbitrary fresh inputs, general integer multiplication, numerical stability, or a new worst-case FFT upper bound.
