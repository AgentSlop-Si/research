# Gaussian Weyl coefficients and reciprocal Green chart weights

Version 2026-10-10, Phase 20 source version 0. Mathematical status: independent scoped acceptance with corrected dense arithmetic counts and an explicit all-length implementation caveat.

The all-length Weyl coefficient identities, even parity blocks and odd first-chart Hankel contraction are valid in the stated exact-field model. The coefficient transform is Fourier-equivalent by simple diagonal/permutation reductions. The weight contraction is an auxiliary convolution, not the full cross-index Weyl synthesis. Finite-chirp parity is classical. None of these facts provides a new full-DFT speedup or establishes historical priority of the specific chart formulation.

The even-chart rank/convolution extension below is an immediate independently derived algebraic corollary, with fresh finite controls; it is distinguished from the original Phase 20 theorem.

## 1. Conventions and hypotheses

Let `K` be a field containing a primitive `N`-th root `w`, with the integer `N` invertible in `K`. The source additionally excludes characteristic two. Let

`S e_t = e_(t+1 mod N)`, `T e_t = w^t e_t`, `TS = w ST`,

and use the **unnormalized, negative-exponent** Fourier matrix `F[k,t] = w^(-kt)`. Let `F = sum_(a,b) C[a,b] S^a T^b`. All exponents are integer residues modulo `N`. Fractions such as `1/4` in an exponent mean inversion modulo odd `N`; they do not mean choosing a complex fourth root.

The exact coefficient is

`C[a,b] = (1/N) trace(T^(-b) S^(-a) F) = G(a+b)/N`,

where `G(r) = sum_t w^(-t^2-rt)`.

Indeed, the t-th diagonal entry of `T^(-b)S^(-a)F` is `w^(-bt)F[t+a,t]`. Weyl trace orthogonality gives the coefficient normalization `1/N`. Replacing `F` with the unitary DFT would multiply every coefficient and chart weight by `1/sqrt(N)`; it would not preserve the displayed prefactor unchanged.

The complete one-axis contraction is

`sum_b C[a,b]w^(bt) = w^(-t^2-at)`.

Character orthogonality proves this directly. In the operator synthesis, the output index is `k=t+a`, so this is precisely `w^(-kt)`. It removes an algebraic summation index while retaining the dense DFT matrix-vector product.

## 2. Independent all-length proof

### Odd length

Substitute `t=u-1` to obtain `G(r+2)=w^(r+1)G(r)`. For odd `N`, completing the square in the exponent ring gives

`G(r)=G(0)w^(r^2/4)`.

The prefactor is nonzero. If `G_plus=sum_t w^(t^2)`, the bijection `(t,s) -> (t-s,t+s)` yields `G(0)G_plus=N`. Define `gamma=G(0)/N`, `D[a,a]=w^(a^2/4)`, and `J[a,b]=w^(ab/2)`. Then

`C=gamma D J D`.

`J` is the negative-exponent DFT with output row `-a/2`. Thus one coefficient matvec and one DFT reduce to each other with linear diagonal and permutation work. For the reverse direction, take `z_b=w^(-b^2/4)x_b`, compute `y=Cz`, and return

`F x[k] = y[(-2k) mod N] / (gamma w^(((-2k) mod N)^2/4))`.

Preparing the inverse diagonals can use the same root-power table and one inverse of `gamma`; it does not require `N` unrelated inversions. The source's test oracle uses per-coordinate inversion, which is acceptable as a check but is not the optimal reduction ledger.

### Even length

Let `N=2m`, `kappa=m mod 2`. Translation by `m` multiplies each summand of `G(r)` by `(-1)^(m+r)`. Therefore the wrong parity vanishes. Iterating the recurrence gives

`G(kappa+2ell)=G(kappa)w^(ell^2+kappa ell)`.

This is consistent when `ell` is reduced modulo `m`: the exponent change is `m(2ell+m+kappa)`, a multiple of `2m`. The surviving value cannot vanish, since otherwise every Fourier coefficient of the nonzero chirp vector would vanish. The Fourier matrix is invertible by character orthogonality.

For row parity `p` and column parity `q`, a block is zero unless `p+q = kappa mod 2`. On a surviving block, write `d=(p+q-kappa)/2` and `gamma=G(kappa)/N`. For `0<=a,b<m`,

`C[2a+p,2b+q] = gamma w^(d^2+kappa d) w^(a^2+(2d+kappa)a) (w^2)^(ab) w^(b^2+(2d+kappa)b)`.

