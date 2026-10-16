# ALG-039: a fully charged polynomial-input tree-jet ledger

Date: 2026-10-16. State: bounded construction and fresh exact controls complete; independent review pending. This is a next-batch candidate. It makes no external changes and does not modify the sealed 79-cell publication.

## Result

For the source's explicit polynomial tree operator K(z), supplied input coordinate polynomials of degree at most d can be processed in O(N(d+1)) scalar field operations and coefficient-address operations. The complete output has a structural capacity of exactly dN+2N−2 coefficient slots in the stated variable-length layout. This capacity **includes the root coordinate**. Each nonroot coordinate has degree **at most** d+v₂(s), with equality possible but not guaranteed. Cancellations may reduce actual degrees and nonzero counts.

This pays for one explicit K application, and for its constant-marker and fixed C/J interfaces. It does not supply or charge a coupled inverse, repeated feedback closure, an arbitrary polynomial marker contraction, or a Fourier coefficient-extraction circuit. Dense full-output materialization at d=Θ(log N) takes Θ(N log N) work in this output model. That observation is not an arithmetic-circuit or FFT lower bound.

## 1. Provenance and preserved state

The repository's `ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md` at the pinned commit is a sanitized 10,440-byte export, SHA-256 `8d55b12a5b65d41fef3dbc5bfa7ff87d78b0ab940b5323ee0888b0f991fa5d33`, Git blob `86d166654a61444ab268a8f208af21d93c114a63`; a fresh connector fetch verified both hashes. Its filename begins with the original source hash `e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f`, but that is not the export's content hash. The original locally available source is 10,468 bytes, SHA-256 `e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f`, Git blob `c8a91a0060f86e8fa5a5930f4cb06ff4c1607c1e`. Exact comparison shows only a private Library identifier replaced by `[private-id]`; all mathematical text is unchanged. The public export is copied in `sources/ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md`.

The source defines K in §2, the leaf-to-root recurrence in §2, the constant-input degree/capacity proof in §3, and the unresolved bordered inverse in §§4–5. The new result below is an explicitly derived extension of that recurrence, not a claim that the source already proved the polynomial-input cost.

Pinned source: [tree-jet report at commit 0339a31](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/e3/e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f__ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md).

The related one-Schur/two-run source, variable-bit source, and next-pivot/variable-bit audit are pinned in `SOURCE_REGISTER.json`. Their accepted bounded results, chart conditions and historical review status are preserved. No source-supplied program was executed or imported; only the freshly authored checker in this packet was run.

The native row read for this candidate confirmed ALG-039 at Catalogue row 140, novelty row 132, and Research overview row 201. Parent status is TO RESEARCH and priority is 34. The current recorded action still requests a primary-source comparison under the source/retained-state interface. This packet does not claim to complete that separate comparison or establish novelty. The broad missing construction remains a fast reduced-border/packet inverse or selected marked-coefficient circuit with polynomial sources, markers, roots and contractions charged, together with uniform recursive closure and shrinking workspaces.

Proposed changes are prefix-only candidates in `PROPOSED_EXISTING_CELL_PREFIXES.json`. They preserve every old cell value verbatim, all scores, statuses, proof grades and history, and require fresh read/rebase and independent acceptance before any later publication. No source URL for this unpublished report is invented.

## 2. Exact interface and computational model

Let N=2ⁿ≥2, n≥1, and d be an integer ≥0. Work over the source's field F with a supplied primitive Nth root ω; this implies characteristic different from 2. The tree identity itself does not use ω, but the source model and C interface retain it. The source operator is

    A₀e_s = e_(2s mod N),     E = e₀1ᵀ,
    K(z) = Σ_(t=0)^(n−1) zᵗ(A₀ᵗ−E).

The variable z is formal and distinct from the input coefficients. Input x(z) has N supplied coefficient arrays x_s[0..d]. Zero leading coefficients are allowed: d is a common upper bound. A zero polynomial has no nonnegative actual degree. The root input x₀ is annihilated by K and need not be read to compute Kx; its mass is needed by the separate bordered right-hand side.

One scalar field addition, subtraction or multiplication has unit arithmetic cost. Reading, writing, copying, zero-initializing and indexing one coefficient slot are charged unit operations. Address words must hold indices into O(N(d+n)) slots, so word size at least Ω(log(N(d+n))) is assumed. For d=O(poly(N)), this is the source's logarithmic-word routing regime. No field-element bit complexity, coefficient-height bound, numerical stability or root-finding algorithm is claimed.

The output is the explicitly materialized coefficient vector in the variable-length layout below, including its root coordinate. Compressed, implicit, shared-DAG, evaluation-only or selected-coefficient outputs are different interfaces and are not subject to this layout's write bound.

## 3. Polynomial recurrence and exactness

Initialize each nonroot array with x_s(z). Visit nonroot vertices in increasing v₂(s), generated without scanning all N states at each level:

    for h=0,...,n−1:
        visit s=2ʰa for odd a<N/2ʰ.

