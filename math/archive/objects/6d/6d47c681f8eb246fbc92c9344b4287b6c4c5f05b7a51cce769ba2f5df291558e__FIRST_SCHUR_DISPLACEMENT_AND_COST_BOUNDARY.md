# First-Schur displacement identities and a scoped chart failure

## Result

The first reduced marked-tree border has an exact Sylvester displacement identity, including its two scalar-border generators and every right-input and left-marker term. It does not yield bounded displacement rank for the following explicitly supplied natural operators:

- Natural forward weighted shifts, including distinct wrap parameters on the left and right: the reduced upper block has displacement rank at least N/16 over the rational-function field, for N>=16.
- Either nonzero weighted doubling tree, j -> 2j or j -> 2j+1: its commutator displacement rank is at least N/32, for N>=32.
- A Stein displacement with any rank-at-most-half-dimensional tree factor: every invertible target has displacement rank at least half its dimension.

The first two bounds persist for the guarded inverses and the full scalar-bordered systems. They are rank bounds for these specified displacement charts, rather than arithmetic lower bounds. Other supplied operators, coordinate changes, block displacement schemes or specially structured generators remain open.

A fully charged formal coefficient recurrence uses the previously proved linear-work constant-input jet primitive once per degree. It gives O(N log N) work through degree log2 N, with up to O(N log N) carried coefficient storage. Thus this direct recurrence reaches the known FFT work scale. It supplies neither a sub-N-log-N solve nor a new lower bound for Fourier circuits.

All previous frozen reports and seals remain unchanged. This is an additive bounded synthesis of the pole-free and one-Schur reports in iteration_10_marked_tree. No uploaded code was executed.

## 1. Field, operators and first reduced border

Let N=2^n>=8, m=N/2 and l=N/4. Work over a field K containing a supplied primitive Nth root omega. Its characteristic is not two. Scalar z can be an indeterminate; rational identities below hold in K(z), and the relevant formal series are based at z=0.

Use the previously specified maps

    A_0 e_s=e_(2s mod N),
    A_1 e_s=omega^s e_(2s+1 mod N),
    Q=A_0+A_1,
    K_0(z)=sum_(a=0)^(n-1) z^a(A_0^a-e_0 1_N^T),
    J e_j=e_(2j+1),
    (C x)_r=omega^r(x_r-x_(r+m)).

Here K_0 is the regularized polynomial tree kernel, not the field K. Let H=C K_0 J, and split its rows and columns into even and odd interface coordinates. Write

    F=H_EE,  G=H_EO,  R=H_OE,  T=H_OO,
    D=I_l-zT,  W=D^(-1),
    S=I_l-zF-z^2 G W R,
    beta^T=-z 1_l^T-z^2 1_l^T W R,
    M=[[S,-e_0],[beta^T,1-z]].                         (1)

The maps R and T do not depend on z:

    R e_j=omega^(4j+1)e_(2j mod l),
    T e_j=omega^(4j+3)e_(2j+1 mod l).

The determinant of D is q(z)=1-z omega^(-1). Thus q!=0 is the scalar-parameter tree-pivot guard. It has constant term one, so W exists as a formal series. Both S(0)=I_l and M(0)=[[I_l,-e_0],[0,1]] are invertible. A numerical inverse of S or M requires its own determinant guard; the D guard alone is insufficient.

## 2. Every source and marker survives the reduction

For arbitrary constant input x and marker h, define

    f=C K_0 x,  sigma=1_N^T x,
    g=f_E+z G W f_O,
    s=sigma+z 1_l^T W f_O,
    a_E=z h^T K_0 J E,  a_O=z h^T K_0 J O,
    p^T=a_E+z a_O W R,
    c=h^T K_0 x+a_O W f_O.

Here E,O are the coordinate injections into even and odd length-m interface coordinates. Then the exact marked identity is

    M[e;t]=[g;s],
    h^T(I-zQ)^(-1)x = c+[p^T,h_0] M^(-1)[g;s].         (2)

The eliminated odd vector is o=W(f_O+zR e), and global recovery is

    u=E e+O o,
    y=K_0 x+zK_0 J u+t e_0.

