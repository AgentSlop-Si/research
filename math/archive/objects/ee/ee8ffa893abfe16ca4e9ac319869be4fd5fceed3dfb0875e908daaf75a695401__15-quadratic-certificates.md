# Q33: independent reconstruction of the finite quadratic phase certificates

10 October 2026. This supplement closes the N3/N4 finite-certificate gap left explicitly open in matrix/final_v1. It does not edit that frozen version. No supplied executable program was run, imported, compiled or AST-parsed.

## 1. Exact scoped theorem

Fix N≥3, a field K of characteristic not2 with a primitive Nth root ω, invertible A,C, and an entrywise nonzero B. Let F[i,j]=ω^(ij), P_j=diag(B[:,j]^−1)A^−1diag((FC^−1)[:,j]) for j=0,1,2, and let Q be the coefficient matrix of all2-square minors of Z_J(c)=[P0c,P1c,P2c] in unscaled monomials(c_ac_b)_(a≤b).

If rank Q=N(N+1)/2, then F=LADBEC has no solution in invertible diagonal L,D,E over K or any extension field. Indeed any solution gives a nonzero c and an everywhere-nonzero rank-one Hadamard quotient Z(c), so Qv(c)=0. A nonzero c has a nonzero square coordinate in v(c), contradicting injectivity. Full column rank persists under field extension. P0 need not be invertible for this argument.

This symmetric-square/minor rejection method is classical. The specific Fourier/Green coefficient map and finite witnesses are its scoped applications. Rank deficiency alone is not feasibility, since the kernel may contain no decomposable v(c), or only forbidden zero-coordinate points, or may fail the remaining columns.

## 2. Fresh reconstruction of both saved finite examples

From the original signed integer cycle weights, diagonal gauges and independent row/column permutations, `check_quadratic.py` reconstructs all eight Green branches by sparse matrix inversion, four for N3 and four for N4. It reproduces the exact saved A,B and component Green matrices modulo97. All Green denominators, A,B inverses, nonzero B entries and P0 inverse are explicitly checked.

The checker derives Q by polarization: evaluate the minor polynomials at e_a and e_a+e_b, then subtract the diagonal terms to recover the c_ac_b coefficients. It matches every entry of the saved9-by6 and18-by10 matrices. The ranks are6 and10.

For N3, rows(0,1,2,3,4,6) give determinant18 modulo97. For N4, our independently selected rows(0,...,9) give determinant31 modulo97. The source advertises a different selected minor66 at N4; we do not claim to have matched that unspecified choice. Matching the entire Q and independently exhibiting a nonzero maximal minor establishes the required full rank.

The rebuilt original commutator matrices exactly match the saved matrices and both have determinant zero. Therefore the old single-commutator gate is silent in these finite-field examples, while the quadratic lift excludes every invertible diagonal gauge even over the algebraic closure of F97.

## 3. Characteristic-zero exceptional-locus existence

For each saved example, let A,B1,B2 be its actual rational Green matrices before reduction. Let C=I and vary only the first output column of B1 by t:

B(t)=B1+B2+(t−1)B1 e0 e0^T.

For t≠0 this remains a legitimate diagonally/monomially gauged Green branch sum. The first column varies linearly; columns1 and2 are fixed. Consequently

T_j(t)=A diag(B(t)[:,0]/B[:,j])A^−1Δ^j, j=1,2,

are linear matrix polynomials in t. Their commutator has degree≤2 and f(t)=det[T1(t),T2(t)] has degree≤2N over Q(ζ_N).

The fresh checker reconstructs that polynomial modulo97 by evaluating the degree-two commutator at t=0,1,2 and expanding its determinant by the Leibniz formula. It gets exactly:

N3: (33,8,31,37,67,4,14), with f(1)=0 and f'(1)=68;
N4: (10,40,72,60,1,29,27,56,93), with f(1)=0 and f'(1)=65.

