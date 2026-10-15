# Independent review of the 22:57 routed/tensor/recurrence source update

Audit: 9 October 2026 UTC. The source documents are dated 10 October. No uploaded program, verifier, test, or nested source module was executed or imported. New controls are independently authored in independent_checks.py.

## Executive verdict

The three mathematical directions are useful and their principal scoped proofs survive review:

1. Recursive Fourier-mass contraction is a correct **conditional recurrence theorem**, with a concrete but unproved paired-Green/banked factorization conjecture. It supplies no contracting Fourier factors or uniform generator.
2. Hero17 Phase6 proves exact four-leg cut ranks and endpoint-local sparse-core rigidity. It explains why local Fourier basis conversion remains charged. It gives no faster all-input circuit.
3. Hero0 Phase9 supplies exact forced-recurrence identities and faster paths for promised sparse-innovation families. Its arbitrary-input identity does not remove the cost of obtaining arbitrary residual spectra. Its randomized membership check is not a deterministic exact certificate on unpromised inputs.

The main implementation qualification is Hero0's incomplete printed counter: a root inversion in ntt_inverse is uncounted, and output writes/general indexing are not represented by the inherited Costs total. This does not invalidate its promised-family asymptotic estimates, but the quoted finite-size totals are not a complete charged-work measurement.

## 1. Provenance, integrity, and review coverage

The original review's source-identity record lists filenames, byte counts and SHA-256 hashes. The following archive filenames describe that historical review context; this compact publication does not include those original archives:

- fft_hero17_phase6_tensor_cut_rigidity_2026-10-10.zip.
- fft_hero0_phase9_dense_cycle_2026-10-10.zip.
- THEORY.md.
- fft_mass_contraction_theory_2026-10-10.zip, the separately located complete supporting bundle.

The mass bundle's THEORY.md is byte-identical to the standalone upload. Its README, SOURCE_LEDGER and verifier were read as data. There is no longer a missing-support-file issue.

All 39 entries in the supplied integrity manifests verify. Hero0's embedded prior_phase8_bundle.zip is byte-identical to the previously reviewed 164,496-byte Phase8 archive, SHA-256 b583a480cee796edecc4be6e07881c91686a08b0dad66e1c53f1e460b4408fd8. Its two inherited source modules are also byte-identical to their prior copies. Thus those dependencies are inherited material rather than a new implementation. Copies used for exact comparison are included under inherited_reference/.

Every new top-level mathematical report, README, and recovery/source-ledger document in the three packets was read. Existing logs and test totals were inspected as source reports, not adopted as independently rerun evidence. The older nested Phase8 packet was identified by byte equality and the earlier review rather than re-executed.

## 2. Recursive Fourier-mass contraction

### Conditional recurrence approved

For N=2^k, assume an exact uniform procedure whose child exponents are at most ceil(k/2), total child length is at most rho N, and all nonrecursive work is O(N). The maximum normalized cost on exponent shells k<=2^h obeys

    A_h <= max(A_(h-1), rho A_(h-1)+C).

This gives the stated O(N), O(N log log N), and O(N (log N)^(log_2 rho)) bounds for rho<1, rho=1, and 1<rho<2, respectively. At rho=2 it returns O(N log N). The harmonic factor 2(1-1/h) gives O(N log N/log log N) by the displayed telescoping identity.

A minor bookkeeping clarification: length-one children have exponent zero, whereas the printed envelope starts at exponent one. Include k=0 in the base envelope, or charge these constant-cost calls into O(N) overhead using their counted recursive mass. This does not change any bound. Any larger fixed base range can likewise be included in the initial envelope.

The memory statement is appropriately conditional on O(N) local live workspace and a depth-first schedule. Counting few parameters alone would not prove the storage claim. Supporting every dyadic exponent, rather than only N=2^(2^h), correctly avoids a quadratic-gap padding shortcut.

### Missing construction remains explicit

GFC-4 asks for four paired, independently routed cyclic-Green layers around a partially active smaller-Fourier bank, with identity bypasses on inactive blocks. It requires exact equality at every dyadic size and an O(N) uniform parameter generator. Neither the document nor its supporting verifier supplies such factors. The verifier exercises ordinary two-bank transforms, intentionally invalid bank deletion, generic Green solves, and recurrence arithmetic. None is a contracting factorization.

With every bank block active, the recursive mass is N and the conditional bound is O(N log log N). A fixed smaller active fraction would give O(N). Those implications are correct, but remain implications of the unproved identity. Generic inverse density and passage through existing architecture gates are not positive evidence of it.

### Bank-aware inverse gates approved

The row-sparse rank lemma is sound: select r=floor(N/(d+1)) consecutive Fourier frequencies, remove at most rd columns touched by a d-row-sparse comparison matrix, and retain an r-by-r Vandermonde minor on untouched columns. The same argument survives monomial endpoints and applies to F or F^-1.

