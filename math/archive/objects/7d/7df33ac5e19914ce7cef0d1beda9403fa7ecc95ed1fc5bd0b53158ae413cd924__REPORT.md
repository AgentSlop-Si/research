# Historical construction-source review: baseline queue 1, rows 0–39

## Result and scope

All **40 unique SHA-256 source texts, totaling 648,428 bytes**, were read in full from the specified canonical root and their exact hashes rechecked. The 157,890-byte pasted history was read in five contiguous character chunks. Character offsets use universal-newline display text (133,911 characters; 151,438 before normalizing 17,527 CRLF pairs); SHA-256 and inert copies preserve the original bytes. A truncated combined tool response was remedied by dedicated complete rereads of rows 1–3. The ledger distinguishes proof-bearing prose, conditional constructions, supporting implementation reports, duplicate-package reports, and a source-authored test log.

This closes **text-inspection coverage for these exact source hashes**. It does not certify every mathematical claim, inherited dependency, uploaded implementation, historical PASS, benchmark, literature priority, or asymptotic theorem. No uploaded executable was run or imported. All original files and existing seals remain unchanged. New checks are confined to the independently authored `independent_controls.py` in this report directory.

The chunk supplies useful exact constructions for restricted input families and several precise candidate interfaces. It does **not** establish a fresh arbitrary-input exact O(N) FFT. The claimed h24/interval-strip improvements and stability regularization are separate conditional branches whose upstream framework/compiler obligations remain material. Nothing here establishes that arbitrary exact sub-N-log-N computation is impossible.

## Strongest constructive implications

### 1. Preserve the exact restricted-family algorithms

**Weighted affine-cycle defects (row 1).** For positive-sign F with primitive dyadic root q, define Mx[j]=q^(bj)x[aj+c]. With a≡1 mod 4 and odd b,c, both the source index map and the Fourier-conjugate index map are full cycles. Direct substitution gives

Mhat y[k] = q^(-c a^(-1)(k+b)) y[a^(-1)(k+b)], and FM=Mhat F.

If u=(I−lambda M)x has s nonzeros and 1+lambda^N≠0, compute Fu as s geometric modes and solve (I−lambda Mhat)y=Fu by a cycle recurrence. This produces every Fourier output in O(N(s+1)) exact field operations with O(N) field registers, given the root and parameters. A majority ratio candidate can be found when the number of nonzero denominator entries exceeds 2s, but must always be verified by a full residual scan. Singular compatible inputs need additional kernel data or deliberate rejection. This is a restricted structured-input theorem, even when x is dense and fresh.

The source's detailed bill (12+2s)N+3 is an authored implementation count, not freshly instrumented here. The reported one-defect 14N+1 correction is one fewer cross-product comparison, saving two multiplications. Root discovery is not free; the shared contract supplies q. Exact complex/cyclotomic registers are not bounded machine words.

**Low-order recurrence full DFT (rows 16/22).** For A(z) and Q(0)=1, retain all coefficients of D=QA, including the right tail. Fold D modulo z^N−1 only for evaluation. At Q(omega^k)≠0, divide the evaluated folded numerator by Q. Recover each exceptional bin directly from A; a degree-d nonzero Q has at most d such bins. A true order-d input recurrence gives a folded numerator of degree <d and a complete O(N(d+1)) field-arithmetic evaluator. Detection, root generation, singular bins, and output are all part of the bill. This is classical structured computation with a useful complete interface.

**Few-coset sparse expansion (row 31).** A support in c small subgroup cosets yields small transforms plus c geometric modulations, with complete output cost O(Nc+cd log d+support setup). This is a good exact positive control; arbitrary prime-length supports do not have those intermediate subgroups.

### 2. Evaluate the fused program, not merely its written depth

Rows 4/33 give dense exact O(N)-field-operation all-pass unitaries. Short scalar-unitary words in one fixed phase-rotated cycle family must pair; their induced-one norms force logarithmic factor counts for a flat target. The family and cutoff are essential.

The same source supplies a decisive warning against overextending such a gate. For N=2m and M^N=−I,

