Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery details are omitted; mathematical source identity, assumptions, costs and limitations are preserved. Original source-report SHA-256: 68d29a3bc633935af283cb981a8015e6accee7a074f155c6913f009b6fb76bda.

# Independent CFGL mixed-carrier DAG review

Date: 2026-10-12 UTC.

## Verdict

**ACCEPT, scoped to the uniform all-size scalar construction and its explicitly expanded literal-radix cost.** The candidate computes every specified within-packet coefficient and every cross-conductor/cross-copy zero. Adjacent conductors genuinely meet in internal scalar registers. Character selection, coefficient preparation, and physical wrappers require only linear additional scalar work. The chosen two-Fourier Gauss implementation nevertheless costs **Theta(N log N)**. Its restricted architecture statement is valid; no unrestricted weighted-DAG or Fourier lower bound follows.

The `CFGL::weighted-DAG` **fast evaluator gate remains OPEN**. This review does not establish O(N log log N), a finite-precision or bit-complexity speedup, an optimized linear-storage evaluator, or novelty/priority. Existing structural and same-N reduction results should be retained.

No substantive change to the sealed candidate is required. One implementation-level ledger distinction is made explicit below: the report's principal block can use 3t arithmetic operations with reused scalings, while the literal verification function recomputes those scalings and performs 4t. Both give the claimed O(N) wrapper bound.

## 1. Immutable inputs and independence

Reviewed candidate archive:

- `CFGL_Uniform_Carrier_DAG_Cost_Obstruction_CANDIDATE_2026-10-12.zip`
- SHA-256: `67f7c83014e4b0a30968442734b3dde445da1dd01611e49a6917af429d9ae643`
- 531,792 bytes; 17 files including the manifest

All 16 manifest-listed files were checked after extraction. Every one of the five source bindings was checked both against the archived evidence and the extant original path. The original research manuscript has 20,033 bytes and SHA-256 `e0c76a5d8694bb15cf0ccc75182a09644a670ea5ace7fe135a71d575c1057cf8`. Its original and historical review programs were never executed or imported.

The review has two distinct empirical components:

1. A cold replay of the newly authored, sealed candidate checker, with maximum t=9. `EXACT_CONTROLS.json`, `DAG_N16.json`, and `DAG_N32.json` reproduced byte-for-byte. This is an independent replay, not an independent implementation.
2. A separately written exact cyclotomic interpreter of scalar DAG JSON. It imports no candidate evaluator or original program. Additional DAG JSON for N=2,4,8,64,128 was emitted using only the sealed fresh candidate generator, with a provenance receipt. The independent interpreter evaluates those graphs from their scalar operations. Its physical reconstruction uses explicit Haar basis signs and Ramanujan shell values rather than copying the candidate's recursive wrapper or prefix procedure.

All scripts are standard-library only. The full evidence is in `results/`, and the candidate extraction remains unmodified in `candidate/`.

## 2. Packet dimensions, boundaries, and root field

For N=2^t, conductor C contributes t-C+1 separate shell-copy labels, each of length m_C=2^(C-2). Consequently

    V = sum_(C=2)^t (t-C+1) 2^(C-2) = N-t-1.

For the band with top conductor h=t-2s, a full adjacent pair has B=4s+3 labels; a final singleton has B=2s+1. Its carrier length is M=2^(h-2)=N/(4*4^s), and R is the next power of two at least B. Within a full pair the input embeddings p=aM/m_C are exactly p=a or p=2a. The last singleton can only be conductor 2, with M=1. Every packet occurs once and none is truncated.

The bound B <= t(t-1)/2 <= 2^t for t>=2 ensures R<=N, so R divides N. Also 2M<=N. Thus the label root xi=omega^(N/R), carrier root theta=omega^(N/M), and doubled root eta=omega^(N/(2M)) are all supplied-root powers. No independent roots or root extraction are used. The root must be primitive, as required by the earlier accepted review; omega^N=1 alone is insufficient.

N=1 is the physical scalar identity and requires no root. N=2 has no detail packet and is entirely principal. N=4 has one C=2 scalar packet with raw value 2 omega_4, not a nontrivial Gauss core. The M=1 branch bypasses the quadratic identity. These cases are consistent with the code and exact physical controls.

Every coefficient lies in Q(omega). Scalar weights may depend on N, but all are prepared by charged operations from the supplied root and fixed rationals. Analytical conjugation of a known Gauss scalar is implemented by inverse root powers, never by conjugation of a data register. Linear identities therefore apply to arbitrary complex input scalars, not just the cyclotomic inputs used in finite checks.

## 3. All-size Gauss and terminal-transfer proofs

For even dyadic M, the phase eta^(-s^2) is M-periodic:

    eta^(-(s+M)^2+s^2) = eta^(-2Ms-M^2) = 1.

