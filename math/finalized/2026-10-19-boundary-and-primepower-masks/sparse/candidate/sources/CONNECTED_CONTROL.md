# M-SPARSE-DEFECT: an exact obstruction to uniform block reduction

Date: 2026-10-18. Owner **M-SPARSE-DEFECT**, priority **42**, status **TO RESEARCH**.

## 1. Result and honest terminal status

**The requested uniform divisibility conjecture is not resolved in this packet.** No proof that every equality mask has `d | N`, and no equality mask with `d` not dividing `N`, is claimed.

The concrete failed premise identified here is stronger than a lack of computation:

> A binary Fourier equality mask need not be a disjoint union of full `d × d` Fourier submatrices, even after arbitrary independent row and column permutations.

An explicit counterexample to that premise has `N = 8`, `d = 4`. Its entire bipartite support graph is connected, although it has 8 row vertices and 8 column vertices. All its original Fourier phases are retained, and both full complex Grams are exactly `4 I_8` before Fourier normalization. The obstruction extends to an infinite family `N = 8m`, `d = 4m` for every odd positive integer `m`.

This is a **failed-lemma result**, not a counterexample to divisibility: `4 | 8`, and `4m | 8m`. It prevents promoting the accepted weight-three structural proof to arbitrary weight by the same full-block conclusion. It does not exclude a different uniform proof.

The fresh exact checker also reconstructs the original minimizing matrix at the base example, verifies both inverse products, verifies the simultaneous support bound on every inverse row and column, and verifies the complete spectral-error identity. Thus the failed structural premise is tested inside the original model, not in a phase-relaxed or one-row model.

## 2. Source binding and retained target

The exact controlling source copies and SHA-256 hashes are in `SOURCE_BINDINGS.json` and `sources/`:

- Selected plan, task 2: uniform complementary divisibility, all `1 <= d < N`.
- Accepted equality criterion: `/workspace/shared/sparse_defect_budget_20261018_1240/REPORT.md`, Results 1–4 and §§2–6.
- Latest accepted boundary: `/workspace/shared/sparse_entrywise_gap_20261018_1508/REPORT.md`, §§1 and 6.
- Accepted weight-three support proof: `/workspace/shared/sparse_codimension_three_20261018_1331/REPORT.md`, §§2–4.

Let `omega = exp(-2 pi i/N)`, `F_N[r,c] = omega^(rc)/sqrt(N)`, and

`Delta_(N,s) = inf ||M-F_N||_2`, over invertible complex `M` whose every inverse row has at most `s` nonzeros.

Set `d = N-s`. The accepted equivalence is

`Delta_(N,N-d) = sqrt(d/N)`

if and only if there is a binary `N × N` matrix `R`, with exactly `d` ones in every column, such that `C = F_N entrywise R` satisfies

`C* C = (d/N) I_N`.

The equality condition automatically gives exactly `d` ones in every row. Divisibility is already sufficient. No new classification of nondivisor pairs follows from the present packet.

No historical checker, search package, or other historical program was executed. Reading the source reports does not import their code.

## 3. Literal binary mask

For `N=8`, let the rows of `R` be

```
0 0 1 1 0 0 1 1
0 1 0 1 0 1 0 1
1 1 0 0 1 1 0 0
1 0 1 0 1 0 1 0
0 0 1 1 0 0 1 1
1 0 1 0 1 0 1 0
1 1 0 0 1 1 0 0
0 1 0 1 0 1 0 1
```

Every row and column has four ones. Put `z = exp(-2 pi i/8)` and `D[r,c] = R[r,c] z^(rc)`. Thus `C = D/sqrt(8)`; there are no independent signs, phases, coefficients, or row/column phase modifications in this definition.

The four distinct column supports, each occurring twice, are

- `S_0 = S_4 = {2,3,5,6}`
- `S_1 = S_5 = {1,2,6,7}`
- `S_2 = S_6 = {0,3,4,5}`
- `S_3 = S_7 = {0,1,4,7}`.

