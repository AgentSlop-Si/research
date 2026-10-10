# Independent audit of the v34 cyclotomic support gate

Completed 10 October 2026. The source's seven-nonunit-edge theorem passes in its stated integral model. A bounded independent extension proves more: **the fixed 99-edge topology has no factorization of the unnormalized Fourier matrix F11 over the cyclotomic valuation ring at 11**, even when any of the allowed edge coefficients may vanish. The extension also holds over valuation-ring extensions with residue characteristic 11 in which the chosen primitive eleventh root reduces to 1.

This does not exclude algebraic weights with poles at that valuation, unrestricted complex weights, or different circuit supports. No Fourier assignment or faster FFT is constructed.

## Frozen source and audit independence

- Source conversation: [private source location omitted]
- Source ZIP: `fft_cyclotomic_zero_forcing_v34.zip`, Library ID `[private file identifier omitted]`.
- ZIP SHA-256: `b0dc809824d222b82225632b43517fc60c9085935c674166a2d956d4f2e1eb97`.
- Accompanying proof: Library ID `[private file identifier omitted]`, SHA-256 `c0af0cfc4e260ed62d12572752e0c954f1c6ec10938ee61976fbcf847f680def`. Its bytes equal the ZIP's `RESEARCH.md`.
- All 16 entries of the source SHA-256 manifest pass. The embedded predecessor ZIP has hash `8daa679b23eadec2862fc8f3c4828a3bb87b469fb79536936436522fc5d04020`, matching the accepted v33 audit. The unchanged topology hash is `4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b`.
- No supplied program was executed, imported, linked, or used as an executable dependency. The supplied JSON and proof were read as data. Fresh audit programs are `audit_forcing.cpp`, `audit_arithmetic.py`, `verify_restricted_certificates.py`, and `audit_summary.py`.
- The forcing computation uses stopping-set enumeration and an upward Boolean zeta transform, not the source's forward propagation search. A second implementation verifies every restricted-support certificate by Python set operations and explicit triangular-minor checks.
- All work remained local; no external file was created, changed, or uploaded.

## The original seven-edge gate passes

Each of the three 11-by-11 support layers has 33 distinct positions and degree three in every row and column. The audit reproduces every minimum-seed histogram for deletions of 0 through 5 edges: 284,274 support masks per layer and 852,822 masks in total. These are separately enumerated layer patterns, not a purported enumeration of all corresponding joint 99-edge deletion sets. The independent search considers all seed sizes through 11, so it does not silently cap a failing case at the expected answer.

The maximum forcing numbers at deletion counts 0,1,2,3,4,5 are:

- A: 2,3,3,3,3,3.
- B: 2,3,3,3,3,4.
- C: 2,3,3,3,3,4.

The forcing bound is valid over every field with arbitrary nonzero values on the surviving support. If a seed of size t recovers every coordinate in a homogeneous kernel equation, restriction to that seed is injective on the kernel. Thus rank is at least 11 minus t. Deleting one edge can increase the required seed count by at most one: add that edge's source coordinate to the old seed and replay the recovery order.

For at most six nonunit edges across the three layers, the source's case split therefore bounds the sum of nullities by 9. Sylvester's inequality gives product rank at least 2. Reduction of the unnormalized F11 at the cyclotomic prime has rank 1, giving the stated contradiction. All three cases, including a single layer with six nonunits, are covered correctly.

A complete independent six-deletion extension checks another 3,322,704 layer masks. The maximum forcing number is 4 in every layer, with respectively 15,15,20 masks attaining 4. This leaves only the distribution (5,1,1) as a possible seven-edge exception to the numerical rank bound. Its three possible five-deletion masks are all excluded by the unique-path argument below. The stronger result does not depend on this intermediate six-deletion extension.

## Complete bounded extension

### A graph lemma over every field

Let A, B, C be 11-by-11 matrices over any field, with entries outside the fixed three supports zero and entries at allowed positions arbitrary, including zero. Then **CBA cannot have rank one with all 121 entries nonzero**.

The proof has three steps.

1. The unchanged directed network has exactly 22 input-output pairs with one path. Independent path traversals agree that the union of the edges on these paths contains 18 edges of A, 18 of B, and 19 of C, or 55 distinct edges in all. For such a pair, the corresponding transfer entry equals the product of the three path coefficients. If every transfer entry is nonzero, each of these 55 coefficients must be nonzero.

