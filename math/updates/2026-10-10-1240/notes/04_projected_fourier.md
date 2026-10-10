# HERO1 Phase 33 projected Fourier and modal decomposition

10 October 2026

Verdict

Accept the prime-power modal decomposition and the dyadic low-conductor projected transform as scoped exact-arithmetic results. The projection computes P_C F_N x exactly for arbitrary input, but its output has only 2^C + (t-C)2^(C-1) independent coordinates. The full transform still needs the discarded complement. The error identity is correct and is an immediate consequence of projector commutation and classical Parseval; it does not ensure that the error is small.

The supplied O(N + 4^C log N) algorithm is valid as an algebraic upper bound. A separate reviewer-derived comparison proposes O(N + (t-C+1)C 2^C) for the same output, using ordinary short FFTs and geometric sums. Its proof and self-checks are frozen in notes/06_projected_comparator.txt. The subsequent independent receipt in notes/07_projected_comparator_review.txt accepts its scope; the frozen note’s pending label records its earlier historical state. It is not part of the accepted source result or a claim of novelty or a faster unrestricted FFT. At C=t its accepted bound is ordinary O(N log N).

The all-input Mellin/Gauss implementation retains two expensive character-basis changes. Its published N=960 count of 17,432 exceeds the Phase29 reference 13,639 by 3,793 operations, approximately 27.81%. No full-FFT promotion is justified.

Source and review scope

Source archive: fft_hero1_phase33_20261010.zip, 10,518,219 bytes
SHA-256: d00b64d6cc6fad64a0d839d9efb789fbab681a80701c97fda18ccec3e24858fb
THEOREM.md SHA-256: 9d6c9d98cb4d8a9e302ff30502d6259bed9ba7f0e9e9af7cbd2cf5b910183a9c
low_conductor_projection.py SHA-256: 8232795745c1ad9ca68b9c165a9a37df8f41c520c4595fb0f1450029b1d793f9
mellin_gauss_fft.py SHA-256: 083142694566f3ecb2a27e5c42d9d0346f08633c144557614cbc26c775ed63c1

The archive CRC and all 35 supplied manifest entries pass. The embedded Phase32 ZIP is byte-identical to the separately retained Phase32 original, SHA-256 d1b121875a62c9743d9f0c1d0d5c093041ba5397128e6c9765fe355acb6281f7. Six inherited top-level modules match versions inside that lineage. The current theorem, implementation, tests, benchmarks, cost ledger, receipts, and references were inspected as inert text. Uploaded programs were never imported or executed. Only newly written independent controls ran. Source execution logs remain author-reported evidence; this audit does not relabel them as independent replay.

1. The projection and its domain

Assume N=2^t, t>=1, and integer 1<=C<=t. Let H_C={a in (Z/NZ)^*: a=1 mod 2^C}. For a permutation R_a of coordinates induced by multiplication by a, P_C=|H_C|^(-1) sum_{a in H_C} R_a. Over C this is the orthogonal projection onto H_C-invariant vectors. Each orbit is averaged with its own orbit size; repeated stabilizer elements in the group average give exactly the same average.

F_N R_a=R_(a^(-1)) F_N for the unnormalized positive-sign DFT. Inversion permutes H_C, so F_N P_C=P_C F_N. Individual multiplier permutations generally intertwine with their inverses rather than commute with F_N; only the subgroup average is being claimed to commute.

On the input shell k=2^(t-j)u, with u odd modulo 2^j, the orbits are the odd residues modulo 2^min(j,C). Their sizes are 2^(j-min(j,C)); zero is a singleton. Therefore

rank(P_C)=1+sum_{j=1}^t 2^(min(j,C)-1)
         =2^C+(t-C)2^(C-1).

The source's bucket representation, retained characters, and output scattering agree with these orbits. The output is an entire length-N vector, rather than selected ordinary frequency bins. Low multiplicative conductor is not the same as low additive frequency. No input sparsity or unverified detection promise is needed to compute the projected answer.

For C=1 the rank is t+1 and the component is the classical gcd-orbit/Ramanujan transform. For C=t, H_C is trivial and P_C=I. For every C<t, choose two distinct indices in one orbit and put +1 and -1 there, zero elsewhere. Then P_C x=0 while F_N x is nonzero. Thus the projected answer can lose 100% of the full transform's relative L2 energy. Exact membership in the invariant subspace can be checked by a linear scan of orbit members. Selecting a cutoff for a requested error tolerance is a separate input-dependent task, not a guarantee supplied by a fixed C.