The scalar c includes the eliminated-marker correction. Omitting it, beta, the source s or the final marker h_0 changes the problem. At scalar z, the displayed source, marker, recovery and tree operations cost O(N) with q guarded. Transposed applications use the transpose of the same linear straight-line programs, so require the same order of arithmetic; this does not assert a fast M inverse.

## 3. Exact Sylvester identity and conditional generators

Let X_L,X_R be explicitly supplied l-by-l operators on the retained coordinates, and let Y be any explicitly supplied l-by-l operator on the eliminated coordinates. Define

    Delta_F=X_L F-F X_R,
    Delta_G=X_L G-G Y,
    Delta_R=Y R-R X_R,
    Delta_T=Y T-T Y.

A direct product calculation gives

    X_L S-S X_R
      =X_L-X_R-z Delta_F
       -z^2[Delta_G W R+G W Delta_R+z G W Delta_T W R]. (3)

The noncommuting resolvent step is

    YW-WY=z W(YT-TY)W.

No interchange of G,R,T or their inverses is used. In particular, choosing Y=T can simplify one term, but does not prove that the other three residuals have low rank.

For a supplied scalar chi, set Xbar_L=diag(X_L,chi) and Xbar_R=diag(X_R,chi). The full border satisfies

    Xbar_L M-M Xbar_R
      =[[X_L S-S X_R, -X_L e_0+chi e_0],
        [chi beta^T-beta^T X_R, 0]].                  (4)

The last column and last row give two explicit rank-one border terms. The source and marker in (2) are retained alongside (4); they are not absorbed into a claim about an unmarked determinant.

For completeness, if the four residuals in (3) are provided as U_i V_i^T, and X_L-X_R=U_0 V_0^T, then (3) factors into the concatenated pairs

    (U_0,                       V_0^T),
    (-z U_F,                    V_F^T),
    (-z^2 U_G,                  V_G^T W R),
    (-z^2 G W U_R,              V_R^T),
    (-z^3 G W U_T,              V_T^T W R).            (5)

At one guarded scalar parameter, processing generators of total length r through (5), including transpose operations, takes O(Nr+N) work and at most O(Nr) explicit coefficient storage. This assumes the input generators are actually supplied or their construction is separately paid. It is not an O(N) assertion when r grows. A short implicit program for a residual matrix is not the same as a bounded-length outer-product generator.

When S is invertible,

    X_R S^(-1)-S^(-1)X_L
       =-S^(-1)(X_L S-S X_R)S^(-1),                  (6)

and similarly for M. Therefore inverse displacement has exactly the same rank, with the two operators swapped. Producing inverse generators by (6) requires solves with S or M; treating those solves as generator preprocessing would hide the unresolved operation.

## 4. Two Taylor coefficients isolate the obstruction

Let E0=e_0 1_l^T and introduce the explicit append-01 map

    V e_j=omega^(8j+2)e_(4j+1 mod l).                 (7)

This V is unrelated to the transpose factors V_i in (5). The first coefficients of the blocks are

    F(0)=G(0)=-E0,
    [z]F=V-E0.

Consequently

    S(z)=I_l+z E0+z^2(-V+E0+E0 R)+O(z^3).            (8)

To verify the phase, start from global index 4j+1, apply A_0 once, and then C. The global position is 8j+2 modulo N. Reduction through the half-difference in C gives coefficient omega^(8j+2) and retained row 4j+1 modulo l. Crossing a half contributes exactly the sign already included by omega^(N/2)=-1. The subtracted root projection contributes -E0.

All extra terms in the z and z^2 coefficients of (8) have only row zero. This makes an exact leading-minor proof possible without evaluating a rational determinant at random z.

## 5. Weighted forward shifts, including distinct wrap guards

Assume l>=4. Supply nonzero c_0,...,c_(l-2), and arbitrary wrap values phi,psi. Let

    Z_phi e_j=c_j e_(j+1)  for j<l-1,
    Z_phi e_(l-1)=phi e_0,

