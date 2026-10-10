# Step-one elimination in the Fourier bank envelope

10 October 2026, 18:01 UTC. Root derivation for independent review. The older accepted coherence proof remains unchanged.

Use the whole-left envelope over Q(q), for odd N, d=N-m>=4. Set h=4^(-1), e=2^(-1) modulo N, rho=q^e and C_k=q^(h k^2). Its sequences have the form

    B(k)=C_k E(q^k)+C_k rho^k O(q^k)+R(q^k),

with deg E<=d-3+floor((d-1)/2), deg O<=d-3+floor((d-2)/2), and deg R<=d-2. Define

    P(t)=E(t^2)+t O(t^2).

Then deg P<=3d-7 for either parity of d, and B(k)=C_k P(rho^k)+R(q^k), since rho^2=q. The shift identity is

    C_(k+1)=q^h rho^k C_k.

Consequently a step-one factor (shift-lambda) transforms the chirp polynomial by

    P(t) -> q^h t P(rho t)-lambda P(t).

For nonzero P the degree rises exactly one and its leading coefficient remains nonzero. This injectivity holds for every scalar lambda, including zero. An ordinary term R(q^k) stays an ordinary polynomial of no larger degree.

## Derivative functional

If the derivative functional at nonzero x were in the recurrence row space, its scaled envelope would agree with k x^(k-1) D(q^k) on k=0,...,m. The degree-2(d-1) operator

    L_x = product_(j=0)^(d-2) (shift-x q^j)^2

annihilates that sequence. Follow it by the degree-(d-1) ordinary killer

    L_0 = product_(j=0)^(d-2) (shift-q^j).

The total degree is r=3(d-1). Their composition kills the ordinary component, raises the degree of any nonzero chirp polynomial by exactly r, and vanishes at k=0,...,m-r. Thus a chirp polynomial of degree at most6d-10 vanishes at N-4d+4 consecutive, distinct rho-powers. If N>=10d-13, there are at least6d-9 such points, strictly more than its degree. It must vanish identically. Injectivity forces the original P=0.

The original ordinary R(q^k) would then agree with k x^(k-1)D(q^k) on m+1 points. Their difference has a monic constant-coefficient recurrence of order at most3(d-1); with enough consecutive initial zeros it vanishes for all nonnegative k. Comparing k=0 and k=N gives 0=N x^(N-1)D(1), impossible in characteristic zero. This is the same final contradiction as the accepted uniform proof.

## Three necessary coordinate guards

It suffices to exclude the coordinate functionals delta_0, delta_m, delta_1. These ensure existence of a nonzero constant, existence of degree m, and exclusion of the derivative functional at x=0, respectively. An all-coordinate claim is not needed here.

Apply only L_0, of degree d-1, to a scaled envelope agreeing with one of these deltas on0,...,m. Its chirp polynomial has degree at most4d-8. For delta_0 and delta_m, there remains a consecutive zero interval of length N-2d+1; for delta_1 use k=2,...,m-(d-1), of length N-2d. Under N>=10d-13 and d>=4, each length is at least4d-7. Ordinary polynomial interpolation in rho^k therefore forces the transformed chirp polynomial, and then the original one, to vanish. The remaining ordinary R agrees with a nonzero single-coordinate sequence on m+1 samples; its degree at mostd-2 and many zero samples force R=0, a contradiction.

## Proposed bank consequence

Take d=floor((N+13)/10), for odd N>=27. Then d>=4 and N>=10d-13. The existing rank bound gives dim W>=N-5d+12, so dim W-1>=(N-1)/2 follows from the weaker N>=10d-23. The previously accepted squarefree-pencil, incidence-axis, descent and exact physical-row reconstruction arguments should therefore give

    M_C(F_N) <= 2N-2 floor((N+13)/10)+2 = 9N/5+O(1).

This consequence remains subject to independent review of every transferred hypothesis and boundary. It concerns permitted signed resolvent banks, not scalar Fourier runtime, minimal bank count, or historical novelty. No original accepted proof is altered.
