# Independent final review: two-shear R30 Fourier interface

Reviewed 18 October 2026 UTC.

**Verdict: PASS within the stated representation and literal-evaluation model.**
No mathematical correction or additional erratum is required. The exact
construction, two-shear minimum over Gaussian dyadics, full cyclic-DFT
embedding, and charged arithmetic ledger are sound. Closing this separately
evaluated local-adapter route as an FFT optimization attempt is warranted.
This verdict does not establish an obstruction to other Fourier algorithms,
joint circuit simplification, auxiliary encodings, or packed arithmetic. It
makes no historical-novelty claim.

## 1. Reviewed release and independence

Reviewed directory: `../candidate`.
The reviewed `PROOF.md` has SHA-256
`56859de554108e86ce9a8735ef14750e8f7b30c3a9b50f88574f235430b7dfd7`.

I read the submitted proof, operation ledger, README, source/eligibility
metadata, verification source and reported results. I inspected the retained
original `graph_fusion.py` recognition, compilation, fused scalar rule and
fixed-grid checks, and its `baseline_r29/recycle_tensor.py` primitive builder.
I also read the earlier independent review and its mandatory scope erratum.

No submitted verification program or original R30 program was imported or
executed. The separate `independent_controls.py` in this review directory was
written after inspection and run locally. Its Fourier oracle uses a real
polynomial quotient, rather than the submission's Gaussian coefficient-lane
oracle. The nine release-file manifest hashes and all four referenced input
hashes were verified. Full machine-readable results and reviewed hashes are
in `independent_results.json`. No external repository or service was changed.

## 2. Exact adapter and genuine eligibility

The claimed conjugacy is correct:

    R = C^-1 diag(-1/2,1/4) C
      = -(1/8) [[1,-3i],[3i,1]],
    K = -8 Q^-1 R Q = [[1,3],[3,1]].

The displayed elementary identity is exact:

    H = diag(1,1/4) L(1) K U(-2)
      = diag(-8,-2) L(1) Q^-1 R Q U(-2).

The input shear, phases, R30 rule, output shear and final scaling occur in the
correct order. In particular the R30 outputs on the adapted input are
`(-(a+b)/8, -i(3a-5b)/8)`, and the completed outputs are `(a+b,a-b)`.
All non-twiddle adapter coefficients lie in `Z[i,1/2]`; no factor 1/3 is hidden.

The exact descriptor has `axes=1`, selected/parity masks 1, rho 3, opposite
forward/inverse tensor directions, three nodes, and no externally observed
intermediate output. These satisfy the inspected original guards and public
wrapper. The literal scalar computation matches `fused_graph` and its builder
operations. Consequently this is a source-verified eligible candidate for the
existing rule. The release correctly disclaims an original-compiler integration
run; this review does not supply one either.

The occurrence was deliberately introduced by a different pair program. It
does not invalidate the prior zero-match statement about unmodified radix-two
stage-component windows under monomial boundaries.

## 3. The two-shear threshold

The proof over `A0 = Z[i,1/2]` is valid for exact products on the same two
complex coordinates. The target determinant is the unit -2; each implemented
rho=+/-3 R30 factor has unit determinant, as does each elementary shear.
Therefore the nonzero entries of every intervening monomial factor must be
units. This rules out a nonunit boundary scaling whose reduction might conceal
a forbidden denominator or singularity.

Modulo 3, `A0/(3)` is the field `F9 = F3[i]`, because `X^2+1` is irreducible
over F3. Each R30 factor reduces to the identity: its off-diagonal coefficients
are multiples of 3 and its diagonal coefficient -1/8 reduces to 1. This is
unchanged by rho sign or tensor direction. Every monomial factor remains
invertible monomial. A product containing at most one elementary shear thus
has at most three nonzero entries after reduction. The reduced H has four.
That contradiction proves the claimed minimum; the exhibited two-shear
identity attains it.

The argument allows any finite number of these R30 factors and monomial
factors, in any positions. Its scope remains two complex coordinates and the
specified ring/factor types. It does not constrain an arbitrary larger
representation. The rational one-shear witness with 1/3 and -5/3 is correct
and demonstrates why the coefficient-ring restriction matters.

The general rescaling family with unit p,q and pq=4 is also correct. Neither
shear can vanish because 3 is not a unit in A0. Independent exact checks cover
20 real and nonreal Gaussian-dyadic unit choices in addition to the main
construction.

## 4. Complete cyclic Fourier transform and exact roots

The positive-sign radix-two DIT stage order, twiddle exponent, pair addresses
and input bit reversal yield the full matrix `F[r,c] = zeta^(r*c)`.
Substitution of the adapter identity into every butterfly preserves each
whole stage, hence the complete transform. This is a cyclic DFT construction,
not only a two-point identity or a Boolean-cube transform.

There are ND/2 pair occurrences. Whole-vector batching is compatible with the
original axis guard only when its dimension fits; the explicit axes=1 pair
fallback avoids exceeding the guard without claiming an arithmetic saving.

For N>=4 the relation `z^(N/4)=i` gives the stated basis of the cyclotomic
field over Q(i). Multiplication by each root power is a bijective coefficient
route with a fourth-root phase. The representation therefore supplies the
exact roots while keeping every actual R30 scalar call Gaussian dyadic.
For N=2 the separate root -1 convention is correct.

