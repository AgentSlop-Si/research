Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 1487122b1177b72aa44605a810c17974919c7404dd8751bd7d262d7b1eb6edfb

---

Independent review of the general odd Rogers Szego guards


                  ACCEPT after normalization repair                11 October 2026 UTC


Decision. ACCEPT the final sealed candidate for the precise theorem below. Its general nonvan-
ishing, separation, nonreality, and two all-size overlap ranges are proved. The degree-seven ordinary-
discriminant and unit-circle claims are also proved. One signed evaluation was corrected before the
candidate was sealed; it does not change any theorem scope. Historical priority is unresolved.


1 Accepted theorem and remaining guards

Let 𝑑 = 2ℎ + 1 ≥ 3, 𝑏 = 2𝑚 + 1 < 𝑑, 𝑚 ≥ 0, and let 𝑞 have exact order 𝑑 in characteristic zero. Use
the accepted normalization
                                𝑏
                                   𝑏 𝑘
                 𝐻𝑏 (𝑧; 𝑞) =           𝑧 = (𝑧 + 1)𝑈 (𝑧),       𝐹 (𝑧) = 1 + 𝑧 𝑑 ,   𝑔 = 𝑈 (−1),
                               𝑘=0
                                   𝑘 𝑞


                         (𝑞; 𝑞)𝑏                  𝑑𝑊
               𝑊 =                     ,     𝜏=      ,       𝐽𝐴+1 = 𝑥 He𝐴 (𝑥) − 𝐴𝜏 He𝐴−1 (𝑥).
                     (𝑞 ; 𝑞 2 )(𝑑+𝑏)/2
                       2                           𝑔
The He𝑗 are monic probabilists' Hermite polynomials. Then

            𝑔 ≠ 0,      Res𝑧 (𝐹 , 𝑈 ) ≠ 0,        𝜏 ∉ ℝ in every primitive complex embedding.

For every integer 𝐴 ≥ 1,

                        Disc𝑥 𝐽𝐴+1 ≠ 0       if 𝑏 < 𝑑 ≤ 2𝑏 + 1      or 𝑑 ≥ 11(𝑏 + 1).

For 𝑏 = 7, every odd 𝑑 ≥ 9 also has Disc𝑧 𝑈 ≠ 0 and no unit-circle zero of 𝑈 in any primitive embedding.
Therefore all Section 3.2 guards are discharged for 𝑏 = 7 at 𝑑 = 9, 11, 13, 15 and every odd 𝑑 ≥ 89.
Cumulative integration boundary. The previously accepted 𝑏 = 1, 3, 5 families keep their all-𝐴,
all-odd-𝑑 > 𝑏 conclusions. In the general odd domain the guards 𝑔 ≠ 0 and Res(𝐹 , 𝑈 ) ≠ 0 may now be
removed. Ordinary residual squarefreeness remains a separate guard for odd 𝑏 ≥ 9. The overlap guard
remains separate for odd 𝑏 ≥ 7 in 2𝑏 + 1 < 𝑑 < 11(𝑏 + 1) unless another accepted argument covers the
instance. In particular this review makes no all-𝐴 claim for 𝑏 = 7, odd 17 ≤ 𝑑 ≤ 87. Finite controls in
that strip are not an all-𝐴 proof.




                                                         1

2 Sector proof and exact normalization audit

The independent controls construct 𝐻𝑛 from the finite Euler product
                                      𝑛−1                      𝑛
                                                                                     𝑛 𝑘
                                            (1 + 𝑞 𝑗 𝑧) =              𝑞 𝑘(𝑘−1)/2        𝑧 .
                                      𝑗=0                     𝑘=0
                                                                                     𝑘 𝑞

Thus the controls do not assume the candidate's degree recurrence. Algebraically that recurrence is

                                   𝐻𝑛+1 = (1 + 𝑧)𝐻𝑛 − (1 − 𝑞 𝑛 )𝑧𝐻𝑛−1 .

Reciprocity gives the odd value 𝐻2𝑚+1 (−1) = 0, while the recurrence gives 𝐻2𝑚 (−1) = (𝑞; 𝑞 2 )𝑚 .
                                  ′
