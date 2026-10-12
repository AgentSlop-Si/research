# Q11 third-pass audit: directed block-rank incidence

Date: 12 October 2026 UTC.

## Verdict

**ACCEPT the new lower bound K >= 20q - 12 in the explicitly restricted Model R.** Together with the independently accepted 20q + 1 legal upper, the restricted minimum lies in [20q - 12, 20q + 1], an additive gap of 13. This does not determine the exact minimum. The broader fixed-partition matching-support model retains only the separately justified 5q support lower bound; neither result is an unrestricted-cycle or general execution lower bound.

The main rank calculation and single-class count below were derived independently from the original target identity before reading the new author draft or the reviewer's derivation. The derivation was recorded before comparison with the candidate report identified by hash below. No source, author, reviewer or historical research program was imported or executed. A new checker supplies the independent finite controls; its scope is recorded separately.

## 1. Original inverse, normalization, field and domain

Freeze m >= 1, q = 483^m, N = 5q^2, s = 5q, h = (N+1)/2, and any primitive complex Nth root omega. Work over L = Q(omega), or any characteristic-zero extension containing it. Define F_ij = omega^(ij), A_ii = omega^(h i^2), and B = (F^(-1)+A)^(-1).

For completeness the inverse identity can be recovered without assuming the proposed lower theorem. The quadratic Gauss sum equals G = q(1+2eta^2+2eta^3), eta = omega^(q^4). Indeed q is odd and coprime to 5. The unique CRT parameterization x = q^2 u + 5v (u modulo 5, v modulo q^2) separates the sum. Write v = r+qt: its inner q-term character sum vanishes unless r=0 because 10h is a unit modulo q. The square-modulus factor is therefore q; the other factor is the five-term sum 1+2eta^2+2eta^3. Since eta is primitive of order 5, direct reduction by 1+eta+eta^2+eta^3+eta^4=0 gives G^2=5q^2=N.

Put T=AF. Completing the square gives

T^2_ij = G omega^(-ij-h j^2) = NG (T^(-1))_ij.

Hence T^3=NG I. The scalar 1+NG is nonzero: otherwise N^3=1, contrary to N>1. Let rho=(1+NG)^(-1), also nonzero. Then

B = rho F(I-T+T^2),
B_ij = rho[omega^(ij) - G omega^(-h(i+j)^2)
            + NG omega^(-h i^2) delta_ij].

This is the unnormalized Fourier convention and the original positive chirp. No root is required to be real. The proof works for every supplied primitive complex root and automatically for all its embeddings. G^2=N implies G is nonzero; no analytic square-root sign is chosen. The frozen family, rather than an arbitrary field or all-length target, is the claimed theorem domain.

## 2. Independent exact block rank

Keep the fixed classes S_a = {a+s u : 0 <= u < q}, 0 <= a < s. Let zeta=omega^s, of exact order q, and x_t=(zeta^(tu))_(u=0,...,q-1). For a != b the diagonal correction vanishes identically. Because s^2=5N and 2h=1 modulo N, direct expansion of the original entry gives

B[S_a,S_b] = C_ab x_b x_a^T + D_ab x_(-a-b) x_(-a-b)^T,
C_ab = rho omega^(ab),
D_ab = -rho G omega^(-h(a+b)^2).

Both scalar coefficients are nonzero. For q>1, two character vectors x_r,x_t are proportional exactly when r=t modulo q: their zeroth entries force the scalar to be one, and their first entries force zeta^r=zeta^t. Thus the left factors coincide exactly when a+2b=0 modulo q, and the right factors coincide exactly when 2a+b=0 modulo q.

If neither congruence holds, both q-by-2 factor matrices have rank 2. Their product with the invertible diagonal coefficient matrix has rank 2. Equivalently its first two rows/columns have a nonzero determinant equal, up to ordering signs, to C_ab D_ab times the two nonzero character differences. There is no possible coefficient cancellation in this case.

If either congruence holds the block has rank at most 1. It is never zero. For any i != j, vanishing of B_ij would give

