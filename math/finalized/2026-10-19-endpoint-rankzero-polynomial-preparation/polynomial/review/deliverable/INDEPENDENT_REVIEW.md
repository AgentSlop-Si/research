# Independent review: polynomial preparation for the accepted even-Prony extra-pole family

19 October 2026.

## Verdict

**Scoped ACCEPT.** The frozen candidate establishes a deterministic polynomial-bit preparation algorithm for the exact previously accepted family, for every even N >= 4 and every requested output exponent p >= 1. The fully charged upper bound is

    Õ((N^8 + Np)^3).

The smaller Õ(N^9 + Np) bound applies only to the published root engine in its coefficient-access model. It is not the full preparation bound. The distinction is explicit and necessary.

Acceptance covers the mathematical algorithm and its bit-cost/precision contract. It does not certify an implemented MSW/Pan root engine, a complete production preparer, practical performance, useful conditioning, fast Fourier computation, h-pole optimality, universal t = 1, or external novelty. Application remains O(N^2) rational operations with the inherited separately charged bit bound. The unscaled moment Vandermonde still has condition number at least 2^(2N^4).

The candidate proof reviewed here has SHA-256

    9e8b30f239ce33f99fbae74f9ad6ab82694e116e14b34f154611e4ac09e58cd2

and its ZIP has SHA-256

    267a003d8b9d0fc9fe64badadca1133dc34ec00d5993a76f57222a84e7a45103.

No outstanding mandatory repair remains. Two small specification repairs identified during review are incorporated in this frozen version: select a dyadic power of two for the disk radius, and explicitly round moment coordinates before invoking the matrix operand-size bound. Cache servicing was also made explicit.

## 1. Provenance, primary source, and exact theorem mapping

All eight candidate manifest entries were independently hashed and copied inertly. The ZIP contents were checked against the same files. The baseline family proof and its prior independent acceptance were read as text. No candidate or historical program was executed; all executed review scripts are newly written here. No external system, repository, table, or accepted dependency was changed.

Primary source checked directly: Mehlhorn–Sagraloff–Wang, arXiv:1301.4870v2, Sections 2.1–2.3, especially Corollary 1 and Theorems 3–4. Both the primary PDF text and the primary HTML rendering were consulted:

- https://arxiv.org/pdf/1301.4870v2
- https://arxiv.org/html/1301.4870v2

The theorem accepts complex coefficients, normalized leading coefficient, and a known distinct-root count. It charges coefficient access at reading cost. For simple roots its refinement cost is Õ(n^3+n^2 tau+nJ+n kappa), while its stated absolute coefficient-precision bound is Õ(n Gamma+J+n kappa). The latter n kappa term is retained by the candidate. Corollary 1 supplies complex dyadic approximations; the certification analysis includes precision doubling and unsuccessful iterations. The integer-coefficient specialization is unnecessary. The root-isolation algorithm is deterministic; the paper's random choices belong to its separate curve-topology application.

For this family, n = k = m = N/2+1 is known from the accepted all-embedding resultant/norm argument. Every multiplicity is one and the leading coefficient is exactly 1. Thus no numerical multiplicity decision, approximate normalization, or extra symbolic square-free computation is being hidden.

## 2. The same pencil and the same mathematical embedding

The input remains

    B(z) = z P_h(z) + 2^(10N^3+2) P_(h-1)(z),
    q = exp(2 pi i/N),  h = N/2,  m = h+1.

The X-polynomial construction agrees literally with the accepted definition of P_n. Each phase exponent n(n-1)/2-j(j-1)/2 is nonnegative. Each coefficient's X-degree is at most n(n-1), and the total integer coefficient l1 norm is at most 2^n. Therefore direct evaluation at the specified q, without reduction modulo a cyclotomic polynomial, produces the same chosen complex embedding.

The earlier proof gives, uniformly over coefficient-field embeddings, the radius, separation, nonzero-root, and forbidden-node margins used here. These bounds are not inferred from one numerical conjugate. In particular, for the prescribed embedding,

    |alpha_i| <= R,
    sigma_i >= delta,
    |B'(alpha_i)| >= delta^(m-1),
    |1+alpha_i^N| >= eta,
    dist(alpha_i, {z : z^N = -1}) >= rho.

The root engine is applied to B itself. Passing instead to a field-norm polynomial would increase the degree and could introduce coinciding conjugate roots; this candidate does neither.

Writing D = log2(delta^-1), one has D = O(N^6). The derivative product at a simple root is bounded below by delta^(m-1), so each derivative logarithm is at most (m-1)D. Hence

    J <= m[(m-1)D + D] = m^2 D = O(N^8).

Together with tau, Gamma = O(N^3) and kappa = p+O(N^7), this gives the claimed engine bound and maximum coefficient request. There is no unnoticed exponential quantity in either logarithmic substitution.

## 3. Fully charged unit-root and coefficient generation

### Fixed-point elementary functions

