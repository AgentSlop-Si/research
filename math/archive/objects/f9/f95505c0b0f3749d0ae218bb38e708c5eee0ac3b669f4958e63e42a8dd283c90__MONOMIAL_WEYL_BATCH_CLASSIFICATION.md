# Monomial Weyl interfaces retain arbitrary-input Fourier batches

10 October 2026. Necessary normal form, explicit paid recovery, and a mixed-radix positive family. No novelty or faster-FFT claim is made. All earlier reports and seals are preserved.

## 1. Main result and scope

If an invertible matrix H conjugates both standard N-dimensional Weyl generators to monomial matrices, then H is a weighted and permuted direct sum of equal-length DFTs. The common length d divides N. Given the transported monomial generators, a supplied primitive root, and one nonzero calibration entry of H, the endpoint weights and routes can be recovered in O(N) exact field operations and O(N) words. No discrete logarithm, root extraction, dense H access, or Fourier evaluation is part of that recovery.

Applied to a full-bank identity F_N=P(I_q tensor F_m)Q whose four actual interface actions are monomial, this gives batch lengths d_P,d_Q dividing N with

    m d_P d_Q >= N.                              (1)

Both exteriors remain arbitrary-input Fourier batches up to cheap monomial maps. The inequality is a support constraint, not an arithmetic lower bound for evaluating those batches. For N=p^2,m=p prime, one exterior has batch length at least p. Dyadic N admits intermediate divisors and can split the missing Fourier work across both exteriors.

The normal form is necessary. Arbitrary monomial endpoints around a Fourier batch do not automatically conjugate both Weyl generators to monomials. Recovering sparse transported actions from an opaque H is also not declared cheap.

## 2. Field, conventions, and input promise

Work over a field containing a supplied primitive N-th root omega, with characteristic not dividing N. Put S e_j=e_(j+1 mod N), D e_j=omega^j e_j, so SD=omega^-1 DS. Fourier matrices use the positive unnormalized sign. Write F_d^- for the matrix with entries (omega^(N/d))^(-k l); it differs from positive F_d only by index reversal, not by an inverse normalization.

The abstract theorem assumes an invertible H and monomial matrices

    U=H S H^-1,              V=H D H^-1.

For the recovery algorithm, supply:

1. U and V as permutation arrays plus their N nonzero edge weights each.
2. omega, with the primitive-root/field promise above.
3. The promise that these are the two conjugates of the intended invertible H.
4. One nonzero seed h_0 specified below, either directly or through one paid application of H to e_0.

The promised validity of U,V is separate from solving the original factorization problem. If their construction required a dense inverse or an expensive parameter search, that preparation must still be charged. The algorithm below does not obtain U,V from a black-box H for free.

## 3. Equal clock-cycle lengths

Write

    U e_v=u_v e_(alpha(v)),
    V e_v=v_v e_(beta(v)),

with all weights nonzero. Because UV=omega^-1 VU, their permutation parts alpha,beta commute. Their joint coordinate action is transitive: an orbit span would otherwise be a proper nonzero common invariant subspace, contradicting the irreducibility of S,D. Irreducibility follows directly from the distinct D eigenvalues and the transitive cyclic shift S, over the stated field.

Alpha maps beta-cycles to beta-cycles and is transitive on their set, since beta itself never changes its own cycle. Therefore all beta-cycles have one common length d, with c=N/d cycles.

The characteristic polynomial of one weighted beta-cycle is x^d-kappa, where kappa is its edge-weight product. V is similar to D and has N distinct eigenvalues. The eigenvalues on a cycle are exactly

    {omega^(r+c l): 0<=l<d}

for one residue r modulo c. Its product kappa equals omega^(dr). Different cycles have different residues, so their products are precisely the c distinct powers of omega^d. In particular exactly one cycle has product 1. This includes d=1 and c=1 without exceptions.

Positive characteristic creates no extra degeneracy under the stated hypotheses: every d divides N, is invertible in the field, and omega^(N/d) has exact order d.

## 4. Explicit Fourier-block formula

Label the cycles by r=0,...,c-1 as above. Choose a base v_(r,0) in each and traverse beta to obtain v_(r,k), 0<=k<d. Let

    h_(r,0)=1,
    h_(r,k)=product_(t=0)^(k-1) v_(v_(r,t)).

The j-th column of H is a V eigenvector of eigenvalue omega^j, and thus lives on cycle r=j mod c. Its entries are

    H[v_(r,k),r+c l]
      =gamma_(r+c l) h_(r,k) omega^(-rk)
          (omega^c)^(-k l),                      (2)

where gamma_j=H[v_(j mod c,0),j] is nonzero. All entries outside the indicated cycle are zero. Formula (2) follows by one step of the weighted-cycle eigenvector recurrence; the wrap step follows from the cycle product.

Consequently

    H=M_out (I_c tensor F_d^-) M_in,             (3)

for explicit nonsingular monomial M_out,M_in. M_in routes column j=r+c l to block coordinate (r,l) and scales it by gamma_j. M_out scales coordinate (r,k) by h_(r,k)omega^(-rk) and routes it to v_(r,k).

