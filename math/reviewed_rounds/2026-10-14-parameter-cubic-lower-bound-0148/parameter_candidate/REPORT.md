# A degree-27 parameter gate for five-node forced windows

14 October 2026. New exact symbolic result; not yet independently reviewed.

## Result

Keep N=11, q=13, characteristic 23, the literal Fourier target, and exactly one effective cross-sign alpha node y in (-,+). Let K be any field containing F23 and take y in K*. For the five forced positive-exponent windows derived below, the following are equivalent:

1. They possess a common monic annihilator of degree at most five, using every recurrence window available at that degree.
2. They possess a monic degree-five annihilator.
3. H(y)=0, where

    H(y) = (y-4)(y-15) P7(y) P18(y),

    P7(y) = y^7+3y^6+6y^5+3y^4+7y^3+16y^2+4y+1,

    P18(y) = y^18+3y^17+18y^16+16y^15+12y^14+22y^13
           +9y^12+19y^11+9y^10+18y^9+12y^8+11y^7
           +20y^6+6y^5+13y^4+11y^3+6y^2+2y+11.

Both P7 and P18 are irreducible over F23. H is squarefree, and H(0) is nonzero. At each of its 27 roots in an algebraic closure, the monic quintic is unique, has nonzero constant term, and is separable. There is never a common monic annihilator of degree at most four.

The same windows admit a representation on five distinct nonzero nodes in K if and only if H(y)=0 and the unique quintic splits over K. This is a necessary-window result. It neither produces a full original-bank representation nor proves any extension-field bank minimum.

A particularly useful specialization is

    y=15:
    h15(t)=t^5+12t^4+17t^3+14t^2+t+14
          =(t-3)(t-21)(t^3+13t^2+13t+13),

where the cubic is irreducible over F23. Thus this forced-window obstruction to five nodes disappears over F_(23^3). It remains a distinct task to test the complete bank sectors, including the independent opposite cross node z and all other coefficient coordinates.

## 1. Original grammar and normalization remain unchanged

The original bank is

    B_(epsilon,delta)(alpha,beta;w)
      =(1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j)T^delta)^(-1),
    Delta=1-alpha^11-beta^11 != 0,

with S e_t=e_(t+1 mod 11), T e_t=13^t e_t, and target F[k,t]=13^(-kt).

All formulas here remain valid over any extension K of F23: q=13 still has order eleven, 11 is invertible, and the Gaussian coefficients lie in the prime field. Fresh code independently extracts the literal target Weyl coefficients and counts all binary noncommutative words of each length up to eleven. This proves the degree-eleven mixed-coefficient vanishing and recovers

    c_F(a,b)=18 f(a,b),  f(a,b)=13^(3(a+b)^2).

Set r=[epsilon a]_11, ell=[delta b]_11 and G_(epsilon,delta)(a,b) equal to the Gaussian ordered-word coefficient when r+ell<=10, and zero otherwise. A bank contributes

    18 A_b alpha^r G_(epsilon,delta)(a,b),
    A_b=beta^ell/(11 Delta 18) sum_j w_j 13^(epsilon b j).

This expression never divides by beta or alpha. Arbitrary legal beta, including zero, is already absorbed into the sector amplitude. No beta=1 assumption is used in the necessary gate.

Grouping equal-alpha banks by their sector-amplitude vectors preserves necessary conditions, including arbitrary cancellations. A zero-alpha ++ group contributes zero in the positive-exponent windows. Repeated physical banks at a node do not supply derivative atoms or repeated-root degrees of freedom. Bank counts still count actual physical summands, not grouped nodes.

The sole-support coordinate (10,1) excludes y=0. For each b=1,...,5, the sole-support coordinate (11-b,b) forces the grouped (-,+) amplitude

    T_b(y) = 1/[y^b G_-+(11-b,b)].

For b<=a<=10-b both negative-delta orientations vanish, and G_++(a,b) is nonzero. Hence every legal full representation must satisfy

    v_b(a;y)
      = [f(a,b)-T_b(y)y^(11-a)G_-+(a,b)]/G_++(a,b)
      = u_(b,a)-d_(b,a)y^(11-a-b)
      = sum_(x in X) A_(b,x) x^a,

where X is the set of distinct nonzero effective ++ nodes. The opposite cross node z is not identified with y. Reflection yields the same necessary test separately for the -- support with parameter z.

## 2. Exact polynomial input

