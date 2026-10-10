# C03: fully costed, singular-safe evaluation at one quotient node

10 October 2026. Constructive follow-up to the accepted C03 factorization and its independently accepted structural refinement. This is a new, source-preserving derivation and fresh implementation of classical algorithms. No supplied executable was run or imported, and no external document was changed.

## Result first

For every field F, arbitrary A,B in F^(m×m), and a supplied w in F with w≠0, the exact value V(w+w^−1) can be computed deterministically in:

- O(m³) field operations and O(m²) field-element storage, by an explicit classical polynomial-pencil determinant algorithm;
- alternatively, Õ(m^ω) field operations, using established deterministic polynomial kernel-basis and polynomial determinant algorithms, followed by an O(m²) scalar resultant calculation. Here Õ suppresses polylogarithmic factors, and ω denotes an admissible matrix-multiplication exponent.

These bounds cover singular A, singular B, identically singular pencils, specialized degree drops, zero answers, w=1, w=−1, and every characteristic. No field extension, root finding, sampling in the pencil variable, or division by an integer 1,...,m is required. The O(m²) storage statement is established for the elementary cubic route; no additional sharp storage claim is made for the fast black-box route.

**This is a cost closure using classical algorithms, not a new fast determinant/resultant algorithm or a novelty clearance for C03.** The earlier O(m⁶) singular-safe endpoint bound was a valid dense-Kronecker fallback, not a lower bound. Its replacement by O(m³), or by Õ(m^ω), follows from existing polynomial-matrix algorithms. In particular, nonendpoint evaluation returns to the very two pencils used in the definition of C03; it must not be presented as a new algorithmic discovery intrinsic to the m²-square residual determinant.

## 1. Exact evaluation algorithm

Retain the accepted normalization

    D(w)=diag(1,w,...,w^(m−1)),
    L=m²(m−1), n=m², b=m(m−1)(2m−1)/6,
    R(w)=Res_(m,m)(det(A−aDAD),det(B−awDBD))
        =w^L(w−1)^n V(w+w^−1).

Res_(m,m) always means the fixed homogeneous degree-(m,m) resultant, including after degree drops. All matrix indices in this note start at zero.

### Branch A: w≠0,1

1. Form C=DAD and E=wDBD. Their entries are C_ij=A_ij w^(i+j) and E_ij=B_ij w^(i+j+1).
2. Compute all m+1 coefficients, including leading zero positions, of f(a)=det(A−aC) and g(a)=det(B−aE), using the pencil algorithm in §2 or §4.
3. Compute r=Res_(m,m)(f,g), by a padded 2m-square Sylvester determinant or the degree-aware Euclidean algorithm in §3.
4. Return r/[w^L(w−1)^n].

The denominator is nonzero in F. Its exponentiation requires O(log(m+1)) operations by repeated squaring. Zero values of r are returned exactly; they do not cause a failed division.

### Branch B: w=1

Let H=diag(0,1,...,m−1). Form

    C=HA+AH,           C_ij=(i+j)A_ij,
    E=HB+BH+B,         E_ij=(i+j+1)B_ij.

Compute

    f(t)=det(C+tA),    g(t)=det(E+tB),

and return Res_(m,m)(f,g). The accepted tangent identity says exactly that this is V(2), with no additional sign or scale. This branch never divides by w−1 and remains valid in small characteristic.

### w=−1 and characteristic 2

If char F≠2, w=−1 uses Branch A: both w and w−1=−2 are nonzero. Its output equals the accepted parity-block determinant V(−2), without building either large parity block.

If char F=2, −1=1 and −2=2=0; the point uses Branch B and gives V(0). There are not two distinct endpoint computations.

### w=0 and an arbitrary x supplied without w

The expression w+w^−1 does not exist at w=0, so zero is not an admissible quotient node. The evaluator rejects it rather than dividing by zero or assigning V an arbitrary value. If the desired quantity is instead the projective endpoint, the existing coefficient certificate computes

    lim_(w→0) w^b V(w+w^−1)=[x^b]V

in O(m³). This is an algebraic constant-term identity, not a finite value V(x) at w=0. For completeness, R(0)=0 when m≥2, while for m=1 it is −A_00 B_00.

