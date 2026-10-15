# Independent audit: Hero0 Phase16 gauge curvature

## Verdict

Accept Theorems 16.1–16.5 within their explicitly restricted models, the conditional Frobenius extension, and the exact finite N=4 two-layer/eight-resolvent certificate. The source's general s=2 rook-to-four-resolvent construction is also algebraically valid when zero edge weights are allowed. These are architecture-specific obstructions and a finite positive control. They establish neither a general faster FFT nor an unrestricted Fourier lower bound, novelty, numerical stability, or bit-complexity savings.

This is not a statement that every file, implementation behavior, inherited claim, or reported experiment has been independently verified. Coverage and limitations are itemized below. Uploaded code was read as inert text and never executed or imported.

## Provenance

The directly supplied ZIP is `fft_hero0_phase16_gauge_curvature_2026-10-10.zip`, SHA-256 `2b0cabeea7b373bb47942db4e2d86f7dd8577ea5e41bb5e5bbaeab8d043847d0`, 473,820 bytes. Its CRC is clean. All 17 entries in its internal SHA256 manifest match their supplied bytes and lengths.

Its nested `prior_phase15_bundle.zip` is byte-identical to the exact Phase15 source retained with the accepted round-0101 review: SHA-256 `94cb33b22de6ecd0cf73c104b9f281a92abfe4ca4748f1e99577ead072dd7285`, 444,884 bytes. Thus the predecessor was not silently replaced. `PROVENANCE.json` records the exact paths and identities. Prior reports remain unchanged.

## Independent proof audit

### 16.1: monomial centralizer

With Q e_j=a_j e_tau(j), evaluating FQ=QF at column zero forces a_j/a_0=omega^(b tau(j)), b=tau(0). Substitution leaves the integer congruence

 i(tau(j)−b)+b tau(j)−j tau_inverse(i)=0 modulo N.

The j=1 equation forces an affine inverse of slope u=tau(1)−b; bijectivity makes u a unit. The resulting affine tau has slope u_inverse, while its first difference is u, so u²=1. Substituting tau(j)=uj+b gives b²+2ubj=0; hence b²=0 and 2b=0. The forced weights reduce to a_j=a_0 omega^(ubj). Conversely these identities make every entry commute. For even N the only possible b are zero and N/2, and the latter survives exactly when 4 divides N. For odd N only b=0 survives.

The argument works over C and over a field with a primitive Nth root; it classifies monomial elements of the commutant, not the full commutant. Our exact exhaustive check covers all 46,232 permutations at N=2 through 8 and compares the forced-weight commuting equations against the classification. This is a control on the independent all-N proof, not its replacement.

### 16.2: exact common-gauge obstruction

For w_t(i)=c_t d_i/d_pi_t(i), direct entry comparison gives P_t=D P_t^0 D_inverse, and consequently the same similarity for each existing Green inverse. Sums with scalar coefficients and ordered products preserve this one common similarity. Since every constant reference topology commutes with Pi_y, the full network commutes with Q=D Pi_y D_inverse.

At even s>=4 the underlying Pi_y has tau(0)=s/2 and tau(1)=s/2+1, hence an affine candidate would be translation by s/2; its value at s/2 is wrong. At s=2 the actual affine map is 1−j modulo 4, and its b=1 violates 2b=0. The monomial classification therefore excludes F and every nonzero scalar multiple of F for all even s>=2, regardless of the conditioning of D. The same proof also permits constant stages c_t=0, provided their Green inverses are defined, although the stated nonzero-edge gauge recognizer does not handle those stages.

All constituent factors must use the same D. An arbitrary intervening permutation, unrelated gauge change, unmatched coordinate relabeling, non-Green factor, or changed scalar coefficient is outside this free common-gauge closure. Such operations need separate analysis/charges; they cannot be inserted for free and then treated as preserving a fixed frame or cut.

### 16.3: unitary-gauge spectral gap

For |d_i|=1 the conjugated involution Q is unitary, and the entries of [U,Q]e_0 are the stated phase differences divided by sqrt(N). Pair i=sx+y and tau(i)=i+s/2 for 0<=y<s/2. The desired phase product is −i a_0² exp(−2 pi i y/s); the actual phase product is one. Minimizing each pair subject only to that product gives squared discrepancy at least 4(1−|cos(theta−pi y/s)|). Relaxing any additional dependencies between pairs can only lower this minimum, so the bound is valid.

For completeness, the absolute-cosine maximization in the source can be justified without an unproved phase-alignment assertion: max_theta sum|cos(theta−alpha_y)| equals max_signs |sum signs_y exp(i alpha_y)|. Here all pairwise angle differences have absolute value <pi/2, so every pairwise cosine is positive; the squared norm is maximized when all signs are equal. The geometric sum is (1/sqrt(2))/sin(pi/(2s)). This gives squared column norm at least 2−2sqrt(2)/(s sin(pi/(2s))). The inequality ||[U−T,Q]||<=2||U−T|| gives the claimed half-square-root distance.

