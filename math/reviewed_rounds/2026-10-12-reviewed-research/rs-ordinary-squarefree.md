Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: c888ff2ccdb0c650677295bd9114678020658abd30059a63807f10e2475ba2d2

---

Ordinary Rogers Szego squarefreeness independent review


                                 ACCEPT 11 October 2026 UTC


Decision. ACCEPT the final sealed candidate for the precise scope below. The uniform large-order
theorem, separate endpoint theorem, and twelve all-order modular certificates are valid. The review
independently reconstructs the finite certificates, checks the analytic argument and primitive-conjugate
transfer, and finds no mathematical repair necessary. Historical priority is not assessed.


1 Accepted scope and retained boundary

Let 𝑘 be any characteristic-zero field, let 𝑞 ∈ 𝑘 have primitive odd order 𝑑, and let 𝑏 = 2𝑚 + 1 < 𝑑.
Define
                            𝑏
                               𝑏 𝑗
               𝐻𝑏 (𝑧; 𝑞) =          𝑧 = (𝑧 + 1)𝑈 (𝑧; 𝑞),   𝑈 (𝑧; 𝑞) = 𝑧 𝑚 𝑃𝑚 (𝑧 + 𝑧 −1 ; 𝑞).
                           𝑗=0
                               𝑗  𝑞

The following statements are accepted:

  1. For every odd 𝑏 ≥ 3 and odd 𝑑 ≥ 4𝑏2 , Disc𝑧 𝑈 ≠ 0.

  2. For every odd 1 ≤ 𝑏 ≤ 25 and every odd 𝑑 > 𝑏, Disc𝑧 𝑈 ≠ 0; 𝑏 = 1 is immediate.

  3. Separately, 𝑃𝑚 (2; 𝑞) ≠ 0 for odd 𝑑 > 6(𝑏 − 1) in the stated primitive domain.

  4. The reciprocal-gcd modular criterion is valid. The stronger proposed bound that every modular
     gcd root has order at most 𝑚 fails at 𝑚 = 12, by an exact order-17 factor. This does not contradict
     statements 1--2.

  5. For 𝑚 ≥ 3, an aﬀine spectral change and diagonal similarity cannot make the original residual
     tridiagonal matrix Hermitian. This obstruction has exactly that limited scope.

Still open here. General ordinary residual squarefreeness remains unproved for odd 𝑏 ≥ 27 and odd
𝑏 < 𝑑 < 4𝑏2 , apart from separately proved instances. The endpoint result alone does not remove the
ordinary discriminant factor. The higher-degree overlap-discriminant intermediate strip is not closed
by this review.
Frozen target. The reviewed candidate ZIP has SHA-256

                9c67c388531ead34fb7cbca3245998b58afc2dee0e01adc3297e8e3ffb20d6f5

Its size is 3,991,513 bytes. Every entry in its manifest was independently hash-checked, and the ZIP
passed its CRC check. Exact source pins are recorded in SOURCE_PINS.json. No candidate or prede-
cessor program was executed or imported.


                                                   1

2 Normalization and the analytic proof

The finite Euler product gives the Gaussian coeﬀicients and their reciprocity. Their degree recurrence
is
                                 𝐻𝑛+1 = (1 + 𝑧)𝐻𝑛 − (1 − 𝑞 𝑛 )𝑧𝐻𝑛−1 .
Define 𝑅0 = 1, 𝑅1 = 𝑥, and 𝑅𝑛+1 = 𝑥𝑅𝑛 − (1 − 𝑞 𝑛 )𝑅𝑛−1 . Substitution 𝑥 = 𝑤 + 𝑤−1 gives

                 𝑅𝑛 (𝑤 + 𝑤−1 ; 𝑞) = 𝑤−𝑛 𝐻𝑛 (𝑤2 ; 𝑞),                            𝑅2𝑚+1 (𝑥; 𝑞) = 𝑥𝑃𝑚 (𝑥2 − 2; 𝑞).           (1)

The second equality is a polynomial identity: 𝑤−2𝑚 𝑈 (𝑤2 ) = 𝑃𝑚 (𝑤2 + 𝑤−2 ). Eliminating the even-
indexed 𝑅𝑛 gives precisely

                        𝑃𝑗 = (𝑡 + 𝑞 2𝑗−1 + 𝑞 2𝑗 )𝑃𝑗−1 − (1 − 𝑞 2𝑗−1 )(1 − 𝑞 2𝑗−2 )𝑃𝑗−2 ,

