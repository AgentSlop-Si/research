Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: a0cc8f5ad2b37505e98649d8b86d02db04386bd243ae775f56852317eb6dd89e

---

Independent review of degree nine Rogers Szego overlap
ACCEPT 11 October 2026 UTC

Decision. ACCEPT the final frozen candidate for two precise results: all-order, all-size overlap nonvan-
ishing in degree nine, and the improved general suﬀicient tail 𝑑 ≥ 15(𝑏+1)/2. All fifteen finite certificates
were reconstructed with a different exact rational method. No mathematical repair is required. Ordi-
nary residual squarefreeness remains a separately imported theorem; the general higher-degree gaps
remain open.


1 Exact accepted scope

In characteristic zero let 𝑞 have exact odd order 𝑑, and let 𝑏 = 2𝑚 + 1 < 𝑑. Write
                                                    𝑏
                                                       𝑏 𝑗
                             𝐻𝑏 (𝑧; 𝑞) =                   𝑧 = (𝑧 + 1)𝑈 (𝑧),       𝑔 = 𝑈 (−1),
                                                   𝑗=0
                                                       𝑗 𝑞

                            (𝑞; 𝑞)𝑏                      𝑑𝑊
               𝑊 =                             ,    𝜏=      ,   𝐽𝐴+1 (𝑥; 𝜏 ) = 𝑥 He𝐴 (𝑥) − 𝐴𝜏 He𝐴−1 (𝑥).
                      (𝑞 2 ; 𝑞 2 )   (𝑑+𝑏)/2              𝑔
Here He𝑛 is the monic probabilists' Hermite polynomial and 𝐴 ≥ 1 is an integer. The review accepts

                      𝑏 = 9, 𝑑 ≥ 11 odd                  ⟹      Disc𝑥 𝐽𝐴+1 ≠ 0     for every 𝐴 ≥ 1,

and, independently, for every odd 𝑏 ≥ 1,
                                 15
                          𝑑≥        (𝑏 + 1)             ⟹    Disc𝑥 𝐽𝐴+1 ≠ 0      for every 𝐴 ≥ 1.
                                  2
The accepted general-guards source supplies 𝑔 ≠ 0, Res𝑧 (1+𝑧 𝑑 , 𝑈 ) ≠ 0, nonreality of 𝜏 in every primitive
complex embedding, and overlap nonvanishing in 𝑏 < 𝑑 ≤ 2𝑏 + 1. The separately accepted ordinary-
squarefreeness source supplies Disc𝑧 𝑈 ≠ 0 for every odd 𝑏 ≤ 25 and all odd 𝑑 > 𝑏. Thus all four guards
are discharged in degree nine. The overlap argument alone does not establish ordinary squarefreeness
or absence of arbitrary unit-circle zeros of 𝑈 .


2 Why the all size implication is valid

For 𝐴 = 1, 2, the discriminants are 4𝜏 and 4(1 + 2𝜏 )3 ; their exceptional parameters are real. A repeated
zero root for general 𝐴 also requires a real parameter: 𝜏 = 0 for odd 𝐴 or 𝜏 = −1/𝐴 for even 𝐴.
For a nonzero repeated root, the Hermite recurrence excludes simultaneous zeros of consecutive factors.
Differentiation gives
                                        𝜏 (𝐴𝜏 + 1)                   𝐴+1
                              𝑦 = 𝑥2 =             = 𝐴𝜏 + (𝐴 + 1) +         .
                                           𝜏 −1                      𝜏 −1
Put 𝐴 + 1 = 2𝑟 + 𝑠, 𝑠 ∈ {0, 1} and 𝛼 = 𝑠 − 1/2. The parity characteristic matrix has diagonal
4𝑗 + 2𝛼 + 2, 0 ≤ 𝑗 < 𝑟, and nonzero real off-diagonal entries 2 𝑗(𝑗 + 𝛼), 1 ≤ 𝑗 < 𝑟. Its last diagonal has
the additional shift 𝐴(𝜏 − 1). The finite factorial formula for He𝑛 , or the monic Laguerre recurrence,
proves this identity for every 𝐴, not just the checked sizes.



                                                                  1

