# F021 chirp-specific source-gate audit

Date: 2026-10-15 UTC. Reviewer task: audit_f021_chirp_gate.

## Decision

The inspected Spiridonov–Zhedanov source supports a precise **nontransfer result**, not a new legal-bank classification or a closure of F021. Its terminal-degree q-Hermite polynomial maps to a polynomial whose roots are all cycle-resonant. Simple terminal quadrature does not establish simplicity at the target half-order degree. The positive-weight specializations do not repair this mismatch.

Keep F021 OPEN and parent priority 53 unchanged. No accepted-theorem, status, stopping-boundary, or priority-cell update is justified by this source. A bounded attribution/source-exclusion note may be retained as research evidence, explicitly without treating it as a new canonical theorem or a completed priority search.

This is an independent analytical and bounded exact-computation review, not Lean verification or a kernel proof. No external writes were made. No supplied archive program was executed or imported.

## 1. Fixed source boundary

The repository baseline was read using the GitHub connector at commit `e5c9c53f7d34e8d858e781d2d5321393aec7e85c`:

- [Open-Waring comparison](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/finalized/2026-10-15-f021-open-waring-comparison/REPORT.md), Git blob `943799a3c6db3ba4697d073bdcf0f5864b14f6c6`.
- [Existing chirp classification](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md), Git blob `bcabf46f7517f9ff367c714425a188a4706737b6`. The independently available local source bytes have the expected SHA-256 `c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1`.

