# Paid bidirectional sector shears and a uniform full-coverage extension

## Results

The existing nested N64 pair supplies a positive, exactly invertible bidirectional mixing primitive once one right/input character mask is explicitly allowed. No new route is needed for the same-kernel reverse channel. A literal transpose reverse channel can instead use two inverse orders, or the same two forward orders at reciprocal poles. All scans and standalone permutation passes are counted below.

The original rank-16 pair gives cross ranks 16 in each direction and rank 32 for the shear product minus the identity. A uniform extension adds just one order, XP, to any suitable existing Hamiltonian route P. Its two shears give cross ranks N/2 and rank N for their product minus the identity. This is complete algebraic sector coverage, not a Fourier coefficient solution.

These constructions extend the previously fixed grammar transparently. They do not alter or supersede the frozen common-pole span obstruction. They do not preserve the accepted N16 seed's pole schedule automatically.

## 1. Existing rank-16 pair and its reverse

Use the exact nested N64 routes P_0=H0-minus and P_1=H0-plus, with X the physical half-shift by 32, Pi_sigma=(I+sigma X)/2, and

    D=diag(chi_x),  chi_x(i)=+1 for i<32 and -1 otherwise.

Then D^2=I and DX=-XD. At a common complex pole t with t != 0 and t^64 != 1, put

    G_j(t)=(I-tP_j)^(-1),
    K(t)=G_0(t)-G_1(t).

The two routes have the same X-plus quotient. Their relative permutation has 16 transpositions and 32 fixed points. Therefore

    K=Pi_- K Pi_-,  rank K=16.

The resolvent identity K=tG_0(P_0-P_1)G_1 proves the rank statement for every guarded t, without a floating-point rank test.

Define two directed mixers

    M=DK=Pi_+ M Pi_-,
    R=KD=Pi_- R Pi_+.

Both have rank 16 and square to zero. R uses the same two existing Green orders and the same common pole as M. Its implementation applies D to the input, then applies G_0 and G_1, and subtracts. That right/input mask is the exact grammar extension being paid for. It is not an original left-mask-only combination.

Indeed the separately frozen common-pole theorem proves that no nonzero arbitrary-left-mask sum of the existing eight common-pole Greens can annihilate minus. R does annihilate minus, so its new right mask cannot be silently folded into the old bank.

## 2. Transpose implementation and inverse orders

The ordinary transpose reverse mixer is

    M^T = K^T D
        = [G_(P_0^-1)(t)-G_(P_1^-1)(t)] D.

For complex t this is an ordinary transpose, not a conjugate transpose. At the explicit real pole t=1/2 the distinction disappears if a Hermitian adjoint is wanted. The shear arguments below use only sector support and rank.

Exact successor-array comparison shows that neither P_0^-1 nor P_1^-1 belongs to the existing eight N64 orders. In fact none of the eight inverse orders equals any of the eight forward orders. The complete inverse arrays and comparison results are saved in the controls.

There are three explicit implementation choices:

1. **Native inverse scans.** Add the two inverse orders and perform two length-64 Green scans on them, after the input mask D. Generate and store the inverse successor arrays in O(N) work. There is no additional standalone physical permutation pass: the scans directly traverse their declared orders. Their route-indexed data movement is included in scan cost.

2. **Reciprocal poles on the original orders.** For any nonzero guarded t,

       G_(P^-1)(t)=I-G_P(1/t).

   This follows by multiplying I-tP^-1=P^-1(P-tI). The identity contributions cancel in the difference, giving

       M^T = -K(1/t)D.

   Thus two scans on the original forward orders at pole 1/t suffice, plus the paid input mask and subtraction/sign. The reciprocal pole is legal because t^N != 1 implies (1/t)^N != 1. At t=1/2 it is 2. This changes the pole schedule; it does not make a reciprocal-pole occurrence free.

3. **Reflection conjugation with an existing scan primitive.** For route P, enumerate v_k=P^k(0), and define J_P(v_k)=v_(-k mod N). Then J_P is an involution and J_P P J_P=P^-1, so

       G_(P^-1)(t)=J_P G_P(t) J_P.

   Two inverse Green occurrences implemented this way cost two ordinary Green scans and four length-N reflection-permutation passes in total. The two route reflections need not agree and are not shared for free. The input mask is additional. Their complete arrays are included in the N64 controls.

