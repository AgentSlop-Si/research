# Exact centering obstruction between the accepted ALG-034 interfaces

18 October 2026 UTC. New bounded composition result, pending independent review.

## Result

The accepted restricted recovery and the accepted retained outer transfer do not have a nonzero exact source-centering overlap. This is a theorem about their actual targets, not merely a missing software wrapper.

Let the supplier dimension be M=2^28. For any outer dimension N with M the least power of two at least 4N, let J_N embed an N-vector in the consecutive centered residues j-floor((N-1)/2). If nonzero x has at most sixteen nonzero coordinates, the recovered target R_M x/alpha cannot equal U_M J_N u for any complex N-vector u and any nonzero alpha. In fact equality would require

    |supp(x)| >= M-N+1 >= 201326593.

The required support is therefore not just above sixteen; it is above three quarters of the supplier length. This remains true without dyadic, finite-width, normalization, or phase restrictions on u. Those restrictions cannot repair the obstruction.

The finite-value decoder can still be converted into the outer stage's numerical sparse-grid format. The resulting stage is a valid retained-operator calculation C Z, with its already accepted every-tape error theorem. That conversion cannot create the original-target centering identity. A fresh exact impulse calculation also shows that centering the sparse raw input first, then using the same supplier/recovery, does not solve this target mismatch.

This closes the proposed direct composition route at the stated interfaces. It does not close ALG-034, rule out a new centered-source provider, rule out a dense fallback, or invalidate the separately accepted all-length mathematical existence theorem. No historical program was executed and no external write was performed.

## 1. Frozen premises and notation

The inspected sources were restored read-only from AgentSlop-Si/research commit d1c6910aa9fc4ef861981358e8bf3e0c71585689, under math/finalized/2026-10-18-cycle-completions. SOURCE_BINDINGS.json records exact SHA-256 values checked against that release's MANIFEST.json. The authoritative scopes are the final outer and recovery reviews, their manuscripts, and REQUIRED_CLARIFICATIONS.md. The outer cost erratum remains mandatory. Pending-review labels inside historical author reports do not supersede the final reviews.

Use the negative unitary transform

    (U_L w)_k = L^(-1/2) sum_j w_j exp(-2 pi i j k/L),
    (R_L w)_k = w_(-k mod L).

Direct finite geometric summation gives U_L^2=R_L, U_L R_L=R_L U_L, and U_L^(-1) R_L=U_L. No sign or conjugation is suppressed.

The supplier's alpha is a scale, unrelated to the exponent named alpha in the inherited weak-coordinate approximation theorem. Here alpha>0 denotes only the supplier scale. The outer scale is written lambda=2^sigma_scale to distinguish it from the decoder's independently random odd multiplier sigma_hash.

## 2. Full original-input binding and target chain

The accepted supplier raw input is a nonzero sparse canonical Gaussian-dyadic vector of length M:

    x_j = c_j 2^(-F),  c_j in Z[i],
    E = sum_j |c_j|^2,
    h = ceil(log2(sqrt(E))), alpha=2^(h-F).

Thus normalized coefficients a_j=c_j/2^h satisfy 1/2<||a||_2<=1. The accepted family has at most sixteen raw support positions for the recovery theorem and at most 1024 bits per real or imaginary raw component. F has a bounded encoding, not a bounded numerical magnitude proportional to log M.

The state has B_A=M. Its balanced-block projection P is exactly the identity only in this singleton family. Therefore the exact source described by the supplier and consumed by the accepted bucket adapter is

    f = U_M x/alpha = U_M a.

The bucket decoder recovers the Fourier coefficients of f. Its mathematical target is

    z_rec = U_M f = R_M a = R_M x/alpha.

The source is f, not a and not an N-coordinate centered embedding by declaration. The raw support, modal descriptor, and evaluation controls remain outside the value-only decoder. Its accepted success event gives a sparse Z with

    ||Z-z_rec||_2 <= 9*2^-400,

and the stated genuine-location and per-returned-coefficient bounds, with probability at least 2033/2048 over an independently uniform odd sigma_hash. A success event is not an observed isolation certificate. No raw bytes, hash label, or median-row owner substitutes for the semantic target chain above.

The outer theorem has a different source chain. It receives a normalized u in C^N, defines v=J_N u, and needs estimates of

    z_outer = U_M v = U_M J_N u.

It transfers those estimates to U_N u and subsequently scales to U_N(lambda u). Its implemented full transfer does not receive u; that source-centering identity must be supplied by its caller. The retained matrix C is defined for this centered-source identity.

For direct composition to discharge that identity using z_rec, one must have

    R_M x/alpha = U_M J_N u.                    (A)

Applying U_M^(-1), which is invertible, shows that (A) is equivalent to

    U_M x/alpha = J_N u.                        (B)

Neither reflection of the returned index list nor relabeling the target removes (B). Reflecting Z changes its ideal target to a, not to U_M J_N u. An additional nontrivial Fourier computation or a different source provider would be new work.

## 3. Centered interval support forces a dense original

### Lemma: no s consecutive Fourier zeros

