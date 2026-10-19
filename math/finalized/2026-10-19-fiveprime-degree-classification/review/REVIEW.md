# Independent acceptance: complete order-5q degree classification

Date: 2026-10-19 UTC. **PASS. No proof repair is required.** This is the separate synthesis acceptance, not a reuse of an endpoint or interval verdict.

For every prime q>5, N=5q, every primitive complex Nth root zeta, and arbitrary binary N-by-N masks R, the fixed-phase matrix D[r,c]=R[r,c] zeta^(rc) can satisfy either scalar Gram identity D*D=dI or DD*=dI exactly at

    d in {0,1,5,q,5q}.

The proper simultaneous inverse-row floor is sharp exactly at s in {5q-1,5q-5,4q}, within 1<=s<=5q-1. Every other budget in that domain has a strict infimum gap above sqrt(1-s/(5q)). No exact value for those larger infima is inferred.

## Frozen candidate and independent evidence

This acceptance binds `fiveq_degree_classification_20261019_1829`:

- REPORT.md SHA-256: ea1eafbcb45284d945feeb6a5b85f4958b4046c6b945526a26dbb483719ef172
- MANIFEST.json SHA-256: 4c8007fa271fdbeecaa8d2f5e2516c003a7b05eefbe864264813b2885a3fa908

The complete packet is retained unchanged in `frozen_candidate/`. All 44 manifest-bound files, the seal, 36 copied source files, the seven underlying candidate manifests containing 129 files, their original source-copy bindings, and the exact acceptance report/manifest hashes were independently checked before and after the fresh controls. The original candidate reports, reviews, and source copies were compared byte for byte with their frozen copies. No candidate or historical checker was imported or executed.

The original selected M-SPARSE-DEFECT record and original Phase20 Section 5 were read. They distinguish the one-sparse-inverse-row lower bound from simultaneous-row sharpness. The record remains TO RESEARCH, priority 42. This acceptance changes no external record, repository, owner status, priority, or score.

## 1. The seven dependencies really accept the required statements

The actual reports and full acceptance reviews were read, rather than inferring their contents from titles, tables, citations, or summaries. The following are the precise accepted inputs. The copied source labels are those in the synthesis packet.

1. **E: equality and attainment.** `E_candidate_REPORT.md`, Sections 2–4, and `E_REVIEW.md`, verdict and Sections 1–5, accept the equivalence between simultaneous inverse-row floor sharpness and a binary complementary fixed-Fourier mask. Their domain is N>=2 and 1<=s<=N-1. The accepted review explicitly establishes strict infimum separation, not merely nonattainment, and the witness M=t(A*)^(-1). Report hash: 1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee. This review has no separate VERDICT.json; its explicit ACCEPT and exact report/manifest binding are present in the review itself.

2. **P: inherited low and high ranges.** `P_candidate_REPORT.md`, supplementary Sections 7 and 7b, and `P_REVIEW.md`, “Supplementary pq results,” explicitly accept both general distinct-prime p<q statements: positive d<q is possible exactly at 1,p; and (p-1)q<d<pq is impossible. P_VERDICT.json also lists both as accepted scopes. Report hash: a54b703ddab52ae93050b1c732c8f288e1b007b7378e4b6e3185ceeeb9e63708. These are not consequences guessed from the report's principal order-2q theorem. Substituting p=5 is directly within their quantified domains.

3. **F: first interior for q>=11.** `F_candidate_REPORT.md`, result and Sections 1–8, and `F_REVIEW.md`, verdict and Sections 1–6, accept every q<d<2q at every prime q>=11. Report hash: aa6c4507c215d7374e2e9aee1bb25a95b7275110178be5b549f4bc783c8cd6d6. The weighted incidence argument handles five-coordinate triangles and four-row near-pencils and preserves empty singleton restrictions. Its q>=11 restriction is substantive and is not weakened here.

