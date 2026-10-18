# N13: exact eighteen-bank minimum for Frobenius-stable supports

18 October 2026 UTC. Selected owner: **M-MAGNETIC-SPAN**, with the same
current theorem appearing in NEW-17, Q35 and NEXT-MAGNETIC-SIGNED. This is a
new uniform, declared-family exclusion, not another degree-seven search.
Independent review of these new bytes is pending.

## Result and exact stopping point

Let K=F_(53^d), where d is a positive integer with gcd(d,210)=1. Keep N=13,
q=16, the original signed-resolvent physical-bank grammar, and exactly one
nonzero effective alpha node in each cross orientation, independently free.

1. **A representation with seven nonzero effective nodes in either same-sign
   orientation cannot have that seven-element support invariant under
   x -> x^53.** The other support and both cross nodes are initially allowed
   to be arbitrary K-valued sets/nodes. All legal beta and all K-valued raw
   weights are allowed. No Frobenius condition on weights or amplitudes is
   assumed.
2. Consequently **every sixteen-bank witness in these degrees must have both
   same-sign supports non-Frobenius-stable**. Both monic degree-seven support
   polynomials must have at least one coefficient outside F53.
3. In the declared family where **both** same-sign nonzero effective supports
   are Frobenius-stable, the exact minimum physical-bank count is **18** for
   every such d, including d=11 and d=13. This excludes seventeen as well as
   sixteen in that family.

The degree-eight cross-node descent in section 4 is the new mechanism. Merely
requiring base-field cross nodes would be a materially weaker result.

This resolves the selected declared-family gate. Stop searches that retain
F53 coefficients for either seven-node same-sign annihilator at d coprime to
210: they cannot produce sixteen banks, even when cross nodes and weights
are searched over the full extension. Do not repeat this excluded family as
an open experiment.

The unrestricted minimum B(K) remains between 16 and 18. This proof does not
exclude certificates with both seven-node supports nonstable, nor determine
whether a nonstable seventeen-bank certificate exists. The four parent views
remain open; no parent closure or novelty change is warranted.

## 1. Source and current-gate binding

The selected mathematical gate is a declared-family exclusion preserving extension-valued cross nodes and coefficients. Its linked parent problems remain open. Private research-register snapshots are not included. No table or repository change is claimed.

Accepted dependencies, read as complete local source bodies and pinned in
`SOURCE_PINS.json`:

- [Original lower-bound scope and arbitrary-beta expansion](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md),
  sections 1–3. Every same-sign orientation requires at least seven distinct
  nonzero effective nodes, over every characteristic-53 field. Cross nodes
  are nonzero. Repeated physical banks, cancellation and arbitrary legal
  beta are allowed.
- [Accepted exact base-field minimum and one-sided census](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/n13_eighteen_independent_review_2034/INDEPENDENT_REVIEW.md),
  sections 2–3. For every y in F53*, no monic degree-seven solution of the
  six forced recurrence equations has seven distinct nonzero F53 roots.
  An original eighteen-bank Fourier witness over F53 is accepted.
- [Accepted forced-moment system and uniform rank](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md),
  sections 1–2. These provide the exact formulas used below. The uniform rank
  theorem is retained, not repeated as a newly completed gate.