Inverting a factorization with one block bank gives a row-support upper bound m times the product of surrounding inverse row degrees. Dense F^-1 therefore forces this product to be at least N. The sparse-plus-rank-defect version follows by telescoping the inverse product, with one rank-r_i error in each summand. No invertibility of the sparse baselines is needed. These are correct extensions of inherited sparse-inverse arguments, not unrestricted Fourier lower bounds.

### Cyclic Green solver and exact cost

The implemented recurrence is

    z[c_t]=u[c_t]+a[c_t] z[c_(t+1)].

With that row/dependency convention, the prefix numerator and denominator 1-product(a) are correct. Individual zero weights are allowed; no weight is divided by. Product(a)=1 is the singular branch and must be rejected. The phrase “P connects c_t to c_(t+1)” should be made explicit as (Pz)[c_t]=z[c_(t+1)]. If instead P e_(c_t)=e_(c_(t+1)) were intended, the displayed recurrence would have the opposite direction.

The supplied kernel ledger is consistent with its code: N setup multiplications, one subtraction and one inversion; then 4N multiplications and 2N-1 additions for an application with diagonal endpoints. The dot accumulator starts at zero, which accounts for its N additions rather than N-1. Input indexing, permutation validation, storage and output remain additional O(N) work. This is an arithmetic/index model, not a numerical-stability or bit-complexity theorem.

The all-length chirp reduction is correct only with the additional roots explicitly available and charged, as the document itself states. A field containing an Nth root does not automatically supply the padded power-of-two root or a suitable square root.

## 3. Hero17 Phase6 tensor-cut rigidity

### Exact ranks and scope approved

For input j=t+Q u and output k=h+M s, the full negative-sign Fourier tensor is

    T[s,h,t,u]=omega^(-h t) xi^(-s t) eta^(-h u).

Expansion of k j proves the identity with no coprimality requirement. The three paired flattenings have ranks N, min(Q,M), N. The middle rank is a rectangular Vandermonde rank; the other two are Fourier/Kronecker products times invertible diagonal/permutation maps. Separate invertible changes on each individual digit leg preserve those ranks. Joint changes on two legs need not.

The CP rank is exactly N: the input/output flattening gives the lower bound, and the explicit sum indexed by (t,u) gives N four-leg rank-one terms.

The single-cut width conclusion is scoped. It grows as min(Q,M), so a statement excluding fixed width requires that quantity to grow, such as square balanced dimensions. If one radix remains fixed, the crossed-cut rank remains fixed. None of these ranks is a lower bound on general multi-stage arithmetic circuits.

### Endpoint-local sparsity rigidity approved

With A acting on s and B on u, the transformed tensor factors entrywise as

    (A F_Q)[a,t] * omega^(-h t) * (F_M B^T)[h,b].

Therefore its support size is the product of the two matrix support sizes, at least QM. Equality forces both invertible factors to be monomial. Thus every N-entry core in this restricted gauge is obtained by inverse-Fourier endpoint transforms up to monomial maps. It does not make those transforms free.

The complex crossed-cut singular-value statement is also correct: the two disjoint-support embeddings have Gram factors Q and M, leaving precisely the singular values of the Q-by-M partial Fourier matrix after normalization. The other two cuts are unitary. Numerical concentration of Schmidt values does not reduce exact rank or establish an exact classical evaluator.

The standard two-axis ledger remains Theta(N log N), including root preparation and all butterflies. There is no new upper bound hidden in the N-sparse center.

### Relation to ongoing research

This source strengthens the local endpoint-gauge explanation and cut bookkeeping. It does not contain the independently derived routed-grid product certificates or weighted-cycle product/mask-rank bounds. Comparisons must preserve digit ordering: its crossed cut has rank min(Q,M), whereas a different realignment/order can have rank min(Q,M)^2. Those are not contradictory statements about one fixed flattening.

## 4. Hero0 Phase9 dense-controller/innovation families

### Universal identity versus restricted algorithm

The controller may be an arbitrary dense circulant. With a seed spectrum having no zero entries, two length-K transforms identify every eigenvalue lambda from F(v1)/F(v0). Later residual spectra satisfy E_t=F_(t+1)-lambda F_t. Summing the forced recurrence gives the stated finite geometric formula, rational numerator, and singular branch.

The identity holds for every raw input and any chosen lambda when the true residuals are supplied. This is not a universal fast evaluator: arbitrary residual spectra contain the original unresolved column transforms. Learning a dense controller does not make the later residuals sparse automatically.

The telescoping boundary is correct:

    B=lambda F_(M-1)-lambda^M F_0.

At lambda z=1 the finite sum gives M F0 plus weighted residual terms; no 0/0 is assigned an arbitrary value. Lambda=0 is harmless. The fully identifiable promise requires nonzero seed-spectrum entries. The code's convention of setting an unobservable eigenvalue to zero is a separate chosen-controller branch, not a guarantee of recovering every possible hidden controller.

### Promised fast paths approved

At most s position spikes per residual can be recovered from 2s consecutive frequency samples by a Vandermonde/Prony argument, with the root scan and small solve charged. O(1) total spikes allow direct O(N) corrections. Per-transition sparse spikes use K short length-M transforms and give the stated O(N(s+log M+R)+R K log K+M s^3) bound.

