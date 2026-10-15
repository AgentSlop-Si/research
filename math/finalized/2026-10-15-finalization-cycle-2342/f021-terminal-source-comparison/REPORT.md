# F021: A terminal root-of-unity theorem does not settle the half-degree gate

Date: 2026-10-15 UTC

Repository baseline: AgentSlop-Si/research, commit e5c9c53f7d34e8d858e781d2d5321393aec7e85c.

Independent mathematical review: ACCEPTED for this bounded source nonmatch and the four attribution-only supplements. No mathematical correction was required. This is not formal verification.

## Result

A specific fresh primary-source comparison gives a qualified nonmatch. The terminal-degree root-of-unity Askey–Wilson result of Spiridonov and Zhedanov specializes to a simple polynomial of degree N. Under F021's polynomial transformation, that terminal polynomial becomes exactly z^N−1. Its nodes are all cycle-resonant and therefore forbidden. It is not the degree-m shifted apolar polynomial needed for the smaller bank.

Neither the source's finite complex orthogonality nor its separately restricted positive-weight theorem repairs this degree and legality mismatch. The calculations below establish these nontransfer statements explicitly. They do not disprove squarefreeness of the actual chirp polynomial.

Keep F021 OPEN, priority 53, with accepted mathematics and existing complexity qualifications unchanged. This is an attribution comparison, not a new chirp theorem, a new correctness audit, a proof of all-composite squarefreeness, or a novelty clearance.

## 1. Exact gate and convention

The current rebuilt index records F021 at Research overview row 19, with an attribution-only next step. Its frozen stopping condition permits an exact implication or a qualified nonmatch. The generic legal-node mechanism was already compared with Ballico–De Paris; it is not revisited here.

Use the existing characteristic-zero, algebraic-closure setup:

    N=2m+1≥3; q primitive of order N; h=(N+1)/2;
    f_k=q^(h k²), g_k=f_(k+1).

The degree-(2m−1) binary moment form has coefficients binom(2m−1,k)g_k. Its unique monic degree-m apolar polynomial, with A(1,z)=T_m(z), satisfies

    Σ_(j=0)^m t_j f_(k+j+1)=0, 0≤k<m;
    T_m(z;q)=Σ_(j=0)^m (−1)^(m−j)[m choose j]_q z^j.

This identity and its LS87 attribution are accepted inputs, not new findings. Extend the same polynomial notation to arbitrary n by

    T_0=1, T_1=z−1,
    T_n=(z−1)T_(n−1)+(1−q^(n−1))zT_(n−2).

The actual free-diagonal m-bank requires T_m to be squarefree with roots outside {0}∪μ_N. Uniform resonance, prime-order squarefreeness, existing family/finite certificates, the forced diagonal, and charged construction remain separately established. The unresolved all-composite case is N≡1 mod 4, m=(N−1)/2; no extension of that scope is claimed here.

## 2. Primary source inspected

V. Spiridonov and A. Zhedanov, *Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity*, Duke Mathematical Journal 89 (1997), 283–305. The inspected arXiv version is v2, revised 18 November 2005; v1 was submitted 21 May 1996.

- Primary full text: https://arxiv.org/html/q-alg/9605034v2
- Version metadata: https://arxiv.org/abs/q-alg/9605034v2

Relevant locations are equations (1.1), (1.5)–(1.8); Section 2, equations (2.4)–(2.10) and Theorem 1; and Section 5, Theorem 3 with (5.10)–(5.15). Section 1 distinguishes complex bilinear orthogonality from positive real orthogonality and explicitly requires simple terminal nodes in the complex case. Section 2 calculates the degree-N polynomial and finite weights. Theorem 3 gives positivity only on a specified continuous-q-Jacobi parameter range. The q-Hermite limit is identified separately in (5.15).

These primary statements are the input. The parameter substitutions and obstruction arguments below are this report's algebraic comparison.

## 3. Exact specialization and the terminal-polynomial obstruction