The fixed term counts and rounding format are sufficient. For the arctangent recurrence the exact multiplier has absolute value at most 1/25. A rounding error of at most epsilon at each step therefore keeps each term error below 2 epsilon. Multiplication by 16 and 4 in Machin's identity and exact fixed-lattice summation give the stated 40M epsilon plus tail bound.

For the exponential Taylor terms at the dyadic real argument x_hat in [0,2], the recurrence error obeys

    E_j <= (2/j) E_(j-1) + epsilon.

The first three upper bounds are epsilon, 2 epsilon, and 7 epsilon/3. For later indices the bound 3 epsilon is invariant. Signed even/odd sums therefore have the claimed linear-in-M error. The integral Taylor remainder for exp(ix) is bounded by 2^(M+1)/(M+1)!, and M = Q+40 is safely in the range where the printed geometric tail estimate holds. The real-argument uncertainty is included before concluding the complex q error.

Every iterate is rounded. This is the key reason the scalar routine uses O(Q+log Q)-bit operands instead of allowing exact rational Taylor denominators to grow quadratically. O(Q) schoolbook arithmetic steps then cost Õ((Q+1)^3).

### Symbolic coefficients and Horner evaluation

The symbolic construction has polynomial size. Dense shifted coefficient arrays need O(N^4) additions of O(N)-bit integers before insertion of t. There are O(N^3) resulting integer coefficients, and insertion of an O(N^3)-bit t costs at most O(N^6).

The q perturbation bound pays both degree N^2 and coefficient height R. Horner evaluation at q_hat amplifies each introduced error by less than 3 because |q_hat| <= 1+N^-2. Each complex coordinate rounding is included in the l1 budget. All nonleading coefficients fit the stated aggregate bound, and the leading coefficient is kept exactly equal to one.

Thus an entire coefficient-vector request of precision A costs

    Õ((A+N^3)^3 + N^3(A+N^3)^2 + N^6),

with harmless logarithmic terms suppressed. This is actual generation cost, not a free cyclotomic coefficient oracle.

### Retries and cache servicing

The cache constructs increasing power-of-two precisions, at most a factor two above the maximum requested precision plus constant guards. Its cubic and quadratic construction costs sum geometrically, apart from baseline polylogarithms. Coarse requests are served from the relevant cached prefixes and truncated to near-requested precision; returning or scanning the entire finest vector for every coarse call is not necessary. The extra O(log m) fractional guard pays simultaneous coordinate truncation.

Consequently oracle construction is paid once at the largest asymptotic precision, while the root algorithm's reading-cost accounting pays the individual requests. Neither repeated certification attempts nor a large number of coarse requests supplies an uncharged operation.

## 4. Compact root certificates, legality, and labels

The final radius is an explicitly computable power of two below the minimum of all downstream tolerances. A general positive dyadic rational would not have a largest member below a nondyadic minimum; the corrected power-of-two selection avoids that issue. The radius exponent is bounded by p+O(N^7).

Set e_c = d_0 r/(256m A_0). The requested kappa has four additional bits beyond ceil(log2(1/e_c)); rounding the root engine's center to the finer specified dyadic lattice keeps total center error below e_c. The retained coordinates consequently need only O(p+N^7) bits, even if the root engine internally used more precision.

For the exact local Taylor coefficients a_k and computed coefficients a_hat_k, the uniform enclosure |a_hat_k-a_k| <= E is valid. The functions

    U(a) = |Re a|+|Im a|,
    L(a) = max(|Re a|,|Im a|)

are respectively an upper and a lower bound for |a|. Consequently the rational strict inequality RC really is a Rouché certificate. The candidate correctly adds the coefficient uncertainty to the upper bounds and subtracts it from the lower bound.

At a proposed center the unperturbed upper-side surrogate is at most 5d_0 r/(128m), whereas L(a_1)r is at least d_0 r/4. The total coefficient-enclosure disturbance is bounded by (4m+2)E < d_0 r/512. Since m >= 3, a positive margin remains. Certification succeeds at this prescribed finite precision; it does not require indefinite refinement at an equality case.

The exact squared-distance comparisons prove that the m disks are disjoint. A degree-m polynomial with one certified root in each therefore has complete, nonduplicated coverage. Root identities are determined by the polynomial, specified embedding, and disks, not by an unsupported radical formula.

For refinements, same-root centers are within delta/8 and different-root centers are at least 7delta/8 apart. Matching with threshold delta/2 preserves labels, including equal-real-part cases. Independently sorting each later batch is correctly forbidden.

Every point of a retained disk is within 2r of its root. The selected tolerances give a nonzero modulus margin a_min/2, forbidden-set distance rho/2, and direct denominator bound |1+z^N| >= 3eta/4. Thus all stored centers and downstream resolvents are legal; a numerical zero-denominator test is unnecessary.

## 5. Weights, residues, bit sizes, and final output precision

Moment coordinates are now explicitly fixed-point evaluated and finally rounded to O(K)-bit dyadics, where K = p+N^7. This is important: sending unrounded powers of a fine q_hat directly into the linear system would invalidate the printed O(NK) common-denominator estimate.

