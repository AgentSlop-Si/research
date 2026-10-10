# Independent audit: selected-convolution source routing and fractional-shift gates

Date: 2026-10-10. Verdict: **accepted within the explicitly stated models**.

The final target is `selected_convolution_escape_0544/RESEARCH_REPORT.md`; an exact inspected copy is included here as `INSPECTED_REPORT.md`, with source hashes in `INPUT_REPORTS.sha256`. This audit accepts the local-encoder rank theorem, its conditional ordinary-FFT cost consequence, the Cauchy structure of a pushed-through twiddle, and the qualified root-interface comparison. It does not establish a faster selected convolution, a universal FFT lower bound, a novel classical matrix theorem, a complete literature review, or verification of an external formal build.

One cost-language qualification was requested and incorporated before acceptance: the enumerative `O(Q K^3)` header preparation gives the stated matching `O(N log N)` total automatically at the accepted asymptotic parameter choice. For other finite parameter triples, the target now explicitly invokes the predecessor's `O(N+n)` two-trie mask construction as the fallback. No mathematical correction to the principal proofs was required.

## 1. Audited hypotheses and parameter edges

The marker construction has `N=2^n`, `b>=7`, `L=2^(b-1)`, and `n>=L+2b`. Its selected full-depth marker with `t=k=1` has bit prefix `0^b 1 0^b`. Hence the selected frequency set `E` contains

    I={c,...,c+M-1}, c=2^(n-b-1), M=2^(n-2b-1).

The hypotheses give `n>=2b+1`, so `M` is an integer at least one. Moreover `c/M=2^b` and `(c+M)/N=2^(-b-1)+2^(-2b-1)<1`, so the displayed interval does not wrap. Nothing in the rank arguments needs a density estimate.

The blocked construction uses `K=min(n,2L+2b)`, `Q=2^K`, `B=2^(n-K)` and `E={Bv+u:v in A,0<=u<B}` with nonempty `A`. The following conditions have distinct roles:

- The one-header rank argument gives `r>=Q` when `B>=Q`, equivalently `n>=2K`.
- The arbitrary-source-block theorem applies to size-`Q` blocks whenever `Q<=M`, equivalently `K<=n-2b-1`.
- The target's explicit sufficient condition `n>=4L+4b` gives `K=2L+2b<n`, both inequalities above, and positive `log B`.
- The base hypotheses alone do not imply this range. For example, `b=7`, `L=64`, `n=78` is legal but gives `K=n`, `B=1`, `Q=N`.
- With `b=floor(log2(n/(4 ln n)))`, one has `L=Theta(n/ln n)` and `b=O(log n)`, so the sufficient condition holds eventually. Finite exceptions are not silently included in the asymptotic cost lower bound.

For a field containing a primitive `N`th root `omega`, its characteristic cannot divide `N`. Thus `B` is nonzero and invertible in the field, as required by Fourier inversion. All rank claims survive nonzero Fourier normalizations and chirp diagonals. The field-independent algebra does not assert conditioning or numerical rank.

## 2. Independent proof of the arbitrary-source rank gate

Let `S={s_1,...,s_d}` be distinct residues modulo `N`, with `d<=M`. In the rows `c,...,c+d-1`, divide column `j` by `omega^(c s_j)`. This yields the Vandermonde matrix with entries `(omega^s_j)^i`, `0<=i<d`. Primitive-root order makes the nodes pairwise distinct, so its determinant is nonzero. The `E`-row matrix therefore has rank exactly `d` on those columns.

This proof also permits a cyclic consecutive row interval: replacing a row exponent by its residue modulo `N` leaves each entry unchanged. The empty-column case is trivial. The proof needs distinct source coordinates and at least `d` consecutive rows; it does not claim all minors of a composite Fourier matrix are nonzero. The rank-one example with `N=8`, rows `{0,2}`, columns `{0,4}` confirms the distinction.

