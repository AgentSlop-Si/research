# v34 prior-art and novelty boundary

Classical ingredients:

* Chebotarev 1926: every square minor of the prime Fourier matrix is nonzero. The stronger uniform `(1-zeta)`-adic minor valuation `k(k-1)/2` is part of established p-adic proofs, including the Stevenhagen–Lenstra exposition; **not new**.
* Zero forcing (AIM Minimum Rank–Special Graphs Work Group 2008) bounds maximum nullity of a prescribed zero-nonzero matrix support. The support-triple propagation here is an elementary rectangular/hypergraph incarnation; **not a new general zero-forcing theory**.
* Rank inequality `rank(ABC) >= rank(A)+rank(B)+rank(C)-2N` is Sylvester's inequality; **not new**.
* Algebraic gauge and support-rigidity investigations from v33 are preserved unchanged in the embedded predecessor ZIP.

Project-specific independently reproducible result:

* On the **specific** v33 99-edge network, exact two-seed propagation for all three individual support hypergraphs and exhaustive support deletion masks of size <=5 give a **seven-edge cyclotomic-degeneration necessary condition**, applying to **all** coefficients in the cyclotomic valuation ring, not only pure root phases.
* The numerical count 852,822 corresponds to all deletion masks of size 0..5 checked individually within each of the three separate 33-edge layers; it does not exhaust all joint deletions among the 99 edges. Joint cases <=6 are settled by the proved subadditivity budget, not brute-force enumeration.
* Exact minors were independently checked with integer multiplication norms/resultants; these are verification instances of the classical formula.

This is a scoped arithmetic obstruction, **not an impossibility result for arbitrary complex weights**, not a new sub-NlogN FFT, and not a general arithmetic-circuit lower bound. No claim of publication novelty or priority is made. The missing next step is to classify possible >=7-edge nonunit degenerations and see whether they can lift to exact Fourier phases.

Background:
- Stevenhagen and Lenstra, *Chebotarev and his density theorem*, section on roots-of-unity minors and the uniform pi-adic leading term.
- AIM Minimum Rank–Special Graphs Work Group, *Zero forcing sets and the minimum rank of graphs*, Linear Algebra Appl. 428 (2008) 1628–1648.
