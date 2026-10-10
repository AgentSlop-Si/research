# Independent review of the corrected direct-axis criterion

10 October 2026. Verdict: **accept the corrected axis criterion and conditional fixed-root theorem; reject the automatic full-axis-rank shortcut.** The accepted 9N/5 Fourier signed-bank theorem is unchanged. This review makes no stronger uniform bank theorem and no historical-priority claim.

The reviewed author package is `research_cycle_1810/direct_axis_guard/`. Exact input hashes, this review's output hashes, and a machine-readable verdict are recorded in `REVIEW_RECEIPT.json` and `MANIFEST.sha256`. No predecessor program was imported or executed; all executable checks used the new `independent_axis_audit.py`. The author programs were inspected only as text and the author JSON files only as inert data.

## 1. Scope and result

The following statements are accepted under their stated hypotheses:

1. The quotient-algebra dual description of the physical axis dependence space.
2. Reciprocal coprimality and 2m > N−1 imply corank at most one, including for nonsquarefree polynomials and in characteristic two.
3. The symmetric Bézout condition and the modular-inverse support condition are each necessary and sufficient for corank one. The decisive sign is C = −B.
4. Adding or deleting a simple root 1 preserves the dependence space, provided the residual polynomial does not vanish at 1.
5. The rational counterexample family is genuinely infinite, reciprocal-coprime and squarefree, and has axis corank exactly one.
6. Saturation of the stated Fourier recurrence envelope forces the fixed root 1. Modular rank certificates at the nine listed pairs establish the characteristic-zero saturation required for that conclusion.
7. The 16 baseline records provide valid finite characteristic-zero lifting recipes using the existing whole-left construction. They do not prove a uniform existence result.

No blocking mathematical defect was found. A nonblocking coverage clarification is that the 112 deterministic trial records contain 82 distinct coefficient polynomials when counted separately within their 16 parameter pairs; repeated trial assignments occur at six pairs with one-dimensional monic affine kernels. The author calls these samples, not 112 distinct witnesses, so no theorem or certificate requires correction.

## 2. Duality, involution, and corank

For a monic g of degree m, with c = g(0) nonzero, the three blocks of the N-row matrix X_N(g) test respectively the coefficient vectors of A modulo g, the scalar A(1), and the coefficient vectors of J_N A modulo g. Here

J_N A = t^N A(1/t) + A(0)(1−t^N).

The constant coefficient remains A(0), while every positive coefficient at index a moves to N−a. Therefore J_N is an involution on polynomials of degree at most N−1 and preserves evaluation at 1. This proves the exact dual space

D_N(g) = {A : deg A ≤ N−1, g divides A, g divides J_N A, A(1)=0}.

No root evaluation or squarefreeness is needed.

Let H = t^m g(1/t), with gcd(g,H)=1. If A is in this space and A(0)=0, then g divides t^N A(1/t). Reversal in the Laurent polynomial ring, followed by removal of a power of t, implies H divides A: both g and H have nonzero constant coefficient, so t is coprime to them. Thus gH divides A. The strict degree inequality 2m > N−1 forces A=0.

Consequently evaluation at 0 injects D_N(g) into the scalar field, proving dim D_N(g) ≤ 1. Also J_N A−A belongs to D_N(g) and has constant 0. Hence every dependence satisfies J_N A=A. This argument does not divide by 2, and remains valid in characteristic two.

The squarefree Vandermonde explanation is valid only with its explicit squarefreeness hypothesis. Multiplication of each negative-node column by x_i^(−N) changes the rows a≥1 into powers of x_i^(−1), and differs from the ordinary Vandermonde matrix only at row 0. Reciprocal coprimality makes the nonzero nodes x_i, 1, x_i^(−1) distinct. The ordinary matrix has full row rank, and a change supported on one row has rank at most one. The quotient proof, rather than this distinct-node proof, supplies the nonsquarefree extension.

## 3. Signs, reversal grades, and the exact criterion

Put d=N−m and e=d−1. The degree hypothesis gives e<m. Coprimality implies g(1)≠0, so a dependence has the unique form

A=(t−1)gB, with deg B≤e−1.

Its constant coefficient is −cB(0). Define the reversal at the fixed grade e by B*=t^e B(1/t), even when B has smaller degree. Direct substitution gives

J_N A = −(t−1)[HB*−cB(0)S_N].

