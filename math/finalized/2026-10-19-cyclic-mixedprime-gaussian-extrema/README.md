# Cyclic minimax, mixed-prime masks, and Gaussian extrema

19 October 2026. Three independently accepted scoped results within existing research owners. Complete proofs, independent reviews, source citations, original programs and retained check outputs are preserved byte for byte.

## 1. An attaining infinite cyclic minimax family

For every integer m>=1, the normalized negative-sign Fourier matrix of order N=4m satisfies

    delta_(4m,m-1) = sin(pi/(8m)).

The least complex correction rank allowing zero external operator-norm error is exactly m. The model allows an unrestricted real scalar core, arbitrary invertible complex monomial outer gauges, and a complex correction of rank at most r; no conditioning restriction is introduced. This includes every dyadic N>=4 and recovers the accepted C8 rank-one value sin(pi/16).

For even N>=4 and integers r>=0 with 4r<N-2, the proof also gives

    delta_(N,r) >= sin(pi(N-4r-2)/(4N)).

For N=4m, every open arc of width 2pi/N contains at most N/2+1 eigenvalues, with multiplicity, of F_N A F_N B for arbitrary diagonal unitary A,B. A closed arc of that width can contain N/2+2 eigenvalues. The width is sharp; attainment of the open-arc count is not asserted.

Read the [proof](cyclic/candidate/PROOF.md), [author summary](cyclic/candidate/REPORT.md), [independent review](cyclic/review/REVIEW.md), and [final verdict](cyclic/review/REVIEW_VERDICT.json). The all-m result follows from the proof, not the finite exact controls. The accepted optional odd-order companion is delta_(N,r)>=sin(pi(N-4r-1)/(4N)) for odd N and N-4r-1>0, with integer r>=0; it supplies no odd-order attainment. Smaller-rank matching attainment, the full rank/error tradeoff, general finite-group optima, jointly real Green constructions, runtime and historical priority remain outside this completion.

## 2. Complete order-2q equality-mask weights and partial semiprime exclusion

For every odd prime q, a binary mask R of order N=2q with D[r,c]=R[r,c] zeta^(rc), zeta primitive of order N, and D*D=dI, with positive degree 1<=d<=N, exists exactly for

    d in {1,2,q,2q}.

Because D is square and d>0, the other Gram DD*=dI follows. The theorem classifies possible degrees, not all support patterns at those degrees. The proof stays in the original Fourier phases and uses both row and column constraints, without assuming a full-square-block decomposition.

For primes p<q and N=pq, the accepted supplementary statements are: possible degrees d<q are exactly 1 and p; and no degree lies in the strict interval (p-1)q<d<pq. For odd p, the lower endpoint of that upper interval and the interior q<d<=(p-1)q are not classified here; for p=2, that endpoint is d=q and is already allowed.

In the original invertible simultaneous inverse-row sparsity problem, the accepted criterion gives

    Delta_(2q,2q-d) = sqrt(d/(2q)) iff d in {1,2,q}, 1<=d<2q.

The d=2q full mask is not an s=0 inverse-row attainment. Substitution into the inherited quantitative no-mask estimate gives Delta^2 >= d/(2q)+1/[20q d^(q-2)] at the newly excluded weights; this is a composition with an earlier bound, not a new optimal gap rate.

Read the [proof](mixedprime/candidate/REPORT.md), [independent review](mixedprime/review/REVIEW.md), and [verdict](mixedprime/review/VERDICT.json). Complete original-model witnesses and both-Gram controls are retained. The independent labeled order-six mask census corroborates the proof; no finite census establishes the universal theorem. The connected (8,4) mask and odd CRT family remain valid. General mixed-prime necessity, remaining exact nonsharp optima and sharper or optimal gap rates remain open.

## 3. Gaussian equality classification and a strict nondivisible gap

Let 1<=d<=N, let P be a complex rank-d orthogonal projector, let Z~CN(0,P) in the convention E|g_j|^2=1, and fix a finite radius r>0. With p_j=P_jj, the inherited bound is

    Pr(max_j |Z_j-b_j|<=r)
      <= product_(p_j>0) (1-exp(-r^2/p_j))^p_j
      <= (1-exp(-Nr^2/d))^d.

