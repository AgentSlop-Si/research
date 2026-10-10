# Fourteen signed magnetic banks for the negative Fourier matrix of order eleven

10 October 2026. New author construction, pending independent review. This is an upper bound in the exact accepted bank grammar. It preserves all accepted order-three, order-five, and order-seven files and results. No minimum at order eleven, general-size exact formula, FFT runtime improvement, or historical novelty is asserted.

## 1. Result, field, and counted object

Let q be any primitive eleventh root of unity, K=Q(q), and F[k,t]=q^(−kt), for 0≤k,t≤10. The explicit monic sextic g over K defined below has six distinct nonzero roots x_1,...,x_6. Let L be its splitting field over K. Then F is a sum of at most fourteen permitted banks over L, and hence over C, with orientation multiplicities

(n_++,n_-+,n_+-,n_--)=(6,1,1,6).

Every bank has beta=1. The ++ and −− groups both use alpha=x_1,...,x_6. The −+ and +− singletons both use alpha=1. Thus the explicit field extension satisfies [L:K]≤6!=720; no claim that these nodes lie in K is made. All transformed moments, all defining matrices, and their solutions lie in K. Actual individual bank amplitudes and phase weights lie in L. Permuting the roots merely permutes banks inside the two six-bank groups.

The exact accepted grammar is

B_(epsilon,delta)(alpha,1;w)
 = (1/11) sum_(j=0)^10 w_j (I−alpha S^epsilon−q^(epsilon delta j)T^delta)^−1,

where S e_i=e_(i+1 mod11), T e_i=q^i e_i, epsilon,delta∈{+1,−1}, and

Delta=1−alpha^11−1=−alpha^11≠0.

There are no extra gauges, new Weyl generators, coordinate transformations, products, or free pre/post maps. In particular alpha^11=1 and alpha^11=−1 are legal. Only alpha=0 is forbidden when beta=1.

The whole phase-weighted bank is counted once. There are fourteen declared parameter pairs, fourteen sign pairs, and 154 raw phase weights (11 per bank). There are twelve algebraic node occurrences coming from six roots, together with two singleton nodes. Zero banks, should any occur, could be omitted and cannot weaken the stated upper bound.

## 2. Coefficient convention and target

Put r=[epsilon a]_11 and ell=[delta b]_11. Define

G_(epsilon,delta)(a,b)
 = [r+ell choose ell]_(q^(epsilon delta)) if r+ell≤10,
 = 0 otherwise,

where [r+ell choose ell]_z = product_(j=1)^ell (1−z^(r+j))/(1−z^j). Empty products are 1. All denominators appearing here are nonzero.

Write C=(1/11) sum_(t=0)^10 q^(−t²) and f(a,b)=q^(3(a+b)²). Here 3 is the inverse of 4 modulo eleven; exponents are taken modulo eleven. C≠0 by the elementary quadratic Gauss-sum identity. The target Weyl coefficient of W_(a,b)=S^aT^b is C f(a,b).

If a bank's normalized sector amplitudes are h_ell, its Weyl coefficient at (a,b) is

C h_ell alpha^r G_(epsilon,delta)(a,b).

This follows from the same finite Gaussian-binomial expansion and finite-character projection as in the accepted manuscript. Section 8 below explicitly converts every chosen h into the original raw weights, including the accepted 1/11 normalization.

## 3. The sextic: four explicit linear conditions

Set H=q/(1+q). Define nine edge moments s_0,...,s_8 by

s_0=1,
s_(a−1)=f(a,1)/(H G_++(a,1))−G_-+(a,1)/G_++(a,1),   2≤a≤9.

Equivalently G_++(a,1)=(1−q^(a+1))/(1−q), and G_-+(a,1)=(1−q^(a−1))/(1−q^(−1)) in this range. Define

T=1/G_-+(9,2)=1/[4 choose 2]_(q^−1),
u_(a−2)=(f(a,2)−T G_-+(a,2))/G_++(a,2),   2≤a≤8.

Thus u_0,...,u_6 are seven explicitly specified elements of K. Define the 4×4 matrix and right-hand side

A = ((s_0,s_1,s_2,s_3),
     (s_1,s_2,s_3,s_4),
     (s_2,s_3,s_4,s_5),
     (u_0,u_1,u_2,u_3)),

v = (−s_6,−s_7,−s_8,−u_6)^t.

Let (c_0,c_1,c_2,c_3)^t=A^−1 v, and set c_4=c_5=0, c_6=1. The promised polynomial is

g(t)=t^6+c_3 t^3+c_2 t²+c_1 t+c_0.

This is an exact, finite algebraic definition, not a finite-field lifting prescription. Section 4 proves A is invertible, c_0≠0, and g is separable in characteristic zero. N11_EXACT_WITNESS.json additionally gives each c_i in the rational basis 1,q,...,q^9, with a common coefficient denominator 469219301 for c_0,...,c_3.

