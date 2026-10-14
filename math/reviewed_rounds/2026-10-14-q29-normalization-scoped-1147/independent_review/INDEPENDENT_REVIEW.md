# Q29 carry-basis conversion and normalization: independent scoped acceptance

Date: 2026-10-14 UTC. Completed review of recovered, previously interrupted work.

## Verdict

**ACCEPT for the exact shared-center conversion and normalization described below.**
The accepted R843 coefficients modulo `(25, Phi3375(z), w^100)` determine the
raw jet `U1687(-1-v;q)` modulo `(pi^200,v^200)`. Exact conversion, the integral
reciprocal identity, coefficientwise content valuation 60, and guarded division
certify the entire normalized polynomial

    F(Y) = pi^(-60) U1687(-1-pi Y;q) modulo pi^140.

Its canonical 360,000-byte representative has SHA-256

    fb09f4ff9f535a864adf3f24ebe00593b3d604777110d08728625a0992c9bc19.

This is an exact finite-ring computation with a justified precision contract.
It is not a complete proof, value, or nonvanishing certificate for Disc R843;
it does not resolve repeated branches or cover the other 26 primary centers.
The full Q29 discriminant problem remains open in this packet. Saved numerical
checks are not promoted into a proof of that larger conclusion.

The producer's contract, SHA-256
`12cfeffbe88092baf5b57123a870168f6d318e4da5ac28991a9d7083fa980a16`,
needs no mathematical repair within its stated scope. Its unmaterialized or
unperformed tasks remain so. This review adds independently verified center
controls; it does not rewrite the producer's execution history.

## 1. Sources, evidence, and independent work

The predecessor `sparse_kernel_independent_review/INDEPENDENT_VERDICT.md` accepts
only the z-basis R843 array. This review supplies the previously excluded
basis conversion, raw-U transfer, content certification, and normalization.
The accepted input is exactly 180,000 canonical bytes with SHA-256

    ebf51150ffbed6e87f3e08875451176963670801c59ffd9128336a02c43ca38c.

`SOURCE_HASHES.json` binds the producer directory, recovered independent
evidence, accepted precision contracts, input arrays, and relevant predecessor
failure disclosures. `PREEXISTING_SNAPSHOT.json` records all 116 files present
in the producer and independent directories before completion. Their contents
were checked unchanged before and after fresh verification.

Three computation paths have distinct provenance:

1. The producer C++ implementation converts z to alpha/beta and then beta to
   pi, with an integral inverse and basis round trips. Its two normalization
   routes and small Gaussian checks are same-author, implementation-diverse
   controls.
2. The saved independent `audit.py` expands `(1+pi)^e`, reduces the complete
   ramified polynomial directly, and forms each numerator before 60 divisions.
   Its saved source, result, stdout, and arrays agree with their recorded hashes.
   It records 12,000 guarded divisions, 199 small quotient controls, and 36
   integral reciprocal-identity/tail cases. `centers.py` and its matching saved
   JSON/stdout provide separately recorded translation controls.
3. The newly authored completion verifier `resume_verify.py` constructs z
   powers by successive multiplication by `alpha*(1+pi)`, avoiding both prior
   conversion implementations. It independently rebuilds all 100 converted R
   coefficients, all 200 raw-U coefficients, every scaled numerator coefficient,
   the uniform F output, and the richer coefficientwise output. It compares
   them directly with the stored bytes, checks every one of 13,830 divisions
   by multiplication back, and rechecks all 200 precision-CSV rows.

No saved program was imported, executed, or compiled during completion. They
were read as source or inert data. In particular, this review did not rerun the
historical scientific programs or the earlier full R843 recurrence. Reliance
on that recurrence is source-bound to its predecessor's explicit acceptance.
The fresh reconstruction from the accepted R bytes supplies additional
independent evidence without changing that dependency.

The matched distinct scientific arrays are:

- Converted R, 180,000 bytes: `9f676e9108122ef4a3666941be1112222da853a479c5f0de890bd680a211e90d`.
- Raw U, 360,000 bytes: `d8113e30c6dc541eaf98d2bd79764d3811e59c3744a7eea514bf70b4ab3d957e`.
- Scaled numerator, 360,000 bytes: `47624ec4d0ef75b47ec5548a527ee5723025d6b9de2e510a34387dfb9dc2f1ec`.
- Uniform F, 360,000 bytes: `fb09f4ff9f535a864adf3f24ebe00593b3d604777110d08728625a0992c9bc19`.
- Coefficientwise F representative, 360,000 bytes: `5c229652300f988e2006089cc7deed69ff25d540c69da59cbb51c59d6c24d768`.

Comparing the same reconstructed array to both saved copies does not create
additional independent mathematical coefficients. Likewise, the three old
mod-5 reference comparisons each cover the same 180,000 raw coordinates.
All three pass, including zero coordinates.

## 2. Exact ring, root binding, and conversion

