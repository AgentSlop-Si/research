# Independent review: paid bidirectional sector shears

## Result

**Accepted as an explicit, invertible mixing primitive in a transparently enlarged grammar.**

- The two existing nested N64 H0 routes give a pair of directed shears with cross ranks 16 in both directions. Their product differs from identity by rank 32.
- Adding the one explicit order XP to P=H0-minus gives cross ranks 32 in both directions and a full-rank difference from identity.
- The all-size two-sheet construction and its parity guards are correct. Full sector coverage is available for N=2n with even n, including every dyadic N>=4.
- The exact inverse needs no new coefficient determinant guard: each directed mixer squares to zero.
- The implementation pays a right/input mask, residual additions, and composition. Its stated four Green occurrences, two masks, and four vector additions are valid. Transpose alternatives separately pay inverse orders, reciprocal poles, or reflection passes.

The result supplies a useful positive primitive. It does not solve the Fourier coefficient equations or preserve the distinct-pole N16 seed automatically. Full-rank cross blocks are a necessary type of mixing, not a certificate of the target operator.

Constructor programs remained inert. All numerical controls here use independently authored exact modular arithmetic, while the uniform statements follow from the explicit proofs below.

## 1. Source, model and exact prerequisites

Source: bidirectional_shear_milestone.zip, SHA256

    44b6f626933e70c78959e4a3bdd85feb52b173d50de6855bf1577726a5cf7f06.

The original proof note and BIDIRECTIONAL_SHEAR_CONTROLS.json are preserved in sources/. SOURCE_PROVENANCE.json records the source archive. The new checker imports only the reviewer's own earlier geometry and modular linear-algebra utilities.

At N64, use the previously defined nested MGG Hamiltonian routes with P e_v=e_p(v), in the order H0-, H0+, H1-, H1+, V0-, V0+, V1-, V1+. They are regenerated from the 4 by 4 least-representative splices and the deterministic four-sheet lift, not taken as opaque source matrices. The high-x swap is X e_v=e_(v xor 32). Every route has P_j^32=X and commutes with X.

Write Pi_±=(I±X)/2 and D=diag(1 on indices 0..31, -1 on 32..63). Then D^2=I and DX=-XD. In sector coordinates use the unnormalized embeddings E_± e_k=e_k±e_(k+32). Their inverse coordinate projections are (I,±I)/2, so all block computations include the required factor 1/2. The same blocks result from orthonormalizing both embeddings by 1/sqrt(2).

For a common complex pole t, set G_j(t)=(I-tP_j)^-1. The guards are

    t != 0,  t^64 != 1.

The H0 pair has the same plus quotient. The relative permutation P_0^-1 P_1 has exactly 16 transpositions and 32 fixed points. Therefore, for

    K=G_0-G_1=t G_0(P_0-P_1)G_1,

we have

    rank K=16,  K=Pi_- K Pi_-.

The equality follows from the resolvent identity; rank follows because both Greens and the scalar t are invertible. At t=0 the difference is zero, so the nonzero guard is essential. At t^64=1 the inverses are undefined.

## 2. Forward and reverse channels

Define

    M=D K,  R=K D.

D exchanges the sectors, giving

    M=Pi_+ M Pi_-,  R=Pi_- R Pi_+.

Both ranks are 16, and M^2=R^2=0, because the output sector of either mixer is orthogonal to its own input sector.

M uses two original left-masked Green terms. R instead applies the character to its input, then applies the same two Greens and subtracts. This right mask is an explicit grammar change. The independently sealed common-pole span theorem proves that no nonzero arbitrary-left-mask sum of the original eight common-pole Greens can annihilate minus input; R does annihilate it. Thus R cannot be silently rewritten as an original eight-term left-mask layer.

That prerequisite review is review_signed_common_poles_sealed.zip, SHA256

    0c2cf1cd7cb106ae7e0db2b4b7a646c91b54c429531d0d8f69b08b4414829ff0.

The present positive construction and its rank proof do not require executing that prerequisite checker. Its separate certificate explains why the newly paid grammar is material.

R is generally different from M^T. The same-kernel reverse needs neither a new route nor a reciprocal pole.

## 3. Transpose alternatives and their exact costs

For an ordinary transpose, permutation matrices obey P^T=P^-1, so

    M^T=[G_(P_0^-1)(t)-G_(P_1^-1)(t)]D.

No complex conjugation is taken. For real t and real D, it also equals the Hermitian adjoint. The distinction matters for complex poles or masks.

The exact regenerated N64 arrays show that none of the eight inverse orders occurs among the eight forward orders. There are three legitimate implementations of the transpose reverse:

