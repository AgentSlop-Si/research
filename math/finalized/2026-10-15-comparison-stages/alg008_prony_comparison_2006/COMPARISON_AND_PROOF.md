# ALG-008: exact Prony-interface comparator and paid recognition contract

2026-10-14 UTC. Parent stable ID **ALG-008**, **Blind sparse inverse discovery**.

## Result and scope

The selected comparison of Phase19 Theorem C against an exact primary sparse-interpolation construction is complete. Its recurrence/Hankel/Vandermonde mechanism is classical. The raw-vector reciprocal-probe interface, subgroup enumeration and complete cyclic certificate require the explicit mapping and costs below; they must not be described as a free black-box interpolation call.

Proposed scoped closure after independent review: `ALG-008::BenOrTiwari-Prony-interface-comparison`, subtype `CLOSED_COMPLETED_SOURCE_COMPARISON`. Parent `TO RESEARCH`, priority 42, accepted original theorem and all unresolved broader gates remain unchanged. No new canonical ID or discovery count is proposed. The closure is earned by completing the named comparator, not by a low promise assessment.

## Primary-source synopsis

Ben-Or and Tiwari, [A Deterministic Algorithm for Sparse Multivariate Polynomial Interpolation](https://www.cecm.sfu.ca/personal/monaganm/teaching/TopicsinCA15/BenOrTiwari.pdf), extended abstract, pp.301–309. Sections3–4, the Hankel determinant theorem and Figure1 (pp.303–304) recover exponential nodes and amplitudes from 2t evaluations. Section6 (p.305) gives cubic direct linear algebra and the quadratic Berlekamp–Massey alternative. Section9 (pp.307–308) discusses separate finite-field obstacles. The full nine-page PDF body was read; no local PDF byte hash is claimed.

Its characteristic-zero algorithm evaluates at powers of distinct primes and recovers exponents from integer nodes. Those evaluation/root-recovery assumptions do not match a finite cyclic subgroup. The moment factorization does match after an explicit algebraic specialization; scanning the known N-node grid replaces integer-root recovery at O(Ns) cost. The paper does not state the entire raw circular-inverse/certificate/full-DFT package under the Phase19 interface. This is a source-specific nonmatch of the full package, not a worldwide priority or novelty conclusion. Its unrestricted nonadaptive sampling lower bound is not imported into this finite-grid model.

Supplementary reference: Massey's [Shift-Register Synthesis and BCH Decoding](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf), SectionIII, permits recurrence synthesis over finite or infinite fields. The fresh checker below does not depend on or implement that algorithm.

## Exact source bindings

The canonical ALG-008 review summary is `PINNED_INTEGRATED_RESULTS.md`, SHA-256 `0b5f8d5db244d83483cf91eecf0d3520feb7f35182469a07cd1f02d872342e53`.

Recovered Phase19 source bodies, matching their saved source manifest:

- `PHASE19_THEOREM.md`: `b1810b01ac901be12667df56c9c19a73a8cfc06baf76c8e2e44c9fc4825ddf9c`
- `PHASE19_COST_LEDGER.md`: `489247df5d5baf6d0521c2067c3623310e1cf230d39ad9a28860b209866f4842`

The bodies, not historical programs, were inspected. The canonical summary's corrections control over broader claims in the older source. In particular, source graph-branch arithmetic proxies are not accepted as exact counters, and the Fourier fallback requires its own admissibility/root contract.

Current local bindings: Catalogue row73; novelty register row34; Research overview row51. The comparison is keyed by stable ID, not by older novelty row50. Before a live update, independently resolve IDs and exact preimages. This packet makes no external writes.

## Hypotheses and recovered object

Let E be a field, N≥2, char(E) not dividing N, and let omega be a supplied primitive Nth root. Its N distinct powers are supplied/validated. Let 1≤s≤floor(N/2). Input is the resident raw vector r in E^N. Define (Sr)[j]=r[j−1 mod N], and the positive-sign unnormalized Fourier map

R_k=Σ_(j=0)^(N−1)r_j omega^(kj).

The promised object is a polynomial C(z)=Σ_(a∈J)c_a z^a, with 1≤|J|≤s, distinct a in {0,...,N−1}, nonzero c_a and

C(S)r=e_0.                                                     (1)

The target is the combined polynomial C and the complete N-vector R. A factorization into graph binomials, a unique delay orientation, or a supplied impulse location is not required. Under the one-impulse graph application, shift/scale normalization is absorbed into C. General multiple-impulse sparse numerator/denominator recovery is outside this scope.

## Independent proof of the mapping

### Paid reciprocal probes

Fourier diagonalization of (1) gives C(omega^k)R_k=1. Therefore every R_k is nonzero. Compute R_k directly for k=0,...,2s−1, each from all N input coordinates, and batch-invert. The resulting moments are

b_k=1/R_k=C(omega^k)=Σ_(a∈J)c_a z_a^k, with z_a=omega^a.

This is the exact exponential-sum interface. A probe costs O(N), rather than one unit-cost query to the underlying raw vector. Failed zero probes are a safe rejection; promised inputs never have them.

### One rank computation handles unknown actual sparsity

Write t=|J| and let V_m be the m×t matrix with entries z_a^i for 0≤i<m. For H_m=(b_(i+j))_(0≤i,j<m),

H_m=V_m diag(c_a)V_m^T.

For m=t, det(H_t)=(∏c_a)∏_(a<b)(z_b−z_a)^2≠0, in every allowed characteristic. For m=s≥t, V_s is injective and V_s^T is surjective, so rank(H_s)=t. Thus one Gaussian rank computation on H_s recovers t in O(s^3). This avoids potentially invalid stopping at the first vanishing smaller leading minor, and avoids an O(s^4) repeated-solve loop.

Let A(Z)=Z^t+Σ_(j=0)^(t−1)a_jZ^j. Solve the nonsingular t×t system

Σ_j b_(i+j)a_j=−b_(i+t), 0≤i<t.

Substitution of the exponential expansion gives V_t diag(c_a)(A(z_a))_a=0. Both factors are invertible, so A(z_a)=0 for every a. Being monic of degree t, A is exactly ∏_(a∈J)(Z−z_a). This is the Prony annihilator with simple roots. The largest moment index used is 2t−1≤2s−1.

### No discrete logarithm or uncharged factoring

Evaluate A at each known omega^a for a=0,...,N−1 by Horner's rule. The t zero positions are the exponents themselves. This uses O(Ns) arithmetic, explicitly pays all N candidates, and requires no discrete-log or general polynomial-factorization oracle. Reject if there are not exactly t distinct grid roots. Solve the t×t Vandermonde system for the amplitudes; its determinant is nonzero. This costs O(s^3) with ordinary Gaussian elimination.

### Full soundness after an arbitrary prefix

The recurrence prefix alone is not a proof of raw membership. Check every coordinate

Σ_(a∈J)c_a r_(j−a)=1 if j=0, and 0 otherwise.                  (2)

This takes O(Ns) arithmetic. A failed equation declines the candidate. If all equations hold, Fourier diagonalization gives C(omega^k)R_k=1 for every k, so all denominators are nonzero and every exact output is 1/C(omega^k). Produce the full denominator vector by t geometric streams and batch-invert every entry. Thus acceptance is sound on arbitrary r, with no probabilistic fingerprint or omitted output. Under the promise, the earlier recovery is complete and (2) succeeds.

The combined sparse inverse is unique modulo z^N−1: equation (1) implies every Fourier coordinate of r is nonzero, so any two inverse polynomials of degree<N have identical N-grid values and are equal. This does not make the graph-binomial factorization or original delay representation unique.

## Exact paid ledger for the fresh verification algorithm

The fresh program uses one s×s rank computation and two t×t Gaussian solves instead of optimized BM. Its O(s^3) cost is already within the theorem's O(Ns+s^3) total. It returns either the complete certified transform or a decline reason; it does not implement a production fallback.

Let a field addition, subtraction, multiplication or inversion each cost one. The exact supplied-power table is an input; constructing its N entries from supplied omega would cost another N−1 multiplications and O(N) writes. Root validity/field acquisition, parsing, bit complexity and hardware costs are outside this scalar ledger and must be separately paid by a caller.

For any accepted or rejected input, the fresh program's field-operation count is at most

B(N,s)=6s^3+2s^2+12Ns+7s+3N+2.                                (3)

Derivation, including operations on zero/one when the code executes them:

- 2s dense probes: 4Ns multiplications (including twiddle stepping) and 2Ns additions, total 6Ns
- Batch inversion of 2s probes: 6s multiplications and one inversion
- s×s Gauss–Jordan rank: at most 2s^3−s^2+s operations
- Recurrence right-hand side: at most s subtractions
- Two t×t augmented Gauss–Jordan solves: at most 4s^3+2s^2 operations combined
- Vandermonde construction: at most s^2−s multiplications
- N-root Horner scan: at most 2Ns operations
- Full cyclic certificate: at most 2Ns operations
- All N denominator values by sparse streams: at most 2Ns operations
- Batch inversion of N outputs: 3N multiplications and one inversion

Summing gives (3). Early exits and zero elimination factors only reduce it. Gaussian elimination includes its pivot inversions and normalization of every augmented entry. Comparison/index/loop/container work is separate; the finite-word abstraction needs O(log N)-bit indices and explicit storage. This fresh algorithm uses O(N+s^2) stored field entries, including input, roots, output and dense Hankel matrices. That is O(N) only for fixed s or where s^2=O(N).

On the promised family, this proves the complete O(Ns+s^3) field bound. On arbitrary inputs it proves the same bounded-attempt toll. For fixed s, a separately admitted O(N log N) Fourier fallback would give that all-input envelope. A primitive Nth root alone does not supply all roots needed by the historical Bluestein backend. No unconditional arbitrary-field fallback complexity is accepted here.

## Fresh checks and reproducibility

The concrete checker operates in the declared prime fields; it is not an arbitrary-field executable or a field-discovery service. Only the newly written standard-library `check_fresh.py` was executed. Historical source programs, saved BM routines and saved exhaustive suites were not run. Its full-DFT audit oracles are deliberately separate from the charged recognition routine; they are verification tools, not a claimed fast fallback.

Final result: 29,204 input/cap decisions; 986 acceptances and 28,218 declines; 10,506 accepted Fourier output coordinates checked exactly.

- Complete F_7^3 census, cap s=1: 343 inputs, 18 accepted
- Complete F_13^4 census, cap s=2: 28,561 inputs, 672 accepted
- 296 structured cases for N=8,12,16,24,32,64 over F_97,F_193,F_257, covering t=s and t<s
- Every accepted case returns the exact support/coefficients, checks all N cyclic equations, and returns all N correct Fourier values
- Every census decision agrees with an independent full-spectrum inverse-support oracle
- All counted attempts obey (3); the census maxima 62 and 180 equal the bound at (N,s)=(3,1),(4,2)
- An altered length16 signal with all six training Fourier probes unchanged reconstructs the original candidate, then fails the full certificate
- A non-grid node, a repeated recurrence root, and a rank-two prefix with singular leading H_2 each decline at the appropriate guard

The all-size claims rest on the proof and operation accounting above, rather than extrapolation from these finite checks. These controls also do not certify the historical programs, production integration, numerical stability or complete Python/physical-resource costs.

## Proposed queue treatment

The one-primary-comparator stopping condition is met. After independent review, close the scoped comparator and preserve its exact match/nonmatch map. Keep the parent open at 42. Replace the selected-comparator action with its completion record while preserving earlier text verbatim. Do not reinterpret the primary source as a supplied-root finite-field runtime theorem or use its sampling lower bound here.

Broader historical priority, general multiple-forcing sparse rational discovery, historical Green/fallback admissibility, numerical/bit/runtime qualification and production wiring remain distinct. No successor is automatically launched by this comparison.
