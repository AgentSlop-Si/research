# Seven is the exact eight-point chirp stage minimum in characteristic zero

**Existing owner:** M-MULTISCALE-CHIRP; related queue view Q24.  
**Date:** 18 October 2026.  
**State:** completed candidate theorem and exact checker; independent review pending.  
**No external write, new catalogue ID, score, status or census change is made.**

## 1. Result and exact scope

Let K have characteristic zero, let ζ be a primitive sixteenth root, let S be the eight-cycle shift, and put

C[i,j] = ζ^((i-j)^2), 0 ≤ i,j < 8.

Use the original literal grammar: a product of individually invertible pure-shift resolvents (I−α S^s)^−1, arbitrary integer strides, and arbitrary interspersed nonzero scalar Weyl-monomial gauges. No arbitrary diagonal gauges, additive branches, selected-output weakening, or changes to C are allowed.

**Theorem.** Every such representation needs at least seven resolvents. Seven suffice over C, over the algebraic closure of Q, and over the splitting field over Q(ζ) of the explicit polynomial below. Thus the exact minimum over C is **7**. The lower bound holds over every characteristic-zero coefficient field containing ζ. The construction may require a finite extension of Q(ζ); exact attainment over Q(ζ) itself is not claimed.

The inherited uniform bound at N=8 was only m+1=4. The previously accepted finite-field search gave minima 10 or 11 over F17 for its eight primitive sixteenth roots. This theorem proves a new characteristic-zero minimum. The same proof, with the explicit witness in Section 10, also gives exact minimum seven over F(17³) at ζ=3. It neither transfers the finite-point search to C nor reruns it.

Write a=ζ^−1 and b=a^4, so b²=−1. Define

Q(x)=1+a x+b x²−a x³+x⁴−a x⁵+b x⁶+a x⁷.

The exact inverse is C^−1=Q(S)/8. The independent integral cyclotomic check in verify_exact.py verifies all 64 entries of C Q(S)=8 I.

## 2. Normalization, gauges and symmetries

Move Weyl gauges through resolvents using T^v S^s T^−v=ω^(vs) S^s. The inverse of any candidate becomes κ S^r T^v times a product of shift binomials. Since C^−1 and the binomial product are invertible circulants, T^v must be scalar, hence v=0 modulo 8. A net shift is harmless: if q_t=a^(t²),

q_(t−r)=a^(r²) a^(−2rt) q_t.

It changes only the scalar and a root-of-unity rescaling of all binomial parameters. Consequently it suffices to decide

P(x)=h Q(x) in K[x]/(x⁸−1), h≠0,

where P is a product of at most six individually invertible binomials.

A zero parameter gives an identity factor; stride zero gives a nonzero scalar. Remove both. For nonzero parameters, replacing stride −s by s contributes a nonzero scalar and a monomial, already covered. Thus all strides may be taken in {1,2,3,4}. The change x↦x³ interchanges strides 1 and 3; stride 6 is reduced to 2 as above. Since Q(x³)=Q(−x), rescaling x by −1 restores the same target. We may therefore assume n1≥n3.

These are exact polynomial-ring identities, valid also over the algebraic closure of F17 with ζ=3, a=6, b=4. The checker verifies the coefficient shift and symmetry identities directly.

## 3. Parity forces at least four odd factors

The target obeys Q(−x)=x⁴Q(x). Write P=O E, where O is the product of odd-stride factors and E is even in x. Since E is invertible, O(−x)=x⁴O(x).

A product with zero or one odd factor cannot satisfy that identity. For two odd factors with strides u,v in {1,3}, the even part requires u+v=4 modulo 8, whereas the odd part requires v−u=4 modulo 8; these cannot both hold for odd u. For three odd factors, the normalized patterns 111, 113, 133 and 333 fail: 111/333 have no constant-pair coefficient at x⁴, while 113/133 have a nonzero x²/x⁶ coefficient without its required partner. Nonzero individual parameters ensure those pair products do not vanish. Thus r=n1+n3≥4.

### Four odd factors

Up to the symmetry, their stride patterns are 1111, 1113 and 1133.

* **1111:** parity forces O=1+x⁴, which is singular on eighth roots.
* **1113:** write O=(1+A x+B x²+C x³)(1+d x³). Parity gives Ad=1, B=Cd, A=−Bd, C=−d. Hence d⁴=1, so the last factor is singular because d⁸=1.
* **1133:** write O=(1+A x+B x²)(1+D x³+E x⁶). Parity gives B=E, A=−BD, D=−AB and 1+B²=AD. If A=0, then D=0 and 1+B²=0, yielding a singular even polynomial. Otherwise
  B=E=ε∈{1,−1}, D=−ε A, A²=−2ε,
  and, with y=x²,
  O=(1+y²)(2+ε y)+A x(1−y²)(1−ε y).

There are at most two even factors when the total length is at most six. Let their product be E0(y)=e0+e1 y+e2 y²+e3 y³ modulo y⁴−1. Comparing O E0=hQ modulo y²−1 and y²+1 gives

(e0+e2, e1+e3)=h(U0,U1),
(e0−e2, e1−e3)=h(V0,V1),

where

U0=(2−ε b)/3, U1=(2b−ε)/3,
V0=a(1+ε)/(2A), V1=a(ε−1)/(2A).

The possible even-stride products are exhausted as follows, allowing fewer factors by taking parameters zero:

* Two stride-4 factors: e1=e3=0, contradicting U1≠0.
* One stride-2 and one stride-4 factor: e0 e3−e1 e2=0. Its displayed value is h²(V0 U1−U0 V1)/2, nonzero for either ε.
* Two stride-2 factors: e3=0, hence U1=V1. For ε=1 this is immediately impossible. For ε=−1, squaring would give a²=2(−3+4b)/9. Together with a⁴=b it implies 177b=−28, inconsistent with b²=−1 in characteristic zero. At the fixed reduction a=6,b=4 in F17, the two sides of that squared equation are 2 and 1, also unequal.

This excludes every case with four odd factors and at most six total factors, both in characteristic zero and at the stated F17 algebraic-closure specialization.

## 4. Five odd factors: elementary cases

The normalized patterns are 11111, 11113 and 11133. With one stride-4 factor, division by it rescales the parity parts independently. Thus O would have to be H Q_c, where

Q_c=1+c x+b x²−c x³+x⁴−c x⁵+b x⁶+c x⁷,

and H,c are nonzero. The same form includes no even factor by setting c=a.

* **11111:** degree at most five cannot provide the nonzero x⁶ coefficient.
* **11113:** let O=(1+A x+B x²+C x³+J x⁴)(1+d x³). Its constant coefficient is 1, so H=1. Coefficients give B=b, d=−c/b, C=1/c, J=−b. The x⁴ and x³ equations respectively imply c²=1−b and c²=b/(1−b)=−(1−b)/2. They contradict characteristic ≠3.
* **11133:** let O=(1+A x+B x²+C x³)(1+D x³+E x⁶). The coefficient equations give
  B=bH, D=−c/b, A=−bH/c, E=−c²/b,
  H=1/(1+c²), C=−cH+c/b.
  The x⁶ equation forces c²=(1+b)/2. The x¹ equation then leaves the nonzero residual (1+3b)/4. This is impossible in characteristic zero, and at b=4 in F17.

For 11111 with one stride-2 factor, parity first forces

O=(1+x⁴)+A x(1−x⁴).

Multiplication by 1+e x² gives even coefficient ratio e=b and odd ratio e=−1, a contradiction.

Thus the only remaining five-odd cases have one stride-2 factor and odd patterns 11113 or 11133. They are handled in Section 6. In particular, Sections 3–4 already exclude **all lengths at most five over the algebraic closure of F17** at ζ=3. This stronger algebraic-closure fact, not the inherited finite-point enumeration, is needed below.

## 5. Why the modular certificates imply the characteristic-zero exclusions

The remaining six-stage patterns, in (n1,n2,n3,n4) notation, are

(3,1,2,0), (4,1,1,0), (3,0,3,0), (4,0,2,0), (5,0,1,0).

The pattern (6,0,0,0) is impossible by degree: it has no x⁷ coefficient. For each of the five displayed patterns,

sum_j gcd(s_j,8) < 8.

This strict bound is crucial. A nonzero projective binomial u+v x^s has at most gcd(s,8) zeros on the eight distinct eighth roots; a monomial or nonzero constant has none. Thus a product in any of these projective patterns cannot vanish at all eight roots, even after specialization.

Suppose a characteristic-zero solution existed. The polynomial coefficient equations and nonvanishing guards would then have an algebraic-number solution: pass to an algebraic closure of Q(a) and use the weak Nullstellensatz. Choose a number field containing its coefficients and a valuation above the prime of Z[a] specified by a↦6 modulo 17. Normalize each parameter pair (u_j,v_j) projectively so both entries are integral and at least one is a unit. Reduce them in the residue field, contained in the algebraic closure of F17.

