# Independent review of the subgroup Fourier baseline

Review date: 2026-10-10 UTC.

Verdict: PASS, accepted as an independently verified classical three-layer Fourier baseline. This receipt grants no novelty, unrestricted optimality, or FFT-improvement status.

The reviewed document is `input_snapshot/EXACT_SUBGROUP_FACTORIZATION.md`, SHA-256 `8cc956d12f0fab593051f826af6d0ad9144adfce44dca8fe22c9054b8aa34f5c`. The supplied document and programs remain unchanged. Its historical “awaiting independent review” wording is superseded for these exact bytes by this separate receipt.

## Accepted mathematical statement

For every odd prime p and every positive divisor d of p−1, put m=(p−1)/d. The supplied construction gives three p-by-p matrices with CBA=F_p, where F_p[k,j]=exp(2πikj/p). Their exact nonzero counts are

- A: 1+d(p−1)
- B: 1+2m+dm²
- C: 1+d(p−1)
- Total: 3+2d(p−1)+(p²−1)/d

Every specified edge is nonzero and every complex weight has modulus at most one. The count includes DC edges, all input processing, and output reconstruction. It is a scalar-circuit edge count with exact constants supplied. Coefficient construction is a separate cost if the chosen computational model charges it.

## Fresh proof

Choose a primitive root g, let h=g^m, and let a_i=g^i for 0≤i<m. The elements a_i h^t, 0≤t<d, partition the nonzero residues. Let z=exp(2πi/p) and w=exp(2πi/d).

The first layer computes the d character coordinates of each multiplicative orbit, with weight w^(−ℓt). The middle layer connects like character coordinates through

G_ℓ(c)=(1/d)∑_{v=0}^{d−1} z^(c h^v) w^(ℓv).

The last layer evaluates those coordinates using w^(−ℓs). For nonzero input j=a_i h^t and output k=a_r h^s, the length-three path sum is

(1/d)∑_v z^(a_r a_i h^v) ∑_ℓ w^(ℓ(v−s−t)).

The inner character sum is d when v=s+t modulo d and zero otherwise. Thus the coefficient is z^(kj). The zero input has coefficient one in every output, and the zero output is the sum of every input. This proves the full complex matrix identity, without any input-symmetry restriction.

For nonvanishing, consider ∑_v w^(ℓv)X^(c h^v mod p) over Q(w), for c≠0. Its d nonzero exponents are distinct, all coefficients are nonzero, its degree is at most p−1, and its constant term is zero. Because gcd(p,d)=1, the cyclotomic degree formula gives [Q(z,w):Q(w)]=p−1. Therefore z has minimal polynomial Φ_p over Q(w). A polynomial of degree at most p−1 vanishing at z must be a scalar multiple of Φ_p, but its zero constant term forces that scalar to vanish. This is a contradiction. Consequently every G_ℓ(c) is nonzero. The triangle inequality gives |G_ℓ(c)|≤1; the outer weights have modulus one.

There are m full d-by-d blocks and one DC edge in each outer layer. The middle layer has d full m-by-m blocks, 2m DC links, and its DC identity edge. The edge formula follows.

The real-variable minimizer of the total is sqrt((p+1)/2); admissible d must divide p−1. For p=11, d=1,2,5,10 gives 143,103,127,215 edges. Thus 103 is minimal within this divisor-subgroup family only. No global lower bound follows.

## Complete independent graph replay

`review_subgroup_graphs.py` was written for this review. It never imports or executes any supplied program. It reads the frozen graph JSON files as data, independently reconstructs the stated support/weight formula, and also sums every length-three graph path using exact Python integers.

For the identity check, path weights are accumulated in the group ring Z[C_p × C_d]. The d-coordinate is reduced by a freshly constructed Φ_d. A remaining polynomial in z of degree below p vanishes precisely when its p coefficients in Q(w) are equal, since it must be a multiple of Φ_p. This supplies an exact characteristic-zero test. No floating-point residual, random sampling, or finite-field transfer is used.

Verified totals:

- 17 of 17 supplied graphs
- All 28,209 Fourier target entries
- All 10,139 listed edge weights exactly nonzero
- Exact rational triangle bounds at most one for every listed weight
- The stated formula, primitive-root data, coset partition, vertex ranges, unique edge positions, and denominators
- The supplied divisor-optimization table for all 25 odd primes through 101
- All 24 supplied manifest bindings and all 25 files in the supplied ZIP against the snapshot
- Original source bytes unchanged throughout the replay

The 86 negative controls all reject: deletion of each layer's DC edge on every graph; omitted middle normalization on every graph with d>1; the wrong Fourier sign on every graph; and duplicate-edge, zero-edge, and single-phase corruption controls. The reducer also has explicit cyclotomic-zero and nonzero-unit controls.

Detailed results are in `INDEPENDENT_GRAPH_RESULTS.json`, with console output in `independent_graph_run.log`.

## Independent bounded search replay

The supplied exploration source was read only to identify its finite family; it was never imported or run. A separate program, `review_bounded_search.py`, enumerates that family and derives each inverse analytically from two nilpotent rank-one factors. Both inverse identities are checked exactly. It uses the real-cyclotomic basis 1,S1,S2,S3,S4, where Sj=z^j+z^(−j) and S5=−1−S1−S2−S3−S4. The embedding into Q(z) is checked exactly.

The replay reproduces all 14,212 unique bases, the complete one-sided score histogram, and the 982 bases passing the one-sided cutoff 61. All 964,324 ordered pairs of those 982 bases were checked. The minimum even-sector edge score is 58, attained by 14 ordered pairs; adding the unchanged 45-edge odd sector yields 103. Both the 4 bound on scaled inverse entries and the conservative 1,152 bound on integer coefficients are independently verified, excluding int64 overflow. No floating-point inversion is used in this replay.

This is a finite negative search result. The pair search does not cover combinations involving discarded one-sided candidates, arbitrary rational or complex bases, alternative sector decompositions, different widths, or other three-layer topologies. It supplies no impossibility theorem for a sub-103-edge F_11 factorization.

Results and a minimizing witness are in `INDEPENDENT_BOUNDED_SEARCH_RESULTS.json`.

## Primary literature and classification

The primary paper by Stephan Ramon Garcia, Gizem Karaali, and Daniel J. Katz, [An improved uncertainty principle for functions with symmetry, version 4](https://arxiv.org/html/1807.07648v4), was checked directly. Equation (9) and Definition 3.12 give character-weighted orbit-sum Fourier matrices. Taking H=⟨h⟩ and χ(h)=w^ℓ identifies each middle block here with the corresponding compressed matrix divided by d. For the trivial character, include the zero orbit; every unscaled zero-orbit entry is d, so the normalized DC entries agree as well. Theorem 5.5 gives nonvanishing of all minors over a prime field, stronger than the entrywise nonvanishing needed here.

This direct overlap supports classical-baseline classification. The review does not certify the exact edge-accounting presentation as a new literature result and does not require novelty to accept its correctness or usefulness as a comparator.

## Replay and preservation

Run `python review_subgroup_graphs.py` and `python review_bounded_search.py` from this folder. The graph replay uses only the Python standard library. The bounded-search replay additionally needs NumPy. Both read `input_snapshot` and write only reviewer results beside their own source. Run them in a copy if preserving the frozen output bytes is important.

`INPUT_SHA256.json` binds every supplied input file. `REVIEW_MANIFEST.json` binds every file in the frozen review folder except the manifest itself. `FROZEN_RECEIPT.json` records the accepted document, review, source, and result hashes. The separate review ZIP is a transport copy; the source directory has not been edited. No external publishing or other external state changes were performed by this review.