Every row and column of H therefore has exactly d nonzeros, and nnz(H)=Nd. This is an exact support statement, not a runtime lower bound for an implicit evaluator.

## 5. Linear-work recovery without logarithms or root extraction

The residues r in (2) are recovered combinatorially, not by taking discrete logarithms of kappa.

1. Traverse beta's cycles once, recording their vertex lists, products, and vertex-to-cycle/index maps. Find the unique product-1 cycle and call it cycle 0.
2. Follow alpha on the cycle set to label the remaining cycles 1,2,...,c-1. The identity VU=omega UV means U sends an eigenvector of eigenvalue lambda to one of eigenvalue omega lambda, so this direction increments the residue. It visits all c cycles exactly once. No arbitrary root of a cycle product is needed.
3. Choose one base vertex in each labeled cycle, compute all h_(r,k), and generate the N powers of omega by recurrence.
4. Supply gamma_0=H[v_(0,0),0] != 0. A single paid H e_0 application yields it once the base is known.
5. For j=0,...,N-2, put r=j mod c and r'=(r+1) mod c. Find

       a=alpha^-1(v_(r',0))=v_(r,k_r).

   The identity H e_(j+1)=U H e_j gives

       gamma_(j+1)
         =u_a gamma_j h_(r,k_r) omega^(-j k_r).   (4)

Each k_r and u_a is a constant-time lookup after the cycle traversals. Each phase is a lookup in the generated omega table. The total is O(N) field operations and index operations, plus the separately charged seed access. The wrap j=N-1 provides a consistency check gamma_N=gamma_0.

All endpoint coefficients are now explicit. If inverse endpoint maps are needed, their nonzero scalar entries can be batch-inverted in O(N) field work and one scalar inversion. No N-by-N matrix is read or constructed. Writing the full matrix H from (2) would separately cost Theta(Nd) entries.

This is a promised-input recovery theorem. Monomial-array validity and the Weyl relation can be checked directly in linear work, and the cycle labels/products and wrap scalar can also be checked, but these checks do not establish that a separately proposed Green circuit implements the intended H. That circuit-to-interface relation remains part of the original certificate.

Once the maps in (3) have been recovered, an evaluator for H and an evaluator for c arbitrary length-d Fourier transforms simulate each other with O(N) extra work. The inputs remain arbitrary because the endpoint monomials are invertible. This conclusion requires the stated supplied actions and seed, or their actual preparation costs; it is not inferred merely from abstract existence.

## 6. Applying the theorem to both full-bank exteriors

Let B=I_q tensor F_m and F_N=P B Q. Define

    T_1=Q S Q^-1,           T_2=Q D Q^-1,
    A_1=P^-1 D P,           A_2=P^-1 S^-1 P.

Assume all four actual actions are monomial. Apply the theorem to H=Q using U=T_1,V=T_2. For P, avoid assuming that P^-1 is cheap: transpose the intertwining equations to get

    P^T S=A_2^T P^T,
    P^T D=A_1^T P^T.

Thus apply the theorem to H=P^T with U=A_2^T,V=A_1^T, and transpose its normal form. Fourier matrices are symmetric, and transposes of monomials are monomial, so P has the same weighted/routed batch form.

The seed for P^T is P[0,v_(0,0)], obtainable from one paid application P e_(v_(0,0)); no inverse-P or transpose-P oracle is required. If P,Q are supplied legal paired-Green circuits with O(N) application, these two seed calls cost O(N). Computing or supplying their actual monomial interface actions still needs an independently justified cost.

Let the resulting block lengths be d_P and d_Q. Each P row has d_P nonzeros, each B row has m, and each Q row has d_Q. A row of P B Q is supported on at most d_P m d_Q columns. Since every Fourier row has N nonzeros, (1) follows. Cancellation cannot increase this support.

The prime-square specialization N=p^2,m=p has d_P,d_Q in {1,p,p^2}, so at least one is at least p. This does not follow for m=2^h in the same form: d_P=2^a,d_Q=2^b can have a+b>=h with both a,b<h. The correct dyadic conclusion is the product bound and the existence of genuine batches, not a claim that one exterior always contains the entire m-point batch.

## 7. Additional full-bank routing restriction

For any monomial T with A=B T B^-1 monomial, every nonzero m-by-m block of T must be a full monomial block, and the nonzero blocks follow a permutation of the q bank blocks.

To see this, T_bc is a partial monomial matrix. If nonzero, every row of F_m T_bc is nonzero, since each used column receives one nonzero contribution. Hence F_m T_bc F_m^-1 has no zero row. The same argument with columns shows no zero column. But this block is part of a monomial A, so it must have exactly m entries. Rank preservation then forces T_bc to have exactly m entries too. No bank row can contain two such blocks.

Inside a nonzero block, both U and F_m U F_m^-1 are monomial. The entry identity F_m U=V F_m shows that U's permutation is affine s -> a s+b with gcd(a,m)=1, and its nonzero weights are a scalar times a Fourier character. This conclusion holds for composite m too; no prime-only minor theorem is being used. These are necessary interface constraints, not an evaluator for P or Q.

For completeness, write U e_j=c_j e_(pi(j)) and V e_k=d_k e_(tau(k)). Dividing the entry identity by its j=0 and k=0 instances yields

    k j=(tau(k)-tau(0))(pi(j)-pi(0)) mod m.

At k=j=1 the two differences multiply to 1, so both are units. Taking k=1 makes pi affine; the original k=0 equation gives c_j/c_0=(omega^(N/m))^(-tau(0)(pi(j)-pi(0))), a character. This explicitly accounts for composite and dyadic moduli.

## 8. Constructive dyadic family beyond the sixteen-point control

Take N=a m b with full bank of q=ab length-m transforms. Use input digits

    j=r_0+a r_1+a m r_2,
    0<=r_0<a, 0<=r_1<m, 0<=r_2<b,

and bank coordinates (r_0,t_2,r_1), at index (r_0 b+t_2)m+r_1. Define Q by a length-b transform in r_2 followed by a twiddle:

    Q[(r_0 b+t_2)m+r_1, r_0+a r_1+a m r_2]
      =omega_(mb)^(r_1 t_2) omega_b^(r_2 t_2).    (5)

Apply the bank F_m in r_1 to produce t_1. Define P by a twiddle and length-a transform in r_0, routing to k=t_2+b t_1+b m t_0:

    P[t_2+b t_1+b m t_0,(r_0 b+t_2)m+t_1]
      =omega_N^(r_0(t_2+b t_1)) omega_a^(r_0 t_0).
                                                            (6)
All unspecified entries are zero. Expanding the exponent verifies

    F_N=P (I_(ab) tensor F_m) Q.

P and Q are explicitly monomial-equivalent to batches of F_a and F_b, respectively, with degrees a,b. Their canonical partial-transform input routes show that both Weyl actions are monomial; diagonal output twiddles and output permutations preserve that property. The support product is sharp: a m b=N.

For dyadic a,b<=4, each of F_a,F_b uses at most two radix-2 butterfly layers. Every butterfly layer is a sum of two nonsingular monomials, hence a legal zero-mask paired-Green layer; padding and absorbing the displayed endpoint monomials supplies exactly two layers for each exterior. This is a uniform allowed family for fixed q=ab<=16 and arbitrary dyadic m. It gives, in particular, a balanced N=256 control with m=q=16 and a=b=4, and N=64 with m=q=8,a=4,b=2.

All twiddles and routes cost O(N) supplied-root preparation/application. The full charged transform work is

    (N/a) T(a)+(N/m) T(m)+(N/b) T(b)+O(N).

For fixed a,b this is ordinary constant-radix recursion, not a growing-radix speedup. In the square-bank regime m=q, the four zero-mask exterior layers require q<=16 by their row-support bound; N=256 attains that endpoint. Nonzero Green layers are not excluded.

## 9. Checked primary literature and provenance

Prasad and Vemuri classify the maximal abelian algebras normalized by the finite Heisenberg canonical representation through maximal isotropic subgroups (Theorem 2.4). This is classical context for a monomial basis: conjugating the diagonal algebra by H produces such a normalized algebra. Their theorem is stated for the complex unitary setting; the elementary field and cost proof above is supplied directly rather than attributed to that theorem. [Primary paper](https://arxiv.org/pdf/0803.2921).

Appleby, Bengtsson, Brierley, Grassl, Gross and Larsson explicitly describe a square-dimension phase-permutation/Zak basis and its partial Fourier change of basis F_n tensor I in Section 3. They also discuss the parity distinctions needed for the full Clifford group. Their stronger Clifford-group theorem should not be confused with the present requirement concerning only two Weyl generators. No novelty is claimed for partial-Fourier monomial bases or mixed-radix factorizations. [Primary paper](https://arxiv.org/pdf/1102.1268).

## Reproducibility and remaining task

`verify_monomial_weyl_batches.py` independently tests the no-log recovery algorithm from supplied sparse actions and one seed, including d=1, composite sizes, odd prime squares, positive characteristic, and deterministic monomial reweightings. It also verifies the explicit three-factor bank family and the sharp N=256 control. Its dense reference matrices are charged research controls, not part of the O(N) recovery algorithm.

The run passes 31 sparse-action recovery cases and seven mixed-radix bank identities. In the N=128 and N=256 cases with a=b=4, it additionally checks all eight nonsingular monomial summands and all four paired-layer factors, with every zero-mask denominator guard equal to 1.

Within the all-four-actions-monomial subclass, finding cheap Green exteriors still means finding cheap arbitrary-input Fourier-batch evaluators. The classification identifies where that work remains; it is not a lower bound on possible Green algorithms. A materially different surviving route can relax monomial actions to genuinely nonmonomial sparse or structured actions, with all extra transport equations and evaluation costs retained.