The matrix is complex symmetric and irreducible tridiagonal. Its eigenspace is one-dimensional, its
last eigenvector coordinate is nonzero, and a repeated eigenvalue admits a Jordan chain. Therefore its
eigenvector 𝑢 satisfies 𝑢𝑇 𝑢 = 0. The bilinear identity implies

                                                         |𝑢𝑟 |2  1
                                              0 < 𝑡 ∶=        2
                                                                ≤ .
                                                         ‖𝑢‖     2

The separate Hermitian inner product gives Im 𝑦 = 𝐴 Im 𝜏 𝑡. Since 𝜏 is nonreal, division is valid. With
𝜌 = |𝜏 − 1|2 , the preceding rational expression for 𝑦 gives

                                    𝐴+1                1       2  8
                        𝐴𝑡 = 𝐴 −        ,         1+     <𝜌 ≤2+ ≤                        (𝐴 ≥ 3).
                                     𝜌                 𝐴       𝐴  3

The inner endpoint is strictly excluded; the outer endpoint is included. Thus any rigorous 𝜌 > 8/3
witness excludes every 𝐴 ≥ 3 at once.
For fixed 𝐴, 𝐷𝐴 (𝑇 ) = Disc𝑥 𝐽𝐴+1 (𝑥; 𝑇 ) ∈ ℚ[𝑇 ]. Vanishing at one cyclotomic embedding would imply
vanishing at all embeddings. A witness outside the critical annulus at any actual primitive root there-
fore proves algebraic nonvanishing. The metric inequality itself is not transported. Nonreality transfers
separately because cyclotomic automorphisms commute with complex conjugation. Finally, any prim-
itive order-𝑑 root in a characteristic-zero field induces an injective map from ℚ(𝜁𝑑 ); an embedding of
the whole base field into ℂ is unnecessary.


3 Independent finite certificates

The fresh checker constructs 𝐻9 by the Gaussian Pascal recurrence, rather than the candidate's finite
Euler product. It obtains exactly

                  𝑔 = (𝑞 − 1)4 (𝑞 2 + 𝑞 + 1)𝐾(𝑞),      (𝑞 2 ; 𝑞 2 )4 = (𝑞 − 1)4 (𝑞 2 + 𝑞 + 1)𝑁 (𝑞),

where the ascending coeﬀicients of 𝐾 are

                              (5, 11, 17, 25, 32, 36, 39, 39, 34, 28, 22, 14, 8, 4, 1),

and 𝑁 = (𝑞 + 1)4 (𝑞 2 + 1)2 (𝑞 4 + 1)(𝑞 2 − 𝑞 + 1). Therefore

                                         𝑑𝑁 (𝑞)
                                  𝜏=             ,           𝐸 = (𝑞 2 ; 𝑞 2 )(𝑑−1)/2 .
                                        𝐸(𝑞)𝐾(𝑞)

The checker uses 256-bit outward dyadic intervals, the different identity

                                     𝜋 = 4 arctan(1/2) + arctan(1/3) ,

