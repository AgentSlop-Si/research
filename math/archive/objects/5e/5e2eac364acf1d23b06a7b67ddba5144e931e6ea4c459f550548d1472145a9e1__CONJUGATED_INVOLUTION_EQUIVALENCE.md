# Conjugated-involution feedback: exact equivalence and the remaining synthesis equation

## Status

This is a bounded follow-on to the frozen two-Cayley report. It proves an algebraic equivalence with explicit cost conditions. It does not prove a general no-go theorem, construct Fourier-compatible factors, or claim external novelty. The original source is Annihilator-Closed Fourier Feedback, Library [private-id], ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9; its feedback and certificate conventions are retained. No uploaded code is executed.

## 1. Exact equivalence

Work over a field of characteristic not two. Let J be an involution, J^2=I, and let C,A be invertible. Choose lambda != 0 with lambda^2 != 1. Suppose

    K=BA=lambda C J C^(-1).

Then B is forced to be

    B=lambda C J C^(-1) A^(-1).                         (1)

Define

    Delta=lambda J(I-lambda J)^(-1)
         =(lambda J+lambda^2 I)/(1-lambda^2).

Since J and I-lambda J commute, the ordering inside this definition is immaterial. No such commutation is assumed for C, A or B. The feedback transfer is exactly

    T=(I-BA)^(-1)B
     =C Delta C^(-1) A^(-1).                            (2)

Proof: I-K=C(I-lambda J)C^(-1), and substitute (1). This proves (2) without interchanging A^(-1) with C or with Delta.

If J is a supplied diagonal sign matrix, Delta is diagonal, with entries lambda/(1-lambda) on the +1 coordinates and -lambda/(1+lambda) on the -1 coordinates. Both entries are nonzero. For an arbitrary supplied involution J, Delta is instead an explicitly cheap affine function of J if J is cheap. Writing it as a diagonal matrix would additionally require an available diagonalizing representation; the abstract fact that J is diagonalizable does not supply a cheap basis change.

The minimal polynomial of K divides z^2-lambda^2. It is exactly quadratic when J is not scalar. H=I-K is invertible by the lambda guard. With A invertible, B and T are invertible too.

For a specified invertible target F, Fourier or otherwise, the following equations are equivalent:

    T=F,
    F A=C Delta C^(-1),
    A=F^(-1) C Delta C^(-1).                            (3)

Thus defining A by the last formula using a dense Fourier matrix is an oracle-based algebra control, not a constructive fast Fourier algorithm. The equivalence itself supplies no cheap representation of that A.

## 2. Converse and cost ledger

Conversely, suppose an actual factorization of the specified target is supplied:

    F=C Delta C^(-1) R,

where Delta has the form above and C,R are invertible. Set

    A=R^(-1),
    B=lambda C J C^(-1) R.

Then BA=lambda CJC^(-1) and the feedback transfer is F. This converse is exact. Admissibility and algorithmic cost remain separate requirements.

There are two cost statements, and they must not be confused.

1. Starting from cheap A and B plus the proved closure, the original evaluator applies B once, A once and B once, followed by O(N) vector arithmetic. It costs O(cost(A)+cost(B)+N), including a constant factor on B, without needing A^(-1), C or C^(-1) at runtime. Constructing all plans and lambda remains charged.
2. Starting from a factorization representation, direct evaluation of (2) costs

       cost(A^(-1))+cost(C^(-1))+cost(Delta)+cost(C).

   For diagonal J, cost(Delta)=O(N). For an arbitrary cheap J it is O(cost(J)+N). This is O(N) only when all four actions and their preparation are uniformly O(N). Cheap forward application of A alone does not establish that its inverse has an O(N) representation or preparation algorithm.

Similarly, constructing B via (1) requires an implementation of A^(-1), C^(-1), J and C, or a separate simplification proving B cheap. Even if each constituent is cheap, their product need not belong to the source's specific sum-of-two-Green-plans class. Membership must be proved rather than inferred from aggregate linear-time cost.

Therefore known-cheap conjugation plus known-cheap inverses recasts the question as a constant-length Fourier factorization. It does not automatically solve that factorization. However this is not a lower bound or a proof that conjugation can never help: finding such a uniform factorization would itself be a constructive result.

## 3. Why simply using two noncommuting Cayley orders loses quadratic closure

Let W,V be weighted even Hamiltonian cycles sharing a parity involution J:

    J W J=-W,   J V J=-V.

Let U=(I+aW)(I-aW)^(-1), Z=(I+bV)(I-bV)^(-1), with all positive and negative denominator guards. Then

    J U J=U^(-1),  J Z J=Z^(-1).

