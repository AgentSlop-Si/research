# Independent review of the split-node base-field construction

10 October 2026. Verdict: **accepted, as a constructive upper bound only**. The frozen author note is `sources/BASEFIELD_FOURIER_UPPER_BOUND.md`, SHA-256 `f8bac209b3cd12da34618bb11118a0bf81b69cbb2c765d97265dda49c5202155`.

## Accepted theorem

For every odd N≥7 and primitive Nth root q, put K=Q(q). The frozen proof establishes M_K(F_N)≤2N−4 with bank multiplicities (N−3,1,1,N−3), all beta parameters one, and every node and raw weight in K. The reviewed mechanism is genuinely split over K and does not descend the earlier algebraic-node witnesses.

## 1. Root coordinates legitimately solve the arithmetic issue

Let m=N−4 and d=N−3. In the normalized b=1 edge define H=q/(1+q), f(a,b)=q^{4^{-1}(a+b)^2}, and

s_(a−1)=(f(a,1)/H−G_-+(a,1))/G_++(a,1), 1≤a≤N−2.

All denominators are nonzero in K. Direct simplification gives s0=1 and s2=q. The latter uses f(3,1)=q⁴, G_-+(3,1)=−q(1+q), and G_++(3,1)=(1+q)(1+q²). Thus no complex absolute-value argument is necessary.

For the linear functional L(t^j)=s_j and P(t)=∏_(i=1)^m(t−yi), set D=L(P), U=L(tP), x=U/D. Then g(t)=(t−x)P(t) has degree d, is already split in the chosen root coordinates, and obeys L(g)=0 identically whenever D≠0.

The nonzero polynomials needed to select legal root coordinates are established separately:

- D has coefficient (−1)^m s0 on ∏yi, hence is nonzero.
- U has coefficient (−1)^(m−1)s2 on every degree-(m−1) squarefree monomial, hence is nonzero.
- U−yiD=L((t−yi)²∏_(j≠i)(t−yj)). Its coefficient of ∏_(j≠i)yj is (−1)^(m−1)(s2−2yi s1+yi²), which is nonzero.
- The factors yi and yi−yj are nonzero polynomials.

Thus the exclusions D≠0, x≠0, yi≠0, x≠yi, yi≠yj are simultaneous nonempty-open conditions in **root** coordinates. This is fundamentally different from selecting coefficients of an annihilator and assuming its roots lie in K.

## 2. The axis has an independently certified nonzero minor

Use m forward fixed-node columns, the negative-epsilon positive-delta singleton, and three backward fixed-node columns y1,y2,y3. There are m+4=N columns. At yi=q^i, i=1,…,m, the b=0 vectors have frequencies

q¹,…,q^(N−4), 1, q^(N−1), q^(N−2), q^(N−3).

These are all N different Nth roots. The resulting matrix is a Fourier/Vandermonde matrix in permuted columns, so its determinant A(y) is a nonzero polynomial. This minor never uses the rationally solved last node x. N≥7 ensures m≥3 and makes the three backward columns available.

One need not show that all guard factors are nonzero at this Fourier specialization. It suffices that each is a nonzero polynomial in the integral domain K[y]. Their product Γ is then nonzero.

## 3. The claimed finite grid bound is valid

For

Γ=A·D·U·∏yi·∏_(i<j)(yi−yj)·∏i(U−yiD),

the individual degree in any yi is at most

(2N−2)+1+1+1+(m−1)+(m+1)=4N−7.

The first bound arises because yi occurs in at most two selected axis columns and every entry has degree at most N−1. Each D,U is multilinear. In the final product yi has degree at most two in its own factor and at most one in each of the other m−1 factors.

The tensor-product interpolation lemma therefore guarantees a nonzero Γ value on {1,…,4N−6}^m. Characteristic zero makes these grid values distinct. Exhaustive exact evaluation in K is a deterministic finite recipe. Its search space is exponential in N; no efficient node-selection or FFT complexity claim follows.

## 4. The deficient first edge is exactly compatible

Use all d nodes yi and x. Solve the d-by-d Vandermonde system for amplitudes Ai satisfying the first d moments s0,…,s_(d−1). The one relation L(g)=0 supplies precisely the remaining moment sd. Set forward bank amplitudes hi=HAi/node_i, backward singleton amplitude H, all backward-group amplitudes zero, and use the opposite-delta singleton for the axis residual.

At a=N−1, only the backward singleton contributes and H·G_-+(N−1,1)=1=f(N−1,1). At a=1,…,N−2, the prescribed edge moment equation gives the target. The opposite-delta singleton supports only a=0 on this row, where it supplies the chosen residual. Thus rank deficiency is resolved by an explicit recurrence, not by a dimension count.

## 5. All positive interior rows have an elementary exact construction

For 2≤b≤(N−1)/2, the coordinate a*=N−b is exclusively supported by the negative-epsilon positive-delta singleton. Choose its amplitude

y_b=f(a*,b)/G_-+(a*,b),