product over lambda^m=1 of K(lambda M)
= [(2^m+1)I+(2^m−1)M^m]/2.

The left side contains m nominal stages; the right side applies in O(N) field work with paid gauge/power preparation. It has only two entries per row and is not Fourier-flat for N>2. It proves that factor count alone is not a runtime lower bound when fusion is allowed. The scalar 2^m also has Theta(N) bits, so the field result is not a bounded-word/bit result.

### 3. Use covariance and parameter compatibility after rank/norm gates

Rows 12/25/28 construct meaningful cheap wide operators:

- Tridiagonal sandwiches A=L^-1 T R^-1 give exact O(N) applications for supplied one-channel separated generators. Small contiguous T-components force logarithmic explicit stage count. Large irreducible cores escape that particular gate.
- Path Green operators have a diagonal-plus-rank-two Fourier conjugate from the two missing wrap edges; the inverse target bound 73/18 permits controlled approximation transport without a transform oracle.
- Haar–Green insertion escapes every fixed p<2 norm budget, while retaining the prior path-pair robust-cut argument under its stated parameters.

None of density, high cut rank, large induced norm, or cheap conjugacy is the missing Fourier factorization. For an actual candidate require AZ=DA and first-column normalization, then one compatible set of generators for the entire transform. The whole-network mincut source (row 34) is a necessary relaxation, not a coefficient constructor. Its concrete N64 witness cannot be re-certified from this prose alone: exact permutation, cut partition and minor indices reside in an external JSON dependency.

### 4. The exact sparse bottleneck is joint geometric evaluation

The Bostan–Mori rational cancellation in row 3 is valid on a pole-free grid. Raw rational samples recover amplitudes divided by 1−c w_s^S. Preweighting or modular numerator correction repairs them. At resonance, the cancelled numerator discards genuine kernel coordinates: restore impulses S b_s at matching grid points. A derivative limit of the fixed-c zero summand cannot recover them.

The literal fused schedule still pays for initial oversampled numerator evaluation and leaf transforms. Standard costs remain O(N log k), or worse when the fused depth is too large. Row 31 likewise observes that advancing modal states already costs O(N) for block width at least k. The unaccelerated part is applying the geometric evaluation matrix to its sequence of fresh modal states. A valid next constructor must jointly accelerate those applications, not call a fixed matrix or precomputed coefficients free.

### 5. Keep the conditional stability route separate

Row 18 proposes a real conditional mechanism: transparentize an effective exact local sub-m-log-m DFT into a two-bank unitary endpoint, certify every local shear prefix, and select a slowly growing block size with a bounded printer. Serial local execution can reset conditioning at unitary boundaries.

Row 38 identifies the correct condition identity for a local prefix S with idle complement: max(1,sigma_max(S))/min(1,sigma_min(S)). Local condition alone is insufficient; determinant-modulus one anchors it. Simultaneously active different blocks need their separate extrema. Restoring zero workspace on actual inputs is weaker than restoring arbitrary dirty workspace in a full-state unitary map. Exact endpoints do not erase roundoff.

The local #130 instantiation, coefficient certificate, explicit normalized macro schedule, preparation runtime, and all-length extension remain dependencies. A short printed program is not automatically a short executed program; use explicit unrolling or a separate preparation cost certificate. This review does not promote the conditional corollary to a verified new stable FFT theorem.

## Defects and required qualifications

