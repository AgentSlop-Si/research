# A four-by-four coefficient gate for two Green terms

## Result and exact scope

A constant-size polynomial identity in entries of the target B is necessary for a specified sum of two independently ordered, monomial-ended weighted-cycle Green maps. It is obtained by eliminating two-component denominator coefficients from zero entries of Q0 B Q1=Q0+Q1. No division by edge weights, target entries or intermediate minors is used.

For the odd-chirp forced B at N=13, this gate gives a nonzero four-by-four determinant for two explicit noncommuting Hamiltonian orders. Thus no choices of their edge weights or diagonal endpoint masks realize B, including zero edges and singular endpoint masks, provided the original Green inverses are defined. These orders pass every earlier half-cut routing test. The result is a fixed-order, fixed-size exclusion, not an exclusion of every paired-Green map or a growing-length Fourier theorem.

## 1. General local elimination

Initially assume both Green branches are invertible. Write B=T0+T1 and Qs=Ts^(-1). Then

    Q0 B Q1=Q0+Q1.                                   (1)

For monomial-ended single-cycle maps, each Q has support on the union of two permutation patterns. Describe row i of Q0 by positions r0(i),r1(i) and coefficients a_i,b_i. Describe column j of Q1 by positions c0(j),c1(j) and coefficients d_j,e_j. All pattern positions are known from the cycle and endpoint permutations. With diagonal endpoints, r0(i)=i, r1(i)=pi(i), c0(j)=j, c1(j)=tau^(-1)(j).

Let Z_i contain the union of all structurally allowed column positions in row i of Q0+Q1. Its size is at most four for arbitrary monomial endpoints, and at most three for diagonal endpoints. These are structural supports: do not remove a position merely because a current edge coefficient vanishes.

For j outside Z_i, equation (1) says

    [a_i,b_i] M_ij [d_j,e_j]^T=0,

where

    M_ij = [[B[r0(i),c0(j)], B[r0(i),c1(j)]],
            [B[r1(i),c0(j)], B[r1(i),c1(j)]]].         (2)

Fix distinct rows i,k. For every j outside Z_i union Z_k, both row vectors [a_i,b_i]M_ij and [a_k,b_k]M_kj annihilate the same nonzero column [d_j,e_j]^T. Their two-by-two determinant must therefore vanish.

Write M_ij=[[A,C],[B,D]] and M_kj=[[E,G],[F,H]]. The determinant becomes

    (A G-C E) a_i a_k
    +(B G-D E) b_i a_k
    +(A H-C F) a_i b_k
    +(B H-D F) b_i b_k = 0.                           (3)

For any four eligible columns j1,j2,j3,j4, stack these coefficient rows into a four-by-four matrix R. The tensor

    z=(a_i a_k,b_i a_k,a_i b_k,b_i b_k)^T

is nonzero because each row of the invertible Q0 is nonzero. Hence

    det R=0                                           (G4)

is necessary.

This works even when a numerator entry, edge coefficient, or two-by-two M_ij is zero or singular. No Möbius quotient is taken. A zero entire column of Q1 would violate its assumed invertibility, so it is not a lost valid branch.

The same construction with every eligible column gives an O(N)-by-four matrix. Its kernel must contain a nonzero decomposable tensor satisfying z0 z3=z1 z2. Thus rank four rejects immediately. At rank three, the unique null direction must satisfy this quadratic equation, providing a second exact local gate. These are necessary local compatibility conditions; passing them does not establish global coefficient consistency, the supported entries of (1), or the original Green guards.

## 2. Singular endpoint masks are covered by polynomial continuation

The determinant in G4 is a polynomial solely in entries of B; the denominator coefficients were eliminated. Consequently its necessity extends to rank-deficient endpoint masks, even though Qs does not exist at that boundary.

Keep the two weighted-cycle denominators fixed and valid. In each endpoint diagonal, replace every zero scale by a formal variable epsilon, leaving nonzero scales unchanged. Keep endpoint permutations fixed. Over E(epsilon), every endpoint is invertible, so the preceding proof shows that the polynomial determinant is identically zero for B(epsilon)=T0(epsilon)+T1(epsilon). Each T_s(epsilon) is regular at epsilon=0 because its Green denominator has not changed; it specializes to the original possibly rank-deficient branch. Evaluate the polynomial identity at epsilon=0. This proves G4 for the original B as well.

The argument works over finite fields using the formal rational-function field; it does not depend on infinitely many distinct numeric epsilon choices. Zero edge weights were already permitted and require no perturbation. A singular original Green denominator is still invalid: multiplying by a zero endpoint does not define an inverse that does not exist.

Thus, for fixed cycle and endpoint permutation patterns, a nonzero G4 determinant excludes all endpoint masks in this model. No invertibility of target principal blocks, M_ij, or Q0+Q1 principal subblocks has been assumed. When both branches and B are invertible, Q0+Q1 itself is invertible by (1), as a consequence rather than an extra unchecked condition.

## 3. Explicit chirp target entries, without applying a Fourier transform