1. Add the two inverse orders and scan them directly. Building their arrays costs O(N) work and words. No additional standalone physical permutation pass is needed when the Green executor directly follows those orders; route traversal itself remains part of the scan.
2. Keep the forward orders but change the poles. For t != 0,

       G_(P^-1)(t)=I-G_P(1/t),

   because both sides multiply I-tP^-1 to I. The identity terms cancel in the difference, giving

       M^T=-K(1/t)D.

   The reciprocal guard follows from t^N != 1. At t=1/2 the new pole is 2. These are two additional declared order/pole occurrences, not free reuse of same-pole data.
3. Define a reflection by J_P(P^k(0))=P^(-k)(0). It is an involution with J_P P J_P=P^-1, so

       G_(P^-1)(t)=J_P G_P(t) J_P.

   Implementing two inverse Greens this way adds four length-N permutation passes. The two reflections need not agree. Their preparation and storage are O(N), and the input character mask is additional.

Every inverse, reciprocal and reflection identity was checked entrywise in the independent controls. Their correctness also follows directly from the displayed algebra; it is not an empirical equality at one pole.

## 4. Exact invertibility and rank of the shear product

For any two directed sector operators M,R with M^2=R^2=0, set

    U=I+M,  V=I+R,  S=UV.

Then

    U^-1=I-M,  V^-1=I-R,
    S^-1=(I-R)(I-M).

No invertibility of a diagonal sector block is required. In plus-first coordinates,

    M=[[0,A],[0,0]],  R=[[0,0],[B,0]],
    S=[[I+AB,A],[B,I]],
    S-I=[[AB,A],[B,0]].

The kernel condition is Bx=0 and ABx+Ay=0. The first equation reduces the second to Ay=0, hence

    ker(S-I)=ker B direct_sum ker A,
    rank(S-I)=rank A+rank B.

Both shears have determinant one, so det S=1, regardless of whether I+AB is singular. This is important: the block I+AB need not be invertible for S to be invertible.

For the original pair, both cross ranks are 16, rank(S-I)=32, and the fixed space of S has dimension 32. Either R=KD or R=M^T gives these ranks. At real t with the transpose reverse, S=(I+M)(I+M)^T is additionally symmetric positive definite. This positivity statement does not extend unchanged to arbitrary complex t or independent complex masks.

The checker also exhaustively verifies the general block rank and determinant identity for all 6,561 pairs of 2 by 2 matrices A,B over F3, including noncommuting pairs and cases where I+AB is singular. This is an independent edge-case control; the argument above proves the identity in every characteristic where the selected sector model makes sense.

## 5. Paid mask degrees of freedom

Replace D by odd diagonal masks D_a,D_b satisfying

    a(i+n)=-a(i),  b(i+n)=-b(i),  N=2n.

Then M_a=D_a K and R_b=K D_b retain opposite sector support and square zero. If all mask entries are nonzero, their ranks remain rank K; zero entries can lower ranks without invalidating the shear inverse.

Let C=K restricted to minus input/output. The cross blocks are exactly

    A=diag(a_low) C,
    B=C diag(b_low),

or B=C^T diag(b_low) for the transpose-kernel reverse. The two odd masks have n+n=N free complex entries. They supply specified row and column scalings, not arbitrary n by n cross matrices. Every nonzero endpoint requirement must be checked on these actual masks.

The independent controls include nowhere-zero nonconstant masks and two additional pole/field choices. They verify the block formulas with the correct sector normalization, rather than inferring them solely from full-matrix rank.

## 6. Uniform two-sheet family

Let N=2n, let q be any n-cycle, let epsilon(k) be bits of odd total parity, and choose an even-cardinality set A of h base tails. Define

    P_0(k,s)=(q(k),s xor epsilon(k)),
    P_1(k,s)=(q(k),s xor epsilon(k) xor 1_A(k)).

One circuit of q changes the sheet for both permutations, so both are single 2n-cycles. They commute with the sheet swap and satisfy P_j^n=X. On plus they both induce q. The relative permutation swaps the two sheets at exactly the h selected tails and fixes the other N-2h vertices. Therefore

    rank(P_0-P_1)=h,
    rank(G_(P_0)(t)-G_(P_1)(t))=h

whenever t != 0 and t^N != 1. The difference is confined to the minus sector. The paid shears have both cross ranks h and correction rank 2h.

For the quarter-rank example, q(k)=k+1, epsilon is one only at the wrap edge, and A consists of the odd k. This requires n divisible by four so h=n/2 is even. It applies to every dyadic N>=8. The actual nested N64 H0 pair realizes h=16 with A the odd base indices; this single verified identification is not an all-size MGG equality claim.

