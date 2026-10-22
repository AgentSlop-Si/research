# Independent review of the ALG-042 odd-affine cover obstruction

Date: 22 October 2026 (UTC).

## Verdict

**ACCEPT, within the stated scope.** No mathematical correction is required to the candidate theorem, its constructive avoidance lemma, or its uncovered-point count. Close only the constant-size odd-affine/translation-cover gate negatively. ALG-042 as a whole remains open.

The reviewed candidate is `THEOREM.md`, SHA-256

    e52c8dc40400dd31e9d6d4a09956b6a88ca839acd6f46b090d63c1a1430b38bc

The accepted conclusion is

    tau_aff(E) >= 2^floor((b+1)/2) >= sqrt(2L),  L=2^(b-1),

for the exact high-time marker-cylinder set in the pinned source, with affine images taken in the cyclic ring Z/(2^n), using odd multipliers. For k<2^d, d=floor((b+1)/2), at least

    (2^d-k)^floor(n/d) * 2^(n mod d)

points are outside any k such images. These are combinatorial covering statements, not operation lower bounds.

## 1. Source and integrity verification

Both source files were independently refetched through the GitHub connector at commit `ac6418587047464926c436ba21ce54d388f77616`, decoded from the returned base64, and compared byte-for-byte with the candidate's local copies. The returned Git blob identities were independently recomputed as SHA-1 of `blob <length>\0<bytes>`.

