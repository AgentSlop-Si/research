# What the fixed-interface exterior would compute

9 October 2026. Exact cost-preserving reductions. No new paired-Green factors, numerical coefficient scan, FFT speedup, or arithmetic lower bound is claimed.

## 1. Conclusion

For a full bank, applying the unique exterior P is exactly equivalent to applying m independent, arbitrary-input length-q DFTs, up to O(N) twiddle and routing work. The sparse interface certificate does not evaluate those transforms.

For a partial bank, blindly stripping the complementary transforms requires paying for their inverses. However, for the fixed contiguous active set there is a stronger exact reduction: ceil(q/|J|) calls to P recover the same arbitrary-input batch using support splitting, shifts, and phases, with no inverse Fourier calls. A constant active fraction makes this a constant-call reduction. In a square split, an O(N) evaluator for this P would consequently give an O(N) evaluator for the full N-point Fourier transform. The same conclusion extends to the usual near-square dyadic split.

This identifies the remaining work precisely. The fixed-interface target asks for a cheap implementation of missing batched Fourier work; solving its sparse interface equations alone is not a separate algorithm for that work. The useful new simplification here is the explicit bounded-call reduction, not a construction of P.

## 2. Contract and charged cost model

Let N=mq over a splitting field of characteristic not dividing N, with a supplied primitive N-th root omega. Fourier matrices are positive-sign and unnormalized. Use bank coordinates (r,t), 0<=r<q and 0<=t<m, at linear index rm+t. Put

    L=F_q tensor I_m,
    Delta[rm+t,rm+t]=omega^(rt),
    C=B_(J complement),
    P_J=L Delta C.

The unique exterior and its interface come from the preceding uniqueness report. Let E_J select the active bank coordinates. The stride permutation R_0 obeys (R_0 x)[rm+s]=x[r+qs], and F_N=P_J B_J R_0.

An evaluator has an input-independent preparation cost and a fresh-vector application cost. Every reduction below charges twiddle generation, routes, selector scans, output additions, and any Fourier or inverse-Fourier calls. Repeated calls can share already-generated P coefficients. If both preparation and application of P are O(N), every constant-call construction below is uniformly O(N), with O(N) auxiliary words when calls are processed sequentially. Supplied roots and exact field arithmetic are the same assumptions as in the existing bank target.

## 3. Full bank: exact equivalence in both directions

If J is all q blocks, then C=I and

    P_all=L Delta,             L=P_all Delta^-1.    (1)

Writing a vector z as a q-by-m array, the action of L is

    (L z)[um+t]=sum_(r=0)^(q-1) omega_q^(ur) z[rm+t].

For each t this is one length-q DFT; there are m independent columns. Their input values are completely arbitrary and independent. Multiplication by the nonzero diagonal Delta is bijective and introduces no structured-input restriction.

Thus:

- To apply P_all, multiply by Delta in O(N), then evaluate the m DFTs.
- To evaluate the m DFTs, multiply the arbitrary input by Delta^-1 in O(N), then call P_all.

Interleaving or collecting the m transform vectors costs O(N) routing. The required forward and inverse twiddle tables are generated in O(N) by consecutive-power recurrences. If App(A) denotes fresh-vector arithmetic work, then

    App(P_all) <= App(L)+O(N),
    App(L) <= App(P_all)+O(N).

The same additive overhead applies to uniform preparation. A hypothetical O(N) paired-Green P_all would therefore evaluate m independent length-q DFTs in O(N) total work. Its sparse Weyl interface is a certificate of the required map, not an implementation of these independent transforms.

## 4. Partial banks: stripping and its paid inverse cost

For any active set J,

    P_J=P_all C,
    P_all=P_J C^-1,
    L=P_J C^-1 Delta^-1.                            (2)

C^-1 is identity on active blocks and F_m^-1 on the q-|J| complementary blocks. Since

    F_m^-1=(1/m) J_m F_m,

where J_m reverses indices modulo m, one inverse costs one ordinary length-m DFT plus O(m) reversal/scaling. If T(m) is a charged ordinary DFT evaluator, either inserting C or stripping C costs

    (q-|J|) T(m)+O(N).

For example, evaluating arbitrary Lz using (2) requires, in order: Delta^-1 z, then C^-1, then P_J. Delta and C generally do not commute. The inverse transforms cannot be omitted, reordered past Delta without proof, or counted as free preprocessing of fresh arbitrary input.

Consequently the unconditional cost comparison from direct stripping is

    App(L) <= App(P_J)+(q-|J|)T(m)+O(N),
    App(P_J) <= App(L)+(q-|J|)T(m)+O(N).

These are reductions, not lower bounds. They do not establish that every evaluator must literally execute those complementary transforms.

## 5. A stronger exact reduction for a contiguous active interval

Suppose J is a nonempty cyclic interval of j=|J| blocks beginning at a_0. Let k=ceil(q/j). Partition the q input row indices into nonwrapping intervals

    I_l={lj,...,min((l+1)j,q)-1},     0<=l<k.

Let E_(I_l) select all m coordinates in those rows. Define

    U_a=S_q^a tensor I_m,         M_a=D_q^a tensor I_m,
    a_l=a_0-lj mod q.

U_(a_l) moves the support of I_l into J, and the Fourier shift rule gives

    L U_a=M_a L.

For any vector v supported in J, C Delta^-1 v=Delta^-1 v, because the complementary Fourier blocks receive zero. Therefore

    P_J Delta^-1 v=L v.

Applying this to each shifted piece proves the exact operator identity

    L=sum_(l=0)^(k-1)
        M_(-a_l) P_J Delta^-1 U_(a_l) E_(I_l).      (3)