Since s sin(pi/(2s)) increases from sqrt(2) at s=2, the result is positive at every even s>=4. Its limit is (1/2)sqrt(2−4sqrt(2)/pi), approximately 0.223252. It is a lower bound, with no Green-network attainability claim. It does not cover nonunitary D or establish a uniform finite-precision implementation guarantee. Our signed-sum enumeration at s=4,6,8,10,12,16,20 is numerical corroboration explicitly labeled as such.

### 16.4: occurrence-wise rank defect and genericity

The resolvent identity G_new−G_old=G_new(P_new−P_old)G_old gives rank at most the number of changed vertex-weight entries in that occurrence. Sums and product telescoping add these bounds. Thus rank(T−T_g)<=k and rank([T,Q])<=2k. Both the old and new resolvents must exist; the claimed invertibility of the reference network itself is stronger than needed for this rank estimate but harmless.

The determinant of [F,D Pi_y D_inverse] is a Laurent-rational function of the nonzero d_i. At D=I it is nonzero by the previously accepted all-even-square Phase15 spectrum. Hence its numerator is a nonzero polynomial and its nonvanishing set is Zariski open and dense in the diagonal torus. On that set exact Fourier equality requires k>=N/2. We reviewed the predecessor's independent proof/report as the all-size dependency and freshly checked full ranks at N=4,16,64. We do not substitute finite-field samples for the complex genericity proof, claim this rank threshold for every D, or infer a cost lower bound from a linear weight count.

k counts each edited resolvent occurrence, including repeated uses of one shared parameter. Our exact repeated-use control again gives rank one for G_new−G_old but rank two for G_new²−G_old². Arbitrary transported/gauge-changed references and added routing cannot receive zero charge. The handoff's recommendation to search for a linear number of curvature defects is a research strategy; this generic rank theorem is not a universal lower bound on the number of forest holonomy residuals under every choice of gauge and reference.

### Gauge recovery and forest residuals

With known nonzero constants c_t and nonzero edge weights, the edge equation d_j=(c_t/w_t(i))d_i propagates along a spanning forest. Every other edge checks consistency. A successful potential assignment is a certificate because substituting it reproduces every input edge; any failed edge rules out a common gauge for those supplied constants. Self-loops and parallel edges must be retained, as in the supplied code. Choosing the forest does not make the count of residuals a canonical minimum-edit count.

The algorithm uses O(E+V) field operations and storage; for one or more permutations E>=V, this is O(E). This is an algebraic field-operation claim, with inversions/comparisons counted; it is not a bit-complexity, unknown-constant fitting, or unrestricted Fourier-compatibility result. Our independent recognizer checks pure gauges and exact one-self-loop negative controls. We statically audited the supplied traversal, but did not execute it or benchmark its implementation.

### 16.5: single-Green/rook support obstruction

For a nonfixed row of (I−P)F, zeros require omega^((pi(i)−i)j)=1/w_i. A nonzero w_i gives either zero solutions or gcd(N,pi(i)−i) solutions. If w_i=0, the row is simply a Fourier row and has no zeros; this separate case repairs the proof's otherwise undefined reciprocal without changing its conclusion. A fixed point has w_i!=1 by invertibility and therefore also has full row support. For nonzero delta modulo N, gcd(N,delta)<=N/p_min. The column argument uses the unique predecessor of each column and its corresponding row weight.

Thus all rows of (I−P)F and columns of F(I−P) have support at least N−N/p_min. For even s>=4, s²/2>2s−1; for odd s>=3, (2/3)s²>2s−1. This proves the required strict inequality at every s>=3. Our exact root-kernel enumerations include 170,640 (N,delta,exponent) cases for N=2 through80 and support-gap checks through s=256.

The theorem excludes one Green inverse beside a rook matrix on either side. It does not exclude sums of Green inverses or arbitrary networks. In particular the exact F4 control is outside its s>=3 scope.

### Conditional relative-Frobenius extension

Fixed-point-freeness makes each relevant pair of Fourier rows orthogonal, giving squared row norm 1+t² and maximum squared entry magnitude <=(1+t)²/N. Removing all but d entries therefore leaves squared error >=1+t²−alpha(1+t)². Complete the square:

 (1−alpha)(t−alpha/(1−alpha))²+(1−2alpha)/(1−alpha).

For alpha<1/2 this is positive. Sum over all rows and divide by ||I−P||<=1+rho to obtain exactly the claimed relative-Frobenius bound. Our checker verifies this rational identity in 2,095 cases. A fixed point or removal of the weight-norm bound would invalidate this stated proof. No assertion of sharpness is accepted.

### 16.6: exact F4 certificate and arbitrary s=2 rook decomposition

