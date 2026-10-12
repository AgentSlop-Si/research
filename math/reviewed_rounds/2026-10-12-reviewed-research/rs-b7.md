Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 87da4c31f51e9e79c5166a170cef37ec68f4bc0cc0f26303ce84628a179e73a9

---

Independent review of degree seven Rogers Szego overlap closure


                                                ACCEPT 11 October 2026 UTC


Decision. ACCEPT the degree-seven full-strip closure. The finite norm signs are correct, every root
used in the sign argument is an actual conjugate of the required squared modulus, and the rational
large-order estimate proves the entire infinite tail. The exact order 17 split handles every integer 𝐴 ≥ 1.
No mathematical repair was required. Historical priority is unresolved.


1 Accepted theorem and integration scope

Let 𝑑 ≥ 9 be odd, let 𝑞 have exact order 𝑑 in any field of characteristic zero, and let 𝐴 ≥ 1 be an integer.
In the accepted normalization set
                                    7
                                       7 𝑘
               𝐻7 (𝑧; 𝑞) =                 𝑧 = (𝑧 + 1)𝑈 (𝑧),             𝐹 (𝑧) = 1 + 𝑧𝑑 ,    𝑔 = 𝑈 (−1),
                                   𝑘=0
                                       𝑘 𝑞


                         (𝑞; 𝑞)7                        𝑑𝑊
             𝑊 =                            ,      𝜏=      ,     𝐽𝐴+1 (𝑥; 𝜏 ) = 𝑥 He𝐴 (𝑥) − 𝐴𝜏 He𝐴−1 (𝑥),
                   (𝑞 2 ; 𝑞 2 )   (𝑑+7)/2                𝑔
where He𝑛 is monic probabilists' Hermite. Then

                       𝑔 ≠ 0,               Disc𝑧 𝑈 Res𝑧 (𝐹 , 𝑈 ) ≠ 0,       Disc𝑥 𝐽𝐴+1 (𝑥; 𝜏 ) ≠ 0.

Moreover, 𝑈 has no unit-circle zero and 𝜏 is nonreal in every primitive complex embedding. Those
two statements refer to embeddings of the cyclotomic field, not to an ordering or conjugation on an
arbitrary base field.
The accepted general-guards review already establishes the residual guards for every odd 𝑑 ≥ 9 and the
overlap guard at 𝑑 = 9, 11, 13, 15 and odd 𝑑 ≥ 89. This review closes the missing strip and supplies a
sharper analytic tail starting at 39. The complete coverage is

                             {9, 11, 13, 15},        {17},     {19, 21, … , 37},    {39, 41, …}.

Thus the manuscript's Section 3.2 guards are automatic for the entire 𝑏 = 7 family. Previously accepted
𝑏 = 1, 3, 5 results remain intact. No new claim is made for 𝑏 ≥ 9, even order, nonprimitive roots, positive
characteristic, 𝐴 = 0, or uniform growing-degree stability. No manuscript, Sheet, GitHub file, or ranking
was edited.




                                                                 1

2 Normalization and the necessary critical annulus

Write 𝑑 = 2ℎ + 1 and put
                       ℎ
                 𝐸=         (1 − 𝑞 2𝑗 ),       𝐾 = 𝑞 7 + 3𝑞 6 + 4𝑞 5 + 6𝑞 4 + 7𝑞 3 + 5𝑞 2 + 5𝑞 + 4,
                      𝑗=1


                                           𝑁 = (𝑞 + 1)3 (𝑞 2 + 1)(𝑞 2 − 𝑞 + 1).
An independent Gaussian Pascal construction gives
                                                           3
                                3   2
                  𝑔 = (1 − 𝑞) (𝑞 + 𝑞 + 1)𝐾,                     (1 − 𝑞 2𝑗 ) = (1 − 𝑞)3 (𝑞 2 + 𝑞 + 1)𝑁 .
                                                          𝑗=1


