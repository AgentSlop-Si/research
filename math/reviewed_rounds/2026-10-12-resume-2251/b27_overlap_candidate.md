# Candidate: full b=27 Rogers–Szegő overlap family

12 October 2026. Status: fresh exact candidate, awaiting independent review. No live table or repository write is implied by this file.

## Statement

Let q have primitive odd order d>27 in a characteristic-zero field. Set H_27(z;q)=sum_j [27 choose j]_q z^j=(z+1)U(z;q), g=H'_27(-1;q),

W=product_(r=1)^27(1-q^r)/product_(r=1)^((d+27)/2)(1-q^(2r)), tau=dW/g.

With monic probabilists' Hermite polynomials, define J_(A+1)(x;tau)=x He_A(x)-A tau He_(A-1)(x). The candidate conclusion is Disc_x J_(A+1) != 0 for every integer A>=1.

This statement concerns the overlap polynomial of degree A+1. It does not assert ordinary residual squarefreeness Disc_z U !=0 for b=27, and it does not close all F020 guards.

## Accepted dependencies and exact arithmetic boundary

The sources used are the remote's pinned reviewed text at commit 95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d:

- math/reviewed_rounds/2026-10-12-reviewed-research/rs-general-odd.md: original normalization, derivative nonvanishing, separation, nonreality, and lower strip b<d<=2b+1.
- math/reviewed_rounds/2026-10-12-b25-overlap/rs-b25-full-overlap.md: all-A critical annulus argument and composition with the improved general tail d>=15(b+1)/2. This report identifies exact historical lower/tail source hashes c4009870cdb96f0af09065b4e41e98346d8159cc3962d7954a92b73963b2e78c and 4f3ef60634b8bc1962e22d28ad3d5254b9d9ce49d21c749040db131a92835a79. This candidate inspected the restored derivative text; it has not independently recovered or replayed the nested historical archive chain.
- math/reviewed_rounds/2026-10-12-b21-overlap/rs-b21-full-overlap.md §§4–5: optional all-A good-prime route.

For b=27, lower odd d=29..55 and tail odd d>=211 leave precisely 77 odd middle orders 57..209. No previously accepted b<=25 calculation was rerun.

## General repeated-root argument being applied

The inherited nonreality proof applies to every odd b<d. Repeated zero roots require real tau (tau=0 at odd A, tau=-1/A at even A), and so are excluded. Consecutive Hermite polynomials have no common zero. At a nonzero repeated root, differentiation and elimination give

x^2=tau(1+A tau)/(tau-1)=A tau+(A+1)+(A+1)/(tau-1).

For A>=3, the parity Jacobi representation and complex-symmetric Jordan-chain argument in the accepted source give, with rho=|tau-1|^2,

1+1/A < rho <= 2+2/A <= 8/3.

For A=1,2 the discriminants are 4tau and 4(1+2tau)^3. Thus a single primitive embedding with rho>8/3 suffices for all A. A primitive embedding with rho>9/4 suffices for A>=8 because 2+2/A<=9/4 there; only A=3..7 then need additional exact checks.

For each fixed A the discriminant is a polynomial with rational coefficients in tau. Nonvanishing at one primitive conjugate therefore implies nonvanishing at every primitive conjugate. It survives the injective cyclotomic-field map into any characteristic-zero ambient field. No metric inequality is transported across embeddings.

## New middle certificates

b27_interval_certificates.json supplies one selected primitive exponent k for every odd d=57..209. The code b27_interval_certify.py uses exact integer/dyadic arithmetic only; the exploratory file supplies integer indices, never proof bounds.

The fixed scale is 2^192. Arithmetic rounds all lower endpoints down and all upper endpoints up. Pi is enclosed using pi=4(atan(1/2)+atan(1/3)), 120 alternating terms per arctangent and the next omitted term. The angle is reduced using the exact residue kj modulo d and divided by d; |theta|<4 is explicitly checked. Sine/cosine Taylor degrees 201/200 carry remainders bounded by 4^203/203! and 4^202/202! respectively. Interval errors from all prior arithmetic are retained.

For every order the parameter is evaluated using the original uncancelled W and the direct derivative sum of Gaussian coefficients reconstructed from their product quotients. Every inverted original factor, W denominator, and derivative has a strictly positive interval squared-norm lower bound. The canceled prefix route d/(E S_13), E=product_(r=1)^((d-1)/2)(1-q^(2r)), is separately evaluated with guarded divisions and overlaps the original tau enclosure.

All 76 orders d=59,61,...,209 have strict rho>8/3 certificates. For d=57 the chosen exponent k=13 is primitive, and the coarsened rigorous enclosure is

2275864/1000000 <= rho <= 2275865/1000000.

Its lower endpoint is strictly larger than 9/4 by 25864/1000000. The imaginary part of tau is enclosed away from zero. This proves the required A>=8 exclusion at d57.

The initial floating exploratory scan found that no d57 conjugate met the cruder rho<=1 or rho>8/3 criterion. That observation motivated the sharper cutoff and is not used as a proof premise, nor is it a simplicity counterexample.

## Finite A=3..7 certificate at d57

b27_d57_finite_A_certificate.json gives an independent-of-interval algebraic route for the remaining sizes. Work in the exact ring R=F_11[X]/(Phi_57 mod11), without assuming R is a field. Its modulus has degree 36. The original Gaussian product quotients, original W and derivative construct t=57W/g in R. Every required denominator is a unit, checked by gcd and explicit inverse multiplication. A separate Pascal construction of all Gaussian coefficients gives the identical derivative.

For each A=3..7 construct D_A(T)=Disc_x(x He_A-A T He_(A-1)) over Z[T] and evaluate it exactly at t in R. Every gcd(D_A(t),Phi_57 mod11) is 1, and inverse multiplication is checked. Thus each reduced discriminant is a unit and in particular nonzero. Since the original denominator specializes to a unit, any characteristic-zero zero identity would specialize to zero. The nonzero specialization excludes it. The additional recorded classes A=1,2,8,9,10 are controls and are not needed for this finite-A bridge.

This proves the proposed d57 gap once the input certificates are independently verified. Joining it with the 76 annulus witnesses and inherited lower/tail theorems yields the candidate full b27 overlap conclusion.

## Alternative check and retained boundaries

b27_d57_prime_probe.json also records a p=5 certificate. The original parameter is integral with t^5-t a unit, and every R_r=x He_r-r t He_(r-1), r=1..4, has unit discriminant. The generic local lemma in the b21 source would therefore prove all A directly. This is a redundant candidate route, not needed by the interval/finite-A proof and not yet independently reviewed.

Ordinary residual squarefreeness remains separate: current accepted ranges are odd b<=25 at every odd d>b, and odd b>=3 at odd d>=4b^2. For b27 the general remaining ordinary-residual strip is odd d=29..2915, absent separately accepted instances. The candidate does not remove it. It makes no general-b overlap theorem, positive-characteristic theorem, finite-precision Fourier-speed claim, novel-identity count, or historical-priority finding.

A complete preservation packet should retain these exact new source/certificate files, the inspected dependency texts and their source hashes, independent reconstruction results, negative controls, and a cold replay receipt. The present source audit is text-level dependency inspection, not a claim to have rerun the nested historical source archive chain.
