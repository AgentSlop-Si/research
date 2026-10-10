# A constructive confluent shear-Green bridge

This is an independently derived mathematical extension and dense verification prototype. It has not been integrated into the uploaded executor. It combines the useful repeated-pole/Newton and distinct-pole/Green ideas without relaxing fresh-raw-input accounting.

## Family and pilot

Fix positive multiplicities d_1,...,d_g with fixed total D=sum d_j. Let a_j be distinct shifts, mu_j nonzero scalars, and lambda_j(h)=mu_j eta^(-a_j h) distinct for every h. Assume Q>=2D, p>N and balanced N=QM. The first 2D raw rows are an unknown nondegenerate polynomial-orbit sum:

    y_t[u] = sum_(j=1)^g sum_(r=0)^(d_j-1)
                 binom(t,r) mu_j^t b_(j,r)[u-a_j t].

The dense baseline rows b_(j,r), the shifts/scalars and even their multiplicities need not be supplied. Assume each channel's D-by-D pilot Hankel is nonsingular. A sufficient hypothesis is nonzero highest-degree component spectrum for each j, distinct nonzero eigenvalues, and p>D. This is the standard confluent Vandermonde nondegeneracy in exact field arithmetic.

Later rows have sparse normalized spectral innovations under

    A(L,S) = product_j (1 - mu_j S_(a_j) L)^(d_j),

with total R=O(Q) modes after the clean 2D-row pilot. Other raw inputs may reject. This pilot is more restrictive than the general single-gauge Newton pilot: it forbids innovations before 2D. Accordingly, the bridge does not contain every previously accepted shear-Newton input.

## Fresh-raw recovery, including unknown multiplicities

1. Compute 2D charged direct row DFTs. At every h, solve the D-by-D Hankel system for the monic degree-D characteristic polynomial P_h.
2. Its trace is s[h]=sum_j d_j mu_j eta^(-a_jh). The direct M-DFT of s reveals the distinct shifts and rho_j=d_j mu_j, since d_j<p and mu_j is nonzero.
3. If the multiplicities are known, recover mu_j=rho_j/d_j. If only D is fixed, enumerate the finitely many positive compositions d_1+...+d_g=D, after ordering the discovered shifts. For each, set mu_j=rho_j/d_j and compare product_j(z-lambda_j(h))^(d_j) with every recovered P_h. There are binom(D-1,g-1) candidates, a D-dependent constant. Require distinct eigenvalues and continue to full raw validation. The true candidate exists under the promise; uniqueness need not be assumed. Choose any completely verified candidate if several fit.
4. Solve a confluent Vandermonde system at each h using basis binom(t,r) lambda_j(h)^t, t=0,...,D-1. Recover all D dense spectral baselines, then their D charged inverse direct transforms.
5. Verify every sample in the 2D-row pilot. Form all later raw residuals using the expanded A(L,S), discover sparse modes with the previously audited budgeted recognizer, and verify/reconstruct every raw sample.

The shifted recurrence has at most product_j(d_j+1)-1<=2^D-1 terms before combining duplicate lag/shift entries. Therefore fixed D preserves linear residual formation and raw reconstruction; a growing D does not inherit this bound for free.

## Exact output kernels

For the baseline coefficient B_(j,r)[h], let z=omega^(-k)lambda_j(h), k=h+sM. Its contribution is

    B_(j,r)[h] z^r B_(r+1,Q-r)(z),

where B_(a,L)(z)=sum_(v=0)^(L-1) binom(v+a-1,a-1) z^v is the already verified truncated binomial-geometric kernel. Handle z=1 by its binomial value, without dividing by zero.

The causal impulse generating function is

    product_j (1-lambda_j(h) z)^(-d_j)
      = sum_j sum_(r=1)^(d_j) A_(j,r)(h)/(1-lambda_j(h)z)^r.

The partial-fraction coefficients exist because the distinct pole factors are coprime. They can be recovered by a fixed D-by-D solve from the first D impulse coefficients; this is O_D(1) work per h. Thus

    H_v(h)=sum_j sum_(r=1)^(d_j)
            A_(j,r)(h) binom(v+r-1,r-1) lambda_j(h)^v.

An innovation c eta^(hu) at t contributes

    M c omega^(-kt) sum_(j,r)
       A_(j,r)(h) B_(r,Q-t)(omega^(-k)lambda_j(h)).

This yields each event's Q relevant outputs in O_D(Q), and every dense baseline in O_D(N). Root, scalar-power, inverse and fixed-degree kernel preparations remain explicitly charged.

## Bound, capacity and evidence

For fixed D, a bounded multiplicity enumeration, balanced dimensions and R_b=O(Q), the complete discovery/rejection and accepted-output work is

    O_D(N + M^2 + M(Q+R_b) + Q R_actual),

with O_D(M+R_b+1) scalar inversions and O_D(N+R_b) words. Exact field inversion word costs are absorbed under the same polynomial-field balanced assumptions. The hidden D-dependent constants include the composition search, confluent solves and up to 2^D recurrence terms. No growing-D theorem or numerical-stability claim is made.

For fixed parameters the description has D M dense baseline field values plus R sparse innovations, O(g) gauge parameters and support choices. It is still an exponentially negligible subset of all raw vectors, with the same p^(-N+O_D(sqrt N)) style capacity bound. This bridge expands the selected structured toolkit; it does not overcome the arbitrary-input barrier.

The independently authored checker tests multiplicities (2), (3), (2,1), (1,2), and (2,2) at N=64,90,144, three examples per pattern/size. It recovers the unknown multiplicities and parameters from the raw pilot, verifies the recurrence/partial fractions, and compares all outputs with the direct raw DFT: 45 full vectors and 4,470 exact bins. Its dense implementation is a reference proof check, not the promised fast executor.

## Bounded dense-channel displacement observation

Independently of any additional archive, the existing output kernel itself gives a precise warning about low displacement rank. Fix h, let z_s=omega^(-(h+sM)), and set

    K[s,j]=sum_(t=0)^(Q-1) (z_s lambda_j)^t.

Since z_s^Q=omega^(-hQ) is independent of s,

    K - diag(z_s) K diag(lambda_j)
      = 1 * [1-omega^(-hQ)lambda_j^Q]_j.

The right side has rank at most one. Nevertheless, when g=Q and the lambda_j are distinct, K=F_Q diag(omega^(-ht)) V_lambda is invertible: F_Q is the Q-point DFT matrix and V_lambda is a square Vandermonde. Thus K has full rank Q. Low displacement rank is a structured-matrix property, not ordinary low rank and not by itself a linear-work matrix-vector multiplication algorithm. An exact joint evaluator still needs an explicit operation ledger and charged fresh-raw coefficient recovery.

The phase index in the original shear formula is (1+Qa)h+sM. Making its h coefficient a multiple of M requires Qa=-1 mod M, possible exactly when gcd(Q,M)=1. In particular it is impossible at nontrivial square Q=M. This is only a check of that specific phase-routing condition; it is not an impossibility theorem for other evaluators.