Let 0!=x in C^M have distinct support n_1,...,n_s, with s<=M. Its transform cannot vanish at s consecutive residues, including a cyclically wrapped run.

Proof. Put z_r=exp(-2 pi i n_r/M), which are nonzero and pairwise distinct. If (U_M x)_(j0+q)=0 for q=0,...,s-1, periodicity permits using the integer indices j0+q even across wrap. Then

    sum_r (x_(n_r) z_r^j0) z_r^q = 0,
    q=0,...,s-1.

The coefficient matrix is Vandermonde with determinant product_(r<t)(z_t-z_r), which is nonzero. Consequently every x_(n_r) z_r^j0=0, contradicting the support definition. This uses exact equality, not a numerical condition estimate. QED.

### Theorem: centered-source disjointness

The support of J_N u lies in one cyclic interval of N consecutive residues. Its complement contains M-N consecutive residues at which J_N u is exactly zero. If (B) holds and s<=M-N, the preceding lemma makes x zero. Hence every nonzero solution of (A) requires

    s >= M-N+1.                                (C)

For the admitted M=2^28, outer length compatibility is precisely

    2^25 < N <= 2^26.

Therefore (C) implies s>=2^28-2^26+1=201326593. The accepted s<=16 family has no nonzero solution. The supplier's larger standalone cap s<=64 also cannot help. Arbitrary complex centered coefficients, alternative normalization, and arbitrary nonzero scale do not change this conclusion.

Equivalent polynomial proof. If v=J_N u, write its support as b,...,b+N-1 modulo M. Then x=alpha U_M^(-1) v has values proportional to a nonzero degree-at-most-(N-1) polynomial evaluated at the M distinct roots of unity, times nonzero phases. Such a polynomial has at most N-1 roots, so x has at least M-N+1 nonzero values. This also shows why a generic sparse-support uncertainty inequality would be too weak: the obstruction uses the consecutive centered support interval.

The zero source is the only overlap at the present support cap. It belongs to the supplier's separate exact-zero outcome, outside the nonzero recovery theorem, and can be handled by a separately bound zero branch.

## 4. A quantitative counterexample to centering the raw sparse input first

One might attempt to start with an N-vector u, center it into a sparse raw vector, and use that vector as the supplier's original. This preserves sparsity but introduces a second transform rather than the single transform needed by the outer interface.

Take M=2^28, N=2^26, a0=floor((N-1)/2), and u=e_(a0). Its centered vector is J_N u=e_0. Feed the supplier raw x=e_0, F=0. Then E=1, h=0, alpha=1, and every hash multiplier is isolated because s=1. The accepted recovery approximates

    z_rec=e_0,

whereas the required centered Fourier target is

    z_outer=U_M e_0=2^-14 (1,...,1).

Even allowing the full accepted recovery error,

    |Z_0-(z_outer)_0| >= 1-2^-14-9*2^-400 > 1/32.

For the legal outer beta=1/4, its required success premise is

    ||Z-z_outer||_infinity <= 4 M^-beta ||u||_2 = 1/32.

Thus that premise fails although restricted recovery is successful. At the same time, dimensions, output grid P=464, D=5, t=4484<M, magnitude cap, and scale sigma_scale=0 are compatible. This isolates the semantic defect from those syntactic conditions. The claim is about the outer success premise, not a refutation of its possibly much looser final error bound or of the all-length existence theorem's separate front end. In particular, no assertion is made that the separate all-length E(beta) sparse-dispatch guards hold at this fixed length.

A stronger repair attempt is to choose the supplier's raw vector r so that its modal source equals J_N u. That uniquely requires r=alpha U_M^(-1)J_N u. For the impulse above, r is a nonzero constant vector with M occupied entries. More generally Section 3 forces at least M-N+1 occupied entries. This is outside the sparse-original deployment family and, for general u, need not be Gaussian dyadic at all.

## 5. What can be composed without claiming the missing identity

On every successfully returned decoder packet, the output has at most sixteen sorted distinct locations and grid P=464. For m=28 this is exactly the outer P=16m+16 grid.

The decoder's bucket numerator guard gives each absolute integer component less than 2^480. Its amplitude division uses a positive midpoint kappa>=1, followed by nearest-even integer rounding. Dividing an integer by a real factor at least one and nearest-even rounding cannot increase its absolute value past that original integer. Hence every returned numerator also has magnitude below 2^480. The outer cap is

    3 M^2 2^P = 3*2^520,

so the cap holds on every returned packet, including an inaccurate bad-isolation packet. This does not turn rejection paths into successful outputs.

Let K be the actual returned sorted support. Form one immutable estimate row from its actual returned P-grid coefficients, and run the existing actual median producer with R_rows=1. A single-row Cartesian median is exactly Z. After the outer's separately paid median replay, its numerical input grammar is satisfied. This is an explicitly proposed adapter contract, not an executed new integrated program. The original-context binding must still retain raw/state/sigma_hash independently and replay the entire 29-call recovery before comparing the result if full semantic replay is requested. Median replay alone rebinds only the supplied row.