with 𝑃0 = 1 and 𝑃1 = 𝑡 + 𝑞 + 𝑞 2 . Thus neither a factor of two nor a change of Hermite normalization
is hidden.
Choose only for the metric argument 𝑞 = 𝑒2𝜋𝑖/𝑑 , and 𝑠2 = 1 − 𝑞 ≠ 0. The scaled monic family 𝑠−𝑛 𝑅𝑛 (𝑠𝑦)
is the characteristic-polynomial family of the complex symmetric tridiagonal 𝑇𝑏 with zero diagonal and
off-diagonal 𝑟𝑗 , where
                                                                  𝑗−1
                                               𝑟𝑗2 = [𝑗]𝑞 =              𝑞ℎ ,     ℜ𝑟𝑗 ≥ 0.
                                                                  ℎ=0
                                                    √
The real symmetric comparison 𝐽𝑏 has off-diagonal 𝑗 and characteristic polynomial He𝑏 . Its eigenvalues
are simple: irreducible tridiagonality bounds each eigenspace by one dimension, and real symmetry gives
diagonalizability.
                                                                            ″        ′
Spacing. The probabilists' differential equation is He𝑏 −𝑥 He𝑏 +𝑏 He𝑏 = 0, consistent with DLMF Table
                                                                                 2
18.9.1 and Table 18.8.1, row 14, directly checked for this review. Hence 𝑢 = 𝑒−𝑥 /4 He𝑏 satisfies

                                                   𝑢″ + (𝑏 + 1/2 − 𝑥2 /4)𝑢 = 0.

On any consecutive-zero interval [𝑎, 𝑐], integration by parts and the Dirichlet Poincare inequality give
                                𝑐              𝑐                  𝑐                                           𝑐
                    𝜋2
                                    𝑢2 ≤           (𝑢′ )2 =           (𝑏 + 1/2 − 𝑥2 /4)𝑢2 ≤ (𝑏 + 1/2)             𝑢2 .
                 (𝑐 − 𝑎)2   𝑎              𝑎                  𝑎                                           𝑎

Thus the minimum separation is at least 𝛿𝑏 = 𝜋/                         𝑏 + 1/2. In particular the candidate uses the correct
probabilists' scale, not the physicists' scale.




                                                                        2

3 Norm bounds multiplicity and field transfer

For 𝑗 ≥ 2, telescoping and |𝑞 − 1| < 2𝜋/𝑑 imply

                                           |[𝑗]𝑞 − 𝑗| < 𝜋𝑗(𝑗 − 1)/𝑑.
                       √ 2                 √
Since ℜ𝑟𝑗 ≥ 0, |𝑟𝑗 +    𝑗| = |𝑟𝑗 |2 + 𝑗 + 2 𝑗ℜ𝑟𝑗 ≥ 𝑗. Consequently
                                                                                    √
                 |𝑟𝑗 −    𝑗| < 𝜋(𝑗 − 1)    𝑗/𝑑,        ‖𝑇𝑏 − 𝐽𝑏 ‖2 ≤ 𝜀𝑏 ∶= 2𝜋(𝑏 − 2) 𝑏 − 1/𝑑.

The 𝑗 = 1 entry is exactly 1. The matrix norm bound follows from equal row/column absolute-sum
bounds for the symmetric error matrix; it does not assume that 𝑇𝑏 is normal.
For 𝑑 ≥ 4𝑏2 , 𝜀𝑏 < 𝛿𝑏 /2, because

                    𝑏4 − (𝑏 − 1)(𝑏 − 2)2 (𝑏 + 1/2) = (9𝑏3 − 11𝑏2 + 4)/2 > 0          (𝑏 ≥ 3).