- [Accepted degree-seven attainment and remaining classification](https://github.com/AgentSlop-Si/research/blob/511689fb34ffa88921b3d2a0dc801e048b49dce2/math/finalized/2026-10-17-resumed-mathematics-0916/reports/n13/REPORT.md).
  Sixteen banks are already attained whenever 2, 3, 5 or 7 divides d. Those
  results are unchanged. No new bank witness or literal inverse replay is
  claimed here.

## 2. Original grammar and the declared family

All indices are modulo 13. Let S e_t=e_(t+1), T e_t=16^t e_t, and
F[k,t]=16^(-kt). One physical bank is exactly

    (1/13) sum_(j=0)^12 w_j
      (I-alpha S^epsilon-beta 16^(epsilon delta j) T^delta)^(-1),
    epsilon,delta in {+1,-1},  Delta=1-alpha^13-beta^13 != 0.

For a fixed orientation and alpha, merge the entire normalized amplitude
vectors of repeated physical banks. A node is effective if the merged vector
is nonzero. Let X_++ and X_-- denote their **nonzero** same-sign alpha
supports. This excludes zero alpha from the support polynomial only; it does
not silently forbid zero-alpha physical banks. Such banks make no contribution
at the positive exponents used below and still count physically.

The declared stable-support family consists of original legal representations
for which X_++^53=X_++ and X_--^53=X_-- as unordered sets. It imposes no
Frobenius condition on individual beta values, raw weights, normalized
amplitudes, their association to nodes, or either cross node. No additional
trace/orbit primitive, field-valued quotient bank, pre/post map, derivative
atom or singular limiting bank is admitted.

For any distinct finite support X, Frobenius stability is equivalent to its
monic annihilator H_X(t)=product_(x in X)(t-x) having F53 coefficients:
Frobenius permutes the factors if the set is stable, and conversely takes
every root of a base-coefficient polynomial to another root. This equivalence
does not by itself put individual roots in F53; the degree condition below
is essential.

## 3. A finite-field orbit lemma

**Lemma.** Suppose gcd(d,210)=1 and a nonzero polynomial P in F53[Y] has
degree at most eight. Every root y of P lying in K=F_(53^d) lies in F53.

**Proof.** The automorphism phi(x)=x^53 satisfies phi^d=id on K. The orbit
length e of y therefore divides d. Because the coefficients of P are fixed,
all e distinct orbit elements are roots of P, so e<=deg P<=8. Every integer
2<=e<=8 has a prime divisor among 2,3,5,7. Coprimality thus forces e=1.
The fixed points of phi are exactly F53: all 53 prime-field elements are
roots of Y^53-Y, which has at most 53 roots. Hence y belongs to F53. QED.

The same proof applies in particular to a degree-seven support annihilator.
This is an all-degree argument, not an inference from finitely tested d.

## 4. A stable seven-node support forces the adjacent cross node to descend

Assume X_++ has exactly seven elements and is Frobenius-stable. Write

    H(t)=h0+h1 t+h2 t^2+h3 t^3+h4 t^4+h5 t^5+h6 t^6+t^7.

Stability gives h_j in F53. Nonzero support gives h0!=0. The orbit lemma
applied to H puts all seven roots in F53. The cross node y in (-,+) is
initially any nonzero element of K; it is not assumed fixed by Frobenius.

For r=[epsilon a]_13, ell=[delta b]_13 and omega=16^(epsilon delta), define

    G_(epsilon,delta)(a,b)
      = product_(i=1)^ell (1-omega^(r+i))/(1-omega^i)
        when r+ell<13, and zero otherwise.

All displayed denominators are nonzero. In the original arbitrary-beta
expansion a bank contributes G_(epsilon,delta)(a,b) alpha^r A_b, where

    A_b=beta^ell/(13 Delta gamma) sum_j w_j 16^(epsilon b j),
    gamma=7.

There is no division by beta. Merging complete A vectors therefore preserves
the same formulas with arbitrary legal beta, repeated nodes and cancellation.

For b=1 and a=1,...,11, the isolated row a=12 fixes the cross amplitude,
and the required (++ ) power moment is

    s_1(a;y) = [16^(10(a+1)^2)
               - y^(12-a) G_-+(a,1)/G_-+(12,1)] / G_++(a,1).

The two negative-delta orientations vanish in these rows. Any zero-alpha
same-sign bank also vanishes because a>0. Since H annihilates all seven
nonzero nodes, its last available b=1 recurrence gives

    sum_(j=0)^7 h_j s_1(4+j;y)=0, with h_7=1.

This identity holds even when the seven moment amplitudes are extension
valued. It follows by interchanging the finite sums and using
sum_j h_j x^(4+j)=x^4 H(x)=0 for each support node x.

The exact base-field constants in this last window are

    s_1(4+j;Y)=u_j-v_j Y^(8-j), j=0,...,7,
    u=(19,45,51,21,12,21,49,6),
    v=(1,16,25,40,36,46,41,12).

Consequently y is a root of the explicit polynomial

    P_H(Y) = C_H
      -h0 Y^8 -16h1 Y^7 -25h2 Y^6 -40h3 Y^5
      -36h4 Y^4 -46h5 Y^3 -41h6 Y^2 -12Y,
    C_H=19h0+45h1+51h2+21h3+12h4+21h5+49h6+6.

All coefficients lie in F53 and the leading coefficient is **-h0!=0**.
Thus P_H is a nonzero polynomial of exact degree eight. The orbit lemma
forces y into F53. No division by a parameter polynomial, no selected chart,
and no rank-specialization assertion is needed.

We now have seven distinct nonzero F53 support nodes and y in F53*. The
actual representation forces all six degree-seven recurrence windows, not
merely the last one. The accepted one-sided base-field obstruction says no
such support exists. This is a contradiction. Notice that the proof does
not try to descend the original weights, beta values or the other support.

Simultaneous reflection (a,b,epsilon,delta)->(-a,-b,-epsilon,-delta)
preserves G and the target 16^(10(a+b)^2), swaps (++ ) and (--), and swaps
the independently free cross nodes. Therefore the identical argument
excludes a Frobenius-stable seven-node (-- ) support as well. QED.

## 5. Exact minimum eighteen in the declared family

Let a stable-support-family representation use at most seventeen physical
banks. The inherited field-uniform lower theorem gives

    |X_++|>=7, |X_--|>=7,
    physical_bank_count >= |X_++|+|X_--|+2.

The final two account for the two nonzero effective cross orientations.
Additional repeated, zero-alpha, ineffective or cancellation-only physical
banks can only increase the physical count. Thus at least one same-sign
support has at most seven nodes, and hence exactly seven. Both supports
are stable by the declared family condition, contradicting section 4.
Every family member therefore uses at least eighteen physical banks.

For the upper bound, the accepted eighteen-bank F53 witness has

    X_++=X_--={1,2,6,7,12,21,22,26}, y=z=1, beta=1,
    physical allocation (8,1,1,8).

All parameters and raw weights belong to F53, all guards are nonzero, and
the full Fourier matrix identity is independently accepted in the source.
The inclusion F53 -> K preserves all sums, products, inverses and nonzero
elements, so it remains an original eighteen-bank witness over K. Both
supports remain Frobenius-stable. Hence the declared-family minimum is
exactly eighteen for every gcd(d,210)=1.

In particular, a sixteen-bank witness necessarily has allocation (7,1,1,7).
Section 4 requires each same-sign support separately to be nonstable. At
seventeen banks, the seven-node side must be nonstable; this theorem does not
require a possible eight-node side to be nonstable.

## 6. Fresh controls, reproducibility and proof dependence

Run `python check_descent.py`. This newly written standard-library program
does not import or execute historical research programs. It constructs G by
the additive Gaussian-binomial Pascal recurrence, checks all 676 reflection
identities, and reconstructs the eight exact (u,v) pairs in section 4. The
nonzero leading coefficient is checked for every possible nonzero h0.

As a regression of an **accepted premise**, it independently reconstructs
the six forced-window equations for every y in F53*, solves their affine
monic degree-seven family for all 53 h6 values, and checks all 2,756
polynomials at all 52 nonzero field elements. The maximum is six roots.
The root-count histogram for counts 0,...,6 is

    (1041,1006,521,150,32,5,1).

The regression also makes 146,068 last-window scalar-identity checks, and a
zero-constant-term mutation confirms that the degree-eight argument would
fail without h0!=0. `CHECK_RESULT.json` and
`BASEFIELD_PREMISE_REGRESSION.json` preserve the results. There are zero
failures. These controls validate constants and the inherited finite lemma;
the uniform theorem follows from sections 3–5, not from finite enumeration.
No new completion credit is claimed for the accepted base-field census.

The theorem depends on the accepted original-bank expansion, the per-side
seven-node lower bound, and the accepted eighteen-bank witness. It supplies
a new proof of the precise stable-support exclusion and exact restricted
minimum. It does not claim a new independent replay of all inherited raw
matrix inverses. Separate independent review of the new theorem remains
required before labeling it independently accepted.

## 7. Owner disposition and preserved limits

After independent acceptance, mark only the named declared-family gate
complete. Keep all four existing owners open at priority 56. A substantive
successor must allow both seven-node annihilators to have genuinely
extension-valued coefficients; searching only prime-field annihilators or
Frobenius-orbit unions cannot solve the remaining d coprime-to-210 problem.

The degree-37 chart exception is not used or excluded: this proof has no
chart division. The result is compatible with the accepted degree-2/3/5/7
witnesses because their degrees violate the coprimality hypothesis.
Arbitrary nonsymmetric, nonstable support pairs, seventeen-bank behavior,
unrestricted cross allocations, other lengths/parameters, historical
novelty and fully paid evaluation costs remain separate. No FFT arithmetic
or runtime improvement follows from a representation-count result.

No external write, publication, table update or denied-action retry occurred.
