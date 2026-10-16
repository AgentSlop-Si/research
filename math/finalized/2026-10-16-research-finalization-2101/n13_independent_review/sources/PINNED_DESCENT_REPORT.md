# N13: descent criterion and a stronger pinned-cross obstruction

Date: 14 October 2026 UTC. New bounded mathematical result; independent review pending. No supplied scientific program was executed. No external service was changed.

## Result first

Let B₁(L) denote the minimum in the accepted original N=13, q=16, characteristic-53 signed-bank grammar, additionally pinning both effective cross alpha nodes to y=z=1. Every legal beta remains allowed. Then

**B₁(L)=16 if and only if L contains a copy of F_(53^5) or F_(53^6).**

In particular, over finite fields,

**B₁(F_(53^d))=16 if and only if 5 divides d or 6 divides d.**

This rules out sixteen banks in degrees 1, 2, 3 and 4 in the pinned-cross subfamily, without any Frobenius-stability assumption on the same-sign supports. It does not rule out sixteen banks over degrees 2, 3 or 4 with freely varying cross nodes. Thus the minimum extension degree in the full independently-free-cross model is still unresolved.

The accepted finite census alone did not prove this stronger pinned result. The new ingredient is a two-equation symbolic sector obstruction that forces its support parameters into the prime field over every characteristic-53 extension. The full-field claim B(L)=16 also follows whenever 6 divides d, by the newly reconstructed pinned upper construction; this is an algebraic existence proof, not a new explicit degree-six field-encoding/literal-inverse certificate.

## 1. Grammar and equality bookkeeping

A physical bank is

    (1/13) Σ_(j=0)^12 w_j
      (I−alpha S^epsilon−beta q^(epsilon delta j)T^delta)^(-1),
    Delta=1−alpha^13−beta^13 ≠ 0.

The target is the original negative unnormalized Fourier matrix. Exactly one effective alpha group is required in each cross orientation. The accepted universal lower theorem requires at least seven distinct nonzero effective alpha nodes in each same-sign orientation, and one nonzero effective cross node on each side.

Consequently, an exactly sixteen-physical-bank certificate has allocation (7,1,1,7), with exactly one bank at each of those sixteen orientation/node pairs. It has no zero-alpha bank, no repeated physical node within an orientation, no ineffective bank and no extra bank canceled by another. Each same-sign support annihilator is monic, squarefree, degree seven and has nonzero constant term.

## 2. Beta normalization is lossless at the sixteen-bank boundary

Put r=[epsilon a]_13, l=[delta b]_13, gamma=7. The accepted original-bank expansion is

    Weyl coefficient = gamma alpha^r G_(epsilon,delta)(a,b) A_b,
    A_b = beta^l/(13 Delta gamma) Σ_j w_j q^(epsilon b j).

This formula includes beta=0 and does not divide by beta. For any alpha ≠ 0 and any desired amplitude vector A over the field, choose

    beta'=1, Delta'=−alpha^13,
    w'_j=Delta' gamma Σ_(b=0)^12 A_b q^(−epsilon b j).

Character orthogonality recovers exactly A_b. Delta' is nonzero. Thus this new legal physical bank has exactly the same full matrix as the old one. At sixteen banks every alpha is nonzero, so replacing all betas by one preserves the count, target and effective supports.

Therefore beta=1 is no restriction on existence at exactly sixteen banks. This argument is not asserted for arbitrary representations containing zero-alpha banks.

## 3. What actual descent requires

Let E/F be a field extension of characteristic 53, and start with a sixteen-bank certificate over E.

- The identical raw certificate is a certificate over F precisely when every listed alpha, beta and raw weight lies in F. For finite fields inside a common algebraic closure, membership in F_(53^d) is equivalent to being fixed by x↦x^(53^d).
- If re-solving weights and replacing beta by one is allowed while retaining the same orientation/alpha support, a certificate over F exists **if and only if all sixteen alpha nodes lie in F**. Necessity is the meaning of retaining that support. For sufficiency, the complete sector matrix has coefficients in F; consistency over E implies consistency over F because matrix and augmented ranks are unchanged by scalar extension. Solve over F and use the preceding inverse-character formula. The isolated cross-sector rows force both cross banks to be effective. If any same-sign bank were ineffective, deleting it would then give a representation in the same grammar using at most fifteen physical banks, contradicting the universal lower bound.
- Equivalently, the retained two cross nodes must lie in F and both same-sign degree-seven annihilators must split into distinct nonzero linear factors over F. Merely having their coefficients in F is insufficient.
- A Frobenius-invariant unordered support only says its annihilator has base-field coefficients. A Frobenius-invariant total matrix or Frobenius-orbit sum only says the sum descends. Neither makes the individual roots legal F-valued alpha parameters. Replacing a nontrivial orbit by a trace-valued bank changes the grammar and is not descent here.

