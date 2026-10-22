# Independent review: uniform signed banks in positive characteristic

22 October 2026. Verdict: **ACCEPT**, with the exact field, grammar, and cost conditions below. No mathematical correction is required in the frozen candidate. This review author independently read the proof sources, independently derived the characteristic-sensitive steps and cost bounds, and authored fresh finite-field controls. No historical research program was executed or imported. No external publication or table update was performed.

## Frozen objects and exact scope

- THEOREM.md SHA256: `d994217b228c62bf36c3b0d66d55657733f42fe64aa286d33a95e0e82d23358c`.
- OPERATION_LEDGER.md SHA256: `41c18c4ab22e95f3b36ae14366f0896ea13a239f44532b08cea92fd0028a54f5`.
- Both are copied unchanged into `frozen_candidate/`. The complete author manifest SHA256 is `4c6379481f5b5e5a451c5e2eec0675ab72f3d798bc59625c0db19fe9a56fd1df`; all 12 covered files were byte/hash checked. Its frontier extract matches the four exact rows of the pinned classification. N13 completion remains inherited, not replayed; the broader owners remain open. AUTHOR_BINDING_RECEIPT.json records this separate provenance check. `SOURCE_FETCHES.json` records six independently fetched predecessor texts, their immutable URLs, SHA256 hashes, and independently recomputed Git blob identities.

Let N be odd, d>=4, N>=8d-10, and m=N-d. Let k contain a supplied primitive Nth root q, with characteristic not dividing N. The accepted result is an at-most-2m+2 representation of the negative unnormalized Fourier matrix by the original individual signed phase-weighted resolvent banks, over a genuine algebraic splitting extension. The same-sign orientations use the m distinct nonzero roots of one polynomial; the two cross-sign orientations have singleton node 1; all beta parameters are 1. Coincidence across orientations is legal. No derivative node, zero-node bank, trace-bank replacement, or relaxed moment-only representation is counted.

For infinite k the coefficient polynomial can lie in k[t]. For finite k=F_Q, q must already lie in F_Q and have exact order N, so N divides Q-1. Coefficients can be chosen in F_(Q^2); the genuine splitting field has degree at most m! over that coefficient field, hence at most 2m! over F_Q. The minimal finite-field splitting degree is the least common multiple of the irreducible factor degrees, not automatically m! and not asserted polynomially bounded. The ledger's F_(Q^(2m!)) is a paid splitting overfield. If the starting input lacks q or a certified field representation, provisioning them is additional work.

With d=floor((N+10)/8), every odd N>=23 has the bound 2N-2floor((N+10)/8)+2=7N/4+O(1) in every admissible characteristic. The 7N/4 constant and characteristic-zero theorem were already accepted. The additional result is the positive-characteristic field scope and quantitative finite coefficient descent, not a new bank constant, minimum, support classification, evaluator breakthrough, or novelty certification. The broader owners remain open.

## 1. Source-by-source proof chain

All predecessor reads use AgentSlop-Si/research commit `3834be7716370cfddf84ab1200da62b7887feb05`.

1. `research_cycle_1824/axis_nonvanishing/AXIS_NONVANISHING_CANDIDATE.md`, SHA256 `2a22a99baf19cdc6bd78f90323b77be7b4c1b11c1866286f4a174a731ecb5040`, supplies the enlarged envelope, sparse-support exclusions, exact fixed divisors, universal reciprocal lemma, zero-node degeneration and simultaneous-guard architecture. Its two genuine characteristic-zero uses are replaced below, not blindly inherited.
2. `research_cycle_1830/zero_node_axis_review/INDEPENDENT_REVIEW.md`, SHA256 `f5743fed9c7fd460676d8f019481c49d04e45e78add9b0af3b3b5a7169b72bda`, establishes that the prior 7N/4 result was already independently accepted only in characteristic zero. Its statement that the positive-characteristic caveat is real is respected: the derivative-at-1 comparison and generic separability must be checked anew.
3. `research_cycle_1735/common_annihilator_barrier/WHOLE_LEFT_RANK_ENVELOPE.md`, SHA256 `8bac3e52ef92ad00ab45ae55ab5cf9190e77e6855b3b752a8e569722f572998c`, Section 4 supplies whole-left reconstruction, reflection, quotient-axis conversion, raw weights and original resolvents. Each of these formulas is audited below for the new field scope.
4. `research_cycle_0958/signed_magnetic_fusion/final_v1/SIGNED_MAGNETIC_FUSION.md`, SHA256 `3632c6a28b0e976c4d4943cf3a2a160621ac8bbbe5a1d4fb143dfe1ac43e8bcb`, explicitly states the original grammar and Fourier Weyl formula over every field of characteristic not dividing N. It supplies the relevant distinction between signed integer powers and scalar signs, and separates counted banks from scalar runtime.
5. `research_cycle_1810/direct_axis_guard/DIRECT_AXIS_GUARD.md` was independently fetched as a rejection control. Its corrected quotient duality is consistent with the present proof. The rejected claim that reciprocal coprimality alone forces full legal axis rank is not restored. Here full rank is proved at an auxiliary zero-constant point and then transported only as nonvanishing of a polynomial minor.
6. `research_cycle_1735/common_annihilator_barrier/STEP_ONE_LINEAR_BANK_THEOREM.md` was independently fetched for predecessor context. Its older characteristic-zero squarefree/axis existence argument is not used as an all-characteristic lemma.

