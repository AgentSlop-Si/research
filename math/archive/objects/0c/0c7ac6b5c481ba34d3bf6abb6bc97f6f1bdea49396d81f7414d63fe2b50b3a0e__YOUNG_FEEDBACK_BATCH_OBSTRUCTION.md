# Young-feedback batching: a bounded-coefficient component obstruction

## Result

The requested young-age batch already costs **Omega(N n)** in the unit-phase/binary-addition complex model when it must accept arbitrary retained coefficient vectors and expose its exact outputs. This is a component lower bound, stronger than the independent-trajectory visit count for this particular interface. It follows from an explicit, orthogonal bank of rectangular Fourier packets, not from assuming that every active trajectory coordinate must be visited.

The crucial distinctions are:

- The routed output width at age t is much smaller than the active trajectory width e_t. The proof uses the smaller width exactly.
- Young ages have disjoint routed output supports. Thus the apparently summed temporal batch is a fixed permutation of independently observable packet-bank outputs.
- Each packet bank has sufficiently large rectangular volume to cost Omega(r L), despite having fewer than r output rows.
- This proves neither an unrestricted arithmetic lower bound nor a finite-field lower bound. It does not apply automatically to a fused source/solve computation whose retained jets are constrained by the original N inputs.

There is therefore no sub-Nn implementation of this exact arbitrary-jet component that merely fuses/reorders its existing bounded-coefficient complex linear gates. A next viable constructive interface must change the gate model or avoid materializing this arbitrary-jet packet bank. No faster finite-field construction is claimed here.

## 1. Scope, notation, and input/output accounting

Use the accepted marker-cut definitions:

    N = 2^n, d = n-b, r = 2^d, eta = omega^(2^b),
    L = 2^(b-1), kappa = max(0,d+1-b),
    g_k = sum_(t=1)^L C_t Q_r^t u_(k-b-t), 0 <= k <= n.

Here omega is a primitive complex Nth root, each u_j is an arbitrary r-vector, and out-of-range coefficients are zero. Assume

    b >= 7,  L+b <= d.                                      (1)

Then L <= kappa, and these conditions hold for all sufficiently large n at the accepted marker choice b=floor(log2(n/(4 ln n))). Small parameters are covered by the exact identities below, but are not needed for the asymptotic bound.

The input is the entire array (u_0,...,u_n), with r(n+1) independent complex entries. Writing the entire dense g array and reading the input cost O(r(n+1)); a sparse representation of the structurally nonzero outputs is also allowed. The lower bound uses only existing output coordinates, so it applies to either convention. Output entries are actual field values, not unevaluated expressions or a newly defined encoding.

The allowed input-dependent operations are copies/permutations, binary addition/subtraction, and multiplication by constants of modulus at most one. Equivalently, a two-parent linear gate with both coefficients of modulus at most one increases the determinant potential by at most two. Input-independent setup may be given for free: this only makes the lower bound stronger. Arbitrary precision is allowed, so this is not a precision or bit-complexity argument. Unbounded scalar multipliers, nonlinear arithmetic, data-dependent encoding/branching, and packed word operations are outside this model.

## 2. Exact routed rows, including all phases and merges

Let K_t be the set of t-bit words k that start and end with 1 and avoid 0^b. Let

    f_t(k) = rev_t(k),  R_t = 2^(d-b-t).

For each q in [0,R_t) and k in K_t, the output index of C_t Q_r^t is

    i(t,q,k) = 2^(b+t) q + k.                               (2)

There is no wrap in (2) under (1). The exact value is

    (C_t Q_r^t u)_(i(t,q,k))
      = omega^gamma(k)
          sum_(j congruent q mod R_t) eta^(j f_t(k)) u_j.    (3)

All other coordinates are zero. The sum in (3) contains exactly 2^(b+t) entries.

