# Independent audit of HERO0 Phase22 transverse bridge exclusion

10 October 2026

## Verdict and scope

The four-axis-term target-only bridge obstruction is accepted. The all-real-fixed-background exclusion for every square length N=s² with s≥7, the uniform relative Frobenius lower bound sqrt(max(0,1/2−5/s)), the diagonal-background bound, and the stated phase-fiber necessary condition are supported by direct proofs. Fresh code independently reproduced all eight pinned modular certificates and all six exact rational-cyclotomic coefficient vectors.

One implementation qualification is needed: the submitted minor-query routine constructs two lists of length s−1. Its field arithmetic is constant per queried minor, but its index/list work is Θ(s). Thus a complete scan of all N rectangles has Θ(N√N) index/list work in the submitted Python, although only O(N) field operations. The advertised O(N) total-work scan requires the small index-selection repair described below. First-minor rejection including O(N) preprocessing remains O(N) overall in the stated unit-cost model.

These conclusions concern two-stage rook-supported factorizations with one transverse path fixed. Joint tuning of both fully complex transverse paths remains unresolved here. No general Fourier-computation lower bound, new fast transform, or externally novel result is established.

## Mathematical evidence and provenance

The accepted statement was checked by independently reconstructing dense modular Green inverses and exact rational cycle entries. Every one of eight pinned modular minors and six characteristic-zero coefficient vectors was reproduced. The submitted program was inspected as text; source execution logs were not used as independent evidence. The archive and mathematical source hashes are recorded in SOURCE_MANIFEST.json.

The accompanying portable verifier retains the mathematical checks and comparison data. Original-archive integrity checks are recorded as provenance, not rerun without the original archive. Explicit seed-19 integer arrays define the pinned backgrounds; reproducing a pseudo-random generator alone is not a substitute for those arrays.

## Division free full target identity

Throughout, F_N[i,j]=ω_N^(ij) is the unnormalized Fourier matrix. Thus ||F_N||_F=N=s². For unitary normalization U_N=F_N/s, the same relative-error statements compare U_N with T/s. Scaling the target alone while leaving a pinned fixed background and coefficients unchanged is a different exact-equation problem; the listed modular minors are for the specified unnormalized target.

Use row-major indices (x,y)↦xs+y. A horizontal matrix preserves the second coordinate; a vertical matrix preserves the first. Write

T=(B+V)(A+H),

where H is horizontally supported, V vertically supported, and A,B are fixed rook-supported matrices. This covers the four-edit family with A the two fixed input-vertical terms and B the two fixed output-horizontal terms, and also the smaller selected-pair family with six fixed terms.

For x≠a and y≠b, exactly two intermediaries can contribute to the product: (x,b) and (a,y). At (a,y), both variable terms vanish by support. Therefore

T[(x,y),(a,b)] = B[(x,y),(a,y)] A[(a,y),(a,b)]
  + (B+V)[(x,y),(x,b)] (A+H)[(x,b),(a,b)].

For fixed x,b, define Q[y,a] as the first product and W_F[y,a]=F[(x,y),(a,b)]−Q[y,a], restricting y≠b,a≠x. Exact equality T=F implies W_F=u qᵀ, so rank(W_F)≤1. Exchanging the coordinate roles proves the reverse orientation.

This is a full finite target equation. It includes the one-sided changes and requires no division by a bridge entry, no nonzero-coordinate chart, and no Hessian normalization. Zero vectors u or q give rank zero and are allowed. Undefined Green inverses are not factors in the original Green model; if finite supported limiting matrices exist, the support identity continues to apply to those matrices.

All rank-one tests remain necessary rather than sufficient. Different rectangles share factor entries, the on-rook equations remain, and Green factors satisfy additional cycle constraints. Testing only one selected minor per rectangle is weaker still: the matrix diag(1,0,1) has a zero leading 2×2 determinant but rank two.

## Exact modular and characteristic zero evidence

Both orientations were rebuilt independently. Every one of the N=s² Fourier residual blocks had rank s−1; every original-network residual block had rank one.

| N | Field | Forward first minor | Reverse first minor | Fourier block rank |
|---:|---:|---:|---:|---:|
| 9 | 109 | 65 | 44 | 2 |
| 16 | 65537 | 46990 | 5754 | 3 |
| 64 | 65537 | 8970 | 35649 | 7 |
| 256 | 65537 | 24394 | 34918 | 15 |

