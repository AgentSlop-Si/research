# Binary Fourier-mask degrees at order 5q

**Complete degree classification.** Let q>5 be prime, N=5q, and zeta any primitive complex Nth root of unity. For an arbitrary binary N-by-N matrix R, set

    D[r,c] = R[r,c] zeta^(rc),    0<=r,c<N.

An R with either D*D=dI or DD*=dI exists exactly when

    d in {0, 1, 5, q, 5q}.

Thus the positive degrees are precisely the divisors of 5q. For the normalized Fourier matrix F_N[r,c]=zeta^(rc)/sqrt(N), the equivalent mask C=F_N entrywise R has scalar Gram (d/N)I.

This theorem has a [separate independent acceptance](review/REVIEW.md), with [exact acceptance bindings](FINAL_ACCEPTANCE.json). The [complete accepted synthesis proof](candidate/REPORT.md) and all seven used component proof/acceptance reports are included. This document consolidates their conclusion; it does not extend it to another order or mask model.

## 1. Model and the scalar endpoints

A Gram diagonal forces d to be an integer between zero and N. When d>0, either square identity makes D invertible and implies the other identity, so every row and column has exactly d supported entries. At d=0, squared norms force D=0 and R=0, without invoking invertibility. At d=N the mask must be all ones.

Every exclusion below applies to arbitrary binary square masks with the original phase zeta^(rc). No support-block premise, adjustable phase, coefficient weight, finite-field replacement, or rectangular one-Gram relaxation is introduced. The source CRT pairing is a literal relabeling of actual cyclic indices.

## 2. Exhaustive proof of necessity

The following disjoint partition exhausts every integer 0<=d<=5q:

| Degree | Conclusion | Accepted dependency |
|---|---|---|
| 0 | Zero mask | Direct |
| 1<=d<q | Exactly 1 and 5 | P, supplementary §7 |
| q | Construction below | Direct / E |
| q<d<2q | Impossible | B at q=7; F at prime q>=11 |
| 2q | Impossible | K |
| 2q<d<3q | Impossible | M |
| 3q | Impossible | K |
| 3q<d<4q | Impossible | U |
| 4q | Impossible | K |
| 4q<d<5q | Impossible | P, supplementary §7b |
| 5q | Full Fourier mask | Direct |

Every prime q>5 is either 7 or at least 11. Thus the separate q=7 theorem fills the only boundary not covered by F. The proper q-multiple endpoints use K, not an illicit extension of an open interval. P explicitly proves its two supplementary results for every distinct prime pair p<q; substituting p=5 is within their hypotheses and is not extrapolation from the principal order-2q result.

For clarity, the two inherited ranges were rederived independently in both the synthesis and its acceptance. In the low range, prime-q cancellation makes the q row supports of a group disjoint and forces d<=5; prime-5/primitive cancellation then rules out 1<d<5. In the high range, prime-q balance forces four-point fiber baselines. Counting extras leaves only d=4q+1; full column degrees force distinct omitted baseline positions across groups, and a primitive cross-group overlap violates binary two-prime cancellation. That argument is strictly for 4q<d<5q; K supplies 4q separately.

The partition and the universal component theorems establish necessity for every permitted q. Finite controls are corroboration, not the proof.

## 3. Explicit positive masks in the original indices

At d=0 use R=0. For any d in {1,5,q,5q}, put m=N/d and define

    I_t = {td+u : 0<=u<d},
    J_t = {t+m ell : 0<=ell<d},    0<=t<m.

Set R=1 precisely on the disjoint rectangles I_t times J_t. Equivalently,

    R[r,c]=1 iff floor(r/d)=c mod m.

Every row and column has d supported entries. A block entry is

    zeta^((td+u)(t+m ell))
       = zeta^((td+u)t) (zeta^m)^(u ell),

because td m ell=tN ell. Since zeta^m is primitive of order d, each block is a diagonal unitary times an unnormalized d-point Fourier matrix, whose two Grams are dI. The blocks have disjoint row and column sets, proving both full Gram identities.

In particular:

