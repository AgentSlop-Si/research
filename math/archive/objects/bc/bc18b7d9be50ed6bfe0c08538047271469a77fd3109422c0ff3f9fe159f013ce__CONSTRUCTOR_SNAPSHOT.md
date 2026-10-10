# Changing the interface: cheap gauges and an admissible sixteen-point control

9 October 2026. Exact constructions and narrowly scoped obstructions. No all-size paired-Green Fourier factorization or new FFT speedup is established. No uploaded code or numerical parameter scan was used.

## 1. Useful results

- Changing Q changes the unique exterior P. If the induced bank-conjugated change and its inverse are cheap, the previous batched-Fourier equivalence survives.
- Constantly many bank-coordinate swaps may create dense O(m^2) transport blocks while retaining O(N) total interface entries for a square split. They nevertheless induce cheap rank-one gauges, so they do not escape that equivalence.
- For monomial Q, demanding a monomial active clock action forces each active block's original coordinates to form an arithmetic-progression coset modulo q. This is a narrow rigidity theorem, not a restriction on all O(N)-nonzero interfaces.
- A genuinely different full-bank interface has P equal to grid transpose and Q equal to a twiddled Fourier batch. All four interface actions are monomial. At N=16, m=q=4, Q is exactly two legal zero-mask paired-Green layers, giving an explicit admissible four-layer exterior construction.
- In that relocated-work family, two zero-mask layers cannot realize Q when m>4. General nonzero Green layers are not excluded. The larger-size Fourier work has moved into Q rather than disappeared.

## 2. Exact interface-change formula and its cost consequence

Keep the same invertible bank B and a baseline factorization F=P_0 B Q_0. For any new invertible Q, write Q=GQ_0. Exact equality forces

    P=P_0 C,             C=B G^-1 B^-1,
    C^-1=B G B^-1.                              (1)

This is operator uniqueness for the newly chosen Q, not a search prescription. If C and C^-1 both have explicit O(N) preparation and application algorithms, then P and P_0 are cost-equivalent up to O(N). The earlier batch reductions therefore remain valid for P.

Cheap application of G alone is insufficient. G^-1 may not be cheaply applicable, and even when G is monomial with an O(N) inverse, its bank conjugate can contain Fourier work. Inverses of paired-Green sums are not assumed to be cheap. Any claim that a new interface is advantageous must pay for these maps or provide the new exterior factors directly.

For actual transport, T_g=G T_(0,g) G^-1 and A_g=C^-1 A_(0,g) C. Thus non-scalar interface changes are allowed, but they change the generator data; they are not centralizer freedom of the already-fixed CT pair.

## 3. Monomial-clock rigidity

Use the positive Fourier convention, N=mq, eta=omega^q. Suppose Q is monomial, with

    Q e_(sigma(b,s))=lambda_(b,s) e_(bm+s),

where sigma is a permutation and every lambda is nonzero. Then T_2=Q D_N Q^-1 is diagonal, with block b equal to diag(omega^(sigma(b,s))). The diagonal weights lambda cancel.

On an active bank block the clock equation is

    A_(2,bb)=F_m diag(omega^(sigma(b,s))) F_m^-1.

If this block is monomial, then there are an integer a_b coprime to m and a residue e_b such that

    sigma(b,s)=e_b+q a_b s mod N.                (2)

Proof. A Fourier conjugate of a diagonal matrix is circulant. An invertible monomial circulant is c S_m^a for some nonzero c. Conjugating back gives diag(c eta^(-as)); evaluating at s=0 shows c=omega^(sigma(b,0)). Since omega has exact order N, equality of these roots gives sigma(b,s)=sigma(b,0)-qa s modulo N. Injectivity in s forces gcd(a,m)=1. Rename -a as a_b. QED.

Thus each active block draws exactly one full residue-class coset modulo q, in an affine order. Distinct active blocks use distinct cosets. For a full bank all q cosets occur, so the permutation part of Q is the stride layout up to bank permutation and within-bank affine permutations.

Scope matters. This uses a monomial clock block, not merely O(N) total entries. It says nothing about the arbitrary nonzero diagonal weights lambda, whose bank conjugates can still be expensive. It also does not cover nonmonomial Q. Relaxing a clock block to a dense exceptional block is a real way around this geometric conclusion, although it need not improve evaluation cost.

## 4. Constant coordinate swaps: more interface entries, but a cheap gauge

Let G exchange two bank coordinates a,b and fix the others. Set v=e_a-e_b. Then

    G=I-vv^T,             G^-1=G,
    C=B G B^-1=I-u w^T,
    u=Bv,                w^T=v^T B^-1.            (3)

C is an involution. Each of u,w is supported in at most two bank blocks. Fourier columns/rows and identity columns/rows produce them explicitly in O(m) supplied-root work. Applying C requires one O(m)-length inner product and one O(m)-length update; the untouched coordinates are passed through. Thus C and its inverse cost O(N) including input/output handling, with only O(m) nontrivial arithmetic. No dense m-by-m multiplication or Fourier transform is needed.

A constant number of swaps yields a product of such cheap conjugated involutions. This remains a cheap reversible gauge under (1), even if the swapped coordinates break the coset condition (2).

For the CT monomial interface T_(0,g), conjugating by a transposition changes only O(1) scalar entries: changed rows and columns of a monomial matrix contain only constantly many entries. Conjugating each resulting elementary matrix E_ij by B gives an outer product supported in one bank-block rectangle, with at most m^2 entries. Therefore a constant number of swaps produces only O(1) exceptional rectangles in A_g. In a square split their total storage is O(m^2)=O(N), although their maximum row or column degree can be m.

