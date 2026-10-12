Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery details are omitted; mathematical source identity, assumptions, costs and limitations are preserved. Original source-report SHA-256: a29e931cb12b113811b564186dd2e9f6dd4416bef78de1f811379b9558d0d092.

Terminology clarification in this derivative: unitary describes each cycle operator U_j, not its Green resolvent (I−U_j)^(-1).

# Independent review: four routed unitary-cycle inverses at N=4

Date: 2026-10-12 UTC. Verdict: **ACCEPT SCOPED**.

The sealed candidate proves the entire negative-sign, unnormalized F4 by one
sum of four resolvents (I−U_j)^(-1), where each U_j is a unitary weighted
Hamiltonian-cycle operator, with noncollinear complex scalar coefficients and invertible outer diagonal
calibration only. It is an exact existence theorem about the unique root in the
specified 18-dimensional real box. The printed center is not the exact root.
There is no minimum-term, all-length, FFT speedup, finite-bit implementation, or
historical-priority conclusion.

## 1. Input and independence

Candidate archive: NF06_N4_Four_Route_Unitary_CANDIDATE_2026-10-12.zip.

SHA256: 0c6667dbc1128c1e351eed0cabeedaa7a667c780b5490b5dc97a6678fe38104c.

Certificate SHA256:
635966b5451f325c50293ca17a58045b7f24b7b54e7ec60eddcb76a489a4c725.

All 26 entries in the candidate's content manifest match their exact bytes and
lengths; archive CRC passes. Candidate proof, checker, controls, costs and source
comparisons were read as inert content. None of the candidate Python programs,
optimizer, refinement code, or historical source programs was imported or run.

The fresh verifier uses Python's standard library only. Its arithmetic consists
of integer intervals on the grid 10^-125, exact integer floor/ceiling rounding,
and rational Taylor remainder bounds for sine and cosine. It does not depend on
mpmath, sympy, binary floating-point transcendental evaluation, or the author's
outward-rounding implementation. Floating diagnostics in the receipts are not
used to decide any mathematical assertion.

Rather than matrix powers and forward automatic differentiation, the fresh
checker uses explicit cyclic-route positions and independently derived analytic
derivatives. The submitted exact center and preconditioner are data, not trusted
claims: the full contraction inequalities are re-established independently.

## 2. Legal network and complete entry formula

The four exact routes are 0123, 0132, 0213 and 0231. Each visits all four vertices
once, and the directed cycles are distinct. There are 19 real coordinates, with
x16 frozen at the exact rational -4.321569660664867; the other 18 range in the
closed infinity-norm box of radius 10^-40 around the supplied exact decimals.
The center, radius, active-coordinate order, frozen coordinate, Fourier sign,
route tuple, and 18-by-18 preconditioner dimensions are checked explicitly.

For each route, let p(v) be the vertex's position. With real vertex phases theta
and real holonomy phase t, the edge from u to v is exp(i(theta_v-theta_u)),
except that the closing edge also contains exp(it). Thus every edge has modulus
exactly one, and the product of all four edges is h=exp(it). This is a symbolic
identity on the entire real domain, not an inference from approximate moduli.
The weighted permutation W is consequently unitary. Its inverse resolvent G is
not itself claimed to be unitary.

Every entry has the exact formula

    G[i,j] = exp(i(theta_i-theta_j + [p(i)<p(j)] t)) / (1-exp(it)).

In particular the diagonal carries the zero-length path and is 1/(1-h), not
h/(1-h). The formula follows by the unique directed path of length 0,1,2,3
from j to i and the geometric identity W^4=hI. The verifier independently uses
this formula for all 64 branch entries. All poles are excluded throughout the
box. There is no product of sums, interstage diagonal, inner endpoint mask,
permutation calibration, dense endpoint, or zero edge.

The coefficients are c0=1 and three independent complex pairs in the declared
coordinate order. Nonzeroness is enclosed. In particular Im(c2)=x16 is nonzero
exactly, so c0 and c2 cannot lie on one real line through the origin. The
real-collinear-coefficient exclusion does not apply. This does not relax the
unit-modulus condition on edges.

## 3. All 16 Fourier entries and the 18 real equations

Set S=sum_b c_b G_b. Every first-row and first-column entry is bounded away from
zero on the box. Nine complex residuals, in i-major order for 1<=i,j<=3, are

    f_ij = S[i,j] S[0,0] / (S[i,0] S[0,j]) - (-i)^(ij).

The real equation vector is the nine real parts followed by the nine imaginary
parts. Its derivative columns follow the specified 18 active real coordinates.
The fresh evaluator checks this convention directly, not by rank alone.

At a zero, choose L_i=1/S[i,0] and R_j=S[0,0]/S[0,j]. For i=0 or j=0 the
calibrated entry is identically one. For the nine remaining pairs it is the
corresponding target by the root equations. Explicitly, the full target is

    1  1   1   1
    1 -i  -1   i
    1 -1   1  -1
    1  i  -1  -i.

This proves the action on every complex input vector. In addition, the fresh
receipt records interval enclosures containing each of the 16 target entries.
That inclusion is only a control; equality follows from the existence theorem
and the equations, not from interval inclusion or a tiny residual.

## 4. Independent exact interval existence proof

For a real interval a, the checker evaluates sine/cosine at its rational midpoint
using the Taylor polynomials through degrees 501 and 500, respectively. The
remainders are bounded by |midpoint|^503/503! and |midpoint|^502/502!; the zero
even/odd next coefficients justify these orders. To enclose the entire input
interval, its radius is added using the global derivative bound |sin'|,|cos'|<=1.
Every polynomial arithmetic step and division rounds outward by exact integer
floor/ceiling. Complex reciprocal denominators use the interval squared norm.