- d=1: the diagonal mask, with entries zeta^(r^2).
- d=5: row blocks of five consecutive rows use column residue classes modulo q.
- d=q: row blocks of q consecutive rows use column residue classes modulo five.
- d=5q: the full Fourier mask.

This is one sufficient construction at each allowed degree. It is not a classification of every possible support pattern.

## 4. Original simultaneous inverse-row consequence

For the normalized complex Fourier target F_N, let Delta(N,s) be the infimum of ||M-F_N||_2 over invertible complex M whose every inverse row has at most s nonzeros. Within 1<=s<=5q-1, the inherited floor is sharp exactly at

    s in {5q-1, 5q-5, 4q}.

The corresponding exact errors are

    1/sqrt(5q), 1/sqrt(q), 1/sqrt(5),

respectively. At every other budget in that domain, the infimum is strictly larger than sqrt(1-s/(5q)). This does not determine the larger values.

The equivalence and strict-infimum argument are the accepted result E. For a proper positive mask degree d=N-s, put C=D/sqrt(N), A=F_N-C and t=s/N. An attained witness is

    M=t(A*)^(-1),     M^(-1)=t^(-1)A*.

Because ||C||_2=sqrt(d/N)<1, A is invertible. The inverse has exactly s nonzeros in each row and column, and the accepted identity gives (M-F_N)(M-F_N)*=(d/N)I. The witness is not simply the retained mask A.

The mask endpoints are separate: d=0 corresponds to the vacuous budget s=N, directly attained by M=F_N; d=N corresponds to s=0, whose invertible admissible class is empty. The full mask is not an s=0 inverse witness.

## 5. Exact dependencies and provenance

The complete [dependency ledger](DEPENDENCIES.json) records local proof/acceptance reports, original report and manifest hashes, and verified immutable existing report links. The [immutable-link receipt](IMMUTABLE_DEPENDENCY_LINKS.json) records the earlier actual-body verification supporting those links; packaging does not claim a fresh network fetch.

- E: [equality criterion and attained divisor masks](candidate/sources/E_candidate_REPORT.md), [acceptance](candidate/sources/E_REVIEW.md), §§2–4.
- P: [general-pq low and strict-high exclusions](candidate/sources/P_candidate_REPORT.md), [acceptance](candidate/sources/P_REVIEW.md), supplementary §§7 and 7b.
- F: [q<d<2q for prime q>=11](candidate/sources/F_candidate_REPORT.md), [acceptance](candidate/sources/F_REVIEW.md).
- B: [q=7 first-interior boundary](candidate/sources/B_candidate_REPORT.md), [acceptance](candidate/sources/B_REVIEW.md).
- M: [2q<d<3q](candidate/sources/M_candidate_REPORT.md), [acceptance](candidate/sources/M_REVIEW.md).
- U: [3q<d<4q](candidate/sources/U_candidate_REPORT.md), [acceptance](candidate/sources/U_REVIEW.md).
- K: [d=2q,3q,4q](candidate/sources/K_candidate_REPORT.md), [acceptance](candidate/sources/K_REVIEW.md).

The complete component proof/acceptance reports and original candidate manifests are retained. Their full historical checker/control archives are not bundled or rerun. Original nested manifests inventory their historical packets; only the top-level publication manifest describes this export. The independent synthesis checker is included unchanged and supplies standalone reproducible scientific controls for the combined statement. Administrative projections and omissions are explicit in [OMISSIONS.json](OMISSIONS.json); no scientific equation, scope, construction, arithmetic function, or control case is changed.

## 6. Scope and completion

The N=5q degree-classification subgate is complete for prime q>5. The broader M-SPARSE-DEFECT owner stays TO RESEARCH at priority 42. All support-pattern classifications, arbitrary odd-semiprime/general-order degree classification outside accepted families, general divisibility necessity, exact nonsharp optima, sharper/optimal gaps, and other owner obligations retain their respective open scopes. No historical novelty, full-owner closure, or Fourier/FFT improvement is asserted. Classical two-prime cancellation retains the source attribution to de Bruijn and Lam–Leung.