The first three paths above are under `math/checkpoints/2026-10-10-1839/sources/`; the original grammar is under `math/current/`. Exact full URLs and blob pins are in SOURCE_FETCHES.json. Classical algebra facts used here are proved within the argument; this review does not rely on external priority claims or a literature inference.

## 2. Envelope, interpolation and exact fixed divisors

The Gaussian product identity placing actual recurrence rows inside E is valid over any allowed field. All denominators involve 1-q^j for 0<j<N. Exponent halves and quarters mean inverses modulo odd N, not division by 2 or 4 in the coefficient field.

For the chirp C_k=q^(h k^2), rho=q^e, the shift factor S-lambda acts on its polynomial by q^h tP(rho t)-lambda P(t). A nonzero P gains a unique nonzero highest term in every characteristic. Thus the required product operators remain injective and their degree accounting does not change after reduction.

If an E-vector is supported on {0,1,m}, applying M of order d-1 to the zero interval 2,...,m-1 yields N-2d-1 distinct zeros for degree at most 4d-8. The assumed range makes the zero count strictly larger than the degree. Hence P=0 and then R=0. This proves joint independence of delta_0, delta_1 and delta_m modulo E, not just individual exclusions. In particular c_0,c_1,c_m are independent on U; c_1,c_m are independent on U_0.

For a fixed nonzero root x of U_0, the ML_x argument yields N-3d+2 zeros for degree at most 5d-9, a positive surplus N-8d+11. Both the leading and constant coefficients of the recurrence are nonzero, so its zeros propagate in both directions. Comparing positions 0 and N gives x^N=1. Writing x=q^s, uniqueness of coefficients modulo z^N-1 identifies the ordinary support with the translate of D's support. The nonzero endpoint coefficients of D already suffice: s and s+d-2 lie in [0,d-2], without wraparound because 2(d-2)<N. Therefore s=0.

The derivative-at-1 argument is also valid in small characteristic. M^2 annihilates k q^(jk): one application of S-q^j produces a scalar multiple of q^(jk), and the second kills it, even when k is interpreted modulo the characteristic. Recurrence propagation forces both R(1)=0 and R(1)=N D(1). The contradiction requires precisely N!=0, not characteristic zero. Sparse-functional independence makes 0 simple for U_0. Thus, over the algebraic closure as well, gcd(U_0)=t(t-1) and gcd(U)=t-1, with the stated multiplicities.

## 3. Generic separability: the essential repair

A nonzero linear coefficient does not itself make an arbitrary polynomial squarefree. For example, over characteristic two, 1+t+t^2+t^3=(t+1)^3 has nonzero linear coefficient and gcd with its derivative equal to (t+1)^2. This negative control is explicitly checked in the fresh test file.

The candidate avoids that error. For V_1=U/(t-1), the exact fixed-divisor result gives gcd(V_1)=1. Its universal polynomial H=sum Z_i h_i is irreducible in k[t,Z]: any factorization has total parameter degree one, so one factor is in k[t] and divides every h_i, hence is a unit. Positive t-degree ensures primitivity over k[Z], and Gauss's lemma yields irreducibility in k(Z)[t]. This argument applies over imperfect fields too.

If g=(t-1)h, coefficient comparison gives h_0=-c_0 and h_1=-c_0-c_1. Joint sparse-functional independence makes h_1 nonzero as a parameter polynomial, including in characteristic two. Therefore H' is not zero. An irreducible polynomial with nonzero derivative is separable: a nontrivial gcd with H' would force H to divide a polynomial of strictly lower degree. This establishes a nonzero discriminant guard, not squarefreeness of every specialization. The separately nonzero h(1)=g'(1) guard makes the restored forced factor t-1 simple. Normalizing the nonzero leading coefficient transports the full-degree squarefree condition to the same monic slice U_1.

