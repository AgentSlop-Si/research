# Independent end-to-end review of the original negative-chirp theorem

Date: 2026-10-20 UTC. Final frozen whole-theorem review; clean independent replay passed.

## Verdict and exact frozen object

**ACCEPT SCOPED: the complete original-family all-N theorem. No essential mathematical repair was needed or supplied.**

The reviewed author object is the complete fusion package, not its earlier
conditional draft. Its FROZEN_FUSION_MANIFEST.json is pinned at
d9871af6db9a406d4b0a5ac22e6321f1dc0cad343c6df41c39c810c65c1b41a3, and its FUSION_PROOF.md at
e123577bd09a8601f06627b449e31443b61bd0bdfd2155c506b4e32ea31d6905. The two final leaf acceptances are separately pinned:

- Representatives 86/87/90: review manifest
  78a649ba39638a6ae01f132a4901863909f0d01f9ab1ae1ad7dcf42c5448398c,
  binding author manifest
  6a985d0bd834b06ab1b714ef5a8322d7318b020fa045ee2922075136e160602d.
- Representatives 111/115/129: review manifest
  6964e1997ec0a6a6520d4e7b02e190aaa6ff4b96ba173906da1ad4026c3d255b,
  binding author manifest
  01c8e78772631cf21ee1c2766ab3e87e8960bdfed3e65a28a5ed16749e6565b3.

The accepted statement is precisely the following. For every positive odd
N=5m with gcd(m,5)=1 and N congruent to 3 modulo 4, and every primitive complex
Nth root omega, let F[i,j]=omega^(ij), A[j,j]=omega^((N+1)j^2/2), and
B=(F^(-1)+A)^(-1). The inverse exists. B cannot be written as the sum of two
fixed-coordinate terms L_r(I-W_r)^(-1)R_r, where all endpoint masks are arbitrary
complex diagonal matrices, W_r follows an arbitrary Hamiltonian row cycle with
arbitrary complex weights, and product(weights) is not 1. Zero weights,
singular masks, and entirely zero masks are included. The two cycles need not
be distinct. Consequently the precise exceptional set defined in the author
proof, within this family and grammar, is empty. There is no size cutoff.

This does not extend to the positive-congruence branch, moduli divisible by
25, unmatched endpoint permutations, products, three or more summands,
unrestricted Fourier algorithms, or a novelty claim. It does not establish
that three summands suffice or are the exact minimum. An empty necessary
system proves nonrepresentability without any sufficiency assertion.

## 1. Independent scope and evidence boundary

I read the complete fusion proof and the original model's analytic reduction,
not just a coverage count. I inspected each accepted leaf review's actual
domain and boundary mechanism, including the distinct root-algebra treatment
of representative 7. I independently reconstructed the entire pair partition
and every member's symmetry transfer, verified every bound payload, and
checked that each leaf acceptance binds the exact candidate being used.

The large row-eliminant and rank-minor computations remain the separately
reviewed mathematical dependencies. This review does not claim to freshly
rebuild all large original determinants or multiply all large four-embedding
norms. It freshly recomputes all 799 rank-record even/odd gcd and positive-ray
tests from their exact inert norm records, and freshly reconstructs all 90
small original block determinants and their full norms. For representative 7,
the prior independent record provides the exact even/odd parts rather than
the full norm coefficient list; those parts' gcd is freshly checked. For
32/33/38, exact norm data come from the author coefficients already fully
reconciled in that group's accepted independent review. These provenance
distinctions are retained rather than disguised as independent reconstruction.

No author or earlier reviewer executable was imported or run by my review
scripts. The new scripts use Python and SymPy and read only inert JSON/text.
The final isolated replay uses a fresh directory, immutable copies of the
required inert inputs, and byte-equal output comparisons. Numerical samples,
floating-point roots, and finite-field anchor counts are not the proof of the
universal exclusion.

No essential mathematical repair, new witness, omitted branch, new guard, or
substitute argument was supplied to the candidate. The candidate's earlier
conditional header was replaced by its author when the final leaf gates
became accepted. That status update was not a mathematical repair. Two
reviewer-local comparison failures during development were caused by SymPy
Poly equality distinguishing ZZ from QQ domains; explicit QQ construction
resolved them. No candidate coefficient or proof changed in response.