2. Independent error derivation

Set r=(I-P_C)x and e=F_N x-P_C F_N x. Commutation gives e=F_N r. Character orthogonality gives F_N^* F_N=N I. Hence

||e||_2^2=r^* F_N^* F_N r=N||r||_2^2.

Equivalently, with B ranging over the index orbits and S_B=sum_{j in B}x_j,

||e||_2^2=N [sum_j |x_j|^2 - sum_B |S_B|^2/|B|].

Orbit sums and energy can be accumulated in O(N) arithmetic, with conjugation and real arithmetic included in the computational model. The scalar is a deterministic exact certificate of the ideal projected answer's norm error. It is not a bound on floating-point roundoff or on the accuracy with which that certificate is evaluated. The subtractive energy formula can suffer cancellation for nearly invariant input. Direct residual accumulation avoids that particular subtraction but still needs a rounding-error analysis.

Over a field of characteristic not dividing N with a primitive Nth root, the bilinear identity is sum_k e_k e_(-k)=N sum_j r_j^2. It has no positive-definite norm interpretation. A concrete counterexample to using a zero modular certificate as proof of zero error is N=8, C=1 over F_17, with x=(0,1,0,4,0,16,0,13) and Fourier root 9. P_C x=0, the certificate is zero, and the DFT error is (0,2,0,0,0,15,0,0), which is nonzero.

3. Mellin and Gauss decomposition

For N=q^t and a nonprincipal character on the order-q^j shell, let q^c be its conductor. When pairing with output shell ell, the additive phase has conductor exponent s=j+ell-t. If s<c, primitive character cancellation on reduction fibers gives zero. If s>c, the additive progression in a lifted fiber gives zero. At s=c the character sum is q^(j-c) tau_c(chi) chi(v)^(-1). Dividing by phi(q^j) gives tau_c(chi)/phi(q^c), independently of j and ell.

Thus the nonprincipal mode goes only to ell=t+c-j and the inverse character. The principal block is the stated prefix/difference Ramanujan block. Its support has (t^2+5t+2)/2 entries; adding N-t-1 monomial entries gives N+t(t+3)/2. The ordinary shell-normalized bases and F_N/sqrt(N) are unitary over C, so the normalized Gauss factors have modulus one. None of this removes the cost of constructing and applying the two bases.

For general odd q, spell out the phrase suitable root-rich field: the field must support the complete unit-group character bases, their nonzero size denominators, and the additive q^t roots. In positive characteristic a safe formulation requires characteristic not dividing q(q-1) and all requisite roots of unity. Merely excluding characteristic q is not sufficient to guarantee a complete character decomposition. The supplied odd-prime reference does require divisibility by all shell group sizes, so its tested domain meets the stronger requirement. In characteristic zero these issues disappear after adjoining the required roots.

The delivered Python implementation is modular, not a complex floating-point implementation. Its algebraic formulas extend to characteristic zero. Exact operations in Q(zeta_N), exact complex arithmetic, and machine arithmetic have different costs; the paper does not establish the latter two as executable constant-cost bit models.

4. Cost of the supplied projected evaluator

Let b_j=2^(min(j,C)-1). A direct count of the source's logged arithmetic gives

T_online=N+t-1+sum_{j=1}^t (b_j-1)(5b_j-1).

The N+t-1 part combines bucket accumulation, shell totals, and principal prefix/differences. Each nonprincipal shell extraction contributes (b_j-1)(2b_j-1), and output synthesis contributes 3b_j(b_j-1). This reproduces all 16 published projected benchmark rows without running the source.

For C>=2, with a_2=1 and a_c=2^(c-2) for c>=3, the logged setup count is

T_setup=t-1+sum_{c=2}^C [2^c+2^(c-2)-1+a_c 2^c].

For C=1 it is zero. These formulas prove O(N+t4^C) online work and O(t+4^C) coefficient setup. A tighter uniform form for this particular evaluator is Theta(N+(t-C+1)4^C). At C=t its direct character tables and work are Theta(N^2), not an FFT improvement. Fixed C yields linear work; more generally a growing C can remain in the linear regime when (t-C+1)4^C=O(N). None of these regimes guarantees small error for arbitrary input.

