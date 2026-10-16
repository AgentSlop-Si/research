# ALG-079: totality and exclusive field costs of the named short-probe detector

16 October 2026 UTC. Baseline repository: AgentSlop-Si/research, commit `35d9dcdc3f3869de75b33b2b09705222e8d09e8d`.

## Result and exact disposition

The complete active detector `discover_short_probe` and its computational callees admit an all-input **normal-return, soundness and finite field-cost theorem** under the explicit ordinary-input contract below. This advances the detector obligation beyond finite test coverage. It is a source-level mathematical proof, not an execution claim or a production RAM/bit/time guarantee.

The bound pays the actual deterministic quadratic-nonresidue search in the linear-trace branch. It is consequently **not an unconditional O_s(N) bound uniform in the prime p**. An exact arithmetic ledger repairs the detector's omitted operations and partitions the lazy residual callback from the detector. The completed CSM1 compiler is used only at its existing separate boundary.

Recommended owner disposition: accept this named detector mathematical child, subject to independent review; keep ALG-079 progressed/open and priority 12 unchanged. The exact migrated-caller source and backend were not recovered in this pass, so complete nonoverlapping cold-lifecycle qualification, all callers/importers, storage/bit/time and practical speed remain open. Do not relabel these remaining obligations as fulfilled or silently archive the parent.

## 1. Exact source and model boundary

The proof is bound to the following complete source files. Historical files were read and hashed as inert text; none was imported, compiled, AST-parsed or executed.

| File | SHA-256 |
|---|---|
| short_probe_fusion.py | `9b976c4415f9520be284c2a07a0857f00035c703d214b01994a7c7b3db8f5675` |
| compressed_resultant.py | `8443a29ea819faf996c6fed51f9e88d2b9def760ec5317f76e542cb73050b3e0` |
| joint_pencil.py | `1fe849cfc43d9c4a49eaa6da4d0984b98a82a5395856bc557b7b498d1813f6cf` |
| trace_subgroup.py | `f24410eed4092e29c788bfbd66ce518789ef845b43438759efc17a2dfadf42d3` |
| reciprocal_union.py | `246db30e69b2988aa24134b41b21496727c7e1e67c2af9abbb3d133adc7a037a` |
| annihilator_engine.py | `c455b803851d82815af2252dc6bb7e538b8b33f9492ba3318abaed393e816c22` |
| blind_sparse_rational.py | `466aa894ea3aed15a01931c9c415f5e6b16a5f6e2c7209ee2ef4968fc50d4a6c` |
| blind_inverse.py | `f2395dd34e71b0c27f6358230b3a9b88a84f64414bb184c39ea0a1f6bc8f5d40` |
| resultant_gate.py | `4a1c07d1d6933a399871655eef547451fe8cb24fd026ab70b733b45bda9d8038` |

These nine files form the runtime mathematical closure used here: prefix streaming, batch inversion, joint resultant construction, interpolation, trace sieve, scalar square root and BSGS/half-scan, candidate pencil gcd, BM/Prony, sparse denominator evaluation and complete cyclic certification. Unused import dependencies and module-loading costs are outside this call contract. In particular, the active route does not call Bluestein, the older `sparse_group_eval`, or `discover_reciprocal_union`.

The accepted polynomial source `PROOF_ALGEBRA.md`, SHA-256 `f7aef958bb7f1d226391c3873609c6b1c577003e166f3b30234dc0f6a95c6d1d`, and complete Phase22 and Phase23 independent reviews were reread. Their polynomial result is summarized in Section 3; finite reported controls are not used as a universal premise.

Cost model F1 counts every executed field multiplication M (including multiplication by 0 or 1), field addition/subtraction A, unary coefficient negation N, and field inverse I separately. Constants in the source, including literal −1 and −2, are supplied field constants. A modular inverse is one abstract inverse, not one machine step. Canonical residue reductions, integer control/index arithmetic, integer binomial-coefficient generation, hashing, allocation, container traffic, telemetry and module setup are outside F1. The complete list is a declared mathematical operation model, not a hidden unit-cost RAM assertion. Abstract built-ins finish and sufficient resources exist; interruption and allocation failure are excluded.