Completing the square and reindexing modulo M gives, for every integer x,

    sum_s eta^(-s^2+2xs) = eta^(x^2) G_M,
    G_M = sum_s eta^(-s^2).

In G_M times its conjugate, substitute s=r+d modulo M. The inner character sum over r is zero unless d=0, so the product is M. Hence G_M is nonzero and its reciprocal is the conjugate sum divided by M. Multiplying the completed-square identity by eta^(-b^2-p^2) proves the stated Fourier kernel theta^(bp). Both complete positive Fourier transforms inside that kernel are present in the emitted scalar DAG.

M=1 is excluded for a mathematical reason: the one-term sum is 1, whereas eta^(x^2) is -1 for odd x. An undoubled quadratic root also produces parity-zero sums. Both exclusions are detected independently.

For an input (lambda,a) and output (mu,b) in the same band, the path sum factors as

    [2^(j_mu-C_mu+1) zeta_mu^(1+2b)] zeta_lambda^(2a)
    * theta^(b p_lambda(a))
    * (1/R) sum_gamma xi^((r_lambda-r_mu) gamma).

All real labels are distinct residues modulo R, including different shell copies of the same conductor. Character orthogonality therefore supplies exactly delta_(lambda,mu). For lambda=mu, the carrier term is (zeta_C^4)^(ab), so the surviving entry is

    2^(j-C+1) zeta_C^((2a+1)(2b+1)).

Different bands are disconnected and thus have no paths. These cases establish every entry and every required zero for all t. No rank inference or numerical pattern is used. The permutation to output shell ell=t+C-j is a bijection on the copy labels of each conductor.

The independent interpreter also recorded nonzero influence from different conductors at the same internal label and core nodes for every tested N>=8. Thus the internal mixing claim is literal, even though the overall transfer is block diagonal.

## 4. Legal scalar realization and exact evaluation ledger

Each emitted operation is a scalar scaling, binary addition, or binary subtraction with strictly earlier scalar predecessors. A scaling has one weighted data edge; an add/subtract has two. Zero padding is a shared scalar zero input, not a vector operation. Fourier calls are recursively expanded into scalar butterflies; no transform is represented by a single edge or instruction.

Write A(n) for the literal radix-2 arithmetic-node count:

    A(1)=0,
    A(n)=2A(n/2)+(3/2)n,
    A(n)=(3/2)n log2(n).

A butterfly has one scaling and two add/subtract nodes. Multiplications by 1 and work on padded or ultimately unused coordinates are deliberately retained. For band g, the exact packet evaluation recurrence is

    C_g = 2 M_g A(R_g) + 2 R_g A(M_g)
          + 3 R_g M_g * 1_(M_g>=2) + 2 V_g.

This is the candidate's recurrence with the endpoint term and M=1 exception written exactly, rather than as O(V_g). Let

    Q = sum_g R_g M_g,
    Qplus = sum_(g:M_g>=2) R_g M_g,
    Hlabel = sum_g R_g M_g log2(R_g),
    Hcore = sum_g R_g M_g log2(M_g), H=Hlabel+Hcore.

The resulting exact packet counts are

    add/subtract nodes = 2H,
    scalar scaling nodes = H+3Qplus+2V,
    all arithmetic nodes = 3H+3Qplus+2V,
    weighted data edges = 5H+3Qplus+2V.

These formulas agree with independent counts of every inspected serialized operation. Weighted-edge count is a graph size, not an assertion that every edge requires both a separate multiplication and a separate addition. Either conventional bounded-fanin charge gives the same asymptotic conclusion.

## 5. Why label overhead is linear and the chosen core is not

Since R<=8s+6 and M=N/(4*4^s),

    Q <= (N/4) sum_(s>=0) (8s+6)/4^s = (26/9)N.

Using log2(8s+6)<=2s+3 gives

    Hlabel <= (N/4) sum_(s>=0) (8s+6)(2s+3)/4^s
           = (350/27)N.

Both constants and the treatment of the final singleton are correct. The two label transforms therefore cost O(N) scalar work despite their padded character groups.

For every partition into groups with R_g at least the number of labels and M_g at least their largest packet size,

    sum_g R_g M_g log2(M_g)
       >= sum_lambda m_lambda log2(m_lambda)
       = N(t-4)+2t+4.

The first inequality is simply a comparison of the specified expanded work counts: every label is assigned at least M_g log M_g >= m_lambda log m_lambda. For the candidate's adjacent bands, Hcore<=Q(t-2), so its literal schedule is Theta(Nt).