The actual evaluator's input/output domain is the explicitly represented
coefficient arrays. The formal complex-field identity is valid more broadly,
but does not imply finite exact encoding of arbitrary complex inputs. The
release makes that distinction and charges expanded storage, routing,
initialization, index arithmetic and output representation. At N>=4 the
literal implementation uses quadratic coefficient storage and
O(N^2 log N) scalar work. Decimal/IEEE output conversion is expressly outside
the implemented exact-output contract and is not treated as free.

## 5. Fully charged arithmetic, fixed grid and width

For one complex pair, after the common twiddle:

| Component | Real additions | Negations | Left shifts | Binary divides |
|---|---:|---:|---:|---:|
| Input U(-2) | 2 | 2 | 2 | 0 |
| Input Q | 0 | 1 | 0 | 0 |
| Literal R30 rho=3 | 8 | 6 | 4 | 4 |
| Output Q^-1 | 0 | 1 | 0 | 0 |
| Output L(1) | 2 | 0 | 0 | 0 |
| Output diag(-8,-2) | 0 | 4 | 4 | 0 |
| Total | 12 | 14 | 10 | 4 |

The ordinary pair has four real additions and two negations. In the stated
separate-factor evaluator, one literal R30 costs eight additions and each
nonzero complex shear costs at least two. The minimum of two shears therefore
implies at least twelve additions for a factor program containing an R30
block. This is an evaluator-specific lower bound. It is not the arithmetic
minimum for the resulting H map, which has the ordinary four-addition
implementation.

Both full-transform ledger versions are correct. The ordinary general-twiddle
count is `T = ND/2 - 3N/2 + 2`; i-twiddles number N/2-1. At N=256 the abstract
adapter transform requires 13,572 real additions versus 5,380 for the ordinary
transform, with the same 2,568 general real multiplications. Its 15,105 signs,
10,240 shifts and 4,096 divides also agree.

For the explicit 64-lane representation at N=256 there are 65,536 scalar pair
calls. The adapter totals are 786,432 additions, 966,720 signs, 655,360 shifts
and 262,144 divides. The corresponding lifted ordinary transform needs
262,144 additions and 180,288 signs. The additional twiddle-phase sign formula
`N^2(D-2)/8 + N/4` is correct, including the N=2 zero case. Direct enumeration
independently verified the twiddle categories and phase-sign totals through
N=4096. Batching changes call boundaries, not these executed scalar counts.

Three common reserve bits suffice for the fused evaluator at every stage:
inputs divisible by 8 make all four divisions exact, and completed outputs
remain divisible by 8. Two reserve bits fail on (4,0). The claimed 9M bound on
pair intermediates is valid and attained. Although the second R30 numerator
can superficially look bounded by 10M, its correlated terms combine as
`3a-5b`, bounded by 8M; the preceding tripling can reach 9M. Together with
stage growth by at most two, this gives `(9/2) N M0`, and therefore the stated
safe `5 N M0` signed-width criterion. Shifts/additions/divides are charged
word operations; the supplied O(ND ell b) upper bit-work bound is appropriately
separate from index work.

## 6. Fresh independent exact controls

The local run completed successfully in approximately 12 seconds and checked:

- Exact Gaussian-rational conjugacy, main adapter identity, rational one-shear
  counterexample to an unrestricted ring claim, and 20 unit rescalings.
- All 294,912 monomial/one-shear/monomial sandwiches over F9; none equals H.
- All 5,460 Fourier coefficients on coordinate basis inputs for
  N=2,4,8,16,32,64.
- All 17,488 expanded real-matrix entries for N=2,4,8,16, including every
  auxiliary real coefficient, rather than only the embedded input lane.
- Independently seeded randomized dense exact integer-coefficient transforms
  for every power of two through N=256, compared against direct DFT sums.
- Executed addition, sign, shift and division counts in every tested full
  transform, including zero-valued coefficients with no arithmetic skipping.
- 625 exact rational pair inputs; all signed extreme/zero pair corners for
  the sharp 9M peak; rejection of insufficient reserve bits and overflow.
- Four live algebraic mutations, each rejected by the butterfly identity.
- Independent enumeration of all twiddle categories/sign totals through
  N=4096, and release/source-reference hash consistency.

The Fourier checks work in `Q[z]/(z^(N/2)+1)` with real coefficients, retaining
Q(i) separately for N=2. The direct oracle accumulates all coefficients with
ordinary addition and cancellation. These finite tests corroborate the
all-size proofs; they are not used as substitutes for those proofs.

## 7. Disposition

Retain the exact construction and sharp, scoped Gaussian-dyadic shear-count
result. Close this literal adapter-only route as an FFT speedup attempt: it
manufactures eligible R30 work while tripling the butterfly additions and
adding shifts/divides. Scaling choices and batching do not remove that cost
in the declared model.

A jointly optimized program can simplify back to the ordinary butterfly.
A different cross-stage algorithm or packed representation requires its own
construction and full cost account. This review offers no obstruction to
those possibilities. The release honors the earlier erratum's separation of
same-coordinate support arguments, literal evaluator counts, and auxiliary
representations, and avoids claims of general Fourier lower bounds or
historical novelty.
