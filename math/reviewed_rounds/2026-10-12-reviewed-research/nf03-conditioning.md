Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: a9267641dfd83d1dfcdda0a2a81fd6d951ce7d6ef4d42a824a680372f92c360c

---

# NF-03 compact-parameter conditioned family: independent scoped review

12 October 2026. This review concerns NF-03::conditioned-family and the existing NF-03 / Q20 / ALG-EVEN-PRONY-EXTRA-POLE / NEW-07 identities. It adds no discovery row and makes no external-priority claim.

## Verdict

**Scoped ACCEPT** for the exact frozen inputs recorded in `INPUT_BINDING.json` and the accompanying final seal. No unresolved mandatory mathematical repair was found. The final proof incorporates the one addressing/dispatch correction identified during review.

For every even N=2h>=4, the least legal member of the rational parameter grid {1/(2N),...,1} is well defined. Its degree h+1 polynomial has distinct nonzero nodes, all avoiding alpha^N=-1. The roots support the accepted full common-shift bank representation. For exactly the unscaled moment Vandermonde in the proof, kappa_2(V)<=2^(2N^3), whereas the old large-parameter family's same-coordinate condition number is >=2^(2N^4). The complete constructive preparation costs 2^[O(p+N^3)] bit operations; the prepared approximate bank, including all branches simultaneously, is applied in O(N^log_2(3)) exact rational operations with the separately stated finite-bit query bound and normalized relative error guarantee.

This is a deterministic finite-selection family, not a proved closed-form choice t=1/(2N) or t=1. It proves a substantial exponent improvement over the specified old family. It does not prove polynomial or practically small conditioning, polynomial-time certified preparation, practical FFT speed, a production floating-point executor, h-pole optimality, or every NF-03 objective. The subquadratic bank query is a paid generic polynomial-multiplication baseline, not a novel FFT claim.

## 1. Exact model and legality

The review preserves the accepted P_n coefficient/phase convention, positive q=exp(2*pi*i/N), c_j=q^[j(j-1)/2], and negative-sign normalized Fourier target q^(-ij)/sqrt(N). The parameter only changes B=zP_h+tP_(h-1). B remains monic of degree m=h+1 for every t, so no exceptional degree loss or root at infinity is hidden.

Consecutive P-polynomial coprimality and P_(h-1)(0)!=0 give gcd(zP_h,P_(h-1))=1. At a repeated root, P_(h-1) cannot vanish, and t is uniquely determined by that root. The eliminant F'G-FG' has degree 2h-1 and leading coefficient 2. Thus at most 2h-1 distinct complex t values are bad for squarefreeness. Each of the 2h forbidden nodes excludes at most one more t, or none when G vanishes. At most 4h-1=2N-1 parameter values are bad; the 2N distinct nonzero rational candidates contain a legal one. Its constant term has modulus t>=1/(2N), ruling out a zero node.

The accepted B recurrence needs exactly s=0,...,h-2 constraints to propagate the first h+1 matching moments through index 2h-1. It does not assert unneeded infinite moment matching. Retaining possible zero residues is legitimate for the at-most-h+1 bank; the inherited Hankel lower bound still supplies at least h nonzero weights. No cancellation is used to excuse an illegal inverse.

The signed-shift identity is exact, including the negative wrap. The endpoint phases reduce to -ij after accounting for the N/2 wrap exponent. Both endpoint applications, normalization, all bank branches and all N outputs remain paid.

## 2. All-embedding radius and denominator-aware norms

The tridiagonal leading-principal determinant recurrence gives B exactly, with final subdiagonal -t and final diagonal zero. At every coefficient-field embedding, the diagonal bound is 3, subdiagonal bound is 2, and superdiagonal modulus is 1; the last subdiagonal has modulus at most 1. The max-coordinate eigenvector argument therefore gives radius at most 6 without assuming normality or positivity. R=8 is a valid common dyadic envelope. The constant/product identity supplies the lower root-radius bound.