Put s_(b,j)(y)=v_b(b+j;y), for 0<=j<L_b=11-2b. The rows below list (u,d,exponent) in increasing a beginning at a=b; each moment is u-d*y^exponent, modulo 23.

    b=1: (19,0,9), (19,17,8), (10,16,7), (12,22,6),
         (21,2,5), (4,8,4), (2,7,3), (9,1,2), (5,5,1)
    b=2: (21,0,7), (9,20,6), (3,1,5), (1,12,4),
         (19,8,3), (17,4,2), (6,14,1)
    b=3: (6,0,5), (19,8,4), (5,11,3), (9,20,2), (20,16,1)
    b=4: (13,0,3), (3,2,2), (8,4,1)
    b=5: (14,0,1).

For a monic quintic h(t)=h0+h1*t+...+h4*t^4+t^5, its six recurrence equations are

    sum_(k=0)^5 h_k s_(b,j+k)(y)=0,

for (b,j)=(1,0),(1,1),(1,2),(1,3),(2,0),(2,1). Shorter windows impose no degree-five recurrence. Define the 6-by-6 matrix E with these rows [s_(b,j),...,s_(b,j+5)], in that order, and A to be its first five columns. Then the system is A(h0,...,h4)^T=-E[:,5].

If an actual support has at most five distinct nonzero nodes, its squarefree support polynomial annihilates every available window. Multiplying it by t^(5-m) for support size m yields a monic quintic satisfying these six rows. This padding creates no actual bank and is only an algebraic necessity argument. Alternatively, ordinary nonzero-node padding is available over any such field, since it contains at least 22 nonzero elements.

## 3. Determinant, all rank cases, and the quintic

Fresh polynomial arithmetic computes determinants by the signed-permutation formula, without symbolic rational simplification. The exact determinant is

    det(E)=15 H(y).

Its coefficients in ascending powers of y are

    [10,16,22,10,15,1,9,1,1,8,12,18,14,14,
     15,17,22,22,1,6,21,9,15,16,5,7,12,15].

Let M_i(y) be the 5-by-5 minor of A formed by omitting row i, using zero-based indexing. All six are retained in RESULTS.json. Their degrees are 22,25,26,27,26,27. Exact extended Euclidean certificates give

    gcd(M_0,M_1)=1,
    gcd(M_0,...,M_5)=1,
    gcd(M_0,det(E))=1.

The saved Bézout coefficients explicitly verify each asserted unit ideal used by the code. In particular, no algebraic value of y makes all coefficient minors vanish. Thus rank A(y)=5 for every y in every extension, including formal y=0. There are no unhandled rank-deficient specializations. The augmented system is compatible exactly when det(E)(y)=0; a compatible solution is unique.

One Cramer formula works at every compatible parameter: omit row zero, set D=M_0, and let N_k be the determinant obtained by replacing column k of this 5-by-5 matrix with the negative sixth column of E. Then

    h_y(t)=t^5+sum_(k=0)^4 [N_k(y)/D(y)] t^k.

For reference, D has ascending coefficients

    [8,0,10,2,1,19,4,6,7,18,0,12,19,18,10,13,9,4,16,17,6,15,17].

All five N_k are provided exactly in RESULTS.json, with degrees 18,19,20,21,22. Substitution into all six recurrence equations gives polynomial residuals divisible by det(E), checked without evaluation or approximate arithmetic.