For every s whose parent p=2s mod N is nonzero, perform

    y_p(z) ← y_p(z) + z y_s(z).

Finally form y₀(z)=−Σ_(s≠0)y_s(z). The excluded propagation into zero is the edge s=N/2→0; there are exactly N−2 propagated edges.

For an odd target s there are no incoming doubling edges, so y_s=x_s. For even nonzero s, its two children have valuation v₂(s)−1 and are processed before s. Thus

    y_s(z) = x_s(z) + z Σ_(c:2c=s mod N) y_c(z),     s≠0.

Expanding the finite acyclic recurrence gives precisely the nonroot entries of Σ_(t<n)zᵗA₀ᵗx. The E terms vanish at nonroot coordinates. Since 1ᵀ(A₀ᵗ−E)=0, the defining Kx has zero coordinate sum, so the final root sum gives its exact missing coordinate. This proves the recurrence for polynomial x as well as constant x, by ring linearity or directly coefficient by coefficient. There is no division, convolution or generic polynomial multiplication: multiplication by z is a one-position shift, and each coefficient addition is charged.

## 4. Degree bounds, capacities and cancellations

Induction up the tree yields

    deg y_s ≤ d+v₂(s),                 s≠0,
    deg y₀ ≤ d+n−1.

There are N/2^(h+1) nonroot vertices of valuation h. The chosen structural layout therefore allocates

    C_nonroot = Σ_(h=0)^(n−1) (d+h+1)N/2^(h+1)
              = d(N−1)+2N−n−2,
    C_root = d+n,
    C_total = dN+2N−2.

The identity Σ hN/2^(h+1)=N−n−1 proves the displayed arithmetic. These are allocation capacities, not a universal count of nonzero coefficients. At d=0 they recover the source's 2N−2 bound. At N=2, C_nonroot=C_root=d+1, and there are no propagated nonroot edges. N=1 is excluded from this formulation; its empty-sum K is zero and should not be treated by the nonroot valuation formula.

The bounds are simultaneously sharp as degree bounds in the source's characteristic-not-2 model: if every x_s=zᵈ, the leading coefficient of y_s at degree d+v₂(s) is 2^v₂(s), and the root's coefficient at degree d+n−1 is −N/2. These are nonzero. For an actual fully dense witness, over C take every x_s=1+z+⋯+zᵈ. Every allocated nonroot coefficient is positive and every allocated root coefficient is negative, so all C_total slots are nonzero.

Actual degrees need not be sharp, even if every input coordinate has exact degree d. For N=4, take

    x(z)=zᵈ(1,1,1,−1)ᵀ.

Then y(z)=zᵈ(−1,1,1,−1)ᵀ. Coordinates 0 and 2 have degree d rather than their upper bound d+1. A root-only polynomial input is annihilated identically. Cancellations must never be used to replace the stated worst-case capacity by an unproved smaller universal cost, nor may upper bounds be reported as all-input actual degrees.

## 5. Scalar, memory, input and output ledger

Initialize the variable-length output arrays in C_total writes and copy at most (N−1)(d+1) nonroot input coefficients. The total child-array length on propagated edges is the full nonroot capacity minus the excluded N/2 array, whose capacity is d+n. Thus the direct schedule performs exactly

    W_edges = C_nonroot−(d+n)
            = d(N−2)+2N−2n−2

coefficient additions during propagation, including additions of zeros in the dense structural implementation. The final root accumulation performs C_nonroot coefficient subtractions into a zeroed root array. Edge index generation takes O(N) address operations. A shift requires no multiplication, but the individual shifted writes/additions above are not free.

Consequently this concrete schedule uses O(N(d+1)) field/address work and O(N(d+1)) coefficient storage, including output initialization and input/output handling. Its arithmetic addition count under the stated initialization convention is 2C_nonroot−(d+n), not one operation per polynomial. N input arrays have N(d+1) supplied slots; the algorithm can skip x₀ when computing K alone, and N−1 remains Θ(N) for N≥2.

Materializing this explicit complete layout entails C_total writes. The dense complex witness also has C_total genuinely nonzero coefficients, so even a representation that omits only zero coefficients cannot improve its output size. Therefore the worst-case complete materialized-output problem and this schedule both take Θ(N(d+1)) work in the specified coefficient IO model. For d=Θ(n)=Θ(log N), this is Θ(N log N). This is an interface/output-size statement; it is not a lower bound for extracting one coefficient, applying K at one scalar, compressed outputs, computing Fourier outputs directly, or general arithmetic circuits.

The boundary d=0 is linear. For d growing but o(n), this one explicit K application is o(N log N) in the coefficient-operation model; that fact alone does not identify a complete Fourier algorithm. Repeated applications must charge the current degree and current input/output arrays each time; their costs cannot be replaced by the d=0 cost.

## 6. C, J, marker, root and scalar specializations

