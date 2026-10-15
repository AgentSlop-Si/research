# ALG-060: exact grammar and endpoint comparison

15 October 2026. Author comparison candidate; external services read-only. Independent review is still required before accepting or applying this candidate.

## Result and decision

The named primary-source comparison in Catalogue85 AE/AF is complete at a bounded, explicitly identified source set. Quasiseparable/Green structure, displacement rank, graph-induced cut rank, and regular rigidity measure different quantities. There are precise overlaps and explicit non-implications below. None of the inspected results is an exact replacement for the entire arbitrary-rerouting, inverse-column-support product grammar. That is a qualified nonmatch within these sources, not a worldwide priority finding.

The existing restricted theorem stays accepted. Tao's prime uncertainty comparison was already completed in the Phase12 audit and is not claimed as new work. The orbit-average identity, commutator rank, and odd-chirp inverse are unchanged. The historical modulation cost repair is not converted into a production certificate.

The conservative cell proposal marks the comparison COMPLETE, retains overview status TO RESEARCH, score 42 and the existing novelty classification, and preserves every old text as a verbatim suffix. The parent explicitly confirmed that TO RESEARCH must remain because the current record retains broader-interface requirements. No new open mathematical obligation is invented by treating an excluded model as a failed theorem.

## 1. Frozen source theorem and legal grammar

The complete inherited Phase12 audit was reread. Its exact SHA256 is de519608a7ea065ea1278805d3b987ae9aa4a2b6001aa5a4202c135bc3e8ec9a. For the unnormalized complex Fourier matrix F, the accepted grammar is

    F = H_L ... H_1,  H_i = G_i + R_i,
    H_i and G_i square invertible, rank(R_i) <= r_i,
    maximum column support(G_i^-1) <= s_i.

Put r=sum r_i and s=product s_i. Ordered inverse telescoping produces

    F^-1 = B + D,  B = G_1^-1 ... G_L^-1,
    rank(D) <= r,  colsp(B) <= s.

The accepted consequences are s(r+1)^2 >= N and, for complex prime N=p, (s+1)(r+1) >= p+1. The r>=N case is automatic. No commutation, common cycle ordering, common graph, bounded coefficients, or bounded condition number is required. Internal monomial routings/gauges are allowed insofar as the stated inverse-column-support bounds and invertibility actually hold. Representation acquisition and nonzero-gauge access are not free.

A useful distinction for the comparison: invertibility is needed to derive B from the product. Once F^-1=B+D is available, the nullvector/uncertainty argument only uses colsp(B) and rank(D); B itself need not be invertible. Thus arbitrary sparse-plus-low-rank decompositions can be compared with the global inequality, even when they cannot be lifted back to the stage grammar.

### Endpoint freedoms, derived here

The physical target is the full N-input, N-output linear map, not selected bins, compressed output, or a rectangular transfer through hidden states. Independent invertible monomial maps U,V at the outer endpoints preserve the same uncertainty inequalities for A=UFV: A^-1=V^-1 F^-1 U^-1, and both monomial operations preserve support cardinalities. This is a direct support-preservation observation, not a new priority claim. Scalar Fourier normalization is included in this class.

Arbitrary dense endpoint changes are not free. For example, U=F^-1, V=I makes UFV=I, admitting r=0,s=1 for N>1. Extending a Fourier obstruction to such endpoints without charging their support would be false. Any more general endpoint must itself be included in the allowed factor and support accounting, or analyzed separately. Internal independent reorderings preserve column support but need not preserve a common quasiseparable ordering or graph cut.

## 2. Primary theorem locators

The following short descriptions specify the source claims. The mathematical mappings in Section3 are independently derived comparisons.

### Q: quasiseparable/Green matrices

