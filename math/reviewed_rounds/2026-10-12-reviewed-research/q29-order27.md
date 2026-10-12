Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: f7b8706baf5021c4a89bfc150b5915fde752cba1df8863c453fb19b0747f631d

---

# Independent acceptance: intrinsic order-27 augmented support

11 October 2026 UTC. Verdict: **ACCEPT, fixed lower base 27 only.** No external writes were made. Original uploaded and historical programs remained inert. Neither candidate Python program was imported or executed by this reviewer.

## Accepted result and scope

For the intrinsic cyclotomic ring O=Z[q]/(q^18+q^9+1), using its full canonical basis 1,q,...,q^17, the exact reduced-coordinate content is

    c_27^+ = 3^68 = 278128389443693511257285776231761.

The supplied accepted augmented overlap theorem therefore gives

    H_((27p-1)/2)(z; zeta_(27p)) is squarefree over characteristic zero

for every prime p congruent to 1 modulo 4 and every primitive 27p-th root. Here H_n(z;q)=sum_(k=0)^n [n choose k]_q z^k is the Rogers–Szegő polynomial, with Gaussian binomial coefficients, and discriminants always use the ordinary z derivative. There is no exceptional prime within this congruence class: p cannot equal 3, so p does not divide 27 or 3^68.

This certifies one fixed repeated-prime lower base. The adjoined prime remains unramified. It does not prove transfer when p divides s, a uniform result over s=3^(2e+1), general augmented support, arbitrary composite squarefreeness, an improved scalar-bank minimum, or historical priority. General Q29 remains open/partial. The root -1 remains present, simple, and resonant for the scalar-bank application.

## Frozen candidate and source pins

The candidate archive is Q29_Order27_Augmented_Support_CANDIDATE_2026-10-11.zip, SHA-256

    90ed513376083f39a07eb2b8d8831a69c29596f880ac86dec7f5b909edc1cfc9.

The review checked this archive hash, equality of every archive member with the frozen candidate directory, the manifest hash and every member hash. A complete unchanged candidate snapshot is under candidate/ in this reviewer packet; CANDIDATE_SEAL.json preserves the author seal.

Important candidate hashes:

- SHA256SUMS.json: 6717568c8829200cc07fc43375b7789a7f1d2deed73fb78ee988c999a458d94c
- EXACT_CERTIFICATE.json: 6239129b102be5f0f014e3df57fbeaa66b24b514e2563144ba70ea391395c913
- CONTROL_CERTIFICATE.json: 64b42dedd94ad4543d8c5c0cb4f25784f89e657f03ea6f80027cb61bf204441c
- REPORT.md: 7c189c4fbe9b4c2dbfbff32d9c52db1471d97ff89a6718c9e0c5a04ea4226f31

The source theorem is candidate/sources/01_COMPOSITE_GUARD_EXTENSION.md, Section 2, SHA-256 ef48feecd50dfcccba0c8fc7345c256d2cffb2800d5ae5bec63019a541db8b97. It is also reproduced with its dependencies in candidate/sources/03_manuscript.md, SHA-256 155434da08c53789edce92664c825e72c2ef7641ce405a96ec8fed4b1e0a641b: Section 1 defines H and ordinary discriminants; Theorem 3.2 supplies the one-simple-shared-root coefficient; Theorem 6.1 is the parity-complete finite-characteristic pairing lemma; Lemma 7.1 and Theorem 7.2 give same-component selection and the unramified bridge. This review accepts the earlier theorem as the supplied accepted dependency, checks its precise statement and applicability, and does not advertise a new independent proof of the entire preceding manuscript.

All six source bindings were hashed and matched their original local source bytes during review. Remaining contextual pins, including the accepted order-75 review and the existing-row snapshot, are fully preserved in candidate/SOURCE_BINDING.json. External historical-priority claims were not made or independently expanded.

## Definitions checked

The complete intrinsic definitions are

    b=13, r=6,
    U=H_13/(z+1), g=U(-1),
    v=product_(j=1..6)(1-q^(2j)) product_(j=0..12)(1-q^(2j+1)),
    delta=2g-v,
    D=Disc_z(U), R=Res_z(z^27+1,U),
    Gamma=DR, iota(q)=q^(-1), pair=Gamma*iota(Gamma),
    A=pair*delta, c_27^+=gcd of every canonical coordinate of A.

