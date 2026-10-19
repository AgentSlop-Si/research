# Endpoint-anchor rank: exact Schur reduction and a uniform obstruction to its natural product lift

Date: 2026-10-19. Owner: M-SCAN-DIMENSION. Priority: unchanged, 34.

## Disposition

**The requested all-dyadic endpoint-anchor rank lemma remains unresolved.** No rational annihilator of its Jacobian has been found, and the endpoint anchor is not disproved. This packet is a bounded unresolved disposition with two new exact structural results, not completion or acceptance of that lemma:

1. Modulo 5, parity Schur decimation of the exact endpoint anchor is self-similar: it sends T_(2n) to 3 T_n. Its differential maps the entire pentadiagonal tangent onto the smaller pentadiagonal tangent, with a 5n-dimensional kernel.
2. The natural complementary pivot for composing those stagewise Schur reductions is singular at every dyadic size N>=16. Equivalently, the odd-index principal block of T_N P_N T_N has an explicit family of integer null vectors and rank exactly N/4+log2(N/4)+1 < N/2. This retains the actual bit reversal and both adjacency couplings. It rejects this particular block-elimination lift; it does **not** reject the endpoint anchor or another, differently grouped Schur proof.

In particular, the second result must not be relabeled a Jacobian annihilator or an original-chart counterexample. No new larger threshold-rank census was used. No historical program was executed, and no external write, owner change, acceptance or whole-record closure is made here.

## 1. Fixed target and source boundaries

For N=2^m>=8 let t=N/4+1, let P_N reverse all m binary digits, and let

    T_N = 3I + L_N + L_N^T + E_00,

where L_N is the subdiagonal shift. The unresolved target is row rank N^2 over Q for

    H[(r,s),(k,i,j)] = (T_N P_N)^k[r,i] (P_N T_N)^(t-1-k)[j,s],
    0<=k<t, |i-j|<=2.

Write B_2(N) for the pentadiagonal space, dimension 5N-6. The accepted original-chart equivalence, regularity guards, finite N=8,16,32 results, all-size depth-two result and the obstruction to the different centrosymmetric anchor are preserved from the sources below. In particular the present positive-definite T_N has nonzero neighbors and all leading/trailing principal minors; the mod-5 calculations are calculations on the integer sparse Jacobian, not a claim of a regular original generator chart in characteristic five.

Sources read as inert text:

- /workspace/shared/next_three_finalization_tasks_20261019_0121/PROPOSALS.md.
- /workspace/shared/bitrev_uniform_20261018_1919/candidate/REPORT.md, Sections 2-5.
- /workspace/shared/bitrev_uniform_20261018_1919/review_independent/REVIEW.md, including its good-anchor qualification.
- /workspace/shared/bitrev_uniform_20261018_1919/candidate/sources/PROOF_CERTIFICATE.md.

An explicit nonzero H_N minor modulo five would imply the required rational rank at that N. What follows supplies a potentially useful exact local recursion, followed by a proved failure of its simplest product-level implementation. It does not supply those minors.

## 2. Exact parity Schur decimation

Let Q_n send the two half-coordinate blocks to even and odd coordinates. In parity coordinates the given anchor is

    Q_n^T T_(2n) Q_n = [[3I+E_00, B], [B^T, 3I]],   B=I+L_n.

Both off-diagonal blocks are retained. Since B B^T=2I-E_00+L_n+L_n^T, its Schur complement with respect to the bottom block 3I is

    S_n = (7I+4E_00-L_n-L_n^T)/3.

Therefore, over F_5,

    S_n = 3 T_n.

There is also an exact characteristic-zero identity behind this reduction. Define

    J_n=-2I+L_n+L_n^T+E_00=-(I-L_n)(I-L_n)^T.

Then parity Schur decimation sends J_(2n) to J_n/2, in any field of characteristic different from two. Indeed its parity blocks are (-2I+E_00, B; B^T,-2I), so the Schur complement is

    -2I+E_00+(1/2)B B^T = J_n/2.

The given T_n reduces to J_n modulo five, and 1/2=3 in F_5. Notice that det J_n=(-1)^n, so this mod-5 anchor is invertible at every size. This observation does not assert that every proper principal minor is nonzero modulo five, nor require that assertion.

### The differential has the exact smaller tangent

