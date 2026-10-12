Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, source identity and limitations are retained. Original source-report SHA-256: 7c8ae712b5f51e09ed17689eec201baaeb125e9972dd4dd2fabdae21f5b4e1aa.

# HERO0 Phase26: independent common-bipartition audit

## Bounded verdict

**ACCEPT_RESTRICTED_EXTENSION.** The candidate proves all-row exact infeasibility for the stated independently fiber-ordered, common-bipartition subclass at every integer side `s >= 4`, over every field containing a primitive `s²`-th root. Its separate complex approximation lower bound is correct and tends to `1/sqrt(2)` in relative Frobenius error and normalized spectral error. No mathematical correction is required for these statements.

The verdict applies only to one scalar-weighted Green inverse plus an arbitrary diagonal per horizontal fiber, in exactly two mixed-axis stages, with both stages preserving the specified common cut. The candidate does not exclude arbitrary fiber-dependent interleavings, growing horizontal term counts, deeper networks, or general Fourier algorithms. It does not establish an FFT construction, speedup, optimal approximation constant, publication priority, or a new discovery count.

Review date: 2026-10-12 UTC. Neither candidate Python nor any original uploaded program was imported or executed.

## Exact input and original grammar

Reviewed archive:

`HERO0_Phase26_Fiber_Dependent_Common_Bipartition_CANDIDATE_2026-10-12.zip`

SHA-256: `85dcf7a984e4a3baf5ffaf6bd0aea5cec482719ff546b0c151556a25fdeabe70`.

All 19 listed candidate members match their lengths and hashes. The manifest accounts for every member other than itself. All five source bindings match. The original archive SHA-256 is `c790508658a55ca935f694451f7927a5da7d8acdefcb6371100569f49e54ebee`; all 13 entries in its inner SHA256SUMS agree. The separately copied original THEOREMS.md is byte-identical to the archive member and has SHA-256 `872d5cc65d9dec4a0b09760309ca95964fe289f031f2510cc1f12ba66603dfd8`. The original accepted review has SHA-256 `d72f4e6fa390f39e7365ef26ee8ef703ade3f3cb5ddf520bb2a42ce3d9a51a8c`.

The original theorem and its accepted review were read. The source architecture is

`T = (Y_H + Y_V)(X_H + X_V)`,

with horizontal operators preserving the second digit and vertical operators preserving the first digit. The source's fixed-template obstruction allows a fixed collection of `q` global horizontal orders and bounded horizontal Green term counts. Its stronger norm barrier tending to one requires a single global order, up to reversal, across both stages and all fibers. The source finite-field rank-one helper requires separately verified rank-one cuts in both horizontal stages.

The new candidate removes the bounded-template requirement but imposes a named common cut. It is a restricted extension into fiber-dependent order choices, not a superset of all prior fixed-template instances and not a result on all independent-order networks. At `s >= 6`, the number `floor(s/2)! ceil(s/2)! / 2` of permitted directed cycles modulo reversal is at least `2s`. Distinct orders can therefore be assigned to all `2s` horizontal fibers, with no constant template budget along an unbounded sequence. This does not create a common fine sibling tree, and the old asymptotic `1-o(1)` norm barrier is not used anywhere in this review.

## Independent proof audit

### 1. Endpoints and field

The endpoint labels stay `j=sa+b`, `k=sx+y`. With `eta` of exact order `s²` and `omega=eta^s`, the target is

`eta^((sx+y)(sa+b)) = eta^(yb) omega^(xb+ya)`.

There is no input/output permutation, digit transpose, hidden Fourier block, or implicit-output convention. Internal cycle orders are wiring choices rather than endpoint relabelings. The existence of a primitive `s²`-th root forces the field characteristic not to divide `s`. The exact proof uses only linear algebra and multiplicative root orders, not inner products, positivity, or complex-only rank assumptions.

### 2. Both cut ranks, including zero weights

Set `u=floor(s/2)`, `X={0,...,u-1}`, `A={u,...,s-1}`. Rotate a permitted cycle to

`x_0,...,x_(u-1),a_0,...,a_(v-1)`.

For `P e_z=w_z e_next(z)`, `P^s=WI`, where `W` is the product of all edges. If `W != 1`,

`G=(I-P)^(-1)=(I+P+...+P^(s-1))/(1-W)`.

Conversely `W=1` means every edge is nonzero and the recurrence around the cycle constructs a nonzero vector fixed by `P`, so the inverse is singular. Thus the stated admissibility condition is exact.

For the cut from `A` to `X`,

`G[x_i,a_j]=(prod_(t=j)^(v-1) w_at)(prod_(t=0)^(i-1) w_xt)/(1-W)`.

For the opposite cut,

`G[a_j,x_i]=(prod_(t=i)^(u-1) w_xt)(prod_(t=0)^(j-1) w_at)/(1-W)`.

Each expression is an outer product with one common nonzero denominator. No individual edge is inverted. Empty products are one. Consequently both cut ranks are at most one even if edges vanish; they may be zero. Reversal simply gives another two-run cycle. A scalar multiple preserves the upper bound and a diagonal has zero entries on these disjoint cuts. This proves all required cut bounds independently for every fiber in both stages. It does not infer the second-stage condition from the first.

