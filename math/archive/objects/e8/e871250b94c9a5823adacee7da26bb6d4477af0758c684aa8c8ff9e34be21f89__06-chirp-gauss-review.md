# Independent audit: exact bounded common quadratic-chirp rank

Audit date: 2026-10-09 UTC.

## Verdict

The supplied note's scoped finite-field recognition and full-output transform theorem is mathematically sound under its stated fixed-rank and exact-arithmetic assumptions. I found no counterexample. The theorem recognizes a restricted family from raw samples; it does not compute the DFT after rejecting an arbitrary input, and does not establish a general linear-time FFT.

One algorithmic omission should be made explicit: return success with the empty, rank-zero representation on the all-zero vector before searching for a nonzero interior witness. A nonzero vector with no such witness can safely be rejected. The implementation also needs to abort a Berlekamp–Massey update before doing work for an order exceeding the bound.

I independently wrote and ran the included checker. No uploaded code was executed. The source note was the only supplied artifact; its statements about earlier programs and their test counts were not independently reproduced and must remain attributed claims.

## Provenance and scope

- Source: `RESEARCH (2).md`, Library identity `[private-id]`.
- Exact source size: 12,541 bytes.
- Source SHA-256: `503cf095980e7114f8d9bff39d7e33fe600a7747bfbb8756cd5c7729cf63c2b9`.
- Source preserved unchanged in `source/RESEARCH (2).md`.
- Audit concerns constructive correctness, endpoints, exact finite-field behavior, and operation accounting. A separate literature review is needed for any novelty claim. This report does not assert priority or a speed advantage over optimized FFT/NTT implementations.

## Formal statement audited

Let r >= 1 and N >= 3r. Let p be prime, N divide p-1, and omega have exact order N in F_p. The promised family consists of vectors

    x_j = omega^(a j^2) sum_(ell=1)^s c_ell omega^(b_ell j),  0 <= j < N,

where 0 <= s <= r, the b_ell are distinct modulo N, and every listed coefficient is nonzero. The case s=0 denotes the zero vector. There is a deterministic exact algorithm that decides membership, returns a verified representation on success, and computes the entire DFT on success in O_r(N) field operations. Failure means nonmembership in this family, not that the arbitrary-input transform was computed.

The field and its primitive root are supplied inputs. Table construction, candidate scanning, all raw-input checks, the base Gauss sum, and all N output writes are charged. Efficiently finding a suitable prime and root from N alone is not part of the proved recognition theorem.

## 1. Interior witness and endpoints

For a nonzero sum of s <= r distinct characters, any s consecutive zero samples would give a square Vandermonde system on distinct nonzero nodes. Its determinant is nonzero, so every coefficient would vanish, a contradiction. Thus a nonzero family member has no r consecutive zeros. Multiplying by a nonzero chirp does not change the zero pattern.

The allowed determinant centers are c in [r, N-r-1], an interval with N-2r entries. Under N >= 3r it contains at least r entries, so a nonzero family member has an eligible nonzero center. Set the window start to h=c-r; then h >= 0 and h+2r <= N-1. There is no off-by-one error in the supplied window.

The all-zero vector is the one exception to the witness argument and must be handled first. Our checker explicitly exercises zero vectors, nonzero vectors supported only at an endpoint, and valid signals having exactly r-1 initial zeros inside the scanned interval at the tight endpoint N=3r.

## 2. Eliminant: degree, nonzero coefficient, and phase root

For a permutation sigma of {0,...,r}, its determinant exponent is

    sum_i binom(i+sigma(i),2)
      = sum_i (i^2-i) + sum_i i sigma(i).

Only the final inner product varies. Strict rearrangement for the distinct ordered integers gives a unique minimum at reversal and a unique maximum at identity. The minimum is

    E_min = (r+1) r (r-1) / 2,

and the difference between maximum and minimum is

    D_r = r(r+1)(r+2)/6 = binom(r+2,3).

Dividing the determinant by t^E_min therefore gives an actual polynomial of degree at most D_r. Its constant term is the unique reversal contribution

    (-1)^(r(r+1)/2) x_c^(r+1),

which is nonzero when the chosen center is nonzero. This conclusion holds in the allowed prime fields, with no assumption that the degree is smaller than p. The standard nonzero-polynomial root bound still suffices even when D_r is larger than the number of candidate phases.

