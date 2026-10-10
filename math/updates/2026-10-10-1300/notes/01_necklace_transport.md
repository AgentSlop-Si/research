# Necklace trace, Hessian transport and locality bounds

Date: 10 October 2026

## Conclusion

The package supplies a valid short-orbit trace evaluator, a valid sparse representation of its Hessian, and a valid support obstruction to bounded-local Fourier marking. These are useful auxiliary results. The proposed inexpensive transport that makes the Hessian equal the Fourier matrix remains unconstructed. No arbitrary-input Fourier complexity improvement follows from the package.

The principal proof claims are accepted in their stated arithmetic setting, with a word-size qualification for unrestricted horizon growth and an additional characteristic obstruction for the canonical trace carrier. Uploaded programs were read as text, not imported or executed. Fresh audit-owned controls are separate from the source's saved execution claims.

## Provenance and evidence scope

The submitted archive and mathematical theory are identified by filename and SHA-256 in SOURCE_MANIFEST.json. Its nine manifest-covered members passed integrity comparison. Submitted programs were inspected as text and remained inert. The independent mathematical controls distributed here do not require the submitted archive or its programs. Historical source execution claims are not independent validation.

## Accepted mathematical statements

### Weighted trace identity

Let N=2^n, n>=1, and give each directed edge e=(s,b), from s to 2s+b modulo N, an independent scalar weight w_e. With the column-source adjacency convention, the following polynomial identity holds over the integers and hence over every field:

    tr(B(w)^k) = sum_C r_C product_(edge occurrences in C) w_e.

Here C ranges over length-k binary necklaces and r_C is the least period, equivalently the number of distinct rotations. Each binary length-k word determines its unique closed walk by periodic extension to the preceding n symbols. Grouping the 2^k words by rotations gives the formula. The coefficient is r_C, not k; a constant necklace has coefficient one. Repeated edges remain repeated factors.

This accepts THEORY.md Section 2, including zero weights. A fresh negative control with only the zero self-loop nonzero gives trace one at k=2; replacing r_C by k incorrectly gives two.

### Fully charged short traces

For K=n+c, c>=0, write L(k) for the number of binary necklaces. The source bound

    L(k) <= 2^k/k + 2^(floor(k/2)+1)

is valid by separating primitive words and shorter periods. FKM generation, copying a length-k word, preparing its n-bit start state, following its k edges, and multiplying its factors cost O((n+k)L(k)) per horizon. The geometric sums yield

    sum_(k=1)^K (n+k)L(k) = O(2^K) = O(N 2^c).

In detail, the primitive contribution is O(n 2^K/K + 2^K). The other contribution is O((n+K)2^(K/2)), which is O(2^K) because n<=K and K=O(2^(K/2)). This includes reading the 2N supplied weights and writing K trace values. A circuit can be generated with O(2^K) scalar nodes and address operations; a direct streaming scalar evaluation needs O(N+K) workspace.

The O(log N)-bit address convention is justified for the intended K=O(log N) schedules, including fixed c and c=ceil(log2(log2(n+2))). If c is unrestricted and superlinear in n, an O(2^K)-node circuit can require O(K)-bit node addresses. The arithmetic bound still holds, but the same O(log N)-bit word contract should not be advertised for all such c without a different representation argument.

With characteristic zero or greater than K, the determinant prefix through degree K follows from Newton identities at an additional O(K^2) field-operation cost. This is a proof consequence. The supplied source does not implement a separate determinant-prefix verifier, and this audit did not claim to run one.

### Hessian application and the conditional Fourier conversion

For the orbit polynomial Psi, a prepared baseline gamma, and a supplied linear transport P, the chain rule gives

    Hessian_z Psi(gamma+Pz) at z=0 = P^T H P,
    H = Hessian_w Psi at gamma.

The scalar source is polynomial, so it is regular at zero even when some gamma entries vanish. Classical forward-over-reverse differentiation gives its Hessian-vector product at constant-factor scalar-circuit overhead. The source compiler's handling of multiply gates, repeated arguments, reverse adjoints, and directional reverse adjoints is consistent with this identity on static review. No new derivative-complexity principle is needed.

Thus each fresh vector is processed in O(N 2^c + W(P) + preparation) work, where both P and its transpose must be available within the charged cost. An append-only compiler uses storage of the same order, not automatically O(N) for growing c. The four-Green construction has this operator-application bound regardless of whether its matrix is Fourier.

The Fourier certificate is exact:

    T e_0 = all ones,   T S = D T,
    S e_j = e_(j+1 modulo N),   D_ii = omega^i.

Both identities imply T e_j=D^j ones, hence T_ij=omega^(ij). They are also necessary. A random probe can disprove them; passing finitely many random probes cannot establish an all-N construction.