The original denominator following 𝐸 consists of exactly the odd factors 1 − 𝑞, 1 − 𝑞 3 , 1 − 𝑞 5 , 1 − 𝑞 7 .
Cancelling them proves
                                 (1 − 𝑞 2 )(1 − 𝑞 4 )(1 − 𝑞 6 )      𝑑𝑁
                            𝑊 =                                 , 𝜏=    .
                                              𝐸                      𝐸𝐾
The factors in the original denominator have indices at most (𝑑 + 7)/2 ≤ 𝑑 − 1. Since 𝑞 2 also has order
𝑑, none vanishes. The accepted sector proof establishes 𝑔 ≠ 0 independently of 𝜏 , hence also 𝐾 ≠ 0.
The imported critical-parameter lemma was checked with its exact normalization. For 𝐴 = 1, 2, the
polynomials are 𝑥2 − 𝜏 and 𝑥(𝑥2 − 1 − 2𝜏 ); their only multiple-root parameters are respectively 0 and
−1/2. These are excluded by nonreality. For 𝐴 ≥ 3, a nonreal multiple-root parameter necessarily
obeys
                                    1                         2    8
                                1 + < 𝜌 ∶= |𝜏 − 1|2 ≤ 2 + ≤ .                                       (1)
                                    𝐴                         𝐴    3
For clarity, at a nonzero multiple root 𝑦 = 𝑥2 = 𝜏 (𝐴𝜏 + 1)/(𝜏 − 1). The parity-Jacobi matrix for 𝐽 is
complex symmetric with real nonzero off-diagonal entries and last-diagonal shift 𝐴(𝜏 − 1). A repeated
eigenvalue has an isotropic eigenvector 𝑣𝑇 𝑣 = 0. Its last-coordinate mass 𝑡 = |𝑣𝑚 |2 /‖𝑣‖2 therefore lies
in (0, 1/2]. Taking the Hermitian inner product and then the imaginary part of the rational formula
for 𝑦 yields
                                             Im 𝑦          𝐴+1
                                        𝐴𝑡 =      =𝐴−           ,
                                             Im 𝜏            𝜌
which proves (1). The strict inner endpoint and inclusive outer endpoint are retained.
The polynomial 𝐷𝐴 (𝑇 ) = Disc𝑥 𝐽𝐴+1 (𝑥; 𝑇 ) belongs to ℚ[𝑇 ]. If 𝐷𝐴 (𝜏 ) = 0, it vanishes at every cyclo-
tomic conjugate. Since the automorphisms commute with conjugation, every conjugate of (𝜏 − 1)(𝜏 − 1)
is |𝜎(𝜏 ) − 1|2 . One embedding violating (1), chosen separately for each 𝐴 if necessary, therefore suﬀices.




                                                               2

3 Independent exact norms and the exceptional order

The review computes 𝜏 through a separate route. Define
                                                                    𝑗
                                          (𝑞; 𝑞 2 )𝑗
                                     𝑠𝑗 = 2 2 ,             𝑆𝑗 =         𝑠𝑘 .
                                         (𝑞 ; 𝑞 )𝑗                 𝑘=0

The sector identities give 𝜏 = 𝑆ℎ /𝑆3 . The fresh controls form this element in ℚ[𝑞]/Φ𝑑 (𝑞), form 𝜌, and
recover its coordinates in the basis 1, 𝑤, … , 𝑤𝑒−1 , where 𝑤 = 𝑞 + 𝑞 −1 and 𝑒 = 𝜑(𝑑)/2.
                2𝑒
For Φ𝑑 (𝑞) = ∑𝑗=0 𝑎𝑗 𝑞 𝑗 , let 𝐶0 = 2, 𝐶1 = 𝑤, and 𝐶𝑗 = 𝑤𝐶𝑗−1 − 𝐶𝑗−2 . Then

                                        𝑒
                       Ψ𝑑 (𝑤) = 𝑎𝑒 +         𝑎𝑒+𝑗 𝐶𝑗 (𝑤),   𝑞 −𝑒 Φ𝑑 (𝑞) = Ψ𝑑 (𝑞 + 𝑞 −1 ).
                                       𝑗=1