### 3. All-row obstruction and algebraic mode capacity

On an off-axis block with `y != b` and rows/columns in disjoint `X,A`, the HH and VV paths vanish. Direct expansion gives

`T[X,A]^(yb)=H_y diag(v^(yb)) + diag(u^(yb)) G_b`,

where `H_y=Y_H^(y)[X,A]` and `G_b=X_H^(b)[X,A]`. The vertical values may be treated as completely independent. This enlarges the completion class and therefore strengthens an impossibility conclusion.

The Fourier block is `eta^(yb) f_b g_y^T`, with `f_b[x]=omega^(bx)` and `g_y[a]=omega^(ya)`. If `f_b` is not in `col(H_y)` and `g_y` is not in `row(G_b)^T`, elementary finite-dimensional separation provides `l,r` with

`l^T H_y=0`, `G_b r=0`, `l^T f_b != 0`, `g_y^T r != 0`.

Every vertical-completion coefficient pairs to zero with `l,r`; the target pairing is `eta^(yb)(l^T f_b)(g_y^T r) != 0`. This is a necessary compatibility dichotomy, not a claimed sufficient factorization test.

Each of `X,A` has at least two consecutive integers. Two restricted Fourier modes on either set can be proportional only if their ratios on those consecutive coordinates agree, forcing `omega^b=omega^c` and hence `b=c mod s`. A rank-one line contains at most one mode; a rank-zero space contains none. This is valid over every stated field, including non-prime finite fields. There is no finite-field tight-frame or arbitrary-minor full-spark assumption.

For each fixed `y`, the first lock covers at most one `b`; all such locks cover at most `s` pairs. For each fixed `b`, the second covers at most one `y`; all such locks cover at most another `s` pairs. Counting possible overlap twice only weakens the upper bound. Complete Fourier equality requires `s(s-1)` off-axis pairs, and

`s(s-1) > 2s` for every `s >= 4`.

Thus for every allowed horizontal choice, at least one required pair has a nonzero separating target functional and no vertical completion. A single such block precludes equality of the entire natural-order matrix and hence computation for every input. This is an all-size, all-weights proof, not extrapolation from finite witnesses. No conclusion at sides 2 or 3 is asserted.

### 4. Separate complex norm proof

This paragraph alone uses `K=C` and a unit-modulus primitive root. On one oriented cut, let `P_y` be the orthogonal projector onto `col(H_y)` and `R_b` onto `col(G_b*)`. Both have rank at most one. Then

`(I-P_y) T[X,A]^(yb) (I-R_b)=0`.

Writing `alpha_yb=||P_y f_b||²` and `beta_yb=||R_b conjugate(g_y)||²`, the squared norm of the projected target is

`(u-alpha_yb)(v-beta_yb) >= uv-v alpha_yb-u beta_yb`.

The conjugate on `g_y` is essential because the target uses a transpose. Fourier orthogonality on either coordinate subset gives `sum_b f_b f_b*=sI` and the corresponding identity for conjugated `g_y`. Thus, after excluding the nonnegative diagonal-pair terms, the sums over `y != b` obey `sum alpha <= s²` and `sum beta <= s²`. The squared error on that rectangle is therefore at least

`[s(s-1)uv-s²(u+v)]_+`.

The opposite rectangle has the same valid bound and has disjoint matrix entries. Adding them, with `||F_(s²)||_F²=s⁴`, proves

`||F_(s²)-T||_F²/s⁴ >= B_s`,

`B_s=(2/s⁴)[s(s-1)floor(s²/4)-s³]_+`.

For `E=(F-T)/s` of dimension `N=s²`, `||E||_2² >= ||E||_F²/N = ||F-T||_F²/s⁴`, giving the same squared lower bound for normalized spectral error.

For even `s`, `B_s=[(s-5)/(2s)]_+`. For odd `s`, `B_s=[(s-5)/(2s)-(s-1)/(2s³)]_+`. Thus `B_s -> 1/2`, and the norm lower bound tends to `1/sqrt(2)`. The coarse quantitative bound is zero at sides 4 and 5 despite exact infeasibility there. Neither attainability nor an optimal constant is proved. No other rectangles, common fine tree, or shared-order near-unit barrier are imported. No norm statement is applied to finite fields.

## Independent computation

Only the three reviewer-written programs in this packet were executed. Candidate programs are retained as `.py.txt` and the original archive was read as bytes.

