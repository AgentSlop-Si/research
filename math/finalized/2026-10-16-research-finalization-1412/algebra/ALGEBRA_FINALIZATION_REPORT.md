# Three algebra continuations: bounded finalization and archival recommendations

Date: 16 October 2026. Repository baseline: `609d5c2189d64350bcbed447eead7e2c33dd3a50` in `AgentSlop-Si/research`.

## Results first

1. **ALG-057:** the exact arbitrary-jet packet-bank obstruction admits the stronger bound `A >= J S/2`, removing the old minor-selection penalty. Under the original assumptions this gives `A >= J N/128`, rather than `J N/256`. The rectangular-volume argument is an application of established bounded-coefficient linear-circuit theory. This closes the selected classical-volume comparison and exhausts attempts to obtain `o(Nn)` by rescheduling the same exposed arbitrary-jet interface.
2. **ALG-050:** the classical nullity theorem maps exactly to the source's inverse cut-rank identity. Its rational-degree, single-solve and scalar-port exclusions are complete at the stated scope. A complete rederivation below checks the singular-principal-block and arbitrary-endpoint qualifications. Repeating common-base low-degree fusion cannot cross the proved degree barrier.
3. **ALG-048:** the comparison with Ailon's 2013 two-register unitary theorem is a qualified model nonmatch. Global unitarity of a dense Green stage is not a certified two-register unitary implementation. The source's own fixed-strength norm obstruction uses `|alpha| Delta delta < 1`. Its immutable statement omits the absolute value once, but the native accepted review already corrects this; no fresh correction credit is claimed. The existing Haar replacement escapes that norm argument and remains a separate unsolved covariance construction.

**Disposition recommendation:** archive ALG-057's current arbitrary-jet mathematical continuation as `CLOSED`, with its proof, unchanged historical priority 34 and all model exclusions retained. Its named comparison is now complete, the frozen component has matched Theta(N log N) order, and the native scope supplies no selected unresolved construction inside that interface. The original-source/fused-inverse and changed-model alternatives remain unproved exclusions, not completed theorems. Keep ALG-048 and ALG-050 `TO RESEARCH` at priorities 42: ALG-048 explicitly selects a Fourier-covariant Haar/Green hierarchy, while ALG-050 also owns a separate scan/broadcast source not re-reviewed here. This is one bounded activity archival and two completed substages, not three whole mathematical theories solved. No mutation is made by this report.

No historical code was executed. No performance measurement, worldwide-priority result, unrestricted Fourier lower bound or new FFT is claimed. Existing finite control results are attributed to their source, not independently replayed here.

## Identity and provenance

All three records occur in the baseline open index with status `TO RESEARCH` and are not among its 83 closed views. Stable IDs, rather than row positions, are authoritative. The source workbook is [Research cycle](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit).

| Stable owner ID | Priority | Overview row | Catalogue row | novelty row |
|---|---:|---:|---:|---:|
| ALG-048 | 42 | 60 | 82 | 43 |
| ALG-050 | 42 | 62 | 84 | 45 |
| ALG-057 | 34 | 210 | 150 | 141 |

The exact paths, verified SHA-256 values, Git blob SHAs, baseline links and owner-row links are in `SOURCE_MANIFEST.json`. File-name hash prefixes were not substituted for hashes of recovered bytes: ALG-057's current body has SHA-256 `f8c8e8323458777c3b44e7925c837bf9e9d1fde4f6d64ed5350fecdf0331c10f`, while its archive file name begins `0c7ac6...`. The connector Git blob SHA matches the recovered bytes for all three sources.

The initial owner selection used the baseline export. A subsequent read of full CellData for Catalogue rows 82/84/150, novelty rows 43/45/141 and overview rows 60/62/210 confirmed these IDs/statuses/priorities and exposed broader owner context. ALG-048 already records the absolute-value guard and preserves a Haar/global-phase construction. ALG-050 also owns a separate scan/broadcast theorem and source, which this pass has not re-reviewed. ALG-057 preserves the constrained-original-source and fused-inverse gap. These findings require ALG-048 and ALG-050 to remain open. ALG-057's current arbitrary-jet continuation can be archived as an exhausted activity while its excluded alternatives remain explicitly unproved. The raw native preimages are not included in this publication. Any later application must again preserve intervening updates.

## 1. ALG-057: rectangular volume closes the remaining bounded comparison

### 1.1 Frozen interface