4. **B: the missing q=7 first interior.** `B_candidate_REPORT.md`, theorem and Sections 1–7, and `B_REVIEW.md`, verdict and symbolic proof audit, accept all d=8,9,10,11,12,13 at N=35. Report hash: 84d43836ff591b5a667213f1c23475bd6b866fd4aa788db5a43bc9ec1a264b6d. The degree-eleven split and single-clique cases are both excluded. The retained seven-row degree-eleven Gram is expressly rectangular and not a square positive construction. Thus F and B together cover every prime q>5: such a prime is either 7 or at least 11.

5. **M: middle open interval.** `M_candidate_REPORT.md`, Sections 1–6, and `M_REVIEW.md`, accepted statement and dependency audit, accept 2q<d<3q for every prime q>5. Report hash: 261dc2e392d864222f61a1b99f9e7d3710ccf48d9f28112c8b7b78742d393ed1. Coverage derives full-cycle row geometry from arbitrary masks, disjoint fiber packing forces singleton fibers, and unrelated group permutations remain allowed. Neither endpoint is included.

6. **U: upper open interval.** `U_candidate_REPORT.md`, Sections 1–6, and `U_REVIEW.md`, accepted narrow statement and symbolic dependency audit, accept 3q<d<4q for every prime q>5. Report hash: c4bacdf2b20eb12c16602aba08e14b04bdd65e9c0f1cce427c7df2c58aceb664. The mixed line/fiber alternatives are retained before packing, and the q=7 inequalities hold directly. Neither endpoint is included.

7. **K: proper q-multiple endpoints.** `K_candidate_REPORT.md`, Sections 1–5, and `K_REVIEW.md`, accepted scope and symbolic proof audit, accept exactly d=2q,3q,4q for every prime q>5. Report hash: c14ab1fc4ed3325972cfb7fc8ae1474ed705dae8dde725b397f9323aa6fc94bf. The endpoint argument permits f=0 from the start. The equation (k-ell)q=(5-ell)f forces f=0 because q>5 is prime and 0<=f<q. All row-dependent k-line sets remain arbitrary. Fixing the second row coordinate then forces five pairwise-disjoint k-subsets of a five-element set, impossible at k=2,3,4. No interior-only nonempty-fiber argument is imported.

The six available component VERDICT.json files all say PASS and bind their respective report and manifest exactly. Individual reports saying that other ranges or a full classification are outside their own scope do not negate accepted results in other packets. The current conclusion is a new logical composition, now separately reviewed.

## 2. Model compatibility, scalar domain, and CRT phases

Every exclusion quantifies over arbitrary binary square masks in the original D[r,c]=R[r,c] zeta^(rc) model, with zeta primitive. There is no extra support-block assumption, amplitude freedom, adjustable entry phase, weighted mask, rectangular substitution, or change of field.

For an arbitrary scalar d, a diagonal entry of a Gram identity first forces d to be an integer between 0 and N. If d>0, D*D=dI makes D invertible with D*=dD^(-1), so DD*=dI; the reverse is identical. Both diagonals therefore supply both degree counts. If d=0, column or row squared norms force D=0, hence R=0, without an invertibility claim. If d=N, every row or column must be full, hence R is all ones.

The CRT formulas are literal original-index identities. The idempotents e5=q(q^(-1) mod 5), eq=5(5^(-1) mod q) have e5+eq=1, e5 eq=0, e5^2=e5 and eq^2=eq modulo N. Thus r=a e5+b eq and c=u e5+v eq give rc=au e5+bv eq. Consequently zeta^(rc)=alpha^(au) beta^(bv), alpha=zeta^e5 and beta=zeta^eq. Both primitive factor roots and the pairing are fixed by the original zeta. A different primitive choice merely changes the primitive character multipliers. No root-sign convention is essential.

The binary primitive cancellation lemma used in the sources is valid: its rational-basis reduction yields epsilon[u,v]=A[u]+B[v] with integer A,B. If both vary, the Cartesian sum has range at least two, contradicting binary values. Thus the support is a union of complete five-fibers or a union of complete q-lines. Prime-order balance applies to integer coefficient counts, not incorrectly to an assumed binary count vector. The classical attribution to de Bruijn and Lam–Leung is preserved; no priority claim is added.

