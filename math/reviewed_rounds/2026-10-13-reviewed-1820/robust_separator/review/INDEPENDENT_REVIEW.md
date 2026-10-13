# Independent review: robust routed-separator duplicate and correction corollary

13 October 2026 UTC. Local proof review and exact controls. No external writes.

## Decision

**ACCEPT at the stated mathematical and source-comparison scope. No mathematical repair is required.**

The bare Frobenius and sharper operator obstruction are exact accepted duplicates. The full row-sparse/low-rank/diagonal correction statement, exact recurrence guard, normalized and unnormalized norm formulas, finite-tolerance cutoffs, and fixed-branch limiting floors in the supplied candidate are valid. This review closes the candidate's pending independent mathematical-review gate for those statements only.

The proper classification is **an immediate classical low-rank-approximation corollary of the already accepted F018 corrected common-rectangle argument**. This is useful consolidation, not a new general approximation principle or a supported independent discovery. No new discovery ID is assigned, and no parent score, stage score, ranking, or historical acceptance record is edited or recalculated. The immutable candidate's recommendation of a completed-stage cap is not an authorization for unrelated reranking.

This does not establish a general FFT lower bound, an obstruction for arbitrary products, a new Fourier algorithm, a sharpness theorem, or logarithmic branch growth at fixed positive error. Historical priority and a stronger uniform robustness frontier remain outside this review.

## 1. Input identity and source-bound duplicate determination

The exact reviewed archive is `Robust_Separator_Duplicate_and_Correction_Candidate_20261013.zip`, 82,053 bytes, SHA-256:

`5aeca15f59661efe037593a4b39646c11127209320c9d23abf5862e7d75d9401`.

Its candidate `REPORT.md` has SHA-256:

`e41777412af7297e9b45836ba71285f1055a327810ac1bce8d21522c344d8b7e`.

All 14 manifest payloads match the ZIP, byte counts and hashes. The unpacked candidate copies match the archive. All seven original historical sources named in `SOURCE_BINDINGS.json` exist locally and match their copied bytes and hashes. The review bundle includes the unchanged candidate ZIP, so each quoted location remains source-bound. Fresh verification details are in `CONTROL_RESULTS.json`.

Positive duplicate evidence is conclusive:

- `sources/FINAL_MATRIX_THEOREMS.md`, Theorem 2B, lines 175–189, explicitly gives squared Frobenius error at least `max(0,m^2/N-qr)` and squared operator error at least `max(0,(m^2/N-qr)/(m-qr))` for `m>qr`; it includes the diagonal version and the fixed-tolerance warning. SHA-256 `6a2a6424d82e313438058a2458cdbc8f555df0fcee6c534cfd7481633d527c6b`.
- `sources/CORE_MATRIX_SECOND_AUDIT.md`, section 2, especially line 58, explicitly verifies both formulas and their limiting interpretation. SHA-256 `21468cedbe52121e3234573375f0ae0f657af34d4863a474730e8d04ee03c3a1`.
- `sources/F018_ORIGINAL_REVIEW.md`, section 8, lines 228–251, already supplies the Frobenius formula and the weaker squared operator formula `max(0,m/N-qr/m)`. Its section 9 also attributes the inherited independent-order accuracy mechanism. SHA-256 `1a4f7ef0ab59e61250d63999e11822539049ec0c6b2f62d29564b44c959bd856`.
- `sources/INDEPENDENT_REVIEW.md`, “Independent selection and correction proof,” provides the accepted common rectangle with `d=s+1+delta`, initial side `floor(N/d)`, per-stage recurrence `ceil((m-q)/3)`, and rank budget `qr+t`. SHA-256 `1796132039a42ad0fa9cf68fba4ebb4c49554f5cbcf7f94d716b9439fb779971`.
- `sources/PREVIOUS_SEPARATOR_COMPARISON.md`, lines 50–52, describes Theorem 2B and explicitly says that comparison adds no correction-compatible approximation theorem. SHA-256 `39fe305a55a95a4b344612fd163cedab4f9d79ed819b0db87561557fa717459a`.