The parameter denominator cannot be omitted from either norm argument. The final proof correctly uses lambda^(2m-2)disc(B) and lambda^N Res(B,z^N+1) as algebraic integers, where lambda=2N. The first degree is the total discriminant coefficient degree; the second is the resultant degree in B's coefficients. Their nonzero field norms are integers. Dividing out all other embeddings yields exactly the displayed denominators, including lambda exponents multiplied by d=phi(N), not merely by d-1.

With 2R=16, m=N/2+1, d<=N, and ceil(log2(2N))<=N-1, the discriminant exponent is at most 2N^3-2N. The forbidden-resultant exponent after isolating one root factor is at most (5/2)N^3+(5/2)N^2-2N-1<=4N^3. Factoring alpha^N+1 then gives the stated nonpole distance. These estimates use all conjugates of the coefficient polynomial, not an unjustified bound on one embedding or a needlessly large splitting field.

The separate root-gap and root-derivative estimates correctly isolate different factors of the discriminant. In particular |B'(alpha)| is obtained directly from its incident-pair product. Substituting the worst pairwise gap into every derivative factor would degrade the exponent to O(N^4); the final proof does not do that.

## 3. Singular values, cancellation and normalized precision

The Vandermonde matrix is precisely V[j,i]=alpha_i^j with no uncharged scaling. Its norm is at most mR^(m-1)<=2^(2N). The identity |det V|=sqrt(|disc B|) and the product of singular values yield ||V^-1||<=U^(m-1)/|det V|. This establishes the claimed inverse and condition bounds; it does not confuse a determinant with the smallest singular value directly. The bound 2^(2N^3) is strictly below the old family's accepted lower bound 2^(2N^4) at every admitted N.

For the unitary signed shift, the inverse norm is controlled by min_tau |1-alpha tau|. The forbidden-node set is invariant under inversion and its nodes have modulus one, so this minimum equals distance from alpha to that set. The pole margins, individual inverse norms and perturbation-resolvent identities therefore use the right geometry, without an omitted |alpha| factor.

The root perturbation and residue-error terms are summed over every branch. They are small enough independently, so the precision proof does not rely on uncertain cancellation to obtain the normalized output. The Neumann bound for the approximate moment solve, the component-to-vector rounding allowance for beta, the subsequent residue rounding and all minimum root tolerances fit p+O(N^3) precision. The retained disks label roots once at the final precision; no unnoticed cross-run permutation is assumed.

For endpoint errors, a telescoping product spends at most (8N+4N+2N)a_0<=16Na_0; the separate exact-scaled bank error is smaller than its assigned budget. A nonzero b-bit dyadic input has norm at least 2^-b. Rounding all 2N real output components within the displayed absolute tolerance gives the claimed relative error. Because the exact Fourier target is unitary, relative-to-input and relative-to-exact-output norms agree. Zero input is handled separately.

## 4. Paid preparation and simultaneous evaluator

Exact parameter selection is an algorithm, not an oracle. Each coefficient-field Sylvester determinant can be tested through its rational multiplication-block representation. The block determinant is its field norm, so nonvanishing is equivalent. The rational denominator is cleared before fraction-free integer elimination. Reducing q exponents modulo N before cyclotomic reduction justifies the stated polynomial coefficient-height bound. Minor bounds keep the elimination operand lengths polynomial, and O(N^20) is safely conservative.

The root-grid procedure is finite at one prescribed coefficient/modulus precision. At a nearest grid center its Rouché inequality has a strict uniform margin. The coefficient-vector uncertainty and modulus enclosures consume less than that margin. Every inconclusive unrelated center is rejected, so there is no indefinitely refined equality case. A retained disk contains one root. Disks for distinct roots cannot meet because 4r<delta, so greedy overlap rejection never loses the last representative of an unrepresented root. The root-derivative bound makes the grid exponent P+O(N^3), and the remaining rational-series, exact solve, root/residue/endpoint and kernel work is polynomial in the provided sizes. The exhaustive grid was not run at its enormous general-theorem bounds.

The full approximate bank kernel is derived from its actual approximate poles/residues: w_i=g_i/(1+a_i^N), followed by the fraction-sum product tree P/Q and formal inverse of Q with Q(0)=1. It is not substituted with the exact chirp kernel. Newton doubling has residual equal to the square of the previous residual. Unequal tree sizes and non-power-of-two N are handled with paid padding/truncation. Karatsuba and the final negative fold compute the action of every branch on the same input, simultaneously.