The input here includes w. If only x is supplied, finding w with w²−xw+1=0, or passing to an extension containing one, is a separate task whose cost is not hidden in the bound.

## 2. Explicit cubic determinant-of-pencil subroutine

The needed subproblem is to compute det(C+tE) for arbitrary C,E in F^(m×m), even when the determinant is identically zero. Mulders–Storjohann, *On Lattice Reduction for Polynomial Matrices*, §4, Figure 5 and Theorem 4.2, already supplies the deterministic O(m³d²) polynomial-matrix algorithm. With entry degree d≤1, its bound is O(m³). The paper's input is an arbitrary square polynomial matrix, not only a nonsingular constant or leading coefficient matrix. [Primary manuscript, pp. 7–10](https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf).

Here is the degree-one specialization, with its cost independently made explicit. It performs no generalized-eigenvalue computation.

### Procedure and correctness

Start with T=C+tE. At a current q-square stage, q≥2, split T=[M | v], with M consisting of the first q−1 columns. For each nonzero row of M, take its rightmost entry of maximal degree as its pivot. While two rows share a pivot column, subtract a scalar times t^δ times the lower-degree row from the higher-degree row to cancel the latter's leading pivot coefficient. Apply the same row operation to v. Each such operation has determinant one.

When the nonzero pivot columns are distinct, q rows and only q−1 possible pivot columns force a zero row of the transformed M. If that row is k, and the corresponding transformed v entry is h(t), expansion along the row gives

    det T=(−1)^(k+q−1) h(t) det T_next,

where k is zero-based and T_next is M with that zero row deleted. Record the signed factor, discard v and the zero row, and repeat with T_next. At q=1, record its sole entry. Return zero immediately upon a zero factor. Otherwise multiply the recorded factors at the end.

This is an exact determinant identity at every stage, including rank-deficient cases. No nonsingularity assumption or generic pivot assumption enters it. Division is only by the nonzero leading coefficient of a selected polynomial pivot.

### Reduction count and polynomial degrees

All entries of the retained core M have degree at most one throughout: cancelling a common pivot never raises the target row's maximal degree. Core row degrees are therefore −1, 0, or 1, with −1 assigned to the zero row.

Fix the original dimension m and assign a nonzero core row the score m·d+p, where d is its row degree and p is its one-based rightmost pivot position. Give a zero row score zero. Each leading-pivot cancellation strictly lowers one score. Deleting the last column and a zero row between stages cannot increase the sum of scores. The initial sum is at most 2m², so there are at most 2m² cancellation operations across all stages, not O(m²) separately at every stage.

The side vector can grow in degree and must be charged. At one q-row stage, let D_i be its current core row degrees, define Δ as the decrease in their sum since the stage started, and put degree(0)=−1. Initially deg v_i≤1≤D_i+2. Induction over each row cancellation gives

    deg v_i ≤ D_i+2+Δ.

Indeed, the monomial shift is the difference of the source and target row degrees, so the update respects the displayed bound before any degree drop. A target degree drop increases Δ by exactly the amount needed to preserve the bound afterward. Since −1≤D_i≤1, Δ≤2q. Thus every side entry has degree at most 2q+3=O(m).

Updating a core row costs O(m) field operations because its entries stay linear; updating its side entry also costs O(m). The O(m²) cancellations therefore cost O(m³). Pivot metadata can be cached and recomputed only for the changed row in O(m) zero tests; scanning cached pivots for a collision costs O(m) per cancellation. Stage setup costs Σ_q O(q²)=O(m³) further coefficient inspections. The arithmetic bound does not hide an O(m⁴) repeated search.

Retain the extracted factors and multiply only after checking that none, including the final one, is zero. In that case their product is the nonzero determinant of an m-square linear pencil, so the sum of their degrees is at most m. Ordinary polynomial multiplication then costs O(m²) in total. If a zero factor is encountered, no accumulated large product is needed.

The core uses O(m²) coefficients, the side vector uses O(m²), and the saved factors use O(m²) at worst. This proves O(m³) field operations and O(m²) storage uniformly. The fresh implementation in this folder uses this procedure; it does not call a symbolic determinant package.

## 3. Fixed-degree resultant, with all padding corrections

