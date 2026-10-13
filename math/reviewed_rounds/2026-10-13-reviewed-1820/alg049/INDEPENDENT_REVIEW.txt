ALG049 rational cycle final factor extension
Independent mathematical and exact certificate review
13 October 2026 UTC

VERDICT: ACCEPT within the precise scope stated below. No repair is required.

The fixed eight-dimensional two-factor prefix cannot be completed to a
nonzero scalar-unitary matrix by any invertible final factor whose inverse
Gram has constant diagonal, even with a unitary monomial at the LAST
boundary. Every spectrally regular and invertible rational function of a
uniform-modulus weighted Hamiltonian cycle satisfies this hypothesis.
The arbitrary-unitary-separator counterexample is valid and makes the
monomial restriction substantive for this broad final-factor class.

This is a mathematical and exact-computation acceptance. It is not a
novelty determination, a general Fourier impossibility result, a runtime
claim, or closure of unrestricted ALG049. There is no change to the first
boundary. The all-dimension result is the cycle lemma; the obstruction
remains the displayed N=8 prefix.

1. Exact source and dependency binding

Reviewed candidate archive:
ALG049_Rational_Cycle_Final_Factor_Extension_Candidate_2026-10-13.zip
Bytes: 167,527
SHA-256: d1716e7f5b33eb087124e125f2a348dae72f5f3674b2c7765846308c9e625367

Candidate PROOF.md:
Bytes: 16,379
SHA-256: a5b888fd82b0b584011edcc782770eb7229eb3e97030010bbe49e9672697bdec

The complete archive membership, every one of the nine manifest-listed
files, all lengths and SHA-256 hashes, and all three SOURCE_PINS entries
are verified. The tenth archive file is MANIFEST.json itself. All ten
files in the supplied working directory matched their archived bytes
before this review packet was sealed. SOURCE_DIRECTORY_CHECK.json records
that read-only check.

The prior independent-acceptance archive is pinned by SHA-256
06466cfce5d6c24e85025d73b716d8f810da435cc51c5a2a70795a17976f2a78.
Its INDEPENDENT_REVIEW.txt is byte-identical to the copied
TWO_PHASE_INDEPENDENT_REVIEW.txt. Its embedded two-phase candidate's
PROOF.md is byte-identical to the copied TWO_PHASE_PROOF.md. This checks
both source identity and the provenance of the quoted proof/review.

The enlarged result is reviewed directly. It does not rely on running
historical verifiers or trusting the historical check counts. Historical
programs were read only, never executed or imported. The new verifier is
independently authored. The author's 4,198 checks and timings are preserved
as source provenance; those counts were not adopted as independent evidence.
The arithmetic sum of those reported category counts is checked.

2. Prefix reconstruction and all four strict certificates

The source uses columns: an edge (u,v,w) means M e_u = w e_v.
The exact fixed cycles are

M1: order (0,1,2,3,4,5,6,7), weights (1,1,1,1,1,1,1,-1).
M2: order (0,1,3,4,5,6,2,7), weights (z,1,1,1,1,1,z^(-1),-1).

The phase condition is |z|=1. The original primitive is
K(M)=(2I-M)(I-M)^(-1), including its numerator. The prefix is
T=K(M1)^e1 K(M2)^e2, with no inserted separator, and L=T* T.

Direct edge reconstruction verifies M^8=-I, unitarity on the unit circle,
characteristic polynomial t^8+1, det(I-M)=2, and det(2I-M)=257.
All factors and their inverses therefore exist throughout the phase domain.

The reviewer reconstructs the two signs by polynomial identities:

K(M) = (3I+M+M^2+...+M^7)/2,
K(M)^(-1) = (129I-64M-32M^2-16M^3-8M^4-4M^5-2M^6-M^7)/257.

Both the defining equation K(M)(I-M)=2I-M and both orders of the inverse
identity are checked entry by entry. This supplies a reconstruction
independent of the candidate's direct-matrix-inversion implementation.
Then the reviewer computes the two individual squared column norms of T,
rather than adopting the candidate's full Gram calculation. On the unit
circle, conjugating a Laurent expression with rational real coefficients
replaces z by 1/z. With x=Re(z), the exact differences are

--: L33-L00=(443686-377300x)/16974593
    >=66386/16974593>0.
-+: L33-L00=(15x-57)/257
    <=-42/257<0.