I independently verify these positive matches and the source identities. I do not turn the candidate's bounded text search into an exhaustive absence claim over all archives or literature. The corrected corollary's validity and classification do not depend on such an absence claim.

## 2. Independent structural proof check

All matrices in the displayed additive representation are understood to have compatible `N x N` dimensions. The assumptions are integers `N>=1`, `r,q>=1`, `s,t>=0`, `delta in {0,1}`; a complex flat normalized unitary `U`; a correction `S` with at most `s` nonzeros in each row; `rank(K)<=t`; diagonal `D`; invertible denominators; branch-specific weighted half-component separators of size at most `q` for the invoked markings; and independently routed permutation-contained endpoints, including zero coefficients.

Choose `m0=floor(N/d)` rows, with `d=s+1+delta`. The union of columns touched by `S+delta D` in these rows has size at most `(d-1)m0`. Since `N>=d m0`, a matching number of untouched columns remains. This deletes the sparse and diagonal corrections on one actual rectangle. It does not delete `K`, which must contribute its separate rank budget `t`.

At side `m_j>=4q`, the branch's inverse rows and columns are marked in different halves of its symmetric bipartite lift. Independent routing creates no color collisions, and completing a zero endpoint support to a permutation is legitimate. After removing at most `q` vertices, both colors retain at least `u=m_j-q` marks; trim to exactly that many. Components have at most `m_j<=4u/3` retained marks. A component in `[2u/3,4u/3]`, or greedy accumulation of smaller components, partitions the components into two unions in that same interval. If one union contains `a` red and `b` blue marks, at least one of `(a,u-b)` and `(u-a,b)` has both coordinates at least `u/3`. Hence a square of side `ceil(u/3)` survives.

The cross block of the lift between one component union and its complement is supported on separator columns. Its rank is at most `q`. Complementary inverse cut ranks agree by the nullity identity, and restriction to the opposite component union cannot increase rank. The inverse lift's lower-left block is `Q_i^-1`, even over complex entries: the lift is symmetric with transpose, and is not being assumed Hermitian. Endpoint zero masks/scales cannot increase rank. Earlier branch bounds persist under restriction.

Therefore the entire selection is independent of the assertion `U=M`. For every legal approximant it constructs a single actual `m x m` rectangle satisfying

`(S+delta D)[I,J]=0` and `rank(M[I,J])<=qr+t=k`.

This checks the only nontrivial transport point from exact equality to approximation. No shared branch order or shared separator graph was silently introduced.

## 3. Exact recurrence and guards

Write `a=3^r`, `c=q(a-1)/2`. Repeated integer ceilings give exactly

`m_r=ceil((floor(N/d)-c)/a)`.

The identity used is `ceil((ceil(x)-q)/3)=ceil((x-q)/3)` for integer `q`. Applying it at `r-1` and using `ceil(y/b)>=4q` exactly when `y>(4q-1)b` yields

`H(q,r)=(4q-1)3^(r-1)+q(3^(r-1)-1)/2+1`.

All calls are valid exactly when `floor(N/d)>=H(q,r)`, equivalently `N>=d H(q,r)`. To check that the last input suffices without circular reasoning, `m_(j+1)>=4q` forces `m_j>=13q-2>=4q`; work backward. At the integer boundary, starting side `H-1` gives last required input `4q-1`, while `H` gives `4q`. The guard does not depend on `t`.

This is the exact validity threshold for the specified conservative recurrence. It is not a necessary condition for a particular matrix to admit some other selection, or for the representation family to exist.

## 4. Independent norm proof and normalization

Let `V=U[I,J]`, `B0=M[I,J]`. Coordinate restriction is contractive in both relevant norms. Flatness gives `||V||_F^2=m^2/N`; unitarity gives `||V||_2<=1`. These are distinct hypotheses and both matter.