Boito–Eidelman, *Computation of quasiseparable representations of Green matrices*, arXiv:2308.02701, Section2, Theorem2.1, printed p.3: for N>q>0, invertible A has A_ij=0 when i-j>q exactly when B=A^-1 satisfies rank B(k:N,1:k+q-1)<=q for 1<=k<=N-q. Equation2.3 gives the lower-generator form. This is the classical Asplund theorem as explicitly restated by the authors, not their claim to have originated it. Their two-sided-band QR construction, Theorem4.4 and Section4.2, printed pp.12–13, is linear in N for fixed bandwidth; a one-sided bandwidth condition alone leaves a dense unstructured side. The LU version adds strong regularity. These are structural and representation-construction statements, not Fourier lower bounds. [Primary full text](https://arxiv.org/pdf/2308.02701)

### D: displacement rank

De Sa–Gu–Puttagunta–Ré–Rudra, *A two-pronged progress in structured dense matrixvector multiplication*, Theorem1.2, Definition6.4, Lemma6.6 and footnote16: if L,R are t-quasiseparable and A is uniquely specified by LA-AR=E of rank d, multiplication by A and A^T uses O(d t^omega M(N) log^2 N + d t^2 M(N) log^3 N) field operations. M(N) is polynomial-multiplication cost. The representation assumes access to low-rank off-diagonal factors, or construction in their factor-size cost. Uniqueness for Sylvester displacement requires disjoint spectra. Theorem1.1 gives a sharper triangular-band case with explicit preprocessing. Footnote1 restricts the main analysis to exact field operations and leaves numerical stability aside. [Primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534155/)

### G: graph-induced rank structure

Chandrasekaran–Epperly–Govindarajan, arXiv:1911.05858v3, Section2.1, Definition1 and Propositions2.1–2.3, printed pp.5–8: GIRS-c means rank A_(H,H-complement)<=c rho(H) for every induced subgraph, with rho counting border edges. Opposite cut ranks are preserved by inversion; sums and products on the same graph have parameter at most c+d. The paper formulates real block matrices. Section2.4, Definition3 assumes a Hamiltonian path inducing a common vertex order. Equations2.27–2.31 and Proposition2.11 use auxiliary states and two directed-flow sums; maximum state dimension h implies GIRS-4h. Fast application requires a compact supplied representation; compact construction/inversion is not automatic. Proposition2.9 instead relates DV application/solve cost to sparse elimination on the graph. [Versioned primary full text](https://arxiv.org/pdf/1911.05858v3)

### R: regular rigidity, full primary text rather than abstract

Dvir–Liu, CCC2019, definition preceding Theorem1 and Theorem1, printed p.17:3; proof restated as Theorem48, pp.17:19–17:20. For fixed 0<epsilon<0.1 and sufficiently large N, their regular-rigidity bound is

    r_F( N / 2^(epsilon^4 (log N)^0.0004) ) <= N^(9 epsilon).

Regular rigidity counts the maximum number of changed entries in each row AND each column needed to reach the target rank. This version is over C. The full theorem and all-length completion proof were inspected; we do not claim to have re-proved every preceding number-theoretic lemma. This precisely identifies the 2019 conference version, avoiding theorem-number/exponent mixing with the longer revised arXiv text. [Official full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol137-ccc2019/LIPIcs.CCC.2019.17/LIPIcs.CCC.2019.17.pdf)

## 3. Exact mappings and non-implications

### 3.1 Quasiseparable rank cannot replace inverse column support

For N>=2 let J be the all-ones matrix and A=I+J over C. Then

    A^-1 = I - J/(N+1).

Every strict upper/lower cut block of A and A^-1 has rank one, yet every column of both matrices has N nonzero entries. Consequently a quasiseparable order-one hypothesis supplies no bound s=1 or s=2 on inverse column support. This remains an explicit counterexample even though application of A and A^-1 is cheap via a shared sum.

There is also a genuine local overlap. For the cyclic shift S and alpha nonzero with alpha^N!=1,

    G=(I-alpha S)^-1,
    G_ij=alpha^((i-j) mod N)/(1-alpha^N).

Both strict off-diagonal cut families have rank one in the natural cycle order, while G^-1 has column support two. The lower-band order-one direction of the Asplund theorem fits I-alpha S, whose wrap entry is in the unrestricted upper side. It is incorrect to call that matrix a two-sided bandwidth-one matrix in this ordering: the top-right wrap is far from the diagonal. A general stride becomes disjoint cycles after a permutation; independent layer permutations need not give one shared ordering. Thus classical Green structure explains a baseline component, whereas the product/low-rank/uncertainty combination still requires the explicit ALG060 hypotheses.

### 3.2 Fourier itself has displacement rank one

Use zero-based indices, F_ij=omega^(ij), T=diag(omega^i), and the nilpotent subdiagonal shift Z, so Z e_j=e_(j+1) for j<N-1 and Z e_(N-1)=0. Then

    TF - FZ = 1 e_(N-1)^T.

For j<N-1 the two entries cancel; for the last column omega^(iN)=1. T is diagonal, Z is one-quasiseparable, and their spectra are disjoint because omega^i is nonzero while Z has only eigenvalue zero. The right-hand factors are explicitly given. This supplies an exact positive mapping of Fourier to the displacement framework, not just a nonmatch assertion. Nonetheless F^-1 is entrywise nonzero, hence colsp(F^-1)=N.

The rank of TF-FZ is not the rank of H-G, and a displacement operator pair is not an input/output basis change. Arbitrarily setting L=R=I makes every displacement zero but destroys unique specification, illustrating why that source guard matters. The cited fast multiplication construction is a field-operation upper bound with parameter/representation costs; it supplies neither an O(N) Fourier evaluator nor a lower bound on every evaluator. For the explicit T,Z example, generator/root powers are obtainable by a charged shared recurrence once a validated root is supplied; this does not certify the historical modulation code.

### 3.3 GIRS cut rank and support are different invariants

The algebraic part of Propositions2.1–2.3 extends from R to C by the same block-rank identities; this sentence is our algebraic extension, not a verbatim field claim from the paper. For a partition into H and its complement, one can prove cut-rank preservation without assuming principal blocks invertible: write K=H-complement and embed y in ker A_(H,K) as x=(0,y). Then Ax=(0,A_(K,K)y) lies in the embedded kernel of (A^-1)_(H,K). This is a bijection whose reverse is multiplication by A^-1: if z=(0,w) with (A^-1)_(H,K)w=0, then A^-1 z=(0,v) and A_(H,K)v=0. Thus the two cut kernels have equal dimensions, and rank-nullity gives equal cut ranks. The product rule follows from the two summands in the cross block of AB.

If all baseline stages are GIRS on one common graph, their product admits a cut bound with summed GIRS parameters. ALG060 instead permits independently rerouted cycles and multiplies column supports. The same-graph hypothesis cannot be discarded. For N=2m, the permutation swapping the two halves has column support one but its upper-right m by m block has rank m; the corresponding middle cut of the fixed line graph has one edge. Small support therefore does not imply a uniformly small GIRS parameter on a prescribed graph. Taking a union graph is possible, but it changes rho(H) and may eliminate the useful small-cut bound.

Diagonal left/right gauges preserve individual cut ranks; a simultaneous row/column permutation preserves them after relabeling the graph. Independent row and column permutations need not preserve the same graph-partitioned matrix model. The two directed state-flow sums in G-SS are a larger representation grammar than the stipulated square product. Their existence is not an admissible ALG060 factorization without a separate translation and full state/support/cost accounting.

### 3.4 Dvir–Liu is compatible even at the global sparse-plus-rank level

Write their decomposition as F=E+L with colsp(E),rowsp(E)<=s and rank(L)<=r. Since F^-1=(1/N)F with a sign-reversal row permutation, it induces a decomposition of F^-1 with the same bounds. Therefore the ALG060 global uncertainty inequality applies directly, without requiring E to be invertible. It is wrong to dismiss the comparison solely because their sparse summand may be singular.

For the displayed admissible upper-bound parameters, r=N^(1-o(1)) and s=N^(9 epsilon) for fixed epsilon. Hence s(r+1)^2 is far above N; at prime lengths (s+1)(r+1) is also above N+1 for sufficiently large N. The statements coexist. These are comparisons using permitted parameter bounds, not assertions that every realizing decomposition attains them.

There is an important conditional lift back to the abstract stage grammar. If the translated sparse summand B in F^-1=B+D is invertible, set

    H=F, G=B^-1, R=F-G=-F D B^-1.

Then H and G are invertible, rank(R)=rank(D)<=r, and colsp(G^-1)=colsp(B)<=s. This is a valid one-layer instance of the abstract inverse-column-support grammar. No small-column-support hypothesis on B^-1 is required. Dvir–Liu does not guarantee that its sparse summand is invertible, so the lift is conditional; singularity is the genuine unconditional-lift blocker. Even where the lift exists, its large parameters remain compatible with the accepted inequalities.

If one separately restricts baseline factors to a particular cyclic/stride-Green family, membership of B^-1 in that extra family would need proof. That extra family restriction is not part of the general accepted theorem in Section1 and must not be silently added to it. The non-rigidity theorem blocks an overstrong general rigidity argument, but does not invalidate the restricted gate and is not a linear-time Fourier algorithm.

## 4. Cost and production boundary

The support inequalities constrain a representation. Turning an L-layer obstruction into work requires the additional sequential implementation that materializes and charges Theta(N) at each layer. State-sharing, branching, rectangular auxiliaries, compressed outputs, and high-support inverses are not excluded. Low rank alone does not force rN work, and dense or full-commutator-rank operators need not be hard.

Structured-matrix upper bounds assume their specified generators, bandwidths, graph/state representation, and field primitives. None supplies free cold discovery/validation, free root preparation, bit complexity, floating stability, or production certification for this project. The accepted Green-orbit fusion still evaluates a stride-Green operator rather than Fourier. The original repeated independent powers still require the accepted shared-power correction; this report does not bless that source as a fully accounted production executor.

### Exact remaining gates, with no new comparison queue

1. A claimed shared evaluator, branch-sum or rectangular/retained-state extension needs an actual selected candidate and its exact inputs, outputs, endpoint maps, state dimensions, preprocessing and online cost model. No such candidate is supplied or selected by this comparison. Its correctness and charged complexity cannot be inferred from the square-product obstruction. This is a source/interface prerequisite, not a request to settle unrestricted Fourier complexity.
2. Production use of the historical modulation repair needs the actual repaired source and a source-bound accounting/replay for the chosen domain: supplied versus acquired root, order validation, running powers, denominator checks, inversion model, allocations/indexing, input/output and storage. Numerical or bit-cost promises need their own specified contract. The independent checker is not that production certificate.
3. The accepted restricted theorem and Tao attribution are complete. The present four-family comparison is complete. Neither is an active successor; no generic further-literature task is created.

## 5. Evidence, replay and stopping condition

Fresh independently authored controls in check_comparisons.py passed 9 exact rational dense-quasiseparable examples, 9 cyclic-Green examples, 5 fixed-line permutation counterexamples, 7 finite-field Fourier displacement/endpoint identities, 9 exact sparse-summand conditional lifts, and 1 explicit two-way cut-kernel map. They support the elementary algebraic mappings. The finite-field controls are not a transfer of complex prime uncertainty, and no historical research program was run. CONTROL_RESULTS.json records all parameters.

The primary documents were accessed as full-text web documents and their listed theorem/proof passages read. Original PDF bytes were not retained: a shell retrieval attempt was cancelled by automatic approval review, and no shell download was retried. Local rendered web-passage receipts are evidence of what was read, not original-paper byte hashes. SOURCE_READ_RECEIPT.json distinguishes these identities. Raw third-party passages are verification-only and excluded from the publication file list. The publication contains our prose, formulas, precise locators, URLs, hashes and fresh controls.

This completes the selected named comparison. It is not an exhaustive prior-art search. No worldwide-first claim, novelty-classification change, priority-score change, implementation acceptance, or generic FFT lower bound is proposed. Any broader solver/interface task needs a newly explicit scope and evidence; this report does not reopen the already accepted elementary theorem or count Tao twice.