whose denominator is nonzero because the local total is 2b≤N−1. Set the other cross-sign singleton amplitude to zero.

Choose the forward root-group moments at a=1,…,N−b−1 to equal the Gaussian-divided residual after subtracting that singleton. There are at most d moments, with consecutive positive powers, so a square Vandermonde using that many of the distinct nonzero nodes is invertible. Unused amplitudes are zero.

Next prescribe backward root-group moments at r=1,…,b−1 for the residuals at a=N−r. Set its zero moment to f(0,b)−y_b−(the sum of the forward amplitudes). These b moments use powers zero through b−1 and require at most d nodes. Their Vandermonde is invertible.

The forward support, exceptional singleton coordinate, backward support, and axis partition the entire row. The positive and negative same-sign groups do not interfere on these nonaxis intervals. This uniform recipe handles b=2 as well; a separate b=2 completion is unnecessary.

## 6. Reflection, normalization, and actual counted objects

Simultaneously reflect a,b to −a,−b and swap ++ with -- and −+ with +−. The target f is invariant and the local r,ell coordinates and epsilon·delta are preserved. Both same-sign groups use the identical node set, so the recipe supplies all remaining rows. In every bank physical rows map bijectively to sectors ell=delta·b modN, leaving no cross-row consistency gap.

With C=N^−1∑q^(−t²), choose raw weights

w_(i,j)=C·Delta_i·∑ell h_(i,ell) q^(−epsilon_i delta_i j ell),
Delta_i=−alpha_i^N.

All nodes are nonzero elements of K, so every guard is nonzero. Every amplitude and weight lies in K. Finite character orthogonality supplies exactly the original 1/N normalization. The accepted finite inverse formula then proves the equality of the original resolvents, not an enlarged moment-bank class.

There are 2d+2=2N−4 whole banks and N(2N−4) declared inverse branches/raw weights. A node used in both same-sign orientations is still two bank occurrences. A trace, orbit, or shared root is not charged as one bank. Zero amplitudes could reduce the count, so the theorem is an upper bound only.

## 7. Independent executable controls

The fresh control chooses fixed integer nodes 2,…,m+1, computes x=U/D, follows the preceding edge/interior/reflection construction, converts all original raw weights, and directly inverts every N-by-N branch matrix by Gaussian elimination. It checks both inverse products and all Fourier entries. It does not use the Gaussian coefficient formula in this final matrix accumulation.

Passed cases:

- N7 over F29, q=16: 10 banks, 70 branch inverses, 49 entries.
- N9 over F73, q=2: 14 banks, 126 branch inverses, 81 entries.
- N11 over F67, q=64: 18 banks, 198 branch inverses, 121 entries.
- N13 over F53, q=16: 22 banks, 286 branch inverses, 169 entries.
- N15 over F61, q=16: 26 banks, 390 branch inverses, 225 entries.

Total: 1,070 two-sided inverse checks and 645 original matrix entries. The composite orders 9 and 15 explicitly exercise the nonprime support formulas. These are controls of a characteristic-zero proof, not modular lifting or evidence substituted for all-order reasoning.

## 8. Scope

The frozen note agrees with this argument and establishes a Fourier-specific base-field upper bound for all odd N≥7. It does not change the sharp target-independent architecture minimum 2N−2. It does not give eight K-banks at N7 or fourteen K-banks at N11, and the accepted 14-bank extension-field result at N11 remains numerically stronger. Exact minima, historical priority, efficient search, stability, bit complexity, and a Fourier runtime gain remain unproved.

## 9. Independent exact small-order controls

`fresh_exact_node_checks.py` separately reconstructs K=Q(q) by rational polynomial arithmetic modulo Phi_N for N7 and N11. It independently derives the edge moments, D and U, verifies the two explicit final-node formulas in Section 5 of the frozen note, constructs the resulting split polynomial from its actual nodes, checks the exact recurrence, and verifies all node distinctness/nonzero conditions and inverse guards. All tests passed. `INDEPENDENT_EXACT_NODE_RESULTS.json` records the exact rational-basis values. These checks are characteristic zero.

The finite-field literal matrix checks and characteristic-zero node checks are deliberately distinguished. The review did not import, execute, compile, or parse an author or predecessor research program. The source proof and inert mathematical data were read. The general theorem follows from the proof reviewed above, not from extrapolating either collection of finite controls.

## 10. Frozen field boundary and resulting bounds

The accompanying arithmetic note proves that the earlier N7 cubic witness has splitting-field degree exactly six and that the earlier N11 sextic is nonsplit over K. Neither observation is a Fourier lower bound over K. The new all-order reconstruction therefore supplies the valid combined bounds 8≤M_K(F7)≤10 and 6≤M_K(F11)≤18 while leaving the accepted complex results unchanged. See `ARITHMETIC_AND_PRIOR_ART_BOUNDARY.md` for exact prime certificates and source comparison. No claim of historical novelty is accepted.
