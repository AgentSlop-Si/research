# N13: sixteen original physical banks over F_(53^29)

18 October 2026 UTC. Candidate attainment theorem with two algorithmically different literal checks, an exact field certificate, and arithmetic boundary controls. External independent review is pending. This extends the accepted degree-23 construction to a new field; it makes no historical novelty claim.

## 1. Exact theorem and scope

Fix N=13, q=16, characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta and raw weights. The explicit witness below and the inherited accepted field-uniform lower theorem establish

    B(F_(53^29)) = 16.

The attained allocation is (7,1,1,7). The extension degree is twenty-nine; the transform length remains thirteen. The witness has beta=1, seven common same-sign support nodes, and equal cross nodes y=z. Equality is permitted by independently free cross parameters; it is not imposed on the theorem's grammar. Both cross nodes are nonbase, and both same-sign supports are non-Frobenius-stable. The smaller constructive subfamily suffices for an upper bound in the stated larger grammar.

The field-uniform lower theorem is inherited from the accepted source-bound reviews. This task does not rerun the large original lower-minor computation, classify other cross allocations, or modify the physical-bank primitive.

## 2. Exact field and arithmetic boundaries

Use K=F53[u]/(u^29+u+8). Coordinates [a0,...,a28] mean sum ai*u^i. The exact field order is

    Q = 53^29 = 100925339366770615067826870974905413660631238363333,
    bit_length(Q) = 167.

search_field.py tests u^29+u+c in increasing c, and FIELD_SEARCH.json records that c=8 is the first irreducible member among c=1,...,8. Before any extension-field inversion, ordinary prime-polynomial arithmetic proves

    X^(53^29) = X mod (X^29+X+8),
    gcd(X^29+X+8, X^53-X) = 1.

Because 29 is prime, the first relation restricts irreducible factor degrees to 1 or 29. Its ambient polynomial has derivative -1 and hence is squarefree. The gcd excludes degree 1, and total degree 29 forces irreducibility. FIELD_IRREDUCIBILITY.json retains all twenty-nine Frobenius remainders. The inert-JSON literal checker repeats the field proof, and witness_structure_check.py explicitly checks primality of 53 and 29.

All active C++ field-order and extension-field exponent paths retain unbounded GMP mpz_class: ORDER, element powers, inversion, polynomial powers, splitting, the quadratic-gate square-root exponent, and recursive root-factorization exponents. No narrowing conversion is introduced. uint64_t is used only for the deliberately wrapping xorshift PRNG and bounded search counters; the separate prime-field exponent routine has small bounded integer exponents.

The order-derived exponents are

    Q-2       = 100925339366770615067826870974905413660631238363331,
    (Q+3)/8   = 12615667420846326883478358871863176707578904795417,
    (Q-1)/2   = 50462669683385307533913435487452706830315619181666.

All exceed 2^128-1. The exact arithmetic probe and an independent ordinary-convolution/Python-integer checker agree on multiplication, inversion, ten boundary and order-derived powers, a known seven-root splitting polynomial, and factor-character values. Six falsification controls detect wrapped order, the 2^128-to-zero exponent boundary, and truncated inverse, split, square-root, and factor exponents. The square-root routine uses Q=5 mod 8 and 23^2=-1 mod 53, and explicitly checks the proposed square root by squaring.

There is a distinct convolution boundary. A degree-29 unreduced coefficient can reach

    29*52^2 = 78,416 > 65,535.

Consequently the accepted degree-23 reviewer's 16-bit packed coefficient implementation cannot be reused unchanged. The active degree-29 Python literal checker uses ordinary coefficient convolution and general polynomial reduction, so it has no packed carry assumption. check_convolution_boundary.py verifies 17-bit packed convolution against ordinary convolution and generic long division on all 841 ordered basis pairs, 100 deterministic dense pairs, and the all-52 worst-case pair. It demonstrates that 16-bit convolution is safe at degree 24, fails at degree 25, and fails at degree 29. Its negative controls reject the unsafe 16-bit carry bound and detect both raw-coefficient and reduced-field-product corruption. These controls ran before discovery, as enforced by run_discovery.py, and are repeated before search in the cold replay.

For the active C++ schoolbook arithmetic, reduction is u^29=-u-8. Each low coefficient receives at most its original term and two contributions of multipliers 1 and 8. High-degree terms reduce directly below degree 29, with no repeated high-degree feedback. The conservative signed bound is 10*78,416=784,160, safely within signed 32-bit int. The literal reconstruction and arithmetic probe additionally pass undefined-behavior sanitization.

## 3. Inert witness and original operators

The two cross nodes are

    y=z=[21,19,5,11,11,49,30,52,1,51,10,27,16,28,24,6,19,16,31,41,21,8,40,41,19,3,43,40,31].

DEGREE29_LITERAL_CERTIFICATE.json stores the seven distinct nonzero actual support roots, their full monic degree-seven annihilator H, sixteen physical-bank records, 208 normalized amplitudes, 208 raw branch weights, every guard, and all 169 target-matrix entries. Every element is a canonical 29-coordinate vector. No formal root placeholder substitutes for an actual field element.

With indices modulo thirteen, define S e_t=e_(t+1) and T e_t=16^t e_t. Each of the sixteen certificate banks is literally

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1).

The general legal guard is 1-alpha^13-beta^13; here beta=1 and hence Delta=-alpha^13. All sixteen guards are recomputed and nonzero. All sixteen resulting bank matrices are nonzero. There is no trace bank, quotient-algebra primitive, derivative bank, singular limit, pre/post map, or uncharged transform.

## 4. Discovery and proof are separate

Discovery retains the symmetric subfamily y=z, equal same-sign supports, and beta=1. Six recurrence windows define a monic degree-seven affine line; the b=3 compatibility gate is solved in the exact new field. These are necessary discovery gates, not a sufficient original-network theorem. The inherited chart theorem applies because 37 does not divide 29. The final literal witness is valid independently of any claim that the discovery chart is complete.

The deterministic xorshift seed is 202610181745. The first split candidate occurs at zero-based trial 10,425, after examining 10,426 nonzero cross nodes and 10,497 nonzero-constant recurrence candidates. The initial cap is 100,000; discovery stops at its first split candidate. Source replay independently reproduces all 302,354 coefficient draws, with no zero cross node skipped. The exact failed prefix and first-hit replay are retained separately. Failed finite searches imply no field-wide nonexistence, stable-support census, or obstruction for other nodes or allocations.

The C++ verifier factors H into seven actual, distinct, nonzero field roots and checks their product. It solves all thirteen equations in each of the thirteen full sixteen-column sector systems and checks all 169 equalities. The sector ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For normalized target f(a,b)=16^(10(a+b)^2) and gamma=7, the raw weights are

    w_j = Delta*7*sum_(b=0)^12 A_b*16^(-epsilon*b*j).

Both literal implementations invert this transform and recover all 208 supplied amplitudes. They then construct the original branches: M[t,t]=1-16^(epsilon*delta*j+delta*t), M[t+epsilon,t]=-alpha.

The C++ implementation constructs inverses by Gauss-Jordan elimination and checks both dense products. The independent Python implementation reads only inert JSON, uses ordinary coefficient arithmetic, and solves each inverse by a zero-diagonal backward recurrence; it checks both sparse matrix products. Neither implementation substitutes the recurrence gate for the actual operator identity.

Each implementation checks 208 legal branch inverses, 416 left/right inverse identities comprising 70,304 scalar equalities, 208 raw-weight/amplitude equalities, and 169 Fourier target entries with zero mismatches. Summing the supplied raw-weighted original branches with the original factor 1/13 gives exactly F[k,t]=16^(-kt). This is equality of operators on every input vector over K, not sampling of input vectors.

Both implementations detect 169 mismatches if 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after adding one to the final raw weight. Separate implementations by the same construction author, source checks, and sanitizer passes do not constitute external independent-review acceptance.

## 5. Lower bound, transfer, and coverage boundary

The accepted inherited lower review explicitly states a theorem for every characteristic-53 field and arbitrary legal beta: each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, and each cross orientation requires a nonzero effective node. Repeated, ineffective, zero-alpha, or cancellation-only banks cannot lower the physical count. Thus the stated free-cross-singleton grammar has B(K)>=7+1+1+7=16. This is the field-uniform theorem, not the narrower y=z=1 necessity criterion from that source.

The explicit verified network supplies equality over F_(53^29). Whenever 29 divides d, the finite-field embedding F_(53^29) into F_(53^d) preserves every parameter, raw weight, nonzero guard, and original operator identity; the inherited lower theorem still applies. Therefore

    29 divides d  =>  B(F_(53^d))=16.

Combining this new candidate attainment with the previously accepted degrees gives the sufficient divisor list

    {2,3,5,7,11,13,17,19,23,29}, with product 6,469,693,230.

Apart from the separately solved base case d=1, the residual degrees not covered by this sufficient list are d>1 coprime to that product; the least is 31. This is not an iff classification or a nonexistence claim at degree 31.

witness_structure_check.py directly computes Frobenius orbits of all seven roots and both cross nodes, each of exact length 29. Applying each of the twenty-nine prime-Frobenius automorphisms to every bank parameter and raw weight gives another original network for the same prime-field target. The cross orbit distinguishes twenty-nine conjugate parameter lists. This witness does not descend to F53; it does not exclude a different prime-field parameter list.

The older prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. Substituting the larger sufficient-divisor product into those obstruction hypotheses would be invalid. Nonbase cross nodes and nonstable same-sign supports are properties of this witness, and do not prove that both cross nodes must be nonbase for every possible witness. The degree-37 chart exception remains a chart exception rather than a physical-network obstruction.

## 6. Reproducibility and exclusions

A standalone inert-certificate check requires only Python's standard library:

    python -I independent_literal_check.py
    python -I witness_structure_check.py
    python -I check_convolution_boundary.py

Source adaptation and binding:

    python -I source_rebuild_check.py

Cold replay in a fresh temporary directory:

    python -I cold_replay.py

Cold replay repeats field irreducibility, both arithmetic boundary preflights, isolated Python literal checking, fresh C++ reconstruction, reconstructed Python checking, undefined-behavior sanitization, and the exact failed-prefix/first-hit discovery replay. Certificate, field receipt, arithmetic receipts, and discovered candidate are byte-identical. C++ compilation requires GNU C++17 and GMP development headers/libraries, linked with -lgmpxx -lgmp; tested GMP is 6.3.0. No installation is performed.

SOURCE_PINS.json records 27 inherited files by byte length, SHA256, and Git blob SHA1. Source replay checks exact adaptation of seven active scientific sources, the modulus search, candidate/header/certificate binding, every large-exponent call path, and the PRNG. It also checks all 52 entries in the accepted degree-23 candidate manifest and all 78 entries in its accepted review manifest against the available original local trees, and binds the inherited acceptance verdict to the exact report, arithmetic receipt, and candidate manifest. These are local source checks, not fresh remote reads. SOURCE_LEDGER.md identifies the inherited theorem provenance. MANIFEST.json seals the new sources and evidence, excluding disposable binaries and caches.

OPERATION_LEDGER.md charges field arithmetic, modulus search, boundary audits, support search, factorization, full-sector solving, raw-weight construction, and actual inverse preparation. A schoolbook degree-29 multiplication has 841 coefficient products before reduction. Sixteen physical banks are not sixteen scalar operations. No general faster FFT, practical runtime advantage, complete field classification, other-allocation theorem, or historical-priority claim is made.

No finite collection of prime-degree certificates proves cofinite or generic existence. A uniform existence theorem would need additional algebraic results, such as an appropriate geometrically irreducible component of the complete split-support/full-sector incidence variety and an effective point-count theorem. This recurrence gate and exact witness do not establish those prerequisites. This task performs no GitHub, Sheets, publication, register, or other external write and creates no additional agents.