The direct two-paired-Green ansatz A=U, B=lambda ZJ has loop

    K=lambda Z U^(-1) J,

and its square is

    K^2=lambda^2 Z U^(-1) Z^(-1) U.                    (4)

The order in (4) is essential. Consequently

    K^2=lambda^2 I  if and only if  U Z=Z U.             (5)

Independent cycle order alone therefore does not preserve the previously constructed involutive closure. If the two Cayley actions genuinely fail to commute, this ansatz fails the claimed annihilator identically; no numerical search is needed.

For nonzero a,b in characteristic not two, the Cayley transform is invertibly rational:

    W=a^(-1)(U-I)(U+I)^(-1),
    V=b^(-1)(Z-I)(Z+I)^(-1).

The denominators U+I and Z+I are invertible under the existing guards. Thus U and Z commute if and only if W and V commute. Accidental commuting Cayley transforms cannot rescue genuinely noncommuting W,V in this nonsingular nonzero-parameter setting.

## 4. An explicit noncommuting closure control, without a supplied four-plan realization

One can force a noncommuting-order closure without a Fourier oracle, provided one allows a longer constant product of scans. For every even N>=6 over characteristic zero, let P be the natural row shift and Q=sigma P sigma, where sigma swaps coordinates 2 and 4. Both cycles alternate natural parity. They do not commute: in row zero, PQ selects coordinate 4 and QP selects coordinate 2.

Set

    U=(I+2P)(I-2P)^(-1),
    Z=(I+3Q)(I-3Q)^(-1),
    C=U Z,
    J=diag((-1)^i),
    A=U,
    B=2 C J C^(-1) U^(-1).

All positive and negative Cayley denominators are nonzero at every even N over characteristic zero. U and Z genuinely do not commute. Nevertheless BA=2 C J C^(-1), so the loop has exact minimal polynomial z^2-4. Every factor and inverse is a bounded number of explicitly generated Green scans, so construction and application cost O(N). This is an honest noncommuting, quadratic-closure control with no FFT hidden in its definition.

It is not supplied as a Fourier candidate: B has a composition of five Cayley factors and a diagonal. No admissible sum-of-two-Green realization is supplied; the longer representation does not prove non-membership in that class. Furthermore its chosen orders retain a simple rank obstruction. For the first N/2 coordinates when N>=10, sigma preserves the cut and both P,Q cross it once in each direction. Each Cayley action and inverse has off-diagonal cut rank at most one: the identity term contributes zero, and the complementary off-diagonal rank of a Green inverse equals that of its sparse denominator, whose crossing rectangle has one edge. Equation (2) contains five such actions with an intervening diagonal, so its output cut rank is at most five. The corresponding Fourier block has rank N/2 by Vandermonde. Hence this particular control cannot equal Fourier for even N>=12. Noncommutation plus low degree is not a phase certificate.

This control is included to separate two issues precisely: obtaining a known low-degree noncommuting loop is possible with cheap conjugation; obtaining the Fourier phases in the required four-plan class is the unresolved step.

## 5. Concrete unresolved equation in the requested architecture

Choose a uniform cheap conjugation C and a fixed nonscalar diagonal J. The remaining synthesis task is to find an A such that both

    A is a sum of two allowed independently ordered Green plans,
    lambda C J C^(-1) A^(-1) is also a sum of two such plans,

and simultaneously

    F_N A=C Delta C^(-1).                              (6)

All coefficients, orders, inverse representations or cancellation formulas must be produced within the cold cost budget. An equivalent Fourier-free statement replaces (6) by the source's covariance and seed equations for T=C Delta C^(-1)A^(-1):

    D C Delta C^(-1)A^(-1)
      = C Delta C^(-1)A^(-1) S,
    C Delta C^(-1)A^(-1)e0=ones.

Quadratic closure is already automatic here; equations (6) and paired-Green membership are not. No construction solving them is established in this note.

## 6. Own exact checks

The newly authored check_conjugated_equivalence.py tests the conjugation equivalence, noncommutation, exact nonscalar quadratic closure, direct-ansatz commutator formula and failure of direct-ansatz quadratic closure at six even sizes over F998244353. It also tests the stated cut-rank bound and Fourier rejection at supported dyadic sizes. Dense matrices are used only to check these explicit formulas. All six conjugation, noncommutation, commutator-formula and direct-ansatz-rejection controls pass, together with four cut bounds and three Fourier rank checks. Counts are recorded in CONJUGATED_RESULTS.json. F65537 was rejected for this control at N=32 because 2^32=1 in that field, making a required Cayley denominator singular; the successful run uses F998244353 and explicitly checks the guards.