U is monic reciprocal of degree 12. The identity Disc(H_13)=g^2 D was checked by a separate full discriminant determinant at every reconstruction component, not only by forming the proposed product. The coefficient ring has degree 18: Phi_27(T+1) is 3-Eisenstein, checked by its integer coefficients.

INDEPENDENT_ARRAYS.json records freshly reconstructed complete H/U arrays and all ten 18-coordinate vectors. Equality with every candidate coordinate was checked, including zero coordinates and signs. No selected projection, evaluation, norm, or unreduced polynomial content was substituted for these arrays.

## Independent arithmetic method and deterministic uniqueness

The reviewer authored independent_review.py from the definitions. It constructs every Gaussian coefficient using the subset identity

    [13 choose k]_q = sum_(0<=a1<...<ak<13) q^(sum ai-k(k-1)/2).

All 8,192 subsets are enumerated; powers are reduced by q^18=-q^9-1. Synthetic division forms U and multiplication by z+1 recovers the entire H. This does not use either candidate recurrence. The integral g,v,delta vectors and the inverse identity g*iota(v)+iota(g)*v=v*iota(v) are reconstructed directly.

Each of the 19 candidate reconstruction primes, from 1000000297 through 1000006129, was certified independently by trial division through its integer square root. Distinctness, congruence 1 modulo 27, exact order of the saved root, and all 18 distinct primitive roots were checked.

For each of the 342 prime/root pairs, the reviewer computes:

1. D as the determinant of multiplication by U' in F_p[z]/U, a 12-by-12 determinant.
2. R as the determinant of multiplication by z^27+1 in the same quotient.
3. A separate full 23-by-23 Sylvester determinant for Res(U,U').
4. A separate full 39-by-39 Sylvester determinant for Res(z^27+1,U).
5. A full 25-by-25 Sylvester determinant for the ordinary discriminant of H_13.

These 1,710 prime-field determinants are independent of the candidate polynomial-Euclid resultant implementation. The discriminant signs are positive here since 12*11/2 and 13*12/2 are even; swapping degrees 27 and 12 in the resonance resultant is also even.

Rather than use the candidate Lagrange implementation, the reviewer solves an exact 18-by-18 Vandermonde system with five simultaneous right-hand sides to recover every coordinate of D,R,g,v,delta modulo each prime. All recovered columns match the candidate columns. Integer CRT then reconstructs the five full integral vectors, and arbitrary-integer multiplication in O constructs all other vectors and the involution.

The candidate uniqueness bounds are valid and were checked arithmetically. With B=2^13, at every complex primitive root the embedding bounds are

    M_D=(13B)^11(78B)^12,
    M_R=(13B)^27,
    M_g=13B, M_v=2^19, M_delta=26B+2^19.

Indeed Gaussian positivity bounds |H_k| by binomial(13,k), and synthetic division bounds each U coefficient by B. The D determinant has 11 rows from U and 12 from U', with l1 bounds 13B and 78B; Hadamard bounds its absolute value. R is the product of U evaluated at the 27 unit-modulus roots of z^27+1.

There is also a simpler stronger independent coordinate bound. At any primitive root alpha,

    Phi_27'(alpha)=9 alpha^8(2 alpha^9+1),
    |Phi_27'(alpha)|=9 sqrt(3)>9.

Each coefficient of Phi_27(T)/(T-alpha) is a sum of at most two unit-modulus terms, so its absolute value is at most 2. Summing the 18 complex Lagrange terms shows that every canonical coordinate of an integral element with embedding bound M has absolute value at most 4M. The five resulting bound bit lengths are respectively 418,453,19,22,22. The CRT modulus has 569 bits and is strictly greater than twice each bound. Thus every integer coordinate is uniquely determined, without heuristic stabilization. The candidate's more conservative maximum 553-bit bound also passes its required strict inequality. Products formed after exact reconstruction need no additional CRT bound.

The full independent results and numerical bounds are saved in INDEPENDENT_RESULTS.json. The checker uses only the Python standard library and the frozen data files; its reproduction command is python independent_review.py.

## Content and saturation

All full-vector contents agree:

- D: 3^9; R: 3^24
- g: 1; v: 3^2; delta: 1
- Gamma and iota(Gamma): 3^33 each
- pair: 3^67; A: 3^68
- Disc(H_13): 3^11

The reviewer independently takes the gcd of all 18 coordinates, checks that every A coordinate is divisible by 3^68, and verifies the exact candidate integer Bézout identity sum w_j A_j=3^68. The normalized coordinates have gcd 1. This proves absence of every additional content prime, not merely the displayed 3-adic lower bound. In particular, contents must not be multiplied mechanically: pair and A acquire extra powers after canonical reduction.

For pi=1-q, every recorded normalized quotient was verified by multiplication pi^valuation * quotient = the reconstructed element. Each final quotient has the claimed nonzero residue in O/(pi)=F_3. The valuations D174,R432,g16,v37,delta16,Gamma606,iota(Gamma)606,pair1212,A1228,Disc(H_13)206 therefore match. The identity pi*J=3, J=2(1+...+q^8)+(q^9+...+q^17), is checked directly. The candidate pi^18/3 vector multiplies back exactly; a fresh fraction-free integer 18-by-18 determinant gives its norm 1, certifying a global integral unit. These lower-ring valuations are not a ramified transfer theorem.

## Same-component, inverse and denominator controls

All 18 components over F_109 and both polynomial gcd arrays at every component were reproduced exactly. Four components fail the augmented condition; 14 pass. At q=81, inverse 35,

    D=53, R=61, g=4, v=63, delta=54,
    Gamma=72, Gamma_iota=63, A=21.

The parameters tau=43 and tau_iota=14 obey 1/tau+1/tau_iota=1 and exclude 2. The two Hermite cluster polynomials at local index 54 each have derivative gcd degree zero. Q_27=q^9-1 and Phi_27' are nonzero in this same component.

The adverse inverse control also passes: at q=21, inverse 26, D=67,R=75,delta=74 are nonzero, but Gamma_iota=A=0. At q=26 the exact derivative gcd is z^2+22z+1, while the resonance gcd remains 1. Thus checking D,R,delta at only the first root is insufficient. This is a guard-omission counterexample in characteristic 109, not a counterexample to the characteristic-zero family. It also shows why requiring every component to pass would be unnecessarily strong.

For p=5, ord_27(5)=18 is checked by all proper-divisor tests, proving Phi_27 is irreducible over F_5. The exact A vector is nonzero modulo 5 by its content. Negative controls detect changing an A coordinate, changing a D coordinate, replacing Gamma*iota(Gamma) by Gamma^2, and illegally treating 1/pi=J/3 as integral.

## Exact bridge applicability

The accepted theorem requires s=4r+3, prime p=1 modulo 4, p not dividing s, c_s^+ nonzero and p not dividing it. All hold for s=27. Since p does not divide 27, O/pO is a product of fields, and the nonzero augmented vector selects one common factor where Gamma, its inverse counterpart, and delta are all nonzero. The lower ordinary discriminants and resonance resultants are therefore nonzero in that same factor.

Because z+1 divides z^27+1, the nonzero resultants ensure both g and iota(g) are units. All exponents in v and iota(v) are strictly between 0 and 27, so their factors are units at the primitive lower roots. The independently checked integral inverse identity yields the parameter relation. Delta excludes tau=2, and the accepted parity-complete inverse-pairing lemma chooses an inverse root with nonsingular cluster polynomial.

For local index h=(p-1)/2, h<p and p does not divide 27, so P_h and the integer powers of 27 in the accepted overlap coefficient are units. Every remaining factor of that coefficient is a unit in the selected component. Its nonvanishing also verifies the characteristic-zero local guards. The accepted exact factorization is

    D_n(q)=Phi_27(q)^L E(q), E in Z[q],
    L=27h(h-1)/2+h,
    E(omega)=Q_27(omega)^L C_ov.

Q_27 is a unit because q^27-1 is squarefree modulo p. If D_n vanished at a primitive 27p-th root, irreducibility would force Phi_(27p) to divide E. But Phi_(27p)=Phi_27^(p-1) modulo p, making E vanish in every lower component, a contradiction. Division occurs integrally before reduction; no false L<p-1 restriction is introduced. Galois conjugacy gives every primitive 27p-th root.

## Scope and remaining work

The accepted fixed bases are3,7,11,15,19,23,27,75, with prior base-specific restrictions retained, including p!=5 for bases15 and75. The new augmented content is c27+=3^68 across all18 coordinates; the inherited unramified bridge gives the stated characteristic-zero27p family for primes p congruent to1 modulo4. General support and repeated-prime transfer remain open. The inverse-component counterexample is not a counterexample to the main squarefreeness objective.
