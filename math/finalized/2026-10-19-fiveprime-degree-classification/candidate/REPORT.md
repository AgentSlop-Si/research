# Complete degree classification for binary fixed-Fourier equality masks at order 5q

Date: 2026-10-19 UTC. This is a new synthesis of independently accepted component theorems, with an explicit construction and a complete coverage proof. Its component results are accepted; this synthesis is a local candidate for a separate review, not a self-issued acceptance. No external write, owner closure, novelty claim, support classification, arbitrary-semiprime theorem, or Fourier/FFT claim is made.

## 1. Answer and exact theorem

**Yes.** The accepted component results together now determine every degree for this particular family. Let q>5 be prime, N=5q, and zeta any primitive complex Nth root of unity. For an arbitrary binary N-by-N matrix R, let

    D[r,c] = R[r,c] zeta^(rc),    0 <= r,c < N.

For a scalar d, an R satisfying either D*D=d I_N or DD*=d I_N exists if and only if

    d in {0, 1, 5, q, 5q}.

Equivalently, the possible positive degrees are exactly the divisors of 5q. For F_N[r,c]=zeta^(rc)/sqrt(N), the normalized binary mask C=F_N entrywise R has scalar Gram (d/N)I at precisely those degrees. This statement classifies possible degrees, not all masks at a possible degree.

No degree gap remains within prime q>5 and this exact binary fixed-phase model. The broader M-SPARSE-DEFECT owner remains TO RESEARCH, priority 42: this result does not determine the exact nonsharp inverse-sparsity optima, classify arbitrary orders or arbitrary odd semiprimes, or resolve the owner's other inverse-support and commutator questions.

## 2. Original owner, model, and normalization audit

The actual original selected owner record was read, not inferred from an interval packet: `sources/O_selected_record.json` is the frozen M-SPARSE-DEFECT record originally bound to repository commit c3a882a7e6e61af05fe1045145bc1a43038d77c6. It identifies “Sparse inverse and commutator approximation floors,” TO RESEARCH, priority 42, and leaves global uniform-row-sparsity sharpness open beyond its prior one-neighborhood result. The historical Phase20 audit was also read; its Section 5 proves the one-inverse-row bound for the normalized complex Fourier target and expressly does not claim simultaneous-row sharpness. Its complete original bytes are retained as `sources/O_phase20_audit.md`.

The later accepted equality criterion [E] defines

    Delta(N,s) = inf ||M-F_N||_2,

where M is invertible over C and every row of M^(-1) has at most s nonzeros; 1<=s<=N-1. Support patterns, complex coefficients, and condition numbers are unrestricted. With d=N-s, its exact statement is

    Delta(N,N-d)=sqrt(d/N)
    iff a binary C=F_N entrywise R obeys C*C=(d/N)I.

Absence of such a mask gives strict separation of the infimum, not merely nonattainment. This uses an attained-limit argument strictly inside error one. The model is not a single-row or rectangular relaxation.

All seven mathematical sources below use precisely this same square binary mask model, or its unnormalized version D=sqrt(N)C. Each interval and endpoint statement allows every primitive complex zeta. The equality source fixes exp(-2 pi i/N), which is one such primitive root, so its original-target consequence follows directly. No change of field, variable entry phases, amplitudes, weighted coefficients, nonbinary masks, or arbitrary row/column rescaling is introduced. CRT formulas in the sources are literal relabelings of original cyclic indices, with unchanged phase zeta^(rc).

For d>0, a square identity D*D=dI gives invertibility and D*=dD^(-1), hence DD*=dI. The converse is identical. The two diagonals give both row and column degrees d. For d=0, the norm diagonal alone implies D=0 and R=0. Thus no invertibility inference is made at zero. For an arbitrary scalar d in the theorem, a Gram diagonal first forces d to be a nonnegative integer at most N; there are no other real or complex scalar possibilities.

## 3. Individually pinned accepted dependencies

The local source paths, SHA-256 hashes, exact copied bytes, candidate-manifest checks, and review bindings are in `SOURCE_BINDINGS.json` and `SOURCE_VERIFICATION.json`. The complete source reports and acceptance reviews are frozen under `sources/`. The labels below identify exact theorem sections, rather than treating a packet title as a proof of an unstated range.

