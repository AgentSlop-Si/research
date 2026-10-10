# Exact accuracy/model comparison of the recovered approximation sources

Date: 10 October 2026. Uploaded programs were neither executed nor imported. This is a static source comparison and mathematical scope analysis, not a new independent audit of every implementation.

## 1. Earlier all-level quantized stage-table construction

Source: canonical_sources/8512b7be7d104174__RESEARCH.md in fft_research_master_20261009/library. SHA256:

    8512b7be7d104174d737abd279fae61b0a9d3f49b8610376a01fb4096520bfcf

Original archive: fft_multilevel_quantized_research_2026-10-09.zip; original member fft_multilevel_quantized_tabulation/RESEARCH.md; Library file [private-id]. The manifest classifies it as text recovered, full text not reviewed in that inventory pass. No separate independent audit specifically of this stage-template theorem was located in the canonical text search; its own reported tests are not an external audit.

### Actual theorem target

For N=2^L and |x_j|≤1, produce all N approximations to the true normalized DFT F_N x/N, satisfying a deterministic maximum-coordinate absolute error at most fixed ε>0. This is not merely agreement with a rounded FFT circuit. The proof compares each rounded group to the exact normalized Fourier stages using their ℓ∞ operator norm at most one.

The parameters are

    R=ceil(8(L+1)/ε),  q=(2R+1)²,
    K=2^t,  K log2 q + log2 K ≤ cL,  0<c<1.

For fixed ε, state/output component precision is Θ(log log N), not constant. Twiddle generation uses O(log N) guarded bits, and the machine word has Θ(log N) bits. Then K=Θ(log N/log log N), t=Θ(log log N), and G=ceil(L/t) grouped passes suffice. Keys contain K log2 q≤c log2 N bits; every K-value table result is explicitly copied in Θ(K) operations. Preprocessing/storage is N^c polylog N=o(N), online time O(N log N/log log N), and final explicit output takes O(N).

The source gives a coarse exact-phase accumulated error (2G+1)/R, and a guarded phase version (4G+1)/R. Its fixed-point twiddle realization is described as an assumption/obligation rather than an implemented proof-certified routine: the prototype uses doubles, toy eager tables, or lazy miss computation. It must not be presented as a measured growing-table runtime implementation.

### Shrinking-accuracy boundary of this table family

Let p=Θ(log log N+log(1/ε_N)) denote the symbol bit width. The complete-table constraint gives K=O(log N/p). A growing gain requires K→∞, hence p=o(log N). If ε_N=N^(−α) for any fixed α>0, then p=Θ(log N), K=O(1), and this all-level complete-table route no longer gives o(N log N) via growing groups.

At fixed ε, its unnormalized DFT error is εN. For unitary normalization it is ε√N. These are absolute error scales, not relative ℓ2 error or relative error in individual coefficients.

### Phase preparation is a closable obligation, not a reason to change its error contract

An O(N) root-power table can in principle be built with b=Θ(log N+log R) fixed-point guard bits: approximate the master root to O(2^(−b)), generate its N powers by rounded recurrence, and choose b so the O(N·2^(−b)) accumulated phase error is O(1/R). Machin/Taylor rational evaluation supplies the initial constant in poly(log N) word operations at this precision. For fixed or polynomially shrinking ε, these values still occupy O(1) sufficiently wide Θ(log N)-bit words. This observation explains why root precision need not destroy the fixed-ε word bound. It is not an execution or independent certificate of the original program. It also does not remove the K=O(1) alphabet obstruction at polynomially shrinking ε.

## 2. Newly recovered three-table archive

Archive: FFT_NEW_THEORY_2026-10-10.zip; Library file [private-id]. Actual theorem SHA256, checked from archive bytes:

    f7c4f9ecf2e46d1e62657a1556031f03b1c122d4dfb28f7e7341c038d029fa7e

This theorem hash and the README hash are absent from canonical_sources.json. Byte-level novelty does not establish that its conclusion is new to the research history.

### Actual claim

For fixed ε∈(0,1), fixed a>0 and fixed c≥0, inputs have integer real/imaginary components bounded by N^c. Let

    L(x)=Σ_j (|Re x_j|+|Im x_j|).

The claim concerns the true unitary DFT U_N, with

    Pr[||ŷ−U_Nx||∞ ≤ ε L(x)/√N] ≥ 1−N^(−a).