For 0 ≤ 𝑎 ≤ 1, normality of 𝐽𝑏 , its resolvent norm, and the Neumann series put every eigenvalue of
𝐽𝑏 +𝑎(𝑇𝑏 −𝐽𝑏 ) within 𝜀𝑏 of a zero of He𝑏 . Choose circles with common radius strictly between 𝜀𝑏 and 𝛿𝑏 /2.
These are disjoint, their boundaries contain no eigenvalue throughout the homotopy, and each initially
contains exactly one eigenvalue counted algebraically. The argument principle preserves this count.
Therefore 𝑇𝑏 , and then 𝑅𝑏 , has only simple roots. This verifies the necessary algebraic-multiplicity step
beyond spectral inclusion.
By (1), 𝑃𝑚 (−2) ≠ 0, since otherwise zero is a multiple root of 𝑅𝑏 ; every repeated root of 𝑃𝑚 would also
give a repeated root of 𝑅𝑏 . Thus Disc 𝑃𝑚 ≠ 0. To handle the other endpoint separately, let 𝑆𝑏 have
off-diagonal squares 1 − 𝑞 𝑗 . For 𝑑 > 6(𝑏 − 1),

                       |1 − 𝑞 𝑗 | = 2 sin(𝜋𝑗/𝑑) < 1,         ‖𝑆𝑏 ‖2 ≤ 2 max   |1 − 𝑞 𝑗 | < 2.
                                                                      1≤𝑗<𝑏


Hence 2 is not an eigenvalue, so 𝑅𝑏 (2) = 2𝑃𝑚 (2) ≠ 0. The 𝑏 = 1 endpoint is immediate. Also
4𝑏2 > 6(𝑏 − 1) for 𝑏 ≥ 3.
If 𝑃𝑚 (𝑡) = ∏𝑖 (𝑡− 𝑡𝑖 ), then 𝑈 = ∏𝑖 (𝑧2 −𝑡𝑖 𝑧 + 1). Taking quadratic discriminants and pairwise resultants
gives the polynomial identity

                                    Disc𝑧 𝑈 = 𝑃𝑚 (2)𝑃𝑚 (−2) Disc𝑡 (𝑃𝑚 )2 .                              (2)

This proves the large-order theorem. All quantities in (1)--(2) lie in ℤ[𝑞]. Nonzero values at the principal
primitive root remain nonzero under every cyclotomic automorphism. Finally the map ℚ(𝜁𝑑 ) → 𝑘,
𝜁𝑑 ↦ 𝑞, is injective. No metric estimate is asserted in another embedding, and no embedding of all of
𝑘 into ℂ is needed.




                                                         3

4 The exact modular implication
                                                                          ∗
Put 𝐶𝑚 = 𝑃𝑚 (2) Disc 𝑃𝑚 ∈ ℤ[𝑞], 𝐹𝑚 = 𝐶𝑚 ≠ 0 in 𝔽2 [𝑞], and 𝐺𝑚 = gcd(𝐹𝑚 , 𝐹𝑚 ), where the reverse
uses the actual degree of 𝐹𝑚 .
If an odd 𝑑 > 𝑏 satisfied Φ𝑑 ∣ 𝐶𝑚 , monic division over ℤ[𝑞] would give Φ𝑑 ∣ 𝐹𝑚 . The factor Φ𝑑 has
                                                               ∗
constant coeﬀicient one and is reciprocal, so it also divides 𝐹𝑚 , even if the degree of 𝐶𝑚 dropped modulo
                                                     𝑑
two. Thus it divides 𝐺𝑚 . In characteristic two, 𝑞 − 1 is separable for odd 𝑑. Reducing its cyclotomic
factorization and inducting over divisors shows that every root of Φ𝑑 has exact order 𝑑. A complete
factorization of 𝐺𝑚 whose roots all have order at most 𝑏 therefore excludes this divisibility for every
odd 𝑑 > 𝑏, with no order-search cutoff.
Ordinary discriminant in characteristic two. Write a monic polynomial 𝑝(𝑡) = 𝐴(𝑡2 ) + 𝑡𝐵(𝑡2 ).
Then 𝑝′ = 𝐵(𝑡2 ) and
                                 Disc𝑡 𝑝 = Res𝑦 (𝐴, 𝐵)2 .                                (3)
For even deg 𝑝 = 2𝑟, 𝐴 is monic. If 𝐵 has degree 𝑠 and leading coeﬀicient 𝑐, the product formula gives

                            Res𝑡 (𝑝, 𝐵(𝑡2 )) = 𝑐2𝑟              𝐴(𝛾)2 = Res𝑦 (𝐴, 𝐵)2 .
                                                     𝐵(𝛾)=0