- **[E] Equality criterion and construction.** `sparse_defect_budget_20261018_1240/REPORT.md`, Sections 2–4; accepted by `sparse_mask_final_review_20261018_1248/REVIEW.md`, verdict and Sections 1–5. Report SHA-256 1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee. This supplies the original inverse-row equivalence, strict infimum separation, and proper-divisor construction. Its construction is explicitly re-proved below, including the full-mask boundary that is outside the proper inverse-row range.

- **[P] Inherited low and high ranges.** `sparse_mixedprime_2q_classification_20261019_1002/REPORT.md`, supplementary Section 7 and Section 7b, not merely its principal order-2q theorem. The independently accepted review is `review_twoprime_mask_family_20261019_1008/REVIEW.md`, “Supplementary pq results,” with its bound VERDICT.json. Report SHA-256 a54b703ddab52ae93050b1c732c8f288e1b007b7378e4b6e3185ceeeb9e63708. For every distinct prime pair p<q, Section 7 allows positive d<q exactly at 1,p, and Section 7b excludes (p-1)q<d<pq. Substituting p=5 proves the exact needed ranges 1<=d<q and 4q<d<5q. The review explicitly accepts both supplementary theorems; this is not extrapolation from p=2.

- **[F] First interior, q>=11.** `sparse_fiveq_first_interior_20261019_1344/REPORT.md`, Sections 1–8; accepted by `fiveprime_interior_independent_review_20261019_1400/REVIEW.md` and VERDICT.json. Report SHA-256 aa6c4507c215d7374e2e9aee1bb25a95b7275110178be5b549f4bc783c8cd6d6. Excludes every q<d<2q for prime q>=11. Its restriction is retained: it is not applied at q=7.

- **[B] First interior, q=7 boundary.** `fiveprime_q7_boundary_20261019_1430/REPORT.md`, Sections 1–7; accepted by `fiveprime_q7_boundary_independent_review_20261019_1441/REVIEW.md` and VERDICT.json. Report SHA-256 84d43836ff591b5a667213f1c23475bd6b866fd4aa788db5a43bc9ec1a264b6d. Excludes d=8,9,10,11,12,13 at N=35. Its rectangular degree-eleven control is not a square positive construction. Every prime q>5 is either 7 or at least 11, so [F] and [B] together cover the first interior exactly.

- **[M] Middle interior.** `fiveq_middle_interval_20261019_1715/REPORT.md`, Sections 2–6; accepted by `fiveq_middle_review_20261019_1721/REVIEW.md` and VERDICT.json. Report SHA-256 261dc2e392d864222f61a1b99f9e7d3710ccf48d9f28112c8b7b78742d393ed1. Excludes 2q<d<3q for every prime q>5. Neither endpoint is silently included.

- **[U] Upper interior.** `fiveq_upper_interval_20261019_1757/REPORT.md`, Sections 2–6; accepted by `fiveq_upper_review_20261019_1758/REVIEW.md` and VERDICT.json. Report SHA-256 c4bacdf2b20eb12c16602aba08e14b04bdd65e9c0f1cce427c7df2c58aceb664. Excludes 3q<d<4q for every prime q>5. Neither endpoint is silently included.

- **[K] Proper q-multiple endpoints.** `fiveq_endpoints_20261019_1815/REPORT.md`, Sections 2–5; accepted by `fiveq_endpoints_independent_review_20261019_1816/REVIEW.md` and VERDICT.json. Report SHA-256 c14ab1fc4ed3325972cfb7fc8ae1474ed705dae8dde725b397f9323aa6fc94bf. Excludes exactly d=2q,3q,4q for every prime q>5. Its proof retains the f=0 branch and arbitrary row-dependent line sets; no interior-only nonempty-fiber step is imported into an endpoint.

Individual packets deliberately say that other ranges or full classification are outside their scope. Those statements are not assertions that independently proved ranges remain globally undecided. The full conclusion here is a separate logical composition of the displayed accepted results.

## 4. Rechecking the inherited ranges rather than trusting the headline

Here are the actual [P] arguments specialized to p=5. They also verify that the inherited endpoints have not been accidentally included.