To distinguish the source's diagonal recurrence coefficient from F021's branch weights, call it β_n. In source equations (1.6)–(1.8), first set b=c=d=0 while keeping a≠0. Direct cancellation gives

    ξ_n=a(1−q^n), η_n=a^−1,
    u_n=ξ_nη_(n−1)=1−q^n,
    β_n=−ξ_n−η_n+a+a^−1=a q^n.

The coefficientwise limit a→0 therefore gives the monic sequence

    S_0=1, S_1=x,
    S_n=xS_(n−1)−(1−q^(n−1))S_(n−2).

For each degree up to N this is a finite recurrence with a well-defined limit. The a^−1 factors in the intermediate presentation cause no singularity after the displayed cancellation.

The source's terminal formula, after this specialization, is

    S_N(t+t^−1)=t^N+t^−N.

Thus S_N is a scaled Chebyshev polynomial, with simple roots. However, the recurrence transformation used in F021 is

    T_n(z)=(i√z)^n S_n((z−1)/(i√z)), z≠0.

It follows directly by substituting the two recurrences, so it is a polynomial identity independent of the square-root choice. At primitive q of odd order N,

    T_N(z)=z^N−1.

An elementary verification needs no limiting argument: for 0<j<N, the Gaussian binomial [N choose j]_q has a numerator factor 1−q^N and no vanishing denominator factor. All intermediate coefficients vanish. The endpoint coefficients are 1 and (−1)^N=−1.

Consequences:

1. The terminal theorem concerns degree N, whereas the chirp gate concerns degree m=(N−1)/2.
2. The terminal roots in the z-variable are exactly μ_N, all of which make (I−zP)^−1 undefined.
3. Relabeling the source's root order as m is invalid: gcd(m,2m+1)=1 and q has exact order 2m+1, so q^m≠1.
4. Choosing any subset of the terminal roots still gives forbidden nodes. No legal lower-bank conclusion follows from their simplicity.

This is a concrete nonmatch, rather than merely absence of a matching phrase in the paper.

## 4. Why the positive-measure theorem does not transfer

The q-Hermite recurrence has u_1=1−q and u_2=1−q². For odd primitive q,

    u_2/u_1=1+q∉R.

Under a common affine change x=αy+β, α≠0, followed by monic renormalization, the recurrence coefficients u_j become u_j/α². Their ratio is unchanged. Consequently u_1 and u_2 cannot both become positive real numbers by such a change. For the unresolved composite cases N≡1 mod 4, N≥9 and m≥4, both coefficients occur within the target sequence.

This also blocks a proposed conversion by diagonal similarity of the recurrence matrix: the product of each opposing pair of off-diagonal entries is invariant. Congruence is a different operation and does not preserve ordinary eigenvalues.

The source's stated positive-weight parameter range is not available at the q-Hermite limit either. Its parameters have the form a=p^(α+1/2), c=−p^(β+1/2), p=e^(πi/N), with real −1<α,β<1. Therefore |a|=|c|=1 throughout that range; a=c=0 lies outside it. Complex orthogonality at the limit cannot be promoted to positive orthogonality by continuity from that parameter set.

These calculations rule out the inspected direct positivity route. They do not rule out every imaginable alternative transformation or proof.

## 5. Independent obstruction to the complex-orthogonality shortcut

Simple terminal nodes and nonzero recurrence coefficients do not, on their own, force every lower-degree polynomial to be squarefree. A small exact example with an even lower degree makes the distinction explicit.

Set P_0=1, P_1=x and P_(n+1)=xP_n−u_nP_(n−1), with

    (u_1,u_2,u_3,u_4)=(1,−4,1,1).

Then

    P_2=x²−1,
    P_3=x³+3x,
    P_4=(x²+1)²,
    P_5=x(x²−1)(x²+2).

All four u_j are nonzero. P_5 has five distinct roots, and P_4 has two double roots. For completeness, the finite bilinear functional on the terminal nodes is

    L(F)=2F(0)−[F(1)+F(−1)]/6
         −[F(i√2)+F(−i√2)]/3.

