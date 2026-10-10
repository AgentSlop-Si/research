# Direct axis guard: a rejected shortcut and an exact replacement

10 October 2026. New author derivation and fresh controls, pending independent review. The accepted 9N/5 Fourier signed-bank theorem is unchanged. No inherited program was executed or imported.

## 1. Main findings

1. Reciprocal coprimality and degree greater than half the axis length do **not** imply full axis rank. A squarefree rational counterexample already occurs at N=5, and there is an infinite counterexample family.
2. Those hypotheses do imply axis corank at most one. The remaining obstruction is an explicit constrained reciprocal Bézout equation, equivalently a support test on one modular inverse.
3. For the Fourier recurrence kernel, attaining the refined rank bound 4d−11 forces the fixed root 1. Thus strict reciprocal coprimality of the original g is impossible in these rank-saturated cases. Removing the simple root 1 preserves the axis dependence space, but does not remove the one-dimensional obstruction.
4. Bounded fresh controls give 112 recurrence-kernel samples at 16 specified parameter pairs. The corrected criterion applies to 111 samples and agrees with direct axis elimination in all 111. Six rational counterexamples have axis rank exactly N−1. All 16 baseline kernel samples have nonzero constant, are squarefree, and have full axis rank modulo their specified primes. Their rank-saturated defining systems provide characteristic-zero lifting recipes. No uniform stronger bank bound follows from this finite list.

## 2. Axis matrix and exact duality

Let F be a field, N≥2, and let g∈F[t] be monic of degree 1≤m≤N−1 with c=g(0)≠0. Put d=N−m and let p_j be the coordinate vector of t^j modulo g. Write X_N(g) for the N by (2m+1) matrix whose row indexed by a is

    (p_a, 1, p_[-a]_N),  0≤a<N.

Define the linear involution on F[t] of degree at most N−1 by

    J_N A(t)=t^N A(1/t)+A(0)(1−t^N).

It fixes the constant coefficient and exchanges coefficients a and N−a for 1≤a<N. Consequently J_N²=I and (J_N A)(1)=A(1).

The row-dependence space of X_N(g) is exactly

    D_N(g)={ A : deg A≤N−1, g|A, g|J_N A, A(1)=0 }.

This follows simply by taking the dot product with each of the three column blocks. The statement is valid for repeated roots as a quotient-algebra assertion. Squarefreeness is needed to identify moment coordinates with distinct physical root-node columns, as in the accepted construction.

## 3. Correct reciprocal-coprime theorem

Assume

    H(t)=t^m g(1/t),   gcd(g,H)=1,   2m>N−1.

Then:

- dim D_N(g)≤1, so rank X_N(g) is either N or N−1;
- every A∈D_N(g) satisfies J_N A=A;
- rank X_N(g)=N−1 if and only if there is a polynomial B with

      deg B≤d−2,  B(0)=1,
      H(t) t^(d−1)B(1/t)+g(t)B(t)=c S_N(t),       (1)

  where S_N=1+t+⋯+t^(N−1).

When d=1 the stated B-space is zero, so the axis is full rank.

### Corank and involution proof

If A∈D_N(g) and A(0)=0, the second divisibility is g|t^N A(1/t). Reversing gives H|A, since g and H have nonzero constant coefficients. Hence gH|A. Its degree 2m exceeds N−1, forcing A=0. Thus A↦A(0) is injective on D_N(g), proving the corank assertion.

The space D_N(g) is J_N-invariant. The element J_N A−A belongs to it and has zero constant coefficient, so it is zero. No characteristic-two exclusion is needed for this argument.

### Independent squarefree Vandermonde interpretation

When g is squarefree, let x_1,…,x_m be its roots in a splitting field. Scale the negative-axis column belonging to x_i by x_i^(−N). In rows a≥1 its entry becomes (x_i^(−1))^a. In row 0 its entry is x_i^(−N), rather than 1. Thus the scaled root-coordinate axis matrix differs in only row 0 from the ordinary Vandermonde matrix on

    {x_1,…,x_m, 1, x_1^(−1),…,x_m^(−1)}.