The monic polynomial Ψ𝑑 is the minimal polynomial of 𝑤. If the reconstructed element is 𝜌 = 𝑅𝑑 (𝑤),
the direct real-field norm is
                                                                                𝑃𝑑 (𝑟)
                         Normℚ(𝑤)/ℚ (𝑟 − 𝜌) = Res𝑤 (Ψ𝑑 (𝑤), 𝑟 − 𝑅𝑑 (𝑤)) =              .                (2)
                                                                                lc 𝑃𝑑

Every one of the eleven resulting primitive integer polynomials 𝑃𝑑 , 17 ≤ 𝑑 ≤ 37 odd, agrees exactly
with the candidate. The candidate's full cyclotomic norm is consequently (𝑃𝑑 / lc 𝑃𝑑 )2 .
No spurious roots. A number-field norm is the product over its embeddings. Every real embedding
of ℚ(𝑤) extends to a cyclotomic embedding, and that extension sends 𝜌 to |𝜎(𝜏 ) − 1|2 . Thus every
root of 𝑃𝑑 is an actual required squared modulus. Irreducibility of 𝑃𝑑 is unnecessary. No arbitrary
annihilating polynomial or numerical root matching is substituted for (2).
At order 17 the primitive polynomial is

                     𝑃17 (𝑟) = 229341493𝑟8 − 2832707713𝑟7 + 15153887119𝑟6
                               − 45862604969𝑟5 + 85895432910𝑟4 − 101959063189𝑟3
                               + 74922959651𝑟2 − 31169293390𝑟 + 5622131609.

Exact evaluations give
                                                                     9069396911
                         𝑃17 (1) = 83521 > 0,       𝑃17 (10/9) = −              < 0,
                                                                      43046721
                                                  154258905557
                                    𝑃17 (11/5) = −               < 0.
                                                     390625
The positive leading coeﬀicient gives a root above 11/5, while the first two signs give a root in (1, 10/9).
For 3 ≤ 𝐴 ≤ 9, the inner bound in (1) is at least 10/9, so the small root excludes a collision. For
𝐴 ≥ 10, the outer bound is at most 11/5, so the large root excludes a collision. Exact Sturm counts
independently give one root in each of these intervals. The already separated 𝐴 = 1, 2 cases complete
order 17.




                                                        3

4 All remaining finite orders and the infinite tail

For each remaining odd order through 37, the positive-leading primitive polynomial has the following
exact negative value at a point 𝑐 ≥ 8/3. The intermediate value theorem gives a root strictly above 𝑐,
excluding (1) for every 𝐴 ≥ 3.

                                    𝑑        𝑐                           𝑃𝑑 (𝑐)
                                   19      8/3    −1088668231078537/19683
                                   21      8/3            −120768983/729
                                   23        3             −161720487281
                                   25        5          −216289055473499
                                   27      8/3     −37354316402647/19683
                                   29        3        −43176635789238461
                                   31        4      −68010412188104193293
                                   33       10     −15523282721476551537
                                   35        3       −2420168966942357819
                                   37        4    −2274903861783142712281

The complete coeﬀicients and real-field representations are in the independent certificate. Exact Sturm
counts of roots in (8/3, ∞) are respectively 1, 3, 4, 4, 5, 8, 8, 6, 8, 12, providing an additional independent
check of the required witnesses.
Now suppose 𝑑 ≥ 39 is odd, and choose 𝑞 = 𝑒2𝑖𝑣 with 𝑣 = 𝜋/𝑑. The rational bound 𝜋 < 22/7 gives

                                        0 < 𝑣 ≤ 𝜋/39 < 22/273 < 1/12.

The coeﬀicients
           √ of 𝐾 are positive and sum to 35, so |𝐾| ≤ 35. The cyclotomic complementary product
gives |𝐸| = 𝑑. Also
                              |𝑁 | = 16 cos3 𝑣 cos(2𝑣)(2 cos(2𝑣) − 1).