Since `w^2` has exact order `m`, each surviving block is invertible and is diagonal-equivalent to a length-m Fourier matrix. Hence `rank C=N` and precisely `N^2/2` entries vanish.

- `N=0 mod 4`: `kappa=0`, so the parity-reordered matrix is block diagonal.
- `N=2 mod 4`: `kappa=1`, so it is block antidiagonal.
- `N=2` is valid, with two one-dimensional blocks.
- `N=1` is trivial mathematically but is outside the supplied public validator's supported domain.

No primitive even-order root exists in characteristic two. More generally, in characteristic `p`, an element cannot have order divisible by `p`. Odd-length algebra does not need the source's blanket exclusion of characteristic two, but the executed implementation is restricted to odd prime fields. No conclusion here silently changes that implementation contract.

### Direct rank and scale identity

For **every** supported length,

`C = (1/N) F diag(w^(-t^2)) F`.

Its `(a,b)` entry is the defining Gauss sum divided by `N`. All factors are invertible, proving full rank without a parity calculation. Over `C`, write `U=F/sqrt(N)`; then `C=U diag(w^(-t^2)) U` is unitary. Consequently `|G(0)|=sqrt(N)` at odd length and `|G(kappa)|=sqrt(2N)` at even length, consistent with both block normalizations. This identity is an elementary audit check, not a novelty claim.

## 3. Green-sector normalization and the weight operator

Let nonzero `alpha,beta` satisfy `delta=1-alpha^N-beta^N != 0`. For `0<=r<N`, set `phi_r=product_(j=1)^r(1-w^j)`, with `phi_0=1`. Every factor is nonzero in a field. The ordered q-binomial identity gives

`(alpha w^ell S + beta w^j T)^N = (alpha^N+beta^N)I`.

The inverse of `I-alpha w^ell S-beta w^j T` is therefore its degree-(N-1) geometric polynomial divided by `delta`. Taking the **normalized double character average** `N^(-2) sum_(ell,j) w^(-a ell-bj)` selects exactly

`g[a,b] S^a T^b`, with `g[a,b]=alpha^a beta^b phi_(a+b)/(delta phi_a phi_b)`

on `a+b<N`, and selects zero otherwise. The distinction between an average and an unnormalized sum matters by `N^2`. Fresh controls directly invert all branch matrices at six small lengths and verify this normalization, independently of the q-factorial formula.

For odd `N`, division of the Fourier coefficient by this sector scalar gives

`W[a,b]=delta gamma A_a B_b H_(a+b)` on `a+b<N`, and zero elsewhere,

where `A_a=phi_a alpha^(-a)`, `B_b=phi_b beta^(-b)`, `H_s=w^(s^2/4)/phi_s`. The scalar is **delta times gamma**. A source docstring saying “gamma/delta” is a wording error; the theorem and implemented scalar use the correct product.

Reverse the columns of `W`. The resulting matrix has support `a<=j`, and its diagonal consists of the nonzero entries `W[a,N-1-a]`. This proves `rank W=N`. A sum of `r` outer products must have `r>=N`; this is a rank bound for a separable coefficient-table representation, not an arithmetic-circuit lower bound.

Set `v_b=B_b x_b`. With `h_s=H_s` for `0<=s<N`, the coefficient of degree `N-1+a` in `h(z) sum_b v_b z^(N-1-b)` is

`sum_(b=0)^(N-1-a) H_(a+b)B_b x_b`.

Thus `Wx` is a diagonally scaled, reversed polynomial convolution. Padding to `L>=2N-1` prevents wraparound. A forward transform of each padded input, pointwise multiplication, and an inverse transform normalized by `1/L` produce it exactly.

The input coordinate `b` here is a **character-weight coordinate**. It is not the original signal coordinate inside `sum_(a,b) W[a,b]g[a,b]S^aT^b x`. The latter expression couples both Weyl indices with shifts and modulations. No cost for executing that full two-chart synthesis is supplied by the single weight-matvec identity.

### Immediate even-length chart corollary

The odd restriction is needed for the source's particular nonvanishing chirp parametrization, not for the convolution mechanism. For arbitrary supported `N`, set

`H_s=G(s)/(N phi_s)` and `W[a,b]=delta A_a B_b H_(a+b)` on the same triangle.

The convolution identity remains valid. At even length, prepare `G` from its one surviving parity and the step-two recurrence in linear field work. The exact rank is