To verify the true-phase identity, put t=omega^(-2a), k=i+j, and y_(h+k)=x_(h+k) omega^(-a(h+k)^2). Then

    x_(h+i+j) t^binom(i+j,2)
      = y_(h+i+j) omega^(a h^2 + a(2h+1)(i+j)).

The final factor separates into nonzero row and column multipliers. Hence at the true phase the polynomial matrix has the same rank as the ordinary dechirped Hankel matrix, whose rank is at most r. The eliminant vanishes there.

The reported r=2 polynomial agrees with direct determinant expansion. We also compared 72 independently constructed eliminant polynomials, for r=1 through 6, against 696 Gaussian-elimination determinant evaluations, including checks of both endpoint coefficients.

## 3. Even-length quotient

The map a -> omega^(-2a) has kernel size gcd(2,N). For even N,

    omega^((N/2)j^2) = omega^((N/2)j)

because j^2-j is even. A representation at a+N/2 is consequently a representation at a with every frequency shifted by N/2. The canonical phase range has N/gcd(2,N) elements, and the phase-to-root map is injective there. At most D_r canonical phases survive the nonzero eliminant.

The quotient removes this universal parameter redundancy; it does not assert uniqueness of a signal's representation across all remaining phases. A signal may legitimately pass at several canonical phases. Returning any completely verified representation is sufficient.

## 4. Bounded recurrence and root-frequency test

Use the recurrence convention

    y_n + C_1 y_(n-1) + ... + C_s y_(n-s) = 0.

Its node polynomial is z^s + C_1 z^(s-1) + ... + C_s, not the unreversed coefficient list evaluated as an ordinary ascending polynomial. Our checker tests the correctly reversed representation when scanning the supplied roots.

For a genuine s-term character sum with nonzero coefficients and distinct nodes, the first s by s Hankel matrix factors as V diag(c) V^T and is invertible. Therefore the true minimal recurrence order is s and its node polynomial is the product over the s distinct nodes. At least 2s samples determine it; N >= 3r provides enough samples. This proves completeness of the bounded Berlekamp–Massey pass plus root scan.

For arbitrary input, prefix linear complexity is nondecreasing. A candidate can be rejected immediately when the next order would exceed r, before growing or updating arrays beyond the bound. Each retained order-increasing update raises the order by at least one, so there are at most r such updates and at most r cached-baseline inversions. The final abort need not perform an extra inversion. Other recurrence updates use the cached inverse and at most O(r) field work per sample.

Require exactly s distinct admissible Nth-root nodes, solve the nonsingular s by s Vandermonde system, and check every sample. These final checks give soundness even if the recurrence implementation makes a poor candidate choice. Genuine family members have nonzero recovered coefficients. The zero vector is handled as s=0.

## 5. Every-phase, every-length Gauss evaluator

Write d=gcd(a,N), m=N/d, A=a/d. For a=0 take d=N and m=1. In

    S_a(c) = sum_(j=0)^(N-1) omega^(a j^2 + c j),

write j=u+vm, with 0 <= u < m and 0 <= v < d. The inner sum over v is a geometric sum over a primitive dth root. It vanishes unless d divides c. If c=d w, the sum becomes d times

    T(w) = sum_(u=0)^(m-1) eta^(A u^2 + w u),   eta=omega^d.

For m=1, this is the N-spike formula and requires no modular inverse. Otherwise A is invertible modulo m.

For odd m, completion of squares gives T(w)=T(0) eta^(-w^2 (4A)^(-1)). One explicit length-m pass computes T(0).

For even m=2q, A is odd. Translating the summation index by q multiplies the summand by (-1)^(Aq+w), so T(w)=0 unless w has the parity of q. Set w0=q mod 2 and compute T(w0) in one length-m pass. For an allowed w, solve

    u = ((w-w0)/2) A^(-1) mod q.

When q=1 use u=0 without invoking an inverse modulo one. Shifting the summation index then gives

    T(w) = T(w0) eta^(-A u^2 - w0 u).

Changing u by q changes the exponent by a multiple of 2q because Aq+w0 is even. Thus the lift is immaterial. This covers even composite lengths, nonunit a, a=0, and the m=2 endpoint. The entire Gauss row can be shared by all modes having the same a, after which each output is a sum of at most r row entries.