To derive (3), a length-t path from source j in Q_r has destination a=2^t j+k modulo r and weight eta^(j rev_t(k)+gamma(k)). The C_t phase changes eta^gamma(k) to omega^gamma(k), and its route is 2^b(a-k)+k modulo r. This route fixes k and retains j modulo R_t. Therefore it merges exactly the source terms in (3), including every one of the 2^b coordinate merges after Q_r^t. No cancellation or merge is treated as free in an implementation.

The number of rows at age t is

    m_t = R_t |K_t|,
    |K_1| = 1,
    |K_t| = a_b(t-2) for t >= 2.                            (4)

This is generally **not** e_t. In fact, for moderate young t, m_t is approximately r/2^(b+2), whereas e_t is approximately r/2.

## 3. Disjoint output supports and the temporal permutation

Regard i(t,q,k) as a fixed-length d-bit word. Immediately before its low t-bit suffix k there are b zero bits. The suffix k avoids 0^b and begins with 1. Hence the rightmost completed marker in i has exactly age t. Its ending bit is 1 because k ends with 1.

Consequently the supports S_t={i(t,q,k)} are pairwise disjoint for t<=L. This argument includes leading zero bits of the fixed-length index; it does not assume q is nonzero.

For i in S_t, there is exactly one potentially contributing age in the batch, so

    (g_(j+b+t))_i = (C_t Q_r^t u_j)_i.                     (5)

Let

    J = n-b-L+1.

Every input vector u_j with 0<=j<J exposes all ages 1,...,L among the requested outputs. Thus selecting and reordering the batch outputs reveals J independent copies of the same packet bank B formed by stacking all rows in (3). No temporal convolution algorithm can merge these scalar outputs without still producing their individual values at this interface.

## 4. Pairwise orthogonality of the input rows

Every row beta_(t,q,k) of B has exactly 2^(b+t) entries, all of modulus one. Therefore

    ||beta_(t,q,k)||_2^2 = 2^(b+t).                         (6)

The rows are pairwise orthogonal over the complex numbers.

For equal t, different q have disjoint supports. For equal t,q but different k, the inner product is a complete geometric sum over 2^(b+t) terms, with distinct frequencies f_t(k) in [0,2^t), and is zero.

For t<t', supports can meet only if q is congruent to q' modulo R_t'. Their intersection is then the entire smaller support j congruent to q modulo R_t. Apart from an irrelevant unit phase, the inner product is

    sum_(ell=0)^(2^(b+t)-1)
          exp(2 pi i ell (f_t(k)-f_t'(k')) / 2^(b+t)),       (7)

where replacing the chosen primitive root by any other primitive root has the same zero criterion. It vanishes unless

    f_t'(k') congruent to f_t(k) modulo 2^(b+t).            (8)

