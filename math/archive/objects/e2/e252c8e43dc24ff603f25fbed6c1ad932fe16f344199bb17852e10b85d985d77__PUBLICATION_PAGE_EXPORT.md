# Mathematical publication candidates from the Fourier research

This research contains substantial theorem candidates even though a faster general FFT has not been established. The two strongest current publication directions are an exact cyclic-resolvent decomposition length and a sharp permutation-sensitive Fourier rank theorem. An explicit resultant identity is also worth preserving, with a more modest standalone publication case after closer comparison.

These are publication candidates, not confirmed worldwide firsts. Proof checking within the project, historical novelty, numerical performance, and external peer review are separate questions. The assessment below covers selected checked results; the complete material inventory is still being reconciled.

## Three leading manuscript candidates

### Exact cyclic resolvent length

For the five-point chirp inverse B₅ = (F₅⁻¹ + diag(ζ₅³ʲ²))⁻¹, the minimum number of diagonal-ended weighted Hamiltonian-cycle resolvent summands is exactly three. The lower bound allows every cycle order, zero edge weights, and singular endpoint masks, while requiring legal inverse denominators. The construction uses two nontrivial reciprocal-pole Green solves and one diagonal correction.

The restriction and specialization argument excludes two terms for an explicit infinite family of full matrices. Independent review also verifies exact length three for their specified five-coordinate restrictions when N = 5q², q is positive and odd, gcd(q,5) = 1, and q ≡ 1 modulo 241. The upper construction remains five-dimensional; a three-term representation of the full matrices has not been established.

The possible contribution is the exact additive length and its arithmetic obstruction family. Linear-time cyclic inversion and general Green/quasiseparable structure are established subjects. Compare [Huhtanen and Perämäki](https://math.aalto.fi/~mhuhtane/manu.pdf) and [Graph-Induced Rank Structures](https://arxiv.org/html/1911.05858). [Read the checked five-point result]([private source omitted]).

### Sharp endpoint permutation rank

For dyadic N ≥ 8 over characteristic zero, the least possible quasiseparable order of the Fourier matrix under independent row and column permutations is N/4 + 1. Here quasiseparable order means the maximum rank across strict complementary upper-right and lower-left cuts. Double bit reversal attains the bound.

The potential novelty is the sharp minimax over all independent endpoint permutations. Double digit-reversal rank-one block structure already appears in [Delvaux and Van Barel’s official preprint](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW470.pdf), and must be credited. Comparison with the final article and subsequent literature remains open. High cut rank alone is not an arithmetic lower bound.

### Universal adjacent Hankel resultant identity

For two adjacent Hankel determinant pencils built from entries Tₑ₊ᵢ₊ⱼ(1 − a wᵉ⁺ⁱ⁺ʲ), the project proves an all-size factorization of their fixed-degree Sylvester resultant: explicit powers of w and w − 1 divide it, the remaining polynomial is reciprocal, and it compresses to a polynomial in w + w⁻¹. The initial w valuation is generically sharp; the identities survive singular specializations.

Closer comparison narrows the contribution: the same factorization mechanism extends to arbitrary square matrices in diagonal-scaling pencils, without a Hankel assumption. The exact closed-form exponents may still be original, but determinant identities, Newton-polygon valuations, and reciprocal-polynomial compression are established tools. This now looks more like a specialized lemma or application than a major standalone elimination theory. Compare [Sturmfels on resultant Newton polytopes](https://www.maths.tcd.ie/EMIS/journals/JACO/Volume3_2/m4496732732u7744.fulltext.pdf), [Nart on resultant valuations](https://arxiv.org/pdf/1205.1340), and [Uteshev and Baravy](https://arxiv.org/html/1603.08752). The broader project derivation awaits its separate proof review.

## Further substantial candidates

- A three-stage quasiseparable Fourier obstruction connecting internal permutations to classical discrepancy theory, with explicit endpoint restrictions.

- A one-layer obstruction for sums of independently ordered weighted-permutation Green operators, with sparse and low-rank corrections.

- An exact common-chirp sparse Fourier recognizer using a guaranteed nonzero bounded-degree phase eliminant. Its fast bound applies to the stated structured-input family.

## Results best used as supporting material

The certified sixteen-point factorization is a useful exact finite witness, but currently has neither an all-size coefficient generator nor a cost advantage. Tree-jet formulas, fiber recognizers, moving-cut certificates, and finite pencil exclusions are valuable lemmas or reproducibility examples; their precise contribution should be stated beside the classical tools they use.

The projective transfer-and-cycle solver needs especially careful attribution. Closely related bilinear constraints, 2-by-2 transfer maps, and cycle eigenvectors already occur in [de Beaudrap and Gharibian’s quantum 2-SAT algorithm](https://arxiv.org/abs/1508.07338) and [Arad and coauthors’ linear-time algorithm](https://theoryofcomputing.org/articles/v014a001/). A general-field specialization may still be useful, but a new general solver paradigm is not established.

## What would make a publication claim credible

1. Isolate one precise theorem with its field, allowed operators, endpoint conventions, and denominator guards.

2. Compare the exact statement and proof mechanism with the closest primary literature, including citation chains.

3. Package a short human-readable proof and small independent certificates; distinguish proof from finite tests.

4. Obtain expert scrutiny before asserting priority or choosing a submission venue.

Assessment dated 10 October 2026. No external submission, public posting, or expert outreach has been made.