## 2. Admitted input contract

Let n be dyadic, 2<=n<=4096, p a supplied/previously validated prime with 2<=p<=2^31−1 and n|(p−1), and omega an exact-order-n root. `engine.n`, `engine.p`, `engine.omega` are these plain integers, and `engine.powers` is the stable ordinary list [omega^j mod p] for 0<=j<n. The root/field admission and table construction have already occurred and must be charged by the caller.

Use plain integer s with 1<=s<=8 and exactly `extra_witness=3`. Set ell=2s+2, b=s(s+1)(2s+1)/6, v=s(s+1)(4s+5)/6, m=s+1. If n<ell or p<=4b+20 the source returns refusal immediately. Active execution is considered only when both inequalities pass.

The residual r is an ordinary stable length-n list of canonical residues. Either prefix_R is None, or it is an ordinary stable length-ell list of canonical residues. For normal return and accepted-output soundness, the supplied prefix need not be trustworthy: the full certificate protects any accepted output. For the usual discovery semantics it equals the first ell Fourier values of r. Noncanonical values, wrong lengths, integer subclasses, hostile properties, concurrent mutation and reentrant accounting sinks are not admitted.

The accounting sink is None (constructing the ordinary historical Work record) or the ordinary exclusive Work record with plain integer counters and its ordinary PolyStats object. Existing counter values are irrelevant: all formulas use deltas.

Lazy variant: r may instead be None only with a supplied canonical prefix and a callback which, if called, terminates, returns this stable canonical n-vector, does not mutate detector state, and has an independently paid cost. The source invokes it at most once, assigning the returned list to r before testing any certificate. The theorem is compositional in that callback contract; it does not promise termination of arbitrary user callbacks. If the callback updates the same Work sink, its delta is subtracted when forming detector-exclusive counters below and added once at the caller boundary.

No malformed-input validator is claimed. A prime-field contract is necessary: oddness alone does not make modular inverses or Tonelli–Shanks safe. The accepted finite cold API's stronger admission is separate evidence and is not replaced by this detector's lightweight guards.

## 3. Assertions and inversions are safe on every admitted input

### Reciprocal probes and compressed construction

The zero-probe gate precedes batch inversion. Every product inverted by batch inversion is nonzero in F_p. The batch uses exactly 3k products and one inverse for k>0.

The reciprocal sample picker asks for r0=b+4 distinct traces t=w+w^−1, with w in {2,...,p−1}. Each trace has at most two preimages, because its preimages satisfy w²−tw+1=0. Thus at most 2r0 trials suffice to obtain r0 traces. The guard p>4b+20 supplies more than enough nonzero/nonidentity candidates. Every tested w is invertible. Interpolation differences between distinct traces are nonzero.

At a sample w, `shared_res_at` builds the two Hankel pencils P_e(a,w)=det[T_(e+i+j)(1−a w^(e+i+j))], e=0,1, order m=s+1. Its largest T index is 2s+1=ell−1. Interpolation in a uses the m+1 nodes 0,...,m; p>m makes all interpolation inverses valid. Gaussian determinant elimination inverts only a selected nonzero pivot. Singular matrices return zero, not an exception. Padding to degree m before the Sylvester determinant preserves the fixed-degree homogeneous resultant convention even when a leading coefficient specializes to zero.

The universal integral identity is

    Res_a(P_0,P_1)=w^v (w−1)^(m²) U(w),
    U(w)=w^b V(w+w^−1), degree V<=b.

