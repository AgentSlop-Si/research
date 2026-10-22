# Independent review: complete original positive-chirp exclusion

## Verdict and exact binding

**ACCEPT SCOPED.** The exact frozen positive-family theorem and all necessary certificate implications pass independent review and a separate clean replay.

The reviewed author candidate is bound by `source/FROZEN_MANIFEST.json`, SHA-256 `028aec843d3bc9d494cfc5a0b7dbdd3d1fec0e55e0c4ff4d2fcedf84f5e927fa`. Every one of its 78 payloads, totaling 17,526,306 bytes, was independently read and hash-checked. The proof `source/POSITIVE_PROOF.md` has SHA-256 `1e1a1b95a5b8427c52f65ba9157125deead29d68dca7951dbef0960ceca84eae`. This review does not accept an earlier mutable draft or a file-count summary.

The exact conclusion under review is E_plus = empty: for every positive integer N=5m with N odd, gcd(m,5)=1 and N congruent to 1 modulo 4, and for every primitive complex Nth root omega, the original target B_N=(F^(-1)+A)^(-1), F_ij=omega^(ij), A_jj=omega^(((N+1)/2)j^2), cannot be the sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary complex diagonal endpoint masks. The masks may be singular or entirely zero, the edge weights may be zero, and the two cycles may coincide. Each original Green denominator must be nonzero. Coordinate order is fixed, without unmatched endpoint permutations.

No essential mathematical repair was supplied by the reviewer. The author's separate integer-root resolution of its initially inconclusive last leaf was independently reconstructed before acceptance. Neither negative-family polynomial outputs nor the old giant cutoff are used to establish the new positive result.

## 1. Independent method and retained inputs

The four recovered positive inputs were read and their exact hashes checked. The accepted restriction/Gauss identities and general closed necessary-system statements are retained inputs. Their previously accepted cutoff and square-modulus conclusions are preserved, not reopened. The already accepted negative original theorem is not a positive-family dependency.

The reviewer wrote eight standalone Python programs, using exact rational and cyclotomic arithmetic with SymPy 1.14.0. They import no author executable, no negative-family executable, and no historical reviewer executable. Author programs and algorithm provenance are retained only as inert source snapshots. The programs reconstruct the positive target, cycle universe, transition graph, selected quadratics, row and column directions, actual augmented minors, resultants, norms and coverage from their mathematical definitions, then compare exact certificate coefficients.

The main independent implementation differences are substantive:

- Cyclotomic values are represented by four rational-polynomial coordinates. The 90 block norms are recomputed as determinants of their 4-by-4 regular multiplication representations, with 360 additional embedding checks.
- Larger norms use an independently implemented tower formula. If t=z+z^(-1), t^2+t-1=0, and p times its complex conjugate is A+B t, the norm is A^2-A B-B^2. This formula is also compared with the regular-representation determinant on all 90 blocks. It does not call the author's polynomial norm routine.
- Actual 11-by-11 minors are rebuilt with subset dynamic programming, retaining all feasible determinant matchings, rather than the author's target-column Laplace enumeration.
- Resultant remainders are reconstructed by high-to-low exact polynomial pseudo-division, rather than the author's forward power recurrence. The supplied U, V and resultant are then checked as exact polynomial identities. The fixed-degree Sylvester interpretation is proved below and independently tested, including degree drops.

`run_review.py` is the portable independent entry point. It first verifies every frozen source payload, runs only reviewer-owned programs, and verifies the frozen source again afterward. The source candidate is not modified.

## 2. Positive signs, actual parameter domain and legal denominators

The reviewed formula is exactly

B_N[S,S] = H_plus(G,eta)/(1+G^3),
H_plus(g,eta)_ij = eta^(ij) - g eta^(-3(i+j)^2) + g^3 eta^(-3i^2) delta_ij,

where S=(0,m,2m,3m,4m), eta=omega^(m^2) has exact order five, and G^2=N. The cubic diagonal sign is positive. G need not be positive; both real signs are covered. The denominator is nonzero because |G^3|=N^(3/2)>1 for N>=5.

