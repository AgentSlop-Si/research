# Phase-separated response tables for the packed approximate Fourier executor

10 October 2026. A new construction relative to the frozen backend, for independent review.

## Result and scope

Keep the accepted finite-word input contract, state encoding, precision, dyadic coefficient certificates, radix-2 layout, packing parameter, and fallback. Replace a table that combines a phase-dependent multiplication and a phase-independent addition by two tables, with one additional rounding of the multiplication result.

Put R = 2^b, S = R^P, Q = 2^g, and d = log2(P), using the frozen parameters below. The frozen packed response tables have

    E_old = (Q-1) S^2 + d S

one-word entries. The new packed response tables have exactly

    E_pack = S^2 + (Q-1+d) S.

The explicit scalar helper tables add QR + R^2 one-word entries. Thus, even charging these helpers rather than silently treating them as oracles,

    E_new = S^2 + (Q-1+d) S + QR + R^2.

The same cold O_c(N(t+log log N)) work and O_c(N) space theorem follows on the same growing-word RAM. The all-input relative-l2 guarantee remains 2^-t; the output lattice is unchanged. The principal preparation bound improves from the frozen construction's conservative N^(17/128) poly(log N) bound to O(N^(1/8) + Q poly(log N)) with the identical packing choice. This is a preparation/memory improvement, not a better asymptotic transform-time bound.

The large-stage update now uses two lookups instead of one. No empirical speedup, practical crossover, exact arbitrary-complex FFT, or historical novelty is claimed. The additional rounding means this is a new approximate executor, **not** a bitwise-equivalent rearrangement of the old executor. A fresh exact counterexample control checks that distinction.

## 1. Frozen inputs and parameter contract

Read-only mathematical sources:

- `packed_fft_candidate_1355/executor_derivation/DYADIC_PACKED_THEOREM.md`, SHA256 `bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`.
- `packed_fft_candidate_1355/all_length_extension/CONDITIONAL_ALL_LENGTH_THEOREM.md`, SHA256 `71d85d704058bd245d14ce5aad65f747cb1a5b038e69510b21b41d3c8a217927`.
- `packed_fft_candidate_1355/practical_scope/PACKED_RUNTIME_SCOPE.md`, SHA256 `7fcf4f7e8d9fbf2e390c242812ebe4ceb3a72be69e2bfa14373ebf3c5225ce2f`.
- `packed_fft_prior_art_1400/PRIOR_ART_AUDIT.md`, SHA256 `8072ddf16f23d542bf6610c704b66246e4d1963fa790072950c2a18ce0ab827d`.

For N=2^v and 2<=t<=v+1, use

    p=t+10+ceil(log2(v+1)),   u=2^-p,
    e_min=-v-p,              e_max=v+4,
    tau=u/N,                E=2v+p+5,
    k=ceil(log2(E+1)),       b=2(p+k+1),
    g=p+10,                 Q=2^g.

A real code has one sign bit, k exponent bits and p fraction bits; a complex code has b bits. Invalid exponent fields decode to zero. The total componentwise quantizer q truncates toward zero, underflows below tau to zero, and clips at the largest finite value below 32N. It returns a canonical code. In particular, for **every** argument, including clipping cases,

    ||q(z)||_2 <= ||z||_2.                                     (1)

When there is no upper clipping, on m complex coordinates,

    ||q(z)-z||_2 <= u||z||_2 + sqrt(2m) tau.                    (2)

Normalization chooses a=x/R_scale with maximum real/imaginary component in [1/2,1), so 1/2<=||a||<=sqrt(2N). Zero input is exact.

The certified coefficients remain those of the frozen proof. If omega is the exact phase assigned to a butterfly, its selected c satisfies

    |c-omega| < delta := u/128,
    |s_hat - 1/sqrt(2)| <= u/1024.

Hence the scaled Hadamard operator H_hat(a,b)=s_hat(a+b,a-b) satisfies

    ||H_hat|| <= 1+u/512,      ||H_hat-H|| < u/512.             (3)

These deliberately loose bounds use sqrt(2)<2. All coefficients are dyadics with O(p) fractional bits. The coefficient grid and catalogue are not eliminated.

Retain the original guard b<=v/64 and choose the largest power of two P with 2bP<=v/8. Thus P>=4, P>v/(32b), and packed values, responses and keys fit inside a model word. Retaining this guard isolates the construction change; it makes no claim that the old constants were necessary or optimal.

## 2. Factorization and complete table definitions