### Sparse Gram representation

When every gamma_e is nonzero, let m_C,e be the multiplicity of edge e in C and

    lambda_C = alpha_C product_e gamma_e^(m_C,e),
    u_C,e = m_C,e / gamma_e.

Twice differentiating each monomial proves

    H = sum_C lambda_C u_C u_C^T + Delta,
    Delta_ee = -sum_C lambda_C m_C,e / gamma_e^2.

Keeping edge occurrences rather than dense u_C vectors makes the total incidence length kL(k)=O(N 2^c). Dot products and scatter additions each take one pass through those occurrences. Setup and every application have the claimed bound. Batch inversion uses O(N) multiplications and one inversion, after rejecting zero baselines. The identity rank(H-Delta)<=L(k) is correct; it does not bound rank(H) by L(k).

At zero baseline entries this representation is undefined. The polynomial differentiation route remains valid. No zero-baseline division is licensed by the theorem.

### Locality obstruction

Fix an edge e=(s,b) and rotate a closed walk containing it until e is the first edge. For k>=n+1, the initial state fixes the final n appended bits and e fixes the first bit, leaving k-n-1 free bits. There are 2^(k-n-1) possible anchored words. For k<=n, periodic consistency leaves at most one anchored word. Each contains at most k edge labels. Consequently every Hessian row has at most

    Delta_k = k 2^max(0,k-n-1)

potentially nonzero entries, independently of coefficients and baseline. Repeated-edge diagonal derivatives fit the same bound; cancellation can only reduce support.

If each column of P has at most s nonzeros and each row at most d, a row of P^T H P can reach at most s Delta_k d columns. Since every Fourier entry is nonzero, a necessary condition is

    N <= s d k 2^max(0,k-n-1).

For k=n+2 and s=d=1, N=16 is already excluded: 16>12. For 2^c=O(log n), any fixed powers of log n in s and d are eventually excluded. This does not constrain arbitrary dense inexpensive transports, total sparsity with unbounded row or column degrees, or unrestricted arithmetic circuits.

## Additional field obstruction

For the canonical choice Psi=tr(B(w)^k), over characteristic p dividing k,

    d tr(B^k) = k tr(B^(k-1) dB) = 0.

Every formal first derivative is identically zero, so H is identically zero at every baseline. Therefore P^T H P cannot equal an invertible Fourier matrix, regardless of the transport's complexity.

An exact fresh example uses F_3, N=2, n=1, k=3, omega=2, and canonical baseline (1,1,1,2). Its 4-by-4 edge Hessian is zero while F_2 has rank two. This is an extra guard for finite-field searches. It does not refute the complex conjecture, nor the broader conjecture permitting different orbit coefficients or a different horizon. The source only reports finite carrier ranks and does not claim an all-field rank theorem.

## Costs and model boundaries

The validated model is exact scalar field arithmetic with separately charged addressing and supplied roots. It is not a bit-operation or numerical-stability result.

- Inputs to trace evaluation are 2N arbitrary edge weights; outputs are K traces, not N Fourier outputs.
- A Hessian application consumes a fresh N-vector and writes all N entries of P^T H P times that vector. Whether these outputs are Fourier values is a separate identity obligation.
- The canonical gamma is generated by a sequential N-entry root-power stream. Other coefficients, gains, masks, and permutations need uniform generators or must have their supplied-table preparation charged.
- Each cyclic Green map solves y_j=x_j+a_j y_pred(j), with product_j a_j !=1. A forward cycle pass prepares the wrap-around constant and a second pass gives all coordinates. Reverse accumulation gives a transposed linear circuit of the same order. The denominator product, nonzero check, inversion, cycle validation and addressing cost O(N).
- The supplied Green emitter uses four such maps and interleaved pairwise sums. No Fourier endpoint map is secretly provided by that grammar.
- A generic dense 2N-by-N congruence P costs quadratic storage/application without an additional representation theorem. Full rank of H is insufficient.
- Coefficient fitting, polynomial-system solving, dense Hessian assembly, Gaussian ranks, and exhaustive rotation grouping are verification/search work, not unpriced online subroutines.
- The supplied profile field named generation_word_upper_proxy is a proxy, not a complete exact instruction ledger. The asymptotic proof includes enumeration; the proxy alone does not certify a measured leading constant.
- Fixed finite prime fields cannot be used as an all-length root-supply claim. Field/root selection and finite-precision behavior remain outside the established result.

## Open and conditional statements

The missing object is a uniformly generated low-work P_N and, if necessary, uniformly generated alpha_C and gamma_N, satisfying P_N^T H_N P_N=F_N for a growing dyadic family. The narrower canonical target fixes k=n+2 and alpha_C=r_C, gamma_(s,0)=1, gamma_(s,1)=omega^s.

