# Target compatibility for two selected Green terms

10 October 2026

Status: independently reviewed; propositions and the four pinned finite-field and complex exclusions accepted. The accepted source proof hash and review scope are recorded in PROOF_STATUS.json at the packet root.

## Scope and conclusion

There is a target-only finite-edit obstruction that keeps both one-sided terms and needs no entrywise division. It applies when exactly one selected input Green term and one selected output Green term may change, while the remaining six terms and all coefficients stay fixed.

The obstruction is different from the baseline normalized mixed-Hessian rank. It comes from eliminating one horizontal weight between two equations of the full target equality. Every reachable target must make a specified matrix with four columns have rank at most three.

Fresh certificates make this matrix have rank four for the pinned seed-19 Fourier targets at N = 4, 16, 64 and 256. These exclude arbitrary finite edits of the selected pair at those fixed six-term baselines, including edits with zero weights. They also certify exclusion for a precisely defined rational lift of those six-term baselines over the complex numbers. They do not exclude changes to the other six terms, changes to the coefficients, a different topology, or general Fourier factorizations.

## Exact finite target equations

Let K be any field. Fix N by N matrices A and B, scalars a and b, and permutation matrices Q_H and Q_V. For arbitrary new weight vectors h and v, set

S_H = I − diag(h) Q_H,
S_V = I − diag(v) Q_V,
H = S_H^−1, V = S_V^−1,
T(v,h) = (A + bV)(B + aH).

Here A is the sum of the three frozen output terms and B is the sum of the three frozen input terms. The original network has a = b = 1/4. The vectors h and v are the complete new weights, not increments. They may include zeros. The only required domain restrictions are det(S_H) ≠ 0 and det(S_V) ≠ 0.

Given a target matrix F, define fixed coefficient matrices

X = F − AB,
R = (X − aA − bB − abI) Q_H^−1,
U = Q_V (X − aA) Q_H^−1,
W = X − bB,
Z = Q_V X.

**Proposition 1.** On the stated inverse domain, T(v,h) = F if and only if

R_ij − v_i U_ij − h_j W_ij + v_i h_j Z_ij = 0

for every i,j.

**Proof.** Multiplying the full target equality on the left by S_V and on the right by S_H gives

S_V F S_H = (S_V A + bI)(B S_H + aI).

Because both pencils are invertible, this step is reversible. Expanding and subtracting the right side yields

X − aA − bB − abI
− diag(v) Q_V (X − aA)
− (X − bB) diag(h) Q_H
+ diag(v) Q_V X diag(h) Q_H = 0.

Right multiplication by Q_H^−1 gives

R − diag(v)U − W diag(h) + diag(v) Z diag(h) = 0.

Taking entries proves the claim. No Green bridge entry is divided out, and the original one-sided changes have not been discarded. ∎

The proposition is an exact coupled system. It is independent of an input vector: equality of these matrices is equality on every input. It also does not use the original values of the two selected weight arrays, except that those values label the original baseline in the source audit.

## A target-only necessary condition

For distinct output indices i,k, define an N by 4 matrix M_ik(F), with row j equal to

[ −R_ij W_kj + R_kj W_ij,
   U_ij W_kj − R_kj Z_ij,
   R_ij Z_kj − U_kj W_ij,
  −U_ij Z_kj + U_kj Z_ij ].

**Proposition 2.** Every reachable F satisfies

M_ik(F) (1, v_i, v_k, v_i v_k)^T = 0.

Consequently rank(M_ik(F)) ≤ 3. For N ≥ 4, every 4 by 4 minor vanishes. A single nonzero such minor excludes T(v,h) = F for every admissible finite pair of selected weight arrays, over K or any field extension of K.

**Proof.** Write the two equations from Proposition 1 for a fixed j as

α_i + β_i h_j = 0,  α_k + β_k h_j = 0,

where α_i = R_ij − v_i U_ij and β_i = −W_ij + v_i Z_ij, and similarly for k. Eliminating h_j without division gives α_i β_k − α_k β_i = 0. Its coefficients in 1, v_i, v_k, v_i v_k are exactly row j of M_ik(F). The stated vector is nonzero because its first entry is 1. Therefore the four columns are linearly dependent. A nonzero minor remains nonzero in a field extension. ∎

Each minor is a polynomial of degree at most eight in the entries of F when the frozen matrices are treated as constants. This is a necessary condition, not a claimed sufficient test. Rank at most three alone does not ensure that the kernel contains a vector of the required form with first coordinate 1. Nor does it synchronize the parameters across different row pairs, ensure a common h_j in degenerate cases, or enforce the inverse domain. Those requirements remain in Proposition 1.

## Pinned exact certificates

Use the source audit's row-permutation convention Q[i,π(i)] = 1 and row-major index xs+y, where N=s². In order, the four permutations are

π_0(x,y) = (x+2y,y),
π_1(x,y) = (x+2y+1,y),
π_2(x,y) = (x,y+2x),
π_3(x,y) = (x,y+2x+1),