These 2m+1 nodes are distinct under squarefreeness and reciprocal coprimality. Since 2m+1≥N, the Vandermonde matrix has row rank N. A perturbation supported on one row has rank at most one, proving axis corank at most one independently. The inverse-remainder criterion below says exactly when this rank-one correction loses one rank. This interpretation uses squarefreeness; the preceding quotient-algebra proof does not.

### Signs and degrees in the Bézout equation

Coprimality implies g(1)≠0. Therefore A(1)=0 and g|A give

    A=(t−1)gB,   deg B≤d−2,   A(0)=−cB(0).

Use reversal at the explicit grade d−1:

    B*=t^(d−1)B(1/t).

Direct substitution, including the sign from 1/t−1, gives

    J_N A=−(t−1)[HB*−cB(0)S_N].

Thus g|J_N A is equivalent to

    HB*−cB(0)S_N=gC,   deg C≤d−1.                (2)

The leading terms actually cancel on the left, so deg C≤d−2, but the weaker bound suffices. Reverse (2) at total grade N−1 and put C*=t^(d−1)C(1/t):

    gB−cB(0)S_N=HC*.                            (3)

Equations (2) and (3) imply

    H(B*+C*)=g(B+C).

Because d−1<m and gcd(g,H)=1, the polynomial B*+C* of degree at most d−1 must vanish. Therefore **C=−B**, not C=B. This is the sign error in the rejected automatic-rank argument. Equation (2) now becomes (1) after normalizing B(0)=1. A nonzero B cannot have B(0)=0, since then g|HB* and deg B*<m force B*=0.

Conversely, (1) gives a nonzero A=(t−1)gB with J_N A=A, g|A and A(1)=0, so it produces an axis dependence.

Evaluating the correct equation at 1 gives

    2g(1)B(1)=Nc,

not B(0)=0. In characteristic zero there is no contradiction.

## 4. One modular-inverse support test

The preceding theorem has an exact computational form. Compute the unique remainder

    R = (c S_N H^(-1)) mod g,   deg R<m.          (4)

The inverse exists precisely because gcd(g,H)=1. Then

    rank X_N(g)=N−1
       if and only if R(0)=0 and deg R≤d−1.      (5)

Otherwise rank X_N(g)=N. A failure certificate is B=t^(d−1)R(1/t), and then A=(t−1)gB. In the failure case B(0)=1 follows automatically.

Necessity follows from (1), because B*=R and B* has zero constant coefficient. Conversely suppose the support test holds. Define B as above and C=(HR−cS_N)/g, of degree at most d−1. Reversing gives gB−cS_N=HC*. As before, coprimality and the degree gap imply C=−B. Evaluate HR−cS_N=gC at 0: since R(0)=0, one obtains C(0)=−1, so B(0)=1. This proves (1).

Thus reciprocal coprimality makes a classical polynomial-inverse solve possible; the additional low-support condition, rather than invertibility alone, decides axis failure.

## 5. Exact counterexamples, including the simple-root-1 variant

For N=5 and m=3 take

    g=t³+t²+t+2,   H=2t³+t²+t+1,
    A=t⁴+t−2=(t−1)g.

Here gcd(g,H)=1, g is squarefree, g(0)=2, and 2m=6>N−1=4. Nevertheless J_5 A=A and A(1)=0. Therefore X_5(g) has rank 4, not 5. Equation (1) has B=1 and the inverse remainder (4) is R=t.

This is an infinite characteristic-zero counterexample family. For integers n≥5 and r≥1 put

    N=nr,  m=(n−2)r,
    g(t)=2+t^r+t^(2r)+⋯+t^((n−2)r),
    A(t)=t^(N−r)+t^r−2=(t^r−1)g(t).