The accepted quintic certificate illustrates the distinction: its total is the prime-field Fourier matrix and its same-sign support is prime-Frobenius-stable, but five individual alpha parameters have degree five. Its support can be retained over F_(53^d) precisely when 5 divides d. F_(53^2), F_(53^3) and F_(53^4) are not subfields of the quintic field; comparisons with them use a common algebraic closure and possible different certificates, rather than literal subfield descent of K.

## 4. The accepted census: exhaustive where, incomplete where

The inert quotient file contains exactly one polynomial for every lambda in F53. Exactly 51 pass squarefree/nonzero-constant guards; all 51²=2,601 ordered guarded pairs occur exactly once. Its only passing pairs are (15,15), (15,37), (37,15), (37,37), with common splitting degrees 5,30,30,6. The earlier independent review reconstructs these checks; the fresh checker here additionally verifies this Cartesian-product bookkeeping.

The declared census fixes y=z=1 and assumes prime-Frobenius-stable support, so the annihilator coefficients and lambda are in F53. General support over F_(53^d) is invariant under the d-th Frobenius, not necessarily the prime Frobenius; its coefficients may lie anywhere in F_(53^d). A finite list of 53 parameter values does not exclude those extension parameters. Furthermore, the census does not vary the cross nodes. The accepted 52×53 forced-window census elsewhere covers all prime-field cross nodes but not extension-valued cross nodes, and does not furnish full-sector classification over extensions.

The beta restriction can be removed by §2. The non-prime-field lambda gap at y=z=1 is removed by §5 below. The arbitrary-cross-node gap is not removed.

## 5. New field-uniform support obstruction when y=z=1

Define G from the original noncommutative binomial coefficients. For omega=q^(epsilon delta),

    D(r,l)=D(r−1,l)+omega^r D(r,l−1), D(0,0)=1,
    G_(epsilon,delta)(a,b)=D([epsilon a]_13,[delta b]_13)

when the two indices sum to less than thirteen, and zero otherwise. The normalized target is f(a,b)=q^(10(a+b)^2).

For the (++) support X let H(t)=Π_(x∈X)(t−x). The six degree-seven forced windows at y=1 give a 6×8 coefficient matrix over F53. Its first six columns have rank six, so over **every** characteristic-53 extension every monic solution is

    H_lambda(t)=t^7+lambda t^6+(50+22lambda)t^5
       +(48+15lambda)t^4+(27+10lambda)t^3
       +(19+11lambda)t^2+(50+25lambda)t+(16+31lambda).

At this stage lambda may be in the extension. Rank six over F53, rather than enumeration of F53 points, proves completeness of the affine parameterization over all extensions.

Now take the full b=3 sector. The sole (−,+) amplitude is forced to be T=49 by row a=10. Let C denote the (+,−) amplitude in this sector, and put M_a=Σ_(x∈X) A_(x,3)x^a. For a=1,...,9 the full sector equations give

    M_1=−2C−8, M_2=9C−9,
    (M_3,...,M_9)=(−4,1,4,9,6,0,−6).

These equations include the previously unused cross-side coupling at a=1,2. The (−,−) block vanishes on all nine of these rows; G_(++) is nonzero there. The displayed expressions follow directly from

    M_a=[f(a,3)−49 G_(−,+)(a,3)−C G_(+,−)(a,3)]/G_(++)(a,3).

Writing H_lambda=Σ_(k=0)^7 h_k t^k, its annihilator recurrence must hold at starts a=1 and a=2. Substitution gives

    (4lambda−6) C+22lambda+15=0,
    (14lambda−15) C−8lambda−21=0.

Eliminating C by cross-multiplication, with no division by a parameter, gives

    22lambda²+22lambda+20
       =22(lambda−15)(lambda−37)=0.

Since the coefficient field is a field of characteristic 53, lambda is 15 or 37. The argument has no omitted exceptional denominator locus. Simultaneous reflection (a,b,epsilon,delta)↦(−a,−b,−epsilon,−delta) preserves the target and G identities; with y=z=1 it applies identically to the (−,−) support. Its parameter is also 15 or 37.