The coefficient root is q=z; x is the polynomial variable. Fix

    alpha = z^1000, beta = z^2376, pi = beta-1, z = alpha*beta.
    g(A) = A^18+A^9+1,
    f(T) = Phi125(1+T) = sum(r=0..4)(1+T)^(25r).

The CRT exponents have the required residues modulo 27 and 125. The order of
5 modulo 27 is 18, so g is irreducible modulo 5. With O the unramified
degree-18 5-adic integer ring, f is Eisenstein of degree 100 and constant
coefficient 5. Thus A=O[pi] is the local integer ring with v_pi(5)=100, and

    B2 = (Z/25Z)[alpha,pi]/(g(alpha),f(pi)) = A/(pi^200).

These structural facts and their valuation lemma are already accepted in the
source-bound precision contract and independent review; they are not inferred
from matching hashes. The current verifier independently checks the instance's
CRT congruences, order calculation, and complete lower f coefficients modulo25.

The exact carry relation is

    pi^100 = -5(1+2pi^25+2pi^50+pi^75+4pi^80+3pi^85+3pi^90+4pi^95).

Replacing it by pi^100=-5 or by pi^100=0 is not valid here. Both inspected
implementations retain all eight lower terms. The z/alpha-beta isomorphism is
integral, and beta=1+pi is an integral unitriangular change of basis. Neither
conversion loses precision. The fresh successive-q construction independently
produces all converted bytes under the same root binding.

The unramified basis is `1,alpha,...,alpha^17`; it is a power basis. For the
canonical coefficient vector, valuation is the minimum of
`b+100*v5(c[b,a])`. Distinct b have distinct valuations modulo100, and the
alpha residues form a field basis, so the minimal valuation cannot cancel.
A zero B2 vector supplies only the lower bound200.

The layout is jet-degree major, pi-degree next, alpha-degree minor:

    offset = 1800*jet_degree + 18*pi_degree + alpha_degree.

The unique modulo-pi^140 representative reduces alpha coordinates modulo25
for pi degrees0..39 and modulo5 for pi degrees40..99. This is reduction by
the ideal pi^140 after ring reduction, not arbitrary digit truncation.

## 3. Integral transfer, content, and precision proof

The accepted integral reciprocal identity is

    U1687(x;q) = sum(k=0..843) r[k](q) x^(843-k)(1+x)^(2k).

Consequently, at x=-1-v,

    U1687(-1-v;q)
      = sum(k=0..843) (-1)^(843+k) r[k](q) v^(2k)(1+v)^(843-k).

The sign agrees with `U=-H/v` at that substitution. This identity holds over
the integers before reduction; it uses no division by a nonunit. The source
and fresh verifier use ordinary integer binomial coefficients modulo25,
not characteristic-5 Frobenius.

Discarded k>=100 terms begin at v^200. Therefore the accepted R data determine
a raw jet J with `U(-1-v)-J(v)` in `(pi^200,v^200)`. Substitution v=pi*Y
turns both sources of error into coefficientwise multiples of pi^200.
For retained degree j, the coefficient-modulus error is even divisible by
pi^(200+j); omitted degrees j>=200 are integral and have substituted valuation
at least j.

The raw coefficients satisfy `v_pi(u[j])+j>=60`. Equality occurs at j=10,30,50.
The independently recomputed scaled numerators agree with all saved valuation
entries. An entry200 is a lower bound, but the witnesses at60 are strictly
below the precision ceiling and are exact. The omitted tail has valuation
at least200. Thus the *true full numerator*, rather than merely a chosen
representative, has coefficientwise content exactly60.

For `x=sum c[b]*pi^b`, divisibility by pi is equivalent to `c[0]` being
divisible by5 in every alpha coordinate. Set

    d[99] = -c[0]/5,
    d[b-1] = c[b]+f[b]*d[99], 1<=b<=99.

The carry relation proves `pi*d=x`. Changing the quotient representative
changes it only by the kernel of multiplication by pi; an input known
modulo pi^P yields a quotient known modulo pi^(P-1). This is guarded exact
division, not inversion of pi. Multiplication back checks representative
arithmetic, while the algebraic error contract justifies the lost precision.

The uniform route performs 60 divisions for each of200 numerator coefficients,
so the certified uniform precision is200-60=140. The fresh completion verifies
all12,000 guards and multiplication-back checks again. The coefficientwise
route needs another sum(j=0..59)(60-j)=1,830 divisions; for j>=60 it uses
multiplication by pi^(j-60). Both routes agree modulo pi^140.

The uniform140 guarantee is sharp for these truncated data alone. Adding
w^100 to a degree843 monic R preserves its accepted w<100 coefficients and
top monic coefficient, but changes F by

    -pi^140 Y^200(1+pi*Y)^743.

Its degree200 coefficient is first detectable modulo pi^141. The exact known
recurrence could supply more data in another computation, but the currently
retained bytes alone do not determine uniform precision141.

