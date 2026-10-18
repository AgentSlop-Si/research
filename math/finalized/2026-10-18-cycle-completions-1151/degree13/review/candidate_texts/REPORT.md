# N13: sixteen original physical banks over F_(53^13)

18 October 2026 UTC. Candidate attainment theorem; external independent review pending. Exact construction and two algorithmically distinct literal verifications have passed. This is an extension of the accepted degree-eleven method, without a historical novelty claim.

## 1. Precise result

Fix N=13, q=16 in characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum number of physical banks in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation. Arbitrary legal beta and raw weights are allowed. Then

    B(F_(53^13))=16.

The explicit witness has allocation (7,1,1,7), beta=1, the same seven nodes in each same-sign orientation, and equal but genuinely nonbase cross nodes. Both same-sign supports are non-Frobenius-stable. Thus it neither repeats the barred stable-support search nor the prime-field-cross family. Equal cross choices are permitted by independently free choices; the theorem does not require their equality in general.

The upper bound is proved by the complete literal certificate here. The matching field-uniform lower bound is inherited from the accepted, byte-bound source chain, not recomputed or newly claimed. The result does not address grammars with more effective cross nodes.

## 2. Field and explicit input

Use K=F53[u]/(u^13+u+1). An element is stored as [a0,...,a12], meaning sum ai*u^i. The order 53^13 is 26036721925606486195973, a 75-bit integer. The C++ code uses unsigned 128-bit exponents; preserving the predecessor's 64-bit exponent type would be incorrect.

Before any extension inverse, the standalone Python verifier proves

    X^(53^13)=X mod (X^13+X+1),
    gcd(X^13+X+1, X^53-X)=1.

The degree 13 is prime. The first identity restricts irreducible factor degrees to 1 or 13 and implies squarefreeness; the gcd removes degree 1. This proves irreducibility. FIELD_IRREDUCIBILITY.json and the second implementation's receipt retain all thirteen Frobenius remainders. The checker also verifies that 16 has exact order 13.

The cross nodes are

    y=z=[11,38,41,38,15,10,28,29,16,23,5,16,35].

The seven actual same-sign nodes and all eight annihilator coefficients are given without abbreviation in DEGREE13_LITERAL_CERTIFICATE.json. Both checkers multiply their seven linear factors and verify the resulting H. They verify distinctness and nonzeroness. The Python checker directly computes all seven 53rd powers and checks that the resulting set differs. It also checks that H has a nonbase coefficient and both cross nodes are nonbase.

## 3. Exact original physical grammar

With indices modulo thirteen, set S e_t=e_(t+1) and T e_t=16^t e_t. Every certificate record is one original physical bank

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1).

Its guard is Delta=1-alpha^13-1=-alpha^13, independently recomputed and nonzero. All sixteen resulting bank matrices are themselves nonzero. No trace, quotient-valued bank, derivative, singular limit, pre/post map, or uncharged transform replaces an original primitive.

The inert JSON records every sign, alpha, beta, guard, seven actual nodes, full H, all 208 normalized amplitudes, all 208 raw branch weights, and all 169 entries of the sum. Canonical field-coordinate lengths and residues are checked before arithmetic.

## 4. Construction and literal verification

Discovery adapts the accepted nonbase-cross degree-eleven construction to the different irreducible degree-thirteen field, new reduction relation, new 75-bit order, and deterministic seed 202610181140. It retains the symmetric subfamily y=z, equal same-sign supports, beta=1. The six forced windows define a monic degree-seven affine recurrence family. The b=3 compatibility equation is solved over K. This is only a necessary candidate gate. Neither passing the gate nor splitting H is treated as a physical-bank proof.

The first split candidate occurs at zero-based trial 1030. Seven actual roots are then recovered. For every b=0,...,12 the reconstruction solves the full thirteen-row, sixteen-column sector system on those roots. All 169 equalities pass. Its ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For normalized target f(a,b)=16^(10(a+b)^2) and gamma=7, the raw weights are

    w_j=Delta*7*sum_(b=0)^12 A_b*16^(-epsilon*b*j).

Both algorithms invert this transform and recover every amplitude. The literal operator check is stronger than this reconstruction:

1. For each of the 208 branches build M with M[t,t]=1-16^(epsilon*delta*j+delta*t) and M[t+epsilon,t]=-alpha.
2. The C++ program computes M^(-1) by Gauss-Jordan elimination and verifies both products with M.
3. The Python program reads only inert JSON. It uses independently implemented generic polynomial arithmetic and the unique zero diagonal row r0=-epsilon*j to generate each inverse by backward recurrence. It then separately verifies both literal sparse matrix products.
4. Each algorithm multiplies by the supplied raw weight and original 1/13, sums all sixteen physical banks and checks all 169 entries against 16^(-kt).

Both runs establish 16 nonzero guards, 208 branch inverses, 416 two-sided component identities, 70,304 scalar inverse-entry equalities, 208 raw-weight/amplitude equalities, and 169 target equalities, with zero target mismatches. Every physical bank is nonzero.

Falsification controls give 169 mismatches when 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after adding one to the final bank's final raw weight. These controls supplement the positive identities. The Python implementation is adapted from the predecessor's separate checker; it is algorithmically independent of the C++ verifier, but does not constitute a new external review.

## 5. Lower bound, scalar extension and next boundary

The accepted degree-eleven independent review explicitly binds the characteristic-53 field-uniform lower theorem: each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, while each cross orientation requires a nonzero node. This permits arbitrary legal beta, repeated physical banks and cancellation. It gives B(K)>=16 in the specified free-cross-singleton grammar. Its large lower-minor computation is inherited, not rerun here.

The literal witness proves B(F_(53^13))<=16, hence equality. If 13 divides d, F_(53^13) embeds in F_(53^d), preserving all nodes, raw weights, nonzero guards and operator identities. Therefore

    13 divides d  =>  B(F_(53^d))=16.

Combining this with the already accepted sufficient degrees 2,3,5,7,11 gives the sufficient divisor list {2,3,5,7,11,13}. Apart from the previously solved base field d=1, the remaining unclassified degrees are d>1 with gcd(d,30030)=1; the smallest is 17. This is not an iff classification. It does not exclude sixteen banks at any remaining degree or close the broad parent problems.

The inherited prime-field-cross obstruction remains compatible: degree 13 is coprime to 210 and both cross nodes here lie outside F53.

## 6. Finite scope, reproducibility and claims withheld

SEARCH_SCOPE.json records the exact deterministic finite search and failed prefix. The cap was 100000 but search stopped at its first split candidate after testing trial indices 0 through 1030. A separate cap-1030 replay verifies the preceding failed cross-node prefix. The nonsplit candidates are not a field-wide impossibility theorem. No stable-support census or prime-field-cross census was rerun.

COLD_REPLAY.json records isolated Python verification in a fresh temporary folder, fresh C++ reconstruction giving byte-identical certificate output, repeat Python verification, and exact deterministic discovery replay. The certificate hash binds all verification receipts. Source code is portable GNU C++17 plus Python standard library; SymPy was used only to locate the modulus initially, and is not a verification dependency.

The operation ledger charges support search, field arithmetic, factorization, actual-root sector solving, raw-weight construction and literal inverses. A sixteen-bank count is not sixteen scalar operations and gives no FFT, bit-complexity or practical speedup claim. No general field classification, historical-priority result, broad-parent closure, publication or external write is claimed.
