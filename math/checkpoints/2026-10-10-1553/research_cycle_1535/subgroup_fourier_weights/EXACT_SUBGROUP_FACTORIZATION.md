# Exact three-layer Fourier graphs from multiplicative subgroups

Status: self-checked classical baseline, awaiting independent review. It is not a novel accepted result.

## Result and limits

For every odd prime p and divisor d of p−1, there is an explicit exact factorization

    F_p = C B A

with three p-by-p matrices and precisely

    nnz(A) = nnz(C) = 1 + d(p−1),
    nnz(B) = 1 + 2(p−1)/d + (p−1)^2/d,
    total = 3 + 2d(p−1) + (p²−1)/d.

Every specified edge is nonzero. All complex edge weights have absolute value at most 1. The convention is (F_p)[k,j] = exp(2π i k j/p); conjugating all weights gives the negative-sign convention.

This is a classical multiplicative-character / Rader-convolution specialization, independently derived here as an explicit three-layer edge-count control. No novelty, optimum over all graphs, FFT breakthrough, or sub-N log N algorithm is claimed. It improves the negation-paired control for many primes, but does **not** improve F_11 below 103 edges.

Examples (all exact checked):

| p | d | A edges | B edges | C edges | Total | Negation-pair total |
|---|---|---|---|---|---|---|
| 11 | 2 | 21 | 61 | 21 | 103 | 103 |
| 13 | 3 | 37 | 57 | 37 | 131 | 135 |
| 17 | 4 | 65 | 73 | 65 | 203 | 211 |
| 19 | 3 | 55 | 121 | 55 | 231 | 255 |
| 29 | 4 | 113 | 211 | 113 | 437 | 535 |
| 31 | 5 | 151 | 193 | 151 | 495 | 603 |
| 43 | 6 | 253 | 309 | 253 | 815 | 1095 |
| 71 | 7 | 491 | 721 | 491 | 1703 | 2803 |
| 89 | 8 | 705 | 991 | 705 | 2401 | 4315 |
| 101 | 10 | 1001 | 1021 | 1001 | 3023 | 5503 |

## Explicit graph and weights

Let m=(p−1)/d. Choose a primitive root g modulo p, set h=g^m, and take coset representatives a_i=g^i, 0≤i<m. Then every nonzero index has the unique form a_i h^t with 0≤t<d.

Set ζ=exp(2πi/p) and η=exp(2πi/d). Both internal layers have one distinguished coordinate 0 and coordinates (i,ℓ), 0≤i<m, 0≤ℓ<d. The numerical slot used in the JSON graphs is 1+i d+ℓ.

Layer A:

    u_0 = x_0,
    u_(i,ℓ) = Σ_(t=0)^(d−1) η^(−ℓt) x_(a_i h^t).

Define the explicit partial Gauss sums

    G_ℓ(c) = (1/d) Σ_(t=0)^(d−1) ζ^(c h^t) η^(ℓt).

Layer B:

    v_0 = u_0 + Σ_i u_(i,0),
    v_(r,ℓ) = 1_(ℓ=0) u_0 + Σ_i G_ℓ(a_r a_i) u_(i,ℓ).

Layer C:

    y_0 = v_0,
    y_(a_r h^s) = Σ_(ℓ=0)^(d−1) η^(−ℓs) v_(r,ℓ).

Those formulas specify every edge; unlisted matrix entries are zero. They are valid for arbitrary complex inputs, not merely real or subgroup-invariant inputs. No source-input preprocessing, output reconstruction, DC wiring, or identity edge is omitted from the count.

## Exact identity proof

For k=a_r h^s and j=a_i h^t, the x_j coefficient in the reconstructed nonzero output is

    (1/d) Σ_ℓ Σ_v ζ^(a_r a_i h^v) η^(ℓ(v−s−t)).

Character orthogonality makes the inner sum over ℓ equal to d if v=s+t modulo d and zero otherwise. The coefficient is therefore

    ζ^(a_r a_i h^(s+t)) = ζ^(kj).

The x_0 coefficient is one since it occurs only in the ℓ=0 channel. The distinguished output is x_0 plus all other inputs. Hence every entry of CBA equals its Fourier target.

## Nonvanishing and coefficient model

A and C contain only roots of unity and the scalar 1. Their edge weights are nonzero and have modulus 1.

For c nonzero, suppose G_ℓ(c)=0. Consider

    Q(X) = Σ_(t=0)^(d−1) η^(ℓt) X^(c h^t mod p)

as a polynomial over K=Q(η), with exponents represented in {1,...,p−1}. These d exponents are distinct, its constant coefficient is zero, and its nonzero coefficients are roots of unity. Since p and d are coprime, Q(ζ_p,η_d)=Q(ζ_(pd)) has degree φ(p)φ(d), so Φ_p remains irreducible over K. If Q(ζ)=0, Φ_p must divide Q. Both have degree at most p−1, so Q is a scalar multiple of Φ_p (or zero). Its zero constant coefficient forces that scalar to be zero, contradicting its nonzero terms. Thus every G_ℓ(c) is nonzero.

The triangle inequality gives |G_ℓ(c)|≤1. All graph weights therefore fit the fixed scalar bound 1 in this unnormalized Fourier convention. This does not imply a better-than-FFT operation bound.