It states expected O_(ε,a,c)(N) time, O(N) words, w=C(ε,a,c)ceil(log2(N+2)), constant-time arithmetic including multiplication/division, exact random words, and all preparation/output charged. This is a randomized approximation for every fixed input, not a statement about random input draws and not an exact transform.

Signed-atom sampling takes k=Θ_(ε,a)(log N) samples. A frequency block has B=Θ(log N) lanes; starting/slope phase descriptors have Θ(log log N) bits. Group size g=Θ(log N/log log N) gives G=Θ(log log N) groups. Group-average symbols have constant precision depending on fixed ε. The third table transposes lane chunks of width Θ(log N/log log N); assembling chunk keys costs O(G²), while lane extraction/output costs O(B). Since G²=o(B), each frequency block costs O(B). Complete tables have sublinear N^γ polylog N or polylog N construction cost.

A static mathematical reading found no immediate flaw in that aggregation argument. The source explicitly says its simulator uses lazy reference tables and does not implement the growing eager schedule. Its own full-word/overflow/physical executor obligations remain. This report did not execute its verifier or accept its source-authored test results as independently reproduced.

For polynomially shrinking ε=N^(−β), its sample count is already Ω(N^(2β)log N), and the group/table alphabets also change. The stated O(N) theorem therefore does not survive substituting shrinking accuracy.

## 3. Crucial history correction: the O(N) coarse theorem is already in the master corpus

Existing source:

    canonical_sources/09d7179e48373c60__WORDRAM_AUDIT.md
    SHA256 09d7179e48373c60aa00058d0c4dbd2c07221d81fba9f0077ca6f58bc12faf0d

It independently audits an existing eager guarded-packed-addition decoder and explicitly states that the fully charged coarse-accuracy O(N) theorem was already established in earlier synthesis. It checks the same integer-input, input-mass-normalized accuracy regime, including certified integer Machin/Taylor phasors, exact mass sampling, packing and output costs. It reports no substantive mathematical error while distinguishing the theorem from toy implementations and practical running time. That audit's recorded independent checks are source evidence here, not rerun results.

Thus the new three-table archive should be described as another explicit synthesis relative to the older v2 checkpoint, with a new transpose-table presentation. It is not the first coarse O(N) approximation result in the full master history. In fact, the existing guarded-addition route avoids the transpose through a different packed aggregation mechanism.

The old v2 source it targets is

    canonical_sources/a0a4c64dc57b2141__SPARSE_SURROGATE_WORDRAM_CHECKPOINT_v2.md
    SHA256 a0a4c64dc57b2141ff9d6f29847e02fc530d037c1b98e13694bec54550c9b0a7.

Do not transfer an audit of the guarded-addition implementation into a claimed independent audit of the new three-table code.

## 4. Why this matters for random binary inputs

For independent Bernoulli(1/2) inputs, L(x)≈N/2. The new theorem then permits unitary error Θ(ε√N) at fixed ε, while a typical non-DC coefficient has size O(1). The older theorem has the same scale up to a constant factor. Neither guarantees useful relative reconstruction of the random fine spectrum.

There is a simple control: compute the DC coefficient exactly and output zero at every other frequency. For each nonzero frequency, subtract the constant input mean; a real/imaginary Hoeffding bound and union bound imply that, with probability at least 1−δ over the random input,

    max_(k≠0) |(F_Nx)[k]| ≤ sqrt(N ln(4N/δ)).

So this O(N) input-scan/output algorithm has normalized error at most

    sqrt(ln(4N/δ)/N),

which tends to zero and eventually beats every fixed-ε normalized guarantee. This control is specific to the random input distribution; it does not replace the approximation theorems' worst-case-input guarantees. Those theorems can still detect macroscopic coherent Fourier structure, sparse mass, or small residuals after a useful baseline.

## 5. Relation to the exact restricted NTT result

The accompanying EXACT_RESTRICTED_NTT.md is qualitatively different: it has exact full finite-field outputs for every binary input, and uses finite-field Frobenius symmetry plus growing chunk-product tables. It incurs O(N log log N) word cost with N log N output bits. The approximation packages concern true complex Fourier outputs at a weak global error scale. Neither implication runs automatically from one result to the other.