G = omega^(ij+h(i+j)^2).

It would make G a root of unity, and therefore N=G^2 a root of unity. The positive rational integer N>1 cannot be a root of unity (equivalently N^N != 1). This argument also disposes of the intersection case where both character pairs coincide. In particular no assumption that a target coefficient is generically nonzero is used.

Consequently the exact rank is 1 iff either displayed congruence holds, and 2 otherwise. For q=1 all blocks are scalar and the same criterion says rank 1; q=1 is a control, not a frozen-family instance. In characteristic-zero extensions matrix ranks are unchanged. Arbitrary finite-field specialization is not covered: a primitive specialized root and nonzero inverse guard do not prevent cancellation.

## 3. The single-class incidence inequality

At a=0 the two congruences reduce to b=0 modulo q, since q is odd. Among the s labels there are exactly five such b, namely 0,q,2q,3q,4q. Excluding b=a leaves four exceptional neighbors. The other s-5 neighbors have rank 2. Symmetry of B gives the same rank in both directions. Therefore

I_0(B) := sum_(b != 0) [rank B[S_0,S_b] + rank B[S_b,S_0]]
         = 2[4+2(s-5)] = 4s-12 = 20q-12.

Define Model R explicitly: the base partition is fixed for all summands; each branch has off-class support on a matching of class labels; for every matched pair at most one directed off-class block is nonzero; that block has rank at most 1. Same-class blocks may be arbitrary. These are conditions on the actual summand matrix, so cancellation inside a branch cannot circumvent their stated rank cap.

For a branch H, class 0 has at most one matching partner, and at most one incident directed block of rank <=1. Thus I_0(H)<=1. A block-diagonal correction D has I_0(D)=0, including an arbitrary same-class correction and hence any per-coordinate diagonal calibration. If B=D+sum_(ell=1)^K H_ell, rank subadditivity separately on each directed block gives

20q-12 = I_0(B) <= sum_ell I_0(H_ell) <= K.

Arbitrary signs, coefficient values and cancellation between summands are allowed. Adding diagonal-only branches cannot improve the rank budget. No positivity or common matching is assumed.

The labels satisfying 3a=0 modulo q give the same maximal count. There are three such residues and five lifts of each for the frozen q divisible by 3, hence 15 labels. This extra observation is unnecessary for the a=0 proof. Likewise the global rank-1 count 50q-90 and global rank demand 50q^2-60q+90 give only the weaker 20q-19 bound at q>=483. The sharper theorem does not rely on those aggregate formulas.

At q=483, the lower is 9,648 and the accepted upper is 9,661. At q=1, the incident bound is 8 and the global matching-capacity bound is 10; there is no claim that the incident bound is strongest for every control parameter.

## 4. Why the accepted upper is inside the model

The accepted branch paths list all of S_a consecutively before all of S_b in each paired component. Weighted zero edges separate every matching component. The path Green inverse has entry one when the row precedes the column, and zero across components. Its diagonal endpoint masks place the left factor only on S_a and the right factor only on S_b, so the entire surviving cross-block is one outer product on S_a-by-S_b. The reverse direction is a different branch. The two Fourier/chirp modes are also separate branches.

The singleton component affects only a same-class block. Its duplicated coordinate diagonal is removed by the accepted additional branch with W=0; this branch has no off-class rank incidence. Therefore every one of the 20q+1 accepted branches meets Model R. Different modes sharing the same structural cycle do not change this conclusion or justify fusing them into one uncounted branch.

Zero weights and singular endpoints are source-legal, and all the displayed accepted branch guards are one. The lower is valid even after relaxing the source grammar to allow an uncharged arbitrary block-diagonal correction. Comparing this relaxed lower with the original legal upper is legitimate and does not assert that a free diagonal is allowed in the original representation.

## 5. Necessary boundaries and a concrete broad-model witness

A matching support restriction alone does not imply the unit rank-incidence capacity. For two three-vertex classes A=(a0,a1,a2) and B=(b0,b1,b2), use one zero-cut path in the order

a0,b0,a1,b1,a2,b2,

