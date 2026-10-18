# Independent review: sixteen-point saturated residual

Date: 18 October 2026. Owner: M-MULTISCALE-CHIRP; related view Q24.

## Verdict

**PASS: exact formulation, symmetry, complete coverage, elementary controls, and resource-blocker interpretation only.**

The exact minimum is unresolved. The accepted interval remains **8 <= r* <= 15**. This review does not establish a legal attainment below fifteen, exclude all shorter patterns, or close the owner or related view.

Reviewed candidate: `/workspace/shared/sixteen_minimum_terminal_20261018_2054`.

The reviewed `REPORT.md` SHA-256 is
`684f31a2b2d8e66204ae3c69dc8c819d291ced773dedd7ffdfcb30c5366d0ae6`.

All nineteen candidate-manifest payload hashes and all three source-binding hashes matched. All nineteen payloads also matched the candidate distribution archive. The candidate directory was not changed. Review artifacts are separate. No external writes occurred.

## 1. Equivalence and legality

I checked the mathematical argument in addition to the finite computations. The accepted original-grammar normalization and the already accepted eight-odd-factor lower bound are inputs to this review; the latter's earlier proof and discovery were not rerun.

For a fixed count vector, the coefficient equations are precisely `P=c_0 Q` in `K[x]/(x^16-1)`. Adding `u*c_0-1` retains exactly the nonzero scalar multiples. A grouped polynomial with constant coefficient one splits over the algebraic closure into no more than its declared number of factors `(1-alpha y)`. Repeated roots, internal zero coefficients, lost leading coefficients, constants, and zero-parameter padding are included. No genericity or exact-degree assumption is needed.

Write `d_s=gcd(16,s)`, `m_s=16/d_s`, and
`R_s=product_(mu^m_s=1) G_s(mu)`.
For any such splitting,
`R_s=product_j(1-alpha_(s,j)^m_s)`.
Consequently nonvanishing of a grouped resultant is exactly all the original factorwise pole guards in that group, including zero-parameter cases.

Let `B=K[b]/I_n`, `D=product_s R_s`, and `delta=det(M_Q)`. The all-entry target identity establishes that `delta` is nonzero. In B, taking determinants of `P=c_0 Q` gives
`delta*c_0^16=product_s R_s^d_s`.
This proves the saturation assertion without assuming B reduced: `c_0^16` is a multiple of D, while `D^8` is a multiple of `c_0^16`, because every `d_s` lies between one and eight and delta is an invertible field element. The two principal ideals therefore have the same radical in B and give the same localization kernel. Thus
`I_n:c_0^infinity = I_n:D^infinity`.
The single Rabinowitsch equation neither drops a pole guard nor removes a legal degeneracy.

The explicit benchmark product `(1-x^8)(1+x^8)=0` is genuinely present in the unsaturated coefficient equations and is rejected by `u*c_0-1`. Retaining the scalar `c_0` rather than imposing `c_0=1` is correct.

## 2. Full target and symmetry

The independent checker uses sparse exact cyclotomic arithmetic with `a^16=-1`. It checked all 256 entries of `C Q(S)=16I` and independently all 256 entries of `Q(S) C=16I`, all 256 shift-normalization coefficient instances, and all sixteen coefficients of the Galois/stride symmetry. Altering one nonconstant target coefficient was rejected by the matrix comparison.

The full-target symmetry is valid. Substitution `x->x^3` followed by `a->a^9` restores Q, since the inverse of three modulo sixteen is eleven and `9*11^2=1 mod 32`. The resulting canonical stride permutation is `(1 3 7 5)(2 6)`, fixing four and eight.

For a nonzero parameter on a negative stride, reversing the binomial extracts only a nonzero scalar and a monomial. If the accumulated exponent is R, the shift identity converts `x^R Q(x)` to a scalar times `Q(a^(-2R)x)`, and substitution by the inverse sixteenth-root scaling restores Q. A parameter's guard is preserved because that variable scaling raised to `s*(16/gcd(16,s))` is one. A zero parameter is simply reassigned as a zero parameter and is never inverted. The Galois action is justified on algebraic solutions; the weak Nullstellensatz supplies such a solution whenever the displayed systems have any complex solution.

## 3. Complete finite coverage

