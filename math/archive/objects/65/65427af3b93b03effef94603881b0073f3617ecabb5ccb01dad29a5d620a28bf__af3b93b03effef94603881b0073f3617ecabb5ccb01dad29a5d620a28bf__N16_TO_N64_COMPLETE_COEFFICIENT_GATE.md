# A complete N16-to-N64 coefficient-lift gate

## What this system asks

The N16 seed is now an independently accepted algebraic solution of the specified 384-endpoint model. This note defines an exact next-size problem that genuinely refers to that seed. It does not assert that a lift exists and does not launch a numerical search.

Two branches are distinguished: a full route-descendant family with 1536 free physical coefficients, and a mean-anchored family with 1152 free nontrivial fiber-character coefficients whose trivial character is fixed by the actual N16 seed. Both must satisfy all 4096 complex N64 Fourier entries. A necessary high-x symmetry-breaking budget is also proved.

## 1. Fix every geometric and algebraic convention

The small grid is 4 by 4, with index v=4x+y. The large grid is 8 by 8, with index k=8X+Y. The projection is

    pi(X,Y)=(X mod 4,Y mod 4),
    X=x+4 epsilon_x, Y=y+4 epsilon_y,
    e=2 epsilon_x+epsilon_y.

For each of the eight labels, use exactly the accepted N16 seed's least-representative-spliced cycle P_j,16. Build P_j,64 by the deterministic nested lift: P0=eta_hat T_64 with eta=P_j,16 T_16^(-1), then rotate the four successors at tails over base vertex 0. Do not replace these with independently min-spliced N64 routes. `N16_TO_N64_SYSTEM.json` contains all eight small and large successor arrays.

Keep the eight scalar poles tau_j=1/(j+2). Set G_j,64=(I-tau_j P_j,64)^(-1). The explicit inverse-entry formula is

    G_j,64[i,k]=(j+2)^(64-p)/((j+2)^64-1)
    when P_j,64^p(k)=i, 0<=p<64.

Every denominator is a specified positive integer. All inverse guards are fixed and nonzero.

Use the large bank B64 with eight length-eight blocks. Blocks x in {0,1,4,5} carry F8 and the other blocks carry I8. This is the pullback of the N16 active labels {0,1}; it has active mass 32 of 64. The bank is not the contiguous first four blocks.

Work over K64=Q[u]/(u^32+1), with the embedding 0<arg(u)<pi/16. Thus u=exp(2 pi i/64), the small Fourier root is z=u^4, and the bank F8 uses u^8. The small coefficient field is embedded by its defining isolated polynomial root, not by rounding its numerical discovery file.

Let a*_l,v,j denote the accepted small algebraic coefficients, ordered by layer l=0,1,2, base vertex v=0,...,15, and term j=0,...,7. They are exactly

    a*=a0+V y*,

where a0,V are the accepted dyadic data and y* is the unique root in ||y||_infinity<=10^-9 of the 256 specified small equations. The exact chart SHA256 is 904d7d24bf3aeee0a7c206eb8fd98ee11045fbc22cc97a105511b51907e1b188.

## 2. Full large family: 1536 variables and 4096 equations

For physical coefficients A_l,v,j,e define

    H_l,64 = sum_j diag(A_l,:,j) G_j,64,
    C64 = H_2,64 H_1,64 B64 H_0,64.

There are 3*8*64=1536 complex physical variables and exactly 24 Green occurrences. Impose

    C64[i,k]=u^(i*k), 0<=i,k<64,
    A_l,v,j,e != 0 for all 1536 entries.

These are 4096 cubic complex equations. Equivalently use all 64 seed-column conditions C64[i,0]=1 and all 4032 successor conditions C64[i,k+1]=u^i C64[i,k], k<63. Neither the seed column nor any successor row may be omitted.

This branch uses the seed routes but leaves the new coefficient law unanchored. Its solutions, if any, would prove existence in a nested-route family, not that the accepted small coefficients lift by a specified law. The parameter count gives no existence guarantee; the map is overdetermined at N64.

## 3. A genuine seed-anchored four-fiber law

Choose the explicit normalization allocation gamma=(1,1,2). This gives product gamma_0 gamma_1 gamma_2=2, the normalization-balanced scalar multiplier studied earlier. Define

    A_l,v,j,e = gamma_l a*_l,v,j
                + sum_(c=1)^3 b_l,v,j,c chi_c(e),
    chi_c(e)=(-1)^(c dot e).

The 384 trivial-character means are fixed to the accepted seed (with the stated scales). The remaining 3*3*8*16=1152 complex coefficients b are free. This is a concrete testable anchoring convention, not a theorem that every useful lift must have these means or this scale allocation.

