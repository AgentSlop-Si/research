# Common node criterion and literature boundary

10 October 2026. Supporting author note for the two all-order theorems in this folder. The classical criterion below organizes the exact legal-node problem; it is not claimed as new Prony or scroll theory.

## A precise finite-node criterion

Work over C and fix one orientation (ε,δ). A triangular coefficient array supported on r+ℓ≤N−1 can be divided by its nonzero Gaussian factors. Write the resulting sector sequences as t_(r,ℓ), 0≤r≤N−1−ℓ. Let L_ℓ=N−ℓ be their lengths.

For a positive integer m, the following are equivalent:

1. The array is a sum of at most m same-orientation legal banks with distinct effective finite nodes after coincident nodes are merged.
2. For some d≤m there exists a monic squarefree polynomial g(z)=Σ_(k=0)^d g_k z^k, g_d=1, whose common recurrence holds in every sector:

   Σ_(k=0)^d g_k t_(r+k,ℓ)=0 whenever 0≤r and r+d<L_ℓ.

The zero array may instead use d=0 and no banks. Zero nodes are allowed in this formulation, so g(0) is not required to be nonzero. For the restricted β=1, nonzero-node class, add g(0)≠0. A squarefree polynomial is essential: a repeated-root annihilator alone permits polynomial-exponential or confluent atoms that are not ordinary legal banks.

Proof of necessity. Merge all banks with equal α in this orientation by adding their sector amplitudes. Let g be the product of z−α over the remaining d finite nodes. Each node power sequence obeys the recurrence, so each sector sum does. The polynomial is squarefree by construction. Merging is legitimate over C even if original β values differ: any prescribed merged amplitudes can be realized at the same α by choosing a nonzero β for which 1−α^N−β^N≠0 and applying the inverse finite-character transform.

Proof of sufficiency. Let x_1,…,x_d be the distinct roots of g. If L_ℓ≥d, recover sector amplitudes A_(i,ℓ) from the first d moments by the invertible d×d Vandermonde matrix (x_i^r)_(r=0,…,d−1). Recurrence induction gives every remaining moment. If L_ℓ<d, the L_ℓ×d truncated Vandermonde has full row rank; choose amplitudes realizing the prescribed moments. Such sectors impose no recurrence. These choices use the same nodes across all sectors. For each node choose nonzero β_i avoiding the finite forbidden set β_i^N=1−x_i^N. Then Δ_i≠0 and all amplitudes are realized by w_(i,j)=Δ_i Σ_ℓ A_(i,ℓ)β_i^(−ℓ)q^(−εδjℓ). If g(0)≠0, simply choose β_i=1. This proves legal exact attainment.

The criterion gives a four-orientation exact feasibility formulation. Introduce four triangular arrays t_o whose Gaussian-weighted contributions sum to the target coefficient array at every overlapping coordinate. Require one squarefree shared recurrence polynomial g_o for each orientation. Minimizing Σ_o deg(g_o), with the zero convention, gives exactly the permitted bank rank over C. The cross-orientation summation equations and common nodes must both be retained. Testing independent scroll ranks of four rescaled copies of the whole target is not equivalent.

For recurrence polynomials and moments defined over a characteristic-zero field k, sufficiency holds over their splitting field. If g_o have degrees d_o, the compositum has degree at most Π_o d_o! over k. This is a sufficient field bound, not a claim that every minimal complex decomposition descends to k.

## Classical source matches

Sturmfels and Sullivant describe the rational normal scroll by x_ij=s^j t_i, followed by concatenated Hankel matrices and their secant minors in Section 5, Theorem 5.7. Dividing by the nonzero Gaussian factors identifies a bank's single orientation with exactly this finite-node chart, with the degree-zero sector retained as a cone vertex. The correspondence and shared-node recurrences are classical; the four differently embedded, overlapping orientations are the application-specific part.

Source: Bernd Sturmfels and Seth Sullivant, Combinatorial secant varieties, Section 5 and Theorem 5.7. https://arxiv.org/pdf/math/0506223

Comon, Qi and Usevich study simultaneous decompositions with shared vectors and sector-dependent coefficients, identifying their binary case as a rational normal scroll in Section 2.4 and distinguishing rank from border rank. Their framework supports the common-node interpretation. It does not by itself determine the legal finite-node rank of a target in this four-orientation union.

Source: Pierre Comon, Yang Qi and Konstantin Usevich, Identifiability of an X-rank decomposition of polynomial maps, Sections 2.4 and 3.2. https://arxiv.org/pdf/1603.01566

Potts and Tasche connect exponential sums with annihilating polynomials, Hankel systems and Vandermonde recovery. The criterion above is the simultaneous truncated-sequence version of this classical mechanism, stated with the nonzero-node and squarefreeness guards needed here.

Source: Daniel Potts and Manfred Tasche, Parameter estimation for exponential sums by approximate Prony method, Section 2. https://www-user.tu-chemnitz.de/~potts/paper/prony.pdf

## How to describe the two new author results

The universal theorem U_k(N;q)=2N−2 is a sharp linear-spanning result for fixed legal parameter configurations. Its count is intrinsic to a preselected programmable dictionary. It does not establish that a device charges one unit per bank or that evaluating it is fast. The proof is elementary support dimension plus explicit simultaneous interpolation. It is an all-order addition to the present manuscript, not a historical-priority assertion.

The inverse-shift separation R_N(S^−1)=N−1 and border R_N(S^−1)=1 concerns a nonclosed dictionary of permitted finite-node banks. The limiting inverse shift is the omitted infinite-node endpoint of the sector-zero rational normal curve. If X is instead defined to be the closed projective scroll, this endpoint already has X-rank one. Therefore this is not an exotic new rank/border-rank separation for a closed projective variety or a claim about tensor border rank. Its use is to quantify how badly closing this particular legal dictionary can change the bank-count question, even after all four orientations are allowed.

Classical binary monomial rank is also nearby: the opposite-orientation sector vector with its only nonzero coefficient at r=1 is the moment-coordinate version of a binary monomial. Carlini, Catalisano and Geramita give a general monomial Waring-rank formula. No count-preserving equivalence between the full signed-bank dictionary and a single Veronese variety is asserted. The direct exponential Vandermonde lower bound is what excludes improvements from the other orientations here.

Source: Enrico Carlini, Maria Virginia Catalisano and Anthony V. Geramita, The solution to Waring's problem for monomials. https://arxiv.org/abs/1110.0745

A limited primary-source search did not locate these exact fixed-bank statements. That is not evidence of historical novelty, an exhaustive bibliographic review, or a specialist assessment. The tools and geometric mechanisms are classical.

## Remaining Fourier-specific gap

Neither all-order theorem proves an asymptotically smaller Fourier-specific upper bound than 2N−2, a formula for M_C(N;q), or optimality of fourteen at N=11. The N=11 sextic works because all required edge recurrences are compatible with a squarefree nonzero-node polynomial and the other row minors remain nonzero. For smaller common node sets at general N, a dimension count for the annihilator equations is not enough: one still must prove consistency, a legal squarefree solution, all coupled-axis conditions, and the remaining row ranks. Those are the precise unresolved steps for extending the special fourteen-bank mechanism to an infinite family of better-than-universal Fourier bounds.
