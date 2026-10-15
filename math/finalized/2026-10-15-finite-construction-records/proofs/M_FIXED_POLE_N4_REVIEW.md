# Complete projective N4 exclusion for the fixed-pole two-cycle pencil

Independent paired review, 9 October 2026 UTC.

## Theorem

Let Z e_j=e_(j+1 mod 4), let V have cycle order (0,2,1,3), and put

G0=(I-Z/4)^(-1), G1=(I-V/5)^(-1), H_[u:v]=uG0+vG1.

There are no three nonzero projective coefficient pairs and invertible
complex diagonal masks L,M such that

F4=H_[a0:a1] L H_[b0:b1] M H_[c0:c1], F4[j,k]=i^(jk).

All three couplings vary independently. The theorem covers every finite
and infinite projective chart, every zero-entry middle support, and all
complex masks. Internal permutations are identity; the cycles and poles
are fixed exactly as above. It does not exclude other poles, additional
gauges, other internal permutations, or larger lengths. In particular,
the independently certified variable-pole N4 point is unaffected.

Because G0,G1 are rational real matrices, the opposite Fourier phase
follows by complex conjugation. Overall nonzero stage and Fourier
normalization scalars are absorbed into a diagonal mask.

## 1. Finite outside couplings and necessary rank constraints

Write H(x)=G0+xG1. Singular square factors cannot produce invertible
F4, so the outside determinant guards are mandatory. Here

det H(x)=(15x+16)(10625x^3+30500x^2+29920x+9984)/159120.

For finite a,c set K=adj(H(a))F4 adj(H(c)). Invertible outer factors
reduce the problem to diagonal equivalence of K and the middle B.
When B is entrywise nonzero, so is K. For i,j=1,2,3, a necessary
equation is

K_ij K_00 B_i0 B_0j-K_i0 K_0j B_ij B_00=0.

Set B=b0G0+b1G1 and collect coefficients of b0^2,b0b1,b1^2 into a
9-by-3 matrix. The nonzero vector (b0^2,b0b1,b1^2) is in its kernel,
so every 3-by-3 coefficient minor vanishes. This includes b0=0.

The three same-row and three same-column minors are exactly divisible
by K_00 K_i0 or K_00 K_0j, respectively. Those factors are nonzero on
this regular support chart. After division and monic normalization,
the six bivariate constraints have total degree 24. Their entire
coefficient arrays are independently reconstructed from geometric
Green sums and symbolic adjugate cofactors by check_six_outer_minors.py.

For the third-row and third-column constraints, divide further by

d(a)d(c), d(x)=(15x+16)(10625x^3+30500x^2+29920x+9984).

Exact divisibility is checked and both removed factors are nonzero
for a valid solution. Call the stripped third-row polynomial F. Its
bidegree is (8,8). Let P1,...,P5 be, in order, row1,row2,col1,col2,
and stripped col3. Define

G1=P1+P2+P3+P4+P5,
G2=P1+2P2+3P3+4P4+5P5.

Both have bidegree (12,12). Every valid regular solution makes
F=G1=G2=0.

## 2. Two exact resultants and their forced singular factors

Let R_j(a)=Res_c(F,G_j), using the generic degrees 8 and 12, hence
20-by-20 Sylvester matrices. Each exact resultant has degree at most
12*8+8*12=192 in a. Define the monic polynomials

h1(a)=a+16/15,
h3(a)=(10625a^3+30500a^2+29920a+9984)/10625.

The independent checker proves over Q(i) that

h1^5 h3^3 divides both R_1 and R_2.

No large exact resultant is needed to verify this divisibility.

### Cubic singular factor

h3 is irreducible and separable over Q(i), and h3(-16/15)!=0.
In Q(i)[a]/(h3), the verifier checks an explicit monic cubic in c
divides both F and each G_j by exact triangular polynomial division.
The corresponding Sylvester nullity at every conjugate root is at
least three. Consequently each determinant vanishes there to order
at least three, proving the factor h3^3.

The cubic divisor is proposed data only: every coefficient relation
needed for its membership is independently checked. The verifier does
not trust a reported Gröbner basis or a modular nullity.

### Fifth order at the linear singular factor

At a0=-16/15 the specialized polynomials f0,g0 have degrees 7 and 10
and exact monic gcd of degree 3. The fixed generic-degree Sylvester
map acts on pairs (u,v) with deg u<12, deg v<8 by uF+vG.
Its specialized kernel has dimension four and basis