For an arbitrary X in B_2(2n), write its parity blocks X_ee,X_eo,X_oe,X_oo. The diagonal blocks are tridiagonal; X_eo is lower bidiagonal and X_oe is upper bidiagonal. Differentiating the Schur complement gives

    dS(X)=X_ee - X_eo B^T/3 - B X_oe/3 + B X_oo B^T/9.       (1)

Every term is pentadiagonal, so dS maps into B_2(n). The map is onto in every field in which 3 is invertible:

- Set the cross blocks to zero.
- For each i=0,...,n-3, the (i,i+2) entry of B X_oo B^T is exactly (X_oo)[i,i+1], and its (i+2,i) entry is exactly (X_oo)[i+1,i]. Thus choose these entries of X_oo to supply nine times any prescribed second off-diagonals.
- The remainder is tridiagonal and is supplied by X_ee.

Consequently

    dS(B_2(2n))=B_2(n),
    dim ker dS=(10n-6)-(5n-6)=5n.

This is an exact one-stage tangent recursion. It has no product-level implication without handling the intervening P_N.

## 3. The actual boundary and the failed complementary pivot

Set N=4h, h=2^q, so n=N/2=2h. Let P=P_h, let D=I+L_h and let F=e_0 e_(h-1)^T. Use parity order at size N and then split each n-coordinate block into its two h-coordinate halves.

The exact bit-reversal boundary in parity coordinates is

    Ptilde = [[P_ee,P_eo],[P_oe,P_oo]],

with

    P_ee=[[P,0],[0,0]],   P_eo=[[0,0],[P,0]],
    P_oe=[[0,P],[0,0]],   P_oo=[[0,0],[0,P]].                 (2)

To verify (2), write an input as 2j+b with j=a h+r. Its reversal is 2(bh+rev_q(r))+a. Thus each n-by-n block has rank h, and the odd sector is not preserved by the boundary.

Factoring the full anchor, rather than discarding its coupling, gives

    Tpar=C diag(S_n,3I) C^T,   C=[[I,B/3],[0,I]].

At each product boundary the resulting matrix is K=C^T Ptilde C. Its odd-odd block G is precisely one ninth of the odd-index principal block O of T_N P_N T_N. This follows either by block multiplication or because the bottom rows of C are (0,I). Direct multiplication of (2), using B=[[D,0],[F,D]] and the fact that P fixes both endpoints, gives

    O = [[D^T P D+3(F+F^T), 3 P D],
         [3 D^T P,                 9 P]].                  (3)

Thus even after retaining and factoring both coupling blocks, the proposed complementary pivot is G=O/9, rather than an identity or an invertible copy of P_n.

### Theorem: exact pivot rank and uniform singularity

Over Q,

    rank O = rank G = h+q+1 = N/4+log2(N)-1.

Over F_5 the rank is h+q+1 when q is even, and h+q when q is odd. In particular, over either field it is at most h+q+1. For h>=4, q+1<h, so O and G are singular. This is every dyadic N>=16.

Proof. The bottom-right block 9P in (3) is invertible. Its Schur complement is

    R = D^T P D - P D P D^T P + 3(F+F^T)
      = L_h^T P L_h - P L_h P L_h^T P + 3(F+F^T).          (4)

Let U=P L_h^T P. The first two terms of (4) equal P[U,L_h]. Let

    M_q={2^b-1 : b=0,...,q}.

For any q-bit word x outside M_q, the word contains a 1 before a later 0. On the basis vector e_x, L_h performs ordinary binary increment: it changes the suffix beginning at the last 0. U performs binary decrement in reversed bit order: it changes the prefix ending at the first 1. Those prefix and suffix regions are disjoint because that first 1 precedes the last 0. Each operation leaves the other operation's stopping bit unchanged. Neither operation hits a truncated endpoint, and consequently U L_h e_x=L_h U e_x.

Hence [U,L_h]e_x=0 for every x outside M_q. The endpoint matrix F+F^T also has zero columns outside M_q. It follows that R has at most q+1 nonzero columns, so rank R<=q+1. Since rank O=h+rank R, the bound follows.

For the exact rank, order M_q as x_b=2^b-1 for b=0,...,q. Direct binary increment and reversed-decrement on these monotone words give

    (P[U,L_h]) e_(x_b) = e_(x_(q-b-1)) - e_(x_(q-b+1)),