For N=4096, C=1,2,3,4, the logged online counts are 4107, 4206, 4686, 6630 and setup counts are 0,19,44,127. The ranks are 13,24,44,80. These figures concern different projected outputs, not substitutes for all 4096 independent Fourier outputs.

Counter qualifications

(a) low_conductor_projection.py lines 68-69 execute two unary negations when preparing signed character and inverse-character entries, without charging them. The literal counts are 2,6,22 at C=2,3,4, or (4^(C-1)+2)/3 for C>=2. A sign-free coefficient representation or an optimized shared table can change that count. State the sign convention or charge the literal operations. The omission is O(4^C), so the asymptotic claim survives.

(b) The projection's hot loops charge every written multiplication, including identity coefficients. They are consequently valid upper counts of scalar multiplies, but do not literally implement the ledger's stated convention of counting only nonidentity multipliers. They should not be described as an optimized exact minimum under that convention.

(c) The plan constructors actually execute modular exponentiation to validate the supplied root before initializing their arithmetic counters. This cost is outside the printed setup totals, even though validation is described as optional in the prose. It is O(log N) field multiplications for the dyadic order test, provided the supplied modulus is already known to be prime. Root search, primality certification, and arithmetic on the modulus are separate costs. Full-plan exact warm formulas are correctly restricted in the theorem to complex arithmetic and the two tested fields; do not generalize the equality to every finite field. For example, N=4, p=5, root=3 has its nonprincipal Gauss multiplier equal to 1, so the source's identity-skipping branch gives 11 rather than the general formula's 12 operations.

(d) The reciprocal of 2 is formed as an integer expression from p. This is legitimate for a supplied odd prime modulus, but a characteristic-zero port must declare rational constants, inversion, and representation costs. Prepared inverse character tables do eliminate per-element hot-loop modular inversions.

(e) Reads, writes, integer residues, dictionaries, allocations, and routing are not all included in the arithmetic counter. With O(log N)-bit word indices the stated loops fit O(N+t4^C) word work and O(N+t2^C+4^C) stored field elements/index words. Python integer bit costs and object overhead are outside those bounds. Reading arbitrary dense input and materializing all N outputs each require Omega(N) accesses.

(f) The norm certificate is mathematically derivable and tested algebraically. calculate(return_witness=True) returns dimension/bucket metadata, not a numerical complex error certificate. A caller must compute the input residual energy separately; that adds O(N), not zero, work.

5. Separately reviewed same-output comparator

The bounded supplemental note notes/06_projected_comparator.txt derives a same-output comparison from orbit geometric sums and short additive FFTs. It establishes O(N+(t-C+1)C2^C) field and word-RAM work including coefficient preparation, with O(N+(t-C+1)2^C) space, for 1<=C<=t. It needs only a primitive 2^C-th root. Its complete output definition, proof, setup, boundary cases, readout charges, and exclusions are in that frozen note.

The comparator's self-check agrees with all 56 fresh modular projected cases and a 64-entry reduced projected-matrix case in F_5, where the full length-64 DFT is not defined. Those author-side self-checks alone were not an independent second review. The later independent proof and controls now accept the comparator, as recorded in notes/07_projected_comparator_review.txt and its hash-bound receipt; it remains separate from the submitted source algorithm. The source's O(N+t4^C) bound is accepted without relying on this comparator.

6. The full-transform comparator remains negative

The source's warm dyadic formula is (3t-7)N+6t+4; its coefficient setup is 3(t-2)N/2+2t+2, under the stated conventions. Both are Theta(N log N). The central stage alone is linear, but the two basis changes dominate. The native radix-2 reference has (3t/2-1)N+1 warm operations; the Mellin method is equal only at N=2 and is more expensive thereafter in the displayed comparisons.

Combining the dyadic method with the inherited 15-point kernel gives 1354, 3188, 7486, 17432 at N=120,240,480,960. The Phase29 reference values are 1178,2701,6107,13639. All supplied formula rows reproduce analytically. Author-reported executions stop at 960 for this comparison; the larger CRT rows are explicitly extrapolations. This review did not rerun either uploaded circuit. The stronger same-output full FFT reference is unchanged.