The new external source is V. Spiridonov and A. Zhedanov, *Zeros and orthogonality of the Askey-Wilson polynomials for q a root of unity*, Duke Mathematical Journal 89 (1997), 283–305; [arXiv:q-alg/9605034v2](https://arxiv.org/html/q-alg/9605034v2), [PDF](https://arxiv.org/pdf/q-alg/9605034v2). The source itself dates the original work April 1996 and v2 is dated 18 November 2005.

Source statement summary: Section 1, equations (1.1)–(1.8), distinguishes positive real recurrence coefficients from general complex ones and requires a separate simplicity check for the latter. Section 2, equations (2.4)–(2.9) and Theorem 1, describes the degree-N terminal polynomial and finite orthogonality for a primitive Nth root, with parameter exclusions and a terminal simplicity condition. Section 4 gives selected positive symmetric regimes. Section 5, Theorem 3, gives a positive continuous-q-Jacobi regime; its later equations (5.14)–(5.15) reach q-Hermite by limits. These statements do not assert simplicity of every earlier polynomial for arbitrary complex recurrence coefficients. This audit read those source bodies, not only metadata or search snippets.

The calculations below are the reviewer's independent target comparison and counterexamples. They are not quotations of the source or an assertion that its authors made the rejected transfer.

## 2. Target, indices, and apolar convention

The unchanged target is odd N=2m+1≥3, primitive q of order N in characteristic zero, h=(N+1)/2, and f_k=q^(h k²). For the shifted moment form

    F(X,Y)=Σ_(k=0)^(2m−1) binom(2m−1,k) f_(k+1) X^(2m−1−k)Y^k,

write the degree-m ordinary differential operator

    A(U,V)=Σ_(j=0)^m t_j U^(m−j)V^j.

Differentiation gives shifted contractions proportional to Σ_j t_j f_(k+j+1), for 0≤k<m. Thus the annihilator is T_m(z)=A(1,z), with no reciprocal, conjugation, or sign reversal:

    T_m(z)=Σ_(j=0)^m (−1)^(m−j) [m choose j]_q z^j.

It obeys T_0=1, T_1=z−1 and

    T_n=(z−1)T_(n−1)+(1−q^(n−1))zT_(n−2).

T_m(0)=(−1)^m, so the zero-node guard is automatic; monicity excludes an infinite node. The recurrence polynomial must still have simple nonzero nonresonant roots. A reduced rational realization cannot discard repeated poles. In particular, a formal orthogonality formula allowing derivatives at repeated nodes does not give legal first-order nonconfluent branches.

## 3. Exact specialization and terminal-degree failure

Set the external source's parameters b=c=d=0 while retaining nonzero a. Direct simplification of its recurrence coefficients gives

    u_n=1−q^n,  b_n=a q^n.

The limit a→0 is regular for each polynomial and produces

    S_0=1, S_1=x,
    S_n=xS_(n−1)−(1−q^(n−1))S_(n−2).

The chirp conversion, checked directly by recurrence, is

    T_n(z)=(i√z)^n S_n((z−1)/(i√z)).

This is a polynomial identity independent of the sign chosen for √z. It supplies the appropriate comparison with continuous q-Hermite, including its normalization; it does not identify degrees m and N.

At degree N the external terminal formula specializes to

    S_N(t+t^(−1))=t^N+t^(−N).

In the conversion choose t=−i√z. Multiplication by (i√z)^N gives, for odd N,

    T_N(z)=z^N−1.

The N roots are simple in characteristic zero, but all satisfy λ^N=1. They are precisely prohibited cycle poles. This is a particularly strong control: even transferring terminal simplicity exactly cannot produce an admissible chirp-resolvent bank.

For the target T_m, m=(N−1)/2 is strictly below N and gcd(m,N)=1. Merely relabeling the external terminal degree as m would also require changing q to have order m, contrary to the target. No power of the same q can have order m>1, because its order must divide N. Powers coprime to N retain order N. This excludes the direct degree/base relabeling shortcut; it does not claim to exclude every imaginable future transformation.

## 4. Positivity does not transfer

For any primitive q of odd order N≥3, q is nonreal. In the target recurrence

    u_2/u_1=(1−q²)/(1−q)=1+q

is nonreal. A common affine change x=αy+β and monic normalization changes each off-diagonal recurrence coefficient by the same factor α^(−2). Therefore, whenever the target degree is at least three, u_1 and u_2 cannot both be made positive real by such a change. This obstruction applies to the recurrence itself, even if all terminal spectral nodes happen to be real.

The source's explicitly positive continuous-q-Jacobi range has parameters on the unit circle. The q-Hermite limit a=c=0 is not in that range; a limit through complex parameters cannot silently inherit positive weights. The separate real-parameter positive symmetric regimes likewise do not identify the target recurrence.

Exceptional small sizes do not create a closure: N=3 has m=1 and T_1=z−1, a forbidden pole. N=5 has m=2 and

    Disc(T_2)=(1+q)²−4=(q−1)(q+3)≠0.

There is only one off-diagonal coefficient at that degree, so the two-coefficient obstruction is intentionally not asserted there. Its simplicity is already within the prime-order baseline. N=1 is outside the target.

## 5. Exact adversarial counterexamples to the invalid inference

These are generic complex/signed Jacobi counterexamples, **not chirp counterexamples**.

Take b_n=0 and (u_1,u_2,u_3,u_4)=(1,−4,1,1). The monic recurrence gives

    P_2=x²−1,
    P_3=x³+3x,
    P_4=(x²+1)²,
    P_5=x(x²−1)(x²+2).

All four recurrence coefficients and their cumulative norm products are nonzero. P_5 has distinct roots and discriminant −10368. But P_4 has two double roots. Moreover gcd(P_3,P_4)=1, so the rational function P_3/P_4 is reduced despite its repeated denominator. Thus neither terminal simplicity plus nonzero norms nor a reduced rational numerator-denominator pair implies lower-degree squarefreeness. The five terminal roots support the usual finite complex quadrature; the lower even degree remains nonsimple.

An independently selected odd-degree control uses (u_1,u_2,u_3,u_4)=(1,−1,1,2). Then P_3=x³ while P_5=x⁵−3x³+x has discriminant 400. This independently rejects the same inference without the parity refinement.

At the actual F021 target, nonsingularity of the shifted Hankel matrix rules out reducing the realization dimension by numerator cancellation. It does not turn repeated poles into a sum of legal simple poles. Distinct first-order resolvents sharing a node combine to one first-order term; they cannot represent derivatives or higher-order poles.

## 6. Scope of fresh checks

`check_independent.py` was written for this review and executed locally using installed SymPy 1.14.0. It imports no research archive code. Exact integer polynomial reduction modulo Φ_N was used at

    N=3,5,7,9,11,13,15,17,21,25.

All controls passed:

- 58 shifted recurrence equations, with independent direct ordinary differentiation of the binary forms.
- Nonzero constant term and reciprocity for each T_m.
- The chirp–Hermite variable conversion at each target degree.
- The terminal identity T_N=z^N−1 at every listed N.
- Direct testing of every cycle root: no target resonance for even m; only λ=1 for odd m, with nonzero derivative there.
- Both generic counterexamples, including squarefree terminal denominators, repeated lower polynomials, and the even example's reduced P_3/P_4.

Full results are in `CHECK_RESULTS.json`. These bounded controls are indexing and nontransfer checks. They are not a new all-composite squarefreeness certificate, do not repeat the earlier 250-size archive certification, and are not a proof for untested orders.

## 7. Preserved mathematical and attribution boundary

The existing all-odd resonance classification, prime-order squarefreeness, separately scoped family certificates, and forced diagonal product are unchanged. The external source assumes a primitive root but not a prime order; that generality concerns its terminal family and does not fill the half-order composite gap. Galois conjugacy transports algebraic identities and gcds, not arbitrary statements about the absolute values of algebraic roots.

The common-P scalar model still excludes confluent branches, changing cycles, branch-dependent endpoints, and resonance. All-composite squarefreeness for N≡1 mod 4 remains unresolved. Generic finite-forbidden-set Waring existence was already attributed in the baseline and is not new progress in this pass.

No source-derived improvement to O(N³) fallback setup/O(N²) application or O(N²) successful lower-bank setup/application was found. Those costs remain operations over the supplied cyclotomic base field, with a growing-dimensional quotient state. This audit adds no bit-complexity, numerical stability, scalar-width-one, explicit base-field root, unrestricted inverse minimum, or FFT-speedup claim.

The defensible outcome is a narrowly source-bound exclusion: the inspected terminal-degree and positive-weight results do not close F021's chirp-specific root-legality/simplicity or historical-priority gate. They also do not disprove the target theorem or certify worldwide novelty. No native state change is justified beyond an optional additive research-source note under the parent's authorized workflow.

## 8. Candidate review and pass-level stopping condition

The companion report `resolve_f021_chirp_gate_2343/REPORT.md` was read in full. Its parameter cancellations, polynomial map, Gaussian-binomial terminal proof, affine/diagonal-similarity positivity obstruction, finite functional, and restrained attribution conclusion are accepted. No mathematical correction is needed. The final accepted report pins arXiv v2 explicitly and has SHA-256 `03489cfd7bdce247eb7389163d1b93bbd54bf2421d977917a820d26a80ac305c`, 12,364 bytes. Its final version only adds the acceptance notice and exact-version URL to the reviewed content; those changes were checked.

The candidate's explicit finite functional was independently evaluated, without running its code, on all 25 products P_i P_j for 0≤i,j≤4. The resulting Gram matrix is exactly diag(1,1,−4,−4,−4). This independently confirms that the generic even-degree counterexample has a fully nondegenerate complex finite orthogonality relation.

The exact index record was independently fetched from `math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json` at the repository baseline, Git blob `b31a38dbb1291fa5b8fdeaa22bdad799018cffa2`; the extracted row is preserved in `F021_GATE_READBACK.json`. It confirms Research overview row 19, status TO RESEARCH, priority 53, and a pass-level condition permitting an exact implication or qualified nonmatch. This report meets that **source-comparison pass** condition. That is distinct from closing the F021 record or its mathematical/priority research gate.

Verdict: **ACCEPT — bounded source nonmatch, no correction required.** The candidate's four proposed additive attribution/next-source cell supplements are mathematically appropriate if the parent elects an authorized update. The reviewer did not check or mutate live cell contents, so fresh exact-cell readback, preservation of existing text, and verification remain the parent's responsibility. No status, priority, accepted-theorem, or stopping-boundary mutation is supported.