1. **Actual literal theorem defect, row 12:** Section 1 permits negative alpha using alpha*Delta*delta<1, but the proof requires |alpha|*Delta*delta<1. With alpha=−10, Delta=1, p=4/3 and delta=1/2, the written assumption holds while its displayed norm upper bound is 1/2. A Cayley transform of a real symmetric one-edge adjacency has spectral radius 1, hence any induced norm is at least 1. The positive parameters used later are unaffected. Correct the hypothesis, not the original sealed source.
2. **Small-characteristic qualification, row 3:** Ordinary derivative quotients H^(mu)/Q^(mu) at a fully cancelled multiplicity-mu root require mu!≠0 in the field. Use Hasse derivatives or explicit factor cancellation in small characteristic. The modal impulse correction itself remains the safe statement.
3. **Word-RAM prototype gaps, rows 9/21/35:** Exact sampling needs finite randomness/capped-rejection failure accounting or an expected-time statement; inputs need a bounded common scale; rows must be fully built and already packed before online lookup; phasors, division, intermediate widths and output scaling must be charged. Lazy rows, NumPy exponentials and online scalar repacking do not execute the cold theorem.
4. **Accuracy wording:** A maximum-coordinate bound relative to input ||x||2 is not vanishing relative output l2 error or “relative energy error.” Polylogarithmic coordinate-sampling budgets still have large relative RMS l2 error on flat dense inputs. Exact arithmetic of a sampled surrogate does not give exact input Fourier outputs.
5. **Scope of rank results:** Complex Frobenius/Hermitian arguments do not automatically extend to arbitrary finite characteristic. Prime Chebotarev consequences are characteristic-zero dependencies. Composite endpoint permutations can weaken contiguous-minor gates. Rank/channel/displacement budgets only imply running time in an explicitly priced implementation architecture.
6. **Partial-output shorthand, row 39:** Write O(N(1+log q)), not literally O(N log q) at q=1. The prose's stated Theta(N) constant-q case already recognizes this.
7. **Historical audit assertions:** Source self-descriptions such as “independently verified,” duplicate-archive byte comparisons, operation instrumentation, tests, modular determinants and benchmark speedups remain historical source claims unless separately linked to exact execution artifacts. Row 30 is a mixed exact/numerical source log, never fresh evidence from this pass.

## New independently executed controls

`INDEPENDENT_CONTROLS.json` and its matching log record only this pass's new code:

- 140 exact affine-cycle source-to-full-spectrum checks over F97 at N=4,8,16, plus 28 singular declines; source/target intertwining and cycle edge product checked separately
- 1,040 exact pole-free rational alias cases and their amplitude corrections, plus 28 exact resonant impulse cases
- Exact rational all-pass unitarity, induced-one norm and nonflatness at N=3,…,8
- Exact half-cycle rational fusion and scalar Gram identities at N=4,6,8
- h24 combinatorial/role/residual/padding arithmetic and rational exponent slack, with **framework transfer explicitly not checked**
- The negative-alpha literal-hypothesis counterexample above

These controls do not run source implementations, verify source operation counts, materialize enormous networks, execute Lean, prove all-length complexity, test realistic wall time, or establish prior art. General algebraic conclusions rely on their stated derivations and hypotheses, not finite PASS counts.

## Prior-art boundary

A limited fresh primary-source check supports three comparator facts:

- [FFTW's pruned FFT notes](https://fftw.org/pruned.html) explicitly describe O(N log K) input/output pruning and the arbitrary-output small-transform decomposition, and caution that arithmetic savings need not improve wall time.
- [Alman's finite-field lookup paper](https://arxiv.org/abs/2211.04643) states the constant-size-field Walsh–Hadamard O(N log N/log log N) bit bound. It is not an arbitrary exact complex FFT theorem.
- [Tao's prime cyclic uncertainty paper](https://arxiv.org/abs/math/0308286) states the support-sum bound and sparse-polynomial zero consequence used by row 31.

This is not an exhaustive novelty search. The pinned 2026 OpenAI/CrocSwap snapshots and their claimed improvements were reviewed as source dependencies, not freshly audited upstream theorems. Their historical revision status must stay attached to any comparison.

## Integration instructions

Use `COVERAGE.json` for exact per-hash claims, defects, dependencies, constructive implications, classification and full-read evidence. It contains only queue-1 rows 0–39 and does not overwrite the main auditor's integration ledger. `SOURCE_HASHES.sha256` uses the required canonical root; `SEALED_MANIFEST.json` seals every new report artifact and records the source manifest. Run `verify_seal.py` to check report integrity and all original source hashes.

The appropriate next constructive specification is a uniform fresh-input/all-output exact map, with full-state correctness and restoration, coefficient/root preparation, routing, representation, fused execution cost and recurrence all explicit. Keep restricted positive controls and adversarial negative controls alongside it. Passing a gate is permission to continue research, not evidence the Fourier constructor exists.
