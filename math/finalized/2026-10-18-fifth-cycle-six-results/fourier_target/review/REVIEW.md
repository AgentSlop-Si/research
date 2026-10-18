# Independent review: unrestricted F8 reduction and resource blocker

18 October 2026. Reviewed packet: `unrestricted_f8_20261018_1919`.

## Verdict and exact acceptance scope

**ACCEPT the original-system encoding, zero-safe necessary inverse reduction, support-aware lifting criterion, and recorded bounded-computation blocker. The unrestricted F8 target is still UNDECIDED.** Keep M-NONLINEAR-COMPATIBILITY **TO RESEARCH, priority 34**.

No mathematical correction to the candidate report is required. Acceptance does not mean that either ideal is proper or the unit ideal. No original witness, characteristic-zero infeasibility identity, image-excluding polynomial, or exhausted zero component has been established. Neither the numerical attempts nor the tangent probe contributes to this acceptance as nonexistence evidence.

The reviewed candidate report has SHA-256 `a6b713f0ea26cfde4742a50663b7afa2801523c3395e74d5a53e8d3fa135557e`. All 42 entries in its manifest matched their recorded lengths and hashes; the packet contains those 42 files plus its manifest. The review did not modify the candidate packet or write externally.

## Independent mathematical review

### Original chart, field, and permutation

The retained original source explicitly uses S[i,i]=d[i], S[i,j]=l[i]m[j] for i>j, and S[i,j]=u[i]v[j] for i<j. Its fixed permutation is p=(7,0,6,3,4,1,2,5), with P e_j=e_p(j), and the target is B P A=F. Thus the displayed 64 equations sum B[i,p(k)]A[k,j] and subtract z^(ij), exactly as emitted.

The four absent endpoints per stage are precisely l[0], m[7], u[7], v[0]. All other 72 variables occur. Adding back these eight freely varying parameters is a polynomial-ring extension, so the executable 72-variable ideal and the displayed 80-variable ideal have the same properness and solution existence. No nonzero generator or normalized-chart hypothesis enters this ideal.

The polynomial z^4+1 is irreducible over Q: translation by 1 gives x^4+4x^3+6x^2+4x+2, Eisenstein at 2. The quotient is therefore a characteristic-zero field. Its distinguished z has order eight. Independent exact coefficient arithmetic verifies both Fourier inverse products and, by the Vandermonde product, det(F)=4096 z^2. Hence every target solution has invertible A and B. No determinant saturation is necessary in the original ring.

The explicit inverse permutation is (1,5,6,3,4,7,2,0). From B P=F C, with C=A^-1, one gets B[i,p(j)]=(F C)[i,j]. The inverse-relaxation code uses this convention, including the harmless sign arising when its two B columns are listed in p-order rather than sorted order.

Properness means existence over an algebraic closure of K, not necessarily over K itself. The exact attempt in QQ[72 stage variables,z] with z^4+1 adjoined is the same quotient problem over K; it is not a finite-field specialization.

### Ladder minors and inversion without principal-block assumptions

Each strictly lower 2-by-2 minor, with column indices a<b and row indices r<s satisfying b<r, lies in a strict lower cut block. Conversely every 2-by-2 minor of a strict lower cut block has this form. The analogous upper assertion holds with s<a. Thus the 70 lower and 70 upper minors are equivalent to rank at most one for each strict off-diagonal cut block. They are necessary for the stage chart, but do not describe its full zero boundary exactly.

For an invertible X and a coordinate decomposition V=E direct-sum H, let projection to E identify the E-by-H block. Then

rank X[E,H] = dim(H) - dim(XH intersect H).

The corresponding formula for X^-1 uses X^-1 H intersect H. Multiplication by X is an isomorphism from X^-1 H intersect H onto H intersect XH. The dimensions, and therefore the two ranks, coincide. Interchanging E and H proves the other orientation. This argument remains valid when either principal diagonal block is singular.

Consequently an invertible original A yields L(C)=0 for C=A^-1, and B=F C P^-1 yields L(B)=0. Adjoining t det(C)-1 gives the stated 65-variable system J, with 280 quadrics and one degree-nine equation. Every original target solution lifts to a point of J. An exact unit-ideal identity for J would therefore exclude all original solutions, including all generator-zero cases. Properness of J alone would not supply an original target witness.

### The support-aware lift is necessary and sufficient

For a lower triangle, let R and S be its nonzero row and column index sets. If the triangle factors as l[i]m[j], then every allowed edge i>j in R times S must be nonzero. Zero triangles are covered by zero factors.

