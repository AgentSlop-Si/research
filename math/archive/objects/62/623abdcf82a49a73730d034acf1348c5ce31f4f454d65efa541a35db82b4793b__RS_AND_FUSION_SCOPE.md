# RS local theorem, scalar banks and fusion scope recheck

10 October 2026. This pass reread the frozen algebra-final-v1 theorem package and final-v2 collision proof. It does not claim a new all-composite squarefreeness result.

## F020 / FUS-02: what remains fully supported

The separated and one-simple-overlap expansions use ordinary z-discriminants, fixed odd lower order d, and q(ε)=ω(1+ε²)^{1/d}. Exact cyclotomic division is performed in Z[q] before reduction modulo p. The arithmetic bridge needs one lower residue component where both residual factors are nonzero, rather than separate good components for the separate factors.

The Hermite parameter disk proof is sound: J=yHe_A−τHe_A' has no nonreal multiple-root parameter inside |1−τ|²≤(A+1)/A. The special real parameters are τ=0 for odd A and τ=−1/A for even A. At half-order overlap d≡3 mod4, the proved reciprocal identity puts τ on |1−τ|=1 with τ≠0. Thus the quasi-Hermite guard is removed in characteristic zero. The residual discriminant guard is not removed, and the disk has no finite-characteristic interpretation.

For s≡1 mod4, prime p≡1 mod4 and p∤s c_s with c_s≠0, N=sp, the proved reduced-coordinate-content statements remain

v_p(d_N)=floor(s(p−3)/8),
v_p(r_N)=floor(N/4),
v_p(c_N)=floor(3s(p−1)/8).

The content carry is one for p≡1 mod8 and zero for p≡5 mod8. The same good lower component makes both exact quotients units, which is essential for adding minimum valuations. These are contents in Z[ζ_N], not polynomial contents in Z[q]. They do not assert absence of unramified content primes.

The resulting m=(N−1)/2 legal scalar-bank minimum with a free diagonal is valid for the stated guarded separated family, and for the paired s≡p≡3 mod4 family giving N≡1 mod4. Without a free diagonal the existing all-odd minimum is m+1. Odd N≡3 mod4 has a forbidden resonant root and still requires m+1 even with a free diagonal. The latter is not cured by squarefreeness.

## FUS-06: conditioning is fixed-degree and analytic

For fixed-degree node clusters z_(a,j)=α_a+εξ_(a,j)+O(ε²), distinct α_a and distinct within-cluster ξ_(a,j), the square moment Vandermonde satisfies

||V||_2=Θ(1), ||V^{-1}||_2=Θ(|ε|^{−(m_*−1)}).

The coefficient vector of each Lagrange interpolation polynomial is a column of (V^T)^{-1}; its denominator has order exactly ε^{m_a−1}, and its leading numerator coefficient is one. This proves both matching norm bounds. Applying the actual RS splitting structure gives exponents A−1 in separated clusters and A in one-simple-overlap clusters. The half-order disk theorem permits dropping only the quasi-Hermite guard there. Constants depend on the fixed degree and residual data. No uniform growing-degree conditioning theorem is supplied.

Varying q analytically near a lower-order ω is not a path of primitive roots at a fixed target cycle length N. If a node is identically resonant, its resolvent is undefined; if it approaches resonance without reaching it, the normal cyclic-resolvent norm may blow up. Exact minimum branch count is not a numerical stability theorem or an application-time lower bound.

## Open mathematical work that this cycle did not close

1. All-composite half-order squarefreeness of H_{(N−1)/2}(z;ζ_N). Existing prime and guarded arithmetic families remain the scope. Neither consecutive formal-orthogonal coprimality nor the new even-bank extra-pole construction proves it.
2. Unramified coordinate-content support. The exact needed assertion is simultaneous nonvanishing of the reduced residual discriminant/resultant product in at least one component over each prime not dividing the lower order. Nonzero norm, individual special values and different good components for different factors do not suffice.
3. Repeated-prime N=sp^a, a≥2. P_A becomes p-divisible when A≥p, so the present unit-leading-quotient bridge fails. Higher-order/divided-power analysis would be genuinely new work.
4. General-b or multiple shared residual clusters. The half-order circle identity does not justify removing all other local guards.
5. All-even h-pole optimum. The completed theorem guarantees h≤Qmin≤h+1, with a legal integer parameter among1,…,4h. It does not prove squarefreeness/nonresonance of the original degree-h polynomial.

No denied Vanderbilt source was revisited and no restriction was bypassed. Lubinsky–Saff1987 and Zhedanov1997 fulltext comparisons remain unclosed. Existing accessible primary comparisons support attribution of the q-root factorization, q→1 Hermite limit, quasi-Laguerre and Prony mechanisms; they do not establish external priority for the exact local coefficients or legal-node minima.

## Bounded next fusion queue

- Supported new synthesis: C06 eliminant + short chirp convolution + complete recurrence verification, with the new O(Nr^{2+log_2 3}+r^{2+3log_2 3}) theorem. This has a concrete improved rank budget and does not require new signal assumptions.
- Supported extension to FUS-05: its raw q-Weyl Prony-recognition step can use the same blocked root/recurrence checks. Recognition improves from O(Nt+t³) to O(Nt^{log_2 3−1}+t³), but application of t weighted permutations still costs O(Nt); the overall evaluator therefore does not improve automatically. The structured worker has a stronger dyadic recognition theorem; the blocked bound is an all-length complement. Keep recognition and application charges separate.
- Research target only: uniform squarefreeness and coordinate-content support for composite RS orders. A proof would enlarge the exact bank-minimum families. No theorem is queued as completed without a mechanism that resolves simultaneous residue guards.
- Research target only: model-matched numerical/bit implementation of the blocked recognizer, with actual Toeplitz eliminant implementation, exact-field operation ledgers, and comparison against applicable FFT/NTT backends. Current controls isolate algebraic correctness and are not production benchmarks.
