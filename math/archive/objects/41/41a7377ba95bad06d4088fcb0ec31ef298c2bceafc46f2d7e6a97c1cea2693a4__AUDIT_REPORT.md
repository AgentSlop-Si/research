# Sparse-defect Fourier gate: independent bounded audit

Audit date: 2026-10-09 UTC. Source internal title/date: 2026-10-10. Verdict: **retain the scoped Fourier theorem; repair the scan escape claim and charged Woodbury costs. No faster arbitrary-input FFT and no universal FFT lower bound.**

## Findings in order of importance

1. **The Fourier rank obstruction is correct.** For every row-q-sparse B, rank(F_N-B) >= floor(N/(q+1)); arbitrary endpoint monomials and inverse Fourier are included. The proof uses m consecutive original Fourier frequencies and m columns outside the union of their B supports. The resulting Vandermonde minor is nonsingular. No full-spark claim for arbitrary Fourier minors is needed; in particular composite N causes no flaw.
2. **The inverse-stage product obstruction is correct.** Telescoping gives a rank budget sum r_j; products of row-s_j-sparse matrices have at most product s_j nonzeros per row. Hence sum r_j >= floor(N/(1+product s_j)). Arbitrary intervening monomial connectors can be absorbed without changing these budgets. Singular sparse baselines B_j and exceptional low-rank corrections are allowed; only the actual G_j are required invertible.
3. **The original scan inverse and bandwidth theorem are correct, but the supplied proof does not establish its broader title/interpretation.** Banded matrices in one ordering are only a subset of arbitrary row-sparse matrices. A new independent combinatorial minor proof now repairs that gap: for the displayed S and every row-q-sparse B,

       rank(S^(-1)-B) >= ceil(floor(N/(q+2))/(2q+1)).

   At fixed q this is a linear-in-N bound. It is invariant under arbitrary endpoint monomials. Full proof and corners are in ARBITRARY_SPARSE_REPAIR.md. This is a bounded mathematical correction, not a priority or optimality claim.
4. **Woodbury setup is understated for variable r.** The source explicitly forms V^T Z, an r-by-r matrix with N-term inner products. With classical arithmetic, fully charged preparation is O(N+Nr^2+r^3), fresh-vector application O(N+Nr+r^2), and stored data O(N+Nr+r^2). At fixed r both remain O(N), so the principal architecture exclusion survives.
5. **The source implementation is narrower than the algebraic theorem.** Its no-pivot Thomas plan requires every elimination pivot nonzero, stronger than nonsingularity of T. Woodbury additionally requires T invertible and K=I+V^T T^(-1) U invertible. These conditions are absent from, and unnecessary for, the rank theorem.

## Scope and quantitative implications

For fixed s >= 2 and rank allowance r, the necessary condition tr >= floor(N/(s^t+1)) implies t >= log_s N - O(log log N). For s=1 it gives sum r_j >= floor(N/2). For r_j=0 it already implies product s_j >= N, equivalently the direct dense-support requirement. These are restrictions on the specified inverse-stage architecture, without coefficient, stability, or conditioning assumptions.

A depth lower bound is not automatically a lower bound on every possible implementation of the product. Under an executor charging Theta(N) scalar work for each complete stage, it rules out sublogarithmic depth and yields an Omega(N log N) stage-by-stage charge. It does not forbid unrelated circuits, fusion with a different representation, or other structured stage classes. The source's conservative claim excluding a bounded number of such O(N)-work stages is valid.

The repaired scan witness only establishes that the separated-generator class contains stages outside every fixed-q/fixed-r inverse-defect family for sufficiently large N. Some other separated scans are diagonal or otherwise lie in that family. No Fourier representation by surviving stages is supplied.

## Exact algebra and exceptional cases

### Fourier/minor theorem

