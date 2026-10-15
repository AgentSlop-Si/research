# Independent audit: Hero17 Phase13 branching Weyl/Hankel package

## Verdict and exact boundary

The six proof statements are accepted with their stated restricted grammars and the cost qualifications below. They give useful exact representation obstructions and counterexamples to overextending those obstructions. They do not give a full-DFT algorithm, an unrestricted FFT lower bound, or a historical-priority result.

The active linear Green executors genuinely fix the predecessor's repeated independent root-power computation: modulation powers now advance by one multiplication each. The batch-prepared full-vector sum costs exactly `13N−1` field operations under the package's add/multiply/inversion convention, excluding root discovery and bit costs. This computes `G_S+G_T`, not Fourier.

## 1. Identity, text coverage and predecessor

Direct uploaded archive: `fft_hero17_phase13_branching_weyl_hankel_union_2026-10-10.zip`, Library `libfile_718d2097d5008191939d5d29fd40748f`, version 0, source message `Sentinel_b4d4f209b5608191b424df429fe889a5`. SHA256 `d10093b53cf25b9439c5da7186978e15bc5a5444ac2f12492e5e86745938548f`, 51,288 bytes. CRC and all 16 internal checksum entries pass. The 17 members are preserved unmodified under `source/`; all 16 non-archive files were read as text in full, including the proofs, research/checkpoint, all four Python programs, run instructions, manifests, logs and JSON results. None of the uploaded Python was run or imported.

The nested Phase12 archive has SHA256 `0af410bcfc0f3368b137773fb8eefa3f5bd4ffc6c334d32b87a51e771ded9f54`, byte-identical to the previously reviewed direct Phase12 source. Its accepted audit is `research_round_0058/review_hero17_phase12/PHASE12_AUDIT.md`, manifest `fd5263086a82b00d70cd13b2aa99afed4b8d45dde00fa80b99094ddff6c854b5`. No duplicate mathematical audit or source execution was needed. Its included test log is a source claim, not our execution record.

Full text inspection is distinct from endorsement of every proposed future direction or outside reference. The Phase14 proposal and externally linked all-length transform are outside this bounded Phase13 audit.

## 2. Accepted algebra, independently checked

Let `N≥3` be odd, `ω` primitive of order N, `S e_j=e_(j+1)`, `T e_j=ω^j e_j`, and `F[i,j]=ω^(ij)`. The proofs apply over the complex numbers; the purely algebraic identities also apply over a field containing ω with characteristic not dividing N. All exponent divisions are in the residue ring modulo N. This is unrelated to floating-point division.

### Canonical Weyl rank

The N² words `S^a T^b` form a basis: on each cyclic diagonal, coefficient extraction is an invertible length-N character transform. Explicitly,

`C_A[a,b]=N^−1 Σ_t ω^(−bt) A[t+a,t]`.

Thus `C_F[a,b]=Γ ω^(−(a−b)²/4)`, where `Γ=N^−1 Σ_t ω^(t²)`. The change of variables `(t,s)→(t−s,t+s)` gives `G(ω)G(ω^−1)=N`, so Γ is nonzero. Factoring off row and column chirps leaves `[ω^(ab/2)]`, an invertible Fourier permutation. Hence every coefficient is nonzero and the coefficient matrix has rank N.

### Fixed canonical ordering

For `α^N≠1`, `β^N≠1`, the coefficient array of `G_S(α)G_T(β)` is the outer product `α^a β^b/[(1−α^N)(1−β^N)]`. Zero parameters cause no problem: use `0^0=1`, yielding an impulse factor. Left/right Weyl monomials only shift coefficient coordinates and multiply separate row/column characters. Any B-path sum in this exact grammar has coefficient rank at most B, so equality to F implies `B≥N`.

Matrix-product orientation matters: `G_S G_T` applies `G_T` to a column input first. The source's informal “followed by” should always be read through its displayed product. No reverse order, mixed orders, different Weyl pairs across branches, arbitrary diagonal gauges, or deeper paths are covered. The representation count does not lower-bound a shared evaluator's arithmetic.