The homogeneous equations P_i=q_i P_0 survive. The strict zero-count bound prevents the reduced P from being zero, so P_0≠0 and the reduced target is invertible. Every reduced factor is therefore individually invertible. If a pair becomes a monomial or a constant, absorb its scalar/shift: there would be an at-most-five-stage representation, already excluded over the algebraic closure of F17 in Sections 3–4. Otherwise all constant entries are nonzero and the reduced factors can be normalized to the affine forms in Section 6. Those forms are excluded by exact polynomial identities.

This proves the five characteristic-zero exclusions. It explicitly controls poles, monomial limits, zero parameters, lost degree and the possible all-zero product. A finite-field point search alone could not justify this step. The elementary normalization is an instance of the standard valuative extension principle for products of projective lines; see [Stacks, projective morphisms](https://stacks.math.columbia.edu/tag/01W7) and [valuative criterion for universal closedness](https://stacks.math.columbia.edu/tag/01KA).

## 6. Small exact certificates over the algebraic closure of F17

All arithmetic here has a=6, b=4, p=17. The identities in CERTIFICATES.json hold as polynomial identities, hence over **every field extension**, not merely on F17-rational points. verify_exact.py verifies them using only Python integer dictionary arithmetic. No Gröbner-basis engine or numerical solver is used by that checker.

For conciseness, "numerator" means the numerator after exact rational cancellation. Every denominator used below is proved nonzero by the preceding coefficient equations and invertibility. Clearing them can only enlarge the necessary zero set.

### 6.1 Pattern 510: five stride-1 factors and one stride-3 factor

Write P=A5(x)(1+D x³), with A5(0)=1. Coefficients force the common zero equations

f= aD²−D+a=0,
g= bD⁴+aD³+D²+aD+b=0.

The stored univariate Bézout identity is u f+v g=1. This excludes the pattern over the algebraic closure.

### 6.2 Pattern 420: four stride-1 and two stride-3 factors

Write P=A4(x)(1+D x³+E x⁶). From the nonzero x⁵ and x⁷ coefficients, D,E are nonzero. The coefficients yield

E=b+aD+a/D, h=D/(D+aE),
E−D²=h(aD+b),
a/E−aE−DE/h−a=0.

The numerators of the last two equations, after the E substitution, are

−3D⁵+5D⁴−3D³+7D²−D−5,
−3D⁶−5D⁴−4D³+4D²+7D−2.

Their stored Bézout identity equals 1.

### 6.3 Pattern 330: three stride-1 and three stride-3 factors

Write P=(1+A x+B x²+C x³)(1+D x³+E x⁶+F x⁹), reducing modulo x⁸−1. The x⁵ and x⁷ coefficients imply D,E≠0. Necessary substitutions are

h=D/(D+aE), A=ah/E, B=−ah/D,
C=(bh−E)/D, F=E(b/a+1/D).

Let f1,f2,f3 be the numerators of

A+CE+F−ah,
C+D+BF+ah,
AD+CF−h.

The stored explicit identity is sum_i H_i f_i=E². Its multipliers have respectively 14, 15 and 9 terms; total product degree is at most 8. Thus the required nonzero E cannot occur.

### 6.4 Pattern 411: four stride-1, one stride-3 and one stride-2 factor

Write the odd part as A4(x)(1+D x³). Its parity equations give

B=−2D²/(1+D⁴), A=2D³/(1+D⁴), H=D(D⁴−1)/(1+D⁴),

with O_even=(1+x⁴)(1+B x²) and O_odd=x(1−x⁴)(A+H x²). Invertibility gives D≠0 and D⁸≠1, so 1+D⁴≠0. If the even factor is 1+e x², its even coefficient ratio forces

e=(b−B)/(1−bB).

The denominator cannot vanish: B=1/b=−b would leave b−B=2b≠0. The two remaining necessary equations are

A+H+(A−H)e=0,
A−He−a(1+Be)=0.

Their univariate numerator polynomials have a stored Bézout identity equal to 1.

### 6.5 Pattern 312: three stride-1, two stride-3 and one stride-2 factor

Write the odd part as (1+A x+B x²+C x³)(1+D x³+E x⁶). The lead coefficient E is nonzero. The parity equations show that D=0 would force a singular odd part, so D≠0. Put

R=1−E²−D²E,
A=D³/R, C=−D−AE, B=E−D²−ADE.

Here R≠0 because AR=D³. Let u=AD, v=B, r=−BD, t=−AE. The parity constraint is f0=1+BE−AD=0. A possible even factor 1+e x² would make all three affine expressions vanish:

(v−bu)+(u−bv)e,
(r+t)+(r−t)e,
(r−au)+(−t−av)e.

Take the three pairwise 2×2 determinants of their coefficient pairs, together with f0, and clear rational denominators. These are f0,f1,f2,f3 in the certificate. The stored identity is

sum_i H_i f_i=D⁶.

The four multipliers have respectively 27, 10, 10 and 9 terms, and total product degree at most 11. Hence D≠0 is impossible.

Together, these five exact identities finish the lower bound. The certificate-construction script is included for reproducibility, but verification does not rerun it or trust its symbolic-algebra output.

## 7. Seven-stage construction and literal legality

Q has degree seven and constant coefficient one. In its splitting field, let ρ1,…,ρ7 be its roots counted with multiplicity, and set αj=ρj^−1. These are well defined because Q(0)=1. Then the exact polynomial identity is

Q(x)=product_(j=1)^7 (1−αj x).

The identity C Q(S)=8I shows Q(λ)≠0 for every eighth root λ. Consequently no factor vanishes at an eighth root: αj⁸≠1 for every j. Thus every resolvent is individually legal, and

C=8 product_(j=1)^7 (I−αj S)^−1.

This is an exact all-row seven-stage witness. The scalar 8 is an allowed scalar gauge. Roots defined by the displayed exact polynomial are algebraic coefficients, not floating approximations. The splitting extension has degree at most 7! over Q(ζ). Its computation, bit complexity, numerical conditioning and implementation costs are not claimed here.

## 8. What closes and what remains open

This completes the selected eight-point characteristic-zero stage-minimum theorem. It strengthens the lower bound from four to seven and matches it with a legal all-row construction. It also proves that the F17 base-field counts 10–11 need not persist on larger coefficient fields, without changing or questioning those accepted counts.

M-MULTISCALE-CHIRP / Q24 remains an existing open parent. Minima at other lengths/fields, attainment over the unextended cyclotomic field, uniform sharp constructions, numerical certification, efficient coefficient discovery and historical attribution remain open. No arithmetic, memory, bit, runtime or FFT speedup follows from the stage count. The broader census remains 98 closed and 229 open unless the parent separately authorizes and verifies a scoped table update.

## 9. Reproduction and source binding

Run `python verify_exact.py`. It checks five explicit ideal identities, exact cyclotomic inverse/gauge identities, all 19 normalized six-stage patterns, and corrupted-certificate/target controls. It writes CHECK_RESULTS.json. `make_certificates.py` regenerates the certificates using SymPy and NumPy; it is not needed to verify them.

SOURCE_BINDINGS.json and sources/SELECTED_RECORD.json pin the current index. sources/CATALOGUE_ROW.json is the fresh exact A68:AF68 owner row. sources/INHERITED_MULTISCALE_AUDIT.md is the inherited literal-grammar audit read as mathematical text. None of its historical scripts or finite-field searches was executed. Exploratory files are separate from the proof's exact verification path.


## 10. Explicit seven-stage extension-field witness

There is a concrete witness over K=F17[t]/(t³+8t²+6t+8), with ζ=3. The defining cubic has no F17 root and is therefore irreducible. In coordinates (constant,t,t²), take the seven shift-one parameters

(3,0,0), (12,16,2), (8,14,15), (9,4,0),
(2,6,4), (0,9,0), (11,2,13).

Then C=8 product_j (I−α_j S)^−1 exactly, and every α_j⁸ differs from 1. The field operations, seven pole guards, inverse-polynomial product, and literal full 64-entry matrix equality are checked by the standalone standard-library program finite_witness.py. FINITE_WITNESS.json stores all parameters and roots.

The construction comes from the exact factorization over F17

Q(x)=6(x−6)(x³+8x²+6x+8)(x³+10x²+4x+1).

Both cubics are irreducible, so all their roots lie in F(17³). The seven parameters are their reciprocal roots. Sections 3–6 exclude every smaller legal representation over the algebraic closure of F17 for this root, so the explicit witness proves **exact minimum seven over F(17³)**. This does not claim that degree three is the smallest possible extension admitting seven stages, nor that the same conclusion has been checked for the other seven F17 primitive sixteenth roots.