A direct kernel proof also verifies the formulas without relying on an implementation of singular-value decomposition. When `k<m`, choose a subspace `W` of `ker(B0)` of dimension exactly `m-k`, and let `P` project onto it. Then

`||(V-B0)P||_F^2=||VP||_F^2=||V||_F^2-||V(I-P)||_F^2>=m^2/N-k`.

The last subtraction is at most `k`, because `I-P` has dimension `k` and `||V||_2<=1`. Consequently

`||U-M||_F^2>=max(0,m^2/N-k)`

and, since `||(V-B0)P||_F^2<=(m-k)||V-B0||_2^2`,

`||U-M||_2^2>=max(0,(m^2/N-k)/(m-k))`.

This uses a chosen kernel subspace of dimension `m-k`; it does not claim that the full error matrix has rank `m-k`. For `k>=m`, the Frobenius floor is zero because `m<=N`, and the operator expression must not be evaluated. The candidate's singular-value-tail argument is equivalently correct.

Dividing the Frobenius norm by `sqrt(N)` gives its stated relative formula. For an unnormalized target `F=sqrt(N)U`, the entire approximation class is closed under common scalar scaling, and each squared absolute error bound acquires a factor `N`. Thus the floors become `max(0,m^2-Nk)` and, when `m>k`, `max(0,(m^2-Nk)/(m-k))`. Relative versions are unchanged.

These are exact stated lower bounds, not claims that every bound is attained by a legal routed family.

## 5. Finite-error cutoff derivations

Set `z=d 3^r`, `C=dq(3^r-1)/2+d-1`, `B=z^2 k`. Then `m>=(N-C)/z` whenever selection is valid. A strict violation of either displayed tolerance cutoff implies `N>B+2C`. This validates every selection call and makes `m>k` in the spectral case. For example, `H(q,r)<=3q3^r/2` while `B>=3dq3^r`, so even `N>B` already lies beyond `dH`; and `(N-C)/z>(B+C)/z>k`.

For relative Frobenius error at most `eta`, with `0<=eta<1/z`, the exact norm inequality forces

`(1-z^2 eta^2)N^2-(B+2C)N+C^2<=0`.

If `N>(B+2C)/(1-z^2 eta^2)`, the first two terms already have positive sum and `C^2>=0`, a contradiction. Therefore candidate (CF) is valid.

For operator error at most `epsilon`, with `0<=epsilon<1/sqrt(z)`, its proposed cutoff exceeds or equals the zero-error cutoff by exactly

`epsilon^2[B(z-1)+Cz]/(1-z epsilon^2)`.

Define `f(y)=y^2-N epsilon^2 y-Nk(1-epsilon^2)`. The norm bound requires `f(m)<=0`. Since `epsilon<1`, the constant term is negative and the quadratic has exactly one positive root. At `x=(N-C)/z>0`,

`z^2 f(x)=(1-z epsilon^2)N^2-[C(2-z epsilon^2)+B(1-epsilon^2)]N+C^2`.

A strict violation of (CO) makes this positive. Thus `x` is above the positive root; `m>=x` then contradicts `f(m)<=0`. This checks the potentially delicate monotonicity issue: it is not necessary to assert that `f` is increasing everywhere on the positive axis.

Both conservative cutoffs reduce to `B+2C` at zero error. The strict denominator restrictions are necessary for these rearrangements. The displayed weak upper bounds do not claim sharp boundary feasibility.

For fixed `r,q,s,t,delta`, `m/N` tends to `1/z`, so the relative Frobenius liminf is at least `1/z` and the operator liminf is at least `1/sqrt(z)`. Increasing `r` to a sufficiently large fixed constant makes these one-rectangle floors smaller than any fixed positive tolerance. Hence this argument cannot imply `r=Omega(log N)` at fixed positive tolerance. This limitation does not construct matching approximants.

