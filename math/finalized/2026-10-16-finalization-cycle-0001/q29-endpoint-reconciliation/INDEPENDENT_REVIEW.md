# Q29 uniform-transfer review: inherited endpoint and exact remaining gate

16 October 2026 UTC. Independent symbolic and provenance review; no supplied
scientific program, installation, large census, or external write.

## Final verdict

The uniform implication B_e != 0 => B_(e+1) != 0 is not established. The fixed
t=27, p=5, e=3 theorem remains accepted and complete. The broader parent stays
OPEN / TO RESEARCH at priority 54, with no closure, count, priority, novelty,
or FFT-performance promotion.

An endpoint nonvanishing argument proposed during this review is valid, but
its entire Q29 specialization is already covered by F021's accepted uniform
resonance theorem. The useful correction is to carry that existing theorem
into Q29's remaining-gate description, rather than claim a new endpoint gate
closure. A general odd-degree version is checked below as a separate elementary
extension, with no historical-novelty assessment.

ACCEPT the final author's source-bound endpoint correction, nonvanishing
equivalences, and elementary endpoint generalization at exactly their stated
scopes. The report is q29_uniform_endpoint_20261016/REPORT.md, SHA256
5bab6bd2df55d20ea3f35bf6d1a452b053a6749433506d43a2d56832039193a6.
The complete final report was read independently after the symbolic and source
review. It claims no proof or disproof of the uniform transfer.

## 1. Independently inspected exact sources

Repository AgentSlop-Si/research, immutable read ref
4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a:

- math/finalized/2026-10-15-frontier-boundaries/README.md.
- q29_transfer_requirements_2345/SYMBOLIC_TRANSFER_AUDIT.md within that packet;
  retained full-text SHA256 8aeabd446e9ac5d6193052a91656a69bc71e965a50d9fd4f1aefc7b80b1c494f.
- q29_transfer_independent_2348/INDEPENDENT_REVIEW.md within that packet;
  retained SHA256 b2ed46aa54023891fd8db3c1d2e15d646151c5aebd2ee6462c702fb549b23ae6.
- q29_aggregate_accounting_review_2045/FINAL_AGGREGATE_REVIEW.md within that packet;
  SHA256 0a17797f8e77976e8af5b6233973a2e4818e4f2fcd5821529119c138b3534396.
- q29_closure_scope_audit_2110/INDEPENDENT_SCOPE_REVIEW.md within that packet.
- math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md,
  especially Sections 1 and 2, lines 1–107; exact complete local file SHA256
  c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1.
- math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md,
  especially lines 56–84; exact complete local file SHA256
  af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333.

The remote F021 theorem and review sections were independently fetched at the
same immutable repository ref; the full local copies were separately hashed.
The source-bound Q29 text was independently fetched, not obtained solely from
the new author. Workbook 1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU,
Research overview row 15 and Research queue row 32, was also read directly.
Its current text preserves the uniform target and the fixed-instance boundary.

## 2. The endpoint was already proved

Use n_e=(27*5^e-1)/2, which is odd. F021 writes its degree as m, whereas Q29
writes its reciprocal-quotient degree as m_e. To avoid conflating them, apply
F021 with its m equal to Q29's n_e and its N equal to 27*5^e.

F021 defines T_n(z;q)=(-1)^n H_n(-z;q), and expressly proves that T_n has a
simple zero at z=1 whenever N=2n+1 is 3 modulo 4. The primary proof establishes
algebraic simplicity by a nonzero linear coefficient of det(R-tB), and the
independent audit verifies that coefficient argument. The monic gcd statement
alone would not suffice to establish simplicity: gcd(T_n,z^N-1)=z-1 is also
consistent with a multiple root in T_n because z^N-1 is squarefree. Here the
separate simplicity assertion and proof are available.

The proof first uses the principal complex embedding and then carries the
algebraic nonzero derivative to each primitive embedding. The actual Q29 q_e
is primitive of order 27*5^e. Consequently

    U_e(-1)=H'_(n_e)(-1;q_e) != 0

for every e, independent of B_e or the lower-layer discriminant. No same-q
reciprocity has been relabeled as an inter-layer transfer.

The latest Q29 transfer audit still lists the shared endpoint in its explicit
product and describes it as an outstanding nonvanishing task. The explicit
product is correct; the task list is unnecessarily broad given the already
accepted F021 theorem. This is a source reconciliation, not a new Q29 theorem.

## 3. Exact remaining equivalences

The accepted residual-factor argument gives U_e(1) a unit, and the uniform
endpoint theorem above gives U_e(-1) nonzero. Hence

    B_e != 0 iff Disc(U_e) != 0 iff Disc(R_e) != 0
             iff Disc(P_(e,j)) != 0 for every j=0,...,26.

The middle equivalence uses the exact ordinary identity

    Disc(U_e)=Disc(R_e)^2 R_e(0)R_e(4),
    U_e(-1)=(-1)^m_e R_e(0), U_e(1)=R_e(4).

Also Disc(H_(n_e))=Disc(U_e) U_e(-1)^2, so nonvanishing of the full H ordinary
discriminant is an equivalent condition. This follows from the ordinary
product-discriminant identity and the actual nonzero endpoint.

