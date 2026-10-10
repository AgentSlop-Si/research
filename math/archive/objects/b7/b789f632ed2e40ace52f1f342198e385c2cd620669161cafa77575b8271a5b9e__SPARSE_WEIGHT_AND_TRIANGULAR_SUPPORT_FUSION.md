# Phase18 extension: sparse branch weights and triangular Weyl support

10 October 2026. Separate derived supplement; it does not modify the frozen Q30/Q32 work or the source Phase18 theorem. Exact field model, primitive Nth root supplied, N=KM, q=omega^M, and Delta=(1-beta^K)^M-alpha^N!=0 throughout. Definitions agree with `PHASE18_PROOF_AND_MODEL_AUDIT.md`.

## E1. Complementary sector evaluation

For 0<=ell<K put L=K-ell. The verified source formula is

R_ell=D^(-1) beta^ell P_ell(S)U^ell,
P_ell(S)=sum_(r=0)^(L-1) alpha^r [r+ell choose ell]_q S^r.

Besides the source's O((ell+1)N+ell^2+K) geometric-window algorithm, there is a direct O(LN+N) algorithm. The coefficients g_r=[r+ell choose ell]_q obey

g_0=1,
g_(r+1)=g_r (1-q^(r+ell+1))/(1-q^(r+1)), 0<=r<L-1.           (E1)

Every denominator and numerator in (E1) is nonzero: their exponents are between 1 and K-1. Generate the powers of q successively, and generate alpha^r g_r using the same ratio times alpha. Alpha=0 is harmless. This costs O(L+log N) exact field work. Apply the L cyclic shifts directly to U^ell x, accumulating each coordinate and charging O(LN) work. The phase, beta^ell, and D solver cost O(N+log N), including all N outputs.

Choose the cheaper of the direct and geometric-window algorithms. Since ell^2<=N(ell+1) and K<=N, their full cost is

O(N s(ell)), s(ell)=min(ell+1,K-ell),                         (E2)

with O(N+K) retained storage. This is a bound on exact field/address operations, not floating-point or bit complexity. The endpoint ell=K-1 is particularly simple:

R_(K-1)=D^(-1) beta^(K-1) U^(K-1),

and is linear-time even though the source's one-sided bound is quadratic there. At ell=0 the verified unweighted linear algorithm is recovered. The improvement uses two elementary realizations of the same polynomial, not a new q-binomial identity.

## E2. Known sparse character weights share the inverse

For raw branch weights w_j, define R_w=(1/K)sum_(j=0)^(K-1)w_j Q_j^(-1). Suppose an exact character expansion is supplied and verified:

w_j=sum_(ell in Lset) gamma_ell q^(-j ell),

where the modes are distinct and the nonzero amplitudes are supplied field elements. Then

R_w x=D^(-1)sum_(ell in Lset)gamma_ell beta^ell P_ell(S)U^ell x. (E3)

Generate and sum the numerators using E1/E2, then apply D^(-1) **once**. If r=|Lset| and C_L=sum_(ell in Lset)s(ell), the complete application costs

O(N(1+C_L)),                                               (E4)

with O(N+K) storage. The zero-weight case writes N zeros. Coefficient preparation and powers are charged in this bound; repeated inputs may reuse them, but no reuse is needed for the stated upper bound. Merely having r modes gives the weaker worst-case O(N r K) bound, not automatic O(Nr). O(Nr) follows when each accepted mode stays within O(1) of the cheap sector endpoints. No generic dense-weight linear claim is made.

### Raw-input recognition interface, with the sign made explicit

If K is dyadic and 1<=t<=K/2, invoke only the recognition portion of accepted S2 in `research_cycle_0958/structured/STRUCTURED_THEOREMS.md`. On a raw length-K vector w, it returns an exact expansion

w_j=sum gamma_u q^(u j), r<=t,

or rejects, in O(K log(t+2)+t^2) exact work, with all K entries verified. The matching sector is ell=(-u) modK, because the Phase18 weighted definition uses q^(-j ell). Confusing the positive recognized mode with ell gives the wrong operator.

The complete method for J fresh inputs has the charged upper bound

O(N+K log(t+2)+t^2+J N(1+C_L)).                              (E5)

All hypotheses match: q is supplied as omega^M, K divides N, and field characteristic does not divide K. Only the recognition theorem transfers; S2's separate Fourier-sandwich application identity is not substituted for the magnetic-resolvent operator. K=1 can be handled directly. For non-dyadic K, one may use the separately accepted O(Kt+t^3) exact recognizer or state the expansion as supplied; no unsupported arbitrary-length pruning bound is assumed. Rejection does not prove the weights have some different sparse representation or authorize the same fast bound on a fallback.