## 2. Original inverse and every primitive character

With h=(N+1)/2, define G=sum_x omega^(h*x^2),
C[i,j]=omega^(-h*(i+j)^2), and D[i,j]=omega^(-h*i^2)delta_ij.
Completing the square gives FAF=GC, while character orthogonality gives
FAC=ND and AD=I. Thus direct expansion yields

    (I+FA)(F-GC+NGD)=(1+NG)F.

The change of variables (u,v)=(x-y,x+y) is bijective for every odd modulus,
including nonsquarefree ones. Therefore G*conjugate(G)=N. Every eligible N is
at least 15, so |NG|=N^(3/2)>1 and 1+NG is nonzero. Left multiplication by
F^(-1) produces a right inverse of F^(-1)+A. This proves the original inverse
exists and equals (F-GC+NGD)/(1+NG); it is not assumed to exist first.

The odd-modulus Gauss-character identity is valid for every unit coefficient.
I checked the stated primary reference directly: Gurevich, Hadani and Howe,
section 3.1, equation (3.3) and Remark 3.3,
https://arxiv.org/html/0808.2447. The latter explicitly uses arbitrary prime
powers in the Jacobi symbol. Writing a primitive character as
omega=exp(2*pi*i*a/N) merely changes the unit coefficient to ah. The ratio for
coefficients -ah and ah is (-1/N)=(-1)^((N-1)/2), giving conjugate(G)=-G and
G^2=-N on the claimed family. No imaginary square-root sign is selected.

My exact cyclotomic controls verify all 460 primitive characters at 15 small
odd moduli, including squareful 9,25,27,45,63,75,135. Some are deliberately
outside the final family as sign/domain controls, not theorem extensions.
The tests separately check G^2, G*conjugate(G), and conjugation, plus 3,130
entrywise FAF/FAC identities. These finite controls supplement the universal
argument, and cannot substitute for it.

## 3. Restriction preserves zero edges and the precise target

For S=(0,m,2m,3m,4m), gcd(5m,m^2)=m, so eta=omega^(m^2) has exact order five.
Since h=3 modulo 5 and NG=-G^3, direct restriction gives

    B[S,S]=H(G,eta)/(1-G^3),
    H[i,j]=eta^(ij)-g*eta^(-3*(i+j)^2)-g^3*eta^(-3*i^2)*delta_ij.

The cubic sign and denominator are both negative. The denominator is legal
by the preceding inverse argument. Both signs of G and all primitive eta
embeddings remain in the leaf domain; correlations between G and eta only
narrow this domain and therefore do not weaken exclusion.

For row-cycle weights, W^N=rho I and
(I-W)^(-1)=(I+...+W^(N-1))/(1-rho). Contracting each arc between successive
selected vertices multiplies its original weights, including zeros. The arcs
partition all original edges, so the contracted product is exactly rho, and
the legal denominator is unchanged. Each selected-to-selected numerator is
the same path product; diagonal numerators are 1. Singleton restrictions also
agree. No edge is divided by. Diagonal masks restrict entrywise, so this
lemma applies with every mask degeneracy retained. The nonzero target scalar
can be absorbed into a mask.

The independent implementation checks 120 exact restrictions across reordered,
singleton, intermediate, and full subsets. Every test has a zero edge, and
the masked versions include all-zero masks. These controls use a separately
written path-product construction, not the author's implementation.

## 4. Closed necessity includes all singular-mask strata

For nonsingular masks, P^(-1)=R_1^(-1)(I-W_1)L_1^(-1) has exactly the allowed
row support, and Q^(-1) has the allowed column support. Normalizing gives
U=D_lambda P^(-1), V=Q^(-1)D_mu, and

    U(P+Q)V=D_lambda V+U D_mu.

This implies the off-support equations and every 11-column maximal minor of
the original 25-by-11 augmented matrix. It does not require the converse
rank-consistency implication, which would fail when the coefficient rank
drops. X,Y remain ten coefficient-column labels, not added unknowns.