Define the total scalar tables, including responses on every malformed input code:

    F[q,z] = encode(q(c_q * decode(z)))               [Q R entries]
    H[a,z] = encode_pair(q(H_hat(decode(a),decode(z))))
                                                     [R^2 entries]

Here `q` in `F[q,z]` is an integer phase index; the quantizer q is distinguished by its argument. `encode_pair` puts the first b-bit output below the second. Each F entry occupies one word; each H entry occupies one word, even though it contains two states.

For every frozen phase pattern id, define a unary packed table

    M_id[W] = pack_l(F[phase(id,l), lane_l(W)]),        [S entries]

and one phase-independent packed Hadamard table

    HP[A | (B << bP)] = pack_pair_l(H[lane_l(A),lane_l(B)]).
                                                     [S^2 entries]

All first outputs occupy the low bP bits and all second outputs the high bP bits. There are still exactly Q-1 phase patterns. Their existing arithmetic IDs remain valid:

    pattern(s,h)[l]=floor(Q(Ph+l)/(P 2^s)),
    id=2^(s-1)-1+h,   1<=s<=g,   0<=h<2^(s-1).

At stage ell>d, put r=ell-d, s=min(r,g), and h=a>>max(r-g,0), where a is the first-half word position. The frozen catalogue identity proves this is the correct phase in every lane, including r>g, where all phases within the word are equal.

Replace each old large-span update by:

    id = stage_base + (a >> stage_shift)
    B1 = M[(id << bP) + W[block+a+half]]
    Z  = HP[W[block+a] | (B1 << bP)]
    W[block+a]      = Z & ((1<<bP)-1)
    W[block+a+half] = Z >> bP

This uses two lookups and O(1) ordinary instructions per pair. There is no per-lane online work or implicit permutation.

For small stages ell<=d, retain one S-entry stage table TS_ell, but define each of its disjoint butterfly responses by the **new** map

    (a,b) -> q(H_hat(a, q(c_q*b))).                            (4)

Thus all stages implement the same extra-rounding convention. Small-stage phase indices and output lane positions are determined by literal DIT within the word. One lookup updates each word. Online work remains O(N+Nv/P)=O(Nb), including initial bit reversal, quantization, and final scalar output.

## 3. A charged Cartesian-table construction lemma

### Lemma

Suppose m independent groups each have a digit in [0,D), where D>=2 is a power of two. The input fields partition the m*log2(D) key bits, so all D^m keys are represented without gaps or overlaps. Changing one digit changes at most a fixed number of input and output bit fields, and its response is evaluable in O(1) charged RAM operations from explicitly available scalar tables. Distinct groups have disjoint output fields. All combined keys and responses fit in a fixed number of words. Then the complete D^m response table can be constructed in

    O(m + D^m) RAM operations

using O(m) scratch words beyond the input scalar tables and output array. Field placements may be interleaved or separated; they need not be adjacent to each other.

### Proof and operation accounting

Prepare the field masks, offsets and fixed per-group parameters in O(m) instructions. Initialize the zero digit tuple, its full key, and its response in O(m) operations. Enumerate all tuples with an ordinary radix-D odometer, with digit zero changing fastest. On changing digit i:

1. update the stored digit;
2. clear and insert its input field(s) in the maintained key, using masks, shifts, AND and OR;
3. evaluate its local response using the charged scalar-table accesses;
4. clear and insert its output field(s) in the maintained response.

Store the maintained response at the maintained key after each increment. This explicitly performs the permutation between interleaved tuple order and the table's actual key order; it is not a free bit-transpose.

Over D^m-1 increments, the total number of digit changes, including reset-to-zero changes on a carry, is

    sum_{i=0}^{m-1} floor((D^m-1)/D^i)
      < D^m D/(D-1) <= 2 D^m.                               (5)

Every changed digit costs a fixed number of instructions, and every output entry is written once. Allocation, loop tests, table reads, and the preparation-budget counter add only fixed factors. The initialization and scratch costs are as stated.

### Application

- For each M_id, m=P, D=R. The local map is F at that lane's fixed phase. Initial phase indices and masks cost O(P) per pattern.
- For HP, m=P, D=R^2. A digit contains one lane from each input half. Its two input fields are at offsets bl and b(P+l); its two output fields have the same separated pattern. One scalar H lookup supplies both outputs.
- For TS_ell, m=P/2, D=R^2. A digit is the pair of lanes joined by that stage's butterfly. Its response is obtained by one F and one H lookup. Fixed stage phases and separated input/output field placements cost O(P) initially.