Now partition all sources into disjoint blocks `S_j` of sizes `d_j<=M`. Suppose the only input-dependent state crossing a cut is `P_j x|S_j` for each block, with `P_j` having `r_j` rows and input-independent coefficients. Originals are discarded, and no reread, bypass, earlier output tape, or additional source-dependent register is available downstream. If the subsequent computation is a fixed linear map, the target restricted to `S_j` factors as `R_j P_j`. The left side has rank `d_j`; hence `rank(P_j)=d_j` and `r_j>=d_j`.

Allowing different dense encoders for each block, arbitrary constants, and arbitrary global linear output recombination does not weaken this argument. The total retained dimension is at least `N` if all blocks' summaries are simultaneously present. This is a statement about a cut and retained information, not a universal memory or arithmetic lower bound. Nonlocal preprocessing and later access to originals are outside the interface.

## 3. Stream fusion: information bound versus operation count

Write `s=a+Qj`, `0<=a<Q`, `0<=j<B`. The proposed local fusion has

    z_rho[j]=sum_a P_j[rho,a] x[a+Qj], 0<=rho<r.

Each fixed `j` is a consecutive source block of size `Q`. Under `Q<=M`, Section 2 immediately forces `r>=Q`.

There are two useful independent checks on this conclusion:

1. Choose one header `v in A`. On its `B` rows, the map from the fixed source block has entries `omega^((Bv+u)(a+Qj))`. Removing nonzero row and column factors leaves `omega^(ua)`, of rank `min(B,Q)`. Thus a single header gives `r>=min(B,Q)`, with `r>=Q` precisely when `B>=Q`.
2. Because the actual source block is consecutive, arbitrary distinct rows in `E` give a Vandermonde matrix in nodes `omega^ell`. Its rank is `min(|E|,Q)`. This proves the target's stronger finite statement `r>=min(|E|,Q)` even outside the sufficient asymptotic range. It does not license the same bound for every arbitrary nonconsecutive source set larger than `M`.

Rank alone stops here. If, additionally, the implementation applies a separate complete ordinary radix-2 transform to each of the `r` streams, that chosen stage contains exactly `r B log2(B)/2` butterflies. Under `r>=Q`, this is at least `N(n-K)/2`. Since `K=o(n)` at the accepted marker choice, it is `Omega(N log N)` with constant-cost butterfly arithmetic and charged scalar traffic.

This is not a lower bound on optimized batch transforms, nonlocal linear circuits, or every algorithm that happens to keep `Q` independent streams. A circuit can preserve all source dimensions and still share arithmetic. The target explicitly retains this boundary. When `B=1`, the butterfly count is zero and cannot establish any logarithmic lower bound.

The matching baseline uses `Nn/2` butterflies across its long and short stages, charged twiddles/routing/root preparation, selection, and mask preparation. The final report correctly qualifies the `O(QK^3)` enumeration asymptotically and names a linear-mask fallback for other finite triples. Optional packet-bank regeneration costs the separately paid `O(NL)`.

## 4. Independent derivation of the fractional-shift matrix

Let `zeta=omega^Q` and `F_B[u,j]=zeta^(uj)`. For integer `a`, define `D_a[u,u]=omega^(au)` and `K_a=F_B^(-1)D_aF_B`. Fourier inversion gives

    K_a[j,k]=(1/B) sum_(u=0)^(B-1) (omega^a zeta^(k-j))^u.

If `Q` does not divide `a`, the geometric ratio is never one: that would require `a+Q(k-j)=0 modulo N`, and hence `Q|a`. Its `B`th power is `omega^(aB)`, also not one. Therefore

    K_a[j,k]=(1-omega^(aB))/(B(1-omega^a zeta^(k-j))).

Set `X_j=zeta^j`, `Y_k=omega^a zeta^k`. Each node set has `B` distinct elements; they are disjoint by the same congruence argument. Consequently `K_a` is a nonzero scalar times the row-scaled Cauchy matrix `X_j/(X_j-Y_k)`.