All factors here are positive. The inequality cos 𝑡 ≥ 1 − 𝑡2 /2 and the strict bound on 𝑣 imply

                                   287                       71                       35
                         cos 𝑣 >       ,         cos(2𝑣) >      ,   2 cos(2𝑣) − 1 >      .
                                   288                       72                       36
Exact rational arithmetic gives
                                3                       √          √
                           287    71 35   15             𝑑 |𝑁 |   3 𝑑
                                         > ,     |𝜏 | =         >     > 1.
                           288 72 36      16             |𝐾|       7
                              √
Therefore 𝜌 ≥ (|𝜏 | − 1)2 > (3 𝑑/7 − 1)2 , whose lower bound increases for 𝑑 ≥ 39. At 𝑑 = 39, its
comparison with 8/3 reduces to
                                  √
                          808    6 39        808 2 36 ⋅ 39      33700
                              >        ,            −        =        > 0.
                          147      7         147        49      21609
Both sides before squaring are positive. Thus 𝜌 > 8/3 for every odd 𝑑 ≥ 39. This is an all-order proof
with no untested tail or numerical trigonometric assumption.




                                                             4

5 Residual imports and the low-order boundary

The accepted general-guards review is a separate sealed theorem, and this review has rechecked the
needed formulas. In the principal embedding,
                                                    𝑗
                                                       sin((2𝑟 − 1)𝑣)
                      𝑠𝑗 = 𝑎𝑗 𝑒−𝑖𝑗𝑣 ,       𝑎𝑗 =                      > 0,             ℎ𝑣 < 𝜋/2.
                                                   𝑟=1
                                                          sin(2𝑟𝑣)

Hence 𝑆3 ≠ 0 and 𝑔 = (𝑞 2 ; 𝑞 2 )3 𝑆3 ≠ 0. The nonempty tail 𝑆ℎ − 𝑆3 has a strictly negative imaginary
pairing with 𝑆3 ; therefore 𝑆ℎ /𝑆3 is nonreal. This algebraic nonreality transfers to every primitive
embedding.
The reflection identity gives
                                                          |𝑆ℎ−4 |2
                                                    𝜌=             .
                                                           |𝑆3 |2
Every prefix modulus strictly increases, since all pairwise phase differences have magnitude below 𝜋/2.
At 𝑑 = 9, 11, 13, 15 we have 0 ≤ ℎ − 4 ≤ 3, so 𝜌 ≤ 1. At 𝑑 = 15 equality holds, which still violates the
strict inner annulus bound. This handles the entire low-order range, including its endpoint.
For ordinary residual squarefreeness, write 𝑈 (𝑧) = 𝑧 3 𝑃3 (𝑧 + 𝑧 −1 ; 𝑞). The exact identity is

                          Disc𝑧 𝑈 = 𝑃3 (2)𝑃3 (−2) Disc𝑡 (𝑃3 )2 ,              𝑃3 (−2) = −𝑔.

The signed evaluation is important and agrees with the corrected sealed predecessor. With 𝑀 = 𝑃3 (2)
and
                             Disc𝑡 𝑃3 = (𝑞 − 1)6 (𝑞 + 1)3 (𝑞 2 + 𝑞 + 1)𝐿(𝑞),
the fresh Gaussian construction reproduces the reverse-polynomial resultants

                                          Res(𝑀 , 𝑀 ∗ ) = 34359738368,

               Res(𝐿, 𝐿∗ ) = −89571360600204619396790555761440557562912921600000.
Thus the real-coeﬀicient polynomials 𝑀 , 𝐿 have no unit-circle zero: such a zero would also annihilate
the reverse polynomial. The remaining displayed factors cannot vanish at odd order 𝑑 ≥ 9. This proves
Disc(𝑈 ) ≠ 0 throughout the theorem.
The separate exact mixed resultant is

                             Res𝑡 (𝑃3 , 𝑞 12 𝑃3 (𝑡; 𝑞 −1 )) = −Φ91 Φ52 Φ33 Φ24 Φ45 Φ46 Φ37 𝐵,

