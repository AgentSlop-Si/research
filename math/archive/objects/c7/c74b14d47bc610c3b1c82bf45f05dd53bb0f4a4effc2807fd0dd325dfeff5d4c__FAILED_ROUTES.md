# Selected routes, failures, and scope boundaries

1. Repeat the accepted B5 or Cq factors on the five-coordinate fibers.
   Failure: off-diagonal fiber blocks have different ρ_bd in equation (4). They are not copies of the principal block, and the full matrix is coupled. The exact CRT formula preserves all those terms.

2. Use the same reciprocal pole pair with independent endpoints on each coupled block.
   Failure: generically t+t⁻¹ is a forced degree-five rational function of ρ. N=45 already has five unequal required traces. The infinite N=5q² bank lower bound is ceil((q−8)/5), with a zero floor.

3. Preaggregate inputs using fixed five-coordinate kernels and separable endpoint arrays.
   Failure: each full branch then has rank at most five. The complementary fiber cut has rank 5 floor(m/2), so at least floor(m/2) branches are necessary. Allowing nonseparable scalar couplings removes the rank obstruction only by reinstating a substantive matrix application.

4. Treat the per-block diagonal repair as a single global diagonal.
   Failure: a diagonal within B[b,d] with b≠d still moves data between fibers. Such repairs form five m×m operators, not an N-entry diagonal.

5. Infer cheapness from tensor rank three.
   Failure: the coupling matrices are F_m and H_m. The fully charged formula uses ten length-m Fourier transforms, plus O(N) work. Tensor-kernel count is not Green-solve count or arithmetic cost.

6. Diagonalize the constant five-dimensional chirp to close a B recursion.
   Partial success: this gives the exact full shifted-resolvent identity (22), with five independent smaller channels across three shifts and matching nonresonance guards. Remaining failure: the accepted B5 certificate does not implement arbitrary smaller shifted resolvents. The setup and root-extension costs remain explicit.

7. Split q² into two CRT factors q and q.
   Invalid because the factors are not coprime. The corrected residue decomposition is (5), with the nontrivial θ^(st) twiddle and two stages of q transforms. Its standard recurrence is Θ(N log N), not a speedup.

8. Modular-control implementation initially asked for the unshifted B5 while only its Fourier/chirp kernels were needed.
   At N=15,p=31 this unshifted inverse is resonant. The checker was corrected to distinguish kernel generation from inverse construction, and still checks every inverse actually used. This is not a bypass of a failed inverse: identity (22) needs only shifted smaller inverses, whose denominator is exactly the full nonzero denominator.

9. Initial conservative invariant degree bound was 18 with 32 exceptional roots.
   Exact cyclotomic polynomial cancellation improves these to a coprime degree-five rational function and eight distinct exceptional roots. The final checker independently reconstructs and verifies both cancellations. No conclusion depends on a sampled fit or an exploratory symbolic package's answer.

Not excluded: arbitrary global Hamiltonian orders; several reciprocal pairs summed inside each 5×5 block; alternative local orders; nonseparable coupling matrices with an independently proved cheap algorithm; other fast Fourier circuit models. The proved obstruction is deliberately narrower than these open possibilities.

10. Optional finite-field endpoint reconstruction at every invariant-regular block.
    Some reductions have a zero norm of 1+t. The invariant guard proves necessity of the trace, not sufficiency for a legal reconstruction at every finite specialization. The checker now verifies traces at all invariant-regular blocks, and performs the stronger endpoint test only with the additional reconstruction norms nonzero, recording both counts. This does not weaken the pole-bank obstruction.