The only valid combined conclusion is the accepted every-tape retained-operator result

    |Y_l - lambda (C Z)_l|
       <= lambda [eta sum_(k in I_l)|Z_k| + 2^-b].

The target C Z is well defined and may be useful, but is not automatically U_N of any original source. Even a full replay proves which original produced Z; it cannot prove the false identity (A).

An explicit actual-source residual can be included if a caller independently supplies u. Put z_true=U_M J_N u, R=||u||_2, and

    Delta=||z_rec-z_true||_infinity, epsilon_rec=||Z-z_rec||_infinity.

Then triangle inequality gives ||Z-z_true||_infinity<=Delta+epsilon_rec. With the inherited retained-row bound |C_lk|<3 and tail operator norm at most 12*4^-s_outer,

    ||lambda^-1 Y-U_N u||_infinity
      <= 3t(Delta+epsilon_rec)
         + t eta (R+Delta+epsilon_rec)
         + 12*4^-s_outer R + 2^-b.             (D)

The coefficient perturbation uses |(z_true)_k|<=R by unitarity. Equation (D) is an honest error decomposition with a separately specified u. It does not bound Delta from source binding or from the decoder's recovery theorem. The impulse example gives Delta=1-2^-14. Any claimed composition must either pay for and control this defect or supply a genuinely different centered-source measurement interface.

## 6. Complete accounting boundary

No all-length speed bound can be inferred by adding the two accepted packets. The recovery theorem is at the fixed M=2^28 only, while the all-length outer estimate has fixed-family asymptotic hypotheses. Merging their labels does not extend the recovery parameter family.

For the proposed numerical adapter only, let W_rec and A_rec be the full accepted recovery work and cumulative-storage receipts, including all five provider preparations, the 29 source executions, all 3,801,088 bucket writes, separately all 3,801,088 consumer reads, source/header handling, scalar windows, phase arithmetic, and outputs. Retain those receipts and their original input/state/hash tape. If semantic replay is required, add a second complete recovery W_rec' and A_rec', not just the row producer. Canonical comparison and retained source/context storage are additional.

Let S<=16, E_outer<=S ceil(Nt/M)<=St, and let H bound actual data/header/address widths, previous ledger-counter widths, and the bit length of the total previous and new event counts. A one-row conversion, its actual median production, median replay, and bounded canonical row comparison have O((S+1)H^2) binary work and O((S+1)H) produced/control bits, plus the actual retained upstream context size and its charged comparisons. This use of H retains the mandatory cost erratum. It is not an m-only bound for arbitrary histories.

For fixed D,beta,d and the actual bounded-width/history conditions of the accepted outer theorem, add the full outer work

    O_D((N+S+E_outer+1)m^2
         + 1_(E_outer>0)m^5 + E_outer m^5),

and its O(Nm+(S+1)H+m^2) peak bits in addition to the complete upstream live/retained state. The N initialization and N output writes are mandatory even for empty support. General original/context retention and the provider's live-array storage remain charged separately; cumulative storage is not peak memory. Caller serialization, repeated exports, and repeated validations are separately paid.

No execution of this entire adapter was performed. These are source-level compositional bounds for a specified adapter, not new receipts or finite measured evidence. Most importantly, no finite amount of paid replay repairs the false centering identity.

The supplier permits |F| as large as a 128-bit integer value. Alpha=2^(h-F) may therefore have an enormous exponent value. The current outer accepts only |sigma_scale|<=d m for fixed d. Passing alpha symbolically does not satisfy that contract; expanding its positive numerator shift has output cost proportional to its actual shift. A valid original-scale integration must restrict the family or explicitly extend and pay the output representation. The obstruction of Section 3 already holds at F=0, so this is a separate contract issue.

## 7. Exact remaining contract and stopping condition

To establish original-target outer transfer, provide an immutable independently retained original N-vector u0, a paid zero/normalization rule u0=lambda u, the actual centered source J_N u, and a measurement provider whose ideal finite bucket values are proved to measure that centered source. Establish the simultaneous recovery guarantee against U_M J_N u, its every-tape support/value bounds, and probability under actual stated independent randomness. Then combine its full receipts and any semantic replay with the already accepted outer stream. A generic original u0, a projected signal, and a first or second Fourier transform must carry different explicit targets.

This packet establishes a precise impossibility of using the accepted sparse-original supplier as that missing provider by identity-preserving rewrapping. It does not rule out a fresh general-source provider, a deliberately different projected target, or direct dense computation. Dense and arbitrary input handling belong to separate target-explicit work. ALG-034 stays open.

## 8. Fresh evidence and limitations

checks.py is newly authored self-contained standard-library code. It imports no preserved program. It verifies the target-transform identities and consecutive-row Vandermonde determinants exactly in small dyadic cyclotomic rings, checks independent large-parameter finite-field analogues, verifies the exact impulse inequality and interface bounds, and checks the source hashes. Finite-field controls are explicitly only analogues; the complex proof is Section 3. No floating-point tolerance, old execution, or prior test count is used as new evidence.

RESULTS.json records the complete fresh controls. Read the independent final review when one is available; this author's report itself does not supply independent acceptance.