For odd degree, 𝐵 is monic and the same product formula has no leading-factor discrepancy. Repeated
roots and exceptional coeﬀicient specializations follow by polynomial identity. Constants in the degrees
encountered here are handled directly. The sign between resultant and discriminant disappears in
characteristic two.
Independent reconstruction. The review does not reuse the author's recurrence as its sole polyno-
mial source, Bareiss determinant, or program. It expands
                                   𝑏−1                    𝑏
                                                                            𝑏 ℎ
                                         (1 + 𝑞 𝑗 𝑧) =         𝑞 ℎ(ℎ−1)/2       𝑧 ,
                                   𝑗=0                   ℎ=0
                                                                            ℎ 𝑞

removes the exact monomial shifts, divides by 𝑧 + 1, and recovers 𝑃𝑚 using 𝑧ℓ + 𝑧 −ℓ in the symmetric
Laurent basis. Over 𝔽2 [𝑞], it computes the Sylvester determinant in (3) by a division-free subset recur-
rence: assign successive rows to unused columns, summing products. Determinant signs are all positive
in characteristic two. The largest matrix is only 11 × 11.
The resulting 𝐹𝑚 = 𝑃𝑚 (0)Disc 𝑃𝑚 agrees coeﬀicient by coeﬀicient with the sealed candidate for every
1 ≤ 𝑚 ≤ 12. Reducing 𝐻𝑏 (1) directly would erase a factor two; the review separately verifies the integer
identity 𝐻𝑏 (1) = 2𝑃𝑚 (2) before reduction.




                                                          4

5 Complete certificates and the obstruction

The independent Euclidean gcds have the following degrees and complete sets of root orders. All supplied
Bezout identities, full factor products, irreducibility witnesses, and least orders were checked by fresh
bit-polynomial arithmetic.

                            𝑚     𝑏   deg 𝐹𝑚     deg 𝐺𝑚         Root orders
                             1    3        2           1        1
                             2    5       14           8        1
                             3    7       44          21        1, 3
                             4    9      100          64        1, 3
                             5   11      190          95        1, 3, 5
                             6   13      322         162        1, 3, 5
                             7   15      504         245        1, 3, 5, 7
                             8   17      744         382        1, 3, 5, 7
                             9   19     1050         503        1, 3, 5, 7, 9
                            10   21     1430         714        1, 3, 5, 7, 9
                            11   23     1892         863        1, 3, 5, 7, 9, 11
                            12   25     2444        1224        1, 3, 5, 7, 9, 11, 17

Every listed order is at most 𝑏. To complete (2), the accepted negative-endpoint lemma was also
                        ′
rechecked: with 𝑔𝑚 = 𝐻2𝑚+1  (−1),
                                                           𝑚
                                                                (𝑞; 𝑞 2 )𝑗
                                      𝑔𝑚 = (𝑞 2 ; 𝑞 2 )𝑚                     .
                                                           𝑗=0
                                                               (𝑞 2 ; 𝑞 2 )𝑗

For 𝑞 = 𝑒2𝑖𝑣 , 𝑣 = 𝜋/𝑑, the 𝑗th ratio is 𝑎𝑗 𝑒−𝑖𝑗𝑣 with 𝑎𝑗 > 0. All denominators are nonzero, and
0 ≤ 𝑗𝑣 < 𝜋/2 because 𝑑 > 2𝑚 + 1. The sum has positive real part, so 𝑔𝑚 ≠ 0; conjugacy then covers
all primitive roots. Since 𝑃𝑚 (−2) = (−1)𝑚 𝑔𝑚 , (2) gives the all-order residual theorem for every odd
𝑏 ≤ 25.
At 𝑚 = 12 the irreducible polynomial

                                   𝑓 = 𝑞8 + 𝑞7 + 𝑞6 + 𝑞4 + 𝑞2 + 𝑞 + 1

has exact order 17 and occurs in 𝐺12 with multiplicity exactly two. The review additionally verifies

                                       gcd(𝐺12 , Φ17 ) = 𝑓 ≠ Φ17 .

