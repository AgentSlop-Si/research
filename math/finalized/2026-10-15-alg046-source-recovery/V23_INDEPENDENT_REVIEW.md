# Independent review: metaplectic Bruhat rigidity v23

## Verdict and correction

**Accept the algebraic classification, two-way Fourier equivalence, any-depth projective fusion and unique three-shear statements for odd prime length.** Correct the arbitrary-depth cost ledger: a fresh word of length t requires reading and multiplying its t symplectic parameters and recovering its projective scalar. The fully charged bound is **O(t+N) plus at most one Fourier application**, with an explicit O(N) scalar/root-table preparation described below. The source's O(N) or T_F(N)+O(N) row is valid only for fixed depth or after word preprocessing; it is not a bound independent of an unbounded fresh word length.

“Fourier-hard” means equivalent to Fourier with O(N) overhead, not a proved Omega(N log N) arithmetic lower bound. Finding a new fast evaluator for a big-cell operator would equally give a new fast Fourier evaluator. The classification does not forbid that achievement; it says the factorization alone does not remove the task.

All mathematical sections 1–9 of RESEARCH.md, the complete CHAIN_CHECKPOINT, README, PRIOR_ART_AUDIT, OPERATION_LEDGER and both result summaries were read. All substantive formal claims are addressed here. Uploaded Python/bytecode stayed inert and was not implementation-certified. Original 10/10 test-group execution, its 120-word seeded samples, N17 full-kernel experiments and logged timings were not rerun. Fresh independent checks and their counts are separated below. Nested v22/earlier appendices retain their earlier coverage, rather than being silently declared re-audited.

## Algebra and conventions

Use W=[[0,−1],[1,0]], L(t)=[[1,0],[t,1]], D(a)=diag(a,a^−1), positive unnormalized F[x,y]=omega^(xy), chirp C_t[x,x]=omega^(t x²/2), and P_a e_j=e_(aj). These signs and permutation directions are mutually consistent.

If b=0, S=[[a,0],[c,a^−1]]=L(c/a)D(a), and its representative is the monomial C_(c/a)P_a. If b≠0, direct 2-by-2 multiplication gives

S=L(d/b)D(−b)W L(a/b),

and applying the four explicit operators gives exactly

R(S)[x,y]=omega^((d x²−2xy+a y²)/(2b)).

Every entry is nonzero. Undoing the two chirps and the dilation extracts F with O(N) work; applying R(S) from F uses the reverse sequence. Thus the two cases are disjoint and exhaustive relative reductions. The lower Borel is a subgroup, so an all-small-cell word remains monomial. A nonzero scalar multiple of F is dense for N>1 and cannot equal that word. This also proves the factor-by-factor corollary without relying on faithfulness or a vague computational hardness assertion.

Multiplying symplectic matrices classifies any-depth words. Projective scalar bookkeeping is required for exact, rather than projective, equality; see the repair below. There is no composite-ring or higher-dimensional classification here.

For L(x)U(y)L(z), its matrix is [[1+yz,y],[x+z+xyz,xy+1]]. Equality to W forces y=−1, then z=x=1. The ULU pattern similarly gives (−1,1,−1). Its central/outer big-cell factors are Fourier-equivalent as stated. Neither factorization improves Fourier costs by itself.

## Exact projective law and fully charged scalar extraction

The reviewer derives an explicit multiplication scalar for the chosen unnormalized representatives. Let S,T have upper-right entries b,e, let ST have upper-right entry f, and let

G=sum_(z in F_N) omega^(z²), with quadratic character chi on F_N^*.

Then R(S)R(T)=lambda R(ST), where

- lambda=1 if b=0 or e=0;
- lambda=N if b and e are nonzero but f=0;
- lambda=chi(f/(2be)) G if b,e,f are all nonzero.