Use N odd, h=(N+1)/2, a primitive Nth root omega, characteristic not dividing 2N, and

    G=sum_j omega^(h j^2),   c=N G,   1+c!=0.

The forced B for the positive quadratic chirp has entries

    B[i,j]=[omega^(ij)-G omega^(-h(i+j)^2)
             +c omega^(-h i^2) indicator(i=j)]/(1+c).  (4)

This is the entrywise form of the independently proved odd-chirp feedback identity. It is used here only to generate selected certificate entries, not as an O(N) arbitrary-vector B evaluator.

All N root powers and chirp phases, and G, are generated in O(N) field operations and storage. With these tables, any selected B entry costs O(1) arithmetic and modular indexing. One fixed row-pair gate using all eligible columns therefore costs O(N) preparation plus O(N) arithmetic and constant-width linear algebra. A chosen four-column witness costs O(N) preparation and O(1) additional arithmetic. Checking all row pairs or constructing a full N-by-N B must be charged separately and is not asserted linear-time.

## 4. A thirteen-point exclusion beyond the routing gate

Let N=13. Choose row cycles

    pi(i)=i+6 mod13,
    tau=sigma pi sigma,   sigma=(0 1).

Explicitly,

    pi  =[6,7,8,9,10,11,12,0,1,2,3,4,5],
    tau =[7,6,8,9,10,11,12,1,0,2,3,4,5].

Both are Hamiltonian. They do not commute; for example pi(tau(0))=0 whereas tau(pi(0))=12. The first cycle alone has six crossings through every cyclic interval of length six. Therefore the pair passes all earlier half-cut crossing budgets, irrespective of the present coefficient obstruction.

Take Q0 supported on diagonal plus pi and Q1 on diagonal plus tau, corresponding to arbitrary diagonal-ended Green branches in these orders. Use rows i=0,k=1. The combined structural right-hand support is

    Z0 union Z1={0,1,6,7}.

The four columns 2,3,4,5 are all eligible. Their tau-inverse coordinates are respectively 9,10,11,12.

Compute the chirp target over F65521 with

    omega=17^((65521-1)/13)=56909,
    h=7,
    G=63693,
    c=13G=41757,
    1+c=41758 != 0.

Using coefficient order (a0 a1,b0 a1,a0 b1,b0 b1), formula (3) gives

    R = [[30388,12950,52923,20728],
         [30191,50630,14717,  481],
         [27205,30796,53578,20728],
         [20815,59325,15216,39038]].

Its determinant is 60131 modulo 65521, which is nonzero. This excludes every valid choice of edge weights and diagonal endpoint masks at these orders, including zero-edge and singular-endpoint branches.

## 5. Characteristic-zero lift

For complex primitive zeta of order13, the certificate entries lie in the cyclotomic field Q(zeta), with denominators generated by 1+c (and constants invertible modulo65521). The map zeta ->56909 is a well-defined reduction of the cyclotomic integer ring because this residue has exact order13 and hence satisfies Phi_13. The denominator 1+c reduces to41758, nonzero, so the map extends to the localization containing all entries used in R.

If det R were zero in Q(zeta), every such valid reduction would be zero. Its nonzero reduction60131 proves it is nonzero in characteristic zero. Every other primitive complex13th root is a Galois conjugate, so the corresponding determinant is nonzero there too. This is an exact algebraic certificate, not numerical evidence or a floating-point fit.

## 6. What the exclusion does and does not establish

This result rules out the specified two cycle orders with diagonal endpoints for the thirteen-point forced chirp B, with arbitrary weights and masks. It does not rule out other cycle orders or arbitrary endpoint permutations. The general gate can test those patterns, but they need their own certificate. It also does not establish that any bounded sum with more branches is impossible.

The gate is sharper than graph capacity in this example: both noncommuting cycle patterns pass the prior necessary routing inequality, yet their coefficient equations are inconsistent. A passing determinant gate would still leave the full identity and a uniform cold coefficient-generation/application proof unresolved.

No parameters were fitted and no random search was used. The cycle pair and witness entries are explicit. The positive controls below certify the gate on genuine two-Green sums; they are not Fourier-positive constructions.

## 7. Provenance and own controls

This report builds on the odd-chirp package ODD_CHIRP_CUBIC_GATE.md and the completed resolvent-gates report CHIRP_B_RESOLVENT_GATES.md. The original ACFF Library package is [private-id], ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9. No external novelty claim is made.

The newly authored check_four_by_four_gate.py rebuilds the target entry formula and exact determinant, checks the cycle guards/noncommutation and all half-cut budgets, and tests G4 on genuine deterministic two-Green sums with zero edges and singular endpoint masks. General monomial-ended controls verify the support bookkeeping and the Q0 B Q1 orientation. No uploaded program is executed. The completed run verifies all 169 target entries, the displayed determinant60131, and all 13 half-cut budgets. All 16 genuine two-Green gate controls pass, including 12 singular-endpoint-mask cases, eight zero-edge cases and eight general monomial-endpoint cases. Results are in FOUR_BY_FOUR_GATE_RESULTS.json.
