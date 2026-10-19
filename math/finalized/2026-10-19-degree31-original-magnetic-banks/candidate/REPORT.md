# N13: sixteen original physical banks over F_(53^31)

19 October 2026 UTC. Degree-31 finite certificate for the existing M-MAGNETIC-SPAN gate (NEW-17, Q35 and NEXT-MAGNETIC-SIGNED are views of the same gate). External independent-review acceptance is required; same-author checks alone do not supply it. Priority 56 and parent-owner status are unchanged.

## 1. Exact result and scope

Fix N=13, characteristic 53, q=16, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha in each cross orientation, allowing arbitrary legal beta parameters and raw weights.

The inert explicit original-bank certificate proves B(F_(53^31)) <= 16. Together with the inherited accepted field-uniform lower theorem B(K) >= 7+1+1+7=16, it establishes the scope-limited equality

    B(F_(53^31)) = 16.

The inherited lower theorem is read and bound through accepted source reviews, not recomputed here. No historical accepted degree<=29 witness or large lower-minor calculation was rerun. Acceptance of this new finite result is conditional on the separate review accompanying this candidate.

The attained allocation is (7,1,1,7), with beta=1, seven common same-sign support roots and equal cross values y=z. The larger grammar permits independent choices of the two cross parameters; equality is a legal chosen value, not a restriction on the claimed lower theorem. A witness from this sufficient subfamily establishes attainment in the larger grammar. The transform length remains 13; 31 is the extension degree.

A field embedding F_(53^31) into F_(53^d), for 31 dividing d, preserves every coefficient, guard and operator identity. The inherited lower bound also persists, so 31 divides d implies B(F_(53^d))=16. This is a sufficient divisibility result. It is not a classification of all fields, a uniform/cofinite existence theorem, an iff statement, an owner closure, or a new result about other cross allocations. No historical novelty, FFT speedup or priority change is claimed.

## 2. Field, representation amendment and arithmetic

Use K=F53[u]/(u^31+2u+11), with canonical ascending 31-coordinate vectors. The order

    Q=283499278281258657725525680568509306972713148562602397

has 178 bits. `ARITHMETIC_PROOF.md` supplies the exact irreducibility and integer-width arguments. `FIELD_IRREDUCIBILITY.json` preserves all 31 Frobenius remainders and the gcd witness. Both the preflight and standalone checker prove irreducibility before extension-field inversion.

The initial deterministic modulus family u^31+u+c had no irreducible member for c=1,...,52. Before any support search, its representation rule was amended to lexicographic u^31+a*u+c, a,c=1,...,52. The 63rd polynomial, a=2,c=11, is the first success. `SEARCH_SCOPE.json` retains the original freeze and `SEARCH_SCOPE_AMENDMENT.json` records this change. It changes only the polynomial representation of the same field F_(53^31). The seed 202610192024 and 100,000-nonzero-cross-node cap were not altered.

Every C++ order/exponent path uses unbounded GMP integers. All Python integer arithmetic is unbounded. Ordinary convolution avoids the unsafe 16-bit packing assumption: 31*52^2=83,824 exceeds 65,535. For the actual modulus, the conservative signed reduction bound is (1+2+11)*83,824=1,173,536, safely within int32. The active checker does not use packed convolution. Differential packing controls explicitly detect unsafe 16-bit corruption. Six separate exponent-width falsification controls detect wrapped/truncated arithmetic.

## 3. Literal certificate and physical primitive

`DEGREE31_LITERAL_CERTIFICATE.json` is inert JSON, SHA256

    20ff3730c3b42568062d6da7151939c23ffd0abdf1bd6a8d79c1abfb905de5ad.

It contains all seven distinct nonzero actual support roots, their full monic degree-seven annihilator H, the two cross nodes, sixteen original bank records, 208 normalized amplitudes, 208 raw branch weights, sixteen pole guards and all 169 target-matrix entries. No formal root, black-box transformed primitive or sampled-input test replaces this data.

Let S e_t=e_(t+1) and T e_t=16^t e_t, with indices modulo 13. Each supplied bank is literally

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha*S^epsilon-16^(epsilon*delta*j)*T^delta)^(-1).

The general pole guard is Delta=1-alpha^13-beta^13; here beta=1 and Delta=-alpha^13. All sixteen guards are recomputed and nonzero. All sixteen bank matrices are nonzero, so none is an ineffective counted bank.

Each actual branch matrix has diagonal M[t,t]=1-16^(epsilon*delta*j+delta*t) and off-diagonal M[t+epsilon,t]=-alpha. The C++ reconstruction inverts these matrices by Gauss-Jordan elimination and explicitly checks both dense products. The standalone Python checker instead solves from the single zero diagonal by backward recurrence and verifies both sparse products. The final sum includes the original factor 1/13 and is checked against all 169 values 16^(-kt). There is no derivative bank, singular limit, trace bank, uncharged pre/post transform or replacement quotient-algebra primitive.

The normalized target is f(a,b)=16^(10(a+b)^2), with gamma=7. Given sector amplitudes A_b, the supplied raw weights satisfy

    w_j = Delta*7*sum_(b=0)^12 A_b*16^(-epsilon*b*j).

Both implementations verify the inverse amplitude transform. All thirteen full sixteen-column sector systems pass all thirteen equations; ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

The thirteen full systems, rather than only the recurrence gate, are checked again directly from supplied amplitudes by the standalone checker.

## 4. Discovery and complete failed prefix

The six recurrence windows and b=3 quadratic compatibility gate are discovery aids within beta=1, y=z and common same-sign support. The degree-37 chart exception does not divide 31. No chart-completeness claim is needed: the final literal identity stands independently of the discovery derivation.

The seed and cap were frozen before discovery. The run stops at the first splitting nonzero-constant candidate, trial 1113 (zero-based), after 1,114 nonzero cross nodes, 1,117 nonzero-constant recurrence candidates and 34,534 PRNG coefficient draws. No zero cross node was skipped. The search took about 11.15 wall seconds in this environment, with the exact child CPU/RSS receipt retained.

`PREFIX_LEDGER.jsonl` retains every generated cross node, PRNG boundary state, tested gate root, full candidate polynomial, constant guard and split verdict through the hit. `PREFIX_AUDIT.json` independently reconstructs every PRNG coefficient draw and checks the inert ledger structure. A cold compile is then run with limits 1,113 and 1,114: the first exhausts exactly the failed prefix with no candidate output; the second reproduces the first hit and complete ledger byte-for-byte. `FIRST_HIT_REPLAY.json` binds these receipts. The last trial's untested second gate root is outside the prefix because discovery stops immediately at its first split.

A failed finite discovery run would only concern this bounded subfamily/seed/cap. It would not exclude other legal nodes, weights, beta values or fields. This successful run is likewise a finite certificate rather than an asymptotic existence theorem.

## 5. Verification, mutation controls and source binding

Both same-author literal implementations pass:

- seven distinct nonzero actual roots and the complete factorization;
- sixteen nonzero pole guards and sixteen effective bank matrices;
- 208 raw/amplitude equalities and 169 full-sector equalities;
- 208 literal branch inverses, both inverse orders, 416 matrix identities and 70,304 scalar inverse equalities;
- every one of the 169 negative unnormalized Fourier target entries, with zero mismatch.

Positive-sign Fourier targets produce 144 mismatches; omitting 1/13 produces 169; adding one to the final raw weight produces 91. Eleven executable inert-certificate mutations test noncanonical coefficients, zero alpha, a false guard, repeated roots, an altered annihilator, weight or amplitude, a missing bank, degree metadata and both target sign/normalization errors. All are rejected by the standalone checker. Positive-control success is bound to the unmodified certificate.

All seven support roots and both cross nodes have exact Frobenius orbit length 31; the same-sign support set is not Frobenius stable. These are properties of this parameter list, not necessary conditions for every possible witness. The 31 Frobenius conjugate lists are preserved by the prime-field target; this does not classify the base-field case.

`SOURCE_PINS.json` binds every adapted source by bytes, SHA256 and Git blob SHA1. The three principal inherited implementations and predecessor report match the published pins in the task selection. Auxiliary sources are individually locally pinned; no claim is made that the whole mutable predecessor directory equals its release. The predecessor independent acceptance is bound to its report and arithmetic receipt. Fresh isolated adaptation reproduces all six adapted active source files byte-for-byte; historical source programs are not executed.

The standalone checker needs only its Python file and inert certificate. Cold replay uses a new temporary directory and standard-library Python, rebuilds the new C++ programs, repeats the field proof, integer/packing controls, literal reconstruction and Python check, and runs both C++ paths under undefined-behavior sanitization. The reconstructed certificate and arithmetic probe are byte-identical. GNU C++17 and GMP headers/libraries are required only for C++ reconstruction/discovery; no installation was performed.

These multiple author-generated checks are not themselves independent-review acceptance. The separately assigned reviewer uses its own field/inverse construction and supplies the final scope-limited verdict.

## 6. Reproduction and cost

Standalone literal check:

    python -I independent_literal_check.py

Supporting new-degree checks:

    python -I field_preflight.py
    python -I source_binding_check.py
    python -I check_convolution_boundary.py
    python -I check_arithmetic.py
    python -I check_prefix_ledger.py
    python -I replay_prefix.py
    python -I mutation_controls.py
    python -I witness_structure_check.py
    python -I cold_literal_replay.py

`check_arithmetic.py` consumes the retained inert arithmetic probe. Cold replay freshly rebuilds that probe before checking it. `prepare.py` is an archival source-capture script with explicit original local paths, not needed for portable certificate checking. A scientific replay does not need the historical directory.

`OPERATION_LEDGER.md` charges modulus selection, field arithmetic, discovery, factoring, all full-sector systems, raw-weight preparation, branch inverse preparation, verification, storage and an explicit unoptimized application budget. Sixteen banks are not sixteen scalar operations. No general faster FFT or practical runtime advantage follows.

The finite degree-31 gate can be accepted after independent review; the broader magnetic owner/views remain open. This candidate work performs no external publication, repository update or owner-register change by itself.
