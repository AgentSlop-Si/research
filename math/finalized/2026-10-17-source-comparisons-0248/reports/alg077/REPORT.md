# ALG-077: bounded precision and word-RAM source comparison

Date: 17 October 2026 (UTC). Outcome: **qualified nonmatch for the named comparators**. This completes the stated bounded comparison, not the parent research program, production implementation, historical priority inquiry, or an exact Fourier problem.

## 1. Decision

The actual ALG-077 all-length Chebyshev/Bessel and charged rational-Taylor contracts are randomized, energy-relative approximations to a normalized complex Fourier transform. The named results of Chan–Jin–Vassilevska Williams–Xu and Fürer supply exact discrete multiplication primitives. Neither theorem, as stated, implies the ALG-077 contract or is implied by it through an identified, fully charged reduction.

The overlap is genuine at the level of finite precision, packing, FFT subroutines, and paid preparation. It is insufficient for a same-model runtime or priority conclusion. In particular:

- The precision scale, probability quantifiers, norm and output type must survive an actual adapter.
- Fusing input channels does not remove the R complete decoder scans.
- A numerical full-row guarantee does not certify a decoder operating on separately prepared, rounded summaries.
- This comparison does not substitute ALG-028/Q01's distinct deterministic finite-word relative-l2 theorem or its earlier comparison for ALG-077.

The narrow owner action is to record this comparator-specific result and retire the instruction to repeat this exact comparison. Preserve accepted scoped correctness, historical text, score 34, the related Q01 material, and unresolved broader attribution/implementation obligations.

## 2. Sources and identity

The repository and current owner-index snapshot were read at commit `26eb7017276591988762f27e2d1c23e739bcf3e4`. Live native owner rows were also read: Catalogue ALG-077 at row 154, novelity breakthough ALG-077 at row 106, and Research overview ALG-077 at row 178. The live cells and the index agreed on the comparison gate and score 34. Row numbers are locators, not identity; any application must re-resolve ALG-077.

Repository sources, read in full as text:

1. [V11_AUDIT.md](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/29/29d7a474e8ccded269595078cbe44f1557f78b5ab4891a92d7ded8eecd390f25__29d7a474e8ccded26959__V11_AUDIT.md), SHA-256 `29d7a474e8ccded269595078cbe44f1557f78b5ab4891a92d7ded8eecd390f25`, 18,092 bytes. Principal locators: sections 2, 4–8.
2. [CHARGED_TAYLOR_PRECISION_EXTENSION.md](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/ef/ef1423c115d5ef1b62060d5cd6c2baa179b0e3c84e1faf55ddfb759470b472a6__ef1423c115d5ef1b6206__CHARGED_TAYLOR_PRECISION_EXTENSION.md), SHA-256 `ef1423c115d5ef1b62060d5cd6c2baa179b0e3c84e1faf55ddfb759470b472a6`, 18,202 bytes. Principal locators: sections 1–7, equations (1)–(10).

These exact repository bodies match the pre-existing local archive bytes. The two source bodies are included for reproducibility. No predecessor program was imported or run. The earlier audits' numerical checks remain attributed historical evidence, not fresh replay claims here.

Primary external sources:

3. [Chan et al., arXiv:2310.13174v3](https://arxiv.org/html/2310.13174v3), dated 19 December 2024: Lemma 2.2, Appendix B, Lemmas B.6–B.7 and Corollary B.8, including their preparation and rearrangement arguments.
4. [Fürer, arXiv:1402.1811v1](https://arxiv.org/pdf/1402.1811v1): Definitions 1–2 on printed pp. 3–4, SS-C discussion and Theorem 1(a) on printed p. 6 (PDF pages 3–4 and 6, one-based).

Only the named contracts and relevant proofs were compared. This is not an exhaustive literature search or independent verification of every theorem in either external paper. `PRIMARY_SOURCE_MAP.json` separates primary statements from conclusions derived in this report.

## 3. Reconstructed ALG-077 contract

### 3.1 Domain, output, and quantifiers

Let N be the complex-transform length, Q the next power of two, and N <= Q < 2N for N >= 2. The dyadic block construction uses Q=KM, M^2<=Q. N=1 is a mathematical identity case; V11 notes that the demonstrated end-to-end code does not handle it without an explicit branch.

The ideal target is the full vector U_N x, with unitary normalization 1/sqrt(N). The mathematical input is x in C^N. A numerical realization needs a declared finite representation and range; the charged extension inherits a common-exponent bounded-integer input model and a certified norm envelope B >= ||x||_2. Conversion to represented x' adds ||x-x'||_2 to normalized Fourier error. Unlimited real precision is not a finite input model.

Randomness is per fixed input. One random state is shared across all expansion ranks within a row; distinct aggregated rows are independent. It is not a single fixed seed that works exactly for every input.

### 3.2 Bias and variance

For V11's H=0 Bessel fusion, with Delta=pi(M-1)/Q:

    ||Xbar - U_N x||_infinity <= (tau_R + Delta)||x||_2
    E|Xhat_k-Xbar_k|^2 <= (M/N)(1+tau_R)^2 ||x||_2^2.

The full charged Taylor lift uses s_n=n/Q, exact nearest-grid residual theta_k=(kQ-j_k N)/N, certified rational rho with |rho-pi|<=eta, q=|rho|<4, and

    p_R(s,theta)=sum_(r<R) (-2i rho theta)^r s^r/r!
    tau_R=eta+q^R/R!.

Its deterministic bias is tau_R||x||_2 and its coordinate variance has the same displayed bound. V11 section 8's frozen-block Taylor variant has the additional Delta term; it is not identical to the full weighted-input Taylor lift.

For the charged Taylor implementation, a common certified row radius r obeys

    r >= g(1+tau_R)sqrt(M/N)B + epsilon_lift B,   g>sqrt(2).

The all-output aggregation guarantee is

    Pr[||Xtilde-U_Nx||_infinity > tau_R||x||_2 + (5/sqrt(2))r + eta_out]
      <= 2N exp[-L D(1/2 || g^-2)],

or, for L=2s-1, at most 2N binom(2s-1,s)g^(-2s). Exact grid classification and certified final conversion are hypotheses. For V11 H=0 use tau_R+Delta in the bias allowance, keeping its variance envelope unchanged.

With fixed s>1+a, fixed a>=0, the extension records error O(sqrt(log N)N^[-1/2+(1+a)/(2s)]||x||_2), failure <=N^-a, and O(N log N/log log N) arithmetic work. At a=0 the literal failure bound 1 is vacuous; the source explicitly replaces it by c<1 to obtain meaningful constant success. Fixed target epsilon instead gives O_epsilon(N) work and its stated O((log N)^2/(epsilon^4 N)) failure regime.

### 3.3 Precision is a certified interface, not just a bit count

The unfused Taylor composition ledger assumes a certified row evaluator on every represented weighted input, with epsilon_0=800 sqrt(QM)log2(Q)u, plus certified seeds, roots, normalizers, balanced scans and exponent range. The sufficient composed error is

    epsilon_lift = sqrt(Q/N) exp(q)[816 sqrt(QM)log2(Q)+16MR]u.

The smallness conditions include 8u log2(Q)<=0.01 and (11R+4)u<=0.01. The source gives an explicit sufficient u bound in equation (10); exp(q) can be replaced by rational upper bound 55. O(log N) mantissa bits suffice in the specified regimes under these conditions. This is not a fixed-binary64 theorem.

The fused path instead requires a decoder-on-summaries guarantee for arbitrary represented d:

    ||Dhat(d)-D(d)||_infinity <= epsilon_D ||d||_2,
    epsilon_D=C_D u log(Q)sqrt(Q).

A composite compression-plus-decoder bound alone does not imply this guarantee for independently rounded summaries. V11 also requires a summable coefficient envelope and charges summary formation, synthesis and Clenshaw rounding. Its fixed-H ledger is

    eta_fp=O([u log Q sqrt(MQ)+uM(log M+R^2+1)]||x||_2).

The distinctions between these two interfaces must survive any proposed use of an exact discrete multiplication subroutine. Exactness inside that subroutine would not certify the surrounding conversions or rounded summaries.

### 3.4 Complete cost ledger

For fixed H,L, streamed storage is O(N) arithmetic values; it is not necessarily only two live vectors. V11 retains a Q-sized plan and a Q-sized decoder forcing/scan for every rank. With Q=Theta(N), its R scans cost O(RN), even when only N selected outputs are returned.

The charged Taylor path pays O(LRN + log(1/eta)) arithmetic operations, plus inherited root/normalizer costs. Machin preparation uses O(log(1/eta)) exact rational operations; their growing operands are not constant-cost words by assertion. Root preparation uses certified guard precision, with O(Q) guard products and roundoff of order u/Q before final rounding. The Bessel alternative charges a bounded-argument series: for b=Theta(log N), R and series length J both Theta(log N/log log N), K=Theta(N/log N), block setup O(RKJ)=O(N log N/(log log N)^2), subordinate to O(RN).

A conservative Taylor bit ledger is

    O(LRN C_arith(w) + Q C_arith(w_g)
      + polynomial(log(1/eta)+w_g+log N) + input/output bit costs).

It also pays exponent/range management, exact O(log N)-bit grid indices, norm certification, three-grid classification and final conversion. O(N) values means O(Nw) mantissa bits plus these other components. Explicit N-coordinate output must be written. None of these charges is erased by calling a component an FFT.

## 4. Exact primary comparator contracts

### 4.1 Chan et al. (v3)

Lemma 2.2 deterministically computes length-n convolution over F_p in O(n log p), for prime p<=n^O(1), on logarithmic-word RAM. B.6 packs t_i=floor(0.1 log n/(m_i L_2 log p)) finite-field DFT instances into O(1) words: lookup costs O(1) after n^(0.2+o(1)) preparation. B.7's degree-L_1 multiplication costs O(L_1 log L_1 log p/log n) after that preparation. B.8 extends this to power-of-two degree Ltilde_1 in [L_1^0.2,L_1^10]. Field construction, roots, fixed twiddles, bit permutations and transpositions are accounted for in Appendix B. The final O(n log p) theorem includes its construction costs. These are exact finite-field outputs, with no probabilistic or numerical-error parameter. [Primary source](https://arxiv.org/html/2310.13174v3).

### 4.2 Fürer (v1)

Definitions 1–2 specify a log-RAM with O(log B)-bit working registers and constant-cost arithmetic including multiplication/division, Boolean operations, shifts and bounded instructions for input/output. Here B denotes the integer-input bit length called n in the paper. Theorem 1(a) gives O(B) time for SS-C exact integer multiplication. Its complex FFT computations use O(log B) accuracy to permit exact recovery by rounding. The proof includes input/output in its packed operation accounting. This is a discrete multiplication theorem; its numerical FFT is an internal component. [Primary source](https://arxiv.org/pdf/1402.1811v1).

## 5. Full mapping and failed direct identifications

This section gives deductions of the comparison rather than additional claims attributed to the papers.

| Requirement | ALG-077 side | What an adapter would have to establish |
|---|---|---|
| Input and algebra | Represented complex vector, exact integer indexing, finite range | Encoding into residue polynomials or integers, bounds on all encoded operands, and a recovery map for complex Fourier outputs. A characteristic-p computation is not automatically a complex computation. |
| Error and normalization | Unit-normalized output; additive l-infinity error measured against input l2 norm | An explicit output error transfer through encoding, arithmetic, decoding and 1/sqrt(N). Exactness of an encoded convolution alone supplies no such transfer. |
| Probability | Shared state across ranks; independent rows; per-input success after all-output aggregation | Preserve the same quantifiers and budget failure across every adapter call. Deterministic multiplication does not remove the random compression error. |
| Precision and range | w,w_g and exponent assumptions; separate row/summary interfaces | Convert each arithmetic step to legal bounded-word work, with rounding and overflow/underflow certified. Do not infer this from w=O(log N) alone. |
| Preparation | Rational coefficients, roots, normalizers, guards, summaries, exact grid classification | Charge every reusable table and conversion in a cold execution, and separately state any amortization. |
| Decoder scans | R complete Q-sized scans per row | Supply a replacement for the scans or retain O(LRN). Accelerating a short transform within a rank is not a proof that the rest disappears. |
| Output | Every one of N approximate complex coordinates | Charge assembly and conversion of all requested coordinates, including each output's width and scale. An encoded product or compact intermediate table entry is not yet that output. |

### 5.1 Norm conversion is substantive

From ||e||_infinity <= epsilon||x||_2, the immediate bound is only

    ||e||_2 <= sqrt(N)epsilon||x||_2.

The factor sqrt(N) is tight for this inference: take all N error coordinates equal in modulus. Thus a relative-l2 target 2^-t would require epsilon<=2^-t/sqrt(N) if this inequality is the only transfer. The stated polynomial-error regime, with exponent strictly less than 1/2, does not by itself give that target. This observation concerns what follows from the contract, not a lower bound on the actual algorithm's possible errors. It prevents silently importing Q01's different relative-l2 guarantee.

Nor does positive additive error imply exact output by rounding. Such a reduction needs a known output lattice separation Delta_out and a proved total error strictly below Delta_out/2 after all scalings. Arbitrary complex DFT outputs do not have an asserted universal lattice separation here.

### 5.2 Length and packing are different resources

The symbols in the three sources have different meanings: N transform coordinates; n finite-field coefficients; B integer bits. Even under a hypothetical lossless representation of N independent w-bit values, B=Theta(Nw), so a linear-in-B operation is O(Nw), not O(N). With w=Theta(log N), this distinction is asymptotically material. This is a size accounting observation, not a claimed complete DFT-to-multiplication reduction.

Likewise, replacing small residue coefficients by full working-precision complex values changes the payload that fits in a word. In the common w=Theta(log N) regime there is no automatic growing packing factor for such values in a Theta(log N)-bit word. A new encoding or multi-operation batching proof could alter that conclusion; none is supplied by a direct symbol substitution.

### 5.3 Exactness and rank do not transfer

For fixed L random states, V11's fused channel observations factor through at most L(H+1) summaries of any full M-coordinate block. If L(H+1)<M, that block has a nonzero common kernel. The two inputs v and -v then have identical summaries and norms but different invertible Fourier images. Therefore increasing R cannot turn this fixed-summary, fixed-state interface into a uniform exact decoder. This is the source's scoped rank gate, not an unrestricted Fourier lower bound and not a contradiction to per-input randomized approximation.

### 5.4 Bounded stop

The named primary sources and full repository contracts are accessible. The outcome is not an access blocker. No complete charged reduction was found within the stated comparison. Record **qualified nonmatch**, with the precise mismatches above. This does not prove that no reduction can exist, that the work is new, or that another source cannot settle its wider attribution.

## 6. Owner proposal and verification boundary

`OWNER_PROPOSAL.json` gives an additive, history-preserving edit plan. It proposes current comparison-result and bounded-stop wording only. It leaves status TO RESEARCH, priority 34, attributed proof status, historical family scores, formulas, and historical Q01 passages unchanged. It does not create another algorithm/discovery identity. It does not close ALG-028 or Q01.

Fresh controls check exact source byte identities, integer nearest-grid invariants, the algebraic sqrt(N) norm-transfer factor, and the declared scan/bit-size accounting. They are small diagnostic checks, not numerical certification of ALG-077, verification of external algorithms, or proof of nonexistence of a reduction. The mathematical comparison rests on the displayed contracts and deductions.

No external write was made. Publication, owner synchronization and independent acceptance are separate actions owned by the parent workflow.