For the source's fixed map (Cv)_r=ωʳ(v_r−v_(r+m)), m=N/2, pair the coefficient arrays and multiply each difference by its scalar twiddle. For r>0, r and r+m have the same valuation; row 0 has length d+n. Hence the structural CKx output capacity is

    C_CK = (d+n)+Σ_(r=1)^(m−1)(d+v₂(r)+1)
         = dm+N−1.

Every subtraction, scalar multiplication, output write and address operation is charged. The required twiddle table is prepared once in O(N) scalar multiplications from supplied ω, or supplied with its preparation charged. There are no twiddles in K itself. J injects a supplied degree-d half-vector into odd positions and zeros the others in O(N(d+1)) coefficient work if that intermediate is materialized; direct routing can skip that intermediate but is not assumed free. These statements pay CK, KJ and CKJ applications only.

For a supplied constant marker h,

    hᵀKx = Σ_(s≠0)(h_s−h₀)y_s.

The N−1 marker differences and C_nonroot scalar multiplications/accumulations give O(N(d+1)) work and an output polynomial of degree at most d+n−1. A nonconstant marker is outside this bound: its polynomial products must be charged separately, e.g. O(N(d+1)(e+1)) for naive dense multiplication when marker degree is at most e. No selected scalar from the coupled inverse is computed by this identity.

The mass 1ᵀx(z), used by the separate border, takes O(N(d+1)) additions if all input arrays are read. At any scalar z, including z=1, Kx is a polynomial evaluation with no pole or invertibility guard. If the inputs are supplied as coefficients rather than already-evaluated scalars, their Horner evaluations cost O(N(d+1)) before the source's O(N) scalar tree application. That input-evaluation charge must not be hidden.

## 7. Preserved inverse and recursive-closure obligations

The source's bordered matrix B(z) obeys det B(z)=det(I−zQ), and its scalar recovery requires this determinant to be nonzero. K itself has no such guard. An optional factorization through M(z) requires the additional M-chart condition and its remaining scalar denominator; full-border invertibility does not imply that optional chart is usable. At z=0 the formal inverse exists, but existence supplies no cheap coefficient algorithm.

The variable-block Schur evaluator still uses its own coupled D_E and S_b guards at scalar z, and the packet representation uses its coupled I−P_b guard. Formal constant-term invertibility must remain distinct from scalar guards. Individual branch invertibility or invertibility of the full Fourier system cannot certify an eliminated chart. The earlier exact finite-field guard counterexamples remain untouched.

The new direct K schedule refines, but does not erase, the older warning about polynomial right-hand sides. It is too broad to say that *this K recurrence* inherently requires convolution: it only shifts and adds. However, it costs O(N(d+1)), not O(N) uniformly in d. Products with other polynomial interfaces, nonconstant markers, repeated feedback, and the coupled border/packet inverse remain uncharged by the constant-input result and by this extension. In particular, no uniform recurrence T(N)=T(N/2ᵇ)+O(N) follows, and no scalar cost is assigned to an inverse, dense solve, determinant, generic jet or top-coefficient extraction.

The accepted variable-block structural frontier count S(N,b)=Θ(N min(n+1,2ᵇ)) remains an exact cost statement about its full-frontier evaluator. At b≈log₂n it remains Θ(Nn). Neither that warning nor this packet's output-size bound rules out a different shared representation or selected-coefficient circuit. No new primary-source equivalence, worldwide priority, unrestricted Fourier runtime or production-readiness claim is made.

## 8. Fresh checks and their limits

`verify_polynomial_tree_jet.py` is self-authored standard-library code. Its tree implementation is compared against a separate defining-sum oracle that routes every input coefficient according to each A₀ power and subtracts E explicitly. It verifies 164 finite-field/size/degree cases across GF(3), GF(17), GF(97), GF(257) and GF(65537), N through 128, with primitive root order checked for the C tests. All passed.

The same cases check exact slot counts, operation counts, zero coordinate sum, root-input annihilation, C output capacity and coefficients, constant-marker contraction, J injection, and 492 exact scalar specializations including z=0 and z=1. Separately, 28 integer witnesses have every allocated output coefficient nonzero; three all-coordinate-degree-d cancellation witnesses refute a universal actual-degree interpretation; seven root-only cases are annihilated; and 32 integer census cases extend through n=128 without allocating those large vectors.

These finite checks corroborate the proof and catch indexing/counting errors. They are not a proof for all N, do not solve a border, and do not claim finite-field success implies numerical or bit-complexity bounds. `CHECK_RESULTS.json` contains the case ledger. Independent acceptance is a separate review and must not be inferred from author PASS.

## Stop condition reached for this candidate

The polynomial-input K recurrence, all-size degree/capacity proof, explicit scalar/IO ledger, boundary examples, preserved inverse obligations, fresh controls and prefix-only publication proposal are complete. No broader coupled inverse, primary-source comparison or global parent gate is closed.
