# Independent audit: spectral determinant and adjacent-tail gate

9 October 2026. This supplements the 16:28 Fourier checkpoint. It does not replace or silently recount that snapshot.

## Result

The new exact F8 necessary identities are valid. A fresh exact characteristic-zero reconstruction matches all 898 coefficients in the quartic Q, the three upper resultants R1/R2/R5, and the cubic W. The exported five-variable coefficient circuit also matches exactly, including its nonzero witness. The Jacobian witness proving algebraic independence of the four displayed polynomials is reproduced exactly. A separately written GF(17) enumeration reproduces every submitted counter, including zero full second-stage successes among 2,546 invertible candidates.

There is still no exact factorization, characteristic-zero nonexistence certificate, or sub-N-log-N arbitrary-input transform. Necessary polynomial identities, algebraic independence, a finite-field exclusion and a computational complexity result are different assertions.

The most useful advance is the adjacent-column tail lemma. It supplies two necessary equations without the earlier onion reconstruction's S or Delta divisions. It can therefore help analyze some of the excluded onion loci, while retaining its own separated-generator and invertibility assumptions.

## Source and provenance

The source is `fft_spectral_determinant_gate_2026-10-09(1).zip`, Library file `[private-id]`, version 0. It has 367,990 bytes and SHA-256 `bacf14578c7631c923beed1a65aebf74989ed573cbd88725a95ece41b9391571`.

The archive has 33 top-level members and 194 recursive member occurrences, with 180 unique byte contents. There are 29 byte-new contents compared with the declared union of the baseline, 14:50, 15:20 and 16:28 source inventories and top-level source hashes. Every one of the 490 embedded manifest entries passes. The nested `previous_research_checkpoint.zip` is byte-identical to the 16:28 dual-support/onion archive (`c9d5d352508985292f80a035a113ab33611c9dbde9df5c20fab9f503af63a1f9`). It is inherited evidence rather than another new research branch.

`SOURCE_MEMBER_INVENTORY.json`, `NEW_UNIQUE_CONTENT.json`, `PRIOR_HASH_REFERENCE.json` and `PROVENANCE_VERIFICATION.json` make these comparisons reproducible. Newness refers to byte contents relative to that snapshot, not publication priority or intellectual novelty. Uploaded Python was treated only as text. No uploaded program or embedded binary was executed or imported.

## 1. Model and inherited assumptions

Let z be a primitive eighth root, F[i,k]=z^(ik), and P=[7,0,6,3,4,1,2,5]. The inverse-stage representation uses C=A^-1 and B[:,j]=(F C)[:,P[j]]. The normalized C chart has diagonal 1, lower entries L_i V_j, and upper entries H_i eta_j, with L_7=eta_7=1. The original two-stage problem additionally needs the corresponding A inverse and stage-corner conditions covered in the preceding audit. Diagonal normalization of A and diagonal normalization of C are different charts.

The eight coordinates are (t,h0,h1,h2,h6,beta,gamma1,gamma2). The inherited Fourier-support conditions give H0..H5 as the three-character sequence with roots 1,z^-1,z^-2; H6=h6 is free and H7=1. For 1<=k<=6,

L_k = [a+b z^-k+beta H_k]/t,
b=(t-1+beta(h0-1))/(z-1), a=1-beta h0-b.

This representation has t!=0 and the inherited endpoint normalizations. Full rational reconstruction additionally excludes h0=0, S denominators, Delta pivots and a boundary determinant. Invertibility and nonzero stage corners are separate guards. A new division is a new branch assumption.

The family uses globally separated off-diagonal generators. A result for this family must not be promoted to arbitrary quasiseparable rank-one matrices, arbitrary internal permutations, more stages or unrestricted FFT algorithms.

## 2. Lower quartic and upper resultants

For rows i=4..7, column k=3 of C transforms as

eta3 * sum_(r<3) z^(ir) H_r + z^(3i) + V3 * sum_(r>3) z^(ir) L_r.

The lower B restriction forces compatibility with the Fourier transform of C's final column. The four vectors consisting of the head sum, tail sum, diagonal spike and final-column transform have zero determinant. Scaling the tail column by t(z-1) gives Q. The reconstructed determinant is exactly the submitted 45-term polynomial, degree 4, with

Q=t A(h)+beta B(h)+C(h),

and term counts 12,21,12 in A,B,C. There are no t*beta terms or powers greater than one in t or beta. Only on B(h)!=0 can one set beta=-(t A+C)/B.

For the upper conditions, let q_a(r)=z^(ar)-gamma_a. At original C column k, a row proportionality condition is

eta_k sum_(r<k) q_a(r)H_r + V_k sum_(r>k) q_a(r)L_r + q_a(k)=0.

The determinant of the three coefficient rows for a=1,2,3 must vanish. Scale the L column by t(z-1), split the third row linearly in gamma3, and call its determinant A_k-gamma3 B_k. The pairwise resultants with k=4 are R_k=A_4 B_k-A_k B_4, k=1,2,5. Fresh characteristic-zero polynomial arithmetic gives precisely the submitted degrees 7 and term counts 192,300,330.