Consequently packed-table expansion costs O(E_pack+(Q+d)P)=O(E_pack), since S=R^P>=P. The R^2 Hadamard helper and QR unary helpers are fully charged separately.

This lemma also accelerates the old direct table construction if its scalar phase-dependent pair tables are supplied. It is a generic table-construction observation, not an exclusive feature or novelty claim for the new factorization. The actual memory reduction above comes from separating the phase-dependent unary map from the universal pair map.

## 4. Constant-word scalar preparation, not a hidden arithmetic oracle

Build the original bit-length chunk table first: h=max(1,floor(v/8)), with O(2^h) work and words. The low-precision guard makes p=O(v). Every decoded state lies on the common lattice 2^(-v-2p) Z[i], has bounded magnitude below 32N, and has a numerator of O(v+p) bits. Multiplication by c_q or s_hat increases the common denominator exponent by O(p), and complex addition contributes at most constant extra guard bits. Thus all scalar F/H intermediates have O(v+p)=O(v) bits, including unreachable but valid finite input states.

With the frozen sufficiently large fixed C(c), each such integer fits a fixed number of C(c)(v+1)-bit words. A fixed number of word additions, multiplications, shifts, divisions and comparisons implements decoding, exact dyadic evaluation, truncation, clipping and encoding. The chunk table finds the leading bit in O(1) word operations. Even multiplication of a fixed number of words can be implemented by a fixed-size schoolbook routine; no arbitrary-precision multiplication is treated as one instruction.

It follows that the scalar helper preparation takes O(QR+R^2) charged operations. Its allocation and every write are counted. The initial certified Q coefficients and s_hat are still constructed by the frozen polynomial-time rational routine, with all multiword certificate arithmetic and scratch allocations charged. Its cost is Q poly(v+p), not O(Q) by fiat.

Together with the Cartesian lemma and coefficient storage, total unbudgeted cold preparation is

    O(E_new + 2^h + Q poly(v+p)).                             (6)

Scratch is O(P)+poly(v+p), in addition to those explicitly counted arrays. There is no P or polynomial factor multiplying every large response-table entry in (6).

In the low-b regime,

    S^2 <= 2^(v/8),
    QS <= 2^(9v/128+10),
    QR <= 2^(3v/128+10),
    R^2 <= 2^(v/32),
    dS <= O(log(v)) 2^(v/16),
    Q <= 2^(v/128+10).

The lower-exponent terms are O(2^(v/8)); hence (6) is

    O(2^(v/8) + 2^(v/128) poly(v)) = O(N^(1/8)).             (7)

The constants are uniform over permitted t passing the guard. The last equality absorbs a fixed polynomial against the strict exponential gap. Writing the less simplified bound is useful because coefficient-certificate constants can be very large at finite sizes. The asymptotic space bound for preparation is also O(N^(1/8)), with fixed polynomial certificate scratch absorbed.

Use exactly the frozen N-step/N-word bounded-build wrapper, counting every instruction and allocation before executing it, and falling back on abort. Equation (7) establishes eventual success without requiring a numeric threshold. Since the scalar fallback is unchanged, the original finite-size uniform O(Nb) proof applies verbatim. The whole algorithm still uses O(N) words, because the working array and explicit input/output dominate.

## 5. All-input error proof for the additional rounding

Let z=(A,B) collect the first and second inputs of all N/2 disjoint butterflies in a stage; let D be the diagonal exact unit-phase operator on B and C its dyadic approximation. Write beta=sqrt(N)tau and alpha=sqrt(2N)tau. For a stage with no upper clipping, put M=q(CB). Equations (2) and the coefficient bound give

    ||M-DB|| <= [u(1+delta)+delta] ||B|| + beta
              <= (1+5/512)u ||z|| + beta,                  (8)

because u<=1/4 and delta=u/128. For the final prequantized value V=H_hat(A,M), equations (1) and (3), which hold even if M clips, imply

    ||V|| <= (1+u/512)(1+delta)||z||
            < (1+u/32)||z||.                             (9)

Combining (8) with (3) and adding final quantization gives

    ||q(V) - H(A,DB)||
      <= [(1+u/512)(1+5/512) + 1/512 + 1+u/32]u||z||
          + (1+u/512)beta + alpha
      <= 3u||z|| + 2alpha.                               (10)