For clarity, its algebraic basis is independent of probes being Fourier data. Simultaneous reversal of the two a-polynomials gives the grade-D reciprocal identity, D=m²(2m−1). Substituting w=1+epsilon and a=1+epsilon*t into each determinant gives epsilon^m, and the resultant affine-change law yields the factor (w−1)^(m²). Over the generic rational-function field in the T variables, Cauchy–Binet gives coefficient valuations j(j−1)+ej. The two Newton polygons have root valuations −2i and −(2j+1); distinct parities prevent root-difference cancellation. Their resultant valuation is v. Hence all coefficients of w-degree below v vanish identically as integral polynomials in T, so the divisibility survives arbitrary field specialization. The remaining reciprocal grade is D−2v−m²=2b. Symmetric integral Laurent polynomials are polynomials in w+w^−1 (the recurrence w^j+w^−j=t(w^(j−1)+w^(1−j))−(w^(j−2)+w^(2−j)) is integral). Therefore no division by characteristic-dependent constants is hidden in V's existence.

Every normalization denominator w^(v+b)(w−1)^(m²) is nonzero. Newton interpolation at b+1 distinct traces recovers that degree-at-most-b V exactly. The three extra witnesses therefore agree identically, including degenerate data and zero resultants; the witness assertion cannot fail in exact arithmetic on this contract. The explicit binomial expansion of w^b V(w+w^−1) is symmetric, so the palindromicity assertion also cannot fail. The map V to U is injective: a highest term of degree d gives a nonzero term of degree b+d in U. Consequently nonzero U implies the V supplied to the trace sieve is nonzero.

### Polynomial division and trace sieve

Both polynomial Euclidean routines invert only nonzero leading coefficients. Each long-division step cancels the current highest coefficient exactly and strictly lowers the dividend degree; each outer Euclidean step strictly lowers the nonzero divisor degree. `trim` loops remove entries, never add them. The zero/zero gamma-gcd case returns [0]. Empty-polynomial and constant cases are handled before a forbidden inverse or divisor.

Removing t−2 factors lowers degree after each successful removal; its one possible failed attempt exits. The remaining modulus is either constant (immediate refusal) or monic of degree at most b. The Dickson computation has log2(n) dyadic rounds. Every intermediate polynomial is reduced to degree below the modulus before another round.

The identity D_n(w+w^−1)−2=(w^n−1)²/w^n shows that a positive-degree gcd contains exactly candidate subgroup traces after removing t−2. All n-th roots are in F_p, because n|(p−1) and the supplied root has order n. Thus the subsequent linear or half-scan enumeration is exhaustive for these trace roots. This is a candidate-enumeration property, not a claim every candidate is a structured model.

### Scalar root extraction and discrete logarithms

For odd prime p, Euler's criterion rejects nonsquares. If the input square is zero, `modular_sqrt` returns zero. The p mod 4=3 exponent formula is exact. Otherwise factor p−1=2^h q, q odd. The deterministic search z=2,3,... reaches a nonresidue by z<=p−1, since the nonzero field has (p−1)/2 nonresidues and 1 is a square. This is finite but is not a supplied-polylogarithmic nonresidue oracle.

Tonelli–Shanks maintains x²=a*t, c of exact order 2^M, and t of order dividing 2^(M−1). Initially these follow from Euler's criterion for square a and nonsquare z. When t!=1, its least squaring exponent j satisfies 1<=j<M. Updating by c^(2^(M−j−1)) preserves x²=a*t and makes the new t have order dividing 2^(j−1); M becomes j. The integer M strictly decreases. The internal nonresidue exception is therefore unreachable, and the final x²=a assertion holds.

BSGS has a finite table of mu=floor(sqrt(n))+1 entries and at most ceil(n/mu)+1 giant iterations per target. Its step is omega^(−mu). Every subgroup exponent d in [0,n) decomposes as i*mu+j with 0<=j<mu and i<ceil(n/mu), so all target subgroup roots are found. Dictionary lookup is a contracted finite operation, not an asserted constant-cost worst-case RAM primitive. No sorting replacement is silently substituted for the executed dictionary.