Analytic branch derivatives are obtained from the displayed entry formula:

    dG = i G d(theta_i-theta_j+wrap*t)
         + exp(i(theta_i-theta_j+wrap*t)) i h dt / (1-h)^2.

The coefficient rule and ordinary product/quotient rules then produce the full
real Jacobian. Differentiability holds on an open neighborhood of the closed box
because all relevant denominators have strict positive guards.

Using the submitted exact rational matrix B, the independent integer-interval
computation establishes the following strict rational inequalities:

- eta = ||B f(center)||_infinity < 4.522 * 10^-90.
- q = sup_D ||I-B Df||_infinity < 8.143 * 10^-34.
- At the center, ||I-B Df(center)||_infinity < 1.994 * 10^-86.
- The minimum squared-modulus guard is > 0.09323560364057315.
- eta + q*10^-40 < 10^-40, with q<1.

The receipt retains the exact integer-rational bounds, not just these rounded
summary inequalities. All 16 edge gains, four holonomies, four coefficients,
four inverse denominators and eight first-row/column guard entries are covered;
S[0,0] occurs twice in that last list. There are 36 guard records.

On the closed, convex, complete real box D, T(x)=x-Bf(x) is q-Lipschitz by the
mean-value inequality and maps D strictly into itself by eta+qr<r. Banach's
fixed-point theorem therefore gives a unique fixed point in D. Since the square
matrix B Df(center) is within norm one of the identity, it is invertible; hence
B is invertible. Therefore the fixed point is an actual zero of f. Conversely
each zero in D is fixed, proving uniqueness of the zero within this slice. This
does not assert uniqueness in the unfrozen 19-variable family.

Thus the tiny center residual is used only together with a full-box derivative
bound, strict self-mapping, completeness, and verified preconditioner
invertibility. No numerical residual has been substituted for existence.

## 5. Independent countercontrols

Twenty-four exact Q(i) cases cover all six directed Hamiltonian orders beginning
at vertex zero and four nonsingular unit holonomies. Rational Pythagorean
vertex phases produce exact unit edges. Independent Gaussian elimination of
I-W verifies both inverse orders and every entry of the route formula. The
checks also establish W*W=W W*=I, G+G*=I, and the zero-length diagonal convention.

For each case, direct edge differentiation forms dW. The independent inverse
identity dG=G(dW)G is compared exactly with the analytic phase-derivative formula
for the holonomy and all three vertex-phase coordinates. All 1,536 entrywise
derivative comparisons pass.

Seven negative controls are rejected: a pole, a changed coefficient imaginary
part, a changed holonomy, a zero preconditioner, a repeated route, reversed wrap
inequalities, and holonomy incorrectly inserted into diagonal paths. Additional
trigonometric symmetry/norm-enclosure controls pass. These are controls on the
fresh checker, separate from the interval existence proof.

## 6. Nonduplication and preservation of previous results

The recovered phase-averaging record already proves finite arbitrary-complex
coefficient unit-edge Fourier existence, using at most 3^(N-1) displayed terms.
At N=4 this is 27 terms on one fixed route. Its positive Fourier sign can be
conjugated to the current negative sign without changing count or unit gains.
The present certificate adds a four-term witness on the specified four routes;
it is not the first unitary complex-coefficient existence proof. The number 27
was an upper bound, never a proven optimum or lower bound.

The paired local F4 kernel has scalar poles r,s satisfying rs=i and
r+s=-(chi+chi^-1). For primitive eighth-root chi, this prescribed sum is nonzero
real. If both r and s had unit modulus and product i, their sum would lie on the
line exp(i*pi/4)R, inconsistent with that prescribed nonzero real value. Hence
that general-field/nonunitary paired construction does not already furnish this
unit-edge witness. No cost or optimality comparison between those models is
claimed.

The Phase16 F4 record is a two-stage product of four-Green sums with 12 zero-edge
occurrences, including identity topology. The other variable-pole F4 record is
multi-stage. The Phase56 N5/N8 records are two-stage networks with general
complex vertex gains and holonomies. None is relabeled as this four-unit-edge,
one-sum construction. The universal arc bound N<=q(q+1)^q and specialized
two-unitary N>8 exclusion do not obstruct N=4,q=4; no previous exclusion is
overturned. Worldwide novelty was not researched or established.

## 7. Cost and unresolved obligations

The candidate's conservative conditional online count is valid: 56 complex
multiplications and 40 additions at N=4, or 52 multiplications when multiplication
by c0=1 is omitted, with cached exact constants. Its cyclic solves require no
dense inverse formation. The generic supplied-constant application cost is
O(qN), with routing, storage, and output work charged separately.

These are field-operation upper bounds conditional on supplied root-derived
constants. Root discovery, refinement, rigorous validation, transcendental edge
evaluation, denominator preparation, diagonal calibration, finite-bit accuracy,
conditioning, and parameter representation remain separate costs. No practical
FFT comparison, stability theorem, or exact finite rational synthesis is proved.
The fixed N=4 computation gives no uniform all-length construction and no claim
that q remains four for unbounded N. Minimal q, other route tuples, and larger
surviving sizes remain open.

## 8. Scope and remaining work

Only the bounded N4 four-route existence obligation is complete.
The one-sum unit-edge model remains distinct from nonunitary and multistage constructions.
Term optimality, broader NF06 synthesis and historical priority remain unresolved.

## Reproduction

In the complete review archive, preserved separately from this report-only publication:

    python independent_exact_check.py input/nf06_routed_n4_0132/CERTIFICATE.json NEW_RECEIPT.json
    python independent_controls.py

The second command overwrites only the review's control receipt. For preserving
the seal, run in a fresh copy or use the exact-check command with a new output
path. Python assertions must remain enabled. The two checker files are fresh
reviewer code and import no uploaded candidate program.
