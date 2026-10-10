# Independent audit: two-sided Fourier tail ranks and complete gate collapse

9 October 2026. The uploaded Python and archive contents were treated as inert text/data. No uploaded executable, module or binary was run or imported. This audit supplies two independently authored checkers with local, relative-path inputs. It does not modify the research master or upload anything.

## Verdict

Theorems A–D are correct under their stated or inherited hypotheses. The two-sided obstruction genuinely applies to all lengths and general quasiseparable stages in the indicated orientations. The complete 11×9 polynomial gate really collapses to its previously selected minor, and the quadratic factor is absolutely irreducible. The boundary-lock determinant identity is also correct, with a real N=8 exception; a proof omitted from the new package is supplied below.

These are structural restrictions and a simplification of an existing necessary gate. They neither exhibit an exact fresh-input Fourier algorithm nor establish a general Fourier arithmetic lower bound. Full complex feasibility at N=8 remains unresolved.

Fresh exact symbolic checks:

- Reconstructed the polynomial generators from their defining recurrences, without importing any old code. Matched Δ, T, V, M, DB, DH and Dhat against inert independently reconstructed prior data.
- Verified the two lower-tail recurrence identities and all five three-frequency tail-coordinate identities.
- Computed all 30 stated 4×4 subspace determinants and all 10 Plücker cross products exactly.
- Computed every one of the 55 full 9×9 gate determinants: 45 are zero polynomials and the other 10 are nonzero constant multiples of Dhat=−DB·DH.
- Reconstructed the homogeneous quadratic matrix. Its rank is exactly four over Q(ζ8), hence over C; the stated 11251 modular witness is correct.

Fresh finite-field controls used lengths 2–18, 24, 32 and 64, including odd and non-power-of-two lengths. They comprise 348 Fourier-kernel annihilation checks, 5,556 consecutive-restriction rank checks, 1,392 full-column-rank-space inequality checks, 93 spectral-complement matrix identities, 93 square-map invertibility checks and 279 spectral-space rank checks. These are controls of the algebraic proofs, not substitutes for them. All completed successfully.

## 1. Theorem A: exact two-sided inequality

Use zero-based indices, a primitive Nth root ζ in a field whose characteristic does not divide N, and the unnormalized Fourier matrix F[i,k]=ζ^(ik). Let C be invertible and B[:,j]=(FC)[:,π[j]]. The hypotheses bound C's strict lower-left blocks by rC↓ and B's strict upper-right blocks by rB↑.

For the last t columns of B, let J be their corresponding C-column set, a=max J and ℓ=N−1−a. The selected-column matrix X=C[:,J] has rank t. Its bottom ℓ rows sit within C's lower-left cut after index a, and the first N−t rows of FX form the upper-right cut of B. Thus their ranks have the asserted bounds, including when J is not a consecutive set.

The kernel K of the first N−t Fourier rows has dimension t. A basis is given by vectors k↦ζ^(rk), r=1,…,t: the nontrivial full root sums vanish, and their full Fourier images occupy precisely the last t rows. Restriction to input coordinates a+1,…,N−1 is a Vandermonde matrix up to nonzero column scalings, so it has rank min(t,ℓ). Rank–nullity on W=col(X) gives

dim(W∩K)≥t−rank(RFX),

rank(TX)≥dim T(W∩K)≥min(t,ℓ)−rank(RFX).

Consequently min(t,ℓ)≤rC↓+rB↑. This proof covers ℓ=0 and needs no nonzero generator or chart normalization.

For the mirror bound, take the first t columns, a0=min J0, the last N−t Fourier rows, and the first a0 input coordinates. The kernel has basis k↦ζ^(−rk), r=0,…,t−1. The same consecutive-coordinate Vandermonde calculation yields min(t,a0)≤rC↑+rB↓.

Invertibility of C is essential to the stated factorization application because it makes the selected columns independent. More generally, the proof works whenever these selected columns alone have rank t. It does not require B to be independently assumed invertible, although B is invertible under the full stated hypotheses.

For a last-three-column set {1,2,5}, min(3,N−6) equals two at N=8 and three for every N≥9. Thus the indicated pair of rank-one stages is excluded for all N≥9 with this fixed trailing set. The theorem applies to arbitrary permutations one at a time; this application is not an exclusion of all permutations. Nor does passing either test prove feasibility. The source's sharpness statement concerns arbitrary selected-column spaces, not realization of a complete two-stage factorization.