Principal restriction contracts consecutive selected-to-selected arcs and multiplies their edge weights. Their total product, and hence the legal Green denominator, is unchanged. No individual edge is divided out. Diagonal masks restrict entrywise. Thus a full permitted representation would give a permitted block representation and then a necessary-system point for H_plus. This implication does not require a block representation to lift back to the full target.

The exclusion is proved on a larger formal locus with g^2 a positive integer of 5-adic valuation one and eta any primitive fifth root. It is not asserted that independently chosen formal (eta,g) are all realizable by an original primitive omega. Actual Gauss data lie in the excluded locus, which is the only implication needed. In particular the last integer-root leaf is not an exclusion theorem for arbitrary rational or continuous real parameters.

## 3. Closed-system and projective-boundary completeness

For each ordered cycle pair, the 25-by-11 augmented matrix has ten coefficient columns and one target column. The formal scale labels are not extra projective variables. Every actual representation with invertible masks supplies the off-support equations and all maximal augmented minors. Vanishing maximal minors is used only as a necessary condition; no consistency or sufficiency inference is made when the first ten columns lose rank.

The determinant multidegree is product lambda_i^(n_i-1) product mu_j^(m_j-1). If an exponent would be negative, the corresponding coefficient column is identically zero and the minor vanishes identically. The remaining equations are therefore closed and multihomogeneous on the full product of ten projective lines.

For singular masks, perturbing each zero mask entry by a formal parameter keeps the Green denominators fixed. Normalizing each inverse pair by its lowest valuation gives a nonzero projective limit, and the homogeneous equations specialize. The argument covers entirely zero masks and permits poles in scale variables; it does not require any chosen projective coordinate, limiting inverse matrix, or edge weight to stay nonzero.

The independent controls construct 48 legal two-Green targets with singular masks and zero edges, including 10 entirely-zero-mask cases and all-zero edge patterns. Their normalized limiting direction pairs are nonzero, their off-support entries vanish, and their augmented ranks are at most ten. These controls supplement, rather than replace, the general formal-parameter argument.

## 4. Complete transport and actual rank leaves

All necessary off-support 2-by-2 blocks have row and column index sets intersecting in at most one element. Exactly 90 unordered determinants are required. All 90 were independently rebuilt with the positive target, their raw certificate polynomials agree, and their exact arithmetic nonvanishing checks pass.

Consequently each transition C=A_i J A_k^t is invertible on the actual locus, so u_k is projectively J C^t u_i. The complete forest transports entire projective directions. A scalar removed from a whole transition or transport matrix cannot vanish there, because its undivided product of invertible matrices would then be zero. This argument does not silently remove equation contents: quadratic, direction and minor contents are retained separately and tested.

All 78 symmetry representatives were reconstructed. For the 50 row-excluded representatives, the two recorded homogeneous binary quadratics, both contents and their exact resultant agree with the independent computation. Those representatives cover 384 actual cycle pairs.

All 44 rank leaves for the remaining 28 representatives were independently reconstructed from the frozen positive target. This includes the selected quadratic coefficients, complete small-component branches, normalized directions, all scalar guards, actual 11-row minors and their multidegrees. A two-vertex component with x(ax+by) or y(bx+cy) has the two displayed complete projective roots because the retained b guard is nonzero. Columns reconstructed from an invertible block and nonzero row direction are nonzero, so no rank-zero column continuum is dropped.

For the remaining full homogeneous root, the prescribed minor degree is calculated from the original multidegrees, not its observed affine degree. With q=a x^2+bxy+c y^2 and f of prescribed degree d, the independently checked polynomial pseudo-division gives

c^(d-1) f(1,t) = U+V t modulo c t^2+b t+a,
(c U^2-b U V+a V^2) = c^(d-1) Res(q,f).

Where c is nonzero, the root-product definition of the resultant proves this formula with the fixed degree d. Both sides are polynomial identities, so they remain valid when c specializes to zero. There is no specialized division by c. Infinity, repeated roots, a zero form and affine degree drops are retained. The reviewer additionally compared all 44 actual resultants with their full fixed-degree Sylvester determinants at 855 exact finite-field specializations across all four fifth-root embeddings; 728 comparisons have leading-degree drops. Five symbolic fixed-degree identities, 20 specializations and four explicit infinity/repeated-root/zero-form controls pass separately. The finite controls are not the characteristic-zero exclusion argument.

