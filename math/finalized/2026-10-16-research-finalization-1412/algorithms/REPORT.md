# Two bounded algorithm gates: finite recurrence recognition and exact membership

Date: 16 October 2026. Baseline: `609d5c2189d64350bcbed447eead7e2c33dd3a50` in AgentSlop-Si/research.

## Decision summary

- **ALG-064: scoped mathematical completion.** A capped finite-sequence synthesizer plus the existing boundary-rational idea gives a complete raw-input recognizer and all-frequency evaluator for every recurrence span at most a supplied cap d. The accepted branch costs O(N(d+1)) additions/multiplications and at most d+1 field inversions, plus explicitly separated field/root acquisition and representation costs. A dyadic ordinary-FFT fallback gives an exact all-input algorithm, with worst-case O(N(d+1)+N log N), not an improved arbitrary-input FFT.
- **ALG-053: scoped deterministic-projection obstruction and a paid deterministic completion.** When a verifier sees the remaining residual only through linear projections across K frequency channels, exact deterministic certification needs probes spanning all K channels if M>2d. Adaptive projections do not evade the result without extra raw-data access. Full materialization and verification do give a deterministic exact algorithm, at O(N log K+dN+N) field work in the compatible dyadic-column model. This restores a transform cost that the promised/randomized result avoided; it is not a speed improvement.
- **Named classical comparison is complete:** finite-sequence recurrence synthesis is a direct classical match. Neither record receives a novelty, priority, whole-parent, production, bit-complexity or numerical-stability promotion. Archive the completed narrow gates against redispatch, while keeping both existing parents TO RESEARCH.

No uploaded program or prior checker was run or imported. `checks.py` is freshly authored. The old audits are read-only evidence. ALG-063 was inspected only to avoid repeating its already complete all-parameter sparse-difference construction; it receives no new completion credit.

## 1. Source binding and what was already complete

The two exact GitHub files at the baseline were retrieved and compared with available local evidence. ALG-064 is byte-identical to its content-addressed local audit. The published ALG-053 body replaces three private provenance identifiers with redaction markers; its mathematical text is unchanged, but its current body hash differs from the original hash retained in its filename. The existing immutable repository URLs are the authoritative evidence; historical source bodies are not duplicated in this packet. Exact inspected current-body hashes are recorded in `SOURCE_MANIFEST.json`.

ALG-064's [pinned Phase23 audit](https://github.com/AgentSlop-Si/research/blob/609d5c2189d64350bcbed447eead7e2c33dd3a50/math/archive/objects/c0/c074b19dd40f6a50a5a4a3b91b0e447824f47e90206032d4c88dc8673a723817__13_PHASE23_AUDIT.md), Sections 6–7, already proves a complete order-two raw-input recognizer, a root-free evaluator, and the O(Nr) evaluator when a degree-r filter is supplied. It explicitly leaves discovery charged and does not implement growing r. The work below supplies capped discovery and its exact interface; it does not claim the already accepted order-two or supplied-filter work as new.

ALG-053's [pinned learned-rational review](https://github.com/AgentSlop-Si/research/blob/609d5c2189d64350bcbed447eead7e2c33dd3a50/math/archive/objects/1f/1f9dd1faecb9925200df1ce5b7163f3edccf6734d92a71155d610e003ff4b336__1f9dd1faecb9925200df1ce5b7163f3edccf6734d92a71155d610e003ff4b336__SOURCE_REVIEW.md), “Learned recurrence and rational synthesis” and “Membership and capacity,” already proves promised-family synthesis and the exact q^(-rank residual) error per independent uniform field probe. It rejects deterministic membership claims from randomized checks. The added result below is a quantified deterministic span requirement under a specified interface, together with a full-cost deterministic alternative.

### Primary comparison (Massey, 1969)

Massey was already listed in these records' comparison sources. The completion here is the explicit hypothesis/interface/cost mapping, not discovery of that citation.

