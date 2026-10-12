Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted. Source SHA-256: 204460f2bdb8bb07d597b5bfc9cfb944f20c796b9c2861499251558044cc169e.

Independent review of the SRCR Green volume obstruction
12 October 2026 UTC

Decision

ACCEPT the exact matched two-jump falsifier, the restricted fixed-state volume
obstruction, and the source-legal small-parameter escape with its local
absolute-perturbation witness. The author proof requires no mathematical
correction within those stated boundaries. The full positive joint macro
obligation SRCR::joint-macro, stable ID SRCR-20261011, remains OPEN.

This is an accepted bounded addendum to the existing SRCR research item. It
is not an accepted O(N log log N) Fourier algorithm, an impossibility theorem
for the full source grammar, or a new general Fourier lower-bound method.

Evidence and source integrity

The reviewed candidate is SRCR_Green_Volume_Obstruction_CANDIDATE_2026-10-12.zip,
SHA256 3b2782eb1bcc1892f86593e1b8dcec7807dea27b916c88ec741843d3347b41b2.
All 14 manifest-listed payload files match their recorded lengths and hashes;
the archive has exactly those files plus MANIFEST.json. All five declared
source bindings also match. The source manuscript has 11181 bytes and hash
096851f9be08ff96d6e8ca8a871fd3ceda6bf00f71216739a7bc9ab7ecec8f0f.

This review directly inspected the manuscript's HIGH definition, allowed
operations, macro identity, recursion and explicit accounting requirements.
The bundled earlier HIGH review and HR cost correction are preserved as
historical accepted context; they are not represented as freshly reproved.
A genuinely different uniform linear-overhead joint macro remains required. No original source or candidate file was changed.

Exact two-jump result

At N=64 the complete HIGH operator is T6 on q=16 coordinates. Let eta be a
primitive 64th root, omega=eta^4, U[k,k]=eta^(2k+1), V[a,a]=eta^(2a).
The entry expansion proves T6=U F16 V over Q(eta).

For r=1 and jumps 1,3, the candidate sets

  A = U L3 L1 U^(-1),
  B = V^(-1) D1^(-1) D3^(-1) V.

The printed source identity Ls F=F Ds gives, in the required order,

  A T6 B = U F D3 D1 D1^(-1) D3^(-1) V = T6.

This is an all-row algebraic identity. The independent program separately
assembles and multiplies all matrices over Q[X]/(X^32+1); all 256 entries
agree. Noncommutativity is real: (D1 D3-D3 D1)[0,14] equals
omega^(-7)-omega^(-5), which is nonzero. There are 30 nonzero commutator
entries in the exact control. Reversing the right inverse order changes
all 256 entries, so the check detects the ordering error rather than
accepting every nearby word.

The target F8 direct_sum F8 has entry [0,8]=0, whereas

  (A T6 B)[0,8] = eta^17 != 0.

All 256 entries of the surviving T6 are nonzero. Nonzero diagonal gauges
and arbitrary separate row/column permutations preserve that dense support;
they cannot create a direct sum with two nonempty blocks. The same matched
cancellation follows for any finite jump list, even when the factors do not
commute. It does not describe unmatched or cross-conductor constructions.

The finite N64 statement rejects the specified F8 direct_sum F8 target.
Since the source allows a fixed but unspecified child-size constant K,
this single finite example is not by itself a contradiction for every
permitted K. The unchanged largest block N/4 fails the required O(sqrt(N))
shrink uniformly as N grows, and no recurrence for this ansatz has been
established. That distinction remains essential to the accepted scope.

The volume calculation

Set h=ceil(t/2), R=2^h and L=t-h-2 for N=2^t. For HIGH, c ranges from
h+3 through t; every size q=2^(c-2) has t-c+1 separate copies. The unit-modulus
twists in Tc=U Fq V give |det Tc|=q^(q/2). Thus, with complete HIGH dimension
H and weighted gap W,

  H = sum_c (t-c+1)q = N-2R(L+2),
  W = sum_c (t-c+1)q(c-2-h) = (L-2)N+(2L+8)R,
  log2 |det G| = (hH+W)/2.

The closed forms apply to nonempty HIGH, L>=1. HIGH is empty exactly for
t<=5. The top c=t term gives W>=NL/4; summing q(c-2-h)<=qL gives W<=NL.
Consequently W=Theta(N log N). The proof is symbolic; finite checks are
implementation controls, not evidence for a universal asymptotic by themselves.

For residual dimension p and Fourier children summing to H-p with
n_nu<=KR, absorb all residuals and gauges into the paid nonrecursive
reconstruction. Then the required nonrecursive log-volume gain is exactly

  Delta = (hH+W)/2 - (1/2)sum_nu n_nu log2 n_nu
        >= W/2 + ph/2 - (H-p)log2 K/2
        >= W/2 - H log2 K/2.