### Rotated basis

For `U=S^uT^v`, `V=S^rT^s`, `D=us−vr` a unit modulo N, the coordinate map is invertible. The actual word phase is

`U^iV^j=ω^[uv i(i−1)/2+rs j(j−1)/2+vr ij] S^(ui+rj)T^(vi+sj)`.

Substitution gives exactly the source formula with quadratic coefficients `u²+v²`, `r²+s²`, and mixed coefficient `δ=(D−ur−vs)/2`. Its rank is `N/gcd(N,δ)`. One proof extracts an invertible Vandermonde submatrix of size equal to the order of `ω^δ`; there are exactly that many distinct rows. Thus changing the ordered generators changes this rank. `(S,ST)` really gives rank one. Composite N can give intermediate ranks; our N=9 examples give rank 3 and N=15 gives ranks 3 or 5.

### Prime fixed-pair Hankel gate

For odd prime length p, all branches must use the same ordered pair U,V and have no extra Weyl endpoints. Oddness ensures `U^p=V^p=I`; each two-resolvent coefficient is geometric in i and j. If δ is nonzero, rank forces B≥p. If δ=0, the identity

`(u²+v²)(r²+s²)=(ur+vs)²+D²=2D²`

forces both quadratic coefficients nonzero modulo p. At j=0 the coefficient sequence is a nondegenerate chirp. Its `m×m` nonwrapping Hankel matrix, `m=(p+1)/2`, factors through the distinct nodes `ω^(−(u²+v²)a/2)`, hence has rank m. Each geometric term contributes rank at most one. Therefore `B≥(p+1)/2` for every fixed generating pair.

The endpoint exclusion is material. In F101 at length 5, cyclically shifting the geometric sequence `2^i` by one gives `[16,1,2,4,8]`; its nonwrapping 3×3 Hankel matrix has rank 2. An endpoint-gauged term need not retain Hankel rank one. This does not affect the separate canonical coefficient-rank theorem, where endpoints are allowed.

### High rank and dense inverse are not computational hardness

The reverse product has coefficients proportional to `α^a β^b ω^(ab)`, hence rank N when αβ≠0 and both Green factors exist. A three-stage `G_S(α)G_T(β)G_S(γ)` also has rank N: its coefficient array factors into an invertible cyclic Green numerator matrix, a nonzero diagonal, F, and another nonzero diagonal. Both products apply in O(N) field work using one/two cyclic recurrences and pointwise multiplication. They are explicit positive controls against treating Weyl rank as an arithmetic lower bound.

For `H=G_S(α)+G_T(β)`, set `0<α<1` and β=0 over C. Then `H^−1=I−(2I−αS)^−1`; each off-diagonal cyclic coefficient is nonzero and the diagonal is nonzero since `(α/2)^N<1/4` for N≥2. Rational continuity supplies sufficiently small nonzero β with dense inverse, nonsingular factors and noncommutation. Noncommutation also follows by multiplying the resolvent commutator by invertible factors and using `αβ(ST−TS)≠0`. Such H cannot be an uncorrected product of L factors whose inverse columns have support at most 2 if `2^L<N`.

The existence proof is not a free uniform finite-field parameter-selection algorithm. Our small finite-field witness search is separately bounded verification. The complex witness can also be kept distinct from F: at β=0, `H[0,0]=1+1/(1−α^N)>2`, while `F[0,0]=1`, and this inequality persists in a sufficiently small neighborhood. No statement about arbitrary low-rank corrections follows.

## 3. Costs, guards and implementation scope

With a supplied primitive root and valid α,β:

| Routine | Add/sub | Multiplication | Inversion |
|---|---:|---:|---:|
| Batch modulation preparation | N | 5N | 1 |
| Cyclic Green application | 2N−1 | 3N−2 | 1 |
| Sum output, beyond cyclic solve | N | N | 0 |
| Preparation plus full sum | 4N−1 | 9N−2 | 2 |

