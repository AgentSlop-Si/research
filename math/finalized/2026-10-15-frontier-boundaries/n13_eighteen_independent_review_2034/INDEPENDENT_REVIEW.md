# Independent review: exact eighteen-bank N13/F53 attainment

Date: 2026-10-14 UTC.

## Verdict and exact scope

**ACCEPT_SCOPE_LIMITED: B(F53)=18** for N=13, q=16, the original signed
resolvent-bank grammar, and exactly one nonzero effective alpha node in each
cross-sign orientation. The cross nodes are independently free in the problem;
the attaining example happens to choose both equal to 1. No restriction that
the same-sign supports coincide is used in the lower bound; they coincide in
this witness only.

Accepted scope:
`M-MAGNETIC-SPAN::Q35::N13-q16-F53-free-cross-singleton-exact18`.

This closes the fixed-instance base-field representation-count gate. It does
not close unrestricted cross allocations, other q or characteristic, exact
extension-field minima, all-length construction, historical novelty, or an
arithmetic-speed/FFT improvement. The broader M-MAGNETIC-SPAN/Q35 parent and
its scores/statuses are not changed by this review.

The exact raw witness is bound by SHA256
`871c3225f1276eba3f81ce574c87005e02b31205d0df2762c1320e08f76c66c5`
at `n13_eighteen_attainment_2033/WITNESS.json`. `CANDIDATE_BINDING.json`
records the final candidate report, contract, manifest, archive and source
bindings. Acceptance attaches only to those frozen bytes.

The frozen candidate report SHA256 is
`e1177512fcb544cba642b98f68ae35bf0ca29da89b86f52df57325166f5a4249`;
its manifest SHA256 is
`caf38c67e5cc453cb015b68437b7664c78261eaadca44a193496be3d42a28297`.
All 19 manifest entries, all 20 candidate archive members, all 7 external source
bindings, every displayed raw-weight row, and the candidate's complete literal
matrix and lower-census data agree with the independently verified objects.

## 1. Grammar and direct verifier

All arithmetic is in F53. Indices are modulo 13, with

    S e_t=e_(t+1), T e_t=16^t e_t, F[k,t]=16^(-kt).

One physical bank is exactly

    (1/13) sum_(j=0)^12 w_j
      (I-alpha S^epsilon-beta 16^(epsilon delta j)T^delta)^(-1),
    Delta=1-alpha^13-beta^13 != 0,
    epsilon,delta in {+1,-1}.

There are no pre/post maps, target conjugations, products of banks, derivative
nodes, singular limits, infinite nodes, or implicit field extensions in the
accepted witness. The fresh checker builds each branch directly, column by
column: its diagonal at t is `1-beta*16^(epsilon*delta*j+delta*t)`, and the
shifted entry at row t+epsilon, column t is `-alpha`. Gauss-Jordan inversion
and separate left/right matrix products certify each original inverse. Only
then are the raw weights and original factor 1/13 applied.

`check_original_banks.py` was newly written for this review before reading the
new witness. It first passed the previously accepted 24-bank data as a control.
The new candidate was treated as inert raw parameters/weights, not as trusted
bank matrices, inverses, output entries, or solver results. No candidate or
historical program was imported, compiled, or executed.

## 2. Eighteen-bank witness and full operator identity

The same-sign supports are

    X_++=X_--={1,2,6,7,12,21,22,26},

the (-,+) and (+,-) nodes are each 1, and beta=1 for every bank. The eight
same-sign denominator values, in this order, are

    52,23,1,1,30,30,30,23.

The two cross denominators are 52. All are nonzero. All raw phase weights are
canonical F53 integers, and every physical bank matrix is nonzero. Every
orientation/alpha group is distinct, and its complete amplitude vector is
nonzero. Thus both physical and effective allocation are exactly

    (++, -+, +-, --) = (8,1,1,8).

The independent reconstruction verifies:

- 234 original 13-by-13 branch inverses and 468 two-sided inverse products;
- 3,042 individual bank Weyl coefficients;
- all 169 entries of the aggregate against the direct literal Fourier matrix;
- all 169 full-sector equations, including every axis sector;
- the raw-weight-to-amplitude transformations and all reported sector ranks.

The thirteen sector ranks are

    13,10,12,13,13,13,13,13,13,13,13,12,10.

Rank deficiency in a sector is allowed; the relevant requirement is that its
complete target equations hold, which they do. The saved reconstructed matrices
and amplitude vectors are in `CANDIDATE_MATRIX_CHECK.json`.

Equality of the matrices proves equality on every vector in F53^13 by linearity.
This is an arbitrary-input operator identity, not a numerical-input sample or
agreement solely on necessary recurrence windows.

## 3. Independent matching lower bound

The earlier independent N13 acceptance is
`review_n13_extension_1315/REVIEW.md`, SHA256
`896200e3b4b12d56dd13ac1d87b5e6ea64ef3283e77887898bb595d1bf304b6f`.
Its 38 manifest entries were verified. Its 18-bank lower bound has exactly the
same base-field, fixed-q, free-cross-singleton grammar as this attainment.
It allows arbitrary legal beta values, repeated physical nodes, cancellations,
and zero same-sign nodes. Those freedoms do not invalidate the lower bound.