Use the literal CRT pairing r=a e_5+b e_q, c=u e_5+v e_q, where e_5=q(q^(-1) mod 5), e_q=5(5^(-1) mod q). Set alpha=zeta^(e_5), beta=zeta^(e_q); then zeta^(rc)=alpha^(au) beta^(bv). Call the q rows with fixed a a group, the five columns with fixed v a fiber, and the q columns with fixed u a line.

Prime-order cancellation says that the overlap counts on all fibers of two distinct rows in the same group are equal. Primitive binary cancellation says that an overlap with both row-coordinate differences nonzero is a union of complete fibers or a union of complete lines. The latter follows by reducing its binary coefficient array epsilon in the rational basis alpha^i beta^j, i<4, j<q-1. Reduction gives epsilon[i,j]-epsilon[i,q-1]-epsilon[4,j]+epsilon[4,q-1]=0, hence epsilon[u,v]=A[u]+B[v] with integer arrays. If both vary, their Cartesian sum has range at least two, impossible for binary values; one is constant. These are classical root-sum facts, not novelty claims.

### Low range: 1<=d<q

Within one group, each overlap has size a multiple of q and is at most d<q, so the q row supports are disjoint. Consequently qd<=5q and d<=5. If 1<d<5, every nonempty orthogonal overlap would have at least five terms: a nonzero row difference has order 5, q, or 5q, and prime balance or primitive binary cancellation gives that lower bound. Since each overlap has at most d<5 terms, all 5q rows would have pairwise disjoint supports. Their total support size 5qd cannot fit in 5q columns. This contradiction leaves only d=1 or d=5. Both are constructed in Section 6. At d=q the initial disjointness step need not hold; it is handled separately by construction.

### High range: 4q<d<5q

For two distinct rows in the same group, their overlap is at least 2d-5q>3q and less than 5q. Prime-q balance therefore makes its size exactly 4q, with four common columns in every fiber. In a fixed group/fiber, the q subsets of five coordinates have pairwise intersection four. Each has weight at least four, at most one has weight five, and all weight-four subsets are identical. Thus all q rows contain the same four-point baseline in that fiber, with at most one extra incidence at the missing point.

Across q fibers, each row has 4q baseline positions and d-4q extras. There are at most q extra incidences for the whole group, so q(d-4q)<=q, forcing d=4q+1. Every row then has one extra, and every fiber has one extra; the row-to-extra-fiber assignment is a bijection for each group.

In a fixed fiber, let m be the number of groups whose baseline omits a given column. Its full degree is (5-m)q+m=5q-m(q-1). Equality to 4q+1 forces m=1. Hence the five groups omit distinct columns in each fiber. Choose rows in different groups with different second coordinates, so their difference is primitive. Their baseline intersection has three points in every fiber; their two extra positions add two distinct points in one or two fibers. At least one fiber is untouched since q>5. The overlap is not a union of full fibers (an untouched fiber has three points), and not a union of full lines (the fiber counts are nonconstant). Primitive binary cancellation is contradicted.

This argument excludes exactly the strict high interval; it does not prove d=4q. That endpoint is supplied by [K]. Nor does it exclude d=5q, where the full mask works.

## 5. Necessity: the complete degree partition

By Section 2 it is enough to classify integers 0<=d<=5q. The following cases are disjoint and exhaustive:

1. d=0: allowed, and only R=0 is possible.
2. 1<=d<q: [P], Section 7, allows exactly d=1,5.
3. d=q: allowed by Section 6.
4. q<d<2q: excluded by [B] when q=7 and [F] when q>=11.
5. d=2q: excluded by [K].
6. 2q<d<3q: excluded by [M].
7. d=3q: excluded by [K].
8. 3q<d<4q: excluded by [U].
9. d=4q: excluded by [K].
10. 4q<d<5q: excluded by [P], Section 7b.
11. d=5q: allowed by Section 6, and row/column degree forces R to be the all-one mask.

This proves that no degree outside {0,1,5,q,5q} can occur. It uses symbolic universal theorems at their stated domains, not a finite-prime extrapolation, mask census, or failed numerical search.

## 6. Sufficiency: exact constructions for every allowed degree

For d=0 take R=0. For each d in {1,5,q,5q}, let m=5q/d. Partition rows and columns into m sets of size d:

    I_t = {td+u : 0<=u<d},
    J_t = {t+m ell : 0<=ell<d},    0<=t<m.