This is a concrete Prony/pruning plus magnetic-twirl interface. Its ingredients and sparse-weight mechanism are classical; worldwide priority is unclaimed.

## E3. Triangular support closes the K=N Fourier loophole

Let T e_i=omega^i e_i, so U=T^M, and let W_(a,b)=S^a T^b, with a,b represented by 0,...,N-1. Since S^N=I,

D^(-1)=Delta^(-1)sum_(t=0)^(M-1)d^(M-1-t)c^t S^(Kt),
d=1-beta^K, c=alpha^K.                                     (E6)

Multiplying D by the right side telescopes to I. It is a polynomial identity valid also when d=0 or c=0; a zeroth power is 1. Combining (E6) with the sector formula shows

supp_Weyl(R_ell) is contained in
{(a,b): a=r+Kt, b=M ell, 0<=r<=K-1-ell, 0<=t<M}.             (E7)

The indices do not wrap because r+Kt<N. The supports for distinct ell have distinct b coordinates. Consequently **every** branch-weight choice w has support contained in

A_(N,K)={(a,M ell):0<=ell<K, (a modK)+ell<=K-1},
|A_(N,K)|=sum_ell M(K-ell)=N(K+1)/2.                         (E8)

This bound is independent of alpha, beta and the branch weights. Therefore a finite sum of different legal parameter pairs with the same N,K,S,U still has support inside the same set. The theorem does not permit changing the Weyl coordinate system or multiplying stages.

For every odd N, not just primes, every Weyl coefficient of the negative Fourier matrix is nonzero. The trace formula and modular completion of the square give

c_(a,b)=(G_-/N)omega^[(a+b)^2/4], G_-=sum_j omega^(-j^2).

Here 4 is inverted modulo the odd integer N. To prove G_-!=0 over any admissible coefficient field, put G_+=sum_l omega^(l^2). Then

G_-G_+=sum_(j,l)omega^[l^2-j^2]
      =sum_(u,v)omega^(uv)=N,

because u=l-j, v=l+j is a bijection modulo odd N; for u!=0 the inner geometric sum is zero, while u=0 contributes N. The characteristic hypothesis makes N nonzero. This argument requires neither a prime N nor an absolute-value/numerical estimate. The matrices W_(a,b) form a basis: their trace pairings are zero except at equal index pairs, where they equal N, so the support comparison is legitimate in every such field.

For odd N>=3 and every K|N, |A_(N,K)|<=N(N+1)/2<N^2. Thus

R_w != F_N for every choice of weights w.                   (E9)

The same exclusion holds for any finite sum of these operators with the same fixed N,K,S,U and legal parameter pairs. At K=N, D is scalar and (E8) is precisely the triangle a+b<=N-1. This supplies a nontrivial rejection certificate where the subgroup commutator [F,S^K] is identically zero and cannot decide the question. Even characteristic 2 is allowed when N is odd; the exponents use modular inverses in Z/NZ, and the field condition is only characteristic not dividing N.

No even-N conclusion is asserted by this full-support proof. No conclusion about arbitrary Weyl-coordinate changes, arbitrary diagonal endpoint gauges, sums across different K, or noncommuting products is asserted. Those change the allowed support grammar.

## E4. Relationship to the branch-count lower bounds

Every Q_j has at most two nonzero entries per column. The accepted F018 separator theorem constrains how many independent such inverse branches can represent a Fourier target in its stated endpoint grammar. It is a representation lower bound. The unweighted Phase18 construction has K literal noncommuting branches, yet its entire non-Fourier average has O(N) work. Equations (E3)–(E5) show further cost sharing from character structure in the raw branch weights.

This gives a concrete reason not to multiply a branch lower bound by N without a separate no-sharing theorem. It does not violate F018: the constructed operator fails to be Fourier, and E9 proves that failure for every weight choice in this fixed odd-length orbit. The useful positive result and the useful exclusion are different statements.

## Evidence and dependency scope

The source-weighted theorem is independently reconstructed in the main Phase18 audit. `fresh_sector_extension_controls.py` independently checks E1, the direct route against sums of original matrix inverses, the q-sign correspondence for raw weight modes, exact Weyl support, and Fourier nonzero support at odd composite lengths. No supplied program is executed. Finite controls supplement the proofs, not replace their all-size quantifiers.

S2 is used in its already-reviewed exact dyadic recognition model, with its source hash recorded in the manifest. Repeating its proof or claiming a new recognizer is unnecessary. E2 is an explicit composition; E1 and E3 are newly derived project corollaries. None is a historical-priority certification or a generic FFT speedup.