This proves that prime-Frobenius-stability of the supports is forced by the full sector equations in this pinned sixteen-bank case. It was not legitimate to assume that fact solely from the finite census.

## 6. Splitting fields and sufficiency

The two possible annihilators factor over F53 as follows:

    H_15=(t−22)(t−36)
         (t^5+20t^4+6t^3+45t^2+49t+34),

    H_37=(t−48)(t−17)(t^2+38t+12)
         (t^3+11t^2+47t+41).

The quintic, quadratic and cubic displayed here are irreducible. Fresh modular-power and gcd checks certify this: each degree is prime, each factor divides t^(53^degree)−t, and its gcd with t^53−t is one. Both H polynomials are squarefree and have nonzero constant term. Thus their splitting fields have degrees five and six, respectively.

Necessity now follows: a retained degree-seven support over L consists of every root of its annihilator, so L must contain the corresponding splitting field. If both signs use H_15, this is F_(53^5); if both use H_37, it is F_(53^6); a mixed pair needs their compositum F_(53^30).

For sufficiency, the fresh checker reconstructs all thirteen complete 13×16 quotient-sector systems for each of the four pairs and solves them over F53. All 52 systems are consistent. At distinct support roots, the root-column matrix equals R_H V_H, with V_H an invertible Vandermonde matrix. Hence each quotient solution gives actual root amplitudes in the splitting field. Set beta=1 and recover all raw weights by §2. All alpha values are nonzero, so every branch denominator is nonzero. The full 169 coefficient identities imply the original matrix identity. The isolated cross-sector rows force both cross banks to be effective. If a same-sign bank were ineffective, deleting it would preserve those cross-singleton conditions and contradict the accepted universal sixteen lower bound.

This is an original-bank existence proof, with a field-independent raw-weight formula. It does not replace banks by traces or quotient operators. An explicit degree-six modulus/coordinate table and 208 separately recorded branch-inverse matrices were not constructed in this bounded task; the algebraic argument does not claim that such a new literal certificate was replayed.

## 7. What remains missing for the full degree-2/3/4 exclusion

An arbitrary sixteen-bank certificate has nonzero independent y,z in its coefficient field. Nothing proved here normalizes those two nodes to one while keeping the original target and grammar. The original forced moments contain y^(13−a−b), and the opposite-cross term contains z^a, so the constant equations in §5 cannot be substituted unchanged at arbitrary y,z.

To exclude degrees 2,3,4 in the full model, one still needs either:

1. a valid target-preserving reduction of every sixteen-bank certificate to y=z=1; or
2. a complete algebraic obstruction for all y,z∈F_(53^d)^*, including any rank-drop loci in the degree-seven recurrence system, together with complete sector consistency and actual splitting of both support polynomials.

Neither the accepted quotient census nor the new pinned eliminant supplies that implication. The existence of a quintic witness still does not prove that degree five is globally least. Whether seventeen occurs in the remaining fields is also unchanged.

## 8. Bounded checks and provenance

`check_fresh.py` is newly authored for this task. It reads only inert JSON data from the accepted gate. It reconstructs G, six forced rows and their rank, the b=3 moments, the two recurrence equations, their exact eliminant, both factorizations and prime-degree irreducibility tests. It independently solves all 52 complete sector systems for the four possible pairs. No extension-element enumeration, variable cross-node search, external write or supplied-code execution occurred.

`CHECK_RESULT.json` records exact residues and receipts. The accepted gate SHA256 is `abcfb71046f9ff1b65cf5f08288454ae51cc46b3a7c9fdc4b8b339e9df2ed486`.

Principal source files, read as inert text/data:

- `n13_publication_claims_audit_2341/THEOREM_AND_OPEN_OBLIGATIONS.md`: current theorem and unresolved full field classification.
- `n13_extension_quotient_gate_2045/CONTRACT.md`: exact bounded census scope.
- `n13_extension_quotient_gate_2045/QUOTIENT_GATE.json`: finite family and full-sector acceptance data.
- `n13_extension_independent_2049/INDEPENDENT_REVIEW.md`, §§1,4,6: source-bound universal lower bound, original-bank quotient bridge and exact accepted census.
- `n13_extension_quotient_gate_2045/sources/PRIOR_LOWER_REVIEW.md`, §§3–6: original arbitrary-beta expansion, forced moments and reflection.

All claims here inherit the accepted universal lower bound. They do not constitute a new replay of its degree-39 minor certificate.