## 5. Both arithmetic mechanisms, with the failed sufficient test retained

For each nonzero p in Q(eta)[g], the complete four-embedding norm P is a nonzero rational polynomial. Writing P(g)=A(g^2)+g B(g^2) gives E(n)=A(n)^2-n B(n)^2, with E(g^2)=P(g)P(-g). Thus a zero of p under any embedding and either real sign forces E(N)=0. This is the correct real-square elimination. The negative-family argument that imaginary and real parts must vanish separately would be invalid here and is not used.

Every one of the 876 retained polynomial checks was independently reconstructed. For 875 checks, the minimum weighted 5-adic valuation and all coefficients of the normalized initial form agree exactly, and the four nonzero residue classes all have nonzero values. Rational denominators are included in the valuation. This proves nonvanishing for every integer N=5m with 5 not dividing m; it is not a finite sweep over dimensions.

The sole unsuccessful sufficient test is representative 87, branch 1, witness 1. Its raw flag remains false, and the initial form x^8(1-x+x^2-x^3+x^4) vanishes at x=4 modulo 5. The independent reconstruction confirms its degree-352 E, its n^8 factor and its primitive residual degree-344 integer polynomial Q with Q(0)=5^48. Every nonzero integer root of Q divides its constant term. A positive integer root with 5-adic valuation one must therefore be 5. The independently recomputed exact Q(5), recorded in `INDEPENDENT_COVERAGE.json`, is nonzero. This completes precisely that leaf without relabeling the failed modular test as a success.

The test also correctly rejects an attempted exclusion of the genuine positive root g=G5 for p=g-G5: its square eliminant is (n-5)^4 and its initial form has a unit root. This is a control against accidentally importing the negative-axis logic.

## 6. Exact symmetry and pair coverage

Dilation by i -> a i mod 5 sends H(g,eta) to H(g,eta^(a^2)) and conjugates both cycles. Transposition, using H^t=H and U'=V^t, V'=U^t, sends (pi,tau) to (tau^(-1),pi^(-1)). Neither operation inverts a direction matrix. Both preserve all coordinate zeros, support conditions and augmented-rank equations. The four-embedding norms supply the required coefficient-field scope.

The reviewer independently checked 100 polynomial dilation identities, target symmetry, and 115,200 support transports over the complete 576-pair universe. The orbit partition is 78 orbits: 12 of size four and 66 of size eight. The actual successor maps, representative membership and transports agree, not merely their counts.

The final independent gate proves a disjoint partition into 384 row-excluded pairs and 192 rank-excluded pairs. All 28 residual representatives have their required one or two complete branches, totaling 44 leaves. It binds every reviewed leaf to its exact frozen file hash. There are no missing cycle pairs, parameters, projective branches or deferred arithmetic obligations in the claimed integer domain.

## 7. Replay and scope

A separate clean directory containing only the eight reviewer programs and the inert frozen source snapshot reproduced all six independent result files byte-for-byte. The 78 author payloads and eight reviewer source files were checked before and after the run. `COLD_REPLAY_RECEIPT.json` records the exact hashes. No network, author program, negative-family program or historical reviewer code was used. The independent coverage gate is PASS for all 576 ordered pairs, 44 rank leaves and 876 polynomial checks.

The accepted scope is the original positive-epsilon two-term fixed-coordinate representation obstruction, for every primitive character and every eligible positive integer N. In particular E_plus is empty, with no lower-size cutoff and no actual exceptions to classify. Empty necessary systems are sufficient for this impossibility conclusion; no sufficiency characterization or block-to-full construction is claimed.

This is not an unrestricted Fourier or FFT lower bound, a novelty assertion, an exact-three full-target upper, or a statement about moduli divisible by 25, unmatched endpoint permutations, other feedback targets, extra summands, products, stability, bit complexity or production performance. It does not alter a source table or close a broader research owner. No external state was changed during this review.
