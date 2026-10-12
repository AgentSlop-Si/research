# ACWL independent bounded lift audit

Date: 2026-10-12. Disposition: **ACCEPT_BOUNDED** of the restricted no-lift theorem below. This accepts a precisely scoped obstruction and the associated indexing controls. It does not accept an exact O(N log log N) DFT algorithm, reject arbitrary fiber-scattering extensions, or establish novelty.

The supplied ACWL manuscript was read without modification. Source SHA-256: `a3f9ab9b869c9e8a807baf50b1059899b78b1db5b2053938b5ab7504bf92e3c0`.

## Finding and exact scope

For the positive-sign, bit-reversed-input DIT partial FFT prescribed in ACWL §7, **no invertible correction built solely from the centered relative shears, arbitrary diagonals, sums, products, and invertible inverses can lift r-covariance to any s-covariance with s>r**. This holds at every dyadic length and at arbitrary packet width/depth. In particular the core-only N=256, 2→4 experiment in §13 cannot succeed.

The obstruction does not apply to the full residue-fiber commutant. Standard FFT continuation is an exact positive control inside that larger commutant. An optional QTGF/scattering operation that supplies new couplings can escape the obstruction; it still needs an explicit construction and a uniform cost proof.

## Algebra and proof

Work over C, or any field containing a primitive N-th root omega, with N=2^w and 1≤r<s≤w. All coordinates are zero-based. Write q=2^r, d=N/q, Q=2^(s−r), and eta=omega^d.

Use permutation matrices with H e_x=e_(H(x)). The source's relative shear, obtained by pi_c S^-1 rather than using pi_c itself, is

`H_c(x) = 1 + (1 + c q)(x−1) mod N`.

Every H_c is a permutation and fixes coordinate 1. For the projector E=e_1 e_1^T, this gives EH_c=H_cE. All diagonal matrices and all weighted versions of these permutations also commute with E. Commutation with E is preserved by sums, products and inverses of invertible matrices. Thus every matrix in the specified rationally closed algebra is block diagonal for `{1}` and its complement. An invertible C in this algebra satisfies

`e_1^T C = lambda e_1^T`, with lambda≠0.

This covers Green resolvents and rational Cayley transforms only when their matrices are built from these generators. A separate solver or a new fiber permutation is not covered merely because it has the same coarse-fiber support.

For positive-sign unnormalized DIT, input bit reversal followed by stages 1 through r gives

`M_r[b q + ell, a + d t] = eta^(ell t)`,

where a is the reversal of the w−r bits of b, 0≤ell,t<q, 0≤b<d; all other entries vanish. Each block is an invertible q-point Fourier transform. Directly, M_r X_r=Z_r M_r.

Row 1 of M_r has support `{d t : 0≤t<q}` with values eta^t. Let D=N/2^s=d/Q. Right multiplication by X_s shifts this row's support to `{d−D+d t}`, with values eta^(t+1). The reversal of d−D in w−r bits is Q−1. Hence for P=M_r X_s M_r^-1,

`e_1^T P = eta e_(q(Q−1)+1)^T = eta e_(2^s−2^r+1)^T`.

The two sides of the claimed lift equation CP=Z_s C would therefore have row 1

`lambda eta e_(2^s−2^r+1)^T`

and

`omega^(N/2^s) lambda e_1^T`.

These are nonzero rows on different coordinates. The lift is impossible.

The argument uses exact algebra over the stated field; finite-field tests below check the implementation and indexing rather than extrapolating to an all-length theorem from numerical failures.

## Decisive size and scope controls

For N=256, r=2, s=4, write i=omega^64. Then row 1 of M_2 has entries `(0:1, 64:i, 128:−1, 192:−i)`, and row 1 of P is exactly `i e_13^T`.

Over F_257 with omega=3 this is `P[1,13]=241`, with every other entry in that row zero. Standard FFT continuation C=M_4 M_2^-1 succeeds, commutes with Z_2, and has row 1

`(1:1, 5:64, 9:249, 13:2)`.

Its non-singleton support is entirely in the residue-1-mod-4 fiber. Thus this is a positive control for the full coarse commutant and a direct witness that the full commutant is larger than the centered-shear algebra.

Additional boundaries:

- The safe permutation x↦x+2^r mod N also moves coordinate 1 while preserving residues modulo 2^r. Adding arbitrary such within-fiber couplings breaks this proof; it does not by itself provide a fast lift.
- The statement concerns the prescribed partial-FFT base. It does not cover every r-covariant M. For example M=F already has full covariance and admits C=I, although that does not supply a cheaper algorithm.
- Invertibility is essential. C=0 satisfies the intertwiner equation trivially but computes nothing useful.
- The original full-period affine cycles pi_c do not fix 1. The unweighted relative shears all commute with one another because they are multiplications about the same center. Noncommutation or cut tests for pi_c do not transfer automatically to H_c. Arbitrary weights may destroy pairwise commutation, but not the shared singleton invariant.

## Review of the remaining claims

The positive-sign Fourier covariance convention is correct. Full covariance implies M=diag(M e_0)F by the row recurrence. Invertibility makes every row scale nonzero. The safe-correction lemma and the lift equivalence are also correct. The intermediate displayed line `C M P=Z_s C M` in §3 is a proof typo: the correct direct step is `C M X_s M^-1=Z_s C`, hence CP=Z_s C. Moreover CP=Z_s C already implies CZ_r=Z_r C by taking powers, since P^(2^(s−r))=Z_r.

The 2-adic identity follows directly by writing a positive difference m as 2^v times an odd integer and factoring the geometric sum: each doubling factor contributes one to its 2-adic valuation, while the odd-length factor contributes none. Its statement should exclude a=1 or define psi_1(t)=t, use nonnegative times or explicitly permit 2-adic/rational negative powers, and distinguish unreduced valuations from coordinates already reduced modulo N. The quotient is an integer geometric sum before reduction; it is not division by an invertible residue modulo N. Bit-r changes have finite-coordinate content only for r<w; Z_rho requires rho≤w.

For a≡1 mod4 and odd increment, the full-period assertion agrees with Hull and Dobell, Theorem 1, printed page 233. The primary paper was independently opened for this audit: [Hull and Dobell, Random Number Generators, SIAM Review 4(3), 1962](https://dspace.library.uvic.ca/bitstreams/b7ffb4ac-e2dd-40fb-bb69-74ae37a79fd8/download). This is attribution of a classical ingredient, not a novelty assessment of ACWL.

The conditional complexity implication is valid if every lift reached by the actual constructed ladder has uniform O(N) preparation and application cost, with constants independent of r and w. This must include generating coefficients/routing without free dense formation of P, and the total work of all fibers. Inverting a single weighted-permutation cycle can be linear-time when invertible; a sparse sum's inverse has no automatic linear-time guarantee. The optional correction must be specified and charged. An exact arithmetic model must be stated; arithmetic-operation bounds are not automatically bit bounds.

There are O(log w) doubling steps. Standard continuation costs Theta(N(s−r)), reducing to Theta(Nr) for an unclipped doubling. If final row scales are not already available, one additional application to e_0 obtains them within the same O(N log log N) target; only the divisions themselves cost O(N). The source's referenced Phase results and power-saving comparator were not independently audited here.

## Fresh exact controls

`check_lift_obstruction.py` was newly authored for this audit. No imported historical checker was executed. It constructs partial FFTs by butterfly stages and their inverses, separately checks the explicit matrix formula, and tests all basis vectors simultaneously using exact modular integers.

All **111 lift pairs** passed: every r<s for N=8,16,32,64,128,256 over F_65537, plus every pair at N=256 over F_257. Checked controls include:

- both inverse identities, base covariance, and equality of the full-stage transform with the dense positive-sign DFT;
- the exact obstructing row, P^(2^(s−r))=Z_r, and every distinct relative shear's fixed point/residue preservation;
- standard FFT continuation satisfying both the lift equation and the coarse commutator, while mixing coordinate 1 within its fiber;
- an invertible weighted-shear resolvent/diagonal sample preserving the singleton and failing the lift equation;
- rejection of a negative-sign FFT under the source's positive-sign covariance convention; and the vacuous singular zero solution.

`exact_results.json` records the results and source/checker hashes. These are bounded verification controls, not benchmarks of a proposed faster algorithm.

## Intake recommendation

Retain ACWL as a conditional research framework. Attach the accepted restricted obstruction and request an explicit enlarged generator/solver grammar before further coefficient fitting. Any escape candidate must identify which operation moves the shared fixed coordinate, verify its exact lift along the actually produced ladder, and charge uniform preparation, application and normalization costs. Keep the exact O(N log log N) algorithm claim **OPEN**.