## 4. Proof of the whole Gram identity

The Gram entry for columns `j,k` is

`(D*D)[j,k] = sum_(r in S_j intersect S_k) z^(r(k-j))`.

The diagonal entries are four. For the off-diagonal entries:

1. If `j = k (mod 4)` and `j != k`, then `k-j = 4 (mod 8)`. Each of the four supports contains two even and two odd indices. Consequently the sum is `2-2=0`.
2. For support classes 0 and 1, their intersection is `{2,6}`. The column difference is odd, so the two summands differ by the factor `z^(4(k-j))=-1`.
3. For support classes 0 and 2, the intersection is `{3,5}`. The column difference is 2 modulo 4; the row difference is 2. Their product is 4 modulo 8, giving cancellation.
4. Support classes 0 and 3, and classes 1 and 2, have empty intersections.
5. For support classes 1 and 3, the intersection is `{1,7}`. The column difference is 2 modulo 4; the row difference is 6. Their product is again 4 modulo 8.
6. For support classes 2 and 3, the intersection is `{0,4}` and the column difference is odd. Again the two terms cancel.

These cases cover every unordered distinct column pair, including either choice within each repeated support class; reversing a pair conjugates its sum. Therefore `D*D = 4 I_8`. Since `D` is square and invertible, also `DD* = 4 I_8`.

The independent exact verifier does not rely only on this case argument. It computes all 64 entries in each Gram by rational arithmetic in `Q[z]/(z^4+1)`. A second calculation records all exponent histograms and their four-coefficient remainders in `GRAM_CERTIFICATE.json`. No floating-point tolerance decides any identity.

## 5. Proof that no full-block decomposition exists

The nonempty intersections between the four distinct support classes form the connected cycle

`0 -- 1 -- 3 -- 2 -- 0`.

Every support has four rows, and their union is all eight rows. Each class contains two actual column vertices, with the same nonempty support. Thus the complete bipartite graph of the mask is connected. The checker independently traverses all 16 vertices.

If row and column permutations made this mask a direct sum of full `4 × 4` blocks, its support graph would instead have two connected components, each with four row vertices and four column vertices. Permutations preserve connectivity. This is impossible.

Equivalently, columns 0 and 1 have distinct supports with intersection size two. In a direct sum of full `4 × 4` blocks, column supports are either identical or disjoint. This also gives an immediate invariant obstruction.

The accepted weight-three theorem is unaffected: its elementary support classification is explicitly special to degree three. Here degree four permits a connected nonrectangular component, and its cancellation uses the original cyclic Fourier phases.

## 6. Infinite family of the same obstruction

Let `m` be any odd positive integer, `N=8m`, and `d=4m`. For `m>1`, let `u` be the inverse of `m` modulo 8 and `v` the inverse of 8 modulo `m`. Under CRT coordinates

`r <-> (a,b) in Z_8 × Z_m`, `c <-> (e,f) in Z_8 × Z_m`,

one has the exact identity

`r c / (8m) = u a e / 8 + v b f / m (mod 1)`.

Therefore the unnormalized Fourier matrix is, after row and column indexing by CRT, the tensor product of the order-eight Fourier matrix with its row index multiplied by `u`, and the order-`m` Fourier matrix with its row index multiplied by `v`.

Define the literal binary mask on the original indices by

`R_N[r,c] = R[(u (r mod 8)) mod 8, c mod 8]`.

The retained Fourier matrix is the tensor product of the base `D`, with its row indexing changed accordingly, and a full order-`m` Fourier matrix. Its two Grams are

`(4 I_8) tensor (m I_m) = 4m I_(8m)`.

It has exactly `4m` nonzeros in every row and column. Replacing each row and column vertex of the connected base graph by `m` twins, with all edges between corresponding twin classes, preserves connectivity. Thus its support is connected on `16m` vertices and cannot be a direct sum of two full `4m × 4m` blocks.