### Prony helpers and certificate

Every candidate pencil has finite size m. At most 2b candidates enter the main loop; this follows both from degree U<=2b and the explicit candidate-count refusal guard. The source generates its own ordinary finite candidate list, so the unrelated legacy API's optional arbitrary iterator is not on this execution path.

BM receives exactly 2s samples and has at most 2s iterations. Its stored discrepancy denominator starts at 1 and is replaced only by a nonzero discrepancy. At iteration k, L<=k and C has at least L+1 entries, so every discrepancy index is valid. The standard update invariant follows directly from the last update index k0: the saved B is the previous C, delay=k−k0, and the extension delay+len(B) supplies at least the new L+1 slots when L is replaced by k+1−L. Before any next iteration L>s is refused. C and B have at most 2s+1 entries during this call; all finite list extensions and slices are safe.

The returned recurrence degree d is checked to be 1<=d<=s. Its roots are scanned through n supplied field values. If exactly d distinct roots are found, the constructed d-by-d Vandermonde is nonsingular. The modular linear solve nevertheless checks every pivot and would refuse a missing pivot. Its inversions are thus safe without relying on a test suite. Every recovered key lies in [0,n), every retained coefficient is canonical and nonzero, and the support size is at most s.

The prefix fit scan is finite. The denominator scan constructs all n Fourier values and rejects any zero. The full cyclic certificate visits at most n entries, each with at most s taps. Every acceptance visits all n entries. Failures continue to the next finite candidate; no invalid 4s-probe uniqueness shortcut is used. The lazy residual is loaded at most once under the callback contract in Section 2.

This proves normal return for every admitted input, including arbitrary residuals, failed models, singular pencils, zero resultants, repeated resultant roots and failed certificates. It is not inferred from successful tests.

## 4. Accepted-output soundness

On every accepted result (A,delta,alpha,Ahat), 1<=delta<n, alpha!=0, 1<=|A|<=s, Ahat[k]=sum_e A[e]omega^(ek) is nonzero for every k, and the literal complete scan establishes

    sum_e A[e] r[(j−e) mod n] = [j=0]−alpha[j=delta]

for every j. Taking the DFT gives Ahat[k]*(F_n r)[k]=1−alpha*omega^(delta*k), hence exact recovery by division at every frequency. This proof requires neither the correctness of a heuristic model guess nor the supplied prefix being honest. A refusal means no model was accepted by these gates; it is not a completeness statement for every sparse rational representation.

The caller may combine this result with separately proved LF=FP and invertibility of L to recover F_n x. No new Green-constructor, fallback-backend or all-caller claim is made here.

## 5. Exact exclusive field-operation ledger

Let W_M, W_A, W_I be the detector-exclusive deltas of the ordinary Work multiplication, addition and inversion counters. Exclude any residual-loader interval, and exclude preview, Green setup, compiler, decode and solve. Define six source-event aggregates:

- G: sum of the returned polynomial lengths at the final monic-normalization list comprehension of every call to `blind_sparse_rational.poly_gcd`; zero for the zero/zero early return.
- H: number of row swaps in all `resultant_gate.det_mod` calls.
- R: number of executed compressed-resultant normalization samples (the expression containing w−1), either zero or b+4 on an admitted complete compression call.
- J: total checked cyclic-certificate coordinates, including failed prefixes of scans.
- Q: number of executed candidate-alpha unary negations after a degree-one gamma gcd, including alpha=0 rejections.
- L: 1 if the linear-trace extraction routine is entered, else 0.

Then the complete F1 vector for the detector call is exactly

    M = W_M + G,
    A = W_A + R + J,
    N = H + Q + L,
    I = W_I.