Every supplied matrix entry and weight string was parsed using a narrowly allowed AST grammar as data, with no eval, compile, execution, import, or sympify of the uploaded content. Our checker uses only exact Python Fractions in the 16-dimensional quadratic quotient algebra with i²=−1, a²=1−2i, b²=1+8i, c²=1−16i. It proves every denominator used is a unit, checks both inverse products for all eight I−P factors, checks each four-Green stage sum equals the supplied X or Y, and checks YX equals the standard unnormalized F4. The identities hold under every complex embedding of the quotient algebra, hence for the supplied principal square roots as well. Rook support is checked separately.

The general local decomposition is valid: choose a nonzero root t of t²−t−ab=0 (at least one root is nonzero), set the swap weights to a/t,b/t, and use 1−(a/t)(b/t)=1/t to obtain diagonal t and off-diagonals a,b. The remaining diagonal r can always be split into two nonzero terms: 1 and r−1, except use 2 and −1 when r=1. Nonzero diagonal terms are identity-permutation Green inverses. This algebra uses zero edge weights when off-diagonal targets are zero; it does not make the P matrices themselves invertible monomial matrices.

There are 12 zero edge-weight occurrences in the supplied F4 certificate. Therefore it cannot literally be passed to the supplied nonzero-edge holonomy recognizers. Nonetheless the first layer's identity-generator weight vector has unequal entries, verified exactly; conjugating a scalar identity by any diagonal gauge leaves it scalar. This is a direct gauge-invariant obstruction to any common constant-reference gauge, even if zero constant stages are admitted. Thus the certificate genuinely escapes the pure-gauge class, but “nonzero multi-generator holonomy” should not be read as a separately computed all-nonzero-edge certificate here.

This is precisely a fixed N=4 identity with eight Green inverses, not an all-length recurrence, arithmetic optimality result, or faster universal FFT.

## Coverage register and unverified boundaries

- Fully read and proof-audited: all sections 0–8 of `THEOREMS.md`, `README.md`, `CHAIN_HANDOFF.md`, `PROVENANCE.md`, and every statement in `CLAIM_AUDIT.json`. Section 8 and the handoff are open research targets, not proved results. There are no separate new mathematical appendices.
- Read and checked as certificate data: all of `EXACT_F4_CERTIFICATE.json`, including all eight weight vectors, matrices and product.
- Read as inert implementation text: all of `phase16_gauge.py`, `positive_small_factor.py`, `test_phase16.py`, `audit.py`, and `explore_rook.py`. Mathematical algorithms were compared against the independent derivations; this is not a full executable implementation certification.
- Static implementation limitations: `apply_network_stages` processes at most two stages because of its zip with two iteration orders. Reversing the order of terms in a sum does not make the two identical stages in `apply_network` noncommuting, despite its docstring. `best_row_sparse(X,0)` selects every column via the `[-0:]` slice, rather than returning zero; the shipped positive-d numerical examples do not encounter that edge case. These do not affect the audited theorems or exact certificate, but preclude a blanket “all implementation behavior verified” claim.
- Read `RESULTS.json` and all four logs; independently verified the 17 manifest hashes and counted 19 source test definitions. We did not run uploaded tests/audit, reproduce its 36/12/72/450 seeded experiment counts as an execution claim, reproduce its exact random samples or float stress outputs, or validate the reported timings. The fresh counts in `INDEPENDENT_RESULTS.json` describe a separate independently authored set of controls. In particular the original N=256 rank samples are not part of our fresh finite checks.
- `explore_rook.py` is a numerical fitting experiment. No optimizer run, convergence claim, or asymptotic implication was certified.
- The nested Phase15 archive's bytes were compared exactly and the accepted independent Phase15 review was read. Its entire archive, nested Phase14/earlier mathematical documents, legacy implementations, and inherited log claims were not re-audited in this review. The specific all-size Phase15 commutator theorem is an explicitly identified previously accepted dependency, not new verification of all predecessor material.
- No external literature/priority search was performed; the source's citations, attribution completeness, and novelty disclaimers were read but not independently bibliographically verified. No installed package, browser, external service, or source-code execution was needed.

## Reproducibility and seal

`independent_checks.py` is independently authored, portable, and standard-library-only. It reads source as data and writes `INDEPENDENT_RESULTS.json`; the corresponding output is retained in `INDEPENDENT_RUN.log`. The complete check was replayed in a newly created isolated directory using Python `-I -S`, with byte-identical results. `PORTABILITY.json` records the replay. See `REPRODUCE.md` for commands.

`SEALED_MANIFEST.json` hashes every review/source artifact except the manifest and its own checksum sidecar. `SEALED_MANIFEST.sha256` pins that manifest. The independent `verify_seal.py` checks all entries and unexpected files. Files and directories were made read-only after verification. This is a hash-pinned, read-only review snapshot, not a claim of operating-system immutability against an owner who deliberately changes permissions.
