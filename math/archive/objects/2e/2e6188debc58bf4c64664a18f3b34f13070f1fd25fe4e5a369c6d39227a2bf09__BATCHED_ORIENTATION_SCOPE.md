# Additive clarification: near-square orientation

Date: 2026-10-09 UTC. This note supplements the sealed review_batched_interface_equivalence report without modifying any of its files or seals.

The proved near-square conversion assumes m=rq for fixed positive integer r. In particular, its radix-two case has m/q=2. The earlier striped-bank layout instead used m=2^floor(k/2), q=2^k/m, so odd k has m/q=1/2.

These are different orientations of the bank. The reviewed radix-two reduction does not, by itself, cover the unchanged earlier odd-k bank. References to balanced dyadic splits in the report must be read with its explicit condition m/q in {1,2}, rather than as a statement about both possible orientations or that previous layout.

The square theorem is unaffected. The support-routing identity recovering L=F_q tensor I_m from P_J is also valid independently of this ratio. What is missing at the original odd-k orientation is a separately proved and fully charged conversion from that batch to B_all=I_q tensor F_m. No such new reduction is asserted in this addendum.
