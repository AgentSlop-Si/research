# Adaptive independent packing: a closed hard prefix and an explicit sharing escape

17 October 2026. New proof and independently written exact controls. Historical programs were read as source, not executed. No external repository, Library item, or document was changed.

## Result and scope

The previous one-level witness is not used as a recursive lower bound. Instead, this report constructs legal inputs whose actual children stay in an explicit invariant for a growing number of adaptive levels. It proves the following sharply restricted theorem.

**Theorem A.** The native Newton ordinary-value multiplier specified in §1, with input-dependent maxima, actual-bit-length recursive calls, zero-row omission, and independent execution of every remaining node call, has worst-case dense-bit complexity

T(n) = n exp(Theta(log n / log log n)).

The lower bound is witnessed by legal inputs C·2^E. The point, rank, block width, packing width, and actual child size are recalculated at every level. A parameter-cell/divisibility lemma keeps this family closed through D=Theta(log n/log log n) levels. No padded-capacity lower recurrence is used.

**Theorem B.** The same witness family has an elementary O(n) algorithm after extracting its powers of two. Moreover, the legal perturbation C·2^E+P gives pairwise distinct first-level child operands and has no input power of two to extract, but its node products still admit an explicit shared-leading-term construction with O(n) complete cost.

Accordingly, Theorem A closes an exactly defined **independent-call adaptive policy**. It does not close the user's broader shared-graph route. Theorem B is a concrete positive shared construction, but only on the stated sparse family. An arbitrary-input shared/adaptive construction or a hard family resistant to sharing remains open. This distinction is essential, not an optional caveat.

## 1. Exact policy being analyzed

This is an explicit self-recursive completion of the retained native Newton values-only packing interface. It is not a claim that the current Python producer already recurses this way. The source still uses a native integer multiplication at each reported packed call. Nor is this a theorem about the different default dyadic API shape in the latest archive.

At a call on signed integers A,B:

1. If either is zero, return zero. Remove signs. Let n=max(bit_length(A),bit_length(B)). Below a fixed finite threshold, use elementary schoolbook multiplication.
2. Set r=floor(log2 n), use the native point P_r, weights W_j and binary block width s_r from the accepted native plan, and split both operands into L=ceil(n/s_r) binary blocks, padding only the shorter block list with zeros.
3. Canonically convert each block to c_0,...,c_(r-1), and evaluate f(x)=sum_j (-1)^j c_j binom(x,j) at the same 2r-1 consecutive minimax-translated integer nodes as the source.
4. For each node, compute the actual row maxima A_x,B_x. Skip that product iff A_x B_x=0. Otherwise use exactly

   w_x = 8 ceil(bit_length(2L A_x B_x)/8),
   U_x = sum_i f_i(x) 2^(i w_x),
   V_x = sum_i g_i(x) 2^(i w_x).

   These are dense signed integers, produced by the source's bounded-window signed streams.
5. The recursive size is max(bit_length(abs U_x),bit_length(abs V_x)), not Lw_x. If a child is not strictly smaller than n, use schoolbook at this parent; otherwise recursively execute every nonzero node product independently. There is no equal-call memoization, factoring of common powers of two or integer content, virtual shifted-integer representation, or cross-node product sharing in this policy.
6. Decode the centered outer convolutions; interpolate the ordinary products; evaluate at -P_r; carry at 2^s_r; restore sign.

The finite fallback is only a termination guard. The standard cap gives every child O(n/log n), so it is unused at all sufficiently large n. Correctness is the same exact canonical encoding, strict signed-packing separation, ordinary interpolation, and binary-carry argument as before.

The native facts needed below, already proved in the accepted packet, are

r-O(log r) <= log2 P_r <= 4r+O(log r),
s_r = Theta(r^2),
s_r <= r log2 P_r.

In particular, eventually r^2/2 <= s_r <= 5r^2. These bounds require no prime-Mersenne hypothesis or external fast multiplier.

## 2. An exact adaptive invariant

