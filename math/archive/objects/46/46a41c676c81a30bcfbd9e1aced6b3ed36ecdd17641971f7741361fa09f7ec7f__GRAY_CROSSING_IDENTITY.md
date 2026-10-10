# Exact crossing count of the binary Gray permutation

Let G_m(i)=i xor(i>>1) on N=2^m coordinates, and let kappa be the natural-path threshold crossing count in MIDDLE_PERMUTATION_COLLAPSE.md. Then

kappa(G_m)=m.

This is a combinatorial identity, not a Fourier realization theorem.

## Proof

Write H=2^(m-1). The binary-reflected Gray path consists of the (m-1)-bit Gray path in the lower half, the reversed copy of that path translated byH in the upper half, and one joining edge. The joining edge has endpointsH/2 and3H/2 for m>=2.

For1<=u<H, the threshold-crossing counts therefore satisfy

v_m(u) = v_(m-1)(u)+1_{u>H/2},
v_m(H+u) = v_(m-1)(u)+1_{u<=H/2},
v_m(H)=1.

Exactly one of the first two alternatives adds one to each old threshold count. Hence max_t v_m(t)=1+max_u v_(m-1)(u). The base path at m=1 has one crossing, proving kappa(G_m)=m.

One maximizing threshold is

t_m=(N+1)/3 when m is odd,
t_m=(2N+1)/3 when m is even.

These are integers and follow from the same recursion. The maximum number of contiguous runs in a preimage G_m^{-1}([0,t)) is floor(m/2)+1: these sets always contain0; whether they also containN-1 is determined by t>N/2. The crossing recurrence gives the upper bound, and the indicated maximizing thresholds attain it (or its boundary-adjusted counterpart).

## The inverse Gray permutation also has crossing countm

LetH_m=G_m^{-1}, and useT=2^(m-1). Its lower-half path isH_(m-1), and its upper-half path is the reflected copy T+(T-1-H_(m-1)(j)). The joining edge ends at2T-1. At every upper-half thresholdT+u,1<=u<T, this joining edge contributes one and the reflected path contributesv_(m-1)(T-u). Thus the maximum is at leastkappa(H_(m-1))+1. Lower-half thresholds can add at most the single joining edge, and the middle threshold has one crossing, giving the matching upper bound. Base m=1 yields kappa(G_m^{-1})=m. One maximizing threshold is(2N+(-1)^m)/3.

## Consequence for the next layout

For an order-r quasiseparable matrixS, the general conjugation lemma gives order at mostm*r for G_m S G_m^{-1}. Therefore the four-stage R-G_m-R word does not collapse into a three-stage family of bounded quasiseparable order through this lemma. Its and its inverse's growing crossing counts meet both necessary Omega(log N) orientation requirements.

This is only removal of one obstruction. It neither proves all terminal ranks are sufficient nor supplies compatible Fourier coefficients. The changed four-stage word remains an explicit open candidate, with the degree-six cut-minor system and full coefficient-preparation charges stated separately.