with all internal weights one and both endpoint diagonals equal to the identity on this part. Other matching parts can be separated by zero edges while the structural cycle stays Hamiltonian. Its A-by-B block is

[1 1 1; 0 1 1; 0 0 1],

of rank 3, and its B-by-A block is

[0 1 1; 0 0 1; 0 0 0],

of rank 2. Thus one entirely legal broad matching-confined branch has incident rank 5 at this class, not 1. Interleaving q vertices in each class similarly gives ranks q and q-1. This is outside Model R but inside the broader matching-confined Model M.

For Model M, nonzero target off-class blocks force the matchings to cover every pair. Since odd s labels give at most (s-1)/2 edges per matching, K>=s=5q. This is a support count. Arbitrary matching-supported matrices can realize arbitrary target off-class blocks in exactly s round-robin summands, so support alone cannot force a larger universal count for that enlarged class; this does not show s legal Green branches suffice for B.

Changing the base partition by branch, connecting one class to multiple partners, using unrestricted effective paths/cycles, non-diagonal mixing, or allowing an off-class correction defeats the specified inference. The theorem is not an unrestricted Green-branch lower bound. Its branch count is not a general arithmetic, bit, FFT, or shared-execution lower bound. The separately stipulated per-branch row-visit execution bound requires that execution rule; a shared or compiled two-DFT evaluation remains outside it. No historical-priority, stability, negative-chirp or all-N result follows.

## 6. Evidence and source binding

The accepted upper archive was independently hashed and matched exactly:

Q11_Subquadratic_Matching_Green_Bridge_Independent_ACCEPT_2026-10-12.zip
SHA-256 604a419f89bd0cb79e53448d39a37798bbef05e01bccc3d3421c98a2beec6a32.

Its top-level REVIEW.md was read directly as inert archive data and compared byte-for-byte with its retained accepted copy. The accepted upper explanation was also pinned. CHECK_RESULTS.json records the actual digests and executed checks.

The newly authored standard-library checker independently constructs integer cyclotomic polynomials and exact powers, reconstructs the scaled original B entries, checks the original defining matrix product at N=5 and N=45, verifies the Gauss sum and guards, tests exact block-rank minors at q=1,3,7 and multiple primitive-root embeddings, enumerates the full q=483 congruence count, and checks literal masks plus the broad interleaving counterexample. It includes an exact finite-field cancellation counterexample to prevent interpreting such images as the characteristic-zero theorem. Small controls are outside the frozen family and are clearly labeled. Uniform correctness comes from sections 1-4; no full q=483 field matrix or 9,661-branch execution is claimed.

No external writes were performed. Broader Q11 remains open.

### Executed check totals and sealed candidate comparison

The fresh run passed 26,320 exact cyclotomic 2-by-2 minor checks, 2,840 nonzero off-block pivot checks, 4,100 defining-product entry checks, and Gauss-sum/inverse-guard checks in all six controls. The q=7 checks include 300 blocks per embedding in which exactly one proportionality congruence holds, while q=3 also covers the double-proportional intersection cases. These tests use embedding powers 1 and 2, both units modulo each odd N. All 5,829,810 ordered off-class pairs at the actual q=483 parameter were enumerated by congruence, not by a million-dimensional field-matrix construction.

After the proof and controls were finished, the reviewed report was compared byte-for-byte with its member in the sealed candidate archive. Candidate SHA-256: b18474cbeabc044a4183f7e90ac7064c1514ca588aaa31e91c47a8a42d7d89e8 (428,595 bytes). Reviewed report SHA-256: 0ba9ec4f888ec18b6abddd086ae64e6dc71aedaeb568e6310f6be34854461321. CANDIDATE_BINDING.json records this comparison. This third pass checks the new incidence theorem and its boundaries; the separate first reviewer owns the candidate-wide manifest and source-pin audit.

Public derivative note: private tracking or coordination details are omitted and source links are localized. Original report SHA-256: `ffae1e8db162c4842aad5cef7b9ea0a111fc3caa26481598c09f3d45a26ee774`.