with out-of-range terms omitted. Therefore the restriction R_M to M_q has entries

    (R_M)[a,b] = 1_(a+b=q-1) - 1_(a+b=q+1)
                 + 3(1_(a=0,b=q)+1_(a=q,b=0)).

Reverse its row order. The resulting (q+1)-square matrix is

    K_q = L_(q+1)-L_(q+1)^T + 3E_00+3E_qq.

Its diagonal is 3 at the two endpoints and zero in the interior; its lower and upper neighboring entries are 1 and -1. The leading-continuant recurrence starts d_0=1,d_1=3; at each interior row d_j=d_(j-2); and at the last row d_(q+1)=3d_q+d_(q-1). Thus det K_q is 6 for even q and 10 for odd q. Both are nonzero over Q, so rank R=q+1 there.

Over F_5, even q still gives full rank q+1. For odd q, the determinant is zero, but the leading q-square minor is d_q=3, so the rank is exactly q. The asserted field-specific ranks follow. QED.

The annihilated vectors are explicit. For every x outside M_q, put

    w_x = (3e_x, -P D^T P e_x) in Q^(2h).                  (5)

Equation (3) gives O w_x=(3R e_x,0)=0. Their first h-coordinate blocks are distinct nonzero basis vectors, so these are h-q-1 linearly independent integer null vectors. They also remain independent over F_5.

For a particularly small uniform witness, take x=2 (valid for all h>=4). Since Ue_2=e_(h-4), formula (5) is

    w_2=(3e_2,-e_2-e_(h-4)).

In the original N-coordinate odd sector its three coefficients occur at indices 5, N/2+5 and N-7, respectively, with weights 3,-1,-1. At N=16 the odd-sector vector is (0,0,3,0,-1,0,-1,0). This is a null vector of the stated principal block, **not** of T_N P_N T_N itself: that full product is invertible, and its even-coordinate output need not vanish.

### What is and is not obstructed

The natural lift would first Schur-decimate each tridiagonal stage, then eliminate the same odd-coordinate sector through the dressed intervening boundary. The latter operation requires the pivot G to be invertible. The theorem disproves that requirement uniformly, with literal integer null vectors.

It does not preclude another choice of coordinates, a larger coupled temporal block, a different elimination order, a different complementary minor, or a direct dual-observability proof. It also does not show any nonzero Z obeying all t pentadiagonal zero-band observations in the target lemma. The local recursion in Section 2 and the obstruction in Section 3 therefore leave the exact endpoint anchor unresolved.

## 4. Fresh reproducible checks

Run from this directory:

    python checks.py

The code was written for this packet, imports no historical program, and uses Python integers and Fraction only. It independently constructs bit reversal and the original tridiagonal anchor. It checks:

- The parity identity, exact characteristic-zero Schur formula, mod-5 self-similarity and the negative-Laplacian factorization.
- Formula (1) on every basis vector of B_2(2n), including support, and an explicit preimage of every basis vector of B_2(n), for n=4,8.
- Formula (3), the commutator identity (4), support on M_q, its exact reversed tridiagonal residual and determinant 6/10, the rational and mod-5 rank formulas, all displayed integer null vectors, and their independence from their first blocks, for h=2,4,8,16,32,64. These are checks of the newly proved structural identities, not threshold-Jacobian rank scans.
- At N=8, the original H_8 has full row rank 64 modulo five, while the candidate odd complementary pivot has determinant -10/81 over Q and is singular modulo five. This small positive control explicitly prevents mistaking a singular auxiliary pivot for failure of the anchor Jacobian.

RESULTS.json contains the exact control output. Finite checks support transcription; the all-size statements are proved above. No H_N rank beyond the already studied N=8,16,32 sizes was computed in this investigation, and the deliverable's rank control uses only N=8.

## 5. Remaining owner scope

M-SCAN-DIMENSION remains TO RESEARCH, priority 34. The exact missing result is still full row rank of the specified H_N at t=N/4+1 for every dyadic N>=8, or an actual rational Jacobian annihilator at one such N. The new obstruction applies only to the specified stagewise odd-sector Schur route.

The accepted good inverse-tridiagonal tangent transport, nonzero-neighbor and principal-minor guards, original finite witnesses, all-size upper bound and depth-two theorem remain intact. No claims about Fourier membership, intermediate-depth gauge completeness, coefficient synthesis, runtime savings or historical novelty follow. The proposed all-dyadic finalization gate is **not completed** by this packet.