7. Independent controls completed

- All archive CRCs and all 35 manifest hashes, plus exact identity of the separately retained Phase32 archive
- 56 dyadic projected cases in new primes 12289 and 65537, N=2 through 128 and every valid C: orbit dimension, projector idempotence, commutation, conductor routing, direct projected DFT, bilinear Parseval, and the additive-quotient comparator
- 3076 dense projected-output entries and 12744 complete basis-entry comparisons through N=32
- 12 complete modal matrices, totaling 5283 entries: dyadic N=2,4,8,16,32 and odd N=3,9,27,5,25,7,49, using newly selected cases/fields and direct character sums
- 15 exact characteristic-zero checks in Q[z]/(z^(M/2)+1), with genuinely complex rational-plus-i-rational input, every C through N=32; commutation, projection, the Hermitian error identity, and orbit-energy formula all hold exactly
- All 16 projected benchmark rows, all 12 dyadic cost rows, and all 7 CRT comparison rows reproduced from independent counting formulas
- Negative controls for every proper cutoff, an explicit nonzero finite-field error with zero certificate, and an identity Gauss multiplier illustrating field-dependent instruction counts
- A 64-entry low-root-only projected example over F_5

These are finite controls supporting the derivations. They are not exhaustive verification of the source executable, numerical stability, arbitrary algebraic representations, or historical priority. The reusable independent code uses only the Python standard library and never imports the supplied programs.

8. Primary prior art and novelty boundary

NIST DLMF 27.10.9-12 gives the Gauss-sum Fourier identity and primitive Gauss magnitude; 27.10.4-5 gives the Ramanujan sum and its divisor formula. These cover the main analytic ingredients. The conductor-shell routing and support count follow by lifting those identities and counting modes; this review has not established priority for that particular formulation.
https://dlmf.nist.gov/27.10

Toth and Haukkanen, The discrete Fourier transform of r-even functions, equation (7) and Proposition 2, give Parseval and the invariant gcd-even Ramanujan transform. Their Proposition 2 explicitly attributes related forms to earlier authors. The C=1 component and the norm identity therefore should not be advertised as new Fourier principles.
https://arxiv.org/pdf/1009.5281

Brodzik and Tolimieri, Fourier and Zak transforms of multiplicative characters (2021), Sections 2-4, analyze primitive character transforms, Gauss sums, and CRT combinations, primarily for odd moduli. The authors themselves describe the primitive DFT formula as prior material. It is relevant context, not direct evidence that the present dyadic implementation or exact C-bound is new.
https://arxiv.org/pdf/2104.09295

The more directly relevant earlier lead is Richard Tolimieri, Multiplicative characters and the discrete Fourier transform, Advances in Applied Mathematics 7(3), 344-380 (1986), DOI 10.1016/0196-8858(86)90039-4. Its publisher abstract explicitly describes DFT decomposition into subspaces defined by multiplicative characters and its relation to multiplicative complexity. The abstract was available; a full-text request was blocked. It is a priority-review requirement, not proof that its full algorithm coincides with Phase33.
https://www.sciencedirect.com/science/article/pii/0196885886900394

The package can claim a tested project implementation, transparent negative benchmark, explicit conductor bookkeeping, and a useful restricted-output evaluator. It cannot currently claim historical originality of the mathematical ingredients, an optimal projected algorithm, a floating-point speedup, or an unrestricted sub-N log N FFT.

Next acceptance gate

Keep the restricted projection as a valid tool, with the sign, validation, certificate, and field qualifications above. For any full-FFT advancement, require an explicit all-input circuit that pays for both basis boundaries, omitted modes, constants, reconstruction, routing, and precision; then compare the same complete output against the strongest applicable circuit. The independently accepted additive-quotient comparison now supplies a same-output comparator for projected-output comparisons. It remains a separate construction from the submitted implementation.


Current comparator status: independently accepted. See notes/07_projected_comparator_review.txt and certificates/projected_comparator/REVIEW_RECEIPT.json. That receipt also records a nested-support reconstruction using O(N) reconstruction work and O(2^C) auxiliary workspace beyond explicit input/output; this preserves the same total field-work theorem rather than creating a new source family.
