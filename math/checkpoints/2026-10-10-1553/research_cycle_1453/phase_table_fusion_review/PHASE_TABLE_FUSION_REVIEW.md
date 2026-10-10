# Independent phase/table fusion review

10 October 2026. Review of the frozen split-table architecture and the forthcoming amplitude rewrite ledger. This file is separate from all accepted artifacts. The optional block-granularity refinement below is a new candidate, not a silent change to the accepted construction.

## Executive result

The literal three-phase rewrite does not establish a smaller leading cold-preparation exponent or faster transform in the frozen architecture. A constant number of phase directions does not make the varying amplitudes, phase choices, rotations, quantization, or packed arithmetic free.

Two independent obstructions must be distinguished:

1. The phase-independent packed Hadamard response table has S² entries, much larger than the phase-dependent QS term under the frozen parameters.
2. The retained leading-bit chunk table itself has Θ(N^(1/8)) entries. Even removing every response table would not improve the total preparation exponent while retaining that chunk width.

There is nevertheless a simple exact response-memory refinement unrelated to a constant phase palette: replace HP by two calls to one P/2-lane Hadamard table. This changes S² to S with constant online overhead and no extra numerical rounding. A genuinely table-free word-parallel floating Hadamard kernel is a different, unproved route; it must charge its lane alignment, normalization, multiplication, and layout operations.

## 1. Read-only sources and scope

Reviewed as mathematics, without importing or executing any source program:

- `research_cycle_1453/packed_improvement/SPLIT_TABLE_CONSTRUCTION.md`.
- `research_cycle_1453/amplitude_fields/approximation_boundary/RATIONAL_APPROXIMATION_BOUNDARY.md`.
- The finite-word and operation contract in `packed_fft_candidate_1355/executor_derivation/DYADIC_PACKED_THEOREM.md`.
- Final candidate `research_cycle_1453/amplitude_fields/packed_twiddle_boundary/PACKED_TWIDDLE_REWRITE_LEDGER.md`, SHA-256 `4d7ae1a0007ac1f453642eff6db4b937ceb0eb301da7835ee56b6622b29a0eca`.

Source hashes are recorded separately. Fresh controls written for this review import only the standard library. No external document or service was changed.

The exact amplitude-field theorem concerns odd-prime Fourier matrices. Its field-degree and exact phase-coverage conclusions do not automatically apply to a dyadic approximate executor. Only elementary cone approximation, finite-accuracy distinguishability, and explicit operation accounting are used here. In particular, the description-count argument below uses the actual half-circle radix-2 twiddles rather than an unrelated prime Fourier matrix.

## 2. The dominant terms in the frozen ledger

Keep the accepted definitions

    R = 2^b,  S = R^P,  Q = 2^g,
    b = 2(p+k+1),  g = p+10,  P >= 4,
    d = log2(P).

The exact response/helper count is

    E = S² + (Q-1+d)S + QR + R².

The ratio relevant to removing a phase catalogue is

    Q/S = 2^(p+10-2P(p+k+1))
        <= 2^(2-7p-8k).

Thus deleting the entire phase-dependent unary catalogue saves only a very small fraction of the dominant response term. The conclusion is stronger than merely Q<S. A fixed-three-phase notation does not touch HP's two independent packed input words.

Separately, the exact chunk-table construction writes 2^h entries for h=max(1,floor(v/8)). In the packed branch v is large, so this is Θ(N^(1/8)). Since S² <= 2^(v/8), that chunk table is never asymptotically smaller than the largest possible HP table. The coefficient-certificate term Q·poly(v+p) has a strict exponential gap under the retained guard. Consequently the retained eager preparation architecture has a Θ(N^(1/8)) contribution even after a hypothetical complete removal of Q-dependent tables. This is an architecture cost, not an FFT lower bound.

## 3. What finite accuracy forces the coefficient descriptions to retain

The accepted local coefficient tolerance is

    δ = u/128 = 8/Q.

The actual large-stage catalogue contains all constant-lane phases indexed by

    q = 0,1,...,Q/2-1.

They occur at r=g, hence stage ell=d+g. This stage is present under the packed guard: g<=v/128+10, d<=log2(v), and the guard forces v well above 32, so d+g<=v. The following count is therefore about phases the transform uses.