An eleven-row minor has scale weight product(lambda_i^(n_i-1)) times
product(mu_j^(m_j-1)). If an index is missing, a coefficient column is zero
and the minor is identically zero. Otherwise all exponents are nonnegative;
total row degree and column degree are six each. This is a polynomial
multihomogeneous system on the whole product of ten projective lines. My
formal entrywise scaling control checks all 275 augmented-entry identities
which yield this determinant weight.

For arbitrary singular masks, replacing every zero mask entry by t makes
both summands invertible over C((t)) while their sum tends to the original
target. Every inverse row/column pair can be normalized by its lowest
nonzero t-valuation. Its coordinates then lie in C[[t]] with a unit among
them. All ten specializations are nonzero projective pairs. Polynomiality
and multihomogeneity preserve the equations on specialization. No limit of
the scale variables is required. This includes an identically zero mask,
and does not divide by any edge or individual direction coordinate.

The independent controls reconstruct these limiting pairs without using the
author routine. They pass 120 singular-mask necessary-system checks,
including 58 with an all-zero mask and 96 with a zero base coordinate. Exact
augmented rank is at most ten in every test. This is evidence about the
implementation, while the valuation argument proves the general statement.

## 5. Every leaf has the required parameter and boundary scope

The computational domain is every real n>0 with g^2=-n, both imaginary signs,
and every primitive fifth root. It is wider than the actual original
integer family, but no theorem about other original N is inferred.

The freshly rebuilt 90 block determinants cover every unordered 2-by-2 row
and column set with intersection at most one. Their four-embedding norms
match the accepted data coefficientwise. Splitting P(g)=A(n)+g B(n), the
exact gcds are 1 or (n+1)^4. Thus the entire original off-support-block family
is nonsingular throughout the claimed domain. Independent all-pair graph
enumeration finds 4,320 transitions and every one of these 90 block types;
there are 456 connected cases and 120 cases with component sizes 2 and 3.

Invertible transitions make projective transports bijective. Forward maps
and backward adjugates remain invertible. A polynomial scalar removed from
an entire such product cannot vanish on the domain, because it would make
the undivided invertible product zero. This reasoning does not permit
discarding equation contents. Quadratic, direction, and minor contents are
explicit guards and are checked separately in the leaves.

The 384 row exclusions use true homogeneous quadratic resultants and retained
contents. I verify their exact indexed candidate polynomials and positive
root exclusion, including n^4-n^3+n^2-n+1, whose product with n+1 is n^5+1.
The accepted row review, rather than this fusion review, supplies the full
384 symbolic resultant reconstructions.

For representative 7, the guarded coordinate change is global on the
quadratic root set: A=ak^2-bk+c is the value at the omitted point [-k:1],
and q(A-kt,t)=A*(t^2+(b-2ka)t+aA). With A nonzero, every projective root is
represented. Tensor quadratic root algebras include repeated roots. A root
evaluation is a nonzero linear functional; a vanishing minor makes its
multiplication operator singular, so its determinant must vanish. The
accepted full norm obstruction and every chart/content guard exclude this
on n>0. This method is not applied indiscriminately to other representatives.

Other connected leaves keep a complete homogeneous root. Split leaves use
x(ax+by) or y(bx+cy), retaining a nowhere-zero b guard. The listed two root
vectors are nonzero, distinct, and exhaustive, including a=0 or c=0. Their
other component stays homogeneous. Each reconstructed column is J A^t u
with A invertible, and therefore cannot be zero. No rank-zero continuum is
lost. Ignoring additional equations only enlarges the necessary solution set.

Every selected determinant is an original eleven-row augmented minor.
Its prescribed homogeneous degree comes from the scale weights, not the
actual affine degree. Fixed-size Sylvester determinants retain infinity,
repeated roots, zero coordinates, leading-degree drops, and zero specialized
forms. Removed contents are still guards. The individual accepted reviews
reconstruct these determinants and compare full prescribed-degree resultants.

The four-embedding norm implication is exact: if one embedding vanishes,
the rational norm does; for real n>0, its real even/odd parts must both
vanish for either nonzero imaginary sign. The gcd therefore contains every
possible positive parameter. My fresh checks reconstruct all recorded norm
splits where provided, recompute all 799 exact gcds, and count their roots
on the open positive ray after removing powers of n. All counts are zero.
The per-group record counts are 7,90,214,73,39,73,118,73,56,56. No guard or
resultant domain was inferred solely from a prose statement of acceptance.