where 𝐵 = 𝑞 6 +𝑞 5 +𝑞 3 +𝑞+1. A unit-circle root of 𝑈 gives a real trace and forces this resultant to vanish.
The displayed cyclotomic factors have order at most 7. If 𝐵 vanished at primitive odd order 𝑑 ≥ 9,
irreducibility would force 𝜑(𝑑) ≤ 6. The only such odd order at least 9 is 9, but 𝐵 mod Φ9 = 𝑞 5 + 𝑞 ≠ 0.
Hence 𝑈 has no unit-circle zero; in particular Res(𝐹 , 𝑈 ) ≠ 0. The general Jacobi separation theorem
independently gives the same resultant guard. All uses are within the exact normalization and domain
of the sealed predecessor.




                                                            5

6 Characteristic zero provenance and final disposition

All characteristic-zero fields. The proof may be performed in ℚ(𝜁𝑑 ) and its complex embeddings.
If 𝑞 has exact order 𝑑 in any characteristic-zero field 𝑘, the map ℚ(𝜁𝑑 ) → 𝑘 sending 𝜁𝑑 to 𝑞 is injective.
Every displayed denominator and discriminant value is an element of this cyclotomic field. Proven
nonzero elements remain nonzero after this injection or any further field extension. No embedding of
the whole field 𝑘 into ℂ is required.
Independent controls. All 245 fresh exact checks pass. They reconstruct 𝐻7 by Gaussian Pascal
recursion, recover the reciprocal residual, recompute its reverse and mixed resultants, form 𝜏 from
the finite prefix sums, and compute norms directly in the maximal real cyclotomic fields. The finite
sign values, exact Sturm root counts, rational tail inequalities, and Hermite derivative and exceptional
discriminants are verified. The real-field defining polynomials and every primitive norm polynomial are
recorded in INDEPENDENT_EXACT_RESULTS.json.
The controls are normalization and finite-certificate corroboration. The written annulus, Galois, interval,
and analytic arguments establish the infinite quantifiers. The candidate program and all older or
uploaded programs were treated as inert source and were not imported or executed. Only the fresh
review program was run.
Source pins. The package includes byte-identical source copies and records exact SHA-256 identities in
SOURCE_PINS.json. The sealed candidate and the accepted predecessor manifests are verified separately.
In particular the following predecessor identities are fixed:

   1. Audited Degree seven Rogers Szego overlap closure, sealed candidate, 11 October 2026. ZIP SHA-
      256:
      db41afdf3e160aa2b817bb7914b1d05ccd36208f0b28e3d39b963c0f3d920424.
     LaTeX SHA-256:
     1b441309a773ea556eec03f6874ecf83e3382b53abb2dd342e59789aa3793eb8.

   2. Independent review of the general odd Rogers Szego guards, ACCEPT, 11 October 2026. ZIP
      SHA-256: 4e5a0c21694ee6dcf1c55412ec44d5a2a3e091fe4e326a976bb47b5aa706d1a6.
      LaTeX SHA-256: c4009870cdb96f0af09065b4e41e98346d8159cc3962d7954a92b73963b2e78c.

   3. RS overlap simplicity independent mathematical review, ACCEPT. LaTeX SHA-256: 590455d943
      c6b936a244c6381a9e01a01a5fd0f0211f8140cd2348bd06730354.

   4. Local ordinary discriminants of Rogers Szego polynomials at odd roots of unity, version 3, Section
      3.2. LaTeX SHA-256: 57bc17168b7b11efe7a5bdc7190473267b0c08fcd4f2bb5b9c59f04f1cbf
      a282.

Integration rule. The degree-seven overlap guard can now be removed for every odd 𝑑 ≥ 9 and every
integer 𝐴 ≥ 1, alongside the already accepted residual guards. This is a full degree-seven theorem. It
is not a general odd-residual squarefreeness theorem and does not close the higher-degree intermediate
strip. Historical novelty and priority remain unresolved. Hashes certify artifact identities only.
Final disposition: ACCEPT. There is no outstanding mathematical repair, missing order, missing
size range, or unverified conjugacy inference in the stated degree-seven theorem.




                                                    6