## 4. Reciprocal lemma and zero-node full-axis guard

After dividing t(t-1) from U_0, its generic residual f is irreducible, has nonzero endpoints, and its endpoint functionals are independent. If f and its fixed-grade reversal shared a factor, they would be proportional. Reversal twice forces lambda^2=1; over characteristic two this has only lambda=1, which still forces an excluded endpoint relation. Thus the generic reciprocal resultant is nonzero in every allowed characteristic.

Choose the reciprocal-coprime residual over the algebraic closure and form monic g_0=t(t-1)f. No bank is assigned to its zero root. The quotient matrix uses only ordinary nonnegative residue powers, so all entries and minors exist polynomially at g_0. Its dependence equations are exactly g_0|A, g_0|J_N A, A(1)=0. Since A(0)=0, reversal yields rev(f)|A. The factors t, t-1, f and rev(f) are coprime as needed, so their product of degree 2m-2 divides A, whose degree is at most N-1. The strict degree gap forces A=0.

Hence one axis minor is a genuinely nonzero polynomial on U_1. The constant, discriminant and axis guards all live on this same irreducible affine linear space, so their product is nonzero. No invalid legal-point reciprocal/full-rank shortcut or assumption of squarefreeness at g_0 enters.

## 5. Finite-field descent and degree audit

For monic g, coefficients of t^j mod g have total coefficient degree at most max(0,j-m+1). Multiplication by t and replacement of t^m proves this inductively. The nonconstant row-degree maxima in X_N(g) are d,...,1 in rows 1,...,d and 1,...,d in rows m,...,N-1. These sets are disjoint in the stated range. Their sum is d(d+1), bounding every N-column determinant. Affine parametrization of U_1 cannot increase degree.

The ordinary monic discriminant has degree at most 2m-2 in every characteristic; the constant guard has degree one. Thus one nonzero simultaneous guard has total degree at most H=d(d+1)+2m-1=d^2-d+2N-1. Characteristic two may square the discriminant polynomial, but neither changes this upper bound nor changes the squarefree/nonzero equivalence.

Because q has exact order N in F_Q, Q>=N+1. The candidate's inequality H<Q^2/2 is valid. An independent direct check is

    (N+1)^2-2H = N^2-2N+3-2d^2+2d
                  >= 62d^2-174d+123 > 0,

using N>=8d-10 and d>=4. The multivariate finite-grid zero bound therefore guarantees a point over E=F_(Q^2), with success probability greater than one half under independent uniform E-valued parameters. The exact rank test may succeed even when the particular theoretical minor vanishes; its failure set is contained in the product guard's zero set. Thus expected fewer than two trials is valid, but is not a deterministic two-trial guarantee. All failed trials are charged by the ledger.

No unrestricted base-field attainment is claimed. For an arbitrary positive-characteristic field containing q, F_p(q) is finite; composing its constructed extension with k preserves the degree-at-most-2m! bound.

## 6. Literal banks and characteristic two

The orientation signs are integers selecting S versus S^-1 and T versus T^-1, not coefficient-field scalar signs. They remain distinct for the present odd N. Each signed commutation root q^(epsilon delta) still has exact order N.

The Weyl coefficient formula follows from trace extraction and completing the square modulo N. The Gauss product G_-G_+=N follows by the invertible change of residue variables (s,t) to (s-t,s+t). Thus its scalar gamma is nonzero in every allowed characteristic. No inversion of the coefficient-field element 2 is present.

The same supported Gaussian products, consecutive-power Vandermonde solves and monic recurrences reconstruct all positive rows. Nonzero distinct roots make the relevant Vandermonde matrices invertible. Reflection permutes integer exponents and signs, supplying negative rows without creating banks. The quotient-axis rank gives the remaining row and the moment-to-root map is invertible. Sector indices remain bijections, so no row assignment conflicts.

For beta=1, the quantum-binomial identity gives X_j^N=(alpha^N+1)I: intermediate Gaussian coefficients vanish at the primitive Nth root, and their denominators are nonzero. Hence Delta=-alpha^N is a unit and the finite geometric sum is a two-sided literal inverse. Finite-character inversion of the stated raw weights yields the matched Weyl coefficients and therefore the original Fourier matrix. Characteristic two changes minus signs to plus signs but does not invalidate any identity or legal denominator.

## 7. Constructive ledger audit

The ledger is fully conservative and explicitly expensive.