At N64 with exact length-8 children, the log2 gap is 8. Independent
characteristic-zero elimination gives squared determinant moduli 16^16
and 8^16, with ratio 65536=2^16, confirming the modulus ratio 2^8.

Accepted theorem and exact limitations

The theorem applies only where every logical nonrecursive factor Mj is a
square invertible map on the same H-coordinate persistent signal state.
A factor may have charged local temporaries, but it may not retain extra
independent coordinates across factors and then discard them at readout.
All residual, gauge, inverse-chart, routing, preparation and output work
must be included. If wj is its paid work and

  max(0,log2 |det Mj|) <= C0 wj

for a constant C0 independent of N, determinant multiplicativity yields

  sum_j wj >= [W/2-H log2 K/2]/C0 = Omega(N log N)

for fixed K and C0>0. If C0=0 and the gap is positive, the factorization
cannot exist. Negative determinant gain cannot cancel this lower bound
on positive gain. The argument permits arbitrary order and cross-conductor
mixing within its square fixed-state model. It is stronger in schedule
coverage than the earlier particular radix-2 continuation count, while
remaining a restricted statement.

The listed primitive bounds are sound. Permutations and supported phase
diagonals have zero gain; a forward Haar pair has one bit of gain and
its normalized inverse has negative gain. For E charged sparse edges of
bounded modulus b, a row with ei edges has norm at most b ei, including
parallel edges. Hadamard and sum log2 ei<=sum ei imply positive gain at
most (1+log2 b)E. An inverse sparse route needs its own paid implementation.

No arbitrary cyclic-bidiagonal solver is automatically volume-bounded just
because its arithmetic count is linear. Invertible charts and fixed square
state are explicit theorem premises, not extra facts silently imposed on
the full manuscript. Arbitrary small denominators, unbounded gauges,
non-volume-bounded residuals, enlarged persistent state and arbitrary
readout remain outside this theorem.

This is the classical determinant/volume method associated with Jacques
Morgenstern. The publisher record for Note on a Lower Bound on the Linear
Complexity of the Fast Fourier Transform, JACM 20(2), 305-306 (1973), was
independently located: https://doi.org/10.1145/321752.321761 . Its abstract
and bibliographic data were available; this review does not claim access
to its full proof. Ailon's primary account independently confirms the
method's bounded-constant and scaling limits:
https://arxiv.org/abs/1403.1307 . No stronger theorem from that work is
imported. The elementary determinant argument above is sufficient here.

The source Green maps and legal inverses

For the printed Ds, only the diagonal permutation and full cyclic
subdiagonal permutation can contribute to its determinant. The diagonal
product vanishes because its j=0 entry is zero. The cyclic sign leaves

  det Ds = -r^q omega^(s q(q-1)/2).

Conjugacy gives the same determinant for Ls. Both are invertible whenever
r!=0, with determinant modulus |r|^q. For direct or inverse source Green
factors the positive gain is bounded by q |log2 |r||. This gives the
claimed uniform per-coordinate volume bound when |r| is uniformly above
zero and below infinity. It says nothing comparable about condition
number; determinant modulus one does not control inverse norm.

The four zero anchors are a=0,m,2m,3m, where m=q/4. Each determines
x[a-1] from b[a], then its m-1 predecessor equations determine the rest
of the chain. Only r and nonzero root powers are inverted. Independent
Gaussian inversion agrees with all 28 basis columns for q=4,8,16 at
r=1/q. Three r=0 controls correctly reject the inverse.

The actual prepared solver uses 2q-4 signal multiplications and q
subtractions/negations. Preparing reciprocal phase coefficients costs
q multiplications and one inversion of r; preparing 1-omega^(4j) costs
q subtractions. An available root table supports all phases. Storage,
input/output and address traffic are O(q), with q required output writes.
These are unit-cost scalar counts; coefficient-vector arithmetic inside
the verifier is not substituted for that model.

For the two-jump charts, the candidate's prepared literal counts are
correct: A costs 4q multiplications and 4q subtractions; B costs 6q-8
multiplications and 2q subtractions; B^(-1) costs 6q multiplications and
2q subtractions. Roots, coefficient preparation and traffic are extra.
These are valid unpruned schedule counts, not minimum counts in special
cases with zero/unit coefficients.

A^(-1) is not supplied by the O(q) Ds solve. The displayed available
implementation U Fq D1^(-1) D3^(-1) Fq^(-1) U^(-1) costs two paid
q-transforms plus O(q), including inverse-transform normalization.
With supported inverse-root routing this is 2 C_F(q)+O(q), not O(q).
A different fast direct L inverse remains an unproved alternative.

The small parameter escape