These operations do not divide by an upper gamma pivot, S or Delta. They nevertheless retain the underlying normalized generator and row-proportionality chart. Their vanishing alone is not sufficient for a B stage: pairwise resultants may vanish when leading coefficients degenerate, and they omit many residual identities.

The Jacobian minor of (Q,R1,R2,R5) in coordinates (t,h0,h1,h2), evaluated in GF(12289) at the submitted point with z=8246, is 10570. Every entry of the submitted Jacobian is independently reproduced. Since z^4+1 vanishes in this valid reduction, a nonzero modular value certifies a nonzero characteristic-zero polynomial minor. The characteristic-zero Jacobian criterion then gives algebraic independence. It does not imply an empty common zero set or establish the codimension of its zero fiber.

## 3. The five-variable circuit

Each R_k is jointly affine in gamma1,gamma2, without their product. Write its coefficient row in the order (1,gamma1,gamma2). Each coefficient is at most quadratic in beta. The determinant G of the three rows is a necessary condition.

With m=-(t A+C), replace each coefficient e0+beta e1+beta^2 e2 by B^2 e0+B m e1+m^2 e2. The determinant H of this new matrix satisfies the exact rational identity H=B^6 G(t,h,m/B). This proves the advertised necessary condition on B!=0. The entire exported coefficient circuit was compared exactly, not merely evaluated at sample points. At the supplied witness over GF(12289), B=12110, m=11930 and H=4730.

The B=0 locus is unresolved. A gamma determinant can become singular after imposing tail constraints; dividing it would silently delete a potentially important branch. Determinants and resultants are useful necessary projections but do not by themselves preserve all solution information.

## 4. Adjacent-column tail lemma: proof without onion denominators

Let u=C[:,1], v=C[:,2], and let T denote the Fourier transform restricted to rows 0..4. The corresponding B columns are 5 and 6, so their restrictions Tu,Tv span at most a line. In time coordinates 3..7, u=V1 L and v=V2 L share the same tail.

The first three Fourier columns restricted to these five rows form a Vandermonde matrix of rank 3. If V1=V2=0, both u and v would be supported on coordinates 0..2, so the rank-one condition on Tu,Tv would contradict independence of C's columns. Thus at least one tail coefficient is nonzero.

The vector w=V2 u-V1 v is nonzero by column independence and is supported on coordinates 0..2. Injectivity on that head space makes Tw nonzero. It belongs both to the head Fourier image and to span(Tu,Tv); hence the latter is exactly the line through Tw. Taking u or v with nonzero tail coefficient and subtracting its head contribution shows that the Fourier image of the common tail lies in the head image.

Consequently there is a head vector whose subtraction from the tail has Fourier coefficients zero at 0..4. Fourier inversion makes its time samples a combination of z^(3k), z^(2k), z^k. On coordinates 3..7 this means

E3=L6-s1 L5+s2 L4-s3 L3=0,
E4=L7-s1 L6+s2 L5-s3 L4=0,

where s1=z+z^2+z^3, s2=z^3+z^4+z^5 and s3=z^6.

This proof does not use h0, S, Delta, an upper corner anchor, or rational reconstruction of the interior generators. It uses invertible C, shared separated tails, and the actual rank-one upper B constraint. Substitution of the explicit L formula still needs that formula's normalization and t!=0. This distinction is useful when applying the lemma to exceptional onion branches.

After multiplying E3,E4 by t(z-1), all three equations E3,E4,Q are affine in (t,beta). Their 3-by-3 coefficient determinant W must vanish. The independently expanded result matches all 31 submitted terms and has degree 3 in (h0,h1,h2,h6). At (2,3,5,7), z=8246 in GF(12289), it equals 9966. Thus it is a genuine nonzero characteristic-zero necessary polynomial.

The 2-by-2 tail coefficient determinant used to solve (t,beta) is itself a nonzero affine polynomial in the four h coordinates (five terms). It is an additional open-locus guard. W=0 is not sufficient, and the zero-pivot branch is not excluded. `independent_tail_coefficients.json` supplies all three coefficient rows and that pivot exactly for subsequent saturated elimination.

A bounded extra check confirms that neither h0, the new tail pivot, nor Q's beta coefficient divides W in Q(zeta8)[h0,h1,h2,h6]. Thus W is not simply a multiple of any one of these tested guards. This does not classify its components or establish a valid factorization branch. A full exact factorization attempt was stopped when it did not finish promptly; factorization and irreducibility remain undetermined.

### A modest general form

The argument extends directly: for two independent columns with a common tail outside a head of s consecutive time coordinates, if their transforms on r consecutive frequencies are rank one and r>=s, the Fourier-Vandermonde head map is injective. The common tail, after a head correction, lies in the span of the N-r omitted Fourier characters. Its samples satisfy the corresponding order-(N-r) recurrence wherever enough consecutive tail samples remain. This is a necessary structural lemma, with no complexity claim.

