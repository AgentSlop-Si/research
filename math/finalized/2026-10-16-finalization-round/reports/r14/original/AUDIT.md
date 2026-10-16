# R14 research audit

**16 October 2026. Decision: a proved-in-this-note mixed-prime scope extension,
with finite exact checks; no new sub-N-log-N algorithm. Independent mathematical
review and worldwide priority review remain unperformed.**

## What the user requested

Continue the research, rather than merely maintain attribution notices. The
primary goal remains an exact, arbitrary-input Fourier algorithm below N log N.
This branch returns to the project's Fourier matrix work, not CrocSwap's
integer-multiplication parameter and network progression.

## The mathematical result obtained

For every finite abelian G of order N=4L>=8,

    min_(independent row/column permutations) q(F_G) = N/4+1.

At N=4 the answer is 1. Here q is maximum off-diagonal cut rank, equivalently
the maximum upper/lower quasiseparable order. It is NOT transform running time.

The later reviewed Q05 report already proves the equality for all abelian
2-groups. The new note extends the stated project scope to mixed-prime N,
including 12,20,24,28,36,40 and48. The upper construction is an attributed
annihilator/coset method, not newly invented machinery. The lower uses the
already proved general Fourier rectangle estimate and the observation that
N/2+1 is coprime to N whenever four divides N. We claim this extension relative
to the read project reports, not global originality or absence from every
other account/repository file.

The accompanying constructor takes an explicit direct product, writes the two
permutations with O(kN) word operations and no dense group/Fourier table, and
supports independently shuffled representatives for validation. This improves
neither the arithmetic exponent of a DFT nor the conditional multiplication
kappa. It constructs labels only.

## Fresh completed runs

- Modular suite: PASS. All group types at orders 4,8,12,16,20,24,28,32,36,40,48
  were covered (38 isomorphism types at those listed orders), each with two
  representative choices and two exact splitting fields. Eight additional
  cyclic-layout controls, including order64, were also run.
- Total modular construction cases: 84; exact-field runs: 160.
- Total modular rank calculations: 11,640, including both corner orientations,
  empty endpoints and quotient cuts. They are not 11,640 independent transforms.
- Characteristic-zero suite: PASS. Thirteen group presentations at orders
  4,8,12,16,20,24, evaluated by exact SymPy cyclotomic-field arithmetic.
- Total characteristic-zero rank calculations: 492, including quotient cuts
  and empty endpoints. No floating-point rank threshold was used.
- Exact rational margins: 10,000 tested integer values L>=2; all positive.
  The theorem for every L comes from the written algebra, not these samples.
- Eight invalid-input controls were rejected.
- Five additional negative controls detect dropping the surviving quotient
  column at an odd cut. They also compare natural and constructed cut ranks.

All counts above are new in this run, and are not combined with earlier v10--v13
counts. The programs, full profiles, software versions and measured test-suite
durations are provided. Suite duration is not a multiplication/FFT benchmark.

## Example

For C12 the deterministic order on both endpoints is

    0,6,2,8,4,10,3,9,5,11,7,1.

Its upper and lower cut-rank profile is

    0,1,2,3,3,4,3,4,3,3,2,1,0.

The value four is optimal by the universal lower proof. Natural C12 order has
maximum off-diagonal rank six. These numbers compare rank structure only;
there is no claim that the reordered matrix-vector product is faster.

## What this does and does not contribute toward the goal

The mixed-prime extension removes a scope gap in the project's matrix analysis.
It prevents a proposed constant-/logarithmic-cut-rank shortcut from being
mistakenly reopened just by changing to mixed-prime bases. It does NOT establish
that all mixed-prime algorithms are slow, or that no faster FFT is possible.
A sparse multistage algorithm may have a dense high-cut-rank final matrix.

No replacement arithmetic recurrence below N log N was obtained. No new whole
FFT benchmark, integer multiplier, finite-field universal minimax lower theorem,
or optimal approximation gap is claimed. The constructed permutations alone
are not an FFT algorithm. Reporting this as a complete breakthrough would be
incorrect.

## Attribution and publication boundary

The moment estimate is from the user's existing Fourier manuscript. The
annihilator upper belongs to the classical dual-subgroup/coset method credited
by the Q05 attribution addendum to Delvaux and Van Barel. The mixed-prime
conclusion is presented as a scope-extension derivation/corollary of these
ingredients. Global priority is unverified. The final 2007 text and TW477 were
not freshly read in this run; the supplied TW477 link failed after redirecting
to institutional authentication. The current institutional abstract already
covers arbitrary finite abelian groups and subgroup rank-one tilings, so a
claim of first invention would be especially premature.

All current-conversation checkpoint ZIPs are unchanged. No remote GitHub
repository was written to during this run. R14 does not merge the two v13
branches or reuse their filenames.