Let a complete varying description comprise all amplitudes, phase selectors, and any other q-dependent coefficient data. With a fixed global palette and a deterministic evaluator, the same description gives the same complex coefficient w. If one description approximates target indices q and q' to error δ, their root separation is at most 2δ=16/Q. Writing a=|q-q'|<=Q/2, concavity of sine gives

    |exp(2πiq/Q)-exp(2πiq'/Q)|
       = 2 sin(πa/Q) >= 4a/Q.

Hence a<=4. One description covers at most five integer indices in the half-grid, and at least

    ceil(Q/10)

distinct joint descriptions are needed. For any fixed O(u) tolerance, changing constants gives the same Ω(Q) conclusion.

For example, suppose the representation uses one of three canonically ordered adjacent palette pairs and at most two dyadic amplitudes in [0,2] with B fractional bits. There are at most

    3(2^(B+1)+1)²

possible descriptions, so B>=g/2-O(1) is necessary. This does not contradict a constructive sufficient B=g+O(1), and it does not establish a sharp coefficient-bit minimum.

Most importantly, distinct coefficient descriptions are not the same as stored table entries. Ω(Q) descriptions does not prove Ω(QS) memory for an arithmetic generator or evaluator. The QS count applies when one explicitly stores a full S-input response table for each of Θ(Q) coefficient descriptions. Compressed tables, shared subtables, generated coefficients, or an arithmetic kernel require their own charged ledger. The count rules out treating the varying data as a constant-size alphabet; it is not a general word-RAM multiplication or storage lower bound.

## 4. The arithmetic accounting boundary

Writing a coefficient as a sum of two nonnegative real scalings followed by fixed rotations can move the complexity into amplitudes. It does not remove multiplication. In particular:

- Fixed rotations of variable complex inputs still require arithmetic or explicitly stored responses.
- Naively scanning B coefficient bits and adding selected shifted values uses Θ(B) rounds in that implementation. This is not a lower bound against word multiplication, alternative circuits, or precomputation.
- Scalar lane extraction, evaluation, and repacking costs Θ(P) operations per packed pair if performed lane by lane, yielding O(Nv), rather than the packed O(Nb) execution bound.
- Replacing phase-dependent unary responses does not by itself remove the phase-independent floating Hadamard response table.

A proposed table-free packed Hadamard algorithm must exhibit operations from the accepted RAM instruction set. Its fixed control flow must handle variable per-lane exponent comparisons and alignment, signed addition/subtraction and cancellation, leading-bit detection and renormalization, multiplication by the certified dyadic normalization factor, quantization/underflow/clipping, malformed-code behavior, and the actual packed field layout. Cross-lane carries and scalar-word multiplication cross terms require proof, not an invocation of SIMD.

If such a kernel takes K_H(P,b,v) charged word operations per P-lane pair while the unary M tables remain, the online bound becomes

    O(N + Nd/P + N(v-d)(1+K_H)/P).

When K_H>=1 this is at most the usual simplified O(N + Nv K_H/P)=O(Nb K_H), with the actual cost of any layout changes included in K_H. Constant K_H would preserve the asymptotic online bound; K_H=O(log b) would instead give O(Nb log b). Neither kernel is established merely by a constant phase palette. Scalar-lane evaluation gives the fully charged fallback K_H=Θ(P).

## 5. A separate exact block-granularity refinement

This refinement does not require a new floating arithmetic kernel. Let

    r=P/2,  L=br,  mask=2^L-1.

Define H_r on two r-lane blocks exactly as HP is defined on two P-lane blocks: apply the same total scalar H to each pair, return all first outputs low and all second outputs high. There are

    R^(2r)=R^P=S

entries in this one universal table, not two separately stored tables.

For the existing dense packed words A and B (after the existing M_id operation), use

    z0 = H_r[(A & mask) | ((B & mask) << L)]
    z1 = H_r[(A >> L) | ((B >> L) << L)]
    A' = (z0 & mask) | ((z1 & mask) << L)
    B' = (z0 >> L) | ((z1 >> L) << L).

The two chunks are contiguous within each original word. No gather, lane permutation, new phase index, or implicit bit transpose appears. Each half lookup evaluates disjoint original lanes, so the reconstructed output equals the original HP output on every key, including malformed state codes. There is no extra numerical quantization. The existing M_id catalogue and the small-stage TS tables remain exactly unchanged.

The Cartesian construction lemma applies with m=r and D=R², using the already charged scalar H table. H_r therefore costs O(S+r)=O(S) construction work and S words. The resulting exact response/helper count is

    E_half = (Q+d)S + QR + R²,
    E - E_half = S²-S.

Two table calls and a fixed number of masks/shifts/ORs replace one HP call. Online execution stays O(Nb), and the accepted stability proof applies unchanged because the local map is identical. This is a storage-versus-constant-online-work tradeoff, not a new transform-time asymptotic or a constant-phase consequence.

With the original bit-length chunk width, total cold preparation remains Θ(N^(1/8)). If a separate variant changes that width to h=max(1,floor(v/16)), every O(v)-bit scalar still has O(1) chunks, and its new table costs O(N^(1/16)). Combined with QS<=2^(9v/128+10), this gives a conservative O(N^(9/128)) eager-preparation upper bound, while the coefficient and helper terms remain below it asymptotically. That is a newly specified parameter variant, not the retained frozen construction.

More generally, reducing all packing blocks by any fixed power-of-two factor trades a fixed online constant for smaller table exponents. Thus the accepted largest-P choice is a design choice; the exponent 1/8 is not intrinsic. The optional half-HP change is useful precisely because it leaves all unary phase indexing intact and has a short exact layout proof.

## 6. Fresh verification

The independently authored `fresh_review_controls.py` checks the two-half layout against direct lane evaluation for 270,848 packed input pairs, using several radices, lane counts, and two arbitrary total scalar maps. This is an exact algebraic-layout control, not an implementation or accuracy test of the theorem's numerical quantizer. The analytic identity above holds for every total scalar H.

An additional 22 exact integer parameter cases check the packed guard, Q/S exponent estimate, table-entry identities, and power bounds. All controls passed. No original/source program was imported or executed; the source artifacts are untouched.

## 7. Status

The final candidate ledger has been read and is accepted within its expressly bounded scope. Its actual-half-grid argument, bounded-dyadic coefficient-bit count, Q/S estimate, deletion fraction, bit-serial implementation caveat, and retained-helper preparation conclusion are valid. It makes neither an unjustified exact-prime-to-dyadic transfer nor a general table-space lower-bound claim.

The distinguishability count is an information-description boundary, not a general algorithm lower bound. The half-HP refinement remains a separately specified candidate rather than a replacement for an archived ledger.

An independent proof-level review by the amplitude-ledger author accepted the half-HP formulas on every total scalar H, the count (Q+d)S+QR+R², the exact saved S²−S entries, and the separately specified v/16 chunk variant's O(N^(9/128)) eager-preparation bound. That review was analytic and did not execute source programs or duplicate the fresh layout controls. Final integration and archival acceptance remain pending in this checkpoint.
