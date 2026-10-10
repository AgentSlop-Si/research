# Independent audit of the holonomy phase cone obstruction

10 October 2026

## Decision

Accept the submitted spectral phase-cone theorem and its stated nonnegative-mixer and jointly phase-integrable Green specializations. The proof is valid for every N>=2, every common entrywise sector of width 0<=W<pi, and arbitrary invertible complex outer monomial gauges. The correct error measure is the complex Euclidean operator norm relative to a normalized flat unitary target.

Accept the O(N+q) bound for the discrete graph and histogram preprocessing in the modular-word model. Do not promote that bound to a complete bit-complexity bound for a certified threshold comparison, magnitude-product validation, coefficient preparation, or Fourier execution. The manuscript already records the main threshold-comparison caveat; the same qualification should accompany the shorter executive claims.

The phase-holonomy lemma is classical gain-graph switching theory. The complete Fourier/Green specialization and its displayed stability bound have been checked mathematically here, but their historical originality has not been established. The accepted unitary real-collinear exclusion and the independently accepted complex phase-averaging construction remain intact.

## Source identity and coverage

The standalone THEOREM(20261010-123847).md and the THEOREM.md inside FFT_HOLONOMY_PHASE_CONE_RIGIDITY_2026-10-10.zip are byte-identical.

- Theorem SHA-256: 62fac4ad0add32886b77c54329bd590eda9f3a61d439478e4353d12c1acfeb64
- Archive SHA-256: 02ae657bcfe3378a32dace476aea1bf2ffc91357a51146b7dc5d54e2ce8ec5cc
- All 14 file members were hashed. The archive CRC check and all 12 entries in its supplied checksum list passed.

This audit read the complete theorem, executive summary, source-audit discussion, next-construction note, and the two submitted verification programs as text. No uploaded program was executed or imported. Source-reported corpus counts and numerical successes are not adopted as independent evidence. The fresh review controls are separate.

The authoritative mathematical evidence for this review is the actual source-file text, preserved under [source statements](../sources/phase_cone/README.md).

## The core proof including the gauges

Let H0 be any normalized flat unitary, so ||H0||_2=1 and |(H0)_jk|=1/sqrt(N). Write the invertible monomial factors as L=V1 D1 and R=D2 V2, where V1,V2 are unitary monomial matrices and D1,D2 are positive diagonal matrices. Then

    V1* (L C R-H0) V2* = Q-H,
    Q=D1 C D2,  H=V1* H0 V2*.

H remains flat and unitary, the error epsilon is unchanged, and Q remains in the same entrywise sector as C. A common scalar phase rotation centers the sector without affecting these facts. Put c=cos(W/2)>0. Then Re Q_jk>=c|Q_jk|.

For E=Q-H,

    ||E||_F <= sqrt(N) epsilon,
    sum_jk |E_jk| <= N ||E||_F <= N^(3/2) epsilon,
    |1* E 1| <= N epsilon,
    |1* H 1| <= N.

Flatness gives sum_jk |H_jk|=N^(3/2), so

    c N^(3/2)(1-epsilon)
      <= c sum_jk |Q_jk|
      <= Re(1* Q 1)
      <= N(1+epsilon).

Rearrangement gives

    epsilon >= max(0,(sqrt(N)c-1)/(sqrt(N)c+1)).

No inverse norm, gauge condition number, minimum nonzero entry, or dominance hypothesis occurs. For epsilon>=1 the inequality is immediate; for smaller errors the same calculation applies. The proof does not assume the outer gauges are unitary, only that their positive parts preserve entry phases and their remaining parts are unitary monomial.

Flatness is essential. The identity matrix is a nonnegative unitary but is not flat for N>=2, so the same conclusion cannot be asserted for every unitary target. Monomiality is also essential: if arbitrary outer matrices were allowed, C=R=I and L=H0 would produce error zero with W=0.

## Exact and approximate consequences

Exact equality requires W>=2 arccos(1/sqrt(N)). For a proposed error tolerance 0<=e<1, rejection is sound when

    sqrt(N) cos(W/2) (1-e) > 1+e.