Conditional on such a construction, fixed c would give O(N) Fourier work, and 2^c=Theta(log n) would give O(N log log N). The package does not provide that construction. Its tested random four-Green instances fail Fourier equality. Its exact F4 positive control belongs to a larger affine-marking grammar and does not certify the four-Green conjecture. No uniform solve, general-length extension, practical speedup, stability theorem, or external priority claim is established.

The next justified work is a formal all-N construction or a scoped obstruction for the specified Green grammar, with preparation and transpose costs included. Merely obtaining dense full-rank carriers or finite fitted parameters does not close the gate.

## Fresh independent controls

Audit-owned `independent_controls.py` uses exhaustive rotations, positional polynomial derivatives, path-jet propagation, explicit Green sums, and finite-field elimination. It imports no uploaded module. These are small exact correctness controls and deliberately slow oracles.

Eight mathematical groups passed, in addition to a separate nine-member source integrity check:
1. 180 weighted-trace comparisons for n=1..5, k=1..n+3, over F_17 and F_97, including partial and all-zero weights.
2. 72 mixed-Hessian comparisons, including zero baselines; 24 also checked against the Gram expression.
3. 60 structural-locality plans for n=1..8 and k=1..n+3, including the N=16 sparse-marking exclusion.
4. 24 Green recurrence checks and a singular-cycle rejection control.
5. Twelve canonical carrier ranks for N=2,4,8,16,32,64 over F_257 and F_65537. Rank is two at N=2 and 2N at the other tested lengths. These extend finite controls only.
6. The characteristic-three zero-Hessian counterexample.
7. The least-period multiplicity negative control.
8. Two algebraic F4 controls, 32 matrix entries total, explicitly outside the four-Green claim.

Mathematical results are in certificates/necklace/INDEPENDENT_RESULTS.json. The portable verifier is under programs/necklace; see REPRODUCE.md. Source integrity belongs to provenance and is excluded from its eight mathematical groups. No uploaded compiler replay, general FFT benchmark, or all-N proof is inferred from these checks.

## Classical lineage and unresolved construction

FKM necklace generation is classical. Ruskey, Savage and Wang prove constant-average-time generation; this supports the enumeration bound after explicit word copying is charged. [Author publication page](https://webhome.cs.uvic.ca/~ruskey/Publications/GenNecklaces/GenNecklaces.html)

Harrison and Hudgins already use closed cycles modulo rotation, products of orbit amplitudes, and the same binary de Bruijn adjacency in a quantum-graph setting. Their Sections 2–4 were inspected directly in this audit. Their result concerns characteristic-polynomial spectral statistics; it does not by itself establish this package's arbitrary-weight short-horizon cost theorem or Fourier transport. The graph/orbit mechanism should not be presented as new. [Primary paper](https://arxiv.org/html/2101.00006v3)

Pearlmutter's exact Hessian-vector construction is established prior work. The present compiler is an application of that derivative mechanism. [Author manuscript](https://www.bcl.hamilton.ie/~barak/papers/nc-hessian.pdf)

Boito and Eidelman's Green-matrix work establishes relevant quasiseparable and linear-complexity inversion background. It should not be cited as proving this specific four-cycle congruence or its conjectured Fourier specialization. [Primary preprint](https://arxiv.org/abs/2308.02701)

The official OpenAI #130 scope document separately describes subsequential exact Fourier savings and a uniform exact-complex power-saving result, with supplied roots and unrestricted coefficients. This audit checked the live scope text, not the Lean proof or accompanying full proofs. It neither credits that external theorem to this package nor asserts that every sub-N-log-N exact Fourier result is unknown. [Official comparator documentation](https://github.com/openai/math/blob/main/lean/docs/130.md)

The direct existing project link is Q31, “Construct regular sparse-jet source.” Its earlier theory was checked at SHA-256 `94da2df24bd6f6bc073b35ab3c8cc0c0d57d94e1b1ee0d4a860a1fc4458f5af1`; the inherited `circuit.py` is byte-identical at SHA-256 `ecbd330cdf2baf8388c96f17674c7b961182dea022e5c6d3eda5d4e8fad4509e`. The new package gives an explicit inexpensive auxiliary polynomial source, but not the Fourier-compatible source required to complete Q31. Q31 remains constructively open. This supplies supporting evidence for the same unresolved construction, rather than a second solved result.

The package also describes links to prior marked-cycle and shared-scan work. Those broader equivalences were not independently re-established in this pass and are not used to close another existing task. Literature inspection is focused rather than exhaustive; historical priority of the cost specialization and locality bound remains unresolved.
