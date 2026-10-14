# Exact singleton signed bank minima over three finite fields

14 October 2026

The same free-cross-singleton dictionary has exact bank counts **14 over F23, 13 over F23³, and 12 over F23⁵**. The first two equalities have independent acceptance reports. The third is the direct corollary of the accepted all-parameter lower bound and the earlier accepted degree-five-field witness. This note records that dependency match; it is not a new arithmetic audit or external peer review.

## The dictionary and theorem

Let K be a field extension of F23. Fix N = 11, q = 13, and, for indices modulo 11,

    S e_t = e_(t+1),       T e_t = 13^t e_t,
    F[k,t] = 13^(-kt).

One counted physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
          (I - alpha S^epsilon - beta 13^(epsilon delta j) T^delta)^(-1),
    Delta = 1 - alpha^11 - beta^11 != 0,

where epsilon and delta independently belong to {+1,-1}, and alpha, beta and all eleven raw weights belong to K. Every legal beta is allowed, including zero. No additional generator, transformed target, pre/post map, bank product, derivative atom, infinite node, trace-bank primitive or singular limit is admitted.

Within each orientation, group the normalized Weyl-sector amplitude vectors of banks sharing alpha. An alpha node is effective when its grouped vector is not identically zero. Require **exactly one effective alpha node in each cross-sign orientation**, y in (-,+) and z in (+,-). Their locations are independently free; y = z is not assumed. There is no corresponding singleton restriction on either same-sign orientation. Grouping is lower-bound bookkeeping: the objective still counts every physical original bank, including repeated banks.

Let b(K) be the minimum physical-bank count representing F under these conditions, or infinity if no representation exists. Then

    b(F23) = 14,       b(F23³) = 13,       b(F23⁵) = 12.

These are three coefficient-field instances of one optimization problem. The cubic and degree-five fields are not a nested chain.

## Proof dependency map

The source labels below identify the frozen review snapshots in `sources/`; complete SHA-256 bindings and certificate locations are in `SOURCE_BINDINGS.json`.

| Claim | Lower-bound dependency | Accepted original-bank attainment |
| --- | --- | --- |
| b(F23) = 14 | [A] excludes at most five same-sign support nodes for every independent singleton choice; reflection gives 6 + 1 + 1 + 6 | [A] reconstructs fourteen legal banks |
| b(F23³) = 13 | [B] excludes every physical count at most twelve | [C] reconstructs thirteen legal banks and checks the domain match to B |
| b(F23⁵) = 12 | [B] requires at least five nonzero effective nodes in each same-sign orientation over every extension | [D] reconstructs twelve legal banks over F23⁵ with cross nodes (4,4), an allowed choice in the free domain |

**A. Base-field equality.** The complete all-22-parameter quintic gate has no admissible five-distinct-nonzero-root support over F23. Reflection applies separately to z, without imposing y = z. The matching witness has allocation (6,1,1,6), in (++,-+,+-,--) order, cross nodes (7,7), and same-sign support {6,7,12,13,17,19} on both sides. Its 154 literal inverse branches and all 121 target entries were independently checked.

**B. All-extension baseline and cubic exclusion.** The coefficient matrix of the six degree-five recurrence equations has rank five at every parameter over every extension. Compatibility occurs precisely at the roots of the reviewed degree-27 parameter polynomial. At each compatible parameter the unique monic quintic has nonzero constant term. These facts together, not rank alone, exclude supports of size at most four: multiplying a smaller support polynomial by a power of t would produce a compatible monic quintic with zero constant term. Reflection and the two required cross groups give b(K) ≥ 12 for every extension K/F23.

Over F23³, an at-most-twelve-bank representation would consequently have allocation (5,1,1,5). The complete parameter gate and splitting certificates force y = z = 15 and both same-sign supports to be the roots of

    h15(t) = t^5 + 12t^4 + 17t^3 + 14t^2 + t + 14
           = (t-3)(t-21)(t^3 + 13t^2 + 13t + 13).

The accepted full-sector functional annihilates every bank in that forced pattern for arbitrary legal beta and weights, but takes value 14 on F. Thus twelve and all smaller counts are impossible. This is an exhaustive lower bound, not merely the failure of one proposed weight vector.