The four defining equations are precisely

s_(r+6)+sum_(k=0)^5 c_k s_(r+k)=0,   r=0,1,2,
u_6+sum_(k=0)^5 c_k u_k=0.

They force one shared root set to interpolate the long b=1 edge and the shorter central portion of b=2. Imposing only the first row of edges is insufficient at order eleven.

## 4. Exact good-reduction nonvanishing certificate

All objects in Section 3 are defined over K first. Let R=Z[q] localized at the maximal ideal (23,q−2). Since 2 has exact order eleven in F_23, evaluation q↦2 gives the residue map R→F_23. Indeed 2^11=1 modulo23 and 2≠1; primality of eleven proves exact order. Therefore every 1−q^j, 1≤j≤10, as well as 11 and 1+q, is a unit of R. Nonzero Gaussian factors with total degree at most ten are units too. Consequently H,T,s_i,u_i are well-defined in R.

Their residues are

H=16, T=9,
(s_0,...,s_8)=(1,17,2,0,5,11,18,10,14),
(u_0,...,u_6)=(9,11,11,20,12,15,19).

The defining system reduces to

Abar=((1,17,2,0),(17,2,0,5),(2,0,5,11),(9,11,11,20)),
vbar=(5,13,9,4)^t,
det(Abar)=1.

Hence A is invertible over R, and all c_i lie in R. Direct substitution gives

gbar(t)=t^6+4t^3+2t²+21t+12.

In particular c_0 has residue12 and is a unit. The Sylvester determinant of gbar and its derivative is

Res(gbar,gbar′)=6 modulo23,

so g is squarefree over K and all six characteristic-zero roots are distinct. The exact 11×11 Sylvester matrix is recorded in N11_MODULAR_CERTIFICATE.json; gcd(gbar,gbar′)=1 was also checked separately. The resultant is a unit of R. These observations prove the Vandermonde and g′(x_i) denominators used later are nonzero.

Reduction must use the original formulas and linear systems in R. Some expanded rational-basis row coefficients in the JSON have denominators divisible by23 because rational-basis expansion can introduce denominators from other primes over23. They must not be reduced term by term. The sextic coefficients themselves have common denominator469219301≡4 modulo23.

A polynomial or determinant that maps to a nonzero residue cannot be zero in K. This is the complete use of reduction here. No solution over F_23 is assumed to lift, and no algebraic root in the finite field is chosen. In particular the construction works for every primitive complex q: each embedding of the abstract cyclotomic field preserves these characteristic-zero nonzero identities.

## 5. Row matrices and nonsingular rows

For 0≤r≤10, let p_r=(p_r0,...,p_r5) be the coefficient vector of t^r modulo g. Initialize p_r to the r-th coordinate vector for r<6, and use

p_r=−sum_(k=0)^5 c_k p_(r−6+k),   r≥6.

For each b, order fourteen transformed unknowns as

z_b=(K_++0,...,K_++5, h_-+, h_+-, K_--0,...,K_--5).

Define the 11×14 matrix M_b by its a-th row, 0≤a≤10:

(G_++(a,b) p_a,
 G_-+(a,b),
 G_+-(a,b),
 G_--(a,b) p_[-a]_11).

This is exactly the original bank coefficient matrix after replacing each six-node group by its first six power moments. No coordinate transformation of the target matrix or Weyl generators occurs: the moment change is solely a way to specify the same six bank amplitudes.

For b=0,3,4,5 take the following ordered zero-based column sets, set all omitted coordinates of z_b to zero, and solve the indicated square system against f_b=(f(0,b),...,f(10,b))^t:

b=0: (0,1,2,3,4,5,6,8,9,10,11), determinant residue5.
b=3: (0,1,2,3,4,5,6,7,8,9,10), determinant residue3.
b=4: (0,1,2,3,4,5,6,7,9,10,11), determinant residue18.
b=5: (0,1,2,3,4,5,6,9,10,11,12), determinant residue8.

The determinant residues are computed from the explicitly displayed formulas at q=2 modulo23, after the legal reduction in Section 4. Every M_b entry lies in R because reduction modulo the monic g adds no denominator. Thus each selected determinant is a unit of R and nonzero in K. The four solves exist uniquely on the selected columns. They specify 44 coordinates; the other 12 coordinates across these four row vectors are set to zero. N11_MODULAR_CERTIFICATE.json records all reduced matrices, and N11_EXACT_WITNESS.json records all exact solutions in the cyclotomic basis.

## 6. Two deficient but compatible edge rows

### Row b=1

Set

K_0=−H (s_5+sum_(k=1)^5 c_k s_(k−1))/c_0,
K_d=H s_(d−1),   1≤d≤5,

and define

z_1=(K_0,...,K_5, H, f(0,1)−K_0−H, 0,0,0,0,0,0).

