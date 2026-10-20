# Sealed independent review: original Prony conditioning and paid contract

20 October 2026.

## Verdict

**SCOPED ACCEPT. No mandatory repair remains in the bound v2 candidate.**

Accepted new results are:

1. For every integer h>=2, q=exp(pi i/h), and the original P_h=-H_h(qz;q), the raw square moment matrix V[k,l]=alpha_l^k, 0<=k<h, is singular or satisfies

   kappa_2(V) >= [2/(h sin(pi/(2h)))]^((h-1)/2)/sqrt(h)
   > (4/pi)^((h-1)/2)/sqrt(h).

   The roots are counted with multiplicity and singular matrices have condition number infinity. This is the canonical complex embedding and unscaled monomial basis only.

2. For every even N=2h>=4 with 16 not dividing N, the same original h-root family has the stated explicit radius, separation, forbidden-node, inverse-Vandermonde, weight and residue upper envelopes. Its elementary certified preparation has bit cost 2^[O(p+N^5)] with polynomial workspace. Its specified independent-bank application costs O(N^2) rational operations and O(N^6(p+b+N^5)^2) bit operations, including both endpoint diagonals, normalization and all outputs, with relative output error below 2^-p. This is an effective mathematical contract, not a production implementation or an optimal complexity bound.

At other even N, the second contract is conditional on separately established ordinary squarefreeness. The first condition bound does not require squarefreeness. Inherited large-t-family results retain their original scope but are not newly recertified or transferred to the original P_h family by this review.

Useful conditioning under alternative coordinates or families, practical preparation and execution, original all-even optimality, the remaining squarefreeness obstruction, universal parameter choices, general stability, and faster Fourier computation remain open. No broader owner or workflow closure follows.

## Frozen objects and repairs

The accepted candidate is the v2 packet identified by:

- PROOF.md SHA-256: e9f61348c4e91ebb63bd9040ea877d075f61602499075fcc3611e18e789a2c44
- MANIFEST.json SHA-256: ed384801908daf6020da067c0f6d7ca65bb71e022b100191778c876649c6ae12
- COST_LEDGER.md SHA-256: 6726646aa8bf9be440d91d7072abe91105157996eee6a7f174050bb2df794ffa

All 20 manifest entries were independently hashed. Comparison against the first freeze, whose proof hash was 6149666e81489142e12f7fdceec7c65c7dfef7eecbc8b4a91d92e780b265cef7, confirms that exactly one proof paragraph changed and the other 19 content files remained byte-identical.

The repaired paragraph supplies both required precision details:

- Select the largest dyadic power not exceeding the displayed root tolerance minimum. This prevents arbitrary gratuitous overprecision from invalidating the stated upper cost.
- Acquire each complex moment within u_c/2 and then round each real and imaginary coordinate within u_c/4. Its final complex error is at most (1/2+sqrt(2)/4)u_c<u_c, as required by the subsequent inverse-perturbation inequality.

The author identified the first tightening; this reviewer requested the second. The repaired text was inspected and its exact diff verified before acceptance. The v1 file remains historical rather than being silently overwritten.

## Independent coefficient, phase and norm verification

The defining product R_h supplies an independent route that does not rely on guessing a Gaussian-binomial normalization. Since q^h=-1 and q^2!=1,

sum_{k=0}^{h-1}q^k=2/(1-q),
sum_{k=0}^{h-1}q^{2k}=0.

Therefore the top two nonleading R_h coefficients are -2/(1-q) and 2/(1-q)^2. Multiplication by the defining moment phases gives a_{h-1}=2q^{-1}/(1-q) and a_{h-2}=2q^{-3}/(1-q)^2. Newton's identity yields

sum_l alpha_l^2 = -4q^{-3}/(1-q).

The negative sign is correct. Its modulus is 2/sin(pi/(2h)), giving max_l|alpha_l|^2>=2/[h sin(pi/(2h))]>4/pi. At h=2, the actual polynomial is z^2+(1-i)z-1 and the sum is 2-2i. At h=1, P_1=z-1 and the squared-root sum is 1, so the coefficient argument must and does exclude this edge case.

The singular-value argument is valid over the complex numbers: an entry in the last row gives ||V||_2>=M^{h-1}, and sigma_min(V)=sigma_min(V*)<=||V*e_0||_2=sqrt(h). No positivity, real-root theorem, or confusion between a transpose and an adjoint is needed. Repeated roots give identical columns. The lower bound is asymptotically exponential but may be below the trivial bound 1 at small h, which the candidate acknowledges.

The candidate correctly does not transport this numerical statement to other cyclotomic embeddings by Galois invariance.

## All-embedding margins and setup audit

The actual recovered sources bind the original P_h definition, all-even forbidden-node exclusion, and ordinary squarefreeness for 16 not dividing N. The later four-times-odd acceptance is needed for the N congruent to 8 modulo 16 part; the earlier baseline scope alone would be too small. The source bodies and their acceptance boundaries were read. No uniform squarefreeness claim for multiples of 16 was inferred from finite certificates.

At every embedding, expanding the product and coefficient phases gives coefficient l1 norm <=2^h. The chosen R=2^{N+1} safely bounds every conjugate root. The constant coefficient is -1, which supplies the nonzero-root lower margin. The nonzero discriminant and forbidden-node resultant are algebraic integers. Their nonzero integer field norms, combined with the separately valid all-embedding upper bounds, justify delta and eta. Removing the remaining root-distance factors gives rho. The exponents are conservative in the correct direction.