This is a strict rejection comparison. Equality does not reject under this bound. In particular, floating-point rounding near N=2,W=pi/2 or N=4,W=2pi/3 must not create a false positive. The N=2 endpoint is attained by 2^(-1/2)[[1,i],[i,1]]. Higher-dimensional sharpness is not asserted or established by the manuscript.

For a fixed eta>0 and W<=pi-eta, the lower bound tends to 1. This is a lower bound on liminf error, not a statement that every architecture has error tending to 1 or that the restricted Green family attains the floor.

For the unnormalized Fourier matrix F=sqrt(N)H0, the corresponding absolute lower bound is sqrt(N) times the displayed floor. Equivalently, ||M-F||_2/||F||_2 satisfies the same normalized bound. An arbitrary nonzero global target scale multiplies the absolute error bound by its modulus. The claim is over the complex numbers and ordinary operator norm; it is not a finite-field norm statement.

## Multistage propagation and degeneracies

An entry of A0 D1 A1 ... Dt At, with entrywise nonnegative real Aj, is a finite sum of nonnegative magnitudes times products of mask entries. Choose a real lift of each mask's containing phase arc. Every nonzero path term lies in the angular sum of those arcs. If the total width W is below pi, that sector is convex, so addition preserves it. This proves the arbitrary-depth extension, including rectangular intermediate mixers of compatible sizes, zero entries, singular mixers, arbitrary mask magnitudes, and stage counts depending on N.

The phase widths must be measured for common arcs, not separately optimized entry by entry. Negative or complex branch coefficients are not automatically nonnegative mixers; one must independently re-establish the actual common-cone hypothesis if such coefficients are present.

If the entire mask is zero, its nonzero-phase set is empty. Define its phase width as zero by convention, or handle it separately: the resulting network is zero and has normalized error exactly 1. A singular core has rank deficiency and hence error at least 1 from any unitary, so singular cases do not threaten the theorem. A zero individual mask entry simply contributes no path term. At W>=pi the narrow-cone test is inconclusive, not evidence of compatibility.

Masks whose entries lie on a common real line produce a scalar multiple of a real core. For N>=3, the nonreal Fourier 2-by-2 cross-ratio excludes exact equality after arbitrary complex monomial gauges. This is a separate projective argument; the cone estimate alone does not claim it.

## Holonomy and positive Green inverses

Use the source's row-edge convention T_uv=w_uv. Diagonal dephasing by H=diag(exp(i theta_u)) changes that entry's phase to phi_uv-theta_u+theta_v. It is positive exactly when

    theta_v-theta_u = -phi_uv modulo 2pi.

The condition telescopes on every closed walk in the undirected union multigraph. Conversely, propagation on a spanning tree defines a potential and the remaining edge checks establish consistency. Reverse traversal negates the phase. Distinct parallel edges must remain distinct constraints: collapsing them can erase a genuine conflict.

Individual cycle balance does not suffice for a union. As an exact example modulo 5, take a phase-zero cycle 0->1->2->0, and the reverse cycle 0->2->1->0 whose phases are generated by vertex potential (0,1,0). Each cycle is separately balanced. The first forces all potentials equal, and the second then has an inconsistent edge. The union has no common potential.

For each legal weighted Hamiltonian cycle, strict positivity of the edge magnitudes and their product p<1 give

    Tpositive^N=pI,
    (I-Tpositive)^(-1)=(I+Tpositive+...+Tpositive^(N-1))/(1-p).

Exactly one path length in 0,...,N-1 joins each ordered coordinate pair, so every inverse entry is strictly positive. Individual weights may exceed one; their product is the relevant guard. At p=1 the positive cycle inverse is singular. At p>1 the displayed inverse has negative entries, so this proof of positive Green sums cannot be used unchanged. All resolvents are ordinary existing inverses, with no pseudoinverse or limiting convention.

A shared potential for each two-cycle stage gives

    A=HA Apositive HA^(-1),
    B=HB Bpositive HB^(-1),
    M=(L HA) Apositive Deffective Bpositive (HB^(-1) R),
    Deffective=HA^(-1) D HB.