Coefficients are in ascending powers of t. Both derivatives are nonzero. Thus f is a nonzero polynomial, and its simple residue root at1 lifts to a root α in the completed local cyclotomic ring at the specified prime above97. All rational functions used in the Green inverses, stage/entry guards and selected Q minor are regular units at t=1 modulo that prime. They stay units at α≡1. In particular α≠0, every stage remains admissible, B(α) remains entrywise nonzero and Q(α) has full column rank.

The local root α is algebraic over Q(ζ_N), because it satisfies the nonzero polynomial f. Therefore Q(ζ_N,α) is a finite algebraic extension and has an embedding into C extending the prescribed embedding of ζ_N. Under that embedding f(α)=0 and all unit/nonvanishing guards persist. This proves, for each N3 and N4, an algebraic complex four-Green instance for which the single commutator is singular but the quadratic lift still rejects every remaining invertible diagonal gauge.

This is a genuine characteristic-zero existence proof using a simple local root. Singular reduction of a rational commutator at t=1 alone would not prove complex singularity at t=1. The lifted α is an algebraic parameter, not asserted equal to1.

The source's polynomial need not be globally monic for this Hensel step: its derivative at the residue root is a unit, so standard Newton simple-root lifting applies to an integral local polynomial. One can also multiply/divide by a leading unit if using the monic formulation: the degree2N leading residues14 and93 are units here. All coefficients are locally integral because their fixed denominators are units.

Primary check: Stacks Project, Lemma10.153.9, https://stacks.math.columbia.edu/tag/04GM, establishes that complete local rings are henselian via successive simple-root Newton lifting. This established theorem, not finitely many saved digits, supplies the infinite local root.

## 4. Independently reconstructed Hensel digits

The checker lifts ω by solving ω^N=1 and corrects t through97²,97³,97⁴ using a freshly evaluated commutator determinant and the unit derivative modulo97. Every saved pair of digits agrees. The final values are:

- N3, modulus88529281: t=13866830, ω=44659902
- N4, modulus88529281: t=32570467, ω=22709274

These are finite regression checks on the local convention and polynomial arithmetic. The proof in §3 remains the justification of a complex algebraic root.

## 5. Analytic and novelty status

For the complex realizations, injective Q supplies the already accepted fixed-stage operator bound

||LADBEC−F||2 ≥ sqrt((N+1)/(2N)) σmin(Q) min|B_uv|
                  / [(sum_(j=0)^2||Pj||2²)^(1/2)||A^−1||2||C^−1||2].

The earlier proof in the matrix finalization remains unchanged: the sharper unscaled-monomial norm and the weighted-row inequality remove the unnecessary source factor sqrt(N+1). This supplement closes its particular finite examples and exceptional-locus application; it does not make its constants uniform in N or over varying stage coefficients. No new interval-certified decimal gap is supplied.

The wider methods, Segre/symmetric-square lifting, common eigenvectors and Hensel lifting, are known. Direct primary comparison in the preceding finalization with Dastidar–Weicht–Wein2025 and Johnston–Lovitz–Vijayaraghavan2023 already prevents a claim that the lifting primitive itself is new. Worldwide priority for the exact Fourier/Green example and application remains unresolved.

## 6. Reproduction and evidence boundary

Run `python check_quadratic.py` with Python3 standard library. It imports only the freshly authored `own_modular.py` and reads the three inert JSON files in source_inputs. The output `results.json` includes matrix sizes/ranks, explicit minor row indices and residues, complete polynomial coefficients, derivatives, every lifted digit and hashes of the parameter inputs.

Accepted conclusion after separate proof review: Q33's finite N3/N4 quadratic certificates and exceptional algebraic complex witness theorem. Not claimed: every four-Green wiring fails, existence of a compatible Fourier target, arbitrary-length construction, uniform conditioning, numerical speedup, or unrestricted FFT lower bounds.