+-: L33-L00=(28474x-35657)/66049
    <=-7183/66049<0.
++: L33-L00=4-x>=3>0.

Indices are zero-based. Both endpoint values of each affine polynomial
have the same nonzero sign; the listed positive absolute lower bounds are
exact minima for x in [-1,1]. Every x in this interval is possible for a
unit z. Denote these four lower bounds by d. There is no exceptional phase
at z=1 or z=-1, and no extra phase has been introduced in M1.

3. General final-factor theorem and separator order

Let T,C be invertible square matrices, S unitary, and B=TSC. Exact
multiplication gives B*B=C*S*LSC. If B*B=cI, then

L=c S(C^(-1))*C^(-1)S*.

The order is correct: this is an invertible congruence, with left
multiplier S(C^(-1))* and right multiplier C^(-1)S*. No commutation or
normality assertion for C is being used. Since B is invertible, a scalar
Gram has c>0, exactly the nonzero scalar-unitary target.

A unitary monomial S has one unit-modulus entry in each row and column.
In (SHS*)_jj only a single diagonal entry H_kk survives, with coefficient
one. Thus S permutes the diagonal of H and preserves its constancy. Taking
H=(C^(-1))*C^(-1) with constant diagonal forces L to have constant diagonal,
contradicting Section 2 for every sign pair and every allowed phase.

The hypothesis refers to squared COLUMN norms of C^(-1) in the original
coordinate basis. Neither constant diagonal of an unrelated Gram nor
constant diagonal after an arbitrary basis change may be substituted.
Normality of C is unnecessary for this general theorem.

Arbitrary unitary multiplication at the two outside endpoints preserves
scalar unitarity in both directions. A nonzero overall scalar does also.
These observations preserve the exclusion; they do not silently preserve
the numerical size of the defect under rescaling.

4. Quantitative estimates

For every real c, E=B*B-cI is Hermitian. Set
D=S(C^(-1))* E C^(-1)S*=L-cSHS*.
The diagonal difference D33-D00 equals L33-L00, because SHS* has constant
diagonal. For Hermitian D,

|D33-D00| <= 2 ||D||_2,
|D33-D00| <= sqrt(2) ||D||_F.

The first follows by bounding each diagonal Rayleigh quotient; the second
is Cauchy-Schwarz on the two diagonal entries, followed by their inclusion
in the Frobenius sum. The constants 2 and sqrt(2) are sharp for the
extraction step, as witnessed by diag(-d/2,d/2).

Unitary invariance and submultiplicativity give, for either norm,
||D|| <= ||C^(-1)||_2^2 ||E||. Therefore

||B*B-cI||_2 >= d/(2 ||C^(-1)||_2^2),
||B*B-cI||_F >= d/(sqrt(2) ||C^(-1)||_2^2).

No assumption c>0 is needed for these inequalities, only c real as stated.
The inverse-norm factor is squared and is in the correct denominator.
The norm estimates are parameter-dependent and do not give a uniform bound
as C varies through an ill-conditioned or rescaled family. The exact
controls verify the full congruence for c=-2,0,7/3 and each sign pair, and
verify the two sharp extraction constants. The universal norm inequalities
are established by the proof above, not inferred from sampled eigenvalues.

5. Uniform-modulus cycle lemma and rational functions

For N>=1 and rho>0, a full weighted directed cycle with |w_j|=rho satisfies
Q^N=mu I, Q*Q=QQ*=rho^2 I, and det(tI-Q)=t^N-mu, where mu=product w_j.
Each coordinate is visited once by Q^k e_j for 0<=k<N. These N vectors
have pairwise disjoint coordinate supports and squared norms rho^(2k).
Consequently, for any degree-less-than-N polynomial h,

(h(Q)*h(Q))_jj = sum_(k=0)^(N-1) |h_k|^2 rho^(2k),

independent of j in the original coordinate basis. Arbitrary cycle order
and individual edge phases cause no problem. Uniform modulus, not merely
the identity Q^N=mu I, is what makes the column norms independent of j.
The determinant identity includes N=1. Nonzero mu gives N distinct roots
of t^N-mu, since its derivative N t^(N-1) cannot vanish at a root.

For a reduced rational function f=p/s, the two guards

gcd(s,t^N-mu)=1 and gcd(p,t^N-mu)=1