For `m=1`, use the base mask. The checker verifies the CRT pairing congruence at every entry for `m=1,3,5,7,9,11,15`, together with all support counts. These are transcription controls for the all-odd-`m` proof; no finite list substitutes for the proof.

## 7. Exact consequence for the original inverse-row optimization

There is no new optimum value here: the accepted divisor construction already gave `Delta_(8,4)=1/sqrt(2)` and `Delta_(8m,4m)=1/sqrt(2)`. The new construction shows that the associated equality masks and minimizers need not have the proposed full-block support structure.

For the base example, write `H[r,c]=z^(rc)`, `A_0=H-D`, and

`M_tilde = 4 (A_0*)^(-1)`, `B_tilde = A_0*/4`.

The actual normalized minimizer is `M=M_tilde/sqrt(8)`. Its inverse is `sqrt(8) B_tilde`, so scaling does not change any support.

The checker verifies exactly:

- `M_tilde B_tilde = B_tilde M_tilde = I_8`
- every row and every column of `B_tilde` has exactly four nonzeros
- `(M_tilde-H)(M_tilde-H)* = 4 I_8`, and the reversed error Gram too.

Hence `M` is invertible, every inverse row satisfies the original simultaneous budget, and `||M-F_8||_2^2=1/2`. For the infinite family, the accepted equality criterion gives the same conclusion. There is no conditioning relaxation and no replacement by the retained mask itself.

## 8. Exact unresolved arithmetic system and search accounting

For general `N,d`, write

`x^t mod Phi_N(x) = sum_(b=0)^(phi(N)-1) a_(t,b) x^b`, for `0<=t<N`.

With Boolean variables `X_(r,c)`, the exact remaining system consists of

1. `X_(r,c)^2-X_(r,c)=0` for every entry;
2. `sum_r X_(r,c)=d` for every column;
3. `sum_r a_((r(k-j) mod N),b) X_(r,j) X_(r,k)=0` for every `j<k` and every `b`.

This uses the precise original Fourier phases. It is equivalent to the requested equality-mask condition. Row sums and the reversed Gram equations follow mathematically; they may also be added as redundant constraints. The unresolved obligation is uniform exclusion for all `d` not dividing `N`, or one exact feasible nondivisor point.

The attempted structural shortcut would replace this system by disjoint full blocks. Sections 3–6 prove that replacement is invalid. No further connected-support invariant sufficient to infer divisibility has been proved here. In particular, the existence of connected supports with strict intermediate overlap cannot be discarded by importing the accepted degree-three lemma.

Two newly written exploratory MILP encodings linearize each product using a binary auxiliary variable `Y=X X'` and the three usual exact Boolean inequalities. One targeted run at `(N,d)=(12,5)` reached its 60-second limit; a strengthened encoding including both Gram orders reached its 180-second limit. Neither returned a feasible incumbent. Those outcomes establish neither existence nor nonexistence. Exploratory solver-reported infeasibility at `(6,4)`, `(10,4)`, and `(9,6)` has no retained exact unsatisfiability certificate and is not used for any mathematical claim. These small computations are explicitly not a replacement target or a proposed census result.

The exact checker is independent of both MILP encodings. It hardcodes the literal mask, uses only the Python standard library, and contains a negative control: a binary 2-by-2 switch preserves every row and column count but fails the Gram identity. Thus degree regularity alone cannot accidentally pass the validator.

## 9. Reproduction and scope

Run `python verify_exact.py` from this directory. It prints `PASS` and writes `RESULTS.json` and `GRAM_CERTIFICATE.json` after all assertions pass. `MANIFEST.json` binds the package files. The source reports are copied and hashed separately.

**Disposition:** retain the uniform conjecture as open, retain M-SPARSE-DEFECT at TO RESEARCH / priority 42, and record only the precise full-block-reduction obstruction if useful. Do not mark the selected uniform gate solved. No improved nonsharp value, quantitative gap, complexity claim, arbitrary-phase classification, or worldwide novelty claim follows.

No GitHub, spreadsheet, repository index, or other external state was changed.
