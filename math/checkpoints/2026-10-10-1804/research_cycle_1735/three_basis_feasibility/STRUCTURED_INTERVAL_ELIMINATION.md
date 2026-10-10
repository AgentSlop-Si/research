# Structured interval elimination beyond coherence

10 October 2026. New feasibility/proof note for independent review. No accepted file is changed. This note supplies a candidate replacement for the two guard exclusions in the accepted square-root argument. It uses ordinary consecutive-row Vandermonde independence, not arbitrary-support three-basis full spark. It applies to odd composite and prime orders alike.

## 1. Elementary interval lemma

Let N be odd, q a primitive Nth root in characteristic zero, e=(N+1)/2 and h=4^(-1) mod N. Write C_k=q^(h k^2). Let

B(k)=C_k E(q^k)+C_k q^(ek) O(q^k)+R(q^k),

where u,v are nonnegative integers, deg E≤u, deg O≤v, and deg R≤b−1, with b≥1. Assume

u+b<e and e+v+b<N.                                                   (A)

If B vanishes on L consecutive integer positions and

L≥(u+1)+(v+1)+4b,                                                    (B)

then E=O=R=0.

Proof. Write S for the step-two forward shift. The operator

M=∏_{j=0}^{b−1}(S−q^(2j))

kills R(q^k). Since C_(k+2)=q^(k+1) C_k and q^(2e)=q, a factor S−λ changes the two chirp polynomials by

E(z)↦q z E(q^2 z)−λ E(z),
O(z)↦q^2 z O(q^2 z)−λ O(z).

Each map takes every nonzero polynomial to a nonzero polynomial of degree one larger: the highest-degree coefficient comes only from its first term. After b factors,

M B(k)=C_k[Ē(q^k)+q^(ek) Ō(q^k)],

with deg Ē≤u+b and deg Ō≤v+b. This sequence vanishes on L−2b consecutive positions. By (A), after division by the nonzero C_k, it is a linear combination of at most

s=(u+b+1)+(v+b+1)

distinct ordinary characters q^(jk), with frequencies in [0,u+b] and [e,e+v+b]. A sum of s distinct characters vanishing on s consecutive positions is zero: its coefficient matrix is a square Vandermonde, multiplied by nonzero column factors for the initial position. Condition (B) gives L−2b≥s. Consequently Ē=Ō=0. Highest-degree preservation gives E=O=0. Finally R has L≥b distinct roots q^k (take the first b positions, with b≤N implicit in (A)), so R=0. ∎

This is a genuinely structured three-basis independence result for coordinate supports whose complement contains a sufficiently long consecutive interval. It is not full spark for arbitrary selections, nor a consequence of pairwise unbiasedness. Normalization of Fourier/chirp atoms is immaterial.

## 2. Exact derivative guard at a linear range

Use precisely the notation of the three accepted source files. Let d≥4, m=N−d and assume

N≥16d−19.                                                          (C)

The envelope degrees are

u=Emax=d−3+floor((d−1)/2),
v=Omax=d−3+floor((d−2)/2),
b=d−1.

Their initial total chirp count is (u+1)+(v+1)=3d−6.

For x≠0, suppose the derivative functional belongs to the row space. The accepted scaled envelope B agrees with k x^(k−1)D(q^k) on k=0,…,m. Apply the existing operator

L_x=∏_{j=0}^{d−2}(S−x^2 q^(2j))^2,

of degree r=2(d−1) in S. The resulting envelope has chirp degree bounds u+r and v+r and ordinary degree at most d−2. It vanishes on

L=m−2r+1=N−5d+5

consecutive positions. Apply the elementary interval lemma to this envelope. Its inequality (B) is exactly

N−5d+5 ≥ (3d−6+2r)+4(d−1)=11d−14,

or N≥16d−19.

The final chirp degree bounds are u+3(d−1) and v+3(d−1). They satisfy

u+3(d−1)≤(9d−13)/2,
v+3(d−1)≤(9d−14)/2.

Under (C), the first is less than e=(N+1)/2 and the second is less than (N−1)/2, for d≥4. Thus the two frequency intervals are disjoint and do not wrap, as required by (A).

The lemma gives that the chirp components after L_x vanish. Highest-degree preservation through L_x then forces the original E=O=0. The accepted ordinary-recurrence contradiction now applies unchanged: R(q^k) agrees with k x^(k−1)D(q^k) at m+1≥3(d−1) consecutive positions, propagates to all nonnegative k, and k=0,N gives 0=N x^(N−1)D(1), impossible.

Equivalently, combine M and L_x from the outset. The total step-two degree is 3(d−1). The pure-chirp result has at most 9d−12 distinct frequencies and vanishes on N−7d+7 consecutive positions. Condition (C) is precisely N−7d+7≥9d−12.

## 3. Exact coordinate guard at the same range

Suppose δ_j belongs to row(A), for some 0≤j≤m. Its scaled envelope B equals D(q^j)δ_j on 0,…,m. The longer of the zero intervals [0,j−1] and [j+1,m] has length

L≥ceil(m/2).

Apply the lemma with the initial degrees u,v and b=d−1. Its sufficient length is

(3d−6)+4(d−1)=7d−10.

Under (C), m=N−d≥15d−19 and hence ceil(m/2)≥7d−10. Expanded chirp intervals are disjoint already under a much weaker bound, and in particular under (C). Thus E=O=R=0, contradicting B(j)=D(q^j)≠0.

This excludes every coordinate functional, including δ_0, δ_m and derivative evaluation at x=0 (=δ_1). No one-missing-row full-spark theorem is needed; use one of the two actual contiguous zero intervals.

## 4. All remaining accepted guards

Under d≥4 and (C):

- N≥7d, so the original envelope ranges and all original definitions are valid.
- m≥(N−1)/2.
- m≥4(d−1), so the original derivative operator has a nonempty zero interval.
- m+1≥3(d−1), so the ordinary recurrence argument propagates.
- dim W≥N−5d+12≥(N+1)/2, because N≥10d−23 follows from (C).

Thus, conditional only on independent verification of this interval-elimination argument, the accepted squarefree-pencil and prescribed-root incidence proofs transfer unchanged. They secure monicity, nonzero constant, squarefreeness, and axis rank simultaneously. The accepted physical-row construction then supplies 2m+2 legal banks over a splitting field; this is not an FFT runtime result.

One deliberately simple candidate parameter is d=floor(N/16) for odd N≥65. It satisfies all the displayed hypotheses and would give the candidate bound 2N−2floor(N/16)+2. A sharper rounding choice d=floor((N+19)/16), odd N≥45, also meets (C), but optimizing rounding is not the objective here. No accepted theorem is changed by this note.

## 5. Bounded next question

Independently prove or refute Sections 1–4, with special attention to the shift action, consecutive-window shrinkage, and frequency nonoverlap. If correct, record a separate reviewed linear-saving bank theorem using the accepted guard machinery. If a flaw appears, identify the exact lemma hypothesis that fails before returning to the much harder arbitrary-support MUB spark problem.