- q is a nonnegative integer; q>=N makes the displayed lower bound vacuous. For q=0 the proof gives full rank N.
- Selecting original frequency indices 0,...,m-1 avoids any wraparound ambiguity; a consecutive shifted range also works.
- Row/column permutations are undone only for choosing the minor. Nonzero diagonal factors multiply its determinant by nonzero scalars.
- The inverse DFT is a Fourier-character matrix with the reciprocal primitive root and nonzero 1/N scaling.
- Over a finite field, N distinct N-th roots are necessary for this argument. The source's complex theorem does not require transferring modular nonsingularity into an unsupported characteristic-zero conclusion.

### Telescoping

The identity is algebraic for any square A_j,B_j:

    A_t...A_1-B_t...B_1
      = sum_j A_t...A_(j+1)(A_j-B_j)B_(j-1)...B_1.

Neither B_j nor partial baseline products need be invertible. The output being a Fourier inverse follows from inverting the assumed exact factorization. Diagonal/permutation connectors preserve both row-sparsity and rank under left/right multiplication. There are no missed singular-baseline or zero-generator branches in this theorem.

### Explicit scan

For S with lower/diagonal/upper values 1/3/2, write S=(I-L)+2J, where L is the strictly lower all-ones matrix. The source Sherman–Morrison inverse formula, det S=2^(N+1)-1, and prefix-scan inverse are correct over C for every N>=1. The source states N>=2, which is sufficient.

For bandwidth b in 0,...,N-2, rows 2(b+1)i and columns 2(b+1)j+b+1 are in range and entirely off-band. Its determinant after the cancelling geometric scalings is exactly beta(beta-alpha)^(m-1), with m=floor((N+b)/(2b+2)) and beta-alpha=-2^(-b-2). No exception occurs over C. For larger b, that particular proof is not claimed.

Finite-field edge cases must remain separate: S_4 is singular modulo 31 because D=31; S_32 is invertible modulo 65,537 but its inverse diagonal entries vanish since 2^32=1. Therefore the source's statement that all inverse entries are nonzero is a characteristic-zero statement. The original code appropriately excludes D=0 for its inverse routine.

### Woodbury and Thomas charts

