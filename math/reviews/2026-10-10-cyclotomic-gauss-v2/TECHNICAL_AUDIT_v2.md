# Schur/path v32 and the Gauss–Superconcentrator proposal

Date: 10 October 2026. Bounded source audit; no uploaded program was run or imported.

## Verdict

Accept v32's cyclotomic count, phase-coverage, bounded-alphabet, and unique-path edge statements within their explicit models, with terminal and arithmetic qualifications below. They are additional restricted obstructions beyond v31's support gate. They neither construct a faster exact Fourier transform nor exclude arbitrary-complex-weight depth-three networks.

The Gauss–Superconcentrator source is a conjectural synthesis proposal. Its quadratic identity and conditional evaluation argument are correct, but it supplies no uniform sparse graph or weight generator. Its informal fiber definition additionally needs an exact amplitude/multiplicity condition: prescribing each path's phase alone does not imply the claimed transfer. No new exact upper bound is accepted.

The existing accepted approximate finite-word theorem is outside these exact-circuit claims and is unchanged. Historical novelty remains unresolved. This audit makes no Sheet, Library, or repository changes.

## 1. Actual sources and integrity

- v32 source conversation (private source link omitted from this public export), accompanying `fft_cyclotomic_path_gate_v32.zip`, and its complete `RESEARCH.md` were read. The 515,809-byte archive has 16 members, passes ZIP CRC, and all 14 entries in its manifest match. Archive SHA-256: `1f4cac73bfd53c82c395299dece3ab598fb4a27a728dd30c0e969cb884d73ef3`.
- The separately supplied `RESEARCH(20261010-140321).md` is byte-identical to the archive's 14,918-byte research note. SHA-256: `691fca4e865decacb38f4739089bf8ea096fc2bf110e923587eaf84333f5627d`.
- The embedded `PRIOR_v31_COMPLETE.zip` is byte-identical to the previously audited v31 archive. SHA-256: `fdc0772ed669d6c486298bead2a80039ba85d6f96b0532af1537af687d58601f`. Thus the prior accepted support analysis remains the actual predecessor, not a similarly named substitute.
- The complete Gauss–Superconcentrator proposal (private source link omitted from this public export), updated 13:41:48 UTC, was read with no omitted content. SHA-256 of the exact UTF-8 assistant-message text: `226ec21957384d1db7074d4050697619b372dbf289cc92345cd2e07e4b04ad55`. This is a text-content hash, not a packaged theorem or program hash.

Source-reported 14/14 tests remain a source report. Fresh independent controls have their own counts in section 6.

## 2. What v32 adds to v31

Let p be prime, ζ a primitive complex pth root, and F[i,j]=ζ^(ij). Use a finite scalar linear DAG with p distinct inputs and p distinct outputs, disjoint terminal sets, and weights that are individual pth roots with positive unit multiplicity. Parallel edges count separately. A terminal path contributes one root. Output normalization, signs, divisions, or arbitrary scalar factors cannot be supplied free.

For a terminal pair, let c_r be the nonnegative integer count of paths with phase ζ^r. Exact equality to ζ^k gives a polynomial C(z)−z^k, degree at most p−1, vanishing at ζ. Since the minimal polynomial is Φ_p=1+z+…+z^(p−1), this difference is tΦ_p. Coefficient comparison gives

    c_r = t + 1[r=k],       t is a nonnegative integer.
    Total path count = 1 + pt.