- [Pinned normalized target](https://github.com/AgentSlop-Si/research/blob/ac6418587047464926c436ba21ce54d388f77616/math/archive/objects/4c/4cf8e9936c6ff131769b212536f28b022892416346065bc12f1831e8f3395c14__NORMALIZED_PACKET_ESCAPE.md): 21,700 bytes; Git blob `b0e81996691257455991eb783c38a4a4a0fb4646`; current SHA-256 `c832a4df1322c7066cce9219423e94e94356b1ba185fbf5615e79b280b593611`.
- [Pinned independent baseline audit](https://github.com/AgentSlop-Si/research/blob/ac6418587047464926c436ba21ce54d388f77616/math/archive/objects/9f/9fce6c41e7201d6daa588b79b2ef8c1b17d466651a99d7d239d2cd8a85f94129__INDEPENDENT_NORMALIZED_FRONTIER_AUDIT.md): 17,065 bytes; Git blob `d255b895a8b93bcfcb58e9bd20cc2956b29b5470`; current SHA-256 `1fc59db37977862e889a1819b9eb3ed04b7eaa154b9a7891688bf0eb0236cd1b`.

All ten entries in the candidate's `SHA256SUMS` verify. The manifest's own SHA-256 is `8c808cbf06c52798029fb5704deddf8eca75225f6f56276ec695e9cbd9b7e2db`.

The archive filenames encode different, historical hashes. They are locators, not current-content integrity hashes. This review authenticates the published bytes at the pinned commit; it does not assert recovery of the historical originals or independently establish the history of sanitization. This limitation does not affect the proof against the explicit E defined in the inspected pinned bytes.

The target's sections 1, 3, 4, and 7 and the audit's sections 2 and 6 match the definitions and open cover question used by the candidate. The O(L) translation upper bound remains an inherited accepted result, not a new consequence of this lower-bound proof. The new lower bound does not use density or that upper bound.

## 2. Mathematical audit

### Exact marker containment

The source selects h-bit labels with MSB-first pattern `0^b rev_t(k) 0^b [free]`, and defines C(h,f) by congruence modulo 2^h. Therefore an element of C(h,f) has zero bits at positions h-b,...,h-1 of its padded n-bit expansion. The extension above position h-1 cannot alter those lower bits. The passage from the source cylinders to E subset Z_b(n) is correct; no reversal of low-bit and high-bit trie conventions occurs. Only the first zero marker is needed, so the restrictions on k do not conceal an additional proof assumption.

### Carries and low-digit induction

Write a partial input as P+2^m v, with 0<=P<2^m, and let the next complete digit have width d. For any integer representatives a,c, the output digit is

    (a v + floor((aP+c)/2^m)) modulo 2^d.

The quotient includes all carries from the lower prefix and the shift. A higher input continuation is a multiple of 2^(m+d), so its product by a changes no lower output digit. Reduction modulo 2^n similarly changes the quotient by a multiple of 2^(n-m), divisible by 2^d because m+d<=n. The calculation also holds for negative representatives when floor division is used.

Odd a is a unit modulo 2^d. Consequently precisely one next digit makes this output block zero. A family of k maps forbids at most k values, even when the forbidden values depend on all earlier choices. For k<2^d every partial path extends. The induction secures earlier output blocks permanently.

### Sliding windows and the last partial block

Let d=floor((b+1)/2). Every b-position interval starting at s contains the aligned block beginning at m=d ceil(s/d), since

    m+d-1 <= s+2d-2 <= s+b-1.

Because the interval lies within the n positions, this block also ends before n and is one of the complete blocks actually secured. This proves the terminal-partial-block case, rather than assuming n is divisible by d. The final n mod d input bits may be chosen freely. The worst zero run spanning nonzero complete blocks and a terminal short block is still too short to defeat the displayed interval argument.

### Counting witnesses and reversing maps

Every valid prefix has at least 2^d-k children at each of floor(n/d) stages. Different choice paths are different lower residues, and every final prefix has 2^(n mod d) distinct full extensions. Thus the candidate's product is a valid lower bound, not an assumption of independence between stages.

For a proposed cover by g_i(E), the appropriate avoidance maps are g_i^(-1), with inverse coefficients a_i^(-1) and -a_i^(-1)c_i modulo 2^n. They are again odd-affine. An x whose inverse images all avoid Z_b(n) also avoids every g_i(E). This proves the stated count for missed frequencies and tau_aff(E)>=2^d. The direction of the inverse-map argument is correct.

### Constants and asymptotic quantifiers

Since 2d>=b and 2L=2^b, 2^d>=sqrt(2L). The lower bound is pointwise for every admissible n,b and every family of fewer than 2^d maps; its coefficients may vary arbitrarily with n and b.

At b=floor(log2(n/(4 ln n))), b tends to infinity and

    n/(16 ln n) < L <= n/(8 ln n).

The source conditions b>=7 and L+2b<=n hold eventually. Hence the bound is Omega(sqrt(n/ln n)), equivalently Omega(sqrt(log N/log log N)). For every fixed K, sufficiently large sizes satisfy K<2^d, and no K-map family can cover E. Fixed b with n growing alone would not prove this divergence; the candidate correctly does not make that claim.

### Permitted map class and compatible-permutation remark

With the positive Fourier-sign convention, substituting s=at in z_s=omega^(cs)x_(a^(-1)s) gives (Fz)_ell=(Fx)_(a ell+ac). Varying c realizes every translation because a is a unit. Thus all odd-affine maps in the conclusion are permitted source-permutation/modulation frequency maps.

The additional remark is also valid as a combinatorial extension. A bijection on Z/(2^n) compatible with congruence modulo every 2^m induces a bijection on each set of lower prefixes: two equal-sized domain fibers cannot both inject into the same equal-sized output fiber. At levels m and m+d this makes the B=2^d extensions of a fixed lower prefix permute the B next output digits. The same branching proof applies.

This does not authorize those more general compatible permutations in the original Fourier algorithm. Arbitrary frequency-bit permutations do not in general satisfy congruence compatibility and are not included in the odd-affine conclusion. The review makes no claim about general F_2-affine maps, arbitrary bit permutations, noninvertible dilations, or non-affine algebraic recovery.

## 3. Independently authored controls

`independent_review_checks.py` was newly written for this review. It imports or executes no candidate or repository program. The supplied controls were inspected, not used as an executable oracle. The principal independent constructor tries digits by direct modular evaluation, without using the candidate's modular-inverse forbidden-digit formula; source toys are built outwards from allowed words and actual cylinders.

The recorded run in `INDEPENDENT_CHECKS.json` passes:

- 1,588,580 exact carry checks, including signed representatives and every full input at the tested small sizes.
- 425,986 exhaustive output-word checks that the complete-block condition excludes every b-zero window, including terminal remainders.
- 3,146,143 exhaustive families of distinct direct-evaluation mask pairs, checking both the zero-run avoidance count and the stronger complete-block count. Repeated masks need not be enumerated because repetition only weakens the asserted lower bound.
- 900 randomized families with a full-universe independent count at n<=12 and k=2^d-1.
- Four literal source-cylinder constructions, through the toy b=4,n=16 case, and 48 direct affine-image versus inverse-map witness checks. These small marker cases are explicitly outside the asymptotic b>=7 theorem regime.
- Thirty admissible b=7,...,12 adversarial cases, covering every possible n mod d. Each family has k=2^d-1 and deliberately distinct first-digit exclusions, so only one safe digit remains at the first stage. Final high input bits are set to all ones rather than to zero.
- Negative controls detect omission of prefix carries, choosing d too large, an even multiplier, the loss of the greedy guarantee at k=2^d, and failure of lower-prefix compatibility for bit reversal.

These finite controls corroborate the all-size proof. They neither establish optimality of the exponent nor provide a historical novelty assessment.

## 4. Disposition and recommended exact scope wording

Recommended dated task text:

> 22 Oct 2026: Constant-size odd-affine/translation cover gate CLOSED NEGATIVELY by independent verification: tau_aff(E)>=2^floor((b+1)/2)>=sqrt(2L), with the stated uncovered-count bound. The inherited O(L) translation cover remains. Faster selected-chirp/frontier construction, early-time outputs, causal/full recovery, and numerical/bit-cost qualifications remain OPEN. This is not an FFT operation lower bound or a novelty claim.

Attach immutable proof and review links when those artifacts are published. Preserve all prior histories and proof/novelty labels. Do not change ALG-042's overall TO RESEARCH status, owner, or priority 34 merely because this subsidiary route is now excluded. A table update should be restricted to the current constant-cover gate and next-action text, with the remaining obligations retained.

The candidate directory was left unchanged. This review made read-only external-source calls and local review-artifact writes only. No repository or table mutation was performed.