The total is `13N−1`. Powers, denominator products and prefix/reverse products are all included; even unused final power updates are counted. Arrays and all output writes require O(N) additional memory operations and O(N) storage. Input-independent tables may be reused only with identical N, β, ω and field; their first construction must be charged. The optional `diag` is a promised correct, full-length prepared array; the source does not validate arbitrary supplied tables.

`prepare_gt` (the default in forward/sum routines) uses running roots and N inversions, also O(N) in the stated unit-inversion model. `prepare_gt_batch` uses one inversion with more multiplications; it is an inversion tradeoff, not a lower total when every inversion costs exactly one. The source large benchmark explicitly supplies the batch table. Reverse/triple defaults also use that table algorithm.

Finite-field root discovery in `omega_root` includes trial primality testing, factorization of N and search over base candidates. It is not a proved O(N) cold setup and is excluded from this field-operation table. Inversions, modular arithmetic and parameter discovery need their own bit-complexity charge. Over C, exact roots and exact arithmetic are assumptions; no numerical-stability or precision guarantee is supplied. Dense matrix, coefficient and rank routines are bounded verification oracles with higher cost, not part of the linear executor.

The poles are `α^N=1` or `β^N=1`; production recurrences reject them through a zero denominator. The matrix/rank theorems need their full odd-N and primitive-root hypotheses. The dense-inverse existence statement allows every N≥2 over C. We do not infer the complex existential claim for every finite field.

## 4. Fresh independent controls and replay

`verify_phase13_independent.py` was authored for this audit, with no source imports. It checks:

- Seven different small fields from the source's fields, at N=3,5,7,9,11,15,17; trace extraction, Gauss products and complete Fourier reconstruction.
- 59 rotated-basis reconstructions (6,771 entries) by actual matrix powers/products rather than the claimed rotated phase formula; five intermediate-rank composite controls.
- All 15,744 generating direction pairs at prime lengths 3,5,7,11, with exact elimination on every mixed-character core; all 1,568 rank-one cases also pass actual Hankel elimination.
- 21 canonical endpoint controls and the rank-two shifted-geometric Hankel countercontrol.
- 201 full basis-vector operator checks for forward/reverse/triple paths, plus seven explicitly inverted dense-inverse noncommuting branch-sum witnesses.
- Exact rational β=0 dense-inverse coefficients for N=2 through 17, pole rejection and zero-parameter controls.
- A freshly seeded arbitrary input at N=65,536: every cyclic recurrence equation, seven direct kernel rows, seven independent DFT bins (all differ), and all preparation/application ledger totals.

All pass. These finite checks accompany the all-size proofs; they do not replace them. The source's two “independent” audit scripts import its operator implementations; our checker does not. Source `python -m unittest -v test_phase13` discovers the later-defined test classes; executing that file directly would reach `unittest.main` before those classes. We followed neither route.

Portable replay: copy only our checker to an unrelated directory and run it with Python 3 standard library. `PORTABILITY_CHECK.json` records the actual relocated run and byte-identical results. `SEALED_MANIFEST.json` hashes all review and preserved source bytes; the adjacent `.sha256` hashes that manifest.

## 5. Primary context and unclaimed provenance

[Gurevich–Hadani–Howe, arXiv:0808.2447](https://arxiv.org/abs/0808.2447) explicitly relates DFT, Gauss sums and the finite Weil representation. [Plonka–Tasche, Prony Methods for Recovery of Structured Functions, Section 2](https://num.math.uni-goettingen.de/plonka/pdfs/gamm-preprint.pdf) gives the classical Hankel/Vandermonde factorization for exponential sums. These support the established context, not priority for this particular path-grammar combination. The source's de Gosson/Luef DOI fetch failed and was not relied upon; its linked all-length FFT note is outside this review. No novelty follows from this limited literature check.