In green_woodbury.py, lines 19–25 assert nonzero pivots; T=[[0,1],[1,0]] is invertible but outside this chart. A pivoted tridiagonal solver repairs this execution restriction while retaining linear arithmetic in N; the official LAPACK [ZGTTRF documentation](https://www.netlib.org/lapack/explore-html/d6/d46/group__gttrf_ga97b78d760b0f786b6798be430a416fa0.html) specifies partial pivoting and an upper factor with at most two superdiagonals. This observation does not change the source code.

Even a pivoted solver cannot use Woodbury with singular T. For example T=diag(0,1), U=V=(1,0)^T gives T+UV^T=I although T^(-1) is undefined. Conversely T invertible does not ensure T+UV^T invertible: T=I, U=(1,0)^T, V=(-1,0)^T makes K=0 and the updated matrix singular. When T is invertible, the determinant lemma makes K nonsingular exactly when the updated matrix is nonsingular. The source's retry loop samples away from singular K; it is an illustration, not coverage of every admissible inverse decomposition.

The kernel at lines 78–80 costs: solve r right-hand sides O(Nr), form V^T Z O(Nr^2), invert K O(r^3), plus O(N) tridiagonal preparation. Lines 84–89 cost O(N)+O(Nr)+O(r^2)+O(Nr) per vector. The generalized code also retains standard API restrictions (positive N, shape-compatible arrays, fixed-width NumPy integers); those do not qualify the mathematical theorem.

## Parameter counts and inherited claims

The new rank proof uses no dimension argument, so it does not need generic parameter counts or nonzero-chart assumptions.

For context, for a fixed row-s support pattern, B has at most Ns free entries, while the variety rank(E)<=r has dimension 2Nr-r^2 for 0<=r<=N. Thus the family B+E has dimension at most min(N^2, Ns+2Nr-r^2), possibly smaller because the two parameterizations overlap. Lower-rank strata are included; one must not add 2Nr free UV parameters without their redundancy. Taking a finite union over support patterns preserves this dimension upper bound. Such generic bounds cannot exclude one special Fourier point.

The nested predecessor PROOF_CERTIFICATE.md was read as text. It explicitly assumes N>=3, uses the separated-generator chart, proves its dimension 5N-6, and removes (t-1)N internal diagonal gauge dimensions to obtain min(N^2,N+t(4N-6)). The proof extends across exceptional points inside the irreducible separated-generator parameter image by density. It explicitly does not cover every possible transition-generator quasiseparable boundary component. The current source's shorthand “all N” should retain that original N>=3 scope. Its full-dimensional Jacobian statements are only for N=8,16,32; they do not imply Fourier factorization or all-length saturation. No predecessor code or saved Jacobian computation was rerun here.

## Arithmetic, storage, and numerical limits

The scan and inverse scan require O(N) scalar arithmetic and O(N) scalar storage if coefficients and outputs are counted as unit-size scalars. Preparation of powers of two and D is O(N) scalar operations. However D has N+1 bits, and S^(-1)e_0 as N separate exact rational outputs has Theta(N^2) total binary length. The advertised arithmetic bound is not a bit-operation bound. Neither the negative theorem nor our repair assumes favorable numerical conditioning, and no stable floating-point implementation is certified.

The source finite-field kernels use NumPy int64. Their small tested lengths and primes fit safely within int64 intermediate product sums, but this does not establish arbitrary-size exact modular execution. This audit's independent kernels use unbounded Python integers and rational fractions instead.

## Independent evidence, distinct from historical evidence

No source-package Python/C++ file was imported, executed, or compiled. The supplied run_all.py was read as text; it would compile and execute predecessor code, so it was not used. Historical RUN_OUTPUT.txt, EXPERIMENT_RESULTS.json, and test declarations establish what the source reports, not new successful reruns.

The audit-owned standard-library checker passed:

- 444 Fourier rank/minor cases, including arbitrary endpoint permutations/scalings, inverse and forward transforms, non-power-of-two lengths, q=0 and vacuous-bound corners.
- 12 heterogeneous telescoping cases, including zero-sparsity and singular baselines, with explicit equality of the telescoping sum.
- 18 rational lengths N=1,...,18 for scan determinant and inverse; 153 rational all-bandwidth minors; 54 fresh rational inverse-vector scans.
- 48 modular banded minors through N=128, plus two finite-field exception controls.
- 305 arbitrary-sparse repair minors; 165 full-rank/monomial comparisons; exhaustive support-graph construction for 23,042 small support patterns.
- 180 Woodbury identities with ranks 1,2,3; an explicit singular-K test; three baseline/Thomas exception controls.
- Five exact radix-2 NTT controls, checking that both forward and inverse butterfly stages are row-2-sparse and attain the expected logarithmic depth.

These finite checks are reproducible with `python -I independent_checks.py`. The all-N mathematical conclusions rest on the written algebraic/combinatorial proofs, not numerical extrapolation.

## Provenance and disposition

Library source: [private-id]. Original archive: fft_sparse_defect_green_gate_2026-10-10.zip, 569,344 bytes, SHA-256 f0bcde62ec1a8fff9609a463c79025edc6ac150fd910f55ccc2cfd3cc56d885b. Parent-provided Library creation context is October 9 around 19:25 UTC; the internal October 10 label is preserved rather than silently normalized.

PROVENANCE.json records every source file hash, this audit's independently read predecessor proof hash, and the source-code execution prohibition. Full discovery/extraction provenance remains owned by the separate triage record. The audit does not modify originals, master research, Library items, or Pages.

Recommended disposition: preserve the original Fourier theorems; append ARBITRARY_SPARSE_REPAIR.md to support the previously overbroad survivor interpretation; correct Woodbury setup/application costs; state the Thomas/Woodbury executable chart and unit-cost scalar arithmetic scope. Continue to label the outcome “scoped architecture barrier and surviving scan class,” never an unrestricted FFT lower bound or faster FFT construction.