For a root-supported moment sequence, g gives K_(r+6)=−sum_(k=0)^5 c_k K_(r+k). The definition of K_0 gives K_6=H s_5; the three s-recurrences in Section 3 then give K_7=H s_6, K_8=H s_7, K_9=H s_8. At a=1 the forward amplitude gives G_++(1,1)K_1=q=f(1,1). At a=10 only the positive-delta backward singleton contributes among nonaxis sectors and gives G_-+(10,1)H=1=f(10,1). At 2≤a≤9 the definition of s_(a−1) gives the desired sum. The negative-delta singleton's ell=10 sector supports only a=0, where it supplies the stated residual. Thus M_1 z_1=f_1 exactly.

### Row b=2

Put

L_1=−(u_5+sum_(k=1)^5 c_k u_(k−1))/c_0,
L_0=−(u_4+c_1 L_1+sum_(k=2)^5 c_k u_(k−2))/c_0,

P=(f(1,2)−G_++(1,2)L_1)/G_+-(1,2),
Q_1=(f(10,2)−T G_-+(10,2))/G_--(10,2),
Q_0=f(0,2)−L_0−T−P,

and define

z_2=(L_0,L_1,u_0,u_1,u_2,u_3, T,P, Q_0,Q_1,0,0,0,0).

The g-recurrence gives the forward-group moments L_a=u_(a−2) for a=2,...,8: the definitions of L_0,L_1 ensure L_6=u_4 and L_7=u_5, and the u-recurrence ensures L_8=u_6. On the central interval 2≤a≤8, the negative-delta sectors have zero support, so the definition of u gives the target. At a=9 the singleton with amplitude T supplies f(9,2)=1. At a=1 the +− singleton's ell=9 sector supplies P times its nonzero Gaussian factor. At a=10 the −− group's ell=9 sector depends only on Q_1 and supplies the missing term. At a=0 all four Gaussian factors equal1, so Q_0 matches the axis. Thus M_2 z_2=f_2 exactly.

Every denominator in these two formulas is nonzero: c_0 is a unit by Section 4, and the two edge Gaussian factors have total degree ten and so are units.

## 7. Reflection supplies all remaining rows

Let

J(K_+0,...,K_+5,h_-+,h_+-,K_-0,...,K_-5)
 =(K_-0,...,K_-5,h_+-,h_-+,K_+0,...,K_+5).

Define z_(11−b)=J(z_b) for b=1,...,5. The simultaneous reflection (a,b)↦(−a,−b) preserves f(a,b), sends ++↔−− and −+↔+−, preserves epsilon delta, and preserves the relevant local r,ell coordinates. Hence these five reflected row vectors solve the remaining rows exactly. This uses only the same simultaneous-reflection identity already present in the accepted order-seven construction. It does not assume either one-coordinate reflection or an extra Fourier-conjugation operation.

We have now specified all 154 transformed sector coordinates. At the good reduction the row ranks are

(11,8,10,11,11,11,11,11,11,10,8).

The explicit formulas prove compatibility of the four rank-deficient rows in characteristic zero; the nonsingular minors prove solvability of the others. The proof does not need to identify every characteristic-zero deficient-row rank exactly.

## 8. Individual bank amplitudes and all 154 raw weights

For any six moments K_0,...,K_5 define the root-amplitude function

A_K(x) = (1/g′(x)) sum_(d=0)^5 K_d sum_(k=d+1)^6 c_k x^(k−1−d).

For each root x_i this is well defined. Indeed the numerator's coefficients are those of g(t)/(t−x_i), and the Lagrange cardinal polynomials imply

sum_(i=1)^6 A_K(x_i) x_i^d=K_d,   0≤d≤5.

The same equality for higher powers follows by reducing t^r modulo g. This explains directly why the row matrix M_b specifies precisely the desired bank coefficients.

For each b=0,...,10 assign the normalized sector amplitude in sector ell=[delta b]_11 as follows:

- ++ root bank i: h_(i,b)=A_(z_b0,...,z_b5)(x_i).
- −+ singleton: h_b=z_b6.
- +− singleton: h_[-b]_11=z_b7.
- −− root bank i: h_(i,[-b]_11)=A_(z_b8,...,z_b13)(x_i).

For a fixed orientation, b↦[delta b]_11 is a permutation, so each bank's eleven sectors are assigned exactly once. Finally, for each bank n and every j=0,...,10, define

w_(n,j)=C Delta_n sum_(ell=0)^10 h_(n,ell) q^(−epsilon_n delta_n j ell),
Delta_n=−alpha_n^11.

This is an explicit algebraic specification of every one of the 154 original branch weights. Finite-character orthogonality gives (1/11) sum_j w_(n,j)q^(epsilon_n delta_n j ell)=C Delta_n h_(n,ell). Thus substituting into the original resolvents produces exactly the sector coefficients already verified. There is no missing or extra factor11.