A simple cubic implementation pads both coefficient lists to length m+1 and takes the determinant of their 2m-square Sylvester matrix. Constructing it costs O(m²); pivoted field elimination costs O(m³). A zero pivot column returns zero. Trimming both lists and silently computing the ordinary resultant is incorrect.

An O(m²) alternative is useful for the fast total bound. For nonzero f,g let r=deg f and s=deg g, let α=lc(f), β=lc(g), and let res(f,g) denote the ordinary actual-degree resultant. Then

    Res_(m,m)(f,g)=0                         if r<m and s<m,
    Res_(m,m)(f,g)=α^(m−s) res(f,g)          if r=m,
    Res_(m,m)(f,g)=(−1)^(m(m−r)) β^(m−r)
                       ·res(f,g)            if r<m and s=m.

If either polynomial is zero, return zero. Both degree-m forms vanish at the point at infinity in the first line. The other lines follow by the full-degree root formula and by swapping the two forms; the sign in the final line must be retained. These formulas also cover nonzero constants.

For completeness, the ordinary resultant is computed by Euclidean remainders. If r≥s≥1, write f=qg+h. A zero remainder gives zero; otherwise with t=deg h,

    res(f,g)=(−1)^(rs) β^(r−t) res(g,h).

Swap the pair, with factor (−1)^(rs), when r<s. The terminal constant rule is res(f,c)=c^deg(f). These identities follow directly by evaluating f=qg+h at the roots of g and remain valid with repeated roots by polynomial specialization. Long division over the coefficient field and the decreasing-degree recurrence cost O(m²) operations; all leading-coefficient powers together cost at most O(m log(m+1)) by repeated squaring. The padding correction adds O(log(m+1)).

Strict control examples:

- For m=2, A=[[1,1],[1,1]], B=I and w=2, the two pencils have f(a)=−a and g(a)=1−10a+16a². The ordinary resultant is 1, but Res_(2,2)=16. Dividing the latter by w^4(w−1)^4 gives the correct V=1.
- For m=2, A=B=[[1,1],[1,1]], the two tangent determinants are both the constant −1. Their ordinary constant/constant resultant is 1, whereas their padded degree-(2,2) resultant, and the correct V(2), are zero.

The control suite separately tests the Euclidean routine and every padding stratum against explicitly built Sylvester determinants, including the sign-sensitive odd m cases.

## 4. Uniform fast bound: an explicit singularity gate