The sign before HB* is negative because (1/t−1)=−(t−1)/t. Thus g divides J_N A exactly when

HB*−cB(0)S_N = gC.

The leading terms cancel, so in fact deg C≤e−1; using only deg C≤e is harmless. Reversing at total grade N−1=m+e gives

gB−cB(0)S_N = HC*, with C*=t^e C(1/t).

Adding the two identities yields H(B*+C*)=g(B+C). Coprimality and deg(B*+C*)≤e<m force B*+C*=0, and hence C=−B. A nonzero dependence has B(0)≠0 by the injectivity already proved, so normalization gives

HB*+gB = cS_N, B(0)=1, deg B≤d−2.

Conversely this identity produces the nonzero dependence A=(t−1)gB, and the displayed formula directly gives J_N A=A. Evaluation at t=1 yields 2g(1)B(1)=Nc; this is not a contradiction and does not force B(0)=0.

Now let R be the degree-less-than-m remainder of cS_N H^(−1) modulo g. If a dependence exists, B*=R because deg B*≤e<m. Necessarily R(0)=0 and deg R≤e.

Conversely, suppose these two support conditions hold. Set B=rev_e(R) and C=(HR−cS_N)/g. Then deg B≤e−1 and deg C≤e. The same fixed-grade reversal argument forces C=−B. The constant coefficient of HR−cS_N=gC gives C(0)=−1, so B(0)=1 follows automatically. The Bézout identity and dependence follow. This also shows that R cannot be zero in the failure case. When d=1 the support condition would require R=0, so failure is impossible.

The criterion is therefore exactly

rank X_N(g)=N−1 if and only if R(0)=0 and deg R≤N−m−1;
otherwise rank X_N(g)=N.

The ordinary inverse's existence is only a coprimality statement. Its support is the extra obstruction; nonsingularity of an ordinary reciprocal Bézoutian does not remove it.

## 4. Counterexamples and the root-1 operation

For N=5, g=t³+t²+t+2 and A=t⁴+t−2, independent rational arithmetic confirms:

