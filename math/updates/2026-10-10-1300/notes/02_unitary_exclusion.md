# All-length real-collinear unitary Green exclusion

10 October 2026. Independent mathematical audit of the submitted note
NEW_THEOREMS_AND_PROOFS.md and its companion evidence bundle.

## Decision

Accept Theorem A as stated: for every integer N>=4, every finite number
of nonsingular unitary Hamiltonian-cycle Green resolvents, and arbitrary
real-collinear coefficients, their sum cannot be made into the cyclic
Fourier matrix by independent row and column permutations and invertible
diagonal factors. The proof does not require positive coefficients,
a bound on the term count, primality, or even N.

Theorem B is mathematically consistent with, and duplicates, the
already accepted complete-extension treewidth bound ceil(N/4)-1 in the
Schur v28 audit, claim SV28-04. It is not a new project result.

These are restricted matrix-representation statements. Neither is an
unrestricted arithmetic lower bound or an improved Fourier algorithm.
Publication priority is unestablished.

A separate phase-averaging construction supplies actual N=2 and N=3 Green
witnesses and complex-coefficient universality. Its independent acceptance
is recorded separately in PROOF_STATUS.json. It is not needed for the exclusion.

## Exact accepted statement

Let W_j, j=1,...,q, be N-by-N monomial matrices whose support is one
directed Hamiltonian cycle and whose nonzero entries have modulus one.
Assume I-W_j is invertible. Let q be any finite nonnegative integer.
Let c_j=lambda r_j, where every r_j is real and lambda is one common
nonzero complex number. Then for N>=4 the matrix

M=sum_j c_j (I-W_j)^(-1)

is unequal to D_1 P_1 F_N P_2 D_2 for every choice of invertible complex
diagonal D_1,D_2 and permutation P_1,P_2. Here
F_N[a,b]=exp(2*pi*i*a*b/N), with indices 0,...,N-1.

The same conclusion holds for the normalized Fourier matrix
N^(-1/2) F_N, the inverse-normalized matrix N^(-1) conjugate(F_N),
and the negative-exponent convention, because nonzero global scales
are absorbed into the diagonal factors and exponent reversal is a
permutation of Fourier column labels.

The empty sum or all-zero coefficients produce the zero matrix and
are trivially excluded. Taking lambda=0 would also be trivial.
Every displayed resolvent must exist; a singular inverse cannot be
made meaningful by placing a zero coefficient in front of it. Such an
unused term should simply be omitted.

## Independent derivation of the Hermitian identity

For a unitary W with I-W invertible, define G=(I-W)^(-1).
Since W^*=W^(-1),

I-W^(-1)=-W^(-1)(I-W),
G^*=(I-W^(-1))^(-1)=-(I-W)^(-1)W=-GW=-WG.

The final commutation is valid because G is a rational function of W.
Hence G+G^*=G(I-W)=I. The sign is negative in G^*=-WG;
the identity is G+G^*=I, not -I or 2I.

Equivalently i(2G-I)=i(I+W)(I-W)^(-1) is Hermitian.
This is the classical inverse Cayley-transform mechanism.
Its singularity is at eigenvalue 1. Eigenvalue -1 is allowed.

For a single weighted Hamiltonian cycle, let H be the product of
its edge phases. Following the directed cycle N times gives W^N=H I.
Its characteristic polynomial is t^N-H, so 1 is an eigenvalue
exactly when H=1. Thus the stated nonsingularity assumption is
equivalent to H!=1 in this model. For H!=1,

G=(I+W+...+W^(N-1))/(1-H).

Every intermediate power W^k, 1<=k<N, has zero diagonal. Therefore
every diagonal entry of G is d_H=1/(1-H), and
d_H+conjugate(d_H)=1. The cycle support, not unitarity alone,
provides the common diagonal.

For real coefficients r_j, let A=sum_j r_j G_j.
Then A+ A^*=(sum_j r_j)I and every diagonal entry is

d=sum_j r_j/(1-H_j).

In particular A_ab=-conjugate(A_ba) for a!=b. This argument is
linear, so cancellation, negative coefficients, zero sum of the
coefficients, repeated cycles, different cycle orders, and any
finite q are all covered.

## Independent Fourier obstruction

Suppose A has a common diagonal d and skew-Hermitian off-diagonal
entries. Suppose also that A=D_1 P_1 F_N P_2 D_2.

The Fourier matrix and all its invertible monomial gauges have no
zero entries. Thus d and every A_ab are nonzero. For distinct a,b,

C_ab=A_aa A_bb/(A_ab A_ba)=-d^2/|A_ab|^2.

Every four-entry cross-ratio of a diagonally gauged Fourier matrix
has modulus one. Consequently |A_ab|=|d| for all a!=b, and all
paired ratios C_ab are the same phase

eta=-d^2/|d|^2.

Let u_a and v_a be the Fourier row and column labels selected at
coordinate a by P_1 and P_2. They are two independent permutations
of Z/NZ. Cancellation of the diagonal factors gives

eta=omega^((u_a-u_b)(v_a-v_b)), omega=exp(2*pi*i/N).

Relabel the common coordinate set to arrange u_a=a. This is only a
reindexing of the equations; no equality of row and column
permutations has been assumed. For some c modulo N,

(a-b)(v_a-v_b)=c mod N for every a!=b.

Taking a=b+1, for b=0,...,N-2, gives v_(b+1)-v_b=c, so
v_a=v_0+ac modulo N. Since v is a permutation, gcd(c,N)=1.
The pair (a,b)=(2,0) gives 4c=c, so 3c=0 modulo N.
Multiplying by the inverse of c yields N dividing 3.