The four stated numerical Fourier restriction determinants were independently reproduced: 1099 at (N,p,ζ)=(16,12289,4134), 121 at (16,65537,64), 2858 at (32,12289,5860), and 4461 at (64,12289,7311).

## 2. Theorem B: complement equivalence and its hypotheses

Assume the same root/field conditions and an integer b≥1 with N≥2b. Define the tail subspace by Lk=Σ(r=1…b) αrζ^(rk) on k=b,…,N−1. For i=0,…,N−b−1 every exponent i+r lies strictly between zero and N, giving

Σ(k=b…N−1) Lkζ^(ik)=−Σ(j=0…b−1) ζ^(ij)Σ(r=1…b) αrζ^(rj).

This is an exact matrix identity. The output lies in the fixed span of the first b characters in i. The coefficient map from α to these b low-character coefficients is a square Vandermonde matrix times nonzero scalings, so it is invertible. Both tail and output spaces have dimension b because N−b≥b. Finally, the map from all N−b tail coordinates to the first N−b Fourier outputs is a square Vandermonde matrix with distinct nodes ζ^b,…,ζ^(N−1), hence invertible. These facts prove the converse, not merely inclusion. The case b=0 can be handled trivially if desired.

For N=8,b=3 the rescaled lower sequence satisfies both order-three recurrence equations identically, even where Δ or T vanishes. Its five values L3,…,L7 therefore form the three-frequency tail. The audit independently recovered the three frequency coefficients by Cramer's rule from L3,L4,L5 and verified all five identities.

Write vj=(ζ^(ij)) for i=0,…,4. For Y2, its first column is v2, its upper column is U0v0+U1v1, and its lower tail is in span(v0,v1,v2). For Y1, the first and upper columns are v1 and U0v0; its lower column adds L2v2 to that same spectral tail. Thus every one of the six columns in [Y1,−Y2] lies in the same fixed three-dimensional space. This is the precise bridge from the all-length identity to the polynomial gate.

## 3. Theorem C: all maximal minors, including exceptional parameter values

Use the exact inherited rescaled Uhat,Lhat family and the fixed N=8 gate. The first five rows have rank at most three. The middle block has five rows, and the last row is the cofactor compatibility row. A nonzero nine-row determinant must therefore select exactly three top rows, all five middle rows and the final row. There are ten such choices, leaving 45 zero determinants.

For an eligible top-row set R, Laplace expansion along the Y2 column block gives precisely −det(Y2[R,:])·DH with the stated column signs. Let V=[v0,v1,v2]. Its three-row minors are ordinary Vandermonde determinants and all are nonzero because the selected nodes are distinct. Since Y2 lies in col(V),

det(Y2[R,:])·det(V[0,1,2,:])=DB·det(V[R,:]).

Thus every eligible maximal minor is a nonzero constant multiple of Dhat, and rank K≤8 if and only if DB·DH=0. The audit explicitly computed the full determinants; it did not infer their equality only from numerical samples or from the structural rank proof.

The ring computations use Q[z]/(z⁴+1). Every polynomial coefficient in the rebuilt generators, factors and determinant identities is integral in 1,z,z²,z³. The exact cross-product identities therefore also hold over Z[z]/(z⁴+1). The rank equivalence is stated over C (or the cyclotomic field), where the nonzero Vandermonde constants are invertible. No unsupported claim about arbitrary reductions or integer-ring pointwise rank is needed.

The identity is valid at every parameter point of this polynomial family, including zero rescaled generators. That does not make all of those points valid original normalized stages. When relating back to the Fourier factorization, retain h0ΔT≠0 on the regular chart and all inherited inverse, anchor, boundary and invertibility guards. Singular excluded branches require their own treatment.

The prior audit's structural-lemma correction also remains: the factorization application uses invertible C, and the case of a zero fourth output multiplier is handled by rank(Y4)≤2, forcing its cofactor vector to vanish. The new collapse theorem does not weaken or replace those conditions.

## 4. Theorem D: absolute irreducibility, with an exact refinement

The independent DB has nine nonzero terms and degree two. Its degree-two homogenization in (h0,h1,h2,h6,q) has a symmetric matrix M with integral cyclotomic entries. The upper-left 4×4 determinant is exactly