Differentiating at −1, with 𝑔𝑚 = 𝐻2𝑚+1 (−1), yields

                               𝑔𝑚 = (𝑞; 𝑞 2 )𝑚 + (1 − 𝑞 2𝑚 )𝑔𝑚−1 ,                        𝑔0 = 1.

Consequently, with
                                                                       𝑟
                                       (𝑞; 𝑞 2 )𝑗
                               𝑠𝑗 =                 ,   𝑆𝑟 =               𝑠𝑗 ,   𝐸 = (𝑞 2 ; 𝑞 2 )ℎ ,
                                      (𝑞 2 ; 𝑞 2 )𝑗                𝑗=0

we obtain 𝑔𝑚 = (𝑞 2 ; 𝑞 2 )𝑚 𝑆𝑚 without using 𝜏 .
The denominator of 𝑊 has length (𝑑 + 𝑏)/2 ≤ 𝑑 − 1, and 𝑞 2 has order 𝑑. The denominators defining 𝑠𝑗
have lengths 𝑗 ≤ ℎ < 𝑑. All are nonzero. In the principal embedding put 𝑣 = 𝜋/𝑑, 𝑞 = 𝑒2𝑖𝑣 ; then
                                                                       𝑗
                                          −𝑖𝑗𝑣                         sin((2𝑟 − 1)𝑣)
                               𝑠𝑗 = 𝑎𝑗 𝑒         ,          𝑎𝑗 =                      > 0.
                                                                   𝑟=1
                                                                          sin(2𝑟𝑣)

Here ℎ𝑣 < 𝜋/2; all summands have positive real part. This proves 𝑆𝑚 ≠ 0 and 𝑔 ≠ 0. The positivity is
used only in this selected embedding. Algebraic nonvanishing then holds in every embedding.
At 𝑛 = 𝑑, the middle Gaussian coeﬀicients vanish, so 𝐻𝑑 = 1 + 𝑧 𝑑 and 𝐸𝑆ℎ = 𝑑. In the original
denominator of 𝑊 , the factors following 𝐸 are precisely the odd factors through 1 − 𝑞 2𝑚+1 . Their
cancellation proves
                                         (𝑞 2 ; 𝑞 2 )𝑚      𝑆
                                    𝑊 =                , 𝜏 = ℎ.
                                               𝐸            𝑆𝑚
In particular no factor 𝑑, sign, or Hermite rescaling has been lost. For 𝑇 = 𝑆ℎ − 𝑆𝑚 ,
                                                        ℎ      𝑚
                              Im(𝑇 𝑆𝑚 ) = −                            𝑎𝑗 𝑎𝑘 sin((𝑗 − 𝑘)𝑣) < 0.
                                                     𝑗=𝑚+1 𝑘=0

The sum is nonempty because 𝑏 < 𝑑 implies 𝑚 < ℎ. Thus Im 𝜏 < 0 in the principal embedding.
Cyclotomic automorphisms commute with complex conjugation, so the nonzero algebraic number 𝜏 − 𝜏
remains nonzero under every automorphism. Only nonreality, not the sign or sector inequalities, is
transported to all primitive embeddings.




                                                                   2

3 Separation proof and every boundary index

Coeﬀicient comparison gives

                                 𝐻𝑏 (𝑞𝑧) = (1 − 𝑧)𝐻𝑏 (𝑧) + 𝑞 𝑏 𝑧𝐻𝑏 (𝑞 −1 𝑧).

The degree recurrence also gives

                           𝐻2𝑚 (−𝑞) = (𝑞; 𝑞 2 )𝑚 ,        𝐻2𝑚+1 (−𝑞) = (𝑞; 𝑞 2 )𝑚+1 .