The proof is sound, including p=2. Target-phase coverage is mandatory; a nonunique representation has at least p+1 paths and all p residues. This uses rational linear relations among prime roots; it is not a statement about arbitrary complex coefficients. The cyclotomic mechanism belongs to classical vanishing-sum theory; see [Lam–Leung](https://arxiv.org/abs/math/9511209). The project-specific combination and its priority have not been novelty-cleared.

If all edge exponents belong to a single global s-element alphabet and every path has at most d edges, possible phase sums number at most binom(d+s,s). For paths of exactly d edges the bound is binom(d+s−1,s−1). Row i=1 of F requires all p target residues, so either quantity being smaller than p rules out this circuit class at every edge count. These are necessary bounds, never sufficient existence tests. At p=101 and d=3, the necessary thresholds are s≥7 for variable depth and s≥8 for exactly three edges.

The alphabet is global across the graph. A small formula or small number of parameters generating many distinct edge phases is not a small global phase alphabet. Every endpoint phase must be counted among the actual edges, or the target and model must be restated after the endpoint gauges. The source's depth is edge depth, not bounded-fanin parallel arithmetic depth.

Positive rational edge amplitudes retain mandatory target-phase coverage: path masses become nonnegative rationals and the same argument gives rational t≥0. They do not retain the integer path-count gap. Two half-amplitude paths can produce a target root.

An additional boundary control shows that positive real amplitudes are too broad even for coverage. Choose ζ=exp(2πi/5), or its complex conjugate, and put q=ζ+ζ⁴=2cos(2π/5)>0 and λ=q+1>0. The other primitive embeddings do not have this positivity property. Then q²+q=1, so

    λζ + λζ⁴ = 1.

Neither path has target phase 1. λ is irrational. The positive-rational restriction therefore matters, independently of the signed/complex restrictions.

There is also a full Fourier counterexample to extending the alphabet gate to all positive real amplitudes. The identities λ(1+ζ²)=ζ and λ(1+ζ³)=ζ⁴ let every entry of F_5 be implemented with depth-one parallel edges using only the global phase palette {1,ζ²,ζ³} and amplitudes 1 or λ. The nine phase-0 entries and eight phase-2/3 entries each use one edge; the eight phase-1/4 entries each use two, totaling 33 edges. Thus s=3,d=1 gives binom(d+s,s)=4<5, yet this positive-real-amplitude circuit computes all of F_5. It is a scope counterexample, not an asymptotic speedup or priority claim.

## 3. The quadratic edge bound, with terminals handled exactly

For n≥2, suppose every entry and every 2×2 minor of M is nonzero and its weighted DAG has exactly one path for each input-output pair. All relevant edge weights are nonzero. Every relevant vertex v has at most one input ancestor or at most one output descendant: otherwise uniqueness forces a 2×2 transfer submatrix through v to be an outer product, contradicting its nonzero determinant.

The source's designated-terminal model can be normalized without adding edges. First prune edges and vertices on no terminal path. If an input s_j has a remaining incoming edge, some input s_k reaches s_j. k=j would give a cycle. For k≠j, all the unique paths from s_k to the outputs must continue through s_j; column k of M is then a fixed nonzero multiple of column j. This contradicts the 2×2-minor hypothesis. The dual argument makes the outputs sinks. Thus inputs and outputs already have the required source/sink property in the relevant core.

For each pair, follow its unique path from an input reaching all n outputs to the designated sink. Mark the first edge u→v where the number of reachable outputs becomes one. Vertex u has at least two output descendants and therefore exactly one input ancestor. Vertex v has exactly one output descendant. This edge is exclusive to that terminal pair. The n² pairs mark n² distinct existing edges, yielding E≥n². No free terminal edges were introduced, so this is also a lower bound for the original graph.

Only nonzero entries and 2×2 minors are needed; total nonsingularity is stronger than necessary. For prime complex Fourier, the relevant determinant vanishes exactly when (i−k)(j−l)=0 modulo p, so it is nonzero for distinct indices. Consequently, if every pair in the unit-root model has at most p paths, it has exactly one and E≥p². Direct Fourier edges attain p².

The n≥2 and distinct/disjoint-terminal conditions should appear in a final theorem. The implementation validates terminal distinctness/disjointness but does not generally validate terminal ranges, source indegrees or sink outdegrees; its supplied constructions are normalized. These software-validation gaps do not invalidate the mathematical argument or the displayed examples.

## 4. Why large path counts cannot be charged as work

The zero gadget is exactly p input→hub edges, p parallel hub→hub edges labeled by all p phases, and p hub→output edges: 3p total. Every one of the p² input-output pairs has p paths, but its transfer is zero because the roots sum to zero. Adding the gadget to the p² direct Fourier edges gives p²+3p edges and p+1 paths per pair.

This is not a sparse Fourier algorithm. It is an exact counterexample to charging each canceling path as a separate arithmetic operation. Runtime for the literal evaluator is charged to edges and required input/output work, not the sum of path multiplicities.

The composite and signed boundaries also stand. For a primitive sixth root, ζ+ζ⁵=1 uses two positive-root paths. Signed weights at odd p permit cancellations outside the pure pth-root grammar. None of these results is a general circuit lower bound.

## 5. Audit of the Gauss proposal

For odd N, 2 is invertible modulo N. With primitive ω and

    G_N = Σ_t ω^(−t²/2),

completion of the square proves

    Σ_t ω^(−t²/2+(i+j)t) = G_N ω^((i+j)²/2).

G_N is nonzero: over C, expand its squared modulus and set t=u+h. The sum over u is zero for h≠0 and N for h=0, since 2·(−1/2)=−1 is invertible modulo odd N. Hence |G_N|²=N. Dividing by G_N and applying the displayed endpoint chirps gives ω^(ij). This is valid for odd composite N as well as primes. It is an algebraic identity, not a sparse realization.

The direct depth-three realization uses all N² edges X_j→U_t, N diagonal edges U_t→V_t and all N² edges V_t→Y_i, with weights ω^(jt), ω^(−t²/2), and ω^(it). Its 2N²+N edges demonstrate the identity but do not establish the claimed near-linear support. The source provides no replacement graph, adjacency rule, explicit edge assignments, supported-length family, or uniform generator.

There is also a precise issue in the proposed QFS definition. Edge weights are written γ_eω^a_e, but the ensuing transfer formula constrains only the summed exponents. Products of γ_e and repeated/missing paths affect each latent t term. Even one path per t with the right phases is insufficient if its amplitudes vary with t. For example, doubling only the t=0 path leaves every phase unchanged but changes the (0,0) sum from G_N to G_N+1.

A sufficient repaired condition is to partition the full path multiset into fibers P_ijt and prove, for every i,j,t,

    Σ_(P in P_ijt) product_(e in P) w_e
      = λ_ij ω^(−t²/2+(i+j)t+ρ_i+σ_j),

with λ_ij independent of t. To obtain Fourier by diagonal endpoint gauges, its nonzero pair dependence must also factor as λ_ij=a_i b_j, or otherwise have an explicit appropriately charged correction. A single common λ is sufficient. Another weighted law is possible only with its own exact summation identity. Merely asserting complete phases, full rank, enough paths or two successful finite-field tests does not prove this condition.

The conditional cost argument is sound once the full graph and constants have a uniform O(N log log N) construction and all gates, coefficients, routing and outputs are charged. Computing the Gauss normalization and endpoint chirps can be charged O(N) using a supplied-root table and an explicit recurrence; the missing Gauss factor is not itself a fatal cost obstruction. Uniform implicit adjacency alone does not prove O(N) working storage: the evaluator also needs a live-state or layer-size bound.

Further scope guards:

- The displayed Gauss derivation assumes odd N. An all-length theorem needs an explicit even-length reduction and its total cost.
- The inherited necessity of superconcentrator support uses prime-complex Fourier total nonsingularity, or a specified totally nonsingular rectangle. It cannot simply be applied to every composite Fourier matrix. The [classical depth-three support theorem](https://web.math.princeton.edu/~nalon/PDFS/super2.pdf) concerns generic support and does not provide Fourier phases.
- A Schur half-rectangle is a necessary subproblem; realizing it does not alone realize the full correction, all Fourier outputs, or cheap branch solves.
- The Weyl certificate M e_0=1 and MS=DM is sufficient as stated for a primitive root, but both symbolic identities must be proved for the actual candidate. The proposal supplies no candidate to certify.
- The v32 root-target count theorem does not directly exclude the Gauss route. Even a pure-root core targets G_N times a gauged Fourier matrix, followed by generally non-root scaling. Arbitrary γ_e further changes its model.

Status: preserve as a conjectural construction target with a repaired weighted-fiber obligation. Do not record O(N log log N) as an attained exact upper bound, infer impossibility from v32, or infer novelty from an unsuccessful literature search.

## 6. Fresh independent controls

The accompanying standard-library-only control program was written afresh and does not import or execute any source-package code. It passes:

- 16,623 prime count-vector/target checks for p=2,3,5,7 by polynomial division.
- Exact rational half-path, composite-sixth-root, and positive-irrational fifth-root boundary controls, including all 25 entries of the 33-edge full F_5 alphabet counterexample.
- Exact 3p-edge zero-gadget and direct-plus-zero path counts for p=2,3,5,7,11.
- 1,276 exact and variable-depth alphabet-sumset checks, plus the p=101 thresholds.
- All 8,192 normalized two-input/two-output DAG supports with two internal vertices. The 317 all-pair-unique supports without a mixed vertex have at least four edges; this is a finite control, not the general proof.
- The Gauss identity and endpoint correction for every entry at N=3,5,7,9,15,17 in two suitable exact finite fields each: 1,356 entries total. These validate controls, not all-length existence or complex-field priority.
- A same-phase/different-amplitude counterexample at N=3 over F_7: expected G=2, perturbed sum 3.
- Source archive CRC, all manifest hashes, standalone-note identity and predecessor byte identity.

Full results are in `FRESH_RESULTS.json`; the source audit code is `fresh_controls.py`. No external write or publication occurred. Reif's comparison remains unresolved; no repeated failed full-text fetch was attempted for that unrelated open gap.
