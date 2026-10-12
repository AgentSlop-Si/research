# Independent review of the ACWL lift normal form

Date: 2026-10-12. Verdict: ACCEPT BOUNDED, subject to the exact source bindings in SOURCE_BINDINGS.json.

The reviewed normal form and support obstruction are correct for the prescribed positive-sign, bit-reversed-input, increasing-size DIT base. They extend the earlier singleton obstruction to a precisely declared inverse-sparse grammar that can mix entire coarse residue fibers. They do not establish a universal Fourier arithmetic lower bound, a faster transform, or novelty. No supplied historical or author program was executed in this review.

## Accepted scope

For N=2^w and 1≤r<s≤w, put q=2^r, h=2^(s-r), Q=2^s, and m=N/Q. Over the complex numbers or a field containing a primitive N-th root, the following claims are accepted:

1. The conjugated operator P=M_r X_s M_r^-1 has m disjoint weighted cycles of length h in every coarse residue fiber. There are q m=N/h cycles globally. The number of cycles is not h in general.
2. Every solution of C P=Z_s C is C=A M_s M_r^-1 with A commuting with Z_s. This includes singular solutions; invertibility is exactly invertibility of the Q independent m-by-m blocks of A.
3. Every row of an invertible C, and every column of C^-1, has support a positive multiple of h. The minimum h is attained by the standard correction.
4. A single correction C=D_L B^-1 D_R, where B has at most K entries per column and the outer factors are invertible monomial matrices, requires K≥h. In particular, a sum of K weighted permutations meets this column sparsity bound regardless of how its permutations are chosen.
5. For a product of L such factors with column bounds K_1,…,K_L, including invertible monomial routings between factors, ∏K_j≥h is necessary. With constant K≥2, L≥ceil(log_K h).
6. At an evolving base G_r M_r, the bound applies to (C_tilde G_r)^-1. If G_r^-1 has maximum column support S, the necessary condition becomes S∏K_j≥h. A bound for an isolated standard base must not be silently transferred to the actual later ladder base.

The candidate states these qualifications correctly. No revision to its mathematical claims was required by this review.

## Independent proof and convention checks

Use X e_j=e_(j+1), so right multiplication of a matrix by X^m shifts its column labels by minus m. This sign is important: the resulting operator P acts on basis columns in the positive cycle direction.

Write d=mh and zeta=omega^d. Index a partial-transform output by (a,ell), with a=rev_(w-r)(b) and physical coordinate qb+ell. Then P sends a to a+m modulo d, with weight zeta^ell exactly when that addition wraps. Writing a=v+mu gives a cycle of length h for each (v,ell), where 0≤v<m. Reversing the binary digits converts this to the candidate's exact physical coordinate

K(ell,beta,u)=Q beta+q rev_(s-r)(u)+ell,

with v=rev_(w-s)(beta). Thus the candidate's column-action formula, bit order, and wrap phase agree with direct conjugation. The boundary case w=s uses rev_0(0)=0 correctly.

For a left eigenrow v of eigenvalue lambda, the equation vP=lambda v gives v_(u+1)=lambda v_u. The wrap closes exactly when lambda^h=zeta^ell. Consequently the left progression is lambda^u, while a right eigenvector has progression lambda^-u. Neither progression contains a zero unless the entire cycle contribution vanishes. The Q eigenvalues lambda_(ell,t)=omega^(m(ell+qt)) are distinct, each repeated across exactly m cycles.

The standard correction C0=M_s M_r^-1 satisfies C0 P=Z_s C0 and is invertible. Therefore C P=Z_s C if and only if A=C C0^-1 commutes with Z_s. The latter commutant has one m-by-m block for each residue modulo Q. Its dimension is Qm^2. Multiplication by the invertible C0 preserves rank, proving rank C=Σ rank A_(ell,t) and the invertibility criterion.

On a single cycle, the matrix with rows lambda_(ell,t)^u is a positive Fourier matrix followed by a diagonal phase mask. Its inverse is h^-1 lambda_(ell,t)^(-u). The factor h^-1 exists because a field with a primitive 2^w-th root has characteristic not dividing 2^w. The candidate's entrywise formulas for C and C^-1 therefore have the right sign, index order, and normalization.

Independently of the entry formula, C P=Z_s C implies P C^-1=C^-1 Z_s. Hence every column of C^-1 is a nonzero right eigenvector of P. On each occupied cycle, its recurrence forces all h entries nonzero; different cycles have disjoint coordinates, so inter-cycle cancellation cannot remove those entries. Each inverse column has at least h nonzeros. The same left-eigenrow argument proves the row claim for C.

If C=D_L B^-1 D_R, then C^-1=D_R^-1 B D_L^-1. Multiplication on either side by an invertible monomial matrix only permutes and nonzero-rescales coordinates or columns, preserving the multiset of column support counts. If D_L and D_R were merely declared square diagonal matrices, invertibility of C and B would already force both diagonals invertible. Singular diagonals are not an escape.