- A supplied certified F_Q and exact-order q are input assumptions, not free implicit outputs. Order can be verified with O(N) successive multiplications. A quadratic coefficient extension is obtained by at most Q^2 candidates, each tested at Q field elements: O(Q^3) base operations. A supplied representation's own cost is separately exposed.
- Envelope/nullspace/monic preparation and each exact legal-coefficient test cost O(N^3) field arithmetic and O(N^2) storage. Deterministic enumeration is exponential in the number of parameters; the randomized option has expected fewer than two tests only after field preparation.
- With t=m! and R=Q^2, all irreducible factor degrees divide t. A degree-t irreducible can be found by the ledger's exhaustive monic-divisor test. Its bound O(t^2 R^(t+floor(t/2))) E operations is valid. Enumerating all R^t field elements and evaluating g costs O(m R^t) L operations, or O(m t^2 R^t) E arithmetic with schoolbook multiplication. These procedures genuinely produce roots; they do not treat formal algebraic symbols as a free splitting field.
- Post-root preparation reuses one Vandermonde inverse, pays all row and axis solves, materializes all BN raw weights, and normalizes them by 1/N. Its O(N^3) L arithmetic and O(N^2) L storage bounds are valid, with inversions separately charged. Optional dense inverse verification costs O(BN^3)=O(N^4), separately and explicitly not claimed executed.
- For a warm branch, exactly one diagonal vanishes at i_0=-epsilon j. The equation there starts the backward recurrence without division by a vanishing diagonal; alpha is nonzero. Per bank, computing -x/alpha costs N multiplications, the N branches require N(N-1) recurrence multiplications and additions, and weighting all branch outputs costs N^2 multiplications. Accumulating the N branches costs N(N-1) additions. Thus each bank costs exactly the stated conservative 2N^2 multiplications and 2N^2-2N additions. Adding B bank outputs gives 2BN^2 multiplications and 2BN^2-BN-N additions, including every output coordinate.
- Addressing, input/output, weights, and extension coordinates are not free. Expanding into E costs O(BN^2 t^2) arithmetic for multiplication. Each L element uses 2t base-field coordinates. The resulting cubic warm field-operation bound, in an enormous extension, gives no arithmetic advantage over the ordinary quadratic dense base-field Fourier evaluation.

No uniform bit-complexity guarantee or arbitrary infinite-field algorithm is inferred from the unit-cost field ledger. Those limitations are stated correctly in the candidate.

## 8. Fresh exact controls and final boundaries

The newly authored `independent_controls.py` runs four exact fixtures:

- N=31 over F_(2^5), modulus x^5+x^2+1.
- N=63 over F_(2^6), modulus x^6+x+1.
- N=31 over F_(5^3), modulus x^3+x+1.
- N=121 over F_(3^5), modulus x^5+2x+1.

Each field is checked by verifying every nonzero element's computed inverse. Each q is certified by checking all positive powers below N. The controls independently construct E, prove the three sparse functionals independent by exact rank, compute gcd(U) and gcd(U_0), test derivative exclusion and the residual linear functional, construct actual whole-left Gaussian rows and verify annihilation, and find a concrete legal monic squarefree witness with full quotient-axis rank. They then verify solvability of all 246 physical rows in total and check the Gauss product. This includes small characteristics dividing m and/or d, not just large primes. The output and witness coefficients are retained in INDEPENDENT_CONTROLS.json.

A second new script, `literal_bank_controls.py`, directly constructs original branch inverses by the zero-diagonal recurrence at N=31 over F32 and N=7 over F29. Across all four orientations at both fixtures it verifies 4,040 branch/right-hand-side solves and 4,040 weighted-bank matrix entries against an independently assembled Weyl expansion. It also checks 1,010 entries of the negative Fourier Weyl identity, rejects the wrong Fourier sign and wrong recurrence direction, and detects omission of 1/N in the odd-characteristic fixture. In characteristic two that normalization alone is indistinguishable because odd N equals 1 in the prime field; the record says so. N=7 is an original-grammar control, not an instance of the N>=23 theorem. LITERAL_BANK_CONTROLS.json retains these results. These controls are the executed subset, not a claim that every suggested author-checklist mutation was run.

The finite examples are implementation controls, not the proof of uniformity, field descent, or splitting-field construction. No enormous m! field or complete large assembled Fourier bank representation was materialized. The uniform conclusion rests on the source-bound algebra above.

**Final disposition: ACCEPT the frozen scoped extension and ledger.** Do not report a new leading bank constant, polynomial extension degree, unrestricted minimum, broad owner closure, general FFT speedup, or historical novelty. No external mutation, approval denial, or pending permission is involved in this review.