For two dense kernels, multiplying and summing over the internal coordinate gives a quadratic Gauss sum with quadratic coefficient f/(2be). Completion of the square yields the third line. If that coefficient vanishes, Fourier orthogonality gives N times the supported monomial, yielding the second. A monomial factor selects a single internal coordinate and gives the first. The classical identity G²=chi(−1)N ensures every scalar is nonzero. The coefficient field must contain the primitive Nth root; this already prevents characteristic N. Fractions in exponents are parameter-field inverses, not division by two in an unrelated coefficient characteristic.

Prepare omega powers, the quadratic-character table, G, and parameter inverses in O(N) field/word operations and O(N) storage. For example, the prime-field inverse table uses inv[k]=−floor(N/k)inv[N mod k] modulo N; quadratic residues are marked by enumerating squares. Each 2-by-2 multiplication and each scalar lookup then takes O(1) field/word work. Accumulate the product scalar during the t-step symplectic fold. Apply the final monomial or big-cell representative and one scalar-vector multiplication. This proves the repaired O(t+N)+at-most-one-Fourier bound with no hidden dense scalar extraction or free arbitrary-depth preprocessing. This explicit repair is supplied by the independent review, not claimed as an original contribution of the uploaded code.

A word whose product is W represents a scalar multiple of F until this accumulated scalar is removed. The source's “exactly F” language is understood after that explicit normalization. Input root/field construction and bit complexity are outside this exact-field model; supplied roots and all phase/lookup preparation are still charged.

## Independent controls

The fresh standard-library checker imports no source program or data. It enumerates SL2(F_N), builds the direct kernels, and independently multiplies the Bruhat factors for N=3,5,7,11,13. It checks 548,496 matrix entries across all elements, verifies the monomial/dense patterns and cell cardinalities N(N−1), N²(N−1), N(N²−1), and exhausts both three-shear parameter triples at all five lengths.

All 14,400 ordered multiplication pairs in SL2(F5) satisfy the exact scalar formula, not merely an existence-of-some-scalar test. One hundred fifty fresh words at lengths 1,2,3,5,12,30 verify the paid accumulated scalar against actual matrix multiplication. Borel closure is checked for every Borel pair at every tested length. Coefficient fields are the first primes admitting an Nth root; all root and Gauss guards are exact. These tests supplement the all-prime proof, not replace it.

The test scope exceeds the source in some directions and differs in seeded samples. In particular it does not claim to reproduce the original N17 operator experiments or all uploaded unit-test behaviors. Isolated replay needs only the reviewer's one script and reproduces the exact result JSON.

## Provenance and prior art

The v23 archive SHA-256 is cf7570b1afd956fded5c5353fb01b0716a2c73c480ebcd64c1f51a8363d9b962, Library libfile_3dbea5c5d3848191b9a0c190bead6f81. CRC and all fourteen internal manifest entries pass. Its nested v22 ZIP is byte-identical to the earlier direct source, SHA-256 e1d30f08aa720c4e492a0e268b343d08d52bd80ecb126ab3fbe6c27097f36906. The accepted v22 review was read for the precise predecessor scope; its two-line classification remains unchanged. V23 extends the project framing to arbitrary-depth one-dimensional metaplectic words using classical Bruhat structure.

Bibliographic corrections: [arXiv:0808.1495](https://arxiv.org/abs/0808.1495) is by Gurevich, Hadani **and Sochen**, not only the first two authors. [arXiv:1010.2831](https://arxiv.org/abs/1010.2831) is by **Feng, Gu, Wang, Wu and Zhou**, not “W. Wang” alone. The source correctly treats the Weil/Bruhat ingredients as classical and makes no publication-priority claim. [Gurevich–Hadani–Howe](https://arxiv.org/abs/0808.2447) is the stated primary Gauss/Weil reference. These primary metadata/abstracts were checked for attribution and subject, not reviewed as full proofs of every cited theorem. The algebraic formulas above were derived independently.

## Remaining boundary

This does not classify higher-dimensional symplectic/tensor embeddings, composite-length ring phenomena, non-metaplectic stages, nonlinear/adaptive algorithms, or new direct Fourier evaluators. A separate v24 companion has been reported and remains a separate pending audit. No claim about it is incorporated into this immutable v23 review.