(u,v)=c^w(g0/h,-f0/h), w=0,1,2,3,

where h=gcd(f0,g0). This gives determinant order at least four.

The coefficient-of-c^19 functional is a nonzero left-kernel vector
at a0 because every specialized image has degree at most 18. Exact
differentiation also gives deg(F_a(a0,c))<=8 and
deg(G_a(a0,c))<=11. Applying the derivative map to each of the four
displayed kernel vectors again has degree at most 18. Thus that
left-kernel functional annihilates the derivative on the entire
right kernel.

Equivalently, the first-order map between the four-dimensional left
and right nullspaces is singular. After constant invertible row and
column operations isolate the nonsingular block of the specialized
Sylvester matrix, its Schur complement is tB+O(t^2), t=a-a0, with
singular 4-by-4 B. Its determinant is divisible by t^5. This proves
the additional fifth factor exactly, rather than assuming a modular
multiplicity persists in characteristic zero.

## 3. Degree-preserving modular certificate completes the exclusion

Reduce modulo 29 with i mapped to 12. Every rational denominator of
the exact input polynomials and monic forced factors survives this
map; 12^2=-1 modulo 29. Both independently computed modular
resultants have full degree 192. Thus both characteristic-zero
resultants also have degree 192.

Let S_j=R_j/(h1^5 h3^3). The exact division has been proved above.
The divisor is monic and has degree 14, so the quotient coefficients
also admit this good reduction. Each S_j has degree 178, preserved
modulo 29. The checker computes and verifies a complete modular
Bézout identity

U S_1_bar + V S_2_bar = 1.

The nonzero reduced univariate resultant therefore lifts to a
nonzero characteristic-zero resultant. Hence S_1,S_2 have no common
complex root. Any common root of R_1,R_2 must instead satisfy
h1 h3=0, precisely a singular outer determinant. Such a root is
forbidden. This excludes every finite unequal-outer regular point.

This is a guarded, degree-preserving resultant lift with exact
characteristic-zero divisibility. It is not an inference from a
finite-field rational-point search, nor from a modular Gröbner basis.
The independent JSON output includes all modular resultant and
quotient coefficients and the Bézout multipliers.

## 4. Zero-middle and projective-boundary completion

Every middle entry is affine in its finite coupling. There are exactly
nine coupling values with a zero entry. For each, the independent
support checker imposes K_ij=0 at every middle zero and all ratio-minor
equations on fully supported 2-by-2 rectangles. Its exact unsaturated
Gröbner basis is {1} over Q(i) for every branch, with independently
variable finite a,c. No nonzero anchor is canceled in these branches.

When exactly one outside factor is pure G1, the independent boundary
checker constructs its one-variable K directly. In each chart, two
degree-18 coefficient minors have a degree-5 gcd supported entirely
on the explicitly forbidden det(H(x))*K_00(x) guard. Repeated exact
gcd removal leaves 1. Every one of the nine zero-middle supports has
univariate necessary-equation gcd 1 without any guard removal.

When both outside factors are pure G1, form
K_infinity=adj(G1)F4 adj(G1). The checker obtains
K_infinity,00=109375/194688 and a nonzero exact first 3-row
coefficient minor. Thus every projective middle coefficient vector
is excluded on this final chart.

Pure-G1 middle support is entrywise nonzero and is already included
in the homogeneous coefficient-rank arguments. Singular stages are
impossible by invertibility of F4. These branches cover the complete
projective family stated in the theorem.

## 5. Independent reproduction and limits

Run the four included independently authored checkers:

1. check_six_outer_minors.py
2. check_finite_outer_resultants.py
3. check_support_and_common_infinity.py
4. check_one_infinite_outer.py

The first reconstructs all rank-constraint coefficients. The second
checks the exact factor proof and modular Bézout/resultant lift. The
last two reconstruct and check all remaining supports and infinity
charts. Only the supplied JSON coefficient/divisor data are read;
no uploaded or constructor program is executed. A separate-directory
portable replay reproduces all exact result JSON files byte-for-byte.

This is a complete exclusion for a concrete N4 family. Failure at N4
is not an asymptotic FFT lower bound. The variable-pole positive
point, root-free/gauge-enlarged families, and unresolved full-product
Fourier recursions must retain their separate scopes.