## 4. What each materialized object means

- R is known only for w degrees0..99, with coefficient precision200.
- Raw U is known only for v degrees0..199, each modulo pi^200. It is a raw jet,
  not the full all-degree polynomial.
- The scaled numerator is the entire polynomial modulo pi^200: all omitted
  degrees>=200 vanish at that uniform precision.
- F is the entire polynomial modulo pi^140: its omitted degrees>=200 vanish
  after the pi^60 normalization.
- Each retained F coefficient j<200 has the stronger class modulo pi^(140+j).
  For j>=60, precision beyond200 is represented by the *factored* datum
  `pi^(j-60) * (u[j] mod pi^200)`, not by treating a B2 array as a larger ring.
  The materialized richer file is capped at `min(200,140+j)`, exactly as its
  independently checked CSV states. For j>=200, only the generic lower bound
  `v_pi(F_j)>=j-60` follows from these data.

All precision numbers are exclusive: valuations strictly below the bound are
exact; a zero gives only the corresponding lower bound. Array capacity does
not restore precision lost by division.

## 5. Residue and five shared-center controls

The independently recovered residue is

    F mod pi = A*Y^10*(Y^4-1)^10,
    A = (1,1,0,4,4,1,2,3,2,3,0,0,4,2,2,3,2,1)

in the alpha power basis. Only degrees10,30,50 are nonzero, with coefficients
A,3A,A. This remains an inseparable residue. It gives no derivative-unit or
terminal repeated-branch conclusion.

The fresh verifier also recomputes coefficients0..10 of F(c+Z) for ordinary
integer centers c=0,1,2,3,4. For c=0,1 the first face runs from (0,15) to(10,0);
for c=2,3,4 it runs from(0,10) through(5,5) to(10,0). The exact saved edge
vectors match. All degrees>10 have nonnegative valuation and lie above the
extension of these negative-slope segments, so the omitted higher points do
not invalidate the displayed first face. This is still first-face evidence,
not resolution of the multiple residual roots.

Ordinary centers must remain distinguished from Teichmuller lifts. Their
mod25 representatives are0,1,7,18,24. The F-value differences for pairs(2,7),
(3,18),(4,24) have exact valuation111, observable below140. The differences
for0 and1 are zero; the recorded140 means at least140. Treating 2,3,4 as their
Teichmuller lifts silently would change the higher computation.

Any integral translation `Y=c+pi^b Z`, b>=0, preserves uniform precision140;
a later justified division by pi^h lowers it to140-h. Fractional scaling
requires an explicitly constructed ramified extension and valuation units.
No such extension or later branch normalization is accepted by this review.

At another primary center x=-alpha^ell, 1<=ell<=26, the residue of
`w=(1+x)^2/x` is nonzero. Thus w is a unit and an omitted w^100 term can affect
the constant coefficient already at valuation0. Translations *inside* the
shared Y disk do not reconstruct those primary-center jets or establish a
symmetry among them.

## 6. Execution and preserved interruption history

The earlier independent calculation and the producer completion were
interrupted before the final independent prose review and seal were issued.
Saved sources, output arrays, successful receipts, and control results were
recovered. The interruption was reported as a service usage-limit failure;
its exact occurrence time was not independently established. It is not
presented as a mathematical or program-test failure. No unsaved outcome is
inferred. `INTERRUPTION_PROVENANCE.json` records this boundary.

The predecessor full-kernel packet's original manifest-schema audit failure
and cyclic-checker compilation history remain intact and source-bound.
They are not erased by this later successful review. The earlier precision
recovery report also retains its historical elapsed-time metadata replay
failure. Those historical programs were not rerun here.

Saved timings are attributed to their saved receipts: the producer workflow
records2.224801522 seconds wall and2.229561 seconds charged CPU; the original
independent audit records3.173412791 seconds wall and3.172654579 seconds CPU;
its center-control run records0.959802682 seconds wall. These are historical
observations, not new replay timings or complexity guarantees.

The fresh completion verifier passed in4.087554427 seconds internal wall and
4.085326662 seconds process CPU, with44,644 KiB peak RSS. It used a180-second
wall alarm, a120-second process CPU limit, and a512 MiB per-process address-space
limit. It started no subprocesses. These limits and observations do not claim
an aggregate cgroup guarantee. Its stdout and empty stderr are retained.
No mathematical assertion or test failed during this completion.

All writes remained local to this review directory. No network request,
repository write, upload, table edit, ranking change, or external publication
was performed by this review.

## 7. Next gate and stopping boundary

The next valid mathematical step is a separately scoped repeated-branch
continuation from this certified shared-center F, with each center lift,
scale, content division, derivative conversion, and remaining precision
recorded explicitly. Stop at any unresolved precision ceiling. Other primary
centers and a full discriminant require additional data or separate proofs.
This acceptance closes the bounded conversion/normalization gate only.
