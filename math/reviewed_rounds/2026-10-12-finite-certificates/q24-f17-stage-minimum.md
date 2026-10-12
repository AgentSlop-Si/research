Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted. Mathematical assumptions, classical attribution, evidence depth and remaining work are retained. Original source-report SHA-256: 413b5844cd8dfa8b7e3c81fbeefc27faad2c91f05418c4bf4067d1d8a818d05f.

# Independent audit: exact Q24 finite stage optimum

Verdict: **ACCEPT, finite scope only.** The exact minimum is 11 for N=8 over F17 with ζ=3. The literal pure-shift-resolvent grammar includes every interspersed nonzero scalar Weyl-monomial gauge. The complete classification for ζ=3^u, u=1,3,5,7,9,11,13,15, is 11,10,10,11,11,10,10,11. No claim is made for extension fields, complex coefficients, other lengths, uniform matching constructions, historical priority, or arithmetic-time lower bounds.

## Source and independence

The reviewed candidate is Q24_F17_Exact_Stage_Minimum_CANDIDATE_2026-10-12.zip, SHA256 e94f5159b57fb8c2ee278de0fad1a95e2d8dcf030f7f544ddcbcd035800873fa (869027 bytes). Its manifest hash is 1b7e432d3f99bbc4c63a0d046a9bac1ca99c8baa91e2bb797e48a5fdfc7962e4. All 21 manifested payloads were verified from a cold extraction. The original Phase15 proof and accepted review were hash-matched to the bound research sources.

The reviewer's C++ enumeration and Python matrix checker were authored independently. No candidate or original-source program was executed, imported, or compiled. Candidate JSON and binary state files were read only as inert certificate data. A cold replay compiled the reviewer C++ from source in a fresh temporary directory, reconstructed every proof-critical state, and executed only reviewer programs. An omitted deepest-ball state and a legal witness mutation were both rejected.

## 1. Exact grammar and all gauges

Write S e_j=e_(j+1) and T e_j=ω^j e_j, where ω=ζ² has order8. The permitted chain is W0 R1 W1 ... RL WL, with Rj=(I−αj S^sj)^−1 and Wj=κj S^aj T^bj. All αj and κj lie in F17; κj is nonzero; every Rj is individually invertible. The index s may be any residue, including zero. Allowing zero α or scalar stages only enlarges the search with an identity class; it does not lower the optimum.

The conjugation identity W R(s,α) W^−1=R(s,αω^(bs)) moves all Weyl gauges to an endpoint. If h=8/gcd(8,s), then (αω^(bs))^h=α^h, so this move preserves the exact denominator guard. A general chain becomes κ S^a T^b R(S). Since C and R(S) are invertible circulants, commutation with S forces ω^b=1, hence b=0. Equivalently, the nonzero circulant entries cannot sustain net modulation. Thus the original all-row problem is exactly

C^−1=κ S^a ∏(I−αj S^sj).

This is an equivalence, not a restriction to a convenient normal form. Conversely any such identity gives a permitted chain. No arbitrary diagonal gauge, changed basis, selected readout, branch sum, or extension-field scalar is admitted.

## 2. Exact legality and finite quotient

For every s and α, the guard is 1−α^h≠0, with h=8/gcd(8,s). The cyclic geometric identity proves sufficiency; the split eigenvalues prove necessity. The reviewer independently checked this guard against modular Gaussian elimination on all 136 raw factors. There are 93 legal and43 singular cases; 70 legal cases have s≠0 and α≠0. The short-cycle case (s,α)=(2,2) is legal even though α^8=1; using the wrong N-period guard would incorrectly discard it.

Evaluation at 1,9,...,9^7 identifies F17[x]/(x^8−1) with F17^8 because the nodes are distinct. Its units are (F17*)^8. Since 3 has order16, take discrete logarithms ℓj and put dj=ℓj−ℓ0 modulo16. The reviewer deliberately uses a different chart from the candidate:

Ψ(v)=(d7 mod2, d1−7d7, d2−14d7, ..., d6−42d7),

where the final six coordinates are modulo16. This is an additive homomorphism. Its kernel is exactly scalar times shift: if Ψ=0, d7 is even and dj=7j d7, giving dj=2aj with a=7d7/2 modulo8. The converse follows immediately. Therefore Ψ identifies precisely the permissible scalar/shift equivalence classes, in a group of order 2·16^6=33,554,432.