The largest exponent in the latter product is 𝑏 < 𝑑, so 𝑓1 = 𝐻𝑏 (−𝑞) ≠ 0. This starting value is essential;
a recurrence with 𝑓0 = 0 alone would not establish separation.
Set 𝑓𝑘 = 𝐻𝑏 (−𝑞 𝑘 ) in the principal embedding. Then

                                𝑓0 = 0,      𝑓𝑘+1 = (1 + 𝑞 𝑘 )𝑓𝑘 − 𝑞 𝑏+𝑘 𝑓𝑘−1 .

The explicit exponential gauge

                                 𝑓𝑘 = 𝑒𝑖𝑣𝑘(𝑘+2𝑏)/2 𝑢𝑘 ,       𝜆 = 𝑒−𝑖𝑣(2𝑏+1)/2

changes this to
                                       𝑢𝑘+1 = 2𝜆 cos(𝑘𝑣)𝑢𝑘 − 𝑢𝑘−1 .
The forward exponent is −(2𝑏 + 1)𝑣/2 and the backward exponent cancels exactly. No ambiguous
fractional power is used. Since 𝑏 ≤ 𝑑 − 2,

                                                 (2𝑏 + 1)𝜋
                                            0<             < 𝜋;
                                                     2𝑑
therefore 𝜆 is nonreal, including the largest allowed 𝑏.
Let 𝑐𝑘 = 2 cos(𝑘𝑣) > 0 for 1 ≤ 𝑘 ≤ ℎ. With 𝑝0 = 1, 𝑝1 = 𝑐1 𝜆, and 𝑝𝑟 = 𝑐𝑟 𝜆𝑝𝑟−1 − 𝑝𝑟−2 , induction
gives 𝑢𝑘 = 𝑢1 𝑝𝑘−1 . The monic polynomials 𝑝𝑟 /(𝑐1 ⋯ 𝑐𝑟 ) are characteristic polynomials of real symmetric
                                                                    √
tridiagonal matrices whose consecutive off-diagonal entries are 1/ 𝑐𝑗 𝑐𝑗+1 . Their zeros are real. Hence
𝑓𝑘 ≠ 0 for all 1 ≤ 𝑘 ≤ ℎ + 1.
Reciprocity and odd 𝑏 give
                                              𝑓𝑑−𝑘 = −𝑞 −𝑘𝑏 𝑓𝑘 .
The first half of the orbit and its reflected half cover every 1 ≤ 𝑘 < 𝑑; no unproved positivity beyond
𝑐ℎ is needed. As 𝑑 is odd, the roots of 𝐹 are exactly −𝑞 𝑘 , 0 ≤ 𝑘 < 𝑑. At 𝑘 = 0, 𝑈 (−1) = 𝑔 ≠ 0. At all
other orbit points,
                                                         𝑓𝑘
                                           𝑈 (−𝑞 𝑘 ) =        ≠ 0.
                                                       1 − 𝑞𝑘
This proves the resultant is nonzero and transfers algebraically to every primitive embedding. It does
not establish absence of arbitrary unit-circle roots for general 𝑏.




                                                          3

4 The critical annulus and exceptional cases

The accepted critical-parameter lemma was rechecked, including the normalization of its rank-one
perturbation. For 𝐴 = 1, 2,
                               𝐽2 = 𝑥 2 − 𝜏 , 𝐽3 = 𝑥(𝑥2 − 1 − 2𝜏 ),
so the only multiple-root parameters are 0 and −1/2. At 𝑥 = 0, the potential critical parameters for
general 𝐴 are also real: 0 when 𝐴 is odd and −1/𝐴 when 𝐴 is even. These cases cannot occur for the
current 𝜏 .
At a nonzero multiple root, consecutive Hermite factors are nonzero by their recurrence. Differentiation
gives
                                                                         𝜏 (𝐴𝜏 + 1)
                   𝐽 ′ = (1 + 𝐴𝜏 ) He𝐴 +𝐴𝑥(1 − 𝜏 ) He𝐴−1 ,     𝑦 = 𝑥2 =             .
                                                                            𝜏 −1
