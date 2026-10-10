# Priority and significance of the overlap and content extensions

Date: 2026-10-10. Bounded primary-source assessment. Correctness and literature priority are separate: the overlap audit accepts all five stated families, and the new content audit accepts its conditional valuation theorem and three fixed-base computations. This assessment does not repeat those audits or certify global originality.

## Decision

**The combined local Rogers–Szegő discriminant work remains a credible focused-paper candidate, but several apparently distinctive ingredients have exact established antecedents.** In particular:

- The overlap polynomial `J` is a standard gap-two Hermite combination. By parity it is a quadratic pullback of an adjacent-degree quasi-Laguerre polynomial, so its standalone ordinary discriminant is covered by Sawa–Uchida's theorem.
- The characteristic-p Wronskian identity is exactly a hook-partition specialization of established pseudo-Wronskian equivalence and the Grosu–Grosu congruence theorem.
- The content exponent is a specific application of the local order and ordinary cyclotomic ramification; its final minimum-valuation/floor step is standard.

These are substantive reductions, not matches based on paper titles. Full normalization maps and proofs appear in `PRIMARY_REDUCTIONS.md`. They narrow the plausible contribution without invalidating the project mathematics.

**The strongest surviving candidate is the explicit leading coefficient of the shared-root local degeneration at an arbitrary fixed odd root of unity, with its ordinary-discriminant coefficient and resulting arithmetic application.** The reciprocal residue identity and paired-good selection provide a potentially useful new combination. No exact antecedent for that combined Rogers–Szegő theorem was established in the inspected sources. This is a bounded negative result, not evidence sufficient to announce priority.

## Claim by claim matrix

| Claim | Exact antecedent or reduction | Candid status and role |
|---|---|---|
| Root-of-unity factorization `H_(Ad+b)=(1+z^d)^A H_b` | q-Lucas; explicit continuous-q-Hermite equivalent in Atakishiyeva–Atakishiyev–Koornwinder (2.8) | Established input; no novelty claim |
| General q-to-1 Hermite limit | Same paper (3.8), among classical limits | Established; distinct from the fixed-ω blow-up |
| `J=He_(A+1)+A(1−τ)He_(A−1)` as a polynomial family | Order-two quasi-orthogonality; exact quasi-Laguerre parity map | Established form; not a new generalized/Dunkl/Uglov family |
| `Disc J` as a standalone ordinary-discriminant object | Sawa–Uchida, Theorem 4.8, plus quadratic pullback | Direct consequence of established formulas |
| Shared-root local coefficient with `τ=dW/g` | No exact equivalent located in inspected fixed-root q-Hermite/Askey–Wilson sources | Narrow principal novelty candidate; needs remaining full-text checks |
| Exact order `ord_(Φ_d)D_(Ad+b)=dA(A−1)/2+A` and full leading coefficient | Standard discriminant root products after the new local coefficient | Useful candidate theorem; not a new general discriminant method |
| `1/τ(ω)+1/τ(ω⁻¹)=1` at `d≡3 mod4`, half degree | Finite q-binomial theorem and complementary half-sum pairing | Specific identity not located verbatim; short classical-identity application |
| `U′V−UV′−yUV=−y^p` for `A=(p−1)/2` | Hook partition `(A+1,1^A)`; Gómez-Ullate–Grandati–Milson Theorem 3.1 plus Grosu–Grosu Theorem 8 | Exact consequence of known theory, with a shorter elementary proof here |
| At least one of the reciprocal-τ pair is squarefree for `p≡3 mod4` | Quasi-Laguerre repeated-root location, hook congruence, and zero-root exclusion | Possible new short corollary/combination; not an independently new broad Wronskian theorem |
| Coupling inverse residue factors to the Rogers–Szegő ramified bridge | No exact combined antecedent established | Useful application candidate; retain existential good-factor scope |
| Five families `d=3,7,11,15,19`, `p≡3 mod4` | Uniform criterion with exact lower-base inputs; five old isolated certificates close `p∣d` cases | Genuine project extension to infinite families; external novelty unresolved |
| `v_p(c_(sp))=floor(3s(p−1)/8)` under `s,p≡1 mod4`, `p∤s c_s` | Exact local order `3sA²/2` plus standard integral-basis and ramification conversion | Clean conditional application candidate; best a corollary in the same paper |
| Prime-base valuation `v_ℓ(c_ℓ)=floor(3(ℓ−1)/8)` | Classical q-to-1 Hermite leading part and prime cyclotomic uniformizer | Particularly elementary specialization; no standalone major-significance claim |
| Reciprocal contraction and smaller determinant for unramified support | Factoring into reciprocal quadratics, Gaussian special values, multiplication resultant | Useful obstruction reduction; classical algebraic ingredients |
| Bases `17,21,25` and their three new infinite-family corollaries | Exact finite computations feeding the already accepted sufficient criterion | Supporting evidence and applications; enumeration itself is not a priority argument |
| Uniform support of all `c_d`, all composites or higher ramification | Not proved by either extension | Outside the theorem; no claim that literature regards these as open |
| Restricted scalar-bank minimum or a faster FFT | Only the former follows in the accepted narrow model | Application appendix at most; no transform-complexity improvement follows |