Thus the stronger bound by 𝑚 really fails. This is not a characteristic-zero cyclotomic divisor, and
17 < 25 leaves the accepted 𝑏 = 25 conclusion intact. No general bound by 𝑏 is inferred from the table.
Gauge obstruction. The original residual matrix has diagonal 𝑎𝑗 = −(1+𝑞)𝑞 2𝑗−1 . Diagonal similarity
preserves these entries. Any complex aﬀine change that sends all three to real numbers would make
their difference ratio real, whereas

                                      (𝑎3 − 𝑎2 )/(𝑎2 − 𝑎1 ) = 𝑞 2 ∉ ℝ

for primitive odd 𝑑 > 2𝑚 + 1 ≥ 7. This excludes only the stated aﬀine and diagonal route, not
another representation or arbitrary similarity. Likewise an ordinary repeated-root polynomial (𝑧 − 1)2
has Res(𝑓(𝑧), 𝑓(𝑞𝑧)) = (𝑞 − 1)4 ≠ 0; a nonzero 𝑞-discriminant does not settle ordinary simplicity.

                                                      5

6 Evidence integration and final disposition

Exact controls. All 852 independent checks pass. They include the complete twelve-row recon-
struction above, polynomial equality with the candidate, all Bezout and factorization witnesses, exact
multiplicative orders, and the order-17 multiplicity check. Further integer controls cover:

  • finite Euler products, trace normalization, 𝑅2𝑚+1 = 𝑥𝑃𝑚 (𝑥2 − 2), the signed negative endpoint
    and 𝐻𝑏 (1) = 2𝑃𝑚 (2) for 1 ≤ 𝑚 ≤ 5;

  • the ordinary reciprocal discriminant identity for 1 ≤ 𝑚 ≤ 3;

  • direct integer discriminants reduced modulo two against the independent subset determinant for
    1 ≤ 𝑚 ≤ 5;

  • the exact all-𝑏 cutoff polynomial identity and probabilists' Hermite differential equations for de-
    grees 1 through 12.

These controls supplement the written proofs; no finite numerical or algebraic test is treated as an
infinite theorem. The independently authored program uses Python and SymPy for the extra integer
controls. Its modular determinant and gcd arithmetic use only integers and exact bit operations.
Reproduction. Run python independent_review_controls.py from the review package. The only
predecessor input read by this program is the pinned JSON certificate data. The program does not
execute or import any candidate or original uploaded program. INDEPENDENT_CONTROLS.json contains
all recovered polynomial bit masks, determinant outputs, complete verified factors and individual check
descriptions. Bit 𝑗 represents the coeﬀicient of 𝑞 𝑗 in 𝔽2 [𝑞].
Cumulative scope. The earlier accepted general-guards review supplies all-odd separation and non-
reality, plus overlap-discriminant nonvanishing for 𝑏 < 𝑑 ≤ 2𝑏 + 1 or 𝑑 ≥ 11(𝑏 + 1). The accepted
degree-seven review preserves its all-order low-degree closure. Because 4𝑏2 ≥ 11(𝑏 + 1) for 𝑏 ≥ 5, the
new analytic region closes all Section 3.2 guards there, with the accepted low-degree cases covering
𝑏 = 1, 3. For odd 9 ≤ 𝑏 ≤ 25, ordinary residual squarefreeness is now all-order, while the separate
higher-degree overlap guard remains in its previously open strip. No all-𝐴 conclusion is made for an
instance where that overlap guard is still open.
Source integrity and audit limits. The candidate ZIP, PDF, TeX and all manifest entries were
hash-verified without alteration. Copies of the candidate source, its certificate JSON and the two
accepted review sources are included with exact source pins. Both DLMF normalization tables were
directly inspected on 11 October 2026. No broader primary-source priority audit was attempted. The
candidate's seven rendered pages were inspected; the review PDF is separately rendered and checked
before sealing.
Final disposition. ACCEPT without required mathematical correction. The scope is characteristic
zero, primitive odd order, 𝑏 < 𝑑, and precisely the ranges stated in Section 1. Even order, positive
characteristic, nonprimitive specializations, general higher-degree small-order squarefreeness, and a full
higher-degree overlap closure are outside this acceptance. The seal identifies the reviewed bytes and
reproducible evidence; it is not a historical-novelty determination. No manuscript, ranking, external
document or repository was modified by this review.




                                                    6