## 9. Literal-resolvent proof and control boundary

For a legal branch set X_j=alpha S^epsilon+q^(epsilon delta j)T^delta. The accepted Gaussian-binomial identity at the primitive eleventh root gives

X_j^11=(alpha^11+1)I,
(I−X_j)^−1=(I+X_j+...+X_j^10)/(−alpha^11).

Both products with I−X_j equal I by telescoping. All branches are legal because alpha=1 or a nonzero root of g. Substituting the raw weights from Section 8 into this exact inverse formula gives the Weyl expansion in Section 2. Sections 5–8 match every coefficient C f(a,b), and the 121 Weyl matrices are a basis. Therefore the sum of the fourteen original resolvent banks equals F in all 121 original matrix entries.

The mathematical proof is characteristic zero and does not depend on numeric root selection, numerical linear solves, or a finite-field lift. The fresh exact author control independently constructs K with rational polynomial arithmetic modulo Phi_11, derives s,u,g and all row vectors from the displayed formulas, solves the four exact square systems, and verifies all 121 Weyl coefficient equations. It separately extracts all 121 Fourier Weyl coefficients using the literal direct trace formula. N11_EXACT_RUN.log records PASS. This control does not claim to be an independent review of the author proof.

No predecessor or supplied research script was executed, imported, compiled, or parsed. The only executed programs are fresh author controls in this new folder. The accepted order-seven proofs and witness files were read, not changed.

## 10. A precise boundary on the simplest twelve-bank extension

This subsection is a restricted obstruction, not a twelve-bank lower bound. Consider the direct symmetric analogue (5,1,1,5), with singleton nodes1 and the same five distinct nonzero root nodes for ++ and −−, and impose that their monic annihilator is depressed:

h(t)=t^5+d_3 t^3+d_2 t²+d_1 t+d_0.

The b=1 equations force the four recurrences

s_(r+5)+sum_(k=0)^3 d_k s_(r+k)=0,   r=0,1,2,3.

The corresponding 4×4 moment determinant has residue20 modulo23, so it uniquely fixes h over K. Its residue is

hbar(t)=t^5+8t^3+4t²+t+10.

On the central b=2 interval, the backward singleton amplitude is forced to T, so the forward root set would have to represent the u sequence. Therefore its annihilator must satisfy

u_(r+5)+sum_(k=0)^3 d_k u_(r+k)=0,   r=0,1.

Their residues are respectively21 and17 modulo23, both nonzero. All defining denominators survive at the same good prime, so these are nonzero characteristic-zero obstructions. Hence this particular depressed-quintic, singleton-one, mirrored-root ansatz cannot represent F_11. Removing the depression condition, changing singleton nodes, using different root sets, admitting repeated-node strata, or using other orientation multiplicities is outside this obstruction. No assertion that thirteen or twelve banks are impossible follows.

## 11. Cost, scope, and prior-art boundary

The result is the constructive upper bound M_C(11;q)≤14 in exactly the accepted representation grammar, replacing the manuscript's generic 44-bank upper bound at this next odd prime. It does not determine M_C(11;q); the accepted general lower bound there is only6. No accepted small-order equality changes.

Algebraic preparation requires one 4×4 solve over K, four 11×11 solves over K, power reduction modulo a sextic, six distinct roots in a splitting field, 132 root-group sector-amplitude evaluations plus 22 singleton amplitudes, and fourteen eleven-point finite sums for the 154 raw phase weights. There are 12 independent coefficient choices in the four nonsingular row solves fixed to zero by the recipe. Root order contributes no mathematical choice. All parameter and amplitude formulas are exact, but field-generation cost, embedding precision, numerical conditioning, and bit complexity have not been analyzed. At fixed N=11 these are finite algebraic operations; no asymptotic FFT conclusion follows.

A literal evaluation of the displayed representation has 154 inverse branches of size11. Sharing or faster algorithms would require separate work. Counting14 banks is not an arithmetic operation count. No infinite-family construction or general N+1 claim is made.

The basic tools (Gaussian-binomial expansion, Weyl projection, Vandermonde moment interpolation, and good reduction) are classical. This packet carries out a new next-prime construction within the reviewed model but makes no historical-priority claim. No new literature search was needed for the algebraic derivation, and novelty remains unresolved.

## Sources inspected

- small_order_synthesis_manuscript/editorial_v2/small_order_synthesis.tex: exact bank grammar, coefficient conventions, accepted field scope, and generic4N upper bound.
- research_cycle_1126/n7_eight_bank_construction/N7_EIGHT_BANK_CONSTRUCTION.md: accepted three-root moment construction and simultaneous-reflection mechanism.

All new work is confined to research_cycle_1453/signed_bank_extension/. This is an author packet awaiting independent review.