No Fourier inverse appears. Every original input coordinate belongs to exactly one I_l, so this computes all m length-q DFTs on unrestricted fresh input, not merely sparse-input transforms. The pieces are arbitrary masked portions of that input and are added back with the exact modulation correction.

Equation (3) costs

    preparation(P_J)+k*application(P_J)+O(kN),

with O(N) reusable scratch and a shared P_J coefficient table. In particular, for j>=theta*q with fixed theta>0, k<=ceil(1/theta) is constant. A uniformly O(N) P_J then supplies the arbitrary-input Fourier batch in O(N), without paying the inverse-bank cost in Section 4.

The interval assumption matters. The same construction works if J merely contains a cyclic interval of length ell, using k=ceil(q/ell). It does not claim that an arbitrary density-theta set has a constant-size translate cover. A fixed number of active intervals with fixed total density does contain a proportional-length interval, so the corresponding bounded-boundary layouts retain a constant-call bound.

For J empty, formula (3) is undefined and unnecessary: B_J=I, so F_N=P_empty R_0 already. For J full, k=1 and (3) reduces to the full-bank formula (1).

## 6. Square split: the same missing batch is the other FFT bank

Let m=q=M and N=M^2. Let K be the grid-transpose permutation K e_(rM+t)=e_(tM+r). Then

    B_all=I_M tensor F_M=K L K.                    (4)

Thus an evaluator for L immediately evaluates the complete input Fourier bank by two O(N) transpositions. The active bank is

    B_J=E_J B_all+(I-E_J),

so it costs one B_all evaluation plus O(N) selection to retain transformed active blocks and original inactive blocks.

Combining (3)-(4) with F_N=P_J B_J R_0 gives an explicit algorithm using

    k+1 calls to P_J, plus O(kN) routing,
    twiddle multiplication, selection, and addition. (5)

For full activity this is two P_all calls. For a contiguous half-active bank it is three P_J calls. All inputs to every call are explicitly computed arbitrary vectors; there is no hidden transform, inverse transform, dense solve, or free spectral encoding.

Consequently a uniformly O(N) paired-Green realization of this fixed square-interface P_J, with a fixed nonzero active fraction, would yield a uniformly O(N) full N-point DFT evaluator. This is a conditional implication, not a discovered linear-time DFT. Density of P_J is irrelevant to the implication and supplies no contrary lower bound.

There is a converse constant-factor batch reduction for square splits. Since

    C=E_J+(I-E_J) K L K,
    P_J=L Delta [E_J+(I-E_J) K L K],               (6)

two calls to L, plus O(N) work, evaluate P_J for any J. Together with (3), a contiguous constant-fraction partial-bank exterior and the arbitrary-input batched Fourier map are computationally equivalent up to constant call factors and linear overhead. The full bank has the sharper one-call equivalence.

## 7. Near-square dyadic extension, with the small radix paid

The consequence is not confined to powers of four. Suppose m=rq, where r is a fixed positive integer, in particular r=2 for the usual odd-exponent dyadic split. There are q length-m transforms in B_all. Ordinary radix-r Cooley-Tukey decomposes those into exactly rq=m independent length-q transforms, which are precisely the batch L, plus N/r length-r transforms, twiddles, and routing.

Explicitly, for input bank b<q, write its length-m input index as h+rs, with h<r and s<q. Permute it to L-input position

    s*m+(b*r+h).

After applying L, denote its value at t*m+(b*r+h) by Y_(b,h,t). The bank output at b*m+(t+qu) is

    sum_(h=0)^(r-1) omega_m^(ht) omega_r^(hu) Y_(b,h,t).

This is one length-r DFT for each pair (b,t), after twiddles. Its charged work is (N/r)T(r)+O(N), which is O(N) only when r is fixed or a separately proved bound makes it so. For r=1 this is the grid-transpose identity. For r=2 the remaining transforms are ordinary two-point butterflies.

Therefore B_all requires one L call plus O(N) work for the usual balanced dyadic split m/q in {1,2}. The k+1 call consequence (5) continues to hold. If a proposed all-dyadic family supplied an O(N) exterior for those splits and a fixed nonzero active interval fraction, it would supply an O(N) DFT on every supported dyadic size. Growing radix work is not silently treated as linear.

## 8. What survives as a construction target

The exact reduction (3) is a useful simplification: it removes inverse complementary Fourier work from a constant-fraction interval reduction by making a bounded number of calls. It does not build the called P_J. Sections 3 and 6 show that this P_J already encodes the missing arbitrary-input Fourier batch, up to cheap maps and bounded call factors.

A successful paired-Green construction must therefore supply the real new ingredient: uniformly generated legal masks, cycle routes and monomial endpoints whose two-layer action evaluates that batch in O(N) total work. Sparse interface actions, the one-dimensional solution space of the intertwining equations, a closed entry formula, and low-cost verification do not supply that evaluator.

No distinct cheap paired-Green simplification has been established here. The fixed-interface approach is a precisely formulated factorization challenge for existing batched Fourier work; its certificate cannot be counted as an algorithm that has already solved the challenge.

## Exact controls

`verify_batched_equivalence.py` is newly authored and executes no uploaded code. It checks both full-bank directions, correctly ordered partial stripping, the support-splitting operator identity for wrapped and unwrapped intervals, square reconstruction of B_all and F_N, and the explicit fixed-radix batched conversion. Results are recorded in `BATCHED_EQUIVALENCE_CONTROLS.json`. All-size proofs are the identities above; finite controls check signs, routes and normalization.