Factorization is obtained with installed SymPy 1.14.0, then independently certified by newly authored arithmetic: multiplication reconstructs det(E); each factor passes the finite-field irreducibility criterion using iterated Frobenius residues and Bézout gcd identities; and gcd(det(E),det(E)')=1. No assertion of irreducibility relies solely on the factorization library's returned label.

## 4. Zero roots, repeated roots, and lower degrees

The code proves gcd(det(E),N_0)=1 by an exact Bézout identity. Consequently every compatible quintic has h0!=0: zero is never one of its roots.

In each of the four fields F23[y]/(y-4), F23[y]/(y-15), F23[y]/P7 and F23[y]/P18, fresh quotient-field arithmetic computes the Cramer quintic and its t derivative. It obtains gcd(h,h')=1 in every case. Full Euclidean chains and Bézout identities are retained in ROOT_CERTIFICATES.json. This is four bounded symbolic field computations, with no enumeration of an extension field. Since the parameter factors are irreducible and exhaust det(E), this proves separability for every one of the 27 compatible parameter values.

If a common monic annihilator g of degree m<5 existed, t^(5-m)g would satisfy the degree-five system and have zero constant term. Uniqueness would force it to equal h_y, contradicting h_y(0)!=0. If det(E)(y)!=0 no monic quintic exists at all. Thus no parameter has an annihilator of degree at most four; there are no lost smaller-support cases.

When h_y splits in K, its five roots are distinct and nonzero. For b=1,2, fit the first five moments by the invertible Vandermonde matrix on those roots. Both the fitted sequence and the supplied sequence obey the same monic order-five recurrence, so all later moments agree. For b=3,4,5 the window has at most five moments and its rectangular Vandermonde matrix has full row rank, so it can also be fit. Converting coefficients of x^j to coefficients of x^(b+j) is legal because x!=0. Hence splitting is sufficient for a common five-node realization of these windows alone. Conversely, a five-node realization yields its split product annihilator, which must be h_y. This explains precisely the extra root condition beyond det(E)=0.

## 5. All 22 base-field specializations

Every moment value, 6-by-6 recurrence matrix, coefficient rank, signed-right-hand-side row reduction, surviving polynomial and nonzero-root list was compared against BOTH source censuses. All 22 nonzero parameter values match exactly.

For every y in F23*, rank A=5. Twenty systems are incompatible. Only the following two quintics survive:

    y=4:
    h4(t)=t^5+8t^4+t^3+18t^2+4t+6.
    It is irreducible over F23 and has no F23 roots.

    y=15:
    h15(t)=t^5+12t^4+17t^3+14t^2+t+14
          =(t-3)(t-21)(t^3+13t^2+13t+13).
    The cubic is irreducible; the only F23 roots of h15 are 3 and 21.

Irreducibility certificates are saved for the quintic at y=4 and the cubic at y=15. Neither provides five distinct nonzero F23 roots. The accepted base-field no-five-node conclusion is therefore recovered exactly. Formal y=0 has det(E)(0)=10 and is incompatible, in addition to being disallowed by the original sole-support equation.

## 6. What extension changes are and are not established

There are two different ways extensions matter:

- Fixed base-field parameters can acquire support roots. At y=4, h4 first splits over F_(23^5). At y=15, h15 first splits over F_(23^3). All roots are nonzero and simple. More generally these respective quintics split over F_(23^n) exactly when 5 divides n or 3 divides n. These are statements about the stated quintics and forced windows, not full-bank constructions.
- New admissible parameter values can appear. The seven roots of P7 first become available in F_(23^7), and the eighteen roots of P18 first become available in F_(23^18). In F_(23^n), these new parameter orbits occur only if 7 divides n or 18 divides n, respectively. Their corresponding quintics are already proved separable with nonzero constant term, so each splits over some finite further extension. Their support-splitting degrees were not computed here.

Extending the field cannot rescue a fixed y for which det(E)(y) is nonzero: incompatibility of this prime-field linear system persists. For example, the base-field singleton nodes 7,10,12 that permit six-node supports do not thereby acquire a degree-five annihilator after extension while y is held fixed.

This report does not classify full-bank solvability over any extension. It does not test a twelve-bank candidate, require y=z, solve omitted coefficient sectors, compute all new-parameter support-splitting degrees, allow extra cross nodes, change q, or claim an unrestricted bank minimum. Passing this gate merely identifies a necessary obstruction that can disappear; complete original-bank attainability remains unestablished.

## 7. Reproducibility and audit boundaries

Only newly written scripts were executed. The reports and JSON censuses in the two historical source directories were read as inert evidence. No historical uploaded code was executed, imported, or compiled. No external writes or existing research-file edits were made. The code imports only standard Python packages, installed SymPy for factorization, and the newly authored local polynomial module.

From the task workspace root, reproduce with

    python -I parameter_gate_candidate/fresh_parameter_gate.py \
      --out parameter_gate_candidate/replay
    python -I parameter_gate_candidate/certify_parameter_roots.py \
      parameter_gate_candidate/replay

SOURCE_HASHES.json binds the six input documents/data sources. RESULTS.json retains exact polynomials, all six minors, Bézout coefficients, Cramer numerators, base-field systems and row reductions. ROOT_CERTIFICATES.json retains all irreducibility, constant-term, separability and cross-census certificates. Replay records bind deterministic outputs; timing is excluded from byte equality. Model-token usage is unknown.

One development assertion initially compared the historical positive final moment column against the negated right-hand side; this was an input-format mismatch, corrected before the successful runs. The actual moment, solution, and row-reduction values were unchanged. SymPy printed a modular-integer ordering deprecation warning during factorization; it did not affect exact outputs. Neither incident is hidden in the audit metadata.

The bounded one-parameter task is complete. Independent review is required before promoting this new symbolic result to accepted status.