Fix a positive odd constant C of bit length c. Suppose

A=B=C·2^E,  s_r divides E,  C<P_r,  c<s_r.

Put K=E/s_r. The binary input consists of K zero blocks and the last block C. Its canonical last block is exactly the constant polynomial C. Therefore every one of the m=2r-1 nodal rows is

(0,0,...,0,C).

Its actual maximum is C and every row is nonzero. The actual packing rule chooses the common width

w = 8 ceil(bit_length(2(K+1)C^2)/8).

The packed integers are exactly

U_x=V_x=C·2^(Kw),

independently of x. Thus each actual child has size

n' = Kw+c = Ew/s_r+c.

There is no cancellation, unused leading guard space, or actual-versus-allocated ambiguity in this identity. The allocation is (K+1)w, but the actual size is Kw+c. The next call has the same form with E'=Ew/s_r, provided the next divisibility and point conditions hold.

This statement also identifies its sharing weakness: all m calls are identical. The independent executor must execute them; a shared executor need not.

## 3. Parameter-cell alignment lemma

**Lemma.** For every sufficiently large integer R, put

c=floor(3R/4), C=2^(c-1)+1,
D=floor(R/(16 ceil(log2 R))).

There exists an integer E in [2^R,3·2^(R-1)] such that the invariant of §2 holds for D consecutive adaptive levels, with the same C. Every rank r_j in this prefix lies between 0.9R and R. In particular the family is closed through a number of levels tending to infinity at the required scale, rather than only at the root.

### Proof

First define a relaxed real exponent process e_0=e on I=[2^R,3·2^(R-1)]. At level j define

r_j=floor(log2(e_j+c)), s_j=s_(r_j),
w_j=8(floor(log2(2(e_j/s_j+1)C^2)/8)+1),
e_(j+1)=e_j w_j/s_j.

For integer L=e_j/s_j+1 this width is exactly the source rule, including its strict power-of-two boundary convention: bit_length(b)=floor(log2 b)+1 for a positive integer b.

Uniformly through the first D steps, the estimates s_j between r_j^2/2 and 5r_j^2 and 1.25R<=w_j<=3R give

1/(4R) <= e_(j+1)/e_j <= 8/R.

These estimates are consistent by induction. Indeed the lower estimate gives

r_j >= R-j(log2 R+2)-1 >= 0.9R

for large R and j<=D; the upper estimate makes exponents decrease and gives r_j<=R. All exponents remain exponentially large in R. Consequently C<P_(r_j), because log2 P_(r_j)>=r_j-O(log R)>c, and c<s_j.

Partition I into half-open intervals on which all r_j,w_j through level D-1 are constant. On any current interval e_j=alpha_j e for one positive rational alpha_j. The ratio of any two e values in I is at most 3/2. Hence e_j+c crosses at most one power of two, giving at most two rank choices. For each fixed rank, 2(e_j/s_j+1)C^2 varies by a ratio at most 3/2 and crosses at most one consecutive 256-power boundary, giving at most two packing-width choices. Each stage therefore creates at most four subintervals. There are at most 4^D final cells. One cell J has length at least

|I|/4^D = 2^(R-1-2D).

On this cell let S=product_(j=0)^(D-1) s_j. Its size satisfies

S <= (5R^2)^D.

Since D<=R/(16 ceil(log2 R)), for sufficiently large R the length of J is much greater than S. Choose an integer multiple E=tS strictly inside J. Every relaxed parameter is then unchanged, and

E_j/s_j = t [product_(h<j) w_h] [product_(h>j) s_h]

is an integer for every j<D. Thus every relaxed step is an exact legal adaptive step. The point and block-size conditions already proved show that its last canonical block remains the constant C at all those levels. This proves the lemma.

The proof is constructive: the rank boundaries and width boundaries are rational numbers, so the cells can be enumerated with exact arithmetic, and an interior multiple of S selected. Efficient generation of the adversarial input is not needed for the lower bound. The control program instead verifies a located exact cell and its interior multiple directly; it does not approximate these boundaries with floating-point logs.

