# Independent audit: uniform singular-safe C03 node evaluation

10 October 2026. Scope: `research_cycle_1535/resultant_evaluation_algorithm/SINGULAR_SAFE_EVALUATION.md`, its recorded controls, the accepted C03 normalization, and the cited primary algorithm theorems. All new files are confined to this audit folder. Supplied programs were statically inspected only; none was run or imported.

## Verdict

**ACCEPT the mathematical and exact-field-arithmetic claims.** For integer m ≥ 1, any field F, arbitrary m-by-m A and B over F, and a supplied nonzero w in F, the prescribed C03 value V(w+w^(-1)) has a deterministic O(m^3)-field-operation, O(m^2)-field-storage evaluator. A separate deterministic soft-O(m^omega)-field-operation evaluator follows from the published kernel-basis and nonsingular polynomial-determinant algorithms, with an O(m^2) scalar resultant backend. No sharp storage bound is accepted here for that fast black-box route.

This supersedes the previous conservative O(m^6) endpoint implementation as an available upper bound. It does not make the previous fallback false. The improvement is an application of classical algorithms to the original two small pencils, not a new determinant/resultant algorithm or a priority upgrade for C03.

One non-blocking implementation qualification: the supplied control harness runs `assert all(len(a)<=2 for row in M for a in row)` after each reduction. Those full-core debug scans can add O(m^4) Python bookkeeping, while leaving the asserted O(m^3) field-operation bound intact. Disable that debug assertion, or replace it by a changed-row check, before calling the literal harness a cubic-runtime implementation. No Python timing or bit-cost conclusion is established.

## Independent proof checks

### Node and endpoint legality

For w different from zero and one, both normalizing factors w^(m^2(m-1)) and (w-1)^(m^2) are nonzero. The fixed-degree resultant may vanish; this never makes division by the normalizer invalid. Repeated squaring costs O(log(m+1)) field operations because the exponents have O(log(m+1)) bits.

At w=1, the tangent pencils det(HA+AH+tA) and det(HB+BH+B+tB), with H=diag(0,...,m-1), give the accepted V(2) with no further sign or scale. The +B term is essential. Integers multiplying entries are formed inside F by addition, so this does not assume invertibility of any integer. The branch never divides by w-1.

In characteristic different from two, w=-1 is a legal nonendpoint-branch input and returns V(-2). In characteristic two, -1=1 and the single tangent branch returns V(0); it is not a separate second endpoint. The input w=0 is correctly rejected. The projective coefficient limit described in the note is distinct from a finite quotient-node value. Supplying x alone would require separately finding or adjoining a root of w^2-xw+1.

### Cubic pencil determinant and its degrees

The retained core has entry degree at most one. Cancellation at a shared rightmost maximal-degree pivot cannot increase its target row degree. Using fixed original dimension m in the row potential m*d+p, with one-based pivot p and zero-row score zero, each cancellation strictly decreases the total potential. Passing to the next core cannot increase it. Thus the total number of cancellations across all stages is O(m^2), not that many independently at each stage.

A stage starts with linear side entries, including side entries beside a zero core row. If D_i is the current core degree and Delta the accumulated core degree-sum drop at that stage, the bound deg(v_i) <= D_i+2+Delta survives each row update. Since Delta <= 2q for q current rows, the side entries have degree O(m). This explicitly charges side-vector growth. A row update and cached-pivot search cost O(m); all arithmetic and necessary pivot inspection is therefore O(m^3).

Every extraction is a determinant-one row transformation followed by a correctly signed cofactor expansion. A zero extracted factor safely certifies a zero determinant. If all factors are nonzero, their product is a determinant of an m-square linear pencil, hence the sum of their degrees is at most m. Deferring multiplication until after zero detection makes ordinary final multiplication O(m^2). Retained core, side column, and saved factors each fit O(m^2) field-element storage. Neither constant nor leading matrix invertibility is required.

### Padded resultant backend

The fixed homogeneous degree-(m,m) convention is indispensable. If both nonzero actual degrees are below m, the answer is zero because both forms vanish at infinity. If deg f=m, the correction is lc(f)^(m-deg g) times the actual-degree resultant. If deg f=r<m and deg g=m, it is (-1)^(m(m-r)) lc(g)^(m-r) times that resultant. Zero input polynomials yield zero for m>=1; nonzero constants are covered without exceptions being silently dropped.

The Euclidean recurrence and swap sign are correct. Ordinary long divisions cost O(m^2) in total by decreasing degrees; leading-coefficient powers cost at most O(m log(m+1)), also within O(m^2). Dense padded Sylvester elimination is a separate valid O(m^3) alternative. There is no assertion that dense elimination itself is quadratic.

### Fast rank gate and arithmetic scope

A nonempty polynomial kernel basis is equivalent to singularity over F(t), since denominators of a rational nullvector can be cleared. An empty basis is therefore the required gate for a theorem assuming a nonsingular polynomial matrix. A zero column can be rejected first, and all-constant pencils can use ordinary field determinant algorithms. Every remaining column degree is zero or one, so the relevant average-degree ceiling is one. Singularity testing and determinant computation are both charged.