Conversely, assume all ladder minors vanish and that this support condition holds. Write r=max(R), s=min(S). Every active row index i satisfies i>s, and every active column index j satisfies j<r. The pivot T[r,s] is therefore an allowed nonzero entry. Taking l[i]=T[i,s] and m[j]=T[r,j]/T[r,s] on the active sets gives the required products: for non-pivot active entries, the minor with rows i,r and columns s,j is wholly strictly lower and equates T[i,j]T[r,s] with T[i,s]T[r,j]. Pivot row and column entries are immediate. Outside the active sets, both sides vanish. Transposition gives the upper result independently; the diagonal is unrestricted.

This is a genuinely zero-safe criterion. For an algebraic J-point C, one must apply it to both C^-1 and F C P^-1, recover generators, and check all 64 original equations. The candidate checker additionally verifies reconstructed products directly.

The counterexample is valid: the cumulative lower triangular matrix A[i,j]=1 for i>=j is an original stage with determinant one. Its inverse has diagonal 1, first subdiagonal -1, and all other entries zero. Both inverse products are exactly the identity and all ladder minors vanish. However C[1,0] and C[2,1] are nonzero while C[2,0]=0, contradicting a globally separated lower factorization. Therefore parametrizing C as another original stage would discard legitimate inverses. This counterexample does not claim to be a Fourier factorization.

## Independent executable evidence

Only the new standard-library `review_checks.py` was executed. No candidate program, historical research program, elimination, optimizer, or tangent search was run. Its successful execution took approximately 0.38 seconds in the recorded tool call.

The script performed stronger transcription checks than point evaluations:

- Verified every one of the 42 candidate manifest entries, plus exact packet file coverage.
- Recomputed all three retained-source Git blob hashes and SHA-256 hashes. The two source files with declared pinned blobs matched those pins. The restriction-frontier source has no declared remote Git-blob pin; its retained local bytes are hash-bound, and this review does not independently attest its remote contents.
- Independently constructed and compared all 64 original polynomials as sparse symbolic polynomials over Q[z]/(z^4+1).
- Independently constructed F C P^-1 and compared all 280 emitted quadrics with direct 2-by-2 minors, verifying that each matrix contributes exactly the complete set of 140 ladder minors.
- Independently parsed all 344 corresponding expressions in the two Singular files and checked exact symbolic agreement, ring variables, field relation, row-major C matrix, and the determinant-invertibility equation. Singular itself was not executed.
- Verified det(F)=4096 z^2 and all 128 entries of the two inverse products with separate exact arithmetic.
- Exhaustively checked the support-aware lifting equivalence on all 729 signed ternary lower triangles of size four.
- Counted actual distinct supports from all lower row/column masks in size eight, obtaining 7,280, hence 2,808,830,402,560,000 for the naive four-triangle product. This remains only a scale count, not a statement that every pattern is target-feasible or requires separate enumeration.
- Verified the cumulative-triangular/bidiagonal inverse boundary directly and checked consistency of the resource logs with the exact-attempt source and status.

The general inverse and support-lifting statements are supported by the proofs above; finite controls do not substitute for those proofs. Numerical provenance records twelve starts and minimum recorded residual 0.66014477471011, consistent with the candidate summary. Those files were read and hash-bound, without rerunning or upgrading their conclusions.

## Resource blocker and remaining completion interface

The inspected attempt constructs the complete 64 original polynomials and z^4+1, uses SymPy 1.14.0 F5B over QQ in 73 variables with grevlex order, and requests soft/hard CPU limits of 180/185 seconds and a 1 GiB address-space limit. The saved start event agrees. The retained exit record states CPU time limit exceeded and exit 152, consistent with SIGXCPU. Only a start event is present; no returned basis or certificate file is present. The saved record supports a resource-blocked, inconclusive run. This review did not independently rerun or instrument that process, and does not certify a minimum resource requirement for other methods. No memory-exhaustion event is recorded.

The residual is still the entire unrestricted original ideal, or alternatively the full necessary inverse ideal as a sufficient exclusion route. No zero-support component has been disposed of. Completion still requires one of the report's exact interfaces: an algebraic original witness with all 64 checks, an exact lifted unit identity for the original ideal, an exact lifted unit identity for J, or a proved image-vanishing polynomial nonzero at F. A finite-field emptiness report, an unsuccessful optimizer, a tangent normal, or a bare unverified solver claim cannot replace that interface.

This review accepts a complete explicit reduction and a documented computation limit. It does not accept closure of the original target gate.