−13568−492544z+709888z²−511488z³,

whose reduction at (p,z)=(12289,8246) is 11251. Hence it is a nonzero cyclotomic number and rank M≥4 over C. The exact 5×5 determinant is zero, and the lower-right 3×3 block is zero, so the rank is exactly four.

Any nontrivial factorization of an affine quadratic over C would homogenize to a product of two linear forms. The symmetric matrix of such a product has rank at most two. Rank four therefore proves absolute irreducibility. This gives a restriction on the geometry of the rank-drop factor; it does not exclude points on DB=0.

The exact rank-four calculation also identifies a unique affine singular point, with h0=h1=0 and explicitly recorded h2,h6 in `symbolic_results.json`. Its existence follows because the 2×2 cross block in the first four variables has nonzero determinant; the recorded coordinates satisfy Mx=0 exactly with q=1. Consequently DB=0 is smooth on the inherited regular h0≠0 chart. This bounded refinement does not remove the quadric branch or settle any remaining compatibility equations.

## 5. Auxiliary boundary-lock identity: exact proof and N=8 exception

The source file `boundary_lock.py` refers to a `PROOF.md` absent from this new package; its all-length algebraic claim is otherwise presented through finite tests. Here is a complete proof for the stated matrix.

Let N≥9, use i=0,…,N−4, and let vj=(ζ^(ij)). Suppose Lk=Σ(r=1…3) αrζ^(rk) on k=3,…,N−1. Form

M=[v0,v1,v2,v5, Σ(k=0…4) Uk vk, Σ(k=6…N−1) Lk vk].

Theorem B gives Σ(k=3…N−1) Lk vk in span(v0,v1,v2). Subtract combinations of the first four columns from the last two. The matrix becomes

[v0,v1,v2,v5, U3v3+U4v4, −L3v3−L4v4].

Since N−3≥6, the six vectors v0,…,v5 are independent by the Vandermonde determinant on the first six output coordinates. It follows exactly that

rank M=4+rank [[U3,−L3],[U4,−L4]],

and hence rank M≤5 if and only if U3L4−U4L3=0. No boundary value is divided out: this includes the all-zero boundary case (rank four), proportional nonzero boundary case (rank five), and nonzero determinant case (rank six).

With columns ordered as above, the first-six-row determinant is

det M[0:6,:]=−(U3L4−U4L3)·∏(0≤i<j≤5)(ζ^j−ζ^i).

The multiplier is nonzero. All six source constants at N=16,32,64 in the two listed prime fields were independently reproduced directly from this product. Fresh controls additionally cover N=9,10,11,12,15,24 and deliberate zero-boundary cases.

At N=8 the matrix has only five rows, so rank≤5 is automatic and implies no boundary lock. For an explicit characteristic-zero counterexample to the converse, take α=(1,0,0), U3=1, U4=0. Then L4=ζ8⁴=−1, so U3L4−U4L3=−1 despite rank≤5. In fact the rank is five: its coefficient matrix relative to the six Vandermonde columns is invertible, and those six columns span a five-dimensional space on the five output coordinates. The checker also verifies this example at p=17,z=9.

## 6. Reproduction, provenance and limits

Run from any working directory with Python 3 and SymPy installed:

    python independent_symbolic_audit.py
    python independent_modular_audit.py

Paths are resolved from each script's own location. The package contains all inert comparison inputs under `input_data/`; prior executable files are not dependencies. The symbolic checker completed in roughly half a minute and the modular checker in roughly two seconds on this execution environment. These timings describe verification work, not Fourier algorithm performance.

`source_hashes.json` identifies every new archive-root input by SHA-256, records the copied local inert inputs, and marks older audit references as provenance only. All 20 entries in the supplied source checksum manifest matched. The nested prior-checkpoint ZIP has SHA-256 `ef1a6c9e74d505ca074ea5d4d87cfe7ff5ccd4c60216051987680626f9f4481a`; the prior review is carried forward rather than rerun wholesale.

This review makes no novelty claim and needs no external prior-art assertion. It does not promote the experimental `lower_gate.py` into a new theorem, or treat seeded permutation statistics as algorithmic evidence. The exact target remains all Fourier outputs for arbitrary fresh inputs with the full arithmetic cost charged. No asymptotic or practical runtime improvement is established by this archive.