The independent count enumeration first splits total counts into odd and even strides, separately enumerates four-part compositions, and interleaves the results. It does not import the candidate generator. The literal count is also checked against
`sum_(o=8)^r binom(o+3,3) binom(r-o+3,3)`.
Every stored representative and member is compared with independently calculated orbits; Burnside fixed-point counts provide an additional count control.

| Length | Literal patterns | Orbits |
|---:|---:|---:|
| 8 | 165 | 43 |
| 9 | 880 | 226 |
| 10 | 2,816 | 720 |
| 11 | 7,008 | 1,786 |
| 12 | 14,946 | 3,802 |
| 13 | 28,680 | 7,284 |
| 14 | 50,940 | 12,922 |
| Total | 105,435 | 26,783 |

All 105,435 patterns pad by zero stride-one parameters into the length-fourteen index, whose 12,922 orbits cover its 50,940 literal patterns exactly once.

The 28 pure-odd-stride characteristic-zero certificates were independently checked, including their actual displayed equation and multiplier metadata. They represent seven orbits across the seven layers, leaving **26,776 unresolved layered orbits**. Only one of those seven orbits is in the length-fourteen list, leaving **12,921 unresolved padded systems**. Subtracting seven from 12,922 would be incorrect; the candidate does not make that error.

## 4. Benchmark and independent controls

The benchmark count vector is `(2,2,2,2,2,1,2,1)`. A separate bit-mask representation of squarefree grouped monomials reconstructed every stored cyclic coefficient without importing candidate code. Its exact statistics agree:

- 2,916 grouped coefficient monomials;
- fifteen variables, including u;
- sixteen equations;
- 5,692 equation terms;
- maximum total degree nine.

Additional independent checks include:

- Grouped expansion versus individual-binomial expansion with repeated parameters, zero parameters, missing leading coefficients, internal zero coefficients, and degree-zero groups.
- Seventy-two exact resultant/determinant examples across all eight strides; sixteen examples are singular and fail the correct factor guard.
- A full mixed-product determinant identity with the benchmark multiplicities and coefficient degeneracies.
- The genuine unsaturated zero-product component and its saturation rejection.
- Rejection of a changed stored symbolic coefficient and a changed target coefficient.

The inspected candidate `verify_exact.py` was also replayed in the separate `replay/` directory and completed successfully. The replay result matches the frozen candidate verification result. Neither candidate generator nor elimination code was imported into the independent checker.

These numerical-instance controls supplement the general algebraic proofs; they are not offered as proofs for all parameter values.

## 5. Resource outcome and remaining blocker

The candidate elimination sources were inspected, but **the expensive elimination was not rerun**. The attempted engine is exact SymPy F5B over the stated degree-sixteen characteristic-zero field, in grevlex order. The child source sets CPU soft/hard limits of 180/185 seconds and a two-GiB address-space ceiling; the wrapper has a 210-second wall guard.

The frozen artifacts consistently report return code -24, namely SIGXCPU, no wall timeout, wall time 183.432574 seconds, child CPU time 185.414128 seconds, and peak RSS 104,476 KiB. The start log records `RUNNING`; the terminal status records the CPU resource limit; no basis artifact exists. These figures are archived telemetry, not measurements newly reproduced in this review.

This is a credible CPU-budget blocker for that specific attempted run. It provides no mathematical emptiness or nonemptiness result and no general algorithmic lower bound. A larger-budget run might still fail; no completion budget or checkpoint/resumption capability is established. The observed peak RSS does not support a claim that additional RAM alone would resolve the attempt.

The unfinished mathematical task remains establishing certified emptiness or producing certified legal solutions for sufficient indexed characteristic-zero systems to determine the minimum. The report correctly leaves that task open.

## 6. Frozen review artifacts

- `independent_checks.py`: fresh independent checker; does not execute elimination.
- `INDEPENDENT_RESULTS.json` and `INDEPENDENT_CHECKS.log`: independent results.
- `CANDIDATE_REPLAY.log` and `replay/VERIFY_RESULTS.json`: short candidate-verifier replay.
- `REVIEW_VERDICT.json`: machine-readable, narrowly scoped verdict.
- `REVIEW_MANIFEST.json`: final review-file hashes and exact candidate/source bindings.

**No minimum theorem is certified by this review.**