- gcd(g,rev_3(g))=1 and gcd(g,g')=1;
- A=(t−1)g, J_5 A=A and A(1)=0;
- X_5(g) has rank 4 and inverse remainder R=t;
- the displayed ordinary Bézout matrix has determinant 20, while Res(g,H)=−20.

For all integers n≥5 and r≥1, set N=nr and

g=2+t^r+⋯+t^((n−2)r), A=t^(N−r)+t^r−2.

With u=t^r, A=(u−1)g, J_N A=A, A(1)=0, and 2deg g>N−1. Also H−g=u^(n−2)−1. A common root would give u^(n−2)=1; g equals 2 when u≠1 and n when u=1. Thus coprimality holds in characteristic zero.

For P(u)=(u−1)g(u)=u^(n−1)+u−2, simultaneous P=P'=0 forces u=2(n−1)/(n−2), a positive rational number, and (n−1)u^(n−2)=−1, which is impossible. P, and hence g(u), is squarefree. Nonzero roots and characteristic zero make substitution u=t^r preserve squarefreeness. The corank bound and nonzero A then prove exact corank one for the entire family. This is an algebraic proof, not an extrapolation from examples.

If g=(t−1)h with h(1)≠0, the conditions h|A and A(1)=0 are equivalent to g|A; applying the same statement to J_N A proves D_N(g)=D_N(h). The simple-root condition matters. The criterion must use the degree of h and d_h=N−deg h after removal. The N=15 example h=t⁹+t⁶+t³+2 and g=(t−1)h has rank 14, so removal alone cannot rescue automatic full rank.

## 5. Conditional Fourier fixed root and characteristic-zero lifting

This conclusion uses exactly the recurrence setup and ranges in the cited whole-left envelope: odd N, primitive q, m≥(N−1)/2, and d=N−m≥4. Let V be its formal constrained triple space of dimension 4d−11, and let D(z)=∏_(j=2)^(d−1)(1−q^jz).

The triple (0,0,D) has the permitted degrees and satisfies the endpoint relation because D(q^(−(d−1)))=0. Its evaluation on the actual columns is the vector (D(q^k))_(k=0)^m. If the recurrence rank is 4d−11, its scaled row space has the same dimension as V and is contained in eval(V); therefore it equals eval(V). Undoing the invertible column scaling by D(q^k) puts the all-ones vector in the original row space. Every kernel polynomial consequently vanishes at 1.

There is no inference about nonsaturated cases, the multiplicity of the fixed root, or the entire characteristic-zero kernel gcd.

Independent reconstruction verified rank 4d−11 at the nine listed pairs: (35,9), (45,11), (51,12), (55,8), (55,13), (65,9), (65,15), (75,10), (75,17). At every pair, the supplied prime and q have the required exact order, and the displayed rank minor is nonzero. The cyclotomic specialization is valid and all Gaussian denominators are units. Therefore the nonzero minor supplies the characteristic-zero lower rank bound, while the analytical envelope supplies the matching upper bound. This justifies characteristic-zero saturation and the exact factor t−1.

The kernel gcd t−1 recorded over each finite field remains explicitly modular data. The verified baseline has a simple root 1 modulo p; after the exact characteristic-zero factor has been established, monic division commutes with specialization. A nonzero residual reciprocal resultant modulo p therefore certifies the corresponding characteristic-zero residual is reciprocal-coprime.

For all 16 baselines, the selected defining minor uses only nonleading coefficient columns. Fixing the other coefficients to the recorded integer residues and the leading coefficient to 1 defines a unique selected-equation solution over Q(q), regular at the chosen prime. The exact analytical rank bound makes every remaining recurrence redundant. The nonzero constant, squarefree resultant, and axis minor lift as nonvanishing conditions. This verifies the recipes without claiming that arbitrary finite-field solutions lift. No characteristic-zero coefficient solve was numerically approximated or substituted for this argument.

## 6. Independent executable controls

`INDEPENDENT_EXACT_CONTROLS.json` records a passing run of the new audit program. It rebuilds the Gaussian coefficients by q-Pascal recursion rather than the author's product formula, and obtains R by a multiplication-operator linear solve in F_p[t]/g rather than the author's polynomial extended Euclidean routine.

Checked against every author record:

- all 16 recurrence matrices and row labels;
- exact prime/order checks, ranks, nullspace dimensions and basis independence;
- all recurrence equations, selected defining minors, modular kernel gcds, derivative and reciprocal gcds;
- all 112 axis ranks and every recorded full-rank axis minor;
- all 111 applicable inverse-remainder results, including the simple-root-1 cases;
- all 16 baseline nonzero/squarefree/full-axis guards;
- the all-ones row functional in all nine rank-saturated cases.

The single inapplicable record has zero constant and is correctly excluded from nonzero-node use. Further independent controls include the six author rational counterexamples, an even-order family case N=12, the N=15 root-1 variant, and the nonsquarefree rational polynomial (t−2)³ at N=5.

An exhaustive supplementary grid over F2 (N≤9), F3 (N≤6), and F5 (N≤5), with 2m>N−1 and m<N, contains 694 admissible reciprocal-coprime polynomials. All agree with the criterion; 46 are nonsquarefree and 14 have corank one. A separate nonsquarefree F3 example g=2+t³+t⁶+t⁹ at N=15 has rank 14 and also matches the criterion. These finite checks support implementation accuracy but are not used as proofs of the universal statements.

## 7. Literature and boundaries

The primary sources cited in the author note were checked directly. Curgus–Dijksma establishes the classical equality of Bézoutian nullity and gcd degree and describes companion/quotient connections. Lubachevsky's abstract treats prescribed-right-hand-side polynomial Bézout solves. Dym–Young discusses Hermitian Schur–Cohn root-location constructions and scalar Bézoutians. These support the classical-tool comparison, not the new restricted-axis implication. The reversal used here has no coefficient conjugation, and no Hermitian inertia claim is being made.

- https://faculty.curgus.wwu.edu/Papers/BezoutianNote3.pdf
- https://arxiv.org/abs/math/0104118
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5AB9F1B5788EC10C3C510CB2218B26FE/S0013091500004806a.pdf/schurcohn_theorem_for_matrix_polynomials.pdf

The automatic full-rank lemma and its proposed 7N/4 consequence remain withdrawn. The corrected corank-one theorem does not establish generic full axis rank in an arbitrary Fourier recurrence kernel. The nine forced-root cases and 16 finite lifting recipes do not establish a uniform stronger bank bound. The accepted 9N/5 theorem and all source files listed in the author bindings were verified unchanged.
