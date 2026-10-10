# Independent signed magnetic fusion review

10 October 2026. Accepted proof: `signed_magnetic_fusion/SIGNED_MAGNETIC_FUSION.md`, exact version/hash recorded in the receipt and frozen source copy. No supplied program was executed, imported, compiled, or AST-parsed. Only the reviewer programs here were run; their matrix helper is copied from this reviewer's independently authored supplement-v2 program. All prior freezes are unchanged.

## Accepted model and support theorem

N is odd and at least3; the exact coefficient field contains a supplied primitive Nth root q and has characteristic not dividing N. A counted bank is an arbitrary phase-weighted average of N resolvents I−alpha S^epsilon−beta zeta^j T^delta, with zeta=q^(epsilon delta) and Delta=1−alpha^N−beta^N nonzero. There are four permitted sign orientations. Parameters and weights may differ between finitely many banks. No arbitrary diagonal gauges, rotated Weyl coordinate systems, products or uncharged transformations are introduced.

The signed Gaussian-binomial expansion is correct. Its Weyl coefficient support is [epsilon a]_N+[delta b]_N≤N−1. The four interior inequalities and all axis cases were checked. Any triple of orientations misses exactly (N−1)/2 exclusive indices; all four cover every index when N is odd. A primitive odd-length Fourier matrix has nonzero coefficients everywhere, using the exact Gauss identity G_-G_+=N. Thus all four orientations are necessary, and four-orientation support coverage alone is insufficient.

## Accepted growing-bank and N9 obstructions

On b=1, a=1,...,N−1, banks with delta=−1 vanish. Each delta=+1 bank supplies at most two exponentials: bases alpha,q alpha for epsilon=+1, and alpha^−1,q alpha^−1 for epsilon=−1. Zero alpha gives zero contribution and requires no inversion. The vanishing endpoints are exactly those excluded by the triangles. Reflection yields the analogous b=−1 statement with ratio q^−1.

The Fourier row Hankel matrix of size m=(N−1)/2 factors as nonzero diagonal matrices around a Vandermonde matrix with distinct nodes q^(i/2). This is valid in every allowed field; the half exponent is computed modulo N, rather than by dividing by2 in the coefficient field. Consequently

r_+≥ceil((N−1)/4), r_-≥ceil((N−1)/4), and total≥max(4,2ceil((N−1)/4)).

One bank per orientation is therefore impossible at every odd N≥11. This is a bank-count statement, not an operation lower bound. Each bank can contain many literal inverse branches that share work.

The N9 boundary certificate is accepted over every allowed characteristic, including2. Four paired exponential bases force the displayed order-four recurrence. The reviewer independently reconstructs its coefficients from the four chirp roots, verifies p1=q p3, verifies p3(q²+1)=1 modulo Phi9, and expands the displayed E-times-V identity to the constant3 modulo Phi9. Since char does not divide9, this is a contradiction. Multiplication by denominators has not introduced an unguarded branch.

The stronger conclusion is accepted: at N9, r_+≥3 and r_-≥3, hence total≥6. If r_+=2, support necessity puts one bank in each positive-modulation orientation; the same row contradiction applies regardless of the number of opposite-sign banks, which vanish on that interval. Simultaneous index reflection proves the other side. Six-bank sufficiency is not established.

## Accepted exact N3 construction

The uniform construction is valid over every admissible field. Use beta=1 and alpha values(1,q,q,1) in orientations(++,+−,−+,−−), respectively. All Delta=−1. The ell0 sectors span the three characters1,q^a,q^−a on b=0; their exact three-point character coefficients match that row. The ell1 coefficient for each orientation is fixed by its exclusive point, dividing only by nonzero alpha(1+q^(epsilon delta)). Two ell2 sectors independently correct the remaining a=0 coefficients without altering previous matches. Since beta is nonzero, all these amplitudes correspond to actual legal raw branch weights.