mean exactly no spectral pole and no spectral zero. They ensure that
C=p(Q)s(Q)^(-1) exists and is invertible. The Euclidean algorithm gives
a unique residue h of degree <N with hp=s modulo t^N-mu. Evaluating at Q
gives h(Q)=C^(-1), so the inverse-Gram diagonal is the positive constant
sum |h_k|^2 rho^(2k). Positivity follows because h(Q) is invertible and
rho>0. The optional spectral-average formula follows from normality of Q
and trace invariance, not merely its characteristic polynomial.

The new controls obtain h by recovering coefficients from ONE column of a
directly inverted rational matrix, then reconstructing every entry of the
inverse and checking hp=s modulo t^N-mu. This is independent of the
author's modular-inversion construction. Both guards and positivity are
checked at the fresh exact test cycles.

At rho=0, Q=0 and f must be regular and nonzero at 0. Then C=f(0)I and
gamma=|f(0)|^(-2). This is a separately handled degenerate limit, not a
nonzero-weight Hamiltonian cycle. Modulo t^N the same inverse residue exists
when p(0)!=0; only its constant coefficient survives in the gamma formula.
The convention rho^0=1 is essential. No spectral-distinctness argument is
used at zero radius.

Reduction of a rational function and evaluation of a literal matrix
quotient are distinguished correctly. An unreduced denominator vanishing
on the spectrum makes the literal inverse undefined. Cancellation may
yield a different, well-defined reduced rational interpretation. Genuine
poles remain excluded. Genuine zeros make C singular and cannot produce
a nonzero scalar-unitary TSC with invertible T,S.

A finite product of rational functions of the SAME Q is another rational
function of Q, after reduction and the appropriate spectral guards.
Products involving unrelated cycles are not claimed to preserve the
constant inverse-Gram diagonal. The enlarged application takes N=8 in
this general lemma and leaves the fixed prefix untouched.

6. Explicit constants and guards

Equation (4) follows from
(aI-Q) sum_(k=0)^(N-1) a^(N-1-k) Q^k=(a^N-mu)I.
The sole resolvent guard is a^N!=mu. There is no division by a, so a=0 is
allowed when mu!=0. Combining the coefficient formula with the cycle
lemma gives equation (5) for C=aI-Q exactly as printed.

For C=(aI-Q)^(-1), the inverse is aI-Q. At N>=2 its two column supports
are distinct, yielding gamma=|a|^2+rho^2. At N=1 the entries coincide,
yielding gamma=|a-mu|^2. This necessary cross-term exception is explicit.
At rho=0, a!=0 gives gamma=|a|^(-2) for C=aI and gamma=|a|^2 for its
resolvent. A vanishing determinant is never treated as invertible.

For the literal Mobius factor C=(aI-Q)(bI-Q)^(-1), both b^N!=mu and
a^N!=mu are required for existence and invertibility. Polynomial
multiplication gives c0=(a b^(N-1)-mu)/(b^N-mu) and
ck=(a-b)b^(N-1-k)/(b^N-mu), 1<=k<N. Swapping a,b gives the inverse
coefficients and equation (7), including its conjugate absolute squares.
The formula is correct at N=1, a=0, b=0, and a=b under the stated guards.
At a=b on a spectral pole the literal expression is undefined even though
the separately reduced rational function 1 is regular. At rho=0 the
literal invertible quotient requires a,b both nonzero and equals (a/b)I.

Taking (a,b)=(2,1) gives equation (8) for gamma_K. Swapping them gives
equation (9) for gamma_(K^(-1)). The guards are mu!=1 and mu!=2^N.
For N=8,rho=1,mu=-1 they reduce to 86/257 and 4 exactly. At zero radius
they are 1/4 and 4. At mu=1 the literal K denominator is singular; at
mu=2^N its denominator is regular but its numerator is singular. Allowing
arbitrary rho means neither exclusion may be discarded via a unit-radius
argument. In the final N=8 application these monodromies are 1 and 256.

All four prefix sign pairs are excluded and either final K sign qualifies.
Thus the new all-eight three-sign statement is proved. The earlier packet
stated only its six requested mixed-sign words; this review does not
rewrite its historical scope.

7. Boundary counterexamples