At N=16,64,256, all six sparse coefficient vectors in Q[z]/(z^(N/2)+1) were independently reconstructed with rational coefficient 1/4 and the same integer weights. They match the submitted vectors exactly and reduce to the listed nonzero modular minors. This proves nonvanishing for the particular rational frozen backgrounds over C, for any primitive complex Nth root by Galois conjugacy.

This argument does not infer complex nonexistence from a failed search over a finite field. It proves a necessary expression in the frozen data and target is nonzero. Arbitrary other lifts of modular weights are different backgrounds.

Fresh reachable controls additionally cover both orientations with arbitrary full rook-supported A,B and arbitrary supported H,V at s=3,4,7. Complete cancellation of the variable bridge gives rank zero in every block and still satisfies the exact identity. At each of N=9,16,64,256, setting all four adjustable Green weight arrays to zero gives four identity pencils, hence valid inverses, and rank zero in every residual block. These explicitly test the zero-bridge branch.

## Generic and diagonal background conclusions

At zero frozen weights each Green term is I, so A and B are diagonal and the opposite off-rook bridge is zero. The canonical 2×2 Fourier determinant is ζ_s^4(ζ_s−1), nonzero for s≥3. Resolvent denominators are 1 at this point. Clearing them gives a nonzero polynomial, proving a proper algebraic exceptional set for the frozen backgrounds.

For every fixed rectangle the full residual at this specialization is a row/column phased copy of an (s−1)×(s−1) Fourier minor. It is invertible because the corresponding inverse-Fourier cofactor is nonzero. A finite product of these determinants gives simultaneous generic full rank in both orientations. Interpret this as an algebraic genericity statement over an infinite field or algebraic closure; it does not assert the existence of a nonzero-coordinate rational point in every small finite field. A finite-field probability statement needs its explicit field-size and invertibility conditioning.

For diagonal A,B, the squared singular values of each Fourier block are s repeated s−2 times and 1 once. Its best rank-one squared error is s(s−3)+1. The N rectangles partition the off-rook entries, giving

||F_N−T||_F / ||F_N||_F ≥ sqrt(1−3/s+1/s²).

This is a lower bound for the full constrained network. The audit does not claim that independently optimal approximants to all blocks assemble into globally admissible factors.

## Every real fixed background fails when s is at least seven

At the canonical rectangle x=b=0, let M=F_s[1:,1:] and let J=Im M. If A,B are real, Q is real. If W_F=u qᵀ, then

J=Im(u qᵀ)=Re(u) Im(q)ᵀ+Im(u) Re(q)ᵀ,

which has real rank at most two.

Let P reverse nonzero residues by j↦s−j. Direct sine orthogonality gives

J Jᵀ=(s/2)(I−P).

The number of two-cycles of P is r_s=(s−1)/2 for odd s and (s−2)/2 for even s. Hence J has precisely r_s nonzero singular values, all sqrt(s). For every s≥7, r_s≥3, contradicting the necessary rank-two bound. The reverse orientation has the same canonical block. Adjustable factors may be fully complex and have arbitrarily large finite entries; no conditioning assumption is needed.

The rank calculation is over R. The outer-product condition is rank at most one over C. Conflating these ranks would incorrectly lower the threshold. At s=3,4,5,6 this particular argument is inconclusive, not an existence proof.

## Uniform real background approximation bound

For any forward rectangle, first restore the excluded row and column. The full s×s Fourier block is

C[y,a]=ζ_s^(xb) ω_(s²)^(yb) ζ_s^(ya).

It has operator norm sqrt(s). For J_full=Im C, summing sin² over a gives

||J_full||_F² ≥ s²/2−gcd(s,2)s/2.

Only rows with s dividing 2y contribute to the exceptional cosine sum. Removing one row and one column loses at most 2s of squared norm. Also ||Im C_restricted||_2≤||C_restricted||_2≤sqrt(s): for a real input vector, taking the imaginary part cannot increase Euclidean norm. Therefore the squared best real-rank-two tail is at least

max(0,s²/2−[4+gcd(s,2)/2]s) ≥ max(0,s²/2−5s).