## Why the older families do not automatically absorb the local theorem

The exact root-of-unity q-Hermite formula fixes `q=ω`; it therefore does not determine the first nonzero term as `q` moves away from `ω` while a polynomial variable approaches a repeated root. Generalized/Dunkl Hermite changes every odd recurrence coefficient, while this `J` changes one terminal coefficient. Uglov's inspected construction varies two Macdonald parameters together and keeps its polynomial variables fixed. Askey–Wilson terminal-node and measure-limit results likewise do not supply the required shared-cluster coefficient in the inspected statements. The detailed equation-level comparisons are in `HERMITE_DEGENERATION_COMPARISON.md`.

The closest standalone discriminant result is ordinary quasi-Laguerre theory. By contrast, Ismail–Witte's explicit Rogers–Szegő product uses a q-difference operator; it is not the derivative discriminant required here. Neither distinction should be turned into a claim that an exhaustive literature exclusion has been achieved.

## Publication recommendation

Prepare one focused manuscript around **local ordinary discriminants at fixed odd roots of unity**, combining separated and simple-overlap clusters. Lead with the general `n=Ad+b` local theorem and exact discriminant, then explain the ramified criterion and the two arithmetic consequences: inverse-pair squarefreeness selection and conditional rational-content valuations. Keep finite base arrays as reproducible supporting data. Put the scalar-resolvent consequence last, with the original model stated precisely.

Credit the quasi-Laguerre discriminant and hook-Wronskian antecedents explicitly. It is reasonable to retain the project's self-contained differential-equation proof because it is short; add that it is a special case of the known hook congruence. Novel application does not require inventing a new polynomial family.

Relative to the earlier assessment, the overlap and valuation results strengthen the coherence and breadth of the manuscript, but the literature reductions reduce the number of independently new mechanisms one may claim. The valuation formula is attractive and exact; it is not evidence of a new general theory of ramification. The package remains more plausibly publishable as a specialized note than as a major general breakthrough. No venue-acceptance prediction is warranted.

## Remaining priority boundaries

Lubinsky–Saff (1987), DOI `10.1007/BF01890574`, and Zhedanov (1997), DOI `10.1142/S0217751X97000438`, still lack complete legitimate full-text comparison in this work. A new author-uploaded ResearchGate lead for the former could not be opened; the latter's available record explicitly offered only a full-text request. No author request was sent. The previously denied Vanderbilt route was not retried or bypassed.

These are outstanding checks, not proof that either paper contains the theorem, and not the only conceivable literature. The next priority decision should compare exact degree ranges, root orders, simple-overlap hypotheses and ordinary derivative normalization against accessible original text. If old sources already prove the five-family squarefreeness, assess the local coefficient separately. If they also contain that coefficient, reframe the work as an attributed arithmetic application.

## Correctness and scope guardrails

The content audit is `content_extension_independent_audit_0420/INDEPENDENT_AUDIT.md`; it accepts the result with two useful scope clarifications: the reduced determinant is defined for `d=4r+1≥5`, and the good upper prime can be chosen explicitly by reduction to the good lower primitive root. This does not establish literature priority.

Retain all local residual discriminant/resultant guards. Retain `p∤d` in the uniform overlap argument and identify the five separate finite exceptions. Retain `p≡3 mod4` in the pairing lemma: at `p≡1 mod4`, the zero-root obstruction can invalidate the conclusion. Retain `p∤s c_s` in the content theorem. One good residue factor is sufficient; it is not equivalent to all factors being good. None of these results proves arbitrary prime powers or excludes additional unramified divisors of the content.

No publication, submission, public posting, or third-party outreach was performed. No submitted implementation was run or imported. The assessment's own exact checks are normalization controls, not a replacement independent audit.