The coefficients are supplied exact constants in the standard scalar circuit model. If coefficient construction must also be counted, it should be stated separately. There are only p−1 basic G-values: writing r+i=q m+s, 0≤s<m, gives

    G_ℓ(g^(r+i)) = η^(−ℓq) G_ℓ(g^s).

Thus m d=p−1 base sums of d terms suffice, plus root-of-unity multipliers. The JSON format repeats explicit terms to avoid relying on hidden coefficient aliases.

## Edge count and selection of d

A and C each have one DC edge and m complete d-by-d transforms, so each count is 1+m d²=1+d(p−1).

B has one distinguished edge, m edges from the ℓ=0 inputs to v_0, m edges from u_0 to the ℓ=0 outputs, and d complete m-by-m character blocks. Its count is 1+2m+d m².

At d=2 this is exactly the classical negation-paired total (p²+8p−3)/2. At d=1 it is the dense Fourier layer plus two identities, p²+2p.

The real-variable minimizer is d=sqrt((p+1)/2), but d must divide p−1. For primes admitting a divisor within constant factors of sqrt(p), this yields O(p^(3/2)) edges in exactly three layers. No assertion is made that every prime admits such a divisor, and O(p^(3/2)) is asymptotically worse than O(p log p) without the three-layer restriction.

For p=11, the possible d are 1,2,5,10, giving totals 143,103,127,215. Thus 103 is the minimum **within this subgroup family only**. Neither a global lower bound nor impossibility of a 99-edge Fourier assignment follows.

## Exact replay

Run:

    python exact_subgroup_certificate.py

The program is freshly written and does not run or import any inherited research program. It generates explicit graph JSON files, reloads each file, multiplies its edge lists, and verifies all p² entries over

    Q[z,w]/(Φ_p(z), Φ_d(w)).

This is a characteristic-zero check, not a floating-point fit or a finite-field-only transfer. Integer polynomial arithmetic is used throughout: the exported middle layer has a shared denominator d, so the multiplication checks C(dB)A=dF_p. Every listed edge is independently reduced and tested nonzero.

The completed run checks 17 graphs and 28,209 target entries. Results and SHA-256 bindings are in EXACT_SUBGROUP_RESULTS.json. The individual source code, graph files, and log are preserved.

## Primary literature and novelty scope

1. C. M. Rader, “Discrete Fourier transforms when the number of data samples is prime,” Proceedings of the IEEE 56 (1968), 1107–1108, DOI [10.1109/PROC.1968.6477](https://doi.org/10.1109/PROC.1968.6477). The primary DOI was identified; its page did not render in this research session.
2. D. J. Bernstein, “[Fast norm computation in smooth-degree Abelian number fields](https://link.springer.com/article/10.1007/s40993-022-00402-0),” Research in Number Theory 9, 82 (2023), especially §4.8.1–4.8.2. The publisher's full text explicitly presents Rader's multiplicative-index cyclic convolution and its folded version for subgroup symmetry. It directly substantiates the classical framework used here; it is not being cited as a statement of this exact edge-count formula.
3. S. Winograd, “[On computing the discrete Fourier transform](https://research.ibm.com/publications/on-computing-the-discrete-fourier-transform),” Mathematics of Computation 32 (1978), 175–199, DOI 10.1090/S0025-5718-1978-0468306-4. The author's IBM publication record states the convolution-complexity basis of the method. Its linked AMS PDF did not render here. This is related prior art, not a claim that this note implements a multiplicatively optimal Winograd codelet.

The construction is simply character decomposition along a multiplicative subgroup inside the classical Rader reduction. The primary literature search supports using it as a known-structure benchmark, not announcing a new algorithm. The independently useful deliverable is the fully specified three-layer accounting and exact replayable graph certificates.

### Closer prior art for the precise middle blocks

Garcia, Karaali, and Katz, [An improved uncertainty principle for functions with symmetry](https://arxiv.org/abs/1807.07648) (arXiv:1807.07648v4, 2021), Definition 3.12, define the same character-compressed Fourier matrices. Their entry formula is the character-weighted orbit sum used above. After the scalar normalization 1/d, the B blocks here are exactly those matrices: the trivial-character block includes index 0, and the others omit it. Their Theorem 5.5 proves that every minor of each such block is nonzero over a prime field. This provides particularly close prior art, stronger than the entrywise nonvanishing needed in this note. The present note does not claim that theorem or this character compression as new.

## Bounded F_11 follow-up, with a precise stopping point

A separate structured rational-basis exploration is recorded in F11_BOUNDED_RATIONAL_SEARCH.json, with fresh source explore_two_sided_even.py and its log. It starts from the six-dimensional even sector and leaves the five-dimensional odd sector unchanged. The source enumerates 14,212 rational star-and-difference bases; every proposed inverse is verified by exact integer matrix multiplication. All zero tests use exact coefficient vectors in the real cyclotomic subfield, not numerical tolerances.

All 14,212 one-sided candidates were checked. The two-sided check used the 982 candidates whose one-sided even-sector score is at most 61, covering 964,324 ordered pairs. It found no improvement on the even-sector score 58, and therefore no improvement on total 58+45=103. This is only a bounded negative result for the explicitly enumerated family. It is not an optimum over all rational bases, algebraic/complex weights, widths, pairings, or three-layer topologies.

The exact blocker for an F_11 improvement remains constructive: no explicit A,B,C with fewer than 103 counted nonzeros and CBA=F_11 has been produced. A generic full-spark graph and a non-Fourier weighting, including a 99-edge one, do not resolve that missing assignment.
