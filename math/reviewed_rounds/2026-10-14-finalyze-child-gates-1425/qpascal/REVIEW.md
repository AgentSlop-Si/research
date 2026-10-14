# Independent review: q-Pascal middle-operator transport obstruction

Date: 14 October 2026

## Verdict

ACCEPT at the stated algebraic scope. For every even N >= 2, every field k containing a primitive Nth root q, and every c in k with c != 0, any matrix K satisfying K H_q(L) = H_q(cL) K obeys rank(DR - K) >= N/2, with D and L defined below. The exact determinant identity in the submitted proof is also correct.

This closes the specific attempt to replace the Fourier middle by an exact scalar-phase transporter with a sublinear-rank additive correction. It does not close ALG-021, ALG-022, or the full-output Fourier evaluator problem. No new asymptotic algorithm, unrestricted arithmetic lower bound, or historical-priority claim follows.

A simpler independent proof shows that the rank bound is an elementary triangular-versus-antidiagonal obstruction. It does not require the special q-Pascal diagonal or the computed determinant. The determinant remains a valid, separately checked specialization.

## Exact hypotheses and definitions

Let N = 2m >= 2 and let q have multiplicative order N in a field k. Necessarily the characteristic does not divide N, so it is not 2. With indices 0 through N-1, define

- f_0 = 1 and f_j = product_(a=1..j)(1-q^a).
- H_q(z) = sum_(j=0..N-1) z^j/f_j.
- d_j = (-1)^j q^(j(j-1)/2)/f_j and D = diag(d_j).
- L is the lower nilpotent shift, L_(i+1,i) = 1; R reverses coordinates.
- T = H_q(L), M = DR, S = diag(f_j).

Every denominator and d_j is nonzero. The Fourier convention is positive-sign and unnormalized, F_(i,j) = q^(ij). Its classical factorization is F = S T D T^transpose S = S T M T R S. K need not be invertible, and c need not be a power of q. All statements are exact field-algebra statements, not floating-point or bit-complexity claims.

## Audit of the submitted proof

1. Write h(z) = H_q(z)-1. Its linear coefficient 1/(1-q) is nonzero. A compositional inverse g modulo z^N exists over k without factorial divisions. From K h(L) = h(cL) K, substitution of g gives K L = c L K. The converse follows by evaluating the polynomial H_q. This argument works in positive characteristic as well as characteristic zero.

2. Since R L R = L^transpose, B = M L M^(-1) = D L^transpose D^(-1). Its superdiagonal is d_i/d_(i+1) = q-q^(-i). The tridiagonal matrix B-cL has determinant recurrence delta_0 = 1, delta_1 = 0, delta_r = c(q-q^(-(r-2))) delta_(r-2).

3. Therefore det(B-cL) = c^m product_(j=0..m-1)(q-q^(-2j)). The element q^(-2) has order m, while q^m = -1. Applying product_j(1-a(q^(-2))^j) = 1-a^m at a=q^(-1) evaluates the product to -2. Thus det(B-cL) = -2c^m != 0. All signs and index boundaries check.

4. If E=M-K, then M L-c L M = E L-c L E. Its rank is N by the determinant computation, while rank(E L-c L E) <= 2 rank(E). Hence rank(E) >= m.

No gap was found in these steps. The proof's exclusion is algebraic. High rank alone does not imply high application cost.

## Independent shorter proof and stronger scope

The equation K L = c L K gives K_(i,j+1) = c K_(i-1,j), with a zero boundary above row 0. It follows inductively that K_(i,j)=0 whenever j>i. Equivalently, for c != 0, K=diag(1,c,...,c^(N-1)) P(L), where deg P<N. Thus every legal transporter is lower triangular.

Take rows 0,...,m-1 and columns m,...,2m-1 of E=DR-K. K vanishes on this entire square block. The corresponding block of DR is antidiagonal, with nonzero antidiagonal entries d_0,...,d_(m-1), so it has rank m. A submatrix cannot have greater rank than the whole matrix. Therefore rank(E) >= m immediately.

This proof applies to any invertible diagonal D and any polynomial H with nonzero linear coefficient, with the corresponding scalar-shift intertwining relation. It gives floor(N/2) for odd N as well. Odd N and c=0 are boundary controls for the nonzero determinant formula; they are not counterexamples to every rank obstruction. In fact, for c=0 the intertwining implies K L=0, and rank(DR-K) >= N-1.

Any finite sum of scalar-phase transporters is still lower triangular. Consequently a decomposition M=sum_r K_r+E, with every K_r intertwining H(L) and H(c_r L), also requires rank(E) >= N/2. This modest extension concerns additive sums in exactly the same coordinate/shift model; it does not exclude changed factorizations, products, other transports, or cheaply applicable high-rank corrections. It is not a historical-novelty claim.

## Fresh finite verification

The supplied verify_transport.py was read as inert text and was not executed or imported. A new standard-library script, independent_audit.py, was written for this review. It verifies complete Fourier matrix identities directly from scalar sums, constructs the conjugated shift from M and M^(-1), uses a general finite-field elimination routine, and checks the pair-collapse coefficients.

Results are PASS:

- Freshly reproduced all 283 reported determinant-phase cases, all 180 reported correction cases and their exact minimum sampled ranks, and 48 boundary/mutation controls.
- Additional exhaustive nonzero-phase tests: 1,562 determinants across 65 primitive-root/prime-field/size fixtures, using primes 3 through 43 and even dimensions through 12 where roots exist.
- Exhausted all 5,000 polynomial transporters for N=4 over F5, across both primitive fourth roots and all four nonzero c. Each case obeys the rank bound. The minimum is 2 in all eight root/phase combinations. For example q=2,c=1,P(L)=4L+2L^3 attains rank(M-K)=2. This is a bounded sharpness example, not a proof of sharpness for all N.
- Independently solved 12 complete linear intertwiner systems at dimensions 2,4,6,8; their dimensions are exactly N, agreeing with the transporter characterization.
- Odd-dimension controls at N=3,5,7 have zero determinant and defect rank N-1 as expected.

The all-field, all-even-N acceptance comes from the proofs above. These finite checks are corroboration, not a replacement for proof or a runtime result.

## Comparison with the existing research record

The live canonical Catalogue was read on 14 October 2026. ALG-021 is row 132; ALG-022 is row 17. The matched Research overview rows are 193 and 21. F096 is a source-family reference shared by the records, not a separate stable task ID and not an independently closable row.

ALG-021 already accepts the complete-orbit identity in a truncated ring for a prescribed sequential same-input path, and explicitly excludes silently replacing the true middle diag(d)R by the alternating-sign diagonal. Its remaining arbitrary-Fourier embedding and source-comparison obligations are unchanged. The reviewed source hash is e0b4fdd1981b636632721e7d44dbe81d68b94fe5d19f0acaba57b1335de8f423; the exact archived text was retrieved and its hash matched.

ALG-022 already accepts the classical q-Pascal Fourier factorization, charged preparation and restricted streaming/Hankel results. Its live record keeps the fresh-input faster kernel evaluator open and records total online cost 2C(N)+O(N). The reviewed source hash is bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0; the exact archived text was retrieved and its hash matched.

The present theorem strengthens the recorded warning about illegal middle substitution into a uniform rank obstruction. It does not provide a fresh-input kernel executor, remove the cost of TET, or change the borrowed compiler's previously audited asymptotic comparison. The live priorities 34 for ALG-021 and 53 for ALG-022 should not be changed on this evidence alone; they are work priorities, not novelty probabilities.

The q-Pascal convolution kernel here has coefficients 1/f_j. No FCML bank-moment identity or runtime claim was used or transferred to this kernel.

## External source and classical-fact comparison

Kuznetsov, arXiv:1507.02959v2, Theorem 1 gives V_q=L D L^transpose with L=P_q T_q P_q^(-1). Moving the diagonal P_q factors recovers exactly the submitted S T diag(d) T^transpose S convention. Theorem 2 supplies related triangular Toeplitz identities. The field extension here is justified by the finite rational identity after clearing denominators; the cited paper states its theorem over complex q. The factorization itself is established prior work.

Primary source: https://arxiv.org/html/1507.02959v2

Dumas and Grenet, arXiv:2302.13600v7, Section 6.3, Algorithm 57 and Proposition 58 state the overwrite triangular-Toeplitz upper bound O(M(N) log N), with the displayed two-half-size recurrence. Substitution M(N)=O(N log N) yields O(N log^2 N). This confirms the candidate's bounded source check. It does not prove a lower bound or exclude a better algorithm, and accumulating routines with separate input/output banks must not be silently treated as the same overwrite contract.

Primary source: https://arxiv.org/pdf/2302.13600v7

The intertwiner/commutant facts, submatrix rank bound and rank-subadditivity argument are elementary linear algebra. The shorter proof especially limits any originality claim for the rank inequality. No global literature search or historical-priority clearance was completed for the specialized determinant formula, and none is needed for this correctness verdict.

## Status recommendation

Add one scoped accepted obstruction note to the existing ALG-021/ALG-022 records: exact scalar-phase transport of the actual Fourier middle cannot be achieved with an o(N)-rank additive repair. If the table tracks this specific low-rank-repair subroute, mark that subroute closed by obstruction. Keep both parent rows open and preserve their other obligations. Do not create an additional F096 task or increment a discovery count merely for this specialization.

The next relevant mathematical question remains a full, charged algorithm for a structured high-rank residual, or a different legal factorization with a proved cost recurrence. Cheap E does not make TET cheap. Multiple transports in a different algebraic layout and unrestricted Fourier circuits remain outside this result.

No table, GitHub, or other external write was performed in this review. No preview-limit error was encountered.

## Provenance

Candidate: QPascal_Transport_Proof_and_Checkpoint_2026-10-14.zip, 11,033 bytes.

Library ID: libfile_b8dbb9a0c39c8191b7d8cbd7645d2a89.

Archive SHA256: a414ccad6b123902868c30fed17d95c7a6139064fdb20464c3d946182187a95e.

All five internal manifest entries matched their bytes. Submitted PROOF.txt SHA256: 33a026b5454df48e56ef2b4850c07879a407dc51ff159f0a2e6fa12dd8d7e4e5.

Originating conversation: https://chatgpt.com/c/6acd233a-4f4c-83ed-bff5-de0ef1cc8c2f?messageId=f969091b-aea4-57e5-b78c-9534d2d401de

Canonical table: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit
