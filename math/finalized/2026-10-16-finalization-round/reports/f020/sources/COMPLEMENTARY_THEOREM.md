# Complementary-degree endpoint certificates and a sharp spectral-fusion limit

13 October 2026 UTC. Author-checked candidate, awaiting independent review.

## Result

At a characteristic-two parameter of exact odd order d=2h+1, the finite RS chain has an inverse-parameter reflection. Its full trace polynomial is a fixed squarefree cyclotomic trace polynomial. These facts give two uniform structural consequences:

1. Explicit product-coefficient certificates exclude common zeros of the complementary endpoints E_m(q) and E_(h-m-1)*(q).
2. The common spectral roots of the complementary trace polynomials P_m(X;q) and P_(h-m-1)(X;q^-1) are simple in their gcd and belong to the known full-chain spectrum.

In particular, for every m>=1, paired endpoint zeros are impossible at every parameter of exact order 4m+3. This is an infinite actual-family exclusion, not a larger finite-b certificate or a norm reformulation.

The same mechanism does not exclude separate collision roots. An exact synthetic five-vertex chain below has the full order-11 cyclotomic trace spectrum, inverse-Frobenius reflection, and nonzero edges, while its two complementary two-vertex blocks both have a double root at distinct conjugate coordinates. This is a precise obstruction to inferring the all-four-channel theorem from those structural properties alone. It is not an actual RS counterexample.

The original all-m paired-support gate remains OPEN at priority 58. No characteristic-zero squarefreeness consequence, general FFT improvement, or historical novelty is claimed.

## 1. Exact setup and the unresolved theorem

Work over a field K of characteristic two. For the integral Gaussian polynomials reduced modulo two, define

H_(2j+1)(z;q)=(z+1)U_j(z;q),
U_j(z;q)=z^j P_j(z+z^-1;q),
P_0=1, P_1=X+q+q^2,
P_j=(X+a_j)P_(j-1)+c_j P_(j-2),
a_j=q^(2j-1)(1+q), c_j=(1+q^(2j-1))(1+q^(2j-2)).

The formula for c_j is used at j>=2; set P_-1=0 when a boundary term is absent. Let E_j=P_j(0;q) and E_j*=q^[j(j+1)]E_j(q^-1), using the accepted actual degree j(j+1) of E_j. E_0=E_0*=1 is a seed.

For the full unresolved gate, split P_m=A_old(X^2)+X B_old(X^2), put R_m=Res(A_old,B_old), Q_m=E_mR_m and N_m=deg Q_m=m(m+1)(2m+1)/3. It remains unknown whether

(Q_m,Q_m*)=(1) in F2[q,1/L_(2m+1)]

for all m, where L_(2m+1)=product_(r=0)^m(1+q^(2r+1)) and Q_m* is reversed at exactly N_m. All four endpoint/collision combinations at inverse parameters matter. This note neither changes that statement nor claims that studying endpoints alone suffices.

## 2. Uniform product certificate for complementary endpoints

Let alpha in K have exact odd order d=2h+1>=3. Define

C_j=product_(r=1)^j(1+alpha^(2r)),
D_j=product_(r=1)^j(1+alpha^(2r-1)),
s_j=D_j/C_j, S_j=sum_(r=0)^j s_r.

Every factor with 1<=j<=h is nonzero: its positive exponent lies below d, and alpha has exact order d. No residue-field denominator is being inverted without this guard.

For every m,n>=0 with m+n=h-1, the following exact identity holds in K:

C_h C_n E_m(alpha) + D_h C_m E_n*(alpha) = C_m C_n.       (1)

Since C_m C_n is a unit, this is an explicit unit-ideal certificate for the complementary pair. It is not an existential rephrasing of their gcd.

### Proof

The accepted endpoint recurrence gives E_j=C_j S_j, by unrolling E_j=D_j+(1+q^(2j))E_(j-1). At exact order d, all interior coefficients of H_d vanish: for 1<=k<d, the Gaussian product numerator contains 1-alpha^d, while its denominator has only exponents below d. Therefore

H_d(z;alpha)=1+z^d.

Ordinary differentiation at z=1 gives E_h(alpha)=H_d'(1;alpha)=1, because d is odd in characteristic two. Thus S_h=1/C_h.

Reflection of each factor gives, for 0<=j<=h,

s_(h-j)=s_h alpha^j s_j=s_h s_j(alpha^-1).                 (2)

Indeed the last j factors in s_h have indices r=h+1-l, so the inverse quotient is

(1+alpha^(1-2l))/(1+alpha^(-2l))
  =alpha (1+alpha^(2l-1))/(1+alpha^(2l)).

Multiplying proves (2), with no analytic conjugation or positivity. Reflect the tail after m, whose complementary length is n=h-m-1:

S_h=S_m+s_h S_n(alpha^-1).                                (3)

Now C_n(alpha^-1)=alpha^[-n(n+1)]C_n(alpha), so

S_n(alpha^-1)=E_n*(alpha)/C_n(alpha).

Insert S_h=1/C_h, s_h=D_h/C_h and S_m=E_m/C_m into (3), then clear only the already nonzero C factors. This is (1). The empty-product m=0 or n=0 cases are included. QED.

### Balanced actual-family exclusion

Take h=2m+1, so d=4m+3. Equation (1), divided by the unit C_m, becomes

C_(2m+1) E_m(alpha) + D_(2m+1) E_m*(alpha) = C_m.          (4)

Consequently, for every m>=1,

gcd(E_m,E_m*, reduced Phi_(4m+3))=1 in F2[q].              (5)

The reduced cyclotomic polynomial is squarefree because 4m+3 is odd, and all its roots have that exact order. Equivalently, (4) is a polynomial congruence modulo reduced Phi_(4m+3), with a right side coprime to that modulus. Multiplying by an inverse of C_m modulo the cyclotomic polynomial yields a conventional right-side-one certificate if desired.

If inversion is a Frobenius power on the alpha orbit, then E_m(alpha)=0 would automatically force E_m(alpha^-1)=0. Thus (4) also excludes a one-sided endpoint zero on those inert/self-reciprocal orbits. No such one-sided conclusion is asserted for a distinct inverse pair.

For other orders, (1) relates different indices m and n. A zero of E_m(alpha) prescribes a nonzero complementary endpoint; it does not create a smaller bad pair. There is no induction to arbitrary d from (1).

## 3. Full-chain reflection and a stronger spectral constraint

Let J_h(alpha) be the h-by-h tridiagonal matrix with diagonal a_1,...,a_h, upper diagonal 1, and lower diagonal c_2,...,c_h. Its characteristic polynomial is P_h by continuant expansion; all c_j are nonzero.

Direct use of alpha^d=1 gives

a_(h+1-j)(alpha)=a_j(alpha^-1),
c_(h+2-j)(alpha)=c_j(alpha^-1) for 2<=j<=h.                (6)

Thus the trailing k-by-k principal block, read in reverse order, has the determinant recurrence of P_k(X;alpha^-1). Reversing swaps upper and lower entries, but only their products enter the determinant recurrence. If a normalized matrix equality is wanted, an invertible diagonal similarity restores upper entries 1 because every edge is a unit. This reversal-plus-similarity is not the forbidden diagonal-affine Hermitian gauge from the prior review; it reverses the vertex order and uses a different construction.

Define the monic degree-h polynomial CYC_d by

z^h CYC_d(z+z^-1)=(z^d+1)/(z+1).

It lies in F2[X] and has constant coefficient 1. The preceding H_d identity proves

P_h(X;alpha)=CYC_d(X).                                   (7)

Its h roots are alpha^j+alpha^-j, 1<=j<=h. They are distinct: for nonzero u,v, equality u+u^-1=v+v^-1 implies (u+v)(uv+1)=0. In the chosen index range this forces equal indices. Hence CYC_d is squarefree, with no zero root. This proves the simple full spectrum without any Hermitian, positivity, or spectral-coordinate field assumption.

For m+n=h-1, cut at the middle vertex m+1. Expansion of the tridiagonal determinant according to whether that vertex is unmatched or paired with either neighbor gives

CYC_d = (X+a_(m+1)) P_m P_n^inv
       + c_(m+1) P_(m-1) P_n^inv
       + c_(m+2) P_m P_(n-1)^inv,                         (8)

where P_j^inv=P_j(X;alpha^-1), and absent boundary terms are zero. One can also prove (8) by the three-term continuant recurrence, separating the three possible matchings at the cut vertex. Characteristic two removes determinant signs.

It follows immediately that

gcd_X(P_m,P_n^inv) divides CYC_d.                         (9)

Therefore this gcd is squarefree and its roots belong to the explicit full spectrum. In particular:

- The complementary polynomials cannot both vanish at X=0.
- They cannot both have a repeated root at the same spectral coordinate: such a root would divide their gcd twice, contradicting (9).
- Equivalently, gcd(P_m,P_m',P_n^inv,(P_n^inv)')=1.

At h=2m+1 these statements concern the same family index at inverse parameters. For an inert parameter with involution sigma(alpha)=alpha^-1, a repeated P_m root fixed by sigma would violate the second item. This conditional conclusion requires that the root lie in a field on which sigma acts and be fixed; neither condition is silently supplied by the original support problem.

Equation (8) also supplies a second explicit endpoint certificate by setting X=0. It checks (1) through an independent algebraic interface, although the two certificates need not have the same coefficients.

## 4. Sharp obstruction to completing the paired theorem from this fusion

The remaining issue is that the two inverse polynomials can have repeated roots at different coordinates. The following synthetic construction satisfies the complete reflection and full-cyclotomic-spectrum premises, not merely nonzero edges.