## 6. Symmetry and actual membership, not a count sum

The cycle enumeration is the 24 lexicographic traversals starting at zero.
I independently construct their successor permutations and their ordered
Cartesian square. The index convention is compared against every baseline
record and every final coverage record, not assumed from matching integers.

Dilation r_a(i)=ai sends cycles to r_a*pi*r_a^(-1) and similarly for tau.
The exact target identity is H(g,eta)[ai,aj]=H(g,eta^(a^2))[i,j]. All required
embeddings are already included. Transpose sends (pi,tau) to
(tau^(-1),pi^(-1)), with U'=V^t,V'=U^t and H^t=H. The X/Y coefficient
columns exchange and equation rows permute. Neither U nor V is inverted,
so singular directions and coordinate zeros are preserved.

These operations yield exactly 78 disjoint orbits: 66 of size eight and
12 of size four. The 384 row pairs form an explicit set; its exact complement
is 192 pairs in 28 whole orbits. Every residual representative has one and
only one accepted rank owner. For every one of the 576 final records I check
the actual pi/tau, exclusion class, exact author and review hashes, accepted
domain, and, where required, the explicit dilation/transpose transfer and
coefficient-record binding. This is a verified set partition, not a numerical
sum of batch sizes.

The groups are 384 row pairs, then 8,24,16,24,20,24,20,16,24,16 rank pairs.
The sum 576 is only a cross-check after the individual incidence proof.
Eleven independent mutations are rejected: a missing pair, a duplicated pair
replacing another, altered successor convention, unaccepted leaf, wrong author
hash, wrong review hash, wrong embedding power, wrong representative,
narrowed sign domain, changed coefficient certificate, and changed row
candidate polynomial. A superficially unchanged total cannot rescue these.

## 7. End-to-end contradiction and review limits

Suppose an original representation exists at an eligible N and primitive
omega. The exact inverse/restriction supplies (G,eta) in the complete leaf
domain. Grammar contraction and singular-mask closure supply a nonzero
projective point of the original necessary system for one induced pair.
The independently verified partition puts that exact pair in one accepted
row or rank class. The valid symmetry, if needed, transfers it to a complete
accepted representative exclusion. This is a contradiction. Hence no
eligible N or primitive character survives, and the defined original-family
exceptional set is empty.

There is no remaining low-modulus range, sign choice, singular mask, zero edge,
chart boundary, or dropped leading-coefficient case inside this statement.
The earlier effective cutoff, projectivity/properness argument, and effective
Nullstellensatz are unnecessary for this final no-cutoff implication. The
historical missing-author-byte question remains separate and is not claimed
solved. No general FFT bound, global novelty assertion, or wider grammar
classification follows.

The dependency and fusion freezes are immutable evidence; older leaf reports
correctly disclaim global conclusions when considered alone. Their scopes
are combined only by this checked end-to-end argument. No GitHub, research
table, Library, or other external state was written by this review.


## 8. Final reproducibility receipt

The final fusion manifest lists 1,483 payload files. Every one was verified,
including the complete inert dependency snapshots. The 23 separately pinned
dependency manifests also pass their own 1,444 payload-occurrence checks. Both
last leaf acceptances were present before this verdict, and their exact bytes
are inside the frozen author inventory.

The clean independent replay passed all three reviewer programs in a fresh
temporary directory in approximately 15.67 seconds. The model-controls,
positivity-audit, and frozen-fusion-audit outputs are byte-identical to their
pre-replay versions. Reviewer code and inert input hashes are unchanged. The
review's own frozen manifest binds the full report, executable controls,
outputs, logs, clean replay receipt, and exact copies of the final fusion's
principal binding documents. The full author's dependency snapshot remains
the input to the manifest audit; the small binding-copy directory is not
misrepresented as a second complete dependency package.

There are no incomplete assigned cases or remaining mathematical blockers
within the stated original family. The review accepts the exact original
freeze only. A redacted, projected, repackaged, or rewritten public version
requires its own genuine-byte manifest and explicit identity mapping; this
verdict does not certify modified bytes through a hash adapter.