with coordinates modulo s. The editable terms are input π_1 and output π_3. All coefficients are 1/4. The remaining six arrays are frozen at the seed-19 arrays specified by the original construction and recorded explicitly in ../certificates/finite_edit/FRESH_PAIR_OBSTRUCTION_RESULTS.json. This data file, rather than any random generator version, fixes the integer arrays for this note.

The fresh verifier reconstructs every Green matrix by dense inversion of I − diag(w)Q over the field with 65537 elements. It imports no submitted module and runs no submitted program. Its Fourier matrix is F_ij = ω^(ij), where ω = 3^((65537−1)/N). All indices below are zero-based.

Every certificate uses the row pair (i,k) = (0,1) and the four rows j = 0,1,2,3 of M_01(F). Their determinants modulo 65537 are:

- N = 4, ω = 65281: 27524
- N = 16, ω = 64: 30664
- N = 64, ω = 8224: 29989
- N = 256, ω = 282: 24911

All are nonzero. The data file includes the full four by four matrices and all eight original integer weight arrays. The permutation construction is specified above and implemented in the fresh verifier. The selected original arrays are retained only for provenance and control comparisons; the obstruction allows their replacements to be arbitrary.

For example, the complete N = 4 certificate matrix is

58614  54051  64241  39617
18827  19640  36248  61646
64736  11486  59379  49368
15607  24663  29289  45219

Its determinant modulo 65537 is 27524.

## Why these particular certificates also apply in characteristic zero

A mere failure to find a solution over a finite field would not prove nonexistence over the complex numbers. The certificate here proves something different: a necessary target-only expression is nonzero.

Define the characteristic-zero frozen network using exactly the recorded integer weights, the same integer permutation matrices, and the rational coefficient 1/4. Let ζ be a primitive complex Nth root and set F_ij = ζ^(ij). Let D be 4 times the product of the determinants of the six frozen integer inverse pencils. These determinants are nonzero over the rational numbers and modulo p=65537: the finite-field inversion checks verify the latter, and each cycle has an integer weight product greater than one.

The frozen matrix entries and the chosen minor lie in the ring

Z[ζ, 1/D].

There is a ring homomorphism from this ring to the field with p elements taking ζ to the recorded ω and integers to their residues. Indeed N is a power of two, so the cyclotomic polynomial is t^(N/2)+1, which vanishes at ω, and D has nonzero residue. Under this homomorphism, the characteristic-zero minor maps to the recorded nonzero modular determinant. Hence that minor cannot be zero in characteristic zero. Proposition 2 therefore excludes the complex target for all complex selected weights for which the two Green inverses exist.

No assumption about reduction of a hypothetical complex solution is used. The contradiction is in a necessary expression depending only on the frozen data and target. Choosing a different primitive complex Nth root is a Galois conjugation of the same nonzero algebraic number and preserves nonvanishing.

This conclusion concerns the explicit integer/rational lift just defined. A different lift of finite-field weights is a different frozen characteristic-zero network and is not covered by these certificates.

## Fresh reachable controls and the old rank test

The verifier also constructs admissible selected replacements, forms the full target T(v,h) directly, and independently checks both the two-sided pencil identity and every scalar equation of Proposition 1. It then checks every distinct row pair in Proposition 2.

- N = 4 dense replacement: all 6 row pairs have rank at most 3; the complete edit has rank 4 in the old baseline normalization.
- N = 16 dense replacement: all 120 row pairs have rank at most 3; the complete edit has old normalized rank 16.
- N = 64 dense replacement: all 2016 row pairs have rank at most 3; the complete edit has old normalized rank 64.
- N = 16 with every new horizontal weight zero: H=I remains admissible, all 120 row pairs have rank at most 3, and the complete edit has old normalized rank 16.

These controls show why the old mixed-only baseline rank cannot serve as the corresponding full-edit obstruction. A genuinely reachable complete edit can have full normalized rank. The new target-only condition accounts for the full finite equality and does not require the moving bridge to be entrywise nonzero.

## Reproduction and limits

The included fresh_pair_obstruction.py uses Python and NumPy; see REPRODUCE.md at the packet root for a self-contained temporary working layout. It writes FRESH_PAIR_OBSTRUCTION_RESULTS.json beside the script in the temporary working directory and checks all stated inverse, scalar-equation, row-pair and baseline-normalization assertions. It operates entirely on fresh matrix code and recorded algebraic specifications.

The displayed topology and explicit recorded integer arrays define the instance completely. The source and exported proof hashes are recorded separately in SOURCE_MANIFEST.json at the packet root.

The general propositions hold over arbitrary fields. The explicit Fourier exclusions are finite-size, fixed-six-term results. No all-length Fourier exclusion, unrestricted architecture exclusion, lower bound on Fourier computation, operation-count improvement, or external novelty claim is established.