and define Z_psi with the same internal weights and wrap psi. Both nilpotent and cyclic shifts are allowed. Consider Z_phi S-S Z_psi.

Select rows 4i+2 and columns j, for 0<=i,j<l/4. The degree-zero coefficient vanishes there: Z_phi-Z_psi has only row zero. The degree-one coefficient also vanishes because Z_phi E0-E0 Z_psi has rows only zero and one.

At degree two, the root terms again contribute only those rows. The product V Z_psi has support only in rows congruent to one modulo four. The remaining term -Z_phi V has, on the selected minor, exactly

    diagonal_j = -omega^(8j+2)c_(4j+1),
    off-diagonal entries = 0.                        (9)

All selected weights are internal, since 4j+1<=l-3. They are nonzero. Thus the determinant of this l/4 square minor has a nonzero coefficient at degree 2(l/4), and

    rank_(K(z))(Z_phi S-S Z_psi)>=l/4=N/16.           (10)

This includes the standard distinct-wrap Toeplitz-type Sylvester chart, so the obstruction is not merely the nonuniqueness of a same-operator commutator. It also includes arbitrary supplied common nonzero edge weights. Formula (6) transfers (10) to the guarded inverse. Formula (4) transfers it to the full border and its guarded inverse, because the upper-left residual remains a submatrix.

These are formal/generic ranks. A particular scalar parameter can lower the rank; z=0 is an explicit example. They do not assert the lower bound at every allowed z.

## 6. Either natural weighted doubling-tree commutator

Assume l>=8. For b=0 or 1 and supplied nonzero c_j, put

    X_b e_j=c_j e_(2j+b mod l).

The products X_b V and V X_b have output residues respectively 2+b and 4b+1 modulo eight. These residues differ for b=0 and b=1. The root-row terms in the commutator with (8) have rows only zero and b.

Select rows 8i+2+b and columns j, for 0<=i,j<l/8. Degrees zero and one vanish. At degree two, -X_b V gives a nonzero diagonal with entries

    -omega^(8j+2)c_(4j+1),

while V X_b and all root terms vanish on those rows. Hence

    rank_(K(z))(X_b S-S X_b)>=l/8=N/32.               (11)

The supplied first-pivot weighted ones-tree is a special case. These bounds also persist for S^(-1), the scalar-border extension diag(X_b,chi), and the inverse of that full border. The N=8 and N=16 cases are still well-defined controls, but (11) is claimed only when l is divisible by eight.

This does not cover an arbitrary long-word tree, a changed coordinate system or every possible left/right pair of distinct tree maps. No such classification is claimed.

## 7. Stein rank and the information lost by singular-tree Sylvester maps

Two elementary limits prevent replacing the preceding charts with an unexamined singular-tree displacement.

First, for every invertible l-by-l A and arbitrary X,Y,

    rank(A-XAY)>=l-rank(XAY)>=l-min(rank X,rank Y).    (12)

A nonzero weighted doubling map has rank l/2. Thus a Stein displacement with either such tree factor has rank at least l/2, regardless of the other factor. For a bordered tree diag(X,chi), rank is at most l/2+1, so the (l+1)-dimensional Stein residual still has rank at least l/2. This statement also applies to invertible inverse targets.

Second, if X and Y are rank-l/2 doubling trees, the map A -> XA-AY has a kernel containing every

    A=U Z V^T,
    XU=0,  V^T Y=0,

where U,V have l/2 independent columns. These give at least l^2/4 independent invisible matrix directions. This is an information bound for the displacement equation on unrestricted matrices, not a lower bound on storing our particular S.

An explicit same-tree control is available. For X_b as in Section 6, take

    u=e_0/c_0-e_(l/2)/c_(l/2),  v=e_(1-b).

Then X_b u=0 and v^T X_b=0; the nonzero rank-one matrix uv^T has zero displacement. Appropriate source and marker coordinates detect its nonzero entry. Low residual rank alone therefore does not specify the requested marked operator unless the homogeneous part is separately supplied with a paid representation.

## 8. Costed formal recurrence and why it reaches the FFT scale