This is an explicit distinction between total sparsity and maximum degree, and between dense coefficient storage and application work. The new interface may have dense blocks, but the gauge is low-rank and cheap. It supplies no faster exterior than the baseline. General paired-Green membership of P_0 C is not inferred from cheap application of C.

## 5. A different full-bank interface with monomial P

Let N=M^2, B=I_M tensor F_M, L=F_M tensor I_M, and let K transpose the M-by-M coordinate grid. Let Delta[ rM+s ]=omega^(rs). Positive Fourier symmetry, or a direct entry expansion, gives

    F_N=K B Delta L.                             (4)

Choose

    P=K,                 Q=Delta L.

P now has one nonzero per row and column. It does not itself evaluate the missing Fourier batch. Q does: applying Q is exactly equivalent to M independent arbitrary-input length-M DFTs, up to an invertible O(N) twiddle multiplication. The previous P-alone equivalence has genuinely changed location.

The actual interface actions are still maximally sparse. For g=1, let (X_1,Y_1)=(S_N,D_N); for g=2, let (X_2,Y_2)=(D_N,S_N^-1). Then

    A_g=K Y_g K,             T_g=B^-1 A_g B.

In bank coordinates b,s:

- A_1 has diagonal block omega^b D_M; T_1 has block omega^b S_M.
- A_2 sends bank b to b-1 modulo M, with I_M on nonwrap edges and S_M^-1 on the edge 0 -> M-1.
- T_2 has the same bank routing, with I_M on nonwrap edges and D_M on the wrap edge.

All four matrices are monomial, and A_g B=B T_g exactly. This is allowed because the bank is full; no proper-active-subspace obstruction applies. Sparse interface actions do not certify that both exteriors have cheap allowed realizations.

## 6. Explicit admissible N=16 realization

Set M=4. Let zeta be a primitive fourth root, and define four-by-four matrices

    E_h=diag(1,1,-1,-1),      Pi_h e_j=e_(j xor 2),
    E_l=diag(1,-1,1,-1),      Pi_l e_j=e_(j xor 1),
    Delta_4=diag(1,1,1,zeta),

with K_2 the two-by-two-grid transpose permutation on four coordinates. Then

    A_4=(E_h+Pi_h) Delta_4,
    C_4=(E_l+Pi_l) K_2,
    F_4=A_4 C_4.

Each A_4 and C_4 is a sum of two nonsingular monomials. Consequently, for N=16, take

    H_1=C_4 tensor I_4,
    H_2=Delta_16 (A_4 tensor I_4),
    H_3=(1/2)I_16+(1/2)I_16,
    H_4=(1/2)K+(1/2)K.

H_2 H_1=Delta_16 (F_4 tensor I_4)=Q and H_4 H_3=K=P. Thus

    F_16=H_4 H_3 (I_4 tensor F_4) H_2 H_1.        (5)

Every summand is a permitted monomial-ended Hamiltonian Green term: choose any Hamiltonian permutation pi, set all edge weights to zero, so U=I-D_0 P_pi=I and the denominator guard is 1, and put the displayed monomial in one endpoint with I in the other. Every endpoint is nonsingular. Characteristic is not 2 in the dyadic contract, so the displayed halves are legal. Independent Hamiltonian orders may be selected even though zero masks make their order irrelevant.

This is an exact small admissible construction using all four prescribed paired layers and a full Fourier bank. It uses the familiar two radix-2 stages for Q, not an uncharged dense solve. Each exterior application is O(16) arithmetic with supplied roots, and the four length-four bank transforms are charged. There is no claim that these fixed sixteen-point factors lift uniformly to larger M.

### Narrow obstruction to that zero-mask extrapolation

If a paired layer has zero masks in both terms, it is a sum of two monomials and has at most two nonzeros in every row. A product of two such layers has row degree at most four. But Q=Delta(F_M tensor I_M) has exactly M nonzeros per row. Therefore this relocated-work family's Q cannot be represented by two zero-mask paired-Green layers when M>4. More generally t such layers require 2^t>=M.

This is a support bound for zero-mask monomial-sum layers. It is not a lower bound for nonzero Green layers, which can be dense while retaining linear-time cyclic solves. It also does not prohibit another choice of P,Q.

## 7. What interface freedom could still matter?

A construction can change Q nonmonomially and move work between exteriors, as (4) demonstrates. A monomial change can also alter the active coset geometry if one allows nonmonomial clock blocks. Neither by itself supplies a speedup.

The cheap-gauge theorem rules out claiming progress merely from changes whose bank conjugates and inverses are already linear-time applicable. Constant coordinate swaps are a concrete example. To escape that equivalence in a useful way, one must exhibit new P and Q that are both uniformly generated and cheaply applicable in the permitted paired-Green family, rather than treating an unevaluated bank-conjugated gauge as free. Such a construction might have no cheap conversion to the old fixed interface, but its actual factor application costs must be paid directly.

The sixteen-point example validates the new nonmonomial-Q interface and the family constraints. Its scalable unresolved task is exactly a cheap realization of the arbitrary-input batch inside Q, or a different split where neither exterior merely hides that missing batch. No such larger-size realization is established here.

## Exact controls

`verify_changed_interface.py` is independently authored and executes no uploaded code. It checks (4), all four monomial transport actions, their two exact intertwining equations, the explicit N=16 factors and zero-mask term decomposition, monomial-clock coset controls, and the rank-one coordinate-swap gauge. Results appear in `CHANGED_INTERFACE_CONTROLS.json`; the accompanying proofs establish the scope beyond the tested sizes.