For arbitrary matrices U,V, a column of UV is a linear combination of at most the number of nonzeros in that column of V columns of U. Thus maximum column support satisfies sigma(UV)≤sigma(U)sigma(V). Cancellations can decrease support but cannot violate this upper bound. Applying it to the reversed product of factor inverses proves ∏K_j≥h. This proof requires no assumption that intermediate factors individually solve a covariance equation.

Finally, C_tilde acting on G_r M_r is a lift exactly when C_tilde G_r is a standard-base lift. Its inverse is G_r^-1 C_tilde^-1, giving h≤S∏K_j. The order of this product is correct. Choosing G_r=C0 makes the already-lifted base M_s, where C_tilde=I is valid; this supplies an explicit reason to retain the evolving-base qualification.

## Scope boundaries and escape controls

The safe translation by q moves coordinate 1 and destroys the earlier common singleton invariant. With arbitrary coordinate diagonal projectors and unrestricted algebraic sums and products, it generates every matrix unit E_ij with i≡j modulo q. Thus the enlarged algebra is the whole coarse commutant. This is an expressivity statement; it provides no bound on the number of generators, preparation work, or solve cost.

At N=256,r=2,s=4, h=4. Accordingly, D_L(D_0+D_1H+D_2T)^-1D_R cannot be a valid invertible standard-base correction: its inverse columns have at most 3 entries. The proof covers all coefficients for which the displayed inverse and outer factors exist. An isolated failing numerical example is unnecessary for this universal restricted conclusion.

The product theorem excludes constant width and constant depth as h grows within this grammar. It does not convert support into a general arithmetic lower bound. In particular:

- A sum of inverse-sparse factors is not a product of such factors. Its inverse may be dense. As a scope control, I-2R on a 4-cycle is a sum of two invertible monomial terms, while its inverse has four entries in every column over F_257. This is not itself a covariance-lift construction; it only demonstrates why the proof cannot be reused for an additive grammar.
- An auxiliary-variable solve, elimination, Schur complement, or scattering network can have a dense effective inverse even if its larger system matrix is sparse. Such a model needs a separate analysis.
- A different covariant base can already be s-covariant, permitting the identity correction. The standard-base hypothesis is substantive.
- Algebraic equivalence to small Fourier blocks does not force every arithmetic circuit to materialize those blocks, and an unrestricted dense A is not free.
- Sparse sums of several permutations do not have a certified linear-cost inverse application merely from their sparsity or a Green-resolvent label.

## Fresh exact controls

The newly written fresh_exact_controls.py uses only standard-library Python and integer arithmetic modulo 257. It verifies primality of 257 by trial division and verifies that 3 has order 256. It imports no candidate, historical, or project code. It was written from the mathematical definitions and run independently.

The 40 cases are every 1≤r<s≤w for 2≤w≤6, and five N=256 pairs (1,8), (2,4), (2,8), (4,8), (7,8). The largest cycle length tested is 128. All pass. The exact machine-readable results and run log accompany this review.

Checks include:

- Partial transforms constructed through iterative positive DIT stages, with both products against their explicit inverses equal to identity
- Direct conjugation by the shift and comparison of every weighted permutation entry against the independent cycle formula
- Global and per-fiber cycle counts, length h, and wrap products
- The standard correction, its inverse, and the full lift equation
- Exact support h in every canonical inverse column
- Nontrivial mixing of repeated-eigenvalue blocks, with all inverse-column supports positive multiples of h
- Q distinct eigenvalues, each with multiplicity m, with invertibility supplying independent eigenvectors
- Two actual N=8 DIT correction stages whose inverses each have exactly two weighted-permutation terms and whose product attains h=4 support
- Singular-diagonal exclusion, an already Fourier-transformed base, an evolving intermediate base, and the additive-sum escape control described above

These exact finite-field checks are convention and implementation controls for the proofs. They are not substitutes for the field-independent proof, exhaustive searches over coefficients, arithmetic lower bounds, or novelty verification. The author’s separate reported numerical controls were read as source claims; this review does not claim to have replayed the author's program.

## Source integrity and handoff

SOURCE_BINDINGS.json identifies and hashes the original supplied manuscript, the earlier first review, the final author report, and the sealed candidate materials. Copies of the reviewed prose are included for independent reading. MANIFEST.json covers this review's own files. The archive seal binds the resulting review ZIP by byte count and SHA-256. The review is additive and does not alter the supplied manuscript or author artifact.

Recommended research status: retain the ACWL framework as a candidate with accepted standard-base normal form and accepted restricted inverse-sparse support obstruction. Keep arbitrary additive or auxiliary-variable scattering packets, their actual evolving bases, and their uniform paid implementation costs open. Do not promote the candidate to an exact O(N log log N) Fourier algorithm, and do not close the enlarged program using this bounded result.