One must not apply a theorem for nonsingular polynomial matrices to an arbitrary singular pencil without a gate. Labahn–Neiger–Zhou, *Fast, deterministic computation of the Hermite normal form and determinant of a polynomial matrix*, provides the two necessary established ingredients: Theorem 7 computes a kernel or column basis without a full-rank hypothesis; Algorithm 2 and Proposition 17 compute the determinant once polynomial nonsingularity is known. For degree-one square input, each costs Õ(m^ω). The manuscript also explicitly discusses deterministic computation over small fields without requiring an extension. [Primary manuscript, Theorem 7 p. 6; Algorithm 2/Proposition 17 pp. 12–13](https://cs.uwaterloo.ca/~glabahn/Papers/HermiteDeterminantPaper.pdf).

Apply them as follows to each pencil P(t):

1. A zero column certifies det P=0 immediately. A constant pencil can use ordinary exact field determinant computation.
2. Otherwise compute a polynomial kernel basis. A nonempty basis certifies det P=0: a rational-function nullvector exists exactly when a polynomial one exists, by clearing its denominators.
3. If the kernel is empty, P is nonsingular over F(t). Apply the determinant algorithm to obtain all coefficients of det P.

Degrees of nonzero columns are 0 or 1, so the average-degree ceiling in the two cited bounds is at most one. The singularity gate is charged, and its cost has the same Õ(m^ω) order as the determinant call. There is no search for an invertible constant evaluation and no assumption that P(0), P's leading coefficient, A, or B is invertible.

Combining the two pencil computations with the O(m²) padded resultant routine of §3 proves the uniform Õ(m^ω) evaluation bound. The fresh executable implements and checks the elementary cubic pencil route and the quadratic resultant backend, not the fast kernel-basis/determinant algorithms. The fast bound is a direct application of their published theorems.

## 5. End-to-end arithmetic accounting

For one supplied nonzero w:

- Input access and matrix formation: O(m²). In Branch A, the powers w^0,...,w^(2m−1) take O(m) multiplications. In Branch B, the integer factors i+j and i+j+1 are generated inside F by repeated addition, requiring O(m) preparation.
- Both pencil determinant polynomials: O(m³) by §2, or Õ(m^ω) by §4.
- Fixed-degree scalar resultant: O(m³) by the padded dense determinant, or O(m²) by §3.
- Normalizing power, inverse and output: O(log(m+1)) in Branch A and no such division in Branch B.

Thus both advertised total bounds include forming the polynomial coefficients and handling their degree loss. They do not count the m²-square Kronecker determinant as an m-square operation. No characteristic restriction is imposed. The model is exact unit-cost field arithmetic and equality tests; no arbitrary-ring complexity, rational bit-complexity, or numerical-stability guarantee follows.

## 6. What this does and does not add

This closes the concrete per-node evaluation cost and improves the available singular-safe endpoint implementation. It does not change C03's accepted factorization, generic exponents, or exact-family priority status. The original two m-square pencils already supported classical per-node evaluation; the residue determinant is not the source of a new asymptotic resultant method.

For q already supplied quotient nodes, total evaluation costs O(qm³), or Õ(qm^ω) through the fast route. Reconstructing all coefficients still requires b+1 distinct quotient values x_i=w_i+w_i^−1, adequate node supply or a charged field extension, and interpolation. Its cost is

    (b+1)·C_evaluate(m) + I(b),

not one per-node evaluation. Classical interpolation has I(b)=O(b²); combined with cubic evaluation this gives O(m⁶) field operations once suitable nodes are supplied. The number of coefficients itself is Θ(m³). There is no all-coefficient cubic claim, no uncharged interpolation, no sparse-recovery legality certificate, and no FFT claim. The previous factor-six asymptotic sampling-ratio observation remains a constant-factor comparison between Θ(m³) sample counts.

## 7. Fresh controls and preservation

`fresh_controls.py` was written in this folder using only the Python standard library, exact rational arithmetic, and prime-field arithmetic. It contains separately implemented:

- degree-one successive weak-Popov determinant reduction;
- permutation expansion for small arbitrary pencil determinant polynomials;
- pivoted scalar determinant and fixed-degree Sylvester construction;
- Euclidean resultant with explicit degree-padding corrections;
- the C03 node evaluator, and the direct m²-square Laurent quotient determinant as an independent value oracle.

`EXACT_CONTROL_RESULTS.json` and `control_run.log` record 3,361 passing exact records: 360 arbitrary-pencil comparisons, 1,596 C03 value comparisons, 1,400 degree-padded Euclidean-resultant comparisons, two strict padding counterexamples, and three zero-node rejection tests. Its case set covers arbitrary pencils through m=4 over Q,F_2,F_3,F_5,F_101; C03 values through m=6 over Q and five prime fields; singular and zero inputs; both endpoint branches; reciprocal-node agreement; all scalar degree strata; and rejection of w=0. Per-operation counts and the reduction/side-degree bounds are checked where recorded. The source reports' hashes are compared before and after the run.

These controls corroborate the algebra and the concrete cubic implementation. They do not test the full fast polynomial-matrix algorithms, establish bit complexity, or determine priority.

## Primary-source comparison

1. Mulders–Storjohann (2003), §4, Fig. 5, Thm. 4.2: the exact classical determinant algorithm underlying the cubic claim. The O(m³) specialization is not new. https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf
2. Labahn–Neiger–Zhou (2016 manuscript; journal 2017), Thm. 7 and Algorithm 2/Prop. 17: deterministic basis computation plus determinant computation underlying the singular-safe fast gate. These are existing algorithms, not a C03 innovation. https://cs.uwaterloo.ca/~glabahn/Papers/HermiteDeterminantPaper.pdf
3. Existing accepted C03 source and its structural refinement: exact normalization and the tangent resultant identity. They are read-only inputs to this note, with bindings recorded in the control receipt.

No exact-family priority upgrade is asserted. This is a corrected, stronger cost statement and a complete usable implementation route for an already defined classical resultant computation.
