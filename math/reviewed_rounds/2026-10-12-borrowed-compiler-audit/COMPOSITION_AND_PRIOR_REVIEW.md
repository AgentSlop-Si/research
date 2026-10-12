# Borrowed Fourier composition and prior-source review

12 October 2026 UTC. Publication edition of the mathematical review. The original reviewed-source hashes are recorded in PROVENANCE.json. This is source-level analysis; imported research code and the Lean development were not executed.

## Verdict

**ACCEPT the mathematical local construction and its all-length implication in the specified exact complex/logarithmic-word model. REPAIR the comparison and novelty account.** No counterexample to Sections 1–5 was found in this review. The global engine is an ordinary theorem dependency, not an unresolved conjecture merely because it was not executed here.

**The decisive prior-source finding changes the proposed asymptotic comparison:** the same pinned OpenAI revision already contains a formally stated exact-width, arbitrary-input, polynomially prepared O(log² r) Fourier compiler. Its manuscript's O(log⁴ r) compiler is therefore an incomplete comparator for what that source corpus already establishes. A claim that the candidate first improves the referenced framework's available local exponent from four to two is unsupported and, against the formal source, false. The narrower claim of improving the manuscript's displayed construction remains literally true.

## 1. Previously overlooked quadratic-depth compiler

Original source: openai/math revision `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, under `lean/OAI/Computability/FourierTransform/`. Direct inspection of the original files confirmed that `FourierWords.lean` has Git blob SHA-1 `50e57b23f72e6c830ead098e80776d70e02db646`, byte-identical to the inspected copy in Sussman's pinned repository.

[FourierWords.lean, lines 101–119](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/FourierWords.lean#L101-L119) supplies:

- `sound_ballad`: the word acts at exact width n when n ≤ 2^e.
- `creates_ballad`: for any primitive nth root u and supplied dyadic roots, it computes the full Fourier matrix on every input.
- `beats_ballad`: its beat count is `score e`.
- `score_le`: `score e ≤ 20000000*(e+1)^2+7`.

Take e = ceil(log₂ n), with e=0 at n=1. This already gives the required quadratic logarithmic count.

### Exact-width/layer-model qualification and its resolution

[LayerWords.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/LayerWords.lean) defines one beat as a scaled-index map followed by an involutive pairing of copies of C, with singleton identities. `Sound` restricts all reads and pair partners to the first n coordinates and makes all outside coordinates identities. It is therefore genuinely exact width; correctness is universally quantified over arbitrary input arrays.

`Sound` alone allows the scaled-index map to be a general gather and permits zero scalings. This is not a fatal model mismatch. For the Fourier word, every intermediate factor restricts to a square n×n linear map, and their product is the invertible Fourier matrix. Therefore every factor is invertible. A square scaled gather is invertible exactly when its index map is a permutation and all scalars are nonzero. Thus the actual Fourier word consists of valid invertible monomial layers and disjoint C layers. Separating a beat into these two layers costs a factor of two. Conversely C itself has a constant shear/diagonal decomposition, so the candidate's shear/monomial model has the same asymptotic depth.

### Preparation is a charged program-existence theorem

The words being written inside `noncomputable section` does not mean their schedules or coefficients are free advice:

1. [LocalCompiler.lean, lines 113–138](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/LocalCompiler.lean#L113-L138): `publish` returns `Engrave` for the Fourier word.
2. [WordCompilation.lean, lines 15–19](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/WordCompilation.lean#L15-L19): `Engrave.layers` asserts `Makes` for the complete finite layer table.
3. [CompilerEnvironment.lean, lines 21–22](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/CompilerEnvironment.lean#L21-L22): `Makes` means `PolyCan`, with time and integer bounds in the ambient width.
4. [PolynomialPrograms.lean, lines 10–13](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/PolynomialPrograms.lean#L10-L13): `PolyCan` supplies one fixed polynomial exponent and a `Can` program bound.
5. [ProgramConstruction.lean, lines 16–21](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/ProgramConstruction.lean#L16-L21): `Can.unfold_bound` gives one RAM program and constants, valid on all inputs, with charged time and polynomial integer cap.
6. `WordPrograms.lean`, `Hue.of_root`, lines 63–71, derives a root's conjugate by a proved-valid inverse. Coefficient conjugates are prepared programs, not a conjugation oracle on the data.

The needed ambient size can be chosen polynomial in n, since e=ceil(log₂ n), 2^e<2n for n>1, the supplied root table has e+1 entries, and these are precisely `publish`'s explicit hypotheses. There is no uncharged exponential preparation hidden in this interface.

### Existing mechanism

The formal compiler already has the two-dirty-bank alternative:

- `CirculantUpdates.lean`: `eddy` forward-transforms both arbitrary banks, makes a spectral accumulation, then inverse-transforms both; `spill_eddy` proves source restoration.
- `ToeplitzUpdates.lean`: `duct` and `well` are nested additive commutators through those two banks.
- `MeasuredFit.lean`: `cliff` is a further product commutator; `reef` uses a fixed 16-way chunk decomposition.
- `ToeplitzLayers.lean`: children run in parallel, the cross update has O(e) beats, and the recurrence `chorus(e+1)=chorus(e)+reachSize(e)` yields O(e²).

The candidate's one-bank shifted-circulant primitive is a different presentation and uses fewer borrowed banks in this comparison. Its historical originality and any meaningful constant improvement remain separate questions. The O(log² r) result itself is already present in the cited formal source.

## 2. Adversarial checks of the candidate's composition

### Conjugate DAG reuse

Maintain a pair of cached registers (v, conjugate(v)) for every scalar-preparation node. Rational literals pair with themselves; roots pair with their inverses; addition, multiplication and division act componentwise. A node referring to a conjugate simply swaps the pair. Thus even repeatedly nested regularizers do not cause exponential expression-tree expansion: at most a constant-factor number of arithmetic nodes is needed for the conjugate-closed DAG. Denominators remain nonzero because conjugation preserves nonzeroness. This proves the polynomial shared-program claim without a complex zero test.

### Dirty registers under synchronized axes

At each slot s, the full-array operation is tensor_j A[j,s]. The product over slots equals tensor_j(product_s A[j,s]) exactly. Local dirty-register restoration is an identity for arbitrary inputs to the whole local word; it does not assert that other axes preserve particular intermediate numeric contents. The tensor identity is enough. No interference counterexample arises from another axis touching the same full-array entries between local instructions.

### Sequential work from layers

The argument does not price a layer as constant sequential work. Each tensor monomial costs O(R) by a prefix traversal carrying original address, destination address, and running scalar product. A tensor C slot decomposes into sectors with widths 2^k, summing to R. A fixed charged engine with uniform constant K gives total sector work at most K R(ell+1)^theta. This is the actual saving step. A local depth bound alone would not imply the global time bound without this engine.

### Index and memory accounting

Digit-prefix traversal has fewer than 2R nodes for radices ≥2. Block-prefix counts are bounded depth-by-depth by digit-prefix counts, including axes that have only one block. The published sector-start formula can be accumulated with constant work per prefix extension. Pack into a separate array to avoid overwriting unread data; this costs O(R) time and memory. The global algorithm does not claim exact-N data-space usage: exact width is a property of local circuit factors. The imported engine uses additional O(2^k) memory with enormous but fixed constants and explicitly charges initialization. For sequential sector calls, these buffers can be reused. All addresses fit O(log N) bits up to a fixed constant factor. This is unit-cost word arithmetic, not a bit-operation bound.

### Root provisioning

The supplied root is specified, not merely an arbitrary primitive root. With L in [2N,4N), the master order D*=(2N)L 2^ceil(log₂(16L)) is below 1024N³. It is divisible by 2N, every factor of L, every required dyadic FFT order, and 4. Charged binary powering extracts all roots with polynomial-in-log N local preparation. This does not prove a theorem using only a supplied primitive Nth root, and the candidate correctly states that boundary.

### Imported auxiliary-role contract

The OpenAI written `network.tex` really proves an arbitrary-role identity. Its scalar network restores arbitrary auxiliary values; after frame telescoping and terminal translation/signed-exchange corrections, every physical role undergoes C^(tensor mf). Recursive batching therefore uses arbitrary transform fibers in all roles legitimately. Its exact recurrence is t(k)≤A+lambda*t(floor(k/m)), with 1<lambda<m; the stated engine theorem includes all preparation, initialization, indexing, and movement. This conclusion uses the written theorem argument rather than substituting finite experiments for it.

### Bound

Constant-many length-L transforms plus polylogarithmic preparation give O(N ell^theta(log ell)^2). The maximal initial-prime-product choice gives ell=Theta(log N/loglog N). Hence O(N(log N)^theta(loglog N)^(2-theta)), and for a=1-theta>0 the ratio to Nlog N tends to zero. The stated asymptotic implication is valid.

## 3. Sussman's newer engine: precise compatibility and limitation

The pinned Sussman source does more than state a README headline. [Seam.lean, lines 186–204](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Seam.lean#L186-L204) states and proves `hillsE8_program` with charged `Can` cost 2^k*ceil((k+1)^alphaE8), for every input array and every batch, where alphaE8=1−8762479/10^10.

`BitLayout.lean:156` defines the output `ripple` as `kernel(Fin k)` applied to the data. `BinaryFrames.lean:67–69,92` defines this kernel as the tensor product of littleC with diagonal (1+i)/2 and off-diagonal (1−i)/2. It is exactly the candidate's C. `Can.unfold_bound` supplies the uniform charged program contract. Thus source-level interface compatibility is established. This review did not rebuild Lean or independently audit Sussman's entire finite-certificate dependency graph.

The kernel saving is **8762479/10^10**. **8762478/10^10** is the slightly weakened pure-log all-length headline saving. They must not be interchanged.

The existing formal transfer explicitly bounds `flightE8(n)=n*(log n)^alphaE8*(loglog n)^2` in `Asymptotics.lean`. That weaker displayed loglog exponent does not rescue local novelty: its imported local compiler already has O(log² r) depth. Combining that existing compiler with the written prime-count/synchronization argument gives the same 2−theta loglog exponent as the candidate. This is a mathematical inference from the retrieved theorems, not a claim that the prior formal file literally states that sharpened expression.

## 4. Final lemma obligations for a clean candidate theorem

These are exposition/packaging obligations, not remaining conjectures:

1. **Conjugate-closed preparation lemma:** explicitly cache the value/conjugate pair per DAG node, giving fixed-polynomial cost and nonzero denominators. Discharge: the construction above.
2. **Rectangular displacement/product lemma:** state L has shape a×e and U has shape e×e; choose one q supporting both a+e−1 and 2e−1. Discharge: the displayed shift-sum identity and chunk inequalities.
3. **Global mixed-layer normalization lemma:** assemble parallel recursive schedules in generalized disjoint layers, then split once into strict types. Do not multiply the recursion by a factor two at each level. Discharge: disjoint supports commute.
4. **Uniform local compiler theorem:** one finite procedure, polynomial in r, emits the full exact-width word from specified roots with all denominators proved nonzero. Discharge: finite recurrences/DAG pair construction and the local algebra.
5. **Charged tensor-slot transfer lemma:** use one fixed engine, a uniform constant, O(R) sector adapters, and explicit permissible global workspace. Discharge: pinned synchronization and engine theorems.
6. **All-length/root lemma:** charge prime selection, CRT, dyadic factor, all chirps, and all three working transforms. Discharge: pinned all-length construction.
7. **Prior-source comparison correction:** distinguish OpenAI's manuscript O(log⁴ r) route from its formal O(log² r) route; add the latter and the two-bank mechanism. This changes the novelty conclusion and must not be treated as an unresolved correctness question.

Overall: **ACCEPT mathematics, REPAIR the research positioning, REFUTE a claim of a new local asymptotic exponent over the complete pinned OpenAI framework.** A narrower one-bank implementation contribution may remain, but it has not been established as historically new by this review.

## Verified chronology and citation identity

The pinned comparison revision fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb is dated 8 October 2026 at 05:20:00 UTC. The path-specific history of FourierWords.lean identifies [the introducing commit 301488868beec11bfd897168433b0a64f5258559](https://github.com/openai/math/commit/301488868beec11bfd897168433b0a64f5258559), dated 8 October 2026 at 05:03:50 UTC. The reviewed FourierWords.lean Git blob is 50e57b23f72e6c830ead098e80776d70e02db646. Its identity was checked directly against OpenAI's source, not inferred solely from attribution in another repository. This source inspection is not a Lean rebuild or a worldwide priority certification.

The factorization binding and the differences between its original dyadic-field contract and this complex all-length local theorem are set out in [SOURCE_BINDING.md](SOURCE_BINDING.md). The finite execution record is separate in [checks/REPORT.md](checks/REPORT.md). Neither a correct construction nor a passed finite test establishes historical originality.