This assertion is **not a direct-sum circuit lower bound**. The encoded channel inputs are correlated, and many carrier outputs are not requested. Sharing across channels, exploiting those dependencies, pruning or algebraically replacing transform calls, or using a different Fourier evaluator can leave the charged architecture. The proof gives no lower bound after those changes. In particular, inserting and cancelling the label transforms is not ruled out by a universal theorem; it merely produces a different schedule from the literal one being counted. The candidate already states the appropriate restriction, and this review preserves it.

## 6. Cold preparation, generation, wrappers, writes, and memory

For N>=2, the preparation routine explicitly performs:

- N-2 multiplications for the full root table;
- one addition and one fixed-constant inversion to obtain 1/2, followed by t doublings and t halvings;
- for each distinct M>=2, M-1 additions and one scaling for the Gauss reciprocal, followed by M output-chirp scalings;
- K additional root/rational scalings, where K is the number of distinct referenced root descriptors with a nonunit rational factor. Only endpoint descriptors contribute, so K<=V.

Thus a sharper exact count for the stated preparation schedule is

    P = N + 2t + 2 sum_(distinct M>=2) M + K.

The carrier sizes decrease by factors of four, so their sum is less than N/3. This proves O(N) preparation and in particular the candidate's conservative bound P<=4N+3t+V+4. The cold checker verifies every referenced coefficient against its descriptor. Descriptors are not uncomputed transform values.

The full graph must also be emitted and traversed: its O(E+N) address operations and descriptor/result writes are charged separately. Quadratic exponents can be generated by finite differences, or by explicitly charged O(log N)-bit index arithmetic. Exact cyclotomic emulation in the tests is not claimed to have unit bit cost. The graph has O(N log N) scalar/word storage; the review accepts no linear-storage implementation merely from an implicit description.

Haar analysis has V pairs and costs 4V scalar operations in the half-sum/half-difference convention; synthesis costs 2V. To achieve the report's 3t principal work, first cache q_j=2^(j-1)c_j (t scalings), then build t prefix sums, then form t output differences using those same q_j. The literal `physical_wrapper_controls` function recomputes the second occurrence of each q_j and uses 4t instead. Therefore:

    complete physical scalar evaluation with reused q_j
      = 3H + 3Qplus + 8V + 3t;

    literal verification wrapper arithmetic
      = 3H + 3Qplus + 8V + 4t.

Add preparation P, graph-generation/address charges, grid initialization/scatter, input reads, V packet-output writes, shell permutation, and all N physical output writes. The last items are O(E+N), with no missing bins represented by a compressed output. Neither principal-block count changes the Theta(N log N) complete schedule.

The exact supplied-root model is essential. No input encoding, approximation guarantee, rounding analysis, or bounded coefficient-height argument is supplied. Accordingly the original numerical and bit-complexity gates remain unresolved.

## 7. Fresh exact controls

The independently written interpreter completed:

- Every packet entry for N=2,4,8,16,32,64,128, plus complete N16/N32 matrices with primitive-root powers 3 and 5: **20,057 entries**, including **17,362 cross-packet zeros**.
- All physical Fourier entries at those sizes and extra root choices: **24,404 entries**, plus the separate N=1 scalar boundary. No output coordinate was omitted.
- Scalar topological legality, valid endpoints, coefficient construction, operation counts, and actual mixed-conductor node support.
- **7,272** complete Gauss carrier-entry identities, norm/nonzero identities, the M=1 exclusion, and the undoubled parity-zero exclusion.
- Dimension, root-divisibility, and exact cost inequalities for every t from 1 through 256. These are controls; the general proofs are above.
- Five independently mutated scalar graphs: omitted input phase, omitted shell factor, omitted label normalization, wrong decoder sign, and a collapsed decoder label. Every mutation was detected. The collapsed-label example sends source (4,4,0) into target (5,5,0) with coefficient 2 omega_32 instead of zero.

The independent cold replay of the sealed candidate additionally reproduced **331,476** packet entries through N512, including **292,656** cross-packet zeros, and **21,845** physical entries through N128 including N1, along with all preparation and negative controls. Its three deterministic output artifacts are byte-identical to the sealed candidate's outputs.

## 8. Scope and remaining work

The uniform carrier/character scalar construction is accepted at its stated exact supplied-root scope. The fast CFGL evaluator remains open.

Accepted conclusion:

> Independent review accepts the uniform adjacent-conductor carrier/character scalar DAG and every terminal coefficient/zero in the exact supplied-root model. Label selection and coefficient preparation have O(N) overhead. The specified fully expanded two-transform Gauss core costs Theta(N log N), with a lower charge proved only for that literal independent-channel architecture. The fast CFGL weighted-DAG gate remains OPEN; no unrestricted lower bound, numerical/bit speedup, or priority claim follows.

All original structural acceptance, primitive-root guards, same-N O(N)-wrapper equivalence, precision limits, and broader open obligations remain in force.