The correction sites are exhaustive for this runtime closure. Gamma-gcd normalization multiplies every returned coefficient but updates no multiplication counter. Each compressed normalization executes w−1 without an addition charge. Every checked cyclic coordinate constructs its right side by a subtraction without an addition charge. Determinant sign changes, alpha extraction, and linear-trace coefficient negation are the three unary-coefficient-negation sites. All other executed field product/add/subtract/inverse expressions in the listed closure have matching literal counter increments, including final loop updates even when their computed value is subsequently unused. Representation modulo operations and integer exponents/indices are outside F1 by definition, rather than lost arithmetic.

This is an algebraic source identity over every admitted execution trace. No Work grand total is added to it: Work is already a projection of the same arithmetic. G<=2b(s+2), Q<=2b, J<=2bn. R<=b+4. H is bounded by the total matrix orders across the bounded determinant calls. The formula includes failed candidates and the unsuccessful part of every certificate.

## 6. Explicit finite all-input bound

The following deliberately loose bound gives a uniform, computable ceiling rather than relying on empirical traces. All quantities count M+A+N+I in F1. Put bit(x)=floor(log2(x))+1 for positive x, a=log2(n), r0=b+4, mu=floor(sqrt(n))+1, gamma=ceil(n/mu)+1, and

    D(k)=2k³+k²+3k.

One k-by-k determinant costs at most D(k): k pivot products/inverses, at most k sign changes, at most sum_{h<k} h factor products, and at most sum_{h<k} h² product/subtraction pairs. Ordinary interpolation at the nodes 0,...,q costs at most 6(q+2)². Newton interpolation at z arbitrary distinct nodes, including their differences and batch inverse, costs at most 8(z+1)². Euclidean gcd at input degrees at most d, including monic normalization, costs at most 4(d+2)³: at most d+1 divisor stages, at most d+1 strictly degree-reducing cancellations per stage, and bounded normalization.

Define the joint-resultant-sample bound

    Z(s)=2s+1 + 6m(m+1) + 2(m+1)D(m)
         +12(m+2)² + D(2m).

The full compressed construction is bounded by

    C(s)=r0[Z(s)+2bit(v+b)+2bit(m²)+10]+1
         +8(b+2)²+6(b+1)+(b+1)(b+2).

Here the +10 per sample covers reciprocal-trace trials, normalized denominator construction including w−1, batch inversion products, and scaling; 2bit(e) bounds each charged exponentiation. The last terms pay arbitrary-node interpolation, three witnesses, and palindromic expansion. Binomial integer arithmetic remains outside F1.

The trace sieve is bounded by

    T(s,n)=4(b+2)³+3(b+2)²+(4b²+1)a+20.

The terms cover factor removal, normalization, degree-one initial reduction, one reduced square per dyadic bit, and the final Euclidean gcd. A reduced polynomial product has at most b² convolution and b² reduction coefficient visits, each a product/addition pair.

For candidate extraction let h0=bit(p). A safe modular-square-root bound is

    S(p)=2h0(p+2)+2h0²+3h0+1.

It pays at most p−2 nonresidue Euler tests, initial Euler test and initialization powers, strictly decreasing Tonelli–Shanks rounds, and the final check. This intentionally coarse bound includes cases that return much earlier. A ceiling for either actual extraction branch is

    E(s,n,p)=(2b+3)floor(n/2)+S(p)+7+mu+2gamma+10bit(n).

The half-scan and linear-branch ceilings are added for convenience although only one branch runs. The half-scan pays the trace sum and every Horner coefficient. The linear branch pays trace negation, discriminant and quadratic roots, subgroup powers, BSGS table/giant products and verification powers. Lookup, sorting and integer-square-root costs are explicitly outside F1.

For a single main-loop candidate define

    P(s)=4s+1 + 6(s+2)(2s+1) + 2(s+2)D(s+1)
         +12(s+3)²+4(s+3)³+1+4ell
         +16(s+1)²+s²+4(s+2)³+3ell*s.