The fixed bridge is real, so each candidate imaginary block has rank at most two. Summing the N disjoint rectangle errors and using ||F_N||_F²=s⁴ proves

||F_N−T||_F / ||F_N||_F ≥ sqrt(max(0,1/2−5/s)).

The reverse orientation is identical after exchanging row and column roles. The displayed bound is zero at s≤10, which does not weaken the separate exact impossibility for s≥7. At s=16 it is 0.4330127; at s=32 it is 0.5863020; its asymptotic limit is 1/sqrt(2).

Fresh numerical checks of the exact sine Gram identity cover every s from 3 through 33. Fresh per-rectangle singular-tail checks cover s=3,4,5,6,7,8,11,16,32 and reproduce the submitted numerical aggregate values at s=8,16,32. These floating-point checks support the proof and are not certified interval bounds.

## Complex phase fibers

Assume real stage coefficients. If non-real weights of the fixed horizontal group occupy u second-coordinate fibers, and those of the fixed vertical group occupy v first-coordinate fibers, the imaginary fixed bridge is supported on u rows and v columns. Therefore its real rank is at most k=u+v. The necessary exact condition is

k≥r_s−2.

The same support bound holds in every rectangle. Its imaginary candidate rank is at most k+2, yielding the valid conservative bound

||F_N−T||_F / ||F_N||_F ≥ sqrt(max(0,1/2−(k+5)/s)).

These are necessary phase-structure conditions. They give no obstruction once an unrestricted fully complex fixed bridge supplies sufficient phase rank; both complex paths jointly adjustable remain outside the present conclusion.

## Reconciliation with the accepted selected pair obstruction

The earlier selected-pair proof remains in the unchanged 12:20 supplement, notes/01_selected_pair_obstruction.md. Its accepted source SHA-256 is 0fd2b9ce370d7e629b9c929883d40a31c45386d02baf758bbff8691e1b4c3be4. Only the exact background arrays needed by the current bridge verifier are repeated here.

That result fixes six terms and edits input term π_1 and output term π_3. It derives a four-column target-only matrix with rank at most three, by eliminating one complete new weight from the full target equations. Its nonzero 4×4 minors certify N=4,16,64,256 for the pinned rational and modular backgrounds.

Phase22 fixes only four terms and allows both horizontal input and both vertical output terms to vary, or the reverse. At N=16,64,256, its exclusions therefore contain the earlier selected-pair exclusion as a subfamily, and they also cover the other opposite-axis selected pairs. The actual frozen integer arrays agree. The new ranks and minor values are different invariants and should not be substituted into the earlier four-column test.

At N=4, each transverse block is 1×1, so rank≤1 is automatic. Keep the earlier N=4 certificate; it is not replaced by this bridge test.

The earlier warning about the mixed-Hessian normalization remains unchanged: the normalized complete edit can have full rank, while only the four-point mixed difference has the applicable normalized rank-one structure under its chart assumptions. Phase22 bypasses that issue with an independent support identity; it does not retroactively validate an invalid complete-edit Hessian test.

## Implementation cost correction

In phase22_bridge_gate.py, one_minor calls rectangle_indices, which materializes every eligible row and column before retaining the first two. For s≥3, that creates 2(s−1) indices per query. A full N-rectangle scan therefore performs Θ(Ns)=Θ(N√N) such index/list work.

This does not contradict the narrower O(N) field-operation count: each minor evaluates only four entries, and the list work is integer/index work rather than field arithmetic. It does require correcting a claim of constant total work per minor or O(N) fully charged total scan work for the submitted implementation. Early rejection on the first block still costs O(N) overall after preprocessing.

A direct constant-work repair is available without changing the mathematics. For an excluded coordinate e, the first two retained coordinates are k+[k≥e] for k=0,1. Build only those two row indices and two column indices, then query the same four entries. After linear cycle/root preprocessing, that version supports O(N) total unit-cost work for the complete scan. No submitted file was modified during this audit.

## Reproduction and boundaries

See REPRODUCE.md for the portable Python/NumPy verifier and exact comparison data. The report under certificates/bridge contains mathematical outputs; source hashes are recorded separately. The verifier imports no submitted program. Floating-point singular-tail diagnostics support the exact proofs and are not interval certificates.



Historical test counts, larger-length timings, and external publication priority are not re-certified here.