Then J_N A=A, A(1)=0, and 2m>N−1. Write u=t^r. The reciprocal difference is H−g=u^(n−2)−1. At a common root, u^(n−2)=1; when u≠1 the value of g is 2, and when u=1 its value is n. Thus g and H are coprime in characteristic zero.

To see squarefreeness, let P(u)=(u−1)(2+u+⋯+u^(n−2))=u^(n−1)+u−2. A repeated root would satisfy P=P'=0, which yields u=2(n−1)/(n−2)>0 and also (n−1)u^(n−2)=−1, a contradiction. The root u=1 is simple, and g has no zero root, so substitution u=t^r preserves squarefreeness.

Taking n=N,r=1 gives a counterexample for every odd N≥5. Taking n=5 and odd r≥3 gives d=2r≥6 within the nontrivial high-gap regime. The fresh rational controls cover (N,m)=(5,3),(7,5),(9,7),(15,9),(25,15),(35,21), each with axis rank exactly N−1.

If g=(t−1)h with h(1)≠0, then

    D_N(g)=D_N(h).

Indeed g|A is equivalent to h|A and A(1)=0, and J_N preserves evaluation at 1. Thus adding the simple root 1 does not change the dependence space. In particular h=t⁹+t⁶+t³+2 at N=15, followed by g=(t−1)h of degree 10, refutes the proposed automatic-rank variant based on reciprocal coprimality of h. The corrected theorem and test apply to h with its own degree and d=N−deg h.

## 6. A forced reciprocal base point in the Fourier kernel

Use exactly the recurrence matrix A_(N,m) and the scaled polynomial envelope from WHOLE_LEFT_RANK_ENVELOPE.md. Its formal constrained triple space V has dimension 4d−11, and its evaluation contains the scaled row space. Let

    D(z)=∏_(j=2)^(d−1)(1−q^jz),
    z*=q^(−(d−1)).

The triple (E,O,R)=(0,0,D) lies in V: it respects the degree bounds and endpoint relation because D(z*)=0. Its actual evaluation is (D(q^k))_(k=0)^m.

**Conditional fixed-root theorem.** If rank A_(N,m)=4d−11, then every g∈ker A_(N,m) satisfies g(1)=0.

Proof: the scaled row space has dimension 4d−11 and is contained in the evaluation of V, whose dimension is at most 4d−11. They are therefore equal. The displayed D-evaluation is in the scaled row space. Undo the invertible column scaling by D(q^k); the all-ones vector is in the original row space. Its annihilation on the kernel is exactly g(1)=0.

This is an exact characteristic-zero statement whenever rank saturation has been proved. It does not assert a forced root when the rank is smaller. In particular it does not assert that the kernel's entire fixed divisor is t−1 without a separate argument.

The fresh controls establish this rank saturation by a nonzero minor modulo the listed prime at the following nine pairs:

    (N,d)=(35,9),(45,11),(51,12),(55,8),(55,13),
          (65,9),(65,15),(75,10),(75,17).

The modular kernel gcd is t−1 at each of these pairs. That observation is recorded as modular data, separately from the exact forced-root theorem. Every baseline polynomial at these pairs has a simple root 1 modulo p and, after dividing it out, has reciprocal-coprime residual polynomial of degree greater than (N−1)/2.

## 7. Bounded exact controls and lifting boundary

The new file fresh_axis_controls.py constructs the Gaussian coefficients, the whole-left sequences, and all recurrence rows directly from their mathematical definitions. It does not load any predecessor program. It uses exact modular arithmetic for 16 fixed pairs:

    (13,5),(17,6),(21,4),(27,4),(35,5),(35,9),
    (45,7),(45,11),(51,7),(51,12),(55,8),(55,13),
    (65,9),(65,15),(75,10),(75,17).

