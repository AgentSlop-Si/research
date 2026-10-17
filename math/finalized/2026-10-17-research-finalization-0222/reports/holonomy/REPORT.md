# ALG-PRIMITIVE-HOLONOMY: classical invariant comparison and single-resolvent closure

Date: 2026-10-17 UTC. Baseline: `AgentSlop-Si/research` commit `e3f3fd2fde808e577989907f00740c16905dbeb1` (90 closed, 237 open records).

## Disposition

**Complete the selected equality/metric comparison gate.** The accepted all-anchor primitive-holonomy curvature theorem remains mathematically valid. Its four-entry invariant is classical dephasing/Haagerup material. Its single-Green/Fourier non-equivalence consequence is subsumed by elementary inverse support, with strictly weaker hypotheses. The corresponding normalized operator-norm obstruction is an exact specialization of the repository's already accepted ALG-044 theorem, not a new metric theorem.

The specific all-anchor determinant remains a useful exact structural identity; neither the external comparison nor this proof establishes its historical priority. Recommend retaining it as a technical appendix and retiring repeated investigation of single-resolvent Fourier equality. **No automatic whole-parent closure, priority change or novelty promotion is proposed.** Multi-resolvent sums/products, tunable internal masks, and the distinct Phase37B pencil remain outside this comparison.

No external writes were made. Historical programs were read only as prose where relevant and were not executed. Newly authored finite controls check indexing and boundaries; they are not the proof.

## 1. Exact source identity

The current open record is preserved in `evidence/OPEN_RECORD.json`. Its selected gate asks for an exact invariant/equality/metric comparison with classical Fourier-equivalence, switching, Gram and spectral methods, while preserving arbitrary-invertible versus unitary distinctions.

Two full archival bodies were fetched at the baseline and saved byte-exactly:

- [Phase37 theorem, Theorem 37A](https://github.com/AgentSlop-Si/research/blob/e3f3fd2fde808e577989907f00740c16905dbeb1/math/archive/objects/41/41e33de3d9eccd79df4ae2ff04f851eb52b0df0e584f36a3d83a08ae096b1bc4__THEOREM_1_.md). SHA-256 `41e33de3d9eccd79df4ae2ff04f851eb52b0df0e584f36a3d83a08ae096b1bc4`.
- [Independent Phase37 review, section 1](https://github.com/AgentSlop-Si/research/blob/e3f3fd2fde808e577989907f00740c16905dbeb1/math/archive/objects/20/206c0390037a3185b57049d815524ca21d52ec7cacb7bed58e080958f649fcc4__REVIEW.md). SHA-256 `206c0390037a3185b57049d815524ca21d52ec7cacb7bed58e080958f649fcc4`.

The original theorem also contains a separate six-resolvent fixed-pencil result and an inherited two-sums counting error. The independent review corrects that circuit to three vector sums. Neither the pencil proof nor its controls are reopened here.

The saved historical Catalogue row is context only, not a fresh native-table read. The current selection comes from the commit-pinned open index.

## 2. Original proof audit

Let `N=2^m>=4`, let `omega` have exact order N, let P be the permutation matrix of one directed N-cycle, and let `alpha!=0`, `alpha^N!=1`. Put `G=(I-alpha P)^(-1)`. In cycle positions,

`G[i,j] = alpha^((i-j) mod N)/(1-alpha^N)`.

Assume `alpha^N=omega^c` with `gcd(c,N)=1`. For nonzero-entry M the anchored ratio is

`R[i,j;a,b] = M[i,j] M[a,b] / (M[i,b] M[a,j])`.

Writing `T[i,j]=1_(i<j)`, the ordinary linear exponents cancel and the Green exponent is

`E[i,j;a,b] = c(T[i,j]-T[i,b]-T[a,j]+T[a,b]) mod N`.

At anchors `a=b=0`, delete the anchor row and column. Then `E=-c L`, where L is the lower-triangular all-ones matrix. Its determinant is `(-c)^(N-1)`, a unit modulo N. For any anchor a, the vectors `e_i-e_a` with `i!=a` form an integral basis of the same zero-sum lattice. Independent changes of the row and column anchor therefore multiply the reduced pairing matrix by unimodular integer matrices. All anchored determinants differ only by sign. Independent permutations are also basis changes, so the conclusion survives them.

For Fourier `F[i,j]=omega^(ij)`, arbitrary relabelings give

`E_F[i,j;a,b]=(r_i-r_a)(c_j-c_b) mod N`.

Its reduction modulo 2 is an outer product of two nonzero vectors, because complete permutations of the even-size label set contain both parities. The rank is exactly one. The primitive Green rank is N−1. The proof is sound.

**Guard that must remain:** the determinant is a unit only when c is coprime to N. For dyadic N and even c, every Green exponent is even and its parity rank is zero, not N−1. Nonprimitive holonomy does not invalidate the separate exclusion below. The original primitive hypothesis is essential for this rank assertion, not for every possible proof of non-equivalence. Over a finite coefficient field, verify all ratios are nonzero and lie in the Nth-root subgroup before reading exponent parity from `R^(N/2)`; exponent parity lives in F2, not the original field.

## 3. Exact all-length inverse-support consequence

### Proposition 1

Let K be a field, `N>=3`, `char(K)` not divide N, and let `omega in K` have exact order N. Let `F_N=(omega^(ij))_(0<=i,j<N)`. For any N-cycle permutation P and any `alpha in K` with `alpha^N!=1`, set `G=(I-alpha P)^(-1)`.

There do not exist invertible monomial matrices L,R such that

`L G R = F_N`.

The same holds for any nonzero scalar normalization of F_N, including the normalized complex Fourier matrix. No primitive-holonomy assumption is needed, and `alpha=0` is included.

### Proof

The finite geometric identity gives

`(I-alpha P)(I+alpha P+...+alpha^(N-1)P^(N-1))=(1-alpha^N)I`,

so the stated inverse exists. Every row and column of `G^(-1)=I-alpha P` has at most two nonzero entries. In contrast,

`(F_N^(-1))[i,j]=N^(-1) omega^(-ij)`

is entrywise nonzero. Inversion of `LGR=F_N` yields

`R^(-1)(I-alpha P)L^(-1)=F_N^(-1)`.

Multiplication by invertible monomial matrices merely permutes and nonzero-scales rows and columns; it preserves the number of nonzeros in each row up to row permutation. The left side has row support at most two, while the right side has row support N. This contradicts `N>=3`. QED.

This is an elementary support argument, not a historical-priority claim. It also applies to any invertible matrix whose inverse has a row with fewer than N nonzeros, and therefore is stronger than needed for this exact single-cycle model. It does not exclude a sum of resolvents or a general product, because their inverses need not retain two-sparse rows.

### All boundary cases

- `alpha=0`: G=I; the support contradiction is stronger (one nonzero per row).
- `alpha^N=1`: `I-alpha P` is singular. G is undefined; no generalized inverse is silently substituted.
- `N=1`: every legal G is a nonzero scalar and is equivalent to F1. Excluded from the proposition.
- `N=2`, `char(K)!=2`: with `P=[[0,1],[1,0]]`, equivalence occurs exactly when `alpha^2=-1`. For nonzero alpha, the sole cross ratio is `1/alpha^2`, whereas the F2 ratio is −1 and remains −1 under row/column swaps. Sufficiency is explicit: with `D=diag(1,alpha)`, `G=(1-alpha^2)^(-1) D F2 D` when `alpha^2=-1`. Alpha zero is not equivalent; alpha squared one is singular. Over R there is no legal equivalence; over C alpha=±i gives it.
- Characteristic dividing N: excluded; the stated inverse-Fourier formula and primitive-root interface must not be assumed. Fields admitting a root of exact order N already avoid that positive-characteristic obstruction, but the condition is stated explicitly.
- Singular endpoint scalings cannot produce an invertible Fourier matrix by rank. The proposition allows arbitrary nonzero endpoint magnitudes, not just unit-modulus phases.

### Independent row-ratio cross-check

For alpha nonzero, compare two adjacent cycle rows. Their coordinatewise quotient takes one value N−1 times and a distinct value once; distinctness follows from `alpha^N!=1`. Invertible column gauges cancel, row gauges rescale both values, and permutations only reorder coordinates or select the corresponding row pair. For two distinct Fourier rows, the quotient is a nontrivial character `omega^(d j)` whose distinct values each occur `gcd(d,N)` times. Equal fiber multiplicities cannot be `(N−1,1)` for N>=3. This proves the same exclusion without using curvature rank. It is a supplementary check, not a separate novelty claim.

## 4. Metric consequence is already accepted ALG-044

The source is [the accepted ALG-044 theorem, section 3.1](https://github.com/AgentSlop-Si/research/blob/324e5ad245c2c1f53b477140353565f8ced28d6b/math/finalized/2026-10-16-research-finalization-2101/source_obligations/REPORT.md). It states for a complex flat unitary U and `T=A Q^(-1)+E`, with Q invertible, column supports at most s in Q and t in A, and `rank E<=k<N`,

`||U-T||_2 >= sqrt(max(0,1-s t (k+1)^2/N))`.

For `T=L G R`, make the exact substitution

`A=L R`, `Q=R^(-1)(I-alpha P)R`, `E=0`.

Then `A Q^(-1)=L G R`, Q has at most two nonzeros per column, A is monomial, and `s=2,t=1,k=0`. Therefore

`||L G R - U||_2 >= sqrt(1-2/N)` for N>=3.

This is absolute operator error against the fixed normalized target `U=F_N/sqrt(N)` (or any other flat unitary), not normalized Frobenius error. Endpoint magnitudes can be arbitrary and no condition-number bound is needed. For an unnormalized target F_N the corresponding absolute bound scales by `sqrt(N)`, after rescaling the approximant; this is a change of normalization, not an identical numerical error claim.

For completeness, an independent row proof is short. Choose a nonzero row b of `(LGR)^(-1)` and its index i. Then `b(LGR)=e_i^T`, and b has support size `s<=2`. Project the identity `b(LGR-U)=e_i^T-bU` away from coordinate i. Unitarity and flatness yield

`||P_(i^c)(bU)||_2^2 = ||b||_2^2 - |(bU)_i|^2 >= (1-s/N)||b||_2^2`.

Use `||b(LGR-U)||_2<=||b||_2||LGR-U||_2` and cancel the nonzero norm. For alpha zero, s=1 yields the stronger `sqrt(1-1/N)` bound. This derivation is consistent with, and not additional to, the accepted sparse-inverse theorem.

## 5. Named primary-source comparisons

### 5.1 Dephasing and four-entry invariants

The primary research article [Östergård and Valtonen, *Equivalence of complex Hadamard matrices* (published 28 July 2026)](https://link.springer.com/article/10.1007/s10801-026-01568-x), Definition 1, Theorem 1 and section 2.3, uses unitary monomial equivalence, uniquely normalized dephasing up to scalar gauge, and the Haagerup four-entry invariant/multiset. The article attributes the invariant to Haagerup; that bibliography is not a read of Haagerup's original chapter.

**Our hypothesis map/inference:** for a unimodular H, its invariant `h_ij conjugate(h_il) conjugate(h_kj) h_kl` equals `h_ij h_kl/(h_il h_kj)`, exactly the archived ratio with anchors `(a,b)=(k,l)`. For general nonzero entries, reciprocals and conjugates differ. The arbitrary-invertible extension is justified directly: each row/column factor cancels in the ratio. With fixed row/column labels, equality of all anchored ratios is equivalent to diagonal equivalence: ratios equal to those of M let one solve the row and column factors from an anchor row and column.

Thus there is an exact invariant-mechanism match and a hypothesis mismatch in applying the paper's Hadamard-domain theorem directly to G. The paper does not supply the cycle's anchored determinant formula. No equivalence conclusion follows merely from equal Haagerup sets: positional information can be lost. The exact basis/determinant calculation in section 2 fills that project-specific step without establishing novelty.

### 5.2 Support and energy

[Tao, *An uncertainty principle for cyclic groups of prime order*, arXiv:math/0308286v6](https://arxiv.org/pdf/math/0308286v6), pages 1–2, equation (1), proves the standard support-product bound for arbitrary finite abelian groups using Cauchy–Schwarz and Plancherel. Theorem 1.1 is the stronger prime-order additive bound.

**Our mapping:** in a hypothetical exact complex factorization `T=U`, take `z=Qe_j` and `Tz=Ae_j`. The above monomial/sparse substitution gives `|supp z|<=2`, `|supp Uz|=1`, contradicting `2<N`. Tao uses a `1/N` transform normalization; scaling by `sqrt(N)` preserves support. The metric estimate is a restricted-energy version of the same argument, already supplied by ALG-044. The prime-order additive theorem is neither needed nor transferred to all composite lengths, and no magnitude argument is transferred to finite fields. The exact inverse-support proof in section 3 supplies the separate algebraic-field conclusion.

### 5.3 What this closes and what it does not

The selected gate asked for a primary theorem with a precise hypothesis/formula/cost map, or a qualified nonmatch. Both are now provided: dephasing/Haagerup mechanism overlap with explicit domain mismatch, the classical support-energy mechanism, and an exact existing internal metric specialization. There is no remaining mathematical lemma needed for single-cycle exact non-equivalence or this normalized operator bound.

The stronger task would need a separately selected family whose inverse is no longer sparse, followed by a new proof or paid construction. Nothing here proves a generic many-cycle-bank exclusion, a faster Fourier evaluator, a production certificate, or historical priority for the anchored determinant.

## 6. Cost and verification boundaries

Proposition 1 is a structural proof from supplied P, alpha and the invertibility guard. It does not require forming N squared entries of G, computing cross ratios, or extracting discrete logarithms. If implemented as a diagnostic on a declared cycle representation, validation of that representation and its parameters must be paid; no root acquisition, field arithmetic, bit complexity or numerical certification is free. A generic dense-matrix input has a different input-reading cost and is not covered by a linear-time claim.

The new checker uses modular arithmetic only for the algebraic identities and rational arithmetic for a Walsh flat-unitary instance of the energy step. It never imports or executes historical source programs. Finite controls do not replace any universal proof and do not prove novelty. Run `python checks/fresh_controls.py` from this directory to reproduce `checks/RESULTS.json`.

## 7. Proposed bounded current-gate wording

> Named single-cycle equality/metric comparison complete. The all-anchor primitive-holonomy determinant and parity-rank theorem remain accepted with their original primitive hypothesis. The cross-ratio mechanism matches classical dephasing/Haagerup invariants after an explicit unitary-versus-arbitrary-invertible hypothesis map. Exact single-Green/Fourier non-equivalence for every N>=3 follows from inverse support, including alpha=0 and nonprimitive holonomy under alpha^N!=1. The normalized complex operator lower bound sqrt(1-2/N), with arbitrary invertible monomial endpoints, is an exact s=2,t=1,k=0 specialization of accepted ALG-044. Do not repeat the single-cycle equality/metric gate. Broader sums/products, tunable masks, finite-precision certification and historical priority remain separate; no parent status or priority change is implied.

Suggested pass/stop condition: accept this bounded comparison after independent proof/source review, then stop this selected activity. Any successor must name a different non-sparse-inverse family or a specifically justified historical attribution question rather than rerun the completed single-factor obstruction.