Write M(z)=sum_(d>=0) M_d z^d and b(z)=[g(z);s(z)]. The constant matrix has the explicit inverse

    M_0^(-1)=[[I_l,e_0],[0,1]].

The unique formal solution v(z)=sum_j v_j z^j obeys

    v_j=M_0^(-1)(b_j-sum_(d=1)^j M_d v_(j-d)).        (13)

One can implement (13) online: after finding the constant vector v_j, compute the complete required jet M(z)v_j using the sealed constant-input one-Schur primitive, subtract its positive-degree coefficients from future residuals, and continue. Each such action costs O(N) arithmetic and coefficient routing through degree n. In particular the two-run feedback is evaluated by its shrinking quotient states, not by an N-by-n dense sweep. The single-tree lower-border series is obtained by weighted tree propagation, with at most O(l+n) state visits through degree n. Root tables are prepared once in O(N).

There are n+1 solved vectors, so this algorithm has an O(N(n+1)) work upper bound. Dense accumulated residual/unknown coefficient arrays can use O(N(n+1)) storage; the argument does not claim they stay within the first-stage 6N slots. Applying M_0^(-1), all accumulation and the carried input coefficients fit within the same bound. This is an upper bound for an actual coefficient schedule; no smaller uniform cost has been proved.

The marker can be handled at the same cost: each already determined constant v_j is contracted against its shifted marked coefficient jet. That jet is supplied by the previously proved O(N) constant-input bilinear tree/two-run programs. Summing n+1 such contractions is O(N(n+1)). This retains arbitrary x and h and never applies a constant-input bound directly to a free polynomial unknown.

After global recovery, the degree-n output is Q^n x. The original stationary graph already evaluates this by n sparse Q applications in Theta(Nn) work, followed by the supplied Fourier reversal/phase correction. Thus (13) exposes an ordinary N-log-N coefficient computation in another representation. It is not a growing asymptotic improvement. A faster retained inverse or a faster marked top-coefficient contraction remains an additional, unsolved primitive.

## 9. Primary literature and solver scope

Bostan, Jeannerod, Mouilleron and Schost define Sylvester/Stein generators and explicitly condition their use as a succinct representation on invertibility of the displacement operator. Their structured algorithms use specified companion-block classes and include generator-product and polynomial-arithmetic costs. The paper also records rank preservation for inverse matrices with swapped displacement operators. These facts do not give a constant-cost solve from a low rank alone. See their [primary paper, Sections 1 and 2](https://arxiv.org/pdf/1703.03734).

Nevanlinna's [primary paper on Sylvester equations](https://arxiv.org/abs/1904.07549) discusses unique recovery under disjoint spectra. The explicit kernel in Section 7 supplies the needed obstruction here directly over the present field, without importing a complex analytic solver or stability claim.

No published structured solver is asserted to improve this reduced problem. The exact identities and lower bounds above are proved in this report; no novelty or historical-priority claim is made.

## 10. Exact finite controls and frozen companions

The fresh standard-library verifier uses GF(65537) with primitive roots for N=8,16,32,64,128. It checks:

- 30 formal leading-minor certificates, with unit/varying shift weights, wrap pairs (1,1),(0,1),(2,3), and both weighted doubling trees;
- 160 scalar displacement identities at z=0,1,2,3, including a noncommuting intermediary Y, the full boundary terms, inverse rank identities whenever guarded, and the tree Stein bound;
- 16 full-space recovery and arbitrary-marker identities through N=64;
- 10 explicit nonzero rank-one matrices invisible to the supplied tree displacement;
- three coefficient-by-coefficient formal solution recurrences at N=8,16,32 with arbitrary polynomial sources.

The per-edge powers and dense finite-field inverses in the checker are bounded verification oracles. They are not claimed to be the root-table/quotient-state implementation in the work proof. The all-size rank bounds follow from the nonzero leading minors, rather than extrapolating scalar samples.

Companions: verify_schur_displacement.py, SCHUR_DISPLACEMENT_CONTROLS.json, PRIMARY_DISPLACEMENT_SOURCES.json, SCHUR_DISPLACEMENT_SHA256SUMS.txt.