This pays two unshared pencils and their interpolations, gamma gcd, alpha negation, corrected sequence, BM, Vandermonde construction/solve, and full prefix matching. BM's at most 2s discrepancy/update iterations cost at most 16(s+1)². Subgroup recurrence-root evaluation, sparse denominator evaluation and full cyclic certification together cost at most (6s+1)n; the final +n includes all certificate right-side subtractions.

Therefore every admitted detector call, with any early exits, satisfies

    F_det <= n(2ell−1) + (3ell+1) + C(s) + T(s,n)
             + E(s,n,p) + 2b[P(s)+(6s+1)n].

If a prefix is supplied, remove n(2ell−1); its production belongs to its caller. If the residual is lazy, add its independent cost at most once. This proves finiteness across the complete detector, including its p-dependent search. The bound is not asserted tight, and simultaneous attainment is not claimed. It does not convert the algorithm into an unrestricted linear-time or sub-NlogN Fourier transform.

## 7. Nonoverlapping caller composition and remaining gate

Use disjoint executed intervals, with the corrected detector vector above assigned to exactly one interval:

    cold admission/root/Green preparation
    + actual preview graph
    + Green probe conversion
    + exclusive detector
    + optional single residual materialization
    + optional compiler
    + either remaining fallback graph, or decode and solve.

Each source operation has one owner. Failed optional setup remains in preparation. Preview and fallback completion partition one graph; completing it pays exactly n log2(n) additions/subtractions and (n/2)log2(n) products across both intervals. Residual materialization is excluded from exclusive detector work and paid once. The completed compiler's actual arithmetic is not added to its own Work projection. The accepted decode tail has 6n products, n additions/subtractions and one inverse, before the separately scoped replacement solve: n products/zero additions if beta=0, otherwise 3n products and 2n−1 additions. This composition does not add overlapping global Field and Work totals.

These equations specify the required accounting partition and permit a later source-bound implementation. They do not prove that an unavailable migrated caller implements every interval or that its setup/physical resources are bounded by these numbers. Source `migrated_caller.py` SHA-256 `843e5c12db800b530d200ab7d545ada01a29d3fae93881a24c1deaea342dfd00`, accepted backend `2141c18183e619322443a5bb5660fe52c88018484ccca2392bf88650ef9354d3`, and bridge `da8dcf482f4c6b4ae022cdf50b974b6b828747afa81cab97ab20a6e2ab02023b` remain required for a complete new caller theorem. The pinned public caller review was fully read, but a report is not a substitute for those program bytes.

Unrestricted historical signature counterexample: `discover_reciprocal_union` accepts an arbitrary candidate_shifts iterable. Take the otherwise well-formed legacy input n=4, p=5, omega=2, powers=[1,2,4,3], r=e0=[1,0,0,0], max_terms=1, and an infinite stream of zero candidate shifts. Its first four Fourier probes are all 1, the reciprocal batch is defined, and line 146 continues forever before incrementing a rank-candidate counter. This refutes totality for that unrestricted optional-iterator API; it does not affect `discover_short_probe`, which constructs a finite list internally. Similarly, arbitrary nonterminating residual callbacks are outside any honest detector-totality theorem. No supplied program was run to establish these direct source counterexamples.

The appropriate completion is the named detector child under F1 and the contract above. Whole lifecycle, other callers, root/prime admission costs, module ingestion, allocation/traffic, bit/elapsed time, wider APIs and practical comparisons remain precisely distinct gates.

## Sources and verification status

- [Pinned historical caller acceptance](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-12-trial-accuracy-caller/alg079-historical-caller.md).
- [Pinned completed CSM1 compiler review](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-12-compiler-scan-qualification/alg079-named-compiler-csm1.md).

This packet executes only newly written arithmetic/bound checks. It does not execute supplied research programs or replay historical tests. Those finite controls check the displayed combinatorial ceilings and small independent algebraic lemmas; the all-input claims rest on the source proof above. Independent review must assess these claims before owner acceptance or publication as an accepted result.