Write 𝐴 + 1 = 2𝑟 + 𝑠, 𝑠 ∈ {0, 1}, and 𝛼 = 𝑠 − 1/2. The quadratic Hermite--Laguerre identity expresses
𝐽 = 𝑥𝑠 det(𝑥2 𝐼 −𝑀 ), where 𝑀 is complex symmetric tridiagonal. Its unperturbed diagonal is 4𝑗+2𝛼+2
for 0 ≤ 𝑗 < 𝑟; its off-diagonal is 2 𝑗(𝑗 + 𝛼) for 1 ≤ 𝑗 < 𝑟. Its last diagonal is shifted by 𝐴(𝜏 − 1),
becoming 𝐴 − 1 + 𝐴𝜏 .
The off-diagonal entries are nonzero, so each eigenspace is one-dimensional and an eigenvector's last
coordinate is nonzero. A repeated eigenvalue admits a Jordan chain. Complex symmetry then gives
𝑣𝑇 𝑣 = 0; this is a bilinear transpose identity, not a Hermitian one. Consequently

                                                      |𝑣𝑟 |2  1
                                           0 < 𝑡 ∶=          ≤ .
                                                      ‖𝑣‖2    2

Separately the Hermitian inner product gives
                                               Im 𝑦
                                                    = 𝐴𝑡.
                                               Im 𝜏
Taking imaginary parts of the displayed rational expression for 𝑦, and putting 𝜌 = |𝜏 − 1|2 , yields

                                      𝐴+1                 1       2  8
                           𝐴𝑡 = 𝐴 −       ,        1+       <𝜌 ≤2+ ≤   .
                                       𝜌                  𝐴       𝐴  3

Here 𝐴 ≥ 3. The inner bound is strict and the outer bound is inclusive. The argument does not assume
that the complex symmetric matrix is diagonalizable.
Finally 𝐷𝐴 (𝑇 ) = Disc𝑥 𝐽𝐴+1 (𝑥; 𝑇 ) lies in ℚ[𝑇 ]. If 𝐷𝐴 (𝜏 ) = 0 at one primitive embedding, it vanishes
at all conjugates. A single principal-embedding norm outside the annulus therefore excludes vanishing
everywhere. Neither the sector positivity nor the norm bounds need hold at every conjugate.




                                                      4

5 Exact range endpoints and the large order estimate

Reflection of the finite sums gives

                                                                          |𝑆ℎ−𝑚−1 |2
                               𝑠ℎ−𝑗 = 𝑠ℎ 𝑠𝑗 ,     |𝑠ℎ | = 1,         𝜌=              .
                                                                            |𝑆𝑚 |2

The index ℎ − 𝑚 − 1 is nonnegative. Each increment

                               |𝑆𝑗 |2 − |𝑆𝑗−1 |2 = 𝑎2𝑗 + 2         𝑎𝑗 𝑎𝑘 cos((𝑗 − 𝑘)𝑣)
                                                             𝑘<𝑗


is strictly positive since 0 ≤ (𝑗 − 𝑘)𝑣 < 𝜋/2. Thus

                              𝜌≤1     ⟺         ℎ−𝑚−1≤𝑚              ⟺      𝑑 ≤ 2𝑏 + 1.

Equality is exactly 𝑑 = 2𝑏 + 1 and gives 𝜌 = 1, which is still strictly below the annulus. The case 𝑚 = 0,
𝑑 = 3 is included.
For the other range assume 𝑑 ≥ 22(𝑚 + 1) = 11(𝑏 + 1). Then (2𝑚 + 1)𝑣 < 𝜋/2. The identity

                              sin2 (2𝑟𝑣) − sin((2𝑟 − 1)𝑣) sin((2𝑟 + 1)𝑣) = sin2 𝑣

and a telescoping product give

                                         sin 𝑣                𝜋
                         𝑎𝑗 ≤                      <                        (0 ≤ 𝑗 ≤ 𝑚).
                                    sin((2𝑗 + 1)𝑣)        2(2𝑗 + 1)