The root tolerance gives K_V H_V e <= 1/8, which is stronger than the accepted inverse-perturbation requirement. The selected moment and root budgets each contribute at most v_b/8 to the solution error, so the exact solve error is at most v_b/4. Rounding all 2m real coordinates within v_b/(8m) adds less than v_b/4 in Euclidean norm. The accepted bound on the exact beta vector is used in the residue perturbation estimate; it is not silently replaced by an unproved computed-vector bound.

The two pre-rounding residue terms each cost at most v_g/8. Final complex rounding costs less than v_g/4, leaving the stated residue accuracy. Zero exact weights need not be detected or omitted.

After clearing a common dyadic denominator, matrix and moment entries have O(NK) bits. Determinant/minor expansions give O(N^2K+N log N)-bit intermediate values. Pivoted fraction-free elimination over Gaussian integers is therefore polynomial-size. Its O(N^3) arithmetic steps fit the claimed Õ(N^7K^2) conservative bound. The argument does not justify an unpivoted floating-point solve and does not claim to.

The final rounded root and residue tolerances are stronger than the accepted bank-perturbation contract. Both endpoint diagonals and the normalizer are constructed and charged. Thus the old relative output error below 2^-p for b-bit dyadic input is preserved, with its paid

    O(N^2) rational-operation application,
    O(N^6(p+b+N^7)^2) bit application.

This assertion inherits the accepted signed-wrap recurrence and final output-rounding argument; neither is changed by the preparation substitution.

## 6. Total complexity and output size

Put A = NK = N^8+Np. Up to logarithms, the separate terms are

    N^6,
    N^9+Np,
    A^3+N^3 A^2,
    N^7 K^2,
    K^3+N^7 K^2.

All are at most Õ(A^3), since K >= N^7. The same domination would even tolerate the weaker N^9K^2 elimination envelope discussed by the candidate. Compact center output, all O(N^2) Taylor-certificate entries, weights, residues, endpoint constants, and their denominators fit polynomial storage and are included in the charges.

Exponential condition numbers are compatible with this bit bound: their logarithms, hence the additional precision needed here, are polynomial in N. The bound does not imply a practically usable precision budget. The previous exp(Omega(N^4)) conditioning obstruction remains intact.

## 7. Fresh independent evidence

The review's scripts import no research executable. Their exact arithmetic results are in `evidence/INDEPENDENT_RESULTS.json` and `evidence/CACHE_RESULTS.json`.

1. Thirty unit-root cases cover N = 4, 6, 10, 32, 128, 10000 and Q = 1, 8, 33, 128, 257. Every produced dyadic q is enclosed against a separately constructed outward interval calculation using direct arctangent terms and interval Taylor products. These are exact integer enclosure tests, not comparisons to an ordinary floating-point reference.
2. Eight complete coefficient-vector cases cover N = 4, 6, 8, 10 and A = 12, 128. A separate outward complex interval Horner evaluation encloses the exact coefficients at the exact chosen q. Every produced vector has rigorous l1 error below 2^(-A-1), and exact monicity is checked.
3. Three positive Gaussian-rational local certificates, three negative cases (no root, repeated root, oversized disk), and a deliberately permuted equal-real-part labeling case pass.
4. An actual N = 4, t = 2^642 instance is certified using the full formal downstream tolerance list at p = 3. Its radius is 2^-101726 and kappa = 134791. All three rational disks pass RC, exact pairwise disjointness, nonzero-center checks, and direct denominator lower bounds. Numerical Newton iteration only proposes these centers; all acceptance decisions are exact rational inequalities. The complete centers and error enclosure are saved in `FULL_TOLERANCE_N4_CERTIFICATE.json`; a separate cold verifier checks the expanded cubic directly, without Newton or imported research code.
5. Exponent and cost domination checks cover 131 even lengths through N = 10000 and three precision values each, totaling 393 cases.
6. Three adversarial cache request sequences, with decreasing/repeated requests and maximum precision 1,000,000, verify the requested guard budgets, logarithmic rebuild count, maximum constructed precision, and geometric cubic construction sum.

The first N = 4 proposal attempt used insufficient absolute-precision headroom for roots of size about 2^321 and reached a numerical stagnation threshold. That diagnostic-only failure is retained in `INITIAL_PROPOSAL_FAILURE.txt`; increasing the proposal guard bits produced the final exact-certified run. It was not a failure of RC or of the mathematical algorithm, and no uncertified center was accepted.

The controls do not implement MSW/Pan, benchmark the claimed asymptotic running time, or replace the all-N proof. They independently exercise the scalar oracle, certificate interfaces, precision budget, and finite same-family instance.

## 8. Permitted conclusion

Close only the exponential-versus-polynomial bit-preparation bottleneck for this specific already accepted large-t family. Preserve all existing algebraic/pole-count scope and leave useful conditioning, practical preparation/execution, h-pole optimality, and universal t = 1 open. This is an application of established root-isolation theory with a paid coefficient oracle and downstream interfaces; no novelty or fast-FFT claim is accepted.