For each pair it tests exactly seven deterministic monic coefficient choices. Prime selection is bounded to p=kN+1 with 1≤k≤200; every selected q is checked to have exact order N. The output records every recurrence row, kernel basis, defining pivot minor, polynomial coefficients, squarefree and reciprocal gcds, axis pivot columns and determinant, and the independent modular-inverse test. The six rational counterexample axis ranks are computed separately over Q.

All 16 systems attain the applicable analytical bound min((d−1)(d−2)/2,4d−11), with a nonzero defining minor involving only nonleading columns. Each baseline has every guard needed for the accepted whole-left lifting method. Specifically, define its characteristic-zero polynomial by fixing the nonpivot coefficients to the listed integer residues, setting the leading coefficient to 1, and solving the displayed selected equations over Q(q). All denominators and the defining minor are units at the selected reduction, and the analytical bound makes all other rows dependent on the selected rows. Thus the polynomial satisfies every recurrence over Q(q). The nonzero constant, squarefree resultant, and axis minor survive in characteristic zero.

At the nine refined-rank-saturated pairs, the exact fixed-root theorem first ensures divisibility by t−1. Polynomial division by this monic factor commutes with reduction. The residual reciprocal gcd 1 modulo p therefore certifies a nonzero residual reciprocal resultant in characteristic zero. This establishes existence of suitable reciprocal-coprime residuals at these **specified finite pairs**, not at all larger orders.

The corrected criterion applies to 111 of the 112 samples and exactly agrees with direct axis ranks. One sample at (N,d)=(21,4) has zero constant coefficient and is explicitly outside the criterion's hypotheses; its quotient-algebra axis calculation is still recorded, but it is not a legal nonzero-node bank witness. The controls are finite corroboration and reproducible lifting data, not an asymptotic nonvanishing proof.

## 8. Classical Bézoutian connection and non-novelty boundary

The ordinary polynomial Bézoutian of g and H is the coefficient matrix of

    [g(x)H(y)−g(y)H(x)]/(x−y).

Its nonsingularity is the classical coprimality test. Curgus–Dijksma, *A proof of the main theorem on Bezoutians*, proves the equality between Bézoutian nullity and gcd degree, and discusses the companion/quotient-algebra relationship. Lubachevsky's inverse Sylvester-matrix work likewise treats solving polynomial Bézout equations with a prescribed right-hand side. These are established tools, not new axis theorems:

- https://faculty.curgus.wwu.edu/Papers/BezoutianNote3.pdf
- https://arxiv.org/abs/math/0104118

The present bridge is the particular right-hand side cS_N and the restricted reversal/support condition in (1)–(5). For the N=5 counterexample the ordinary Bézout matrix, in ascending monomials, is

    [ −1  −1  −3 ]
    [ −1  −3  −1 ]
    [ −3  −1  −1 ],

with determinant 20, while the physical axis has rank 4. Thus even an invertible reciprocal Bézoutian does not certify full axis rank.

Classical Schur–Cohn constructions connect reciprocal polynomial Bézoutians to unit-circle root location; see the primary scalar-matrix discussion in *A Schur-Cohn theorem for matrix polynomials*:

- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5AB9F1B5788EC10C3C510CB2218B26FE/S0013091500004806a.pdf/schurcohn_theorem_for_matrix_polynomials.pdf

Here H is the purely algebraic reversal t^m g(1/t), with no coefficient conjugation and no Hermitian inertia or stability assertion. The earlier C03/resultant-refinement notes share the reciprocal-polynomial and quotient-invariant toolkit; their diagonal matrix-pencil resultant is a different object and supplies no missing axis implication. No historical-priority claim is made.

## 9. Frozen conclusions and stopping point

The automatic reciprocal-coprime axis lemma and its proposed 7N/4 consequence are rejected. The accepted 9N/5 theorem remains unchanged. The exact corank-one criterion and the conditional forced-root theorem are separate bounded results. No evaluation-functional theorem at N≥8d−11 is claimed here, and no finite sample or expected dimension is promoted to a uniform axis proof.