The claims are exact unit-cost field arithmetic, with exact equality tests. They do not imply arbitrary-ring complexity, rational/integer bit complexity, numerical conditioning, or stable floating-point rank decisions. The polynomial determinant has degree at most m; the residual trace polynomial can have degree b=Theta(m^3). The per-node bound does not construct all coefficients of V. Interpolation requires b+1 distinct quotient values, charged interpolation, and adequate nodes or a charged extension.

## Primary sources read directly

1. Mulders–Storjohann, *On Lattice Reduction for Polynomial Matrices*, primary manuscript, Section 4, Figure 5 and Theorem 4.2, printed pages 7–10. The input is an arbitrary square polynomial matrix over a field; the theorem gives deterministic O(n^3 d^2) field operations. Its side-vector degree argument and amortized state-drop analysis match the specialization used here. The introduction also explicitly allows rank-deficient inputs. Read through the primary PDF text; one screenshot request failed with a cache-miss error, which did not prevent reading the full theorem text.
   https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf

2. Labahn–Neiger–Zhou, *Fast, deterministic computation of the Hermite normal form and determinant of a polynomial matrix*, 2016 primary manuscript. Theorem 7, printed page 6, applies to m-by-n matrices with m<=n and m=Theta(n), without a full-rank assumption. Algorithm 2 and Proposition 17, printed page 13, expressly assume a nonsingular square polynomial matrix. For square degree-one inputs, the kernel gate followed by this determinant routine gives soft-O(m^omega). The introduction discusses small finite fields without requiring a field extension. The relevant definitions, theorem, algorithm, proposition, and complexity discussion were read directly.
   https://cs.uwaterloo.ca/~glabahn/Papers/HermiteDeterminantPaper.pdf

No independent implementation of the fast kernel/determinant algorithms was attempted. Acceptance of that route is theorem-based, with its hypotheses checked, rather than an executable-performance claim.

## Fresh exact controls and mutations

`independent_controls.py` was authored before static inspection of the supplied control program. It uses only standard-library rational arithmetic and independently implemented finite-field arithmetic, including F4=F2[z]/(z^2+z+1). Polynomial determinant comparison uses a separate permutation expansion. Scalar resultant comparison uses a separately constructed padded Sylvester matrix. C03 comparison uses the direct accepted Laurent quotient matrix with finite-sum entries, without division by w-1.

Completed results: **5,723 passing records**, plus **eight strict mutation/boundary witnesses**:

- 840 arbitrary-pencil comparisons through m=6 over Q, F2, F3, F5, F7, F101 and F4, including forced singular and constant pencils.
- 256 exhaustive binary 2-by-2 pencils.
- 2,660 padded-resultant comparisons through m=8, with every requested actual degree stratum enforced, including zeros and constants.
- 1,960 C03 node comparisons through m=5, each also checked at the reciprocal node. These include singular A or B, both singular, zero inputs, both characteristic-zero endpoints, and F4 nonendpoint nodes in characteristic two.
- Seven zero-node rejection checks.

The pencil controls also verify the descending potential, linear retained cores, stage side-degree bound, total-reduction bound, and final nonzero-factor degree sum. Maximum observed reduction count was 55 and maximum side degree was 6; these observations corroborate but do not prove the asymptotic bound.

Strict witnesses reject:

1. Trimming nonendpoint degree padding: correct 1 versus mutant 1/16.
2. Trimming constant tangent padding: correct 0 versus mutant 1.
3. Dropping the odd-m padding sign: correct -1 versus mutant 1.
4. Omitting tangent +B: correct -3 versus mutant 0.
5. Inferring polynomial regularity merely from nonzero columns: [[1,t],[0,0]] remains singular.
6. Rejecting a pencil because both endpoint coefficient matrices are singular: diag(t,1) has determinant t.
7. Testing polynomial rank only at base-field nodes: diag(t,t+1) over F2 has nonzero determinant t^2+t, which vanishes at every F2 node.
8. Reusing the generic division branch at w=1: division by zero occurs, while the tangent value for A=B=I_2 is -3.

The supplied 3,361-record receipt was read and its record counts reconciled, but none of those results substitutes for the fresh controls above. All input-file hashes were checked again at completion and remained unchanged.

## Recommended accepted wording

“Classical polynomial-matrix algorithms give a uniform deterministic O(m^3)-field-operation, O(m^2)-field-storage evaluator of V(w+w^(-1)) for arbitrary A,B and every supplied w!=0, including the tangent endpoint and small characteristic. A kernel-gated classical alternative costs soft-O(m^omega) field operations, with no additional sharp storage claim. This improves the previously recorded conservative endpoint upper bound; it does not change the C03 factorization or establish a new resultant algorithm, all-coefficient bound, numerical guarantee, or priority result.”