Dually, s spectral innovations per transition can be detected from 2s raw-position residual probes after obtaining the dense circulant kernel. A mode affects only M outputs. The stated O(N(s+R+1)+(R+1)K log K+s M^2+M s^3) bound is sound in the supplied-root field model. For M=Theta(log N), fixed s,R gives O(N) on the promise; growing s=O(log log N) gives the claimed conditional log-log scale.

The sampled syndromes alone are not membership proofs. Dense nonzero residuals can be invisible to the probes, in either domain. The source correctly gives adversarial controls and a separate random check.

### Randomized verification is not deterministic exact recognition

For a fixed true-minus-proposed residual matrix R over F_q and independently uniform w, the probability w^T R=0 is q^(-rank R), and independent rounds multiply these probabilities. The transpose-circulant eigenvalue reversal lambda[-ell] is correct for the source's shift convention. The default OS-random sampling is selected after the candidate parameters are fixed.

Promised inputs always pass and their computed transform is exact. An unpromised input can falsely pass with positive probability and then receive an incorrect output. FFT fallback on rejection does not turn this into a deterministic all-input exact algorithm; the worst-case fallback work also remains ordinary FFT scale. The exact finite-field probability must not be silently transferred to an exact-complex random-sampling model.

The stated rarity formula is correct conditional on an observable first seed: subsequent uniform columns induce uniform residuals after subtracting a fixed function of the past, so the sparse-volume probability multiplies across transitions. It says nothing about other Fourier algorithms.

### Counter qualification

Static inspection finds that phase9_dense_cycle.py:ntt_inverse computes pow(root,P-2,P) without invoking the counter's inversion routine or adding its exponentiation bound. The inherited Costs class tracks field additions/multiplications, selected zero tests, selected inversions and input reads, but its total excludes general indexing/storage and there is no output-write field. Root discovery is also outside that total.

These missing operations can be repaired by supplied/table root reuse or explicit charging, plus a separate O(N) I/O/index ledger. They do not change the promised-family asymptotic conclusions at fixed verification rounds. They do mean that statements calling the printed finite-size totals “all charged work” need qualification. The packet already reports no measured advantage over its radix-two baseline; this review makes no corrected performance claim.

## 5. Independent evidence produced here

The independently authored checker verifies:

- 7,282 raw tensor entries, 33 exact flattening ranks, and 21,846 directly summed endpoint-gauge entries across 11 rectangular/square sizes.
- 11 numerical crossed-cut spectrum controls, used only to corroborate the separate exact proof.
- All 480 GL2(F5) matrices by support histogram, accounting for 230,400 endpoint-gauge pairs and 1,024 support minimizers. This is support accounting, not 230,400 explicit full tensor reconstructions.
- 12 arbitrary-input forced-recurrence cases, 528 full output entries, and 13 singular-denominator outputs.
- All support subsets up to size four for the first four K=8 Fourier probes; 48 single-event decodes across both domains; both dense invisible-probe controls.
- Exact Freivalds annihilator counts over all 125 test vectors for three residual matrices.
- 24 cyclic-solver/guard controls, including zero weights and product-one singular cases.
- Exact constant-mass recurrence envelopes through height 40, the harmonic telescope through height 100, and 48 row-sparse/Vandermonde rank controls.
- All integrity and inherited-byte comparisons described above.

The source's larger claimed test totals are kept as source reports. They were not rerun, and these new smaller controls do not certify every implementation branch or replace the written proofs.

## 6. Benchmark and novelty boundary

The official OpenAI scope page currently distinguishes a subsequential result from a separate uniform all-length exact DFT/convolution formalization with work O(N (log N)^(1-10^-13)), including stated scalar/root-order preparation under unrestricted exact complex arithmetic. This supports the packet's benchmark caveat; it does not supply the missing GFC factors. [Official scope](https://github.com/openai/math/blob/main/lean/docs/130.md)

Ailon's primary paper states its Fourier lower bound under a uniform conditioning restriction, so it does not rule out the packets' unrestricted-coefficient model. [Primary paper](https://arxiv.org/abs/1403.1307)

The recurrence analysis, Fourier diagonalization, Prony/Vandermonde decoding, Freivalds testing, tensor flattenings, and sparse-inverse arguments have established antecedents. The packets appropriately do not claim publication priority. This review does not establish novelty of their particular combinations.

## 7. What is useful next

The mass-contraction target is a meaningful change of objective only if it leads to an exact size-uniform rewrite that truly lowers the sum of recursive Fourier lengths. The next positive deliverable must be actual phase-compatible factors, a uniform coefficient/index generator, and a fully charged recurrence. The Hero17 local-gauge result prevents assigning zero cost to the endpoint conversions. Hero0's arbitrary-input identity prevents disguising the missing transform bank as dense residual preparation. The existing scoped inverse and compatibility gates remain useful early rejection tests, without becoming general impossibility claims.

No new universal sub-FFT or linear-time Fourier algorithm is established by this source update.