2. Therefore zero coefficients can occur only among the remaining 15,15,14 positions of the respective layers. This leaves exactly 2^15 + 2^15 + 2^14 = 81,920 possible layer support patterns. Every one has a three-coordinate forcing seed. Equivalently, every surviving pattern contains an 8-by-8 submatrix with a unique perfect matching: ordering its rows and columns by the forcing recovery sequence makes it lower triangular, with nonzero diagonal entries. Its determinant is the product of those eight entries. Thus each layer has rank at least 8 for every choice of its nonzero coefficients, over every field.

3. Sylvester's rank inequality gives rank(CBA) at least 8+8+8-2*11 = 2, contradicting rank one.

This is a finite certificate proof, not an assertion based on random weights or an optimizer. The field does not need to have characteristic 11 for the graph lemma.

### Complete certificate coverage

The restricted masks have minimum-forcing-number histograms, listed in order t=0,1,2,3:

- A: 3,360; 21,206; 8,098; 104. Total 32,768.
- B: 2,806; 19,630; 10,145; 187. Total 32,768.
- C: 436; 10,019; 5,777; 152. Total 16,384.

`restricted_seed_certificates.txt` contains exactly one line per mask. Each line gives three decimal integers: zero-based layer number, a 33-bit deleted-edge mask, and an 11-bit seed mask. Edge indices are the unchanged order in `topology_11.json`. Every seed has exactly three bits, obtained by augmenting a minimum seed when necessary. Adding known coordinates preserves forcing.

The independent verifier regenerates unique paths by a different forward traversal, rebuilds the entire admissible powerset, rejects duplicates, verifies exact coverage, and checks every certificate with sets. Each certificate recovers the eight remaining coordinates using eight distinct rows. It explicitly verifies that no selected row contains a later selected column and that each diagonal position survives. This proves a nonzero triangular 8-by-8 minor without making assumptions about the numerical coefficient values.

The combined deterministic checksum of every checked mask, seed, and recovery sequence is `e569c90fe2b05aaaf0c19201a2cdf49e55c682ed2001249294580b506deca462`. Full coverage and certificate receipts are in `restricted_verifier_receipt.json`.

A separate reviewer independently parsed the topology and certificate data, regenerated the unique paths, and verified every powerset mask and all eight recovery steps without executing the certificate author's programs. It also passed all 81,920 certificates. Its unchanged checker is retained as `root_verify_v34.py`, with receipt `ROOT_INDEPENDENT_CERTIFICATE_CHECK.json`. The checker was authored by the reviewing agent, rather than the author of this audit's generator and first verifier.

### Consequence for Fourier

Let R be a valuation ring with residue field k of characteristic 11. Suppose R contains a primitive eleventh root zeta whose image in k is 1. All entries of the unnormalized matrix F11 = (zeta^(ij)) are units of R and reduce to 1.

Assume A,B,C have the fixed supports, all allowed coefficients lie in R, and CBA=F11. Reduction modulo the maximal ideal is a ring homomorphism, so the reduced product is the all-ones matrix over k. It has rank one and all entries nonzero, contradicting the graph lemma. Hence no such integral factorization exists.

The same argument applies to a target obtained from F11 by input/output permutations and diagonal matrices with unit entries. Its reduced transfer is still rank one with every entry nonzero.

In particular, take K=Q(zeta11), pi=zeta11-1, and R=Z[zeta11] localized at the prime ideal (pi). This is the source's discrete valuation ring. If a factorization exists over any algebraic extension with a chosen extension of that valuation, at least one coefficient has negative valuation. This conclusion is about each chosen place above 11 under the stated unnormalized target and unit endpoint gauges.

## Arithmetic checks and exact ring distinctions

The classical Fourier minor valuation formula is correct. For a prime p, write zeta^i=1+pi*u_i with u_i reducing to i modulo pi. Cauchy-Binet applied to the binomial expansion shows that the unique least possible pi exponent in a k-by-k minor is k(k-1)/2. Its coefficient reduces to the product of the row and column Vandermonde determinants divided by the product of r! for 0<=r<k. All factors are nonzero in the residue field. This establishes the exact valuation. In the base cyclotomic DVR, the local Smith valuations are consequently 0,1,...,p-1.

