# Three-phase twiddle rewrite: a bounded cost comparison

10 October 2026. Read-only comparison against the accepted split-table executor. No new packed kernel or improved runtime is claimed.

## Verdict

The three-phase positive-rational representation does not, by itself, improve the accepted phase-separated packed executor. It moves phase variation into amplitude/selector variation. Complete response tabulation preserves the relevant phase-dependent table family; unpacking to do ordinary scalar arithmetic loses the packed work saving; a literal binary scale/add implementation spends Θ(B) rounds for B-bit coefficients.

Even an oracle that deletes all phase-dependent tables and their online work would leave the retained full-word universal Hadamard table and leading-bit helper. Thus this specific rewrite cannot improve the accepted preparation exponent while those parts of the architecture remain unchanged. This is a scoped comparison, not a lower bound against every packed-arithmetic algorithm, compressed table representation, table granularity, or FFT design.

## 1. Frozen source and parameter ledger

Accepted construction: `research_cycle_1453/packed_improvement/SPLIT_TABLE_CONSTRUCTION.md`, SHA-256 `be8de35159ed47f2a5d0bad71937d83bb7053ef83ae6ce358c0dfd80add78ded`.

Independent acceptance: `research_cycle_1453/packed_adversarial/SPLIT_TABLE_INDEPENDENT_REVIEW.md`, SHA-256 `7aa359016f6d51108c1c8c0dfdbc61b770d9865616b1cbae179b8475f569c89d`.

Use that construction's notation, where p is a precision parameter, not the prime from the exact field theorem:

    N=2^v,
    p=t+10+ceil(log₂(v+1)),        u=2^(−p),
    k=ceil(log₂(2v+p+6)),         b=2(p+k+1),
    g=p+10,                      Q=2^g,
    R=2^b,                       S=R^P,       d=log₂P.

The low-precision branch retains b≤v/64 and the largest power of two P with 16bP≤v. In particular P≥4 and P>v/(32b). Each complex state occupies b bits; P states form one persistent packed word.

The accepted complete response arrays have

    E_split = S² + (Q−1+d)S + QR + R²

one-word entries. Here S² is the universal packed Hadamard table HP; (Q−1)S is the unary phase-pattern catalogue; dS covers small stages; QR and R² are explicitly built scalar helpers. Certified phase-coefficient preparation costs Q·poly(v+p), separately. The leading-bit chunk table has 2^floor(v/8) entries. Online work is O(N+Nv/P)=O(Nb).

The prepared dyadic phase coefficient c_q approximates its exact grid phase with error below

    δ=u/128=8/Q.

The target grid has Q phases, although the catalogue's constant-pattern subfamily already uses the half-grid q=0,…,Q/2−1. All phase addresses and lane patterns are already charged in the accepted executor.

## 2. What a three-phase rewrite actually supplies

The approximation geometry works for the power-of-two phase grid without invoking the prime-field theorem. For Q≥8, put a=floor((Q+1)/3) and use grid phases at exponents 0,a,Q−a. Their circular gap ratios lie in [1/4,3/8], so each denominator sine is at least 1/sqrt(2). Every unit phase can therefore be written using two adjacent palette rays with nonnegative real coefficients at most sqrt(2).

Approximate those real coefficients by bounded dyadics to O(δ), and approximate the three common rays tightly enough that coefficient and ray errors together stay below δ. Since the coefficient sum is bounded, B=p+O(1) fractional bits suffice. The retained dyadic amplitudes may be bounded by 2. This is a new way to prepare an approximate coefficient; it is not bitwise equality to the original certified c_q unless that is established separately.

The representation of c_q z is schematically

    a_(q,1) ρ_(j(q,1)) z + a_(q,2) ρ_(j(q,2)) z.

There are three common rotations ρ_j, but the amplitude pair and selected adjacent sector still depend on q. Applying a fixed rotation remains a multiplication or a paid lookup. Calling it a fixed pretransform does not make it free, and preparing it once for one input does not prepare it for every later butterfly input.