## 3. Independent rederivation of both inherited ranges

The inherited low/high statements are particularly important to the synthesis and were rechecked directly at p=5.

For 1<=d<q, two distinct rows in one first-coordinate group have overlap equal to q times a nonnegative integer, by prime-q balance, and at most d<q. Their supports are disjoint. There are q such rows in 5q columns, so qd<=5q and d<=5. If 1<d<5, every nonempty orthogonal overlap would have at least five terms: row-difference order is 5, q, or 5q, and prime balance or binary primitive cancellation gives that lower bound. All 5q row supports would then be pairwise disjoint, impossible for d>1. This leaves precisely d=1,5, both constructed below. The argument does not cover or exclude d=q.

For 4q<d<5q, same-group row overlaps are greater than 3q and less than 5q. Balance forces four points in every fiber. In each group/fiber, the q five-coordinate restrictions therefore share a common four-point baseline; at most one is the full five-set. Counting extra incidences across the q rows forces d=4q+1, exactly one extra per row and per fiber, and a bijection assigning rows to extra fibers.

For a fixed column, if m groups omit it from their baselines, its degree is (5-m)q+m. Equality to 4q+1 forces m=1, so the five groups omit distinct columns in every fiber. A primitive pair from different groups has three common baseline points per fiber and two distinct extra common points in one or two fibers. An untouched fiber exists since q>5 and has three points, ruling out full-fiber unions. Touched and untouched counts differ, ruling out full-line unions. This contradicts primitive cancellation. The conclusion is exactly the strict interval; d=4q still needs K, and d=5q remains a valid positive boundary.

## 4. The exhaustive partition closes every degree

After the scalar-domain reduction to integers 0<=d<=5q, there is an exhaustive, disjoint partition:

- d=0: zero mask.
- 1<=d<q: P leaves only 1,5.
- d=q: positive construction.
- q<d<2q: B at q=7; F at every larger permitted prime.
- d=2q: K.
- 2q<d<3q: M.
- d=3q: K.
- 3q<d<4q: U.
- d=4q: K.
- 4q<d<5q: P.
- d=5q: full Fourier mask.

There is no degree gap, endpoint overlap problem, unhandled prime, or scalar possibility outside this list. This proof uses the universally quantified accepted theorems at their precise domains. The finite partition sweep in the checker is only an implementation guard against an omitted interval, not a proof by finite primes.

## 5. Positive masks preserve the original phases and both Grams

For any positive divisor d of N, set m=N/d and take

    I_t={td+u:0<=u<d},  J_t={t+m ell:0<=ell<d},  0<=t<m,
    R[r,c]=1 exactly on the union of I_t times J_t.

These sets partition rows and columns, and each supported block has size d by d. Its actual entries are

    zeta^((td+u)(t+m ell))
      =zeta^((td+u)t) (zeta^m)^(u ell),

because td m ell=tN ell. Since zeta^m is primitive of order d, the block is a diagonal unitary times an unnormalized d-point Fourier matrix. Both block Grams are dI. The disjoint row/column blocks give both full Grams dI. This is a description of one valid construction; no necessity of this block geometry is asserted.

It supplies d=1,5,q,N in the original index order, for every primitive zeta. In particular d=1 is diagonal with entries zeta^(r^2), and d=N is the full Fourier matrix. Together with R=0 this proves sufficiency for all five claimed values.

## 6. Original inverse-row translation and the two outside endpoints

Let F[r,c]=exp(-2 pi i rc/N)/sqrt(N) be the original normalized target. For 1<=s<=N-1, set d=N-s, t=s/N and a=sqrt(d/N). E accepts

    Delta(N,s)=a  iff  C=F entrywise R satisfies C*C=a^2 I.

The mask classification therefore leaves precisely d=1,5,q, equivalently

    s=5q-1, 5q-5, 4q,

with respective values 1/sqrt(5q), 1/sqrt(q), 1/sqrt(5). Each lies strictly inside the accepted inverse-row domain.