**C. Cubic attainment.** Take K = F23[u]/(u³ + 13u² + 13u + 13). The accepted allocation is (5,1,1,6): the ++ support is {3,21,u,u²³,u⁵²⁹}, the cross nodes are (15,7), and the -- support is {6,7,12,13,17,19}. The review reconstructs 143 literal inverse branches, all thirteen nonzero banks and all 121 target entries. Together with B this gives equality thirteen.

**D. Degree-five attainment.** Take K = F23[v]/(g), where

    g(t) = t^5 + 8t^4 + t^3 + 18t^2 + 4t + 6.

The earlier independent witness review proves that g is irreducible and reconstructs twelve legal nonzero banks with allocation (5,1,1,5), both same-sign supports the five Frobenius roots of g, and cross nodes (4,4). All 132 literal inverse branches and all 121 target entries were checked. A pinned witness remains admissible when the pins are freed. Combining this upper bound with B's all-parameter bound gives the asserted free-domain equality twelve; the older pinned-only lower bound is not used for this inference.

All three upper witnesses choose beta = 1. Their lower bounds allow every legal beta, zero/repeated same-sign nodes, ineffective groups and cancellations. Passing a necessary recurrence gate alone is never used as full-bank attainment.

## Distinct pinned statements

The independently accepted fixed-(4,4) base-field minimum is sixteen [E]. It optimizes over a smaller permitted set than b(F23). The free-domain fourteen-bank witness uses (7,7), so the two exact statements are compatible.

The fixed-(15,15) obstruction in B is different again. Over every extension it requires at least six nonzero effective nodes in each same-sign orientation, hence at least fourteen physical banks; it does not establish attainment in that pinned domain. Its functional has cross contraction P_+-(z) = 6z(z-15), which need not vanish when z changes. It therefore cannot exclude the accepted cubic thirteen-bank witness with cross nodes (15,7).

## Classical context and limits

The bounded primary-literature comparison [F] leaves historical novelty unresolved. The closest mechanisms are classical:

- Holtz, Mehrmann and Schneider, [root-of-unity quantum binomial identities](https://arxiv.org/pdf/math/0512607), supply the mechanism behind the finite resolvent expansion.
- Gurevich and Hadani, [Weyl coefficients and the Fourier operator](https://people.math.wisc.edu/~sgurevich/YACHA673.pdf), give a nearby representation-theoretic context; their complex-scalar conventions do not establish the present F23 identities.
- van der Hoeven and Lecerf, [finite-field sparse interpolation](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf), and Schmidt and Sidorenko, [common recurrences for unequal-length sequences](https://arxiv.org/pdf/cs/0605044), cover the annihilator and amplitude-recovery mechanisms.
- Reznick and Tokcan, [relative binary-form ranks](https://arxiv.org/pdf/1608.08560), are especially close conceptually: admissible squarefree splitting controls field-dependent rank. Their complex-subfield Waring setting differs from this finite-field bank dictionary. Lavrauw and Zullo's [finite-field Waring subspaces](https://arxiv.org/pdf/2207.13456) provide further nearby context.

The necessary moment windows can be interpreted as a restricted simultaneous Waring/Prony problem. That correspondence does not include the remaining full-bank sector equations. Neither field-sensitive rank nor three different minima is claimed as a new general phenomenon.

The result is a fixed-size exact representation-count theorem. It does not address unrestricted cross-orientation supports, classify all optimal witnesses or extension degrees, vary N or q, lift to characteristic zero, or establish historical priority. Bank counting omits branch evaluation and extension-field arithmetic; **no arithmetic-complexity or FFT speed claim follows**.

## Remaining prerequisites

No unreviewed numerical assertion is needed for these three equalities once the source integrity checks in `SOURCE_BINDINGS.json` pass. This synthesis itself adds no scientific computation and does not substitute for independently reviewing its final exposition.

Before presenting it as a submission-ready paper, the remaining work is a self-contained proof presentation with its exact certificates, a clear mathematical motivation for the restricted dictionary, a broader specialist literature review, and ordinary external mathematical review. Historical novelty and publication significance remain undecided. No broader calculation, theorem classification or external publication is part of this note.

[A]: sources/A__free_singleton_basefield_acceptance__REVIEW.md
[B]: sources/B__parameter_cubic_lower_bound__REVIEW.md
[C]: sources/C__cubic_thirteen_independent_acceptance__REVIEW.md
[D]: sources/D__degree_five_twelve_acceptance__REVIEW.md
[E]: sources/E__pinned_sixteen_acceptance__REVIEW.md
[F]: sources/F__pinned_bank_literature__REPORT.md