The simpler R=KD from Section 1 avoids inverse orders and reciprocal poles, but it is generally not the transpose M^T. Both choices give the exact ranks below.

## 3. Invertible shears and exact coverage

Since M^2=R^2=0, the two shears

    U=I+M,  V=I+R

have exact inverses I-M and I-R. Their product S=UV has inverse

    S^-1=(I-R)(I-M),

and determinant one. The identity/residual additions are explicit O(N) operations; they are not absorbed into uncharged Green terms.

Choose sector coordinates with plus first and minus second. Write

    M = [[0,A],[0,0]],
    R = [[0,0],[B,0]].

Then

    S = [[I+AB,A],[B,I]],
    S-I = [[AB,A],[B,0]].

This formula applies to either reverse implementation and to arbitrary directed matrices A and B. For a vector (x,y), (S-I)(x,y)=0 exactly when Bx=0 and Ay=0. Therefore

    ker(S-I)=ker(B) direct_sum ker(A),
    rank(S-I)=rank(A)+rank(B).

For the existing N64 pair, rank A=rank B=16. Both cross blocks of S have rank 16, rank(S-I)=32, and the fixed space of S has dimension 32. Invertibility of S does not imply complete mixing coverage; these are separate assertions, and both are quantified here.

With R=M^T and real t, S=(I+M)(I+M)^T is additionally symmetric positive definite. This observation is not needed for any Fourier claim.

## 4. Paid mask freedom

The character D may be replaced by a diagonal mask D_a with

    a(i+N/2)=-a(i).

Such a diagonal anticommutes with X. With independent odd masks a,b, put

    M_a=D_a K,  R_b=K D_b.

The nilpotence and shear inverse formulas remain exact. If every entry of both masks is nonzero, their two ranks remain rank K. There are N/2 free complex entries in each odd mask, hence N complex mask parameters for the pair. Nonzero masks must be guarded explicitly if the declared endpoint branch requires them.

Let C denote K restricted to the minus sector, in the E_sigma e_k=e_k+sigma e_(k+N/2) coordinates. Then

    A=diag(a_low) C,
    B=C diag(b_low).

For a transpose-kernel reverse option, B=C^T diag(b_low). Thus paid two-direction coverage does not supply arbitrary cross matrices: the remaining freedom consists of these explicit row and column scalings and any declared pole choice.

## 5. A uniform paired-route construction

The rank-16 example is an instance of a general two-sheet construction, independent of numerical fitting.

Let N=2n. Choose any n-cycle q on base vertices {0,...,n-1}, a bit voltage epsilon(k) with odd total parity, and a set A of base edges with even cardinality h. On vertices (k,s), s in {0,1}, define

    P_0(k,s)=(q(k), s xor epsilon(k)),
    P_1(k,s)=(q(k), s xor epsilon(k) xor 1_A(k)).

Both permutations are Hamiltonian 2n-cycles: one circuit around q toggles the sheet, because the two total voltages are both odd. Both commute with the sheet swap X and satisfy P_j^n=X. Their plus restrictions are the same q. The relative permutation P_0^-1 P_1 swaps the two sheets at precisely the h base tails in A. It has h transpositions and N-2h fixed points. Consequently, for every nonzero legal t,

    rank(G_(P_0)(t)-G_(P_1)(t))=h,
    K=Pi_- K Pi_-.

The same forward/right-mask reverse shears have cross ranks h and product correction rank 2h.

An explicit uniform quarter-rank family is obtained for n divisible by four by choosing q(k)=k+1 mod n, epsilon(k)=1 only at k=n-1, and A={1,3,...,n-1}. Then h=n/2=N/4. In particular this is defined for all dyadic N>=8. It is a new explicit route family, not an assertion that independently spliced or nested MGG descendants have identical plus quotients at every size.

The actual N64 H0 pair fits the abstract construction: its shared q and two voltage tables are supplied, and A consists of the 16 odd physical base indices. No all-size MGG equality beyond that verified instance is inferred from this fact.

## 6. Full-sector coverage with just one added order

There is an especially simple uniform choice h=n. It is legal whenever n is even, because |A|=n must have even parity. This includes all dyadic N>=4.

Start from any Hamiltonian P commuting with a fixed-point-free sheet swap X. A permutation commuting with a single cycle is a power of that cycle; the fixed-point-free involution must be X=P^n. Define the added order

    P_new=XP=P^(n+1).

