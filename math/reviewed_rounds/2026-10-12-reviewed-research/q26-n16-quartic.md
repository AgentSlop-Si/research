Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: ca7a6a3e923f66184f9d22387dbebde33a6d6155903b12354f767e65913d151e

---

# Independent review: Q26 Phase39 N16 quartic exhaustion

## Finite result being reviewed

For the exact original Phase39 seven-Green family at N=16, every one of the 10,483,200 ordered assignments of two distinct middle rows and four distinct middle columns has a nonsingular fixed 15-row minor of the 18-by-15 quartic coefficient matrix. This has been independently exhaustively reproduced over both fields 998244353 and 2013265921. The three quadrics are q01, q02, q13. The selected zero-based rows are 0 through 10 and 12 through 15, with bit mask 63487. Every mapping has rank 15.

This is an exhaustive quartic-certificate upgrade at one already cubic-certified size. It is not a newly excluded size, a new arbitrary-family obstruction, an all-N theorem, a Phase38 promotion, or an FFT algorithm.

## Exact model and gauge cancellation

The fixed model is

F = A D1 P1 (G2 + lambda G3 + mu G6) P2 D2 C,

where A = G0 + ((1+i)/3)G1, C = G4 + ((1-i)/4)G5, each Gs = (I-alpha_s Ws)^(-1), all seven cycle orderings and resolvent parameters are fixed, the two middle coefficients range independently over the complex numbers, and both internal masks are arbitrary invertible diagonal matrices with arbitrary internal permutations. The target is the positive-exponent, unnormalized Fourier matrix.

Let T = A^(-1) F C^(-1), and B(x) = x0 G2 + x1 G3 + x2 G6. Any proposed factorization gives a nonzero projective x and induced ordered middle indices r0,r1 and c0,c1,c2,c3. For a pair a,b of target columns,

q_ab = T[0,a]T[1,b] B[r1,c_a]B[r0,c_b] - T[0,b]T[1,a] B[r1,c_b]B[r0,c_a].

Substituting the masked equality makes both terms the same product of row and column mask entries. Thus each q_ab vanishes. No division by a middle-pencil entry is used, so there is no lost zero-coordinate branch. Homogenizing includes x0=0 and therefore proves a stronger exclusion than the affine chart x0=1 alone.

## Why a nonsingular quartic minor is a certificate

The rows of K4 are the six degree-two monomial multiples of each of q01, q02, q13. Its 15 columns are all degree-four monomials in x0,x1,x2. Rank 15 says these multiples span every quartic monomial. At a common nonzero projective root all rows, hence every quartic monomial, would vanish. A nonzero coordinate has a nonzero fourth power, contradiction. Therefore no proposed induced mapping can realize the target.

The older cubic certificate uses four quadrics q01,q02,q03,q12, each multiplied by the three linear monomials, giving a 12-by-10 matrix. Complete N16 cubic results do not by themselves certify the three-equation quartic matrices; the original source explicitly described N16 quartic as 100,000 sampled mappings per prime.

The anchored star q01,q02,q03 has a common projective basepoint where both middle-pencil entries at column c0 vanish. It cannot provide this full-rank homogeneous exclusion. The independent control finds rank 14, as expected.

## Why enumeration is exhaustive

There are 16*15 ordered distinct row pairs and 16*15*14*13 = 43,680 ordered distinct column quadruples, giving 10,483,200 mappings. Every pair of full internal permutations induces exactly one such partial assignment. Conversely each assignment extends to full permutations. The excluded mappings therefore cover all internal permutation pairs even though full permutations were not individually enumerated.

The reviewer used a distinct traversal: cyclic row offset delta=1..15, then r0=0..15, with r1=(r0+delta) mod 16, and recursive available-column traversal. Each sextuple was encoded as six four-bit digits in a 24-bit integer. A visited array rejected duplicates; exactly 10,483,200 distinct keys were found in each complete run. All 240 row-pair ledger records, each with 43,680 assignments, agree individually with the candidate's determinant products and sums.

## Valid specialization to characteristic zero

The coefficient field is Q(zeta16), with i=zeta16^4. Both prime fields admit the specified primitive 16th root, and the input reconstruction verifies zeta16^8=-1. The rational denominators, all seven Green denominators 1-alpha_s^16, and determinants of A and C are nonzero after reduction. Hence the matrix entries belong to a localization with well-defined reduction into each field. A nonzero modular determinant proves that its algebraic characteristic-zero value is nonzero. One valid prime would suffice for each mapping; both were independently checked. No inference is made from a zero modular determinant.

## Independent computation and controls

The reviewer did not import or execute any original source program. The exact input was reconstructed from seeded/frozen cycle definitions using the analytic cyclic Green formula alpha^distance/(1-alpha^16), rather than the candidate builder's sparse-matrix inverse construction. Each Green inverse identity and A*T*C=F were checked. Reconstructed bytes match the original source ZIP and the candidate input pins.

The exhaustive review code independently computes quadratic coefficients by ordered variable-pair convolution; constructs the transpose of the fixed minor; and performs pivot-row-normalized elimination. Its row-pair ordering differs from the candidate, and visitation is explicitly verified. Separate Python sparse-polynomial and incremental row-basis code verifies the full 18-by-15 rank and determinant at all 106 dispersed witnesses per field, including the first and last mapping.

Controls include determinant signs, rank-14 and zero matrices; an identity-mapped B(1,7,11) planted target of exact rank 14; nontrivial row and column permutations and invertible masks on seven projective-support branches, all rank deficient (13 or 14); anchored-star rank 14; zero target and zero pencil rank 0. Deficiency is only a control outcome, not evidence of a Fourier factorization.

## Numerical fingerprints

- p=998244353: 10,483,200 nonzero fixed minors; product 765744317; sum 479976063; first determinant 824479582.
- p=2013265921: 10,483,200 nonzero fixed minors; product 958214106; sum 589643050; first determinant 278436587.

## Scope and remaining work

Only the fixed Phase39 N16 quartic three-equation certificate is now exhaustive in both exact primes:10,483,200 induced mappings per prime, all rank15. Larger N32,64,128,256 remain sampled. Phase38 is unchanged. This is not a new all-size exclusion or faster FFT.