For any `d` selected rows and columns, a null column combination would give a rational function `sum_k c_k/(X-Y_k)` vanishing at `d` distinct `X_j`. Multiplication by the `d` denominator factors gives a polynomial of degree at most `d-1` with `d` roots, so it is zero. Evaluation at each selected `Y_k` then forces `c_k=0`. Every square minor is nonsingular.

The following consequences are valid and precisely limited:

- Every entry is nonzero, so its ordinary circulant convolution kernel uses every cyclic offset.
- Every rectangular submatrix has rank equal to its smaller side. In particular, a balanced off-diagonal cut has rank `floor(B/2)`. Independent row/column permutations and nonzero endpoint scalings preserve this total nonsingularity. Exact uniformly bounded quasiseparable ranks cannot describe this one operator as `B` grows.
- Conjugation gives `K_a K_c=K_(a+c)` and `K_a^(-1)=K_(-a)`. When `Q` does not divide `a`, the inverse is dense too. If `K_a=P T^(-1)R` for invertible monomial `P,R`, then `T=R K_(-a)P` has every entry nonzero. Thus a representation of this specific form cannot have a genuinely sparse `T`.
- For `a=Qm`, the geometric-series quotient is inapplicable and `K_a x[j]=x[j-m modulo B]`; in particular `K_0=I` and `K_Q x[j]=x[j-1]`. For `Q=1`, no integer `a` satisfies the nonintegral hypothesis. For `B=1`, the sole nonzero entry satisfies the theorem but the balanced-cut lower bound is vacuous.

These facts do not rule out fast Cauchy multiplication, short factorizations using more general endpoints, sums or products of sparse inverses, or approximate low-rank representations. Over the complex numbers the full `K_a` is unitary; exact rank of its subblocks does not imply a lower bound on their smallest singular values. Direct application by two complete `B`-point FFTs costs `O(B log B)`. Preparing its circulant row costs `O(B)` once `omega^a` is available, with the final target explicitly charging extraction if it is not already tabled. Preparation is not application.

## 5. External theorem and the additional root resource