Equality in the first bound occurs exactly for phase-block projectors with constant magnitudes inside each of d orthogonal blocks; b_j=0 at positive-leverage coordinates and |b_j|<=r at zero-leverage coordinates. Block sizes need not agree. Equality in the ambient bound occurs exactly when d divides N, b=0, and all d phase blocks have size N/d.

Centering maximizes the probability, and the maximum over projectors is attained. For d not dividing N, it is strictly below the ambient envelope. The positive gap is nonquantitative and is uniform only with fixed N,d,r, or fixed N,d on a compact positive radius interval. No computable gap or changing-dimension uniformity is supplied.

Rounded blocks are not generally optimal. In every nondivisible pair N,d, a constant-diagonal projector beats every orthogonal-line block projector once r^2>log(N)/(N/d-floor(N/d)). For N=3,d=2 at r^2=log(16), rounded blocks give 3825/4096, the equal-diagonal construction gives at least 3904/4096, and the true maximum is below 3969/4096. At r^2=1/100, rounded blocks beat that particular equal-diagonal construction. Neither comparison determines the global maximizer. An exact compact-simplex integral reduction is retained for N=3,d=2.

Read the [proof](gaussian/candidate/REPORT.md), [independent review](gaussian/review/REVIEW.md), and [verdict](gaussian/review/VERDICT.json). The geometric Brascamp–Lieb equality classification is explicitly attributed to Valdimarsson; the bound and its normalization are inherited. The exact nondivisible optimum, general critical-window law, sphere-prior adaptive theorem, every-input achievability, arithmetic complexity and historical priority remain open at their previous scopes.

## Inherited results and owner scope

PHASE-DEFECT-RANK-20261011 remains TO RESEARCH, priority 37; M-SPARSE-DEFECT remains TO RESEARCH, priority 42; ALG-036 remains TO RESEARCH, priority 34. No owner closes, no priority or census changes, and no novelty claim is made. [OWNER_DISPOSITIONS.json](OWNER_DISPOSITIONS.json) gives the exact retained and remaining scope. [ACCEPTED_RESULT_PRESERVATION.json](ACCEPTED_RESULT_PRESERVATION.json) identifies preserved foundations and scope qualifications.

Historical author pending-review labels remain unchanged as source history. Scientific acceptance comes from the separately preserved final independent reviews. Historical broader open-gate sentences are read with the later accepted scope dispositions; already completed subcases are not reopened. Prior attribution, models, normalizations, endpoint exclusions and independent broader obligations remain in force.

## Integrity and publication boundary

All author proofs, final reviews, scientific checkers and saved outputs in the six frozen source packets are retained exactly, including their original manifests and seals. There is one privacy omission: the inherited mixed-prime supporting owner-gate review contains private native workbook mappings and an old update proposal. Its original manifest entry and hash remain intact, but that file is absent from the public candidate copy. Its sparse scientific scope, attribution and immutable proof links are preserved verbatim in a separately labeled [privacy-safe excerpt](mixedprime/privacy_projection/PRESERVED_SPARSE_SCOPE_EXCERPT.md). See [OMISSIONS.json](OMISSIONS.json) and [PROJECTION_DISCLOSURE.json](PROJECTION_DISCLOSURE.json). Selected foundational reports and reviews and prior public scope records are also exact copies. [COPY_BINDINGS.json](COPY_BINDINGS.json) records these correspondences; older dependency collections are not recursively included. The 63 retained source-packet files and 10 selected supporting files are exact copies; the single excerpt is explicitly a projection, not the complete original. No theorem, proof, verdict, checker or saved result is rewritten or path-adapted. Original local paths and run commands remain provenance; original source-manifest verification expects the privately omitted file, so use the release verifier for this publication projection. No relocation-tested scientific replay is claimed.

The packaging verifier checks documentary integrity, acceptance bindings, scope and a bounded privacy scan. It does not execute scientific or historical programs. Run:

    python3 -B verify_package.py

Publish only the files listed in [PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json), under math/finalized/2026-10-19-cyclic-mixedprime-gaussian-extrema. Private owner snapshots, semantic recommendations and operational handoff files are outside the public root. Full third-party paper bodies, scans and private workbook data are excluded.

This is a locally sealed packet. It does not claim a GitHub commit, remote-byte verification or a native table update, and it does not alter or supersede the five earlier publication packets or their separately guarded 76-cell synchronization batch.