For b=e_m, back substitution and
prod_(j=1)^(m-1)(1-omega^(4j))=m prove exactly

  (Ds^(-1))[0,m] = -m r^(-m) omega^(-s m(m-1)/2).

The source imposes no lower bound on |r|. Choose r=1/q: q is formed
from 1 using log2 q doublings and inverted once. No unsupported root
or externally supplied dense constant is required. The same anchored
solver therefore has O(q) exact scalar work but

  log2 |det Ds^(-1)| = q log2 q,
  |(Ds^(-1))[0,m]| = m q^m.

This is a concrete source-legal obstruction to extending the bounded-volume
premise to all O(q) solves. It is not a construction of the required
cross-conductor normal form. The independent small-r tests use the actual
r=1/q, not only a nearby fixed constant such as 1/2.

Local absolute precision versus representation

For an independently perturbed chart input b+delta e_m, exact linearity
gives selected output error magnitude m |r|^(-m)|delta|. To guarantee
that output error is at most 2^(-b) for every such perturbation with
|delta|<=2^(-p), the necessary bound is

  p >= b + log2 m + m log2(1/|r|).

For r=1/q, let g=log2 m+m log2 q. The phase-separated coefficient is
an integer of exactly g+1 ordinary binary digits, and the local absolute
input accuracy requires g guard bits. Both statements are accepted.
At q=16 this gives g=18 and 19 integer digits; at q=256, g=518 and
519 integer digits. A q=32, s=5 exact perturbation test independently
checks the full phase and the error response on a dense rational input.

Crucially m q^m is itself a power of two. Its magnitude can have a one-bit
normalized mantissa and an exponent encoded in O(log q) bits; the phase
can also be retained symbolically. The ordinary integer bit length does
not force a Theta(q log q)-bit floating mantissa or universal bit-cost
lower bound. Conversely, compact exponent encoding does not erase the
stated absolute-input perturbation amplification. That precision claim
is local to a separately materialized chart with independently perturbed
inputs, not a theorem for every fused/correlated implementation or every
relative-error model. No numerical-stability conclusion about a complete
SRCR transform is certified.

Recurrence and remaining positive gate

Root preparation, both chart directions actually needed, gauges, residuals,
routing, readout, principal work, LOW copies, Haar analysis and synthesis
must all be paid. From supplied 1 and a primitive Nth root, one full table
requires N-2 multiplications for N>=2. Reusing a warm plan must not erase
its cold generation from a cold-cost claim. The principal block's required
linear budget remains part of the full construction obligation.

Only if all nonrecursive work is uniformly O(N), total recursive dimension
including every LOW and HIGH child is at most N, and maximum child size
is at most K sqrt(N), does the source's O(N log log N) unit-cost recurrence
follow. Neither the matched cancellation nor the escape solve supplies
those premises. A new construction still needs legal root/inverse paths,
all-row normal-form identities, paid residual and explicit readout, complete
costs and a representation/error model when claiming bit or precision bounds.
A volume ledger is a necessary diagnostic, never a sufficient certificate.

Fresh independent controls and replay

The new reviewer program uses dense rational coefficient vectors and
recursive dyadic-norm field inversion, rather than the candidate's sparse
representation and polynomial extended Euclid. It performs independent
matrix elimination, full matrix products, and instrumented backward solves.
No program inside source_inert was imported or executed.

The fresh run passes 56 Green cases, 6656 source conjugacy matrix entries,
112 independently eliminated Green determinants, 112 source solver vectors,
28 inverse basis columns, and 1025 complete mass/boundary identities.
It also passes all 256 N64 entries, a 30-entry noncommutativity control,
256 wrong-inverse-order discrepancies, the exact off-block falsifier,
the exact determinant ratio, three singular-parameter rejection controls,
a q32 dense-input local-perturbation control, and coefficient/exponent
records through q=4096. These finite controls supplement the all-size proof.

The identical new reviewer program was copied into a separate cold directory
with no candidate files and rerun. COLD_REPLAY.json binds its code and the
byte-identical result/log hashes. A package manifest and verifier bind this
verdict and every evidence file. The original candidate remains inert and
unchanged. This is a new independent replay, not a claim that every
historical program or predecessor theorem has been rerun.

Scope and remaining work

The full SRCR joint macro remains open. Accepted bounded results are:
matched noncommuting Green words are stabilizers; a fixed-H square-state
macro with uniformly bounded volume gain per charged operation needs
Omega(N log N) nonrecursive work; the source-legal r=1/q escape prevents
generalizing this to all source operations. State the precision witness
as local absolute perturbation amplification with a compact-exponent caveat.

Preserve the earlier accepted N64 HIGH classical witness and its
schedule-specific obstruction, including HR rather than H(R-1) direct
reference additions. The full positive macro remains open. This theorem is not a general impossibility,
and sufficient determinant gain alone does not prove a transform identity.