Cold coefficient preparation still requires the q-dependent amplitudes. A direct certified sine-ratio construction costs Q·poly(v+p), just as the accepted coefficient-preparation envelope already does. No O(1)-sized total constant table follows from having three distinct phase labels.

## 3. Quantitative residual variation

Suppose two indices q,q′ in the half-grid use the identical amplitude/selector tuple, hence the same approximating complex coefficient c, and both have error at most δ. Let h=|q−q′|≤Q/2. Then

    2 sin(πh/Q) = |ω_q−ω_q′| ≤ 2δ.

For 0≤h≤Q/2, sine concavity gives 2sin(πh/Q)≥4h/Q. Consequently

    h ≤ Qδ/2 = 4.

One tuple can cover at most five half-grid indices, so at least ceil(Q/10) distinct tuples are required. This is an elementary separated-points argument, independent of the exact cyclotomic-field obstruction.

If each of at most two nonnegative coefficients belongs to the B-bit dyadic grid in [0,2], there are at most

    3(2^(B+1)+1)²

coefficient/adjacent-sector tuples. Thus that representation needs

    3(2^(B+1)+1)² ≥ Q/10,
    B ≥ g/2−O(1) = Ω(p).

The constructive B=p+O(1) choice is therefore of the right asymptotic bit order. More importantly, three phase labels do not remove a growing amplitude-description alphabet.

This is **not** an Ω(QS) space lower bound for an arithmetic evaluator: distinct coefficient descriptions may be generated, shared, compressed, or applied by arithmetic. It is also not a proof that Q independent constants must be stored. It prevents only the inference that a three-phase palette itself makes the remaining coefficient dependence constant-sized.

## 4. Three literal implementation choices

### 4.1 Fuse the rewrite into complete unary response tables

Define the new scalar map by carrying out the rewritten dyadic coefficient product and the chosen quantization, then build a complete packed table for each existing catalogue pattern. Each map still consumes one of S packed input states and returns one packed state. This produces the same (Q−1)S response-table count, up to any separately proved deduplication. Additional fixed-rotation tables are not a reduction in this count.

If fixed rotations and amplitude scalings are tabulated as separate stages, their scalar helpers, amplitude-pattern packed tables, intermediate codes, and extra rounding must all be charged. No smaller complete family or O(1) online arithmetic kernel is established merely by the algebraic decomposition. The existing scalar/helper construction already pays for q-dependent unary multiplication.

### 4.2 Unpack and perform scalar dyadic scale/add

Decoding and processing each of P lanes takes Ω(P) literal lane operations per packed pair. Each scalar product fits a fixed number of the allowed Θ(v)-bit words, but that does not make P such products one operation. The resulting schedule has O(Nv) scalar work rather than the accepted O(Nv/P)=O(Nb) packed work.

The decoded common-lattice numerators have O(v+p) bits. Placing P such general intermediates side by side would require O(P(v+p)) bits, not one Θ(v)-bit model word when P grows. This identifies the failure of the literal full-decoding approach. It is not a proof that every other representation or broadword multiplication technique must unpack.

### 4.3 Use coefficient bit planes and repeated dyadic scale/add

For a coefficient a=n2^(−B), the exact identity

    a z = Σ_(ell: bit_ell(n)=1) 2^(ell−B) z

allows a literal bit-serial implementation. Even granting an ideal constant-time packed masked scale/add per bit, the fixed B-bit schedule executes Θ(B) rounds. With B=Θ(p), its online work is O(BNv/P)=O(Nbp), versus the accepted O(Nb). This comparison grants perfect accuracy; an actual floating-state implementation would additionally need an all-input analysis of every new quantization, underflow, clipping, and exponent change.