The common-denominator construction is consistent even though its f_i and D_common are Gaussian integers rather than real integers. In variable u=z/2^H, the numerator tree and formal reciprocal use Gaussian-integer coefficients. The final coefficient denominators share Delta=D_common*2^[H(N-1)]. Conjugation and a squared norm turn the last complex division into ordinary rational coordinates with only constant-factor bit growth. Intermediate coefficient bounds, dyadic inputs/endpoints, integer convolution, negative folding and output division all fit O(N^log2(3)[N^2(p+N^3)+b]^2) schoolbook bit work. A rational-operation bound is not treated as a fixed-word or bit bound.

### Corrected issue before freeze

The draft labeled all Karatsuba address/dispatch work O(N log N). Recursive three-way dispatch has O(N^log2(3)) instances. The frozen proof now charges that overhead within the full O(N^log2(3)) query cost; only the outer root-power/division/routing work retains the smaller O(N log N) bound. The repair changes no main theorem, precision exponent or query bit bound.

## 5. Fresh independent controls and limits

No supplied, inherited or author executable was run. All three control scripts here were written independently for this review. Copied inputs were read as inert text. The scripts use installed general-purpose arithmetic libraries, not author code. The final author code/results were statically inspected, including its larger finite-field legality certificates; those author runs are not mislabeled as independent reruns. Every manifest member, the candidate archive, and the four copied-source pins were checked against their declared hashes.

- Exact characteristic-zero cyclotomic arithmetic for every even N=4,...,20 tests every member of the full 2N-candidate parameter grid, checks the first legal choice, the three-term recurrence, the tridiagonal characteristic polynomial, every required moment-propagation constraint, the exact discriminant and forbidden-resultant denominator clearing, and nonzero integer field norms. The forbidden t=0 zero-node case is rejected. In these finite cases k=1 works; no universal k=1 inference follows.
- Rational-interval certificates for N=4,6,8,10,12 enclose all 3,4,5,6,7 roots respectively in disjoint radius-2^-40 disks. Machin's identity, alternating trigonometric remainders, dyadic outward enclosures and exact squared comparisons support each Rouché inequality. Numerical mpmath roots propose centers only; no numerical root output is accepted without the exact rational certificate. Shifted false centers and a repeated-root test are rejected.
- Exact Gaussian-rational whole-bank tests at N=4,6,8,10,12,14,16 compare every basis-column action and a mixed input against independent signed-resolvent recurrences. Karatsuba scalar-product counts agree with the three-way recurrence. Replacing the negative wrap with a positive wrap fails the negative control.
- Independent fraction-tree/formal-inverse tests at N=4,6,8,10,14,18,22,26,30 reproduce all direct bank moments. A second Gaussian-integer common-denominator construction reproduces those exact coefficients, including non-power-of-two tree sizes; every promised integer coefficient is checked.
- Exact phase-exponent checks cover every target entry for even N=4,...,80. Conservative exponent-ledger checks cover every even N through 10000. These finite controls supplement the proof, not replace its all-degree arguments.

This is a review of the mathematical construction, formal bit contract and fresh finite controls. It is not validation of a complete production implementation, an executed exhaustive general root grid, or a practical performance benchmark.

## 6. Guidance for the existing rows

Accept and record these bounded sub-obligations as completed: a deterministic compact rational legal family for every admitted even N; an explicitly improved same-coordinate uniform condition envelope; complete paid certified preparation and precision requirements; and a simultaneous full-bank subquadratic rational-operation evaluator with a distinct bit ledger.

Keep the broader conditioned/practical NF-03 continuation open. Explicitly retain polynomial or practically small conditioning, practical polynomial-bit preparation, a production finite-word executor and matched FFT comparison, exact h-pole optimality, universal t=1, other model/field extensions and external priority as open or not established. Preserve the old accepted construction and lower bound. Update only the existing stable identities, without increasing discovery counts or presenting the generic Karatsuba baseline as a novel FFT.