## 4. Actual volume expands at every aligned adaptive level

Write n_j=E_j+c. The ratio of total actual child sizes to the actual parent size is exactly

V_j = (2r_j-1)(E_j w_j/s_j+c)/(E_j+c).

Since log2 E_j=r_j+O(1) and s_j=Theta(R^2), the actual width satisfies

w_j >= r_j+2c-O(log R) >= r_j+1.5R-O(log R).

Using s_j<=r_j log2 P_(r_j)<=r_j(4r_j+O(log R)) gives

V_j >= ((2r_j-1)(r_j+1.5R-O(log R))) /
       (r_j(4r_j+O(log R))) · (1-o(1))
    >= 5/4-o(1).

Thus V_j>=6/5 at every level of the closed prefix for sufficiently large R. All children are strictly smaller, since their ratio to the parent is O(1/R). The input-aware early exit and termination guard do not remove any of these calls.

There are product_(h<j)(2r_h-1) independently executed calls at level j. In the dense-bit model each of their returned integer products has Theta(n_j) bits and must be materialized separately; the retained signed-stream executor also materializes its streams explicitly. Therefore the work at level D alone is at least a constant times

n_0 product_(j<D) V_j >= n_0(6/5)^D.

Since D=(1/16+o(1)) log n_0/log log n_0,

T(n_0) >= n_0 exp((log(6/5)/16+o(1)) log n_0/log log n_0).

Logs in this last display are natural. For a clean fixed constant, every a<log(6/5)/16 gives an Omega(n exp(a log n/log log n)) worst-case bound. Inputs with these lengths occur in a fixed-ratio interval for every sufficiently large R. Hence the usual worst-case function over inputs of at most n bits has the same lower scale for all sufficiently large n, by choosing the preceding rank interval.

This is a lower bound from an actually repeated, explicitly specified computation, not from substituting a worst-case function into an upper recurrence. Its closure lasts D levels; no claim about the remaining descendants is required because the work already performed at level D suffices.

## 5. Complete upper bound and absence of circularity

Every actual adaptive child is bounded by the corresponding retained fixed-cap child. The accepted cap calculation gives sizes Theta(n/log n) and total cap volume at most

v_plus+o(1),  v_plus=4+(2+2J*)=9.0889395816...,
J*=1.5444697908... .

Use elementary algorithms for all local work, yielding the same conservative F(n)=O(n(log n)^4) ledger: native point/setup, conversion, integer maps, signed-stream materialization, transposition, finite-difference interpolation, evaluation, and binary output. The only large products omitted from F are precisely the recursive calls.

For Phi_b(n)=n exp(b log n/log log n), the cap recurrence ratio tends to at most e^(-b)v_plus. Thus any b>log(v_plus) provides an inductive upper bound O(Phi_b(n)), with F absorbed by the fixed eventual margin. Smaller actual children and zero-row omissions only decrease this upper bound. The finite schoolbook guard is paid and proves termination. Together with §4 this establishes Theorem A on the n exp(Theta(log n/log log n)) scale.

No external integer multiplier, unproved prime supply, uncharged cancellation, or lower bound inferred from an upper inequality is used.

## 6. The matching positive sharing constructions

### 6.1 Exact content extraction eliminates the unperturbed witness

For X=C·2^E with odd C, a dense binary scan finds E=v_2(X) and extracts the c-bit odd core. Multiply the two cores by ordinary schoolbook, then restore the shift. This costs

O(n+c^2)=O(n)

on the constructed family, since c=Theta(log n). The output has Theta(n) bits, so this is tight in the dense-output model. It is a valid preprocessing option for the same base/matrix route: after extraction only the small core product remains. No external fast multiplier is inherited.

Equal-call memoization also removes the independent branching in §2. It leaves one distinct child per aligned level, not 2r-1. Neither optimization is covered by Theorem A.