[James L. Massey, *Shift-Register Synthesis and BCH Decoding*, IEEE Transactions on Information Theory 15(1), 122–127](https://crypto.stanford.edu/~mironov/cs359/massey.pdf), DOI 10.1109/TIT.1969.1054260, was read through the six-page PDF's extracted text. The screenshot request returned a reference without an image available for visual inspection, so no visual-page verification is claimed. Section II, equation (2), permits any field and an untapped final register. Section III, Theorem 2 and its algorithm, gives shortest-register synthesis for each finite prefix. Theorem 3 and its corollary identify the 2L-sample uniqueness threshold under the recurrence promise. These match the finite-sequence recurrence convention used here and in ALG-053/064. They do not supply the Fourier roots, column spectra, complete negative-instance verification, exceptional-frequency evaluator, floating-point guarantees, or raw-input speedup. The classical synthesis ingredient therefore has a direct match; the full Fourier interface requires the paid work below. No broad historical-priority clearance follows.

## 2. ALG-064: exact cap contract

### 2.1 Domain and output

Let F be a field, N>=1, x=(x_0,...,x_(N-1)) in F^N, and 0<=d<N. Assume a supplied element omega of exact order N. The target is the unnormalized vector

    X_k = sum_(j=0)^(N-1) x_j omega^(kj),  0<=k<N.

An admissible recurrence is a **pair** (L,C), with 0<=L<=d and

    C(T)=1+c_1 T+...+c_L T^L,
    x_t + sum_(i=1)^L c_i x_(t-i) = 0,  L<=t<N.

Trailing coefficients can vanish: L need not equal deg C. For example, (1,0,0,...) has minimal register length one with C=1. Reducing the declared length to deg C would incorrectly discard its initial impulse. L=0 is permitted only for the all-zero vector.

The recognizer must accept exactly when such a pair exists. Acceptance returns the pair and all N target outputs. Rejection means only that this cap fails. The optional dyadic fallback still returns the exact transform.

“Root-free” here means no characteristic-polynomial factorization, algebraic node extraction, data-dependent square root, or discrete logarithm. The transform root omega is still an explicit input premise.

### 2.2 Capped synthesis and correctness

Use the finite-prefix discrepancy update with connection polynomial C, prior connection polynomial B, current minimal length L, shift s, and inverse of the previous nonzero discrepancy b. Initially C=B=1, L=0, s=1, b=1. At sample t, compute

    delta = x_t + sum_(i=1)^L c_i x_(t-i).

For zero delta, increment s. Otherwise the next minimal length is L'=max(L,t+1-L). If L'>d, reject before allocating a longer polynomial. If L'<=d, update

    C <- C - delta b^(-1) T^s B.

When 2L<=t, retain the old C as B, set L=t+1-L, b=delta and s=1; otherwise increment s. Keep zero padding through the declared length.

The finite-prefix minimality invariant establishes soundness and completeness. Minimal length is nondecreasing because any recurrence generating a longer prefix generates every shorter prefix. Thus an early cap rejection can never later become an acceptance. On acceptance, all N samples have participated. A late impulse cannot slip through a prefix-only test.

Every step takes O(d+1) scalar arithmetic and O(d+1) coefficient copying/indexing. The inverse b^(-1) is cached and changes only when L strictly increases. Hence there are at most d inversions, not N inversions. A discrepancy causing cap rejection requires no new inverse. The working recurrence state is O(d) field words; preserving x for output evaluation costs N words unless the caller retains a rereadable input.

### 2.3 Boundary-polynomial evaluation

For an accepted pair, write X(T)=sum x_j T^j. Define, for 0<=j<L,

    P_j = sum_(i=0)^j c_i x_(j-i),
    B_j = sum_(i=j+1)^L c_i x_(N+j-i),  with c_0=1.

All middle coefficients vanish by the verified recurrence, so exact coefficient multiplication proves

    C(T) X(T) = P(T) + T^N B(T).

No asymptotic or convergence interpretation is needed. At t=omega^k, t^N=1 and

    C(t) X(t) = A(t),  A=P+B.

Compute C(t), A(t) by Horner's rule on the complete root orbit. Batch-invert only the nonzero C(t), using one field inversion and O(N) multiplications. Then output A(t)/C(t). At every zero of C, evaluate the original X(t) directly by Horner's rule. Because C(0)=1, C is not the zero polynomial and has at most deg C<=L exceptional nodes. This handles repeated roots, nonsplit polynomials, zero characteristic roots, and all genuine resonances. Repeated roots do not create more distinct exceptional frequencies. For L=0 the formula simply returns all zeros.

The field need not split C. Its transform-root orbit is distinct. A plain running-power scan checks omega^N=1 and no earlier return to 1 in O(N) field operations and comparisons, without factoring N. It does not construct a field or discover omega.

### 2.4 Full ledger and fallback

After the stated field is available, the following charges are cumulative:

| Stage | Adds/multiplies and control | Inversions | Storage |
|---|---:|---:|---:|
| Read/reduce x and verify root orbit | O(N), plus actual input encoding/reduction | 0 | O(N) |
| Complete capped synthesis | O(N(d+1)) | <=d | O(d) |
| Prepare P and B | O(L^2) | 0 | O(L) |
| Evaluate C and A at all roots | O(N(L+1)) | 0 | O(N) |
| Regular batch inversion and division | O(N) | <=1 | O(N) |
| Exceptional evaluations | O(N L) | 0 | O(1) beyond input/output |
| Write all outputs | N writes | 0 | N output words |

Since L<=d<N, L^2<=Nd. Total: O(N(d+1)) additions/multiplications, O(N(d+1)) word/control work, at most d+1 field inversions, and O(N+d) field/index words. There is no free synthesis, denominator preparation, singular bin or output tape.

For dyadic N, rejection invokes an ordinary exact radix-2 FFT with a paid running-root table, permutation, butterflies, and outputs. Worst-case work is O(N(d+1)+N log N). Choosing d<=floor(log2 N) keeps this O(N log N); it does not improve that worst case. Accepted inputs of fixed bounded span use O(N) field work; growing d is explicitly charged. `adaptive_dft` in the checker is a small fresh implementation of this complete dyadic contract, not production qualification of any historical dispatcher.

Over F_p with known prime p, B=ceil(log2 p), charge each scalar multiplication/reduction at its B-bit cost and each of at most d+1 inversions at I(B). A useful form is O(N(d+1) M_mod(B)+(d+1) I(B)), plus actual input encoding, N B output bits, index/control work, and field/root selection and certification. The code assumes primality; it is not a primality prover. Exact order validation is included. Arbitrarily oversized input integers require their actual reading and reduction costs. Over C, the algebra is exact but no coefficient-conditioning, rounding, stability or algebraic-number bit theorem is claimed. Real-residual normalization/parity conversion is an additional O(N) interface only when its constants and conventions are supplied and paid.

## 3. ALG-053: the deterministic projection boundary

### 3.1 Fixed interface

Let N=KM, with K independent frequency channels and M time positions per channel. The column Fourier transform is invertible over F, with its compatible root supplied. Let 1<=d and **M>2d**. Fix an admitted training prefix of length 2d in every frequency channel, and fix the fitted recurrences C_l with constant coefficient one and lengths at most d. A genuine recurrence continuation supplies a zero-residual reference input.

For t>=2d, let

    E_(t,l) = f_(t,l) + sum_(i=1)^d c_(i,l) f_(t-i,l),

where coefficients are zero-padded. A probe v in F^K returns the entire vector E v across the untrained time positions. The verifier may choose each next v from the fixed training data, fixed fitted coefficients and earlier probe responses. It receives no other residual-dependent information or raw-input inspection affecting its choice or decision. This last restriction is essential.

### 3.2 Surjectivity lemma

For each fixed channel, the map from its untrained tail f_(2d,...,M-1) to E_(2d,...,M-1) is triangular with diagonal entries one. Given any residual sequence, recover the tail sequentially from

    f_(t,l)=E_(t,l)-sum_i c_(i,l) f_(t-i,l).

Thus the residual matrix is arbitrary once the prefix and coefficients are fixed. This is an algebraic fact, not a probability statement. Every resulting spectral column array corresponds to raw data by invertibility of the column transform.

### 3.3 Exact span theorem (including adaptivity)

Suppose a deterministic verifier accepts the valid reference continuation. Follow its all-zero transcript and write its selected probes as v_1,...,v_R. If their span has dimension less than K, choose a nonzero row vector w annihilating every v_j. Perturb only the final time spectrum by w:

    f'_(M-1,l)=f_(M-1,l)+w_l.

The training prefix remains unchanged because M>2d; all earlier residuals are unchanged; the last residual becomes w because the recurrence's coefficient on the current value is one. Hence E' v_j=0 for every selected probe. Inductively, the adaptive verifier observes the identical transcript, chooses the same probes, and accepts this invalid continuation. The full Fourier output also changes because the complete transform is invertible.

Therefore an exact deterministic verifier in this interface needs the zero-transcript probes to span F^K and consequently R>=K. If K=1 this requires at least one probe; if M=2d there is no untrained tail and the theorem does not apply. The result excludes no algorithm that inspects extra raw information, uses a different certificate, or chooses projections from such extra information. It is not an arithmetic lower bound or a general lower bound for deterministic recurrence checking.

The source's uniform random probe has a different quantifier: for a fixed nonzero residual its miss probability is |F|^(-rank E); independent repetitions multiply this. Replacing those independent draws with a short fixed deterministic list cannot inherit exact soundness. This probability statement is retained from the pinned audit, not newly counted as a discovery.

### 3.4 Fully paid deterministic alternative

There is no difficulty obtaining exactness by paying for the missing data. Materialize all M length-K column spectra, then synthesize and/or verify every channel recurrence on all M entries. For the accepted-family bound assume dyadic K and a supplied primitive Nth root Omega. With the positive-exponent convention, lay out x_(uM+t), set omega_K=Omega^M and

    f_(t,l)=sum_(u=0)^(K-1) x_(uM+t) omega_K^(lu).
    X_(l+jK)=sum_(t=0)^(M-1) f_(t,l) z^t,
    z=Omega^(l+jK),  z^M=omega_K^l.

The source's negative convention is obtained by replacing Omega with its inverse. Output nodes in one channel are distinct. Root powers and twiddles are prepared in O(N) after acquisition. The following accepted-family costs allow any M, while the ordinary fallback and total O(N log N) bound additionally require dyadic M:

1. Input reads, layout and common root preparation: O(N+K), with root acquisition separate.
2. M exact K-point transforms: O(M K log K)=O(N log K) field work, O(N) storage.
3. Capped synthesis or verification on K streams: O(dN+N), with at most dK discovery inversions when synthesis is included. Merely checking already fitted coefficients uses no inversions.
4. Boundary polynomials and all output-node evaluations: at the M output nodes for channel l, z^M is its known common phase gamma_l, so evaluate (P_l+gamma_l B_l)/C_l with direct Horner at genuine zeros. The cost is O(K d^2+dN+N)=O(dN+N) because d<=M. Genuine exceptional nodes contribute at most dM per channel. Nonzero denominators may be batch-inverted globally at one additional inversion with O(N) temporary words.
5. Rejecting channels, **assuming M also dyadic**: an ordinary M-point fallback in each channel costs at most O(N log M), with twiddles prepared and charged in the standard Cooley–Tukey layout. If the intended deliverable is membership only, no transform fallback is needed after rejection. For other M, supply and charge a compatible backend rather than assuming an O(M log M) field algorithm from an Nth root alone.

The exact accepted-family deterministic evaluation costs O(N log K+dN+N), plus inversions and acquisition/encoding. When K and M are both dyadic, a total all-input Fourier algorithm costs O(N log K+dN+N log M+N)=O(N log N+dN+N). At M=Theta(log N) and fixed d, log K remains Theta(log N): the deterministic baseline does not retain the promised-input O(N) benefit. The span theorem itself does not prove that every possible deterministic algorithm must pay this time; it establishes only the specified projection-interface obstruction.

## 4. Controls and reproducibility

Run `python checks.py` in this directory. The program uses only Python's standard library, contains no imports of project code, and performs no network access. It writes `CHECK_RESULTS.json`.

Observed PASS:

- 617 exhaustive finite sequences over F_2 and F_3, with independent brute-force minimum-span oracle;
- 3,179 capped acceptance/rejection decisions, including untapped final registers and late impulses;
- 655 exact accepted-vector DFT comparisons at dyadic N=4 through 64 over F_17, F_97 and F_193;
- 326 actual exceptional-frequency evaluations across those controls;
- 77 complete adaptive-vector comparisons, including 67 ordinary FFT fallbacks;
- 729 exhaustive two-probe matrices over F_3 at K=3, each with an explicit nonzero invisible residual;
- 50 exact arbitrary-tail residual reconstructions and four invalid-root rejections;
- 16 complete channel-coset evaluations reconstructed from raw inputs, including 25 singular nodes, checking the actual P+gamma B formula against a full direct DFT.

These counts describe finite checks, not proof by testing. The all-size proofs and cost counts are above. The direct DFT and brute-force recurrence fitter are test oracles, never called by the fast recurrence branch. No submitted timing, old acceptance log, source execution, machine-speed result, production wiring, or numerical claim is recertified.

## 5. Proposed record disposition

**ALG-064:** mark the named finite-sequence synthesis comparison and capped-span exact arithmetic constructor complete. Keep the parent TO RESEARCH, its priority and proof/novelty classifications unchanged. Any next dispatch must specify a distinct certified numerical representation, bit-cost improvement, historical source implementation correction/integration, or model-matched broader comparison. Do not rerun the already accepted order-two gate or claim arbitrary-input speedup from low-span behavior.

**ALG-053:** mark the fixed-interface deterministic projection question resolved negatively for probe spans below K, and the full-cost deterministic alternative established. Keep the parent TO RESEARCH, priority and proof/novelty unchanged. A new fast deterministic gate must name a different raw-input/certificate interface and charge its access. No automatic continuation or generic archive of the entire research family is recommended.

These are two bounded finalizations, not two globally closed research records. No external files, tables, statuses or repository branches were changed by this worker.