The fresh arithmetic program does not use the source's permutation expansion or multiplication-matrix norm routine. It computes determinants by column-subset dynamic programming, then repeatedly divides their integral power-basis coefficients exactly by zeta-1. Each division is checked by multiplication back. The final unit quotient is independently compared with the Vandermonde leading coefficient.

All 251 minors for p=5 and all 3,431 for p=7 pass, as do 24 additional complete p=2 and p=3 controls. All 31 source p=11 cases pass; their exact norms independently agree with polynomial resultants. Eleven additional leading minors cover every order 1 through 11, including the full determinant valuation 55. A duplicated row gives zero, and multiplying a nonzero minor by pi increases its valuation by exactly one.

The unweighted layer determinants over the integers are -9,3,3, reducing to 2,3,3 modulo 11. The path multiplicities are 22 entries with one path, 42 with two, 39 with three, 16 with four, and 2 with five. The 22 unique-path exponent vectors have rational rank 22. The counts of row pairs intersecting in exactly one column are 27,23,25. These subsidiary source diagnostics also reproduce.

Scope distinctions that must be preserved:

- In the base DVR, pi is a uniformizer and nonunit is equivalent to divisibility by pi. In a ramified extension ring, pi need not generate the maximal ideal. There the safe statement is positive valuation, or residue zero; a nonunit need not be divisible by pi in that extension ring. The seven-edge rank argument and the stronger exclusion use residue zero, so they remain valid with this wording.
- The exact minor valuation is k(k-1)/2 when v(pi)=1 in the base field, or after normalizing an extended valuation by v(pi)=1. An integer-normalized uniformizer valuation in a ramified extension multiplies these numbers by the ramification index.
- The target is the unnormalized F11. A unitary normalization involving 1/sqrt(11) has a pole at the cyclotomic prime and is outside the integral all-unit-output model.
- Unit vertex gauges preserve integrality and unit status. Arbitrary internal gauge changes can alter them. No claim is made that every algebraic solution can be gauged into this integral model while keeping unit endpoint gauges.
- There is no exclusion of weights with poles or arbitrary complex factorizations. An abstract complex number is not assigned a valuation without a specified coefficient field and valuation model.
- The classical minor-valuation proof and Sylvester inequality are not claimed as new. This audit makes no literature-wide priority claim for the finite graph exclusion.

## Relation to the earlier rational-map audit

The accepted v33 results remain compatible with this obstruction: the support is a superconcentrator and admits generic full-spark transfer matrices. The rational cross-ratio map has dimension 56, and the corresponding numerator Jacobian has rank 56. These facts do not imply Fourier compatibility. The v33 precision correction remains in force: the rank-56 matrix is the denominator-squared numerator of the rational cross-ratio derivative, not the off-target derivative of the cleared Fourier residual equations.

The new graph lemma concerns dense rank-one targets over a residue field; it does not prohibit generic full-rank transfer matrices over the original field. No unrestricted Fourier existence or impossibility conclusion follows.

## Reproduction

Run from this audit directory:

    g++ -O3 -std=c++17 audit_forcing.cpp -o audit_forcing
    ./audit_forcing 6 1 < topology_input.txt > forcing_receipt.json
    ./audit_forcing 15 1 1 < restricted_input.txt > restricted_forcing_receipt.json
    python3 verify_restricted_certificates.py
    python3 audit_arithmetic.py
    python3 audit_summary.py

The first enumeration verifies the source and bounded six-deletion extension. The second creates the 81,920 restricted seed certificates. The independent verifier proves complete coverage and checks all triangular minors. The arithmetic audit and final summary produce the remaining receipts. Python's SymPy dependency is used only for exact resultants, integer determinants, and rational rank checks, not the support certificate verification.

The source files and Library identities are retained in `SOURCE_IDENTITIES.json` and `manifest_receipt.json`. `FINAL_RECEIPT.json` records the verdict and restrictions. `AUDIT_SHA256SUMS.txt` freezes the proof, fresh programs, inputs, and receipts.

The separate reviewer's unchanged checker uses the original workspace-relative audit directory, so run it from the workspace root if that directory layout is preserved. The main reproduction commands above are self-contained within the audit directory.