If t'<t+b, (8) is impossible: f_t'(k') has its highest bit t'-1 set, since k' ends with 1, while f_t(k)<2^t. If t'>=t+b, (8) says that the first t bits of k' equal k and its next b bits are all zero. This places the forbidden marker 0^b inside k'. This is also impossible. The borderline t'=t+b is included and would additionally conflict with the final 1.

The omega^gamma phases in (3) multiply rows by unit constants, so they do not change orthogonality or norms. This proves the exact Gram identity

    B B* = diag(2^(b+t), repeated m_t times).               (9)

The forbidden-word condition is essential. If it is removed, (8) can hold and both the cross-age orthogonality and the disjoint routed supports can fail.

## 5. Rectangular volume, with all input coordinates retained

Put m=sum_t m_t. Equation (9) gives

    det(B B*) = 2^S,
    S = sum_(t=1)^L (b+t) m_t.                             (10)

In particular m<=r. Cauchy–Binet gives

    sum_(I subset [r], |I|=m) |det B_I|^2 = 2^S.

Therefore some m-column minor satisfies

    log2 |det B_I| >= S/2 - (1/2) log2 binom(r,m).          (11)

To use the ordinary full-dimensional determinant potential, append the original input-coordinate rows e_j for j outside I to these m output rows. The resulting r-by-r determinant has modulus exactly |det B_I|. This step does not discard, summarize, or provide any input for free: every original coordinate is already an initial linear form, and all r input dimensions remain present.

For J independently supplied u_j blocks, select the corresponding minor in each block, append their complementary input coordinates, and append the untouched coordinates of every other input vector. The full r(n+1)-dimensional determinant has modulus |det B_I|^J. Permuting the output rows according to (5) affects only its sign.

The maximal absolute determinant among full-dimensional selections of computed coefficient rows starts at 1. A unit-bounded scalar multiplication cannot increase it, and a binary addition increases it by at most a factor 2, by linearity in the new row. Thus the number A of paid binary additions obeys the explicit bound

    A >= J [ S/2 - (1/2) log2 binom(r,m) ].                 (12)

This proof allows every original input coordinate to remain available, even if an actual implementation overwrites or discards it. The lower-bound potential is conceptual and does not impose a storage convention.

## 6. Young-age asymptotics

For t>=2, a union bound on occurrences of 0^b in a uniformly random (t-2)-bit word yields

    a_b(t-2) >= 2^(t-2) [1 - (t-2)/2^b]
               >= 2^(t-3),  for 2<=t<=L.

Combining this with (4) and 2^b=2L gives

    m_t >= r/2^(b+3) = r/(16L), 2<=t<=L.                 (13)

Consequently, for L>=2,

    S/2 >= r/(32L) sum_(t=2)^L t >= r L/64.              (14)

Using binom(r,m)<=2^r in (12), and L>=64 from b>=7, gives

    A >= J (r L/64-r/2) >= J r L/128
      = J N/256.                                         (15)

At the accepted marker choice, L=o(n), b=o(n), and J=(1-o(1))n. Hence the exact arbitrary-jet young-feedback batch requires Omega(Nn) additions in this model. This matches the order of the displayed independent-trajectory schedule for this component. The proof does not rely on counting its intermediate coordinate visits.

Allowing arbitrary scalar constants bounded by a fixed K>1 changes only a constant in a total-gate lower bound: each gate increases the potential by at most max(2,K). A growing bound K_N must be accounted for explicitly and does not give the same theorem. No bound on intermediate numerical magnitudes was assumed.

## 7. Matching paid upper bound and causal execution

A simple matching-order implementation makes the cost comparison independent of any claim that the original executor is optimal by inspection. Prepare the N consecutive omega powers, the r eta powers, and the gamma/phase tables by binary-parent recurrences, in O(N+n) field/address operations and O(N) words. A primitive root is supplied in the accepted field-operation model; the lower bound granted all such setup for free. No per-edge exponentiation is needed. Membership of the low t-bit word is tested in O(1) after O(r) integer-table preparation for bit length and longest zero run.

Initialize the r(n+1) output slots and read all r(n+1) inputs. For each coefficient j, copy u_j into an r-word scratch vector. For t=1,...,min(L,n-b-j), apply the two-edge Q_r step to that vector, then implement C_t by scanning its r entries, testing k=a mod 2^t, multiplying by omega^gamma(k) eta^(-gamma(k)), and adding at index 2^b(a-k)+k modulo r in g_(j+b+t). Every scan, scratch initialization, phase multiplication, route, and merge is paid. The resulting totals are

    work = O(N+n+r(n+1)+r n L) = O(Nn),
    storage = O(N+r(n+1)) words.                           (16)

This is an upper bound using full r-vector steps; pruning can reduce constants but is not needed. Input and output use O(log N)-bit addresses and the accepted unit-cost address model. The scan never treats a whole polynomial multiplication or a many-input sum as one operation.

For causal use, run the same work as soon as u_j=(v_j)_R is finalized and add directly into the future residual slot j+b+t. All destinations are strictly later than j. Thus this upper bound composes with the accepted causal solve, with its direct retained-edge and other feedback/recovery work still separately charged. Its order matches (15) for this explicit arbitrary-jet young-feedback interface. No cheaper causal implementation is supplied.

## 8. Causal limitation and the next viable interface

The lower bound already holds for an offline batch with every u_j known in advance. An online or causal schedule that must expose the same g values cannot evade it. A divide-and-conquer convolution schedule, delayed updates, shared trajectory cache, or causal packet routing using the same bounded gates therefore cannot make this exact arbitrary-jet component sub-Nn.

This does **not** alone establish an Omega(Nn) bound for every implementation of the retained inverse. The inverse might never expose the selected packet outputs separately, and its inputs are f rather than u. More importantly, source-generated jets depend on only N original input coordinates, while the arbitrary-jet interface here exposes J r independent input coordinates, approximately N ln n at the accepted marker choice. Substituting constrained jets into this component theorem without proving the required rank/volume property would be invalid.

There are three precise ways to pose a next constructive attempt:

1. **Constrained and fused source/solve interface.** Accept the original N-vector x and produce retained/recovery outputs without materializing the arbitrary-jet bank. Its exact identities must exhibit the constraint exploited and pay for the constraint representation, forcing, causal composition, and final recovery. This leaves the present component obstruction, but a complete sub-Nn unnormalized complex transform still faces the already accepted full-transform bounded-coefficient determinant bound.
2. **Explicitly changed complex gate model.** Specify input-dependent unbounded scalar multipliers or nonlinear/encoding operations, their constants and representation, their manufacture and application costs, and a complete causal implementation. If a circuit uses U input-dependent multiplications by constants c with |c|>1, the same potential proof requires A+sum log2|c| >= the right side of (12); this is a necessary budget, not an algorithm or a sufficiency result. Merely producing constants in setup does not apply them to input data for free.
3. **Finite-field-only construction.** Supply a concrete field family and primitive roots, specify the representation and setup, then give an actual batched circuit with causal composition. For a prime field, N must divide p-1. For GF(p^s), N must divide p^s-1 and the s-coordinate representation, modulus construction, root provision, and extension-operation cost must be paid in the chosen base-field/bit/word model. The complex absolute-value volume proof does not transfer to finite fields. Existence of an extension by itself is not a costed construction.

No construction satisfying any of these replacement obligations is supplied in this package. The accepted output is the scoped structural obstruction and a precise remaining interface, not a faster FFT or a finite-field impossibility theorem.

## 9. Verification and provenance

The constructor and independent audit reports were read; their seal manifests were verified without changing any predecessor file. No constructor, predecessor, or uploaded executable was imported or run. The new verifier in this directory is standalone Python using only the standard library. It independently checks:

- The closed routed row formula against explicit Q_r propagation and phase/routing merges.
- The same rows against full-N weighted propagation with all retained states killed between steps, so changed-cut first returns are checked independently.
- Disjoint routed supports, exact support cardinalities, and pairwise reciprocal-root Gram products in finite fields.
- The full arbitrary-coefficient time-shifted batch against the independently propagated implementation.
- Exact avoiding-word counts and the numerical inequalities used by the all-size proof.
- A negative control: admitting a word containing the forbidden marker destroys both orthogonality and age-disjoint support.

All controls passed in 46 parameter/field cases in GF(65537) and GF(998244353), including exact-order checks of every supplied root. They cover 1,192 routed rows, 45,116 reciprocal-root row pairings, 260 full-N first-return input vectors including 168 basis vectors, 88,304 arbitrary-jet batch output coordinates, and 4,083 symbolic count inequalities through b=12 and L=2048. The forbidden-word negative control gives a nonzero pairing, as required. The deterministic run was repeated and its log matched byte for byte.

Finite-field equality checks validate algebraic identities and indexing; they do not establish the complex lower bound. The all-size proofs are Sections 2–6. Dense arrays, direct sums, and modular exponentiation in the verifier are finite oracles, not a claimed production-cost implementation.

`YOUNG_FEEDBACK_SHA256SUMS.txt` seals this report, the new verifier, deterministic controls and replay logs, and read-only source seal records. The source reports are:

- `marker_cut_audit_0241/INDEPENDENT_MARKER_CUT_AUDIT.md`
- `marker_cut_compression_0229/EXACT_MARKER_CUT_COMPRESSION.md`

Their exact hashes are recorded in `READONLY_SOURCE_HASHES.txt`.
