# Independent review of three bounded theorem increments

16 October 2026 UTC. Verdict: the ALG-032 omitted affine branch, ALG-039 polynomial-input tree-jet ledger, and C10 selected-subsystem solver improvement are accepted in the exact scopes below. This is mathematical acceptance of a next-batch increment, not confirmation of publication or native-cell application. The existing 79-cell publication is separate and unchanged. No external state was written by this reviewer.

## Review method and evidence

The reviewer independently read the actual source text and author proofs, derived the critical identities and costs, and wrote fresh standard-library checks. No supplied research program or author checker was executed or imported. The independent programs compare defining formulas or original bilinear equations against separately implemented constructions. Finite controls test transcription and edge cases; the all-size proofs establish the unbounded results.

The companion results distinguish independent checks from author-reported checks. The review does not count support controls or previously accepted claims as new theorem closures. Mathematical novelty, primary-source equivalence, worldwide priority, production readiness, and broad Fourier-construction gates are not decided here.

## ALG-032: accepted omitted even-step/even-intercept branch

Fix exactly the source one-sketch natural-adjoint decoder. Let M=2^L>=4, a odd, K>=1, N=KM and s_r=b+dr with both b,d even. On x_n=1, the decoded DC is 2 sqrt(N), the true DC is sqrt(N), and the error divided by ||x||_1/sqrt(N) is exactly one. Consequently the promised non-strict maximum-bin bound fails for every epsilon<1. Neither K even nor K<M is required for this DC statement.

The proof is complete. For S(s)=sum_t e_M(at^2+st), expand the squared norm with t=u+h. Orthogonality kills every h except 0 and M/2 because a is a unit modulo M. The surviving phase is exp(2 pi i aM/4)(-1)^s=(-1)^s, since 4 divides M. Thus |S(s)|^2=M(1+(-1)^s). The exact decoder normalization is Xhat_0/sqrt(N)=(1/N)sum_r |S(s_r)|^2, giving two. No inverse of d, nonzero alias argument or cancellation by a nonunit is used.

The guards matter. M=2 reverses the parity outcomes; M=1 is exact. Even a can violate the displayed factor-two formula. Odd d and even K instead give exact flat-input DC, so the odd-d alias obstruction remains a separate theorem. Epsilon=1 is not refuted by an error equal to one. Rescaling the decoder would change the claim; no arbitrary-decoder, nonlinear recovery, multiple-sketch, changed-measurement or repetition lower bound follows.

The odd-b all-zero-sketch branch is preserved historical support. Only the previously omitted even-b branch earns the new completion. The author's 599,144 even-step checks include 299,568 new-branch controls, 299,568 complementary historical controls and eight M=2 controls. Those totals must not be reported as 599,144 new-branch cases.

Independent checks pass: 2,730 exact cyclotomic pair-expansion identities; 21,840 even-step DC cases; 21,840 odd-step guard cases; M=1, M=2 and even-a counterexamples. These use integer pair counts in the exact power-of-two cyclotomic quotient, not floating-point magnitudes.

Source: AFFINE_RESONANCE.md at commit 0339a31eb6109f0b96074ab8321f8653641e7530, SHA256 504e7f01540b55df9a65692fe6d79e87fee014e7b08ab7f50f0bf499239aad55, Git blob cf459be54b0e1b3bfeb080209965b2625be05936. The source explicitly leaves the accepted new branch unclassified.

## ALG-039: accepted explicit polynomial-input K ledger

Let N=2^n>=2 and d>=0. Inputs are supplied coefficient arrays with deg x_s<=d. The source field and C interface retain a supplied primitive Nth root; its preparation is not root finding. One exact K application satisfies

- deg y_s<=d+v2(s) for s!=0;
- deg y_0<=d+n-1;
- nonroot capacity d(N-1)+2N-n-2;
- root capacity d+n;
- total capacity dN+2N-2.

The proof is a valid polynomial extension of the source recurrence. Every propagation multiplies by z, hence shifts and adds; generic convolution is unnecessary for K itself. The root is obtained by the zero-sum identity and includes its full coefficient cost. The root input x_0 is annihilated. The explicit propagation additions number d(N-2)+2N-2n-2, and the root accumulation uses one subtraction per nonroot allocated coefficient under the stated dense schedule. Initialization, copying, addressing and writes are charged, giving O(N(d+1)) operations and storage.

A constant marker contraction has the same bound. The fixed C map has capacity dN/2+N-1, with actual twiddle multiplications and O(N) table preparation from the supplied primitive root charged. J routing has charged coefficient IO. These are fixed interfaces, not a coupled inverse or arbitrary polynomial marker computation.

The upper degree bounds are not universal actual degrees. Cancellation witnesses lower them, and root-only input is annihilated. Over the complex numbers, x_s=1+z+...+z^d makes every allocated output slot nonzero, so the explicit materialized-output interface has an Omega(N(d+1)) worst-case write bound. At d=Theta(log N), this particular full-output problem takes Theta(N log N) work. It gives no lower bound against shared representations, scalar evaluation, selected-coefficient circuits or Fourier algorithms. The determinant/chart guards of the separate bordered or variable-block inverse remain untouched.