Work over F4=F2[w]/(w^2+w+1), with sigma(w)=w^2. Use the tridiagonal five-by-five matrix with

- diagonal (0,0,1,0,0),
- upper diagonal (1,1,1,1),
- lower diagonal (w^2,w^2,w,w).

All edges are nonzero. Conjugating its diagonal and edge products gives their reverse sequence, exactly the structural condition (6). The leading and trailing two-vertex characteristic polynomials are

L=X^2+w^2=(X+w)^2,
R=X^2+w=(X+w^2)^2.

Both have an ordinary collision, at distinct conjugate roots. Their endpoint values are nonzero and gcd(L,R)=1, so the obstruction deliberately survives every common-coordinate exclusion above.

The full characteristic polynomial, by direct expansion or the central-cut formula, is

(X+1)(X^2+w^2)(X^2+w)+w^2 X(X^2+w)+w X(X^2+w^2)
  =X^5+X^4+X^2+X+1
  =CYC_11(X).                                            (10)

Its derivative is X^4+1, and its value at X=1 is 1, so it is squarefree. Its endpoint is 1. This is the exact full spectrum required at d=11, h=5, m=n=2.

All objects can be placed in the actual quadratic trace-field setting: take L=F_(2^10), K=F_(2^5), let alpha have order 11, and sigma(u)=u^32. The subfield F4 lies in L, sigma(w)=w^2, and sigma(alpha)=alpha^-1. CYC_11 has precisely the five actual trace roots alpha^j+alpha^-j in K. The checker supplies explicit residues in F2[t]/(t^10+t^3+1), including an order-11 alpha and an order-3 w, and verifies every equality.

This is not the actual RS J_5(alpha): its zero first diagonal contradicts a_1=alpha(1+alpha), which is nonzero at order 11. Therefore (10) does not refute the paired-support conjecture, and no actual-family bad factor is asserted.

What it refutes is precisely this proposed implication:

"A reflected nonzero-edge chain with full characteristic polynomial CYC_d must have at least one squarefree complementary block."

The full matrix is semisimple, has the exact desired spectrum, and respects the inverse Frobenius involution, yet both complementary blocks are nonsquarefree. Any continuation needs a further property of the actual RS diagonal/edge formulas that excludes these distinct-coordinate collisions. Repeating full-chain semisimplicity, a norm interpretation, reflection, or common-root coprimality will not suffice.

## 5. Sources and comparison

The accepted endpoint recurrence, kernel recurrence, Frobenius guards, reciprocal descent, and fixed b31 conclusions are used at their exact source-bound scopes. The b31 all-A report already contains the characteristic-zero prefix reflection used in its lower-order argument. Section 2 supplies its denominator-checked characteristic-two algebraic version, with explicit complementary certificates and the resulting infinite balanced-order exclusion. The reflection identity is therefore not claimed as an unprecedented mechanism.

The general continuant determinant method and Gaussian root-of-unity specialization are classical. Vinroot's primary-source account records the Rogers-Szego recurrence and Gauss evaluation (https://www.math.wm.edu/~vinroot/RogersSzego_1.pdf). The elementary proof of H_d=1+z^d given above is also the basic q-Lucas specialization. No new q-Lucas or continuant theorem is claimed.

Relative to the inspected packet, the precise new deliverable is the all-parameter complementary-minor interface, its explicit high-order endpoint exclusion, and the exact cyclotomic-spectrum countermodel delineating what this interface cannot prove. Historical novelty and publication priority have not been established. No literature-wide nonimplication is claimed.

## 6. Tests and final boundary

check_complement.py imports no predecessor or producer research program. It works in the full reduced cyclotomic quotient ring, so each selected test checks all primitive components, not just one convenient irreducible factor. The balanced controls use only already studied m=1,2,12, at their theorem-prescribed orders 7,11,51. Two unbalanced controls use (d,m,n)=(31,12,2),(15,2,4). The complementary index 4 and full-chain boundary indices are auxiliary identity-construction data, not newly certified finite stages or a support census.

For every control, direct Gaussian q-Pascal reconstruction and trace folding agree with the separate three-term trace recurrence at both orientations. The code checks H_d, all reflection coefficients, the full central-cut identity, both endpoint certificates, prefix reflection, exact primitive-order and unit-denominator guards. The synthetic model is checked over F4 and embedded into an explicitly certified F_(2^10). Corruption controls reject 24 exact false identities or witness changes. Cold replay and source verification are recorded separately.

The all-parameter statements rely on the proofs, not these finite controls. This is author-side orthogonal reconstruction, not an independent-person review. The broad gate remains OPEN at 58; the endpoint gate remains OPEN at 53. The named bounded step is ready for review, not declared accepted. No b33 step, table edit, repository mutation, child task, Fourier runtime claim, or new canonical discovery is part of this packet.