For clarity, the witness and error calculation are independently checked algebraically. Put A=F-C. Since ||C||=a<1 and F is unitary, ||Ax||>=(1-a)||x||; thus A is invertible. Set B=t^(-1)A* and M=B^(-1)=t(A*)^(-1). The complementary binary mask gives exactly s nonzeros per row and column of B. Expanding C*C=(1-t)I yields

    tI-A*F-F*A+A*A=0,
    I-BF-F*B*+tBB*=0.

For E0=M-F, BE0=I-BF, so

    BE0 E0* B*=(I-BF)(I-BF)*=(1-t)BB*.

Invertibility of B gives E0 E0*=(1-t)I. Thus the claimed error is attained. M is not confused with the retained mask A, and t is never set to zero.

The strict infimum conclusion in E is also valid. If admissible matrices approached an error a<1, their norms would be bounded and their least singular values uniformly positive. A convergent subsequence has invertible limit; inverse matrices converge, and the at-most-s-nonzeros-per-row set is closed. The limit would attain the floor and produce a mask. Absence of a mask therefore forces a strict gap, not just nonattainment. The admissible class is nonempty for s>=1, for example it contains scalar identity matrices.

The two mask boundaries are correctly separated. At d=0, s=N is outside E's stated domain but directly has M=F and error zero. At d=N, s=0 would force every inverse row to vanish, so no invertible admissible M exists. The full mask is a mask witness only; it is never an inverse-row witness.

## 7. Fresh self-authored exact controls

`independent_check.py` was authored for this review. It uses only the Python standard library, integer root-sum arithmetic, and rational cyclotomic-field arithmetic. It executes no candidate or historical code and uses no floating tolerance. Mathematical controls are reproducible from the retained frozen packet alone; `--originals` additionally compares the original local source files.

The final successful run records:

- 60 positive mask/root-choice cases at q=7,11,13,17, using d=0,1,5,q,5q and primitive multipliers 1,2,-1. Both complete original-index Grams and both degree counts pass.
- 24 fresh regular negative masks at q=7,11,13: a cyclic degree-two mask; four cycle-union families with degrees q+4,2q+3,3q+2,4q+1 and group-dependent affine special-fiber permutations; and all three endpoint families with line sets varying with the second row coordinate. Every case passes regular degree counts but fails both full Grams. Nonzero exact witnesses are retained.
- 606,600 complete original-index Gram entries across the positive and negative controls.
- 15,700 actual CRT pairing congruences and 240 monomial comparisons between tensor-basis reduction and independently constructed univariate Phi_(5q) remainders. The latter polynomial is produced by exact monic division Phi_5(X^q)/Phi_5(X).
- 380,750 integer degree-partition cases across all 165 primes 7<=q<=997, including every endpoint, plus the proper inverse-budget and squared-value substitutions. These are finite partition guards only.
- Two fresh exact original inverse witnesses at N=35, d=5 and d=7. Gaussian elimination over Q(zeta_7) and Q(zeta_5) computes the small diagonal-omission factors; both small inverse products and both small error Grams are checked exactly. Tensoring with the other full prime Fourier factor gives actual fixed-phase order-35 witnesses. Exact factor-product separation certifies all 4,900 original-index inverse-product entries and all 4,900 original-index error-Gram entries across both witnesses. This is an explicit factorized product certificate, not a claim of unrelated dense 35-by-35 multiplication. Both inverse row and column budgets are 30 and 28 respectively.

These finite tests supplement the symbolic proofs and accepted universal component theorems. No test count, numerical search failure, optimizer result, or finite-prime extrapolation is used as the proof of the classification.

## 8. Final limits

PASS is for the full degree classification at N=5q with prime q>5 and the stated sharp-floor translation only. It is not a classification of all masks at allowed degrees, arbitrary pq or arbitrary N, sharp nonzero gap rates, exact nonsharp optima, implementation costs, or Fourier/FFT complexity. Historical novelty and priority were not investigated. Classical attribution and all broader owner limitations remain intact. No external write or owner closure occurred.