This proves minimum bank count exactly four for N3, including over C. It is a fixed small-size construction, not an asymptotic FFT. In addition to checking the coefficient proof, the reviewer independently evaluates the twelve underlying resolvents with the constructed weights and matches the complete Fourier matrix in F4,F7,F13,F19,F31. The F4 control directly tests the characteristic-two case.

## N7 symbolic control and still-open small scope

The necessary central-row equations and their signs/endpoint normalization are accepted for all odd N. The reviewer independently builds the N7 equations in Q(zeta7)[x,y], clears only the two nonzero denominators, and obtains the exact reduced Groebner basis[1]. This independently reproduces the owner's computational characteristic-zero obstruction. Both calculations use SymPy as the algebra engine, so this is computational evidence, not two independent algebra-engine implementations or a hand-sized all-characteristic Bezout identity.

In characteristic zero the same row isolation strengthens that computational result to r_+≥3,r_-≥3 at N7. The all-characteristic theorem is not enlarged by this calculation. N5's full complex coefficient realization with exactly one bank per orientation remains open. The owner's F11 and F29 searches remain explicitly finite-field controls; this reviewer does not extrapolate them or claim to have repeated their entire search.

## Accepted universal 4N-bank upper construction

For each orientation, assign target Weyl coefficients to its triangle and divide by the nonzero local Gaussian factor. Extend each fixed-sector sequence by zeros to length N. Use N parameters alpha_j=q^j,beta_j=1, all with Delta_j=−1; invert the ordinary root-grid Vandermonde by h_(j,ell)=N⁻¹sum_r t_(r,ell)q^(−jr). Orthogonality matches every assigned coefficient. Each h is realized by legal raw weights using gamma=−h. Four triangles cover every index, so at most4N banks represent any matrix over every admissible field.

Combined with the lower theorem, Fourier bank count is Theta(N) in this grammar. Growing-bank existence is settled; exact minima and efficient shared evaluation remain open. This distinction corrects an earlier overly broad open-question formulation.

The source's conservative O(N³) preparation and application, with O(N²) stored weight data, is valid and is not a speed improvement. In the chosen beta1 branches, exactly one diagonal vanishes, at i0=−epsilon k. The first equation fixes y_(i0−epsilon)=−x_(i0)/alpha. Backward traversal solves all remaining coordinates by dividing only by nonzero alpha, never by a vanished diagonal. Each of4N² literal branch applications costs O(N), including phases, weights and output accumulation. Direct coefficient extraction and the two parameter transforms cost O(N³); primitive-root discovery, bit complexity and numerical stability remain outside this exact model.

The reviewer independently constructs arbitrary and Fourier targets at N3,5,7,9, evaluates every original branch inverse, and matches all entries. Each original inverse is also checked against the proposed backward solver. These eight complete constructions agree.

## Independent evidence and limits

Reviewer evidence:

- All15 odd support sets N3 through31, every omitted-orientation hole set and all-four coverage
- 48 signed weighted-average matrix equalities at N3,5,7,9,11,15, rebuilt by direct inversion of original branches
- Full-rank Fourier row-Hankel controls on both signs at those lengths
- All N9 forced recurrence and Bezout identities expanded exactly
- Independent exact N7 characteristic-zero unit-ideal computation
- Five complete original-branch N3 constructions, including F4
- Eight complete universal-upper constructions and all their backward branch solves

The all-size algebraic proofs establish the accepted theorems; finite controls are falsification checks. The Gaussian-binomial and Hankel/Vandermonde mechanisms are classical and closely related to the already reviewed F014 arguments. The counted object differs: a phase-weighted magnetic bank is not F014's fixed-pair two-resolvent product or one F018 literal inverse branch. Those counts cannot be substituted or multiplied by a per-branch cost without a separate sharing argument.

Still open: N5 four-bank coefficient realization, N7 all-characteristic exclusion, exact attainment of the sharper bank-count lower bounds, compact parameter descriptions and an improved shared evaluator, bit/precision/stability behavior and worldwide priority. The coarse interpolation parameters and cubic-work evaluator are already explicit. No general arithmetic lower bound or faster unrestricted FFT follows. Current primary comparisons remain provisional.