The live official [publication README](https://github.com/openai/math/blob/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/README.md) identifies OpenAI and September 25, 2026. The official [introduction](https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/introduction.tex) states an all-length exact DFT bound `O(N(log N)^(1-10^-13))`, with unrestricted complex coefficients, one supplied polynomial-order root, charged preparation and indexing, and no bit-complexity or numerical-stability claim. This is an external stated result; the local restricted gates cannot be presented as a universal obstruction to it.

The official [scope note](https://raw.githubusercontent.com/openai/math/main/lean/docs/130.md) separately describes subsequential and uniform formal statements. The included challenge file has placeholder proofs and the configured solution module has theorem bodies; these are different files with different roles. Neither their presence nor this static reading establishes a successful Lean build. No dependency execution, compilation, comparator run, or full external proof audit was performed.

### Additional hypothesis needed for the import guard

Merely saying that the ambient scalar field contains `omega` is insufficient to restrict constants to its cyclotomic subfield. The target correctly adds the stronger hypothesis that the initially available constants are rational numbers, `omega`, and `1/sqrt(2)`, with all others produced by field operations. For `N=2^n`, `n>=3`, the generated field is contained in `K_0=Q(zeta_N)`; the normalizer already belongs to `Q(zeta_8)`. Any primitive choice of `omega` generates the same cyclotomic field.

For an odd integer `R`, coprimality implies `Q(zeta_N,zeta_R)=Q(zeta_(NR))`. Since `N` divides `NR`, the degree ratio is

    [K_0(zeta_R):K_0]=phi(NR)/phi(N)=phi(R).

Thus an odd root of order at least three cannot be generated from those initial constants by field operations alone. This is a constant-resource restriction, not an impossibility of extension-field simulation or of a different base-field algorithm.

### Quantitative check of the target's bound

The official [all-lengths section](https://raw.githubusercontent.com/openai/math/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex) uses `R` equal to the largest initial odd primorial not exceeding `2N`; writes `W=R 2^e` with minimal `e` making `W>=2N`; and specifies `D=(2N)W 2^ceil(log2(16W))`. The latter is below `1024N^3`. This audit checks the following arithmetic independently.

Let `ell` be the number of primes in `R`, and `p_next` the first omitted prime. Maximality gives `R>2N/p_next`. Since the `j`th odd prime satisfies `p_j>=j+2`,

    R/phi(R)=product_j p_j/(p_j-1)
            <=product_j (j+2)/(j+1)=(ell+2)/2.

Therefore `phi(R)>=2R/(ell+2)>4N/((ell+2)p_next)`.

The estimate `ell=O(log N)` follows directly from `R>=3^ell`. The elementary prime bound used in the primary source is sound: central-binomial estimates give `4^u/(2u+1)<=binomial(2u,u)<=(2u)^pi(2u)`. For each prime, its exponent in that binomial coefficient is at most `floor(log_p(2u))`, which proves the upper estimate. With `u=(j+1)^2`, taking logarithms forces `pi(2u)>j+1` for all sufficiently large `j`; thus `p_j=O((j+1)^2)`. Hence `p_next=O((log N)^2)` and the target's conservative `phi(R)=Omega(N/(log N)^3)` follows. No prime number theorem is needed.

Finally write `D=2^s R`. Here `s>=n`, so `N|D`. The exact relative degree is

    phi(D)/phi(N)=2^(s-n) phi(R).

This formula is correct for the displayed master root, but that root order need not be minimal for an algorithm. A generic extension-field basis would have the indicated dimension; there is no justified universal degree-times-runtime lower bound. The target makes no such claim. If a master root is explicitly supplied in the model, this particular import guard disappears.

## 6. Evidence, independence, and preservation

The target report, source ledger, earlier construction, and relevant primary-source text were read as inert text. No supplied Python program, Lean file, build script, or dependency was executed, imported, compiled, or AST-parsed. The independently written `audit_controls.py` loads no target code or data. It uses a different finite field, `GF(97)`, with verified primitive root orders, and performs:

- 56,508 consecutive-row/arbitrary-column rank checks, including empty source sets and wrapped row intervals;
- 321 local-channel rank checks across all coordinate blocks and headers of the small tested factorizations, including `B<Q`, `B=1`, and `Q=1`;
- 198 direct Fourier-kernel versus rational-Cauchy comparisons, with negative and positive `a`;
- 1,892 exhaustive small Cauchy-minor rank checks;
- 63 exceptional-shift, negative-minor, and finite-parameter boundary checks;
- 14 working-length, totient-bound, and exact cyclotomic-degree arithmetic cases.

All controls passed, and an independent rerun produced byte-identical JSON. The controls corroborate algebra and edge handling; they do not prove marker density, characteristic-zero conditioning, asymptotic complexity, or a formal theorem.

The author's final SHA-256 manifest was independently checked successfully. The final inspected report and primary snapshots are preserved in this audit directory. `INPUT_REPORTS.sha256` identifies the exact external target reports. `SHA256SUMS.txt` seals this audit package; its verification log is separate from the manifest to avoid self-reference. No central registry, checkpoint, or master research file was changed.

## Final acceptance boundary

Accepted: a source-local lossless-encoding rank barrier; an ordinary-separate-FFT architecture cost barrier; total nonsingularity, dense inverse, and exact off-diagonal-rank facts for the nonintegral fractional shift; and the explicitly additional minimal-root import guard. Rejected as inferences: a universal Fourier/Cauchy arithmetic lower bound, any practical approximation barrier, an external theorem refutation, a verified Lean build, a novelty conclusion, or a new fast transform.