The first inequality is equality at 𝑗 = 0 and strict for 𝑗 > 0; the second is strict also at 𝑗 = 0. The
bounds sin 𝑣 < 𝑣 and sin 𝑢 ≥ 2𝑢/𝜋 justify the second step in the entire required interval.
The convex, integrable function 𝑢−1/2 satisfies the midpoint integral bound on each interval [𝑗, 𝑗 + 1],
including the improper interval at zero. Hence
                                  𝑚       √ 𝑚
                                            𝜋
                         |𝑆𝑚 | ≤     𝑎𝑗 <         (𝑗 + 1/2)−1/2 ≤ 𝜋(𝑚 + 1).
                                 𝑗=0
                                           2  𝑗=0


The even residues and their negatives partition the nonzero residues modulo odd 𝑑. Thus 𝐸𝐸 =
 𝑑−1                                                  √
∏𝑟=1 (1 − 𝑞 𝑟 ) = 𝑑, also for composite 𝑑, and |𝑆ℎ | = 𝑑. Therefore

                                   𝑑                      √                 √
                     |𝜏 | >              ≥       22/𝜋 >       7,       𝜌 > ( 7 − 1)2 > 8/3.
                                𝜋(𝑚 + 1)

The last comparison is exact: 7 < 64/9. Both stated ranges are therefore suﬀicient for every 𝐴 ≥ 1.
No limiting statement in 𝐴, estimate uniform in a varying local parameter, or finite-grid extrapolation
occurs.




                                                        5

6 Ordinary residual squarefreeness and degree seven

Recovering the trace polynomial independently from the reciprocal coeﬀicients of 𝑈 confirms

                           𝑈 (𝑧) = 𝑧 𝑚 𝑃𝑚 (𝑧 + 𝑧 −1 ),      𝑃0 = 1,      𝑃1 = 𝑡 + 𝑞 + 𝑞 2 ,

                      𝑃𝑚 = (𝑡 + 𝑞 2𝑚−1 + 𝑞 2𝑚 )𝑃𝑚−1 − (1 − 𝑞 2𝑚−1 )(1 − 𝑞 2𝑚−2 )𝑃𝑚−2 .
Factoring 𝑧𝑚 𝑃 (𝑧 + 𝑧 −1 ) into 𝑧2 − 𝑡𝑗 𝑧 + 1 proves

                                    Disc𝑧 𝑈 = 𝑃𝑚 (2)𝑃𝑚 (−2) Disc𝑡 (𝑃𝑚 )2 .

The required signed evaluation is
                                               𝑃𝑚 (−2) = (−1)𝑚 𝑔.
The pre-seal candidate incorrectly wrote 𝑃𝑚 (−2) = 𝑔. This is false for every tested odd 𝑚, including
𝑚 = 1 and 𝑚 = 3. The author repaired the equality before sealing and added sign controls. The proof
uses only nonvanishing here, so no theorem or bound changed.
The remaining general ordinary-discriminant issue is exactly

                      Φ𝑑 (𝑞) ∤ 𝑃𝑚 (2; 𝑞) Disc𝑡 𝑃𝑚 (𝑡; 𝑞)         (𝑚 ≥ 1, 𝑑 ≥ 2𝑚 + 3 odd).

It is not settled in general by this review.
For 𝑚 = 3, the independent Euler-product construction reproduces all coeﬀicients of the candidate's
𝑀 = 𝑃3 (2) and its degree-21 𝐿, with

                               Disc𝑡 𝑃3 = (𝑞 − 1)6 (𝑞 + 1)3 (𝑞 2 + 𝑞 + 1)𝐿(𝑞).

For 𝑅∗ (𝑞) = 𝑞 deg 𝑅 𝑅(𝑞 −1 ), exact recomputation gives

                                         Res(𝑀 , 𝑀 ∗ ) = 34359738368,

               Res(𝐿, 𝐿∗ ) = −89571360600204619396790555761440557562912921600000.
Independent rational Bezout identities certify both gcds are 1. A real-coeﬀicient polynomial with a
unit-circle zero shares it with its reverse. These nonzero resultants exclude all unit-circle zeros of 𝑀 , 𝐿;
the remaining factors have orders at most 3. Together with 𝑔 ≠ 0 this proves Disc(𝑈 ) ≠ 0 for all odd
𝑑 ≥ 9.
The separate mixed resultant is exactly

                           Res𝑡 (𝑃3 , 𝑞 12 𝑃3 (𝑡; 𝑞 −1 )) = −Φ91 Φ52 Φ33 Φ24 Φ45 Φ46 Φ37 𝐵(𝑞),