and 180 alternating terms per arctangent. The tangent addition is exactly 1 and the angle lies in
(0, 𝜋/2), proving the identity. At each rational angle midpoint it evaluates exact rational cosine and sine
polynomials of degrees 120 and 121. Each error radius is the first omitted alternating-term magnitude
plus the angle interval radius, using | sin′ |, | cos′ | ≤ 1.
Independent binary powers and a direct sum of powers reconstruct 𝐸, 𝐾, 𝑁 , 𝜏 , 𝜌. A second route
computes 𝑆ℎ /𝑆4 from its original prefix definition. Every reconstructed root, 𝐸, 𝐾, 𝑁 , 𝜏 and 𝜌 enclosure
lies inside the candidate's recorded 192-bit endpoints. This proves the frozen certificate endpoints
themselves contain the exact quantities. No candidate program is run or imported.


                                                         2

            Order 𝑑    Primitive index 𝑘    Lower bound for 1000𝜌      Upper bound for 1000𝜌
                  21                   8             5962                       5963
                  23                   7             3022                       3023
                  25                   2             3080                       3081
                  27                   8             4116                       4117
                  29                  11             10896                      10897
                  31                   3             6062                       6063
                  33                  10             7591                       7592
                  35                  11             5186                       5187
                  37                  14             12559                      12560
                  39                   4             8805                       8806
                  41                   4             10510                      10511
                  43                  13             12177                      12178
                  45                  17             13087                      13088
                  47                  18             14020                      14021
                  49                   4             13177                      13178

All intervals are closed rational enclosures, not rounded numerical observations. Each gcd(𝑘, 𝑑) = 1,
every lower endpoint exceeds 3000, and both normalization routes give 𝜌 > 3 > 8/3. These fifteen
orders are exactly the remaining finite strip 21 ≤ 𝑑 ≤ 49. No finite scan over 𝐴 is used as proof.


4 Audit of the degree nine infinite tail

For odd 𝑑 ≥ 51, put 𝑞 = 𝑒2𝑖𝑣 , 𝑣 = 𝜋/𝑑. The exact rational inequality

                                     0 < 𝑣 ≤ 𝜋/51 < 22/357 < 1/16

is strict even at 𝑑 = 51. Positivity of every 𝐾 coeﬀicient gives |𝐾(𝑞)| ≤ 𝐾(1) = 315. Factoring 𝑁 gives
positive cosine factors and

                        |𝑁 (𝑞)| = 128 cos4 𝑣 cos2 (2𝑣) cos(4𝑣)(2 cos(2𝑣) − 1) > 119.

Indeed, cos 𝑡 ≥ 1 − 𝑡2 /2 gives respective strict lower bounds 511/512, 127/128, 31/32 and 63/64. The
difference between their product and 119/128 is
                                         4083845960015521
                                                           > 0.
                                       2305843009213693952
Since the even residues and their negatives partition the nonzero residues modulo odd 𝑑, |𝐸|2 = 𝑑,
including composite orders. Thus
                                  √                                   √         2
                                17 𝑑                         2      17 𝑑
                         |𝜏 | >      > 1,       𝜌 ≥ (|𝜏 | − 1) >         −1         .
                                 45                                  45

The last expression is increasing in √𝑑 ≥ 51. At 51, comparison with 8/3 reduces to comparing the
positive quantities 3788/675 and 34 51/45. Their squared difference is exactly 1083844/455625 > 0.
Squaring is legitimate, and 𝜌 > 8/3 follows.
The imported range 𝑑 = 11, 13, 15, 17, 19, the fifteen certificates, and the proved tail 𝑑 ≥ 51 exhaust all
odd 𝑑 > 9. The all-𝐴 degree-nine conclusion has no missing order or size boundary.

                                                     3

5 Audit of the sharper general bound

Let 𝑑 ≥ 15(𝑏 + 1)/2 = 15(𝑚 + 1), ℎ = (𝑑 − 1)/2 and 𝑣 = 𝜋/𝑑. Use the accepted prefix normalization
                                                 𝑗                                     𝑗
                   (𝑞; 𝑞 2 )𝑗                                     𝑆                       sin((2𝑟 − 1)𝑣)
              𝑠𝑗 = 2 2 = 𝑎𝑗 𝑒−𝑖𝑗𝑣 ,      𝑆𝑗 =         𝑠𝑟 ,     𝜏 = ℎ,          𝑎𝑗 =                      .
                  (𝑞 ; 𝑞 )𝑗                     𝑟=0
                                                                  𝑆𝑚                  𝑟=1
                                                                                             sin(2𝑟𝑣)