An odd number of voltage toggles instead makes the second lift split into two n-cycles. The parity restriction is substantive, not cosmetic. The checker explicitly tests these negative cases.

## 7. One added order gives full sector coverage

Suppose P is any Hamiltonian 2n-cycle commuting with a fixed-point-free involution X. The centralizer of a full cycle consists of its powers. The only nonidentity involution among those powers is P^n, so X=P^n.

Assume n is even and define

    P_new=XP=P^(n+1).

Here gcd(n+1,2n)=1, so P_new is Hamiltonian. It flips every voltage and corresponds to h=n in the preceding family. The same construction fails to be Hamiltonian when n is odd: the gcd is two and P_new splits into two cycles.

On minus, T=P|minus satisfies T^n=-I, and P_new restricts to -T. Hence

    Phi=G_P(t)-G_(XP)(t)=Pi_- Phi Pi_-,
    Phi|minus=2t T (I-t^2 T^2)^-1.

Both factors I-tT and I+tT are invertible under the Hamiltonian inverse guards; their product is I-t^2 T^2. Since t and T are invertible, Phi has rank n. The shears

    (I+D Phi)(I+Phi D)

have both cross ranks n, correction rank N, and no nonzero fixed vector. This is full sector coverage in the precise rank sense.

At N64, P_new(v)=p_H0minus(v) xor 32, equivalently P_H0minus^33. Its complete array was independently regenerated and is absent from the original eight-order list. Exactly one new distinct order is added. Full coverage is uniformly legal for every even n, including all dyadic N>=4; N=2 is excluded by the parity condition.

The checker verifies the explicit minus resolvent formula as a matrix identity and tests the smallest N=4 case, arbitrary base-cycle/voltage examples, and the source's eight N=8,16,32,64 quarter/full instances.

## 8. Cost and target equations

The declared same-kernel shear pair pays:

- four Green applications, two per shear;
- two diagonal-mask applications, an input mask for the reverse and an output mask for the forward;
- four vector additions/subtractions, a Green difference and an identity residual per shear;
- no extra standalone permutation passes when each Green is evaluated directly on its declared route.

A “Green scan” here denotes one O(N) Green application, with the established executor's internal constant-pass recurrence and wrap solve. Four such occurrences must not be misread as an assertion of exactly four N scalar operations. Every denominator 1-t^N, pole, mask value, array construction, and exact-coefficient representation remains declared data. The costs are arithmetic/word-operation costs, not bit-complexity bounds.

Native-inverse and reciprocal-pole transpose implementations have the same four-application count. Reflection conjugation adds four standalone permutation passes. The full-coverage version adds one order XP; the original rank-16 same-kernel version adds no order but still changes the right-mask/residual/composition grammar. Appending the pair to a 24-Green candidate therefore gives 28 declared occurrences, before any separately proved fusion. No common occurrence cancels merely because two factors use the same route.

For a fixed invertible prefix C_0, correcting by S alone requires W=F_N C_0^-1 to obey all four exact equations

    W_--=I,
    W_+-=A,
    W_-+=B,
    W_++=I+AB,

with A,B in the actual mask/kernel family and all pole and nonzero guards imposed. In particular det W=1. Full rank of A and B does not imply any of these target values. If other layers remain variable, their full expanded product must still satisfy every Fourier entry equation.

These primitives do not produce a fast Fourier transform, a uniform coefficient law, a seed-preserving descent, or a general no-go. Reciprocal poles, equalized poles, added XP orders and input masks all need explicit accounting when entering the original architecture. The earlier common-pole left-span obstruction remains correct in its original grammar.

## 9. Independent replay

Run:

    python3 independent_checks.py

Dependencies are only the Python standard library. Source and constructor scripts are neither executed nor imported.

VERIFIED_RESULTS.json includes regenerated inverse-order comparisons, exact original and added-order ranks, both inverse products, determinants, sector block identities, reciprocal/reflection identities, source uniform controls, fresh nonconstant-mask and second-field controls, all even-toggle combinatorial cases through n=8, representative full-matrix controls of every available toggle rank at those sizes, parity negative controls, and all 6,561 generic block-algebra cases over F3.

PORTABLE_REPLAY.json records the isolated temporary-directory replay and requires byte-identical results. All reviewed source bytes and reviewer outputs are sealed additively; no earlier constructor or reviewer archive is modified. Attribution remains with the source constructor for the primitive and uniform family, with the independent audit and its additional controls identified here. No publication-priority claim is made.