The 70 nontrivial legal factors produce35 nonzero signatures; including identity gives36. The reviewer also checked signature invariance for all16 scalar multipliers and all8 shifts on every legal factor, and checked all64 matrix entries of560 legal factor/modulation conjugations.

## 3. Exhaustion and minimum

Let A include those35 signatures and zero. Starting at B0={0}, generate B(d+1)=Bd+A. Because zero is included, Bd is exactly the set represented by at most d stages. The independent counts are

1,36,624,6841,52560,303488 through depth5.

All candidate B1–B5 binary files were compared state-for-state against the independently recreated sets after changing from the candidate's pivot1 chart to the reviewer's pivot7 chart. Matching counts alone were not used as evidence. The discovery-only B6 count1,375,720 was also independently reproduced; it is unnecessary for the proof.

Every word of at most10 stages splits into two words of at most5 stages. Hence such a word exists exactly when B5 intersects target−B5. The complete intersection has zero elements for ζ=3,11,14,6. For ζ=10,5,7,12, the B5 versus target−B4 intersection is empty, excluding all lengths≤9. The corresponding B5/B5 intersections have2016,608,2016,608 elements respectively. Explicit10-stage witnesses for these four roots and11-stage witnesses for the other four close the upper bounds. This proves the exact eight-root classification.

## 4. Explicit ζ=3 construction and all-row verification

The11 ordered pairs (s,α) are

(3,14),(3,12),(3,11),(2,10),(2,5),(1,5),(4,3),(3,7),(1,14),(1,11),(1,10).

Their binomial product P has cyclic coefficients (8,10,8,6,9,10,9,6). The inverse chirp coefficients are q=(15,5,9,12,15,12,9,5), and q=10 S^3 P. Therefore

C=12 S^5 ∏(I−α S^s)^−1.

The exact stage divisors are2,2,2,14,5,2,9,2,2,2,2, all nonzero. The reviewer checked every recorded coefficient and divisor, every product matrix by independent dense modular arithmetic, and the actual cyclic-solve executor on all8 basis vectors. All64 entries equal3^((i−j)^2). The inverse q was separately checked by modular Gaussian elimination and both products C C^−1 and C^−1 C. The same checks cover all8 primitive roots.

Negative controls: removing the scalar or the shift produces64 mismatches; a legal factor mutation produces56. This rules out an accidentally unchecked endpoint or parameter.

## 5. Full cost audit and boundaries

For g=gcd(8,s), the declared cycle solver costs16−g multiplications and16−2g additions per stage and writes8 outputs. The11-stage witness has Σg=16. Independent instrumentation reproduces160 multiplications and144 additions for the stages, plus8 scalar multiplications and8 endpoint writes:168 multiplications,144 additions,96 application-buffer writes total.

Denominator preparation costs29 multiplications,11 subtractions,11 inversions, and11 separately charged inverse-divisor stores. Four additional squarings verify the supplied root and yield ω=9. First application including those checks therefore costs201 multiplications,155 additions/subtractions,11 inversions,11 preparation stores, and96 application writes. The two length8 application buffers are reused. Factor parameters, strides, root/scalar/shift constants, cycle metadata, comparisons, and indexing are explicit additional discrete work. No unprovided coefficients or roots are free. Inversion-as-one-operation is only a field-operation convention.

The listed factor constants were found by exhaustive finite search. Through B5 there are2,162,232 generator-addition transitions; adding discovery-only B6 gives13,087,800, before set maintenance and intersection work. B5 alone occupies1,213,952 bytes in its four-byte encoding. Verification and discovery are separate from applying the published fixed operator.

These are upper bounds for one unfused executor, not runtime lower bounds or a speedup over a DFT algorithm. The accepted classical fused Green control and generic L≥m+1 theorem remain intact. The finite result shows the bound4 is unattainable in F17 at N8 for every primitive root; it leaves uniform and other-field matching questions open.

## Disposition

The bounded stronger-obstruction obligation and exact finite matching witness are accepted. The general matching-construction question remains open, and all prior scope and historical-priority qualifications are retained. No broader solved claim follows.