One could store coefficient masks for each pattern and bit using O(QB) words, rather than an S-response array per pattern. Those masks are another paid q-dependent table; on-demand mask generation from scalar amplitudes requires its own lane-access accounting. Such a trade can reduce subordinate response storage, but this literal schedule loses a factor Θ(B) online. A different constant-time packed arithmetic kernel is a separate research obligation, not a consequence of the three-phase lemma.

## 5. Why even free phase removal leaves the current dominant preparation unchanged

From b=2(p+k+1) and P≥4,

    g≤b/2+10,
    Q/S = 2^(g−bP) ≤ 2^(10−7b/2).

The tighter expression 2^(2−7p−8k) follows by substituting b explicitly. Thus the accepted (Q−1)S phase-pattern term is much smaller than S² in this branch.

Deleting both Q-dependent response/helper terms removes

    D=(Q−1)S+QR,
    D/E_split < 2Q/S ≤ 2^(11−7b/2).

For the four displayed accepted thresholds, the actual exponents log₂(Q/S) are −285, −327, −383, and −657, respectively. The table-only saving is therefore tiny relative to HP in that particular retained layout, despite Q itself being very large.

Keeping HP already preserves its S² cost. Independently, the unchanged leading-bit chunk table costs Θ(2^floor(v/8))=Θ(N^(1/8)) actual writes. Therefore deleting every Q-dependent table and all their preparation cannot improve the accepted O(N^(1/8)) backend-preparation exponent **while this helper and the rest of the architecture remain fixed**. The online operation count can change by a constant, but the O(Nb) transform-time order is unchanged.

This conclusion has a narrow scope. Changing the HP block granularity or replacing the leading-bit helper is outside the phase rewrite. For example, two P/2-lane Hadamard lookups can replace the full-P HP lookup and alter its table count at constant overhead. That separate table-granularity proposal is not ruled out here and is not being silently credited to amplitude decomposition. Other work is reviewing such changes independently.

## 6. Accuracy and model boundaries

The accepted split executor has a proved all-input recurrence, bounded-build fallback, common output lattice, and explicit treatment of malformed codes and clipping. The proposed algebraic rewrite changes a response map unless it is collapsed back into exactly the same certified c_q and quantizer. Extra quantized multiplications and sums are generally not bitwise interchangeable with one combined multiplication.

No revised state width b, larger packing P, lower guard threshold, or new all-input error theorem is obtained in this comparison. The exact field theorem and its three-phase rational approximation give no permission to omit q-dependent amplitude bits, to assume free vector multiplication, or to transfer growing-word claims to fixed 64/128-bit hardware.

The established packed-FFT/table context includes [Chan, Jin, Vassilevska Williams and Xu, Appendix B](https://arxiv.org/html/2310.13174v2), also cited in the accepted split-table review. That primary source was revisited for context; the present ledger makes no priority claim about packed tabulation, ordinary phase separation, or bit-serial multiplication.

## 7. Fresh controls, bounded outcome, and stopping point

`fresh_ledger_controls.py` is newly authored and uses only the Python standard library. It reads source Markdown only as bytes for hash checks; no source program is imported or executed. It checks the four threshold parameter sets, complete response counts, the Q/S and maximum deletion-fraction bounds, bounded-dyadic tuple capacity, 28 power-of-two near120° gap configurations, and 5,140 exact rational bit-serial multiplication identities. The source hashes pin the accepted split construction and both amplitude-field artifacts.

These are ledger and arithmetic-identity controls, not a new packed executor or a benchmark. The initial fresh-control run had a relative-path error while locating a Markdown hash input; the path was corrected and the complete run passes. No mathematical assertion was weakened.

Outcome: no improvement established from the specified three-phase rewrite. The missing ingredient for a different claim would be a fully charged constant-time packed amplitude kernel or an independently verified architectural change to the dominant tables/helpers. Neither is supplied by this rewrite, and this bounded lane stops here rather than adding unproved computational primitives.