The outer products remain monomial. It is the phases of Deffective that determine the rejection width, not the phases of D alone. Each stage union is connected because it contains a Hamiltonian cycle. Consequently its potential is unique up to one additive constant, and changing the two constants only rotates every effective phase equally. This justifies width invariance. The same assertion would require care for disconnected general graphs with independently shiftable components.

Failure of a union-potential test only says this specialization is unavailable. It is not itself a no-go certificate for the network. Conversely, passing the test and the angular threshold is only absence of this obstruction, not a synthesis certificate.

## The near-linear algorithm and the certification boundary

For integer phase labels modulo q and four explicit Hamiltonian cycles, there are 4N directed edges. A static traversal checks the two union systems and recovers potentials with O(N) modular-word operations. It works for prime, composite, and q=1 moduli; it does not require division in the residue ring. Computing N effective residues costs O(N). A q-bin occupancy scan costs O(N+q) time and O(N+q) storage including the graphs.

For occupied residues a1<...<am, define gaps as a_(j+1)-a_j and a1+q-am. The shortest width is q minus the largest such interoccupied distance, measured in qths of a revolution. It is not q minus the number of unoccupied bins. A singleton has one circular gap q and width zero. The empty set is treated separately as above. The condition W<pi is the exact integer comparison 2k<q, where k is the histogram span.

The final strict comparison can avoid square roots. With W=2pi k/q and a rational tolerance e, test the sign of

    Delta=N cos^2(pi k/q)(1-e)^2-(1+e)^2.

Reject only when Delta>0 is certified. A cyclotomic algebraic-number sign algorithm or rigorous rational interval bounds can supply this certificate. Intervals containing zero must remain inconclusive or be refined; an exact equality needs a separate equality procedure if termination on all inputs is required. Neither ordinary machine cosine nor a tolerance-based numeric assertion is a zero-error proof.

Our small review implementation uses rational Machin-formula bounds for pi and rational Taylor bounds for cosine. It handles common special-angle equalities exactly and otherwise returns a sign only after its rational interval excludes zero. It is a sound control implementation with a finite precision cap, not a claimed complete all-input near-linear certified solver. It never rejects an unresolved case.

The O(N+q) count assumes q fits the modular-word model and phase labels are supplied. It does not charge bit growth, the precision required by near-threshold comparisons, extraction of exact phase residues from arbitrary complex input data, or exact validation of magnitude products. Hamiltonian structure can be checked in linear combinatorial time, but coefficient and magnitude representations must be specified for a complete machine certificate. The manuscript assumes each product guard; a deployment must either validate it or explicitly trust it as certified input.

## Relation to the accepted unitary packages

The earlier accepted real-collinear theorem concerns sums of unitary-cycle resolvents with |w|=1 and nontrivial cycle holonomy H!=1. It excludes every N>=4 with any finite number of real-collinear coefficients, while genuine N=2 and N=3 witnesses exist. Its proof uses the common diagonal and G+G*=I.

The separately accepted phase-averaging construction proves that unrestricted complex coefficients in a fixed-holonomy diagonal-conjugacy orbit span every constant-diagonal complex matrix. A Fourier column gauge puts Fourier in that space. The explicit formula displays up to 3^(N-1) terms and is not an efficient transform algorithm or a minimum-term statement.

There is no contradiction. Unit-modulus cycles fail the new theorem's product-of-magnitudes-below-one hypothesis. A unit-modulus cycle with completely removable edge phases would also have holonomy one and a singular resolvent, whereas the earlier legal objects require holonomy different from one. In addition, independent internal conjugations and arbitrary complex summation coefficients do not establish either a shared stage potential or a narrow common entrywise cone. Even for damped individually dephasable cycles, their union need not share one potential.

The phase-averaging proof retains its accepted status and frozen SHA-256 880c45d731f4d5296f7f73ba637838542ada72dd321adb3b2b553458b5723fda. Its independent acceptance report has SHA-256 8c7ed876e83e579f59270cd8e712d47fe7cdc3d7a44014e78aba532e5cccf037. No prior accepted record was revised by this audit.

## Fresh independent controls

All fresh controls passed:

- 221 exact modular union-potential cases, plus explicit individually balanced but union-frustrated and parallel-edge negative controls.
- 2,046 exhaustive occupancy subsets for q=1,...,10, compared with a separate brute-force covering algorithm, including rotations, empty sets, singletons, wraparound, and antipodal phases.
- 2,135 exact rational-interval threshold decisions on a grid, plus 10 named equality or strict-sign cases. Floating-point values were a secondary cross-check, not the certificates.
- Three exact four-Green examples at N=3,4,6, including similarity, two-sided inverse identities, positivity, and effective quadrant cones; additional guards cover p=1, p>1, and an individual edge magnitude greater than one.
- 90 numerical operator-norm examples with random outer phases and permutations, strongly uneven positive gauge magnitudes, and zero cores.
- 12 numerical multimask examples through nine masks, plus the N=2 equality endpoint and explicit scope counterexamples.

A complete additional N=4,q=4 certificate uses effective residues (0,1,0,1), so W=pi/2, and exact cycle products 1/16 and 16/81 in each stage. For target error e=1/10 the squared comparison gap is exactly 41/100>0. This rejects every invertible complex outer monomial gauge without numerical dense-matrix evidence. In this example the raw mask phases span 3pi/2. A companion control has raw width zero but effective width pi, demonstrating the danger of using the raw mask.

The reproducible files are [fresh_controls.py](../controls/phase_cone/fresh_controls.py), [FRESH_CONTROL_RESULTS.json](../controls/phase_cone/FRESH_CONTROL_RESULTS.json), and [EXACT_REJECTION_CERTIFICATE.json](../controls/phase_cone/EXACT_REJECTION_CERTIFICATE.json). The raw console log is excluded from this export. These finite controls supplement the general proof; they do not prove it by extrapolation.

## Primary literature and novelty limits

Zaslavsky's [Biased Graphs I](https://people.math.binghamton.edu/zaslav/Tpapers/bg1.jctb1989.pdf), Journal of Combinatorial Theory B 47 (1989), Lemma 5.3, already identifies balanced gain graphs with graphs switchable to identity gains and uses a spanning-tree argument. This directly subsumes the manuscript's holonomy equivalence. The gain-graph lemma should therefore be explicitly attributed as classical.

Tadej and Zyczkowski's [A concise guide to complex Hadamard matrices](https://arxiv.org/pdf/quant-ph/0512154), Definitions 2.1–2.3 and Lemma 2.5, supplies standard flat-unitary normalization, phase/permutation equivalence, and the Haagerup four-entry invariant background. These are established ingredients rather than new concepts in this package.

The official [exact Fourier comparator](https://github.com/openai/math/blob/main/lean/docs/130.md) distinguishes a subsequential circuit result from a separate uniform sub-n-log-n result in exact complex arithmetic with unrestricted coefficients and a supplied root of unity. A phase-constrained representation obstruction does not contradict those stated models and is not an unrestricted FFT lower bound.

Johansson's [Arb paper](https://fredrikj.net/math/arbpaper.pdf), IEEE Transactions on Computers 66 (2017), describes rigorous arbitrary-precision interval arithmetic and error tracking. It is relevant background for the certification requirement, not a source for the Fourier obstruction or a complexity proof for this oracle.

Targeted searches did not identify the precise displayed stability inequality as an earlier published theorem. This is a limited negative search result, not evidence of first publication. The audit accepts correctness and scope, with the combination described conservatively as an elementary specialization or synthesis unless a fuller historical comparison establishes more.

## Recommended source clarifications

1. Attribute the holonomy equivalence directly to classical gain-graph switching theory.
2. Repeat the threshold-certification caveat beside short O(N+q) claims, not only in the full theorem.
3. Define empty phase sets and specify interoccupied circular gap distance to eliminate boundary ambiguity.
4. Label an integrability failure or threshold pass as inconclusive, and distinguish trusted magnitude guards from checked ones.
5. Keep all phase-averaging, unitary-collinear, nonnegative-mixer, and jointly dephasable models separate. Preserve the existing statements that no universal O(N) FFT, sharp higher-dimensional optimum, or historical novelty has been established.

These are attribution and implementation-scope clarifications. No fatal proof error was found in the stated restricted spectral obstruction. All changes produced by this audit are local; the source artifacts and remote repositories were left unchanged.