Lagrange interpolation proves the inverse norm bound without a condition-number oracle. The displayed logarithmic estimates are O(N^4) for separation and forbidden-node margins and O(N^5) for inverse-Vandermonde, weights and residues. These are upper envelopes, not assertions about the actual asymptotic condition number.

For the root grid, A_0 bounds the relevant Taylor coefficient sums, d_0 lower-bounds the derivative at each simple root, and the dyadic radius and spacing retain positive Rouché slack. At m=2 the worst-case normalized slack is already at least 1/2-1/128-1/32>1/4. The enclosure disturbance is smaller than the reserved margin. The nearest grid point to every root is certified at one prescribed finite precision; there is no unbounded refinement at inconclusive grid points.

Disks containing different roots cannot intersect when r<=delta/8. Consequently greedy rejection can remove duplicates but cannot remove every disk representing a missing root. Counting m certified disks gives complete nonduplicated coverage. Later label matching uses the stronger radius restriction delta/16, so the claimed delta/8 and 7delta/8 center-distance bounds are valid.

The coefficient acquisition pays for the specified q embedding and the degree-O(N^2) coefficient polynomials. Its rounding and Taylor-shift error budgets fit theta. Exact rational Machin/Taylor evaluation and modulus bisection are elementary terminating procedures; the deliberately loose B^20 overhead and B^10 storage bounds dominate their intermediate sizes. This audit certifies the mathematical bound, not an executed exhaustive grid or a particular transcendental library.

## Weight precision, complete transform and bit accounting

The largest-dyadic tolerance repair makes log(1/e_*)=p+O(N^5), rather than merely a lower bound on the requested precision. The final rounded moments now meet the u_c error budget. The inverse perturbation bound, root-to-weight error, Euclidean rounding of weights, residue formation and final residue rounding all fit the stated v_b and v_g budgets. The bank perturbation is at most eps/4 from its explicit upper envelopes. The lower condition bound is not used as a sufficient precision estimate.

The signed-wrap recurrence was independently reconstructed for general N. The equations are y_i-a y_{i-1}=x_i for i>0 and y_0+a y_{N-1}=x_0. Substituting y_{N-1}=a^{N-1}y_0+b_* gives exactly y_0=(x_0-a b_*)/(1+a^N). Both the plus sign in the denominator and the minus sign in its numerator are necessary.

The endpoint phases satisfy T=E_R^{-1} S E_R and E_L E_R=Q, including the negative cyclic wrap when N is even. Thus the implemented normalized target is precisely the original negative-sign Fourier matrix. Paid endpoint and normalizer errors, followed by output rounding relative to the lower bound ||x||>=2^-b for a nonzero dyadic input, give the stated relative error. The zero vector is explicitly handled.

Before the weight solve, moments and root centers are dyadic with O(K)-bit coordinates. Powers give O(NK)-bit matrix operands after clearing a common dyadic denominator; minor bounds give O(N^2K+N log N)-bit exact elimination intermediates. The resulting O(N^7K^2) schoolbook solve bound is conservative and is charged to setup.

Online, one branch introduces a denominator with O(NK) bits. Summing at most m branches gives O(N^2K)-bit running rational coordinates. This supports O(N^6K^2) bit work for O(N^2) rational operations. The proof correctly distinguishes O(N+m) scalar registers from O(N) fixed-word memory and charges O(N^3K) bits of online storage. Reading inputs, writing all outputs, signed recurrences, summation, both endpoint diagonals and normalization are included.

## Meaning of the conditioning result and historical ledger

For an arbitrary fixed invertible V, kappa_2(V) is the exact worst-case relative right-hand-side amplification over all nonzero right-hand sides. Singular vectors exhibit perturbations with amplification epsilon*kappa_2(V). This does not establish that the fixed chirp right-hand side is such a worst case, that actual rounding errors realize those perturbations, or that structured root perturbations have the same condition number.

A requirement uniform over arbitrary right-hand sides and all relative data errors up to 2^-t would require 2^-t*kappa_2(V)<=tau to bound the propagated relative solution error by tau. That statement belongs to that specified error model, not an inherent arithmetic bit lower bound. Scaling, preconditioning, alternative bases, exact arithmetic, shared computation and alternative legal families remain outside the obstruction. The final normalized Fourier operator remains unitary.

The ledger preserves the historical large-t family's separate accepted polynomial preparation result and explicitly charges coefficient generation rather than quoting only its root-engine cost. It does not claim that engine is implemented or that the theorem automatically transfers to P_h. Its original-family exponential lower bound is not advertised as a conditioning improvement over the large-t lower bound: two different lower bounds cannot establish that comparison, and the available original upper envelope is much larger.

## Executed checks and attribution

The separately authored independent_checks.py checks the symbolic Newton identity and a wrong-sign negative control, exact N=4 endpoint/normalized-target algebra, the signed-wrap branch with symbolic a and arbitrary x, a wrong-sign branch control, and the uniform m>=2 Rouché slack. It also binds the first frozen manifest. A separate v2 verification bound all repaired hashes and the exact one-paragraph diff.

No author or inherited checker, root census, exhaustive grid, or production executor was run by this reviewer. The author's reported finite controls are supplementary evidence, not the uniform proof.

An optional reciprocal-root sharpening was suggested by this reviewer before the freeze. It was deliberately not incorporated into the candidate and is not needed for this acceptance. The accepted candidate therefore does not treat a reviewer's own new sharpening as independently accepted work. The review's essential specification contribution is the explicit total moment-rounding budget; the main mathematical arguments were independently checked at the frozen scope.

This review changes no external repository, live table, discovery count or broader accepted scope.