All 4096 large entry equations and all 1536 physical nonzero guards remain. In terms of algebraic root coordinates one may instead solve a coupled system in y and b:

- 256 small root coordinates y, isolated by the already certified polydisk;
- 1152 nontrivial large-character coefficients b;
- 256 small equations f16(y)=0;
- 4096 large equations C64(a0+Vy,b)=F64.

This totals 1408 unknowns and 4352 equations. The small equations and isolation condition force the already accepted seed; they do not allow drifting to an unrelated N16 solution. Nonzero bounds for the small physical coefficients are already certified, while all large physical endpoints still need new guards.

The choice gamma=(1,1,2) keeps the first two means unchanged and doubles the outer layer mean. Other declared nonzero scale allocations could be separate branches. Nothing is gained by silently varying them during a fixed-branch rejection test.

## 4. Exact outer elimination, if useful

For the full family fix inner coefficients and write X=H_1,64 B64 H_0,64. At each output row i the eight outer templates are row_i(G_j,64 X). A successful Fourier identity makes X invertible. The fixed G templates have exact row rank eight, so the transported templates also have rank eight.

Choose and record eight pivot columns per row. Solving them eliminates all 512 outer physical entries. Keep the 64 nonzero pivot-minor guards and every reconstructed endpoint nonzero guard. The remaining 64*(64-8)=3584 entry-compatibility equations are in 1024 inner physical variables. A singular chosen pivot chart calls for a different chart; it is not a rejection of the whole family.

For the mean-anchored branch, the inner mean constraints leave 768 nontrivial inner character variables over the accepted seed field. After outer elimination, add the 128 outer mean equations to the 3584 entry residuals. This gives 3712 compatibility/mean equations in 768 inner variables. If the small root coordinates are carried explicitly, add their 256 unknowns, 256 equations, and isolating condition.

As before, clearing an eight-template determinant can raise the residual degree to 16. Direct cubic verification of every full-product entry remains the clean final acceptance step.

## 5. Necessary high-x mask budget

Let X_high be the global shift by 32, equivalently the high-x sheet swap. The nested routes at N64 and the pulled-back bank commute with X_high. Thus each scalar-pole Green commutes with X_high.

For Fourier, F64 X_high=D F64 where D=diag((-1)^i). Consequently

    [X_high,F64]=(X_high-D)F64.

The shift by 32 preserves parity, so X_high and D commute. Each physical pair {i,i+32} has one eigenvector of X_high equal to its common parity sign and one with the opposite sign. Therefore X_high-D has rank one per pair and

    rank([X_high,F64])=32.

For C=H_2 H_1 B H_0, the commutator product rule and [X_high,B]=0 imply

    32 <= sum_(l=0)^2 rank([X_high,H_l]).

For one masked term, since its Green commutes with X_high and is invertible,

    rank([X_high,diag(A)G])=rank([X_high,diag(A)]).

The latter is twice the number of high-x pairs on which A differs. Rank subadditivity across all 24 occurrences gives

    sum_(l,j) #{high-x pairs with unequal mask values} >= 16.

In the character law of section 3, the two high-x differences in base fiber v are, up to sign,

    2(b_l,v,j,2+b_l,v,j,3),
    2(b_l,v,j,2-b_l,v,j,3).

Thus at least 16 of these pair differences across the 24 masks must be nonzero. Restricting to b_2=b_3=0 leaves only alpha+beta chi_y masks and fails immediately. Nonconstant high-y dependence alone does not suffice, despite supplying rank freedom for the earlier scalar-descent test.

This is a necessary aggregate rank/symmetry budget. High-rank diagonal defects remain cheap to apply, so no runtime lower bound follows.

The earlier quotient-descent bound also applies separately: for this half-active small bank, the sum of three layer-descent-defect ranks must be at least 8. It does not replace the high-x commutator requirement.

## 6. What would count as a complete lift certificate

Accept either an explicit algebraic coefficient representation with exact verification of all 4096 entries and guards, or a rigorous isolated-root certificate for a complete equivalent polynomial system. A decimal least-squares residual would only be a discovery signal.

Unlike the N16 problem, a square-Jacobian contraction argument for an arbitrary subset of equations is insufficient here. The full branch has 2560 more equations than variables; the coupled anchored branch has 2944 more. If one certifies a square subsystem, every omitted equation still needs an exact consequence certificate, for example a polynomial ideal-membership identity with all denominators and saturation guards stated, or an exact algebraic evaluation at the isolated root. Numerical smallness of the omitted residuals cannot replace that step.

