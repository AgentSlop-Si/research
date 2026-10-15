# ALG-060 independent primary-source comparison review

## Verdict

ACCEPT the repaired named comparison at author report SHA256 d4c462dca53510a4d24c24f76a173c8540f3d29a33621ea2a44c1e6e4c704a3e. Parent status remains TO RESEARCH. Acceptance means independent mathematical review, not Lean or other proof-assistant verification.

The complete inherited Phase12 audit was read, with SHA256 de519608a7ea065ea1278805d3b987ae9aa4a2b6001aa5a4202c135bc3e8ec9a verified. The ordered inverse telescoping, sparse-column product and nullvector uncertainty derivation remain accepted within their original square invertible-stage grammar. Tao was already compared in that audit and is not counted twice.

## Independently checked source passages

- [Boito–Eidelman](https://arxiv.org/pdf/2308.02701): section 2 definitions and Theorem 2.1, plus the full relevant two-sided-band Theorem 4.4 construction/proof. One-sided lower bandwidth leaves an unrestricted upper side. Green/quasiseparable cut rank does not bound column support. The author's I+J and cyclic-resolvent examples correctly separate the invariants and identify a genuine overlap.
- [De Sa et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534155/): Theorems 1.1–1.2, Definition 6.4, resolvent reduction and generator-access qualification. The Sylvester uniqueness, disjoint spectra, field-operation count, parameter dependence and supplied/constructed off-diagonal factors are preserved. The explicit Fourier displacement TF-FZ=1 e_last^T has rank one, while the Fourier inverse is dense. Displacement rank is not perturbation rank.
- [Chandrasekaran–Epperly–Govindarajan v3](https://arxiv.org/html/1911.05858v3): Definition 1, Propositions 2.1–2.3 and their rank arguments; Definition 3, equations 2.27–2.31, and Propositions 2.9–2.11. The common graph, border edges and Hamiltonian ordering are material. Real-to-complex extension is explicitly an algebraic derivation. Sparse support can have large prescribed-graph cut rank. Auxiliary-state sums do not automatically instantiate the product grammar or provide compact construction.
- [Dvir–Liu, CCC2019](https://drops.dagstuhl.de/storage/00lipics/lipics-vol137-ccc2019/LIPIcs.CCC.2019.17/LIPIcs.CCC.2019.17.pdf): regular-rigidity definition, Theorem 1 and the complete all-length Theorem 48 proof. The fixed-epsilon parameter, field and row/column change budgets match this conference version. Its allowed parameters are compatible with the global uncertainty inequality. This review does not claim an independent reconstruction of every earlier number-theoretic lemma.

## Reviewer corrections now incorporated

The original candidate reversed the direction of its cut-kernel map. The repaired proof correctly maps a vector in the A cut kernel by A to the inverse cut kernel; A inverse supplies the reverse bijection. It does not assume principal blocks invertible.

The original candidate also understated the conditional lift from a sparse-plus-low-rank inverse decomposition. If F inverse equals B+D and B is invertible, G=B inverse and R=F-G=-F D B inverse give a valid one-layer abstract grammar, with rank R equal to rank D and column support of G inverse equal to that of B. No sparsity of B inverse is needed. The repaired report states this exactly. Dvir–Liu supplies no unconditional invertibility guarantee; extra membership in a particular cyclic/stride-Green family must be stated as an additional restriction, not silently inserted into the accepted theorem.

## Cost, replay and state boundary

Outer monomial endpoints preserve support. Dense endpoints do not: cancellation by F inverse would trivialize the target. Low rank does not by itself imply rank-times-N work; sequential layer materialization remains a separate cost premise. Root acquisition, validation, generators, I/O and any numerical/bit promises are not free.

After inspecting the fresh author control script, the reviewer replayed it in a separate local file. All 40 exact controls passed: 9 dense quasiseparable, 9 cyclic Green, 5 fixed-line permutations, 7 finite-field Fourier identities, 9 conditional sparse lifts, and 1 kernel-map example. Output matched the author's result bytes (SHA256 001802338b21f196827b8ed5b696d62be6313ed7f0032fa1610bef82dbd0d155). These controls corroborate algebra, not the complex uncertainty theorem, asymptotic novelty or production readiness. No inherited historical research executor was run.

The named four-family comparison is complete. The actual broader-interface source/contract prerequisite and source-bound production accounting for the shared-power repair remain visible. No new generic literature queue is introduced. The repaired report does not certify a full FFT implementation, free arbitrary endpoints or worldwide novelty.

The seven author cells and all added current-view mirrors retain complete prior descriptions. Scores, novelty class, parent status, links and notes stay protected. All author manifest identities were checked; raw third-party passage receipts are excluded from publication. Parent-only native writes require fresh exact preimage comparison. This reviewer made no external write.