1. **Saved evidence:** All 78 pinned certificates at sides 4–16 were independently reconstructed using the finite geometric-sum inverse, without running the candidate solver. Verified 3,120 left/right inverse identities, 3,120 both-orientation cut ranks, 17,784 mode-membership decisions, and all 780 vertical-variable coefficient pairings. Every saved target pairing is nonzero and exact.
2. **All-weight finite controls:** Exhausted every field-weight assignment and every cut-respecting directed cyclic order at `(s,p)=(4,5),(5,3),(6,3)`, omitting singular monodromy. This checks 30,060 matrices and 60,120 ranks, including 27,948 zero-weight matrices. These controls concern the Green cut lemma alone and do not require a primitive Fourier root; in particular, no Fourier claim is made over GF(3) at side 6.
3. **Fresh networks:** 36 new prime-field networks at sides 4–12 use independently shuffled/reversed/rotated orders, zero edges, all-zero cycles, zero scalar terms, arbitrary diagonals and arbitrary vertical matrices. Generic elimination cross-checks 576 zero-safe solves. Full stage-matrix products at sides 4–8 verify 34,696 entries, including 25,376 off-axis identities. Natural-endpoint Fourier identities are checked on 242,448 entries. All 36 networks have new exact dual witnesses against every vertical completion.
4. **Non-prime field:** A separate implementation of `GF(3)[x]/(x⁴+x+2)` validates inverses for all 80 nonzero elements, finds all eight primitive 16th roots, checks 96 pairwise mode-independence tests and 512 cut ranks, and produces 32 additional exact dual certificates. This supports, but does not replace, the field-uniform proof.
5. **Outside-subclass countercontrol:** The saved side-4 GF(17) example reconstructs `rank(H)=1`, `rank(G)=2`, with `det(G)=15`. It correctly demonstrates that a single Green term does not make an arbitrary interleaved cut rank one. It is not a Fourier construction.
6. **Norm and cost arithmetic:** Exact rational identities and literal cost totals checked at every side 4–10,000 and at `10^6,10^9`. Twelve additional complex numerical controls at sides 4,5,6,8,11,16 verify the transpose/conjugate placement, frame sums, cancellation of completion terms, disjoint cuts, and the bound against independently solved local least-squares relaxations. Those numerical tests are sanity checks only; the proof above establishes the norm theorem.

The finite checks are supporting evidence. They are not substituted for either universal proof. The newly pinned certificates can certify only their pinned horizontal choices; the counting argument certifies every horizontal choice.

## Paid resource audit

The candidate ledger is a correct explicit upper bound for executing an allowed network, which the theorem proves cannot implement full Fourier. It is not the cost of a successful Fourier algorithm or a lower bound against alternative implementations.

- **Field and root:** Supplied field operations and a primitive `s²`-root are assumptions. Root construction, factorization and order certification are separate costs. A full optional root table requires `s²-1` multiplications and `s²` stored field elements.
- **Horizontal preparation:** `2s` orders of length `s`, `2s²` edges, `2s` scalars, and `2s²` diagonal entries are explicitly loaded and checked. Monodromies and inverse denominators require `2s²` multiplications, `2s` subtractions and `2s` inversions. Zero edges are never divided by.
- **Green solve:** With denominators prepared, a full affine pass uses `s` multiplications and `s` additions; solving the start value uses one multiplication; the recovery pass uses `s-1` multiplications and `s-1` additions. This is `2s` multiplications and `2s-1` additions. Scaling, diagonal action and addition raise this to `4s` multiplications and `3s-1` additions per horizontal fiber.
- **Vertical data and arithmetic:** Both vertical stages explicitly contain `2s³` coefficients. Loading or independently generating all of them is separately charged. Ordinary dense application needs `2s³` multiplications and `2s²(s-1)` additions; it is not free or presumed to be Fourier.
- **Full application:** Across both stages, including the H+V additions, the verified totals are at most `2s³+8s²` multiplications and `2s³+6s²-2s` additions after preparation.
- **Routing and storage:** Routing is `O(s²)` indexed gathers/scatters in the stated word-RAM, with `2s²` index words. Coefficient storage is `2s³+O(s²)` field elements, scratch storage `O(s²)`, and all `s²` natural-order outputs are materialized with `s²` writes. No geometric routing bound, bit-complexity statement, or conditioning claim follows.

These literal counts include multiplication by identities rather than relying on special-case discounts. Verifier matrix materialization is separate from the claimed execution ledger.

## Scope and remaining work

The previous accepted restricted obstruction remains intact. The accepted extension concerns the named common-bipartition subclass only. The broader outside-grammar question remains partially open: this is not a theorem about every independently ordered network and does not change historical priority.

Both horizontal stages and both cut orientations have zero-safe rank bounds at most one. Over C only, the separate two-rectangle relative-Frobenius and normalized-spectral error lower bound tends to 1/sqrt(2). Arbitrary fiber-dependent interleavings, growing term counts, deeper networks, general algorithms and external novelty remain open. Future construction attempts therefore require orders lacking a common low-rank bipartition, or another explicitly chosen open grammar.

Independent recorded controls passed. No separately evidenced sealed-extraction cold replay is claimed.

## Reproduction

The following commands refer to the separately preserved complete review archive, rather than this report-only publication:

`python independent_checks.py`

`python extension_field_checks.py`

`OPENBLAS_NUM_THREADS=1 python complex_controls.py`

The first program uses the reviewed candidate archive located one directory above this review folder. It checks its hash before reading it. The exact programs use the Python standard library. The third additionally requires NumPy. `MANIFEST.json` binds all packet files except itself, and the external seal binds the full ZIP plus manifest. No uploaded program is executed by these commands.