### 6.2 Removing duplicates is not enough: a distinct, odd perturbation

At an aligned root take

X=C·2^E+P_r = C rho^K+P_r.

The low block P_r is legal for all sufficiently large r and has canonical digits c_1=1, all others zero. Its ordinary value is -x. The top block is still the constant C. At every retained node,

row_x=(-x,0,...,0,C).

Since C exceeds every node magnitude, the actual maxima and packing width are unchanged. Consequently

U_x=V_x=C·2^(Kw)-x.

These are pairwise distinct for all 2r-1 nodes. Their actual bit lengths are the same as the unperturbed children for sufficiently large K. At least r-1 of them are odd, and X itself is odd because P_r is odd. Thus this control really removes both root input power-of-two extraction and equality of first-level child pairs.

Nevertheless let H=C·2^(Kw). Every required product is

(H-x)^2 = C^2·2^(2Kw) - (2Cx)·2^(Kw) + x^2.

One small C^2 product is shared. The remaining products involve only O(r)-bit numbers, and the powers of two are shifts. The exact outer convolution has only positions 0,K,2K nonzero. Existing ordinary interpolation recovers respectively P_r^2, 2CP_r, and C^2, so the final answer is

P_r^2 + 2CP_r rho^K + C^2 rho^(2K).

The root maps can skip the known zero outer columns; only three output columns require reconstruction. All setup and local arithmetic use r^{O(1)} elementary bit operations, and dense assembly costs O(n). Hence the complete cost is O(n) for this family as well. This is a concrete shared product construction on the same ordinary-value/base representation, not a switch to an external multiplier.

More generally, rows with a shared leading monomial C_A Y^K, C_B Y^K and small residual constants a_x,b_x admit

(C_A Q^K+a_x)(C_B Q^K+b_x)
= C_A C_B Q^(2K)+(C_A b_x+C_B a_x)Q^K+a_xb_x.

A single shared leading product plus paid small residual products suffices. This exact lemma explains why neither literal child distinctness nor actual argument lengths alone proves a shared-graph lower bound.

### 6.3 Remaining boundary

The controls do not show that the perturbed family remains hard after another adaptive level. On a node with x<=0 its residual -x is a small nonnegative constant; the next transformation can again create identical children. On x>0, binary borrowing changes the lower blocks. Neither behavior supplies a closed sharing-resistant family.

The unresolved task is now precise: construct and analyze a producer exploiting shared structure for arbitrary legal inputs, or construct a family with sufficiently long closed adaptive behavior after the allowed sharing/content rules have been explicitly defined. The preceding theorem must not be extended to an unspecified adaptive policy, arbitrary compressed arithmetic DAGs, or unrestricted integer multiplication.

## 7. Fresh evidence and provenance

The intact successor archive was materialized and retained privately. Its SHA-256 is

936bf7706643fc130c7cb1197848bf1c2bf193be533cdc01e6c3b265351c1581.

Relevant source was read as text:

- fft_outside_crt/asymptotic/packed_outer.py: actual maxima, strict byte-rounded width, zero-product omission, separate actual lengths, independent node loop;
- fft_outside_crt/asymptotic/PACKING_AND_FULL_COST.md: retained native plan and unclosed recurrence;
- fft_outside_crt/audit/node_offsets.py: dimension-only node shift;
- fft_compact_followup/encoding/minimal_denominator.py: exact native point;
- fft_advance_next/newton_bridge/PAIRED_CRT_RESULT.md: explicitly unchanged outer calls and widths;
- fft_advance_next/README.md: native multiplication remains the reported subroutine and no new exponent is claimed.

The accepted predecessor and independent review are local source evidence, not programs imported into these controls. `fresh_controls.py` is newly written and contains its own native arithmetic, exact parameter-cell computations, canonical encoding, source-rule packing, a recursive correctness executor, and sharing controls. `CONTROL_RESULTS.json` and `RUN.log` contain actual results; numerical controls supplement the proof and do not replace its asymptotic argument.