The source is `YOUNG_FEEDBACK_BATCH_OBSTRUCTION.md`, sections 1–8. Put `N=2^n`, `d=n-b`, `r=2^d`, `L=2^(b-1)` and assume `b>=7` and `L+b<=d`. A primitive complex N-th root is supplied. Every vector `u_j` is an independent, arbitrary complex r-vector. The required outputs are the actual scalar entries of

`g_k = sum_(t=1)^L C_t Q_r^t u_(k-b-t)`, with out-of-range inputs zero.

The allowed input-dependent gates are copying/permutation, binary addition or subtraction, and multiplication by a scalar of modulus at most one. The theorem charges additions. It remains valid when setup is free, originals remain available, and all inputs are known offline. It does not assume bounded intermediate magnitudes.

For age t, let `K_t` be the binary t-bit words beginning and ending in 1 and avoiding `0^b`; let `f_t(k)=rev_t(k)` and `R_t=2^(d-b-t)`. The source's row formula is

`(C_t Q_r^t u)_(2^(b+t)q+k) = omega^gamma(k) sum_(j=q mod R_t) eta^(j f_t(k)) u_j`,

where `eta=omega^(2^b)`. There are `m_t=R_t |K_t|` rows, each supported on `2^(b+t)` columns.

These routed indices have pairwise disjoint age supports. In the fixed d-bit word for an index, the rightmost completed block of b zero bits has exactly the age t: it is followed by k, which begins with 1 and contains no such block. Thus for `J=n-b-L+1`, selecting already-requested outputs gives J separate copies of the same row bank B, acting on `u_0,...,u_(J-1)`. This selection is only an analysis of existing outputs, not a new free encoded output interface.

### 1.2 Orthogonality checked directly

Rows with the same t and distinct q have disjoint input supports. At equal t and q but distinct k, their inner product is a complete geometric sum with a nonzero frequency difference modulo `2^(b+t)`, hence vanishes.

For `t<t'`, intersecting supports give the geometric sum over `2^(b+t)` terms with frequency difference `f_t(k)-f_t'(k')`. A nonzero inner product requires

`f_t'(k') = f_t(k) mod 2^(b+t)`.

If `t'<t+b`, this fails because `f_t'(k')` has bit `t'-1` equal to 1, whereas `f_t(k)<2^t`, and both integers lie below the modulus. If `t'>=t+b`, it forces a block of b zero bits into k' immediately after its initial t bits, contrary to the definition of K_t'. The equality case is included. Unit row phases do not affect this argument. Consequently

`B B* = diag(2^(b+t), repeated m_t times)`.

Write `m=sum_t m_t` and `S=sum_t (b+t)m_t`. Then `det(B B*)=2^S` and the selected J-bank output matrix has Gram determinant `2^(JS)`.

### 1.3 Sharper volume lemma, with proof

Let a linear circuit start with D independent input-coordinate forms, and let q be any integer from 1 to D. For a q-tuple of available coefficient rows, define its volume to be the Euclidean norm of their exterior product, equivalently the square root of their Gram determinant. Let V be the maximum of this volume over available q-tuples. Initially `V=1`, because coordinate q-tuples are orthonormal and repeated coordinates give zero.

A copy or permutation cannot enlarge V. Replacing or appending a scalar multiple of one available form, with scalar modulus at most one, cannot enlarge it. If a new form is `a+b`, any q-tuple containing it has exterior product equal to the sum of the two exterior products obtained by substitution of a or b. Each summand has norm at most the preceding V (or is zero when rows repeat). By the triangle inequality the new maximum is at most `2V`. The same proof handles subtraction and two-parent gates with coefficients bounded by one.

After A additions, every available q-row output volume is therefore at most `2^A`. Apply this with `q=Jm` and `D=r(n+1)` to the selected J-bank output matrix. Its volume is `2^(JS/2)`. Thus

**`A >= J S/2`.**

This avoids both choosing an m-column minor and adjoining complementary coordinate rows. In particular, the factor `binom(r,m)` in the historical proof is unnecessary. The earlier weaker bound remains correct.

For completeness, a multiplier of arbitrary modulus c increases this potential by at most `max(1,|c|)`. The same argument yields the necessary budget

`A + sum log2 max(1,|c|) >= J S/2`.

This is not a construction, and does not make large scalars free.

### 1.4 All terminal partial banks and the exact available-volume budget

The J complete banks are sufficient, but some final input vectors also expose partial banks. An age-t packet from u_j appears exactly when `0<=j<=n-b-t`, because its output time is `j+b+t`. Within a fixed input block, all available ages remain mutually orthogonal; distinct input blocks use independent coordinates. Selecting every such requested packet row therefore gives the stronger bound

**`A >= (1/2) sum_(t=1)^L (n-b-t+1)(b+t)m_t >= JS/2`.**

This follows from the identical volume potential: each age-t row norm contributes `(b+t)/2` to log-volume in each of its `n-b-t+1` occurrences. It is a classical-tool substitution, not a claim of an optimal exact circuit bound.

### 1.5 Explicit asymptotic consequence and matching order

For `2<=t<=L`, a union bound for a b-zero run among t−2 free bits gives `|K_t| >= 2^(t-3)`. Hence `m_t >= r/(16L)` and

`S/2 >= r/(32L) sum_(t=2)^L t >= rL/64`.

Since `rL=N/2`, the improved result is **`A >= JN/128`**. At the source's marker choice `b=floor(log2(n/(4 ln n)))`, one has `L=o(n)`, `b=o(n)` and `J=(1-o(1))n`; the exact arbitrary-jet component therefore needs `Omega(Nn)` additions. The source's paid trajectory schedule performs `O(rnL+rn+N+n)=O(Nn)` operations, so the asymptotic order is already matched in this interface. Reducing constants is not an asymptotic escape.

### 1.6 Primary-theorem mapping and decision