## 5. Finite-field search and its exact limitations

The independent search in `finite_field_audit/` uses three-mode interpolation, direct Fourier determinants, fresh modular linear solves and all 289 gamma pairs for each eligible h tuple. It does not run the uploaded enumeration or polynomial solver. It reproduces every source counter:

- 78,608 h tuples (h0!=0) examined
- 4,624 singular tail linear systems omitted
- 4,352 solutions with t=0 omitted
- 4,596 survivors of tail equations and Q
- 17,829 gamma pairs satisfying the selected upper conditions
- 12,358 fail reconstruction: 11,648 denominator cases plus 710 alpha=0 cases forcing dependent columns
- 2,546 invertible C candidates
- Zero candidates even satisfying all 30 tested necessary B minors

It evaluates 1,328,244 gamma pairs. Of the 2,546 invertible candidates, 619 fail at least one additional B or inverse-C corner guard; 1,927 satisfy all four. The source's 2,546 is therefore a tested superset of the fully corner-regular candidates. This strengthens the bookkeeping precision without weakening the rejection: every candidate, even in the superset, already fails a genuine B minor.

The disjoint first-failure reconstruction counts are S1=0: 5,483; boundary determinant=0: 1,292; Delta=0: 4,873; and alpha=0: 710. Alpha is not a denominator. Its vanishing forces C columns 6 and 7 to be proportional, independently verified in all 710 cases. Those cannot give invertible targets; the other 11,648 are unresolved denominator branches.

This enumerator never divides Q's beta coefficient: it retains 863 such zero-coefficient lower survivors, including 444 invertible candidates. It also retains singular gamma systems, including 740 rank-one and 18 rank-zero coefficient matrices. The separate five-variable H circuit's nonzero-beta-coefficient chart must not be imposed on the enumeration.

This is an exhaustive negative result over GF(17), z=9, on the enumerated open branch. It leaves h0=0, t=0, singular tail systems and zero rational-chart denominators unresolved. More fundamentally, a complex solution need not specialize to a GF(17)-rational point. Neither the field enumeration nor algebraic independence can substitute for an exact characteristic-zero saturated-ideal certificate.

## 6. The two-boundary-defect identity

The all-length identity is a direct Fourier-support calculation. If H* is an N-sample combination of characters 1,z^-1,z^-2 and H agrees with it except at N-2,N-1, its transform for i>=3 is

(H_(N-2)-H*_(N-2)) z^(-2i) + (H_(N-1)-H*_(N-1)) z^(-i).

The normalized chart sets H_(N-1)=1. Orthogonality of roots proves the identity for every N admitting the stated distinct characters over characteristic zero, and over a field where N is invertible and z has exact order N. It is not inherently limited to the source's four tested lengths.

A fresh exact check interpolates the three characters independently and tests N=8,16,32,64,128 in GF(257) and GF(65537), with two root embeddings each. All 9,320 exact row checks pass. This is a control for the symbolic identity, not an exact two-stage factorization or an algorithmic speedup.

## 7. How this should be fused into the project

1. Retain the prior twelve-equation, eight-coordinate chart and exception-complete lift. Q, R, H and W are necessary projections and aids, not replacement sufficient systems.
2. Add the two denominator-free tail recurrences to the exceptional-branch analysis before imposing S and Delta nonvanishing. Retain all original matrix identities and invertibility constraints.
3. On the nonzero tail-pivot branch, substitute t,beta and keep W with the complete residual equations. On the zero-pivot branch, keep the two linear equations undivided and analyze ranks/compatibility separately.
4. Use the existing complete separated-generator lift to cover endpoint, normalization and corner-zero cases. Any exclusion needs proper saturation and an exact certificate over Q(zeta8), not just GF(17).
5. Keep this algebraic branch separate from the approximate v9 error guarantee, sparse-spectrum exact recovery, independently ordered Green sums, unitary entropy, and Harper covariance tests. It neither improves the numerical precision theorem nor bypasses their architectural restrictions.

A positive fixed-F8 solution would still need extension to arbitrary size, verification of every Fourier coefficient and a fully charged evaluator. A negative fixed-permutation F8 result would still not prove a general Fourier arithmetic lower bound.

## Reproduction and evidence labels

Run `python3 audit_provenance.py`, `python3 exact_audit/independent_exact_check.py`, `python3 exact_audit/independent_defect_check.py`, `python3 exact_audit/independent_guard_check.py`, and `python3 finite_field_audit/independent_gf17_audit.py`. Python and SymPy are required for the characteristic-zero check; the finite-field scripts use their documented dependencies.

The uploaded `REGRESSION_LOG.txt` remains a source-reported test log. The present exact results, enumeration and defect controls are independent computations. The mathematical arguments above explain their scope; computational witnesses are not silently upgraded to broader theorems. No publication-priority claim is made.