Independent checks pass: 333 direct defining-sum versus recurrence cases over integers, GF(3) and GF(97), N<=256, with exact storage/addition counts, root-input annihilation, zero sums, C capacity and constant-marker contraction; 37 simultaneously dense integer witnesses; and 37 additional actual C-map comparisons with a certified primitive Nth root over GF(257). Tree-only controls over other fields test the polynomial identity, not the existence of a primitive root there.

Source-byte qualification is verified independently. The original 10,468-byte source has SHA256 e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f and Git blob c8a91a0060f86e8fa5a5930f4cb06ff4c1607c1e. The published sanitized 10,440-byte file, still under the original hash-named archive path, has actual SHA256 8d55b12a5b65d41fef3dbc5bfa7ff87d78b0ab940b5323ee0888b0f991fa5d33 and Git blob 86d166654a61444ab268a8f208af21d93c114a63. Exactly one private-identifier substitution makes the two byte sequences equal; mathematical content is identical. A filename hash must not be substituted for actual published-byte hash.

Publication wording refinement: the author's X140 phrase “O(N) root preparation” is replaced in the accepted overlay with “a supplied primitive root and O(N) twiddle-table preparation where needed.” The report already states this precise model. No root-finding complexity is accepted.

## C10: accepted sorting/sequential-2SAT improvement

The input is M selected bilinear equations u_j^T L_e u_i=0 on N projective directions. Rank-two edges define invertible projective transports and a spanning forest. Reverse transport by adjugate is valid projectively, including in characteristic two. Substitution of every internal equation gives a degree-at-most-two homogeneous binary polynomial. A finite-chart gcd plus an explicit infinity bit summarizes its common-root domain in O(N+M) field/graph work.

Every nonzero cross-component edge has rank one and factors into a positive disjunction of two equality-to-point conditions. The two forms remain nonzero after invertible transports. Zero edges impose nothing. Canonicalizing and sorting at most 2M point occurrences deduplicates the equality flags, provided an exact sortable canonical scalar representation is available. Equality-only field operations alone do not imply that capability.

For k distinct flags in one component, the sequential at-most-one encoding with k-1 auxiliaries and 3k-4 clauses (k>=2) is exact. A second true flag contradicts the propagated prefix; every at-most-one assignment extends by prefix ORs. Across the graph there are at most 4M Boolean variables and 9M clauses. Strongly connected components solve the resulting 2-CNF in linear graph time.

No at-least-one clause is necessary once all component domains are certified nonempty. If all flags of a component are false, select any allowed point and turn on its matching flag if named. This preserves all positive edge clauses, never violates a forbidden unit, and leaves at most one true flag. Recomputing the prefix auxiliaries completes the repair. This is valid for finite fields with every point named, restricted domains, infinity, repeated roots, loops and parallel edges.

The resulting decision bound is O(N+M) field/graph operations plus O(M log(M+1)) canonical-key comparisons and their actual representation costs. In the specified unit-cost field/inversion and canonical-word comparison model this is O(N+M log(M+1)). Target extraction retains its separately stated S_B+O(N+M E_B) cost; all-target M may still be O(N^3). This is not an unconditional bit bound or a comparison bound over a generic equality-only field.

Algebraic-closure decision needs no quadratic-root extraction: a nonconstant finite-chart gcd or allowed infinity suffices. Base-field nonemptiness may need a separately charged certified quadratic-root test. Witness finding, field representations and output arithmetic are additional. Per-component roots can have degree at most two; a common explicit compositum is not free or promised small. Reconstruction can verify internal equations in each component's representation and cross edges through their rank-one zero factors, avoiding an uncharged common-field product. There is no column compatibility, supported-scale, legal-Green-parameter or full factorization/Fourier conclusion.

Independent checks pass: 1,920 random selected graphs over GF(2), GF(3), GF(5), compared with exhaustive assignments to the original bilinear equations; 687 satisfiable instances and 1,252 actual all-false component repairs; all 722 single-edge matrices over these fields; 511 complete flag patterns for k=0,...,8; a closure-versus-base-field quadratic counterexample; and the tight three-quadratic obstruction in four characteristics. Finite root enumeration in this independent verifier is a test oracle, not the asserted root algorithm or runtime.

## Native/publication acceptance guard

The companion ACCEPTED_PREFIX_SPEC.json contains only reviewed new prefixes, their target identities and baseline hashes. It supersedes author-candidate wording. It does not contain the full inherited native-cell text and is not an execution receipt.

Before applying any prefix, the publisher must freshly reread the exact userEnteredValue, stable row identity and protected status/score/history/gates. If any preimage changed, preserve the new current value verbatim, rebase the additive prefix, and recheck scope; never overwrite from the old snapshot. Change only listed userEnteredValue fields. Preserve formulas, notes, formats, dimensions, every unlisted cell, all old targeted text as an exact suffix, priorities and parent statuses. Mathematical acceptance does not close the primary-source comparison, constructor or wider parent gates. Do not increase historical theorem/novelty counts or duplicate closure credit.

Publish only verified safe artifacts, use actual published-byte hashes, then attach verified report/review links without inventing URLs. Perform exact postwrite readback, suffix preservation and protected-state checks before claiming native integration. The accepted prefixes remain eligible, but unapplied, until this fresh guard succeeds. This reviewer performed no native or repository writes.