[Bürgisser–Lotz, arXiv:cs/0301016v1](https://arxiv.org/pdf/cs/0301016v1), section 2.1 and section 3 equation (2), supplies the classical rectangular row-volume lower-bound framework. Their circuit size counts additions and bounded scalar multiplications, with scalar bound 2. Here the unit-bounded model permits a stronger additions-only accounting: scalar gates do not increase the chosen volume. The matrix is the selected block-diagonal packet bank; its row-volume is exactly `2^(JS/2)`. No Fourier-normalization or extra-input substitution is needed. This is an exact methodological match, not an attribution of the source's specific marker-word construction to that paper. The elementary proof above makes the narrower gate accounting explicit.

**Close the named comparison and stop further rescheduling/cache/convolution attempts that keep this same arbitrary-jet, bounded-coefficient, explicitly exposed-output interface. Archive only this current arbitrary-jet research activity under ALG-057, preserving its recorded original-source/fused-inverse gap. The fresh native owner presents those alternatives as exclusions and supplies no selected successor solver inside the frozen interface.** Preserve the source's separate alternatives: constrained source-generated jets, fused source/solve outputs, changed gates, or a paid finite-field construction. Source-generated jets have only N independent inputs and cannot be silently replaced by these arbitrary independent vectors. No assertion about the unresolved alternatives is made.

## 2. ALG-050: common-base rational fusion is bounded by cut rank

### 2.1 Frozen statement and primary match

The source is `PROOF.md`, sections 1–6. Let `qsep(X)` be the largest rank of either off-diagonal block across any prefix/suffix split in one fixed order. Let `beta_N=floor(N^2/4)/N`.

[Vandebril–Van Barel, The nullity theorem](https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/nullity/node3.html), Corollary 2, states the complementary off-diagonal inverse rank identity. Taking a prefix I and its complement J gives exactly `rank(A^-1[I,J])=rank(A[I,J])`. Its proof uses invertibility of the full A, not invertibility of principal blocks. The displayed source uses real matrices; the kernel proof below works over any field, including C. This is an exact algebraic-tool match. It is not an algorithmic runtime theorem, and it does not itself supply the Fourier-specific rank estimate or the whole rational-degree application. The PDF route failed in this pass; the authors' complete HTML statement and proof were readable.

### 2.2 Complete rank derivation

For an invertible A, `z` in `ker(A^-1[I,J])` corresponds to the unique w satisfying `A^-1(0,z)=(0,w)`. Then `A[I,J]w=0` and `z=A[J,J]w`. Conversely every w in `ker(A[I,J])` yields this z, and the map is injective because A is invertible. Both kernels have ambient dimension |J|, so their nullities, hence ranks, agree. Exchanging I,J proves `qsep(A^-1)=qsep(A)` without Schur-complement assumptions.

Block multiplication gives `qsep(XY)<=qsep(X)+qsep(Y)`. Addition is subadditive, and adding a scalar identity does not change off-diagonal blocks.

Suppose `qsep(T)<=h`, `q(T)` is invertible and `p/q` is reduced of degree `d=max(deg p,deg q)`. Over a splitting field, partial fractions express p/q as its polynomial part plus groups at poles. A pole of multiplicity a contributes a polynomial of degree a in `(T-lambda I)^-1` with zero constant term. Horner's rule and the product bound give qsep at most ah. The polynomial part has order at most `h max(deg p-deg q,0)`. Summing pole multiplicities gives

**`qsep(p(T)q(T)^-1) <= hd`.**

This partial-fraction calculation proves rank only; it supplies no free roots, coefficients or implementation.

For normalized Fourier F, every physical s-by-t submatrix has squared Frobenius norm st/N and operator norm at most 1. Thus its rank is at least st/N. Independent row/column permutations and nonzero row/column scalings preserve rank. Therefore any X transformed to F by arbitrary nonsingular endpoint monomials satisfies `qsep(X)>=beta_N`. The norm estimate is applied to F before arbitrary scaling, not to scaled entries. It works at composite N without a full-spark assumption. Combining gives **`hd>=beta_N`**.

For the common weighted unitary cycle M, each cut has one directed crossing edge each way, so `qsep(M)=1`. Because `M*=M^-1`, every admitted factor `K(lambda M)^(+/-1)` or `K(lambda M*)^(+/-1)`, with `K(X)=(2I-X)(I-X)^-1`, is rational of numerator/denominator degree at most one in M. A defined t-factor product therefore has degree at most t. Exact endpoint-equivalent Fourier requires **`t>=ceil(beta_N)`**, even after algebraic cancellation. This conclusion requires one common M; arbitrary internal shuffles do not preserve that premise.

For one solve `L A^-1 R` in a common order, if each matrix X has half-bandwidth b_X plus a rank-r_X correction, then `qsep(X)<=b_X+r_X`. Hence exact Fourier endpoint-equivalence requires

**`(b_A+r_A)+(b_L+r_L)+(b_R+r_R)>=beta_N`.**

If an m-coordinate auxiliary solve has `qsep(A)<=h`, with N inputs injected into distinct single-coordinate ports and N outputs read at distinct single-coordinate ports, choose a prefix containing exactly `a=floor(N/2)` input ports. If it contains b output ports, the two transfer cross-block dimensions are `b by (N-a)` and `(N-b) by a`. Their ranks are at most h and at least their dimension products divided by N. Thus `h>=max(b(N-a),(N-b)a)/N>=beta_N`, independently of the auxiliary dimension. Dense encoders/readouts and nonlocal feedthrough do not satisfy these port hypotheses.

### 2.3 Why the existing continuation can stop

The source already provides the degree-(N−1) signed-cycle chirp representation of Fourier. Its antiperiodic coefficients and diagonal phases give exact Fourier entries, so the unrestricted common-cycle rational class has required degree `Theta(N)`, up to constants. This is a representation barrier and a classical chirp realization, not a new fast evaluator. A long half-cycle word is another source example with an O(N) evaluator, proving that large degree or cut rank alone is not an arithmetic lower bound.

**Close the named nullity comparison and stop repeated bounded-degree/common-order scalar-port fusion attempts without a changed premise. Keep the whole ALG-050 owner open: the fresh native scope additionally includes the separate scan/broadcast theorem and source, which this pass did not review.** Preserve the genuinely different problems: fast application at growing degree, changing geometry/order, nonlocal ports, special fast high-width solvers, exact bit/precision costs and production implementation. None is solved or ruled out by this report.

## 3. ALG-048: fixed-strength norm budget and the exact escape boundary

### 3.1 Corrected condition and complete argument

The source's section 1 writes `alpha Delta delta<1` once, but its displayed bound and proof use `|alpha|`. The sufficient hypothesis is **`|alpha| Delta delta<1`**, where `delta=2/p−1` and `1<p<2`. It is required also for negative alpha. The native accepted review already states this corrected condition and explicitly rejects the signed-only premise. This report preserves that correction; it does not count it as new progress. The recorded positive-strength applications are unaffected.

For a real symmetric adjacency matrix A of maximum degree Delta, `exp(itA)` is unitary on l2 and has l1 norm at most `exp(|t| Delta)` by the power series. Finite-dimensional complex interpolation gives l_p norm at most `exp(|t| Delta delta)`. The resolvent integral

`(I−i alpha A)^−1 = integral_0^infinity exp(−s) exp(i alpha s A) ds`

therefore has l_p norm at most `(1−|alpha| Delta delta)^−1`. Since the Cayley transform is `C_alpha(A)=2(I−i alpha A)^−1−I`, its l_p norm is at most `1+2/(1−|alpha| Delta delta)`. The inverse is covered by −alpha.

For uniformly bounded strengths, degrees and number of Cayleys per stage, select one p sufficiently close to 2. Every stage then has norm at most a constant K independent of N. Coordinate permutations and unit-modulus diagonal phases are l_p isometries. A t-stage product has norm at most `K^t`, whereas a normalized Fourier column has l_p norm `N^(1/p−1/2)`. Exact Fourier therefore requires `t>=((1/p−1/2) ln N)/ln K` when K>1; if K=1 it is impossible for N>1. This is only a stage-count theorem. It does not lower-bound arbitrary fused execution cost.

For the source's fixed numerical parameters, `p=9/5`, path strength 1/32, tree strength 2 and epsilon 1/512, the source's bound is

`K=(17/15)^(2/9)(1+7/512)/sqrt(1+512^(-2))`,

giving `t>=ln N/(18 ln K)`. No rescheduling of the same factors changes this norm budget.

### 3.2 Preserve the existing Haar escape

The source replaces the tree mixer with Haar synthesis H on `m=N/2` entries, whose first column is `m^(-1/2)` times the all-ones vector. For `R_H=[[0,H],[H*,0]]` and `V_H=(I+i epsilon R_H)/sqrt(1+epsilon^2)`, the basis input in that Haar-scaling coordinate satisfies

`||V_H e||_p >= epsilon m^(1/p−1/2)/sqrt(1+epsilon^2)`.

The path factors and their inverses have uniformly bounded l_p norms; thus the full Haar stage also has norm growing as `N^(1/p−1/2)` for every fixed p<2. It is outside the constant-K premise. This refutes any attempt to extend the old norm obstruction to that replacement. It proves neither Fourier covariance nor a cheap Fourier factorization.

For covariance `E(A)=AZ−DA`, an additive correction E has `rank(EZ−DE)<=2 rank(E)`. Therefore any correction making covariance exact must have `rank(E)>=rank(E(A))/2`. Only the source's sampled specific defects were asserted full rank; no new all-N defect theorem or replay of those samples is claimed here.

### 3.3 Primary-theorem comparison and decision

[Ailon, arXiv:1305.4745](https://arxiv.org/pdf/1305.4745), section 2 and Theorem 2.1, proves an `N log2(N)/2` lower bound for sequential two-coordinate unitary gates with exactly N current coordinates. ALG-048's dense Cayley stage is globally unitary but implemented through a solve; the source supplies no decomposition into those gates with certified total count and workspace. The endpoint target is compatible, but primitive, intermediate-state and cost units are not. A count of dense stages cannot be substituted for Ailon's scalar-gate count. Therefore the named comparison is a qualified nonmatch; conditional application would require a paid implementation meeting every gate and live-state premise. It does not certify the source's original execution model or prohibit the Haar replacement.

**Close this named comparison and the repeated fixed-strength norm-budget substage; keep ALG-048 open.** Source section 6 expressly selects a uniform Fourier-covariant Haar/Green hierarchy, and its mathematical value has not been exhausted here. Preserve that selected successor, growing strengths/degrees, changed gates, arbitrary-magnitude internal diagonals, fresh amplitudes and explicitly paid fused execution. The fixed-strength result is not a reason to close the whole owner.

## 4. Proposed owner wording and application boundary

Use the stable owners and scopes in `PROPOSED_OWNER_DISPOSITIONS.json`. That file supplies current-action and pass/stop prefixes, completed-substage reasons and preserved unresolved scopes. It is not a write receipt. ALG-048 and ALG-050 remain `TO RESEARCH`. ALG-057 is recommended `CLOSED` as an activity archive, not a proof of its excluded alternatives. Numeric priorities and row positions are unchanged; ALG-057's priority becomes historical/inactive. All original proofs, finite controls, source histories and rejected approaches stay available.

An independent reviewer should verify the volume improvement, source binding and owner scope before applying even these bounded progress updates. ALG-057's activity archival follows the fresh native scope and the independently checked completed-comparison/matched-order reason above. ALG-050 whole-owner archival remains unsupported without its other source scope being assessed. No new continuation is selected; ALG-048's already-selected successor is preserved.