## 6. Fresh independent exact controls

`independent_controls.py` was written for this review using only Python standard-library integer/fraction arithmetic, graph traversal, and independent rational Gaussian elimination. The candidate and historical programs were read as static text only; none was executed, imported, compiled, or replayed. No numerical tolerance supports acceptance.

Successful controls recorded in `CONTROL_RESULTS.json`:

- 58,971 exact recurrence/guard cases, plus 768 pairs at the exact `N=dH-1,dH` guard boundary
- 192,524 admissible packed red/blue count pairs
- 21,600 exact finite-tolerance violation tests at the first forbidden integer and additional non-neighbor points, including exact polynomial identities and inherited guards
- 112,968 exact squared-singular-value/rank-budget cases, including zero, full, and oversized rank budgets
- One actual rational `3 x 3` block of normalized Hadamard order four with squared singular values `(1,1,1/4)`. The exact rank-two truncated approximation attains the `1/4` squared Frobenius and operator floors. Its projector, rank, residual, and minimal-polynomial identities are checked rationally.
- Six actual independently routed families: `(N,r,q,s,t,delta)` equal to `(64,1,1,0,0,0)`, `(512,1,1,1,1,1)`, `(256,2,1,0,1,0)`, `(64,1,2,0,0,0)`, `(512,1,2,1,1,1)`, and `(1024,2,2,0,1,0)`.

The `q=1` denominators use weighted rooted-tree support, whose bipartite lifts are trees. The `q=2` denominators are weighted cyclic shifts subtracted from identity, with cycle product two; their lifts are actual cycles, and the checked construction removes two separator vertices. Their inverse entries are exact integers, and invertibility follows from the cycle product being unequal to one. Each family uses independent endpoint permutations and zero masks. Actual sparse/diagonal support deletion, branch ranks, low-rank correction rank, total rank, side recurrence, and target-block error are checked. All six certified Frobenius floors are positive. The randomly selected rooted-tree branch blocks happen to have rank zero; the cycle controls have nonzero rank-one branch blocks and nonzero corrected sum ranks. This is a control limitation, not a maximal-rank claim.

The target for these controls is a normalized Sylvester-Hadamard matrix; multiplying all matrices by `sqrt(N)` permits exact rational squared-error calculations even when `sqrt(N)` is irrational. The actual spectral controls are certified via exact trace/dimension lower bounds on their error blocks, alongside the abstract sharp-tail example. They do not require floating-point eigenvalues.

Negative controls expose the invalid substitutions: flatness without unitarity (`J4/2`), rank of the error mistaken for `m-k` (`I3-diag(2,0,0)`), using a zero or negative spectral denominator, averaged sparsity replacing per-row sparsity, and a missing unitary/unnormalized factor. These finite checks complement the uniform proofs; they do not replace them.

## 7. Primary comparison and final disposition

I freshly reopened Chi-Kwong Li and Gilbert Strang's author manuscript, *An elementary proof of Mirsky's low rank approximation theorem*. Theorem 1 applies over real or complex matrices and states truncated-SVD optimality for every unitarily invariant norm; pages 2–3 prove singular-value tail domination, with the operator and Frobenius norms explicitly covered. [Primary author PDF](https://cklixx.people.wm.edu/uinorm-note.pdf).

The candidate uses precisely that classical analytic principle plus contraction and flat block energy. Its full correction transport uses already accepted support deletion and rank subadditivity. This review does not claim to have inspected the bodies of the 1907, 1936 or 1960 originals, or to have broadened the completed GIRS/TQS structural comparison.

**Final disposition: ACCEPT the source-bound duplicate verdict and corrected robust corollary, including its guards, scaling and conservative tolerance cutoffs. Retain it as an F018 consolidation. No independently counted novelty, no new discovery ID, no reranking, and no external writes.**