`rank W = N` if `N` is odd or `N=2 mod 4`, and `rank W=N-1` if `N=0 mod 4`.

For `N=2 mod 4`, the final antidiagonal is nonzero. For `N=0 mod 4`, the last row is zero, while the leading `(N-1)` square has nonzero final antidiagonal of degree `N-2`. This proves both bounds. Forty additional exact even-field cases verify the corollary. It is an audit-derived extension, not a result claimed in the Phase 20 theorem and not a historical originality claim.

## 4. Complete operation accounting

These are unit-cost field ledgers, not wall-clock timings or bit-operation counts. Let `E(e)=bit_length(e)+popcount(e)-1`, the source's binary-power multiplication count, and let

`V(n)=E(n)+sum_(prime r divides n) E(n/r)`.

This charges its successful primitive-root validation. Let `T(L)=L-1+(3/2)L log2(L)` be one unnormalized radix-2 transform: root-table generation plus one multiplication and two additions per butterfly.

### First-chart cold setup

The exact constructor count is

`P(N,L)=11N+1+2E(N)+V(N)+V(L)`.

It includes root checks, N-th powers of the scalar parameters, root powers, forward q-factorials, one inverse for all reciprocal factorials followed by a backward recurrence, inverses of `alpha,beta,N`, chirp access, the Gauss prefactor, and the final scalar. Its integer indexing and factorization operations are separate from field arithmetic.

### Chart application

The exact online count is

`3T(L)+L+4N+2 = (9/2)L log2(L)+4L+4N-1`.

The non-transform terms are `N` input scalings, `L` pointwise products, two inversions, and three multiplications per returned coordinate, including inverse-transform normalization. Reversal, zero padding, extraction, input reads, output writes, and root-table indexing are not field operations; they require linear or `O(L log L)` RAM work. There are a constant number of length-N and length-L arrays, so live storage is `O(N)` because `2N-1<=L<4N-2`.

For repeated inputs, a fixed kernel transform could be cached, but its transform must be charged to setup. The source recomputes it and correctly charges three transforms per call. Neither variant avoids FFT/convolution work.

### Corrected dense comparison

Let `Q=N(N+1)/2`. The actual displayed dense loop costs `3Q+2N` online. Both this loop and the convolution share setup `P`; a cold/cold comparison must add it to both. Moving `B_b x_b` outside the output loop gives the equally elementary direct algorithm with online cost `2Q+3N`. This optimized direct baseline remains quadratic.

| N | Convolution cold total | Correct literal dense online | Correct literal dense cold | Cold ratio | Shared-input direct cold ratio |
|---:|---:|---:|---:|---:|---:|
| 255 | 26,699 | 98,430 | 101,326 | 3.80 | 2.58 |
| 1,023 | 125,024 | 1,573,374 | 1,584,739 | 12.68 | 8.49 |
| 4,095 | 573,579 | 25,167,870 | 25,213,070 | 43.96 | 29.34 |
| 8,191 | 1,220,698 | 100,667,390 | 100,757,597 | 82.54 | 55.06 |
| 16,383 | 2,588,812 | 402,661,374 | 402,841,743 | 155.61 | 103.77 |

Every ratio compares an auxiliary weight matvec with a quadratic way of computing that same matvec. None compares two full DFT algorithms. The source's 207.38 ratio is not the count of its stated direct loop.

### Coefficient-transform benchmark and all-length fallback

For the source's even implementation, the wrapper overhead is `V(N)+5N+4`, plus two chosen half-length transforms. At `N=65536`, this reproduces **1,867,811** operations. The ordinary radix-2 count is **1,638,399**, or **1,638,432** with the same root-validation charge. Both are `Theta(N log N)`, and they compute different, simply related operators.

At odd `N=8191`, the full coefficient action is **1,179,717**, while its ordinary Bluestein DFT is **1,138,735**. These source counts, including the chirps, root tests and normalizations, match the static formulas.

On even `N` with non-dyadic `N/2`, the supplied `dft_baseline` chooses direct summation. The exact coefficient count is then `N^2+6N+2+V(N)`, for example **1,106** at `N=30`. Supplying `ntt_root` does not alter that branch. A generic fast backend can repair the implementation scope, but would be an additional implementation, and its needed roots and conversions must be charged. It would not be new mathematics.

## 5. Exact-field, root-supply and numerical boundaries