where 𝐵 = 𝑞 6 + 𝑞 5 + 𝑞 3 + 𝑞 + 1. A unit-circle zero of 𝑈 would give a real common trace root and force
this resultant to vanish. If a primitive odd root of order 𝑑 ≥ 9 killed 𝐵, then 𝜑(𝑑) ≤ 6. Its prime
divisors can only be 3, 5, 7; the allowed exponents and products leave exactly the odd orders 1, 3, 5, 7, 9.
Hence 𝑑 = 9. But 𝐵 mod Φ9 = 𝑞 5 + 𝑞 ≠ 0. Thus 𝑈 has no unit-circle zero in this degree-seven domain.
This conclusion is not inferred from the noncyclotomic nature of 𝐵 or numerical root plots.




                                                           6

7 Controls provenance and final disposition

Independent exact controls. All 745 checks pass. They reconstruct Gaussian coeﬀicients through
the finite Euler product, recover trace polynomials through the symmetric Laurent basis, check signed
evaluations and ordinary discriminants, recompute the degree-seven resultants and rational Bezout
identities, and verify the critical-parameter Jacobi and derivative normalizations for 1 ≤ 𝐴 ≤ 12. Exact
cyclotomic arithmetic tests all odd 𝑏 < 𝑑 for odd 3 ≤ 𝑑 ≤ 21, including every nontrivial orbit point in
the separation claim. Actual overlap discriminants are also checked for 1 ≤ 𝐴 ≤ 8, odd 3 ≤ 𝑑 ≤ 17.
These are corroborating controls, not proofs of infinite parameter ranges. Only the new review program
was executed. The candidate and prior uploaded or historical programs were treated as inert source.
No manuscript, Sheet, repository, ranking, or access setting was changed.
Noncyclotomic obstruction. The identity

                            𝐵(𝑞)/𝑞 3 = 𝑤3 + 𝑤2 − 3𝑤 − 1,       𝑤 = 𝑞 + 𝑞 −1 ,

has exact sign brackets (−3, −2), (−1, 0), and (1, 2). A root below −2 proves that 𝐵 is not a product
only of cyclotomic polynomials. This is an obstruction to that factorization pattern, not a root-of-unity
counterexample and not a general squarefreeness proof.
Source identities. The review is pinned to the repaired final candidate. The included source archives
and files are copied without alteration; their exact byte identities and the verified candidate manifest
are recorded in SOURCE_PINS.json.

  1. General odd Rogers Szego residual guards, sealed candidate, 11 October 2026. ZIP SHA-256:
     48637ead399c767d450c5cab8647142bfab7496be5baebe303b6b5c614c1605d. Repaired LaTeX
     SHA-256:
     f2ea051fa8e491f97198a1bcaaff991f70a0c3fc0e585fe39b4f3e0359313542.

  2. Local ordinary discriminants of Rogers Szego polynomials at odd roots of unity, version 3, Section
     3.2. LaTeX SHA-256:
     57bc17168b7b11efe7a5bdc7190473267b0c08fcd4f2bb5b9c59f04f1cbfa282.

  3. RS overlap simplicity independent mathematical review, ACCEPT, and Independent review of
     degree five Rogers Szego overlap simplicity, ACCEPT. The former supplies the accepted critical-
     annulus baseline, rechecked in Section 4; the latter preserves the already proved full degree-five
     family. Their source identities are in the pins.

Final disposition. ACCEPT the repaired candidate, with the general ordinary residual lemma and
the intermediate overlap strip retained exactly as stated in Section 1. The review needs no further
mathematical repair. The seal certifies artifact identity, not historical novelty. Characteristic two
or other positive characteristic, even order, nonprimitive roots, 𝐴 = 0, and uniform growing-degree
stability are outside this theorem.




                                                   7