The nonuniform N=8 cycle with weights
(2,1/2,1,1,1,1,1,-1) has mu=-1. For C=I-Q the exact inverse-Gram diagonal is
(11/4,11/16,11/4,11/4,11/4,11/4,11/4,11/4).
This disproves the assertion that Q^N=mu I alone suffices. It does not
assert that this particular C completes the fixed prefix.

For Q=P/2 and C=I-Q, exact inversion gives H00=1028/765 and H01=104/153.
The real unitary block [[3/5,4/5],[-4/5,3/5]] on coordinates 0 and 1
changes the first two diagonal entries of SHS* to 7636/3825 and 2644/3825.
They differ. Thus arbitrary unitary conjugation does not preserve constant
diagonal, despite preservation under monomial conjugation.

The stronger existence counterexample is also correct. For any invertible
T choose an SVD T=V D W*, with D positive diagonal. For the ordinary cycle
P let P=F Lambda F*, with a unitary Fourier eigenvector matrix F and N
distinct eigenvalues. Interpolate a polynomial p of degree <N with
p(lambda_j)=D_jj^(-1). Then C=p(P)=F D^(-1)F* is invertible, belongs to the
permitted rational-cycle class, and has no spectral pole or zero. With
S=W F*, one obtains T S C=V F*, which is unitary.

This proof applies to the fixed obstructed prefix itself, for each allowed
phase and sign pair. Its chosen S cannot be monomial, by the established
exclusion. No pole restriction at 1 applies to the interpolating polynomial.
The fresh program additionally constructs an exact N=8 control using
singular values 1,...,8, nontrivial V,W, exact eighth roots of unity, and
explicit interpolating coefficients. It verifies the full completion
identity without a numerical SVD or an approximate eigensolver. This finite
control corroborates the general existence proof; it is not itself the
argument for every fixed-prefix instance.

At N=1 every nonzero scalar is scalar-unitary. The cycle lemma still holds,
but no all-N prefix obstruction follows. The N=8 certificate explicitly
uses positions 0 and 3 of the specified eight-dimensional matrices.
A singular C always yields rank(TSC)=rank(C)<N for invertible T,S and
cannot attain the nonzero scalar-unitary target. Zero products are excluded
by the target convention.

8. Independent controls and reproducibility

The reviewer program reads the pinned candidate archive as bytes and JSON
data, without extracting or evaluating executable source. Its fresh exact
controls include complete source binding, the four symbolic prefix
certificates, formal resolvent and Mobius polynomial identities for
N=1,...,20, and fresh weighted cycles in every dimension N=1,...,9.
The latter use different exact phases, reverse cycle orders, and radii
2/3 and 4/3. They check characteristic polynomials, forward and reverse
normality, traversal monodromy, all path supports and norms, direct
resolvents, shifted-cycle and resolvent Gram constants, Mobius constants
including both K signs, and a genuinely higher-degree rational factor.

Specialized controls cover zero radius and singular monodromies at
N=1,2,8; literal versus removable poles; genuine zeros; N=1 cross terms;
zero shifts; coincident Mobius shifts; exact N=8 monomial congruences;
the quantitative diagonal witnesses; both printed counterexamples; and
an explicitly interpolated arbitrary-unitary completion.

The fresh successful run completed 7,530 exact assertions in 170.60 seconds
wall time, 170.71 seconds user CPU, and 79,780 KiB peak RSS, using Python
3.12.14 and SymPy 1.14.0. INDEPENDENT_RESULTS.json contains the exact derived
data, transparent per-category counts, total check count, and resource usage.
VERIFICATION_LOG.txt records the complete successful run. One matrix-entry
comparison counts as one assertion, with a separate shape assertion.
Finite controls support the implementation. The proofs above establish
the parameter-continuous and all-dimension statements within their scopes.

Reproduce from the extracted review directory, with Python 3, SymPy 1.14.0
and assertions enabled:

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 timeout 300s python3 review_fresh.py

Each run has a 240-second CPU limit and 2 GiB address-space cap; the command
adds a 300-second wall cap. BLAS and OMP use one thread. The reviewer makes
no floating-point mathematical decisions, uses no numerical search,
executes/imports no historical program, installs no dependencies, and
makes no network calls. Times are provenance rather than a complexity
claim. No Sheet or GitHub writes were made. Candidate and historical
source files are unchanged. The sealed review includes the original
candidate archive unchanged, this review, the new verifier, and its data.