Direct substitution verifies L(P_iP_j)=0 for i≠j, 0≤i,j≤4, with squared norms

    (h_0,h_1,h_2,h_3,h_4)=(1,1,−4,−4,−4).

Hence even a fully nondegenerate finite complex orthogonality relation on simple terminal nodes does not establish lower-degree squarefreeness. This is a generic counterexample to that inference, not a counterexample to F021 or to Rogers–Szegő squarefreeness.

## 6. Verification and exact stopping boundary

The report uses the primary HTML theorem body, not a search snippet. Source version dates and journal metadata were read separately. No claim of rendered-PDF inspection is made.

The fresh local script check_nontransfer.py verifies the generic recurrence, gcd(P_4,P_4′)=x²+1, gcd(P_5,P_5′)=1, and gcd(P_4,P_5)=1. It checks all 25 entries of the displayed finite orthogonality matrix and its five stated norms. It also checks T_N=z^N−1 modulo Φ_N(q) at N=3,5,9. These bounded exact controls support the displayed algebra; the uniform terminal identity is proved above. They are not new composite chirp certificates. No predecessor code was executed or imported, no large search was run, and no external write was made.

The remaining accepted mathematical question is still nonvanishing of the ordinary discriminant of T_((N−1)/2)(z;ζ_N) for all unclassified composite N≡1 mod 4. The remaining attribution task requires an actual theorem at the half-order degree, or a separately matching explicit legal construction. The inspected terminal-degree and positive-range statements do not supply either. The present result neither establishes historical novelty nor changes any asymptotic claim.

## 7. Proposed minimal attribution-only cell supplement

Proposal only. No spreadsheet mutation was made. Preserve existing cell contents and all accepted theorem, status, priority and stopping-boundary cells.

Append to Catalogue!AD14 and 'Research overview'!O19:

    [2026-10-15; bounded primary-source nonmatch]
    Spiridonov–Zhedanov (Duke Math. J. 89, 1997), equations (1.6)–(1.8), (2.4)–(2.10), and Theorem 3, were compared with the exact chirp polynomial. The q-Hermite specialization proves simplicity at terminal degree N; under the chirp transformation its polynomial is T_N(z)=z^N−1, whose nodes are all forbidden. It does not establish squarefreeness of T_((N−1)/2). The positive-weight range excludes the q-Hermite limit; complex finite orthogonality alone does not imply lower-degree simplicity. This is a qualified source nonmatch, not a chirp counterexample or novelty clearance. Existing accepted scope, OPEN status and priority 53 remain unchanged.

Append to Catalogue!AE14 and 'Research overview'!P19:

    [2026-10-15; precise remaining attribution target]
    Seek a primary theorem controlling the ordinary derivative discriminant at degree m=(N−1)/2 for primitive q of order N, or a construction matching the legal simple nonzero nonresonant common-cycle branch grammar with charged costs. Terminal-degree root-of-unity simplicity and positive-weight theorems outside their parameter range do not close this gate. Retain all current model, field, finite-certification and complexity qualifications.

The independent reviewer accepted this bounded source comparison and the four additive attribution-only supplements. Its separate report is INDEPENDENT_REVIEW.md in the corresponding audit packet. This acceptance satisfies the qualified-nonmatch stopping condition for this particular primary source; it does not close F021 or establish all-composite squarefreeness.

## 8. Project evidence read

- Current exact gate: math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json, F021 record, at the pinned baseline. Its extracted record is saved in F021_GATE_SNAPSHOT.json.
- Accepted generic comparison: https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/finalized/2026-10-15-f021-open-waring-comparison/REPORT.md
- Chirp classification: https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md
- Its recorded independent audit: https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md
- Earlier source recovery: local F021_SOURCE_BOUND_REPORT.txt in f021_primary_recovery_1055, used to preserve the already-recorded LS87 identity attribution and source-access boundaries.

No changes to repository, branch, native Sheet, or canonical theorem register were made in this pass.