This review additionally rebuilds the base-field lower bound independently,
without executing the earlier checker or relying on its all-extension
degree-six minor argument.

Put r=[epsilon*a]_13 and ell=[delta*b]_13. For r+ell<13 define the ordered
Gaussian coefficient by the finite product

    G_(epsilon,delta)(a,b)
      = product_(i=1)^r (1-omega^(ell+i))/(1-omega^i),
    omega=16^(epsilon*delta),

and set it to zero otherwise. Every denominator in the product is nonzero.
The fresh matrix controls independently validate this coefficient formula.
For arbitrary legal beta the normalized sector amplitude is

    A_b=beta^ell/(13 Delta gamma) sum_j w_j * 16^(epsilon*b*j),
    gamma=(1/13)sum_t 16^(-t^2)=7.

No beta is inverted. Banks with the same orientation and alpha combine by
adding this whole vector, exactly the stipulated effective-node definition.

Let y be the sole effective (-,+) node. For b=1,...,6, at a=13-b only that
orientation supports the nonzero target, so y!=0 and its amplitude is forced.
For b<=a<=12-b the two negative-delta orientations vanish. Dividing by the
nonzero ++ coefficient gives the forced moments

    s_b(a;y)=[16^(10(a+b)^2)
      - y^(13-a-b) G_-+(a,b)/G_-+(13-b,b)]/G_++(a,b).

They have lengths 11,9,7,5,3,1 and must all be representable using the common
distinct nonzero ++ support. A zero node contributes nothing at these positive
exponents. Repeated nodes merge amplitudes and do not become derivative atoms.

If there were at most seven such nodes, extend their set to seven distinct
nonzero F53 elements. This is possible because F53 has 52 nonzero elements.
The monic product of those seven linear factors would satisfy every available
degree-seven consecutive recurrence window. There are six windows: four from
the length 11 sequence and two from the length 9 sequence.

For each of all 52 nonzero y, the fresh checker constructs the six equations
directly from the displayed formulas. Their first six coefficient columns are
invertible. Fixing the coefficient of t^6 arbitrarily in F53 therefore gives
exactly all 53 monic degree-seven solutions, with no omitted solutions.

All 2,756 resulting polynomials are checked against every recurrence equation,
then evaluated at every nonzero field element: 143,312 exact root evaluations.
None has seven distinct nonzero roots; the maximum is six. The entire fresh
polynomial/root-list mapping matches the earlier accepted inert census, not
merely its survivor count. `FRESH_BASE_FIELD_CENSUS.json` records every case.

Hence ++ requires at least eight distinct nonzero effective nodes. Simultaneous
reflection of a,b,epsilon,delta preserves the Gaussian support and normalized
target, so the identical argument applies to -- with its own independently
free cross singleton z. It requires eight more nodes. The two nonzero effective
cross groups require at least two further physical banks. Thus every legal
representation in this scope has at least 8+1+1+8=18 physical banks. Combining
this with the direct 18-bank witness proves the exact minimum.

The older all-extension lower bound 16 is preserved as an accepted dependency,
not re-proved by this base-field census. The new F53 witness survives scalar
extension, so the corresponding extension-field interval improves to 16..18.
Its exact minimum remains open; the base-field splitting obstruction must not
be exported to extension-valued nodes.

## 4. Controls and preservation

Falsification controls detect 169 target-entry mismatches if 1/13 is omitted,
144 if the opposite Fourier sign is used, and 91 if the first raw weight is
incremented by one. Removing any individual bank changes the target; all 18
deletion mismatch counts are positive and retained.

Twelve additional legal-bank controls use (alpha,beta)=(0,2),(2,0),(2,3) in all
four orientations. Their 156 branch inversions, 312 inverse-product checks, and
2,028 Weyl coefficient checks pass. Four deliberately singular alpha=0,beta=1
branches are rejected. These controls exercise zero parameters and illegal
denominators; the symbolic original-bank formula supplies the general scope.

No sealed predecessor is overwritten. The old 24-bank witness remains a valid
historical upper bound and a fresh checker control, while the new exact 18
statement supersedes its open 18..24 interval only for this fixed base-field
contract. The accepted N11 results and their field restrictions are untouched.

No bank-count reduction is identified with arithmetic savings. A bank contains
13 inverse branches, and no new shared fast evaluator or paid comparison with
the same-field convolution baseline has been established here.

## 5. Completion boundary

The proof obligations for this finite representation gate are complete:
the frozen candidate bindings and cold replay of all five mathematical result
files pass. No repair is requested. The review
does not independently certify how exhaustive or efficient the producer's
bounded witness search was; existence needs only the verified final witness.
Search failure would not have proved impossibility, and search statistics are
not used in the lower bound.

The semantic proposal correctly retains the broad parent status TO RESEARCH
and priority 56 and closes only the named fixed-instance child. Its row locators
and native preimages were not freshly verified by this mathematical review;
publication still requires separately guarded source/table handling.

The fresh reviewer scripts use only standard-library Python. Local data reads,
new local review artifacts, and fresh code execution were the only actions.
No external write, table edit, repository publication, historical execution,
or candidate-code execution occurred. No mathematical assertion or test failed
during this review.
