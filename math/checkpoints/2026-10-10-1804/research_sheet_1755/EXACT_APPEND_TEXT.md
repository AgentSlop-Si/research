[2026-10-10 18:00 UTC; independently accepted bank-count refinements] For odd N, m≥(N−1)/2 and d=N−m≥4, the whole-left recurrence matrix has rank at most min((d−1)(d−2)/2, 4d−11). A monic degree-m kernel polynomial with nonzero constant, distinct roots and full axis rank yields 2m+2 legal banks over its splitting field. Exact characteristic-zero lifts establish 18, 24 and 54 banks at N=13,17,35. The guards are now uniformly proved: the earlier accepted bound is 2N−2 floor((sqrt(N)+16)/13)+2 for odd N≥1297; the separately accepted block-coherence refinement improves this to 2N−2 floor(sqrt(N)/8)+2 for every odd N≥1025. Put d=floor(sqrt(N)/8), m=N−d: orientations are (m,1,1,m), all beta=1, with shared same-sign roots of a polynomial over Q(q), and splitting-field degree at most m!. Thus the additive saving is sqrt(N)/4+O(1), while the leading coefficient remains 2. The finite parameter-grid recipe is not claimed efficient. No K-only attainment, unrestricted minimum, 8N/5 theorem, scalar FFT runtime improvement or historical-priority claim follows. See NEW-17 and the separately hash-bound envelope, uniform and constant-eight review receipts.

[2026-10-10 18:00 UTC; independently accepted aggregate-chain refinement] For prime p≥5 and W(n)=sum over prime divisors r of v_r(n)(1−1/r), an explicit subgroup-ordered sine-difference chain has exact separately colored aggregate count E=2p²+2p−2−(p−1)W(p−1). This sharpens the preserved four-chain count for p≥7 and retains E(5)=54. An unconditional sequence of prime divisors of Fermat numbers has Omega(p log log p) savings relative to 2p²+p. For every finite abelian group G of order n, max Σ_j(|Stab(T_j)|−1)=n W(n), over all element orderings and all nonempty prefixes. Maximizers are exactly recursive prime-index subgroup coset blocks with independently maximizing block orders; the top subgroup is unique. Their labeled count satisfies A(G)=Σ over maximal K of [G:K]! A(K)^[G:K], A({0})=1. The Fourier count is optimal only within the fixed sine-difference single-chain coefficient family, not among all aggregate graphs. Dense A=F keeps construction and evaluation quadratic. No global aggregate minimum, subquadratic FFT, bounded-coefficient or historical-priority claim is made. See NEW-16.

[2026-10-10 18:00 UTC; independently accepted pole/gauge review] On a finite source-to-sink DAG, internal gauges fixing boundary vertices make every nonzero edge valuation nonnegative exactly when every full input-output path has nonnegative total valuation; zero edges are omitted. Applied to the fixed 99-edge N11 support, any algebraic Fourier solution must have a negative-valuation full path at each place above 11. The reviewed entrywise tropical candidates are excluded by exact two-by-two minors/initial forms. The 26 one-family minors force 63 coefficients nonzero (21 per layer); 21 safe gauge choices plus one of edges 0,11,22 give three charts covering all possible factorizations. Nonzero does not mean valuation zero. Arbitrary poles and arbitrary complex coefficients remain OPEN. The later symbolic 16-variable/59-equation continuation is unreviewed and is not promoted here. See NEW-18.

[
  [
    "NEW-16",
    "Subgroup-chain count and prefix optimization",
    "Proof closed (scoped)",
    "For prime p≥5, E=2p²+2p−2−(p−1)W(p−1), with W(n)=Σ over primes r of v_r(n)(1−1/r). This is an exact separately colored edge ledger. Along an unconditional prime-divisor sequence, the saving from 2p²+p is Ω(p log log p). For every finite abelian group G of order n, max Σ_j(|Stab(T_j)|−1)=n W(n), over all element orderings and all nonempty prefixes. Maximizers are exactly recursive prime-index subgroup coset blocks with independently maximizing block orders; the top subgroup is unique. Their labeled count satisfies A(G)=Σ over maximal K of [G:K]! A(K)^[G:K], A({0})=1. The Fourier count is optimal only within the fixed sine-difference single-chain coefficient family, not among all aggregate graphs.",
    "Dense A=F keeps Θ(p²) construction/evaluation. Ordering optimality is confined to the fixed sine-difference single-chain coefficient family. No unrestricted aggregate minimum, bounded-weight or FFT-speedup claim.",
    "Independently accepted correctness; historical priority remains unresolved. Related refinements are grouped in one result row, not counted as separate discoveries.",
    "SCHUR-V28",
    "1735 aggregate review; 1744 prefix-optimality independent acceptance"
  ],
  [
    "NEW-17",
    "Uniform square-root saving in signed banks",
    "Proof closed (scoped)",
    "For every odd N≥1025 and primitive Nth root q, at most 2N−2 floor(sqrt(N)/8)+2 legal signed banks realize negative Fourier over a finite splitting extension of K=Q(q). With d=floor(sqrt(N)/8), m=N−d, orientations are (m,1,1,m) and extension degree is ≤m!. The proof secures monic, squarefree, nonzero-node and axis guards. Separately accepted finite lifts give 18,24,54 banks at N=13,17,35. The common-annihilator envelope is rank≤min((d−1)(d−2)/2,4d−11) in its stated range.",
    "Bank count is 2N−sqrt(N)/4+O(1), with leading coefficient 2. Literal branch count is N times the bank count. No K-only attainment, unrestricted minimum, 8N/5 theorem, efficient parameter search or scalar FFT runtime claim. Earlier constant-13 proof remains valid.",
    "Independent proof acceptance only; classical coherence/annihilator ingredients. Historical priority unconfirmed. Construction and refinements form one grouped result.",
    "Q35",
    "1735 bank-envelope, uniform-sqrt and constant-eight acceptance receipts"
  ],
  [
    "NEW-18",
    "Integralizing gauges and fixed-support pole exclusions",
    "Proof closed (scoped)",
    "A finite source-to-sink DAG can be internally gauged integral with boundary fixed iff every full path has nonnegative valuation, after omitting zero edges. For the fixed 99-edge N11 support, any algebraic Fourier solution must have a negative full path at every place above 11. Reviewed tropical candidates fail exact minor/initial-form tests. The 26 one-family minors force 63 nonzero edges; 21 safe gauges plus the choice of edge 0,11 or 22 cover all solutions with three charts.",
    "Necessary conditions and exclusions of specified candidates only. Nonzero edges need not be units. Arbitrary poles/complex factorization remain OPEN. The symbolic 16-variable/59-equation continuation is unreviewed and excluded.",
    "Difference constraints, tropical tests and path-minor tools are classical. Fixed-topology checks are accepted; worldwide novelty and a full pole obstruction are not established.",
    "SCHUR-V28",
    "1735 pole-escape review; minor, monomial-rank and mandatory-edge receipts"
  ]
]