A negative result must identify its scope: a particular mean anchoring, a particular algebraic chart, a finite search domain, or a proved incompatibility of the entire specified family. Failure of the anchored branch would not exclude unanchored large coefficients, changed poles, extra masks, a different bank, or other route families.

## 7. Geometry mismatch and cost obligations remain explicit

This defines a genuine first nested geometry step from the N16 seed routes. It does not connect that chain to the independent expansion-certified seed geometries at N=2^17 and N=2^18. Starting the nested recurrence from N16 preserves its own routes and masks, not the unrelated threshold-size min-spliced bases. Any expansion guarantee or coefficient bridge must be supplied for the chosen chain.

Even a successful N64 lift would still need a uniform rule for later sizes, every inverse/endpoint guard, a charged coefficient generator, and a bounded term/state count. The four-character operator identities alone give standard four-subtransform accounting, not a speedup.

## 8. Bounded construction controls

`build_lift_system.py` generates the exact geometry, model ledger, and fixed denominator guards without searching for coefficients. It verifies all 64 eight-template row ranks, commutation of every Green and the pulled-back bank with X_high, rank 32 of the Fourier commutator, and the exact high-x pair-count formula for all four pure characters. `N16_TO_N64_SYSTEM.json` records the complete arrays and counts. No uploaded source or numerical coefficient search is executed.

## 9. Which extensions change the parameter budget?

The N16 submersion certificate cannot be transferred by parameter counting. At N16 there were 384 physical complex coefficients for 256 entry equations. At N64 the unchanged 24-term, one-endpoint family has 1536 coefficients for 4096 entries, so its generic Jacobian cannot be surjective. Fourier is one specific target; this dimension observation does not prove it is outside the image.

Some natural extensions remain O(N) in parameters and scan work per fixed term:

- Giving each of the 24 occurrences its own scalar pole adds only 24 parameters, for 1560 raw parameters at N64. Using one pole per order shared across layers adds eight instead.
- Adding an arbitrary right endpoint to every fixed-pole term gives 3072 raw endpoint parameters. Each term has the scalar gauge (a,b)->(lambda a,lambda^(-1)b), so its effective count is at most 127 rather than 128 at N64.
- Arbitrary nonzero edge weights and both endpoints appear to give 4608 raw parameters, but most of the edge freedom is a gauge. For a weighted cyclic shift D_w P, choose tau with tau^64=product(w), and a diagonal D_s with w_target=tau s_target/s_source. Then

      (I-D_w P)^(-1)=D_s (I-tau P)^(-1) D_s^(-1).

  Both endpoint diagonals absorb D_s. Thus the nonzero-weight family is locally equivalent, up to a finite root choice, to two endpoints and one scalar pole: at most 2N=128 effective complex parameters per term after the endpoint scalar gauge. For 24 terms the bound is 3072, still below 4096. Two global layer-rescaling gauges can reduce the product-image dimension further. Raw edge-weight counts must not be mistaken for independent coefficient freedom.

These statements concern generic dimension and gauges, not Fourier impossibility. They identify why merely adding poles or weighted edges does not restore the N16 generic-submersion argument at N64. Allowing more terms, new orders, or stronger nonlinear structure is a different declared branch and must be charged. A fixed finite number of ordinary scans remains linear to apply even when its parameterized image is low-dimensional.

## 10. A sharply bounded next experiment

A useful first target-specific test is an outer-correction law, rather than indefinite optimization of the overdetermined system:

1. Freeze both inner N64 layers to the literal fiber pullbacks of the accepted N16 inner coefficients, with gamma_0=gamma_1=1.
2. Allow all 512 physical outer endpoint coefficients to vary independently, including genuine high-x dependence.
3. For each of the 64 output rows, form its eight fixed transported templates and the target row. Propose one nine-column augmented minor using numerical pivot selection only for discovery. Verify nonvanishing with exact algebraic arithmetic or rigorous interval bounds over the accepted small root's isolating region.
4. Stop on the first certified nonzero augmented minor: this rejects that entire outer-correction law and proves that at least one inner layer must change in this branch. Alternatively, if every target row is exactly consistent, solve all outer rows and verify every full-product entry and nonzero guard.

The bounded negative test needs at most one proposed minor per row (64 attempts); failure to certify a minor is inconclusive, not evidence of existence. The accepted small coefficient root may be refined within its existing exact chart if interval widths obstruct certification. No new broad coefficient fit is required.

This experiment is narrower than either full system above. A rejection must not be reported as failure of all 1536-variable N64 coefficients or the mean-anchored 1152-variable family. It tests whether the actual accepted seed can be corrected solely at the outer layer, and therefore identifies which part of a genuine lift law needs additional fiber dependence.
