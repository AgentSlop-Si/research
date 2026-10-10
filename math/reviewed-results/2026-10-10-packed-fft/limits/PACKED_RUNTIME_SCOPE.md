# Practical scope of the accepted packed theorem

10 October 2026. This note preserves the accepted proof and makes no new
algorithm, performance, crossover, or novelty claim.

The source is *A cold packed finite-state radix-2 Fourier executor*,
`DYADIC_PACKED_THEOREM.md`, SHA-256
`bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`,
read together with `FROZEN_PROOF_REVIEW.md`. The review accepts its stated
finite-dyadic, relative-Euclidean-error word-RAM theorem at the paper level.

## 1. Exact necessary thresholds for this literal branch rule

Write `N=2^v`. The prescribed parameters are

    p = t + 10 + ceil(log2(v+1))
    k = ceil(log2(2v+p+6))
    b = 2(p+k+1).

The algorithm immediately selects its scalar fallback unless `64b <= v`.
Exact integer enumeration of all smaller admissible `v` gives:

| Accuracy exponent t | Smallest v passing guard | p | k | b | Necessary N |
|---:|---:|---:|---:|---:|---:|
| 2 | 5,120 | 25 | 14 | 80 | 2^5120 |
| 8 | 5,888 | 31 | 14 | 92 | 2^5888 |
| 16 | 6,912 | 39 | 14 | 108 | 2^6912 |
| 53 | 11,904 | 77 | 15 | 186 | 2^11904 |

These are **necessary eligibility thresholds, not sufficient successful-build
thresholds**. A passing instance must still finish every charged preparation
step and allocation within the literal `N`-instruction and `N`-word budgets.
Otherwise it also uses the scalar fallback. The proof establishes eventual
success, without supplying a numerical practical crossover.

At each displayed threshold, the prescribed largest power of two
`P <= v/(16b)` is exactly `P=4`; hence `d=2`. With `g=p+10`, the exact number
of mandatory response entries is

    T = (2^g-1) 2^(2bP) + d 2^(bP).

Each response entry occupies one model word. This count excludes coefficients,
helper tables, scratch, input/output, and the work of constructing each entry.

| t | Exact response-entry count T | Exact power bounds | Exact T/N bounds |
|---:|---|---|---|
| 2 | (2^35-1) 2^640 + 2·2^320 | 2^674 < T < 2^675 | 2^-4446 < T/N < 2^-4445 |
| 8 | (2^41-1) 2^736 + 2·2^368 | 2^776 < T < 2^777 | 2^-5112 < T/N < 2^-5111 |
| 16 | (2^49-1) 2^864 + 2·2^432 | 2^912 < T < 2^913 | 2^-6000 < T/N < 2^-5999 |
| 53 | (2^87-1) 2^1488 + 2·2^744 | 2^1574 < T < 2^1575 | 2^-10330 < T/N < 2^-10329 |

Thus the response tables can be tiny **relative to N** while already enormous
in absolute size. `T<N` alone does not certify the full preparation budgets.
No table was allocated for this audit: the companion script computes only
scalar integer parameters and counts.

## 2. What the machine model does and does not imply

The accepted RAM has word width `w=C(c)(v+1)=Theta_c(log N)` for a sufficiently
large fixed constant, and unit-cost word multiplication and division. Its
fixed-number-of-words arithmetic concerns these **growing model words**.
This is different from fixing machine words at 64 or 128 bits while letting
`N` increase: representing `Theta_c(v)`-bit states, intermediate integers,
and addresses then uses a growing number of fixed-width limbs, whose costs
must be charged separately. The theorem supplies no direct fixed-hardware
runtime bound or benchmark speedup.

Even an idealized range with `v <= 128` lies far below the smallest guard
threshold, `v=5120` at the least allowed `t=2`; larger `t` only increases `b`.
In particular, throughout ordinary 64/128-bit-addressable problem sizes this
literal algorithm selects the scalar branch. The `t=53` row requests normwise
relative error `2^-53`; it is not an assertion of binary64-compatible inputs,
outputs, intermediates, or per-component error.

## 3. Bottom line

The asymptotic theorem remains intact: cold work
`O_c(N(t+log2(v+1)))`, `O_c(N)` words, and all-input relative-Euclidean error
at most `2^-t` on its stated finite-dyadic domain. At fixed `t` this is
`O_t(N log log N)` in the stated word-RAM model.

The enormous numbers above follow from conservative constants and the
specific eager-table branch in this proof. They are **not intrinsic lower
bounds for optimized algorithms**, and they do not rule out different,
practical constructions. Conversely, this accepted theorem and its toy/exact
controls establish no measured industrial win, no production executor, and
no useful observed crossover. This audit undertakes no new algorithm search
and executes no uploaded or predecessor program.

Reproduction: run the newly authored standalone
`check_guard_thresholds.py`; its calculations use exact Python integers and
allocate no FFT or response-table arrays.