- The finite-field programs assume a supplied **prime** `p`. Their validator does not prove primality. The composite example `p=91,N=3,w=29` passes its order-style checks but gives character sum `1+w+w^2=52 mod 91`, not zero. Thus the validator is not a standalone proof of the field hypotheses. This is outside the promised prime-input contract, not a counterexample to the theorem.
- Existence of an N-th root does not imply existence of the padding root. The source executor additionally needs a primitive L-th root in the **same field**. For odd `N`, `N L` divides `p-1`. Finding a suitable prime/root, constructing an extension, and translating input/output representations are not proved free or uniformly cheap.
- A field inversion is counted as one operation. Real implementations pay for arithmetic on `log p`-bit residues. Integer modular exponents, integer inverses modulo `N`, addressing and factorization are not included in these field totals. No integer-multiplication result follows.
- Over complex numbers, `C` is well conditioned in the 2-norm, but this does not automatically establish a stable implementation. The Green weight matrix can have severe diagonal scaling, reciprocal-factorial dynamic range and parameter-dependent conditioning. Near-singular `delta`, tiny `alpha` or `beta`, cancellation in Gauss sums, and root approximation need explicit precision analysis. The source offers none, and exact modular tests do not supply one.
- Treating the coefficient or weight table as an implicit linear-size representation is valid storage compression. It neither removes all field operations nor authorizes treating cross-index Weyl synthesis or N explicit outputs as free.

## 6. Primary-source comparison and priority

**Finite chirps, including even parity.** Casazza and Fickus define `c_a^b(t)=exp(pi i b t(t-a)/a)`. Taking `a=N,b=-2` gives the chirp `w^(-t^2)` for the canonical root. Their normalized negative-exponent transform is `G(r)/sqrt(N)`. Proposition 5 yields support on all residues for odd N, even residues for `N=0 mod 4`, and odd residues for `N=2 mod 4`; Theorems 1–2 give the decimated chirp phases. The even zero-pattern claim is therefore directly covered over C. A different primitive root follows by changing the chirp rate and relabeling frequencies. The finite-field proof above is independent. [Casazza–Fickus, 2006, pp. 4–6](https://link.springer.com/content/pdf/10.1155/ASP/2006/70204.pdf).

**Weyl symbols.** The trace-over-dimension formula and quadratic Weyl kernels are explicit in Gurevich–Hadani, §1.3.1, equations (1.2)–(1.3). Their paper treats the odd-prime finite Weil setting; it is not, by itself, a citation proving every composite or even-length statement here. [Gurevich–Hadani](https://arxiv.org/html/0902.0668v1).

**q-binomial ingredients.** The ordered q-binomial theorem, factorial ratio, and recurrence appear in Stoyanovsky's Theorem 1, which explicitly credits earlier work. Dividing that factorial ratio into a Gaussian coefficient produces the displayed diagonal-Hankel form by elementary algebra. This does not establish historical priority for the particular chart packaging. [Stoyanovsky](https://arxiv.org/pdf/0812.4916).

**Convolution and CZT.** Rabiner–Schafer–Rader's 1969 paper derives chirp preprocessing, a convolution, and output chirp scaling; it explicitly uses two forward FFTs, one inverse FFT, and padding length at least `N+M-1`. Bluestein's published chirp-filter paper predates this project's relabeling by decades. The present Hankel kernel has an extra reciprocal q-factorial, so it is not literally the same chirp sequence; its convolution executor is the same classical primitive. [CZT original paper, §§II–III](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/015_czt.pdf); [Bluestein, 1970](https://doi.org/10.1109/TAU.1970.1162132).

**Structured matrices.** De Sa et al. place Hankel matrices among established structured families with fast matvecs. Full ordinary matrix rank is compatible with low-complexity structured multiplication; it does not establish a general operation lower bound. [De Sa et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534155/).


## Verification boundary

Fresh controls verified 250 field/root cases through length 64, 357,748 coefficient entries, 750 complete coefficient matvecs, 1,198,912 odd-chart entries and 188 complete convolution matvecs, including every output at N=255 and 1023. They also checked 216 literal Green branch matrices and 216 normalized sector matrices, and 40 even-chart cases. The supplied large checks beyond N=1023 are not relabelled as independent full-output replays.

The included fresh checker reads the original Phase 20 source only as inert syntax for its cost audit. The original source itself was not imported or executed in this review. Field-root existence, root discovery, bit costs and numerical stability remain explicit extra obligations.