This is impossible for N>=4. No illegitimate division modulo a
composite integer occurs: invertibility of c was first forced by
the permutation hypothesis. The argument uses (2,0) only when
N>=3. At N=2, the single paired-ratio condition is possible;
at N=3, it is also possible.

For common complex-line coefficients, apply this result to
A=M/lambda. If M had the proposed Fourier equivalence then so
would A, after replacing D_1 by D_1/lambda. The needed Hermitian
identity is asserted after this scalar division; it need not hold
for M itself when lambda is nonreal.

## Boundaries and controls

The submitted source correctly limits its conclusion to real-collinear
coefficients and ordinary inverses. It does not cover genuinely
noncollinear complex coefficients, nonunitary gains, sums of products,
pseudoinverses at holonomy one, or arbitrary arithmetic circuits.

The field is the complex numbers with ordinary conjugation and
positive absolute value. This proof is not automatically a
finite-field theorem. The Fourier matrix is the cyclic Fourier
matrix F_N. One must not extend the conclusion to every group
character table or every complex Hadamard matrix; for example real
skew-Hadamard matrices have precisely this sort of shifted
skew-Hermitian structure.

The common-diagonal assumption matters in the abstract lemma.
An arbitrary unitary resolvent has G+G^*=I but may have unequal
diagonal entries. The theorem applies only when the stated cycle
structure or another valid argument supplies a common diagonal.

The finite term count is unrestricted, but the source does not
define infinite sums. No convergence convention is needed or
asserted here.

The independent controls use only freshly written code and exact
arithmetic in Q(zeta_12), with a rational polynomial power basis.
They did not execute or import the submitted verification program
or either of the submitted source test suites.

- Exhaustive cross-ratio permutation checks for N=2,...,9 tested
  409,112 permutations. There were 2 admissible permutations at
  N=2, 6 at N=3, and none for N=4,...,9.
- Thirty-six exact legal-cycle cases, N=2,...,10, checked both
  inverse multiplication orders, unitarity, holonomy, diagonal
  constancy, entry nonvanishing, and G+G^*=I.
- Forty-five exact signed-real sum cases used q=0,1,2,7,17,
  including positive and negative terms and zero total coefficient.
  The complex-collinear scaled identity was checked separately.
- Holonomy-one cyclic shifts supplied exact singular-kernel checks.
  A nonunitary two-cycle control has a valid inverse but fails
  G+G^*=I.
- Exact N=2 and N=3 realizations and the N=4 noncollinear
  construction passed as controls of the separate reviewer-derived
  note. Their source acceptance and review statuses remain separate.

These bounded computations supplement the all-size proofs.
They do not prove the theorem merely by testing small N.

## Comparison with primary literature

Del Corso, Poloni, Robol, and Vandebril, When is a matrix unitary or
Hermitian plus low rank?, Section 7 and Lemma 16, state the
classical unitary/Hermitian Cayley correspondence and the exclusion
of eigenvalue 1 for the inverse transform. This directly situates
the Hermitian identity as a standard ingredient, not new mathematics.
Their displayed scalar inverse-domain exception has a typographical
minus sign; the denominator and Lemma 16 give the correct exclusion.
The algebra above is checked independently.
https://arxiv.org/abs/1811.05854

Ostergard and Valtonen, Equivalence of Complex Hadamard Matrices,
Section 2.3, discuss the classical Haagerup invariant built from
four matrix entries and attribute it to Haagerup. The paired ratio
used here is a specialization of this standard invariant mechanism.
The new proof must not be described as inventing cross-ratios or
monomial equivalence.
https://arxiv.org/abs/2609.21653

Rajchel, Gasiorowski, and Zyczkowski, Robust Hadamard matrices,
unistochastic rays in Birkhoff polytope and equi-entangled bases
in composite spaces, Appendix C, use Haagerup invariants to rule
out robust matrices equivalent to odd-order Fourier matrices.
Their argument imposes the particular paired phase -1. The present
common-diagonal theorem permits a general paired phase eta, so
that result is a close comparator rather than an identified proof
of the full submitted theorem. Its N=3 exception here causes no
conflict: the witness has nonreal diagonal and eta a cube root,
not -1.
https://arxiv.org/abs/1804.10715

These primary sources establish substantial classical ingredients
and a close earlier obstruction. The finite targeted comparison did
not locate the exact all-N real-collinear Hamiltonian-resolvent
statement. That negative finding is not a historical-priority
certificate.

## Theorem B and model separation

The submitted bound for K=[[A,E],[P,0]] is the same ceil(p/4)-1
bound already accepted in the Schur v28 audit. Its terminal inverse
block is -F_p^(-1); its support graph must include the E and P
routing edges. The inverse-separator proof permits singular
principal subblocks. The refined terminal grouping and its
generality to targets with all inverse square minors nonzero
match the earlier accepted claim. Record this as overlap, not
another new theorem or another priority claim.

The real-collinear unitary Hamiltonian-cycle model audited here
is distinct from the signed magnetic bank model based on inverses
of I-alpha S^epsilon-beta zeta^j T^delta and weighted phase-indexed
banks. A bank count in that model is not the q of this theorem.
No four-bank or five-bank classification, field-dependent
magnetic witness, or remaining small-order magnetic question is
settled by this audit.

## Provenance and evidence scope

The submitted theorem and companion archive are identified by filename and SHA-256 in SOURCE_MANIFEST.json. The theorem bytes match across the two sources. The broad historical novelty ranking in the companion report is not adopted here. Original source programs were not executed or imported. Independent exact controls and their mathematical certificates are distributed under programs/unitary and certificates/unitary; see REPRODUCE.md.