Then (2𝑚 + 1)𝑣 < 2𝜋/15, including equality in the hypothesis on 𝑑. The exact trigonometric identity

                          sin2 (2𝑟𝑣) − sin((2𝑟 − 1)𝑣) sin((2𝑟 + 1)𝑣) = sin2 𝑣 > 0

gives, by telescoping, 𝑎2𝑗 ≤ sin 𝑣/ sin((2𝑗 + 1)𝑣) for 0 ≤ 𝑗 ≤ 𝑚, with equality only at 𝑗 = 0. All divided
factors are positive. For 0 < 𝑢 < 2𝜋/15, using 𝜋2 < 10,

                                                                  131
                                        sin 𝑢 ≥ 𝑢 − 𝑢3 /6 >           𝑢.
                                                                  135
Together with sin 𝑣 < 𝑣, this yields 𝑎2𝑗 < 135/[131(2𝑗 + 1)], strictly even at 𝑗 = 0. Convexity and
integrability of 𝑢−1/2 give

                                      135 𝑚                               270
                            |𝑆𝑚 | <           (𝑗 + 1/2)−1/2 ≤                 (𝑚 + 1).
                                      262 𝑗=0                             131

The midpoint-integral comparison is valid also on the improper first interval [0, 1]. Using |𝑆ℎ |2 = 𝑑 now
gives
                                                131𝑑       131
                                     |𝜏 |2 >             ≥     .
                                             270(𝑚 + 1)     18
Since 101/18 > 0 and (101/18)2 − 4(131/18) = 769/324 > 0,
                                                                           2    8
                                 𝜌 ≥ (|𝜏 | − 1)2 >           131/18 − 1        > .
                                                                                3
Every strict endpoint and the 𝑚 = 0 case are valid. Combined with nonreality for the small sizes, this
proves the stated general all-𝐴 tail.




                                                        4

6 Integration guidance and source identity

The full-family overlap closures now include odd 𝑏 = 1, 3, 5, 7, 9. The general intermediate overlap strip
remains open for odd 𝑏 ≥ 11 at
                                                      15
                                        2𝑏 + 1 < 𝑑 < (𝑏 + 1),
                                                       2
except separately proved instances. Keep ordinary residual squarefreeness separate: its accepted ranges
are all odd 𝑏 ≤ 25 with odd 𝑑 > 𝑏, and all odd 𝑏 ≥ 3 with odd 𝑑 ≥ 4𝑏2 . The remaining ordinary residual
domain is odd 𝑏 ≥ 27, 𝑏 < 𝑑 < 4𝑏2 , except separately proved instances. No global higher-degree closure
is authorized by this review.
The candidate ZIP has 24 verified payload entries and a clean CRC check. The included accepted
general-guards, degree-seven, and ordinary-squarefreeness sources match their original bytes. Frozen
identities are:

  • Candidate ZIP SHA-256:
    70a2df0ecf344d04f0e061485ce6e5df9d4cafef363f899b340c88f4c4339196.

  • Candidate proof SHA-256:
    17e9118e14a01fda743368dc95e4401948e289719940838dbbd12cc7d8efedf3.

  • Candidate exact interval certificate SHA-256:
    3c3764dfec9b75cfaf5d51123ab9a5c6703b97d069f557b4a88c38f240cef174.

All 337 fresh independent exact checks pass, including rational tail comparisons, candidate endpoint
containment, normalization controls, primitive-index checks and mutation controls. Finite Hermite
checks corroborate the all-𝐴 proof; they do not replace it. Historical novelty, positive characteristic,
even orders, nonprimitive roots, 𝐴 = 0, and quantitative conditioning are not certified. No external
document, Sheet, manuscript, repository, ranking, permission or access was changed.




                                                    5