For the last inequality, the square-bracketed factor is less than 3 at u<=1/4, and (1+u/512)/sqrt(2)+1<2. This is a normwise bound; it makes no linearity assertion about rounding. The same argument applies to small-span TS tables because their constituent butterflies are disjoint.

Initial quantization satisfies the weaker bound (10) with identity ideal stage. Let J=v+1, including initial quantization, and A0=||a||. For every clipping-free prefix,

    e_(j+1) <= (1+3u)e_j + 3u A0 + 2alpha.

Since 3uJ<1/2, the geometric multiplier is at most 2, and A0>=1/2. Therefore

    e_J/A0 <= 6uJ + 8J alpha
             <= 6uJ + 16JN tau
             = 22uJ
             <= (22/1024) 2^-t < 2^-t.                   (11)

The same bound holds for every prefix.

There cannot be a first clipping event. Before its stage, the stored vector has norm at most (1+2^-t)A0. A candidate first clipping in CB has prequantized norm at most (1+delta)(1+2^-t)sqrt(2N). A candidate first clipping in V has the bound in (9); the intervening quantizer is norm nonincreasing by (1). Both bounds are below 2sqrt(2N), hence below 32N. No real component can reach the clipping threshold. Initial normalized quantization is also safe. This covers **both** the new unary intermediate and the final Hadamard output without assuming their clipping-free errors in advance.

Thus (11) holds for every represented input, including arbitrarily small normalized components and cancellation-heavy data. Exact restoration of R_scale proves the desired relative-l2 statement. Output states remain on 2^(-v-2p) Z[i], with the same O(v+p)-bit numerator and decoding contract.

## 6. All lengths and practical scope

The conditional all-length compiler requires only the backend's all-input error, cold cost, finite-word domain, and common output lattice. All are preserved here. Its one backend call at T=t+10, including its T<=v+1 domain check and independent all-length fallback, therefore remains valid. No Taylor-rank multiplier or arbitrary-precision exemption is introduced. The all-length cold theorem is unchanged.

At the old literal guard thresholds, the same P=4 is selected. The following are exact integer inequalities; no arrays of these sizes were allocated:

| t | v | g | bP | Old packed response entries | New entries including scalar F/H |
|---:|---:|---:|---:|---|---|
| 2 | 5120 | 35 | 320 | between 2^674 and 2^675 | between 2^640 and 2^641 |
| 8 | 5888 | 41 | 368 | between 2^776 and 2^777 | between 2^736 and 2^737 |
| 16 | 6912 | 49 | 432 | between 2^912 and 2^913 | between 2^864 and 2^865 |
| 53 | 11904 | 87 | 744 | between 2^1574 and 2^1575 | between 2^1488 and 2^1489 |

This is a substantial symbolic storage reduction by a factor near Q, while the absolute numbers remain unusably large. Necessary guard thresholds are unchanged; successful-build thresholds are not known numerically. A lower table count is not a measured time improvement, especially when the online path adds a lookup.

The RAM words grow as Theta(log N). None of the arithmetic, addressing, or packed-lane counts are a free translation to fixed 64/128-bit hardware. In all ordinary 64/128-bit-addressable ranges the unchanged guard still chooses the scalar branch. The value t=53 denotes a normwise tolerance; it is not a binary64 format or coordinatewise rounding guarantee.

## 7. Prior-art boundary and verification

The inherited audit already establishes substantial precedent for persistent packed FFT arrays, batched tables, and charged sublinear setup. The primary source [Chan, Jin, Vassilevska Williams and Xu, Appendix B](https://arxiv.org/html/2310.13174v2) was revisited; no claim of inventing packed/table-based Fourier computation is made. Separating phase multiplication from a Hadamard is ordinary FFT structure, and Cartesian-product table enumeration is a generic construction device. The new local contribution is the explicit table-size/charged-build calculation **with a checked extra-rounding error budget in this frozen finite-state contract**. Priority for this exact variant is not established.

`check_split_tables.py` is freshly authored and imports only Python standard-library modules. It neither executes nor imports source/predecessor programs. Its exact controls test total-table layout, separated input/output fields, odometer write coverage and change counts, phase-catalogue indices, and packed-versus-scalar execution of the new two-rounding toy map. A separate exact rational witness falsifies the stronger claim that the split map always equals the original one-rounding map. Integer-only threshold counts allocate no full-sized tables.

These checks do not implement the theorem's full certified eager executor at its real parameters, do not establish practical speed, and do not replace the analytic all-input proof. The new proof and construction remain pending independent review.