Put R[r,c]=1 if (r,c) belongs to I_t x J_t for some t, and zero otherwise. Equivalently,

    R[r,c]=1 iff floor(r/d) = c mod m.

This is an explicit mask in the original cyclic indices, with exactly d entries in every row and column. For r=td+u and c=t+m ell, its nonzero entries are exactly

    zeta^((td+u)(t+m ell))
      = zeta^((td+u)t) (zeta^m)^(u ell),

since td*m*ell=t*N*ell. The root zeta^m is primitive of order d. Therefore each d-by-d block is a diagonal unitary times an unnormalized d-point Fourier matrix, whose two Grams equal dI. The distinct blocks have disjoint row and column sets, so the full matrix has D*D=DD*=dI. This holds for every primitive zeta, not only one sign convention.

Written out for the four positive degrees:

- d=1: R[r,c]=1 exactly when r=c. The entries are zeta^(r^2), a diagonal unitary.
- d=5: R[r,c]=1 exactly when floor(r/5)=c mod q. The q row blocks of five consecutive rows use column residue classes modulo q.
- d=q: R[r,c]=1 exactly when floor(r/q)=c mod 5. The five row blocks of q consecutive rows use column residue classes modulo five.
- d=5q: m=1 and R is all ones; D is the full unnormalized Fourier matrix.

The block structure above is one sufficient construction. It is not asserted to be necessary for all masks at an allowed degree.

## 7. Exact original inverse-row consequence and its boundary

Use the original normalized target F_N[r,c]=exp(-2 pi i rc/N)/sqrt(N), N=5q, and the simultaneous-row problem from Section 2. In its accepted domain 1<=s<=N-1, put d=N-s. Then

    Delta(5q,5q-d)=sqrt(d/(5q)) iff d in {1,5,q}.

Equivalently, the inherited floor is sharp exactly at the three inverse-row budgets

    s in {5q-1, 5q-5, 4q}.

Their exact values are respectively 1/sqrt(5q), 1/sqrt(q), and 1/sqrt(5). For every other integer 1<=s<=5q-1 the infimum is strictly above sqrt(1-s/(5q)), by [E]. This classification does not determine those strictly larger values.

For each proper positive divisor construction, set C=D/sqrt(N), A=F_N-C, t=s/N=1-d/N, and

    M=t(A*)^(-1),     M^(-1)=t^(-1)A*.

This is [E]'s actual witness, not an unsupported identification of M with the retained mask A. Since ||C||_2=sqrt(d/N)<1, A=F_N-C is invertible. Its adjoint has exactly s supported positions per row and column, so the displayed inverse has exactly s nonzeros per row and column. The accepted equality calculation gives (M-F_N)(M-F_N)*=(d/N)I and hence the asserted attained error.

The mask endpoints must be kept distinct from this domain. Degree d=0 corresponds to s=N: the constraint is vacuous and M=F_N attains error zero, which can be checked directly without extending the strict-error-below-one argument to a new case. Degree d=N corresponds to s=0: every inverse row would be zero, so there is no invertible admissible M. Thus the full mask is not an s=0 inverse witness. No use of the displayed witness is made at t=0.

## 8. Verification, credit, and what is not concluded

The local synthesis check reads and hashes source bytes, verifies every candidate-manifest member, checks source copies and the acceptance reviews' report/manifest bindings, and records the exact resulting hashes. It never imports or executes a historical mathematical checker. No finite test count is promoted to a proof. The classification proof is the exhaustive symbolic degree partition plus accepted universal exclusions and the symbolic original-phase construction.

Classical two-prime cancellation retains the component papers' attribution to de Bruijn and Lam–Leung. No historical novelty or priority determination is made. No result for arbitrary pq, p^a q, arbitrary N, weighted masks, all support patterns, sharp positive gap rates, preparation costs, application algorithms, or unrestricted Fourier complexity follows merely from this synthesis.

The narrow degree-classification question is answered completely. The synthesis still needs its own independent acceptance before being represented as a reviewed combined artifact. The original owner remains TO RESEARCH at priority 42, and no external record, repository, index, or status was changed.