Since gcd(n+1,2n)=1 when n is even, P_new is Hamiltonian. It corresponds to flipping every base-edge voltage. It shares P's plus restriction and negates its minus restriction.

Let T=P|minus. Then T^n=-I and

    Phi=G_P(t)-G_(XP)(t)=Pi_- Phi Pi_-,
    Phi|minus=(I-tT)^-1-(I+tT)^-1
             =2t T (I-t^2 T^2)^-1.

Under t != 0 and t^N != 1, every factor is invertible on the minus sector. Therefore rank Phi=n. The shear pair

    (I+D Phi)(I+Phi D)

has both cross ranks n and rank(product-I)=N. It has no nonzero fixed vector. This is complete sector coverage in the stated linear-algebra sense.

At N64, choose the existing P=P_H0minus. The added successor is simply p_new(v)=(p(v)+32) mod 64, equivalently P^33. It is absent from the original eight-order list; this exact comparison and its full successor array are supplied. Thus the full-coverage variant adds one distinct order, rather than requiring two unrelated new routes. Its four Green occurrences are still all charged.

The smallest-size parity conditions matter. The quarter-rank construction needs n divisible by four, and the full-rank construction needs n even. They are not asserted at N=2, where flipping the sole base edge destroys the Hamiltonian condition.

## 7. Application and preparation costs

For the shear pair using the same-kernel right-mask reverse:

- Four length-N Green scans: two in each shear.
- Two diagonal-mask applications, one at the input of the reverse mixer and one at the output of the forward mixer.
- Four length-N vector additions/subtractions: one Green difference and one residual identity addition per shear.
- Zero standalone physical permutation passes when the declared Green orders are scanned directly.

For the transpose reverse, native inverse scans or reciprocal-pole scans have the same four-scan count. The reflection-conjugation implementation instead adds four length-N permutation passes. A global minus sign can be included in the already charged difference operation.

For the existing rank-16 construction the same-kernel option adds no distinct route, but it adds a right mask. The native-transpose option adds two inverse routes; the reciprocal version adds two order/pole occurrences at 1/t without new routes. For the full-coverage construction, one additional order XP is charged. If appended as a separate gate to a 24-scan three-layer candidate, the explicit total is 28 scans, plus the extra masks and additions; no existing scan is canceled across compositions without an actual operator identity.

Each successor array, inverse array, reflection array, or voltage list is constructed in O(N) word operations and stored in O(N) words. Only arrays used by the chosen implementation need be stored. Denominator/pole preparation and all mask values are additional declared data. These are arithmetic/word-operation costs, not a bit-complexity claim for exact large rational coefficients.

## 8. Remaining coefficient equations

A primitive with two full-rank cross blocks is not a Fourier factorization. For example, suppose a fixed invertible lifted prefix C_0 is to be corrected only by this shear pair:

    S C_0 = F_N,  W=F_N C_0^-1.

In the declared sector coordinates this is equivalent to all four block equations

    W_-- = I,
    W_+- = A,
    W_-+ = B,
    W_++ = I+AB,

with A and B in the exact paid mask/kernel families of Section 4, all pole and nonzero guards imposed. In particular det W=1 is necessary. These block equations are target-specific restrictions and must be proved or solved; coverage does not establish them.

If additional original Green layers or the active Fourier bank remain variable, the complete expanded product must still satisfy every Fourier entry equation with all new masks, orders, poles, and occurrences counted. Changing a common pole, introducing a reciprocal pole, or appending XP does not by itself descend to the accepted distinct-pole N16 seed. Seed preservation, bank compatibility, and a uniform coefficient law remain open obligations. No numerical lift search was launched for this bounded primitive.

## 9. Exact controls and preservation

`check_bidirectional_shears.py` regenerates the N64 routes, proves all eight inverse orders are absent by exact array comparisons, checks the reciprocal and reflection identities entrywise, and verifies nilpotence, both inverse products, both cross ranks, and correction ranks in exact modular arithmetic. It also checks eight uniform instances at N=8,16,32,64 and the one-added-order full-coverage N64 extension. The all-size rank and invertibility statements follow from the displayed algebraic and combinatorial proofs, not from extrapolating those finite controls.

Run `python check_bidirectional_shears.py --verify` to check the saved exact data without rewriting it. All code was newly authored in this construction track. No uploaded source is executed. The signed-pole, opposite-channel, and earlier constructor seals remain unchanged; independent review of this additive package is separate.