We checked every a and every c at every length N=1 through 80 against a separately implemented direct sum: 3,240 rows and 173,880 entries. Recognition itself is only claimed for N >= 3r; testing the smaller Gauss endpoints does not extend that hypothesis.

## 6. Honest complexity ledger

With D=D_r, the original direct-permutation construction admits:

- O(N) field operations for the root-power table and scans, plus linear output writes.
- O((r+1)! r^2) conservative work for the determinant coefficients, with permutations generated sequentially.
- O(ND) for Horner evaluation over the canonical phase range.
- At most D candidate tests, each taking O(Nr + r^3) field operations for dechirping, bounded recurrence, root scanning, amplitude solve, and full verification.
- O(N+rN) for one base Gauss row and the complete accepted transform.

Combining gives O(NrD + (r+1)!r^2 + Dr^3 + N), as stated. The supplied note's O_r(N) conclusion is consequently valid only for fixed r. An explicit space accounting for the implementation is O(N + D + r^2), with no need to store all permutations; this is O_r(N), or O(N) when r is fixed. The baseline and Vandermonde inversions are bounded in number by a function of r.

In a word-RAM interpretation, p=N^O(1), modular multiplication/reduction assumptions, word-sized residue indices, and inverse/gcd costs must remain explicit. Extended-Euclidean inversions require O_r(log N) word steps under that model. Python arbitrary-precision runtimes below validate identities; they do not establish unit-word deployment or optimized FFT/NTT performance. Exact complex-field arithmetic is an algebraic extension only; stable floating-point recognition and finite-precision FFT complexity are not proved.

## 7. Independent results

All included tests passed.

| Test | Independent result |
|---|---:|
| Gauss rows, all phases, N=1..80 | 3,240 rows; 173,880 exact entries |
| Determinant polynomials, r=1..6 | 72 polynomials; 696 independent Gaussian evaluations |
| Structured recognition, r=1..6 | 252 runs; 10,810 direct-DFT bins |
| Exhaustive F_7^3, r=1 | 343 vectors; 55 accepted |
| Exhaustive F_5^4, r=1 | 625 vectors; 33 accepted |
| Exhaustive F_7^6, r=2 | 117,649 vectors; 1,513 accepted |
| Exhaustive membership total | 118,617 vectors; 1,601 accepted; no disagreement |
| Random dense vectors | 810 rejected |
| Forced r-1 interior zeros at N=3r | 24 valid signals accepted and transformed |
| Zero vectors / no-witness nonzero vectors | 6 zero successes / 6 correct rejections |
| Ordinary Hankel rank demonstrations | N=7,17,31,63,119,127; ranks=3,8,15,31,59,63 |

The exhaustive tests enumerate the entire structured family separately and compare the recognizer on every possible raw vector in the small field space. Every accepted vector also receives an independent direct-DFT comparison. Thus both false positives and false negatives are checked in those spaces. Random rejection by itself would not establish either property in general; the mathematical proof supplies the general argument.

The recorded checker runtime is an execution diagnostic only, not a benchmark. Exact counts, deterministic seed, source/checker hashes, and elapsed runtime appear in `independent_results.json`. The original note's claimed 15 test groups and other historical totals have not been audited because their code and logs were not provided.

## 8. What remains open

The fixed-rank family is a finite union of subspaces of dimension at most r. For r<N it is a proper measure-zero subset over C. In F_p^N the stated union bound N binom(N,r) p^(r-N) is valid, since smaller supports can be padded to r and there are at most N phase choices. The bound may be numerically trivial for some parameters; it is a coverage bound, not an FFT lower bound.

Letting r grow enough to cover arbitrary input destroys the present fixed-rank linear-time conclusion. Even a better eliminant construction alone does not remove the growing-r candidate, recurrence, and all-mode output costs. The audited result is a constructive exact structured fast path with raw-input recognition. It supplies neither a universal O(N) transform nor a lower bound ruling one out.

## Minimal corrections recommended for the source

1. Define s=0 as the empty representation and explicitly return zero output for x=0 before selecting the interior witness.
2. State that bounded BM aborts before performing an update whose new order exceeds r; distinguish node-polynomial convention from recurrence coefficients.
3. Make the supplied-prime/root assumption and fixed-rank memory qualification explicit.
4. Attach the original claimed programs/logs or label their historical test counts as unverified. Keep newly reproduced tests separate.
5. Retain the current non-universality, no-speed-benchmark, and no-priority qualifications.