The last uses the actual complete-DVR factorization, whose degree-12 residual
discriminant and all cross-resultants are units. None of these identities
provides coefficients or discriminants of P_(e+1,j), so none proves transfer.

The factor P_(e,0)(-1) must remain in the exact valuation identity. It is
nonzero, but it cannot be absorbed into a unit: the accepted e=3 endpoint has
valuation 75. Retain exactly

    B_e=epsilon_e P_(e,0)(-1) product_j Disc(P_(e,j)),

with epsilon_e a unit. Distinguish nonvanishing from unitness throughout.

## 4. Independent elementary check of the proposed broader endpoint lemma

Let n=2k+1<N, and let q be primitive of order N in characteristic zero. The
integral Rogers–Szegő recurrence gives

    H_(r+1)=(1+z)H_r-z(1-q^r)H_(r-1).

At z=-1, H_(2k)=product_(j=1)^k(1-q^(2j-1)) and H_(2k+1)=0.
Writing d_k=H'_(2k+1)(-1), differentiation gives d_0=1 and

    d_k=product_(j=1)^k(1-q^(2j-1))+(1-q^(2k))d_(k-1).

Induction yields

    d_k=sum_(r=0)^k product_(j=1)^r(1-q^(2j-1))
                         product_(j=r+1)^k(1-q^(2j)).

For q=exp(2*pi*i/N), every exponent a occurring lies between 1 and n-1<N.
Thus 1-q^a=(-i) exp(pi*i*a/N) 2*sin(pi*a/N), with positive last factor.
The term indexed by r has phase (-i)^k exp(pi*i*[k(k+1)-r]/N).
All phases lie in an arc of width pi*k/N<pi/2. Rotating its midpoint to the
positive real direction makes every term have strictly positive real part.
The sum is nonzero. Algebraic Galois invariance gives the assertion at every
primitive q. This verifies the actual polynomial identity without synthetic
corrections, truncated jets, numerical approximations, or a census.

The larger degree range is not the recorded half-order statement of F021, but
the Q29 application is already inherited. No novelty claim follows.
The author's optional observation N=n also checks: the largest exponent is
n-1=N-1, so every sine factor remains positive and the same strict arc bound
holds. The Q29 specialization only needs N>n.

The final report's principal-embedding geometric statement also checks. F021
excludes all unit-circle roots of U_e after removing the simple -1 root of H.
The map z -> z+2+z^-1 sends the unit circle onto [0,4], so R_e has no root in
that interval in this embedding. This does not control multiple complex roots
elsewhere or their absolute values under arbitrary field automorphisms.

## 5. Exact adversarial control for a tempting stronger matrix argument

The F021 argument at the zero root does not prove that every root is simple.
Even real positive off-diagonals and positive Hermitian real and imaginary
parts of B do not imply simplicity of all generalized eigenvalues.

Let R be the real symmetric 4-by-4 tridiagonal matrix with zero diagonal and
off-diagonal entries (1,2/sqrt(5),1). Put

    b=(3+i)/sqrt(10), c=(1+3i)/sqrt(10), B=diag(b,b,c,c).

Both Re(B) and Im(B) are positive definite. The continuant recurrence gives

    det(R-tB)=t^4 b^2c^2-t^2[b^2+c^2+(4/5)bc]+1.

Since bc=i, b^2+c^2=6i/5, this determinant is

    -t^4-2i*t^2+1=-(t^2+i)^2.

Its nonzero roots are double. This is an exact counterexample to that generic
matrix inference only. It is not a Rogers–Szegő family counterexample and does
not disprove the Q29 implication. Actual q-specific structure remains essential.

## 6. Boundary retained

No higher-layer multiple root, actual-family transfer certificate, or uniform
ordinary-discriminant nonvanishing theorem has been obtained. Hensel existence,
synthetic perturbations, old content-60 normalization, and fixed e=3 acceptance
cannot replace that missing actual-family control. All old precision and
primitive-component guards remain active. The only accepted proposed change
is the source-bound nonvanishing-gate correction above.

## 7. Final byte binding and independence limits

The final author report hash is recorded above. Its source-binding artifact is
q29_uniform_endpoint_20261016/SOURCE_BINDINGS.json, SHA256
bc48b53e77dcb7a336e1677d58d591ca5bee5cdbbb1bfe9066aeabc3cbf80bbb.
Its bounded-control receipt is q29_uniform_endpoint_20261016/BOUNDED_CONTROLS.json,
SHA256 534275dcb1eb7e6f216ea28174f6335a8979334c69942b3d54e098f7316ef7ef.
All three hashes were independently recomputed after reading the final report.

The author's eleven finite polynomial checks were read as an inert receipt,
not rerun and not used as a substitute for the independently checked universal
recurrence proof. No author or historical scientific program was executed.
The exact 4-by-4 counterexample was independently derived by the continuant
calculation displayed in Section 5. It is included solely as an adverse control
against a generic proof strategy, not attributed to the actual Q29 family.

Every reported source-binding digest was independently recomputed. Full F021
repository payloads were matched to their local source bytes. The four current
Q29 source texts were independently fetched at the immutable ref and matched
by SHA256. The source reconciliation and accepted bounded lemma do not alter
the completed fixed instance or the open parent.
